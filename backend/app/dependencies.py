import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.auth import UserResponse

# Load environment variables from project root
ROOT_DIR = Path(__file__).resolve().parents[1].parent
load_dotenv(ROOT_DIR / ".env", override=True)

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Bearer token authentication
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserResponse:

    # Check Supabase configuration
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase authentication is not configured."
        )

    # Get access token
    access_token = credentials.credentials

    # Verify token through Supabase Auth
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