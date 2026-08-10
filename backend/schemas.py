
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any,Generic, TypeVar
from datetime import date , datetime

# ================= AUTH =================
class RegisterSchema(BaseModel):
    name: Optional[str] = None
    email: str
    password: str


class LoginSchema(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str="bearer"

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool

    model_config = {
        "from_attributes": True
    }

# ================= SYMBOL =================

class SymbolResponse(BaseModel):
    id: int
    company_name: str
    symbol: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    exchange: Optional[str] = None
   

    class Config:
        from_attributes = True


# ================= PORTFOLIO =================
class PortfolioCreate(BaseModel):
    symbol: str
    quantity: float
    avg_buy_price: float



class PortfolioResponse(BaseModel):
    company_name: str

    symbol: str

    quantity: float

    avg_buy_price: float

    invested_amount: float

    current_price: float

    current_value: float

    profit_loss: float

    profit_loss_percent: float
    
    class Config:
        from_attributes = True


class PortfolioTransactionCreate(BaseModel):

    symbol: str

    transaction_type: str

    quantity: float

    price: float

class PortfolioTransactionResponse(BaseModel):

   

    symbol: str

    company_name: str

    transaction_type: str

    quantity: float

    price: float

    transaction_date: datetime

    class Config:
        from_attributes = True

class PortfolioHoldingResponse(BaseModel):

    symbol: str

    company_name: str

    quantity: float

    avg_buy_price: float

    invested_amount: float

    current_price: float

    current_value: float

    profit_loss: float

    profit_loss_percent: float



class PortfolioTransactionRequest(BaseModel):

    symbol: str

    quantity: float = Field(gt=0)

    price: float = Field(gt=0)

# ================= ALERT =================

class AlertCreateRequest(BaseModel):
    symbol: str
    field: str
    operator: str
    target_value: float
    is_active: bool = True


class AlertResponse(BaseModel):
    id: int
    company_id: int
    metric: str
    operator: str
    value: float
    is_active: bool
    trigger_count: int
    last_triggered_at: Optional[datetime] = None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class AlertEvaluationResponse(BaseModel):
    alert_id: int
    symbol: str
    metric: str
    operator: str
    target_value: float
    current_value: Optional[float]
    triggered: bool
    message: str


class AlertHistoryResponse(BaseModel):
    id: int
    alert_id: int
    company_id: int
    metric: str
    current_value: float
    triggered_at: datetime

    model_config = {
        "from_attributes": True
    }


class FundamentalsResponse(BaseModel):

    company_id: int

    market_cap: Optional[float] = None

    enterprise_value: Optional[float] = None

    pe_ratio: Optional[float] = None

    forward_pe: Optional[float] = None

    peg_ratio: Optional[float] = None

    price_to_book: Optional[float] = None

    dividend_yield: Optional[float] = None

    eps: Optional[float] = None

    revenue: Optional[float] = None

    ebitda: Optional[float] = None

    net_income: Optional[float] = None

    total_cash: Optional[float] = None

    total_debt: Optional[float] = None

    roe: Optional[float] = None

    roa: Optional[float] = None

    report_date: Optional[date] = None

    class Config:
        from_attributes = True


class HistoricalMetricsResponse(BaseModel):

    company_id: int

    date1 : Optional[date] = None

    open_price: Optional[float] = None

    high_price: Optional[float] = None

    low_price: Optional[float] = None

    close_price: Optional[float] = None

    adjusted_close: Optional[float] = None

    volume: Optional[float] = None

    revenue: Optional[float] = None

    ebitda: Optional[float] = None

    net_profit: Optional[float] = None

    eps: Optional[float] = None

    revenue_growth: Optional[float] = None

    profit_growth: Optional[float] = None

    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


class StockDetailsResponse(BaseModel):

    company: SymbolResponse

    fundamentals: Optional[FundamentalsResponse] = None

    historical: Optional[HistoricalMetricsResponse] = None

# ================= SCREENER (DSL BASED) =================
class ScreenerCondition(BaseModel):
    field: str = Field(..., example="pe")
    operator: str = Field(..., example=">")
    value: float = Field(..., example=20)


class TimeFilter(BaseModel):
    type: str = Field(..., example="last_n_quarters")
    value: int = Field(..., example=3)


class ScreenerRequest(BaseModel):
    entity: str = "fundamentals"
    logic: str = "AND"
    conditions: List[ScreenerCondition]
    time_filter: Optional[TimeFilter] = None
    limit: Optional[int] = 20


# ================= NLP =================
class NLPRequest(BaseModel):
    query: str 

class DSLRequest(BaseModel):

    entity: str = "symbol"

    logic: str

    conditions: list

    time_filter: Optional[dict] = None

    limit: int = 20



T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):

    success: bool = True

    message: str = "Success"

    data: Optional[T] = None