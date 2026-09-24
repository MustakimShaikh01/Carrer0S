"""
Tests for the identity (auth) module.
"""

import pytest
from httpx import AsyncClient

from tests.backend.conftest import make_auth_header


@pytest.mark.asyncio
async def test_register_super_admin(client: AsyncClient):
    """Super admins can register without a tenant_id."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "admin@careeros.dev",
            "full_name": "Super Admin",
            "password": "securepassword123",
            "role": "super_admin",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "admin@careeros.dev"
    assert data["role"] == "super_admin"
    assert data["tenant_id"] is None


@pytest.mark.asyncio
async def test_register_institution_admin_requires_tenant(client: AsyncClient):
    """Non-super_admin users must have a tenant_id."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "admin@iitb.ac.in",
            "full_name": "Inst Admin",
            "password": "securepassword123",
            "role": "institution_admin",
            # No tenant_id
        },
    )
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Duplicate email should return 409."""
    payload = {
        "email": "duplicate@careeros.dev",
        "full_name": "First User",
        "password": "securepassword123",
        "role": "super_admin",
    }
    response1 = await client.post("/api/v1/auth/register", json=payload)
    assert response1.status_code == 201

    response2 = await client.post("/api/v1/auth/register", json=payload)
    assert response2.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Login with valid credentials returns JWT pair."""
    # Register first
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@careeros.dev",
            "full_name": "Login User",
            "password": "securepassword123",
            "role": "super_admin",
        },
    )

    # Login
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "login@careeros.dev", "password": "securepassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] > 0


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Login with wrong password returns 422."""
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "wrongpass@careeros.dev",
            "full_name": "User",
            "password": "correctpassword",
            "role": "super_admin",
        },
    )

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "wrongpass@careeros.dev", "password": "wrongpassword"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_me_endpoint(client: AsyncClient):
    """Authenticated user can access /me endpoint."""
    # Register and login
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "me@careeros.dev",
            "full_name": "Me User",
            "password": "securepassword123",
            "role": "super_admin",
        },
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "me@careeros.dev", "password": "securepassword123"},
    )
    token = login_resp.json()["access_token"]

    # Access /me
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@careeros.dev"
    assert data["role"] == "super_admin"


@pytest.mark.asyncio
async def test_refresh_token_rotation(client: AsyncClient):
    """Refresh token should return new pair and invalidate old token."""
    # Register and login
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "refresh@careeros.dev",
            "full_name": "Refresh User",
            "password": "securepassword123",
            "role": "super_admin",
        },
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "refresh@careeros.dev", "password": "securepassword123"},
    )
    refresh_token = login_resp.json()["refresh_token"]

    # Use refresh token
    response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    new_tokens = response.json()
    assert "access_token" in new_tokens
    assert new_tokens["refresh_token"] != refresh_token  # New token issued

    # Old refresh token should be revoked
    response2 = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response2.status_code == 422  # Revoked
