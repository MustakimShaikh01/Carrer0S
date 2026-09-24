"""
Multi-tenancy middleware and utilities.

Strategy: Shared schema with tenant_id column (ADR-007).
All queries are automatically filtered by the current tenant.
"""

import logging
from contextvars import ContextVar
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from backend.app.core.security import TokenPayload, get_current_user

logger = logging.getLogger(__name__)

# ── Tenant context ───────────────────────────────────────────────────────────
_current_tenant: ContextVar[str | None] = ContextVar("current_tenant", default=None)


def get_current_tenant_id() -> str:
    """Get the current tenant ID from context. Raises if not set."""
    tenant_id = _current_tenant.get()
    if tenant_id is None:
        raise RuntimeError("Tenant context not set — is TenantMiddleware installed?")
    return tenant_id


def set_current_tenant_id(tenant_id: str) -> None:
    """Set the current tenant ID in context."""
    _current_tenant.set(tenant_id)


# ── Middleware ───────────────────────────────────────────────────────────────
class TenantMiddleware(BaseHTTPMiddleware):
    """Extract tenant_id from the JWT and set it in context.

    Public routes (health checks, auth endpoints) are excluded.
    """

    EXCLUDED_PREFIXES = (
        "/health",
        "/docs",
        "/openapi.json",
        "/api/v1/auth",
    )

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        path = request.url.path

        # Skip tenant extraction for public routes
        if any(path.startswith(prefix) for prefix in self.EXCLUDED_PREFIXES):
            return await call_next(request)

        # Tenant ID will be set by the auth dependency — here we just
        # ensure the context variable is available
        response = await call_next(request)
        return response


# ── FastAPI dependency ───────────────────────────────────────────────────────
async def ensure_tenant(
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
) -> str:
    """Dependency: extracts tenant_id from JWT and sets it in context.

    Use as a dependency on any route that requires tenant isolation:
        @router.get("/students", dependencies=[Depends(ensure_tenant)])
    """
    if not current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No tenant context in token",
        )
    set_current_tenant_id(current_user.tenant_id)
    return current_user.tenant_id
