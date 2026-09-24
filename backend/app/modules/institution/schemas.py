"""
Institution module — Pydantic schemas for request/response validation.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


# ── Institution ──────────────────────────────────────────────────────────────
class InstitutionCreate(BaseModel):
    """Request: create a new institution."""

    name: str = Field(..., min_length=2, max_length=255, examples=["IIT Bombay"])
    slug: str = Field(
        ...,
        min_length=2,
        max_length=100,
        pattern=r"^[a-z0-9\-]+$",
        examples=["iit-bombay"],
    )
    domain: str | None = Field(default=None, examples=["iitb.ac.in"])
    logo_url: str | None = None


class InstitutionUpdate(BaseModel):
    """Request: update an institution (partial)."""

    name: str | None = Field(default=None, min_length=2, max_length=255)
    domain: str | None = None
    logo_url: str | None = None
    is_active: bool | None = None


class InstitutionResponse(BaseModel):
    """Response: institution details."""

    id: uuid.UUID
    name: str
    slug: str
    domain: str | None
    logo_url: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Batch ────────────────────────────────────────────────────────────────────
class BatchCreate(BaseModel):
    """Request: create a new batch within an institution."""

    name: str = Field(..., min_length=1, max_length=255, examples=["CSE 2027"])
    year: int = Field(..., ge=2020, le=2035, examples=[2027])


class BatchResponse(BaseModel):
    """Response: batch details."""

    id: uuid.UUID
    institution_id: uuid.UUID
    name: str
    year: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
