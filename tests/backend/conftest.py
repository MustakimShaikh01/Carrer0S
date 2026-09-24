"""
Test configuration and fixtures for backend tests.
"""

import asyncio
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from backend.app.core.database import Base, engine
from backend.app.core.security import Role, create_access_token
from backend.app.main import app


@pytest.fixture(scope="session")
def event_loop():
    """Create a single event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client for testing FastAPI endpoints."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    """Create tables before each test and drop after."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# ── Auth helpers ─────────────────────────────────────────────────────────────
def make_auth_header(
    user_id: str = "test-user-id",
    role: Role = Role.SUPER_ADMIN,
    tenant_id: str = "test-tenant-id",
) -> dict[str, str]:
    """Create an Authorization header with a valid JWT for testing."""
    token = create_access_token(subject=user_id, role=role, tenant_id=tenant_id)
    return {"Authorization": f"Bearer {token}"}
