from openai import OpenAI
import json
from errors import DSLParsingError

client = OpenAI()

SYSTEM_PROMPT = """
You are a DSL parser for stock screener.

Convert user query into STRICT JSON DSL format.

Allowed fields:
- pe_ratio
- market_cap
- revenue
- close_price

Allowed operators:
<, >, <=, >=, =

Output format:

{
 "conditions": [
   {
     "field": "pe_ratio",
     "operator": "<",
     "value": 20
   }
 ],
 "logic": "AND"
}

Return JSON only.
"""

def parse_to_dsl(query: str):

    if not query or len(query.strip()) == 0:
        raise DSLParsingError("Query cannot be empty")

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ]
        )

        dsl = json.loads(response.choices[0].message.content)

        return dsl

    except Exception as e:
        raise DSLParsingError(f"Failed to parse query: {str(e)}")