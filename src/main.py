from uuid import UUID
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise import Tortoise, functions
from tortoise.contrib.fastapi import register_tortoise
from src.models.transaction import Transaction
from src.models.transaction_create import TransactionCreate

app = FastAPI()

# CORS Configuration
origins = [
    "http://127.0.0.1:5173",
    "http://localhost:*",
    "http://localhost:5173",
    # Add other allowed origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

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


@app.get("/transactions/{user_id}")
async def get_transactions(user_id: str, year: int, month: int):
    year_month = f"{year}-{month:02}"
    return await Transaction.filter(
        user_id=user_id,
        start_date__startswith=year_month,
    )


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
