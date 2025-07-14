# Accounting System Technical Plan - Version 10

## Executive Summary

This technical plan provides the database schemas, system architecture, and implementation specifications for the Accounting Global Requirements v10. The design centers on a double-entry accounting system built upon `transaction` and `transaction_line` as core tables, with comprehensive support for payment processing, commission management, and financial reporting.

### Key Technical Decisions
- **Database**: MariaDB 12.x LTS with InnoDB engine for ACID compliance
- **Architecture**: Microservice-based with event-driven communication
- **Security**: PCI compliance through Paysafe tokenization, zero sensitive data storage
- **Performance**: Real-time processing with strategic caching for reports
- **Compliance**: Full audit trail with 7-year retention for financial data

### Global Requirements Alignment
- **GR-41**: Table schema requirements - singular table names, standardized fields
- **GR-02**: Database migrations - audit fields, tenant awareness considerations
- **GR-19**: Table relationships - proper foreign keys and mapping tables
- **GR-52**: Universal entity management - for external integrations
- **GR-44**: Communication architecture - for notices and alerts

## Database Schema Design

### Core Accounting Tables

#### transaction
Primary table for all financial transactions in the system.

```sql
CREATE TABLE transaction (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_number VARCHAR(50) NOT NULL,
    transaction_type_id BIGINT UNSIGNED NOT NULL,
    transaction_date DATETIME NOT NULL,
    effective_date DATE NOT NULL,
    posting_date DATE NOT NULL,
    
    -- Business context
    source_type VARCHAR(50) NOT NULL, -- 'POLICY', 'QUOTE', 'CLAIM', 'MANUAL'
    source_id BIGINT UNSIGNED NULL,
    policy_id BIGINT UNSIGNED NULL,
    producer_id BIGINT UNSIGNED NULL,
    
    -- Financial summary
    total_debit DECIMAL(12,2) NOT NULL DEFAULT 0,
    total_credit DECIMAL(12,2) NOT NULL DEFAULT 0,
    
    -- Processing
    is_posted BOOLEAN DEFAULT FALSE,
    posted_at DATETIME NULL,
    is_reversed BOOLEAN DEFAULT FALSE,
    reversal_transaction_id BIGINT UNSIGNED NULL,
    reversal_reason VARCHAR(255) NULL,
    
    -- Metadata
    description TEXT NULL,
    reference_number VARCHAR(100) NULL,
    external_reference VARCHAR(100) NULL,
    
    -- Audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    UNIQUE KEY uk_transaction_number (transaction_number),
    INDEX idx_transaction_date (transaction_date),
    INDEX idx_effective_date (effective_date),
    INDEX idx_source (source_type, source_id),
    INDEX idx_policy (policy_id),
    INDEX idx_producer (producer_id),
    INDEX idx_status (status_id),
    
    -- Foreign keys
    FOREIGN KEY (transaction_type_id) REFERENCES transaction_type(id),
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (producer_id) REFERENCES producer(id),
    FOREIGN KEY (reversal_transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### transaction_line
Detailed line items for each transaction, implementing double-entry accounting.

```sql
CREATE TABLE transaction_line (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_id BIGINT UNSIGNED NOT NULL,
    line_number INT NOT NULL,
    
    -- Accounting
    account_id BIGINT UNSIGNED NOT NULL,
    debit_amount DECIMAL(12,2) NOT NULL DEFAULT 0,
    credit_amount DECIMAL(12,2) NOT NULL DEFAULT 0,
    
    -- Component breakdown
    component_type_id BIGINT UNSIGNED NOT NULL, -- PREMIUM, POLICY_FEE, MVCPA_FEE, etc.
    component_amount DECIMAL(12,2) NOT NULL,
    
    -- Context
    description VARCHAR(255) NULL,
    entity_type VARCHAR(50) NULL, -- 'VEHICLE', 'DRIVER', 'COVERAGE'
    entity_id BIGINT UNSIGNED NULL,
    
    -- Metadata
    calculation_details JSON NULL,
    
    -- Audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    CHECK (debit_amount > 0 OR credit_amount > 0),
    CHECK (NOT (debit_amount > 0 AND credit_amount > 0)),
    
    -- Indexes
    INDEX idx_transaction (transaction_id),
    INDEX idx_account (account_id),
    INDEX idx_component_type (component_type_id),
    INDEX idx_entity (entity_type, entity_id),
    
    -- Foreign keys
    FOREIGN KEY (transaction_id) REFERENCES transaction(id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES account(id),
    FOREIGN KEY (component_type_id) REFERENCES component_type(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### account
Chart of accounts for the accounting system.

```sql
CREATE TABLE account (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    account_type_id BIGINT UNSIGNED NOT NULL, -- ASSET, LIABILITY, EQUITY, REVENUE, EXPENSE
    account_category_id BIGINT UNSIGNED NOT NULL,
    
    -- Hierarchy
    parent_account_id BIGINT UNSIGNED NULL,
    level INT NOT NULL DEFAULT 1,
    is_detail_account BOOLEAN DEFAULT TRUE,
    
    -- Properties
    normal_balance ENUM('DEBIT', 'CREDIT') NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_system_account BOOLEAN DEFAULT FALSE,
    
    -- Configuration
    require_entity BOOLEAN DEFAULT FALSE,
    allowed_entity_types JSON NULL,
    
    -- Metadata
    description TEXT NULL,
    
    -- Audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    UNIQUE KEY uk_account_number (account_number),
    INDEX idx_type (account_type_id),
    INDEX idx_category (account_category_id),
    INDEX idx_parent (parent_account_id),
    INDEX idx_active (is_active),
    
    -- Foreign keys
    FOREIGN KEY (account_type_id) REFERENCES account_type(id),
    FOREIGN KEY (account_category_id) REFERENCES account_category(id),
    FOREIGN KEY (parent_account_id) REFERENCES account(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Payment Management Tables

#### payment_method
Stores tokenized payment methods with zero sensitive data.

```sql
CREATE TABLE payment_method (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    payment_method_type_id BIGINT UNSIGNED NOT NULL, -- CREDIT_CARD, ACH, CHECK
    
    -- Token information
    gateway_token VARCHAR(255) NOT NULL,
    gateway_id BIGINT UNSIGNED NOT NULL,
    
    -- Display information (non-sensitive)
    display_name VARCHAR(100) NULL,
    last_four VARCHAR(4) NULL,
    expiration_month TINYINT NULL,
    expiration_year SMALLINT NULL,
    
    -- Ownership
    owner_type VARCHAR(50) NOT NULL, -- 'POLICY', 'PRODUCER', 'AGENCY'
    owner_id BIGINT UNSIGNED NOT NULL,
    
    -- Verification
    is_verified BOOLEAN DEFAULT FALSE,
    verified_at DATETIME NULL,
    verification_method VARCHAR(50) NULL,
    
    -- Usage
    is_default BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    last_used_at DATETIME NULL,
    use_count INT DEFAULT 0,
    
    -- Metadata
    metadata JSON NULL,
    
    -- Audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    UNIQUE KEY uk_gateway_token (gateway_id, gateway_token),
    INDEX idx_owner (owner_type, owner_id),
    INDEX idx_type (payment_method_type_id),
    INDEX idx_active (is_active),
    INDEX idx_verified (is_verified),
    
    -- Foreign keys
    FOREIGN KEY (payment_method_type_id) REFERENCES payment_method_type(id),
    FOREIGN KEY (gateway_id) REFERENCES payment_gateway(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### payment_transaction
Records all payment attempts and results.

```sql
CREATE TABLE payment_transaction (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_id BIGINT UNSIGNED NOT NULL,
    payment_method_id BIGINT UNSIGNED NULL,
    
    -- Payment details
    amount DECIMAL(10,2) NOT NULL,
    currency_code CHAR(3) DEFAULT 'USD',
    payment_date DATETIME NOT NULL,
    
    -- Gateway interaction
    gateway_id BIGINT UNSIGNED NOT NULL,
    gateway_transaction_id VARCHAR(255) NULL,
    gateway_response JSON NULL,
    
    -- Processing
    payment_status_id BIGINT UNSIGNED NOT NULL, -- PENDING, APPROVED, DECLINED, ERROR
    approval_code VARCHAR(50) NULL,
    decline_reason VARCHAR(255) NULL,
    
    -- Check processing
    is_physical_check BOOLEAN DEFAULT FALSE,
    check_number VARCHAR(50) NULL,
    postmark_date DATE NULL,
    deposit_date DATE NULL,
    
    -- Reconciliation
    is_reconciled BOOLEAN DEFAULT FALSE,
    reconciled_at DATETIME NULL,
    reconciliation_id BIGINT UNSIGNED NULL,
    
    -- Metadata
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    metadata JSON NULL,
    
    -- Audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_transaction (transaction_id),
    INDEX idx_payment_method (payment_method_id),
    INDEX idx_payment_date (payment_date),
    INDEX idx_gateway (gateway_id, gateway_transaction_id),
    INDEX idx_status (payment_status_id),
    INDEX idx_reconciliation (is_reconciled, reconciliation_id),
    INDEX idx_check (is_physical_check, check_number),
    
    -- Foreign keys
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (payment_method_id) REFERENCES payment_method(id),
    FOREIGN KEY (gateway_id) REFERENCES payment_gateway(id),
    FOREIGN KEY (payment_status_id) REFERENCES payment_status(id),
    FOREIGN KEY (reconciliation_id) REFERENCES reconciliation(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### payment_gateway
Configuration for payment gateways per program.

```sql
CREATE TABLE payment_gateway (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    gateway_type_id BIGINT UNSIGNED NOT NULL, -- PAYSAFE, STRIPE, etc.
    
    -- Configuration
    is_primary BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    configuration JSON NOT NULL, -- Encrypted credentials
    
    -- Program assignment
    program_id BIGINT UNSIGNED NOT NULL,
    
    -- Features
    supported_payment_types JSON NOT NULL,
    supported_currencies JSON DEFAULT '["USD"]',
    
    -- Limits
    max_transaction_amount DECIMAL(10,2) NULL,
    daily_limit DECIMAL(12,2) NULL,
    monthly_limit DECIMAL(12,2) NULL,
    
    -- Failover
    failover_gateway_id BIGINT UNSIGNED NULL,
    auto_failover_enabled BOOLEAN DEFAULT FALSE,
    failover_threshold INT DEFAULT 5,
    
    -- Metadata
    metadata JSON NULL,
    
    -- Audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    UNIQUE KEY uk_program_code (program_id, code),
    INDEX idx_type (gateway_type_id),
    INDEX idx_program (program_id),
    INDEX idx_active (is_active),
    
    -- Foreign keys
    FOREIGN KEY (gateway_type_id) REFERENCES gateway_type(id),
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (failover_gateway_id) REFERENCES payment_gateway(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### check_register
Tracks physical checks for printing and reconciliation.

```sql
CREATE TABLE check_register (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    check_number VARCHAR(50) NOT NULL,
    check_type_id BIGINT UNSIGNED NOT NULL, -- REFUND, COMMISSION, CLAIM
    
    -- Check details
    payee_name VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    check_date DATE NOT NULL,
    
    -- Associated transaction
    transaction_id BIGINT UNSIGNED NOT NULL,
    
    -- Status tracking
    check_status_id BIGINT UNSIGNED NOT NULL, -- PENDING, PRINTED, MAILED, CLEARED, VOID
    printed_at DATETIME NULL,
    printed_by BIGINT UNSIGNED NULL,
    mailed_at DATETIME NULL,
    cleared_at DATETIME NULL,
    
    -- Void handling
    is_void BOOLEAN DEFAULT FALSE,
    void_date DATETIME NULL,
    void_reason VARCHAR(255) NULL,
    void_by BIGINT UNSIGNED NULL,
    
    -- Banking
    bank_account_id BIGINT UNSIGNED NOT NULL,
    
    -- Metadata
    memo TEXT NULL,
    address_line_1 VARCHAR(255) NULL,
    address_line_2 VARCHAR(255) NULL,
    city VARCHAR(100) NULL,
    state VARCHAR(2) NULL,
    zip_code VARCHAR(10) NULL,
    
    -- Audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    UNIQUE KEY uk_check_number (bank_account_id, check_number),
    INDEX idx_check_date (check_date),
    INDEX idx_transaction (transaction_id),
    INDEX idx_status (check_status_id),
    INDEX idx_payee (payee_name),
    
    -- Foreign keys
    FOREIGN KEY (check_type_id) REFERENCES check_type(id),
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (check_status_id) REFERENCES check_status(id),
    FOREIGN KEY (bank_account_id) REFERENCES bank_account(id),
    FOREIGN KEY (printed_by) REFERENCES user(id),
    FOREIGN KEY (void_by) REFERENCES user(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Commission Management Tables

#### commission_structure
Defines commission rates and rules at program and agency levels.

```sql
CREATE TABLE commission_structure (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    program_id BIGINT UNSIGNED NOT NULL,
    
    -- Scope
    scope_type VARCHAR(50) NOT NULL, -- 'PROGRAM', 'AGENCY', 'PRODUCER'
    scope_id BIGINT UNSIGNED NULL,
    
    -- Commission rates
    new_business_rate DECIMAL(5,2) NOT NULL,
    renewal_rate DECIMAL(5,2) NOT NULL,
    
    -- Term-specific rates
    six_month_rate DECIMAL(5,2) NULL,
    twelve_month_rate DECIMAL(5,2) NULL,
    
    -- Hierarchy overrides
    is_override BOOLEAN DEFAULT FALSE,
    override_level INT DEFAULT 0, -- 0=direct, 1=agency, 2=master agency
    override_rate DECIMAL(5,2) NULL,
    
    -- Calculation basis
    calculation_basis VARCHAR(50) NOT NULL, -- 'WRITTEN', 'EARNED', 'COLLECTED'
    
    -- Effective dates
    effective_date DATE NOT NULL,
    expiration_date DATE NULL,
    
    -- Special rates
    is_special_rate BOOLEAN DEFAULT FALSE,
    special_rate_reason VARCHAR(255) NULL,
    
    -- Metadata
    metadata JSON NULL,
    
    -- Audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_program (program_id),
    INDEX idx_scope (scope_type, scope_id),
    INDEX idx_effective (effective_date, expiration_date),
    INDEX idx_override (is_override, override_level),
    
    -- Foreign keys
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### commission_calculation
Records calculated commissions for policies.

```sql
CREATE TABLE commission_calculation (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_id BIGINT UNSIGNED NOT NULL,
    policy_id BIGINT UNSIGNED NOT NULL,
    producer_id BIGINT UNSIGNED NOT NULL,
    
    -- Calculation details
    commission_structure_id BIGINT UNSIGNED NOT NULL,
    premium_amount DECIMAL(10,2) NOT NULL,
    commission_rate DECIMAL(5,2) NOT NULL,
    commission_amount DECIMAL(10,2) NOT NULL,
    
    -- Timing
    calculation_date DATE NOT NULL,
    earned_date DATE NULL,
    payable_date DATE NULL,
    
    -- Status
    commission_status_id BIGINT UNSIGNED NOT NULL, -- CALCULATED, EARNED, PAYABLE, PAID
    
    -- Payment tracking
    is_paid BOOLEAN DEFAULT FALSE,
    paid_date DATE NULL,
    payment_transaction_id BIGINT UNSIGNED NULL,
    check_register_id BIGINT UNSIGNED NULL,
    
    -- Adjustments
    is_adjustment BOOLEAN DEFAULT FALSE,
    original_calculation_id BIGINT UNSIGNED NULL,
    adjustment_reason VARCHAR(255) NULL,
    
    -- Clawback protection
    clawback_eligible_until DATE NULL,
    is_clawback_protected BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    metadata JSON NULL,
    
    -- Audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_transaction (transaction_id),
    INDEX idx_policy (policy_id),
    INDEX idx_producer (producer_id),
    INDEX idx_calculation_date (calculation_date),
    INDEX idx_status (commission_status_id),
    INDEX idx_payable (is_paid, payable_date),
    
    -- Foreign keys
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (producer_id) REFERENCES producer(id),
    FOREIGN KEY (commission_structure_id) REFERENCES commission_structure(id),
    FOREIGN KEY (commission_status_id) REFERENCES commission_status(id),
    FOREIGN KEY (payment_transaction_id) REFERENCES payment_transaction(id),
    FOREIGN KEY (check_register_id) REFERENCES check_register(id),
    FOREIGN KEY (original_calculation_id) REFERENCES commission_calculation(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### commission_hierarchy
Defines agency hierarchy relationships for override commissions.

```sql
CREATE TABLE commission_hierarchy (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    producer_id BIGINT UNSIGNED NOT NULL,
    parent_producer_id BIGINT UNSIGNED NOT NULL,
    hierarchy_level INT NOT NULL, -- 1=direct parent, 2=grandparent, etc.
    
    -- Override configuration
    override_rate DECIMAL(5,2) NULL,
    override_type VARCHAR(50) NOT NULL, -- 'PERCENTAGE_OF_COMMISSION', 'FLAT_RATE'
    
    -- Effective dates
    effective_date DATE NOT NULL,
    expiration_date DATE NULL,
    
    -- Metadata
    metadata JSON NULL,
    
    -- Audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    UNIQUE KEY uk_producer_parent (producer_id, parent_producer_id),
    INDEX idx_parent (parent_producer_id),
    INDEX idx_level (hierarchy_level),
    INDEX idx_effective (effective_date, expiration_date),
    
    -- Foreign keys
    FOREIGN KEY (producer_id) REFERENCES producer(id),
    FOREIGN KEY (parent_producer_id) REFERENCES producer(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Configuration Tables

#### program_config
Program-specific accounting configuration.

```sql
CREATE TABLE program_config (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    program_id BIGINT UNSIGNED NOT NULL,
    config_key VARCHAR(100) NOT NULL,
    config_value JSON NOT NULL,
    
    -- Configuration metadata
    config_type VARCHAR(50) NOT NULL, -- 'PAYMENT', 'COMMISSION', 'FEE', 'CANCELLATION'
    description TEXT NULL,
    
    -- Validation
    validation_rules JSON NULL,
    
    -- Audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    UNIQUE KEY uk_program_key (program_id, config_key),
    INDEX idx_type (config_type),
    
    -- Foreign keys
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### fee_structure
Configurable fee definitions by program.

```sql
CREATE TABLE fee_structure (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    program_id BIGINT UNSIGNED NOT NULL,
    fee_type_id BIGINT UNSIGNED NOT NULL,
    
    -- Fee configuration
    calculation_method VARCHAR(50) NOT NULL, -- 'FLAT', 'PERCENTAGE', 'FORMULA'
    flat_amount DECIMAL(8,2) NULL,
    percentage_rate DECIMAL(5,2) NULL,
    formula JSON NULL,
    
    -- Application rules
    apply_to VARCHAR(50) NOT NULL, -- 'POLICY', 'VEHICLE', 'DRIVER', 'TRANSACTION'
    apply_order INT NOT NULL,
    is_waivable BOOLEAN DEFAULT FALSE,
    waiver_approval_required BOOLEAN DEFAULT TRUE,
    
    -- Conditions
    conditions JSON NULL,
    
    -- Effective dates
    effective_date DATE NOT NULL,
    expiration_date DATE NULL,
    
    -- Metadata
    metadata JSON NULL,
    
    -- Audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_program (program_id),
    INDEX idx_fee_type (fee_type_id),
    INDEX idx_apply_order (apply_order),
    INDEX idx_effective (effective_date, expiration_date),
    
    -- Foreign keys
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (fee_type_id) REFERENCES fee_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### payment_plan
Defines available payment plans by program.

```sql
CREATE TABLE payment_plan (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    program_id BIGINT UNSIGNED NOT NULL,
    code VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    
    -- Plan configuration
    payment_plan_type_id BIGINT UNSIGNED NOT NULL, -- PERCENTAGE, DATE_DRIVEN, PAID_IN_FULL
    down_payment_percentage DECIMAL(5,2) NULL,
    installment_count INT NULL,
    
    -- Rules
    minimum_down_payment DECIMAL(10,2) NOT NULL,
    installment_fee_id BIGINT UNSIGNED NULL,
    
    -- Scheduling
    payment_schedule_rules JSON NOT NULL,
    grace_period_days INT NOT NULL,
    
    -- Eligibility
    eligibility_rules JSON NULL,
    
    -- Display
    display_order INT NOT NULL DEFAULT 0,
    is_default BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Metadata
    metadata JSON NULL,
    
    -- Audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    UNIQUE KEY uk_program_code (program_id, code),
    INDEX idx_type (payment_plan_type_id),
    INDEX idx_active (is_active),
    INDEX idx_display (display_order),
    
    -- Foreign keys
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (payment_plan_type_id) REFERENCES payment_plan_type(id),
    FOREIGN KEY (installment_fee_id) REFERENCES fee_structure(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Audit and Compliance Tables

#### audit_log
Comprehensive audit trail for all financial operations.

```sql
CREATE TABLE audit_log (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    audit_type VARCHAR(50) NOT NULL, -- 'TRANSACTION', 'PAYMENT', 'ADJUSTMENT', 'ACCESS'
    
    -- Context
    entity_type VARCHAR(50) NOT NULL,
    entity_id BIGINT UNSIGNED NOT NULL,
    
    -- Action details
    action VARCHAR(100) NOT NULL,
    action_timestamp DATETIME NOT NULL,
    
    -- Changes
    old_values JSON NULL,
    new_values JSON NULL,
    
    -- User context
    user_id BIGINT UNSIGNED NOT NULL,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    session_id VARCHAR(255) NULL,
    
    -- Additional context
    request_id VARCHAR(255) NULL,
    correlation_id VARCHAR(255) NULL,
    
    -- Metadata
    metadata JSON NULL,
    
    -- Created timestamp only (audit logs are immutable)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_entity (entity_type, entity_id),
    INDEX idx_action (action, action_timestamp),
    INDEX idx_user (user_id),
    INDEX idx_timestamp (action_timestamp),
    INDEX idx_correlation (correlation_id),
    
    -- Foreign keys
    FOREIGN KEY (user_id) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### reconciliation
Bank and payment reconciliation records.

```sql
CREATE TABLE reconciliation (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    reconciliation_type_id BIGINT UNSIGNED NOT NULL, -- BANK, PAYMENT_GATEWAY, COMMISSION
    reconciliation_date DATE NOT NULL,
    
    -- Period
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    
    -- Accounts
    bank_account_id BIGINT UNSIGNED NULL,
    payment_gateway_id BIGINT UNSIGNED NULL,
    
    -- Summary
    statement_balance DECIMAL(12,2) NOT NULL,
    system_balance DECIMAL(12,2) NOT NULL,
    variance_amount DECIMAL(12,2) NOT NULL,
    
    -- Item counts
    total_items INT NOT NULL,
    matched_items INT NOT NULL,
    unmatched_items INT NOT NULL,
    exception_items INT NOT NULL,
    
    -- Status
    reconciliation_status_id BIGINT UNSIGNED NOT NULL, -- IN_PROGRESS, COMPLETED, APPROVED
    completed_at DATETIME NULL,
    approved_at DATETIME NULL,
    approved_by BIGINT UNSIGNED NULL,
    
    -- Files
    statement_file_path VARCHAR(255) NULL,
    report_file_path VARCHAR(255) NULL,
    
    -- Metadata
    reconciliation_rules JSON NULL,
    exception_details JSON NULL,
    notes TEXT NULL,
    
    -- Audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_type (reconciliation_type_id),
    INDEX idx_date (reconciliation_date),
    INDEX idx_period (period_start, period_end),
    INDEX idx_status (reconciliation_status_id),
    INDEX idx_bank_account (bank_account_id),
    INDEX idx_gateway (payment_gateway_id),
    
    -- Foreign keys
    FOREIGN KEY (reconciliation_type_id) REFERENCES reconciliation_type(id),
    FOREIGN KEY (bank_account_id) REFERENCES bank_account(id),
    FOREIGN KEY (payment_gateway_id) REFERENCES payment_gateway(id),
    FOREIGN KEY (reconciliation_status_id) REFERENCES reconciliation_status(id),
    FOREIGN KEY (approved_by) REFERENCES user(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### reconciliation_item
Individual items within a reconciliation.

```sql
CREATE TABLE reconciliation_item (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    reconciliation_id BIGINT UNSIGNED NOT NULL,
    
    -- Item identification
    source_type VARCHAR(50) NOT NULL, -- 'BANK_STATEMENT', 'SYSTEM_TRANSACTION'
    source_reference VARCHAR(255) NOT NULL,
    source_date DATE NOT NULL,
    source_amount DECIMAL(10,2) NOT NULL,
    
    -- Matching
    is_matched BOOLEAN DEFAULT FALSE,
    matched_type VARCHAR(50) NULL,
    matched_id BIGINT UNSIGNED NULL,
    match_confidence DECIMAL(5,2) NULL,
    
    -- Variance
    variance_amount DECIMAL(10,2) DEFAULT 0,
    variance_reason VARCHAR(255) NULL,
    
    -- Exception handling
    is_exception BOOLEAN DEFAULT FALSE,
    exception_type VARCHAR(50) NULL,
    exception_resolution VARCHAR(255) NULL,
    resolved_by BIGINT UNSIGNED NULL,
    resolved_at DATETIME NULL,
    
    -- Metadata
    metadata JSON NULL,
    
    -- Audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_reconciliation (reconciliation_id),
    INDEX idx_source (source_type, source_reference),
    INDEX idx_matched (is_matched, matched_type, matched_id),
    INDEX idx_exception (is_exception),
    
    -- Foreign keys
    FOREIGN KEY (reconciliation_id) REFERENCES reconciliation(id) ON DELETE CASCADE,
    FOREIGN KEY (resolved_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Reference Tables

#### transaction_type
```sql
CREATE TABLE transaction_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL, -- 'PREMIUM', 'PAYMENT', 'ADJUSTMENT', 'COMMISSION'
    description TEXT NULL,
    
    -- Journal rules
    debit_account_type VARCHAR(50) NOT NULL,
    credit_account_type VARCHAR(50) NOT NULL,
    
    -- Display
    display_order INT NOT NULL DEFAULT 0,
    is_system_type BOOLEAN DEFAULT FALSE,
    
    -- Audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    UNIQUE KEY uk_code (code),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### component_type
```sql
CREATE TABLE component_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT NULL,
    
    -- Accounting
    default_account_id BIGINT UNSIGNED NOT NULL,
    
    -- Display
    display_order INT NOT NULL DEFAULT 0,
    
    -- Audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    UNIQUE KEY uk_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed data for component types
INSERT INTO component_type (code, name, default_account_id, status_id) VALUES
('PREMIUM', 'Premium', 1, 1),
('POLICY_FEE', 'Policy Fee', 2, 1),
('MVCPA_FEE', 'MVCPA Fee', 3, 1),
('SR22_FEE', 'SR-22 Fee', 4, 1),
('INSTALLMENT_FEE', 'Installment Fee', 5, 1),
('LATE_FEE', 'Late Fee', 6, 1),
('NSF_FEE', 'NSF Fee', 7, 1),
('REINSTATEMENT_FEE', 'Reinstatement Fee', 8, 1),
('ENDORSEMENT_FEE', 'Endorsement Fee', 9, 1),
('COMMISSION', 'Commission', 10, 1),
('TAX', 'Tax', 11, 1);
```

#### fee_type
```sql
CREATE TABLE fee_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL, -- 'POLICY', 'TRANSACTION', 'EVENT'
    description TEXT NULL,
    
    -- Accounting
    component_type_id BIGINT UNSIGNED NOT NULL,
    
    -- Display
    display_order INT NOT NULL DEFAULT 0,
    
    -- Audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    UNIQUE KEY uk_code (code),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## Technical Architecture

### System Components

#### Microservice Boundaries
The accounting domain operates as an independent microservice with clear boundaries:

1. **Accounting Service**
   - Core transaction processing
   - Journal entry management
   - Account balance calculations
   - Financial reporting

2. **Payment Service**
   - Payment method tokenization
   - Payment processing
   - Gateway integration
   - Payment reconciliation

3. **Commission Service**
   - Commission calculations
   - Hierarchy management
   - Commission payments
   - Override processing

4. **Reconciliation Service**
   - Bank reconciliation
   - Payment reconciliation
   - Exception handling
   - Variance analysis

#### API Endpoint Structure

```
/api/v1/accounting/
├── transactions/
│   ├── POST   /                    # Create transaction
│   ├── GET    /{id}               # Get transaction details
│   ├── POST   /{id}/reverse       # Reverse transaction
│   └── GET    /search             # Search transactions
├── payments/
│   ├── POST   /tokenize           # Tokenize payment method
│   ├── POST   /process            # Process payment
│   ├── GET    /{id}/status        # Payment status
│   └── POST   /refund             # Process refund
├── commissions/
│   ├── POST   /calculate          # Calculate commissions
│   ├── GET    /pending            # Pending commissions
│   ├── POST   /approve            # Approve for payment
│   └── GET    /hierarchy          # Get hierarchy
├── reconciliation/
│   ├── POST   /import             # Import statements
│   ├── POST   /match              # Auto-match items
│   ├── POST   /resolve            # Resolve exceptions
│   └── GET    /report             # Reconciliation report
└── reports/
    ├── GET    /trial-balance      # Trial balance
    ├── GET    /income-statement   # P&L statement
    ├── GET    /cash-flow          # Cash flow
    └── GET    /commission-summary # Commission report
```

#### Event-Driven Architecture

The system publishes events for other domains to consume:

1. **Transaction Events**
   - `transaction.created`
   - `transaction.posted`
   - `transaction.reversed`

2. **Payment Events**
   - `payment.processed`
   - `payment.failed`
   - `payment.refunded`
   - `payment.reconciled`

3. **Commission Events**
   - `commission.calculated`
   - `commission.earned`
   - `commission.paid`

4. **Reconciliation Events**
   - `reconciliation.completed`
   - `reconciliation.exception`

### Security Architecture

#### Token Storage and Management
1. **Zero Sensitive Data**
   - No credit card numbers stored
   - No bank account numbers stored
   - Only tokens and metadata retained

2. **Token Lifecycle**
   - Tokens created through Paysafe hosted fields
   - Tokens stored with encryption at rest
   - Token expiration monitoring
   - Automatic token refresh before expiration

3. **Access Control**
   - Role-based permissions for financial data
   - Separate roles for viewing vs. processing
   - Audit logging for all access
   - Data masking in non-production

#### PCI Compliance
1. **Scope Reduction**
   - No cardholder data in our systems
   - Paysafe handles all PCI requirements
   - Reduced compliance burden

2. **Security Controls**
   - TLS 1.3 for all API communications
   - IP whitelisting for payment processing
   - Rate limiting on payment endpoints
   - Fraud detection through Paysafe

### Performance Optimization

#### Database Indexing Strategy
1. **Primary Indexes**
   - All foreign keys indexed
   - Date fields for range queries
   - Status fields for filtering
   - Search fields for lookups

2. **Composite Indexes**
   - Multi-column indexes for common queries
   - Covering indexes for read-heavy tables
   - Partial indexes for large tables

3. **Performance Targets**
   - Transaction creation: <100ms
   - Payment processing: <2s
   - Report generation: <5s
   - Reconciliation matching: <30s for 10k items

#### Caching Strategy
1. **Redis Caching**
   - Account balances (5-minute TTL)
   - Commission rates (1-hour TTL)
   - Report data (15-minute TTL)
   - Configuration data (1-hour TTL)

2. **Database Query Cache**
   - Prepared statement caching
   - Result set caching for reports
   - Connection pooling

3. **Application-Level Caching**
   - In-memory caching for static data
   - Lazy loading for reference data
   - Cache warming for critical data

### Integration Specifications

#### Internal Domain Integration

1. **Policy Domain**
   - Receive policy binding events
   - Receive endorsement events
   - Receive cancellation events
   - Send payment status updates

2. **Producer Portal**
   - Provide commission statements
   - Accept payment methods
   - Send payment receipts

3. **Document Management**
   - Generate invoices
   - Generate statements
   - Store payment receipts

4. **Communication Service**
   - Trigger payment reminders
   - Send payment confirmations
   - Send commission statements

#### External Integration Readiness

1. **Payment Gateway Abstraction**
   ```
   interface PaymentGatewayInterface {
       tokenize(paymentData): Token
       authorize(token, amount): Authorization
       capture(authorization): Transaction
       refund(transaction, amount): Refund
       verify(token): Verification
   }
   ```

2. **Banking Integration**
   ```
   interface BankingInterface {
       generateACH(transactions): ACHFile
       importStatement(file): Statement
       validateAccount(routing, account): Validation
       initiateTransfer(transfer): Confirmation
   }
   ```

3. **General Ledger Export**
   ```
   interface GeneralLedgerInterface {
       exportJournalEntries(period): JournalBatch
       mapAccounts(mapping): AccountMap
       validateBalances(trial): Validation
       closeperiod(period): Closure
   }
   ```

## Data Management

### Data Retention Policies

1. **Financial Transactions**
   - 7-year retention for all transactions
   - Archive after 2 years to separate schema
   - Indexed by year for performance
   - Immutable once archived

2. **Payment Data**
   - Token retention per Paysafe agreement
   - Payment history for 7 years
   - Failed payment attempts for 1 year

3. **Audit Logs**
   - 7-year retention for financial audits
   - 90-day retention for access logs
   - Permanent retention for compliance events

### Archive Strategy

1. **Yearly Archives**
   ```sql
   -- Archive tables by year
   CREATE TABLE transaction_2024 LIKE transaction;
   CREATE TABLE transaction_line_2024 LIKE transaction_line;
   
   -- Partition by date
   ALTER TABLE transaction PARTITION BY RANGE (YEAR(transaction_date)) (
       PARTITION p2024 VALUES LESS THAN (2025),
       PARTITION p2025 VALUES LESS THAN (2026),
       PARTITION pMAX VALUES LESS THAN MAXVALUE
   );
   ```

2. **Archive Process**
   - Monthly archive job
   - Verify archive completeness
   - Update archive indexes
   - Test archive retrieval

### Backup and Recovery

1. **Backup Strategy**
   - Full daily backups
   - Transaction log backups every 15 minutes
   - Offsite replication
   - 30-day backup retention

2. **Recovery Procedures**
   - Point-in-time recovery capability
   - Maximum 15-minute data loss
   - Automated recovery testing
   - Documented recovery runbooks

## Compliance and Standards

### Regulatory Compliance

1. **SOX Compliance**
   - Segregation of duties
   - Change management controls
   - Access controls and monitoring
   - Regular compliance audits

2. **Insurance Regulations**
   - State-specific requirements supported
   - Premium tax calculations
   - Statutory reporting capability
   - Rate filing support

3. **Financial Auditing**
   - Complete audit trails
   - Immutable transaction history
   - Balance reconciliation
   - Exception reporting

### Technical Standards Compliance

1. **GR-41 Table Schema Standards**
   - Singular table names
   - Consistent naming conventions
   - Standard audit fields
   - Proper foreign key constraints

2. **GR-02 Migration Standards**
   - Versioned migrations
   - Rollback capability
   - Data validation
   - Performance testing

3. **GR-19 Relationship Standards**
   - Explicit foreign keys
   - No polymorphic relationships
   - Proper indexing
   - Referential integrity

## Implementation Priorities

### Phase 1: Core Foundation (Weeks 1-2)
1. Core transaction tables
2. Basic payment processing
3. Account management
4. Journal entry system

### Phase 2: Payment Integration (Weeks 3-4)
1. Paysafe integration
2. Payment method tokenization
3. Payment processing
4. Basic reconciliation

### Phase 3: Commission System (Weeks 5-6)
1. Commission structures
2. Calculation engine
3. Hierarchy management
4. Commission payments

### Phase 4: Advanced Features (Weeks 7-8)
1. Full reconciliation system
2. Financial reporting
3. Audit logging
4. Performance optimization

## Success Metrics

### Technical Metrics
- Transaction processing: <100ms average
- Payment success rate: >95%
- System availability: 99.9%
- Data accuracy: 100%

### Business Metrics
- Automated reconciliation: >90%
- Commission calculation accuracy: 100%
- Report generation time: <5 seconds
- User satisfaction: >90%

## Conclusion

This technical plan provides a comprehensive blueprint for implementing the Accounting System v10 requirements. The architecture ensures scalability, security, and compliance while maintaining the flexibility needed for future enhancements. The focus on transaction and transaction_line as core tables provides a solid foundation for double-entry accounting while supporting all business requirements outlined in the functional specification.

---

**Document Version**: 1.0  
**Date**: 2025-01-10  
**Status**: FINAL  
**Related Document**: accounting-global-requirements-generation-v10.md