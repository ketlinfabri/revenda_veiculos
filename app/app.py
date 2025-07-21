from fastapi import FastAPI
from app.databases.database import init_db
from app.handlers import vehicles, sales, users, login

app = FastAPI(
    title="Revenda de Veículos",
    description="FIAP - FASE 3 | API para Revenda de Veículos",
    version="1.0.0"
)

init_db()

app.include_router(vehicles.router)
app.include_router(sales.router)
app.include_router(users.router)
app.include_router(login.router)


