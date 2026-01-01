import base64
import time
import requests

class KrogerClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()

        self._access_token = None
        self._token_expires_at = 0 

    def _get_token(self, scope: str = "product.compact") -> None:
        token_url = "https://api.kroger.com/v1/connect/oauth2/token"

        basic = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode("utf-8")).decode("ascii")
        headers = {
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "client_credentials",
            "scope": scope,
        }

        r = self.session.post(token_url, headers=headers, data=data, timeout=30)
        r.raise_for_status()
        payload = r.json()

        self._access_token = payload["access_token"]
        self._token_expires_at = int(time.time()) + int(payload.get("expires_in", 0)) - 30 

    def _ensure_token(self) -> None:
        if not self._access_token or time.time() >= self._token_expires_at:
            self._get_token()

    def request(self, method: str, url: str, *, params=None, json=None, headers=None):
        self._ensure_token()

        req_headers = dict(headers or {})
        req_headers["Authorization"] = f"Bearer {self._access_token}"
        req_headers.setdefault("Accept", "application/json")

        r = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            headers=req_headers,
            timeout=30,
        )

        if r.status_code == 401:
            self._get_token()
            req_headers["Authorization"] = f"Bearer {self._access_token}"
            r = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                headers=req_headers,
                timeout=30,
            )

        r.raise_for_status()
        return r.json()