"""Ollama gateway — local LLM provider (Qwen, Llama, Mistral, etc.)."""
from __future__ import annotations

import logging

import requests
from django.conf import settings

from .base import BaseGateway, GatewayMessage, GatewayResponse

log = logging.getLogger("careerbrain.gateway.ollama")


class OllamaGateway(BaseGateway):
    """Calls a locally-running Ollama instance. Primary provider — free."""

    def __init__(self) -> None:
        self._base: str = getattr(settings, "OLLAMA_URL", "http://localhost:11434")
        self._model: str = getattr(settings, "OLLAMA_MODEL", "qwen2.5:7b")
        self._available: bool | None = None

    @property
    def name(self) -> str:
        return f"ollama/{self._model}"

    @property
    def is_available(self) -> bool:
        if self._available is None:
            try:
                requests.get(f"{self._base}/api/tags", timeout=2)
                self._available = True
            except Exception:
                self._available = False
        return self._available

    def complete(
        self,
        messages: list[GatewayMessage],
        max_tokens: int = 800,
        temperature: float = 0.3,
    ) -> GatewayResponse | None:
        if not self.is_available:
            return None
        try:
            resp = requests.post(
                f"{self._base}/api/chat",
                json={
                    "model": self._model,
                    "messages": [{"role": m.role, "content": m.content} for m in messages],
                    "stream": False,
                    "options": {"temperature": temperature, "num_predict": max_tokens},
                },
                timeout=30,
            )
            resp.raise_for_status()
            return GatewayResponse(
                text=resp.json()["message"]["content"],
                model=self._model,
            )
        except Exception as exc:
            log.warning("Ollama error: %s", exc)
            self._available = False
            return None
