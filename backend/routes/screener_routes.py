from fastapi import APIRouter, Depends

from schemas import (
    NLPRequest,
    DSLRequest
)

from services.screener_service import (
    process_nlp_query,
    process_dsl_query
)

from cache_util import get_cached_result, cache_result
from utils.dependencies import get_current_user

router = APIRouter(
    prefix="/screener",
    tags=["AI Screener"]
)


# ====================================================
# Natural Language
# ====================================================

@router.post("/nlp")
def run_nlp_query(
    request: NLPRequest,
    current_user=Depends(get_current_user)
):

    cached_result = get_cached_result(
        request.query
    )

    if cached_result is not None:

        cached_result["cached"] = True

        return cached_result

    
    result=process_nlp_query(
        request.query
    )

    result["cached"] = False

    cache_result(
        request.query,
        result
    )

    return result



# ====================================================
# Execute DSL
# ====================================================

@router.post("/dsl")
def run_dsl_query(
    request: DSLRequest,
    current_user=Depends(get_current_user)
):

    return process_dsl_query(
        request.model_dump()
    )