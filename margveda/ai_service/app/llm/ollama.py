from __future__ import annotations

import time
from typing import AsyncIterator

import httpx

from app.core.config import settings
from app.core.logging import get_logger
from app.llm.base import BaseLLM, LLMResponse, Message

log = get_logger(__name__)


class OllamaLLM(BaseLLM):
    def __init__(self) -> None:
        self._base = settings.OLLAMA_URL.rstrip("/")
        self._model = settings.OLLAMA_MODEL
        self._timeout = settings.OLLAMA_TIMEOUT

    async def chat(
        self,
        messages: list[Message],
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        t0 = time.monotonic()
        payload = {
            "model": self._model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": False,
            "options": {
                "temperature": temperature if temperature is not None else settings.OLLAMA_TEMPERATURE,
                "num_predict": max_tokens or settings.OLLAMA_MAX_TOKENS,
            },
        }
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            r = await client.post(f"{self._base}/api/chat", json=payload)
            r.raise_for_status()
        data = r.json()
        latency = (time.monotonic() - t0) * 1000
        msg = data.get("message", {})
        return LLMResponse(
            content=msg.get("content", ""),
            model=data.get("model", self._model),
            input_tokens=data.get("prompt_eval_count", 0),
            output_tokens=data.get("eval_count", 0),
            latency_ms=latency,
        )

    async def stream(
        self,
        messages: list[Message],
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        import json
        payload = {
            "model": self._model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": True,
            "options": {
                "temperature": temperature if temperature is not None else settings.OLLAMA_TEMPERATURE,
                "num_predict": max_tokens or settings.OLLAMA_MAX_TOKENS,
            },
        }
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            async with client.stream("POST", f"{self._base}/api/chat", json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    chunk = json.loads(line)
                    token = chunk.get("message", {}).get("content", "")
                    if token:
                        yield token
                    if chunk.get("done"):
                        break

    async def is_available(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"{self._base}/api/tags")
                if r.status_code != 200:
                    return False
                models = r.json().get("models", [])
                model_base = self._model.split(":")[0]
                return any(m.get("name", "").startswith(model_base) for m in models)
        except Exception:
            return False


class AnthropicFallback(BaseLLM):
    """Used only when Ollama is not available."""

    async def chat(
        self,
        messages: list[Message],
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        if not settings.ANTHROPIC_API_KEY:
            raise RuntimeError("No LLM available: Ollama offline and ANTHROPIC_API_KEY not set")
        import httpx as _h
        payload = {
            "model": settings.ANTHROPIC_MODEL,
            "max_tokens": max_tokens or settings.OLLAMA_MAX_TOKENS,
            "system": next((m.content for m in messages if m.role == "system"), ""),
            "messages": [{"role": m.role, "content": m.content} for m in messages if m.role != "system"],
        }
        async with _h.AsyncClient(timeout=30) as client:
            r = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={"x-api-key": settings.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01"},
                json=payload,
            )
            r.raise_for_status()
        data = r.json()
        return LLMResponse(content=data["content"][0]["text"], model=data["model"])

    async def stream(self, messages, temperature=None, max_tokens=None) -> AsyncIterator[str]:
        r = await self.chat(messages, temperature, max_tokens)
        yield r.content

    async def is_available(self) -> bool:
        return bool(settings.ANTHROPIC_API_KEY)


_ollama: OllamaLLM | None = None
_fallback: AnthropicFallback | None = None


async def get_llm() -> BaseLLM:
    global _ollama, _fallback
    if _ollama is None:
        _ollama = OllamaLLM()
    if await _ollama.is_available():
        return _ollama
    log.warning("Ollama unavailable — switching to Anthropic fallback")
    if _fallback is None:
        _fallback = AnthropicFallback()
    return _fallback
