"""
Student module — ORM models.

Students belong to a batch (and thus an institution). They connect
their GitHub account, submit resumes, and build career evidence.
"""

import uuid
from datetime import datetime, timezone
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class CareerTrack(StrEnum):
    """Supported career tracks for analysis."""

    BACKEND = "backend"
    FRONTEND = "frontend"
    FULLSTACK = "fullstack"
    DATA_ENGINEERING = "data_engineering"
    AI_ML = "ai_ml"
    DEVOPS = "devops"
    MOBILE = "mobile"
    UNDECIDED = "undecided"


class Student(Base):
    """A student in the CareerOS system."""

    __tablename__ = "students"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default_factory=uuid.uuid4,
        init=False,
    )
    # Multi-tenancy: every student belongs to an institution
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )
    batch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("batches.id"),
        nullable=False,
    )

    # Profile
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True, default=None)
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)

    # GitHub integration
    github_username: Mapped[str | None] = mapped_column(
        String(100), nullable=True, default=None
    )
    github_connected: Mapped[bool] = mapped_column(default=False)
    github_access_token: Mapped[str | None] = mapped_column(
        Text, nullable=True, default=None
    )

    # Career intelligence
    career_track: Mapped[str] = mapped_column(
        String(50), default=CareerTrack.UNDECIDED
    )
    skill_snapshot: Mapped[dict | None] = mapped_column(
        JSONB, nullable=True, default=None, init=False
    )  # Latest computed skill map
    evidence_score: Mapped[float | None] = mapped_column(
        nullable=True, default=None, init=False
    )

    # Auth
    hashed_password: Mapped[str | None] = mapped_column(
        Text, nullable=True, default=None
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        init=False,
    )

    def __repr__(self) -> str:
        return f"<Student {self.email}>"
