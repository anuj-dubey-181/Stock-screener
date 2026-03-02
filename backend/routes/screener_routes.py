from fastapi import APIRouter, HTTPException
from llm_parser import parse_to_dsl
from dsl_validator import validate_dsl
from errors import DSLParsingError, DSLValidationError

router = APIRouter()


@router.post("/screener/nlp")
def nlp_screener(request: dict):

    try:

        query = request.get("query")

        dsl = parse_to_dsl(query)

        validate_dsl(dsl)

        return {"status": "success", "dsl": dsl}

    except DSLParsingError as e:

        raise HTTPException(
            status_code=400,
            detail={"status": "error", "code": e.code, "message": e.message},
        )

    except DSLValidationError as e:

        raise HTTPException(
            status_code=400,
            detail={"status": "error", "code": e.code, "message": e.message},
        )
    return query.all()
