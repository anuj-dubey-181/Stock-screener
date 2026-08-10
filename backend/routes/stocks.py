from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import get_db

from utils.dependencies import get_current_user

from services.stock_service import (
    get_all_stocks,
    search_stocks,
    get_all_sectors,
    get_sector_stocks,
    get_stock_details
)

router = APIRouter(
    prefix="/stocks",
    tags=["Stocks"]
)


# =====================================================
# Get All Stocks
# =====================================================

@router.get("")
def all_stocks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    stocks = get_all_stocks(db)

    return {

        "success": True,

        "count": len(stocks),

        "results": stocks

    }


# =====================================================
# Search Stocks
# =====================================================

@router.get("/search")
def search(
    q: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    stocks = search_stocks(
        db,
        q
    )

    return {

        "success": True,

        "count": len(stocks),

        "results": stocks

    }


# =====================================================
# Sectors
# =====================================================

@router.get("/sectors")
def sectors(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    sectors = get_all_sectors(db)

    return {

        "success": True,

        "count": len(sectors),

        "results": sectors

    }


# =====================================================
# Companies By Sector
# =====================================================

@router.get("/sector/{sector}")
def sector(
    sector: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    stocks = get_sector_stocks(
        db,
        sector
    )

    return {

        "success": True,

        "count": len(stocks),

        "results": stocks

    }


# =====================================================
# Stock Details
# =====================================================

@router.get("/{symbol}")
def details(
    symbol: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    result = get_stock_details(
        db,
        symbol
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Stock not found."
        )

    return {

        "success": True,

        "data": result

    }



