"""
Identity module — service layer (auth business logic).
"""

import hashlib
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import get_settings
from backend.app.core.security import (
    Role,
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from backend.app.modules.identity.models import RefreshToken, User
from backend.app.modules.identity.schemas import (
    LoginRequest,
    PasswordChangeRequest,
    RegisterRequest,
    TokenResponse,
)
from backend.app.shared.exceptions import (
    DuplicateError,
    NotFoundError,
    ValidationError,
)

settings = get_settings()


def _hash_token(token: str) -> str:
    """SHA-256 hash a refresh token for storage."""
    return hashlib.sha256(token.encode()).hexdigest()


class IdentityService:
    """Business logic for authentication and user management."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ── Registration ─────────────────────────────────────────────────
    async def register(self, data: RegisterRequest) -> User:
        """Register a new user. Raises DuplicateError if email exists."""
        existing = await self.db.execute(
            select(User).where(User.email == data.email)
        )
        if existing.scalar_one_or_none():
            raise DuplicateError("User", "email", data.email)

        # Validate role-tenant consistency
        if data.role != "super_admin" and not data.tenant_id:
            raise ValidationError(
                "Non-super_admin users must be associated with a tenant (institution)"
            )

        user = User(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hash_password(data.password),
            role=data.role,
            tenant_id=data.tenant_id,
            student_id=data.student_id,
        )
        self.db.add(user)
        await self.db.flush()
        return user

    # ── Login ────────────────────────────────────────────────────────
    async def login(self, data: LoginRequest) -> TokenResponse:
        """Authenticate with email + password and return JWT pair."""
        result = await self.db.execute(
            select(User).where(User.email == data.email)
        )
        user = result.scalar_one_or_none()

        if not user or not verify_password(data.password, user.hashed_password):
            raise ValidationError("Invalid email or password")

        if not user.is_active:
            raise ValidationError("Account is deactivated")

        return await self._create_token_pair(user)

    # ── Token Refresh ────────────────────────────────────────────────
    async def refresh_tokens(self, refresh_token_raw: str) -> TokenResponse:
        """Exchange a refresh token for a new token pair (rotation)."""
        token_hash = _hash_token(refresh_token_raw)

        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        stored = result.scalar_one_or_none()

        if not stored:
            raise ValidationError("Invalid refresh token")

        if stored.is_revoked:
            # Possible token replay attack — revoke all tokens for this user
            await self._revoke_all_tokens(stored.user_id)
            raise ValidationError("Refresh token has been revoked — all sessions invalidated")

        if stored.expires_at < datetime.now(timezone.utc):
            raise ValidationError("Refresh token has expired")

        # Revoke the used token (rotation)
        stored.is_revoked = True
        await self.db.flush()

        # Fetch user and create new pair
        user_result = await self.db.execute(
            select(User).where(User.id == stored.user_id)
        )
        user = user_result.scalar_one_or_none()
        if not user:
            raise NotFoundError("User", str(stored.user_id))

        return await self._create_token_pair(user)

    # ── Password Change ──────────────────────────────────────────────
    async def change_password(
        self, user_id: uuid.UUID, data: PasswordChangeRequest
    ) -> None:
        """Change a user's password. Revokes all refresh tokens."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("User", str(user_id))

        if not verify_password(data.current_password, user.hashed_password):
            raise ValidationError("Current password is incorrect")

        user.hashed_password = hash_password(data.new_password)
        await self._revoke_all_tokens(user_id)
        await self.db.flush()

    # ── Get User ─────────────────────────────────────────────────────
    async def get_user(self, user_id: uuid.UUID) -> User:
        """Get a user by ID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("User", str(user_id))
        return user

    # ── Internal helpers ─────────────────────────────────────────────
    async def _create_token_pair(self, user: User) -> TokenResponse:
        """Create access + refresh token pair and store the refresh token."""
        tenant_id = str(user.tenant_id) if user.tenant_id else ""

        access_token = create_access_token(
            subject=str(user.id),
            role=Role(user.role),
            tenant_id=tenant_id,
        )
        refresh_token_raw = secrets.token_urlsafe(64)

        # Store refresh token hash
        stored_refresh = RefreshToken(
            user_id=user.id,
            token_hash=_hash_token(refresh_token_raw),
            expires_at=datetime.now(timezone.utc)
            + timedelta(days=settings.refresh_token_expire_days),
        )
        self.db.add(stored_refresh)
        await self.db.flush()

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token_raw,
            expires_in=settings.access_token_expire_minutes * 60,
        )

    async def _revoke_all_tokens(self, user_id: uuid.UUID) -> None:
        """Revoke all refresh tokens for a user."""
        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked == False,  # noqa: E712
            )
        )
        for token in result.scalars().all():
            token.is_revoked = True
