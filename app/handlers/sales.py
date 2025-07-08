from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.databases.database import SessionLocal
from app.models.models import Vehicle, User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/comprar/{vehicle_id}")
def buy_vehicle(vehicle_id: int, user_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id, Vehicle.vendido == False).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Veículo indisponível")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=403, detail="Usuário não autorizado")

    vehicle.vendido = True
    db.commit()
    return {"mensagem": "Compra realizada com sucesso", "veiculo": vehicle.modelo}
