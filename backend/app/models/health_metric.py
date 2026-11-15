import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, Uuid, func, text,CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class HealthMetric(Base):
    __tablename__ = "health_metrics"
    __table_args__ = (
        CheckConstraint(
            "data_type IN ('numeric', 'text')",
            name="health_metrics_data_type_check"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )

    code: Mapped[str] = mapped_column(String, nullable=False,unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    definition: Mapped[str] = mapped_column(Text, nullable=False)

    measurement_method: Mapped[str | None] = mapped_column(Text, nullable=True)

    data_type: Mapped[str] = mapped_column(String, nullable=False)
    unit: Mapped[str | None] = mapped_column(String, nullable=True)

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )