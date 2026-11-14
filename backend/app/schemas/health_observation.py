from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class HealthObservationCreate(BaseModel):
    metric_id: UUID
    numeric_value: Decimal | None = None
    text_value: str | None = None
    unit: str | None = None
    observed_at: datetime
    device_identifier: str | None = None
    measurement_method: str | None = None
    data_status: str
    processing_level: str = "RAW"
    quality_status: str = "VALID"
    observation_metadata: dict[str, Any] = Field(default_factory=dict)

class HealthObservationResponse(BaseModel):
    id: UUID
    astronaut_id: UUID
    metric_id: UUID
    source_id: UUID
    numeric_value: Decimal | None
    text_value: str | None
    unit: str | None
    observed_at: datetime
    recorded_at: datetime
    device_identifier: str | None
    measurement_method: str | None
    protocol_reference: str | None
    external_record_id: str | None
    data_status: str
    processing_level: str
    quality_status: str
    observation_metadata: dict[str, Any]
    period_start: datetime | None
    period_end: datetime | None

    model_config = ConfigDict(from_attributes=True)