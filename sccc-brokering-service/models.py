from datetime import datetime
from typing import TypeVar, Optional, Generic

from pydantic import BaseModel
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')

class Response(GenericModel, Generic[DataT]):
    data: Optional[DataT]

class Company(BaseModel):
    symbol: str
    name: str
    available_shares: int
    last_update: datetime

class StockQuoteApiResponse(BaseModel):
    """ Model to represent the relevant data from the broker API """
    symbol: str
    description: str
    last: float
    change: float
    change_percentage: float

class Currency(BaseModel):
    name: str
    code: str

class BaseUser(BaseModel):
    username: str

class User(BaseUser):
    password: str