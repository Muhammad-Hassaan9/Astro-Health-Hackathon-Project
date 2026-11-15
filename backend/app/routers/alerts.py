from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_astronaut
from app.models.astronaut import Astronaut
from app.crud import (
    get_alerts_by_astronaut_id,
    get_alert_by_id,
    update_alert_status,
)
from app.schemas.alert import AlertResponse, AlertStatusUpdate


router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("", response_model=list[AlertResponse])
def read_alerts(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    current_astronaut: Astronaut = Depends(get_current_astronaut),
    db: Session = Depends(get_db),
):
    return get_alerts_by_astronaut_id(
        db=db,
        astronaut_id=current_astronaut.id,
        limit=limit,
        offset=offset,
    )

@router.get("/{alert_id}", response_model=AlertResponse)
def read_alert(
    alert_id: UUID,
    current_astronaut: Astronaut = Depends(get_current_astronaut),
    db: Session = Depends(get_db),
):
    alert = get_alert_by_id(
        db=db,
        alert_id=alert_id,
        astronaut_id=current_astronaut.id,
    )

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found.",
        )

    return alert

@router.patch("/{alert_id}/status", response_model=AlertResponse)
def change_alert_status(
    alert_id: UUID,
    status_data: AlertStatusUpdate,
    current_astronaut: Astronaut = Depends(get_current_astronaut),
    db: Session = Depends(get_db),
):
    alert = update_alert_status(
        db=db,
        alert_id=alert_id,
        astronaut_id=current_astronaut.id,
        status_data=status_data,
    )

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found.",
        )

    return alert