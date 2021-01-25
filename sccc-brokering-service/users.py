import logging 
from persistence import get_cursor
from models import Operators

LOGGER = logging.getLogger(__name__)

def update_balance(change: float, username: str, operator: Operators):
    with get_cursor() as cursor:
        LOGGER.debug('Requested to change balance of %s by %s', username, change)
        if operator == Operators.INCREMENT:
            LOGGER.debug('Incrementing balance')
            query = "UPDATE users SET balance = balance + %s WHERE username = %s;"
        else:
            LOGGER.debug('Decrementing balance for %s by %s', username, change)
            query = "UPDATE users SET balance = balance - %s WHERE username = %s;"
        cursor.execute(query,
            (
                change,
                username
            )
        )

def update_shares_owned(change: int, username: str, symbol: str, operator: Operators):
    if operator == Operators.INCREMENT:
        LOGGER.debug('Allocating %s shares to %s for symbol %s', change, username, symbol)
        query = """INSERT INTO shares_owned_by_user (company_symbol, username, shares_owned)
                           VALUES(%s, %s, %s)
                           ON CONFLICT (company_symbol, username)
                           DO UPDATE
                           SET shares_owned = shares_owned_by_user.shares_owned + EXCLUDED.shares_owned"""
    else:
        LOGGER.debug('Deallocating %s shares to %s for symbol %s', change, username, symbol)
        query = """INSERT INTO shares_owned_by_user (company_symbol, username, shares_owned)
                    VALUES(%s, %s, %s)
                    ON CONFLICT (company_symbol, username)
                    DO UPDATE
                    SET shares_owned = shares_owned_by_user.shares_owned - EXCLUDED.shares_owned"""
    with get_cursor() as cursor:
        cursor.execute(query, (symbol, username, change))

def get_shares_portfolio(username: str):
    with get_cursor() as cursor:
        LOGGER.debug('Getting shares owned for %s', username)
        query = """SELECT company_symbol, shares_owned FROM shares_owned_by_user
                WHERE username = %s
                ORDER BY company_symbol;"""
        cursor.execute(query, (username,))
        return cursor.fetchall()
