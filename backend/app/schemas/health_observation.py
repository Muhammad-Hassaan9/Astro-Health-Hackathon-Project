
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


# Allowed data origins
class DataStatus(str, Enum):
    SIMULATED = "SIMULATED"
    MANUAL = "MANUAL"
    SENSOR = "SENSOR"


# How the observation has been processed
class ProcessingLevel(str, Enum):
    RAW = "RAW"
    PROCESSED = "PROCESSED"
    DERIVED = "DERIVED"


# Data quality classification
class QualityStatus(str, Enum):
    VALID = "VALID"
    SUSPECT = "SUSPECT"
    INVALID = "INVALID"


# Data received from the frontend
class HealthObservationCreate(BaseModel):
    metric_id: UUID

    numeric_value: Decimal | None = None
    text_value: str | None = Field(default=None, min_length=1)

    unit: str | None = None
    observed_at: datetime

    device_identifier: str | None = None
    measurement_method: str | None = None
    protocol_reference: str | None = None
    external_record_id: str | None = None

    period_start: datetime | None = None
    period_end: datetime | None = None

    observation_metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("text_value", mode="before")
    @classmethod
    def clean_text_value(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value

    @model_validator(mode="after")
    def validate_observation_value(self):
        has_numeric = self.numeric_value is not None
        has_text = self.text_value is not None

        if has_numeric == has_text:
            raise ValueError(
                "Provide exactly one of numeric_value or text_value."
            )

        return self

    @model_validator(mode="after")
    def validate_observation_period(self):
        has_start = self.period_start is not None
        has_end = self.period_end is not None

        if has_start != has_end:
            raise ValueError(
                "period_start and period_end must both be provided."
            )

        if (
            has_start
            and has_end
            and self.period_start >= self.period_end
        ):
            raise ValueError(
                "period_start must be earlier than period_end."
            )

        return self


# Data returned by the backend
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

    data_status: DataStatus
    processing_level: ProcessingLevel
    quality_status: QualityStatus

    observation_metadata: dict[str, Any]

    period_start: datetime | None
    period_end: datetime | None

    model_config = ConfigDict(from_attributes=True)
