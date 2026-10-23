# Test Cases: Get Booking IDs API

## Scope

This document covers test cases for the get booking IDs API

## Base URL

`https://restful-booker.herokuapp.com`

## Endpoints covered

- `POST /auth`
- `POST /booking`
- `GET /booking`
- `GET /booking/{bookingid}`
- `DELETE /booking/{bookingid}`

## Common setup for data-dependent cases

1. Create a booking using `POST /booking` with the first name, last name, and dates stated in the test case
2. Save `bookingid` from the response
3. Obtain a valid token through `POST /auth` before cleanup
4. Delete the created booking with `DELETE /booking/{bookingid}` and header `Cookie: token=<token>`

---

## Test case GBI-1: Get all booking IDs

**Endpoint:** `GET /booking`

**Preconditions:**
- Booking API is available

**Steps:**
1. Send `GET /booking`
2. Inspect the response status code and body

**Expected result:**
- Status code is `200`
- Response body is an array
- Every item is an object containing integer field `bookingid`

## Test case GBI-2: Get booking IDs by first name

**Endpoints:**
- `POST /booking`
- `GET /booking?firstname=Autotest_GBI-2`
- `GET /booking/{bookingid}`
- `DELETE /booking/{bookingid}`

**Steps:**
1. Create a booking with first name `Autotest_GBI-2`
2. Send the filter request
3. For every returned ID, request booking details
4. Delete the created booking

**Expected result:**
- Creation and filter requests return `200`
- The filter response is a non-empty array of integer booking IDs
- Every returned booking has `firstname` equal to `Autotest_GBI-2`
- Deletion returns `201`

## Test case GBI-3: Get booking IDs by last name

**Endpoints:**
- `POST /booking`
- `GET /booking?lastname=Autotest_GBI-3`
- `GET /booking/{bookingid}`
- `DELETE /booking/{bookingid}`

**Steps:**
1. Create a booking with last name `Autotest_GBI-3`
2. Send the filter request
3. For every returned ID, request booking details
4. Delete the created booking

**Expected result:**
- Creation and filter requests return `200`
- The filter response is a non-empty array of integer booking IDs
- Every returned booking has `lastname` equal to `Autotest_GBI-3`
- Deletion returns `201`

## Test case GBI-4: Get booking IDs by check-in date

**Endpoints:**
- `POST /booking`
- `GET /booking?checkin=2026-10-12`
- `GET /booking/{bookingid}`
- `DELETE /booking/{bookingid}`

**Steps:**
1. Create a booking with check-in date `2026-10-13`
2. Send the filter request
3. Request details for each returned ID
4. Delete the created booking

**Expected result:**
- Creation and filter requests return `200`
- The filter response is non-empty and contains integer booking IDs
- Every returned booking has `bookingdates.checkin` greater than or equal to `2026-10-13`
- Deletion returns `201`

## Test case GBI-5: Get booking IDs by check-out date

**Endpoints:**
- `POST /booking`
- `GET /booking?checkout=2026-10-19`
- `GET /booking/{bookingid}`
- `DELETE /booking/{bookingid}`

**Steps:**
1. Create a booking with check-out date `2026-10-20`
2. Send the filter request
3. Request details for each returned ID
4. Delete the created booking

**Expected result:**
- Creation and filter requests return `200`
- The filter response is non-empty and contains integer booking IDs
- Every returned booking has `bookingdates.checkout` greater than or equal to `2026-10-20`
- Deletion returns `201`

## Test case GBI-6: Get booking IDs by first name and check-in date

**Endpoints:**
- `POST /booking`
- `GET /booking?firstname=Autotest_GBI-6&checkin=2026-10-12`
- `GET /booking/{bookingid}`
- `DELETE /booking/{bookingid}`

**Steps:**
1. Create a booking with first name `Autotest_GBI-6` and check-in `2026-10-13`
2. Send the filter request
3. Request details for each returned ID
4. Delete the created booking

**Expected result:**
- Creation and filter requests return `200`
- The filter response is a non-empty array of integer booking IDs.
- Each returned booking has the requested first name
- Each returned booking has check-in date greater than or equal to `2026-10-13`
- Deletion returns `201`

## Test case GBI-7: Get booking IDs by last name and check-out date

**Endpoints:**
- `POST /booking`
- `GET /booking?lastname=Autotest_GBI-7&checkout=2026-10-19`
- `GET /booking/{bookingid}`
- `DELETE /booking/{bookingid}`

**Steps:**
1. Create a booking with last name `Autotest_GBI-7` and check-out `2026-10-20`
2. Send the filter request
3. Request details for each returned ID
4. Delete the created booking

**Expected result:**
- Creation and filter requests return `200`
- The filter response is a non-empty array of integer booking IDs.
- Each returned booking has the requested last name
- Each returned booking has check-out date greater than or equal to `2026-10-20`
- Deletion returns `201`

## Test case GBI-8: Get booking IDs using all filters

**Endpoints:**
- `POST /booking`
- `GET /booking?firstname=Autotest_GBI-8_first&lastname=Autotest_GBI-8_last&checkin=2026-10-12&checkout=2026-10-19`
- `GET /booking/{bookingid}`
- `DELETE /booking/{bookingid}`

**Steps:**
1. Create a booking with first name `Autotest_GBI-8_first`, last name `Autotest_GBI-8_last`, check-in `2026-10-13`, and check-out `2026-10-20`
2. Send the filter request with all four parameters
3. Request details for each returned ID
4. Delete the created booking

**Expected result:**
- Creation and filter requests return `200`
- The filter response is a non-empty array of integer booking IDs.
- Every returned booking has `firstname` equal to `Autotest_GBI-8_first` and `lastname` equal to `Autotest_GBI-8_last`.
- Every returned booking has check-in date greater than or equal to `2026-10-13` and check-out date greater than or equal to `2026-10-20`.
- Deletion returns `201`

## Test case GBI-9: Check-in filter boundary: one day before

**Endpoints:** `POST /booking`, `GET /booking?firstname=Autotest_GBI-9&checkin=2026-10-12`, `DELETE /booking/{bookingid}`

**Preconditions:**
- Auth API and Booking API are available

**Steps:**
1. Send `POST /booking` to create a booking with `firstname` equal to `Autotest_GBI-9` and `bookingdates.checkin` equal to `2026-10-13`
2. Save the `bookingid` returned by `POST /booking` as `post_id`
3. Send `GET /booking?firstname=Autotest_GBI-9&checkin=2026-10-12`
4. Check whether `post_id` is present in the response array
5. Delete the created booking with `DELETE /booking/{post_id}`

**Expected result:**
- `POST /booking` returns status code `200` and contains `bookingid`.
- `GET /booking?firstname=Autotest_GBI-9&checkin=2026-10-12` returns status code `200` and an array
- The response array contains `post_id`
- `DELETE /booking/{post_id}` returns status code `201`

## Test case GBI-9.1: Check-in filter boundary: exact date

**Endpoints:**
- `POST /booking`
- `GET /booking?firstname=Autotest_GBI-9.1&checkin=2026-10-13`
- `DELETE /booking/{bookingid}`

**Preconditions:**
- Auth API and Booking API are available

**Steps:**
1. Create a booking with `firstname` equal to `Autotest_GBI-9.1` and `bookingdates.checkin` equal to `2026-10-13`
2. Save its `bookingid` as `post_id`
3. Send `GET /booking?firstname=Autotest_GBI-9.1&checkin=2026-10-13`
4. Check whether `post_id` is present in the response array
5. Delete the created booking

**Expected result:**
- The creation request returns `200` and contains `bookingid`
- The filter request returns `200` and an array
- The response array contains `post_id`
- The delete request returns `201`

## Test case GBI-9.2: Check-in filter boundary: one day after

**Endpoints:**
- `POST /booking`
- `GET /booking?firstname=Autotest_GBI-9.2&checkin=2026-10-14`
- `DELETE /booking/{bookingid}`

**Preconditions:**
- Auth API and Booking API are available

**Steps:**
1. Create a booking with `firstname` equal to `Autotest_GBI-9.2` and `bookingdates.checkin` equal to `2026-10-13`
2. Save its `bookingid` as `post_id`
3. Send `GET /booking?firstname=Autotest_GBI-9.2&checkin=2026-10-14`
4. Check whether `post_id` is absent from the response array
5. Delete the created booking

**Expected result:**
- The creation request returns `200` and contains `bookingid`
- The filter request returns `200` and an array
- The response array does not contain `post_id`
- The delete request returns `201`

## Test case GBI-10: Check-out filter boundary: one day before

**Endpoints:**
- `POST /booking`
- `GET /booking?firstname=Autotest_GBI-10&checkout=2026-10-19`
- `DELETE /booking/{bookingid}`

**Preconditions:**
- Auth API and Booking API are available

**Steps:**
1. Create a booking with `firstname` equal to `Autotest_GBI-10` and `bookingdates.checkout` equal to `2026-10-20`
2. Save its `bookingid` as `post_id`
3. Send `GET /booking?firstname=Autotest_GBI-10&checkout=2026-10-19`
4. Check whether `post_id` is present in the response array.
5. Delete the created booking.

**Expected result:**
- The creation request returns `200` and contains `bookingid`
- The filter request returns `200` and an array
- The response array contains `post_id`
- The delete request returns `201`

## Test case GBI-10.1: Check-out filter boundary: exact date

**Endpoints:**
- `POST /booking`
- `GET /booking?firstname=Autotest_GBI-10.1&checkout=2026-10-20`
- `DELETE /booking/{bookingid}`

**Preconditions:**
- Auth API and Booking API are available

**Steps:**
1. Create a booking with `firstname` equal to `Autotest_GBI-10.1` and `bookingdates.checkout` equal to `2026-10-20`
2. Save its `bookingid` as `post_id`
3. Send `GET /booking?firstname=Autotest_GBI-10.1&checkout=2026-10-20`
4. Check whether `post_id` is present in the response array
5. Delete the created booking

**Expected result:**
- The creation request returns `200` and contains `bookingid`.
- The filter request returns `200` and an array.
- The response array contains `post_id`.
- The delete request returns `201`.

## Test case GBI-10.2: Check-out filter boundary: one day after

**Endpoints:**
- `POST /booking`
- `GET /booking?firstname=Autotest_GBI-10.2&checkout=2026-10-21`
- `DELETE /booking/{bookingid}`

**Preconditions:**
- Auth API and Booking API are available

**Steps:**
1. Create a booking with `firstname` equal to `Autotest_GBI-10.2` and `bookingdates.checkout` equal to `2026-10-20`
2. Save its `bookingid` as `post_id`
3. Send `GET /booking?firstname=Autotest_GBI-10.2&checkout=2026-10-21`
4. Check whether `post_id` is absent from the response array
5. Delete the created booking

**Expected result:**
- The creation request returns `200` and contains `bookingid`
- The filter request returns `200` and an array
- The response array does not contain `post_id`
- The delete request returns `201`

## Test case GBI-11: Get booking IDs with a nonexistent first name

**Endpoint:**
- `GET /booking?firstname=NonExistent_GBI-11`

**Preconditions:**
- No booking has first name `NonExistent_GBI-11`

**Steps:**
1. Send the request

**Expected result:**
- Status code is `200`
- Response body is an empty array

## Test case GBI-12: Get booking IDs with a nonexistent first name and last name combination

**Endpoint:**
- `GET /booking?firstname=NonExistent_GBI-11_first&lastname=NonExistent_GBI-11_last`

**Preconditions:**
- No booking has this first name and last name combination

**Steps:**
1. Send the request.

**Expected result:**
- Status code is `200`
- Response body is an empty array

## Test case GBI-13: Get booking IDs with invalid check-in date value

**Endpoint:**
- `GET /booking?checkin=2020-25-10`

**Steps:**
1. Send the request.

**Expected result:**
- Status code is `500`
- Response body equals `Internal Server Error`

## Test case GBI-14: Get booking IDs with invalid check-in date format

**Endpoint:**
- `GET /booking?checkin=15.10.2026`

**Steps:**
1. Send the request

**Expected result:**
- Status code is `500`
- Response body equals `Internal Server Error`

## Test case GBI-15: Get booking IDs with invalid check-out date value

**Endpoint:**
- `GET /booking?checkout=2020-25-10`

**Steps:**
1. Send the request

**Expected result:**
- Status code is `500`
- Response body equals `Internal Server Error`

## Test case GBI-16: Get booking IDs with invalid check-out date format

**Endpoint:**
- `GET /booking?checkout=15.10.2026`

**Steps:**
1. Send the request.

**Expected result:**
- Status code is `500`
- Response body equals `Internal Server Error`
