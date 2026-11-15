from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_astronaut
from app.models.astronaut import Astronaut
from app.services.simulation_service import generate_and_save_health_reading
from app.crud import (
    get_all_health_metrics,
    get_all_data_sources,
    create_health_observation,
    get_health_observation_by_id,
    get_health_observations,
)
from app.schemas.health_observation import (
    HealthObservationCreate,
    HealthObservationResponse,
    DataStatus,
)
from app.schemas.health_metric import HealthMetricResponse


router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/metrics", response_model=list[HealthMetricResponse])
def read_health_metrics(
    current_astronaut: Astronaut = Depends(get_current_astronaut),
    db: Session = Depends(get_db),
):
    return get_all_health_metrics(db)

@router.post(
    "/observations",
    response_model=HealthObservationResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_health_observation(
    observation_data: HealthObservationCreate,
    current_astronaut: Astronaut = Depends(get_current_astronaut),
    db: Session = Depends(get_db),
):
    # Manual observations must use a backend-managed MANUAL data source.
    sources = get_all_data_sources(db, source_type="MANUAL")

    if not sources:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Manual data source is not configured.",
        )

    observation = create_health_observation(
        db=db,
        astronaut_id=current_astronaut.id,
        source_id=sources[0].id,
        data_status=DataStatus.MANUAL,
        observation_data=observation_data,
    )

    return observation

@router.get(
    "/observations",
    response_model=list[HealthObservationResponse],
)
def read_health_observations(
    metric_id: UUID | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    current_astronaut: Astronaut = Depends(get_current_astronaut),
    db: Session = Depends(get_db),
):
    return get_health_observations(
        db=db,
        astronaut_id=current_astronaut.id,
        metric_id=metric_id,
        limit=limit,
        offset=offset,
    )

@router.get(
    "/observations/{observation_id}",
    response_model=HealthObservationResponse,
)
def read_health_observation(
    observation_id: UUID,
    current_astronaut: Astronaut = Depends(get_current_astronaut),
    db: Session = Depends(get_db),
):
    observation = get_health_observation_by_id(
        db=db,
        observation_id=observation_id,
        astronaut_id=current_astronaut.id,
    )

    if observation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health observation not found.",
        )

    return observation

@router.post("/simulate", status_code=status.HTTP_201_CREATED)
async def simulate_health_reading(
    current_astronaut: Astronaut = Depends(get_current_astronaut),
    db: Session = Depends(get_db),
):
    return await generate_and_save_health_reading(
        db=db,
        astronaut_id=current_astronaut.id,
    )