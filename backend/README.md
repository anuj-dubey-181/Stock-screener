# Stock-screener-2
# LLM Parser Guardrails and Validation Strategy

The LLM parser converts natural language into DSL JSON.

The LLM output is treated as untrusted input.

Guardrails implemented:

Field whitelist
Only allowed metrics:
- pe_ratio
- market_cap
- revenue
- close_price

Operator whitelist
Allowed operators:
<, >, <=, >=, =

Structure validation
Conditions must be non-empty list.

Type validation
Numeric fields must contain numeric values.

Logical validation
Logic must be AND or OR.

Query limits
Maximum query length: 500
Maximum conditions: 10

Error handling
All errors return structured format:

{
 "status": "error",
 "code": "DSL_VALIDATION_ERROR",
 "message": "Invalid field"
}

Security
No user input is directly used in SQL.
All queries are parameterized.