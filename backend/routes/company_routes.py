from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Symbol, Fundamentals,HistoricalMetrics
from database import SessionLocal

router = APIRouter(prefix="/company")

def get_db():
    db = SessionLocal()
    yield db
    db.close()


@router.get("/")
def get_companies(db: Session = Depends(get_db)):
    return db.query(Symbol).all()


@router.get("/{symbol}")
def get_company(symbol: str, db: Session = Depends(get_db)):
    return db.query(Symbol).filter(Symbol.symbol == symbol).first()


@router.get("/{symbol}/fundamentals")
def get_fundamentals(symbol: str, db: Session = Depends(get_db)):
    company = db.query(Symbol).filter(Symbol.symbol == symbol).first()
    return db.query(Fundamentals).filter(
        Fundamentals.company_id == company.id
    ).first()


@router.get("/{symbol}/history")
def get_history(symbol: str, db=Depends(get_db)):

    company = db.query(Symbol).filter(Symbol.symbol == symbol).first()

    data = db.query(HistoricalMetrics).filter(
        HistoricalMetrics.company_id == company.id
    ).order_by(HistoricalMetrics.quarter).all()

    return [
        {
            "date": d.quarter,
            "close_price": d.close_price
        }
        for d in data
    ]






