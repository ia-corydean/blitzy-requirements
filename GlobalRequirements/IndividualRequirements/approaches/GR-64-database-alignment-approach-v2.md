# GR-64 Database Alignment Approach - V2

## Overview
This document outlines the approach for handling policy reinstatements using the existing transaction-based architecture, aligning with the approach defined in GR-41.

## Current State Analysis

From GR-41 v2 approach, we have:
- Transaction-based reinstatement handling
- Use of `transaction` and `transaction_type` tables
- Transaction line items for detailed tracking
- Integration with payment processing

## Approach: Extending Transaction Model for GR-64

### 1. Additional Transaction Types for Reinstatement Workflow
```sql
-- Extend transaction types for complete reinstatement lifecycle
INSERT INTO transaction_type (code, name, description, is_default, status_id) VALUES
('REINSTATEMENT_QUOTE', 'Reinstatement Quote', 'Quote for policy reinstatement', FALSE, 1),
('REINSTATEMENT_PENDING', 'Pending Reinstatement', 'Reinstatement awaiting conditions', FALSE, 1),
('REINSTATEMENT_PARTIAL', 'Partial Reinstatement', 'Partial coverage reinstatement', FALSE, 1),
('REINSTATEMENT_CONDITIONAL', 'Conditional Reinstatement', 'Reinstatement with conditions', FALSE, 1),
('REINSTATEMENT_CANCELLED', 'Cancelled Reinstatement', 'Reinstatement request cancelled', FALSE, 1);

-- Additional line item types for detailed tracking
INSERT INTO transaction_line_type (code, name, description, is_default, status_id) VALUES
('REINSTATEMENT_BACKDATE_PREMIUM', 'Backdated Premium', 'Premium for backdated coverage period', FALSE, 1),
('REINSTATEMENT_PENALTY', 'Reinstatement Penalty', 'Penalty fee for late reinstatement', FALSE, 1),
('REINSTATEMENT_INSPECTION_FEE', 'Inspection Fee', 'Required inspection fee', FALSE, 1),
('REINSTATEMENT_UNDERWRITING_FEE', 'Underwriting Review Fee', 'Fee for underwriting review', FALSE, 1);
```

### 2. Leverage Existing Tables with Reinstatement Context
```sql
-- Create a view that combines transaction data for reinstatement workflow
CREATE VIEW v_reinstatement_workflow AS
SELECT 
    t.id as transaction_id,
    tt.code as transaction_type,
    tt.name as transaction_type_name,
    t.policy_id,
    p.policy_number,
    p.effective_date as original_effective_date,
    p.expiration_date as original_expiration_date,
    t.reinstatement_date,
    t.lapse_start_date,
    t.lapse_end_date,
    DATEDIFF(IFNULL(t.lapse_end_date, CURDATE()), t.lapse_start_date) as lapse_duration_days,
    t.reinstatement_reason,
    t.requires_underwriting,
    s.code as status_code,
    s.name as status_name,
    t.created_at as request_date,
    t.updated_at as last_updated
FROM transaction t
JOIN transaction_type tt ON t.transaction_type_id = tt.id
JOIN policy p ON t.policy_id = p.id
JOIN status s ON t.status_id = s.id
WHERE tt.code LIKE 'REINSTATEMENT_%'
ORDER BY t.created_at DESC;

-- View for reinstatement financial summary
CREATE VIEW v_reinstatement_financials AS
SELECT 
    t.id as transaction_id,
    t.policy_id,
    p.policy_number,
    SUM(CASE WHEN tlt.code LIKE '%PREMIUM%' THEN tl.amount ELSE 0 END) as total_premium,
    SUM(CASE WHEN tlt.code LIKE '%FEE%' THEN tl.amount ELSE 0 END) as total_fees,
    SUM(CASE WHEN tlt.code LIKE '%PENALTY%' THEN tl.amount ELSE 0 END) as total_penalties,
    SUM(tl.tax_amount) as total_tax,
    SUM(tl.amount + IFNULL(tl.tax_amount, 0)) as total_due,
    COUNT(DISTINCT tl.id) as line_item_count
FROM transaction t
JOIN transaction_type tt ON t.transaction_type_id = tt.id
JOIN policy p ON t.policy_id = p.id
LEFT JOIN transaction_line tl ON t.id = tl.transaction_id
LEFT JOIN transaction_line_type tlt ON tl.transaction_line_type_id = tlt.id
WHERE tt.code LIKE 'REINSTATEMENT_%'
GROUP BY t.id, t.policy_id, p.policy_number;
```

### 3. Integration with Policy Status Management
```sql
-- Add policy status tracking for reinstatements
CREATE TABLE IF NOT EXISTS policy_status_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    policy_id INT NOT NULL,
    status_id INT NOT NULL,
    reason VARCHAR(255),
    transaction_id INT COMMENT 'Related transaction if applicable',
    effective_date DATETIME NOT NULL,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_policy_status_history (policy_id, effective_date),
    INDEX idx_policy_status_transaction (transaction_id),
    CONSTRAINT fk_policy_status_history_policy 
        FOREIGN KEY (policy_id) 
        REFERENCES policy(id),
    CONSTRAINT fk_policy_status_history_status 
        FOREIGN KEY (status_id) 
        REFERENCES status(id),
    CONSTRAINT fk_policy_status_history_transaction 
        FOREIGN KEY (transaction_id) 
        REFERENCES transaction(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tracks policy status changes including reinstatements';

-- Status entries for reinstatement workflow
INSERT INTO status (code, name, description, is_default) VALUES
('POLICY_LAPSED', 'Lapsed', 'Policy lapsed due to non-payment', FALSE),
('POLICY_CANCELLED', 'Cancelled', 'Policy cancelled', FALSE),
('POLICY_REINSTATEMENT_ELIGIBLE', 'Reinstatement Eligible', 'Eligible for reinstatement', FALSE),
('POLICY_REINSTATEMENT_PENDING', 'Reinstatement Pending', 'Reinstatement in progress', FALSE),
('POLICY_REINSTATED', 'Reinstated', 'Policy successfully reinstated', FALSE);
```

### 4. Reinstatement Rules Configuration
```sql
-- Use configuration tables for reinstatement rules
INSERT INTO configuration_type (code, name, description, is_default, status_id) VALUES
('REINSTATEMENT_RULES', 'Reinstatement Rules', 'Business rules for policy reinstatement', FALSE, 1),
('REINSTATEMENT_GRACE_PERIODS', 'Grace Period Rules', 'Grace period configurations', FALSE, 1),
('REINSTATEMENT_REQUIREMENTS', 'Reinstatement Requirements', 'Requirements by state/product', FALSE, 1);

-- Store complex reinstatement rules as JSON
INSERT INTO configuration_value (configuration_id, key_name, value_json)
SELECT 
    c.id,
    'standard_rules',
    JSON_OBJECT(
        'max_lapse_days', 30,
        'require_payment_in_full', true,
        'require_no_claims_during_lapse', true,
        'allow_partial_reinstatement', false,
        'underwriting_required_after_days', 60,
        'inspection_required_after_days', 90,
        'state_specific_rules', JSON_OBJECT(
            'CA', JSON_OBJECT('max_lapse_days', 45, 'grace_period_days', 10),
            'TX', JSON_OBJECT('max_lapse_days', 30, 'grace_period_days', 7),
            'FL', JSON_OBJECT('max_lapse_days', 60, 'grace_period_days', 14)
        )
    )
FROM configuration c
JOIN configuration_type ct ON c.configuration_type_id = ct.id
WHERE ct.code = 'REINSTATEMENT_RULES';
```

### 5. Reinstatement Workflow Tracking
```sql
-- Create a reinstatement request tracking mechanism
CREATE TABLE IF NOT EXISTS reinstatement_workflow (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL UNIQUE,
    workflow_step VARCHAR(50) NOT NULL,
    step_status VARCHAR(50) NOT NULL,
    step_result TEXT,
    completed_at DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_reinstatement_workflow_step (workflow_step, step_status),
    CONSTRAINT fk_reinstatement_workflow_transaction 
        FOREIGN KEY (transaction_id) 
        REFERENCES transaction(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tracks reinstatement workflow steps';

-- Workflow steps
INSERT INTO reinstatement_workflow (transaction_id, workflow_step, step_status) VALUES
(1001, 'ELIGIBILITY_CHECK', 'COMPLETED'),
(1001, 'CALCULATE_PREMIUM', 'COMPLETED'),
(1001, 'PAYMENT_COLLECTION', 'IN_PROGRESS'),
(1001, 'UNDERWRITING_REVIEW', 'PENDING'),
(1001, 'POLICY_UPDATE', 'PENDING'),
(1001, 'NOTIFICATION', 'PENDING');
```

### 6. Integration Points

#### With Payment System
```sql
-- View to track reinstatement payments
CREATE VIEW v_reinstatement_payments AS
SELECT 
    t.id as transaction_id,
    t.policy_id,
    p.policy_number,
    mtp.payment_amount,
    mtp.payment_date,
    mtp.payment_reference,
    mtp.is_successful,
    pm.payment_method_type_id,
    pmt.name as payment_method
FROM transaction t
JOIN transaction_type tt ON t.transaction_type_id = tt.id
JOIN policy p ON t.policy_id = p.id
LEFT JOIN map_transaction_payment mtp ON t.id = mtp.transaction_id
LEFT JOIN payment_method pm ON mtp.payment_method_id = pm.id
LEFT JOIN payment_method_type pmt ON pm.payment_method_type_id = pmt.id
WHERE tt.code LIKE 'REINSTATEMENT_%';
```

#### With Document Management
```sql
-- Track required documents for reinstatement
CREATE TABLE IF NOT EXISTS reinstatement_documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    document_name VARCHAR(255),
    is_required BOOLEAN DEFAULT TRUE,
    is_received BOOLEAN DEFAULT FALSE,
    received_date DATETIME,
    document_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_reinstatement_docs_transaction (transaction_id),
    INDEX idx_reinstatement_docs_type (document_type),
    CONSTRAINT fk_reinstatement_docs_transaction 
        FOREIGN KEY (transaction_id) 
        REFERENCES transaction(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Documents required for reinstatement';
```

## Example Reinstatement Process

```sql
-- 1. Create reinstatement quote
INSERT INTO transaction (transaction_type_id, policy_id, status_id, reinstatement_date, lapse_start_date, lapse_end_date, reinstatement_reason)
SELECT 
    tt.id, 
    456, -- policy_id
    s.id,
    DATE_ADD(CURDATE(), INTERVAL 1 DAY), -- proposed reinstatement date
    '2024-01-01', -- when policy lapsed
    CURDATE(), -- current date as end of lapse
    'Customer requested reinstatement after resolving payment issues'
FROM transaction_type tt
CROSS JOIN status s
WHERE tt.code = 'REINSTATEMENT_QUOTE'
AND s.code = 'REINSTATEMENT_PENDING';

SET @transaction_id = LAST_INSERT_ID();

-- 2. Add line items for fees and premium
INSERT INTO transaction_line (transaction_id, transaction_line_type_id, amount, description, coverage_start_date, coverage_end_date)
SELECT 
    @transaction_id,
    tlt.id,
    CASE 
        WHEN tlt.code = 'REINSTATEMENT_BACKDATE_PREMIUM' THEN 850.00
        WHEN tlt.code = 'REINSTATEMENT_LAPSE_FEE' THEN 75.00
        WHEN tlt.code = 'REINSTATEMENT_PROCESSING' THEN 25.00
    END,
    CASE 
        WHEN tlt.code = 'REINSTATEMENT_BACKDATE_PREMIUM' THEN 'Premium for lapse period coverage'
        WHEN tlt.code = 'REINSTATEMENT_LAPSE_FEE' THEN 'Late reinstatement fee'
        WHEN tlt.code = 'REINSTATEMENT_PROCESSING' THEN 'Administrative processing'
    END,
    '2024-01-01',
    '2024-12-31'
FROM transaction_line_type tlt
WHERE tlt.code IN ('REINSTATEMENT_BACKDATE_PREMIUM', 'REINSTATEMENT_LAPSE_FEE', 'REINSTATEMENT_PROCESSING');

-- 3. Initialize workflow
INSERT INTO reinstatement_workflow (transaction_id, workflow_step, step_status)
VALUES 
    (@transaction_id, 'ELIGIBILITY_CHECK', 'IN_PROGRESS'),
    (@transaction_id, 'CALCULATE_PREMIUM', 'PENDING'),
    (@transaction_id, 'PAYMENT_COLLECTION', 'PENDING'),
    (@transaction_id, 'UNDERWRITING_REVIEW', 'PENDING'),
    (@transaction_id, 'POLICY_UPDATE', 'PENDING'),
    (@transaction_id, 'NOTIFICATION', 'PENDING');

-- 4. Track policy status change
INSERT INTO policy_status_history (policy_id, status_id, reason, transaction_id, effective_date)
SELECT 
    456,
    s.id,
    'Reinstatement initiated',
    @transaction_id,
    NOW()
FROM status s
WHERE s.code = 'POLICY_REINSTATEMENT_PENDING';
```

## Benefits of This Approach

1. **Unified Model**: Uses same transaction framework as GR-41
2. **No Table Duplication**: Leverages existing infrastructure
3. **Complete Audit Trail**: Full history through transactions
4. **Flexible Configuration**: Rules stored in configuration tables
5. **Workflow Support**: Built-in workflow tracking
6. **Financial Integration**: Seamless payment tracking

## Migration Considerations

1. **No New Core Tables**: Only supporting tables for workflow
2. **Configuration-Driven**: Rules can be adjusted without code changes
3. **View-Based Reporting**: Easy to create reports without schema changes
4. **Backward Compatible**: Existing systems continue to function

## Conclusion

This approach fully aligns with GR-41's transaction-based model while meeting all GR-64 reinstatement requirements. By using existing tables and adding minimal supporting structures, we achieve a robust reinstatement system without architectural changes.