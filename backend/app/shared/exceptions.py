"""
Application-level exceptions and FastAPI exception handlers.
"""

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse


# ── Domain exceptions ────────────────────────────────────────────────────────
class CareerOSError(Exception):
    """Base exception for all CareerOS domain errors."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


class NotFoundError(CareerOSError):
    """Resource not found."""

    def __init__(self, resource: str, identifier: str):
        super().__init__(
            message=f"{resource} '{identifier}' not found",
            code="NOT_FOUND",
        )
        self.resource = resource
        self.identifier = identifier


class DuplicateError(CareerOSError):
    """Resource already exists."""

    def __init__(self, resource: str, field: str, value: str):
        super().__init__(
            message=f"{resource} with {field}='{value}' already exists",
            code="DUPLICATE",
        )


class TenantAccessError(CareerOSError):
    """Attempted access to a resource outside the current tenant."""

    def __init__(self):
        super().__init__(
            message="Access denied: resource belongs to a different tenant",
            code="TENANT_ACCESS_DENIED",
        )


class IntegrationError(CareerOSError):
    """External service integration failure (GitHub, Vertex AI, etc.)."""

    def __init__(self, service: str, detail: str):
        super().__init__(
            message=f"Integration error with {service}: {detail}",
            code="INTEGRATION_ERROR",
        )
        self.service = service


class ValidationError(CareerOSError):
    """Business-logic validation failure."""

    def __init__(self, detail: str):
        super().__init__(message=detail, code="VALIDATION_ERROR")


# ── Exception handlers ──────────────────────────────────────────────────────
async def careeros_error_handler(request: Request, exc: CareerOSError) -> JSONResponse:
    """Convert domain exceptions to structured JSON responses."""
    status_map = {
        "NOT_FOUND": status.HTTP_404_NOT_FOUND,
        "DUPLICATE": status.HTTP_409_CONFLICT,
        "TENANT_ACCESS_DENIED": status.HTTP_403_FORBIDDEN,
        "INTEGRATION_ERROR": status.HTTP_502_BAD_GATEWAY,
        "VALIDATION_ERROR": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "INTERNAL_ERROR": status.HTTP_500_INTERNAL_SERVER_ERROR,
    }
    return JSONResponse(
        status_code=status_map.get(exc.code, 500),
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        },
    )
