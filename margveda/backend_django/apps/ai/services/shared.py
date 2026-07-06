"""Shared Services container — single place that owns all shared infrastructure.

Every agent receives these via CareerBrain.
No agent instantiates shared services directly.

Current services:
  gateway  — AI Gateway Router (LLM provider abstraction)
  rag      — RAG Client (FastAPI ai_service)
  short_mem — Short-term conversation memory (Redis)
  long_mem  — Long-term student memory (PostgreSQL)

Future services (CBES volumes 2+):
  analytics  — event tracking
  scheduler  — n8n / Celery task scheduling
  notifier   — push / email notifications
  payments   — Razorpay
"""
from __future__ import annotations

from apps.ai.gateway.router import AIGatewayRouter
from apps.ai.rag.client import RAGClient
from apps.ai.memory.short_term import ConversationMemory
from apps.ai.memory.long_term import StudentMemory


class SharedServices:
    """Singleton container for all services shared across agents."""

    _instance: "SharedServices | None" = None

    def __init__(self) -> None:
        self.gateway = AIGatewayRouter()
        self.rag = RAGClient()
        self.short_mem = ConversationMemory()
        self.long_mem = StudentMemory()

    @classmethod
    def get(cls) -> "SharedServices":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
