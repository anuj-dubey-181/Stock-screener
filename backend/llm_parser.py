import json
from errors import DSLParsingError
from google import genai
from google.genai.errors import ClientError
from config import GEMINI_API_KEY
from dsl_schema import FIELD_ALIASES
import re
from dsl_schema import DOMAIN_ALIASES
from dsl_schema import FIELD_METADATA

def build_allowed_fields():

    sections = {}

    for field, meta in FIELD_METADATA.items():

        table = meta["table"]

        sections.setdefault(table, [])

        sections[table].append(field)

    text = ""

    for table in sections:

        text += f"\n{table.upper()}\n"

        for field in sorted(sections[table]):

            text += f"- {field}\n"

    return text

def build_field_description():

    text = ""

    for field, meta in FIELD_METADATA.items():

        aliases = ", ".join(meta["aliases"])

        text += (

            f"{field}\n"

            f"Description : {meta['description']}\n"

            f"Type : {meta['type']}\n"

            f"Aliases : {aliases}\n\n"

        )

    return text

def normalize_query(query: str):

    query = query.lower()

    # -------------------------
    # Normalize fields
    # -------------------------

    aliases = sorted(
        FIELD_ALIASES.keys(),
        key=len,
        reverse=True
    )

    for alias in aliases:

        pattern = r"\b" + re.escape(alias) + r"\b"

        query = re.sub(
            pattern,
            FIELD_ALIASES[alias],
            query,
            flags=re.IGNORECASE
        )

    # -------------------------
    # Normalize sector names
    # -------------------------

    for alias, sector in DOMAIN_ALIASES.items():

        pattern = r"\b" + re.escape(alias) + r"\b"

        query = re.sub(
            pattern,
            sector,
            query,
            flags=re.IGNORECASE
        )

    return query

QUERY_REWRITES = {

    r"\bit companies\b":
    "companies where sector = Technology",

    r"\btech companies\b":
    "companies where sector = Technology",

    r"\bbank stocks\b":
    "companies where sector = Financial Services",

    r"\bbanking companies\b":
    "companies where sector = Financial Services",

    r"\bpharma companies\b":
    "companies where sector = Healthcare",

    r"\bhealthcare companies\b":
    "companies where sector = Healthcare",

    r"\benergy companies\b":
    "companies where sector = Energy",

    r"\bfmcg companies\b":
    "companies where sector = Consumer Defensive",

}

def rewrite_query(query):

    for pattern, replacement in QUERY_REWRITES.items():

        query = re.sub(

            pattern,

            replacement,

            query,

            flags=re.IGNORECASE

        )

    return query

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL = "gemini-2.5-flash-lite"
PROMPT = """
You are an expert financial DSL generator.

Your task is to convert a natural language stock screener query into STRICT JSON.

The JSON MUST follow the schema below.

Return ONLY valid JSON.
Do NOT return explanations.
Do NOT wrap JSON inside markdown.
Do NOT invent fields.

==========================================================
ALLOWED FIELDS

forward_pe
peg_ratio
price_to_book
dividend_yield

eps
revenue
ebitda
net_income

total_cash
total_debt

current_ratio
quick_ratio

roe
roa

Historical Metrics Table

open_price
high_price
low_price
close_price
adjusted_close

volume

historical_revenue
historical_ebitda
historical_eps
net_profit

revenue_growth
profit_growth
==========================================================
ALLOWED OPERATORS
==========================================================

=
!=
>
<
>=
<=
between
in
like

==========================================================
TIME FILTERS
==========================================================

latest

last_n_quarters

last_n_years

==========================================================
DSL FORMAT
==========================================================

{
    "logic":"AND",

    "conditions":[

        {
            "field":"pe_ratio",
            "operator":"<",
            "value":20
        }

    ],

    "time_filter":{
        "type":"last_n_quarters",
        "value":4
    },

    "limit":20
}

time_filter is OPTIONAL.

==========================================================
RULES
==========================================================

1.
Use ONLY field names from the allowed field list.

Never generate

sector_name

category

marketCapitalization

priceBook

etc.

2.

For string fields

sector

industry

exchange

company_name

symbol

use

=

!=

like

in

3.

For numeric fields

use

>

<

>=

<=

=

!=

between

in

4.

If user says

Top 10

set

limit = 10

If user does not specify

limit = 20

5.

Examples

"PE below 20"

↓

{
"logic":"AND",
"conditions":[
{
"field":"pe_ratio",
"operator":"<",
"value":20
}
],
"limit":20
}

----------------------------------------------------------

"Market cap greater than 100000"

↓

{
"logic":"AND",
"conditions":[
{
"field":"market_cap",
"operator":">",
"value":100000
}
],
"limit":20
}

----------------------------------------------------------

"Sector is Technology"

↓

{
"logic":"AND",
"conditions":[
{
"field":"sector",
"operator":"=",
"value":"Technology"
}
],
"limit":20
}

----------------------------------------------------------

"Sector contains Bank"

↓

{
"logic":"AND",
"conditions":[
{
"field":"sector",
"operator":"like",
"value":"Bank"
}
],
"limit":20
}

----------------------------------------------------------

"Sector in Technology,Banking"

↓

{
"logic":"AND",
"conditions":[
{
"field":"sector",
"operator":"in",
"value":["Technology","Banking"]
}
],
"limit":20
}

----------------------------------------------------------

"PE between 20 and 40"

↓

{
"logic":"AND",
"conditions":[
{
"field":"pe_ratio",
"operator":"between",
"value":[20,40]
}
],
"limit":20
}

----------------------------------------------------------

"Revenue growth greater than 15 in last 4 quarters"

↓

{
"logic":"AND",
"conditions":[
{
"field":"revenue_growth",
"operator":">",
"value":15
}
],
"time_filter":{
"type":"last_n_quarters",
"value":4
},
"limit":20
}

----------------------------------------------------------

"Show IT companies having PE below 20 and ROE above 18"

↓

{
"logic":"AND",
"conditions":[
{
"field":"sector",
"operator":"=",
"value":"Technology"
},
{
"field":"pe_ratio",
"operator":"<",
"value":20
},
{
"field":"roe",
"operator":">",
"value":18
}
],
"limit":20
}

==========================================================

If the query cannot be converted confidently, return

{
    "error":"QUERY_NOT_UNDERSTOOD"
}

Return ONLY JSON.
"""


def parse_query_to_dsl(query: str):

    if not query or len(query.strip()) == 0:
        raise DSLParsingError("Query cannot be empty")
    
    # Stage 1
    query = normalize_query(query)

    # Stage 2
    query = rewrite_query(query)


    try:    
            full_prompt = PROMPT + "\nUser Query: " + query

            response = client.models.generate_content(
                    model=MODEL,
                    contents=full_prompt,
                    config={
                    "temperature": 0,
                    "response_mime_type": "application/json"
                }

                )
            
            raw_text = response.text.strip()
            print(raw_text)

            clean_text = raw_text.replace("```json", "").replace("```", "").strip()

            try:
                dsl = json.loads(clean_text)
                return dsl

            except json.JSONDecodeError:
                raise ValueError("LLM returned invalid JSON")
    except ClientError as e:
        if "429" in str(e):
          return {"error": "RATE_LIMIT_EXCEEDED"}
        
        
       
 
# query = "Find stocks where PE ratio < 22 and promoter holding > 50  and ebitda 5 in Q2"

# dsl = parse_query_to_dsl(query)

# print(dsl)