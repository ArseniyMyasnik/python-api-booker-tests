import allure

@allure.suite('Health Check tests')
@allure.feature('Health Check API')
class TestHealthCheck:

    @allure.title('Test Case H-1: Check ping response')
    def test_health_check(self, health_api):

        response = health_api.health_check()

        assert response.status_code == 201, f'Expected status code 201, got {response.status_code}'
        assert response.text == 'Created', f'Unexpected text: {response.text}'