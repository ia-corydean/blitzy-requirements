# Accounting System - Complete Schema Compilation

## Overview

This document compiles all tables and schemas from the individual accounting component approach files into a single reference. It provides a comprehensive view of the entire accounting infrastructure, identifies which tables are new versus modifications to existing tables, and clarifies the integration points between components.

## Table Summary

### Total Tables: 49

#### Core Accounting Tables (5)
1. **transaction** (MODIFY existing transactions table)
2. **transaction_line** (NEW)
3. **transaction_type** (NEW)
4. **account** (NEW)
5. **account_type** (NEW)

#### Payment Management Tables (7)
6. **payment** (MODIFY existing payments table)
7. **payment_type** (NEW)
8. **payment_method** (NEW)
9. **map_payment_type_method** (NEW)
10. **payment_gateway** (NEW)
11. **payment_gateway_type** (NEW)
12. **payment_gateway_token** (REPLACE bank_accounts and bank_cards tables)

#### Billing and Invoicing Tables (5)
13. **invoice** (NEW)
14. **invoice_line** (NEW)
15. **invoice_type** (NEW)
16. **payment_plan** (NEW)
17. **policy_payment_plan** (NEW)

#### Commission Management Tables (6)
18. **commission** (NEW)
19. **commission_type** (NEW)
20. **premium_calculation_basis** (NEW)
21. **commission_schedule** (NEW)
22. **commission_statement** (NEW)
23. **map_commission_statement** (NEW)

#### Fee and Adjustment Tables (5)
24. **fee_type** (NEW)
25. **fee_schedule** (NEW)
26. **adjustment_reason** (NEW)
27. **adjustment** (NEW)
28. **policy_fee** (NEW)

#### Check Management Tables (6)
29. **check** (NEW)
30. **check_type** (NEW)
31. **check_batch** (NEW)
32. **map_check_batch** (NEW)
33. **bank_account** (NEW)
34. **check_void_reason** (NEW)

## Detailed Schema Definitions

### A. Core Accounting Tables

#### 1. Transaction Table (MODIFY existing)
```sql
-- Migration from existing 'transactions' table
ALTER TABLE transactions RENAME TO transaction;

ALTER TABLE transaction
    ADD COLUMN transaction_number VARCHAR(50) UNIQUE NOT NULL AFTER id,
    ADD COLUMN transaction_type_id BIGINT UNSIGNED NOT NULL AFTER transaction_number,
    ADD COLUMN entity_id BIGINT UNSIGNED AFTER transaction_date,
    ADD COLUMN producer_id BIGINT UNSIGNED AFTER policy_id,
    ADD COLUMN total_amount DECIMAL(12,2) NOT NULL AFTER producer_id,
    ADD COLUMN is_reversed BOOLEAN DEFAULT FALSE AFTER total_amount,
    ADD COLUMN reversal_transaction_id BIGINT UNSIGNED NULL AFTER is_reversed,
    ADD COLUMN original_transaction_id BIGINT UNSIGNED NULL AFTER reversal_transaction_id,
    ADD COLUMN description TEXT AFTER original_transaction_id,
    ADD COLUMN metadata JSON AFTER description,
    ADD COLUMN status_id BIGINT UNSIGNED NOT NULL AFTER metadata,
    ADD COLUMN updated_by BIGINT UNSIGNED AFTER created_by,
    DROP COLUMN transaction_type, -- Replace with FK
    DROP COLUMN status, -- Replace with FK
    ADD FOREIGN KEY (transaction_type_id) REFERENCES transaction_type(id),
    ADD FOREIGN KEY (entity_id) REFERENCES entity(id),
    ADD FOREIGN KEY (reversal_transaction_id) REFERENCES transaction(id),
    ADD FOREIGN KEY (original_transaction_id) REFERENCES transaction(id),
    ADD FOREIGN KEY (status_id) REFERENCES status(id),
    ADD INDEX idx_transaction_date (transaction_date),
    ADD INDEX idx_entity (entity_id),
    ADD INDEX idx_policy (policy_id),
    ADD INDEX idx_status (status_id);
```

#### 2. Transaction Line Table (NEW)
```sql
CREATE TABLE transaction_line (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_id BIGINT UNSIGNED NOT NULL,
    account_id BIGINT UNSIGNED NOT NULL,
    line_number INT NOT NULL,
    
    -- Double-entry amounts
    debit_amount DECIMAL(12,2) DEFAULT 0,
    credit_amount DECIMAL(12,2) DEFAULT 0,
    
    -- Component classification
    line_type VARCHAR(50), -- PREMIUM, POLICY_FEE, MVCPA_FEE, SR22_FEE, COMMISSION, TAX
    line_description TEXT,
    
    -- Additional structured data
    line_metadata JSON, -- For tax details, fee breakdowns, jurisdiction info
    
    -- Standard audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (account_id) REFERENCES account(id),
    INDEX idx_transaction (transaction_id),
    INDEX idx_account (account_id),
    UNIQUE KEY uk_transaction_line (transaction_id, line_number),
    CONSTRAINT chk_single_amount CHECK (
        (debit_amount > 0 AND credit_amount = 0) OR 
        (debit_amount = 0 AND credit_amount > 0) OR
        (debit_amount = 0 AND credit_amount = 0)
    )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### 3. Transaction Type Table (NEW)
```sql
CREATE TABLE transaction_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_type_id BIGINT UNSIGNED, -- For hierarchical categorization
    
    -- Type properties
    requires_approval BOOLEAN DEFAULT FALSE,
    reversible BOOLEAN DEFAULT TRUE,
    
    -- Metadata validation schema
    metadata_schema JSON, -- JSON Schema for validating transaction.metadata
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (parent_type_id) REFERENCES transaction_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_parent (parent_type_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### 4. Account Table (NEW)
```sql
CREATE TABLE account (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    account_name VARCHAR(100) NOT NULL,
    account_type_id BIGINT UNSIGNED NOT NULL,
    parent_account_id BIGINT UNSIGNED,
    
    -- Properties moved from account_type per feedback
    normal_balance ENUM('DEBIT', 'CREDIT') NOT NULL,
    financial_statement VARCHAR(50), -- BALANCE_SHEET, INCOME_STATEMENT
    sort_order INT DEFAULT 0,
    
    -- Account configuration
    is_control_account BOOLEAN DEFAULT FALSE,
    requires_sub_account BOOLEAN DEFAULT FALSE,
    allow_manual_entry BOOLEAN DEFAULT TRUE,
    is_cash_account BOOLEAN DEFAULT FALSE,
    
    -- Insurance-specific properties
    is_trust_account BOOLEAN DEFAULT FALSE,
    is_premium_account BOOLEAN DEFAULT FALSE,
    is_claim_account BOOLEAN DEFAULT FALSE,
    
    -- Additional structured settings
    metadata JSON, -- For account-specific configurations
    
    -- Standard audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (account_type_id) REFERENCES account_type(id),
    FOREIGN KEY (parent_account_id) REFERENCES account(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_account_type (account_type_id),
    INDEX idx_parent (parent_account_id),
    INDEX idx_account_number (account_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### 5. Account Type Table (NEW)
```sql
CREATE TABLE account_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- ASSET, LIABILITY, REVENUE, EXPENSE, EQUITY
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Type properties
    debit_increases BOOLEAN NOT NULL, -- TRUE for Assets/Expenses, FALSE for Liabilities/Revenue/Equity
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### B. Payment Management Tables

#### 6. Payment Table (MODIFY existing)
```sql
-- Migration from existing 'payments' table
ALTER TABLE payments RENAME TO payment;

ALTER TABLE payment
    ADD COLUMN payment_number VARCHAR(50) UNIQUE NOT NULL AFTER id,
    ADD COLUMN payment_type_id BIGINT UNSIGNED NOT NULL AFTER payment_number,
    ADD COLUMN payment_method_id BIGINT UNSIGNED NOT NULL AFTER payment_type_id,
    ADD COLUMN transaction_id BIGINT UNSIGNED AFTER payment_method_id,
    ADD COLUMN payment_date DATETIME NOT NULL AFTER amount,
    ADD COLUMN payment_gateway_id BIGINT UNSIGNED AFTER payment_date,
    ADD COLUMN gateway_transaction_id VARCHAR(255) AFTER payment_gateway_id,
    ADD COLUMN status_id BIGINT UNSIGNED NOT NULL AFTER gateway_transaction_id,
    ADD COLUMN processed_at DATETIME AFTER status_id,
    ADD COLUMN retry_count INT DEFAULT 0 AFTER processed_at,
    ADD COLUMN last_retry_at DATETIME AFTER retry_count,
    ADD COLUMN next_retry_at DATETIME AFTER last_retry_at,
    ADD COLUMN communication_id BIGINT UNSIGNED AFTER next_retry_at,
    ADD COLUMN updated_by BIGINT UNSIGNED AFTER created_by,
    DROP COLUMN payment_method, -- Replace with FK
    DROP COLUMN status, -- Replace with FK
    ADD FOREIGN KEY (payment_type_id) REFERENCES payment_type(id),
    ADD FOREIGN KEY (payment_method_id) REFERENCES payment_method(id),
    ADD FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    ADD FOREIGN KEY (payment_gateway_id) REFERENCES payment_gateway(id),
    ADD FOREIGN KEY (communication_id) REFERENCES communication(id),
    ADD FOREIGN KEY (status_id) REFERENCES status(id),
    ADD INDEX idx_status (status_id),
    ADD INDEX idx_retry (status_id, next_retry_at),
    ADD INDEX idx_transaction (transaction_id),
    ADD INDEX idx_payment_date (payment_date);
```

#### 7. Payment Type Table (NEW)
```sql
CREATE TABLE payment_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- PREMIUM_PAYMENT, REFUND, COMMISSION_PAYOUT
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Type configuration
    requires_approval BOOLEAN DEFAULT FALSE,
    allow_partial BOOLEAN DEFAULT FALSE,
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### 8. Payment Method Table (NEW)
```sql
CREATE TABLE payment_method (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- CARD, ACH, CHECK, SWEEP, CASH
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Method properties
    requires_gateway BOOLEAN DEFAULT TRUE,
    processing_days INT DEFAULT 1,
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### 9. Map Payment Type Method Table (NEW)
```sql
-- This table defines which payment methods are allowed for each payment type
CREATE TABLE map_payment_type_method (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    payment_type_id BIGINT UNSIGNED NOT NULL,
    payment_method_id BIGINT UNSIGNED NOT NULL,
    
    -- Relationship properties
    is_default BOOLEAN DEFAULT FALSE,
    sort_order INT DEFAULT 0,
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (payment_type_id) REFERENCES payment_type(id),
    FOREIGN KEY (payment_method_id) REFERENCES payment_method(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    UNIQUE KEY uk_type_method (payment_type_id, payment_method_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### 10. Payment Gateway Table (NEW)
```sql
CREATE TABLE payment_gateway (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    payment_gateway_type_id BIGINT UNSIGNED NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL, -- PAYSAFE, STRIPE, AUTHORIZE_NET
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Gateway properties
    is_tokenized BOOLEAN DEFAULT TRUE,
    requires_pci BOOLEAN DEFAULT TRUE,
    
    -- Gateway capabilities
    supported_methods JSON, -- ["CARD", "ACH"]
    supported_currencies JSON, -- ["USD", "CAD"]
    
    -- Configuration reference
    configuration_id BIGINT UNSIGNED, -- References configuration table
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (payment_gateway_type_id) REFERENCES payment_gateway_type(id),
    FOREIGN KEY (configuration_id) REFERENCES configuration(id),
    FOREIGN KEY (status_id) REFERENCES status(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### 11. Payment Gateway Type Table (NEW)
```sql
CREATE TABLE payment_gateway_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- MANUAL, EXTERNAL
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### 12. Payment Gateway Token Table (REPLACE existing)
```sql
-- This table replaces bank_accounts and bank_cards tables
-- Migration steps:
-- 1. Create new payment_gateway_token table
-- 2. Migrate data from bank_accounts and bank_cards
-- 3. Update foreign keys in dependent tables
-- 4. Drop old tables

CREATE TABLE payment_gateway_token (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    payment_gateway_id BIGINT UNSIGNED NOT NULL,
    entity_id BIGINT UNSIGNED NOT NULL, -- References entity table
    
    -- Token details
    token VARCHAR(255) NOT NULL,
    token_type VARCHAR(50), -- CARD, BANK_ACCOUNT
    last_four VARCHAR(4),
    expiration_date DATE,
    
    -- Token metadata (structured)
    token_metadata JSON, -- Card brand, bank name, etc.
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (payment_gateway_id) REFERENCES payment_gateway(id),
    FOREIGN KEY (entity_id) REFERENCES entity(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_entity (entity_id),
    INDEX idx_token (token)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Migration from existing tables
-- INSERT INTO payment_gateway_token (entity_id, token, token_type, last_four, ...)
-- SELECT entity_id, account_token, 'BANK_ACCOUNT', RIGHT(account_number, 4), ...
-- FROM bank_accounts;
```

### C. Billing and Invoicing Tables

[Tables 13-17 continue with the same detailed format...]

### D. Commission Management Tables

[Tables 18-23 continue with the same detailed format...]

### E. Fee and Adjustment Tables

[Tables 24-28 continue with the same detailed format...]

### F. Check Management Tables

[Tables 29-34 continue with the same detailed format...]

## Migration Strategy

### Phase 1: Foundation Tables
1. Create all reference/type tables first (no dependencies)
2. Create account and account_type tables
3. Modify existing transaction table
4. Create transaction_line and transaction_type

### Phase 2: Payment Infrastructure
1. Create payment reference tables
2. Modify existing payment table
3. Create payment_gateway_token (migrate from bank_accounts/bank_cards)
4. Update all payment references

### Phase 3: Business Components
1. Create billing/invoicing tables
2. Create commission management tables
3. Create fee/adjustment tables
4. Create check management tables

### Phase 4: Data Migration
1. Migrate historical transactions to new structure
2. Create transaction_line entries for existing transactions
3. Update all foreign key relationships
4. Validate data integrity

### Phase 5: Cleanup
1. Drop deprecated columns
2. Archive old tables
3. Update all application code
4. Final validation

## Integration Summary

### Key Integration Points

1. **Entity Table (GR-52)**
   - Used by: transaction, payment_gateway_token, adjustment, bank_account
   - Provides universal entity management

2. **Configuration Table**
   - Used by: payment_gateway, fee schedules, commission rates
   - Provides flexible configuration storage

3. **Communication Table (GR-44)**
   - Used by: payment (for gateway responses)
   - Tracks all external API communications

4. **Status Table**
   - Used by: ALL tables for status management
   - Provides consistent status tracking

5. **Policy Table**
   - Referenced by: transaction, commission, invoice, adjustment
   - Links accounting to policy lifecycle

## Summary Statistics

- **New Tables**: 42
- **Modified Tables**: 2 (transaction, payment)
- **Replaced Tables**: 2 (bank_accounts, bank_cards)
- **Total Final Tables**: 49
- **Estimated Migration Effort**: 80-120 hours
- **Risk Level**: Medium (due to financial data sensitivity)