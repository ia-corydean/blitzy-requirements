# Accounting Simplified - Implementation Approach

## Requirement Understanding

The accounting system needs to support insurance financial operations including billing, payments, commissions, and reconciliation. The current v10 proposal includes 40+ tables with complex relationships. This approach dramatically simplifies the design to 9 core tables while maintaining essential double-entry accounting principles and business functionality.

Core business needs:
- Double-entry accounting with full audit trail
- Payment processing through Paysafe tokenization
- Commission calculations and disbursements  
- Fee management (policy, installment, NSF, etc.)
- Reconciliation capabilities
- Program-specific configuration
- 7-year data retention

## Domain Classification
- Primary Domain: accounting
- Cross-Domain Impact: Yes - integrates with producer-portal (policies), entity-integration (payment gateways)
- Complexity Level: Medium (simplified from High)

## Pattern Analysis

### Reusable Patterns Identified
- **GR-41 (Table Schema Requirements)**: 
  - Use singular table names
  - Standard audit fields (created_by, updated_by, created_at, updated_at)
  - Status tracking via status_id
  - Consistent foreign key patterns

- **GR-52 (Universal Entity Management)**:
  - Payment gateway abstraction through universal entity pattern
  - Flexible metadata storage using JSON columns
  - Configuration-driven behavior

- **GR-02 (Database Migrations)**:
  - Proper audit trail implementation
  - Version-controlled schema changes

### Domain-Specific Needs
- **Double-Entry Accounting**: Every transaction must balance (debits = credits)
- **Payment Tokenization**: Store only Paysafe tokens, never raw payment data
- **Commission Hierarchies**: Support agency overrides through flexible structure
- **Program Configuration**: Each insurance program has unique rules

## Proposed Implementation

### Simplification Approach
- **Current Complexity**: 40+ tables with intricate relationships for every business concept
- **Simplified Solution**: 9 core tables that handle all functionality through strategic use of:
  - JSON metadata columns for flexibility
  - Type/category fields for classification
  - Embedded data instead of excessive normalization
  
- **Trade-offs**:
  - Lose: Some query optimization for specific reports, separate tables for each fee type
  - Gain: 75% reduction in complexity, faster development, clearer data model, easier maintenance

### Technical Approach

#### Phase 1: Core Schema Design
1. **Core Accounting Tables** (Week 1)
   - [ ] Create `transaction` table - all financial events
   - [ ] Create `transaction_line` table - double-entry details
   - [ ] Create `account` table - chart of accounts
   - [ ] Implement balanced transaction validation

2. **Payment & Commission Tables** (Week 1)
   - [ ] Create `payment` table - tokenized payments with gateway metadata
   - [ ] Create `commission` table - flexible hierarchy support
   - [ ] Add payment method types and commission structures

3. **Configuration Tables** (Week 2)
   - [ ] Create `program_config` table - all program-specific rules
   - [ ] Create `reference_data` table - generic lookups
   - [ ] Create `reconciliation` table - with embedded line items
   - [ ] Create `audit_log` table - immutable audit trail

#### Phase 2: Business Logic Implementation
1. **Transaction Processing** (Week 2)
   - [ ] Implement transaction creation with automatic line generation
   - [ ] Add fee calculation engine using program_config
   - [ ] Create payment allocation logic
   - [ ] Build commission calculation service

2. **Reconciliation & Reporting** (Week 3)
   - [ ] Implement reconciliation matching logic
   - [ ] Create financial reporting views
   - [ ] Add audit trail triggers
   - [ ] Build data retention policies

### Simplified Table Designs

```sql
-- 1. transaction: Core financial events
CREATE TABLE transaction (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_number VARCHAR(50) UNIQUE NOT NULL,
    transaction_type VARCHAR(50) NOT NULL, -- INVOICE, PAYMENT, ADJUSTMENT, COMMISSION
    transaction_date DATETIME NOT NULL,
    entity_type VARCHAR(50), -- POLICY, PRODUCER, CLAIM
    entity_id BIGINT UNSIGNED,
    total_amount DECIMAL(12,2) NOT NULL,
    description TEXT,
    metadata JSON, -- Flexible additional data
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. transaction_line: Double-entry details
CREATE TABLE transaction_line (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_id BIGINT UNSIGNED NOT NULL,
    account_id BIGINT UNSIGNED NOT NULL,
    debit_amount DECIMAL(12,2) DEFAULT 0,
    credit_amount DECIMAL(12,2) DEFAULT 0,
    line_type VARCHAR(50), -- PREMIUM, POLICY_FEE, COMMISSION, TAX
    line_metadata JSON, -- Additional line-specific data
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (account_id) REFERENCES account(id)
);

-- 3. account: Chart of accounts
CREATE TABLE account (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    account_name VARCHAR(100) NOT NULL,
    account_type VARCHAR(50) NOT NULL, -- ASSET, LIABILITY, REVENUE, EXPENSE
    parent_account_id BIGINT UNSIGNED,
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. payment: Tokenized payment records
CREATE TABLE payment (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    payment_number VARCHAR(50) UNIQUE NOT NULL,
    transaction_id BIGINT UNSIGNED,
    payment_method VARCHAR(50), -- CARD, ACH, CHECK, SWEEP
    gateway_name VARCHAR(50), -- PAYSAFE, MANUAL
    gateway_token VARCHAR(255), -- Tokenized reference
    amount DECIMAL(12,2) NOT NULL,
    status VARCHAR(50), -- PENDING, PROCESSED, FAILED, REVERSED
    processed_at DATETIME,
    gateway_response JSON, -- Full gateway response data
    check_details JSON, -- For physical checks
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES transaction(id)
);

-- 5. commission: Flexible commission structure
CREATE TABLE commission (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_id BIGINT UNSIGNED NOT NULL,
    producer_id BIGINT UNSIGNED NOT NULL,
    policy_id BIGINT UNSIGNED,
    commission_type VARCHAR(50), -- NEW, RENEWAL, OVERRIDE
    base_amount DECIMAL(12,2) NOT NULL,
    rate DECIMAL(5,4), -- Commission percentage
    calculated_amount DECIMAL(12,2) NOT NULL,
    hierarchy_data JSON, -- Parent producer, override rates, etc.
    earned_date DATE,
    paid_date DATE,
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES transaction(id)
);

-- 6. program_config: Program-specific rules
CREATE TABLE program_config (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    program_code VARCHAR(50) NOT NULL,
    config_type VARCHAR(50) NOT NULL, -- FEE, PAYMENT_PLAN, COMMISSION, GRACE_PERIOD
    config_data JSON NOT NULL, -- Flexible configuration storage
    effective_date DATE NOT NULL,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_program_type (program_code, config_type)
);

-- 7. reconciliation: Simplified reconciliation
CREATE TABLE reconciliation (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    reconciliation_date DATE NOT NULL,
    reconciliation_type VARCHAR(50), -- BANK, GATEWAY, COMMISSION
    source_system VARCHAR(50),
    total_items INT NOT NULL,
    matched_items INT NOT NULL,
    exception_items INT NOT NULL,
    reconciled_amount DECIMAL(12,2),
    variance_amount DECIMAL(12,2),
    items JSON, -- Embedded reconciliation items
    status VARCHAR(50), -- IN_PROGRESS, COMPLETED, APPROVED
    approved_by BIGINT UNSIGNED,
    approved_at DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. reference_data: Generic lookup table
CREATE TABLE reference_data (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(50) NOT NULL, -- TRANSACTION_TYPE, FEE_TYPE, PAYMENT_STATUS
    code VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    sort_order INT DEFAULT 0,
    metadata JSON,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_category_code (category, code)
);

-- 9. audit_log: Immutable audit trail
CREATE TABLE audit_log (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    record_id BIGINT UNSIGNED NOT NULL,
    action VARCHAR(20) NOT NULL, -- INSERT, UPDATE, DELETE
    changed_data JSON NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_table_record (table_name, record_id),
    INDEX idx_user_date (user_id, created_at)
);
```

### Configuration Examples

```json
// program_config examples
{
  "config_type": "FEE",
  "config_data": {
    "policy_fee": 50.00,
    "mvcpa_fee_per_vehicle": 0.50,
    "installment_fee": 5.00,
    "nsf_fee": 15.00,
    "reinstatement_fee": 25.00,
    "sr22_fee": 25.00
  }
}

{
  "config_type": "PAYMENT_PLAN", 
  "config_data": {
    "plans": [
      {"code": "FULL", "name": "Paid in Full", "down_percent": 100, "installments": 1},
      {"code": "SEMI", "name": "Semi-Annual", "down_percent": 50, "installments": 2},
      {"code": "QUARTERLY", "name": "Quarterly", "down_percent": 25, "installments": 4},
      {"code": "MONTHLY", "name": "Monthly", "down_percent": 16.67, "installments": 12}
    ],
    "grace_period_days": 11
  }
}

{
  "config_type": "COMMISSION",
  "config_data": {
    "new_business_rate": 0.15,
    "renewal_rate": 0.10,
    "override_rates": {
      "level_1": 0.03,
      "level_2": 0.02
    }
  }
}
```

## Risk Assessment
- **Risk 1**: Reporting complexity with JSON data
  → Mitigation: Create materialized views for common reports, use JSON indexing
  
- **Risk 2**: Loss of referential integrity for some relationships  
  → Mitigation: Implement application-level validation, use database triggers for critical constraints

- **Risk 3**: Performance with embedded reconciliation items
  → Mitigation: Limit items per reconciliation, archive old reconciliations, use JSON indexing

## Context Preservation
- **Key Decisions**: 
  - Use JSON for flexibility vs. normalized tables
  - Embed related data to reduce joins
  - Single payment table for all payment types
  - Generic reference_data instead of dozens of lookup tables
  
- **Dependencies**: 
  - Paysafe integration for tokenization
  - Policy and producer tables from producer-portal domain
  - Status table from core system
  
- **Future Impact**: 
  - Easy to add new fee types via configuration
  - Simple to support new payment gateways
  - Flexible commission structures without schema changes

## Pattern Reuse Score: 78%

## Approval Section
**Status**: PENDING APPROVAL
**Reviewer Comments**: [Space for feedback]
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER
**Feedback**: 