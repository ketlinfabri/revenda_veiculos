from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String)
    modelo = Column(String)
    ano = Column(Integer)
    cor = Column(String)
    preco = Column(Float)
    vendido = Column(Boolean, default=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
