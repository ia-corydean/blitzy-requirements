# GR-64 Database Alignment Approach - V4

## Overview
This approach focuses on policy financial transactions related to reinstatement, not general ledger accounting. It leverages existing tables and transaction patterns to track premium changes and policy financial events.

## Key Feedback Integration
- **NOT a general ledger system** - Focus on policy financial transactions only
- **Reference existing data** where possible
- **Support processes** that create/change premiums
- **Credits/debits in transaction_line** for financial clarity
- **Use existing reinstatement tables** with mapping approach
- **Calculations in source code**, results in transaction tables

## Current Database Reality

### Existing Reinstatement Tables
Based on feedback, we have:
1. **reinstatement** - Core reinstatement records
2. **reinstatement_type** - Types of reinstatements
3. **map_reinstatement_transaction** - Links reinstatements to transactions

### Transaction Tables (from GR-70)
1. **transaction** - General transaction information
2. **transaction_line** - Specific transaction details with amounts
3. **transaction_type** - Types of transactions
4. **map_policy_transaction** - Links policies to transactions

## Approach: Policy Financial Transaction Focus

### 1. Reinstatement as Policy Financial Event
```sql
-- Reinstatement types for different scenarios
INSERT INTO reinstatement_type (code, name, description, is_default, status_id) VALUES
('NONPAYMENT_30DAY', 'Non-Payment 30-Day', 'Standard reinstatement within 30 days of cancellation', TRUE, 1),
('ADMINISTRATIVE', 'Administrative', 'Reinstatement due to administrative error', FALSE, 1),
('REGULATORY', 'Regulatory Required', 'State-mandated reinstatement', FALSE, 1),
('APPEALS', 'Appeals Process', 'Reinstatement through appeals process', FALSE, 1);

-- Transaction types for reinstatement financial events
INSERT INTO transaction_type (code, name, description, is_default, status_id) VALUES
('REINSTATEMENT_QUOTE', 'Reinstatement Quote', 'Calculate reinstatement amounts', FALSE, 1),
('REINSTATEMENT_PREMIUM_ADJUSTMENT', 'Premium Adjustment', 'Adjust premium for lapse period', FALSE, 1),
('REINSTATEMENT_FEE', 'Reinstatement Fee', 'Administrative reinstatement fee', FALSE, 1),
('REINSTATEMENT_PAYMENT', 'Reinstatement Payment', 'Payment to reinstate policy', FALSE, 1),
('REINSTATEMENT_COMPLETE', 'Reinstatement Complete', 'Policy successfully reinstated', FALSE, 1);
```

### 2. Enhanced Reinstatement Table
```sql
-- Add financial tracking to reinstatement table
ALTER TABLE reinstatement
ADD COLUMN IF NOT EXISTS policy_id INT NOT NULL AFTER reinstatement_type_id,
ADD COLUMN IF NOT EXISTS cancellation_date DATE NOT NULL,
ADD COLUMN IF NOT EXISTS reinstatement_effective_date DATETIME NOT NULL,
ADD COLUMN IF NOT EXISTS lapse_days INT NOT NULL,
ADD COLUMN IF NOT EXISTS original_premium DECIMAL(10,2) NOT NULL,
ADD COLUMN IF NOT EXISTS adjusted_premium DECIMAL(10,2) NOT NULL,
ADD COLUMN IF NOT EXISTS reinstatement_fee DECIMAL(10,2) DEFAULT 0.00,
ADD COLUMN IF NOT EXISTS total_amount_due DECIMAL(10,2) NOT NULL,
ADD COLUMN IF NOT EXISTS payment_received_date DATETIME,
ADD COLUMN IF NOT EXISTS notes TEXT,
ADD INDEX idx_reinstatement_policy (policy_id),
ADD CONSTRAINT fk_reinstatement_policy FOREIGN KEY (policy_id) REFERENCES policy(id);
```

### 3. Transaction Structure for Reinstatement

#### Transaction Record (General Info)
```sql
-- Example reinstatement transaction
INSERT INTO transaction (
    transaction_type_id,
    reference_type,
    reference_id,
    transaction_date,
    total_amount,
    status_id,
    created_by
) VALUES (
    (SELECT id FROM transaction_type WHERE code = 'REINSTATEMENT_QUOTE'),
    'reinstatement',
    123, -- reinstatement.id
    NOW(),
    475.05, -- Total calculated amount
    (SELECT id FROM status WHERE code = 'PENDING'),
    1
);
```

#### Transaction Lines (Specific Details)
```sql
-- Premium adjustment line
INSERT INTO transaction_line (
    transaction_id,
    line_type,
    description,
    debit_amount,
    credit_amount,
    line_order
) VALUES 
-- Original premium (debit what was owed)
(
    @transaction_id,
    'PREMIUM',
    'Original 6-month premium',
    600.00,
    0.00,
    1
),
-- Lapse credit (credit for unused days)
(
    @transaction_id,
    'ADJUSTMENT',
    'Credit for 15 lapse days (15 × $3.33)',
    0.00,
    49.95,
    2
),
-- Unpaid balance (debit previous amount due)
(
    @transaction_id,
    'BALANCE',
    'Previous unpaid premium balance',
    100.00,
    0.00,
    3
),
-- Reinstatement fee (debit fee)
(
    @transaction_id,
    'FEE',
    'Reinstatement processing fee',
    25.00,
    0.00,
    4
),
-- Previous payments (credit what was paid)
(
    @transaction_id,
    'PAYMENT',
    'Previous payments collected',
    0.00,
    200.00,
    5
);

-- Net result: 725.00 debit - 249.95 credit = 475.05 due
```

### 4. Mapping Tables Usage

#### Link Reinstatement to Transactions
```sql
-- When reinstatement quote is created
INSERT INTO map_reinstatement_transaction (
    reinstatement_id,
    transaction_id,
    transaction_role,
    created_by,
    created_at
) VALUES (
    123, -- reinstatement.id
    @transaction_id,
    'QUOTE', -- Role of this transaction
    1,
    NOW()
);

-- When payment is received
INSERT INTO map_reinstatement_transaction (
    reinstatement_id,
    transaction_id,
    transaction_role,
    created_by,
    created_at
) VALUES (
    123,
    @payment_transaction_id,
    'PAYMENT',
    1,
    NOW()
);
```

#### Link to Policy
```sql
-- Link reinstatement transactions to policy
INSERT INTO map_policy_transaction (
    policy_id,
    transaction_id,
    transaction_role,
    created_by,
    created_at
) VALUES (
    456, -- policy.id
    @transaction_id,
    'REINSTATEMENT_QUOTE',
    1,
    NOW()
);
```

### 5. Reinstatement Process Flow

```sql
-- Step 1: Check eligibility (in application code)
-- Step 2: Create reinstatement record
INSERT INTO reinstatement (
    reinstatement_type_id,
    policy_id,
    cancellation_date,
    reinstatement_effective_date,
    lapse_days,
    original_premium,
    adjusted_premium,
    reinstatement_fee,
    total_amount_due,
    status_id,
    created_by
) VALUES (
    (SELECT id FROM reinstatement_type WHERE code = 'NONPAYMENT_30DAY'),
    456,
    '2024-01-01',
    '2024-01-15 14:30:00',
    15,
    600.00,
    550.05,
    25.00,
    475.05, -- After credits and previous payments
    (SELECT id FROM status WHERE code = 'PENDING'),
    1
);

-- Step 3: Create quote transaction (as shown above)
-- Step 4: Link reinstatement to transaction
-- Step 5: Process payment
-- Step 6: Update policy status
UPDATE policy 
SET 
    status_id = (SELECT id FROM status WHERE code = 'ACTIVE'),
    reinstatement_date = '2024-01-15 14:30:00',
    updated_by = 1,
    updated_at = NOW()
WHERE id = 456;

-- Step 7: Update reinstatement status
UPDATE reinstatement
SET 
    status_id = (SELECT id FROM status WHERE code = 'COMPLETED'),
    payment_received_date = NOW()
WHERE id = 123;
```

### 6. Premium and Installment Updates

```sql
-- Update policy premium after reinstatement
UPDATE policy
SET 
    premium = 550.05, -- Adjusted for lapse
    paid_to_date = '2024-01-15',
    balance_due = 475.05, -- What's still owed
    updated_at = NOW()
WHERE id = 456;

-- Create new installment schedule (if applicable)
-- This would be handled by existing installment tables
-- Just reference the new amounts based on adjusted premium
```

### 7. Action Tracking Integration (from GR-37)

```sql
-- Track reinstatement actions
INSERT INTO action (
    action_type_id,
    entity_type,
    entity_id,
    description,
    user_id,
    created_at
) VALUES 
(
    (SELECT id FROM action_type WHERE code = 'POLICY_REINSTATEMENT_INITIATED'),
    'policy',
    456,
    'Reinstatement process started for policy #456',
    1,
    NOW()
),
(
    (SELECT id FROM action_type WHERE code = 'POLICY_REINSTATEMENT_CALCULATED'),
    'policy',
    456,
    'Reinstatement calculation: $475.05 due (15 day lapse)',
    1,
    NOW()
),
(
    (SELECT id FROM action_type WHERE code = 'POLICY_REINSTATEMENT_COMPLETED'),
    'policy',
    456,
    'Policy #456 reinstated effective 2024-01-15 14:30:00',
    1,
    NOW()
);
```

## Key Differences from V3

1. **No GL Accounts** - Removed all general ledger references
2. **Use Existing Tables** - Leverages reinstatement and mapping tables
3. **Simpler Transaction Lines** - Just debits/credits, no GL codes
4. **Reference Pattern** - Links to data in other tables vs. duplicating
5. **Policy Focus** - All about policy financial events, not accounting

## Benefits of This Approach

1. **Leverages Existing Structure** - Uses current reinstatement tables
2. **Clear Financial Tracking** - Debits/credits show money flow
3. **Flexible Mapping** - Can link multiple transactions to reinstatement
4. **Simple Integration** - Works with existing transaction framework
5. **No GL Complexity** - Focused on policy financials only
6. **Source Code Calculations** - Database stores results, not logic

## Implementation Notes

1. **Calculations in Application**
   - Daily rate calculation
   - Lapse credit computation
   - Fee determination
   - Balance calculations

2. **Transaction Patterns**
   - One reinstatement can have multiple transactions
   - Each transaction can have multiple lines
   - Lines show financial breakdown

3. **Status Management**
   - Reinstatement has its own status
   - Transactions have separate status
   - Policy status updated on completion

4. **Audit Trail**
   - Actions tracked in action table
   - Transactions provide financial history
   - Mappings show relationships

## Summary

This approach treats reinstatement as a policy financial event, not an accounting entry. It uses the existing reinstatement and transaction tables with appropriate mappings, storing calculation results while keeping the calculation logic in application code. The focus is on tracking premium adjustments and payments related to policy reinstatement, not on general ledger accounting.