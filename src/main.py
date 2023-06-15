from uuid import UUID
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from src.models.transaction import Transaction
from src.models.transaction_create import TransactionCreate

app = FastAPI()

TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://db.sqlite3",
    },
    "apps": {
        "models": {
            "models": ["src.models.transaction"],
            "default_connection": "default",
        },
    },
}


@app.on_event("startup")
async def startup():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

register_tortoise(
    app,
    config=TORTOISE_ORM,
)


@app.get("/transactions/{user_id}/{year}/{month}")
async def get_transactions(user_id: str, year: int, month: int):
    return await Transaction.filter(user_id=user_id,
                                    start_date__year=year,
                                    start_date__month=month)


@app.post("/transaction")
async def create_transaction(transaction: TransactionCreate):
    new_transaction = await Transaction.create(**transaction.dict())
    return new_transaction


@app.put("/transaction/{transaction_id}")
async def update_transaction(transaction_id: UUID, transaction: TransactionCreate):
    transaction_db = await Transaction.get(id=transaction_id)
    for key, value in transaction.dict().items():
        setattr(transaction_db, key, value)
    await transaction_db.save()
    return transaction_db


@app.delete("/transaction/{transaction_id}")
async def delete_transaction(transaction_id: UUID):
    transaction = await Transaction.get(id=transaction_id)
    await transaction.delete()
    return {"message": "Transaction deleted"}
