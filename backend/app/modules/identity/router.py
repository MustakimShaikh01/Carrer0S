"""
Identity module — placeholder router for auth endpoints.

Will be expanded with login, register, refresh token, and OAuth flows.
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
async def login():
    """Authenticate a user and return JWT tokens.

    TODO: Implement with email/password + OAuth.
    """
    return {"message": "Auth endpoint — implementation pending"}


@router.post("/register")
async def register():
    """Register a new user (institution admin or student).

    TODO: Implement with invitation-based registration.
    """
    return {"message": "Registration endpoint — implementation pending"}


@router.post("/refresh")
async def refresh_token():
    """Refresh an expired access token.

    TODO: Implement JWT refresh flow.
    """
    return {"message": "Token refresh endpoint — implementation pending"}
