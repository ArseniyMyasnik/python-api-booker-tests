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
    assert response.status_code == 200
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
