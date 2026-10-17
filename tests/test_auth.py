import requests
import allure

def assert_bad_credentials(response):
    assert response.status_code == 200, f'Expected status code 200, got {response.status_code}'

    response_body = response.json()
    assert 'reason' in response_body, f'Expected "reason" in response body, got {response_body}'
    assert response_body['reason'] == 'Bad credentials',\
        f'Expected reason to be "Bad credentials", got {response_body["reason"]}'
    assert 'token' not in response_body, f'Unexpected token in response body: {response_body}'

@allure.suite('Auth tests')
@allure.feature('Auth tests')
class TestAuth:
    @allure.title('Test case A-1: Create token with valid credentials')
    def test_create_token_with_valid_credentials(self, auth_api):

        payload = {
            "username": "admin",
            "password": "password123"
        }

        response = auth_api.create_token(payload)

        assert response.status_code == 200, f'Expected status code 200, got {response.status_code}'

        response_body = response.json()
        assert 'token' in response_body, f'Expected "token" in response body, got {response_body}'
        assert isinstance(response_body['token'], str), f'Expected token to be a string, got {type(response_body["token"])}'
        assert response_body["token"], "Expected token to be non-empty"
        assert 'reason' not in response_body, f'Unexpected reason in response body: {response_body}'

    @allure.title('Test case A-2: Create token with invalid username')
    def test_create_token_with_invalid_username(self, auth_api):

        payload = {
            "username": "notadmin",
            "password": "password123"
        }

        response = auth_api.create_token(payload)

        assert_bad_credentials(response)

    @allure.title('Test case A-3: Create token with invalid password')
    def test_create_token_with_invalid_password(self, auth_api):

        payload = {
            "username": "admin",
            "password": "password12333"
        }

        response = auth_api.create_token(payload)

        assert_bad_credentials(response)

    @allure.title('Test case A-4: Create token with both invalid credentials')
    def test_create_token_with_both_invalid_credentials(self, auth_api):

        payload = {
            "username": "administrator",
            "password": "password123456"
        }

        response = auth_api.create_token(payload)

        assert_bad_credentials(response)

    @allure.title('Test case A-5: Create token without username')
    def test_create_token_without_username(self, auth_api):

        payload = {
            "password": "password123"
        }

        response = auth_api.create_token(payload)

        assert_bad_credentials(response)

    @allure.title('Test case A-6: Create token without password')
    def test_create_token_without_password(self, auth_api):

        payload = {
            "username": "admin"
        }

        response = auth_api.create_token(payload)

        assert_bad_credentials(response)

    @allure.title('Test case A-7: Create token with an empty JSON object')
    def test_create_token_with_empty_json(self, auth_api):

        payload = {}

        response = auth_api.create_token(payload)

        assert_bad_credentials(response)

    @allure.title('Test case A-8: Create token with unsupported Content-Type')
    def test_create_token_with_unsupported_content_type(self, auth_api):

        payload = {
            "username": "admin",
            "password": "password123"
        }
        headers = {
            "Content-Type": "application/xml"
        }

        response = auth_api.create_token(payload=payload, headers=headers)

        assert response.status_code == 400, f'Expected status code 400, got {response.status_code}'
        assert response.text == 'Bad Request', f'Expected response body "Bad Request", got {response.text}'
        assert 'token' not in response.text, f'Unexpected token in response text: {response.text}'

    @allure.title('Test case A-9: Create token with SQL injection attempt in username')
    def test_create_token_with_sql_injection_attempt_in_username(self, auth_api):

        payload = {
            "username": "' OR '1' = '1' --",
            "password": "password123"
        }

        response = auth_api.create_token(payload)

        assert_bad_credentials(response)