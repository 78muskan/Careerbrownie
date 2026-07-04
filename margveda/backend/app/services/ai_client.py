import json
import logging
from typing import Any

import httpx

from app.core.config import settings


logger = logging.getLogger(__name__)


class AIServiceClient:
    """Async HTTP client for the AI service with connection pooling.

    Uses ``httpx.AsyncClient`` for non-blocking requests and proper
    connection reuse between calls.
    """

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or settings.AI_SERVICE_URL).rstrip("/")
        self._client: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=httpx.Timeout(15.0, connect=5.0),
                limits=httpx.Limits(max_keepalive_connections=10, max_connections=20),
            )
        return self._client

    async def post(
        self,
        path: str,
        payload: dict[str, Any],
        timeout: int = 12,
    ) -> dict[str, Any]:
        """Send a POST request to the AI service.

        Args:
            path: API path, e.g. ``/chat``.
            payload: JSON-serialisable request body.
            timeout: Request timeout in seconds.

        Returns:
            Parsed JSON response dict.

        Raises:
            RuntimeError: If the AI service is unreachable or returns an error.
        """
        client = self._get_client()
        try:
            resp = await client.post(
                path,
                json=payload,
                timeout=timeout,
            )
            resp.raise_for_status()
            return resp.json()
        except (httpx.ConnectError, httpx.ConnectTimeout) as exc:
            logger.warning("AI service connection failed | path=%s | error=%s", path, exc)
            raise RuntimeError("AI service is unavailable — connection refused") from exc
        except httpx.TimeoutException as exc:
            logger.warning("AI service timed out | path=%s | error=%s", path, exc)
            raise RuntimeError("AI service is unavailable — request timed out") from exc
        except httpx.HTTPStatusError as exc:
            logger.warning(
                "AI service returned %d | path=%s | body=%s",
                exc.response.status_code,
                path,
                exc.response.text[:500],
            )
            raise RuntimeError(f"AI service error: {exc.response.status_code}") from exc
        except json.JSONDecodeError as exc:
            logger.warning("AI service returned invalid JSON | path=%s", path)
            raise RuntimeError("AI service returned invalid response") from exc

    async def close(self) -> None:
        """Close the underlying HTTP client. Call on application shutdown."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
