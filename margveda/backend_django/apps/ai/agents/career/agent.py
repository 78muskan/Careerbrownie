"""Career Agent — answers career, college, exam, and scholarship queries.

Primary agent for all student-facing career guidance.
Knowledge: all 10 RAG domains.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from apps.ai.agents.base import AgentResult, BaseAgent
from apps.ai.agents.registry import AgentRegistry
from apps.ai.gateway.base import GatewayMessage
from apps.ai.prompts.templates import CAREER_SYSTEM

if TYPE_CHECKING:
    from apps.ai.gateway.router import AIGatewayRouter
    from apps.ai.rag.client import RAGClient

log = logging.getLogger("careerbrain.agents.career")

_ESCALATION_KEYWORDS = frozenset({
    "depressed", "anxious", "suicid", "mental health",
    "family pressure", "stress", "breakdown", "hopeless",
    "can't decide", "completely lost", "don't know what to do",
})


@AgentRegistry.register("career")
class CareerAgent(BaseAgent):
    goal = "Answer career guidance, college admissions, exam, and scholarship queries for Indian students"
    knowledge_domains = [
        "career", "college", "exam", "scholarship",
        "salary", "skills", "timeline", "faq", "govt_jobs",
    ]
    permissions = ["read:student_profile", "read:knowledge_base"]

    def run(
        self,
        query: str,
        history: list[dict],
        student_context: dict,
        domain: str | None,
        gateway: "AIGatewayRouter",
        rag: "RAGClient",
    ) -> AgentResult:
        # 1. Retrieve context from RAG microservice
        context_text, citations, sources = self._retrieve(query, domain, rag)

        # 2. Build message list
        messages = self._build_messages(query, history, student_context, context_text)

        # 3. Generate response via gateway (Ollama → Anthropic → fallback)
        resp = gateway.complete(messages, max_tokens=1000, temperature=0.3)

        # 4. Post-process
        suggestions = self._extract_suggestions(resp.text)
        needs_counselor = self._needs_escalation(query)

        return AgentResult(
            answer=resp.text,
            sources=sources,
            citations=citations,
            suggestions=suggestions,
            needs_counselor=needs_counselor,
            from_cache=False,
            metadata={"model": resp.model, "output_tokens": resp.output_tokens},
        )

    # ── Private helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _retrieve(
        query: str, domain: str | None, rag: "RAGClient"
    ) -> tuple[str, list[dict], list[str]]:
        context_parts: list[str] = []
        citations: list[dict] = []
        sources: list[str] = []
        try:
            result = rag.search(query=query, domain=domain, top_k=5)
            for i, hit in enumerate(result.get("hits", []), 1):
                context_parts.append(
                    f"[{i}] **{hit['title']}** (domain: {hit['domain']}, "
                    f"relevance: {hit['score']:.0%})\n{hit['excerpt']}"
                )
                citations.append({
                    "index": i,
                    "title": hit["title"],
                    "domain": hit["domain"],
                    "score": hit["score"],
                })
                sources.append(hit.get("id", hit["title"]))
        except Exception as exc:
            log.warning("RAG unavailable: %s — proceeding without context", exc)
        return "\n\n".join(context_parts), citations, sources

    @staticmethod
    def _build_messages(
        query: str,
        history: list[dict],
        student_context: dict,
        context_text: str,
    ) -> list[GatewayMessage]:
        system = CAREER_SYSTEM
        if student_context:
            lines = [f"  {k}: {v}" for k, v in student_context.items() if v]
            if lines:
                system += "\n\nStudent Profile:\n" + "\n".join(lines)
        if context_text:
            system += f"\n\nRelevant Knowledge Base:\n{context_text}"

        messages: list[GatewayMessage] = [GatewayMessage(role="system", content=system)]
        for turn in history[-8:]:
            if turn.get("role") in ("user", "assistant") and turn.get("content"):
                messages.append(GatewayMessage(role=turn["role"], content=turn["content"]))
        messages.append(GatewayMessage(role="user", content=query))
        return messages

    @staticmethod
    def _extract_suggestions(text: str) -> list[str]:
        suggestions: list[str] = []
        for line in text.split("\n"):
            stripped = line.strip().lstrip("•-*123456789. ")
            if stripped.endswith("?") and 20 < len(stripped) < 120:
                suggestions.append(stripped)
        return suggestions[:3]

    @staticmethod
    def _needs_escalation(query: str) -> bool:
        q = query.lower()
        return any(kw in q for kw in _ESCALATION_KEYWORDS)
