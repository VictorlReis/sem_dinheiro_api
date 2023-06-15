from datetime import datetime
from pydantic import BaseModel, validator
from src.models.transaction import TransactionType


class TransactionCreate(BaseModel):
    description: str
    type: TransactionType
    start_date: str
    payment_method: str
    tag: str
    value: float
    user_id: str

    @validator('start_date')
    def validate_start_date(cls, value):
        try:
            date = datetime.strptime(value, "%Y-%m-%d")
            return date.date().isoformat()
        except ValueError:
            raise ValueError('Invalid date format')
