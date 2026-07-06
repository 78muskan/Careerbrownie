"""Base Agent — abstract contract every CareerBrain agent must satisfy.

CBES Section 10: Every agent has Goal, Tools, Memory, Permissions, Knowledge, Output.
No duplicated logic. Shared services are injected — never owned by the agent.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.ai.gateway.router import AIGatewayRouter
    from apps.ai.rag.client import RAGClient


@dataclass
class AgentResult:
    """Standardized output every agent returns to CareerBrain."""
    answer: str
    sources: list[str] = field(default_factory=list)
    citations: list[dict] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    needs_counselor: bool = False
    from_cache: bool = False
    metadata: dict = field(default_factory=dict)


class BaseAgent(ABC):
    """
    Abstract base for every CareerBrain agent.

    Subclasses declare class-level attributes:
        name              — unique slug used for routing ("career", "crm", ...)
        goal              — one-sentence purpose
        knowledge_domains — which RAG domains this agent queries
        permissions       — what data this agent is allowed to access
    """

    name: str = "base"
    goal: str = ""
    knowledge_domains: list[str] = []
    permissions: list[str] = []

    @abstractmethod
    def run(
        self,
        query: str,
        history: list[dict],
        student_context: dict,
        domain: str | None,
        gateway: "AIGatewayRouter",
        rag: "RAGClient",
    ) -> AgentResult: ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r}>"
