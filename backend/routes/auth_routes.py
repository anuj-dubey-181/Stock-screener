from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import RegisterSchema, LoginSchema
from auth import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth")


def get_db():
    db = SessionLocal()
    yield db
    db.close()


@router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    user = User(email=data.email, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    return {"message": "User created"}


@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not verify_password(data.password, user.password_hash):
        return {"error": "Invalid credentials"}

    token = create_token({"id": user.id})

    return {"access_token": token}
