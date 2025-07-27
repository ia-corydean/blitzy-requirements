# Accounting Commission Management - Implementation Approach

## Overview

The commission management system handles the calculation, tracking, and payment of commissions to insurance producers. Following the simplified approach where commissions go only to the producer of record, this system manages new business commissions, renewals, chargebacks, and commission disbursements while maintaining complete audit trails.

## Core Principles

### 1. Producer of Record Only
- Commissions paid only to the producer of record on the policy
- No commission splits or hierarchies
- Clear ownership and accountability
- Simplified reconciliation

### 2. Automated Calculation
- Rate-based commission calculations
- Premium basis options (written, earned, collected)
- Automatic chargeback processing
- Configurable commission schedules

### 3. Complete Lifecycle Management
- Calculation at point of sale
- Earning based on premium collection
- Payment scheduling and processing
- Chargeback and recovery handling

## Table Schemas

### 1. Commission Table

**Purpose**: Track all commission calculations and payments

```sql
CREATE TABLE commission (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_id BIGINT UNSIGNED NOT NULL,
    commission_type_id BIGINT UNSIGNED NOT NULL,
    
    -- Commission details (only producer of record)
    producer_id BIGINT UNSIGNED NOT NULL,
    policy_id BIGINT UNSIGNED,
    
    -- Calculation details
    base_amount DECIMAL(12,2) NOT NULL, -- Premium amount used for calculation
    commission_rate DECIMAL(5,4) NOT NULL, -- Rate as decimal (0.15 = 15%)
    calculated_amount DECIMAL(12,2) NOT NULL,
    
    -- Calculation basis
    premium_calculation_basis_id BIGINT UNSIGNED NOT NULL,
    
    -- Timing and payment
    earned_date DATE,
    scheduled_payment_date DATE,
    paid_date DATE,
    payment_id BIGINT UNSIGNED, -- References payment when paid
    
    -- Chargeback support
    is_chargeback BOOLEAN DEFAULT FALSE,
    original_commission_id BIGINT UNSIGNED, -- For chargebacks
    chargeback_reason VARCHAR(255),
    
    -- Commission period (for reporting)
    period_start_date DATE NOT NULL,
    period_end_date DATE NOT NULL,
    
    -- Standard audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (commission_type_id) REFERENCES commission_type(id),
    FOREIGN KEY (producer_id) REFERENCES producer(id),
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (premium_calculation_basis_id) REFERENCES premium_calculation_basis(id),
    FOREIGN KEY (payment_id) REFERENCES payment(id),
    FOREIGN KEY (original_commission_id) REFERENCES commission(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_producer (producer_id),
    INDEX idx_policy (policy_id),
    INDEX idx_earned_date (earned_date),
    INDEX idx_scheduled_payment (scheduled_payment_date, status_id),
    INDEX idx_period (period_start_date, period_end_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - no direct existing equivalent

### 2. Commission Type Table

**Purpose**: Define types of commissions in the system

```sql
CREATE TABLE commission_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- NEW_BUSINESS, RENEWAL, BONUS, OVERRIDE, ADJUSTMENT
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Type configuration
    clawback_days INT DEFAULT 90, -- Days before commission is safe from clawback
    requires_approval BOOLEAN DEFAULT FALSE,
    approval_threshold DECIMAL(12,2) DEFAULT 0,
    
    -- Payment timing
    payment_timing VARCHAR(50), -- IMMEDIATE, COLLECTED, EARNED
    payment_delay_days INT DEFAULT 0,
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - categorizes commission types

### 3. Premium Calculation Basis Table

**Purpose**: Define how premiums are calculated for commission purposes

```sql
CREATE TABLE premium_calculation_basis (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- WRITTEN, EARNED, COLLECTED
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Calculation properties
    calculation_method VARCHAR(50), -- IMMEDIATE, PRORATED, DEFERRED
    includes_fees BOOLEAN DEFAULT FALSE,
    includes_taxes BOOLEAN DEFAULT FALSE,
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - defines commission calculation methods

### 4. Commission Schedule Table

**Purpose**: Define commission rates by producer and product

```sql
CREATE TABLE commission_schedule (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    producer_id BIGINT UNSIGNED NOT NULL,
    program_id BIGINT UNSIGNED NOT NULL,
    commission_type_id BIGINT UNSIGNED NOT NULL,
    
    -- Rate configuration
    commission_rate DECIMAL(5,4) NOT NULL, -- 0.1500 = 15%
    min_premium_amount DECIMAL(12,2) DEFAULT 0,
    max_premium_amount DECIMAL(12,2),
    
    -- Effective dates
    effective_date DATE NOT NULL,
    expiration_date DATE,
    
    -- Override default settings
    override_clawback_days INT,
    override_payment_timing VARCHAR(50),
    
    -- Metadata for special rules
    schedule_metadata JSON, -- Tier rates, bonuses, etc.
    
    -- Standard audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (producer_id) REFERENCES producer(id),
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (commission_type_id) REFERENCES commission_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_producer_program (producer_id, program_id),
    INDEX idx_effective_date (effective_date, expiration_date),
    UNIQUE KEY uk_schedule (producer_id, program_id, commission_type_id, effective_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - manages commission rates

### 5. Commission Statement Table

**Purpose**: Group commissions for payment processing

```sql
CREATE TABLE commission_statement (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    statement_number VARCHAR(50) UNIQUE NOT NULL,
    producer_id BIGINT UNSIGNED NOT NULL,
    
    -- Statement period
    period_start_date DATE NOT NULL,
    period_end_date DATE NOT NULL,
    statement_date DATE NOT NULL,
    
    -- Financial summary
    total_commissions DECIMAL(12,2) NOT NULL,
    total_chargebacks DECIMAL(12,2) DEFAULT 0,
    total_adjustments DECIMAL(12,2) DEFAULT 0,
    net_amount DECIMAL(12,2) NOT NULL,
    
    -- Payment information
    payment_id BIGINT UNSIGNED,
    paid_date DATE,
    
    -- Statement metadata
    commission_count INT NOT NULL,
    statement_metadata JSON, -- Summary by type, product, etc.
    
    -- Standard audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (producer_id) REFERENCES producer(id),
    FOREIGN KEY (payment_id) REFERENCES payment(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_producer_period (producer_id, period_end_date),
    INDEX idx_statement_date (statement_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - groups commissions for payment

### 6. Map Commission Statement Table

**Purpose**: Link individual commissions to statements

```sql
CREATE TABLE map_commission_statement (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    commission_id BIGINT UNSIGNED NOT NULL,
    commission_statement_id BIGINT UNSIGNED NOT NULL,
    
    -- Line item details
    line_number INT NOT NULL,
    included_amount DECIMAL(12,2) NOT NULL,
    
    -- Standard fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (commission_id) REFERENCES commission(id),
    FOREIGN KEY (commission_statement_id) REFERENCES commission_statement(id),
    UNIQUE KEY uk_commission_statement (commission_id, commission_statement_id),
    INDEX idx_statement (commission_statement_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - links commissions to statements

## Business Rules

### 1. Commission Calculation
- Rate determined by active commission schedule
- Base amount from premium (excluding fees/taxes per config)
- Automatic calculation on policy issuance
- Recalculation on endorsements

### 2. Commission Earning
- Based on premium calculation basis
- Written: Earned immediately
- Collected: Earned when premium paid
- Earned: Pro-rated over policy term

### 3. Chargeback Processing
- Automatic chargeback on early cancellation
- Within clawback period (typically 90 days)
- Creates negative commission entry
- Offsets future payments

### 4. Payment Processing
- Commissions grouped into statements
- Net payment after chargebacks
- Minimum payment thresholds
- Multiple payment methods supported

## Integration Points

### 1. With Double-Entry Accounting
- Commission expense entries
- Payable accruals
- Payment disbursement entries
- Chargeback reversals

### 2. With Policy Management
- Commission calculation on bind
- Recalculation on endorsements
- Chargeback on cancellations
- Producer assignment tracking

### 3. With Payment Processing
- Commission payment generation
- ACH/Check disbursements
- Payment reconciliation
- 1099 reporting data

### 4. With Billing System
- Premium collection tracking
- Commission earning triggers
- NSF impact on commissions
- Reinstatement handling

## Implementation Considerations

### 1. Performance Optimization
- Batch statement generation
- Indexed commission queries
- Efficient chargeback detection
- Cached rate lookups

### 2. Compliance Requirements
- 1099 reporting support
- State licensing validation
- Escheatment handling
- Audit trail maintenance

### 3. Producer Portal Integration
- Real-time commission visibility
- Statement access
- Commission projections
- Performance analytics

## Configuration Examples

### 1. Program Commission Configuration
```json
{
  "configuration_type": "PROGRAM_COMMISSION",
  "scope_type": "program",
  "program_id": 123,
  "config_data": {
    "default_rates": {
      "new_business": 0.15,
      "renewal": 0.10,
      "referral": 0.05
    },
    "calculation_basis": "COLLECTED",
    "clawback_rules": {
      "enabled": true,
      "days": 90,
      "rate": 1.0
    },
    "payment_schedule": {
      "frequency": "MONTHLY",
      "cutoff_day": 25,
      "payment_delay": 5,
      "minimum_payment": 50.00
    },
    "approval_thresholds": {
      "NEW_BUSINESS": 5000.00,
      "BONUS": 1000.00
    }
  }
}
```

### 2. Producer Commission Override
```json
{
  "schedule_metadata": {
    "tier_rates": [
      {"min_volume": 0, "rate": 0.12},
      {"min_volume": 50000, "rate": 0.15},
      {"min_volume": 100000, "rate": 0.18}
    ],
    "bonus_targets": {
      "quarterly_target": 75000,
      "bonus_rate": 0.02
    },
    "special_products": {
      "SR22": {"rate": 0.10},
      "HIGH_RISK": {"rate": 0.20}
    }
  }
}
```

## Cross-References

- **GR-41**: Table schema requirements
- **GR-52**: Entity management for producers
- Transaction table for journal entries
- Payment table for disbursements
- Policy table for commission basis

## Validation Rules

### 1. Commission Creation
- Valid producer assignment required
- Active commission schedule must exist
- Premium amount must be positive
- Rate must be within allowed range

### 2. Payment Processing
- Producer must be active
- Banking information required
- Minimum payment threshold met
- No compliance holds

### 3. Chargeback Rules
- Within clawback period
- Original commission must exist
- Cannot exceed original amount
- Proper reason required

## Reporting Capabilities

### 1. Commission Statements
- Detailed transaction listing
- Summary by product/type
- YTD earnings
- Chargeback analysis

### 2. Management Reports
- Commission expense by period
- Producer performance metrics
- Product profitability
- Trend analysis

### 3. Compliance Reports
- 1099 preparation data
- License verification
- Escheatment tracking
- Audit reports