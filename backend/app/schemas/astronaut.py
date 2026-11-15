
from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AstronautCreate(BaseModel):
    display_name: str = Field(
        min_length=1,
        max_length=255
    )

    date_of_birth: date | None = None

    mission_name: str | None = Field(
        default=None,
        max_length=255
    )

    mission_role: str | None = Field(
        default=None,
        max_length=255
    )

    @field_validator("display_name")
    @classmethod
    def validate_display_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Display name cannot be empty.")

        return value


class AstronautUpdate(BaseModel):
    display_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    date_of_birth: date | None = None

    mission_name: str | None = Field(
        default=None,
        max_length=255
    )

    mission_role: str | None = Field(
        default=None,
        max_length=255
    )

    @field_validator("display_name")
    @classmethod
    def validate_display_name(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()

            if not value:
                raise ValueError("Display name cannot be empty.")

        return value


class AstronautResponse(BaseModel):
    id: UUID
    display_name: str
    date_of_birth: date | None
    mission_name: str | None
    mission_role: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
