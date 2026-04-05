# dsl_schema.py

# Allowed stock metrics (fields)

ALLOWED_FIELDS = {
    "pe_ratio": "fundamentals.pe_ratio",
    "promoter_holding": "fundamentals.promoter_holding",
    "market_cap": "fundamentals.market_cap",
    "ebitda": "historical_metrics.ebitda",
    "cash_flow": "historical_metrics.cash_flow",
    "peg": "fundamentals.peg",
    "volume":"historical_metrics.volume"
}

ALLOWED_OPERATORS = [
    ">", "<", ">=", "<=", "="
]

ALLOWED_LOGIC = [
    "AND",
    "OR"
]



# Allowed time filters (quarters)
ALLOWED_TIME_FILTERS = {
    "last_n_quarters":int
}


# Field data types
FIELD_DATA_TYPES = {
    "pe_ratio": "float",
    "market_cap": "float",
    "ebitda": "float",
    "promoter_holding": "float",
    "peg_ratio": "float",
    "cash_flow": "float"
}


# DSL Structure
DSL_SCHEMA = {
    "filters": list,
    "logic": str,
    "time_filter": str,
    "limit": int
}