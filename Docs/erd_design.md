## EDR Design Decisions and Rationale of ERD creation to be used in MoMo SMS Analyser.

### 1. Introduction
This paper gives the design options and rationale of the Entity Relationship Diagram (ERD) created in MoMo SMS Analyzer system. The database design aims at achieving the following;
support the loading, transformation and extraction (ETL) of Mobile Money (MoMo) SMS data into a formatted relational database. 
The system facilitates dependable storage, categorization and analysis of information of transaction while maintaining the integrity, scalability and maintainability of data.

**ERD_Diagram** link:(https://drive.google.com/file/d/1aKMfamhQR59Cia8msxjYVvw6bNi0KIz6/view?usp=sharing) 

### 2. Overview of Entities
The following are the main entities in the ERD:
Users
Transactions
TransactionCategories
Tags
Transaction_Tags (junction table)
System_Logs
These organisations are actual players and processes in the Mobile Money operations and
ETL workflows.

### 3. Entity and Attribute Justification.

#### 3.1 Users Entity
Purpose: Stores people who engage in transactions either as senders or receivers.
Attributes will consist of user_id (primary key), full_name, phone_number (unique) and created_at timestamp.
Design Justification: One Users entity will not have redundancy, nor will it be normalized. Phone numbers are limited to validity, and indexed so that they can be quickly looked up.

#### 3.2 TransactionCategories Entity.
Purpose: Categorizes the transactions in terms of deposits, withdrawals and transfers.
Attributes are category_id, category_name, description, is_active and created_at.
Design Justification: Separating categories and transactions helps in the normalization and allows easy future expansion.

#### 3.3 Transactions Entity
Purpose: This is the main storage of all records that are stored on SMS transactions.
Attributes can be transaction_id, sender_id, receiver_id, category_id, amount, fee, currency, transaction_date, raw_sms, status, and audit fields.
Design Justification: Foreign keys are guaranteed to provide referential integrity. Financial values are approved by constraints and analytics queries are supported by indexes.

#### 3.4 Tags Entity
Purpose: Allows the transactions to be flexibly labeled to use in analytical processing.
There are tag_id, tag_name attributes.
Design Justification: Tagging enables the classification to be done without modifying the transaction schema, and benefits.
Extensibility.

#### 3.5 TransactionTags Entity
Purpose: Solves the many to many relationship between transactions and tags.
These attributes are transaction_id and tag_id.
Design Justification: Helps to avoid duplication and has normalization.

#### 3.6 SystemLogs Entity
Purpose: Audits and debugs the events of Stores system and ETL processes.
The attributes are log_id, event_type, message, event_time, source and related_entity.
Design Justification: This separates business transaction information and operational logging-out.

### 4. Relationships Summary
Users to Traffic (seller and buyer): One-to-many.
TransactionCategories to Transactions: One-to-many.
Many-to-many Relations: Transactions to Tags.
Users or Transactions are optional whose reference is made in System_Logs.

### 5. Normalization and Integrity.
The design is in compliance with First, Second, and Third Normal Form (1NF, 2NF, and 3NF). Data integrity is implemented by primary keys, foreign keys, unique constraints, and check constraints.

### 6. Scalability and Extensions in the future.
The ERD helps in the further development such as fraud detection, machine learning analysis, single currency operations, and third party API connections.

### 7. Conclusion
This is an ERD design that offers a strong, normalized and scalable database foundation of data storage and analysis.
Data on Mobile Money SMS transaction. The structure provides uniformity, adaptability, and appropriateness to superior analytics and reporting.
