import logging

from fastapi import FastAPI, HTTPException, Depends, status, Body, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

import zeep
import requests
import uuid
from datetime import datetime, timezone, timedelta

from auth import get_current_user, authenticate_user, create_token
from persistence import get_cursor
from models import Company, Response, Currency, StockQuoteApiResponse, CompanyListing, \
    CompanyDetails, CompanyPriceHistory, User, Transaction, BalanceOperators
from config import DBConfig, CURRENCY_SOAP_URL, STOCK_PRICE_URL, STOCK_PRICE_TOKEN
from prices import (
    get_company_quote, 
    insert_update_price_for_company,
    convert_price_to_currency,
    get_latest_price_for_company
)
from transactions import log_purchase, get_transactions_by_username, log_sale
from users import update_balance

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOGGER = logging.getLogger(__name__)

def _check_company_exists(symbol: str = Path(...)) -> Company:
    with get_cursor() as cursor:
        cursor.execute("""SELECT symbol, name, available_shares, last_update FROM companies 
                        WHERE symbol = %s""", (symbol,))
        if (company := cursor.fetchone()) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Company not found.')
    return Company(**company)

@app.get("/")
def health_check():
    return {'check': 'ok'}

@app.post("/login", dependencies=[Depends(get_current_user)])
async def check_token():
    return {'authenticated': True}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """ Login a user and return a token if correct """
    if (user := authenticate_user(username=form_data.username, password=form_data.password)) is None:
        LOGGER.debug("User auth failed for %s", form_data.username)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized.")
    access_token = create_token(username=user.username)
    LOGGER.info("Token generated for user %s", form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/companies", response_model=Response[List[CompanyListing]], dependencies=[Depends(get_current_user)])
def get_companies():
    with get_cursor() as cursor:
        cursor.execute("""SELECT symbol, name, available_shares, last_update,
                (SELECT price FROM prices
                    WHERE company_symbol = symbol
                    ORDER BY timestamp DESC
                    LIMIT 1
                ) AS last_price,
                (SELECT currency FROM prices
                    WHERE company_symbol = symbol
                    ORDER BY timestamp DESC
                    LIMIT 1
                )
                FROM companies
                ORDER BY symbol;""")
        companies = cursor.fetchall()

    return {"data": [CompanyListing(**c) for c in companies]}

@app.get("/companies/{symbol}", response_model=Response[CompanyDetails])
def get_prices_for_company(
    company: Company = Depends(_check_company_exists),
    user: User = Depends(get_current_user)
):
    with get_cursor() as cursor:
        cursor.execute("""SELECT shares_owned FROM shares_owned_by_user
                          WHERE username = %s AND company_symbol = %s;""",
                        (user.username, company.symbol)
                    )
        shares_owned = cursor.fetchone()
    return {"data": {
            **get_company_quote(company.symbol).dict(), 
            'available_shares': company.available_shares,
            'shares_owned': shares_owned['shares_owned']
        }
    }

@app.get("/companies/{symbol}/history")
def get_price_history_for_company(symbol: str):
    with get_cursor() as cursor:
        cursor.execute("""SELECT price, currency, timestamp FROM prices 
                        WHERE company_symbol = %s 
                        ORDER BY timestamp DESC""", (symbol,)
                    )
        prices = cursor.fetchall()
    return {"data": [CompanyPriceHistory(**history) for history in prices]}

@app.patch("/companies/{symbol}/update-prices", dependencies=[Depends(get_current_user)], status_code=status.HTTP_204_NO_CONTENT)
def update_price_for_company(symbol: str, currency: str = Body('GBP')):
    with get_cursor() as cursor:
        cursor.execute("SELECT timestamp FROM prices ORDER BY timestamp DESC LIMIT 1;")
        row = cursor.fetchone()
        time_delta = datetime.now(tz=timezone.utc) - row['timestamp'] if row is not None else None
        if time_delta is not None and time_delta.total_seconds() <= timedelta(minutes=10).total_seconds():
            LOGGER.debug('Update too soon %s seconds difference', time_delta.total_seconds())
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Requesting update too soon.')

    insert_update_price_for_company(symbol, currency)
    return {}

@app.post("/companies/{symbol}/sell",
    status_code=status.HTTP_201_CREATED
)
def sell_shares(
    company: Company = Depends(_check_company_exists),
    amount_of_shares: int = Body(..., embed=True),
    currency: str = Body(..., embed=True),
    user: User = Depends(get_current_user)
):
    with get_cursor() as cursor:
        cursor.execute("""SELECT shares_owned FROM shares_owned_by_user
                          WHERE username = %s AND company_symbol = %s;""",
                        (user.username, company.symbol))
        total_shares_owned = cursor.fetchone()
    
    if amount_of_shares >= total_shares_owned:
        LOGGER.info('Requested to sell more shares than owned.')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Too many shares.')
    price_of_sale = get_latest_price_for_company(symbol=company.symbol)
    total = price_of_sale * amount_of_shares

    with get_cursor() as cursor:
        cursor.execute("""INSERT INTO shares_owned_by_user (company_symbol, username, shares_owned)
                    VALUES(%s, %s, %s)
                    ON CONFLICT (company_symbol, username)
                    DO UPDATE
                    SET shares_owned = shares_owned_by_user.shares_owned - EXCLUDED.shares_owned""", 
                (company.symbol, user.username, amount_of_shares)
            )
        remaining_shares = company.available_shares - amount_of_shares
        cursor.execute("UPDATE companies SET available_shares = %s WHERE symbol = %s;", (remaining_shares, company.symbol))

    update_balance(change=total, username=user.username, operator=BalanceOperators.INCREMENT)
    LOGGER.info('Balance updated for %s', user.username)

    transaction_id = log_sale(
        company_symbol=company.symbol,
        username=user.username,
        amount=total,
        total_shares=amount_of_shares,
        currency=currency
    )

    insert_update_price_for_company(symbol=company.symbol, currency=currency)

    return {"transaction_id": transaction_id}
 

@app.post("/companies/{symbol}/purchase", 
    status_code=status.HTTP_201_CREATED,
    response_model=dict
)
def purchase_shares(
    company: Company = Depends(_check_company_exists), 
    amount_of_shares: int = Body(..., embed=True),  
    currency: str = Body(..., embed=True), 
    user: User = Depends(get_current_user)
):
    if amount_of_shares > company.available_shares:
        LOGGER.info('Requested to purchase too many shares')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not enough shares available.')

    price = next(get_latest_price_for_company(symbol=company.symbol), None)
    if price is None:
        LOGGER.info('Existing price not found, gathering price data for purchase.') 
        insert_update_price_for_company(symbol=company.symbol, currency=currency)
        price = get_latest_price_for_company(symbol=company.symbol)

    with get_cursor() as cursor:
        converted_price = convert_price_to_currency(price['price'], currency_from='GBP', currency_to=currency)
        total = converted_price * amount_of_shares
        cursor.execute("""INSERT INTO shares_owned_by_user (company_symbol, username, shares_owned)
                           VALUES(%s, %s, %s)
                           ON CONFLICT (company_symbol, username)
                           DO UPDATE
                           SET shares_owned = shares_owned_by_user.shares_owned + EXCLUDED.shares_owned""", 
                        (company.symbol, user.username, amount_of_shares)
                    )
        LOGGER.info('Updated users shares: %s', user.username)
        remaining_shares = company.available_shares - amount_of_shares
        cursor.execute("UPDATE companies SET available_shares = %s WHERE symbol = %s;", (remaining_shares, company.symbol))

    update_balance(change=total, username=user.username, operator=BalanceOperators.DECREMENT)
    LOGGER.info('Balance updated for username %s', user.username)

    transaction_id = log_purchase(
        company_symbol=company.symbol,
        username=user.username,
        amount=total,
        total_shares=amount_of_shares,
        currency=currency
    )

    insert_update_price_for_company(symbol=company.symbol)
    return {"transaction_id": transaction_id}

@app.get('/transactions', response_model=Response[List[Transaction]])
def get_transaction_history(user: User = Depends(get_current_user)):
    return {'data': get_transactions_by_username(user.username)}


@app.get('/currencies', response_model=Response[List[Currency]], dependencies=[Depends(get_current_user)])
def get_currencies():
    client = zeep.Client(wsdl=CURRENCY_SOAP_URL)
    currencies = client.service.GetCurrencyCodes()
    return {"data": [Currency(name=c['name'], code=c['code']) for c in currencies]}
