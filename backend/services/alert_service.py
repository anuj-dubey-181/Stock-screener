from datetime import datetime

from sqlalchemy.orm import Session

from models import (
    Alert,
    AlertHistory,
    Symbol,
    Fundamentals,
    HistoricalMetrics
)

from dsl_schema import VALID_FIELDS
from dsl_validator import validate_alert_request

def create_alert(
    db: Session,
    user_id: int,
    symbol: str,
    field: str,
    operator: str,
    target_value: float,
    is_active: bool = True
):

    # --------------------------------
    # Validate request
    # --------------------------------

    validate_alert_request({
        "symbol": symbol,
        "field": field,
        "operator": operator,
        "target_value": target_value
    })

    # --------------------------------
    # Find company
    # --------------------------------

    company = (
        db.query(Symbol)
        .filter(
            Symbol.symbol == symbol.upper()
        )
        .first()
    )

    if company is None:
        raise ValueError(
            "Stock symbol not found."
        )

    # --------------------------------
    # Create alert
    # --------------------------------

    alert = Alert(
        user_id=user_id,
        company_id=company.id,
        metric=field,
        operator=operator,
        value=target_value,
        is_active=is_active,
        trigger_count=0
    )

    db.add(alert)

    try:

        db.commit()

        db.refresh(alert)

    except Exception:

        db.rollback()

        raise

    return alert

def get_user_alerts(
    db: Session,
    user_id: int
):

    alerts = (
        db.query(
            Alert,
            Symbol
        )
        .join(
            Symbol,
            Alert.company_id == Symbol.id
        )
        .filter(
            Alert.user_id == user_id
        )
        .order_by(
            Alert.created_at.desc()
        )
        .all()
    )

    results = []

    for alert, company in alerts:

        results.append({

            "id": alert.id,

            "symbol": company.symbol,

            "company_name": company.company_name,

            "metric": alert.metric,

            "operator": alert.operator,

            "value": alert.value,

            "is_active": alert.is_active,

            "trigger_count": (
                alert.trigger_count or 0
            ),

            "last_triggered_at":
                alert.last_triggered_at,

            "created_at":
                alert.created_at

        })

    return results

def evaluate_alert(
    db: Session,
    user_id: int,
    alert_id: int
):

    # --------------------------------
    # Find alert
    # --------------------------------

    alert = (
        db.query(Alert)
        .filter(
            Alert.id == alert_id,
            Alert.user_id == user_id
        )
        .first()
    )

    if alert is None:

        raise ValueError(
            "Alert not found."
        )

    if not alert.is_active:

        raise ValueError(
            "Alert is inactive."
        )

    # --------------------------------
    # Find company
    # --------------------------------

    company = (
        db.query(Symbol)
        .filter(
            Symbol.id == alert.company_id
        )
        .first()
    )

    if company is None:

        raise ValueError(
            "Associated stock not found."
        )

    # --------------------------------
    # Get field metadata
    # --------------------------------

    field_mapping = VALID_FIELDS.get(
        alert.metric
    )

    if field_mapping is None:

        raise ValueError(
            "Invalid alert metric."
        )

    table_name, column_name = (
        field_mapping.split(".")
    )

    # --------------------------------
    # Get current value
    # --------------------------------

    current_value = None

    if table_name == "fundamentals":

        fundamentals = (
            db.query(Fundamentals)
            .filter(
                Fundamentals.company_id ==
                company.id
            )
            .order_by(
                Fundamentals.report_date.desc()
            )
            .first()
        )

        if fundamentals:

            current_value = getattr(
                fundamentals,
                column_name,
                None
            )

    elif table_name == "historical_metrics":

        historical = (
            db.query(HistoricalMetrics)
            .filter(
                HistoricalMetrics.company_id ==
                company.id
            )
            .order_by(
                HistoricalMetrics.date.desc()
            )
            .first()
        )

        if historical:

            current_value = getattr(
                historical,
                column_name,
                None
            )

    elif table_name == "symbol":

        current_value = getattr(
            company,
            column_name,
            None
        )

    if current_value is None:

        raise ValueError(
            "Current value unavailable."
        )

    # --------------------------------
    # Evaluate condition
    # --------------------------------

    target = alert.value

    if alert.operator == ">":
        triggered = current_value > target

    elif alert.operator == "<":
        triggered = current_value < target

    elif alert.operator == ">=":
        triggered = current_value >= target

    elif alert.operator == "<=":
        triggered = current_value <= target

    elif alert.operator == "=":
        triggered = current_value == target

    elif alert.operator == "!=":
        triggered = current_value != target

    else:

        raise ValueError(
            "Unsupported alert operator."
        )

    # --------------------------------
    # Record trigger
    # --------------------------------

    if triggered:

        now = datetime.utcnow()

        alert.trigger_count = (
            (alert.trigger_count or 0) + 1
        )

        alert.last_triggered_at = now

        history = AlertHistory(

            alert_id=alert.id,

            company_id=company.id,

            metric=alert.metric,

            current_value=current_value,

            triggered_at=now

        )

        db.add(history)

        db.commit()

    return {

        "alert_id": alert.id,

        "symbol": company.symbol,

        "metric": alert.metric,

        "operator": alert.operator,

        "target_value": target,

        "current_value": current_value,

        "triggered": triggered,

        "message": (
            "Alert condition triggered."
            if triggered
            else "Alert condition not triggered."
        )

    }

def set_alert_status(
    db: Session,
    user_id: int,
    alert_id: int,
    is_active: bool
):

    alert = (
        db.query(Alert)
        .filter(
            Alert.id == alert_id,
            Alert.user_id == user_id
        )
        .first()
    )

    if alert is None:

        raise ValueError(
            "Alert not found."
        )

    alert.is_active = is_active

    db.commit()

    db.refresh(alert)

    return alert

def get_alert_history(
    db: Session,
    user_id: int,
    alert_id: int
):

    # First make sure alert belongs to user

    alert = (
        db.query(Alert)
        .filter(
            Alert.id == alert_id,
            Alert.user_id == user_id
        )
        .first()
    )

    if alert is None:

        raise ValueError(
            "Alert not found."
        )

    history = (
        db.query(AlertHistory)
        .filter(
            AlertHistory.alert_id == alert_id
        )
        .order_by(
            AlertHistory.triggered_at.desc()
        )
        .all()
    )

    return history
