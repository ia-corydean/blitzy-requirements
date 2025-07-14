# Accounting Schema - Balanced Normalization Design

## Executive Summary

This document presents a balanced approach to the accounting schema that addresses all feedback while maintaining practical flexibility. The design normalizes entities that could grow at scale into proper tables while strategically using JSON fields for structured but flexible data. This approach prioritizes human maintainability and intuitive organization.

### Design Philosophy
- **Normalize** entities that represent core business concepts or could grow significantly
- **Use JSON** for structured data that benefits from flexibility
- **Create type tables** for all categorizations and classifications
- **Maintain consistency** with status_id and audit fields across all tables

### Schema Overview
**Total Tables: ~25** (organized into logical groups)

## Core Accounting Tables

### 1. Transaction Table
```sql
CREATE TABLE transaction (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_number VARCHAR(50) UNIQUE NOT NULL,
    transaction_type_id BIGINT UNSIGNED NOT NULL,
    transaction_date DATETIME NOT NULL,
    
    -- Business context
    entity_type VARCHAR(50), -- POLICY, PRODUCER, CLAIM
   - This will be defined in the entity table
    entity_id BIGINT UNSIGNED,
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
    INDEX idx_entity (entity_type, entity_id),
    INDEX idx_policy (policy_id),
    INDEX idx_status (status_id),
    FOREIGN KEY (transaction_type_id) REFERENCES transaction_type(id),
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

-- Sample transaction types with hierarchy
-- PAYMENT (parent)
--   ├── PREMIUM_PAYMENT
--   ├── FEE_PAYMENT
--   └── OVERPAYMENT
-- ADJUSTMENT (parent)
--   ├── PREMIUM_ADJUSTMENT
--   ├── FEE_WAIVER
--   └── COMMISSION_ADJUSTMENT
```

### 4. Account Table (Enhanced)
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

### 5. Account Type Table (Simplified)
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
- this is already handled in the payment table right?
```sql
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
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Gateway configuration (structured JSON)
    gateway_config JSON, -- Endpoint URLs, timeout settings, etc.
   - this should be in configuration with configuration_type as third party or something.
   - then map/associate the entity for the gateway to the configuration
    
    -- Gateway capabilities
    supported_methods JSON, -- ["CARD", "ACH"]
    supported_currencies JSON, -- ["USD", "CAD"]
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (payment_gateway_type_id) REFERENCES payment_gateway_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```

### 11. Payment Gateway Type Table
```sql
CREATE TABLE payment_gateway_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- PAYSAFE, STRIPE, AUTHORIZE_NET, MANUAL
    - the examples should be stored in payment_gateway and the type as manual or external
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Type properties
    is_tokenized BOOLEAN DEFAULT TRUE,
    - This should be on the gateway configuration or the gateway table itself.
    requires_pci BOOLEAN DEFAULT TRUE,
   - This should be on the gateway configuration or the gateway table itself.
    
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
    entity_type VARCHAR(50) NOT NULL, -- POLICY, PRODUCER
    entity_id BIGINT UNSIGNED NOT NULL,
    
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
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_entity (entity_type, entity_id),
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
    
    -- Type configuration
    requires_approval BOOLEAN DEFAULT FALSE,
    approval_threshold DECIMAL(12,2),
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```

## Commission Management Tables

### 15. Commission Table
```sql
CREATE TABLE commission (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_id BIGINT UNSIGNED NOT NULL,
    commission_type_id BIGINT UNSIGNED NOT NULL,
    
    -- Commission details
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
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_producer (producer_id),
    INDEX idx_policy (policy_id),
    INDEX idx_earned_date (earned_date)
);
```

### 16. Commission Hierarchy Table
- we are not goin to have this. Comissions will only go to the producer of record.

```sql
CREATE TABLE commission_hierarchy (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    commission_id BIGINT UNSIGNED NOT NULL,
    
    -- Hierarchy levels
    level INT NOT NULL, -- 1, 2, 3
    producer_id BIGINT UNSIGNED NOT NULL,
    producer_role VARCHAR(50), -- AGENT, AGENCY, MGA
    
    -- Commission split
    split_percentage DECIMAL(5,4) NOT NULL,
    split_amount DECIMAL(12,2) NOT NULL,
    override_rate DECIMAL(5,4),
    
    -- Payment tracking
    payment_id BIGINT UNSIGNED,
    paid_date DATE,
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (commission_id) REFERENCES commission(id),
    FOREIGN KEY (producer_id) REFERENCES producer(id),
    FOREIGN KEY (payment_id) REFERENCES payment(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_commission (commission_id),
    INDEX idx_producer (producer_id),
    UNIQUE KEY uk_commission_level (commission_id, level)
);
```

### 17. Commission Type Table
```sql
CREATE TABLE commission_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- NEW_BUSINESS, RENEWAL, OVERRIDE, BONUS
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

### 18. Premium Calculation Basis Table
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

### 19. Invoice Table
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

### 20. Invoice Line Table
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

### 21. Invoice Type Table
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

### 22. Fee Type Table
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

### 23. Adjustment Reason Table
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

### Program-Specific Configuration
All program-specific settings (fees, limits, thresholds) are stored in the existing `configuration` table:

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
      "commission_approval": 5000.00
    },
    "commission_rates": {
      "new_business_default": 0.15,
      "renewal_default": 0.10,
      "override_rates": {
        "level_2": 0.03,
        "level_3": 0.02
      }
    },
    "payment_plans": [
      {
        "code": "FULL",
        "name": "Paid in Full",
        "down_percent": 100,
        "installments": 1
      },
      {
        "code": "MONTHLY",
        "name": "Monthly",
        "down_percent": 16.67,
        "installments": 12
      }
    ],
    "grace_period_days": 11,
    "cancellation_settings": {
      "refund_prevention_days": 5,
      "small_refund_threshold": 10.00
    }
  }
}
```

## Strategic JSON Usage

### When to Use JSON Fields

1. **Metadata Fields**: For extensible, validated data
   - Transaction metadata (validated against schema)
   - Token metadata (card details, bank info)
   - MICR data (routing numbers, account info)

2. **Configuration Data**: For flexible settings
   - Gateway configuration
   - Program-specific rules
   - Notification templates

3. **Address/Contact Data**: For structured but variable data
   - Payee addresses
   - Contact information
   - Geographic data

### JSON Schema Examples

#### Transaction Metadata Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "reversal_reason": {
      "type": "string",
      "enum": ["NSF", "FRAUD", "CUSTOMER_REQUEST", "ERROR"]
    },
    "original_reference": {
      "type": "string",
      "pattern": "^TXN-[0-9]{10}$"
    },
    "processing_notes": {
      "type": "string",
      "maxLength": 500
    }
  },
  "required": ["reversal_reason"]
}
```

#### Check MICR Data Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "routing_number": {
      "type": "string",
      "pattern": "^[0-9]{9}$"
    },
    "account_number": {
      "type": "string",
      "pattern": "^[0-9]{4,17}$"
    },
    "check_number": {
      "type": "string",
      "pattern": "^[0-9]{1,10}$"
    }
  },
  "required": ["routing_number", "account_number", "check_number"]
}
```

## Removed/Modified Tables

### Reconciliation Table
Per user feedback, bank reconciliation is not needed at this time. The table can be added later if required. Gateway reconciliation can be handled through payment status tracking and communication logs.

### Reference Data Table
Replaced with specific type tables (fee_type, adjustment_reason, etc.) for better organization and type safety.

## Benefits of This Design

### 1. Scalability
- Core entities that could grow (payment methods, gateways, fees) have dedicated tables
- Type tables allow easy addition of new categories
- JSON fields provide flexibility for edge cases

### 2. Maintainability
- Clear table purposes and relationships
- Consistent naming conventions
- Structured JSON with validation schemas
- Human-intuitive organization

### 3. Performance
- Proper indexing on all foreign keys and search fields
- Minimal JSON querying required
- Clear join paths for common queries

### 4. Flexibility
- Strategic use of JSON for truly variable data
- Configuration-driven behavior
- Extensible without schema changes

## Implementation Notes

1. **Status Management**: All tables use status_id for consistency
2. **Audit Fields**: Standard created_by, updated_by, created_at, updated_at
3. **JSON Validation**: Application layer validates JSON against schemas
4. **Configuration**: Program-specific settings in configuration table
5. **Communication**: Gateway responses logged in communication table

This balanced approach provides the structure needed for a maintainable system while preserving flexibility where it adds value.