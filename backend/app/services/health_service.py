from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import (
    get_health_metric_by_id,
    get_all_data_sources,
    create_health_observation,
)
from app.models.health_metric import HealthMetric
from app.schemas.health_observation import (
    HealthObservationCreate,
    HealthObservationResponse,
    DataStatus,
)

def validate_health_observation(
    metric: HealthMetric,
    observation_data: HealthObservationCreate,
) -> None:
    """Validate observation values against the selected metric."""

    if not metric.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This health metric is currently inactive.",
        )

    data_type = metric.data_type
    if hasattr(data_type, "value"):
        data_type = data_type.value

    data_type = str(data_type).upper()

    if data_type == "NUMERIC" and observation_data.numeric_value is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This metric requires a numeric value.",
        )

    if data_type == "TEXT" and observation_data.text_value is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This metric requires a text value.",
        )

    if data_type not in ("NUMERIC", "TEXT"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported health metric data type.",
        )

    if observation_data.unit and metric.unit:
        if observation_data.unit.strip() != metric.unit.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Expected measurement unit: {metric.unit}.",
            )

    if not observation_data.unit and metric.unit:
        observation_data.unit = metric.unit

def add_manual_health_observation(
    db: Session,
    astronaut_id: UUID,
    observation_data: HealthObservationCreate,
):
    """Validate and save a manually entered health observation."""

    metric = get_health_metric_by_id(
        db=db,
        metric_id=observation_data.metric_id,
    )

    if metric is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health metric not found.",
        )

    validate_health_observation(metric, observation_data)

    sources = get_all_data_sources(
        db=db,
        source_type="MANUAL",
    )

    if not sources:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Manual data source is not configured.",
        )

    observation = create_health_observation(
        db=db,
        astronaut_id=astronaut_id,
        source_id=sources[0].id,
        data_status=DataStatus.MANUAL,
        observation_data=observation_data,
    )

    return observation