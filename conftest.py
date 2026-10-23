import os

import pytest
from dotenv import load_dotenv

from api.auth_api import AuthApi
from api.health_api import HealthApi
from api.get_booking_ids_api import GetBookingIdsApi
from api.create_booking_api import CreateBookingApi
from api.delete_booking_api import DeleteBookingApi

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    base_url = os.getenv("BASE_URL")

    if not base_url:
        raise RuntimeError("BASE_URL is not set. Add it to .env file")

    return base_url


@pytest.fixture(scope="session")
def auth_api(base_url):
    return AuthApi(base_url)


@pytest.fixture
def correct_auth_token(auth_api):
    response = auth_api.create_token({"username": "admin", "password": "password123"})
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code}"
    return response.json()["token"]


@pytest.fixture(scope="session")
def health_api(base_url):
    return HealthApi(base_url)


@pytest.fixture(scope="session")
def get_booking_ids_api(base_url):
    return GetBookingIdsApi(base_url)


@pytest.fixture(scope="session")
def create_booking_api(base_url):
    return CreateBookingApi(base_url)


@pytest.fixture(scope="session")
def delete_booking_api(base_url):
    return DeleteBookingApi(base_url)


@pytest.fixture
def booking_factory(create_booking_api, delete_booking_api, correct_auth_token):

    created_booking_ids = []

    def create_test_booking(payload):
        response = create_booking_api.create_booking(payload)

        assert (
            response.status_code == 200
        ), f"Expected status code 200, got {response.status_code}"

        response_body = response.json()

        assert (
            "bookingid" in response_body
        ), f'Expected "bookingid" in response body, got {response_body}'
        assert isinstance(
            response_body["bookingid"], int
        ), f'Expected "bookingid" to be an integer, got {type(response_body["bookingid"])}'

        post_id = response_body["bookingid"]
        created_booking_ids.append(post_id)

        return post_id

    yield create_test_booking

    for booking_id in created_booking_ids:
        response = delete_booking_api.delete_booking(
            booking_id=booking_id, auth_token=correct_auth_token
        )

        assert (
            response.status_code == 201
        ), f"Expected status code 201, got {response.status_code}"
