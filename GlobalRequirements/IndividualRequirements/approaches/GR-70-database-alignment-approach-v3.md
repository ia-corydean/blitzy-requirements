# GR-70 Database Alignment Approach - V3
- this is not going to be a general ledger system
- we are to account for the finanical transactions associated with policies, policy changes, payments, etc..
  - we should reference data that exisits in other table where possible
  - it's essentially supporting the processes that create the premium and changes to premium and reflects the change to policy and installment premium premium.
  - the credits and debits should be depicten in the transaction_line
  - the general/overall transaction information should be in transaction
  - then we can say map_policy_transaction to see the overall details and the specfifics
- calculations should be handled in source code while the data to support those calculations are distrinuted amongs main tables and the result of those calculations end up in transaction and transaction_line and the policy table
## Overview
This document incorporates accounting patterns from the Accounting output documentation and aligns with reinstatement workflow requirements from the Documentation folder, providing a comprehensive accounting architecture.

## Changes from V2
1. **Added double-entry accounting patterns** - From accounting-infrastructure-support-updated.md
2. **Incorporated reinstatement accounting workflows** - Integration with GR-64 patterns
3. **Enhanced GL mapping structure** - More detailed chart of accounts integration
4. **Added payment processing integration** - Paysafe token-based architecture from documentation

## Accounting Architecture Analysis

From the Accounting documentation, key requirements:
- **Equity-based accounting system** - Assets = Liabilities + Equity
- **Program-centric configuration** - Each insurance program defines its own rules
- **Zero sensitive data storage** - Only Paysafe tokens stored
- **Audit-first design** - Complete transaction traceability
- **Modular and extensible** - Configuration-driven fee types and rules

## Approach: Comprehensive Accounting with Transaction Framework

### 1. Core Accounting Tables Enhancement
```sql
-- Enhance transaction table for full accounting support
ALTER TABLE transaction 
-- Core accounting fields
ADD COLUMN IF NOT EXISTS transaction_subtype VARCHAR(50) AFTER transaction_type_id,
ADD COLUMN IF NOT EXISTS accounting_date DATE COMMENT 'Date for accounting purposes',
ADD COLUMN IF NOT EXISTS fiscal_period VARCHAR(7) COMMENT 'YYYY-MM fiscal period',
ADD COLUMN IF NOT EXISTS accounting_reference VARCHAR(100) COMMENT 'External accounting reference',
ADD COLUMN IF NOT EXISTS journal_entry_id VARCHAR(50) COMMENT 'General ledger journal entry',
ADD COLUMN IF NOT EXISTS is_posted BOOLEAN DEFAULT FALSE COMMENT 'Posted to accounting system',
ADD COLUMN IF NOT EXISTS posted_date DATETIME COMMENT 'When posted to accounting',
ADD COLUMN IF NOT EXISTS posting_user_id INT COMMENT 'User who posted transaction',
ADD COLUMN IF NOT EXISTS posting_batch_id INT COMMENT 'Batch posting reference',

-- Reversal support
ADD COLUMN IF NOT EXISTS reversal_transaction_id INT COMMENT 'Reference to reversal transaction',
ADD COLUMN IF NOT EXISTS is_reversal BOOLEAN DEFAULT FALSE COMMENT 'Is this a reversal transaction',
ADD COLUMN IF NOT EXISTS reversal_reason VARCHAR(255) COMMENT 'Reason for reversal',

-- Program configuration
ADD COLUMN IF NOT EXISTS program_id INT COMMENT 'Insurance program reference',
ADD COLUMN IF NOT EXISTS program_rules_applied JSON COMMENT 'Program-specific rules applied',

ADD INDEX idx_transaction_accounting_date (accounting_date),
ADD INDEX idx_transaction_fiscal_period (fiscal_period),
ADD INDEX idx_transaction_posted (is_posted, posted_date),
ADD INDEX idx_transaction_program (program_id),
ADD CONSTRAINT fk_transaction_reversal 
    FOREIGN KEY (reversal_transaction_id) 
    REFERENCES transaction(id),
ADD CONSTRAINT fk_transaction_posting_user 
    FOREIGN KEY (posting_user_id) 
    REFERENCES user(id),
ADD CONSTRAINT fk_transaction_program 
    FOREIGN KEY (program_id) 
    REFERENCES program(id);

-- Comprehensive transaction types for accounting
INSERT INTO transaction_type (code, name, description, is_default, status_id) VALUES
-- Premium transactions
('PREMIUM_NEW', 'New Business Premium', 'Initial policy premium', FALSE, 1),
('PREMIUM_RENEWAL', 'Renewal Premium', 'Policy renewal premium', FALSE, 1),
('PREMIUM_ENDORSEMENT', 'Endorsement Premium', 'Premium change from endorsement', FALSE, 1),
('PREMIUM_AUDIT', 'Audit Premium', 'Premium adjustment from audit', FALSE, 1),
('PREMIUM_REINSTATEMENT', 'Reinstatement Premium', 'Premium for reinstated policy', FALSE, 1),

-- Fee transactions
('FEE_POLICY', 'Policy Fee', 'Standard policy issuance fee', FALSE, 1),
('FEE_INSTALLMENT', 'Installment Fee', 'Payment plan fee', FALSE, 1),
('FEE_LATE', 'Late Payment Fee', 'Late payment penalty', FALSE, 1),
('FEE_NSF', 'NSF Fee', 'Non-sufficient funds fee', FALSE, 1),
('FEE_SR22', 'SR22 Filing Fee', 'SR22 filing fee', FALSE, 1),
('FEE_REINSTATEMENT', 'Reinstatement Fee', 'Policy reinstatement fee', FALSE, 1),

-- Payment transactions
('PAYMENT_RECEIVED', 'Payment Received', 'Customer payment received', FALSE, 1),
('PAYMENT_REFUND', 'Payment Refund', 'Refund to customer', FALSE, 1),
('PAYMENT_CHARGEBACK', 'Payment Chargeback', 'Payment chargeback', FALSE, 1),
('PAYMENT_VOID', 'Payment Void', 'Voided payment', FALSE, 1),

-- Commission transactions
('COMMISSION_NEW', 'New Business Commission', 'Commission on new policy', FALSE, 1),
('COMMISSION_RENEWAL', 'Renewal Commission', 'Commission on renewal', FALSE, 1),
('COMMISSION_ADJUSTMENT', 'Commission Adjustment', 'Commission correction', FALSE, 1),
('COMMISSION_CHARGEBACK', 'Commission Chargeback', 'Commission recovery', FALSE, 1),

-- Adjustment transactions
('ADJUSTMENT_PREMIUM', 'Premium Adjustment', 'Manual premium adjustment', FALSE, 1),
('ADJUSTMENT_FEE', 'Fee Adjustment', 'Manual fee adjustment', FALSE, 1),
('ADJUSTMENT_WAIVER', 'Fee Waiver', 'Waived fees', FALSE, 1),
('ADJUSTMENT_WRITEOFF', 'Write-off', 'Bad debt write-off', FALSE, 1);
```

### 2. Enhanced Transaction Line for Double-Entry
```sql
-- Enhance transaction_line for complete double-entry accounting
ALTER TABLE transaction_line
-- Double-entry fields
ADD COLUMN IF NOT EXISTS debit_amount DECIMAL(10,2) DEFAULT 0 COMMENT 'Debit amount',
ADD COLUMN IF NOT EXISTS credit_amount DECIMAL(10,2) DEFAULT 0 COMMENT 'Credit amount',
ADD COLUMN IF NOT EXISTS gl_account_code VARCHAR(20) COMMENT 'General ledger account',
ADD COLUMN IF NOT EXISTS cost_center VARCHAR(50) COMMENT 'Cost center allocation',
ADD COLUMN IF NOT EXISTS department_code VARCHAR(20) COMMENT 'Department allocation',

-- Component breakdown
ADD COLUMN IF NOT EXISTS component_type VARCHAR(50) COMMENT 'PREMIUM, FEE, TAX, COMMISSION',
ADD COLUMN IF NOT EXISTS component_subtype VARCHAR(50) COMMENT 'Detailed component classification',

-- Tax handling
ADD COLUMN IF NOT EXISTS tax_code VARCHAR(20) COMMENT 'Tax code for reporting',
ADD COLUMN IF NOT EXISTS tax_rate DECIMAL(5,4) COMMENT 'Applied tax rate',
ADD COLUMN IF NOT EXISTS is_taxable BOOLEAN DEFAULT TRUE COMMENT 'Subject to tax',

-- Program-specific
ADD COLUMN IF NOT EXISTS program_fee_config_id INT COMMENT 'Program fee configuration used',

ADD INDEX idx_transaction_line_gl_account (gl_account_code),
ADD INDEX idx_transaction_line_component (component_type, component_subtype),
ADD INDEX idx_transaction_line_amounts (debit_amount, credit_amount),
ADD CONSTRAINT fk_transaction_line_fee_config 
    FOREIGN KEY (program_fee_config_id) 
    REFERENCES program_fee_configuration(id),
ADD CONSTRAINT chk_debit_credit_balance CHECK (
    (debit_amount > 0 AND credit_amount = 0) OR 
    (credit_amount > 0 AND debit_amount = 0) OR
    (debit_amount = 0 AND credit_amount = 0)
);
```

### 3. Chart of Accounts Structure
```sql
-- Account types
CREATE TABLE IF NOT EXISTS account_type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    normal_balance ENUM('DEBIT', 'CREDIT') NOT NULL,
    financial_statement VARCHAR(50) COMMENT 'BALANCE_SHEET, INCOME_STATEMENT',
    display_order INT DEFAULT 0,
    status_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_account_type_status 
        FOREIGN KEY (status_id) 
        REFERENCES status(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO account_type (code, name, normal_balance, financial_statement, display_order, status_id) VALUES
('ASSET', 'Assets', 'DEBIT', 'BALANCE_SHEET', 1, 1),
('LIABILITY', 'Liabilities', 'CREDIT', 'BALANCE_SHEET', 2, 1),
('EQUITY', 'Equity', 'CREDIT', 'BALANCE_SHEET', 3, 1),
('REVENUE', 'Revenue', 'CREDIT', 'INCOME_STATEMENT', 4, 1),
('EXPENSE', 'Expenses', 'DEBIT', 'INCOME_STATEMENT', 5, 1);

-- Chart of Accounts
CREATE TABLE IF NOT EXISTS chart_of_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_code VARCHAR(20) UNIQUE NOT NULL,
    account_name VARCHAR(100) NOT NULL,
    account_type_id INT NOT NULL,
    parent_account_id INT NULL,
    level INT DEFAULT 1,
    is_header BOOLEAN DEFAULT FALSE COMMENT 'Header account (no transactions)',
    is_active BOOLEAN DEFAULT TRUE,
    is_system_account BOOLEAN DEFAULT FALSE COMMENT 'Protected system account',
    normal_balance ENUM('DEBIT', 'CREDIT') NOT NULL,
    description TEXT NULL,
    
    -- Insurance-specific
    component_type VARCHAR(50) COMMENT 'Default component type for this account',
    is_premium_account BOOLEAN DEFAULT FALSE,
    is_commission_account BOOLEAN DEFAULT FALSE,
    is_tax_account BOOLEAN DEFAULT FALSE,
    
    status_id INT NOT NULL,
    created_by INT NOT NULL,
    updated_by INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_coa_code (account_code),
    INDEX idx_coa_type (account_type_id),
    INDEX idx_coa_parent (parent_account_id),
    INDEX idx_coa_component (component_type),
    CONSTRAINT fk_coa_type 
        FOREIGN KEY (account_type_id) 
        REFERENCES account_type(id),
    CONSTRAINT fk_coa_parent 
        FOREIGN KEY (parent_account_id) 
        REFERENCES chart_of_accounts(id),
    CONSTRAINT fk_coa_status 
        FOREIGN KEY (status_id) 
        REFERENCES status(id),
    CONSTRAINT fk_coa_created 
        FOREIGN KEY (created_by) 
        REFERENCES user(id),
    CONSTRAINT fk_coa_updated 
        FOREIGN KEY (updated_by) 
        REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Chart of accounts for insurance operations';

-- Standard insurance chart of accounts
INSERT INTO chart_of_accounts 
(account_code, account_name, account_type_id, normal_balance, is_header, component_type, is_system_account, status_id, created_by) 
VALUES
-- Assets
('1000', 'Assets', 1, 'DEBIT', TRUE, NULL, TRUE, 1, 1),
('1100', 'Cash and Cash Equivalents', 1, 'DEBIT', TRUE, NULL, TRUE, 1, 1),
('1110', 'Operating Cash', 1, 'DEBIT', FALSE, NULL, TRUE, 1, 1),
('1120', 'Premium Trust Account', 1, 'DEBIT', FALSE, NULL, TRUE, 1, 1),
('1200', 'Receivables', 1, 'DEBIT', TRUE, NULL, TRUE, 1, 1),
('1210', 'Premium Receivable', 1, 'DEBIT', FALSE, 'PREMIUM', TRUE, 1, 1),
('1220', 'Agent Balances', 1, 'DEBIT', FALSE, NULL, TRUE, 1, 1),

-- Liabilities
('2000', 'Liabilities', 2, 'CREDIT', TRUE, NULL, TRUE, 1, 1),
('2100', 'Unearned Premium', 2, 'CREDIT', FALSE, 'PREMIUM', TRUE, 1, 1),
('2200', 'Claims Payable', 2, 'CREDIT', FALSE, NULL, TRUE, 1, 1),
('2300', 'Taxes Payable', 2, 'CREDIT', TRUE, NULL, TRUE, 1, 1),
('2310', 'Premium Tax Payable', 2, 'CREDIT', FALSE, 'TAX', TRUE, 1, 1),
('2320', 'Sales Tax Payable', 2, 'CREDIT', FALSE, 'TAX', TRUE, 1, 1),

-- Revenue
('4000', 'Revenue', 4, 'CREDIT', TRUE, NULL, TRUE, 1, 1),
('4100', 'Premium Revenue', 4, 'CREDIT', TRUE, NULL, TRUE, 1, 1),
('4110', 'Written Premium', 4, 'CREDIT', FALSE, 'PREMIUM', TRUE, 1, 1),
('4120', 'Earned Premium', 4, 'CREDIT', FALSE, 'PREMIUM', TRUE, 1, 1),
('4200', 'Fee Revenue', 4, 'CREDIT', TRUE, NULL, TRUE, 1, 1),
('4210', 'Policy Fees', 4, 'CREDIT', FALSE, 'FEE', TRUE, 1, 1),
('4220', 'Installment Fees', 4, 'CREDIT', FALSE, 'FEE', TRUE, 1, 1),
('4230', 'Late Fees', 4, 'CREDIT', FALSE, 'FEE', TRUE, 1, 1),
('4240', 'NSF Fees', 4, 'CREDIT', FALSE, 'FEE', TRUE, 1, 1),
('4250', 'SR22 Fees', 4, 'CREDIT', FALSE, 'FEE', TRUE, 1, 1),

-- Expenses
('5000', 'Expenses', 5, 'DEBIT', TRUE, NULL, TRUE, 1, 1),
('5100', 'Commission Expense', 5, 'DEBIT', TRUE, NULL, TRUE, 1, 1),
('5110', 'Agent Commission', 5, 'DEBIT', FALSE, 'COMMISSION', TRUE, 1, 1),
('5120', 'Broker Commission', 5, 'DEBIT', FALSE, 'COMMISSION', TRUE, 1, 1);
```

### 4. GL Account Mapping Configuration
```sql
-- GL mapping by transaction and component type
CREATE TABLE IF NOT EXISTS gl_account_mapping (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_type_id INT NULL COMMENT 'Specific transaction type',
    transaction_line_type_id INT NULL COMMENT 'Specific line type',
    component_type VARCHAR(50) NULL COMMENT 'Component type filter',
    component_subtype VARCHAR(50) NULL COMMENT 'Component subtype filter',
    
    -- Account mappings
    debit_account_code VARCHAR(20) NOT NULL,
    credit_account_code VARCHAR(20) NOT NULL,
    
    -- Conditions
    condition_json JSON COMMENT 'Additional conditions for mapping',
    priority INT DEFAULT 100 COMMENT 'Higher priority wins',
    
    -- Program specific
    program_id INT NULL COMMENT 'Program-specific mapping',
    
    is_active BOOLEAN DEFAULT TRUE,
    effective_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_gl_mapping_type (transaction_type_id),
    INDEX idx_gl_mapping_line_type (transaction_line_type_id),
    INDEX idx_gl_mapping_component (component_type, component_subtype),
    INDEX idx_gl_mapping_priority (priority DESC),
    INDEX idx_gl_mapping_program (program_id),
    CONSTRAINT fk_gl_mapping_trans_type 
        FOREIGN KEY (transaction_type_id) 
        REFERENCES transaction_type(id),
    CONSTRAINT fk_gl_mapping_line_type 
        FOREIGN KEY (transaction_line_type_id) 
        REFERENCES transaction_line_type(id),
    CONSTRAINT fk_gl_mapping_program 
        FOREIGN KEY (program_id) 
        REFERENCES program(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Maps transactions to GL accounts';

-- Standard GL mappings
INSERT INTO gl_account_mapping 
(transaction_type_id, component_type, debit_account_code, credit_account_code, priority) 
VALUES
-- Premium transactions
((SELECT id FROM transaction_type WHERE code = 'PREMIUM_NEW'), 'PREMIUM', '1210', '4110', 100),
((SELECT id FROM transaction_type WHERE code = 'PREMIUM_ENDORSEMENT'), 'PREMIUM', '1210', '4110', 100),
((SELECT id FROM transaction_type WHERE code = 'PREMIUM_REINSTATEMENT'), 'PREMIUM', '1210', '4110', 100),

-- Fee transactions
((SELECT id FROM transaction_type WHERE code = 'FEE_POLICY'), 'FEE', '1210', '4210', 100),
((SELECT id FROM transaction_type WHERE code = 'FEE_INSTALLMENT'), 'FEE', '1210', '4220', 100),
((SELECT id FROM transaction_type WHERE code = 'FEE_LATE'), 'FEE', '1210', '4230', 100),
((SELECT id FROM transaction_type WHERE code = 'FEE_NSF'), 'FEE', '1210', '4240', 100),
((SELECT id FROM transaction_type WHERE code = 'FEE_SR22'), 'FEE', '1210', '4250', 100),

-- Payment transactions
((SELECT id FROM transaction_type WHERE code = 'PAYMENT_RECEIVED'), NULL, '1110', '1210', 100),
((SELECT id FROM transaction_type WHERE code = 'PAYMENT_REFUND'), NULL, '1210', '1110', 100),

-- Commission transactions
((SELECT id FROM transaction_type WHERE code = 'COMMISSION_NEW'), 'COMMISSION', '5110', '1220', 100);
```

### 5. Payment Integration with Paysafe Tokens
```sql
-- Payment method storage (tokens only)
CREATE TABLE IF NOT EXISTS payment_method_token (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    paysafe_token VARCHAR(255) NOT NULL COMMENT 'Paysafe tokenized payment method',
    payment_method_type VARCHAR(50) NOT NULL COMMENT 'CARD, ACH, AGENT_SWEEP, MAIL',
    
    -- Display information only
    last_four VARCHAR(4) COMMENT 'Last 4 digits for display',
    expiration_month INT COMMENT 'Card expiration month',
    expiration_year INT COMMENT 'Card expiration year',
    account_holder_name VARCHAR(100) COMMENT 'Name on account',
    nickname VARCHAR(50) COMMENT 'Customer-defined nickname',
    
    -- Verification
    verification_status VARCHAR(50) DEFAULT 'PENDING',
    verified_date DATETIME,
    verification_amount DECIMAL(10,2) COMMENT 'Zero-dollar auth amount',
    
    -- Mail-in payment details
    check_number VARCHAR(50) COMMENT 'For mail-in payments',
    postmark_date DATE COMMENT 'Mail postmark date',
    
    is_default BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    status_id INT NOT NULL,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_payment_token_customer (customer_id),
    INDEX idx_payment_token_type (payment_method_type),
    CONSTRAINT fk_payment_token_customer 
        FOREIGN KEY (customer_id) 
        REFERENCES customer(id),
    CONSTRAINT fk_payment_token_status 
        FOREIGN KEY (status_id) 
        REFERENCES status(id),
    CONSTRAINT fk_payment_token_created 
        FOREIGN KEY (created_by) 
        REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Stores only payment tokens, no sensitive data';

-- Payment transaction linkage
CREATE TABLE IF NOT EXISTS payment_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL,
    payment_method_token_id INT NOT NULL,
    
    -- Payment details
    payment_amount DECIMAL(10,2) NOT NULL,
    payment_date DATETIME NOT NULL,
    paysafe_transaction_id VARCHAR(100) COMMENT 'Paysafe reference',
    
    -- Status tracking
    payment_status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    status_message TEXT,
    
    -- For batch processing (agent sweep)
    batch_id INT NULL,
    batch_date DATE NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_payment_trans (transaction_id),
    INDEX idx_payment_token (payment_method_token_id),
    INDEX idx_payment_status (payment_status),
    INDEX idx_payment_batch (batch_id),
    CONSTRAINT fk_payment_trans_transaction 
        FOREIGN KEY (transaction_id) 
        REFERENCES transaction(id),
    CONSTRAINT fk_payment_trans_token 
        FOREIGN KEY (payment_method_token_id) 
        REFERENCES payment_method_token(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Links payments to transactions';
```

### 6. Accounting Workflow Integration
```sql
-- Accounting batch processing
CREATE TABLE IF NOT EXISTS accounting_batch (
    id INT AUTO_INCREMENT PRIMARY KEY,
    batch_number VARCHAR(50) UNIQUE NOT NULL,
    batch_type VARCHAR(50) NOT NULL COMMENT 'DAILY, MONTHLY, MANUAL',
    batch_date DATE NOT NULL,
    fiscal_period VARCHAR(7) NOT NULL,
    
    -- Batch totals
    transaction_count INT DEFAULT 0,
    total_debits DECIMAL(12,2) DEFAULT 0,
    total_credits DECIMAL(12,2) DEFAULT 0,
    
    -- Status tracking
    batch_status VARCHAR(50) DEFAULT 'PENDING',
    validation_status VARCHAR(50),
    posting_status VARCHAR(50),
    
    -- Processing details
    created_by INT NOT NULL,
    reviewed_by INT,
    posted_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at DATETIME,
    posted_at DATETIME,
    
    -- Integration
    external_batch_ref VARCHAR(100) COMMENT 'External system reference',
    export_file_path VARCHAR(500) COMMENT 'Export file location',
    
    notes TEXT,
    
    INDEX idx_accounting_batch_date (batch_date),
    INDEX idx_accounting_batch_period (fiscal_period),
    INDEX idx_accounting_batch_status (batch_status),
    CONSTRAINT fk_accounting_batch_created 
        FOREIGN KEY (created_by) 
        REFERENCES user(id),
    CONSTRAINT fk_accounting_batch_reviewed 
        FOREIGN KEY (reviewed_by) 
        REFERENCES user(id),
    CONSTRAINT fk_accounting_batch_posted 
        FOREIGN KEY (posted_by) 
        REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tracks accounting batch processing';

-- Revenue recognition for insurance
CREATE TABLE IF NOT EXISTS premium_earning_schedule (
    id INT AUTO_INCREMENT PRIMARY KEY,
    policy_id INT NOT NULL,
    transaction_line_id INT NOT NULL,
    
    -- Schedule details
    coverage_start_date DATE NOT NULL,
    coverage_end_date DATE NOT NULL,
    total_days INT NOT NULL,
    premium_amount DECIMAL(10,2) NOT NULL,
    daily_rate DECIMAL(8,4) NOT NULL,
    
    -- Earning tracking
    earned_to_date DECIMAL(10,2) DEFAULT 0,
    unearned_amount DECIMAL(10,2) NOT NULL,
    last_earning_date DATE,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_earning_policy (policy_id),
    INDEX idx_earning_dates (coverage_start_date, coverage_end_date),
    INDEX idx_earning_active (is_active),
    CONSTRAINT fk_earning_policy 
        FOREIGN KEY (policy_id) 
        REFERENCES policy(id),
    CONSTRAINT fk_earning_line 
        FOREIGN KEY (transaction_line_id) 
        REFERENCES transaction_line(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tracks premium earning over coverage period';
```

### 7. Accounting Views and Reports
```sql
-- Trial Balance View
CREATE VIEW v_trial_balance AS
SELECT 
    coa.account_code,
    coa.account_name,
    at.name as account_type,
    coa.normal_balance,
    SUM(tl.debit_amount) as total_debits,
    SUM(tl.credit_amount) as total_credits,
    SUM(
        CASE 
            WHEN coa.normal_balance = 'DEBIT' 
            THEN IFNULL(tl.debit_amount, 0) - IFNULL(tl.credit_amount, 0)
            ELSE IFNULL(tl.credit_amount, 0) - IFNULL(tl.debit_amount, 0)
        END
    ) as balance,
    t.fiscal_period
FROM transaction t
JOIN transaction_line tl ON t.id = tl.transaction_id
JOIN chart_of_accounts coa ON tl.gl_account_code = coa.account_code
JOIN account_type at ON coa.account_type_id = at.id
WHERE t.is_posted = TRUE
GROUP BY coa.account_code, coa.account_name, at.name, coa.normal_balance, t.fiscal_period
ORDER BY coa.account_code;

-- Income Statement View
CREATE VIEW v_income_statement AS
SELECT 
    coa.account_code,
    coa.account_name,
    at.name as account_type,
    t.fiscal_period,
    SUM(
        CASE 
            WHEN at.code = 'REVENUE' THEN tl.credit_amount - tl.debit_amount
            WHEN at.code = 'EXPENSE' THEN tl.debit_amount - tl.credit_amount
            ELSE 0
        END
    ) as amount
FROM transaction t
JOIN transaction_line tl ON t.id = tl.transaction_id
JOIN chart_of_accounts coa ON tl.gl_account_code = coa.account_code
JOIN account_type at ON coa.account_type_id = at.id
WHERE t.is_posted = TRUE
AND at.financial_statement = 'INCOME_STATEMENT'
GROUP BY coa.account_code, coa.account_name, at.name, t.fiscal_period
ORDER BY at.display_order, coa.account_code;

-- Balance Sheet View
CREATE VIEW v_balance_sheet AS
SELECT 
    coa.account_code,
    coa.account_name,
    at.name as account_type,
    SUM(
        CASE 
            WHEN coa.normal_balance = 'DEBIT' 
            THEN IFNULL(tl.debit_amount, 0) - IFNULL(tl.credit_amount, 0)
            ELSE IFNULL(tl.credit_amount, 0) - IFNULL(tl.debit_amount, 0)
        END
    ) as balance,
    MAX(t.accounting_date) as as_of_date
FROM transaction t
JOIN transaction_line tl ON t.id = tl.transaction_id
JOIN chart_of_accounts coa ON tl.gl_account_code = coa.account_code
JOIN account_type at ON coa.account_type_id = at.id
WHERE t.is_posted = TRUE
AND at.financial_statement = 'BALANCE_SHEET'
GROUP BY coa.account_code, coa.account_name, at.name
ORDER BY at.display_order, coa.account_code;

-- Reinstatement Accounting Integration View
CREATE VIEW v_reinstatement_accounting AS
SELECT 
    t.id as transaction_id,
    t.policy_id,
    rc.reinstatement_effective_date,
    rc.lapse_days,
    rc.adjusted_total_premium,
    rc.unpaid_premium_balance,
    rc.reinstatement_fee,
    rc.total_amount_due,
    -- GL entries
    '1210' as debit_account, -- Premium Receivable
    rc.total_amount_due as debit_amount,
    '4110' as credit_account_premium, -- Written Premium
    rc.adjusted_total_premium as credit_amount_premium,
    '4210' as credit_account_fee, -- Policy Fees
    rc.reinstatement_fee as credit_amount_fee
FROM transaction t
JOIN reinstatement_calculation rc ON t.reinstatement_calculation_id = rc.id
WHERE t.transaction_type_id IN (
    SELECT id FROM transaction_type 
    WHERE code IN ('REINSTATEMENT_COMPLETED', 'PREMIUM_REINSTATEMENT')
);
```

### 8. Stored Procedures for Accounting
```sql
DELIMITER //

-- Create accounting entries for a transaction
CREATE PROCEDURE sp_create_accounting_entries(
    IN p_transaction_id INT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(500)
)
BEGIN
    DECLARE v_transaction_type_id INT;
    DECLARE v_total_amount DECIMAL(10,2);
    DECLARE v_debit_total DECIMAL(10,2) DEFAULT 0;
    DECLARE v_credit_total DECIMAL(10,2) DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_success = FALSE;
        SET p_message = 'Error creating accounting entries';
    END;
    
    START TRANSACTION;
    
    -- Get transaction details
    SELECT transaction_type_id INTO v_transaction_type_id
    FROM transaction 
    WHERE id = p_transaction_id;
    
    -- Create debit/credit entries based on GL mapping
    INSERT INTO transaction_line (
        transaction_id,
        gl_account_code,
        debit_amount,
        credit_amount,
        component_type,
        description,
        line_order
    )
    SELECT 
        p_transaction_id,
        CASE 
            WHEN entry_type = 'DEBIT' THEN glm.debit_account_code
            ELSE glm.credit_account_code
        END,
        CASE 
            WHEN entry_type = 'DEBIT' THEN tl.amount + IFNULL(tl.tax_amount, 0)
            ELSE 0
        END,
        CASE 
            WHEN entry_type = 'CREDIT' THEN tl.amount + IFNULL(tl.tax_amount, 0)
            ELSE 0
        END,
        tl.component_type,
        CONCAT(entry_type, ' - ', tlt.name),
        tl.line_order * 2 + CASE WHEN entry_type = 'DEBIT' THEN 0 ELSE 1 END
    FROM transaction_line tl
    JOIN transaction_line_type tlt ON tl.transaction_line_type_id = tlt.id
    JOIN gl_account_mapping glm ON (
        glm.transaction_type_id = v_transaction_type_id
        AND (glm.component_type = tl.component_type OR glm.component_type IS NULL)
    )
    CROSS JOIN (SELECT 'DEBIT' as entry_type UNION SELECT 'CREDIT') et
    WHERE tl.transaction_id = p_transaction_id
    AND tl.gl_account_code IS NULL; -- Don't duplicate if already has GL codes
    
    -- Validate balanced entries
    SELECT 
        SUM(debit_amount),
        SUM(credit_amount)
    INTO v_debit_total, v_credit_total
    FROM transaction_line
    WHERE transaction_id = p_transaction_id;
    
    IF v_debit_total != v_credit_total THEN
        ROLLBACK;
        SET p_success = FALSE;
        SET p_message = CONCAT('Entries not balanced. Debits: ', v_debit_total, ' Credits: ', v_credit_total);
    ELSE
        -- Update transaction
        UPDATE transaction 
        SET 
            accounting_date = IFNULL(accounting_date, CURDATE()),
            fiscal_period = DATE_FORMAT(IFNULL(accounting_date, CURDATE()), '%Y-%m')
        WHERE id = p_transaction_id;
        
        COMMIT;
        SET p_success = TRUE;
        SET p_message = 'Accounting entries created successfully';
    END IF;
END//

-- Post transactions to accounting
CREATE PROCEDURE sp_post_to_accounting(
    IN p_batch_id INT,
    IN p_user_id INT,
    OUT p_posted_count INT,
    OUT p_message VARCHAR(500)
)
BEGIN
    DECLARE v_batch_status VARCHAR(50);
    DECLARE v_transaction_count INT DEFAULT 0;
    
    -- Check batch status
    SELECT batch_status INTO v_batch_status
    FROM accounting_batch
    WHERE id = p_batch_id;
    
    IF v_batch_status != 'APPROVED' THEN
        SET p_posted_count = 0;
        SET p_message = 'Batch must be approved before posting';
        RETURN;
    END IF;
    
    -- Post transactions
    UPDATE transaction t
    JOIN accounting_batch_transaction abt ON t.id = abt.transaction_id
    SET 
        t.is_posted = TRUE,
        t.posted_date = NOW(),
        t.posting_user_id = p_user_id,
        t.posting_batch_id = p_batch_id
    WHERE abt.batch_id = p_batch_id
    AND t.is_posted = FALSE;
    
    SET v_transaction_count = ROW_COUNT();
    
    -- Update batch
    UPDATE accounting_batch
    SET 
        posting_status = 'POSTED',
        posted_by = p_user_id,
        posted_at = NOW()
    WHERE id = p_batch_id;
    
    SET p_posted_count = v_transaction_count;
    SET p_message = CONCAT('Posted ', v_transaction_count, ' transactions');
END//

DELIMITER ;
```

## Benefits of This Approach

1. **Complete Double-Entry Accounting**: Every transaction creates balanced entries
2. **Program-Centric Configuration**: Each insurance program can have unique rules
3. **Token-Based Security**: No sensitive payment data stored locally
4. **Full Audit Trail**: Complete transaction history with reversals
5. **Flexible GL Mapping**: Configuration-driven account assignments
6. **Revenue Recognition**: Proper premium earning over coverage periods
7. **Reinstatement Integration**: Seamless accounting for complex workflows

## Migration Path

1. **Phase 1**: Enhance transaction and transaction_line tables
2. **Phase 2**: Create chart of accounts and mapping tables
3. **Phase 3**: Set up payment token infrastructure
4. **Phase 4**: Create accounting batch processing
5. **Phase 5**: Implement stored procedures and views
6. **Phase 6**: Configure GL mappings and test posting

## Conclusion

This v3 approach provides a comprehensive accounting solution that integrates seamlessly with the existing transaction framework while supporting all requirements from the Accounting documentation. The solution maintains data security through tokenization, provides complete audit trails, and supports complex insurance accounting workflows including reinstatements.