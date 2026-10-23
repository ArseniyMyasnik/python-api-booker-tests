# python-api-booker-tests

Automated API tests for the demo booking website [Restful-booker](https://restful-booker.herokuapp.com/apidoc/index.html) using **Python**, **pytest**, **requests**, **Allure Report**, and the **API Client Pattern**.

## Test Coverage

This project includes automated tests for:

- **Auth API**: `POST /auth`
  - Valid and invalid credentials
  - Missing required fields
  - Empty JSON object
  - Unsupported `Content-Type`
  - SQL injection attempt

- **Health Check API**: `GET /ping`
  - API availability check

- **Booking API**: `GET /booking`
  - Retrieve all booking IDs
  - Filter by first name, last name, check-in date, and check-out date
  - Combine supported filters
  - Validate filter boundaries
  - Handle nonexistent names and name combinations
  - Handle invalid check-in and check-out date values and formats
  - Document known check-in and check-out filter defects with `xfail`

## Technology Stack

- **Python 3.10+** — programming language
- **pytest 9.x** — test runner and test organization
- **requests 2.x** — HTTP library
- **Allure Report 2.x** — test reporting integration
- **API Client Pattern** — test architecture pattern

## Project Structure

```text
python-api-booker-tests/
├── api/
│   ├── auth_api.py                # Client for POST /auth
│   ├── health_api.py              # Client for GET /ping
│   ├── get_booking_ids_api.py     # Client for GET /booking and GET /booking/{bookingid}
│   ├── create_booking_api.py      # Client for POST /booking
│   └── delete_booking_api.py      # Client for DELETE /booking/{bookingid}
├── tests/
│   ├── test_auth.py               # Auth API tests
│   ├── test_ping.py               # Health Check API tests
│   └── test_get_booking_ids.py    # Get Booking IDs API tests
├── test_cases/
│   ├── auth_test_cases.md         # Manual Auth API test cases
│   ├── health_check_cases.md      # Manual Health Check API test cases
│   └── get_booking_ids.md         # Manual Get Booking IDs API test cases
├── conftest.py                    # Shared pytest fixtures and test-data cleanup
├── pytest.ini                     # Pytest settings
├── requirements.txt               # Project dependencies
├── .env.example                   # Example environment variables
├── .gitignore                     # Ignored local and generated files
└── README.md                      # Project documentation
```

## Test Data

Tests that create bookings use unique values generated with `uuid4`. The `booking_factory` fixture tracks every created booking and deletes it during teardown, including when a test fails.

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

Run all tests:

```bash
python -m pytest
```

Run tests with Allure results:

```bash
python -m pytest --alluredir=allure-results
```

Generate and open the Allure report:

```bash
allure serve allure-results
```

