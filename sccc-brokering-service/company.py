import logging 

from persistence import get_cursor
from models import Operators

LOGGER = logging.getLogger(__name__)

def get_shares_owned_by_user(symbol: str, username: str):
    with get_cursor() as cursor:
        cursor.execute("""SELECT shares_owned FROM shares_owned_by_user
                    WHERE username = %s AND company_symbol = %s;""",
                (username, symbol))
        shares_owned = cursor.fetchone()

    return shares_owned['shares_owned'] if shares_owned['shares_owned'] is not None else 0

def update_available_shares(symbol: str, change: int, operator: Operators):
    if operator == Operators.INCREMENT:
        LOGGER.debug('Incrementing available shares for %s by %s', symbol, change)
        query = "UPDATE companies SET available_shares = available_shares + %s WHERE symbol = %s;"
    else:
        LOGGER.debug('Decrementing available shares for %s by %s', symbol, change)
        query = "UPDATE companies SET available_shares = available_shares - %s WHERE symbol = %s;"

    with get_cursor() as cursor:
        cursor.execute(query, (change, symbol))
