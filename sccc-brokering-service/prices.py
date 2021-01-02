import logging
import requests
import zeep

from config import STOCK_PRICE_TOKEN, STOCK_PRICE_URL, CURRENCY_SOAP_URL
from models import StockQuoteApiResponse

LOGGER = logging.getLogger(__name__)
SOAP_CLIENT = zeep.Client(wsdl=CURRENCY_SOAP_URL)

def get_company_quote(symbol: str) -> StockQuoteApiResponse:
    """ Use the broker API to get the relevant information for a given company """
    data = requests.get(f"{STOCK_PRICE_URL}/markets/quotes",
        params={"symbols": symbol},
        headers={"Authorization": f"Bearer {STOCK_PRICE_TOKEN}", "Accept": "application/json"}
    )

    return StockQuoteApiResponse(**data.json()["quotes"]["quote"])

def convert_price_to_currency(price: float, currency_from: str, currency_to: str) -> float:
    """ Convert a given price from a currency to another """
    divisor = SOAP_CLIENT.service.GetConversionRate(currency_from, currency_to)
    return price / divisor
