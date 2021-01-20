import uuid
from datetime import datetime, timezone

from persistence import get_cursor
from models import Transaction, TransactionTypes

def get_transactions_by_username(username: str):
    with get_cursor() as cursor:
        cursor.execute("""
            SELECT transaction_id, symbol, username,
            transaction_type, transaction_at, amount,
            total, currency
            FROM transactions
            WHERE username = %s;
        """, (username,))
        yield from cursor.fetchall()

def _log_transaction(transaction: Transaction) -> uuid.UUID:
    """ Main function for inserting a transation """
    timestamp = datetime.now(tz=timezone.utc).isoformat()
    with get_cursor() as cursor:
        cursor.execute("""
            INSERT INTO transactions
            (
                transaction_id, symbol, username,
                transaction_type, transaction_at, currency,
                amount, total
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                transaction.transaction_id,
                transaction.symbol,
                transaction.username,
                transaction.transaction_type,
                timestamp,
                transaction.currency,
                transaction.amount,
                transaction.total
            )
        )
    return transaction.transaction_id
 
def log_sale(
    company_symbol: str, 
    username: str, 
    amount: float, 
    total_shares: int, 
    currency: str
):
    """ Insert transaction entry for a share purchase. """
    transaction_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc)
    transaction = Transaction(
        transaction_id=transaction_id,
        symbol=company_symbol,
        username=username,
        transaction_type=TransactionTypes.SELL,
        transaction_at=timestamp,
        amount=amount,
        total=total_shares,
        currency=currency
    )
    return _log_transaction(transaction)

def log_purchase(
    company_symbol: str, 
    username: str, 
    amount: float, 
    total_shares: int, 
    currency: str
) -> uuid.UUID:
    """ Insert transaction entry for a share purchase. """
    transaction_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc)
    transaction = Transaction(
        transaction_id=transaction_id,
        symbol=company_symbol,
        username=username,
        transaction_type=TransactionTypes.BUY,
        transaction_at=timestamp,
        amount=amount,
        total=total_shares,
        currency=currency
    )
    return _log_transaction(transaction)
