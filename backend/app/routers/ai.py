from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_astronaut
from app.models.astronaut import Astronaut
from app.schemas.ai import AIQuestionRequest, AIGuidanceResponse
from app.crud.health_observation import get_health_observations
from app.crud.health_metric import get_all_health_metrics
from app.services.ai_service import generate_health_guidance


router = APIRouter(prefix="/ai", tags=["AI Assistant"])


def build_health_context(db: Session, astronaut: Astronaut) -> dict:
    observations = get_health_observations(
        db=db,
        astronaut_id=astronaut.id,
        limit=200,
        offset=0,
    )

    metrics = get_all_health_metrics(db, active_only=True)
    metric_map = {metric.id: metric for metric in metrics}

    latest_readings = {}

    for observation in observations:
        metric = metric_map.get(observation.metric_id)

        if metric is None:
            continue

        if observation.quality_status == "INVALID":
            continue

        if metric.code in latest_readings:
            continue

        value = (
            float(observation.numeric_value)
            if observation.numeric_value is not None
            else observation.text_value
        )

        latest_readings[metric.code] = {
            "metric": metric.name,
            "value": value,
            "unit": observation.unit or metric.unit,
            "observed_at": observation.observed_at.isoformat(),
            "data_status": observation.data_status,
            "quality_status": observation.quality_status,
        }

    return {
        "astronaut": {
            "display_name": astronaut.display_name,
            "mission_name": astronaut.mission_name,
            "mission_role": astronaut.mission_role,
        },
        "latest_health_readings": latest_readings,
        "available_reading_count": len(latest_readings),
    }


@router.post("/guidance", response_model=AIGuidanceResponse)
async def get_health_guidance(
    request: AIQuestionRequest,
    current_astronaut: Astronaut = Depends(get_current_astronaut),
    db: Session = Depends(get_db),
):
    health_context = build_health_context(
        db=db,
        astronaut=current_astronaut,
    )

    answer = await generate_health_guidance(
        question=request.question,
        health_context=health_context,
    )

    return AIGuidanceResponse(answer=answer)