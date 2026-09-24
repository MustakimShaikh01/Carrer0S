"""
Student module — API routes.
"""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.security import Role, TokenPayload, get_current_user, require_role
from backend.app.modules.student.schemas import (
    StudentBulkImport,
    StudentCreate,
    StudentResponse,
    StudentUpdate,
)
from backend.app.modules.student.service import StudentService
from backend.app.shared.multi_tenancy import ensure_tenant
from backend.app.shared.pagination import PaginatedResponse, PaginationParams

router = APIRouter()


def get_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[str, Depends(ensure_tenant)],
) -> StudentService:
    return StudentService(db, tenant_id)


# ── Student CRUD ─────────────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=StudentResponse,
    status_code=201,
    dependencies=[Depends(require_role(Role.SUPER_ADMIN, Role.INSTITUTION_ADMIN))],
)
async def create_student(
    data: StudentCreate,
    service: Annotated[StudentService, Depends(get_service)],
):
    """Create a single student."""
    return await service.create_student(data)


@router.post(
    "/bulk-import",
    status_code=202,
    dependencies=[Depends(require_role(Role.SUPER_ADMIN, Role.INSTITUTION_ADMIN))],
)
async def bulk_import_students(
    data: StudentBulkImport,
    service: Annotated[StudentService, Depends(get_service)],
):
    """Bulk import students. Queues an async job and returns 202."""
    return await service.bulk_import(data)


@router.get("/", response_model=PaginatedResponse[StudentResponse])
async def list_students(
    service: Annotated[StudentService, Depends(get_service)],
    pagination: Annotated[PaginationParams, Depends()],
    batch_id: uuid.UUID | None = Query(default=None),
):
    """List students for the current tenant."""
    items, total = await service.list_students(
        batch_id=batch_id,
        offset=pagination.offset,
        limit=pagination.limit,
    )
    return PaginatedResponse.create(items, total, pagination)


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: uuid.UUID,
    service: Annotated[StudentService, Depends(get_service)],
):
    """Get a single student by ID."""
    return await service.get_student(student_id)


@router.patch(
    "/{student_id}",
    response_model=StudentResponse,
)
async def update_student(
    student_id: uuid.UUID,
    data: StudentUpdate,
    service: Annotated[StudentService, Depends(get_service)],
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
):
    """Update a student profile. Students can update their own; admins can update any."""
    if current_user.role == Role.STUDENT and current_user.sub != str(student_id):
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Students can only update their own profile",
        )
    return await service.update_student(student_id, data)
