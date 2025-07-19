from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.models import Vehicle, User
from app.auth.auth import get_current_user, get_db
from pydantic import BaseModel

router = APIRouter(tags=["Compra de Veículos"])


class PurchaseResponse(BaseModel):
    mensagem: str
    veiculo: str

@router.post(
    "/comprar/{vehicle_id}",
    response_model=PurchaseResponse,
    summary="Comprar um veículo (autenticado)"
)
def buy_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    token: User = Depends(get_current_user)
):
    """
    Compra de veículo. Requer autenticação via JWT.
    """
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id, Vehicle.vendido == False).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Veículo indisponível ou já vendido")

    vehicle.vendido = True
    db.commit()

    return {
        "mensagem": f"Veículo '{vehicle.modelo}' comprado com sucesso",
        "veiculo": vehicle.modelo
    }
