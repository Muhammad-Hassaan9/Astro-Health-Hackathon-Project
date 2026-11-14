from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.astronaut import Astronaut
from app.schemas.astronaut import AstronautCreate, AstronautUpdate

def get_astronaut_by_user_id(
    db: Session,
    user_id: UUID
) -> Astronaut | None:
    """Retrieve an astronaut profile using the user's ID."""

    statement = select(Astronaut).where(
        Astronaut.user_id == user_id
    )

    return db.scalar(statement)

def create_astronaut_profile(
    db: Session,
    user_id: UUID,
    profile_data: AstronautCreate
) -> Astronaut:
    """Create a new astronaut profile."""

    astronaut = Astronaut(
        user_id=user_id,
        **profile_data.model_dump()
    )

    try:
        db.add(astronaut)
        db.commit()
        db.refresh(astronaut)

        return astronaut

    except Exception:
        db.rollback()
        raise

def update_astronaut_profile(
    db: Session,
    user_id: UUID,
    profile_data: AstronautUpdate
) -> Astronaut | None:
    """Update only the fields provided by the user."""

    astronaut = get_astronaut_by_user_id(db, user_id)

    if astronaut is None:
        return None

    updated_data = profile_data.model_dump(
        exclude_unset=True
    )

    if not updated_data:
        return astronaut

    for field, value in updated_data.items():
        setattr(astronaut, field, value)

    try:
        db.commit()
        db.refresh(astronaut)

        return astronaut

    except Exception:
        db.rollback()
        raise