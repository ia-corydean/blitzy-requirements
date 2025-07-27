# Accounting Payment Processing - Implementation Approach

## Overview

The payment processing system manages all monetary transactions in the insurance platform, from premium collections to refunds and commission disbursements. It implements secure token-based payment handling with multiple gateway support while maintaining zero storage of sensitive payment data.

## Core Principles

### 1. Security First
- No storage of credit card numbers or bank account details
- Token-based payment method references only
- PCI compliance through tokenization
- Complete audit trail of all payment activities

### 2. Gateway Abstraction
- Support for multiple payment gateways
- Configuration-driven gateway selection
- Automatic failover capabilities
- Unified interface for all payment types

### 3. Payment Flexibility
- Multiple payment methods (Card, ACH, Check, Sweep)
- Full and partial payment support where allowed
- Payment scheduling and retry logic
- Comprehensive status tracking

## Table Schemas

### 1. Payment Table

**Purpose**: Core payment transaction records linking to accounting transactions

```sql
CREATE TABLE payment (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    payment_number VARCHAR(50) UNIQUE NOT NULL,
    payment_type_id BIGINT UNSIGNED NOT NULL,
    payment_method_id BIGINT UNSIGNED NOT NULL,
    transaction_id BIGINT UNSIGNED, -- Link to accounting transaction
    
    -- Payment details
    amount DECIMAL(12,2) NOT NULL,
    payment_date DATETIME NOT NULL,
    
    -- Gateway relationship
    payment_gateway_id BIGINT UNSIGNED,
    gateway_transaction_id VARCHAR(255), -- External reference from gateway
    
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Key Changes from Existing `payments` Table**:
- Rename `payments` to `payment` (singular per naming convention)
- Add `payment_number` for unique business identifier
- Add `payment_type_id` FK instead of inline type
- Add `payment_method_id` FK instead of string method
- Add `payment_gateway_id` for gateway tracking
- Add retry logic fields
- Replace string `status` with FK to `status_id`
- Add `communication_id` for API log reference

### 2. Payment Type Table

**Purpose**: Define categories of payments (premium, refund, commission payout)

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - categorizes payment purposes

### 3. Payment Method Table

**Purpose**: Available payment methods in the system

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - replaces string-based payment methods

### 4. Map Payment Type Method Table

**Purpose**: Define which payment methods are allowed for each payment type

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - business rules for payment combinations

### 5. Payment Gateway Table

**Purpose**: Payment gateway configurations

```sql
CREATE TABLE payment_gateway (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    payment_gateway_type_id BIGINT UNSIGNED NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL, -- PAYSAFE, STRIPE, AUTHORIZE_NET
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Gateway properties
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - gateway management

### 6. Payment Gateway Type Table

**Purpose**: Classify gateways as manual or external

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - simple gateway classification

### 7. Payment Gateway Token Table

**Purpose**: Secure storage of payment method tokens

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Key Changes from Existing Payment Method Storage**:
- Replaces `bank_accounts` and `bank_cards` tables
- Unified token storage for all payment methods
- Links to entity table for ownership
- No sensitive data storage

## Business Rules

### 1. Payment Processing Flow
1. Customer enters payment information (via Paysafe hosted fields)
2. Gateway returns token
3. System stores token reference
4. Payment created with token
5. Gateway processes using token
6. Response logged in communication table
7. Accounting transaction created
8. Payment status updated

### 2. Gateway Selection
- Program configuration determines primary gateway
- Fallback gateway for failures
- Manual override capability
- Gateway health monitoring

### 3. Retry Logic
- Configurable retry attempts by payment type
- Exponential backoff strategy
- Maximum retry limits
- Notification on final failure

## Integration Points

### 1. With Double-Entry System
- Every payment creates accounting transaction
- Automatic journal entry generation
- Component breakdown in transaction lines

### 2. With Communication System (GR-44)
- Gateway API calls logged as communications
- Request/response tracking
- Error logging and debugging

### 3. With Configuration System
- Gateway credentials in configuration
- Program-specific payment rules
- Fee structures and limits

### 4. With Entity Management (GR-52)
- Payment tokens linked to entities
- Customer payment method management
- Producer payment accounts

## Implementation Considerations

### 1. Migration from Existing System
- Migrate bank_accounts to payment tokens
- Migrate bank_cards to payment tokens
- Update payment records with new FKs
- Preserve all existing tokens

### 2. Security Requirements
- Encrypt tokens at rest
- Audit all token access
- PCI compliance validation
- Regular security scans

### 3. Performance Optimization
- Index strategy for payment queries
- Batch processing for bulk payments
- Async processing for gateway calls

## Gateway Configuration

### Sample Configuration Entry
```json
{
  "configuration_type": "PAYMENT_GATEWAY",
  "scope_type": "entity",
  "entity_id": 1, -- payment_gateway.id
  "config_data": {
    "environment": "production",
    "endpoints": {
      "tokenize": "https://api.paysafe.com/v1/tokenize",
      "charge": "https://api.paysafe.com/v1/charge",
      "refund": "https://api.paysafe.com/v1/refund"
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
    }
  }
}
```

## Cross-References

- **GR-44**: Communication architecture for API logging
- **GR-52**: Universal entity management for token ownership
- **GR-65**: Payment processing architecture requirements
- Configuration table for gateway settings

## Validation Rules

### 1. Payment Creation
- Amount must be positive
- Payment method must be active
- Gateway must be available
- Token must be valid

### 2. Processing Rules
- No duplicate processing
- Status transitions enforced
- Timeout handling
- Idempotency keys

### 3. Security Rules
- Token format validation
- Expiration monitoring
- Usage limits
- Fraud detection hooks