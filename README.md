# SMS_MoMo
## Enterprise-level fullstack app SMS_MoMo
### Project Description:
This project is an enterprise full-stack application that processes MOMO SMS Transaction data(XML format), cleans and categorizes the data, stores it in a relational database(SQLite), and presents analytics through a web dashboard.


## Team Members
- Jonathan ISHIMWE
- Olivier Collins ITANGISHAKA
- Andrew Thon Riem Alier

## High-Level System Architecture
> The system is composed of the following major components:
  - Data source
  - ETL Pipeline: Parses, clean, normalizes, categorizes and loads data
  - Databases: SQLite relational database
  - Analytics layer: Aggregated JSON for frontend consumption
  - Frontend Dashboard: Static HTML/CSS/JS (charts & tables)

> **Architecture Diagram:**
(https://drive.google.com/file/d/1EjnItnHn04vEQYKvoszLRVkfsoYBMbjV/view?usp=sharing)

## Project Structure

```
SMS_MoMo/
│
├── api/
│   └── server.py
│
├── database/
│   ├── database_setup.sql
│   └── crud_operations.sql
│
├── Docs/
│   ├── BSE Team Task Sheet_[EWD_Database Design and Implementation_Cohort 4_Team].xlsx
│   ├── erd_design.md
│   └── erd_diagram.jpeg
│
├── dsa/
│   ├── search_algorithms.py
│   ├── xml_parser.py
│   └── transactions.json
│
├── examples/
│   ├── README.md
│   ├── json_schemas.json
│   └── sql_to_json_mapping.md
│
├── index.html
├── modified_sms_v2.xml
├── README.md
└── requirements.txt
```

## Prerequisites

- Python 3.10+

## How To Launch The App

Run the following from the project root (`SMS_MoMo/`):

1. Generate `transactions.json` from XML (optional if `dsa/transactions.json` already exists):

```bash
python dsa/xml_parser.py
```

2. Start the API server:

```bash
python api/server.py
```

3. Access the API at:

- `http://localhost:8000/transactions`

Use Basic Authentication:

- Username: `admin`
- Password: `password123`

## Quick API Endpoints

- `GET /transactions` - list all transactions
- `GET /transactions/{id}` - get one transaction
- `POST /transactions` - create transaction
- `PUT /transactions/{id}` - update transaction
- `DELETE /transactions/{id}` - delete transaction
