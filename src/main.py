from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from src.models.transaction import Transaction
from src.models.transaction import TransactionCreate

app = FastAPI()

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['src.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.get("/transactions/{user_id}/{year}/{month}")
async def get_transactions(user_id: str, year: int, month: int):
    return await Transaction.filter(user_id=user_id, start_date__year=year, start_date__month=month)


@app.post("/transaction")
async def create_transaction(transaction: TransactionCreate):
    new_transaction = await Transaction.create(**transaction.dict())
    return new_transaction


@app.put("/transaction/{transaction_id}")
async def update_transaction(transaction_id: int, transaction: TransactionCreate):
    transaction_db = await Transaction.get(id=transaction_id)
    for key, value in transaction.dict().items():
        setattr(transaction_db, key, value)
    await transaction_db.save()
    return transaction_db


@app.delete("/transaction/{transaction_id}")
async def delete_transaction(transaction_id: int):
    transaction = await Transaction.get(id=transaction_id)
    await transaction.delete()
    return {"message": "Transaction deleted"}
