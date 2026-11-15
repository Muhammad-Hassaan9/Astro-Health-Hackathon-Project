import httpx

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.dependencies import (
    SUPABASE_URL,
    SUPABASE_ANON_KEY,
    get_current_user,
)
from app.schemas.auth import (
    SignupRequest,
    LoginRequest,
    RefreshTokenRequest,
    AuthResponse,
    SignupPendingResponse,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_supabase_headers() -> dict:
    return {
        "apikey": SUPABASE_ANON_KEY,
        "Content-Type": "application/json",
    }

def check_supabase_config():
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase authentication is not configured.",
        )

def handle_supabase_error(response: httpx.Response) -> None:
    try:
        error_data = response.json()
        message = (
            error_data.get("msg")
            or error_data.get("message")
            or error_data.get("error_description")
            or "Authentication request failed."
        )
    except ValueError:
        message = "Authentication request failed."

    raise HTTPException(
        status_code=(
            response.status_code
            if 400 <= response.status_code < 500
            else status.HTTP_502_BAD_GATEWAY
        ),
        detail=message,
    )

@router.post(
    "/signup",
    response_model=AuthResponse | SignupPendingResponse,
)
async def signup(user_data: SignupRequest):
    check_supabase_config()

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                f"{SUPABASE_URL.rstrip('/')}/auth/v1/signup",
                headers=get_supabase_headers(),
                json={
                    "email": user_data.email,
                    "password": user_data.password,
                },
            )

        if response.status_code >= 400:
            handle_supabase_error(response)

        data = response.json()
        session = data.get("session") or data
        user = data.get("user") or session.get("user") or (
            data if data.get("id") else None
        )

        if not user or not user.get("id"):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Supabase did not return user information.",
            )

        access_token = session.get("access_token")

        if not access_token:
            pending_response = SignupPendingResponse(
                user_id=user["id"],
                message="Account created. Please verify your email, then log in.",
            )

            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED,
                content=pending_response.model_dump(mode="json"),
            )

        return AuthResponse(
            access_token=access_token,
            refresh_token=session.get("refresh_token"),
            user_id=user["id"],
            message="Account created and authenticated successfully.",
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to Supabase.",
        )


@router.post("/login", response_model=AuthResponse)
async def login(user_data: LoginRequest):
    check_supabase_config()

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                f"{SUPABASE_URL.rstrip('/')}/auth/v1/token?grant_type=password",
                headers=get_supabase_headers(),
                json={
                    "email": user_data.email,
                    "password": user_data.password,
                },
            )

        if response.status_code >= 400:
            handle_supabase_error(response)

        data = response.json()
        user = data.get("user")

        if not user or not user.get("id") or not data.get("access_token"):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Supabase did not return a valid authentication session.",
            )

        return AuthResponse(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token"),
            user_id=user["id"],
            message="Login successful.",
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to Supabase.",
        )

@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(token_data: RefreshTokenRequest):
    check_supabase_config()

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                f"{SUPABASE_URL.rstrip('/')}/auth/v1/token?grant_type=refresh_token",
                headers=get_supabase_headers(),
                json={
                    "refresh_token": token_data.refresh_token,
                },
            )

        if response.status_code >= 400:
            handle_supabase_error(response)

        data = response.json()
        user = data.get("user")

        if not user or not user.get("id") or not data.get("access_token"):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Supabase did not return a valid refreshed session.",
            )

        return AuthResponse(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token"),
            user_id=user["id"],
            message="Token refreshed successfully.",
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to Supabase.",
        )

@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: UserResponse = Depends(get_current_user),
):
    return current_user