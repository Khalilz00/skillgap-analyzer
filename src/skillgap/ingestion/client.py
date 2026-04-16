from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from skillgap.ingestion.auth import FranceTravailAuth


class FranceTravailClient:
    def __init__(self, auth: FranceTravailAuth, base_url: str):
        self.auth = auth
        self.base_url = base_url or "https://api.francetravail.io/partenaire/offresdemploi/v2"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def search_jobs(
        self, query: str, range_start: int = 0, range_end: int = 10
    ) -> list[dict[str, Any]]:
        headers = self._build_headers()
        params = {
            "range": f"{range_start}-{range_end}",
            "motsCles": query,
        }
        response = httpx.get(
            f"{self.base_url}/offres/search", headers=headers, params=params, timeout=10
        )
        response.raise_for_status()
        resultats: list[dict[str, Any]] = response.json().get("resultats", [])
        return resultats

    def _build_headers(self) -> dict[str, str]:
        token = self.auth.get_token()
        return {
            "Authorization": f"Bearer {token}",
        }
