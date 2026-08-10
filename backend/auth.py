from jose import jwt
from passlib.context import CryptContext

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "JWT_SECRET_KEY is not configured."
    )

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")


def hash_password(password:str):
    print("Debug pass:",repr(password))
    print("Debug bytes:",len(password.encode("utf-8")))

    return pwd_context.hash(password)


def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)


def create_token(data):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
