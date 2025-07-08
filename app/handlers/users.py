from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.databases.database import SessionLocal
from app.models.models import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/usuarios/")
def register_user(user: dict, db: Session = Depends(get_db)):
    new_user = User(**user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
