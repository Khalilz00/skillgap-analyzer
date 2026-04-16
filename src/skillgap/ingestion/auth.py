import time

import httpx


class AuthenticationError(Exception):
    pass


class FranceTravailAuth:
    def __init__(self, client_id: str, client_secret: str, token_url: str, scope: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.scope = scope
        self._access_token: str | None = None
        self._expires_at: float | None = None

    def get_token(self) -> str:
        if not self._is_token_valid():
            self._fetch_new_token()
        assert self._access_token is not None
        return self._access_token

    def _is_token_valid(self) -> bool:
        if self._access_token is None or self._expires_at is None:
            return False
        return time.time() < self._expires_at - 60

    def _fetch_new_token(self) -> None:
        try:
            response = httpx.post(
                self.token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "scope": self.scope,
                },
                timeout=10.0,
            )
            response.raise_for_status()
            token_data = response.json()
            if "access_token" not in token_data or "expires_in" not in token_data:
                raise AuthenticationError(
                    "Invalid token response: missing 'access_token' or 'expires_in'"
                )
            self._access_token = token_data["access_token"]
            self._expires_at = time.time() + token_data["expires_in"]

        except httpx.HTTPError as e:
            raise AuthenticationError(f"Failed to connect to auth server: {e}") from e
