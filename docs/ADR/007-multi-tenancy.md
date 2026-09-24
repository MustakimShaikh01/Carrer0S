# ADR-007: Multi-Tenancy Strategy

**Status:** Accepted
**Date:** 2026-09-24
**Deciders:** @mustakimshaikh

## Context

CareerOS is a B2B SaaS platform serving multiple educational institutions. Each institution's data must be isolated from others. We need a multi-tenancy strategy.

## Decision

We will use **shared schema with a `tenant_id` column** on all tenant-scoped tables.

Tenant isolation is enforced at three levels:
1. **Middleware** — Extracts `tenant_id` (called `tid`) from the JWT and sets it in a context variable
2. **Service layer** — All queries include a `WHERE tenant_id = :tid` filter
3. **Future: Row-level security** — PostgreSQL RLS policies as an additional safeguard

## Rationale

1. **Simplicity** — No schema management complexity. Standard SQL, standard ORMs, standard migrations.
2. **Cost** — One database connection pool serves all tenants. No per-tenant database provisioning.
3. **Query flexibility** — Cross-tenant analytics (for super admins) are simple `GROUP BY tenant_id` queries.
4. **Scale path** — If a single tenant outgrows shared infrastructure, we can implement schema-per-tenant or database-per-tenant for that specific tenant.

## Implementation

```python
# Student model — tenant_id is mandatory, indexed
class Student(Base):
    __tablename__ = "students"
    tenant_id: Mapped[uuid.UUID] = mapped_column(index=True, nullable=False)
    ...

# Service layer — all queries scoped
class StudentService:
    def __init__(self, db: AsyncSession, tenant_id: str):
        self.tenant_id = tenant_id

    async def list_students(self):
        return await self.db.execute(
            select(Student).where(Student.tenant_id == self.tenant_id)
        )
```

## Consequences

- **Positive:** Fast to implement, easy to reason about, low operational cost
- **Negative:** Risk of data leak if a developer forgets the tenant filter
- **Mitigation:** Code review checklist, integration tests that verify tenant isolation, eventual PostgreSQL RLS policies

## Alternatives Considered

| Strategy | Complexity | Isolation | Rejected because |
|---|---|---|---|
| Schema-per-tenant | Medium | Medium | Adds migration complexity for every tenant |
| Database-per-tenant | High | High | Excessive for < 50 institutions at launch |
