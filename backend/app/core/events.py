"""
Pub/Sub event publisher.

Abstracts Google Cloud Pub/Sub behind a simple interface so workers can
consume events without coupling to the publisher's implementation.

In local development, falls back to an in-memory queue for testing.
"""

import json
import logging
from typing import Any, Protocol

from backend.app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class EventPublisher(Protocol):
    """Interface for publishing domain events."""

    async def publish(self, topic: str, data: dict[str, Any]) -> str: ...


class PubSubPublisher:
    """Google Cloud Pub/Sub publisher."""

    def __init__(self):
        # Lazy import — only needed in staging/production
        from google.cloud import pubsub_v1

        self._client = pubsub_v1.PublisherClient()
        self._project = settings.gcp_project_id

    async def publish(self, topic: str, data: dict[str, Any]) -> str:
        full_topic = f"projects/{self._project}/topics/{settings.pubsub_topic_prefix}-{topic}"
        future = self._client.publish(
            full_topic,
            json.dumps(data).encode("utf-8"),
        )
        message_id = future.result()
        logger.info("Published event to %s: %s", full_topic, message_id)
        return message_id


class InMemoryPublisher:
    """In-memory publisher for local development and testing."""

    def __init__(self):
        self.messages: list[tuple[str, dict[str, Any]]] = []

    async def publish(self, topic: str, data: dict[str, Any]) -> str:
        self.messages.append((topic, data))
        message_id = f"local-{len(self.messages)}"
        logger.info("Published event to [local] %s: %s", topic, message_id)
        return message_id

    def clear(self):
        self.messages.clear()


# ── Factory ──────────────────────────────────────────────────────────────────
_publisher: EventPublisher | None = None


def get_event_publisher() -> EventPublisher:
    """Return the appropriate publisher for the current environment."""
    global _publisher
    if _publisher is None:
        if settings.is_production or settings.gcp_project_id:
            _publisher = PubSubPublisher()
        else:
            _publisher = InMemoryPublisher()
    return _publisher


# ── Topic constants ──────────────────────────────────────────────────────────
class Topics:
    """Well-known event topic names."""

    GITHUB_SYNC = "github-sync"
    RESUME_PARSE = "resume-parse"
    CODING_ASSESS = "coding-assess"
    CAREER_ANALYZE = "career-analyze"
    BULK_IMPORT = "bulk-import"
    NOTIFICATION = "notification"
