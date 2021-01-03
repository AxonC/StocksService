import logging

from fastapi import FastAPI, HTTPException, Depends, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

import zeep
import requests

from auth import get_current_user, authenticate_user, create_token
from persistence import get_cursor
from models import Company, Response, Currency, StockQuoteApiResponse
from config import DBConfig, CURRENCY_SOAP_URL, STOCK_PRICE_URL, STOCK_PRICE_TOKEN
from prices import get_company_quote

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOGGER = logging.getLogger(__name__)

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


@app.get("/companies", response_model=Response[List[Company]], dependencies=[Depends(get_current_user)])
def get_companies():
    with get_cursor() as cursor:
        cursor.execute("SELECT symbol, name, available_shares, last_update FROM companies;")
        companies = cursor.fetchall()
    return {"data": [Company(**c) for c in companies]}


@app.get("/companies/{symbol}", response_model=Response[StockQuoteApiResponse], dependencies=[Depends(get_current_user)])
def get_prices_for_company(symbol: str):
    with get_cursor() as cursor:
        cursor.execute("SELECT symbol, name FROM companies;")
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail='Company not found.')
    return {"data": get_company_quote(symbol)}


@app.get('/currencies', response_model=Response[List[Currency]], dependencies=[Depends(get_current_user)])
def get_currencies():
    client = zeep.Client(wsdl=CURRENCY_SOAP_URL)
    currencies = client.service.GetCurrencyCodes()
    return {"data": [Currency(name=c['name'], code=c['code']) for c in currencies]}

