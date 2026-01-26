# SQL to JSON Mapping Documentation

## Overview
This document explains how relational database entities from the MoMo SMS Analyzer database are serialized into JSON format for API responses. The mapping demonstrates how foreign key relationships and junction tables are transformed into nested JSON structures.

---

## Mapping Principles

### 1. **Direct Field Mapping**
Most database columns map directly to JSON properties with the same name. Data types are converted as follows:
- `INT` → `integer`
- `VARCHAR/TEXT` → `string`
- `DECIMAL` → `number` (with appropriate precision)
- `DATETIME` → `string` (ISO 8601 format: `YYYY-MM-DDTHH:mm:ssZ`)
- `BOOLEAN` → `boolean`

### 2. **Foreign Key Relationships → Nested Objects**
Foreign keys are resolved by joining related tables and embedding the related entity as a nested JSON object.

### 3. **Many-to-Many Relationships → Arrays**
Junction tables (like `transaction_tags`) are serialized as arrays of related objects.

### 4. **Optional Fields**
Nullable database columns become optional JSON properties (may be `null` or omitted).

---

## Entity Mappings

### Users Table → JSON

**SQL Table Structure:**
```sql
users (
    user_id INT PRIMARY KEY,
    full_name VARCHAR(100),
    phone_number VARCHAR(20),
    created_at DATETIME
)
```

**JSON Representation:**
```json
{
  "user_id": 1,
  "full_name": "Alice Johnson",
  "phone_number": "0788110381",
  "created_at": "2026-01-20T10:15:00Z"
}
```

**Mapping Notes:**
- Direct 1:1 mapping
- `DATETIME` converted to ISO 8601 string format
- All fields are required (NOT NULL constraints)

---

### Transaction Categories Table → JSON

**SQL Table Structure:**
```sql
transaction_categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(50),
    description TEXT,
    is_active BOOLEAN,
    created_at DATETIME
)
```

**JSON Representation:**
```json
{
  "category_id": 1,
  "category_name": "Send Money",
  "description": "Peer to peer money transfer",
  "is_active": true,
  "created_at": "2026-01-20T10:00:00Z"
}
```

**Mapping Notes:**
- Direct field mapping
- `BOOLEAN` maps to JSON boolean
- `TEXT` maps to JSON string

---

### Tags Table → JSON

**SQL Table Structure:**
```sql
tags (
    tag_id INT PRIMARY KEY,
    tag_name VARCHAR(50)
)
```

**JSON Representation:**
```json
{
  "tag_id": 1,
  "tag_name": "High_value"
}
```

**Mapping Notes:**
- Simple direct mapping
- Used as nested objects within transactions

---

### System Logs Table → JSON

**SQL Table Structure:**
```sql
system_logs (
    log_id INT PRIMARY KEY,
    event_type VARCHAR(50),
    message TEXT,
    event_time DATETIME,
    source VARCHAR(100),
    related_entity VARCHAR(50)
)
```

**JSON Representation:**
```json
{
  "log_id": 1,
  "event_type": "INFO",
  "message": "Transaction TXN1001 inserted successfully",
  "event_time": "2026-01-21T09:30:00Z",
  "source": "ETL Parser",
  "related_entity": "TXN1001"
}
```

**Mapping Notes:**
- Direct mapping
- `related_entity` can be `null` if not applicable

---

### Transactions Table → JSON (Simple)

**SQL Table Structure:**
```sql
transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    sender_id INT FOREIGN KEY → users(user_id),
    receiver_id INT FOREIGN KEY → users(user_id),
    category_id INT FOREIGN KEY → transaction_categories(category_id),
    amount DECIMAL(12,2),
    fee DECIMAL(12,2),
    currency VARCHAR(10),
    status VARCHAR(30),
    transaction_date DATETIME,
    ...
)
```

**Simple JSON (without joins):**
```json
{
  "transaction_id": "TXN1001",
  "amount": 5000.00,
  "currency": "RWF",
  "status": "completed",
  "transaction_date": "2026-01-21T10:00:00Z"
}
```

**Mapping Notes:**
- Foreign key IDs (`sender_id`, `receiver_id`, `category_id`) are not included in simple representation
- `DECIMAL` values maintain precision as JSON numbers

---

### Transactions Table → JSON (Complex with Nested Relations)

**Complex JSON (with all related data):**

```json
{
  "transaction_id": "TXN1001",
  "transaction_date": "2026-01-21T10:00:00Z",
  "amount": 5000.00,
  "fee": 100.00,
  "currency": "RWF",
  "status": "completed",
  "transaction_channel": "SMS",
  
  "sender": {
    "user_id": 1,
    "full_name": "Alice Johnson",
    "phone_number": "0788110381"
  },
  
  "receiver": {
    "user_id": 2,
    "full_name": "Jean Pierre",
    "phone_number": "0783945743"
  },
  
  "category": {
    "category_id": 1,
    "category_name": "Send Money",
    "description": "Peer to peer money transfer"
  },
  
  "tags": [
    { "tag_id": 1, "tag_name": "High_value" },
    { "tag_id": 4, "tag_name": "Personal" }
  ],
  
  "system_logs": [
    {
      "log_id": 1,
      "event_type": "INFO",
      "message": "Transaction TXN1001 inserted successfully",
      "source": "ETL Parser"
    }
  ]
}
```

**SQL Query Equivalent:**
```sql
SELECT 
    t.*,
    s.user_id as sender_id, s.full_name as sender_name, s.phone_number as sender_phone,
    r.user_id as receiver_id, r.full_name as receiver_name, r.phone_number as receiver_phone,
    c.category_id, c.category_name, c.description
FROM transactions t
JOIN users s ON t.sender_id = s.user_id
JOIN users r ON t.receiver_id = r.user_id
JOIN transaction_categories c ON t.category_id = c.category_id
LEFT JOIN transaction_tags tt ON t.transaction_id = tt.transaction_id
LEFT JOIN tags tg ON tt.tag_id = tg.tag_id
LEFT JOIN system_logs sl ON sl.related_entity = t.transaction_id
WHERE t.transaction_id = 'TXN1001'
```

**Mapping Notes:**
- **Foreign Key Resolution:**
  - `sender_id` → JOIN with `users` → nested `sender` object
  - `receiver_id` → JOIN with `users` → nested `receiver` object
  - `category_id` → JOIN with `transaction_categories` → nested `category` object

- **Many-to-Many Resolution:**
  - `transaction_tags` junction table → JOIN with `tags` → `tags` array
  - Multiple tags per transaction become array elements

- **One-to-Many Resolution:**
  - `system_logs.related_entity` → Filter logs by `transaction_id` → `system_logs` array
  - Multiple logs per transaction become array elements

---

## Complete Mapping Table

| SQL Table | SQL Field | JSON Field | JSON Type | Relationship Type | Notes |
|-----------|-----------|------------|-----------|-------------------|-------|
| `users` | `user_id` | `user_id` | integer | Primary Key | Direct mapping |
| `users` | `full_name` | `full_name` | string | - | Direct mapping |
| `users` | `phone_number` | `phone_number` | string | - | Direct mapping |
| `users` | `created_at` | `created_at` | string (ISO 8601) | - | DATETIME conversion |
| `transaction_categories` | `category_id` | `category_id` | integer | Primary Key | Direct mapping |
| `transaction_categories` | `category_name` | `category_name` | string | - | Direct mapping |
| `transaction_categories` | `description` | `description` | string | - | Direct mapping |
| `transaction_categories` | `is_active` | `is_active` | boolean | - | Direct mapping |
| `tags` | `tag_id` | `tag_id` | integer | Primary Key | Direct mapping |
| `tags` | `tag_name` | `tag_name` | string | - | Direct mapping |
| `transactions` | `transaction_id` | `transaction_id` | string | Primary Key | Direct mapping |
| `transactions` | `sender_id` | `sender` | object | Foreign Key → `users` | JOIN → nested object |
| `transactions` | `receiver_id` | `receiver` | object | Foreign Key → `users` | JOIN → nested object |
| `transactions` | `category_id` | `category` | object | Foreign Key → `transaction_categories` | JOIN → nested object |
| `transactions` | `amount` | `amount` | number | - | DECIMAL conversion |
| `transactions` | `fee` | `fee` | number | - | DECIMAL conversion |
| `transactions` | `currency` | `currency` | string | - | Direct mapping |
| `transactions` | `status` | `status` | string | - | Direct mapping |
| `transactions` | `transaction_date` | `transaction_date` | string (ISO 8601) | - | DATETIME conversion |
| `transaction_tags` | `transaction_id` + `tag_id` | `tags` | array | Junction Table | JOIN → array of objects |
| `system_logs` | `related_entity` | `system_logs` | array | One-to-Many | Filter → array of objects |

---

## Serialization Patterns

### Pattern 1: Simple Entity (No Relations)
```json
{
  "entity_id": 1,
  "field1": "value1",
  "field2": "value2"
}
```
**Use Case:** List endpoints, minimal data requirements

### Pattern 2: Entity with Single Relations
```json
{
  "entity_id": 1,
  "field1": "value1",
  "related_entity": {
    "id": 2,
    "name": "Related Name"
  }
}
```
**Use Case:** Detail endpoints with one level of nesting

### Pattern 3: Entity with Multiple Relations (Complex)
```json
{
  "entity_id": 1,
  "field1": "value1",
  "related_entity_1": { ... },
  "related_entity_2": { ... },
  "related_entities_array": [ ... ]
}
```
**Use Case:** Full detail endpoints, comprehensive data retrieval

---

## API Response Examples

### Example 1: Get Transaction by ID
**Endpoint:** `GET /api/transactions/TXN1001`

**SQL Query:**
```sql
SELECT t.*, s.*, r.*, c.*
FROM transactions t
JOIN users s ON t.sender_id = s.user_id
JOIN users r ON t.receiver_id = r.user_id
JOIN transaction_categories c ON t.category_id = c.category_id
WHERE t.transaction_id = 'TXN1001'
```

**JSON Response:**
```json
{
  "success": true,
  "data": {
    "transaction_id": "TXN1001",
    "amount": 5000.00,
    "sender": { "user_id": 1, "full_name": "Alice Johnson" },
    "receiver": { "user_id": 2, "full_name": "Jean Pierre" },
    "category": { "category_id": 1, "category_name": "Send Money" }
  }
}
```

### Example 2: Get User Transactions
**Endpoint:** `GET /api/users/1/transactions`

**SQL Query:**
```sql
SELECT t.*, c.category_name
FROM transactions t
JOIN transaction_categories c ON t.category_id = c.category_id
WHERE t.sender_id = 1 OR t.receiver_id = 1
```

**JSON Response:**
```json
{
  "success": true,
  "user": { "user_id": 1, "full_name": "Alice Johnson" },
  "transactions": [
    {
      "transaction_id": "TXN1001",
      "amount": 5000.00,
      "category": { "category_name": "Send Money" }
    }
  ]
}
```

---

## Best Practices

1. **Consistent Date Formatting:** Always use ISO 8601 format (`YYYY-MM-DDTHH:mm:ssZ`)
2. **Nested Objects:** Keep nested objects lightweight - only include essential fields
3. **Arrays for M:N:** Always serialize many-to-many relationships as arrays
4. **Null Handling:** Omit `null` values or use explicit `null` based on API design
5. **Performance:** Use simple JSON for list endpoints, complex JSON for detail endpoints
6. **Versioning:** Include API version in response structure for future compatibility

---

## Conclusion

This mapping demonstrates how relational database structures are transformed into hierarchical JSON structures suitable for RESTful API responses. The key principle is resolving foreign keys through JOINs and embedding related entities as nested objects or arrays, creating a more intuitive and efficient data structure for frontend consumption.
