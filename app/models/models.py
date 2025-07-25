from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base

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
    id_comprador = Column(String, nullable=True)


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
    id_comprador: str


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    preco: float = Field(None)
    vendido: bool = Field(None)
    id_comprador: str = Field(None)


class VehicleResponse(VehicleBase):
    id: int

    class Config:
        from_attributes = True


class PurchaseResponse(BaseModel):
    mensagem: str
    veiculo: str