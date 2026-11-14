from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

# Signup Request
class SignupRequest(BaseModel):
    email: EmailStr
    password: str

# Login Request
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Authentication Response
class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: UUID

# Authenticated User Response
class UserResponse(BaseModel):
    id: UUID
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)