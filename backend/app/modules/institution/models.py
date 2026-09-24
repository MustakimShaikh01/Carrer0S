"""
Institution module — ORM models.

Represents the top-level tenant entity. Each institution has batches,
and each batch contains students.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class Institution(Base):
    """An educational institution (college, bootcamp, training institute)."""

    __tablename__ = "institutions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default_factory=uuid.uuid4,
        init=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    domain: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)
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

    # Relationships
    batches: Mapped[list["Batch"]] = relationship(
        back_populates="institution",
        cascade="all, delete-orphan",
        init=False,
        default_factory=list,
    )

    def __repr__(self) -> str:
        return f"<Institution {self.slug}>"


class Batch(Base):
    """A cohort/batch within an institution (e.g., 'CSE 2027')."""

    __tablename__ = "batches"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default_factory=uuid.uuid4,
        init=False,
    )
    institution_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False,
    )

    # Relationships
    institution: Mapped["Institution"] = relationship(
        back_populates="batches",
        init=False,
    )

    def __repr__(self) -> str:
        return f"<Batch {self.name} ({self.year})>"
