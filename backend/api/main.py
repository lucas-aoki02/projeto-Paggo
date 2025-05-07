from fastapi import FastAPI, Query
from datetime import datetime
from typing import List

from backend.models.fonte import init_db
from backend.crud import get_data_by_date
from backend.config import settings # Importe as configurações
from backend.database import DATABASE_URL_FONTE # Importe a variável diretamente

app = FastAPI()

# Inicializa o banco ao iniciar o servidor
@app.on_event("startup")
async def startup_event():
    init_db()
    print(f"DATABASE_URL_FONTE em main.py (startup): {DATABASE_URL_FONTE}") # ADICIONE ESTA LINHA

@app.get("/data/")
def read_data(start_date: str, end_date: str, variables: List[str] = Query(None)):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DDTHH:MM:SS"}

    data = get_data_by_date(start, end, variables)
    return {"data": data}

@app.get("/")
def root():
    return {"message": "API Fonte is running. Use /data/ to query data."}