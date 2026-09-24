"""
Institution module — service layer (business logic).
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.modules.institution.models import Batch, Institution
from backend.app.modules.institution.schemas import (
    BatchCreate,
    InstitutionCreate,
    InstitutionUpdate,
)
from backend.app.shared.exceptions import DuplicateError, NotFoundError


class InstitutionService:
    """Business logic for institution management."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_institution(self, data: InstitutionCreate) -> Institution:
        """Create a new institution. Raises DuplicateError if slug exists."""
        existing = await self.db.execute(
            select(Institution).where(Institution.slug == data.slug)
        )
        if existing.scalar_one_or_none():
            raise DuplicateError("Institution", "slug", data.slug)

        institution = Institution(
            name=data.name,
            slug=data.slug,
            domain=data.domain,
            logo_url=data.logo_url,
        )
        self.db.add(institution)
        await self.db.flush()
        return institution

    async def get_institution(self, institution_id: uuid.UUID) -> Institution:
        """Get institution by ID. Raises NotFoundError if missing."""
        result = await self.db.execute(
            select(Institution).where(Institution.id == institution_id)
        )
        institution = result.scalar_one_or_none()
        if not institution:
            raise NotFoundError("Institution", str(institution_id))
        return institution

    async def list_institutions(
        self, offset: int = 0, limit: int = 25
    ) -> tuple[list[Institution], int]:
        """List all institutions with pagination."""
        count_result = await self.db.execute(
            select(Institution.id)
        )
        total = len(count_result.all())

        result = await self.db.execute(
            select(Institution)
            .order_by(Institution.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all()), total

    async def update_institution(
        self, institution_id: uuid.UUID, data: InstitutionUpdate
    ) -> Institution:
        """Partial update of an institution."""
        institution = await self.get_institution(institution_id)
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(institution, field, value)
        await self.db.flush()
        return institution

    async def create_batch(
        self, institution_id: uuid.UUID, data: BatchCreate
    ) -> Batch:
        """Create a batch within an institution."""
        # Verify institution exists
        await self.get_institution(institution_id)

        batch = Batch(
            institution_id=institution_id,
            name=data.name,
            year=data.year,
        )
        self.db.add(batch)
        await self.db.flush()
        return batch

    async def list_batches(
        self, institution_id: uuid.UUID
    ) -> list[Batch]:
        """List all batches for an institution."""
        result = await self.db.execute(
            select(Batch)
            .where(Batch.institution_id == institution_id)
            .order_by(Batch.year.desc(), Batch.name)
        )
        return list(result.scalars().all())
