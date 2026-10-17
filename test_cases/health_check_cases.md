# Test Cases: Health Check API

## Scope

This document covers test cases for the health check API

## Base URL

`https://restful-booker.herokuapp.com`

## Endpoints Covered

- `GET /ping`

# GET /ping test cases

## Test Case H-1: Check ping response

**Endpoint:** `GET /ping`

**Preconditions:**
- None

**Steps:**
1. Send a `GET` request to `/ping`
2. Check the response status code
3. Check the response body content

**Expected Results:**
- Status code is 201
- Response body is `Created`