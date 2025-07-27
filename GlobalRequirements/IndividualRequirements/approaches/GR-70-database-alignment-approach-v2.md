# GR-70 Database Alignment Approach - V2

## Overview
This document outlines the approach for adding accounting capabilities to the existing transaction framework without renaming tables or creating redundant structures.

## Current State Analysis

Existing tables that support accounting:
- `transaction` - Core transaction records
- `transaction_type` - Transaction categorization
- `transaction_line` - Line item details
- `transaction_line_type` - Line item categorization
- Various fee, discount, surcharge, commission tables

## Approach: Enhance Transaction Tables for Accounting

### 1. Extend Transaction Tables with Accounting Fields
```sql
-- Add accounting fields to transaction table
ALTER TABLE transaction 
ADD COLUMN IF NOT EXISTS accounting_date DATE COMMENT 'Date for accounting purposes',
ADD COLUMN IF NOT EXISTS fiscal_period VARCHAR(7) COMMENT 'Fiscal period (YYYY-MM)',
ADD COLUMN IF NOT EXISTS accounting_reference VARCHAR(100) COMMENT 'External accounting reference',
ADD COLUMN IF NOT EXISTS journal_entry_id VARCHAR(50) COMMENT 'General ledger journal entry',
ADD COLUMN IF NOT EXISTS is_posted BOOLEAN DEFAULT FALSE COMMENT 'Posted to accounting system',
ADD COLUMN IF NOT EXISTS posted_date DATETIME COMMENT 'When posted to accounting',
ADD COLUMN IF NOT EXISTS posting_user_id INT COMMENT 'User who posted transaction',
ADD COLUMN IF NOT EXISTS reversal_transaction_id INT COMMENT 'Reference to reversal transaction',
ADD COLUMN IF NOT EXISTS is_reversal BOOLEAN DEFAULT FALSE COMMENT 'Is this a reversal transaction',
ADD INDEX idx_transaction_accounting_date (accounting_date),
ADD INDEX idx_transaction_fiscal_period (fiscal_period),
ADD INDEX idx_transaction_posted (is_posted, posted_date),
ADD CONSTRAINT fk_transaction_reversal 
    FOREIGN KEY (reversal_transaction_id) 
    REFERENCES transaction(id);

-- Add accounting fields to transaction_line
ALTER TABLE transaction_line
ADD COLUMN IF NOT EXISTS debit_amount DECIMAL(10,2) COMMENT 'Debit amount for double-entry',
ADD COLUMN IF NOT EXISTS credit_amount DECIMAL(10,2) COMMENT 'Credit amount for double-entry',
ADD COLUMN IF NOT EXISTS gl_account_code VARCHAR(50) COMMENT 'General ledger account code',
ADD COLUMN IF NOT EXISTS cost_center VARCHAR(50) COMMENT 'Cost center for allocation',
ADD COLUMN IF NOT EXISTS tax_code VARCHAR(20) COMMENT 'Tax code for reporting',
ADD COLUMN IF NOT EXISTS is_taxable BOOLEAN DEFAULT TRUE COMMENT 'Subject to tax',
ADD INDEX idx_transaction_line_gl_account (gl_account_code),
ADD INDEX idx_transaction_line_amounts (debit_amount, credit_amount);
```

### 2. Create Accounting Configuration
```sql
-- Add accounting-specific configuration types
INSERT INTO configuration_type (code, name, description, is_default, status_id) VALUES
('ACCOUNTING_GL_MAPPING', 'GL Account Mapping', 'Maps transaction types to GL accounts', FALSE, 1),
('ACCOUNTING_TAX_RULES', 'Tax Configuration', 'Tax calculation and reporting rules', FALSE, 1),
('ACCOUNTING_PERIOD_SETTINGS', 'Accounting Periods', 'Fiscal period configurations', FALSE, 1),
('ACCOUNTING_INTEGRATION', 'Accounting System Integration', 'External accounting system settings', FALSE, 1);

-- GL Account mapping table
CREATE TABLE IF NOT EXISTS gl_account_mapping (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_line_type_id INT NOT NULL,
    gl_account_code VARCHAR(50) NOT NULL,
    gl_account_name VARCHAR(100),
    account_type VARCHAR(50) COMMENT 'ASSET, LIABILITY, REVENUE, EXPENSE',
    is_default BOOLEAN DEFAULT TRUE,
    effective_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_gl_mapping_type (transaction_line_type_id),
    INDEX idx_gl_mapping_account (gl_account_code),
    INDEX idx_gl_mapping_dates (effective_date, end_date),
    CONSTRAINT fk_gl_mapping_line_type 
        FOREIGN KEY (transaction_line_type_id) 
        REFERENCES transaction_line_type(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Maps transaction line types to GL accounts';

-- Sample GL mappings
INSERT INTO gl_account_mapping (transaction_line_type_id, gl_account_code, gl_account_name, account_type) 
SELECT 
    tlt.id,
    CASE 
        WHEN tlt.code LIKE '%PREMIUM%' THEN '4100'
        WHEN tlt.code LIKE '%FEE%' THEN '4200'
        WHEN tlt.code LIKE '%COMMISSION%' THEN '5100'
        WHEN tlt.code LIKE '%TAX%' THEN '2300'
        WHEN tlt.code LIKE '%DISCOUNT%' THEN '4150'
        ELSE '4900'
    END,
    CASE 
        WHEN tlt.code LIKE '%PREMIUM%' THEN 'Premium Revenue'
        WHEN tlt.code LIKE '%FEE%' THEN 'Fee Revenue'
        WHEN tlt.code LIKE '%COMMISSION%' THEN 'Commission Expense'
        WHEN tlt.code LIKE '%TAX%' THEN 'Tax Payable'
        WHEN tlt.code LIKE '%DISCOUNT%' THEN 'Premium Discounts'
        ELSE 'Other Revenue'
    END,
    CASE 
        WHEN tlt.code LIKE '%COMMISSION%' THEN 'EXPENSE'
        WHEN tlt.code LIKE '%TAX%' THEN 'LIABILITY'
        ELSE 'REVENUE'
    END
FROM transaction_line_type tlt;
```

### 3. Accounting Views and Reports
```sql
-- Trial Balance View
CREATE VIEW v_trial_balance AS
SELECT 
    gl.gl_account_code,
    gl.gl_account_name,
    gl.account_type,
    SUM(tl.debit_amount) as total_debits,
    SUM(tl.credit_amount) as total_credits,
    SUM(IFNULL(tl.debit_amount, 0) - IFNULL(tl.credit_amount, 0)) as net_balance,
    t.fiscal_period
FROM transaction t
JOIN transaction_line tl ON t.id = tl.transaction_id
JOIN gl_account_mapping gl ON tl.gl_account_code = gl.gl_account_code
WHERE t.is_posted = TRUE
GROUP BY gl.gl_account_code, gl.gl_account_name, gl.account_type, t.fiscal_period;

-- Revenue Recognition View
CREATE VIEW v_revenue_recognition AS
SELECT 
    t.id as transaction_id,
    t.accounting_date,
    t.fiscal_period,
    tt.name as transaction_type,
    tl.coverage_start_date,
    tl.coverage_end_date,
    DATEDIFF(tl.coverage_end_date, tl.coverage_start_date) + 1 as coverage_days,
    tl.amount as total_amount,
    tl.amount / (DATEDIFF(tl.coverage_end_date, tl.coverage_start_date) + 1) as daily_amount,
    CASE 
        WHEN CURDATE() BETWEEN tl.coverage_start_date AND tl.coverage_end_date 
        THEN tl.amount * DATEDIFF(CURDATE(), tl.coverage_start_date) / (DATEDIFF(tl.coverage_end_date, tl.coverage_start_date) + 1)
        WHEN CURDATE() > tl.coverage_end_date 
        THEN tl.amount
        ELSE 0
    END as earned_amount,
    tl.amount - CASE 
        WHEN CURDATE() BETWEEN tl.coverage_start_date AND tl.coverage_end_date 
        THEN tl.amount * DATEDIFF(CURDATE(), tl.coverage_start_date) / (DATEDIFF(tl.coverage_end_date, tl.coverage_start_date) + 1)
        WHEN CURDATE() > tl.coverage_end_date 
        THEN tl.amount
        ELSE 0
    END as unearned_amount
FROM transaction t
JOIN transaction_type tt ON t.transaction_type_id = tt.id
JOIN transaction_line tl ON t.id = tl.transaction_id
JOIN transaction_line_type tlt ON tl.transaction_line_type_id = tlt.id
WHERE tlt.code LIKE '%PREMIUM%'
AND t.is_posted = TRUE;

-- Accounting Summary by Period
CREATE VIEW v_accounting_summary AS
SELECT 
    t.fiscal_period,
    COUNT(DISTINCT t.id) as transaction_count,
    COUNT(DISTINCT CASE WHEN t.is_reversal THEN t.id END) as reversal_count,
    SUM(tl.debit_amount) as total_debits,
    SUM(tl.credit_amount) as total_credits,
    COUNT(DISTINCT t.policy_id) as unique_policies,
    COUNT(DISTINCT DATE(t.accounting_date)) as active_days
FROM transaction t
JOIN transaction_line tl ON t.id = tl.transaction_id
WHERE t.is_posted = TRUE
GROUP BY t.fiscal_period
ORDER BY t.fiscal_period DESC;
```

### 4. Accounting Integration Tables
```sql
-- Accounting batch processing
CREATE TABLE IF NOT EXISTS accounting_batch (
    id INT AUTO_INCREMENT PRIMARY KEY,
    batch_number VARCHAR(50) UNIQUE NOT NULL,
    batch_date DATE NOT NULL,
    fiscal_period VARCHAR(7) NOT NULL,
    transaction_count INT DEFAULT 0,
    total_debits DECIMAL(12,2) DEFAULT 0,
    total_credits DECIMAL(12,2) DEFAULT 0,
    status VARCHAR(50) DEFAULT 'PENDING',
    posted_date DATETIME,
    posted_by INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_accounting_batch_date (batch_date),
    INDEX idx_accounting_batch_period (fiscal_period),
    INDEX idx_accounting_batch_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tracks accounting batch processing';

-- Link transactions to batches
CREATE TABLE IF NOT EXISTS accounting_batch_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    batch_id INT NOT NULL,
    transaction_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE INDEX idx_batch_transaction (batch_id, transaction_id),
    CONSTRAINT fk_batch_transaction_batch 
        FOREIGN KEY (batch_id) 
        REFERENCES accounting_batch(id),
    CONSTRAINT fk_batch_transaction_trans 
        FOREIGN KEY (transaction_id) 
        REFERENCES transaction(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Links transactions to accounting batches';
```

### 5. Automated Accounting Entry Creation
```sql
-- Stored procedure to create accounting entries
DELIMITER //
CREATE PROCEDURE sp_create_accounting_entries(IN p_transaction_id INT)
BEGIN
    DECLARE v_total_amount DECIMAL(10,2);
    
    -- Get total transaction amount
    SELECT SUM(amount + IFNULL(tax_amount, 0)) INTO v_total_amount
    FROM transaction_line
    WHERE transaction_id = p_transaction_id;
    
    -- Create debit entry (Cash/Receivable)
    UPDATE transaction_line 
    SET debit_amount = amount + IFNULL(tax_amount, 0),
        credit_amount = 0,
        gl_account_code = '1200' -- Accounts Receivable
    WHERE transaction_id = p_transaction_id
    AND transaction_line_type_id IN (
        SELECT id FROM transaction_line_type WHERE code LIKE '%PREMIUM%'
    )
    LIMIT 1;
    
    -- Create credit entries based on line type
    UPDATE transaction_line tl
    JOIN transaction_line_type tlt ON tl.transaction_line_type_id = tlt.id
    LEFT JOIN gl_account_mapping glm ON tlt.id = glm.transaction_line_type_id
    SET tl.credit_amount = tl.amount,
        tl.debit_amount = 0,
        tl.gl_account_code = IFNULL(glm.gl_account_code, '4900')
    WHERE tl.transaction_id = p_transaction_id
    AND tl.id NOT IN (
        SELECT id FROM transaction_line 
        WHERE transaction_id = p_transaction_id 
        AND debit_amount > 0
        LIMIT 1
    );
    
    -- Mark transaction as having accounting entries
    UPDATE transaction 
    SET accounting_date = IFNULL(accounting_date, CURDATE()),
        fiscal_period = DATE_FORMAT(IFNULL(accounting_date, CURDATE()), '%Y-%m')
    WHERE id = p_transaction_id;
END//
DELIMITER ;
```

### 6. Tax Handling
```sql
-- Tax configuration
CREATE TABLE IF NOT EXISTS tax_configuration (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tax_code VARCHAR(20) NOT NULL UNIQUE,
    tax_name VARCHAR(100) NOT NULL,
    tax_rate DECIMAL(5,4) NOT NULL,
    tax_type VARCHAR(50) COMMENT 'SALES, VAT, GST, etc',
    gl_account_code VARCHAR(50),
    state_code VARCHAR(2),
    effective_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_tax_config_code (tax_code),
    INDEX idx_tax_config_state (state_code),
    INDEX idx_tax_config_dates (effective_date, end_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tax rates and configuration';

-- Sample tax configurations
INSERT INTO tax_configuration (tax_code, tax_name, tax_rate, tax_type, gl_account_code, state_code) VALUES
('CA_SALES', 'California Sales Tax', 0.0725, 'SALES', '2310', 'CA'),
('TX_SALES', 'Texas Sales Tax', 0.0625, 'SALES', '2310', 'TX'),
('FL_SALES', 'Florida Sales Tax', 0.0600, 'SALES', '2310', 'FL');
```

## Example Usage

### Creating a Transaction with Accounting
```sql
-- 1. Create transaction
INSERT INTO transaction (transaction_type_id, policy_id, accounting_date, fiscal_period, status_id)
VALUES (
    (SELECT id FROM transaction_type WHERE code = 'PREMIUM_PAYMENT'),
    789,
    CURDATE(),
    DATE_FORMAT(CURDATE(), '%Y-%m'),
    1
);

SET @trans_id = LAST_INSERT_ID();

-- 2. Add line items with amounts
INSERT INTO transaction_line (transaction_id, transaction_line_type_id, amount, tax_amount, coverage_start_date, coverage_end_date)
VALUES 
    (@trans_id, 
     (SELECT id FROM transaction_line_type WHERE code = 'MONTHLY_PREMIUM'),
     1000.00,
     72.50,
     DATE_FORMAT(CURDATE(), '%Y-%m-01'),
     LAST_DAY(CURDATE()));

-- 3. Create accounting entries
CALL sp_create_accounting_entries(@trans_id);

-- 4. Add to batch for posting
INSERT INTO accounting_batch (batch_number, batch_date, fiscal_period)
VALUES (
    CONCAT('BATCH-', DATE_FORMAT(CURDATE(), '%Y%m%d'), '-01'),
    CURDATE(),
    DATE_FORMAT(CURDATE(), '%Y-%m')
);

INSERT INTO accounting_batch_transaction (batch_id, transaction_id)
VALUES (LAST_INSERT_ID(), @trans_id);
```

### Posting to External Accounting System
```sql
-- Mark transactions as posted
UPDATE transaction t
JOIN accounting_batch_transaction abt ON t.id = abt.transaction_id
JOIN accounting_batch ab ON abt.batch_id = ab.id
SET t.is_posted = TRUE,
    t.posted_date = NOW(),
    t.posting_user_id = 1,
    t.journal_entry_id = CONCAT('JE-', ab.batch_number)
WHERE ab.id = 123
AND ab.status = 'APPROVED';
```

## Benefits of This Approach

1. **No Table Renaming**: Works within existing transaction framework
2. **Double-Entry Support**: Debit/credit fields enable proper accounting
3. **GL Integration**: Flexible mapping to chart of accounts
4. **Tax Compliance**: Built-in tax handling and reporting
5. **Audit Trail**: Complete tracking of accounting entries
6. **Batch Processing**: Supports periodic posting to external systems
7. **Revenue Recognition**: Handles earned/unearned calculations

## Migration Path

1. **Phase 1**: Add accounting fields to existing tables
2. **Phase 2**: Create GL mapping and configuration
3. **Phase 3**: Implement views and reports
4. **Phase 4**: Set up batch processing
5. **Phase 5**: Enable external system integration

## Conclusion

This approach enhances the existing transaction infrastructure to support full accounting functionality without creating new core tables or renaming existing ones. It provides enterprise-grade accounting capabilities while maintaining backward compatibility with current systems.