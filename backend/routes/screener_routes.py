# from fastapi import APIRouter, Depends
# from llm_parser import parse_query_to_dsl
# from schemas import NLPRequest
# from dependencies import get_db
# from models import Symbol, Fundamentals
# from sql_compiler import SQLCompiler
# from execution import execute_query
# from utils.query_logger import log_query 



# router = APIRouter(prefix="/screener")
# ob=SQLCompiler()


# FIELD_MAP = {
#     "pe_ratio": Fundamentals.pe_ratio,
#     "promoter_holding": Fundamentals.promoter_holding,
#     "ebitda": Fundamentals.ebitda,
#     "market_cap": Fundamentals.market_cap,
#     "peg": Fundamentals.peg_ratio
# }


# OPERATOR_MAP = {
#     "<": lambda column, value: column < value,
#     ">": lambda column, value: column > value,
#     "<=": lambda column, value: column <= value,
#     ">=": lambda column, value: column >= value,
#     "=": lambda column, value: column == value
# }


# @router.post("/nlp")
# def nlp_screener(data: NLPRequest, db=Depends(get_db)):

#     # Step 1: NLP → DSL
#     dsl_query = parse_query_to_dsl(data.query)
#     print("dsl output",dsl_query)
#     # Step 2: Base Query
#     query = db.query(Symbol.symbol).join(
#         Fundamentals,
#         Symbol.id == Fundamentals.company_id
#     )

#     # Step 3: Apply Filters Dynamically
#     for con in dsl_query["conditions"]:

#         field = con["field"]
#         operator = con["operator"]
#         value = con["value"]
#         print(f"Applying filter: {field} {operator} {value}")

#         if field not in FIELD_MAP:
#             raise ValueError(f"Unsupported field: {field}")

#         column = FIELD_MAP[field]

#         if operator not in OPERATOR_MAP:
#             raise ValueError(f"Unsupported operator: {operator}")

#         query = query.filter(OPERATOR_MAP[operator](column, value))
    
        
#     # Step 4: Limit
#     limit = dsl_query.get("limit", 20)
#     query = query.limit(limit)   
#     dsl = parse_query_to_dsl(data.query)

   
#     # print(dsl)
#     # sql, values = ob.compile(dsl)
#     # print(sql)

#     print("Generated SQL:")
#     print(query.statement.compile(compile_kwargs={"literal_binds": True}))

#     # results = execute_query(sql, values)

#     # log_query(data.query, dsl, sql, values, results)

#     results = query.all()


#     return {
#         "dsl_query": dsl_query,
#         "results": results
#     }
from fastapi import APIRouter, Depends
from dependencies import get_db

from llm_parser import parse_query_to_dsl
from dsl_validator import validate_dsl
from sql_compiler import compile_dsl
from execution import execute_query
from utils.query_logger import log_query
from schemas import NLPRequest


router = APIRouter(prefix="/screener")


@router.post("/nlp")

def run_screener(data: NLPRequest, db=Depends(get_db)):

    prompt = data.query
    print(prompt)

    dsl = parse_query_to_dsl(prompt)

    validate_dsl(dsl)
    print(dsl)

    sql, values = compile_dsl(dsl)
    print(sql,values)
    

    results = execute_query(sql, values)

    log_query(prompt, dsl, sql, values, results)

    return {
        "prompt": prompt,

        "dsl": dsl,

        "sql": sql,
        
        "values": values,

        "results": results
    }