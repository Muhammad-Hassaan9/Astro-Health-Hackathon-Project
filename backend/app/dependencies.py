import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.schemas.auth import UserResponse
from app.database import get_db
from app.crud.astronaut import get_astronaut_by_user_id
from app.models.astronaut import Astronaut

ROOT_DIR = Path(__file__).resolve().parents[1].parent
load_dotenv(ROOT_DIR / ".env", override=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserResponse:

    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase authentication is not configured."
        )

    access_token = credentials.credentials

    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {access_token}"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{SUPABASE_URL.rstrip('/')}/auth/v1/user",
                headers=headers
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired access token.",
                headers={"WWW-Authenticate": "Bearer"}
            )

        user_data = response.json()

        return UserResponse.model_validate(user_data)

    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to Supabase authentication service."
        )

def get_current_astronaut(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Astronaut:

    astronaut = get_astronaut_by_user_id(
        db,
        current_user.id
    )

    if astronaut is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Astronaut profile not found for this user."
        )

    return astronaut