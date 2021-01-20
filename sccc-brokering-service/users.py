from persistence import get_cursor
from models import BalanceOperators

def update_balance(change: float, username: str, operator: BalanceOperators):
    with get_cursor() as cursor:
        if operator == BalanceOperators.INCREMENT:
            query = "UPDATE users SET balance = balance + %s WHERE username = %s;"
        else:
            query = "UPDATE users SET balance = balance - %s WHERE username = %s;"
        cursor.execute(query,
            (
                change,
                username
            )
        )