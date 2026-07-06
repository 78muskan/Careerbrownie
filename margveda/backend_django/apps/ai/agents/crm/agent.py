"""CRM Agent — stub for Volume 6.

Handles lead management, student follow-up, and CRM automation.
Full implementation: CBES Volume 6.
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

log = logging.getLogger("careerbrain.agents.crm")


@AgentRegistry.register("crm")
class CRMAgent(BaseAgent):
    goal = "Manage leads, follow-ups, and student CRM operations"
    knowledge_domains = ["faq", "counsellor"]
    permissions = ["read:leads", "write:leads", "read:student_profile"]

    def run(self, query, history, student_context, domain, gateway, rag) -> AgentResult:
        messages = [
            GatewayMessage(role="system", content=(
                "You are CareerBrownie's CRM assistant. "
                "Help with lead qualification, follow-up scheduling, and student communication. "
                "CBES Volume 6 implementation pending."
            )),
            GatewayMessage(role="user", content=query),
        ]
        resp = gateway.complete(messages, max_tokens=600)
        return AgentResult(answer=resp.text)
