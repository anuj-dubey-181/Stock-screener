"""
FIELD_METADATA

Single Source of Truth

Everything in the project should derive from this file.

Used by

✔ DSL Validator
✔ SQL Compiler
✔ LLM Prompt Generator
✔ Query Normalizer
✔ Alert Engine
✔ Redis Cache
✔ AI Explanation Engine
✔ Future Ranking Engine
"""

FIELD_METADATA = {

# ==========================================================
# SYMBOL TABLE
# ==========================================================

"symbol":{

    "column":"symbol.symbol",
    "table":"symbol",
    "type":"string",

    "aliases":[

        "ticker",
        "stock symbol",
        "company symbol"

    ],

    "description":"NSE stock symbol",

    "unit":None,

    "search_priority":10

},

"company_name":{

    "column":"symbol.company_name",
    "table":"symbol",
    "type":"string",

    "aliases":[

        "company",
        "company name",
        "stock"

    ],

    "description":"Company Name",

    "unit":None,

    "search_priority":10

},

"sector":{

    "column":"symbol.sector",
    "table":"symbol",
    "type":"string",

    "aliases":[

        "industry sector",
        "business sector",
        "segment"

    ],

    "description":"Business Sector",

    "unit":None,

    "search_priority":9

},

"industry":{

    "column":"symbol.industry",
    "table":"symbol",
    "type":"string",

    "aliases":[

        "business",
        "industry type"

    ],

    "description":"Industry",

    "unit":None,

    "search_priority":8

},

"exchange":{

    "column":"symbol.exchange",
    "table":"symbol",
    "type":"string",

    "aliases":[

        "market",
        "stock exchange"

    ],

    "description":"Stock Exchange",

    "unit":None,

    "search_priority":8

},

# ==========================================================
# FUNDAMENTALS
# ==========================================================

"market_cap":{

    "column":"fundamentals.market_cap",
    "table":"fundamentals",
    "type":"number",

    "aliases":[

        "market capitalization",
        "market cap",
        "mcap"

    ],

    "description":"Market Capitalization",

    "unit":"₹",

    "search_priority":10

},

"enterprise_value":{

    "column":"fundamentals.enterprise_value",
    "table":"fundamentals",
    "type":"number",

    "aliases":[

        "ev",
        "enterprise valuation"

    ],

    "description":"Enterprise Value",

    "unit":"₹",

    "search_priority":7

},

"pe_ratio":{

    "column":"fundamentals.pe_ratio",
    "table":"fundamentals",
    "type":"number",

    "aliases":[

        "pe",
        "p/e",
        "price earnings",
        "price earning ratio"

    ],

    "description":"Price to Earnings Ratio",

    "unit":"ratio",

    "search_priority":10

},

"forward_pe":{

    "column":"fundamentals.forward_pe",
    "table":"fundamentals",
    "type":"number",

    "aliases":[

        "forward price earnings",
        "future pe"

    ],

    "description":"Forward PE",

    "unit":"ratio",

    "search_priority":7

},

"peg_ratio":{

    "column":"fundamentals.peg_ratio",
    "table":"fundamentals",
    "type":"number",

    "aliases":[

        "peg",
        "peg ratio"

    ],

    "description":"PEG Ratio",

    "unit":"ratio",

    "search_priority":8

},

"price_to_book":{

    "column":"fundamentals.price_to_book",
    "table":"fundamentals",
    "type":"number",

    "aliases":[

        "pb",
        "p/b",
        "price book",
        "price to book ratio"

    ],

    "description":"Price to Book Ratio",

    "unit":"ratio",

    "search_priority":8

},

"dividend_yield":{

    "column":"fundamentals.dividend_yield",
    "table":"fundamentals",
    "type":"number",

    "aliases":[

        "dividend",
        "yield"

    ],

    "description":"Dividend Yield",

    "unit":"%",

    "search_priority":7

},

"eps":{

    "column":"fundamentals.eps",
    "table":"fundamentals",
    "type":"number",

    "aliases":[

        "earnings per share"

    ],

    "description":"EPS",

    "unit":"₹",

    "search_priority":9

},

"revenue":{

    "column":"fundamentals.revenue",
    "table":"fundamentals",
    "type":"number",

    "aliases":[

        "sales",
        "turnover"

    ],

    "description":"Revenue",

    "unit":"₹",

    "search_priority":9

},

"ebitda":{

    "column":"fundamentals.ebitda",
    "table":"fundamentals",
    "type":"number",

    "aliases":[

        "operating profit"

    ],

    "description":"EBITDA",

    "unit":"₹",

    "search_priority":8

},

"net_income":{

    "column":"fundamentals.net_income",
    "table":"fundamentals",
    "type":"number",

    "aliases":[

        "profit",
        "income",
        "net profit"

    ],

    "description":"Net Income",

    "unit":"₹",

    "search_priority":8

},

"total_cash":{

    "column":"fundamentals.total_cash",
    "table":"fundamentals",
    "type":"number",

    "aliases":[

        "cash"

    ],

    "description":"Total Cash",

    "unit":"₹",

    "search_priority":6

},

"total_debt":{

    "column":"fundamentals.total_debt",
    "table":"fundamentals",
    "type":"number",

    "aliases":[

        "debt",
        "borrowings"

    ],

    "description":"Total Debt",

    "unit":"₹",

    "search_priority":7

},

"current_ratio":{

    "column":"fundamentals.current_ratio",
    "table":"fundamentals",
    "type":"number",

    "aliases":[

        "liquidity ratio"

    ],

    "description":"Current Ratio",

    "unit":"ratio",

    "search_priority":6

},

"quick_ratio":{

    "column":"fundamentals.quick_ratio",
    "table":"fundamentals",
    "type":"number",

    "aliases":[

        "acid test ratio"

    ],

    "description":"Quick Ratio",

    "unit":"ratio",

    "search_priority":6

},

"roe":{

    "column":"fundamentals.roe",
    "table":"fundamentals",
    "type":"number",

    "aliases":[

        "return on equity"

    ],

    "description":"ROE",

    "unit":"%",

    "search_priority":9

},

"roa":{

    "column":"fundamentals.roa",
    "table":"fundamentals",
    "type":"number",

    "aliases":[

        "return on assets"

    ],

    "description":"ROA",

    "unit":"%",

    "search_priority":8

},

# ==========================================================
# HISTORICAL
# ==========================================================

"open_price":{
    "column":"historical_metrics.open_price",
    "table":"historical_metrics",
    "type":"number",
    "aliases":["open"],
    "description":"Opening Price",
    "unit":"₹",
    "search_priority":5
},

"high_price":{
    "column":"historical_metrics.high_price",
    "table":"historical_metrics",
    "type":"number",
    "aliases":["high"],
    "description":"Highest Price",
    "unit":"₹",
    "search_priority":5
},

"low_price":{
    "column":"historical_metrics.low_price",
    "table":"historical_metrics",
    "type":"number",
    "aliases":["low"],
    "description":"Lowest Price",
    "unit":"₹",
    "search_priority":5
},

"close_price":{
    "column":"historical_metrics.close_price",
    "table":"historical_metrics",
    "type":"number",
    "aliases":[
        "close",
        "closing price",
        "current price"
    ],
    "description":"Closing Price",
    "unit":"₹",
    "search_priority":9
},

"adjusted_close":{
    "column":"historical_metrics.adjusted_close",
    "table":"historical_metrics",
    "type":"number",
    "aliases":[
        "adj close",
        "adjusted price"
    ],
    "description":"Adjusted Close",
    "unit":"₹",
    "search_priority":4
},

"volume":{
    "column":"historical_metrics.volume",
    "table":"historical_metrics",
    "type":"number",
    "aliases":[
        "trading volume"
    ],
    "description":"Trading Volume",
    "unit":"shares",
    "search_priority":8
},

"historical_revenue":{
    "column":"historical_metrics.revenue",
    "table":"historical_metrics",
    "type":"number",
    "aliases":[
        "quarterly revenue"
    ],
    "description":"Historical Revenue",
    "unit":"₹",
    "search_priority":7
},

"historical_ebitda":{
    "column":"historical_metrics.ebitda",
    "table":"historical_metrics",
    "type":"number",
    "aliases":[
        "quarterly ebitda"
    ],
    "description":"Historical EBITDA",
    "unit":"₹",
    "search_priority":7
},

"historical_eps":{
    "column":"historical_metrics.eps",
    "table":"historical_metrics",
    "type":"number",
    "aliases":[
        "quarterly eps"
    ],
    "description":"Historical EPS",
    "unit":"₹",
    "search_priority":7
},

"net_profit":{
    "column":"historical_metrics.net_profit",
    "table":"historical_metrics",
    "type":"number",
    "aliases":[
        "quarterly profit"
    ],
    "description":"Historical Net Profit",
    "unit":"₹",
    "search_priority":7
},

"revenue_growth":{
    "column":"historical_metrics.revenue_growth",
    "table":"historical_metrics",
    "type":"number",
    "aliases":[
        "sales growth"
    ],
    "description":"Revenue Growth",
    "unit":"%",
    "search_priority":8
},

"profit_growth":{
    "column":"historical_metrics.profit_growth",
    "table":"historical_metrics",
    "type":"number",
    "aliases":[
        "earnings growth"
    ],
    "description":"Profit Growth",
    "unit":"%",
    "search_priority":8
}

}

VALID_FIELDS = {
    field: meta["column"]
    for field, meta in FIELD_METADATA.items()
}

FIELD_TABLES = {
    field: meta["table"]
    for field, meta in FIELD_METADATA.items()
}

FIELD_TYPES = {
    field: meta["type"]
    for field, meta in FIELD_METADATA.items()
}

FIELD_ALIASES = {}

for field, meta in FIELD_METADATA.items():

    FIELD_ALIASES[field.lower()] = field

    for alias in meta["aliases"]:
        FIELD_ALIASES[alias.lower()] = field


# ============================================================
# Operators
# ============================================================

VALID_OPERATORS = {
    "=",
    "!=",
    ">",
    "<",
    ">=",
    "<=",
    "between",
    "in",
    "like"
}

VALID_LOGIC = {
    "AND",
    "OR"
}

VALID_TIME_FILTERS = {
    "latest",
    "last_n_quarters",
    "last_n_years"
}


DOMAIN_ALIASES = {

    "it": "Technology",

    "tech": "Technology",

    "technology": "Technology",

    "bank": "Financial Services",

    "banking": "Financial Services",

    "finance": "Financial Services",

    "pharma": "Healthcare",

    "healthcare": "Healthcare",

    "auto": "Automobile",

    "automobile": "Automobile",

    "fmcg": "Consumer Defensive",

    "energy": "Energy",

    "oil": "Energy",

    "power": "Utilities"

}