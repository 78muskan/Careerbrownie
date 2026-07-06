"""Booking Agent — stub for Volume 7.

Handles session scheduling, calendar management, and booking confirmations.
Full implementation: CBES Volume 7.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from apps.ai.agents.base import AgentResult, BaseAgent
from apps.ai.agents.registry import AgentRegistry
from apps.ai.gateway.base import GatewayMessage

if TYPE_CHECKING:
    from apps.ai.gateway.router import AIGatewayRouter
    from apps.ai.rag.client import RAGClient

log = logging.getLogger("careerbrain.agents.booking")


@AgentRegistry.register("booking")
class BookingAgent(BaseAgent):
    goal = "Schedule and manage counselling sessions and calendar operations"
    knowledge_domains = ["counsellor"]
    permissions = ["read:sessions", "write:sessions", "read:counsellors"]

    def run(self, query, history, student_context, domain, gateway, rag) -> AgentResult:
        messages = [
            GatewayMessage(role="system", content=(
                "You are CareerBrownie's booking assistant. "
                "Help students book, reschedule, or cancel counselling sessions. "
                "CBES Volume 7 implementation pending."
            )),
            GatewayMessage(role="user", content=query),
        ]
        resp = gateway.complete(messages, max_tokens=400)
        return AgentResult(
            answer=resp.text,
            suggestions=["Book a free session", "View available slots", "Talk to a counsellor"],
        )
