from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.schemas.alert import AlertStatusUpdate
from datetime import datetime, timezone

def get_alerts_by_astronaut_id(
    db: Session,
    astronaut_id: UUID,
    limit: int = 100,
    offset: int = 0
) -> list[Alert]:
    """Retrieve alerts belonging to a specific astronaut."""

    statement = (
        select(Alert)
        .where(Alert.astronaut_id == astronaut_id)
        .order_by(Alert.created_at.desc())
        .limit(limit)
        .offset(offset)
    )

    return list(db.scalars(statement).all())

def get_alert_by_id(
    db: Session,
    alert_id: UUID,
    astronaut_id: UUID
) -> Alert | None:
    """Retrieve a specific alert belonging to an astronaut."""

    statement = select(Alert).where(
        Alert.id == alert_id,
        Alert.astronaut_id == astronaut_id
    )

    return db.scalar(statement)

def update_alert_status(
    db: Session,
    alert_id: UUID,
    astronaut_id: UUID,
    status_data: AlertStatusUpdate
) -> Alert | None:
    """Update the status of an astronaut's alert."""

    alert = get_alert_by_id(
        db,
        alert_id,
        astronaut_id
    )

    if alert is None:
        return None

    try:
        alert.status = status_data.status
        if status_data.status == "RESOLVED":
            alert.resolved_at = datetime.now(timezone.utc)
        else:
            alert.resolved_at = None

        db.commit()
        db.refresh(alert)

        return alert

    except Exception:
        db.rollback()
        raise


def create_alert(
    db: Session,
    astronaut_id: UUID,
    alert_category: str,
    severity: str,
    title: str,
    message: str,
    observation_id: UUID | None = None,
    recommended_action: str | None = None
) -> Alert:
    """Create and save a new alert for an astronaut."""

    alert = Alert(
        astronaut_id=astronaut_id,
        observation_id=observation_id,
        alert_category=alert_category,
        severity=severity,
        title=title,
        message=message,
        recommended_action=recommended_action
    )

    try:
        db.add(alert)
        db.commit()
        db.refresh(alert)

        return alert

    except Exception:
        db.rollback()
        raise