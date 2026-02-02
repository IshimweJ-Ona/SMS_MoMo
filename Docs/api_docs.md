# MoMo SMS Transaction API Documentation

> **Author:** Andrew Thon Riem Alier  
> **Date:** February 2, 2026  
> **Assignment:** Building and Securing a REST API  
> **Task:** API Documentation (Task 4)

---

##  Table of Contents

- [Overview](#overview)
- [Base Configuration](#base-configuration)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
  - [GET /transactions](#1-get-transactions)
  - [GET /transactions/{id}](#2-get-transactionsid)
  - [POST /transactions](#3-post-transactions)
  - [PUT /transactions/{id}](#4-put-transactionsid)
  - [DELETE /transactions/{id}](#5-delete-transactionsid)
- [Error Codes](#error-codes)
- [Testing Guide](#testing-guide)

---

## Overview

The **MoMo SMS Transaction API** provides programmatic access to mobile money SMS transaction records. This RESTful API supports full CRUD (Create, Read, Update, Delete) operations and requires Basic Authentication for all endpoints.

### Key Features

-  RESTful design following HTTP standards
-  JSON request/response format
-  Basic Authentication security
-  Comprehensive error handling
-  Transaction data from parsed XML SMS records

---

## Base Configuration

| Property | Value |
|----------|-------|
| **Base URL** | `http://localhost:8000` |
| **Content Type** | `application/json` |
| **Authentication** | Basic Authentication (HTTP Header) |
| **Protocol** | HTTP (HTTPS recommended for production) |

---

## Authentication

All API endpoints require **Basic Authentication**. Credentials must be included in the `Authorization` header.

### Format

```http
Authorization: Basic <base64-encoded-credentials>
```

### Valid Credentials

```
Username: admin
Password: password123

Username: user
Password: user123

Username: test
Password: test123
```

### Example Authentication Header

```bash
# Using curl with -u flag (automatically encodes credentials)
curl -u admin:password123 http://localhost:8000/transactions

# Manual base64 encoding
# "admin:password123" → base64 → "YWRtaW46cGFzc3dvcmQxMjM="
curl -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" http://localhost:8000/transactions
```

---

## API Endpoints

### 1. GET /transactions

Retrieve all transaction records from the system.

#### Endpoint

```
GET /transactions
```

#### HTTP Method

`GET`

#### Authentication

**Required** - Valid Basic Auth credentials must be provided

#### Request Headers

```http
Authorization: Basic <credentials>
```

#### Request Example (curl)

```bash
curl -X GET http://localhost:8000/transactions \
  -u admin:password123 \
  -H "Accept: application/json"
```

#### Request Example (Postman)

```
Method: GET
URL: http://localhost:8000/transactions
Authorization: 
  Type: Basic Auth
  Username: admin
  Password: password123
```

#### Success Response (200 OK)

```json
{
  "data": [
    {
      "id": 1,
      "address": "+250788123456",
      "type": "received",
      "amount": "5000",
      "date": "Jan 15, 2025 10:30:00 AM",
      "raw_message": "You have received 5,000 RWF from +250788654321. Your new balance is 15,000 RWF."
    },
    {
      "id": 2,
      "address": "+250788111222",
      "type": "payment",
      "amount": "10000",
      "date": "Jan 15, 2025 11:45:00 AM",
      "raw_message": "Payment of 10,000 RWF to EUCL successful. Your new balance is 5,000 RWF."
    },
    {
      "id": 3,
      "address": "+250788555666",
      "type": "transferred",
      "amount": "2500",
      "date": "Jan 15, 2025 12:00:00 PM",
      "raw_message": "You have transferred 2,500 RWF to +250788777888. Your new balance is 2,500 RWF."
    }
  ]
}
```

#### Error Codes

| Code | Description | Response |
|------|-------------|----------|
| 401 | Unauthorized - Invalid or missing credentials | `{"error": "Unauthorized - Valid credentials required", "status_code": 401}` |

---

### 2. GET /transactions/{id}

Retrieve a specific transaction by its unique ID.

#### Endpoint

```
GET /transactions/{id}
```

#### HTTP Method

`GET`

#### Authentication

**Required** - Valid Basic Auth credentials must be provided

#### URL Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Unique transaction identifier |

#### Request Headers

```http
Authorization: Basic <credentials>
```

#### Request Example (curl)

```bash
# Get transaction with ID 5
curl -X GET http://localhost:8000/transactions/5 \
  -u admin:password123 \
  -H "Accept: application/json"
```

#### Request Example (Postman)

```
Method: GET
URL: http://localhost:8000/transactions/5
Authorization: 
  Type: Basic Auth
  Username: admin
  Password: password123
```

#### Success Response (200 OK)

```json
{
  "data": {
    "id": 5,
    "address": "+250788121314",
    "type": "bank deposit",
    "amount": "15000",
    "date": "Jan 15, 2025 2:30:00 PM",
    "raw_message": "Bank deposit of 15,000 RWF successful. Your new balance is 17,500 RWF."
  }
}
```

#### Error Codes

| Code | Description | Response |
|------|-------------|----------|
| 400 | Bad Request - Invalid ID format | `{"error": "Invalid transaction ID format", "status_code": 400}` |
| 401 | Unauthorized - Invalid or missing credentials | `{"error": "Unauthorized - Valid credentials required", "status_code": 401}` |
| 404 | Not Found - Transaction does not exist | `{"error": "Transaction 999 not found", "status_code": 404}` |

---

### 3. POST /transactions

Create a new transaction record in the system.

#### Endpoint

```
POST /transactions
```

#### HTTP Method

`POST`

#### Authentication

**Required** - Valid Basic Auth credentials must be provided

#### Request Headers

```http
Authorization: Basic <credentials>
Content-Type: application/json
```

#### Request Body

All fields are **required**:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `address` | string | Phone number or identifier | "+250788999111" |
| `type` | string | Transaction type | "received", "payment", "transferred", "bank deposit" |
| `amount` | string | Transaction amount (RWF) | "25000" |
| `date` | string | Transaction date/time | "Jan 18, 2025 10:00:00 AM" |
| `raw_message` | string | Original SMS message | "You have received 25,000 RWF..." |

#### Request Example (curl)

```bash
curl -X POST http://localhost:8000/transactions \
  -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{
    "address": "+250788999111",
    "type": "received",
    "amount": "25000",
    "date": "Jan 18, 2025 10:00:00 AM",
    "raw_message": "You have received 25,000 RWF from +250788222333. Your new balance is 50,000 RWF."
  }'
```

#### Request Example (Postman)

```
Method: POST
URL: http://localhost:8000/transactions
Authorization: 
  Type: Basic Auth
  Username: admin
  Password: password123
Headers:
  Content-Type: application/json
Body (raw JSON):
{
  "address": "+250788999111",
  "type": "received",
  "amount": "25000",
  "date": "Jan 18, 2025 10:00:00 AM",
  "raw_message": "You have received 25,000 RWF from +250788222333. Your new balance is 50,000 RWF."
}
```

#### Success Response (201 Created)

```json
{
  "data": {
    "id": 23,
    "address": "+250788999111",
    "type": "received",
    "amount": "25000",
    "date": "Jan 18, 2025 10:00:00 AM",
    "raw_message": "You have received 25,000 RWF from +250788222333. Your new balance is 50,000 RWF."
  },
  "message": "Transaction created successfully"
}
```

#### Error Codes

| Code | Description | Response |
|------|-------------|----------|
| 400 | Bad Request - Missing required field | `{"error": "Missing required field: amount", "status_code": 400}` |
| 400 | Bad Request - Invalid JSON format | `{"error": "Invalid JSON format", "status_code": 400}` |
| 401 | Unauthorized - Invalid or missing credentials | `{"error": "Unauthorized - Valid credentials required", "status_code": 401}` |
| 500 | Internal Server Error | `{"error": "Server error: <details>", "status_code": 500}` |

---

### 4. PUT /transactions/{id}

Update an existing transaction record. Supports partial updates (only specified fields will be updated).

#### Endpoint

```
PUT /transactions/{id}
```

#### HTTP Method

`PUT`

#### Authentication

**Required** - Valid Basic Auth credentials must be provided

#### URL Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Unique transaction identifier |

#### Request Headers

```http
Authorization: Basic <credentials>
Content-Type: application/json
```

#### Request Body

Fields to update (all optional, include only what you want to change):

| Field | Type | Description |
|-------|------|-------------|
| `address` | string | Phone number or identifier |
| `type` | string | Transaction type |
| `amount` | string | Transaction amount (RWF) |
| `date` | string | Transaction date/time |
| `raw_message` | string | Original SMS message |

#### Request Example (curl)

```bash
# Update amount and type for transaction ID 10
curl -X PUT http://localhost:8000/transactions/10 \
  -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{
    "type": "payment",
    "amount": "600"
  }'
```

#### Request Example (Postman)

```
Method: PUT
URL: http://localhost:8000/transactions/10
Authorization: 
  Type: Basic Auth
  Username: admin
  Password: password123
Headers:
  Content-Type: application/json
Body (raw JSON):
{
  "type": "payment",
  "amount": "600"
}
```

#### Success Response (200 OK)

```json
{
  "data": {
    "id": 10,
    "address": "+250788394041",
    "type": "payment",
    "amount": "600",
    "date": "Jan 16, 2025 11:00:00 AM",
    "raw_message": "Payment of 500 RWF to MTN Airtime successful. Your new balance is 4,500 RWF."
  },
  "message": "Transaction updated successfully"
}
```

#### Error Codes

| Code | Description | Response |
|------|-------------|----------|
| 400 | Bad Request - Invalid ID format | `{"error": "Invalid transaction ID format", "status_code": 400}` |
| 400 | Bad Request - Invalid JSON format | `{"error": "Invalid JSON format", "status_code": 400}` |
| 401 | Unauthorized - Invalid or missing credentials | `{"error": "Unauthorized - Valid credentials required", "status_code": 401}` |
| 404 | Not Found - Transaction does not exist | `{"error": "Transaction 999 not found", "status_code": 404}` |
| 500 | Internal Server Error | `{"error": "Server error: <details>", "status_code": 500}` |

---

### 5. DELETE /transactions/{id}

Permanently remove a transaction record from the system.

#### Endpoint

```
DELETE /transactions/{id}
```

#### HTTP Method

`DELETE`

#### Authentication

**Required** - Valid Basic Auth credentials must be provided

#### URL Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Unique transaction identifier |

#### Request Headers

```http
Authorization: Basic <credentials>
```

#### Request Example (curl)

```bash
# Delete transaction with ID 7
curl -X DELETE http://localhost:8000/transactions/7 \
  -u admin:password123
```

#### Request Example (Postman)

```
Method: DELETE
URL: http://localhost:8000/transactions/7
Authorization: 
  Type: Basic Auth
  Username: admin
  Password: password123
```

#### Success Response (200 OK)

```json
{
  "data": {
    "id": 7,
    "address": "+250788212223",
    "type": "transferred",
    "amount": "3000",
    "date": "Jan 15, 2025 4:00:00 PM",
    "raw_message": "You have transferred 3,000 RWF to +250788242526. Transaction failed."
  },
  "message": "Transaction deleted successfully"
}
```

#### Error Codes

| Code | Description | Response |
|------|-------------|----------|
| 400 | Bad Request - Invalid ID format | `{"error": "Invalid transaction ID format", "status_code": 400}` |
| 401 | Unauthorized - Invalid or missing credentials | `{"error": "Unauthorized - Valid credentials required", "status_code": 401}` |
| 404 | Not Found - Transaction does not exist | `{"error": "Transaction 999 not found", "status_code": 404}` |
| 500 | Internal Server Error | `{"error": "Server error: <details>", "status_code": 500}` |

---

## Error Codes

The API uses standard HTTP status codes to indicate the success or failure of requests.

### Success Codes

| Code | Name | Description |
|------|------|-------------|
| 200 | OK | Request succeeded (GET, PUT, DELETE) |
| 201 | Created | Resource created successfully (POST) |

### Client Error Codes

| Code | Name | Description | Common Causes |
|------|------|-------------|---------------|
| 400 | Bad Request | Invalid request format or parameters | Missing fields, invalid JSON, malformed ID |
| 401 | Unauthorized | Authentication failed or missing | Wrong credentials, missing Authorization header |
| 404 | Not Found | Resource does not exist | Non-existent transaction ID |

### Server Error Codes

| Code | Name | Description | Common Causes |
|------|------|-------------|---------------|
| 500 | Internal Server Error | Server-side processing error | Unexpected exception, server malfunction |

### Error Response Format

All errors follow this JSON structure:

```json
{
  "error": "Human-readable error message",
  "status_code": 400
}
```

### Example Error Responses

**Unauthorized (401):**
```json
{
  "error": "Unauthorized - Valid credentials required",
  "status_code": 401
}
```

**Not Found (404):**
```json
{
  "error": "Transaction 999 not found",
  "status_code": 404
}
```

**Bad Request (400):**
```json
{
  "error": "Missing required field: amount",
  "status_code": 400
}
```

---

## Testing Guide

### Prerequisites

-  API server running on `http://localhost:8000`
-  curl installed OR Postman application
-  Valid authentication credentials

### Quick Test Commands

```bash
# 1. Test successful GET (list all)
curl -u admin:password123 http://localhost:8000/transactions

# 2. Test successful GET (single transaction)
curl -u admin:password123 http://localhost:8000/transactions/5

# 3. Test unauthorized access (should return 401)
curl -u wrong:credentials http://localhost:8000/transactions

# 4. Test POST (create new transaction)
curl -X POST http://localhost:8000/transactions \
  -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{
    "address": "+250788999111",
    "type": "received",
    "amount": "25000",
    "date": "Jan 18, 2025 10:00:00 AM",
    "raw_message": "You have received 25,000 RWF."
  }'

# 5. Test PUT (update transaction)
curl -X PUT http://localhost:8000/transactions/10 \
  -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{"amount": "600"}'

# 6. Test DELETE (remove transaction)
curl -X DELETE http://localhost:8000/transactions/7 \
  -u admin:password123

# 7. Test 404 error (non-existent ID)
curl -u admin:password123 http://localhost:8000/transactions/999
```

### Postman Collection Setup

1. **Create new collection:** "MoMo API Tests"
2. **Set collection-level authorization:**
   - Type: Basic Auth
   - Username: `admin`
   - Password: `password123`
3. **Add requests** for each endpoint
4. **Run collection** to verify all endpoints work

---

## Additional Notes

### Security Considerations

-  Basic Authentication transmits credentials with every request
-  Credentials are base64-encoded but **NOT encrypted**
-  **Production systems must use HTTPS** to prevent credential interception
-  Consider implementing JWT or OAuth 2.0 for enhanced security

### Best Practices

- Always include proper error handling in client applications
- Validate user input before sending requests
- Use HTTPS in production environments
- Implement rate limiting to prevent abuse
- Log all API access for security monitoring

### Data Structure

Transactions follow this schema:

```json
{
  "id": integer,
  "address": string,
  "type": string,
  "amount": string,
  "date": string,
  "raw_message": string
}
```

---

##  Support

For issues or questions:
- Check server logs for detailed error messages
- Verify authentication credentials
- Ensure proper JSON formatting in requests
- Confirm the server is running on the correct port

---

**Documentation completed by:** Andrew Thon Riem Alier  
**Last updated:** February 2, 2026  
**Version:** 1.0

---
