from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

# Alert Response
class AlertResponse(BaseModel):
    id: UUID
    astronaut_id: UUID
    observation_id: UUID | None
    alert_category: str
    severity: str
    title: str
    message: str
    recommended_action: str | None
    status: str
    created_at: datetime
    resolved_at: datetime | None

    model_config = ConfigDict(from_attributes=True)

# Alert Status Update
class AlertStatusUpdate(BaseModel):
    status: str