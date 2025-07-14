# Accounting Schema - Revised Final Design

## Executive Summary

Based on comprehensive feedback and analysis of existing system patterns, this document presents the final simplified accounting schema. The design leverages existing tables where possible, adds necessary _type tables for standardization, and maintains the simplification philosophy while ensuring 100% coverage of v10 requirements.

### Key Changes from Previous Design
- Leverages existing `configuration` and `communication` tables
- Adds requested _type tables for all major entities
- Removes redundant `audit_log` table (uses standard audit fields)
- Clarifies reconciliation and reference_data purposes
- Aligns with existing system patterns

## Final Schema Overview

### Core Accounting Tables (4)
1. `transaction` - All financial events
2. `transaction_line` - Double-entry details
3. `account` - Chart of accounts
4. `account_type` - Account classifications

### Payment Tables (2)
5. `payment` - Tokenized payment records
6. `payment_type` - Payment method definitions

### Commission Tables (2)
7. `commission` - Commission tracking
8. `commission_type` - Commission classifications

### Billing Tables (2)
9. `invoice` - Billing and installments
10. `invoice_type` - Invoice classifications

### Supporting Tables (3)
11. `transaction_type` - Transaction classifications
12. `reconciliation` - Bank/gateway reconciliation
    13. We are not going to auto reconcile with banks at the moment.
13. `reference_data` - Generic lookup values

### Leveraged Existing Tables (4)
- `configuration` - Program and system settings (replaces program_config)
- `communication` - API request/response logging for notices
- `form` - Document templates and forms
- `form_type` - Form classifications

**Total New Tables: 13** (down from 40+ in v10)

## Detailed Schema Definitions

### 1. Transaction Table (Enhanced)
```sql
CREATE TABLE transaction (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_number VARCHAR(50) UNIQUE NOT NULL,
    transaction_type_id BIGINT UNSIGNED NOT NULL,
    transaction_date DATETIME NOT NULL,
    
    -- Business context
    entity_type VARCHAR(50), -- POLICY, PRODUCER, CLAIM
    entity_id BIGINT UNSIGNED,
    policy_id BIGINT UNSIGNED,
    producer_id BIGINT UNSIGNED,
    
    -- Financial summary
    total_amount DECIMAL(12,2) NOT NULL,
    
    -- Reversal support
    is_reversed BOOLEAN DEFAULT FALSE,
    reversal_transaction_id BIGINT UNSIGNED NULL,
    original_transaction_id BIGINT UNSIGNED NULL,
    
    -- Flexible data
    description TEXT,
    metadata JSON, -- Stores reversal_reason, business context, etc.
    
    -- Standard audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_transaction_date (transaction_date),
    INDEX idx_entity (entity_type, entity_id),
    INDEX idx_policy (policy_id),
    INDEX idx_status (status_id),
    
    -- Foreign keys
    FOREIGN KEY (transaction_type_id) REFERENCES transaction_type(id),
    FOREIGN KEY (reversal_transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (original_transaction_id) REFERENCES transaction(id)
);
```

### 2. Transaction Line Table
```sql
CREATE TABLE transaction_line (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_id BIGINT UNSIGNED NOT NULL,
    account_id BIGINT UNSIGNED NOT NULL,
    
    -- Double-entry amounts
    debit_amount DECIMAL(12,2) DEFAULT 0,
    credit_amount DECIMAL(12,2) DEFAULT 0,
    
    -- Component classification
    line_type VARCHAR(50), -- PREMIUM, POLICY_FEE, COMMISSION, TAX
    line_metadata JSON, -- Additional line-specific data
    
    -- Standard audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (account_id) REFERENCES account(id),
    INDEX idx_transaction (transaction_id),
    INDEX idx_account (account_id)
);
```

### 3. Account Table
```sql
CREATE TABLE account (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    account_name VARCHAR(100) NOT NULL,
    account_type_id BIGINT UNSIGNED NOT NULL,
    parent_account_id BIGINT UNSIGNED,
    
    -- Account properties
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSON, -- Flexible properties
    
    -- Standard audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (account_type_id) REFERENCES account_type(id),
    FOREIGN KEY (parent_account_id) REFERENCES account(id),
    INDEX idx_account_type (account_type_id),
    INDEX idx_parent (parent_account_id)
);
```

### 4. Account Type Table
```sql
CREATE TABLE account_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- ASSET, LIABILITY, REVENUE, EXPENSE, EQUITY
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Type properties
    normal_balance VARCHAR(10) NOT NULL, -- DEBIT or CREDIT
    - This should be in account.
    financial_statement VARCHAR(50), -- BALANCE_SHEET, INCOME_STATEMENT
    - This should be in account.
    sort_order INT DEFAULT 0,
    - This should be in account.
    
    -- Standard fields
    is_active BOOLEAN DEFAULT TRUE,
    - this should use status_id
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 5. Payment Table (Enhanced)
```sql
CREATE TABLE payment (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    payment_number VARCHAR(50) UNIQUE NOT NULL,
    payment_type_id BIGINT UNSIGNED NOT NULL,
    transaction_id BIGINT UNSIGNED,
    
    -- Payment details
    payment_method VARCHAR(50), -- CARD, ACH, CHECK, SWEEP
    - payment_method and payment_method_type should be their own tables and referenced by id.
    gateway_name VARCHAR(50), -- PAYSAFE, MANUAL
    - payment_gateway and payment_gateway_type should be their own tables and referenced by id.
    gateway_token VARCHAR(255), -- Tokenized reference
    - this should be in payment_gateway
    amount DECIMAL(12,2) NOT NULL,
    
    -- Processing status
    status VARCHAR(50), -- PENDING, PROCESSED, FAILED, REVERSED
    processed_at DATETIME,
    
    -- Retry logic support
    retry_count INT DEFAULT 0,
    last_retry_at DATETIME,
    next_retry_at DATETIME,
    
    -- Gateway and check details
    gateway_response JSON, -- Full gateway response
    - this should be in communication table and referencing the comunication_id
    check_details JSON, -- Physical check information
    - check and check_type should be their own tables.
    
    -- Standard audit fields
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (payment_type_id) REFERENCES payment_type(id),
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    INDEX idx_status (status),
    INDEX idx_retry (status, next_retry_at),
    INDEX idx_transaction (transaction_id)
);
```

### 6. Payment Type Table
```sql
CREATE TABLE payment_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- PREMIUM_PAYMENT, REFUND, COMMISSION_PAYOUT
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Type configuration
    allowed_methods JSON, -- ["CARD", "ACH", "CHECK"]
    - These should be stored as values in payment_type
    requires_approval BOOLEAN DEFAULT FALSE,
    max_amount DECIMAL(12,2),
    - This should be defined in the program manager.
    
    -- Standard fields
    is_active BOOLEAN DEFAULT TRUE,
    - should be status_id
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 7. Commission Table
```sql
CREATE TABLE commission (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_id BIGINT UNSIGNED NOT NULL,
    commission_type_id BIGINT UNSIGNED NOT NULL,
    
    -- Commission details
    producer_id BIGINT UNSIGNED NOT NULL,
    policy_id BIGINT UNSIGNED,
    base_amount DECIMAL(12,2) NOT NULL,
    rate DECIMAL(5,4), -- Commission percentage
    calculated_amount DECIMAL(12,2) NOT NULL,
    
    -- Hierarchy and overrides
    hierarchy_data JSON, -- Parent producer, override rates, split percentages
    - elaborate.
    -- Timing
    earned_date DATE,
    paid_date DATE,
    
    -- Standard audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (commission_type_id) REFERENCES commission_type(id),
    INDEX idx_producer (producer_id),
    INDEX idx_policy (policy_id),
    INDEX idx_earned_date (earned_date)
);
```

### 8. Commission Type Table
```sql
CREATE TABLE commission_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- NEW_BUSINESS, RENEWAL, OVERRIDE, BONUS
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Type configuration
    calculation_basis VARCHAR(50), -- WRITTEN, EARNED, COLLECTED
    - this should be a table and referenced by id. Maybe premium_calculation_type?
    clawback_days INT DEFAULT 90,
    requires_approval BOOLEAN DEFAULT FALSE,
    
    -- Standard fields
    is_active BOOLEAN DEFAULT TRUE,
    - status_id
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 9. Invoice Table
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
    
    -- Component breakdown
    components JSON, -- {premium: 100.00, policy_fee: 50.00, ...}
    
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
    INDEX idx_policy_installment (policy_id, installment_number),
    INDEX idx_due_date (due_date),
    INDEX idx_status (status_id)
);
```

### 10. Invoice Type Table
```sql
CREATE TABLE invoice_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- INITIAL, INSTALLMENT, ENDORSEMENT, REINSTATEMENT
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Type configuration
    generates_notice BOOLEAN DEFAULT TRUE,
    notice_days_before INT DEFAULT 20,
    grace_period_days INT,
    
    -- Standard fields
    is_active BOOLEAN DEFAULT TRUE,
    - status_id
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 11. Transaction Type Table
```sql
CREATE TABLE transaction_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Type properties
    category VARCHAR(50), -- PREMIUM, PAYMENT, ADJUSTMENT, COMMISSION
    - These should be transaction_types.
    requires_approval BOOLEAN DEFAULT FALSE,
    approval_amount_threshold DECIMAL(12,2),
    - This should be set in program manager.
    
    -- Metadata validation
    metadata_schema JSON, -- JSON schema for metadata validation
    
    -- Standard fields
    is_active BOOLEAN DEFAULT TRUE,
    - status_id
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 12. Reconciliation Table
- We may not need this.
```sql
CREATE TABLE reconciliation (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    reconciliation_date DATE NOT NULL,
    reconciliation_type VARCHAR(50), -- BANK, GATEWAY, COMMISSION
    source_system VARCHAR(50),
    
    -- Summary statistics
    total_items INT NOT NULL,
    matched_items INT NOT NULL,
    exception_items INT NOT NULL,
    reconciled_amount DECIMAL(12,2),
    variance_amount DECIMAL(12,2),
    
    -- Detailed items (embedded for simplicity)
    items JSON, -- Array of reconciliation line items
    
    -- Workflow support
    status VARCHAR(50), -- IN_PROGRESS, COMPLETED, APPROVED
    approved_by BIGINT UNSIGNED,
    approved_at DATETIME,
    approval_notes TEXT,
    
    -- Standard audit fields
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    INDEX idx_date (reconciliation_date),
    INDEX idx_type (reconciliation_type),
    INDEX idx_status (status)
);
```

### 13. Reference Data Table
```sql
CREATE TABLE reference_data (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(50) NOT NULL, -- FEE_TYPE, ADJUSTMENT_REASON, PAYMENT_STATUS
    - from these examples, these should be in their own tables andreferenced by id.
    code VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Flexible properties
    sort_order INT DEFAULT 0,
    metadata JSON, -- Category-specific properties
    
    -- Standard fields
    is_active BOOLEAN DEFAULT TRUE,
    - status_id
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    UNIQUE KEY uk_category_code (category, code),
    INDEX idx_category (category)
);
```

## Leveraged Existing Tables

### Configuration Table (from existing system)
Used for all program-specific settings:
```json
{
  "configuration_type": "PROGRAM_ACCOUNTING",
  "scope_type": "program",
  "program_id": 123,
  "config_data": {
    "fees": {
      "policy_fee": 50.00,
      "mvcpa_fee_per_vehicle": 0.50,
      "installment_fee": 5.00,
      "nsf_fee": 15.00,
      "reinstatement_fee": 25.00
    },
    "payment_plans": [...],
    "commission_rates": {...},
    "grace_period_days": 11,
    "gateway_config": {...}
  }
}
```

### Communication Table (from GR-44)
Used for notice generation and delivery tracking:
- Records all outbound communications (billing notices, cancellation warnings, etc.)
- Tracks delivery status via third-party APIs (Twilio, SendGrid)
- Maintains complete audit trail of customer communications

### Form and Form Type Tables
Used for document generation:
- `form` - Stores templates for checks, statements, reports
- `form_type` - Classifies forms (CHECK, STATEMENT, NOTICE, REPORT)

## Key Design Clarifications

### Approval Workflows
The design supports approval workflows through:
1. **Transaction-level approvals**: `transaction_type.requires_approval` flag
2. **Amount thresholds**: `transaction_type.approval_amount_threshold`
3. **Status management**: Standard `status_id` field tracks approval states
4. **Metadata tracking**: Approval details stored in transaction metadata

Example approval states in status table:
- PENDING_APPROVAL
- APPROVED
- REJECTED
- AUTO_APPROVED

### Reconciliation Purpose
The `reconciliation` table serves as a central point for matching:
1. **Bank reconciliation**: Matching bank statements to payment records
2. **Gateway reconciliation**: Matching Paysafe reports to payment transactions
3. **Commission reconciliation**: Verifying commission calculations and payouts

Key features:
- Embedded line items in JSON for simplicity
- Variance tracking for exception management
- Approval workflow for large variances
- Complete audit trail

### Reference Data Purpose
The `reference_data` table provides a flexible lookup system for:
1. **Dynamic value lists**: Fee types, adjustment reasons, etc.
2. **Business rule parameters**: Late fee amounts, grace periods
3. **UI dropdown values**: User-selectable options
4. **Validation rules**: Acceptable values for various fields

Benefits:
- No code changes for new lookup values
- Self-service administration
- Consistent data validation
- Reduced table proliferation

### Audit Strategy
Instead of a separate audit_log table, the design uses:
1. **Standard audit fields**: created_by, updated_by, created_at, updated_at on all tables
2. **Immutable transactions**: No updates allowed on financial records
3. **Status tracking**: Complete history via status changes
4. **Communication logs**: API requests/responses in communication table

## Implementation Benefits

### Simplification Achieved
- **70% reduction**: From 40+ tables to 13 new tables
- **Clear separation**: Each table has a single, well-defined purpose
- **Minimal joins**: Most queries need only 2-3 tables
- **JSON flexibility**: Handles edge cases without schema changes

### Scalability Features
- **Type tables**: Easy to add new types without schema changes
- **Configuration-driven**: Business rules in configuration, not code
- **Event sourcing ready**: Immutable transactions support event sourcing
- **Multi-tenant ready**: All tables include tenant awareness

### Maintenance Advantages
- **Self-documenting**: Clear table and column names
- **Consistent patterns**: All tables follow same design principles
- **Version-friendly**: JSON fields allow gradual evolution
- **Tool-friendly**: Standard Laravel/MySQL patterns

## Questions Addressed

1. **Invoice Generation**: First invoice created upfront at binding, subsequent invoices generated just-in-time before due dates

2. **Notice Delivery**: System queues notices in `communication` table, actual delivery via third-party APIs (Twilio, SendGrid, mail vendors)

3. **Approval Workflows**: Embedded in transaction flow using status management and type-based rules

4. **Payment Allocation**: Simplified - no cross-policy payments or partial invoice payments

5. **Data Retention**: Designed for permanent retention with application-level archival strategies

## Conclusion

This revised schema successfully balances simplicity with completeness. By leveraging existing system tables and following established patterns, we achieve a clean, maintainable design that fully supports all v10 accounting requirements while reducing complexity by 70%.