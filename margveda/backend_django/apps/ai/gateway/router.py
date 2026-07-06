"""AI Gateway Router — tries providers in priority order.

Priority: Ollama (free, local) → Anthropic Claude (cloud) → Rule-based fallback.
Business logic never changes when providers are added or swapped.
"""
from __future__ import annotations

import logging

from .base import BaseGateway, GatewayMessage, GatewayResponse
from .ollama import OllamaGateway
from .anthropic import AnthropicGateway

log = logging.getLogger("careerbrain.gateway")

_FALLBACK_TEXT = (
    "I'm currently unable to generate a full response. "
    "Please try again shortly or speak directly with one of our career counsellors."
)


class AIGatewayRouter:
    """
    Routes LLM requests across providers.
    Returns a deterministic fallback if all providers are unavailable.
    """

    def __init__(self) -> None:
        self._providers: list[BaseGateway] = [
            OllamaGateway(),
            AnthropicGateway(),
        ]

    def complete(
        self,
        messages: list[GatewayMessage],
        max_tokens: int = 800,
        temperature: float = 0.3,
    ) -> GatewayResponse:
        for provider in self._providers:
            if not provider.is_available:
                log.debug("Gateway: skipping %s (unavailable)", provider.name)
                continue
            result = provider.complete(messages, max_tokens=max_tokens, temperature=temperature)
            if result is not None:
                log.debug("Gateway: used %s (%d output tokens)", provider.name, result.output_tokens)
                return result

        log.warning("All LLM providers unavailable — using rule-based fallback")
        return GatewayResponse(text=_FALLBACK_TEXT, model="fallback")

    @property
    def active_provider(self) -> str:
        for p in self._providers:
            if p.is_available:
                return p.name
        return "fallback"
