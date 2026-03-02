from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Symbol, Fundamentals
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