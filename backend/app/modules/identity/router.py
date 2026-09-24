"""
Identity module — API routes for authentication.
"""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.security import TokenPayload, get_current_user
from backend.app.modules.identity.schemas import (
    LoginRequest,
    PasswordChangeRequest,
    RefreshRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
    UserProfile,
)
from backend.app.modules.identity.service import IdentityService

router = APIRouter()


def get_service(db: Annotated[AsyncSession, Depends(get_db)]) -> IdentityService:
    return IdentityService(db)


@router.post("/register", response_model=RegisterResponse, status_code=201)
async def register(
    data: RegisterRequest,
    service: Annotated[IdentityService, Depends(get_service)],
):
    """Register a new user account.

    - `super_admin` users don't need a tenant_id
    - All other roles require a valid tenant_id (institution)
    """
    user = await service.register(data)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    service: Annotated[IdentityService, Depends(get_service)],
):
    """Authenticate with email + password and receive JWT tokens."""
    return await service.login(data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    data: RefreshRequest,
    service: Annotated[IdentityService, Depends(get_service)],
):
    """Exchange a refresh token for a new token pair.

    Each refresh token can only be used once (rotation).
    Reusing a revoked token invalidates ALL sessions for that user.
    """
    return await service.refresh_tokens(data.refresh_token)


@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    service: Annotated[IdentityService, Depends(get_service)],
):
    """Get the current authenticated user's profile."""
    user = await service.get_user(uuid.UUID(current_user.sub))
    return user


@router.post("/change-password", status_code=204)
async def change_password(
    data: PasswordChangeRequest,
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    service: Annotated[IdentityService, Depends(get_service)],
):
    """Change the current user's password. Revokes all active sessions."""
    await service.change_password(uuid.UUID(current_user.sub), data)
