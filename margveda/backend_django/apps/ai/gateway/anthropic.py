"""Anthropic Claude gateway — cloud LLM provider (fallback after Ollama)."""
from __future__ import annotations

import logging

import requests
from django.conf import settings

from .base import BaseGateway, GatewayMessage, GatewayResponse

log = logging.getLogger("careerbrain.gateway.anthropic")

_API_URL = "https://api.anthropic.com/v1/messages"


class AnthropicGateway(BaseGateway):
    """Calls Anthropic Claude API. Secondary provider — paid per token."""

    def __init__(self) -> None:
        self._key: str = getattr(settings, "ANTHROPIC_API_KEY", "")
        self._model: str = getattr(settings, "CLAUDE_MODEL", "claude-sonnet-4-6")

    @property
    def name(self) -> str:
        return f"anthropic/{self._model}"

    @property
    def is_available(self) -> bool:
        return bool(self._key and not self._key.startswith("sk-ant-api03-..."))

    def complete(
        self,
        messages: list[GatewayMessage],
        max_tokens: int = 800,
        temperature: float = 0.3,
    ) -> GatewayResponse | None:
        if not self.is_available:
            return None

        system = next((m.content for m in messages if m.role == "system"), "")
        user_messages = [
            {"role": m.role, "content": m.content}
            for m in messages
            if m.role != "system"
        ]

        try:
            resp = requests.post(
                _API_URL,
                headers={
                    "x-api-key": self._key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": self._model,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "system": system,
                    "messages": user_messages,
                },
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            usage = data.get("usage", {})
            return GatewayResponse(
                text=data["content"][0]["text"],
                model=self._model,
                input_tokens=usage.get("input_tokens", 0),
                output_tokens=usage.get("output_tokens", 0),
            )
        except Exception as exc:
            log.error("Anthropic error: %s", exc)
            return None
