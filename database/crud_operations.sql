USE momo_sms_analyzer;



-- Insert Users
INSERT INTO users (full_name, phone_number) VALUES
('Alice Johnson', '0788110381'),
('Jean Pierre', '0783945743'),
('Olivier Mugisha', '0795798420'),
('Daniel Kalisa', '0788628841'),
('Kendra Brown', '0784637123');

-- Insert Transaction Categories
INSERT INTO transaction_categories (category_name, description) VALUES
('Send Money', 'Peer to peer money transfer'),
('Withdraw', 'Cash withdrawal'),
('Deposit', 'Incoming funds'),
('Airtime', 'Airtime purchase'),
('Merchant Payment', 'Payment to merchant');

-- Insert Tags
INSERT INTO tags (tag_name) VALUES
('High_value'),
('Low_value'),
('Suspicious'),
('Personal'),
('Business');

-- Insert Transactions
INSERT INTO transactions (
    transaction_id, sender_id, receiver_id, category_id,
    financial_transaction_id, external_transaction_id, token_number,
    message_from_sender, message_to_receiver, service_center_number,
    sms_received_at, transaction_channel, currency,
    amount, fee, balance_after, transaction_date, raw_sms, status
) VALUES
('TXN1001', 1, 2, 1, 'FIN001', 'EXT001', 'TK001',
 'You sent 5000 RWF to Jean Pierre', 'You received 5000 RWF from Alice',
 '2020', NOW(), 'SMS', 'RWF', 5000, 100, 15000, NOW(), 'Sample raw SMS 1', 'completed'),

('TXN1002', 2, 3, 4, 'FIN002', 'EXT002', 'TK002',
 'Airtime purchase 2000 RWF', 'Airtime received',
 '2020', NOW(), 'APP', 'RWF', 2000, 50, 13000, NOW(), 'Sample raw SMS 2', 'completed'),

('TXN1003', 3, 1, 3, 'FIN003', 'EXT003', 'TK003',
 'Deposit 10000 RWF', 'Deposit confirmed',
 '2020', NOW(), 'USSD', 'RWF', 10000, 0, 20000, NOW(), 'Sample raw SMS 3', 'completed'),

('TXN1004', 4, 5, 5, 'FIN004', 'EXT004', 'TK004',
 'Paid merchant 3000 RWF', 'Payment received',
 '2020', NOW(), 'APP', 'RWF', 3000, 50, 9000, NOW(), 'Sample raw SMS 4', 'pending'),

('TXN1005', 5, 1, 2, 'FIN005', 'EXT005', 'TK005',
 'Withdraw 4000 RWF', 'Withdrawal confirmed',
 '2020', NOW(), 'ATM', 'RWF', 4000, 100, 8000, NOW(), 'Sample raw SMS 5', 'completed');

-- Insert Transaction Tags
INSERT INTO transaction_tags (transaction_id, tag_id) VALUES
('TXN1001', 1),
('TXN1002', 2),
('TXN1003', 4),
('TXN1004', 5),
('TXN1005', 3);

-- Insert System Logs
INSERT INTO system_logs (event_type, message, source, related_entity) VALUES
('INFO', 'Transaction TXN1001 inserted', 'ETL Parser', 'TXN1001'),
('INFO', 'Transaction TXN1002 inserted', 'ETL Parser', 'TXN1002'),
('WARNING', 'Pending transaction detected', 'Validator', 'TXN1004'),
('INFO', 'User record created', 'User Module', '1'),
('ERROR', 'Invalid SMS format skipped', 'Parser', 'N/A');


-- View all users
SELECT * FROM users;

-- View all transaction categories
SELECT * FROM transaction_categories;

-- View all transactions
SELECT * FROM transactions;

-- View all tags
SELECT * FROM tags;

-- View all system logs
SELECT * FROM system_logs;

-- Recent transactions
SELECT *
FROM transactions
ORDER BY transaction_date DESC
LIMIT 5;


-- Join query (test relationships)
SELECT
    t.transaction_id,
    s.full_name AS sender,
    r.full_name AS receiver,
    c.category_name,
    t.amount,
    t.status
FROM transactions t
JOIN users s ON t.sender_id = s.user_id
JOIN users r ON t.receiver_id = r.user_id
JOIN transaction_categories c ON t.category_id = c.category_id;


-- Update transaction status
UPDATE transactions
SET status = 'received'
WHERE transaction_id = 'TXN1004';


-- Delete a tag
DELETE FROM tags
WHERE tag_name = 'Suspicious';


-- VERIFY AFTER UPDATE & DELETE
SELECT transaction_id, status FROM transactions;

SELECT * FROM tags;