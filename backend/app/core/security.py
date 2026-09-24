"""
Authentication & authorization utilities.

- JWT creation / validation
- Password hashing (bcrypt via passlib)
- RBAC dependency for FastAPI routes
"""

from datetime import datetime, timedelta, timezone
from enum import StrEnum
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from backend.app.core.config import get_settings

settings = get_settings()

# ── Password hashing ────────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/login")


# ── Roles ────────────────────────────────────────────────────────────────────
class Role(StrEnum):
    """Application roles for RBAC."""

    SUPER_ADMIN = "super_admin"
    INSTITUTION_ADMIN = "institution_admin"
    MENTOR = "mentor"
    STUDENT = "student"


# ── JWT helpers ──────────────────────────────────────────────────────────────
def create_access_token(
    subject: str,
    role: Role,
    tenant_id: str,
    extra_claims: dict | None = None,
) -> str:
    """Create a signed JWT access token."""
    now = datetime.now(timezone.utc)
    claims = {
        "sub": subject,
        "role": role.value,
        "tid": tenant_id,
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
        "type": "access",
    }
    if extra_claims:
        claims.update(extra_claims)
    return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_refresh_token(subject: str, tenant_id: str) -> str:
    """Create a signed JWT refresh token."""
    now = datetime.now(timezone.utc)
    claims = {
        "sub": subject,
        "tid": tenant_id,
        "iat": now,
        "exp": now + timedelta(days=settings.refresh_token_expire_days),
        "type": "refresh",
    }
    return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT. Raises HTTPException on failure."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# ── FastAPI dependencies ─────────────────────────────────────────────────────
class TokenPayload:
    """Parsed JWT payload for use in route handlers."""

    def __init__(self, sub: str, role: Role, tenant_id: str, raw: dict):
        self.sub = sub
        self.role = role
        self.tenant_id = tenant_id
        self.raw = raw


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> TokenPayload:
    """Dependency: extract and validate the current user from JWT."""
    payload = decode_token(token)
    return TokenPayload(
        sub=payload["sub"],
        role=Role(payload["role"]),
        tenant_id=payload["tid"],
        raw=payload,
    )


def require_role(*allowed_roles: Role):
    """Dependency factory: restrict a route to specific roles.

    Usage:
        @router.get("/admin", dependencies=[Depends(require_role(Role.INSTITUTION_ADMIN))])
    """

    async def _check(
        current_user: Annotated[TokenPayload, Depends(get_current_user)],
    ) -> TokenPayload:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' is not authorized for this action",
            )
        return current_user

    return _check
