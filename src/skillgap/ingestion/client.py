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
        self,
        query: str,
        grand_domaine: str | None = None,
        range_start: int = 0,
        range_end: int = 10,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> tuple[int, list[dict[str, Any]]]:
        headers = self._build_headers()
        params: dict[str, str] = {
            "range": f"{range_start}-{range_end}",
            "motsCles": query,
        }
        if grand_domaine is not None:
            params["grandDomaine"] = grand_domaine
        if start_date is not None and end_date is not None:
            params["minCreationDate"] = start_date
            params["maxCreationDate"] = end_date
        response = httpx.get(
            f"{self.base_url}/offres/search", headers=headers, params=params, timeout=10
        )
        if response.status_code >= 400:
            print(f"STATUS: {response.status_code}")
            print(f"BODY: {response.text}")
        response.raise_for_status()
        resultats: list[dict[str, Any]] = response.json().get("resultats", [])
        total_objects_string = response.headers["Content-Range"]
        total_objects = int(total_objects_string.split("/")[-1]) if total_objects_string else 0
        return total_objects, resultats

    def _build_headers(self) -> dict[str, str]:
        token = self.auth.get_token()
        return {
            "Authorization": f"Bearer {token}",
        }
