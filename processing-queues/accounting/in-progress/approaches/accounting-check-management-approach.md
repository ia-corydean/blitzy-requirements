# Accounting Check Management - Implementation Approach

## Overview

The check management system handles both inbound and outbound check processing for the insurance platform. This includes premium payment checks from customers, refund checks to insureds, commission checks to producers, and vendor payments. The system tracks the complete lifecycle of physical and electronic checks while maintaining security and compliance with banking regulations.

## Core Principles

### 1. Complete Check Lifecycle
- Creation and printing/generation
- Mailing and delivery tracking
- Deposit and clearing
- Void and reissue handling
- Escheatment for uncashed checks

### 2. Security and Controls
- Check number sequencing
- Signature authorization levels
- Positive pay file generation
- Fraud prevention measures
- MICR encoding standards

### 3. Reconciliation Support
- Bank statement matching
- Outstanding check tracking
- Stop payment processing
- NSF handling
- Daily reconciliation reports

## Table Schemas

### 1. Check Table

**Purpose**: Track all checks in the system, both inbound and outbound

```sql
CREATE TABLE check (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    check_type_id BIGINT UNSIGNED NOT NULL,
    payment_id BIGINT UNSIGNED, -- Links to payment record
    
    -- Check identification
    check_number VARCHAR(50) NOT NULL,
    check_date DATE NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    
    -- Parties
    payee_name VARCHAR(255) NOT NULL,
    payee_address JSON, -- Structured address data
    payer_name VARCHAR(255),
    payer_bank VARCHAR(255),
    
    -- Check status tracking
    status_id BIGINT UNSIGNED NOT NULL,
    issued_date DATE,
    mailed_date DATE,
    cleared_date DATE,
    void_date DATE,
    void_reason TEXT,
    reissue_check_id BIGINT UNSIGNED, -- References new check if reissued
    
    -- Physical check details
    postmarked_date DATE, -- For incoming checks
    received_date DATE, -- When check was received
    deposited_date DATE,
    deposit_batch_number VARCHAR(50),
    
    -- Bank reconciliation
    bank_cleared_date DATE,
    bank_cleared_amount DECIMAL(12,2),
    reconciliation_date DATE,
    reconciliation_notes TEXT,
    
    -- MICR and printing details
    micr_data JSON, -- Routing number, account number, check number
    printing_data JSON, -- Signature lines, watermarks, security features
    
    -- Escheatment tracking
    escheatment_date DATE,
    escheatment_state VARCHAR(2),
    escheatment_reference VARCHAR(100),
    
    -- Standard audit fields
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (check_type_id) REFERENCES check_type(id),
    FOREIGN KEY (payment_id) REFERENCES payment(id),
    FOREIGN KEY (reissue_check_id) REFERENCES check(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_check_number (check_number),
    INDEX idx_check_date (check_date),
    INDEX idx_status (status_id),
    INDEX idx_deposit_batch (deposit_batch_number),
    INDEX idx_payee (payee_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Key Changes from Potential Existing Tables**:
- Standardized naming (singular `check` not `checks`)
- Added `check_type_id` FK instead of string type
- Enhanced tracking fields for full lifecycle
- Added escheatment support
- Structured JSON for addresses and MICR data

### 2. Check Type Table

**Purpose**: Define categories of checks in the system

```sql
CREATE TABLE check_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- PREMIUM_PAYMENT, REFUND, COMMISSION, CLAIM, VENDOR, MANUAL
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Type configuration
    is_inbound BOOLEAN NOT NULL,
    requires_approval BOOLEAN DEFAULT FALSE,
    approval_threshold DECIMAL(12,2) DEFAULT 0,
    
    -- Check handling rules
    auto_deposit BOOLEAN DEFAULT TRUE,
    requires_endorsement BOOLEAN DEFAULT TRUE,
    allow_partial_payment BOOLEAN DEFAULT FALSE,
    
    -- Accounting configuration
    default_account_id BIGINT UNSIGNED,
    clearing_account_id BIGINT UNSIGNED,
    
    -- Escheatment rules
    escheatment_days INT DEFAULT 180, -- Days before escheatment
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (default_account_id) REFERENCES account(id),
    FOREIGN KEY (clearing_account_id) REFERENCES account(id),
    FOREIGN KEY (status_id) REFERENCES status(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - categorizes check types

### 3. Check Batch Table

**Purpose**: Group checks for printing or deposit

```sql
CREATE TABLE check_batch (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    batch_number VARCHAR(50) UNIQUE NOT NULL,
    batch_type VARCHAR(50) NOT NULL, -- PRINT, DEPOSIT, VOID
    batch_date DATE NOT NULL,
    
    -- Batch details
    check_count INT NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    
    -- Processing information
    processed_date DATETIME,
    processed_by BIGINT UNSIGNED,
    
    -- For print batches
    starting_check_number VARCHAR(50),
    ending_check_number VARCHAR(50),
    printer_id VARCHAR(100),
    
    -- For deposit batches
    bank_account_id BIGINT UNSIGNED,
    deposit_slip_number VARCHAR(50),
    
    -- Batch metadata
    batch_metadata JSON, -- Error counts, exceptions, etc.
    
    -- Standard audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (processed_by) REFERENCES user(id),
    FOREIGN KEY (bank_account_id) REFERENCES bank_account(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_batch_date (batch_date),
    INDEX idx_batch_type (batch_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - manages check batches

### 4. Map Check Batch Table

**Purpose**: Link checks to batches

```sql
CREATE TABLE map_check_batch (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    check_id BIGINT UNSIGNED NOT NULL,
    check_batch_id BIGINT UNSIGNED NOT NULL,
    
    -- Batch position
    sequence_number INT NOT NULL,
    
    -- Processing status
    is_processed BOOLEAN DEFAULT FALSE,
    processed_at DATETIME,
    processing_notes TEXT,
    
    -- Standard fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (check_id) REFERENCES check(id),
    FOREIGN KEY (check_batch_id) REFERENCES check_batch(id),
    UNIQUE KEY uk_check_batch (check_id, check_batch_id),
    INDEX idx_batch (check_batch_id),
    INDEX idx_sequence (check_batch_id, sequence_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - links checks to batches

### 5. Bank Account Table

**Purpose**: Track bank accounts for check processing

```sql
CREATE TABLE bank_account (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    entity_id BIGINT UNSIGNED NOT NULL, -- Company or producer entity
    
    -- Account identification
    account_number_encrypted VARCHAR(255) NOT NULL, -- Encrypted storage
    account_number_last_four VARCHAR(4) NOT NULL,
    routing_number VARCHAR(9) NOT NULL,
    bank_name VARCHAR(100) NOT NULL,
    
    -- Account details
    account_type VARCHAR(50) NOT NULL, -- CHECKING, SAVINGS
    account_purpose VARCHAR(50), -- OPERATING, TRUST, PAYROLL
    
    -- Check configuration
    next_check_number INT DEFAULT 1,
    check_number_prefix VARCHAR(10),
    
    -- Positive pay setup
    positive_pay_enabled BOOLEAN DEFAULT FALSE,
    positive_pay_format VARCHAR(50),
    
    -- Account status
    is_active BOOLEAN DEFAULT TRUE,
    activated_date DATE,
    deactivated_date DATE,
    
    -- Standard audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (entity_id) REFERENCES entity(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_entity (entity_id),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - manages bank accounts

### 6. Check Void Reason Table

**Purpose**: Standardize reasons for voiding checks

```sql
CREATE TABLE check_void_reason (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- STALE_DATED, STOP_PAYMENT, ERROR, LOST, DAMAGED
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Reason properties
    requires_reissue BOOLEAN DEFAULT TRUE,
    requires_approval BOOLEAN DEFAULT FALSE,
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - standardizes void reasons

## Business Rules

### 1. Check Issuance
- Sequential check numbering by account
- Approval required above thresholds
- Signature rules by amount
- Address verification required

### 2. Check Processing
- Inbound checks linked to payments
- Deposit batches for bank submission
- NSF handling and fee generation
- Partial payment rules

### 3. Void and Reissue
- Void requires valid reason
- Stop payment notification to bank
- Automatic reissue generation
- Original check cross-reference

### 4. Escheatment Process
- Monitor uncashed checks
- State-specific timing rules
- Required notifications
- Reporting to state agencies

## Integration Points

### 1. With Payment Processing
- Checks linked to payment records
- Automatic check generation
- Payment status updates
- NSF reversal handling

### 2. With Banking Systems
- Positive pay file generation
- Electronic deposit files
- Bank reconciliation import
- ACH conversion options

### 3. With Double-Entry Accounting
- Check issuance journal entries
- Deposit and clearing entries
- Void and reissue entries
- Escheatment accounting

### 4. With Document Management
- Check image storage
- Signature card management
- Deposit slip archival
- Audit documentation

## Implementation Considerations

### 1. Security Requirements
- Encrypted account storage
- Check stock control
- Dual approval workflows
- Fraud detection patterns

### 2. Performance Optimization
- Batch processing efficiency
- Index strategy for searches
- Archive old check data
- Quick reconciliation queries

### 3. Compliance Requirements
- MICR standards compliance
- Positive pay formatting
- Escheatment reporting
- Record retention rules

## Configuration Examples

### 1. Check Type Configuration
```json
{
  "check_type": "REFUND",
  "configuration": {
    "approval_rules": [
      {"max_amount": 1000, "approvers": 1},
      {"max_amount": 5000, "approvers": 2},
      {"max_amount": null, "approvers": 3}
    ],
    "signature_rules": [
      {"max_amount": 5000, "signatures": 1},
      {"max_amount": 25000, "signatures": 2}
    ],
    "void_rules": {
      "stale_days": 180,
      "auto_void": true,
      "notification_days": [30, 60, 90]
    }
  }
}
```

### 2. Bank Account Configuration
```json
{
  "bank_account_id": 123,
  "configuration": {
    "positive_pay": {
      "enabled": true,
      "format": "BAI2",
      "delivery_method": "SFTP",
      "schedule": "DAILY",
      "cutoff_time": "15:00"
    },
    "reconciliation": {
      "auto_match": true,
      "tolerance_amount": 0.01,
      "match_window_days": 5
    },
    "check_printing": {
      "stock_type": "LASER",
      "micr_font": "E13B",
      "security_features": ["WATERMARK", "MICROPRINT", "VOID_PANTOGRAPH"]
    }
  }
}
```

## Cross-References

- **GR-41**: Table schema requirements
- **GR-52**: Entity management for payees
- Payment table for payment linking
- Bank reconciliation processes
- Document management for images

## Validation Rules

### 1. Check Creation
- Valid check type required
- Amount must be positive
- Payee information complete
- Check number unique per account

### 2. Deposit Processing
- Check must be endorsed
- Not previously deposited
- Valid deposit batch
- Within deposit limits

### 3. Void Processing
- Check not already cleared
- Valid void reason
- Approval if required
- Stop payment if issued

## Reporting Capabilities

### 1. Outstanding Checks
- Checks issued but not cleared
- Aging analysis
- Stale dated checks
- Escheatment candidates

### 2. Reconciliation Reports
- Daily deposit summaries
- Cleared check listings
- Exception reports
- Balance confirmations

### 3. Management Reports
- Check volume analysis
- Void and reissue metrics
- Processing time analysis
- Cost per check tracking