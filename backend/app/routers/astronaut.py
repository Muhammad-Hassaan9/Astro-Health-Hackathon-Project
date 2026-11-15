from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.auth import UserResponse
from app.schemas.astronaut import (
    AstronautCreate,
    AstronautUpdate,
    AstronautResponse,
)
from app.crud.astronaut import (
    get_astronaut_by_user_id,
    create_astronaut_profile,
    update_astronaut_profile,
)

router = APIRouter(
    prefix="/astronaut",
    tags=["Astronaut Profile"],
)

@router.post(
    "/profile",
    response_model=AstronautResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_profile(
    profile_data: AstronautCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing_profile = get_astronaut_by_user_id(
        db,
        current_user.id,
    )

    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Astronaut profile already exists.",
        )

    return create_astronaut_profile(
        db=db,
        user_id=current_user.id,
        profile_data=profile_data,
    )

@router.get(
    "/profile",
    response_model=AstronautResponse,
)
def read_profile(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    astronaut = get_astronaut_by_user_id(
        db,
        current_user.id,
    )

    if astronaut is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Astronaut profile not found.",
        )

    return astronaut

@router.patch(
    "/profile",
    response_model=AstronautResponse,
)
def edit_profile(
    profile_data: AstronautUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    astronaut = update_astronaut_profile(
        db=db,
        user_id=current_user.id,
        profile_data=profile_data,
    )

    if astronaut is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Astronaut profile not found.",
        )

    return astronaut