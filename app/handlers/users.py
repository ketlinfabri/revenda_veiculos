from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.databases.database import SessionLocal
from app.models.models import User

router = APIRouter(tags=["Usuários"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    nome: str = Field(..., example="João da Silva")
    email: str = Field(..., example="joao@email.com")
    senha: str = Field(..., min_length=6, example="senha123")


class UserResponse(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        from_attributes = True


@router.post(
    "/usuarios/",
    response_model=UserResponse,
    summary="Registrar novo usuário",
    response_description="Usuário criado com sucesso"
)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário no sistema.

    - **nome**: Nome completo do usuário
    - **email**: Endereço de e-mail (deve ser único)
    - **senha**: Senha de acesso (mínimo 6 caracteres)
    """
    # Verifica se email já está cadastrado
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
