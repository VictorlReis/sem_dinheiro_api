import datetime
import os
import json
from pynubank import Nubank, MockHttpClient
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

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


def date_in_month_and_year(data_str, month, year):
    data = datetime.datetime.fromisoformat(data_str)
    return data.month == month and data.year == year


@app.get("/nubank/get_transactions_mock")
async def get_nubank_transactions_mock(year: int, month: int):
    dados_json = """
    """

    dados_python = json.loads(dados_json)

    dados_transformados = []

    for dado in dados_python:
        novo_dado = {
            "description": dado["description"] or "no description",
            "type": "expense",
            "date": dado["time"] or datetime.datetime.now(),
            "amount": dado["amount"] or 0,
            "category": dado["title"] or "no title",
        }
        dados_transformados.append(novo_dado)

    return {"transactions": dados_transformados}


@app.get("/nubank/get_transactions")
async def get_nubank_transactions(year: int, month: int):
    cert_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'cert.p12'))

    # nu = Nubank(MockHttpClient())
    nu = Nubank()
    nu.authenticate_with_cert(
        '', '', cert_path)

    transactions = nu.get_card_statements()

    # Filtrar os dados com base na data
    monthly_transactions = [transaction for transaction in transactions if date_in_month_and_year(
        transaction['time'], month, year)]

    filtered_data = []

    for dado in monthly_transactions:
        new_data = {
            "description": dado["description"] or "no description",
            "type": "expense",
            "date": dado["time"] or datetime.datetime.now(),
            "amount": dado["amount"] or 0,
            "category": dado["title"] or "no title",
        }
        filtered_data.append(new_data)

    return {"transactions": filtered_data}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
