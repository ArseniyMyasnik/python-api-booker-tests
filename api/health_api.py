import requests

class HealthApi:

    def __init__(self, base_url, timeout=10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    def health_check(self):
        return requests.get(
            url=f'{self.base_url}/ping',
            timeout=self.timeout
        )