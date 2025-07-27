from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.auth import validar_token_cognito
from app.databases.database import get_db
from app.models.models import Vehicle, PurchaseResponse, Purchase, TipoPagamentoEnum

router = APIRouter(tags=["Compra de Veículos"])


@router.post(
    "/comprar/{id_veiculo}",
    response_model=PurchaseResponse,
    summary="Comprar um veículo (autenticado)"
)
def buy_vehicle(
    vehicle_id: int,
    token: str = Query(description="Authorization: Bearer"),
    tp_pagamento: TipoPagamentoEnum = Query(description="Tipo Pagamento"),
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

        purchase = db.query(Purchase)

        purchase.id_comprador = dados['sub']
        purchase.id_veiculo = vehicle.id
        purchase.tipo_pagamento = tp_pagamento

        db.commit()

        return {
            "id_comprador": dados['sub'],
            "veiculo": f"{vehicle.marca} {vehicle.modelo}, vendido por R${vehicle.preco} reais",
            "tipo_pagamento": tp_pagamento.value
        }

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erro ao validar token: {e}")



