# ────────────────────────────────────────────────────────────────────
# CareerOS — Makefile
# ────────────────────────────────────────────────────────────────────
.PHONY: help dev infra backend frontend migrate seed test lint clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── Infrastructure ───────────────────────────────────────────────────
infra: ## Start local infrastructure (Postgres, Redis, Pub/Sub)
	docker compose up -d

infra-down: ## Stop local infrastructure
	docker compose down

infra-reset: ## Reset all local data
	docker compose down -v
	docker compose up -d

# ── Backend ──────────────────────────────────────────────────────────
backend-install: ## Install backend dependencies
	cd backend && pip install -e ".[dev]"

backend: ## Start FastAPI dev server
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# ── Frontend ─────────────────────────────────────────────────────────
frontend-install: ## Install frontend dependencies
	cd frontend && npm install

frontend: ## Start Next.js dev server
	cd frontend && npm run dev

# ── Database ─────────────────────────────────────────────────────────
migrate: ## Run Alembic migrations
	cd backend && alembic upgrade head

migrate-new: ## Create a new migration (usage: make migrate-new MSG="add users table")
	cd backend && alembic revision --autogenerate -m "$(MSG)"

seed: ## Seed database with demo data
	cd backend && python -m scripts.seed

# ── Development ──────────────────────────────────────────────────────
dev: infra ## Start everything for local development
	@echo "Infrastructure is up. Run 'make backend' and 'make frontend' in separate terminals."

# ── Quality ──────────────────────────────────────────────────────────
lint: ## Run linter (ruff)
	cd backend && ruff check . --fix
	cd backend && ruff format .

typecheck: ## Run type checker (mypy)
	cd backend && mypy app/

test: ## Run backend tests
	cd backend && pytest -v

test-cov: ## Run tests with coverage
	cd backend && pytest --cov=app --cov-report=html

# ── Cleanup ──────────────────────────────────────────────────────────
clean: ## Remove caches and build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .ruff_cache -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
