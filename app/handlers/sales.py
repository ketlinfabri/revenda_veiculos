from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.auth import validar_token_cognito
from app.databases.database import get_db
from app.models.models import Vehicle, PurchaseResponse


router = APIRouter(tags=["Compra de Veículos"])


@router.post(
    "/comprar/{vehicle_id}",
    response_model=PurchaseResponse,
    summary="Comprar um veículo (autenticado)"
)
def buy_vehicle(
    vehicle_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    """
    Compra de veículo requer autenticação.
    """

    try:
        dados = validar_token_cognito(token)
        print("Token válido. Dados:", dados)

        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id, Vehicle.vendido == False).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="Veículo indisponível ou já vendido")

        vehicle.vendido = True
        vehicle.id_comprador = dados['sub']
        db.commit()

        return {
            "mensagem": f"Veículo {vehicle.modelo} comprado com sucesso",
            "veiculo": vehicle.modelo
        }

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erro ao validar token: {e}")



