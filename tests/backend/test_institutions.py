"""
Tests for the institution module.
"""

import pytest
from httpx import AsyncClient

from backend.app.core.security import Role
from tests.backend.conftest import make_auth_header


@pytest.mark.asyncio
async def test_create_institution(client: AsyncClient):
    """Super admin can create an institution."""
    headers = make_auth_header(role=Role.SUPER_ADMIN)
    response = await client.post(
        "/api/v1/institutions/",
        json={
            "name": "IIT Bombay",
            "slug": "iit-bombay",
            "domain": "iitb.ac.in",
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "IIT Bombay"
    assert data["slug"] == "iit-bombay"
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_create_institution_duplicate_slug(client: AsyncClient):
    """Duplicate slug returns 409."""
    headers = make_auth_header(role=Role.SUPER_ADMIN)
    payload = {"name": "Test Inst", "slug": "test-inst"}

    resp1 = await client.post("/api/v1/institutions/", json=payload, headers=headers)
    assert resp1.status_code == 201

    resp2 = await client.post("/api/v1/institutions/", json=payload, headers=headers)
    assert resp2.status_code == 409


@pytest.mark.asyncio
async def test_list_institutions(client: AsyncClient):
    """List institutions returns paginated response."""
    headers = make_auth_header(role=Role.SUPER_ADMIN)

    # Create a few institutions
    for i in range(3):
        await client.post(
            "/api/v1/institutions/",
            json={"name": f"Institution {i}", "slug": f"inst-{i}"},
            headers=headers,
        )

    response = await client.get("/api/v1/institutions/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 3
    assert data["page"] == 1


@pytest.mark.asyncio
async def test_create_batch(client: AsyncClient):
    """Create a batch within an institution."""
    headers = make_auth_header(role=Role.SUPER_ADMIN)

    # Create institution
    inst_resp = await client.post(
        "/api/v1/institutions/",
        json={"name": "Test University", "slug": "test-uni"},
        headers=headers,
    )
    inst_id = inst_resp.json()["id"]

    # Create batch
    response = await client.post(
        f"/api/v1/institutions/{inst_id}/batches",
        json={"name": "CSE 2027", "year": 2027},
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "CSE 2027"
    assert data["year"] == 2027


@pytest.mark.asyncio
async def test_student_cannot_create_institution(client: AsyncClient):
    """Student role should be forbidden from creating institutions."""
    headers = make_auth_header(role=Role.STUDENT)
    response = await client.post(
        "/api/v1/institutions/",
        json={"name": "Hacker Inst", "slug": "hacker"},
        headers=headers,
    )
    assert response.status_code == 403
