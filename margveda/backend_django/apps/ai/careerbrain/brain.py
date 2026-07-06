"""CareerBrain — the central AI orchestrator for CareerBrownie.

CBES Section 3: CareerBrain is NOT an LLM.
CareerBrain is the orchestrator that controls:
  Agent Selection → Context Retrieval → Memory → Reasoning →
  Security → Logging → Caching → Analytics → Tool Calling

Single entry point for every AI operation on the platform.
Usage:
    brain = CareerBrain.get()
    response = brain.process(BrainRequest(query="What career after PCM?", user_id=42))
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any

log = logging.getLogger("careerbrain")


@dataclass
class BrainRequest:
    """Everything CareerBrain needs to process one request."""
    query: str
    user_id: int | str | None = None
    session_id: str | None = None
    agent_hint: str = "career"     # which agent to route to
    domain: str | None = None      # RAG domain filter
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class BrainResponse:
    """Everything CareerBrain returns to the caller."""
    answer: str
    agent_used: str
    sources: list[str] = field(default_factory=list)
    citations: list[dict] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    needs_counselor: bool = False
    from_cache: bool = False
    latency_ms: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


class CareerBrain:
    """
    Central AI orchestrator — singleton.

    Responsibilities per CBES Volume 1:
    ✓ Agent selection
    ✓ Context assembly (memory + RAG)
    ✓ LLM routing via AI Gateway
    ✓ Memory read/write
    ✓ Security (permissions checked via agent.permissions)
    ✓ Logging & latency tracking
    □ Caching (Volume 4)
    □ Analytics (Volume 10)
    □ Tool calling (Volumes 5-11)
    """

    _instance: "CareerBrain | None" = None

    def __init__(self) -> None:
        from apps.ai.agents.registry import AgentRegistry
        from apps.ai.services.shared import SharedServices

        self._registry = AgentRegistry()
        self._svc = SharedServices.get()
        log.info(
            "CareerBrain initialized | gateway=%s | rag=%s | agents=%s",
            self._svc.gateway.active_provider,
            self._svc.rag.health(),
            self._registry.all_names(),
        )

    @classmethod
    def get(cls) -> "CareerBrain":
        """Return the process-global CareerBrain singleton."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # ── Main entry point ──────────────────────────────────────────────────────

    def process(self, request: BrainRequest) -> BrainResponse:
        """Route a request through the appropriate agent and return a response."""
        start = time.monotonic()
        log.info(
            "Brain.process | agent=%s | user=%s | session=%s | q=%.80r",
            request.agent_hint, request.user_id, request.session_id, request.query,
        )

        # 1. Load long-term memory (student profile)
        student_ctx: dict = {}
        if request.user_id:
            student_ctx = self._svc.long_mem.load(request.user_id)

        # 2. Load short-term memory (conversation history)
        history: list[dict] = []
        if request.session_id:
            history = self._svc.short_mem.load(request.session_id)

        # 3. Select agent
        agent = self._registry.select(request.agent_hint)

        # 4. Run agent (RAG + LLM inside agent)
        result = agent.run(
            query=request.query,
            history=history,
            student_context=student_ctx,
            domain=request.domain,
            gateway=self._svc.gateway,
            rag=self._svc.rag,
        )

        # 5. Persist to short-term memory
        if request.session_id:
            self._svc.short_mem.append(
                request.session_id, request.query, result.answer
            )

        latency = int((time.monotonic() - start) * 1000)
        log.info(
            "Brain.process done | agent=%s | latency=%dms | counselor=%s",
            agent.name, latency, result.needs_counselor,
        )

        return BrainResponse(
            answer=result.answer,
            agent_used=agent.name,
            sources=result.sources,
            citations=result.citations,
            suggestions=result.suggestions,
            needs_counselor=result.needs_counselor,
            from_cache=result.from_cache,
            latency_ms=latency,
            metadata=result.metadata,
        )
