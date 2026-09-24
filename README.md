# CareerOS

> **Technical career intelligence platform** — measures demonstrated skills, identifies gaps, recommends actions, and gives institutions actionable intervention analytics.

```
CareerOS tells every CSE student what evidence they have,
what they are missing, and exactly what they should do next.
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Next.js 16 Frontend                          │
│                 (TypeScript + Tailwind + shadcn/ui)             │
└───────────────────────────┬─────────────────────────────────────┘
                            │ REST API
┌───────────────────────────▼─────────────────────────────────────┐
│                 FastAPI Backend (Modular Monolith)               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────────────┐ │
│  │ Identity │ │ Student  │ │Institut. │ │ Career Intel.      │ │
│  │          │ │          │ │          │ │ ┌────┐ ┌────┐      │ │
│  │ Auth     │ │ Profile  │ │ Batches  │ │ │Skill│ │Gap │      │ │
│  │ RBAC     │ │ Import   │ │ CRUD     │ │ │Eng. │ │Det.│      │ │
│  └──────────┘ └──────────┘ └──────────┘ └─┴────┴─┴────┴──────┘ │
│  ┌──────────┐ ┌──────────────────────┐  ┌────────────────────┐  │
│  │Analytics │ │ Evidence             │  │ Intervention       │  │
│  │          │ │ ┌──────┐ ┌────────┐  │  │ Mentors, Workshops │  │
│  │ Cohort   │ │ │GitHub│ │Resume  │  │  └────────────────────┘  │
│  │ Insights │ │ │      │ │        │  │                          │
│  └──────────┘ │ └──────┘ └────────┘  │                          │
│               └──────────────────────┘                          │
└───┬───────────────────┬───────────────────┬─────────────────────┘
    │                   │                   │
┌───▼──┐          ┌─────▼──┐         ┌──────▼──────┐
│Postgr│          │ Redis  │         │ Google Cloud│
│  SQL │          │        │         │   Pub/Sub   │
│pgvect│          │Cache   │         │             │
│  or  │          │Rate Lim│         │  ┌─────┐    │
└──────┘          └────────┘         │  │Work.│    │
                                     └──┴─────┴───┘
```

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16 + TypeScript |
| UI | Tailwind CSS + shadcn/ui |
| Backend | FastAPI + Python 3.12 |
| ORM | SQLAlchemy 2 (async) |
| Database | PostgreSQL 16 + pgvector |
| Cache | Redis 7 |
| Events | Google Cloud Pub/Sub |
| Storage | Google Cloud Storage |
| Compute | Google Cloud Run |
| AI | Vertex AI / Gemini |
| IaC | Terraform |

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 20+
- Docker & Docker Compose

### 1. Start infrastructure
```bash
make infra
```

### 2. Install dependencies
```bash
make backend-install
make frontend-install
```

### 3. Set up environment
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your values
```

### 4. Run migrations
```bash
make migrate
```

### 5. Start development servers
```bash
# Terminal 1
make backend

# Terminal 2
make frontend
```

### 6. Open
- **API docs:** http://localhost:8000/docs
- **Frontend:** http://localhost:3000

## Project Structure

```
careeros/
├── frontend/          # Next.js 16 + TypeScript
├── backend/           # FastAPI modular monolith
│   ├── app/
│   │   ├── core/      # Config, database, security, events
│   │   ├── modules/   # Domain modules (identity, student, institution, ...)
│   │   └── shared/    # Pagination, exceptions, multi-tenancy
│   └── alembic/       # Database migrations
├── workers/           # Pub/Sub consumers (GitHub, resume, coding, career)
├── infrastructure/    # Terraform
├── docs/
│   └── ADR/           # Architecture Decision Records
├── docker-compose.yml # Local development infrastructure
└── Makefile           # Developer commands
```

## Architecture Decision Records

| ADR | Title |
|---|---|
| [001](docs/ADR/001-why-postgresql.md) | Why PostgreSQL + pgvector |
| [002](docs/ADR/002-modular-monolith.md) | Modular Monolith Architecture |
| [007](docs/ADR/007-multi-tenancy.md) | Multi-Tenancy Strategy |

## License

MIT
