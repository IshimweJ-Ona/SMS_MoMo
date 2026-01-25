CREATE DATABASE IF NOT EXISTS momo_sms_analyzer;

USE momo_sms_anaylzer;

-- USERS Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_phone_length CHECK (CHAR_LENGTH(phone_number) BETWEEN 10 AND 15)
);

CREATE INDEX idx_users_phone ON users(phone_number);


-- TRANSACTION CATEGORIES
CREATE TABLE IF NOT EXISTS transaction_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- TRANSACTIONS
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    category_id INT NOT NULL,

    financial_transaction_id VARCHAR(50),
    external_transaction_id VARCHAR(100),
    token_number VARCHAR(100),
    message_from_sender TEXT,
    message_to_receiver TEXT,
    service_center_number VARCHAR(20),
    sms_received_at DATETIME,
    transaction_channel VARCHAR(50),
    currency VARCHAR(10) DEFAULT 'RWF',

    amount DECIMAL(12,2) NOT NULL,
    fee DECIMAL(12,2) DEFAULT 0,
    balance_after DECIMAL(12,2) NOT NULL,
    transaction_date DATETIME NOT NULL,
    raw_sms TEXT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'completed',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_transaction_sender FOREIGN KEY (sender_id) REFERENCES users(user_id) ON DELETE RESTRICT,
    CONSTRAINT fk_transaction_receiver FOREIGN KEY (receiver_id) REFERENCES users(user_id) ON DELETE RESTRICT,
    CONSTRAINT fk_transaction_category FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id) ON DELETE RESTRICT,

    CONSTRAINT chk_amount_positive CHECK (amount > 0),
    CONSTRAINT chk_fee_non_negative CHECK (fee >= 0),
    CONSTRAINT chk_transaction_status CHECK (status IN ('pending', 'completed', 'failed', 'received'))
);

CREATE INDEX idx_transaction_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_sender ON transactions(sender_id);
CREATE INDEX idx_transactions_receiver ON transactions(receiver_id);
CREATE INDEX idx_transactions_category ON transactions(category_id);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_amount ON transactions(amount);
CREATE INDEX idx_transactions_channel ON transactions(transaction_channel);


-- TAGS
CREATE TABLE IF NOT EXISTS tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    tag_name VARCHAR(50) NOT NULL UNIQUE COMMENT 'ex High_value'
);


-- TRANSACTION_TAGS (junction table)
CREATE TABLE IF NOT EXISTS transaction_tags (
    transaction_id VARCHAR(50) NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (transaction_id, tag_id),
    CONSTRAINT fk_tt_transaction FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) ON DELETE CASCADE,
    CONSTRAINT fk_tt_tag FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
);


-- SYSTEM LOGS
CREATE TABLE IF NOT EXISTS system_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL COMMENT 'INFO, WARNING, ERROR',
    message TEXT NOT NULL,
    event_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(100) COMMENT 'ETL module or System component',
    related_entity VARCHAR(50) COMMENT 'ID of related entity (transaction_id, user_id)'
);

CREATE INDEX idx_logs_event_time ON system_logs(event_time);
CREATE INDEX idx_logs_event_type ON system_logs(event_type);