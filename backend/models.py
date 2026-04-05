# from sqlalchemy import Column, Integer, String, Float, ForeignKey
# from database import Base


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     email = Column(String, unique=True)
#     password_hash = Column(String)


# class Symbol(Base):
#     __tablename__ = "symbol"

#     id = Column(Integer, primary_key=True)
#     symbol = Column(String, unique=True)
#     sector = Column(String)
#     company_name = Column(String,unique=True)
#     industry = Column(String)
    


# class Fundamentals(Base):
#     __tablename__ = "fundamentals"

#     id = Column(Integer, primary_key=True)
#     company_id = Column(Integer, ForeignKey("symbol.id"))
#     pe = Column(Float)
#     market_cap = Column(Float)
#     revenue = Column(Float)
#     promoter_holding = Column(Float)
#     ebitda = Column(Float)
#     peg_ratio = Column(Float)
#     price_to_book = Column(Float)
#     revenue_growth = Column(Float)
#     profit_margin = Column(Float)


# class HistoricalMetrics(Base):
#     __tablename__ = "historical_metrics"

#     id = Column(Integer, primary_key=True)
#     company_id = Column(Integer,ForeignKey("symbol.id"))
#     date = Column(String)
#     ebitda = Column(Float)
#     close_price = Column(Float)
#     open_price = Column(Float)
#     high_price = Column(Float)
#     low_price = Column(Float)
#     volume = Column(Float)


# class Portfolio(Base):
#     __tablename__ = "portfolio"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer)
#     company_id = Column(Integer)
#     quantity = Column(Float)
#     buy_price = Column(Float)


# class Alert(Base):
#     __tablename__ = "alerts"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer)
#     company_id = Column(Integer)
#     metric = Column(String)
#     operator = Column(String)
#     value = Column(Float)

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


# ================= SYMBOL (COMPANY) =================
class Symbol(Base):
    __tablename__ = "symbol"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False, unique=True)
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
    company_id = Column(Integer, ForeignKey("symbol.id"), nullable=False)

    pe_ratio = Column(Float)
    peg_ratio = Column(Float)
    debt_fcf = Column(Float)
    ebitda = Column(Float)
    revenue = Column(Float)
    promoter_holding = Column(Float)
    market_cap = Column(Float)

    report_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# ================= HISTORICAL METRICS =================
class HistoricalMetrics(Base):
    __tablename__ = "historical_metrics"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("symbol.id"), nullable=False)

    quarter = Column(Date)
    revenue = Column(Float)
    ebitda = Column(Float)
    net_profit = Column(Float)
    close_price = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    volume = Column(Float)



# ================= PORTFOLIO =================
class Portfolio(Base):
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("symbol.id"), nullable=False)

    quantity = Column(Integer)
    buy_price = Column(Float)

    added_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Symbol")


# ================= ALERT =================
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    condition_json = Column(JSON)
    company_id = Column(Integer)

    metric = Column(String)
    operator = Column(String)
    value = Column(Float)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)