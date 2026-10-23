import requests


class GetBookingIdsApi:

    def __init__(self, base_url, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get_ids(self, params=None):
        return requests.get(
            url=f"{self.base_url}/booking", params=params, timeout=self.timeout
        )

    def get_by_id(self, booking_id):
        return requests.get(
            url=f"{self.base_url}/booking/{booking_id}", timeout=self.timeout
        )
