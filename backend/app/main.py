"""
CareerOS — FastAPI Application Entrypoint

Mounts all module routers, configures middleware, and registers
exception handlers. This is the modular monolith orchestrator.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import get_settings
from backend.app.shared.exceptions import CareerOSError, careeros_error_handler
from backend.app.shared.multi_tenancy import TenantMiddleware

# ── Module routers ───────────────────────────────────────────────────────────
from backend.app.modules.identity.router import router as identity_router
from backend.app.modules.institution.router import router as institution_router
from backend.app.modules.student.router import router as student_router

logger = logging.getLogger(__name__)
settings = get_settings()


# ── Lifespan ─────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle hook."""
    logger.info(
        "Starting %s v%s [%s]",
        settings.app_name,
        settings.app_version,
        settings.environment,
    )
    yield
    logger.info("Shutting down %s", settings.app_name)


# ── App factory ──────────────────────────────────────────────────────────────
def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Technical career intelligence platform — measures demonstrated skills, "
            "identifies gaps, recommends actions, and provides institutional analytics."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # ── Middleware (order matters — outermost first) ──────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(TenantMiddleware)

    # ── Exception handlers ───────────────────────────────────────────────
    app.add_exception_handler(CareerOSError, careeros_error_handler)

    # ── Routes ───────────────────────────────────────────────────────────
    prefix = settings.api_v1_prefix

    app.include_router(identity_router, prefix=f"{prefix}/auth", tags=["Auth"])
    app.include_router(
        institution_router, prefix=f"{prefix}/institutions", tags=["Institutions"]
    )
    app.include_router(student_router, prefix=f"{prefix}/students", tags=["Students"])

    # Health check — no auth required
    @app.get("/health", tags=["System"])
    async def health_check():
        return {
            "status": "healthy",
            "version": settings.app_version,
            "environment": settings.environment,
        }

    return app


app = create_app()
