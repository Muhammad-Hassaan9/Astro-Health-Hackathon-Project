from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class HealthMetricResponse(BaseModel):
    id: UUID
    code: str
    name: str
    category: str
    definition: str
    measurement_method: str | None
    data_type: str
    unit: str | None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)