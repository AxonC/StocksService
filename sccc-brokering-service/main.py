from fastapi import FastAPI
from contextlib import contextmanager
from typing import List

import psycopg2
from psycopg2.extras import DictCursor
import zeep

from .models import Company, Response, Currency
from .config import DBConfig, CURRENCY_SOAP_URL

app = FastAPI()

@contextmanager
def get_cursor():
    connection = psycopg2.connect(
        database=DBConfig.NAME,
        user=DBConfig.USERNAME,
        password=DBConfig.PASSWORD,
        host=DBConfig.ADDRESS
    )

    with connection:
        connection.autocommit = True
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            yield cursor

    connection.close()

@app.get("/")
def health_check():
    return {'check': 'ok'}

@app.get("/companies", response_model=Response[List[Company]])
def get_companies():
    with get_cursor() as cursor:
        cursor.execute("SELECT symbol, name, available_shares, last_update FROM companies;")
        companies = cursor.fetchall()
    return {"data": [Company(**c) for c in companies]}

@app.get('/currencies')
def get_currencies():
    client = zeep.Client(wsdl=CURRENCY_SOAP_URL)
    currencies = client.service.GetCurrencyCodes()
    return {"data": [Currency(name=c['name'], code=c['code']) for c in currencies]}

