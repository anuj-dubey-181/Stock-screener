from sqlalchemy.orm import Session

from models import User
from schemas import RegisterSchema
from utils.security import (
    hash_password,
    verify_password,
    create_access_token
)

# ===================================
# REGISTER
# ===================================

def register_user(
    db: Session,
    user: RegisterSchema
):

    existing = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing:

        raise ValueError(
            "Email already registered."
        )

    new_user = User(

        name=user.name,

        email=user.email,

        password_hash=hash_password(
            user.password
        ),

        is_active=True

    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user

# ===================================
# LOGIN
# ===================================

def login_user(
    db: Session,
    email: str,
    password: str
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:

        raise ValueError(
            "Invalid email or password."
        )

    if not verify_password(
        password,
        user.password_hash
    ):

        raise ValueError(
            "Invalid email or password."
        )

    if not user.is_active:

        raise ValueError(
            "User account is inactive."
        )

    token = create_access_token(

        {
            "sub": user.email,
            "user_id": user.id
        }

    )

    return token