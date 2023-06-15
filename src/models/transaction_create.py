from datetime import datetime
from pydantic import BaseModel
from src.models.transaction import TransactionType


class TransactionCreate(BaseModel):
    description: str
    type: TransactionType
    start_date: datetime
    payment_method: str
    tag: str
    value: float
    user_id: str
