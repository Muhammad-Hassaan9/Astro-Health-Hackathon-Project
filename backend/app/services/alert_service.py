from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.alert import create_alert
from app.models.alert import Alert

VALID_SEVERITIES = {
    "INFO",
    "WARNING",
    "CRITICAL",
}

VALID_CATEGORIES = {
    "HEALTH",
    "DATA_QUALITY",
    "SYSTEM",
}

def create_health_alert(
    db: Session,
    astronaut_id: UUID,
    severity: str,
    title: str,
    message: str,
    observation_id: UUID | None = None,
    recommended_action: str | None = None,
    alert_category: str = "HEALTH",
) -> Alert:
    """
    Validate and create a health-related alert
    for a specific astronaut.
    """

    severity = severity.upper().strip()
    alert_category = alert_category.upper().strip()
    title = title.strip()
    message = message.strip()

    if severity not in VALID_SEVERITIES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid alert severity.",
        )

    if alert_category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid alert category.",
        )

    if not title or not message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Alert title and message are required.",
        )

    if recommended_action is not None:
        recommended_action = recommended_action.strip() or None

    return create_alert(
        db=db,
        astronaut_id=astronaut_id,
        observation_id=observation_id,
        alert_category=alert_category,
        severity=severity,
        title=title,
        message=message,
        recommended_action=recommended_action,
    )