# Accounting Fee and Adjustment Management - Implementation Approach

## Overview

The fee and adjustment management system handles all financial modifications to policies and accounts outside of standard premium calculations. This includes policy fees, service charges, manual adjustments, corrections, write-offs, and various compliance-related fees. The system ensures all adjustments maintain accounting integrity through proper documentation and approval workflows.

## Core Principles

### 1. Comprehensive Fee Management
- Standardized fee types across all programs
- Configurable fee amounts and rules
- Automatic fee generation based on events
- Support for one-time and recurring fees

### 2. Controlled Adjustments
- Approval workflows for significant adjustments
- Required documentation and reason codes
- Complete audit trail of all changes
- Reversibility with proper controls

### 3. Accounting Integrity
- All adjustments create balanced journal entries
- Proper revenue recognition timing
- Clear categorization for reporting
- Integration with billing and collection

## Table Schemas

### 1. Fee Type Table

**Purpose**: Define all types of fees that can be charged in the system

```sql
CREATE TABLE fee_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- POLICY_FEE, INSTALLMENT_FEE, NSF_FEE, SR22_FEE, etc.
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Fee categorization
    fee_category VARCHAR(50), -- POLICY, TRANSACTION, PENALTY, SERVICE, COMPLIANCE
    
    -- Fee properties
    is_waivable BOOLEAN DEFAULT FALSE,
    is_refundable BOOLEAN DEFAULT TRUE,
    is_taxable BOOLEAN DEFAULT FALSE,
    
    -- Accounting configuration
    revenue_account_id BIGINT UNSIGNED NOT NULL,
    receivable_account_id BIGINT UNSIGNED NOT NULL,
    
    -- Fee timing
    timing_type VARCHAR(50), -- IMMEDIATE, DEFERRED, EARNED
    earning_method VARCHAR(50), -- STRAIGHT_LINE, IMMEDIATE, POLICY_TERM
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (revenue_account_id) REFERENCES account(id),
    FOREIGN KEY (receivable_account_id) REFERENCES account(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_category (fee_category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - standardizes fee definitions

### 2. Fee Schedule Table

**Purpose**: Define fee amounts by program and effective date

```sql
CREATE TABLE fee_schedule (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    fee_type_id BIGINT UNSIGNED NOT NULL,
    program_id BIGINT UNSIGNED,
    
    -- Fee amount configuration
    amount DECIMAL(12,2) NOT NULL,
    min_amount DECIMAL(12,2) DEFAULT 0,
    max_amount DECIMAL(12,2),
    
    -- Calculation method
    calculation_method VARCHAR(50), -- FLAT, PERCENTAGE, TIERED
    calculation_basis VARCHAR(50), -- PREMIUM, POLICY, VEHICLE
    
    -- Effective dates
    effective_date DATE NOT NULL,
    expiration_date DATE,
    
    -- Fee rules (JSON for flexibility)
    fee_rules JSON, -- Conditional logic, tiers, etc.
    
    -- Standard audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (fee_type_id) REFERENCES fee_type(id),
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_program_fee (program_id, fee_type_id),
    INDEX idx_effective (effective_date, expiration_date),
    UNIQUE KEY uk_fee_schedule (fee_type_id, program_id, effective_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - manages fee amounts over time

### 3. Adjustment Reason Table

**Purpose**: Define valid reasons for financial adjustments

```sql
CREATE TABLE adjustment_reason (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- PREMIUM_CORRECTION, FEE_WAIVER, REFUND, WRITE_OFF, etc.
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Reason categorization
    adjustment_category VARCHAR(50), -- CORRECTION, WAIVER, REFUND, WRITE_OFF, GOODWILL
    
    -- Approval requirements
    requires_approval BOOLEAN DEFAULT FALSE,
    approval_threshold DECIMAL(12,2) DEFAULT 0,
    requires_documentation BOOLEAN DEFAULT FALSE,
    
    -- Accounting impact
    adjustment_type VARCHAR(50), -- DEBIT, CREDIT
    default_account_id BIGINT UNSIGNED,
    
    -- Restrictions
    max_adjustment_amount DECIMAL(12,2),
    allowed_by_role JSON, -- Role restrictions
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (default_account_id) REFERENCES account(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_category (adjustment_category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - standardizes adjustment reasons

### 4. Adjustment Table

**Purpose**: Track all manual adjustments to accounts

```sql
CREATE TABLE adjustment (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    adjustment_number VARCHAR(50) UNIQUE NOT NULL,
    adjustment_reason_id BIGINT UNSIGNED NOT NULL,
    transaction_id BIGINT UNSIGNED NOT NULL,
    
    -- Adjustment target
    entity_id BIGINT UNSIGNED NOT NULL, -- From entity table
    policy_id BIGINT UNSIGNED,
    invoice_id BIGINT UNSIGNED,
    
    -- Adjustment details
    adjustment_date DATE NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    
    -- Documentation
    description TEXT NOT NULL,
    supporting_documentation JSON, -- File references, ticket numbers, etc.
    
    -- Approval tracking
    requires_approval BOOLEAN DEFAULT FALSE,
    approved_by BIGINT UNSIGNED,
    approved_at DATETIME,
    approval_notes TEXT,
    
    -- Reversal support
    is_reversed BOOLEAN DEFAULT FALSE,
    reversal_adjustment_id BIGINT UNSIGNED,
    original_adjustment_id BIGINT UNSIGNED,
    
    -- Standard audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (adjustment_reason_id) REFERENCES adjustment_reason(id),
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (entity_id) REFERENCES entity(id),
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (invoice_id) REFERENCES invoice(id),
    FOREIGN KEY (approved_by) REFERENCES user(id),
    FOREIGN KEY (reversal_adjustment_id) REFERENCES adjustment(id),
    FOREIGN KEY (original_adjustment_id) REFERENCES adjustment(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_entity (entity_id),
    INDEX idx_policy (policy_id),
    INDEX idx_adjustment_date (adjustment_date),
    INDEX idx_status (status_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - tracks all adjustments

### 5. Policy Fee Table

**Purpose**: Track fees applied to specific policies

```sql
CREATE TABLE policy_fee (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    policy_id BIGINT UNSIGNED NOT NULL,
    fee_type_id BIGINT UNSIGNED NOT NULL,
    transaction_id BIGINT UNSIGNED,
    
    -- Fee details
    amount DECIMAL(12,2) NOT NULL,
    applied_date DATE NOT NULL,
    
    -- Fee status
    is_waived BOOLEAN DEFAULT FALSE,
    waiver_reason VARCHAR(255),
    waived_by BIGINT UNSIGNED,
    waived_at DATETIME,
    
    -- Billing integration
    invoice_id BIGINT UNSIGNED,
    is_billed BOOLEAN DEFAULT FALSE,
    is_collected BOOLEAN DEFAULT FALSE,
    
    -- Fee metadata
    fee_metadata JSON, -- Vehicle count, coverage details, etc.
    
    -- Standard audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (fee_type_id) REFERENCES fee_type(id),
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (invoice_id) REFERENCES invoice(id),
    FOREIGN KEY (waived_by) REFERENCES user(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_policy (policy_id),
    INDEX idx_applied_date (applied_date),
    INDEX idx_billing_status (is_billed, is_collected)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - links fees to policies

## Business Rules

### 1. Fee Application
- Automatic fees applied based on policy events
- Policy fee on new business
- Installment fees per payment plan
- SR22/SR26 fees when filing required
- NSF fees on payment failures

### 2. Adjustment Controls
- Dollar amount approval thresholds
- Role-based adjustment limits
- Required documentation for certain types
- Supervisor approval workflows

### 3. Revenue Recognition
- Immediate recognition for transaction fees
- Deferred recognition for policy fees
- Pro-rata earning over policy term
- Proper handling of cancellations

### 4. Write-off Management
- Age-based write-off rules
- Approval requirements by amount
- Recovery tracking after write-off
- Impact on producer commissions

## Integration Points

### 1. With Double-Entry Accounting
- Fee charges create journal entries
- Adjustments maintain balanced books
- Proper account categorization
- Revenue recognition timing

### 2. With Billing System
- Fees added to invoices
- Waiver impact on billing
- NSF fee generation
- Collection tracking

### 3. With Policy Management
- Event-driven fee generation
- Endorsement fee handling
- Cancellation adjustments
- Reinstatement fees

### 4. With Commission System
- Fee impact on commissionable premium
- Chargeback on adjustments
- Write-off effects
- Recovery handling

## Implementation Considerations

### 1. Performance Optimization
- Efficient fee calculation
- Batch adjustment processing
- Indexed queries for reporting
- Cached fee schedules

### 2. Compliance Requirements
- State-specific fee limits
- Required fee disclosures
- Refund regulations
- Documentation retention

### 3. User Experience
- Clear fee breakdowns
- Adjustment reason selection
- Approval workflow visibility
- Audit trail access

## Configuration Examples

### 1. Fee Schedule Configuration
```json
{
  "fee_type_id": 123, // SR22_FEE
  "fee_rules": {
    "base_amount": 25.00,
    "per_vehicle_amount": 15.00,
    "max_total": 100.00,
    "waiver_conditions": {
      "military_discount": true,
      "loyalty_years": 3
    },
    "state_overrides": {
      "CA": {"amount": 35.00},
      "TX": {"amount": 20.00}
    }
  }
}
```

### 2. Adjustment Workflow Configuration
```json
{
  "adjustment_category": "PREMIUM_CORRECTION",
  "approval_rules": [
    {
      "threshold": 100.00,
      "approver_role": "SUPERVISOR",
      "auto_approve": true
    },
    {
      "threshold": 500.00,
      "approver_role": "MANAGER",
      "requires_documentation": true
    },
    {
      "threshold": 1000.00,
      "approver_role": "DIRECTOR",
      "requires_documentation": true,
      "requires_review": true
    }
  ]
}
```

## Cross-References

- **GR-41**: Table schema requirements
- **GR-52**: Entity management
- Transaction table for journal entries
- Invoice table for billing integration
- Account table for GL posting

## Validation Rules

### 1. Fee Application
- Fee type must be active
- Amount within min/max limits
- Policy must be active
- No duplicate fees

### 2. Adjustment Creation
- Valid reason required
- Amount within allowed range
- Required fields completed
- Approval obtained if needed

### 3. Waiver Processing
- Fee must be waivable
- Valid reason provided
- Authorized user
- Not previously waived

## Reporting Capabilities

### 1. Fee Analysis
- Fee revenue by type
- Waiver frequency and amounts
- Fee collection rates
- Trending over time

### 2. Adjustment Reports
- Adjustments by reason
- Approval metrics
- User activity
- Reversal tracking

### 3. Financial Impact
- Revenue impact analysis
- Write-off summaries
- Recovery tracking
- GL reconciliation