import csv
from uuid import UUID
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI, UploadFile, File
from datetime import datetime
from src.models.transaction import Transaction, TransactionType
from src.models.transaction_create import TransactionCreate

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:*",
    "http://localhost:5173",
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


@app.post("/transactions/csv")
async def create_transactions_from_csv(file: UploadFile = File(...)):
    try:
        transactions = []

        contents = await file.read()
        decoded_content = contents.decode("utf-8")
        reader = csv.reader(decoded_content.splitlines(), delimiter=";")
        next(reader)

        for row in reader:
            try:
                date_str, establishment, _, value_str, _ = row
                value = float(value_str.replace("R$", "").replace(",", "."))

                date = datetime.strptime(date_str, "%d/%m/%Y")
                formatted_date = date.date().isoformat()

                transaction = TransactionCreate(
                    description=establishment,
                    type=TransactionType.Expense,
                    start_date=formatted_date,
                    payment_method="fatura xp",
                    tag="",
                    value=value,
                    user_id="string",
                )

                created_transaction = await Transaction.create(**transaction.dict())
                transactions.append(created_transaction)
            except Exception as e:
                print(f"Error processing row: {row}. Error: {str(e)}")

        return {"message": "Transactions created", "transactions": transactions}
    except Exception as e:
        print(f"Error creating transactions: {str(e)}")
        return {"message": "Error creating transactions"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
