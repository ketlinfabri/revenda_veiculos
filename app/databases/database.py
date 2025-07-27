import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.models.models import Base, Vehicle

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db():
    #Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(Vehicle).count() == 0:
            vehicles = [
                Vehicle(
                    marca="Ford",
                    modelo="Ka",
                    ano=2019,
                    cor="Prata",
                    preco=28000.00,
                    placa="ABC1234",
                    renavan="12345678901",
                    chassi="9BWZZZ377VT004251",
                    vendido=False
                ),
                Vehicle(
                    marca="Chevrolet",
                    modelo="Onix",
                    ano=2020,
                    cor="Branco",
                    preco=35000.00,
                    placa="XYZ9876",
                    renavan="98765432100",
                    chassi="9BWZZZ377VT004252",
                    vendido=False
                )
            ]
            db.add_all(vehicles)
        db.commit()
    finally:
        db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()