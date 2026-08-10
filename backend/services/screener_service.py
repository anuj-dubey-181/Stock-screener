from llm_parser import parse_query_to_dsl
from dsl_validator import validate_dsl
from sql_compiler import compile_dsl
from execution import execute_query


# =====================================================
# NLP -> DSL -> SQL -> PostgreSQL
# =====================================================

def process_nlp_query(query: str):

    # -----------------------------
    # LLM
    # -----------------------------
    dsl = parse_query_to_dsl(query)

    if "error" in dsl:

        return {

            "success": False,

            "message": dsl["error"]

        }

    # -----------------------------
    # Validation
    # -----------------------------

    validate_dsl(dsl)

    # -----------------------------
    # Compile SQL
    # -----------------------------

    sql, params = compile_dsl(dsl)

    # -----------------------------
    # Execute SQL
    # -----------------------------

    result = execute_query(
        sql,
        params
    )

    return {

        "success": True,

        "query": query,

        "dsl": dsl,

        "sql": sql,

        "execution_time": result.get("execution_time"),

        "count": result.get("count"),

        "results": result.get("Results", [])

    }


# =====================================================
# Execute DSL directly
# =====================================================

def process_dsl_query(dsl: dict):

    validate_dsl(dsl)

    sql, params = compile_dsl(dsl)

    result = execute_query(
        sql,
        params
    )

    return {

        "success": True,

        "dsl": dsl,

        "sql": sql,

        "execution_time": result.get("execution_time"),

        "count": result.get("count"),

        "results": result.get("Results", [])

    }