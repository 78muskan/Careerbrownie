import os
from typing import Any

import httpx


BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000/api/v1").rstrip("/")


def _headers(token: str | None = None) -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def api_request(
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    token: str | None = None,
) -> dict[str, Any] | list[dict[str, Any]]:
    url = f"{BACKEND_API_URL}{path}"
    with httpx.Client(timeout=20) as client:
        response = client.request(
            method,
            url,
            json=payload,
            headers=_headers(token),
        )

    if response.status_code >= 400:
        detail = response.json().get("detail", response.text)
        raise ValueError(str(detail))

    return response.json()
