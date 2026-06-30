from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import Optional

from app.core.config import settings
from app.core.logging import get_logger

log = get_logger(__name__)

_redis = None


def _get_redis():
    global _redis
    if _redis is None:
        import redis.asyncio as aioredis
        _redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis


@dataclass
class Turn:
    role: str  # user | assistant
    content: str
    metadata: dict | None = None


class ConversationMemory:
    def __init__(self, session_id: str) -> None:
        self._key = f"cb:chat:{session_id}"
        self._ttl = settings.MEMORY_TTL
        self._max = settings.MEMORY_MAX_TURNS

    async def append(self, role: str, content: str, metadata: dict | None = None) -> None:
        r = _get_redis()
        turn = json.dumps({"role": role, "content": content, "metadata": metadata or {}})
        await r.rpush(self._key, turn)
        await r.ltrim(self._key, -self._max * 2, -1)
        await r.expire(self._key, self._ttl)

    async def get_history(self, last_n: int | None = None) -> list[Turn]:
        r = _get_redis()
        raw = await r.lrange(self._key, 0, -1)
        turns = [Turn(**json.loads(t)) for t in raw]
        if last_n:
            turns = turns[-last_n:]
        return turns

    async def clear(self) -> None:
        await _get_redis().delete(self._key)

    async def set_profile(self, profile: dict) -> None:
        r = _get_redis()
        await r.set(f"cb:profile:{self._key}", json.dumps(profile), ex=self._ttl)

    async def get_profile(self) -> dict:
        r = _get_redis()
        raw = await r.get(f"cb:profile:{self._key}")
        return json.loads(raw) if raw else {}
