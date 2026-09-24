"""
Institution module — API routes.
"""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.security import Role, require_role
from backend.app.modules.institution.schemas import (
    BatchCreate,
    BatchResponse,
    InstitutionCreate,
    InstitutionResponse,
    InstitutionUpdate,
)
from backend.app.modules.institution.service import InstitutionService
from backend.app.shared.pagination import PaginatedResponse, PaginationParams

router = APIRouter()


def get_service(db: Annotated[AsyncSession, Depends(get_db)]) -> InstitutionService:
    return InstitutionService(db)


# ── Institution CRUD ─────────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=InstitutionResponse,
    status_code=201,
    dependencies=[Depends(require_role(Role.SUPER_ADMIN))],
)
async def create_institution(
    data: InstitutionCreate,
    service: Annotated[InstitutionService, Depends(get_service)],
):
    """Create a new institution. Requires SUPER_ADMIN role."""
    institution = await service.create_institution(data)
    return institution


@router.get("/", response_model=PaginatedResponse[InstitutionResponse])
async def list_institutions(
    service: Annotated[InstitutionService, Depends(get_service)],
    pagination: Annotated[PaginationParams, Depends()],
):
    """List all institutions with pagination."""
    items, total = await service.list_institutions(
        offset=pagination.offset, limit=pagination.limit
    )
    return PaginatedResponse.create(items, total, pagination)


@router.get("/{institution_id}", response_model=InstitutionResponse)
async def get_institution(
    institution_id: uuid.UUID,
    service: Annotated[InstitutionService, Depends(get_service)],
):
    """Get a single institution by ID."""
    return await service.get_institution(institution_id)


@router.patch(
    "/{institution_id}",
    response_model=InstitutionResponse,
    dependencies=[Depends(require_role(Role.SUPER_ADMIN, Role.INSTITUTION_ADMIN))],
)
async def update_institution(
    institution_id: uuid.UUID,
    data: InstitutionUpdate,
    service: Annotated[InstitutionService, Depends(get_service)],
):
    """Update an institution. Requires SUPER_ADMIN or INSTITUTION_ADMIN role."""
    return await service.update_institution(institution_id, data)


# ── Batch CRUD ───────────────────────────────────────────────────────────────
@router.post(
    "/{institution_id}/batches",
    response_model=BatchResponse,
    status_code=201,
    dependencies=[Depends(require_role(Role.SUPER_ADMIN, Role.INSTITUTION_ADMIN))],
)
async def create_batch(
    institution_id: uuid.UUID,
    data: BatchCreate,
    service: Annotated[InstitutionService, Depends(get_service)],
):
    """Create a batch within an institution."""
    return await service.create_batch(institution_id, data)


@router.get("/{institution_id}/batches", response_model=list[BatchResponse])
async def list_batches(
    institution_id: uuid.UUID,
    service: Annotated[InstitutionService, Depends(get_service)],
):
    """List all batches for an institution."""
    return await service.list_batches(institution_id)
