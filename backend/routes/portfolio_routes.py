# from fastapi import APIRouter, Depends
# from schemas import PortfolioCreate
# from models import Portfolio, Symbol
# from dependencies import get_db, get_current_user

# router = APIRouter(prefix="/portfolio")


# @router.post("/")
# def add_portfolio(
#     data: PortfolioCreate,
#     db=Depends(get_db),
#     user=Depends(get_current_user)
# ):
#     company = db.query(Symbol).filter(
#         Symbol.symbol == data.symbol
#     ).first()

#     item = Portfolio(
#         user_id=user.id,
#         company_id=company.id,
#         quantity=data.quantity,
#         buy_price=data.buy_price
#     )

#     db.add(item)
#     db.commit()

#     return {"message": "Added"}

from fastapi import APIRouter, Depends, HTTPException
from schemas import PortfolioCreate
from models import Portfolio, Symbol, HistoricalMetrics
from dependencies import get_db, get_current_user

router = APIRouter(prefix="/portfolio")


# ================= CREATE =================
@router.post("/")
def add_portfolio(
    data: PortfolioCreate,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    company = db.query(Symbol).filter(Symbol.symbol == data.symbol).first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    item = Portfolio(
        user_id=user.id,
        company_id=company.id,
        quantity=data.quantity,
        buy_price=data.buy_price
    )

    db.add(item)
    db.commit()

    return {"message": "Added"}


# ================= GET =================
# @router.get("/")
# def get_portfolio(
#     db=Depends(get_db),
#     user=Depends(get_current_user)
# ):
#     items = db.query(Portfolio, Symbol).join(
#         Symbol, Portfolio.company_id == Symbol.id
#     ).filter(
#         Portfolio.user_id == user.id
#     ).all()

#     result = []
#     for p, s in items:
#         result.append({
#             "id": p.id,
#             "symbol": s.symbol,
#             "company_name": s.company_name,
#             "quantity": p.quantity,
#             "buy_price": p.buy_price,
#             "holdings" : p.quantity*p.buy_price

#         })

#     return result
@router.get("/")
def get_portfolio(db=Depends(get_db), user=Depends(get_current_user)):

    data = db.query(Portfolio, Symbol).join(
        Symbol, Portfolio.company_id == Symbol.id
    ).filter(
        Portfolio.user_id == user.id
    ).all()

    results = []

    for p, s in data:

         # ✅ ONLY LATEST RECORD
        h = db.query(HistoricalMetrics).filter(
            HistoricalMetrics.company_id == s.id
        ).order_by(HistoricalMetrics.quarter.desc()).first()

        current_price = h.close_price or 0
        invested = p.quantity * p.buy_price
        current_value = p.quantity * current_price

        profit = current_value - invested
        growth = (profit / invested * 100) if invested > 0 else 0

        results.append({
            "symbol": s.symbol,
            "quantity": p.quantity,
            "buy_price": p.buy_price,
            "current_price": current_price,
            "profit": profit,
            "growth_percent": round(growth, 2)
        })

    return results


# ================= UPDATE =================
@router.put("/{portfolio_id}")
def update_portfolio(
    portfolio_id: int,
    data: PortfolioCreate,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    item = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == user.id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    company = db.query(Symbol).filter(Symbol.symbol == data.symbol).first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    item.company_id = company.id
    item.quantity = data.quantity
    item.buy_price = data.buy_price

    db.commit()

    return {"message": "Updated"}


# ================= DELETE =================
@router.delete("/{portfolio_id}")
def delete_portfolio(
    portfolio_id: int,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    item = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == user.id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    db.delete(item)
    db.commit()

    return {"message": "Deleted"}