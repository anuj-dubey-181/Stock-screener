from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    RegisterSchema,
    LoginSchema,
    Token,
    UserResponse
)
from services.auth_service import (
    register_user,
    login_user
)
from utils.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ==========================================
# REGISTER
# ==========================================

@router.post("/register")
def register(
    user: RegisterSchema,
    db: Session = Depends(get_db)
):

    try:

        new_user = register_user(db, user)

        return {

            "success": True,

            "message": "User registered successfully.",

            "data": UserResponse.model_validate(new_user)

        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# ==========================================
# LOGIN
# ==========================================

@router.post(
    "/login",
    response_model=Token
)
def login(
    user: LoginSchema,
    db: Session = Depends(get_db)
):

    try:

        token = login_user(
            db,
            user.email,
            user.password
        )

        return {

            "access_token": token,

            "token_type": "bearer"

        }

    except ValueError as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )


# ==========================================
# CURRENT USER
# ==========================================

@router.get(
    "/me",
    response_model=UserResponse
)
def me(
    current_user=Depends(get_current_user)
):

    return current_user