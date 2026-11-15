from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.health_observation import HealthObservation
from app.schemas.health_observation import HealthObservationCreate,DataStatus

def create_health_observation(
    db: Session,
    astronaut_id: UUID,
    source_id: UUID,
    data_status: DataStatus,
    observation_data: HealthObservationCreate
) -> HealthObservation:
    """Save a health observation for an astronaut."""

    observation = HealthObservation(
        astronaut_id=astronaut_id,
        source_id=source_id,
        data_status=data_status,
        **observation_data.model_dum()
    )

    try:
        db.add(observation)
        db.commit()
        db.refresh(observation)

        return observation

    except Exception:
        db.rollback()
        raise

def get_health_observation_by_id(
    db: Session,
    observation_id: UUID,
    astronaut_id: UUID
) -> HealthObservation | None:
    """Retrieve an observation belonging to a specific astronaut."""

    statement = select(HealthObservation).where(
        HealthObservation.id == observation_id,
        HealthObservation.astronaut_id == astronaut_id
    )

    return db.scalar(statement)

def get_health_observations(
    db: Session,
    astronaut_id: UUID,
    metric_id: UUID | None = None,
    limit: int = 100,
    offset: int = 0
) -> list[HealthObservation]:
    """Retrieve an astronaut's observations with optional metric filtering."""

    statement = select(HealthObservation).where(
        HealthObservation.astronaut_id == astronaut_id
    )

    if metric_id is not None:
        statement = statement.where(
            HealthObservation.metric_id == metric_id
        )

    statement = (
        statement
        .order_by(HealthObservation.observed_at.desc())
        .limit(limit)
        .offset(offset)
    )

    return list(db.scalars(statement).all())