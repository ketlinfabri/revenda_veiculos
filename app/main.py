from fastapi import FastAPI
from app.databases import database as db
from app.handlers import vehicles, sales

app = FastAPI(
    title="Revenda de Veículos",
    description="FIAP - FASE 3 | API para Revenda de Veículos",
    version="1.0.0"
)

db.init_db()

app.include_router(vehicles.router)
app.include_router(sales.router)



