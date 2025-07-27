# GR-41 Database Alignment Approach - V2

## Overview
This document outlines the approach for leveraging existing transaction, transaction_type, and transaction_line tables to handle reinstatements, following the transaction-based architecture already established in the database.

## Current Table Analysis

### Existing Transaction Tables
- `transaction_type` - Categorizes different types of transactions
- `transaction` - Core transaction records
- `transaction_line_type` - Types of transaction line items
- `transaction_line` - Individual line items within transactions

## Approach: Using Transaction Tables for Reinstatements

### 1. Add Reinstatement Transaction Types
```sql
-- Add reinstatement as a transaction type
INSERT INTO transaction_type (code, name, description, is_default, status_id) VALUES
('REINSTATEMENT', 'Policy Reinstatement', 'Transaction for reinstating a lapsed or cancelled policy', FALSE, 1),
('REINSTATEMENT_FEE', 'Reinstatement Fee', 'Fee charged for policy reinstatement', FALSE, 1),
('REINSTATEMENT_REVERSAL', 'Reinstatement Reversal', 'Reversal of a reinstatement transaction', FALSE, 1);

-- Add corresponding line item types
INSERT INTO transaction_line_type (code, name, description, is_default, status_id) VALUES
('REINSTATEMENT_PREMIUM', 'Reinstatement Premium', 'Premium amount for reinstatement period', FALSE, 1),
('REINSTATEMENT_LAPSE_FEE', 'Lapse Fee', 'Fee for policy lapse period', FALSE, 1),
('REINSTATEMENT_PROCESSING', 'Processing Fee', 'Administrative processing fee', FALSE, 1);
```

### 2. Extend Transaction Tables for Reinstatement Details
```sql
-- Add reinstatement-specific fields to transaction table
ALTER TABLE transaction 
ADD COLUMN policy_id INT COMMENT 'Reference to policy being reinstated',
ADD COLUMN reinstatement_date DATE COMMENT 'Effective date of reinstatement',
ADD COLUMN lapse_start_date DATE COMMENT 'Date policy lapsed',
ADD COLUMN lapse_end_date DATE COMMENT 'Date lapse period ended',
ADD COLUMN reinstatement_reason VARCHAR(255) COMMENT 'Reason for reinstatement',
ADD COLUMN requires_underwriting BOOLEAN DEFAULT FALSE COMMENT 'Whether underwriting review required',
ADD CONSTRAINT fk_transaction_policy 
    FOREIGN KEY (policy_id) 
    REFERENCES policy(id) 
    ON UPDATE CASCADE;

-- Add financial details to transaction_line
ALTER TABLE transaction_line
ADD COLUMN transaction_id INT COMMENT 'Reference to parent transaction',
ADD COLUMN amount DECIMAL(10,2) COMMENT 'Line item amount',
ADD COLUMN tax_amount DECIMAL(10,2) DEFAULT 0.00 COMMENT 'Tax on line item',
ADD COLUMN description TEXT COMMENT 'Line item description',
ADD COLUMN coverage_start_date DATE COMMENT 'Coverage period start',
ADD COLUMN coverage_end_date DATE COMMENT 'Coverage period end',
ADD CONSTRAINT fk_transaction_line_transaction 
    FOREIGN KEY (transaction_id) 
    REFERENCES transaction(id) 
    ON UPDATE CASCADE;
```

### 3. Create Reinstatement Workflow Views
```sql
-- View for active reinstatements
CREATE VIEW v_active_reinstatements AS
SELECT 
    t.id as transaction_id,
    t.policy_id,
    p.policy_number,
    t.reinstatement_date,
    t.lapse_start_date,
    t.lapse_end_date,
    DATEDIFF(t.lapse_end_date, t.lapse_start_date) as lapse_days,
    t.reinstatement_reason,
    t.requires_underwriting,
    s.name as status,
    SUM(tl.amount) as total_amount,
    SUM(tl.tax_amount) as total_tax
FROM transaction t
JOIN transaction_type tt ON t.transaction_type_id = tt.id
JOIN policy p ON t.policy_id = p.id
LEFT JOIN transaction_line tl ON t.id = tl.transaction_id
LEFT JOIN status s ON t.status_id = s.id
WHERE tt.code = 'REINSTATEMENT'
GROUP BY t.id;

-- View for reinstatement history
CREATE VIEW v_reinstatement_history AS
SELECT 
    p.id as policy_id,
    p.policy_number,
    COUNT(DISTINCT t.id) as reinstatement_count,
    MAX(t.reinstatement_date) as last_reinstatement_date,
    SUM(CASE WHEN t.status_id = 1 THEN 1 ELSE 0 END) as successful_reinstatements,
    SUM(CASE WHEN t.status_id = 2 THEN 1 ELSE 0 END) as failed_reinstatements
FROM policy p
JOIN transaction t ON p.id = t.policy_id
JOIN transaction_type tt ON t.transaction_type_id = tt.id
WHERE tt.code IN ('REINSTATEMENT', 'REINSTATEMENT_REVERSAL')
GROUP BY p.id;
```

### 4. Integration with Existing Systems

#### Payment Processing Integration
```sql
-- Link reinstatement transactions to payments
CREATE TABLE IF NOT EXISTS map_transaction_payment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL,
    payment_method_id INT NOT NULL,
    payment_amount DECIMAL(10,2) NOT NULL,
    payment_date DATETIME NOT NULL,
    payment_reference VARCHAR(100),
    is_successful BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_transaction_payment (transaction_id),
    INDEX idx_payment_transaction (payment_method_id),
    CONSTRAINT fk_map_transaction_payment_transaction 
        FOREIGN KEY (transaction_id) 
        REFERENCES transaction(id),
    CONSTRAINT fk_map_transaction_payment_method 
        FOREIGN KEY (payment_method_id) 
        REFERENCES payment_method(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Links transactions to payment methods';
```

#### Status Tracking
```sql
-- Use existing status table for reinstatement workflow
-- Example status codes for reinstatements:
INSERT INTO status (code, name, description, is_default) VALUES
('REINSTATEMENT_PENDING', 'Pending Reinstatement', 'Reinstatement initiated, awaiting payment', FALSE),
('REINSTATEMENT_PAID', 'Payment Received', 'Payment received, pending processing', FALSE),
('REINSTATEMENT_REVIEW', 'Under Review', 'Reinstatement under underwriting review', FALSE),
('REINSTATEMENT_APPROVED', 'Approved', 'Reinstatement approved and active', FALSE),
('REINSTATEMENT_REJECTED', 'Rejected', 'Reinstatement rejected', FALSE);
```

## Benefits of This Approach

1. **Consistency**: Uses existing transaction framework
2. **Flexibility**: Transaction types can be extended without schema changes
3. **Audit Trail**: Built-in tracking through transaction history
4. **Financial Integration**: Leverages existing payment and fee structures
5. **Reporting**: Can use existing transaction reporting infrastructure

## Example Usage

### Creating a Reinstatement Transaction
```sql
-- Step 1: Create the main transaction
INSERT INTO transaction (transaction_type_id, policy_id, status_id, reinstatement_date, lapse_start_date, lapse_end_date, reinstatement_reason)
SELECT 
    tt.id,
    123, -- policy_id
    s.id,
    '2024-01-15',
    '2023-12-01',
    '2024-01-15',
    'Customer requested reinstatement within grace period'
FROM transaction_type tt
CROSS JOIN status s
WHERE tt.code = 'REINSTATEMENT'
AND s.code = 'REINSTATEMENT_PENDING';

-- Step 2: Add line items
INSERT INTO transaction_line (transaction_id, transaction_line_type_id, amount, description, coverage_start_date, coverage_end_date)
VALUES 
    (LAST_INSERT_ID(), 
     (SELECT id FROM transaction_line_type WHERE code = 'REINSTATEMENT_PREMIUM'),
     450.00,
     'Premium for lapse period',
     '2023-12-01',
     '2024-01-15'),
    (LAST_INSERT_ID(),
     (SELECT id FROM transaction_line_type WHERE code = 'REINSTATEMENT_LAPSE_FEE'),
     50.00,
     'Late reinstatement fee',
     '2024-01-15',
     '2024-01-15');
```

## Migration Path

1. **Phase 1**: Add new transaction types and extend existing tables
2. **Phase 2**: Create views and integration tables
3. **Phase 3**: Migrate any existing reinstatement data to transaction format
4. **Phase 4**: Update application code to use transaction-based approach

## Conclusion

This approach leverages the existing transaction infrastructure to handle reinstatements without creating redundant tables. It provides a flexible, scalable solution that integrates seamlessly with the current database design while meeting all GR-41 requirements.