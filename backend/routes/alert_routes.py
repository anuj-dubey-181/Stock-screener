from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import get_db

from utils.dependencies import get_current_user

from schemas import (
    AlertCreateRequest,
    AlertEvaluationResponse
)

from services.alert_service import (
    create_alert,
    get_user_alerts,
    evaluate_alert,
    set_alert_status,
    get_alert_history
)


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)

@router.post("")
def create(
    request: AlertCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    try:

        alert = create_alert(
            db=db,
            user_id=current_user.id,
            symbol=request.symbol,
            field=request.field,
            operator=request.operator,
            target_value=request.target_value,
            is_active=request.is_active
        )

        return {
            "success": True,
            "message": "Alert created successfully.",
            "data": alert
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("")
def get_alerts(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return {
        "success": True,
        "results": get_user_alerts(
            db,
            current_user.id
        )
    }

@router.post("/{alert_id}/check")
def check_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    try:

        return evaluate_alert(
            db=db,
            user_id=current_user.id,
            alert_id=alert_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.patch("/{alert_id}/status")
def update_status(
    alert_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    try:

        alert = set_alert_status(
            db=db,
            user_id=current_user.id,
            alert_id=alert_id,
            is_active=is_active
        )

        return {
            "success": True,
            "message": "Alert status updated.",
            "data": alert
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.get("/{alert_id}/history")
def history(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    try:

        results = get_alert_history(
            db=db,
            user_id=current_user.id,
            alert_id=alert_id
        )

        return {
            "success": True,
            "results": results
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )