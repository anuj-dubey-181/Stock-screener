from sqlalchemy.orm import Session
from sqlalchemy import desc

from models import (
    Symbol,
    Fundamentals,
    HistoricalMetrics
)

from schemas import (
    SymbolResponse,
    FundamentalsResponse,
    HistoricalMetricsResponse,
)


# =====================================================
# Get all companies
# =====================================================

def get_all_stocks(db: Session):

    stocks = (
        db.query(Symbol)
        .order_by(Symbol.company_name)
        .all()
    )

    return [
    SymbolResponse.model_validate(stock)
    for stock in stocks
]


# =====================================================
# Search by symbol/company
# =====================================================

def search_stocks(
    db: Session,
    query: str
):

    stocks = (
        db.query(Symbol)
        .filter(
            (Symbol.symbol.ilike(f"%{query}%")) |
            (Symbol.company_name.ilike(f"%{query}%"))
        )
        .order_by(Symbol.company_name)
        .all()
    )

    return [
    SymbolResponse.model_validate(stock)
    for stock in stocks
]


# =====================================================
# Get all sectors
# =====================================================

def get_all_sectors(db: Session):

    sectors = (
        db.query(Symbol.sector)
        .distinct()
        .order_by(Symbol.sector)
        .all()
    )

    return [
        row[0]
        for row in sectors
        if row[0]
    ]


# =====================================================
# Get companies of one sector
# =====================================================

def get_sector_stocks(
    db: Session,
    sector: str
):

    return (
        db.query(Symbol)
        .filter(Symbol.sector == sector)
        .order_by(Symbol.company_name)
        .all()
    )


# =====================================================
# Company Details
# =====================================================

def get_stock_details(
    db: Session,
    symbol: str
):

    company = (
        db.query(Symbol)
        .filter(Symbol.symbol == symbol.upper())
        .first()
    )

    if company is None:
        return None

    fundamentals = (
        db.query(Fundamentals)
        .filter(
            Fundamentals.company_id == company.id
        )
        .order_by(desc(Fundamentals.report_date))
        .first()
    )

    historical = (
        db.query(HistoricalMetrics)
        .filter(
            HistoricalMetrics.company_id == company.id
        )
        .order_by(desc(HistoricalMetrics.date))
        .first()
    )

    return {
        "company": SymbolResponse.model_validate(company),
        "fundamentals": (
                FundamentalsResponse.model_validate(fundamentals)
                if fundamentals
                else None
            ),
        "historical": (
                HistoricalMetricsResponse.model_validate(historical)
                if historical
                else None
            ),

    }