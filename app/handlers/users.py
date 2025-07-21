from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.databases.database import SessionLocal
from app.models.models import User
from app.auth.auth import get_password_hash, get_current_user, verify_password, create_access_token

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
    senha: str

    class Config:
        from_attributes = True


@router.post("/usuarios/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    hashed_password = get_password_hash(user.senha)
    new_user = User(nome=user.nome, email=user.email, senha=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

