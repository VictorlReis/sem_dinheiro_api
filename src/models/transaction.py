import uuid
from enum import IntEnum
from tortoise import fields
from tortoise.models import Model


class TransactionType(IntEnum):
    Expense = 0
    Income = 1


class Transaction(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    description = fields.CharField(max_length=255)
    type = fields.IntEnumField(TransactionType)
    start_date = fields.DatetimeField()
    payment_method = fields.CharField(max_length=255)
    tag = fields.CharField(max_length=255)
    value = fields.FloatField()
    user_id = fields.CharField(max_length=255)

    def get_type(self) -> TransactionType:
        return TransactionType(self.type)

    def set_type(self, value: TransactionType):
        self.type = value.value
