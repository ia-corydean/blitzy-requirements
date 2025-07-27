# Accounting Billing and Invoicing - Implementation Approach

## Overview

The billing and invoicing system manages the generation, tracking, and collection of premium payments for insurance policies. It supports multiple payment plans, installment management, automated billing cycles, and comprehensive invoice lifecycle tracking from generation through payment or cancellation.

## Core Principles

### 1. Flexible Payment Plans
- Support for paid-in-full and installment options
- Configurable down payment requirements
- Variable installment counts and frequencies
- Mid-term payment plan changes

### 2. Automated Billing Cycles
- Scheduled invoice generation based on due dates
- Automated reminder notices
- Grace period management
- Cancellation warnings

### 3. Complete Invoice Lifecycle
- Generation with detailed line items
- Payment application and tracking
- Partial payment handling
- Write-off and adjustment support

## Table Schemas

### 1. Invoice Table

**Purpose**: Track all invoices generated for policy premiums and fees

```sql
CREATE TABLE invoice (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    invoice_type_id BIGINT UNSIGNED NOT NULL,
    policy_id BIGINT UNSIGNED NOT NULL,
    
    -- Installment tracking
    installment_number INT NOT NULL,
    total_installments INT NOT NULL,
    
    -- Invoice dates
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    
    -- Financial details
    amount_due DECIMAL(12,2) NOT NULL,
    amount_paid DECIMAL(12,2) DEFAULT 0,
    balance DECIMAL(12,2) NOT NULL,
    
    -- Payment tracking
    paid_date DATE,
    payment_id BIGINT UNSIGNED, -- References payment when fully paid
    
    -- Notice tracking
    last_notice_date DATE,
    notice_count INT DEFAULT 0,
    
    -- Cancellation tracking
    cancellation_notice_date DATE,
    scheduled_cancellation_date DATE,
    
    -- Standard audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (invoice_type_id) REFERENCES invoice_type(id),
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (payment_id) REFERENCES payment(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_policy_installment (policy_id, installment_number),
    INDEX idx_due_date (due_date),
    INDEX idx_status (status_id),
    INDEX idx_scheduled_cancellation (scheduled_cancellation_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Key Changes from Potential Existing Tables**:
- Standardized naming (singular `invoice` not `invoices`)
- Added `invoice_type_id` FK instead of string type
- Added notice and cancellation tracking fields
- Added installment tracking for payment plans
- Replace string `status` with FK to `status_id`

### 2. Invoice Line Table

**Purpose**: Detailed breakdown of charges on each invoice

```sql
CREATE TABLE invoice_line (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    invoice_id BIGINT UNSIGNED NOT NULL,
    line_number INT NOT NULL,
    
    -- Line details
    fee_type_id BIGINT UNSIGNED NOT NULL,
    description TEXT,
    amount DECIMAL(12,2) NOT NULL,
    
    -- Component tracking (links to transaction lines)
    transaction_line_id BIGINT UNSIGNED,
    
    -- Tax information
    is_taxable BOOLEAN DEFAULT FALSE,
    tax_amount DECIMAL(12,2) DEFAULT 0,
    tax_rate DECIMAL(5,4) DEFAULT 0,
    
    -- Line-level metadata
    line_metadata JSON, -- Vehicle info, coverage details, etc.
    
    -- Standard fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (invoice_id) REFERENCES invoice(id),
    FOREIGN KEY (fee_type_id) REFERENCES fee_type(id),
    FOREIGN KEY (transaction_line_id) REFERENCES transaction_line(id),
    UNIQUE KEY uk_invoice_line (invoice_id, line_number),
    INDEX idx_fee_type (fee_type_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - provides detailed invoice breakdown

### 3. Invoice Type Table

**Purpose**: Categorize different types of invoices

```sql
CREATE TABLE invoice_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- INITIAL, INSTALLMENT, ENDORSEMENT, REINSTATEMENT, FINAL
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Type configuration
    generates_notice BOOLEAN DEFAULT TRUE,
    notice_days_before INT DEFAULT 20,
    grace_period_days INT DEFAULT 11,
    
    -- Cancellation settings
    allows_cancellation BOOLEAN DEFAULT TRUE,
    cancellation_notice_days INT DEFAULT 10,
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - defines invoice behavior

### 4. Payment Plan Table

**Purpose**: Define available payment plan options

```sql
CREATE TABLE payment_plan (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- PAID_IN_FULL, MONTHLY, QUARTERLY, SEMI_ANNUAL
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Plan configuration
    installment_count INT NOT NULL,
    down_payment_percentage DECIMAL(5,2) DEFAULT 0,
    installment_fee_id BIGINT UNSIGNED, -- References fee_type
    
    -- Plan rules
    min_premium_amount DECIMAL(12,2) DEFAULT 0,
    max_installments INT DEFAULT 12,
    
    -- Availability
    available_for_new BOOLEAN DEFAULT TRUE,
    available_for_renewal BOOLEAN DEFAULT TRUE,
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (installment_fee_id) REFERENCES fee_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - manages payment plan options

### 5. Policy Payment Plan Table

**Purpose**: Track payment plan selection and changes for each policy

```sql
CREATE TABLE policy_payment_plan (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    policy_id BIGINT UNSIGNED NOT NULL,
    payment_plan_id BIGINT UNSIGNED NOT NULL,
    
    -- Plan details at time of selection
    total_premium DECIMAL(12,2) NOT NULL,
    down_payment_amount DECIMAL(12,2) NOT NULL,
    installment_amount DECIMAL(12,2) NOT NULL,
    installment_fee_amount DECIMAL(12,2) DEFAULT 0,
    
    -- Plan status
    effective_date DATE NOT NULL,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Change tracking
    previous_plan_id BIGINT UNSIGNED,
    change_reason VARCHAR(255),
    
    -- Standard audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (payment_plan_id) REFERENCES payment_plan(id),
    FOREIGN KEY (previous_plan_id) REFERENCES policy_payment_plan(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_policy_active (policy_id, is_active),
    INDEX idx_effective_date (effective_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - links policies to payment plans

## Business Rules

### 1. Invoice Generation
- Generated based on payment plan schedule
- Down payment invoice on policy effective date
- Subsequent invoices on scheduled dates
- Prorated amounts for mid-term changes

### 2. Payment Application
- Payments applied to oldest invoice first
- Partial payments allowed per configuration
- Overpayments create credits
- NSF handling with fee generation

### 3. Notice Generation
- Billing notice X days before due date
- Past due notices after grace period
- Cancellation notice per state requirements
- Electronic delivery when opted-in

### 4. Cancellation Process
- Grace period per program configuration
- Notice of cancellation sent
- Scheduled cancellation date set
- Reinstatement possible until cancellation

## Integration Points

### 1. With Double-Entry Accounting
- Invoice generation creates receivable entries
- Payment application creates cash entries
- Automatic revenue recognition
- Fee and tax component tracking

### 2. With Payment Processing
- Payment links to invoice for application
- Automatic payment plan processing
- Failed payment retry logic
- Refund generation for overpayments

### 3. With Policy Management
- Policy creation triggers billing setup
- Endorsements generate adjustments
- Cancellations stop future billing
- Reinstatements resume billing

### 4. With Communication System (GR-44)
- Invoice delivery via email/mail
- Notice generation and tracking
- Payment confirmation messages
- Cancellation warnings

## Implementation Considerations

### 1. Performance Optimization
- Batch invoice generation process
- Indexed queries for due date searches
- Efficient payment application
- Async notice generation

### 2. State Compliance
- Configurable grace periods by state
- Notice requirements by jurisdiction
- Cancellation rules compliance
- Tax calculation by location

### 3. Payment Plan Flexibility
- Mid-term plan changes
- Endorsement handling
- Short-rate calculations
- Pro-rata adjustments

## Configuration Examples

### 1. Program Billing Configuration
```json
{
  "configuration_type": "PROGRAM_BILLING",
  "scope_type": "program",
  "program_id": 123,
  "config_data": {
    "payment_plans": {
      "default": "MONTHLY",
      "available": ["PAID_IN_FULL", "MONTHLY", "QUARTERLY"],
      "down_payment_rules": {
        "MONTHLY": {
          "percentage": 25,
          "min_amount": 100
        }
      }
    },
    "billing_cycle": {
      "generation_days_before": 20,
      "notice_days_before": 15,
      "grace_period_days": 11
    },
    "fees": {
      "installment_fee": 5.00,
      "nsf_fee": 25.00,
      "reinstatement_fee": 25.00
    },
    "cancellation": {
      "notice_required": true,
      "notice_days": 10,
      "reinstatement_window": 30
    }
  }
}
```

### 2. Invoice Type Configuration
```json
{
  "code": "INSTALLMENT",
  "invoice_metadata": {
    "template": "standard_installment",
    "delivery_methods": ["email", "mail"],
    "reminder_schedule": [
      {"days_before": 10, "method": "email"},
      {"days_before": 5, "method": "email"},
      {"days_after": 1, "method": "email"}
    ]
  }
}
```

## Cross-References

- **GR-44**: Communication architecture for notices
- **GR-64**: Policy reinstatement with billing
- Transaction and payment tables for integration
- Configuration table for billing rules

## Validation Rules

### 1. Invoice Creation
- Policy must be active
- Payment plan must be selected
- Due date must be future
- Amount must be positive

### 2. Payment Application
- Invoice must be unpaid
- Payment amount validation
- Cannot overpay final balance
- Status transitions enforced

### 3. Plan Changes
- Active policy required
- Valid reason for change
- Proper proration calculation
- Outstanding balance handling

## Reporting Capabilities

### 1. Aging Reports
- Outstanding invoices by age
- Past due analysis
- Collection efficiency
- Write-off tracking

### 2. Billing Cycle Reports
- Upcoming invoice generation
- Notice scheduling
- Cancellation pipeline
- Payment plan distribution

### 3. Revenue Analysis
- Billed vs collected
- Payment plan performance
- Fee income analysis
- Cancellation impact