ALLOWED_FIELDS = {
    "pe_ratio": float,
    "market_cap": float,
    "revenue": float,
    "close_price": float
}

ALLOWED_OPERATORS = {
    "<",
    ">",
    "<=",
    ">=",
    "="
}

ALLOWED_LOGIC = {
    "AND",
    "OR"
}

MAX_CONDITIONS = 10

MAX_QUERY_LENGTH = 500