import os
from typing import Any

import httpx


API_BASE_URL = os.getenv("MARGVEDA_API_URL", "http://localhost:8000/api/v1")


class APIClient:
    def __init__(self, base_url: str = API_BASE_URL) -> None:
        self.base_url = base_url.rstrip("/")

    async def request(
        self,
        method: str,
        path: str,
        token: str | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.request(
                method,
                f"{self.base_url}{path}",
                headers=headers,
                json=json,
            )
            response.raise_for_status()
            return response.json()

    async def get(self, path: str, token: str | None = None) -> dict[str, Any]:
        return await self.request("GET", path, token=token)

    async def post(
        self,
        path: str,
        json: dict[str, Any],
        token: str | None = None,
    ) -> dict[str, Any]:
        return await self.request("POST", path, token=token, json=json)

    async def put(
        self,
        path: str,
        json: dict[str, Any],
        token: str | None = None,
    ) -> dict[str, Any]:
        return await self.request("PUT", path, token=token, json=json)


api_client = APIClient()
