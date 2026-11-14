from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.health_metric import HealthMetric

def get_all_health_metrics(
    db: Session,
    active_only: bool = True
) -> list[HealthMetric]:
    """Retrieve all health metrics, optionally filtering inactive ones."""

    statement = select(HealthMetric)

    if active_only:
        statement = statement.where(
            HealthMetric.is_active.is_(True)
        )

    statement = statement.order_by(HealthMetric.name)

    return list(db.scalars(statement).all())

def get_health_metric_by_id(
    db: Session,
    metric_id: UUID
) -> HealthMetric | None:
    """Retrieve a health metric using its UUID."""

    statement = select(HealthMetric).where(
        HealthMetric.id == metric_id
    )

    return db.scalar(statement)

def get_health_metric_by_code(
    db: Session,
    code: str
) -> HealthMetric | None:
    """Retrieve a health metric using its unique code."""

    statement = select(HealthMetric).where(
        HealthMetric.code == code
    )

    return db.scalar(statement)