from fastapi import APIRouter, Depends
from schemas import AlertCreate
from models import Alert, Symbol
from dependencies import get_db, get_current_user

router = APIRouter(prefix="/alerts")


@router.post("/")
def create_alert(data: AlertCreate, db=Depends(get_db), user=Depends(get_current_user)):
    company = db.query(Symbol).filter(Symbol.symbol == data.symbol).first()

    alert = Alert(
        user_id=user.id,
        company_id=company.id,
        metric=data.metric,
        operator=data.operator,
        value=data.value,
    )

    db.add(alert)
    db.commit()

    return {"message": "Alert created"}
