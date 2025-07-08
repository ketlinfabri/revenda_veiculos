from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.databases.database import SessionLocal
from app.models.models import Vehicle

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/veiculos/")
def create_vehicle(vehicle: dict, db: Session = Depends(get_db)):
    db_vehicle = Vehicle(**vehicle)
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


@router.put("/veiculos/{vehicle_id}")
def update_vehicle(vehicle_id: int, vehicle: dict, db: Session = Depends(get_db)):
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    for key, value in vehicle.items():
        setattr(db_vehicle, key, value)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


@router.get("/veiculos/disponiveis")
def list_available_vehicles(db: Session = Depends(get_db)):
    return db.query(Vehicle).filter(Vehicle.vendido == False).order_by(Vehicle.preco.asc()).all()


@router.get("/veiculos/vendidos")
def list_sold_vehicles(db: Session = Depends(get_db)):
    return db.query(Vehicle).filter(Vehicle.vendido == True).order_by(Vehicle.preco.asc()).all()
