from sqlalchemy.orm import Session
from datetime import datetime

from models import (
    Symbol,
    Portfolio,
    PortfolioTransaction,
    HistoricalMetrics
)


def buy_stock(
    db: Session,
    user_id: int,
    symbol: str,
    quantity: float,
    price: float,):


    company = (
    db.query(Symbol)
    .filter(Symbol.symbol == symbol.upper())
    .first()
    )

    if company is None:
        raise ValueError("Invalid stock symbol.")

    holding = (
    db.query(Portfolio)
    .filter(
        Portfolio.user_id == user_id,
        Portfolio.company_id == company.id,
    )
    .first()
    )
    
    transaction = PortfolioTransaction(

    user_id=user_id,

    company_id=company.id,

    transaction_type="BUY",

    quantity=quantity,

    price=price,

    )

    db.add(transaction)

    if holding is None:

        holding = Portfolio(

            user_id=user_id,

            company_id=company.id,

            quantity=quantity,

            avg_buy_price=price,

            invested_amount=quantity * price,

        )

        db.add(holding)

    else:

        new_quantity = holding.quantity + quantity

        new_investment = (

            holding.invested_amount + quantity * price

         )

        holding.quantity = new_quantity

        holding.invested_amount = new_investment

        holding.avg_buy_price = (

            new_investment / new_quantity

         )
        
    db.commit()

    db.refresh(holding)

    return holding


def sell_stock(
    db: Session,
    user_id: int,
    symbol: str,
    quantity: float,
    price: float,
     ):

        company = (
            db.query(Symbol)
            .filter(Symbol.symbol == symbol.upper())
            .first()
        )

        if company is None:
            raise ValueError("Invalid stock symbol.")

        holding = (
            db.query(Portfolio)
            .filter(
                Portfolio.user_id == user_id,
                Portfolio.company_id == company.id,
            )
            .first()
        )

        if holding is None:
            raise ValueError("Stock not present in portfolio.")

        if quantity > holding.quantity:
            raise ValueError("Insufficient quantity.")

        try:

            transaction = PortfolioTransaction(
                user_id=user_id,
                company_id=company.id,
                transaction_type="SELL",
                quantity=quantity,
                price=price,
            )

            db.add(transaction)

            remaining_qty = holding.quantity - quantity

            if remaining_qty == 0:

                db.delete(holding)

            else:

                holding.invested_amount -= (
                    quantity * holding.avg_buy_price
                )

                holding.quantity = remaining_qty

                holding.avg_buy_price = (
                    holding.invested_amount /
                    holding.quantity
                )

            db.commit()

        except:
            db.rollback()
            raise

        return {
            "message": "Stock sold successfully."
        }



def get_portfolio(
    db: Session,
    user_id: int
):
    holdings = (
        db.query(Portfolio, Symbol)
        .join(
            Symbol,
            Portfolio.company_id == Symbol.id
        )
        .filter(
            Portfolio.user_id == user_id
        )
        .all()
    )

    results = []

    for holding, company in holdings:

        # Get latest market price
        latest = (
            db.query(HistoricalMetrics)
            .filter(
                HistoricalMetrics.company_id == company.id
            )
            .order_by(
                HistoricalMetrics.date.desc()
            )
            .first()
        )

        # No market data available
        if latest is None:
            current_price = 0.0
        else:
            current_price = latest.close_price or 0.0

        quantity = holding.quantity or 0.0
        invested_amount = holding.invested_amount or 0.0
        avg_buy_price = holding.avg_buy_price or 0.0

        current_value = quantity * current_price

        profit_loss = (
            current_value - invested_amount
        )

        if invested_amount > 0:
            profit_loss_percent = (
                profit_loss / invested_amount
            ) * 100
        else:
            profit_loss_percent = 0.0

        results.append({
            "symbol": company.symbol,
            "company_name": company.company_name,
            "quantity": quantity,
            "avg_buy_price": avg_buy_price,
            "invested_amount": invested_amount,
            "current_price": current_price,
            "current_value": current_value,
            "profit_loss": profit_loss,
            "profit_loss_percent": profit_loss_percent
        })

    return results

def get_transaction_history(
    db: Session,
    user_id: int
):

    transactions = (
        db.query(
            PortfolioTransaction,
            Symbol
        )
        .join(
            Symbol,
            PortfolioTransaction.company_id == Symbol.id
        )
        .filter(
            PortfolioTransaction.user_id == user_id
        )
        .order_by(
            PortfolioTransaction.transaction_date.desc()
        )
        .all()
    )

    results = []

    for transaction, company in transactions:

        results.append({
            "symbol": company.symbol,
            "company_name": company.company_name,
            "transaction_type": transaction.transaction_type,
            "quantity": transaction.quantity or 0.0,
            "price": transaction.price or 0.0,
            "transaction_date": transaction.transaction_date
        })

    return results