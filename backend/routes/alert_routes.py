# from fastapi import APIRouter, Depends
# from schemas import AlertCreate
# from models import Alert, Symbol
# from dependencies import get_db, get_current_user

# router = APIRouter(prefix="/alerts")


# @router.post("/")
# def create_alert(data: AlertCreate, db=Depends(get_db), user=Depends(get_current_user)):
#     company = db.query(Symbol).filter(Symbol.symbol == data.symbol).first()

#     alert = Alert(
#         user_id=user.id,
#         company_id=company.id,
#         metric=data.metric,
#         operator=data.operator,
#         value=data.value
#         # condition_json=data.condition_json
#     )

#     db.add(alert)
#     db.commit()

#     return {"message": "Alert created"}

from fastapi import APIRouter, Depends, HTTPException
from schemas import AlertCreate
from models import Alert, Symbol
from dependencies import get_db, get_current_user

router = APIRouter(prefix="/alerts")


# ================= CREATE =================
@router.post("/")
def create_alert(
    data: AlertCreate,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    company = db.query(Symbol).filter(Symbol.symbol == data.symbol).first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

# 🔴 CHECK FOR DUPLICATE
    existing_alert = db.query(Alert).filter(
        Alert.user_id == user.id,
        Alert.company_id == company.id,
        Alert.metric == data.metric,
        Alert.operator == data.operator,
        Alert.value == data.value
    ).first()

    if existing_alert:
        existing_alert.value = data.value
        db.commit()
        return { "status":"duplicate",
            "message": "🔁 Alert updated"}

    alert = Alert(
        user_id=user.id,
        company_id=company.id,
        metric=data.metric,
        operator=data.operator,
        value=data.value,
        condition_json=data.condition_json  # ✅ NOW ENABLED
    )

    db.add(alert)
    db.commit()

    return {"message": "Alert created"}


# ================= GET =================
@router.get("/")
def get_alerts(
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    alerts = db.query(Alert, Symbol).join(
        Symbol, Alert.company_id == Symbol.id
    ).filter(
        Alert.user_id == user.id
    ).all()

    result = []
    for a, s in alerts:
        result.append({
            "id": a.id,
            "symbol": s.symbol,
            "company_name": s.company_name,
            "metric": a.metric,
            "operator": a.operator,
            "value": a.value,
            "condition_json": a.condition_json,
            "is_active": a.is_active
        })

    return result


# ================= DELETE =================
@router.delete("/{alert_id}")
def delete_alert(
    alert_id: int,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == user.id
    ).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    db.delete(alert)
    db.commit()

    return {"message": "Alert deleted"}

@router.get("/check")
def check_alerts_api(db=Depends(get_db)):
    from alert_engine import check_alerts
    return check_alerts(db)