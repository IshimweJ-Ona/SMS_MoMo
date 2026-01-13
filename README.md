# SMS_MoMo
## Enterprise-level fullstack app SMS_MoMo
### Project Description:
This project is an enterprise full-stack application that processes MOMO SMS Transaction data(XML format), cleans and categorizes the data, stores it in a relational database(SQLite), and presents analytics through a web dashboard.


## Team Members
- Jonathan ISHIMWE

## High-Level System Architecture
> The system is composed of the following major components:
  - Data source
  - ETL Pipeline: Parses, clean, normalizes, categorizes and loads data
  - Databases: SQLite relational database
  - Analytics layer: Aggregated JSON for frontend consumption
  - Frontend Dashboard: Static HTML/CSS/JS (charts & tables)

> **Architecture Diagram:**
(https://app.diagrams.net/#G1EjnItnHn04vEQYKvoszLRVkfsoYBMbjV#%7B%22pageId%22%3A%22ssyUKd4MVkcAJwYSX6I5%22%7D)

## Project Structure
```
.
|--- README.md           
|--- .env                  
|--- requirements.txt     
|--- index.html            
|--- web/
|   |---styles.css
|   |---chart_handler.js
|   |---assets/
|--- data/
|   |---raw/
|   |   |___momo.xml
|   |---processed/
|   |   |___dashboard.json
|   |---db.sqlite3
|   |---logs/
|   |   |___etl.log
|   |   |___dead_letter/
|   |---etl/
|   |   |--- __init__.py
|   |   |--- config.py
|   |   |--- parse_xml.py
|   |   |--- clean_normalize.py
|   |   |--- categorize.py
|   |   |--- load_db.py
|   |   |--- run.py
|   |---api/
|   |   |--- __init__.py
|   |   |--- app.py
|   |   |--- db.py
|   |   |--- schemas.py
|   |---scripts/
|   |   |--- run_etl.sh
|   |   |--- export_json.sh
|   |   |--- serve_frontend.sh
|   |---tests/
|   |   |--- test_parse_xml.py
|   |   |--- test_clean_normalize.py
|   |   |--- test_categorize.py
```
