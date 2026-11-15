from fastapi import HTTPException, status
from fastapi.security import HTTPBearer

from app.core.config import settings

# Extract Bearer token from Authorization header
security = HTTPBearer(
    auto_error=True
)

def validate_supabase_config() -> None:
    """
    Ensure required Supabase authentication
    configuration is available.
    """
    if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase authentication is not configured."
        )

def get_supabase_auth_headers(access_token: str | None = None) -> dict:
    """
    Generate headers for Supabase Auth API requests.
    """
    validate_supabase_config()

    headers = {
        "apikey": settings.SUPABASE_ANON_KEY,
    }

    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    return headers