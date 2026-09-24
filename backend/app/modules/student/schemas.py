"""
Student module — Pydantic schemas.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class StudentCreate(BaseModel):
    """Request: create or import a single student."""

    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    batch_id: uuid.UUID
    phone: str | None = None
    career_track: str = "undecided"


class StudentBulkImportRow(BaseModel):
    """A single row from a CSV bulk import."""

    email: EmailStr
    full_name: str
    phone: str | None = None
    career_track: str = "undecided"


class StudentBulkImport(BaseModel):
    """Request: bulk import students into a batch."""

    batch_id: uuid.UUID
    students: list[StudentBulkImportRow] = Field(..., min_length=1, max_length=5000)


class StudentUpdate(BaseModel):
    """Request: update student profile (partial)."""

    full_name: str | None = None
    phone: str | None = None
    career_track: str | None = None
    github_username: str | None = None


class StudentResponse(BaseModel):
    """Response: student details."""

    id: uuid.UUID
    tenant_id: uuid.UUID
    batch_id: uuid.UUID
    email: str
    full_name: str
    phone: str | None
    avatar_url: str | None
    github_username: str | None
    github_connected: bool
    career_track: str
    evidence_score: float | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class StudentDashboard(BaseModel):
    """Response: student-facing dashboard summary."""

    student: StudentResponse
    skill_snapshot: dict | None = None
    top_skills: list[str] = []
    missing_skills: list[str] = []
    weekly_recommendations: list[str] = []
