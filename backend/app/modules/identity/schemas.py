"""
Identity module — Pydantic schemas for auth flows.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# ── Registration ─────────────────────────────────────────────────────────────
class RegisterRequest(BaseModel):
    """Request: register a new user account."""

    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    role: str = Field(
        default="student",
        pattern=r"^(super_admin|institution_admin|mentor|student)$",
    )
    tenant_id: uuid.UUID | None = None
    student_id: uuid.UUID | None = None


class RegisterResponse(BaseModel):
    """Response: successful registration."""

    id: uuid.UUID
    email: str
    full_name: str
    role: str
    tenant_id: uuid.UUID | None
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Login ────────────────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    """Request: log in with email + password."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response: JWT token pair."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


# ── Token Refresh ────────────────────────────────────────────────────────────
class RefreshRequest(BaseModel):
    """Request: exchange a refresh token for a new token pair."""

    refresh_token: str


# ── User Profile ─────────────────────────────────────────────────────────────
class UserProfile(BaseModel):
    """Response: current user's profile (from /me endpoint)."""

    id: uuid.UUID
    email: str
    full_name: str
    role: str
    tenant_id: uuid.UUID | None
    student_id: uuid.UUID | None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class PasswordChangeRequest(BaseModel):
    """Request: change the current user's password."""

    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)
