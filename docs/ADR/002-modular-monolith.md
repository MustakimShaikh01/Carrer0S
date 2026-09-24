# ADR-002: Modular Monolith Architecture

**Status:** Accepted
**Date:** 2026-09-24
**Deciders:** @mustakimshaikh

## Context

CareerOS is a new product with evolving domain boundaries. We need to decide between:
1. **Microservices** — Separate deployable services from day one
2. **Monolith** — Single application with no internal structure
3. **Modular monolith** — Single deployable unit with well-defined internal module boundaries

## Decision

We will use a **modular monolith** architecture with FastAPI as the backend framework.

The application is organized into domain modules (`identity`, `student`, `institution`, `evidence`, `career_intelligence`, `intervention`, `analytics`), each with its own router, service, models, and schemas. Modules communicate through direct Python imports (service-to-service calls), not HTTP or message queues.

Background processing (GitHub sync, resume parsing, career analysis) runs as separate **worker processes** consuming from Pub/Sub, but they share the same codebase and database.

## Rationale

1. **Domain boundaries are unclear** — We don't yet know if "Evidence" and "Career Intelligence" are separate bounded contexts or tightly coupled. A modular monolith lets us discover real boundaries through code before committing to service extraction.

2. **Developer velocity** — One repo, one deployment, one database. No inter-service communication overhead, no distributed transaction complexity, no service mesh.

3. **Refactoring safety** — Python imports create compile-time (or import-time) coupling. If a module changes its interface, dependent modules break immediately — not at runtime in production.

4. **Extraction path** — When a module grows complex enough to justify its own service (e.g., the evidence pipeline processes 10x more traffic), we can extract it by:
   - Replacing direct imports with HTTP/gRPC calls
   - Moving the module to its own deployment
   - Keeping the same database initially, then splitting later

## Module Structure

```
backend/app/modules/
├── identity/          # Auth, users, RBAC
├── student/           # Student profiles, onboarding
├── institution/       # Institution + batch management
├── evidence/          # GitHub, resume, coding evidence
│   ├── github/
│   ├── resume/
│   └── coding/
├── career_intelligence/  # Skill engine, gap detection, recommendations
├── intervention/      # Mentor assignments, workshops
└── analytics/         # Institutional dashboards, cohort analytics
```

## Rules

1. **No circular imports between modules** — If module A depends on module B, module B must NOT depend on module A
2. **Shared code goes in `app/shared/`** — Pagination, exceptions, multi-tenancy middleware
3. **Events for cross-cutting concerns** — Use Pub/Sub events when a module needs to notify others without coupling (e.g., "student connected GitHub" → triggers evidence pipeline)
4. **No direct model access across modules** — Module A should call Module B's service, not query Module B's tables directly

## Consequences

- **Positive:** Fast development, simple deployment, clear internal structure
- **Negative:** All modules share a process — a bug in one module can affect others
- **Mitigation:** Strong testing discipline, structured logging per module, feature flags for new modules

## When to Extract a Service

Extract a module into its own service when:
- It has fundamentally different scaling requirements
- It has a different team ownership boundary
- It needs a different technology (e.g., a Go-based worker for CPU-intensive analysis)
- It accounts for > 50% of the monolith's resource usage
