import requests
import time
import hmac
import hashlib
import uuid
import base64
import urllib.parse
from typing import Optional, Any


class Session(requests.Session):
    """
    A custom session class for making authenticated requests to the Letterboxd API.

    Attributes:
        api_key (str): The API key for Letterboxd.
        secret (str): The secret key for signing the requests.
    """

    def __init__(self, api_key: str, secret: str) -> None:
        super().__init__()

        if not api_key:
            raise ValueError("API key must be provided")
        if not isinstance(api_key, str):
            raise TypeError(f"Expected api_key to be a string, not {api_key!r}")

        if not secret:
            raise ValueError("Secret must be provided")
        if not isinstance(secret, str):
            raise TypeError(f"Expected secret to be a string, not {secret!r}")
        
        self.api_key = api_key
        self.secret = base64.b64decode(secret)

        self.headers = {
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
            "User-Agent": "okhttp/3.14.9",
        }

    def request(
        self,
        method: str,
        url: str,
        params: Optional[dict] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        **kwargs,
    ) -> requests.Response:
        params = params or {}
        params.update(
            {
                "apikey": self.api_key,
                "nonce": str(uuid.uuid4()),
                "timestamp": str(int(time.time())),
            }
        )

        url_with_params = f"{url}?{urllib.parse.urlencode(params)}"
        payload = data or json.dumps(json, separators=(",", ":")) if json else ""

        return super().request(
            method,
            url_with_params,
            params={"signature": self._sign(method, url_with_params, payload)},
            data=data,
            json=json,
            **kwargs,
        )

    def _sign(self, method: str, uri: str, body: str = "") -> str:
        payload = "\x00".join([method, uri, body]).encode("utf-8")
        mac = hmac.new(self.secret, payload, hashlib.sha256)
        return mac.hexdigest()