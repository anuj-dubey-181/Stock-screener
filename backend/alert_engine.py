from sqlalchemy.orm import Session
from models import Alert, Symbol, Fundamentals, HistoricalMetrics

def check_alerts(db: Session):

    alerts = db.query(Alert).all()
    triggered = []

    for alert in alerts:

        company = db.query(Symbol).filter(Symbol.id == alert.company_id).first()

        # Get latest data
        fundamentals = db.query(Fundamentals).filter(
            Fundamentals.company_id == company.id
        ).first()

        historical = db.query(HistoricalMetrics).filter(
            HistoricalMetrics.company_id == company.id
        ).first()

        value = None

        if hasattr(fundamentals, alert.metric):
            value = getattr(fundamentals, alert.metric)

        elif hasattr(historical, alert.metric):
            value = getattr(historical, alert.metric)

        if value is None:
            continue

        condition_met = False

        if alert.operator == ">" and value > alert.value:
            condition_met = True
        if alert.operator == "<" and value < alert.value:
            condition_met = True

        if condition_met:
            triggered.append({
                "symbol": company.symbol,
                "metric": alert.metric,
                "value": value,
                "target": alert.value
            })

    return triggered