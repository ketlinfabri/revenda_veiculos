from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.databases.database import SessionLocal
from app.models.models import Vehicle
from pydantic import BaseModel, Field

router = APIRouter(tags=["Veículos"])


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


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    preco: float = Field(None)
    vendido: bool = Field(None)


class VehicleResponse(VehicleBase):
    id: int

    class Config:
        from_attributes = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/veiculos/", response_model=VehicleResponse, summary="Cadastrar veículo")
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    """
    Cadastrar um veículo para venda.
    * Marca, Modelo, Chassi e Renavan sâo campos obrigatórios.
    """
    db_vehicle = Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


@router.put("/veiculos/{vehicle_id}", response_model=VehicleResponse, summary="Editar dados veículo")
def update_vehicle(vehicle_id: int, vehicle: VehicleUpdate, db: Session = Depends(get_db)):
    """
    Editar os dados do veículo.
    """
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    for key, value in vehicle.dict(exclude_unset=True).items():
        setattr(db_vehicle, key, value)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


@router.get("/veiculos/disponiveis", response_model=List[VehicleResponse], summary="Listar veículos disponíveis")
def list_available_vehicles(db: Session = Depends(get_db)):
    """
    Listagem de veículos à venda, ordenada por preço, do mais barato para o mais caro.
    """
    return db.query(Vehicle).filter(Vehicle.vendido == False).order_by(Vehicle.preco.asc()).all()


@router.get("/veiculos/vendidos", response_model=List[VehicleResponse], summary="Listar veículos vendidos")
def list_sold_vehicles(db: Session = Depends(get_db)):
    """
    Listagem de veículos vendidos, ordenada por preço, do mais barato para o mais caro.
    """
    return db.query(Vehicle).filter(Vehicle.vendido == True).order_by(Vehicle.preco.asc()).all()
