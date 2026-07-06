"""RAG Client — synchronous HTTP client for the FastAPI ai_service microservice.

CareerBrain delegates all vector search and RAG chat to the FastAPI ai_service.
This client is the only place that knows the ai_service URL and protocol.

Routes used:
    POST /search  — similarity search, no LLM
    POST /chat    — full RAG pipeline with LLM response
    GET  /health  — liveness check
"""
from __future__ import annotations

import logging

import requests
from django.conf import settings

log = logging.getLogger("careerbrain.rag")

_EMPTY_SEARCH: dict = {"hits": [], "total": 0}
_EMPTY_CHAT: dict = {
    "answer": "",
    "citations": [],
    "suggestions": [],
    "from_fallback": True,
    "needs_counselor": False,
    "latency_ms": 0,
}


class RAGClient:
    """Wraps the FastAPI ai_service. All timeouts are conservative defaults."""

    def __init__(self) -> None:
        self._base: str = getattr(settings, "AI_SERVICE_URL", "http://localhost:9000")
        self._key: str = getattr(settings, "INTERNAL_API_KEY", "")
        self._headers = {
            "Content-Type": "application/json",
            "X-Internal-Key": self._key,
        }

    # ── Public API ────────────────────────────────────────────────────────────

    def search(
        self, query: str, domain: str | None = None, top_k: int = 5
    ) -> dict:
        """Vector similarity search. Returns {"hits": [...], "total": N}."""
        try:
            resp = requests.post(
                f"{self._base}/search",
                headers=self._headers,
                json={"query": query, "domain": domain, "top_k": top_k},
                timeout=5,
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            log.warning("RAG.search failed: %s", exc)
            return _EMPTY_SEARCH

    def chat(
        self,
        query: str,
        history: list[dict] | None = None,
        student_profile: dict | None = None,
        domain: str | None = None,
    ) -> dict:
        """Full RAG chat — retrieves context then calls LLM. Returns ChatResponse dict."""
        try:
            resp = requests.post(
                f"{self._base}/chat",
                headers=self._headers,
                json={
                    "query": query,
                    "history": history or [],
                    "student_profile": student_profile,
                    "domain": domain,
                },
                timeout=30,
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            log.error("RAG.chat failed: %s", exc)
            return _EMPTY_CHAT

    def health(self) -> bool:
        """Return True if the ai_service is reachable and ready."""
        try:
            resp = requests.get(f"{self._base}/health", timeout=3)
            return resp.status_code == 200
        except Exception:
            return False
