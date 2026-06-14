import json
import logging
import urllib.error
import urllib.request
from typing import Any

from app.core.config import settings


logger = logging.getLogger(__name__)


class AIServiceClient:
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or settings.AI_SERVICE_URL).rstrip("/")

    def post(self, path: str, payload: dict[str, Any], timeout: int = 12) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=data,
            method="POST",
            headers={"Content-Type": "application/json"},
        )

        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            logger.warning("AI service request failed | url=%s | error=%s", url, exc)
            raise RuntimeError("AI service is unavailable") from exc
