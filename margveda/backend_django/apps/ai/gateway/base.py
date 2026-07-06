"""Abstract AI Gateway — one interface for all LLM providers.

CareerBrain never calls a provider directly.
Every LLM call goes through a BaseGateway implementation.
This lets us swap Ollama → Anthropic → Gemini without changing business logic.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class GatewayMessage:
    role: str       # "system" | "user" | "assistant"
    content: str


@dataclass
class GatewayResponse:
    text: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    from_cache: bool = False
    metadata: dict = field(default_factory=dict)


class BaseGateway(ABC):
    """Abstract LLM gateway."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def is_available(self) -> bool: ...

    @abstractmethod
    def complete(
        self,
        messages: list[GatewayMessage],
        max_tokens: int = 800,
        temperature: float = 0.3,
    ) -> GatewayResponse | None: ...
