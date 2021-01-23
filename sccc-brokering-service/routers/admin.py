import logging
from datetime import datetime, timezone
from fastapi import APIRouter, status, HTTPException, Body, Response

from persistence import get_cursor
from models import BaseCompany
from prices import insert_update_price_for_company

from psycopg2.errors import UniqueViolation

router = APIRouter()

LOGGER = logging.getLogger(__name__)

@router.post('/companies', status_code=status.HTTP_201_CREATED)
def create_company(company: BaseCompany, currency: str = Body(..., embed=True)):
    """ Create a new company in the database and create initial price """
    timestamp = datetime.now(tz=timezone.utc).isoformat()
    with get_cursor() as cursor:
        LOGGER.debug('Inserting company with symbol %s into database', company.symbol)
        try:
            cursor.execute("""INSERT INTO companies (symbol, name, available_shares, last_update)
                VALUES (%s, %s, %s, %s);""", (company.symbol, company.name, company.available_shares, timestamp)
            )
        except UniqueViolation as exc:
            LOGGER.warning('Company with symbol already created requested.')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Company not found') from exc
    insert_update_price_for_company(company.symbol, currency=currency)

    return {'message': 'Created'}

@router.patch('/companies/{symbol}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def modify_company(symbol: str, available_shares: int = Body(..., embed=True)):
    with get_cursor() as cursor:
        LOGGER.debug('Modifying shares of company')
        cursor.execute("UPDATE companies SET available_shares = %s WHERE symbol = %s", (available_shares, symbol))
