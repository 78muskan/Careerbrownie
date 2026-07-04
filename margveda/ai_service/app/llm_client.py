"""LLM client — Ollama primary, Anthropic Claude fallback, rule-based last resort.

Priority chain
--------------
1. **Ollama** (``OLLAMA_URL`` is set and the server responds) — free, local, no API key.
2. **Anthropic Claude** (``ANTHROPIC_API_KEY`` is set) — production quality.
3. **Rule-based fallback** — always succeeds; returns a helpful static message so the
   service stays functional even with no LLM configured.

Ollama is called via its native HTTP API (``POST /api/chat``) using ``httpx``.
Anthropic is called via the official ``anthropic`` async client.

Retry strategy (Ollama + Anthropic)
-------------------------------------
- Connection / timeout errors: retry with back-off ``[1.0, 2.5, 5.0]`` s.
- Rate limit (Anthropic only): exponential back-off, up to LLM_MAX_RETRIES.
- Server errors (5xx): single retry after 1 s.
- Non-retryable errors (auth, bad request): propagate immediately.
"""
from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass
from typing import Any

import httpx

from app.config import settings

log = logging.getLogger(__name__)

_RETRY_DELAYS = [1.0, 2.5, 5.0]


# ── Public data types ─────────────────────────────────────────────────────────

@dataclass
class LLMResponse:
    text: str
    input_tokens: int = 0
    output_tokens: int = 0
    model: str = ""
    from_fallback: bool = False


# ── LLMClient ─────────────────────────────────────────────────────────────────

class LLMClient:
    """
    Unified async LLM client with Ollama primary and Claude fallback.

    Instantiate once at startup and reuse; the underlying HTTP clients are
    connection-pooled.
    """

    def __init__(
        self,
        ollama_url: str = settings.OLLAMA_URL,
        ollama_model: str = settings.OLLAMA_MODEL,
        anthropic_key: str = settings.ANTHROPIC_API_KEY,
        claude_model: str = settings.CLAUDE_MODEL,
    ) -> None:
        self._ollama_url = ollama_url.rstrip("/") if ollama_url else ""
        self._ollama_model = ollama_model
        self._anthropic_key = anthropic_key
        self._claude_model = claude_model

        # Lazy-initialised clients
        self._httpx_client: httpx.AsyncClient | None = None
        self._anthropic_client: Any = None

        # Detect which backends are usable
        self._ollama_enabled = bool(ollama_url)
        self._anthropic_enabled = bool(anthropic_key)
        self._available = self._ollama_enabled or self._anthropic_enabled

        if self._ollama_enabled:
            log.info("LLM primary: Ollama (%s) at %s", ollama_model, ollama_url)
        if self._anthropic_enabled:
            log.info("LLM %s: Anthropic %s", "fallback" if self._ollama_enabled else "primary", claude_model)
        if not self._available:
            log.warning("No LLM configured — service will use rule-based fallback only")

    # ── Public API ────────────────────────────────────────────────────────────

    async def chat(
        self,
        messages: list[dict],
        system: str = "",
        *,
        max_tokens: int = settings.LLM_MAX_TOKENS,
        temperature: float = settings.LLM_TEMPERATURE,
        fallback_text: str = "",
    ) -> LLMResponse:
        """
        Send a conversation to the best available LLM and return the response.

        Tries Ollama first; if unavailable or failing, falls back to Claude;
        if that also fails, returns ``fallback_text`` (or a static message).
        """
        # Try Ollama
        if self._ollama_enabled:
            result = await self._try_ollama(messages, system, max_tokens, temperature)
            if result is not None:
                return result
            log.warning("Ollama unavailable — trying Anthropic Claude")

        # Try Anthropic
        if self._anthropic_enabled:
            result = await self._try_anthropic(messages, system, max_tokens, temperature)
            if result is not None:
                return result
            log.error("Anthropic also failed — using rule-based fallback")

        return LLMResponse(
            text=fallback_text or _static_fallback(messages),
            from_fallback=True,
            model="fallback",
        )

    async def close(self) -> None:
        """Close underlying HTTP clients on shutdown."""
        if self._httpx_client and not self._httpx_client.is_closed:
            await self._httpx_client.aclose()
            self._httpx_client = None
        if self._anthropic_client is not None:
            await self._anthropic_client.close()
            self._anthropic_client = None

    @property
    def model(self) -> str:
        """Primary model identifier string."""
        if self._ollama_enabled:
            return self._ollama_model
        return self._claude_model

    @property
    def is_available(self) -> bool:
        return self._available

    # ── Ollama ────────────────────────────────────────────────────────────────

    async def _try_ollama(
        self,
        messages: list[dict],
        system: str,
        max_tokens: int,
        temperature: float,
    ) -> LLMResponse | None:
        """
        Call Ollama via POST /api/chat.  Returns None on any failure so the
        caller can fall through to the next backend.
        """
        client = self._get_httpx()
        ollama_messages = _build_ollama_messages(messages, system)
        payload = {
            "model": self._ollama_model,
            "messages": ollama_messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        for attempt in range(settings.LLM_MAX_RETRIES):
            try:
                resp = await asyncio.wait_for(
                    client.post(
                        f"{self._ollama_url}/api/chat",
                        json=payload,
                        headers={"Content-Type": "application/json"},
                    ),
                    timeout=settings.LLM_TIMEOUT_SECS,
                )
                resp.raise_for_status()
                data = resp.json()
                text = data.get("message", {}).get("content", "")
                eval_count = data.get("eval_count", 0)
                prompt_eval_count = data.get("prompt_eval_count", 0)
                return LLMResponse(
                    text=text,
                    input_tokens=prompt_eval_count,
                    output_tokens=eval_count,
                    model=f"ollama/{self._ollama_model}",
                )

            except (httpx.ConnectError, httpx.ConnectTimeout) as exc:
                log.warning("Ollama connection error (attempt %d): %s", attempt + 1, exc)
                return None  # Ollama not running — skip immediately

            except asyncio.TimeoutError:
                log.warning("Ollama timeout (attempt %d/%d)", attempt + 1, settings.LLM_MAX_RETRIES)
                if attempt < settings.LLM_MAX_RETRIES - 1:
                    await asyncio.sleep(_RETRY_DELAYS[attempt])

            except httpx.HTTPStatusError as exc:
                if exc.response.status_code >= 500:
                    log.warning("Ollama server error %d (attempt %d)", exc.response.status_code, attempt + 1)
                    await asyncio.sleep(1.0)
                else:
                    log.error("Ollama returned %d — not retrying", exc.response.status_code)
                    return None

            except Exception as exc:
                log.error("Ollama unexpected error: %s: %s", type(exc).__name__, exc)
                return None

        log.error("Ollama failed after %d attempts", settings.LLM_MAX_RETRIES)
        return None

    # ── Anthropic ─────────────────────────────────────────────────────────────

    async def _try_anthropic(
        self,
        messages: list[dict],
        system: str,
        max_tokens: int,
        temperature: float,
    ) -> LLMResponse | None:
        """
        Call Anthropic Claude.  Returns None on any failure.
        """
        client = self._get_anthropic()
        last_exc: Exception | None = None

        for attempt in range(settings.LLM_MAX_RETRIES):
            try:
                resp = await asyncio.wait_for(
                    client.messages.create(
                        model=self._claude_model,
                        system=system,
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                    ),
                    timeout=settings.LLM_TIMEOUT_SECS,
                )
                text = resp.content[0].text if resp.content else ""
                return LLMResponse(
                    text=text,
                    input_tokens=resp.usage.input_tokens,
                    output_tokens=resp.usage.output_tokens,
                    model=resp.model,
                )

            except Exception as exc:
                last_exc = exc
                if _is_rate_limit(exc):
                    delay = _RETRY_DELAYS[min(attempt, len(_RETRY_DELAYS) - 1)]
                    log.warning("Claude rate limited (attempt %d/%d); retrying in %.1f s", attempt + 1, settings.LLM_MAX_RETRIES, delay)
                    await asyncio.sleep(delay)
                elif _is_server_error(exc):
                    log.warning("Claude server error (attempt %d); retrying in 1 s", attempt + 1)
                    await asyncio.sleep(1.0)
                elif _is_timeout(exc):
                    log.warning("Claude timeout (attempt %d/%d)", attempt + 1, settings.LLM_MAX_RETRIES)
                    if attempt < settings.LLM_MAX_RETRIES - 1:
                        await asyncio.sleep(0.5)
                else:
                    log.error("Claude non-retryable error: %s: %s", type(exc).__name__, exc)
                    return None

        log.error("Claude failed after %d attempts: %s", settings.LLM_MAX_RETRIES, last_exc)
        return None

    # ── Client factories ──────────────────────────────────────────────────────

    def _get_httpx(self) -> httpx.AsyncClient:
        if self._httpx_client is None or self._httpx_client.is_closed:
            self._httpx_client = httpx.AsyncClient(timeout=settings.LLM_TIMEOUT_SECS + 5)
        return self._httpx_client

    def _get_anthropic(self) -> Any:
        if self._anthropic_client is None:
            import anthropic
            self._anthropic_client = anthropic.AsyncAnthropic(api_key=self._anthropic_key)
        return self._anthropic_client


# ── Helpers ───────────────────────────────────────────────────────────────────

def _build_ollama_messages(messages: list[dict], system: str) -> list[dict]:
    """Prepend a system message for Ollama's API format."""
    out: list[dict] = []
    if system:
        out.append({"role": "system", "content": system})
    out.extend(messages)
    return out


def _is_rate_limit(exc: Exception) -> bool:
    return "RateLimitError" in type(exc).__name__ or "rate_limit" in str(exc).lower()


def _is_server_error(exc: Exception) -> bool:
    name = type(exc).__name__
    return "APIStatusError" in name or "InternalServerError" in name or "ServiceUnavailable" in name


def _is_timeout(exc: Exception) -> bool:
    return "TimeoutError" in type(exc).__name__ or isinstance(exc, asyncio.TimeoutError)


def _static_fallback(messages: list[dict]) -> str:
    last_user = next(
        (m["content"] for m in reversed(messages) if m.get("role") == "user"), ""
    )
    excerpt = last_user[:120].strip()
    return (
        f"I'm currently unable to process your query — \"{excerpt}\" — because the AI service "
        "is temporarily unavailable. Please try again in a moment, or book a session with a "
        "CareerBrownie counsellor for personalised guidance."
    )
