from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


# ================= USERS =================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    portfolio = relationship("Portfolio", backref="user")
    alerts = relationship("Alert", backref="user")
    is_active = Column(Boolean, default=True)


# ================= SYMBOL (COMPANY) =================
class Symbol(Base):
    __tablename__ = "symbol"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), nullable=False, unique=True)
    company_name = Column(String, nullable=False)
    sector = Column(String)
    industry = Column(String)
    exchange = Column(String(10))
    
    created_at = Column(DateTime, default=datetime.utcnow)

    fundamentals = relationship("Fundamentals", backref="company")
    historical = relationship("HistoricalMetrics", backref="company")


# ================= FUNDAMENTALS =================
class Fundamentals(Base):
    __tablename__ = "fundamentals"

    id = Column(Integer, primary_key=True)

    company_id = Column(
        Integer,
        ForeignKey("symbol.id"),
        nullable=False
    )

    market_cap = Column(Float)

    enterprise_value = Column(Float)

    pe_ratio = Column(Float)

    forward_pe = Column(Float)

    peg_ratio = Column(Float)

    price_to_book = Column(Float)

    dividend_yield = Column(Float)

    eps = Column(Float)

    revenue = Column(Float)

    ebitda = Column(Float)

    net_income = Column(Float)

    total_cash = Column(Float)

    total_debt = Column(Float)

    current_ratio = Column(Float)

    quick_ratio = Column(Float)

    roe = Column(Float)

    roa = Column(Float)

    report_date = Column(Date)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ================= HISTORICAL METRICS =================
class HistoricalMetrics(Base):
    __tablename__ = "historical_metrics"

    id = Column(Integer, primary_key=True)

    company_id = Column(
        Integer,
        ForeignKey("symbol.id"),
        nullable=False
    )

    # Financials
    quarter = Column(Date)

    revenue = Column(Float)
    ebitda = Column(Float)
    net_profit = Column(Float)

    eps = Column(Float)

    # Market Data
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    adjusted_close = Column(Float)
    volume = Column(Float)

    # Growth Metrics
    revenue_growth = Column(Float)
    profit_growth = Column(Float)

    date = Column(Date)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



# ================= PORTFOLIO =================
class Portfolio(Base):
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    company_id = Column(
        Integer,
        ForeignKey("symbol.id"),
        nullable=False
    )

    quantity = Column(Float)

    avg_buy_price = Column(Float)

    invested_amount = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    company = relationship("Symbol")



class PortfolioTransaction(Base):
    __tablename__ = "portfolio_transactions"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    company_id = Column(
        Integer,
        ForeignKey("symbol.id")
    )

    transaction_type = Column(String)
    # BUY / SELL

    quantity = Column(Float)

    price = Column(Float)

    transaction_date = Column(
        DateTime,
        default=datetime.utcnow
    )
    company = relationship("Symbol")


# ================= ALERT =================
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    company_id = Column(
        Integer,
        ForeignKey("symbol.id")
    )

    metric = Column(String)

    operator = Column(String)

    value = Column(Float)

    is_active = Column(
        Boolean,
        default=True
    )

    trigger_count = Column(
        Integer,
        default=0
    )

    last_triggered_at = Column(DateTime)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
 # ================= ALERT History========

class AlertHistory(Base):
    __tablename__ = "alert_history"

    id = Column(Integer, primary_key=True)

    alert_id = Column(
        Integer,
        ForeignKey("alerts.id"),
        nullable=False
    )

    company_id = Column(
        Integer,
        ForeignKey("symbol.id"),
        nullable=False
    )

    metric = Column(String)

    current_value = Column(Float)

    triggered_at = Column(
        DateTime,
        default=datetime.utcnow
    )