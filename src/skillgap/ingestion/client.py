import httpx

from skillgap.ingestion.auth import FranceTravailAuth


class IngestionError(Exception):
    pass


class FranceTravailClient:
    def __init__(self, auth: FranceTravailAuth, base_url: str):
        self.auth = auth
        self.base_url = base_url or "https://api.francetravail.io/partenaire/offresdemploi/v2"

    def search_jobs(self, query: str, range_start: int = 0, range_end: int = 10) -> list[dict]:
        headers = self._build_headers()
        params = {
            "range": f"{range_start}-{range_end}",
            "motsCles": query,
        }
        try:
            response = httpx.get(
                f"{self.base_url}/offres/search", headers=headers, params=params, timeout=10
            )
            response.raise_for_status()
            return response.json().get("resultats", [])
        except httpx.HTTPError as e:
            raise IngestionError(f"Error occurred while searching jobs: {e}") from e

    def _build_headers(self) -> dict[str, str]:
        token = self.auth.get_token()
        return {
            "Authorization": f"Bearer {token}",
        }
