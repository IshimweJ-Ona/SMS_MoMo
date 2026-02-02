MoMo SMS Transaction API Documentation
Author: Andrew Thon Riem Alier
Date: February 2, 2026
Assignment: Building and Securing a REST API
Task: API Documentation

Table of Contents

Overview
Base Configuration
Authentication
API Endpoints
Error Codes
Testing Guide


Overview
The MoMo SMS Transaction API provides programmatic access to mobile money SMS transaction records. This RESTful API supports full CRUD (Create, Read, Update, Delete) operations and requires Basic Authentication for all endpoints.
Key Features

RESTful design following HTTP standards
JSON request/response format
Basic Authentication security
Comprehensive error handling
Transaction data from parsed XML SMS records


Base Configuration
PropertyValueBase URLhttp://localhost:8000Content Typeapplication/jsonAuthenticationBasic Authentication (HTTP Header)ProtocolHTTP (HTTPS recommended for production)

Authentication
All API endpoints require Basic Authentication. Credentials must be included in the Authorization header.
Format
Authorization: Basic <base64-encoded-credentials>
Valid Credentials
Username: admin
Password: password123

Username: user
Password: user123

Username: test
Password: test123
Example Authentication Header
bash# Using curl with -u flag (automatically encodes credentials)
curl -u admin:password123 http://localhost:8000/transactions

# Manual base64 encoding
# "admin:password123" → base64 → "YWRtaW46cGFzc3dvcmQxMjM="
curl -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" http://localhost:8000/transactions

API Endpoints
## 1. GET /transactions
Retrieve all transaction records from the system.
Endpoint
GET /transactions
HTTP Method
GET
Authentication
Required - Valid Basic Auth credentials must be provided
Request Headers
Authorization: Basic <credentials>
Request Example (curl)
bashcurl -X GET http://localhost:8000/transactions \
  -u admin:password123 \
  -H "Accept: application/json"
Request Example (Postman)
Method: GET
URL: http://localhost:8000/transactions
Authorization: 
  Type: Basic Auth
  Username: admin
  Password: password123
Success Response (200 OK)
json{
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
Error Codes
CodeDescriptionResponse401Unauthorized - Invalid or missing credentials{"error": "Unauthorized - Valid credentials required", "status_code": 401}

## 2. GET /transactions/{id}
Retrieve a specific transaction by its unique ID.
Endpoint
GET /transactions/{id}
HTTP Method
GET
Authentication
Required - Valid Basic Auth credentials must be provided
URL Parameters
ParameterTypeRequiredDescriptionidintegerYesUnique transaction identifier
Request Headers
Authorization: Basic <credentials>
Request Example (curl)
bash# Get transaction with ID 5
curl -X GET http://localhost:8000/transactions/5 \
  -u admin:password123 \
  -H "Accept: application/json"
Request Example (Postman)
Method: GET
URL: http://localhost:8000/transactions/5
Authorization: 
  Type: Basic Auth
  Username: admin
  Password: password123
Success Response (200 OK)
json{
  "data": {
    "id": 5,
    "address": "+250788121314",
    "type": "bank deposit",
    "amount": "15000",
    "date": "Jan 15, 2025 2:30:00 PM",
    "raw_message": "Bank deposit of 15,000 RWF successful. Your new balance is 17,500 RWF."
  }
}
Error Codes
CodeDescriptionResponse400Bad Request - Invalid ID format{"error": "Invalid transaction ID format", "status_code": 400}401Unauthorized - Invalid or missing credentials{"error": "Unauthorized - Valid credentials required", "status_code": 401}404Not Found - Transaction does not exist{"error": "Transaction 999 not found", "status_code": 404}

## 3. POST /transactions
Create a new transaction record in the system.
Endpoint
POST /transactions
HTTP Method
POST
Authentication
Required - Valid Basic Auth credentials must be provided
Request Headers
Authorization: Basic <credentials>
Content-Type: application/json
Request Body
All fields are required:
FieldTypeDescriptionExampleaddressstringPhone number or identifier"+250788999111"typestringTransaction type"received", "payment", "transferred", "bank deposit"amountstringTransaction amount (RWF)"25000"datestringTransaction date/time"Jan 18, 2025 10:00:00 AM"raw_messagestringOriginal SMS message"You have received 25,000 RWF..."
Request Example (curl)
bashcurl -X POST http://localhost:8000/transactions \
  -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{
    "address": "+250788999111",
    "type": "received",
    "amount": "25000",
    "date": "Jan 18, 2025 10:00:00 AM",
    "raw_message": "You have received 25,000 RWF from +250788222333. Your new balance is 50,000 RWF."
  }'
Request Example (Postman)
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
Success Response (201 Created)
json{
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
Error Codes
CodeDescriptionResponse400Bad Request - Missing required field{"error": "Missing required field: amount", "status_code": 400}400Bad Request - Invalid JSON format{"error": "Invalid JSON format", "status_code": 400}401Unauthorized - Invalid or missing credentials{"error": "Unauthorized - Valid credentials required", "status_code": 401}500Internal Server Error{"error": "Server error: <details>", "status_code": 500}

## 4. PUT /transactions/{id}
Update an existing transaction record. Supports partial updates (only specified fields will be updated).
Endpoint
PUT /transactions/{id}
HTTP Method
PUT
Authentication
Required - Valid Basic Auth credentials must be provided
URL Parameters
ParameterTypeRequiredDescriptionidintegerYesUnique transaction identifier
Request Headers
Authorization: Basic <credentials>
Content-Type: application/json
Request Body
Fields to update (all optional, include only what you want to change):
FieldTypeDescriptionaddressstringPhone number or identifiertypestringTransaction typeamountstringTransaction amount (RWF)datestringTransaction date/timeraw_messagestringOriginal SMS message
Request Example (curl)
bash# Update amount and type for transaction ID 10
curl -X PUT http://localhost:8000/transactions/10 \
  -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{
    "type": "payment",
    "amount": "600"
  }'
Request Example (Postman)
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
Success Response (200 OK)
json{
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
Error Codes
CodeDescriptionResponse400Bad Request - Invalid ID format{"error": "Invalid transaction ID format", "status_code": 400}400Bad Request - Invalid JSON format{"error": "Invalid JSON format", "status_code": 400}401Unauthorized - Invalid or missing credentials{"error": "Unauthorized - Valid credentials required", "status_code": 401}404Not Found - Transaction does not exist{"error": "Transaction 999 not found", "status_code": 404}500Internal Server Error{"error": "Server error: <details>", "status_code": 500}

## 5. DELETE /transactions/{id}
Permanently remove a transaction record from the system.
Endpoint
DELETE /transactions/{id}
HTTP Method
DELETE
Authentication
Required - Valid Basic Auth credentials must be provided
URL Parameters
ParameterTypeRequiredDescriptionidintegerYesUnique transaction identifier
Request Headers
Authorization: Basic <credentials>
Request Example (curl)
bash# Delete transaction with ID 7
curl -X DELETE http://localhost:8000/transactions/7 \
  -u admin:password123
Request Example (Postman)
Method: DELETE
URL: http://localhost:8000/transactions/7
Authorization: 
  Type: Basic Auth
  Username: admin
  Password: password123
Success Response (200 OK)
json{
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
Error Codes
CodeDescriptionResponse400Bad Request - Invalid ID format{"error": "Invalid transaction ID format", "status_code": 400}401Unauthorized - Invalid or missing credentials{"error": "Unauthorized - Valid credentials required", "status_code": 401}404Not Found - Transaction does not exist{"error": "Transaction 999 not found", "status_code": 404}500Internal Server Error{"error": "Server error: <details>", "status_code": 500}

Error Codes
The API uses standard HTTP status codes to indicate the success or failure of requests.
Success Codes
CodeNameDescription200OKRequest succeeded (GET, PUT, DELETE)201CreatedResource created successfully (POST)
Client Error Codes
CodeNameDescriptionCommon Causes400Bad RequestInvalid request format or parametersMissing fields, invalid JSON, malformed ID401UnauthorizedAuthentication failed or missingWrong credentials, missing Authorization header404Not FoundResource does not existNon-existent transaction ID
Server Error Codes
CodeNameDescriptionCommon Causes500Internal Server ErrorServer-side processing errorUnexpected exception, server malfunction
Error Response Format
All errors follow this JSON structure:
json{
  "error": "Human-readable error message",
  "status_code": 400
}
Example Error Responses
Unauthorized (401):
json{
  "error": "Unauthorized - Valid credentials required",
  "status_code": 401
}
Not Found (404):
json{
  "error": "Transaction 999 not found",
  "status_code": 404
}
Bad Request (400):
json{
  "error": "Missing required field: amount",
  "status_code": 400
}

## Testing Guide
Prerequisites

API server running on http://localhost:8000
curl installed OR Postman application
Valid authentication credentials

Quick Test Commands
bash# 1. Test successful GET (list all)
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
Postman Collection Setup

Create new collection: "MoMo API Tests"
Set collection-level authorization:

Type: Basic Auth
Username: admin
Password: password123


Add requests for each endpoint
Run collection to verify all endpoints work
