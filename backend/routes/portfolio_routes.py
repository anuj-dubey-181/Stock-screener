from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from utils.dependencies import get_current_user

from schemas import (
    PortfolioTransactionRequest,
)

from services.portfolio_service import (
    buy_stock,
    sell_stock,
    get_portfolio,
    get_transaction_history,
)

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"],
)

@router.post("/buy")
def buy(
    request: PortfolioTransactionRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return buy_stock(
        db=db,
        user_id=current_user.id,
        symbol=request.symbol,
        quantity=request.quantity,
        price=request.price,
    )

@router.post("/sell")
def sell(
    request: PortfolioTransactionRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return sell_stock(
        db=db,
        user_id=current_user.id,
        symbol=request.symbol,
        quantity=request.quantity,
        price=request.price,
    )

@router.get("")
def portfolio(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return get_portfolio(
        db,
        current_user.id,
    )

@router.get("/history")
def history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return get_transaction_history(
        db,
        current_user.id,
    )