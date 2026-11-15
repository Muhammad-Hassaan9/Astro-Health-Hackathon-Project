
from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MetricDataType(str, Enum):
    NUMERIC = "numeric"
    TEXT = "text"


class HealthMetricResponse(BaseModel):
    id: UUID
    code: str
    name: str
    category: str
    definition: str
    measurement_method: str | None
    data_type: MetricDataType
    unit: str | None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
