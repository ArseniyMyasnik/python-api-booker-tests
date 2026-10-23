import allure
from datetime import date, datetime, timedelta

import pytest


def compare_two_dates(date_one, date_two):
    date_one = datetime.strptime(date_one, "%Y-%m-%d")
    date_two = datetime.strptime(date_two, "%Y-%m-%d")
    return date_one >= date_two


def add_offset_to_date(date_str, offset):
    date_str = date.fromisoformat(date_str)
    date_str = date_str + timedelta(days=offset)
    date_str = date_str.isoformat()
    return date_str


@allure.suite("Get Booking IDs tests")
@allure.feature("Get Booking IDs API")
class TestGetBookingIds:
    @allure.title("Test case GBI-1: Get all booking IDs")
    def test_get_all_booking_ids(self, get_booking_ids_api):

        response = get_booking_ids_api.get_ids()
        assert (
            response.status_code == 200
        ), f"Expected status code 200, got {response.status_code}"

        response_body = response.json()
        assert isinstance(
            response_body, list
        ), f"Expected response body to be a list, got {type(response_body)}"

        for booking in response_body:
            assert isinstance(
                booking, dict
            ), f"Expected booking to be a dict, got {type(booking)}"
            assert (
                "bookingid" in booking
            ), f"Expected bookingid in booking, got {booking}"
            assert isinstance(
                booking["bookingid"], int
            ), f'Expected bookingid to be an int, got {type(booking["bookingid"])}'

    @allure.title("Test case GBI-2: Get booking IDs by first name")
    def test_get_booking_ids_by_first_name(
        self,
        get_booking_ids_api,
        create_booking_api,
        correct_auth_token,
        delete_booking_api,
    ):

        post_id = None
        firstname = "Autotest_GBI-2"
        try:
            response = create_booking_api.create_booking(
                payload={
                    "firstname": firstname,
                    "lastname": "Brown",
                    "totalprice": 111,
                    "depositpaid": True,
                    "bookingdates": {"checkin": "2018-01-01", "checkout": "2019-01-01"},
                    "additionalneeds": "Breakfast",
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"
            post_id = response.json()["bookingid"]

            response = get_booking_ids_api.get_ids(params={"firstname": firstname})
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"

            response_body = response.json()
            assert isinstance(
                response_body, list
            ), f"Expected response body to be a list, got {type(response_body)}"
            assert (
                len(response_body) > 0
            ), f"Expected at least one element in the response, got zero"

            for booking in response_body:
                assert isinstance(
                    booking, dict
                ), f"Expected booking to be a dict, got {type(booking)}"
                assert (
                    "bookingid" in booking
                ), f"Expected bookingid in booking, got {booking}"
                assert isinstance(
                    booking["bookingid"], int
                ), f'Expected bookingid to be an int, got {type(booking["bookingid"])}'

            booking_ids = [booking["bookingid"] for booking in response_body]

            for booking_id in booking_ids:
                response = get_booking_ids_api.get_by_id(booking_id=booking_id)
                assert (
                    response.status_code == 200
                ), f"Expected status code 200, got {response.status_code}"

                response_booking = response.json()
                assert isinstance(
                    response_booking, dict
                ), f"Expected response body to be a dict, got {type(response_booking)}"
                assert (
                    "firstname" in response_booking
                ), f"Expected firstname in booking, got {response_booking}"
                assert (
                    response_booking["firstname"] == firstname
                ), f'Expected first name {firstname}, got {response_booking["firstname"]}'

        finally:
            if post_id is not None:
                delete_response = delete_booking_api.delete_booking(
                    booking_id=post_id, auth_token=correct_auth_token
                )
                assert (
                    delete_response.status_code == 201
                ), f"Expected status code 201, got {delete_response.status_code}"

    @allure.title("Test case GBI-3: Get booking IDs by last name")
    def test_get_booking_ids_by_last_name(
        self,
        get_booking_ids_api,
        create_booking_api,
        correct_auth_token,
        delete_booking_api,
    ):

        post_id = None
        lastname = "Autotest_GBI-3"
        try:
            response = create_booking_api.create_booking(
                payload={
                    "firstname": "James",
                    "lastname": lastname,
                    "totalprice": 111,
                    "depositpaid": True,
                    "bookingdates": {"checkin": "2018-01-01", "checkout": "2019-01-01"},
                    "additionalneeds": "Breakfast",
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"
            post_id = response.json()["bookingid"]

            response = get_booking_ids_api.get_ids(params={"lastname": lastname})
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"

            response_body = response.json()
            assert isinstance(
                response_body, list
            ), f"Expected response body to be a list, got {type(response_body)}"
            assert (
                len(response_body) > 0
            ), "Expected at least one element in the response, got zero"

            for booking in response_body:
                assert isinstance(
                    booking, dict
                ), f"Expected booking to be a dict, got {type(booking)}"
                assert (
                    "bookingid" in booking
                ), f"Expected bookingid in response body, got {booking}"
                assert isinstance(
                    booking["bookingid"], int
                ), f'Expected bookingid to be an int, got {type(booking["bookingid"])}'

            booking_ids = [booking["bookingid"] for booking in response_body]

            for booking_id in booking_ids:
                response = get_booking_ids_api.get_by_id(booking_id=booking_id)
                assert (
                    response.status_code == 200
                ), f"Expected status code 200, got {response.status_code}"

                response_booking = response.json()
                assert isinstance(
                    response_booking, dict
                ), f"Expected response booking to be a dict, got {type(response_booking)}"
                assert (
                    "lastname" in response_booking
                ), f"Expected lastname in response body, got {response_booking}"
                assert (
                    response_booking["lastname"] == lastname
                ), f'Expected lastname {lastname}, got {response_booking["lastname"]}'

        finally:
            if post_id is not None:
                delete_response = delete_booking_api.delete_booking(
                    booking_id=post_id, auth_token=correct_auth_token
                )
                assert (
                    delete_response.status_code == 201
                ), f"Expected status code 201, got {delete_response.status_code}"

    @allure.title("Test case GBI-4: Get booking IDs by check-in date")
    def test_get_booking_ids_by_checkin_date(
        self,
        get_booking_ids_api,
        create_booking_api,
        correct_auth_token,
        delete_booking_api,
    ):

        post_id = None
        checkin_date = "2026-10-13"
        try:
            response = create_booking_api.create_booking(
                payload={
                    "firstname": "James",
                    "lastname": "Doe",
                    "totalprice": 111,
                    "depositpaid": True,
                    "bookingdates": {"checkin": checkin_date, "checkout": "2026-10-20"},
                    "additionalneeds": "Breakfast",
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"
            post_id = response.json()["bookingid"]

            response = get_booking_ids_api.get_ids(
                params={"checkin": add_offset_to_date(checkin_date, offset=-1)}
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"

            response_body = response.json()
            assert isinstance(
                response_body, list
            ), f"Expected response body to be a list, got {type(response_body)}"
            assert (
                len(response_body) > 0
            ), "Expected at least one element in the response, got zero"

            for booking in response_body:
                assert isinstance(
                    booking, dict
                ), f"Expected booking to be a dict, got {type(booking)}"
                assert (
                    "bookingid" in booking
                ), f"Expected bookingid in booking, got {booking}"
                assert isinstance(
                    booking["bookingid"], int
                ), f"Expected bookingid to be an int, got {type(booking)}"

            booking_ids = [booking["bookingid"] for booking in response_body]
            for booking_id in booking_ids:
                response = get_booking_ids_api.get_by_id(booking_id=booking_id)
                assert (
                    response.status_code == 200
                ), f"Expected status code 200, got {response.status_code}"

                response_booking = response.json()
                assert isinstance(
                    response_booking, dict
                ), f"Expected response booking to be a dict, got {type(response_booking)}"
                assert (
                    "bookingdates" in response_booking
                ), f"Expected booking dates in response booking, got {response_booking}"
                assert isinstance(
                    response_booking["bookingdates"], dict
                ), f'Expected booking dates to be a dict, got {type(response_booking["bookingdates"])}'
                assert (
                    "checkin" in response_booking["bookingdates"]
                ), f"Expected check-in in response booking, got {response_booking}"
                assert compare_two_dates(
                    response_booking["bookingdates"]["checkin"], checkin_date
                ), f'Expected date in the response to be greater than or equal to the filter date, got {response_booking["bookingdates"]["checkin"]} !>= {checkin_date}'
        finally:
            if post_id is not None:
                response = delete_booking_api.delete_booking(
                    booking_id=post_id, auth_token=correct_auth_token
                )
                assert (
                    response.status_code == 201
                ), f"Expected status code 201, got {response.status_code}"

    @pytest.mark.xfail(
        strict=True,
        reason='Known Restful-booker defect: the checkout filter uses "<" instead of documented ">="',
    )
    @allure.title("Test case GBI-5: Get booking IDs by check-out date")
    def test_get_booking_ids_by_checkout_date(
        self,
        create_booking_api,
        get_booking_ids_api,
        correct_auth_token,
        delete_booking_api,
    ):

        post_id = None
        checkout_date = "2026-10-20"
        try:
            response = create_booking_api.create_booking(
                payload={
                    "firstname": "James",
                    "lastname": "Doe",
                    "totalprice": 111,
                    "depositpaid": True,
                    "bookingdates": {
                        "checkin": "2026-10-13",
                        "checkout": checkout_date,
                    },
                    "additionalneeds": "Breakfast",
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"
            post_id = response.json()["bookingid"]

            response = get_booking_ids_api.get_ids(
                params={"checkout": add_offset_to_date(checkout_date, -1)}
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"

            response_body = response.json()
            assert isinstance(
                response_body, list
            ), f"Expected response body to be a list, got {type(response_body)}"
            assert (
                len(response_body) > 0
            ), f"Expected at least one element in the response, got zero"

            for booking in response_body:
                assert isinstance(
                    booking, dict
                ), f"Expected booking to be a dict, got {type(booking)}"
                assert (
                    "bookingid" in booking
                ), f"Expected bookingid in booking, got {booking}"
                assert isinstance(
                    booking["bookingid"], int
                ), f"Expected bookingid to be an int, got {type(booking)}"

            booking_ids = [booking["bookingid"] for booking in response_body]

            for booking_id in booking_ids:
                response = get_booking_ids_api.get_by_id(booking_id=booking_id)
                assert (
                    response.status_code == 200
                ), f"Expected status code 200, got {response.status_code}"

                response_booking = response.json()
                assert isinstance(
                    response_booking, dict
                ), f"Expected response booking to be a dict, got {type(response_booking)}"
                assert (
                    "bookingdates" in response_booking
                ), f"Expected booking dates in response booking, got {response_booking}"
                assert isinstance(
                    response_booking["bookingdates"], dict
                ), f'Expected booking dates to be a dict, got {type(response_booking["bookingdates"])}'
                assert (
                    "checkout" in response_booking["bookingdates"]
                ), f"Expected check-out in booking, got {response_booking}"
                assert compare_two_dates(
                    response_booking["bookingdates"]["checkout"], checkout_date
                ), f'Expected date in the response to be greater than or equal to the filter date, got {response_booking["bookingdates"]["checkout"]} !>= {checkout_date}'

        finally:
            if post_id is not None:
                response = delete_booking_api.delete_booking(
                    auth_token=correct_auth_token, booking_id=post_id
                )
                assert (
                    response.status_code == 201
                ), f"Expected status code 201, got {response.status_code}"

    @allure.title("Test case GBI-6: Get booking IDs by first name and check-in date")
    def test_get_booking_ids_by_firstname_and_checkin_date(
        self,
        create_booking_api,
        get_booking_ids_api,
        correct_auth_token,
        delete_booking_api,
    ):

        post_id = None
        firstname = "Autotest_GBI-6"
        checkin_date = "2026-10-13"
        try:
            response = create_booking_api.create_booking(
                payload={
                    "firstname": firstname,
                    "lastname": "Doe",
                    "totalprice": 111,
                    "depositpaid": True,
                    "bookingdates": {"checkin": checkin_date, "checkout": "2026-10-20"},
                    "additionalneeds": "Breakfast",
                }
            )

            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"
            post_id = response.json()["bookingid"]

            response = get_booking_ids_api.get_ids(
                params={
                    "firstname": firstname,
                    "checkin": add_offset_to_date(checkin_date, -1),
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"

            response_body = response.json()
            assert isinstance(
                response_body, list
            ), f"Expected response body to be a list, got {type(response_body)}"
            assert (
                len(response_body) > 0
            ), f"Expected at least one element in the response, got zero"

            for booking in response_body:
                assert isinstance(
                    booking, dict
                ), f"Expected response body to be a dict, got {type(booking)}"
                assert (
                    "bookingid" in booking
                ), f"Expected bookingid in booking, got {booking}"
                assert isinstance(
                    booking["bookingid"], int
                ), f'Expected bookingid to be an int, got {booking["bookingid"]}'

            booking_ids = [booking["bookingid"] for booking in response_body]

            for booking_id in booking_ids:
                response = get_booking_ids_api.get_by_id(booking_id=booking_id)
                assert (
                    response.status_code == 200
                ), f"Expected status code 200, got {response.status_code}"

                response_booking = response.json()
                assert isinstance(
                    response_booking, dict
                ), f"Expected response body to be a dict, got {type(response_booking)}"
                assert (
                    "firstname" in response_booking
                ), f"Expected first name in response booking, got {response_booking}"
                assert (
                    response_booking["firstname"] == firstname
                ), f'Expected firstname {firstname}, got {response_booking["firstname"]}'
                assert (
                    "bookingdates" in response_booking
                ), f"Expected booking dates in response booking, got {response_booking}"
                assert isinstance(
                    response_booking["bookingdates"], dict
                ), f'Expected booking dates to be a dict, got {type(response_booking["bookingdates"])}'
                assert (
                    "checkin" in response_booking["bookingdates"]
                ), f'Expected checkin in booking dates, got {response_booking["bookingdates"]}'
                assert compare_two_dates(
                    response_booking["bookingdates"]["checkin"], checkin_date
                ), f'Expected date in the response to be greater than or equal to the filter date, got {response_booking["bookingdates"]["checkin"]} !>= {checkin_date}'

        finally:
            if post_id is not None:
                response = delete_booking_api.delete_booking(
                    auth_token=correct_auth_token, booking_id=post_id
                )
                assert (
                    response.status_code == 201
                ), f"Expected status code 201, got {response.status_code}"

    @pytest.mark.xfail(
        strict=True,
        reason='Known Restful-booker defect: the checkout filter uses "<" instead of documented ">="',
    )
    @allure.title("Test case GBI-7: Get booking IDs by last name and check-out date")
    def test_get_booking_ids_by_lastname_and_checkout_date(
        self,
        create_booking_api,
        get_booking_ids_api,
        correct_auth_token,
        delete_booking_api,
    ):

        post_id = None
        lastname = "Autotest_GBI-7"
        checkout_date = "2026-10-20"
        try:
            response = create_booking_api.create_booking(
                payload={
                    "firstname": "James",
                    "lastname": lastname,
                    "totalprice": 111,
                    "depositpaid": True,
                    "bookingdates": {
                        "checkin": "2026-10-13",
                        "checkout": checkout_date,
                    },
                    "additionalneeds": "Breakfast",
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"
            post_id = response.json()["bookingid"]

            response = get_booking_ids_api.get_ids(
                params={
                    "lastname": lastname,
                    "checkout": add_offset_to_date(checkout_date, -1),
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"

            response_body = response.json()
            assert isinstance(
                response_body, list
            ), f"Expected response body to be a list, got {type(response_body)}"
            assert (
                len(response_body) > 0
            ), f"Expected at least one element in the response, got zero"

            for booking in response_body:
                assert isinstance(
                    booking, dict
                ), f"Expected response body to be a dict, got {type(booking)}"
                assert (
                    "bookingid" in booking
                ), f"Expected bookingid in booking, got {booking}"
                assert isinstance(
                    booking["bookingid"], int
                ), f'Expected bookingid to be an int, got {booking["bookingid"]}'

            booking_ids = [booking["bookingid"] for booking in response_body]

            for booking_id in booking_ids:
                response = get_booking_ids_api.get_by_id(booking_id=booking_id)
                assert (
                    response.status_code == 200
                ), f"Expected status code 200, got {response.status_code}"

                response_booking = response.json()
                assert isinstance(
                    response_booking, dict
                ), f"Expected response body to be a dict, got {type(response_booking)}"
                assert (
                    "lastname" in response_booking
                ), f"Expected last name in response booking, got {response_booking}"
                assert (
                    response_booking["lastname"] == lastname
                ), f'Expected last name {lastname}, got {response_booking["lastname"]}'
                assert (
                    "bookingdates" in response_booking
                ), f"Expected booking dates in response booking, got {response_booking}"
                assert isinstance(
                    response_booking["bookingdates"], dict
                ), f'Expected booking dates to be a dict, got {type(response_booking["bookingdates"])}'
                assert (
                    "checkout" in response_booking["bookingdates"]
                ), f'Expected checkout in booking dates, got {response_booking["bookingdates"]}'
                assert compare_two_dates(
                    response_booking["bookingdates"]["checkout"], checkout_date
                ), f'Expected date in the response to be greater than or equal to the filter date, got {response_booking["bookingdates"]["checkout"]} !>= {checkout_date}'

        finally:
            if post_id is not None:
                response = delete_booking_api.delete_booking(
                    auth_token=correct_auth_token, booking_id=post_id
                )
                assert (
                    response.status_code == 201
                ), f"Expected status code 201, got {response.status_code}"

    @pytest.mark.xfail(
        strict=True,
        reason='Known Restful-booker defect: the checkout filter uses "<" instead of documented ">="',
    )
    @allure.title("Test case GBI-8: Get booking IDs using all filters")
    def test_get_booking_ids_using_all_filters(
        self,
        create_booking_api,
        get_booking_ids_api,
        correct_auth_token,
        delete_booking_api,
    ):

        post_id = None
        firstname = "Autotest_GBI-8_first"
        lastname = "Autotest_GBI-8_last"
        checkin_date = "2026-10-13"
        checkout_date = "2026-10-20"
        try:
            response = create_booking_api.create_booking(
                payload={
                    "firstname": firstname,
                    "lastname": lastname,
                    "totalprice": 111,
                    "depositpaid": True,
                    "bookingdates": {
                        "checkin": checkin_date,
                        "checkout": checkout_date,
                    },
                    "additionalneeds": "Breakfast",
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"
            post_id = response.json()["bookingid"]

            response = get_booking_ids_api.get_ids(
                params={
                    "firstname": firstname,
                    "lastname": lastname,
                    "checkin": add_offset_to_date(checkin_date, -1),
                    "checkout": add_offset_to_date(checkout_date, -1),
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"

            response_body = response.json()
            assert isinstance(
                response_body, list
            ), f"Expected response body to be a list, got {type(response_body)}"
            assert (
                len(response_body) > 0
            ), "Expected at least one element in the response, got zero"

            for booking in response_body:
                assert isinstance(
                    booking, dict
                ), f"Expected response body to be a dict, got {type(booking)}"
                assert (
                    "bookingid" in booking
                ), f"Expected bookingid in booking, got {booking}"
                assert isinstance(
                    booking["bookingid"], int
                ), f'Expected bookingid to be an int, got {booking["bookingid"]}'

            booking_ids = [booking["bookingid"] for booking in response_body]

            for booking_id in booking_ids:
                response = get_booking_ids_api.get_by_id(booking_id=booking_id)
                assert (
                    response.status_code == 200
                ), f"Expected status code 200, got {response.status_code}"

                response_booking = response.json()
                assert isinstance(
                    response_booking, dict
                ), f"Expected response booking to be a dict, got {type(response_booking)}"
                assert (
                    "firstname" in response_booking
                ), f"Expected firstname in response booking, got {response_booking}"
                assert (
                    response_booking["firstname"] == firstname
                ), f'Expected first name {firstname}, got {response_booking["firstname"]}'
                assert (
                    "lastname" in response_booking
                ), f"Expected lastname in response booking, got {response_booking}"
                assert (
                    response_booking["lastname"] == lastname
                ), f'Expected last name {lastname}, got {response_booking["lastname"]}'
                assert (
                    "bookingdates" in response_booking
                ), f"Expected booking dates in response booking, got {response_booking}"
                assert isinstance(
                    response_booking["bookingdates"], dict
                ), f'Expected bookingdates to be a dict, got {type(response_booking["bookingdates"])}'
                assert (
                    "checkin" in response_booking["bookingdates"]
                ), f'Expected check in in booking dates, got {response_booking["bookingdates"]}'
                assert compare_two_dates(
                    response_booking["bookingdates"]["checkin"], checkin_date
                ), f'Expected date in the response to be greater than or equal to the filter date, got {response_booking["bookingdates"]["checkin"]} !>= {checkin_date}'
                assert (
                    "checkout" in response_booking["bookingdates"]
                ), f'Expected check out in booking dates, got {response_booking["bookingdates"]}'
                assert compare_two_dates(
                    response_booking["bookingdates"]["checkout"], checkout_date
                ), f'Expected date in the response to be greater than or equal to the filter date, got {response_booking["bookingdates"]["checkout"]} !>= {checkout_date}'

        finally:
            if post_id is not None:
                response = delete_booking_api.delete_booking(
                    auth_token=correct_auth_token, booking_id=post_id
                )
                assert (
                    response.status_code == 201
                ), f"Expected status code 201, got {response.status_code}"

    @allure.title("Test case GBI-9: Check-in filter boundary: one day before")
    def test_checkin_filter_boundary_one_day_before(
        self,
        create_booking_api,
        get_booking_ids_api,
        correct_auth_token,
        delete_booking_api,
    ):

        post_id = None
        firstname = "Autotest_GBI-9"
        checkin_date = "2026-10-13"
        try:
            response = create_booking_api.create_booking(
                payload={
                    "firstname": firstname,
                    "lastname": "Doe",
                    "totalprice": 111,
                    "depositpaid": True,
                    "bookingdates": {"checkin": checkin_date, "checkout": "2026-10-20"},
                    "additionalneeds": "Breakfast",
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"
            post_id = response.json()["bookingid"]

            response = get_booking_ids_api.get_ids(
                params={
                    "firstname": firstname,
                    "checkin": add_offset_to_date(checkin_date, -1),
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"

            response_body = response.json()
            assert isinstance(
                response_body, list
            ), f"Expected response body to be a list, got {type(response_body)}"
            assert post_id in [
                booking["bookingid"] for booking in response_body
            ], f'Expected post id {post_id} in response booking, got {[booking["bookingid"] for booking in response_body]}'

        finally:
            if post_id is not None:
                response = delete_booking_api.delete_booking(
                    auth_token=correct_auth_token, booking_id=post_id
                )
                assert (
                    response.status_code == 201
                ), f"Expected status code 201, got {response.status_code}"

    @pytest.mark.xfail(
        strict=True,
        reason='Known Restful-booker defect: the checkin filter uses ">" instead of documented ">="',
    )
    @allure.title("Test case GBI-9.1: Check-in filter boundary: exact date")
    def test_check_checkin_filter_boundary_exact_date(
        self,
        create_booking_api,
        get_booking_ids_api,
        correct_auth_token,
        delete_booking_api,
    ):

        post_id = None
        firstname = "Autotest_GBI-9.1"
        checkin_date = "2026-10-13"
        try:
            response = create_booking_api.create_booking(
                payload={
                    "firstname": firstname,
                    "lastname": "Doe",
                    "totalprice": 111,
                    "depositpaid": True,
                    "bookingdates": {"checkin": checkin_date, "checkout": "2026-10-20"},
                    "additionalneeds": "Breakfast",
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"
            post_id = response.json()["bookingid"]

            response = get_booking_ids_api.get_ids(
                params={"firstname": firstname, "checkin": checkin_date}
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"

            response_body = response.json()
            assert isinstance(
                response_body, list
            ), f"Expected response body to be a list, got {type(response_body)}"
            assert post_id in [
                booking["bookingid"] for booking in response_body
            ], f'Expected post id {post_id} in response booking, got {[booking["bookingid"] for booking in response_body]}'

        finally:
            if post_id is not None:
                response = delete_booking_api.delete_booking(
                    auth_token=correct_auth_token, booking_id=post_id
                )
                assert (
                    response.status_code == 201
                ), f"Expected status code 201, got {response.status_code}"

    @allure.title("Test case GBI-9.2: Check-in filter boundary: one day after")
    def test_checkin_filter_boundary_one_day_after(
        self,
        create_booking_api,
        get_booking_ids_api,
        correct_auth_token,
        delete_booking_api,
    ):

        post_id = None
        firstname = "Autotest_GBI-9.2"
        checkin_date = "2026-10-13"
        try:
            response = create_booking_api.create_booking(
                payload={
                    "firstname": firstname,
                    "lastname": "Doe",
                    "totalprice": 111,
                    "depositpaid": True,
                    "bookingdates": {"checkin": checkin_date, "checkout": "2026-10-20"},
                    "additionalneeds": "Breakfast",
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"
            post_id = response.json()["bookingid"]

            response = get_booking_ids_api.get_ids(
                params={
                    "firstname": firstname,
                    "checkin": add_offset_to_date(checkin_date, +1),
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"

            response_body = response.json()
            assert isinstance(
                response_body, list
            ), f"Expected response body to be a list, got {type(response_body)}"
            assert post_id not in [
                booking["bookingid"] for booking in response_body
            ], f"Unexpected post id {post_id} in response body, got {response_body}"

        finally:
            if post_id is not None:
                response = delete_booking_api.delete_booking(
                    auth_token=correct_auth_token, booking_id=post_id
                )

                assert (
                    response.status_code == 201
                ), f"Expected status code 201, got {response.status_code}"

    @pytest.mark.xfail(
        strict=True,
        reason='Known Restful-booker defect: the checkout filter uses ">" instead of documented ">="',
    )
    @allure.title("Test case GBI-10: Check-out filter boundary: one day before")
    def test_check_checkout_filter_boundary_one_day_before(
        self,
        create_booking_api,
        get_booking_ids_api,
        correct_auth_token,
        delete_booking_api,
    ):

        post_id = None
        firstname = "Autotest_GBI-10"
        checkout_date = "2026-10-20"
        try:
            response = create_booking_api.create_booking(
                payload={
                    "firstname": firstname,
                    "lastname": "Doe",
                    "totalprice": 111,
                    "depositpaid": True,
                    "bookingdates": {
                        "checkin": "2026-10-13",
                        "checkout": checkout_date,
                    },
                    "additionalneeds": "Breakfast",
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"
            post_id = response.json()["bookingid"]

            response = get_booking_ids_api.get_ids(
                params={
                    "firstname": firstname,
                    "checkout": add_offset_to_date(checkout_date, -1),
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"

            response_body = response.json()
            assert isinstance(
                response_body, list
            ), f"Expected response body to be a list, got {type(response_body)}"
            assert post_id in [
                booking["bookingid"] for booking in response_body
            ], f'Expected post id {post_id} in response booking, got {[booking["bookingid"] for booking in response_body]}'

        finally:
            if post_id is not None:
                response = delete_booking_api.delete_booking(
                    auth_token=correct_auth_token, booking_id=post_id
                )
                assert (
                    response.status_code == 201
                ), f"Expected status code 201, got {response.status_code}"

    @allure.title("Test case GBI-10.1: Check-out filter boundary: exact date")
    def test_check_checkout_filter_boundary_exact_date(
        self,
        create_booking_api,
        get_booking_ids_api,
        correct_auth_token,
        delete_booking_api,
    ):

        post_id = None
        firstname = "Autotest_GBI-10.1"
        checkout_date = "2026-10-20"
        try:
            response = create_booking_api.create_booking(
                payload={
                    "firstname": firstname,
                    "lastname": "Doe",
                    "totalprice": 111,
                    "depositpaid": True,
                    "bookingdates": {
                        "checkin": "2026-10-13",
                        "checkout": checkout_date,
                    },
                    "additionalneeds": "Breakfast",
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"
            post_id = response.json()["bookingid"]

            response = get_booking_ids_api.get_ids(
                params={"firstname": firstname, "checkout": checkout_date}
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"

            response_body = response.json()
            assert isinstance(
                response_body, list
            ), f"Expected response body to be a list, got {type(response_body)}"
            assert post_id in [
                booking["bookingid"] for booking in response_body
            ], f'Expected post id {post_id} in response booking, got {[booking["bookingid"] for booking in response_body]}'

        finally:
            if post_id is not None:
                response = delete_booking_api.delete_booking(
                    auth_token=correct_auth_token, booking_id=post_id
                )
                assert (
                    response.status_code == 201
                ), f"Expected status code 201, got {response.status_code}"

    @pytest.mark.xfail(
        strict=True,
        reason='Known Restful-booker defect: the checkout filter uses ">" instead of documented ">="',
    )
    @allure.title("Test case GBI-10.2: Check-out filter boundary: one day after")
    def test_check_checkout_filter_boundary_one_day_after(
        self,
        create_booking_api,
        get_booking_ids_api,
        correct_auth_token,
        delete_booking_api,
    ):

        post_id = None
        firstname = "Autotest_GBI-10.2"
        checkout_date = "2026-10-20"
        try:
            response = create_booking_api.create_booking(
                payload={
                    "firstname": firstname,
                    "lastname": "Doe",
                    "totalprice": 111,
                    "depositpaid": True,
                    "bookingdates": {
                        "checkin": "2026-10-13",
                        "checkout": checkout_date,
                    },
                    "additionalneeds": "Breakfast",
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"
            post_id = response.json()["bookingid"]

            response = get_booking_ids_api.get_ids(
                params={
                    "firstname": firstname,
                    "checkout": add_offset_to_date(checkout_date, +1),
                }
            )
            assert (
                response.status_code == 200
            ), f"Expected status code 200, got {response.status_code}"

            response_body = response.json()
            assert isinstance(
                response_body, list
            ), f"Expected response body to be a list, got {type(response_body)}"
            assert post_id not in [
                booking["bookingid"] for booking in response_body
            ], f"Unexpected post id {post_id} in response body, got {response_body}"

        finally:
            if post_id is not None:
                response = delete_booking_api.delete_booking(
                    auth_token=correct_auth_token, booking_id=post_id
                )

                assert (
                    response.status_code == 201
                ), f"Expected status code 201, got {response.status_code}"

    @allure.title("Test case GBI-11: Get booking IDs with a nonexistent first name")
    def test_get_booking_ids_with_nonexistent_firstname(self, get_booking_ids_api):

        response = get_booking_ids_api.get_ids(
            params={"firstname": "NonExistent_GBI-11"}
        )
        assert (
            response.status_code == 200
        ), f"Expected status code 200, got {response.status_code}"

        response_body = response.json()
        assert isinstance(
            response_body, list
        ), f"Expected response body to be a list, got {type(response_body)}"
        assert (
            len(response_body) == 0
        ), f"Expected an empty response body, got {response_body}"

    @allure.title(
        "Test case GBI-12: Get booking IDs with a nonexistent first name and last name combination"
    )
    def test_get_booking_ids_with_nonexistent_firstname_and_lastname(
        self, get_booking_ids_api
    ):

        response = get_booking_ids_api.get_ids(
            params={
                "firstname": "NonExistent_GBI-11_first",
                "lastname": "NonExistent_GBI-11_last",
            }
        )
        assert (
            response.status_code == 200
        ), f"Expected status code 200, got {response.status_code}"

        response_body = response.json()
        assert isinstance(
            response_body, list
        ), f"Expected response body to be list, got {type(response_body)}"
        assert (
            len(response_body) == 0
        ), f"Expected an empty response body, got {response_body}"

    @allure.title("Test case GBI-13: Get booking IDs with invalid check-in date value")
    def test_get_booking_ids_with_invalid_checkin_data_value(self, get_booking_ids_api):

        response = get_booking_ids_api.get_ids(params={"checkin": "2020-25-10"})
        assert (
            response.status_code == 500
        ), f"Expected status code 500, got {response.status_code}"
        assert (
            response.text == "Internal Server Error"
        ), f"Expected to get Internal Server Error, got {response.text}"

    @allure.title("Test case GBI-14: Get booking IDs with invalid check-in date format")
    def test_get_booking_ids_with_invalid_checkin_data_format(
        self, get_booking_ids_api
    ):

        response = get_booking_ids_api.get_ids(params={"checkin": "15.10.2026"})
        assert (
            response.status_code == 500
        ), f"Expected status code 500, got {response.status_code}"
        assert (
            response.text == "Internal Server Error"
        ), f"Expected to get Internal Server Error, got {response.text}"

    @allure.title("Test case GBI-15: Get booking IDs with invalid check-out date value")
    def test_get_booking_ids_with_invalid_checkout_data_value(
        self, get_booking_ids_api
    ):

        response = get_booking_ids_api.get_ids(params={"checkout": "2020-25-10"})
        assert (
            response.status_code == 500
        ), f"Expected status code 500, got {response.status_code}"
        assert (
            response.text == "Internal Server Error"
        ), f"Expected to get Internal Server Error, got {response.text}"

    @allure.title(
        "Test case GBI-16: Get booking IDs with invalid check-out date format"
    )
    def test_get_booking_ids_with_invalid_checkout_data_format(
        self, get_booking_ids_api
    ):

        response = get_booking_ids_api.get_ids(params={"checkout": "15.10.2026"})
        assert (
            response.status_code == 500
        ), f"Expected status code 500, got {response.status_code}"
        assert (
            response.text == "Internal Server Error"
        ), f"Expected to get Internal Server Error, got {response.text}"
