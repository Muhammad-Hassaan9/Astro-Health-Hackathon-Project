from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.data_source import DataSource

def get_all_data_sources(
    db: Session,
    source_type: str | None = None
) -> list[DataSource]:
    """Retrieve all data sources, optionally filtered by source type."""

    statement = select(DataSource)

    if source_type:
        statement = statement.where(
            DataSource.source_type == source_type
        )

    statement = statement.order_by(DataSource.source_name)

    return list(db.scalars(statement).all())

def get_data_source_by_id(
    db: Session,
    source_id: UUID
) -> DataSource | None:
    """Retrieve a data source using its UUID."""

    statement = select(DataSource).where(
        DataSource.id == source_id
    )

    return db.scalar(statement)