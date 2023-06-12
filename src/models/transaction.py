from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class TransactionType(str, Enum):
    Expense = "Expense"
    Income = "Income"


class Transaction(BaseModel):
    id: int
    description: str
    type: TransactionType
    start_date: datetime
    end_date: Optional[datetime] = None
    payment_method: str
    tag: str
    value: float
    user_id: str
