import requests


class CreateBookingApi:

    def __init__(self, base_url, timeout=10):
        self.base_url = f"{base_url}".rstrip("/")
        self.timeout = timeout

    def create_booking(self, payload):
        response = requests.post(
            url=f"{self.base_url}/booking/", json=payload, timeout=self.timeout
        )
        return response
