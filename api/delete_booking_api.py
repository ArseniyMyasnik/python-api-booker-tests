import requests


class DeleteBookingApi:

    def __init__(self, base_url, timeout=10):
        self.base_url = base_url
        self.timeout = timeout

    def delete_booking(self, booking_id, auth_token):
        return requests.delete(
            url=f"{self.base_url}/booking/{booking_id}",
            headers={"Cookie": f"token={auth_token}"},
            timeout=self.timeout,
        )
