"""
Student module — service layer.
"""

import uuid

from sqlalchemy import select, func as sqlfunc
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.events import Topics, get_event_publisher
from backend.app.modules.student.models import Student
from backend.app.modules.student.schemas import (
    StudentBulkImport,
    StudentCreate,
    StudentUpdate,
)
from backend.app.shared.exceptions import DuplicateError, NotFoundError


class StudentService:
    """Business logic for student management."""

    def __init__(self, db: AsyncSession, tenant_id: str):
        self.db = db
        self.tenant_id = tenant_id

    async def create_student(self, data: StudentCreate) -> Student:
        """Create a single student."""
        existing = await self.db.execute(
            select(Student).where(Student.email == data.email)
        )
        if existing.scalar_one_or_none():
            raise DuplicateError("Student", "email", data.email)

        student = Student(
            tenant_id=uuid.UUID(self.tenant_id),
            batch_id=data.batch_id,
            email=data.email,
            full_name=data.full_name,
            phone=data.phone,
            career_track=data.career_track,
        )
        self.db.add(student)
        await self.db.flush()
        return student

    async def bulk_import(self, data: StudentBulkImport) -> dict:
        """Bulk import students from CSV data. Publishes event for async processing."""
        publisher = get_event_publisher()

        # Publish bulk import event for async processing
        message_id = await publisher.publish(
            Topics.BULK_IMPORT,
            {
                "tenant_id": self.tenant_id,
                "batch_id": str(data.batch_id),
                "students": [s.model_dump() for s in data.students],
            },
        )

        return {
            "message": f"Bulk import of {len(data.students)} students queued",
            "job_id": message_id,
            "count": len(data.students),
        }

    async def get_student(self, student_id: uuid.UUID) -> Student:
        """Get a student by ID, scoped to current tenant."""
        result = await self.db.execute(
            select(Student).where(
                Student.id == student_id,
                Student.tenant_id == uuid.UUID(self.tenant_id),
            )
        )
        student = result.scalar_one_or_none()
        if not student:
            raise NotFoundError("Student", str(student_id))
        return student

    async def list_students(
        self,
        batch_id: uuid.UUID | None = None,
        offset: int = 0,
        limit: int = 25,
    ) -> tuple[list[Student], int]:
        """List students for the current tenant, optionally filtered by batch."""
        query = select(Student).where(
            Student.tenant_id == uuid.UUID(self.tenant_id)
        )
        count_query = select(sqlfunc.count(Student.id)).where(
            Student.tenant_id == uuid.UUID(self.tenant_id)
        )

        if batch_id:
            query = query.where(Student.batch_id == batch_id)
            count_query = count_query.where(Student.batch_id == batch_id)

        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0

        result = await self.db.execute(
            query.order_by(Student.full_name).offset(offset).limit(limit)
        )
        return list(result.scalars().all()), total

    async def update_student(
        self, student_id: uuid.UUID, data: StudentUpdate
    ) -> Student:
        """Update a student profile."""
        student = await self.get_student(student_id)
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(student, field, value)
        await self.db.flush()
        return student
