from fastapi import Depends, HTTPException
from jose import jwt
from database import SessionLocal
from models import User
from fastapi.security import HTTPBearer

security = HTTPBearer()
SECRET_KEY = "secret123"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token=Depends(security), db=Depends(get_db)):
    payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
    user = db.query(User).filter(User.id == payload["id"]).first()
    return user