"""Query-level caching with Redis primary and in-memory LRU fallback.

Strategy
--------
- Cache key: SHA-256 hash of (query + domain + student_profile_hash)
- TTL: configurable via CACHE_TTL_SECS (default 1 hour)
- Redis: used when REDIS_URL is set and reachable; async-safe via threading lock
- In-memory LRU: automatic fallback when Redis is unavailable; evicts oldest entries
  when CACHE_MAX_MEMORY limit is hit

Usage::

    cache = RAGCache()
    key = cache.make_key("what is JEE?", domain="exam")
    cached = cache.get(key)
    if cached:
        return RAGResponse(**cached)
    # ... compute response ...
    cache.set(key, response.to_dict())
"""
from __future__ import annotations

import hashlib
import json
import logging
import threading
import time
from collections import OrderedDict
from typing import Any

from app.config import settings

log = logging.getLogger(__name__)


class RAGCache:
    """
    Thread-safe cache with Redis primary and in-memory LRU fallback.

    Args:
        redis_url: Redis connection string.  If empty, uses in-memory only.
        ttl: Seconds before a cached entry expires.
        max_memory: Maximum entries in the in-memory cache (LRU eviction).
    """

    def __init__(
        self,
        redis_url: str = settings.REDIS_URL,
        ttl: int = settings.CACHE_TTL_SECS,
        max_memory: int = settings.CACHE_MAX_MEMORY,
    ) -> None:
        self._ttl = ttl
        self._max_memory = max_memory
        self._lock = threading.Lock()
        self._redis = self._connect_redis(redis_url)
        # OrderedDict preserves insertion order for LRU eviction
        self._memory: OrderedDict[str, tuple[Any, float]] = OrderedDict()  # key → (value, expires_at)
        backend = "Redis" if self._redis else "in-memory LRU"
        log.info("RAGCache initialised — backend=%s  ttl=%ds  max_memory=%d", backend, ttl, max_memory)

    # ── Public API ────────────────────────────────────────────────────────────

    def make_key(self, query: str, domain: str | None = None, profile: dict | None = None) -> str:
        """Return a stable SHA-256 cache key for this (query, domain, profile) combination."""
        payload = json.dumps({
            "q": query.strip().lower(),
            "d": domain or "",
            "p": _stable_hash_dict(profile or {}),
        }, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()

    def get(self, key: str) -> dict | None:
        """Return cached value or None if missing / expired."""
        if self._redis:
            return self._redis_get(key)
        return self._memory_get(key)

    def set(self, key: str, value: dict) -> None:
        """Store value under key with the configured TTL."""
        if self._redis:
            self._redis_set(key, value)
        else:
            self._memory_set(key, value)

    def invalidate(self, key: str) -> None:
        """Remove a specific cached entry."""
        if self._redis:
            try:
                self._redis.delete(key)
            except Exception:
                pass
        with self._lock:
            self._memory.pop(key, None)

    def clear(self) -> int:
        """Flush the entire cache.  Returns the number of entries removed."""
        count = 0
        if self._redis:
            try:
                keys = self._redis.keys("rag:*")
                if keys:
                    count = self._redis.delete(*keys)
            except Exception:
                pass
        with self._lock:
            count += len(self._memory)
            self._memory.clear()
        return count

    @property
    def size(self) -> int:
        """Approximate number of entries currently in the cache."""
        if self._redis:
            try:
                return len(self._redis.keys("rag:*"))
            except Exception:
                pass
        return len(self._memory)

    # ── Redis helpers ─────────────────────────────────────────────────────────

    def _connect_redis(self, url: str):
        if not url:
            return None
        try:
            import redis
            client = redis.from_url(url, socket_connect_timeout=3, socket_timeout=3, decode_responses=True)
            client.ping()
            log.info("Redis cache connected at %s", url)
            return client
        except Exception as exc:
            log.warning("Redis unavailable (%s) — falling back to in-memory cache", exc)
            return None

    def _redis_get(self, key: str) -> dict | None:
        try:
            raw = self._redis.get(f"rag:{key}")
            return json.loads(raw) if raw else None
        except Exception as exc:
            log.debug("Redis GET failed: %s", exc)
            return None

    def _redis_set(self, key: str, value: dict) -> None:
        try:
            self._redis.setex(f"rag:{key}", self._ttl, json.dumps(value))
        except Exception as exc:
            log.debug("Redis SET failed: %s", exc)

    # ── In-memory helpers ─────────────────────────────────────────────────────

    def _memory_get(self, key: str) -> dict | None:
        with self._lock:
            entry = self._memory.get(key)
            if entry is None:
                return None
            value, expires_at = entry
            if time.monotonic() > expires_at:
                del self._memory[key]
                return None
            # Move to end (most recently used)
            self._memory.move_to_end(key)
            return value

    def _memory_set(self, key: str, value: dict) -> None:
        with self._lock:
            if key in self._memory:
                self._memory.move_to_end(key)
            self._memory[key] = (value, time.monotonic() + self._ttl)
            # Evict oldest entries if over limit
            while len(self._memory) > self._max_memory:
                evicted_key, _ = self._memory.popitem(last=False)
                log.debug("LRU eviction: %s", evicted_key)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _stable_hash_dict(d: dict) -> str:
    """Return a short hash of a dict for use as a cache key component."""
    return hashlib.md5(json.dumps(d, sort_keys=True).encode()).hexdigest()[:8]
