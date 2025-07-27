import enum
from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    ano = Column(Integer)
    cor = Column(String)
    preco = Column(Float)
    placa = Column(String)
    renavan = Column(String, nullable=False)
    chassi = Column(String, nullable=False, unique=True)
    vendido = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class VehicleBase(BaseModel):
    marca: str = Field(..., min_length=1, description="Marca não pode ser nulo ou vazio")
    modelo: str = Field(..., min_length=1, description="Modelo não pode ser nulo ou vazio")
    ano: int
    preco: float
    cor: str
    placa: str
    renavan: str = Field(..., min_length=11, description="Renavan não pode ser nulo ou vazio")
    chassi: str = Field(..., min_length=17, description="Chassi não pode ser nulo ou vazio")
    vendido: bool = False
    created_at: datetime
    updated_at: datetime


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    preco: float = Field(None)
    marca: str = Field(..., min_length=1, description="Marca não pode ser nulo ou vazio")
    modelo: str = Field(..., min_length=1, description="Modelo não pode ser nulo ou vazio")
    ano: int
    preco: float
    cor: str
    placa: str


class VehicleResponse(VehicleBase):
    id: int

    class Config:
        from_attributes = True


class TipoPagamentoEnum(enum.Enum):
    CARTAO = "cartao"
    BOLETO = "boleto"
    PIX = "pix"


class Purchase(Base):
    __tablename__ = "purchase"

    id = Column(Integer, primary_key=True, index=True)
    id_veiculo = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    id_comprador = Column(String, nullable=False)
    tipo_pagamento = Column(Enum(TipoPagamentoEnum), nullable=False)
    dt_compra = Column(DateTime, default=datetime.utcnow, nullable=False)


class PurchaseBase(BaseModel):
    id_veiculo: int
    id_comprador: str
    tipo_pagamento: TipoPagamentoEnum


class PurchaseResponse(BaseModel):
    id_comprador: str
    veiculo: str
    tipo_pagamento: str

    class Config:
        from_attributes = True

