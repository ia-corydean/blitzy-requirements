# Accounting Double-Entry System - Implementation Approach

## Overview

The double-entry accounting system forms the foundation of financial integrity in the insurance management platform. Every financial transaction must maintain the fundamental accounting equation (Assets = Liabilities + Equity) through balanced journal entries where total debits equal total credits.

## Core Principles

### 1. Transaction Immutability
- Financial records cannot be modified after creation
- Corrections require reversal entries and new transactions
- Complete audit trail maintained for all activities

### 2. Balance Enforcement
- Every transaction must have balanced debits and credits
- System prevents creation of unbalanced entries
- Real-time validation at multiple levels

### 3. Component Tracking
- Detailed breakdown of transaction components
- Support for premium, fees, taxes, and commissions
- Line-level metadata for reporting

## Table Schemas

### 1. Transaction Table

**Purpose**: Central record of all financial events in the system

```sql
CREATE TABLE transaction (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_number VARCHAR(50) UNIQUE NOT NULL,
    transaction_type_id BIGINT UNSIGNED NOT NULL,
    transaction_date DATETIME NOT NULL,
    
    -- Business context
    entity_id BIGINT UNSIGNED, -- References entity table per GR-52
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Key Changes from Existing `transactions` Table**:
- Rename `transactions` to `transaction` (singular per naming convention)
- Add `transaction_number` for unique business identifier
- Replace string `transaction_type` with FK to `transaction_type_id`
- Add `entity_id` linking to universal entity management (GR-52)
- Add reversal support fields
- Replace string `status` with FK to `status_id`
- Add structured `metadata` field with schema validation

### 2. Transaction Line Table

**Purpose**: Detailed journal entries for each transaction implementing double-entry bookkeeping

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

**This is a NEW table** - no existing equivalent

### 3. Transaction Type Table

**Purpose**: Categorize and validate different transaction types

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

**This is a NEW table** - replaces string-based transaction types

## Business Rules

### 1. Balance Validation
```sql
-- Database trigger to enforce balance
DELIMITER $$
CREATE TRIGGER validate_transaction_balance 
BEFORE INSERT ON transaction 
FOR EACH ROW
BEGIN
    DECLARE total_debits DECIMAL(12,2);
    DECLARE total_credits DECIMAL(12,2);
    
    -- This would be checked after all lines are inserted
    -- Actual implementation would use stored procedure
    SET NEW.metadata = JSON_SET(NEW.metadata, '$.balance_validated', FALSE);
END$$
DELIMITER ;
```

### 2. Transaction Creation Pattern
1. Create transaction header
2. Create all transaction lines
3. Validate total debits = total credits
4. Mark transaction as balanced
5. Prevent further modifications

### 3. Component Types
- **PREMIUM**: Insurance premium amounts
- **POLICY_FEE**: One-time policy fees
- **MVCPA_FEE**: Per-vehicle MVCPA fees
- **SR22_FEE**: SR-22 filing fees
- **INSTALLMENT_FEE**: Payment plan fees
- **COMMISSION**: Agent/producer commissions
- **TAX**: Various tax components

## Integration Points

### 1. With Chart of Accounts
- Every transaction line references an account
- Account types determine debit/credit behavior
- Financial statement categorization

### 2. With Payment Processing
- Payment transactions create specific journal entries
- Automatic distribution to revenue accounts
- Fee component breakdown

### 3. With Policy Management
- Policy transactions linked via policy_id
- Premium calculations feed transaction creation
- Endorsement adjustments tracked

### 4. With Commission System
- Commission calculations create transaction entries
- Producer payments tracked through journal

## Implementation Considerations

### 1. Migration from Existing System
- Existing `transactions` table must be migrated
- Historical data needs journal entry creation
- Balance validation for migrated data

### 2. Performance Optimization
- Index strategy for large transaction volumes
- Partition considerations for historical data
- Query optimization for financial reports

### 3. Audit Requirements
- Immutable transaction records
- Complete user tracking
- Timestamp precision for legal compliance

## Cross-References

- **GR-02**: Database migration patterns
- **GR-41**: Table schema requirements
- **GR-52**: Universal entity management
- **GR-65**: Payment processing architecture

## Validation Rules

### 1. Transaction Level
- Transaction date cannot be future dated
- Total amount must match sum of line amounts
- Status transitions follow defined workflow

### 2. Line Level
- Either debit or credit, not both
- Line numbers must be sequential
- Account must be active
- Amount precision to 2 decimal places

### 3. Balance Rules
- Sum of debits must equal sum of credits
- No negative amounts allowed
- Zero-amount lines allowed for memo entries

## Reporting Capabilities

### 1. Trial Balance
- Summary of all account balances
- Debits and credits by account
- Period-based filtering

### 2. Journal Reports
- Detailed transaction listing
- Component breakdown
- User activity tracking

### 3. Financial Statements
- Income statement generation
- Balance sheet preparation
- Cash flow analysis