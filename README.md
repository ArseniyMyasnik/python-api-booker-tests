# python-api-booker-tests

Automated API tests for the demo booking website [Restful-booker](https://restful-booker.herokuapp.com/apidoc/index.html) using **Python**, **pytest**, **requests**, **Allure Report**, and the **API Client Pattern**.

## Test Coverage

This project includes automated tests for:
- Auth API: `POST /auth`
  - Valid and invalid credentials
  - Missing required fields
  - Empty JSON object
  - Unsupported `Content-Type`
  - SQL injection attempt
- Health Check API: `GET /ping`
  - API availability check

## Technology Stack

- **Python 3.10+** - programming language
- **pytest 9.x** - test runner and test organization
- **requests 2.x** - HTTP library
- **Allure Report 2.x** - test reporting integration
- **API Client Pattern** - test architecture pattern

## Project Structure

```text
python-api-booker-tests/
├── api/
│   ├── auth_api.py            # API client for POST /auth requests
│   └── health_api.py          # API client for GET /ping requests
├── tests/
│   ├── test_auth.py           # Automated tests for the Auth API
│   └── test_ping.py           # Automated tests for the Health Check API
├── test_cases/
│   ├── auth_test_cases.md     # Manual test cases for the Auth API
│   └── health_check_cases.md  # Manual test cases for the Health Check API
├── conftest.py                # Shared pytest fixtures and configuration
├── pytest.ini                 # Pytest settings
├── requirements.txt           # Project dependencies
├── .env.example               # Example environment variables
├── .gitignore                 # Ignored local and generated files
└── README.md                  # Project documentation
```

## Test Documentation

Manual test cases are stored in:

`test_cases/`

They describe endpoints, preconditions, requests, steps, and expected results.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ArseniyMyasnik/python-api-booker-tests.git
   cd python-api-booker-tests
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment.

   **Windows Command Prompt:**

   ```bat
   venv\Scripts\activate.bat
   ```

   **Linux / macOS:**

   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Create a local environment file.

   **Windows:**

   ```bat
   copy .env.example .env
   ```

   **Linux / macOS:**

   ```bash
   cp .env.example .env
   ```

## Running Tests

Running all tests:
```bash
python -m pytest
```

Running tests with Allure results:
```bash
python -m pytest --alluredir=allure-results
```
Generate and open the Allure report:
```bash
allure serve allure-results
```
