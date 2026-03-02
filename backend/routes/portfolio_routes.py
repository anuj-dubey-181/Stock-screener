from fastapi import APIRouter, Depends
from schemas import PortfolioCreate
from models import Portfolio, Symbol
from dependencies import get_db, get_current_user

router = APIRouter(prefix="/portfolio")


@router.post("/")
def add_portfolio(
    data: PortfolioCreate,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    company = db.query(Symbol).filter(
        Symbol.symbol == data.symbol
    ).first()

    item = Portfolio(
        user_id=user.id,
        company_id=company.id,
        quantity=data.quantity,
        buy_price=data.buy_price
    )

    db.add(item)
    db.commit()

    return {"message": "Added"}