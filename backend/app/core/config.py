"""
Application configuration using pydantic-settings.
All config is loaded from environment variables with sensible defaults for local development.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """CareerOS application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="CAREEROS_",
    )

    # ── App ──────────────────────────────────────────────────────────────
    app_name: str = "CareerOS"
    app_version: str = "0.1.0"
    environment: Literal["local", "staging", "production"] = "local"
    debug: bool = True
    log_level: str = "INFO"

    # ── API ──────────────────────────────────────────────────────────────
    api_v1_prefix: str = "/api/v1"
    allowed_origins: list[str] = ["http://localhost:3000"]

    # ── Database ─────────────────────────────────────────────────────────
    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://careeros:careeros@localhost:5432/careeros"
    )
    database_pool_size: int = 20
    database_max_overflow: int = 10
    database_echo: bool = False

    # ── Redis ────────────────────────────────────────────────────────────
    redis_url: RedisDsn = Field(default="redis://localhost:6379/0")

    # ── Auth / JWT ───────────────────────────────────────────────────────
    jwt_secret_key: str = "CHANGE-ME-IN-PRODUCTION"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # ── Google Cloud ─────────────────────────────────────────────────────
    gcp_project_id: str = ""
    gcs_bucket_name: str = "careeros-uploads"
    pubsub_topic_prefix: str = "careeros"

    # ── GitHub App ───────────────────────────────────────────────────────
    github_app_id: str = ""
    github_app_private_key: str = ""
    github_client_id: str = ""
    github_client_secret: str = ""
    github_webhook_secret: str = ""

    # ── Vertex AI ────────────────────────────────────────────────────────
    vertex_ai_location: str = "us-central1"
    vertex_ai_model: str = "gemini-2.0-flash"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance — reads env/file once."""
    return Settings()
