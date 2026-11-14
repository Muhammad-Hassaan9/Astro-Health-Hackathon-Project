import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    Uuid,
    func,
    text
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class HealthObservation(Base):
    __tablename__ = "health_observations"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )

    astronaut_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("astronaut_profiles.id"),
        nullable=False
    )

    metric_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("health_metrics.id"),
        nullable=False
    )

    source_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("data_sources.id"),
        nullable=False
    )

    numeric_value: Mapped[Decimal | None] = mapped_column(
        Numeric, nullable=True
    )

    text_value: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    unit: Mapped[str | None] = mapped_column(
        String, nullable=True
    )

    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    device_identifier: Mapped[str | None] = mapped_column(
        String, nullable=True
    )

    measurement_method: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    protocol_reference: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    external_record_id: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    data_status: Mapped[str] = mapped_column(
        String, nullable=False
    )

    processing_level: Mapped[str] = mapped_column(
        String,
        nullable=False,
        server_default=text("'RAW'")
    )

    quality_status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        server_default=text("'VALID'")
    )

    observation_metadata: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb")
    )

    period_start: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    period_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )