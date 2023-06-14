from enum import Enum
from typing import Optional
from datetime import datetime
from tortoise.models import Model
from pydantic import BaseModel


class TransactionType(int, Enum):
    Expense = 0
    Income = 1


class Transaction(Model):
    id: int
    description: str
    type: TransactionType
    start_date: datetime
    end_date: Optional[datetime] = None
    payment_method: str
    tag: str
    value: float
    user_id: str


class TransactionCreate(BaseModel):
    description: str
    type: TransactionType
    start_date: datetime
    end_date: Optional[datetime]
    payment_method: str
    tag: str
    value: float
    user_id: str
