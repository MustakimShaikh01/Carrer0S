"""
Tests for the health endpoint and basic app startup.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Health endpoint should return 200 with status and version."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert data["environment"] == "local"


@pytest.mark.asyncio
async def test_openapi_docs_available(client: AsyncClient):
    """OpenAPI docs should be accessible."""
    response = await client.get("/docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_api_v1_prefix(client: AsyncClient):
    """API routes should be under /api/v1."""
    response = await client.get("/api/v1/auth/login")
    # POST-only route returns 405 on GET
    assert response.status_code == 405
