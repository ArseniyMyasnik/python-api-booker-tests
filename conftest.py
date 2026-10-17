import os

import pytest
from dotenv import load_dotenv

from api.auth_api import AuthApi

load_dotenv()

@pytest.fixture(scope='session')
def base_url():
    base_url = os.getenv("BASE_URL")

    if not base_url:
        raise RuntimeError('BASE_URL is not set. Add it to .env file')

    return base_url

@pytest.fixture(scope='session')
def auth_api(base_url):
    return AuthApi(base_url)