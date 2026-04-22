import json
from errors import DSLParsingError
from google import genai
from google.genai.errors import ClientError
from config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)

MODEL = "gemini-2.5-flash-lite"

PROMPT = """
 You are a STRICT DSL generator.

  Convert the user query into JSON DSL.

  Allowed fields:
  pe, peg, promoter_holding, ebitda, debt_free_cash, revenue, net_profit

  Entity rules:
  - fundamentals → pe_ratio, peg, promoter_holding
  - historical_metrics → revenue, ebitda, net_profit, debt_free_cash
  - symbol → when fields belong to both tables

  DSL structure:

  {{
  "entity": "...",
  "logic": "AND",
  "conditions": [
    {{
      "field": "...",
      "operator": "...",
      "value": number
    }}
  ],
  "time_filter": {{
    "type": "last_n_quarters",
    "value": number
  }},
  "limit": 20
  }}

  Examples:

  User Query:
  show companies with pe less than 20

  DSL:
  {{
  "entity":"fundamentals",
  "logic":"AND",
  "conditions":[
   {{"field":"pe_ratio","operator":"<","value":20}}
  ],
  "limit":20
  }}

  User Query:
  show companies with ebitda greater than 1000000

  DSL:
  {{
 "entity":"historical_metrics",
 "logic":"AND",
 "conditions":[
   {{"field":"ebitda","operator":">","value":1000000}}
 ],
 "limit":20
  }}

User Query:
show companies with pe < 50 and ebitda > than 100000 for the past 3 quarters and market capatalization greater than 10000

  DSL:
  {{
 "entity":"symbol",
 "logic":"AND",
 "conditions":[
   {{"field":"pe_ratio","operator":"<","value":50}},
   {{"field":"ebitda","operator":">","value":100000}}
   {{"field":"market_cap","operator":">","value"1}}

 ],
 "time_filter": {
        "type": "last_n_quarters",   # ONLY THIS
        "value": 3                  # integer > 0
    } ,
 "limit":20
  }}

  Rules:
  Return JSON only.
  If query cannot be parsed return:
  {{ "error":"QUERY_NOT_UNDERSTOOD" }}


Only return JSON.
"""


def parse_query_to_dsl(query: str):

    if not query or len(query.strip()) == 0:
        raise DSLParsingError("Query cannot be empty")

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