# Accounting Schema - Final Refinement

## Executive Summary

This document presents the final refined accounting schema based on all feedback received. The design removes redundant tables, leverages existing system patterns (particularly the entity table from GR-52), and maintains a clean, maintainable structure. The schema has been reduced to approximately 22 tables while maintaining full functionality.

### Key Refinements
- Removed commission_hierarchy table (commissions only go to producer of record)
- Leverages existing entity table pattern for external entities
- Moved all gateway configuration to the configuration table
- Simplified payment_gateway_type to just MANUAL or EXTERNAL
- Clarified the purpose of mapping tables

## Core Accounting Tables

### 1. Transaction Table
```sql
CREATE TABLE transaction (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_number VARCHAR(50) UNIQUE NOT NULL,
    transaction_type_id BIGINT UNSIGNED NOT NULL,
    transaction_date DATETIME NOT NULL,
    
    -- Business context
    -- Note: entity_type is defined in the entity table per GR-52
    entity_id BIGINT UNSIGNED, -- References entity table
    policy_id BIGINT UNSIGNED,
    producer_id BIGINT UNSIGNED,
    
    -- Financial summary
    total_amount DECIMAL(12,2) NOT NULL,
    
    -- Reversal support
    is_reversed BOOLEAN DEFAULT FALSE,
    reversal_transaction_id BIGINT UNSIGNED NULL,
    original_transaction_id BIGINT UNSIGNED NULL,
    
    -- Structured metadata with defined schema
    description TEXT,
    metadata JSON, -- Validated against transaction_type.metadata_schema
    
    -- Standard audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes and constraints
    INDEX idx_transaction_date (transaction_date),
    INDEX idx_entity (entity_id),
    INDEX idx_policy (policy_id),
    INDEX idx_status (status_id),
    FOREIGN KEY (transaction_type_id) REFERENCES transaction_type(id),
    FOREIGN KEY (entity_id) REFERENCES entity(id),
    FOREIGN KEY (reversal_transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (original_transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```

### 2. Transaction Line Table
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
    line_type VARCHAR(50), -- PREMIUM, POLICY_FEE, COMMISSION, TAX
    line_description TEXT,
    
    -- Additional structured data
    line_metadata JSON, -- For tax details, fee breakdowns, etc.
    
    -- Standard audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (account_id) REFERENCES account(id),
    INDEX idx_transaction (transaction_id),
    INDEX idx_account (account_id),
    UNIQUE KEY uk_transaction_line (transaction_id, line_number)
);
```

### 3. Transaction Type Table
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
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```

### 4. Account Table
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
    metadata JSON, -- For account-specific settings
    
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
    INDEX idx_parent (parent_account_id)
);
```

### 5. Account Type Table
```sql
CREATE TABLE account_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- ASSET, LIABILITY, REVENUE, EXPENSE, EQUITY
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```

## Payment Management Tables

### 6. Payment Table
```sql
CREATE TABLE payment (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    payment_number VARCHAR(50) UNIQUE NOT NULL,
    payment_type_id BIGINT UNSIGNED NOT NULL,
    payment_method_id BIGINT UNSIGNED NOT NULL,
    transaction_id BIGINT UNSIGNED,
    
    -- Payment details
    amount DECIMAL(12,2) NOT NULL,
    payment_date DATETIME NOT NULL,
    
    -- Gateway relationship
    payment_gateway_id BIGINT UNSIGNED,
    gateway_transaction_id VARCHAR(255), -- External reference
    
    -- Processing status
    status_id BIGINT UNSIGNED NOT NULL,
    processed_at DATETIME,
    
    -- Retry logic
    retry_count INT DEFAULT 0,
    last_retry_at DATETIME,
    next_retry_at DATETIME,
    
    -- Communication reference for gateway responses
    communication_id BIGINT UNSIGNED, -- References communication table for API logs
    
    -- Standard audit fields
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (payment_type_id) REFERENCES payment_type(id),
    FOREIGN KEY (payment_method_id) REFERENCES payment_method(id),
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (payment_gateway_id) REFERENCES payment_gateway(id),
    FOREIGN KEY (communication_id) REFERENCES communication(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_status (status_id),
    INDEX idx_retry (status_id, next_retry_at),
    INDEX idx_transaction (transaction_id),
    INDEX idx_payment_date (payment_date)
);
```

### 7. Payment Type Table
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
);
```

### 8. Payment Method Table
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
);
```

### 9. Map Payment Type Method Table
```sql
-- This table defines which payment methods are allowed for each payment type
-- It's different from the payment table which records actual payments
-- Example: REFUND payment type might only allow CHECK and ACH methods
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
);
```

### 10. Payment Gateway Table
```sql
CREATE TABLE payment_gateway (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    payment_gateway_type_id BIGINT UNSIGNED NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL, -- PAYSAFE, STRIPE, AUTHORIZE_NET
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Gateway properties (moved from type table)
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
);
```

### 11. Payment Gateway Type Table (Simplified)
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
);
```

### 12. Payment Gateway Token Table
```sql
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
);
```

## Check Management Tables

### 13. Check Table
```sql
CREATE TABLE check (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    check_type_id BIGINT UNSIGNED NOT NULL,
    payment_id BIGINT UNSIGNED,
    
    -- Check details
    check_number VARCHAR(50) NOT NULL,
    check_date DATE NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    
    -- Parties
    payee_name VARCHAR(255) NOT NULL,
    payee_address JSON, -- Structured address
    payer_name VARCHAR(255),
    payer_bank VARCHAR(255),
    
    -- Check status
    status_id BIGINT UNSIGNED NOT NULL,
    issued_date DATE,
    cleared_date DATE,
    void_date DATE,
    void_reason TEXT,
    
    -- Physical check details
    postmarked_date DATE, -- For mailed-in checks
    deposited_date DATE,
    
    -- MICR and printing details (structured JSON)
    micr_data JSON, -- Routing, account, check number
    printing_data JSON, -- Signature lines, watermarks, etc.
    
    -- Standard audit fields
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (check_type_id) REFERENCES check_type(id),
    FOREIGN KEY (payment_id) REFERENCES payment(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_check_number (check_number),
    INDEX idx_check_date (check_date),
    INDEX idx_status (status_id)
);
```

### 14. Check Type Table
```sql
CREATE TABLE check_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- REFUND, COMMISSION, CLAIM, MANUAL
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Type configuration (thresholds in configuration table)
    requires_approval BOOLEAN DEFAULT FALSE,
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```

## Commission Management Tables (Simplified)

### 15. Commission Table
```sql
CREATE TABLE commission (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_id BIGINT UNSIGNED NOT NULL,
    commission_type_id BIGINT UNSIGNED NOT NULL,
    
    -- Commission details (only producer of record)
    producer_id BIGINT UNSIGNED NOT NULL,
    policy_id BIGINT UNSIGNED,
    
    -- Calculation details
    base_amount DECIMAL(12,2) NOT NULL,
    commission_rate DECIMAL(5,4) NOT NULL,
    calculated_amount DECIMAL(12,2) NOT NULL,
    
    -- Calculation basis reference
    premium_calculation_basis_id BIGINT UNSIGNED NOT NULL,
    
    -- Timing
    earned_date DATE,
    paid_date DATE,
    payment_id BIGINT UNSIGNED, -- References payment when paid
    
    -- Standard audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (commission_type_id) REFERENCES commission_type(id),
    FOREIGN KEY (premium_calculation_basis_id) REFERENCES premium_calculation_basis(id),
    FOREIGN KEY (payment_id) REFERENCES payment(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_producer (producer_id),
    INDEX idx_policy (policy_id),
    INDEX idx_earned_date (earned_date)
);
```

### 16. Commission Type Table
```sql
CREATE TABLE commission_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- NEW_BUSINESS, RENEWAL, BONUS
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Type configuration
    clawback_days INT DEFAULT 90,
    requires_approval BOOLEAN DEFAULT FALSE,
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```

### 17. Premium Calculation Basis Table
```sql
CREATE TABLE premium_calculation_basis (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- WRITTEN, EARNED, COLLECTED
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Calculation properties
    calculation_method VARCHAR(50), -- IMMEDIATE, PRORATED, DEFERRED
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```

## Billing Management Tables

### 18. Invoice Table
```sql
CREATE TABLE invoice (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    invoice_type_id BIGINT UNSIGNED NOT NULL,
    policy_id BIGINT UNSIGNED NOT NULL,
    
    -- Installment tracking
    installment_number INT NOT NULL,
    total_installments INT NOT NULL,
    
    -- Financial details
    due_date DATE NOT NULL,
    amount_due DECIMAL(12,2) NOT NULL,
    amount_paid DECIMAL(12,2) DEFAULT 0,
    balance DECIMAL(12,2) NOT NULL,
    
    -- Payment tracking
    paid_date DATE,
    payment_id BIGINT UNSIGNED,
    
    -- Standard audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (invoice_type_id) REFERENCES invoice_type(id),
    FOREIGN KEY (payment_id) REFERENCES payment(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_policy_installment (policy_id, installment_number),
    INDEX idx_due_date (due_date),
    INDEX idx_status (status_id)
);
```

### 19. Invoice Line Table
```sql
CREATE TABLE invoice_line (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    invoice_id BIGINT UNSIGNED NOT NULL,
    line_number INT NOT NULL,
    
    -- Line details
    fee_type_id BIGINT UNSIGNED NOT NULL,
    description TEXT,
    amount DECIMAL(12,2) NOT NULL,
    
    -- Tax information
    is_taxable BOOLEAN DEFAULT FALSE,
    tax_amount DECIMAL(12,2) DEFAULT 0,
    
    -- Standard fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (invoice_id) REFERENCES invoice(id),
    FOREIGN KEY (fee_type_id) REFERENCES fee_type(id),
    UNIQUE KEY uk_invoice_line (invoice_id, line_number)
);
```

### 20. Invoice Type Table
```sql
CREATE TABLE invoice_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- INITIAL, INSTALLMENT, ENDORSEMENT, REINSTATEMENT
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Type configuration
    generates_notice BOOLEAN DEFAULT TRUE,
    notice_days_before INT DEFAULT 20,
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```

## Fee and Adjustment Tables

### 21. Fee Type Table
```sql
CREATE TABLE fee_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- POLICY_FEE, INSTALLMENT_FEE, NSF_FEE, SR22_FEE
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Fee properties
    fee_category VARCHAR(50), -- POLICY, TRANSACTION, PENALTY
    is_waivable BOOLEAN DEFAULT FALSE,
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```

### 22. Adjustment Reason Table
```sql
CREATE TABLE adjustment_reason (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- PREMIUM_CORRECTION, FEE_WAIVER, REFUND
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Reason properties
    requires_approval BOOLEAN DEFAULT FALSE,
    requires_documentation BOOLEAN DEFAULT FALSE,
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```

## Configuration Integration

### Gateway Configuration in Configuration Table
```json
{
  "configuration_type": "PAYMENT_GATEWAY",
  "scope_type": "entity",
  "entity_id": 123, -- payment_gateway.id
  "config_data": {
    "endpoints": {
      "sandbox": "https://sandbox.paysafe.com/api/v1",
      "production": "https://api.paysafe.com/api/v1"
    },
    "credentials": {
      "vault_path": "/secret/payment/paysafe/prod"
    },
    "timeout_settings": {
      "connect_timeout": 5000,
      "read_timeout": 30000
    },
    "retry_policy": {
      "max_retries": 3,
      "backoff_multiplier": 2
    },
    "features": {
      "supports_3ds": true,
      "supports_recurring": true,
      "supports_refunds": true
    }
  }
}
```

### Program Accounting Configuration
```json
{
  "configuration_type": "PROGRAM_ACCOUNTING",
  "scope_type": "program",
  "program_id": 123,
  "config_data": {
    "fees": {
      "POLICY_FEE": 50.00,
      "MVCPA_FEE_PER_VEHICLE": 0.50,
      "INSTALLMENT_FEE": 5.00,
      "NSF_FEE": 15.00,
      "REINSTATEMENT_FEE": 25.00,
      "SR22_FEE": 25.00
    },
    "payment_limits": {
      "max_payment_amount": 10000.00,
      "min_payment_amount": 1.00
    },
    "approval_thresholds": {
      "adjustment_approval": 500.00,
      "refund_approval": 1000.00,
      "commission_approval": 5000.00,
      "check_approval": {
        "REFUND": 1000.00,
        "COMMISSION": 5000.00
      }
    },
    "commission_rates": {
      "new_business_default": 0.15,
      "renewal_default": 0.10
    },
    "grace_period_days": 11
  }
}
```

## Clarifications and Design Decisions

### 1. Entity Table Usage
The transaction table references the existing `entity` table from GR-52 instead of storing entity_type directly. This maintains consistency with the universal entity management pattern.

### 2. Map Payment Type Method Purpose
This mapping table serves a different purpose than the payment table:
- **map_payment_type_method**: Defines business rules (which methods are allowed for each payment type)
- **payment table**: Records actual payment transactions
- Example: REFUND payment type might only allow CHECK and ACH methods, not CARD

### 3. Gateway Configuration
All gateway-specific configuration (endpoints, credentials, timeouts) is stored in the existing `configuration` table, not in the payment_gateway table. This follows the established pattern for configuration management.

### 4. Simplified Gateway Types
Per feedback, payment_gateway_type now only has two values:
- **MANUAL**: For manual/offline payment processing
- **EXTERNAL**: For all third-party gateway integrations

Specific gateway names (PAYSAFE, STRIPE, etc.) are stored in the payment_gateway table itself.

### 5. Commission Simplification
Commission hierarchy table has been removed since commissions only go to the producer of record. Any future override or split requirements can be handled through configuration or additional commission records.

### 6. Gateway Properties
Properties like `is_tokenized` and `requires_pci` have been moved to the payment_gateway table itself, as these are gateway-specific, not type-specific.

## Benefits of Final Design

### 1. Cleaner Structure
- ~22 tables instead of 40+ from v10
- No redundant tables
- Clear purpose for each table

### 2. Consistency
- Uses existing entity table pattern
- Leverages configuration table for settings
- Maintains standard audit fields throughout

### 3. Flexibility
- Strategic JSON usage for truly variable data
- Configuration-driven behavior
- Easy to extend without schema changes

### 4. Maintainability
- Human-intuitive organization
- Clear relationships
- Minimal complexity

## Summary

This final refinement achieves the goal of a simplified yet comprehensive accounting schema. By removing redundant tables (commission_hierarchy), leveraging existing patterns (entity table, configuration table), and clarifying the purpose of each component, we have a clean, maintainable design that supports all accounting requirements while being intuitive for human maintainers.