import requests


class AuthApi:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def create_token(self, payload, headers=None):
        return requests.post(
            url=f"{self.base_url}/auth",
            json=payload,
            headers=headers,
            timeout=self.timeout,
        )
