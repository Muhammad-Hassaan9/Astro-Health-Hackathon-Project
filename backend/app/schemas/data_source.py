from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class DataSourceResponse(BaseModel):
    id: UUID
    source_type: str
    source_name: str
    source_system: str | None
    external_reference: str | None
    reference_url: str | None
    version_label: str | None
    citation: str | None
    description: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)