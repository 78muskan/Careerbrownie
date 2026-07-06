"""Short-term conversation memory — backed by Django cache (Redis in production).

Stores conversation turns per session_id.
TTL: 1 hour (configurable via BRAIN_CONV_TTL_SECS in settings).
Max turns kept: BRAIN_CONV_MAX_TURNS (default 10 turns = 20 messages).
"""
from __future__ import annotations

import json
import logging

from django.conf import settings
from django.core.cache import cache

log = logging.getLogger("careerbrain.memory.short_term")

_PREFIX = "brain:conv:"
_MAX_TURNS: int = getattr(settings, "BRAIN_CONV_MAX_TURNS", 10)
_TTL: int = getattr(settings, "BRAIN_CONV_TTL_SECS", 3600)


class ConversationMemory:
    """Redis-backed conversation history per session."""

    def load(self, session_id: str) -> list[dict]:
        """Return the current conversation history for a session."""
        raw = cache.get(f"{_PREFIX}{session_id}")
        if not raw:
            return []
        try:
            return json.loads(raw)
        except Exception:
            return []

    def append(self, session_id: str, user_message: str, assistant_reply: str) -> None:
        """Append a user/assistant turn and persist back to cache."""
        history = self.load(session_id)
        history.extend([
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": assistant_reply},
        ])
        max_messages = _MAX_TURNS * 2
        if len(history) > max_messages:
            history = history[-max_messages:]
        cache.set(f"{_PREFIX}{session_id}", json.dumps(history), timeout=_TTL)

    def clear(self, session_id: str) -> None:
        cache.delete(f"{_PREFIX}{session_id}")

    def length(self, session_id: str) -> int:
        return len(self.load(session_id)) // 2
