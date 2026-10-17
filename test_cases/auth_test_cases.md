# Test Cases: Auth API

## Scope

This document covers test cases for the Auth API

## Base URL

`https://restful-booker.herokuapp.com`

## Endpoints covered

- `POST /auth`

# POST /auth test cases

## Test case A-1: Create token with valid credentials
**Endpoint:** `POST /auth`

**Preconditions:**
- Auth API is available
- Valid credentials are known

**Headers:**
Content-Type: `application/json`
**Body:**
```
{
  "username": "admin",
  "password": "password123"
}
```

**Steps:**
1. Send a `POST` request to `/auth`
2. Check the response status code
3. Check the response body structure

**Expected Result:**
- Status code is `200`
- Response body contains `token` field
- `token` field contains a string
- `token` field is a non-empty string
- Response body does not contain the `reason` field

## Test case A-2: Create token with invalid username
**Endpoint:** `POST /auth`

**Preconditions:**
- Auth API is available

**Headers:**
Content-Type: `application/json`
**Body:**
```
{
  "username": "notadmin",
  "password": "password123"
}
```

**Steps:**
1. Send a `POST` request to `/auth`
2. Check the response status code
3. Check the response body structure

**Expected Result:**
- Status code is `200`
- Response body contains the `reason` field
- `reason` field has the value `Bad credentials`
- Response body does not contain the `token` field

## Test case A-3: Create token with invalid password
**Endpoint:** `POST /auth`

**Preconditions:**
- Auth API is available

**Headers:**
Content-Type: `application/json`
**Body:**
```
{
  "username": "admin",
  "password": "password12333"
}
```

**Steps:**
1. Send a `POST` request to `/auth`
2. Check the response status code
3. Check the response body structure

**Expected Result:**
- Status code is `200`
- Response body contains the `reason` field
- `reason` field has the value `Bad credentials`
- Response body does not contain the `token` field

## Test case A-4: Create token with both invalid credentials
**Endpoint:** `POST /auth`

**Preconditions:**
- Auth API is available

**Headers:**
Content-Type: `application/json`
**Body:**
```
{
  "username": "administrator",
  "password": "password123456"
}
```

**Steps:**
1. Send a `POST` request to `/auth`
2. Check the response status code
3. Check the response body structure

**Expected Result:**
- Status code is `200`
- Response body contains the `reason` field
- `reason` field has the value `Bad credentials`
- Response body does not contain the `token` field

## Test case A-5: Create token without username
**Endpoint:** `POST /auth`

**Preconditions:**
- Auth API is available

**Headers:**
Content-Type: `application/json`
**Body:**
```
{
  "password": "password123"
}
```

**Steps:**
1. Send a `POST` request to `/auth`
2. Check the response status code
3. Check the response body structure

**Expected Result:**
- Status code is `200`
- Response body contains the `reason` field
- `reason` field has the value `Bad credentials`
- Response body does not contain the `token` field

## Test case A-6: Create token without password
**Endpoint:** `POST /auth`

**Preconditions:**
- Auth API is available

**Headers:**
Content-Type: `application/json`
**Body:**
```
{
  "username": "admin"
}
```

**Steps:**
1. Send a `POST` request to `/auth`
2. Check the response status code
3. Check the response body structure

**Expected Result:**
- Status code is `200`
- Response body contains the `reason` field
- `reason` field has the value `Bad credentials`
- Response body does not contain the `token` field

## Test case A-7: Create token with an empty JSON object
**Endpoint:** `POST /auth`

**Preconditions:**
- Auth API is available

**Headers:**
Content-Type: `application/json`
**Body:**
```
{}
```

**Steps:**
1. Send a `POST` request to `/auth`
2. Check the response status code
3. Check the response body structure

**Expected Result:**
- Status code is `200`
- Response body contains the `reason` field
- `reason` field has the value `Bad credentials`
- Response body does not contain the `token` field

## Test case A-8: Create token with unsupported Content-Type
**Endpoint:** `POST /auth`

**Preconditions:**
- Auth API is available

**Headers:**
Content-Type: `application/xml`
**Body:**
```
{
  "username": "admin",
  "password": "password123"
}
```

**Steps:**
1. Send a `POST` request to `/auth`
2. Check the response status code
3. Check the response body content

**Expected Result:**
- Status code is `400`
- Response body is `Bad Request`
- Response body does not contain the `token` field


## Test case A-9: Create token with SQL injection attempt in username
**Endpoint:** `POST /auth`

**Preconditions:**
- Auth API is available

**Headers:**
Content-Type: `application/json`
**Body:**
```
{
  "username": "' OR '1' = '1' --",
  "password": "password123"
}
```

**Steps:**
1. Send a `POST` request to `/auth`
2. Check the response status code
3. Check the response body structure

**Expected Result:**
- Status code is `200`
- Response body contains the `reason` field
- `reason` field has the value `Bad credentials`
- Response body does not contain the `token` field
