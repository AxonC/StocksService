from datetime import datetime
from typing import TypeVar, Optional, Generic, List

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

from enum import Enum, IntEnum

DataT = TypeVar('DataT')

class Response(GenericModel, Generic[DataT]):
    data: Optional[DataT]

class BaseCompany(BaseModel):
    symbol: str
    name: str
    available_shares: int

class Company(BaseCompany):
    last_update: datetime

class CompanyListing(Company):
    last_price: float = Field(None)
    currency: str = Field(None)

class StockQuoteApiResponse(BaseModel):
    """ Model to represent the relevant data from the broker API """
    symbol: str
    description: str
    last: float
    change: float
    change_percentage: float

class TransactionTypes(IntEnum):
    BUY = 1
    SELL = 2

class Operators(Enum):
    INCREMENT = "+"
    DECREMENT = "-"

class Transaction(BaseModel):
    transaction_id: str
    symbol: str
    username: str
    transaction_type: TransactionTypes
    transaction_at: datetime
    amount: float
    total: float
    currency: str

class CompanyDetails(StockQuoteApiResponse):
    available_shares: int
    shares_owned: int = Field(0)

class CompanyPriceHistory(BaseModel):
    price: float
    currency: str
    timestamp: datetime

class Currency(BaseModel):
    name: str
    code: str

class BaseUser(BaseModel):
    username: str

class User(BaseUser):
    password: str
    balance: int

class SharesOwned(BaseModel):
    company_symbol: str
    shares_owned: int

class UserWithPortfolio(User):
    portfolio: List[SharesOwned]
