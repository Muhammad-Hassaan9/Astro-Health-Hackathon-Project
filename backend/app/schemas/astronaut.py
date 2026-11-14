from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

# Schema for creating an astronaut profile
class AstronautCreate(BaseModel):
    display_name: str
    date_of_birth: date | None = None
    mission_name: str | None = None
    mission_role: str | None = None

# Schema for returning astronaut profile data
class AstronautResponse(BaseModel):
    id: UUID
    display_name: str
    date_of_birth: date | None
    mission_name: str | None
    mission_role: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)