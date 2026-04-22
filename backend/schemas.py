# from pydantic import BaseModel

# class RegisterSchema(BaseModel):
#     email: str
#     password: str

# class Symbol(BaseModel):

#     company_name: str
#     symbol: str


# class LoginSchema(BaseModel):
#     email: str
#     password: str



# class PortfolioCreate(BaseModel):
#     symbol: str
#     quantity: float
#     buy_price: float


# class AlertCreate(BaseModel):
#     symbol: str
#     metric: str
#     operator: str
#     value: float


# class ScreenerFilter(BaseModel):
#     field: str
#     operator: str
#     value: float


# class ScreenerRequest(BaseModel):
#     filters: list[ScreenerFilter]


# class NLPRequest(BaseModel):
#     query: str


from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


# ================= AUTH =================
class RegisterSchema(BaseModel):
    name: Optional[str] = None
    email: str
    password: str


class LoginSchema(BaseModel):
    email: str
    password: str


# ================= SYMBOL =================
class SymbolResponse(BaseModel):
    company_name: str
    symbol: str
    sector: Optional[str]
    industry: Optional[str]


# ================= PORTFOLIO =================
class PortfolioCreate(BaseModel):
    symbol: str
    quantity: int
    buy_price: float



class PortfolioResponse(BaseModel):
    company_name: str
    symbol: str
    quantity: int


# ================= ALERT =================
class AlertCreate(BaseModel):
    symbol: str
    metric: str
    operator: str
    value: float
    
    # Store full DSL instead of single condition
    condition_json: Optional[ Dict[str, Any]] = None


class AlertResponse(BaseModel):
    id: int
    condition_json: Dict[str, Any]
    is_active: bool


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