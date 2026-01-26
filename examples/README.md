# JSON Data Modeling Examples

This directory contains JSON schemas and examples for the MoMo SMS Analyzer database entities.

## Files

- **`json_schemas.json`** - Complete JSON schemas and examples for all database entities
  - Individual entity schemas (users, categories, tags, logs)
  - Simple transaction examples
  - Complex nested transaction examples with all related data
  - API response examples

- **`sql_to_json_mapping.md`** - Comprehensive documentation explaining:
  - How SQL tables map to JSON structures
  - Foreign key relationships → nested objects
  - Many-to-many relationships → arrays
  - Data type conversions
  - API serialization patterns

## Usage

These examples demonstrate:
1. How relational database entities are serialized to JSON
2. Proper nesting of related data (users, categories, tags)
3. API response structures for different endpoints
4. Data type handling (dates, decimals, booleans)

## Key Features

- ✅ All main entities represented (users, categories, tags, logs, transactions)
- ✅ Proper nesting for related data
- ✅ Complex transaction JSON with all related entities
- ✅ API response examples
- ✅ Complete SQL to JSON mapping documentation
