from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from app.core.logging import get_logger
from app.llm.base import Message
from app.llm.ollama import get_llm

log = get_logger(__name__)


@dataclass
class AgentContext:
    session_id: str
    user_query: str
    student_profile: dict = field(default_factory=dict)
    history: list[Message] = field(default_factory=list)
    retrieved_docs: list[dict] = field(default_factory=list)


@dataclass
class AgentResult:
    agent: str
    data: dict
    confidence: float = 1.0
    sources: list[dict] = field(default_factory=list)


class BaseAgent(ABC):
    name: str = "base"
    system_prompt: str = ""

    async def run(self, ctx: AgentContext) -> AgentResult:
        try:
            return await self._execute(ctx)
        except Exception as exc:
            log.error("Agent %s failed: %s", self.name, exc)
            return AgentResult(agent=self.name, data={"error": str(exc)}, confidence=0.0)

    @abstractmethod
    async def _execute(self, ctx: AgentContext) -> AgentResult: ...

    async def _llm_json(self, messages: list[Message], max_tokens: int = 1024) -> dict:
        llm = await get_llm()
        resp = await llm.chat(messages, temperature=0.1, max_tokens=max_tokens)
        text = resp.content.strip()
        # Strip markdown code fences if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to extract JSON from the response
            import re
            m = re.search(r"\{.*\}", text, re.DOTALL)
            if m:
                return json.loads(m.group())
            return {"raw": text}
