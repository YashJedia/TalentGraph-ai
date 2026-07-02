from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.db.repository import FraudRepository
from app.models.schemas import FraudAlert as FraudAlertSchema, FraudAlertsResponse
from app.models.database import FraudAlert

router = APIRouter()
fraud_repo = FraudRepository()


@router.get("/alerts", response_model=FraudAlertsResponse)
async def list_fraud_alerts(session: AsyncSession = Depends(get_db_session)) -> FraudAlertsResponse:
    alerts = await fraud_repo.list_alerts(session)
    alert_models = [FraudAlertSchema.model_validate(alert) for alert in alerts]
    severity_counts = {}
    for alert in alert_models:
        severity_counts[alert.severity] = severity_counts.get(alert.severity, 0) + 1
    return FraudAlertsResponse(
        total_alerts=len(alert_models),
        by_severity=severity_counts,
        recent_alerts=alert_models,
    )


@router.get("/alerts/{alert_id}", response_model=FraudAlertSchema)
async def get_fraud_alert(alert_id: UUID, session: AsyncSession = Depends(get_db_session)) -> FraudAlertSchema:
    alert = await fraud_repo.get_alert(session, alert_id)
    if alert is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fraud alert not found")
    return FraudAlertSchema.model_validate(alert)
