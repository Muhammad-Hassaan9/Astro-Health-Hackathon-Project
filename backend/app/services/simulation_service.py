from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.services.alert_service import create_health_alert
from app.services.websocket_service import manager

from app.crud import (
    get_all_health_metrics,
    get_all_data_sources,
    create_health_observation,
)
from app.schemas.health_observation import (
    HealthObservationCreate,
    DataStatus,
)
from app.services.simulator import generate_health_reading
from app.services.websocket_service import manager

METRIC_ALIASES = {
    "heart_rate": {"HEART_RATE", "HEARTRATE"},
    "spo2": {"SPO2", "OXYGEN_SATURATION", "BLOOD_OXYGEN"},
    "body_temperature": {"BODY_TEMPERATURE", "TEMPERATURE"},
    "physical_activity": {"PHYSICAL_ACTIVITY", "ACTIVITY"},
    "sleep_duration": {"SLEEP_DURATION", "SLEEP"},
    "physical_activity": {"PHYSICAL_ACTIVITY", "ACTIVITY", "ACTIVITY_DURATION",},
}

DEMO_ALERT_RULES = {
    "heart_rate": {
        "min": 60,
        "max": 100,
        "severity": "WARNING",
        "title": "Heart Rate Outside Demo Range",
    },
    "spo2": {
        "min": 95,
        "max": 100,
        "severity": "CRITICAL",
        "title": "Low Oxygen Saturation",
    },
    "body_temperature": {
        "min": 36.0,
        "max": 38.0,
        "severity": "WARNING",
        "title": "Body Temperature Outside Demo Range",
    },
}

def normalize_code(value: str) -> str:
    return value.upper().strip().replace("-", "_").replace(" ", "_")


async def generate_and_save_health_reading(
    db: Session,
    astronaut_id: UUID,
) -> dict:
    reading = generate_health_reading()

    metrics = get_all_health_metrics(db)
    sources = get_all_data_sources(db)

    simulated_source = next(
        (
            source for source in sources
            if normalize_code(str(source.source_type).split(".")[-1])
            in {"SIMULATED", "SIMULATOR"}
        ),
        None,
    )

    if simulated_source is None:
        raise HTTPException(
            status_code=500,
            detail="Simulated data source is not configured in the database.",
        )

    saved_readings = {}

    for reading_key, aliases in METRIC_ALIASES.items():
        metric = next(
            (
                item for item in metrics
                if normalize_code(item.code) in aliases
                and item.is_active
            ),
            None,
        )

        if metric is None:
            continue

        observation_data = HealthObservationCreate(
            metric_id=metric.id,
            numeric_value=Decimal(str(reading[reading_key])),
            unit=metric.unit,
            observed_at=datetime.now(timezone.utc),
            observation_metadata={"simulation": True},
        )

        observation = create_health_observation(
            db=db,
            astronaut_id=astronaut_id,
            source_id=simulated_source.id,
            data_status=DataStatus.SIMULATED,
            observation_data=observation_data,
        )

        saved_readings[reading_key] = {
            "value": reading[reading_key],
            "unit": metric.unit,
            "observation_id": str(observation.id),
        }

        rule = DEMO_ALERT_RULES.get(reading_key)
        value = float(reading[reading_key])

        if rule and (value < rule["min"] or value > rule["max"]):
            alert = create_health_alert(
                db=db,
                astronaut_id=astronaut_id,
                observation_id=observation.id,
                severity=rule["severity"],
                title=rule["title"],
                message=(
                    f"Recorded value: {value} {metric.unit}. "
                    f"Demo range: {rule['min']} - {rule['max']} {metric.unit}."
                ),
                recommended_action=(
                    "Review this reading and contact the mission medical "
                    "officer if necessary."
                ),
            )

            await manager.send_alert(
                astronaut_id,
                jsonable_encoder({
                    "id": alert.id,
                    "severity": alert.severity,
                    "title": alert.title,
                    "message": alert.message,
                    "status": alert.status,
                }),
            )

    if not saved_readings:
        raise HTTPException(
            status_code=500,
            detail="No matching active health metrics were found.",
        )

    result = {
        "recorded_at": reading["recorded_at"],
        "data_status": "SIMULATED",
        "readings": saved_readings,
    }

    await manager.send_health_update(
        astronaut_id,
        jsonable_encoder(result),
    )

    return result