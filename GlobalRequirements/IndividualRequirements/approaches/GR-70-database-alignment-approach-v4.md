# GR-70 Accounting Architecture - Database Alignment Approach V4

## Overview
This approach focuses on policy financial transactions and premium accounting, not general ledger systems. It uses the existing transaction/transaction_line structure to track all financial events related to policies, payments, and premium changes.

## Key Principles (Based on Feedback)
- **NOT a general ledger system** - Policy financial tracking only
- **Reference existing data** - Don't duplicate information
- **Support premium processes** - Track premium creation and changes
- **Debits/Credits in transaction_line** - Show money flow clearly
- **Calculations in source code** - Database stores results only
- **Use existing tables** - Work within current structure

## Current Transaction Structure

### Core Tables
1. **transaction** - General transaction information
   - Links to policies, quotes, payments via reference_type/reference_id
   - Stores total amounts and dates
   - Has transaction_type_id for categorization

2. **transaction_line** - Detailed breakdown
   - Shows debits and credits
   - Multiple lines per transaction
   - Describes components of transaction

3. **transaction_type** - Transaction categories
   - QUOTE, BIND, PAYMENT, ENDORSEMENT, etc.
   - Defines what kind of financial event

## Approach: Policy Financial Transaction System

### 1. Transaction Types for Policy Lifecycle
```sql
-- Core policy financial events
INSERT INTO transaction_type (code, name, description, is_default, status_id) VALUES
-- Quoting
('QUOTE_INITIAL', 'Initial Quote', 'First quote calculation', FALSE, 1),
('QUOTE_REVISION', 'Quote Revision', 'Updated quote calculation', FALSE, 1),

-- Binding/Issuance
('BIND_POLICY', 'Bind Policy', 'Convert quote to policy', FALSE, 1),
('ISSUE_POLICY', 'Issue Policy', 'Policy documents issued', FALSE, 1),

-- Premium transactions
('PREMIUM_CHARGE', 'Premium Charge', 'Regular premium charge', FALSE, 1),
('PREMIUM_ADJUSTMENT', 'Premium Adjustment', 'Mid-term premium change', FALSE, 1),

-- Payments
('PAYMENT_RECEIVED', 'Payment Received', 'Customer payment', FALSE, 1),
('PAYMENT_NSF', 'Payment NSF', 'Payment failed - insufficient funds', FALSE, 1),
('PAYMENT_REFUND', 'Payment Refund', 'Refund to customer', FALSE, 1),
('PAYMENT_VOID', 'Payment Void', 'Void a payment', FALSE, 1),

-- Fees
('FEE_POLICY', 'Policy Fee', 'Policy issuance fee', FALSE, 1),
('FEE_INSTALLMENT', 'Installment Fee', 'Payment plan fee', FALSE, 1),
('FEE_LATE', 'Late Fee', 'Late payment fee', FALSE, 1),
('FEE_NSF', 'NSF Fee', 'Non-sufficient funds fee', FALSE, 1),
('FEE_SR22', 'SR22 Fee', 'SR22 filing fee', FALSE, 1),

-- Endorsements
('ENDORSEMENT_ADD_VEHICLE', 'Add Vehicle', 'Add vehicle mid-term', FALSE, 1),
('ENDORSEMENT_REMOVE_VEHICLE', 'Remove Vehicle', 'Remove vehicle mid-term', FALSE, 1),
('ENDORSEMENT_ADD_DRIVER', 'Add Driver', 'Add driver mid-term', FALSE, 1),
('ENDORSEMENT_COVERAGE_CHANGE', 'Coverage Change', 'Modify coverage levels', FALSE, 1),

-- Cancellations
('CANCEL_NONPAYMENT', 'Cancel Non-Payment', 'Cancel for non-payment', FALSE, 1),
('CANCEL_REQUEST', 'Cancel by Request', 'Customer requested cancellation', FALSE, 1),
('CANCEL_UNDERWRITING', 'Cancel Underwriting', 'Underwriting cancellation', FALSE, 1),

-- Reinstatement (from GR-64)
('REINSTATEMENT_QUOTE', 'Reinstatement Quote', 'Calculate reinstatement', FALSE, 1),
('REINSTATEMENT_COMPLETE', 'Reinstatement Complete', 'Policy reinstated', FALSE, 1),

-- Commission
('COMMISSION_NEW', 'New Business Commission', 'Commission on new policy', FALSE, 1),
('COMMISSION_RENEWAL', 'Renewal Commission', 'Commission on renewal', FALSE, 1),
('COMMISSION_CHARGEBACK', 'Commission Chargeback', 'Reverse commission', FALSE, 1);
```

### 2. Transaction Line Types
```sql
-- Line item types for transaction breakdowns
INSERT INTO transaction_line_type (code, name, description, is_default, status_id) VALUES
-- Premium components
('BASE_PREMIUM', 'Base Premium', 'Base premium amount', FALSE, 1),
('DISCOUNT', 'Discount', 'Applied discount', FALSE, 1),
('SURCHARGE', 'Surcharge', 'Applied surcharge', FALSE, 1),
('TAX', 'Tax', 'Premium tax', FALSE, 1),

-- Coverage specific
('LIABILITY_PREMIUM', 'Liability Premium', 'Liability coverage premium', FALSE, 1),
('COLLISION_PREMIUM', 'Collision Premium', 'Collision coverage premium', FALSE, 1),
('COMPREHENSIVE_PREMIUM', 'Comprehensive Premium', 'Comprehensive coverage premium', FALSE, 1),
('UNINSURED_MOTORIST', 'Uninsured Motorist', 'UM/UIM premium', FALSE, 1),

-- Fees
('POLICY_FEE', 'Policy Fee', 'Policy issuance fee', FALSE, 1),
('INSTALLMENT_FEE', 'Installment Fee', 'Payment plan fee', FALSE, 1),
('SR22_FEE', 'SR22 Fee', 'SR22 filing fee', FALSE, 1),
('LATE_FEE', 'Late Fee', 'Late payment penalty', FALSE, 1),
('NSF_FEE', 'NSF Fee', 'Returned payment fee', FALSE, 1),

-- Payments
('PAYMENT', 'Payment', 'Payment received', FALSE, 1),
('PAYMENT_REVERSAL', 'Payment Reversal', 'Reverse a payment', FALSE, 1),

-- Adjustments
('ADJUSTMENT', 'Adjustment', 'Premium adjustment', FALSE, 1),
('CREDIT', 'Credit', 'Account credit', FALSE, 1),
('PRORATION', 'Proration', 'Pro-rated amount', FALSE, 1),

-- Commission
('AGENT_COMMISSION', 'Agent Commission', 'Agent commission amount', FALSE, 1),
('BROKER_COMMISSION', 'Broker Commission', 'Broker commission amount', FALSE, 1);
```

### 3. Example: Policy Bind Transaction

```sql
-- Create bind transaction
INSERT INTO transaction (
    transaction_type_id,
    reference_type,
    reference_id,
    transaction_date,
    effective_date,
    total_amount,
    status_id,
    created_by
) VALUES (
    (SELECT id FROM transaction_type WHERE code = 'BIND_POLICY'),
    'policy',
    123, -- policy.id
    NOW(),
    '2024-02-01',
    625.00, -- Total premium + fees
    (SELECT id FROM status WHERE code = 'COMPLETED'),
    1
);

SET @trans_id = LAST_INSERT_ID();

-- Transaction lines showing premium breakdown
INSERT INTO transaction_line (
    transaction_id,
    transaction_line_type_id,
    description,
    debit_amount,
    credit_amount,
    line_order
) VALUES 
-- Premium components (debits - what customer owes)
(
    @trans_id,
    (SELECT id FROM transaction_line_type WHERE code = 'BASE_PREMIUM'),
    'Base 6-month premium',
    500.00,
    0.00,
    1
),
(
    @trans_id,
    (SELECT id FROM transaction_line_type WHERE code = 'DISCOUNT'),
    'Good driver discount (10%)',
    0.00,
    50.00,
    2
),
(
    @trans_id,
    (SELECT id FROM transaction_line_type WHERE code = 'LIABILITY_PREMIUM'),
    'Liability coverage',
    100.00,
    0.00,
    3
),
(
    @trans_id,
    (SELECT id FROM transaction_line_type WHERE code = 'COLLISION_PREMIUM'),
    'Collision coverage',
    50.00,
    0.00,
    4
),
(
    @trans_id,
    (SELECT id FROM transaction_line_type WHERE code = 'POLICY_FEE'),
    'Policy issuance fee',
    25.00,
    0.00,
    5
);

-- Net: 675.00 debit - 50.00 credit = 625.00 total
```

### 4. Example: Payment Transaction

```sql
-- Payment received
INSERT INTO transaction (
    transaction_type_id,
    reference_type,
    reference_id,
    transaction_date,
    total_amount,
    payment_method,
    payment_reference,
    status_id,
    created_by
) VALUES (
    (SELECT id FROM transaction_type WHERE code = 'PAYMENT_RECEIVED'),
    'policy',
    123,
    NOW(),
    208.33, -- Monthly payment
    'CREDIT_CARD',
    'STRIPE_ch_1234567890',
    (SELECT id FROM status WHERE code = 'COMPLETED'),
    1
);

SET @payment_trans_id = LAST_INSERT_ID();

-- Payment line
INSERT INTO transaction_line (
    transaction_id,
    transaction_line_type_id,
    description,
    debit_amount,
    credit_amount,
    line_order
) VALUES (
    @payment_trans_id,
    (SELECT id FROM transaction_line_type WHERE code = 'PAYMENT'),
    'Monthly installment payment',
    0.00,
    208.33, -- Credit reduces what's owed
    1
);

-- Link to policy
INSERT INTO map_policy_transaction (
    policy_id,
    transaction_id,
    created_by,
    created_at
) VALUES (
    123,
    @payment_trans_id,
    1,
    NOW()
);
```

### 5. Example: Endorsement (Add Vehicle)

```sql
-- Endorsement transaction
INSERT INTO transaction (
    transaction_type_id,
    reference_type,
    reference_id,
    transaction_date,
    effective_date,
    total_amount,
    status_id,
    created_by
) VALUES (
    (SELECT id FROM transaction_type WHERE code = 'ENDORSEMENT_ADD_VEHICLE'),
    'endorsement',
    456, -- endorsement.id
    NOW(),
    '2024-02-15',
    150.00, -- Additional premium
    (SELECT id FROM status WHERE code = 'PENDING'),
    1
);

SET @endorse_trans_id = LAST_INSERT_ID();

-- Endorsement lines
INSERT INTO transaction_line (
    transaction_id,
    transaction_line_type_id,
    description,
    debit_amount,
    credit_amount,
    line_order
) VALUES 
(
    @endorse_trans_id,
    (SELECT id FROM transaction_line_type WHERE code = 'PRORATION'),
    'Pro-rated premium for new vehicle (135 days)',
    125.00,
    0.00,
    1
),
(
    @endorse_trans_id,
    (SELECT id FROM transaction_line_type WHERE code = 'POLICY_FEE'),
    'Endorsement processing fee',
    25.00,
    0.00,
    2
);
```

### 6. Policy Balance Calculation

```sql
-- View to calculate policy balance from transactions
CREATE OR REPLACE VIEW v_policy_balance AS
SELECT 
    p.id as policy_id,
    p.policy_number,
    -- Sum all debits (charges)
    COALESCE(SUM(
        CASE 
            WHEN tl.debit_amount > 0 THEN tl.debit_amount 
            ELSE 0 
        END
    ), 0) as total_charges,
    -- Sum all credits (payments/discounts)
    COALESCE(SUM(
        CASE 
            WHEN tl.credit_amount > 0 THEN tl.credit_amount 
            ELSE 0 
        END
    ), 0) as total_credits,
    -- Calculate balance
    COALESCE(SUM(tl.debit_amount - tl.credit_amount), 0) as balance_due
FROM policy p
LEFT JOIN map_policy_transaction mpt ON p.id = mpt.policy_id
LEFT JOIN transaction t ON mpt.transaction_id = t.id
LEFT JOIN transaction_line tl ON t.id = tl.transaction_id
WHERE t.status_id = (SELECT id FROM status WHERE code = 'COMPLETED')
GROUP BY p.id, p.policy_number;

-- Usage
SELECT * FROM v_policy_balance WHERE policy_id = 123;
```

### 7. Premium Earning Tracking

```sql
-- Track earned vs unearned premium
CREATE TABLE IF NOT EXISTS premium_earning (
    id INT AUTO_INCREMENT PRIMARY KEY,
    policy_id INT NOT NULL,
    transaction_id INT NOT NULL,
    earning_date DATE NOT NULL,
    days_in_period INT NOT NULL,
    total_premium DECIMAL(10,2) NOT NULL,
    daily_rate DECIMAL(8,4) NOT NULL,
    earned_amount DECIMAL(10,2) NOT NULL,
    unearned_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_earning_policy (policy_id),
    INDEX idx_earning_date (earning_date),
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (transaction_id) REFERENCES transaction(id)
);

-- Daily earning calculation (run by scheduled job)
INSERT INTO premium_earning (
    policy_id,
    transaction_id,
    earning_date,
    days_in_period,
    total_premium,
    daily_rate,
    earned_amount,
    unearned_amount
)
SELECT 
    p.id,
    t.id,
    CURDATE(),
    DATEDIFF(p.expiration_date, p.effective_date) + 1,
    p.premium,
    p.premium / (DATEDIFF(p.expiration_date, p.effective_date) + 1),
    (p.premium / (DATEDIFF(p.expiration_date, p.effective_date) + 1)) * 
        DATEDIFF(CURDATE(), p.effective_date),
    p.premium - ((p.premium / (DATEDIFF(p.expiration_date, p.effective_date) + 1)) * 
        DATEDIFF(CURDATE(), p.effective_date))
FROM policy p
JOIN map_policy_transaction mpt ON p.id = mpt.policy_id
JOIN transaction t ON mpt.transaction_id = t.id
WHERE p.status_id = (SELECT id FROM status WHERE code = 'ACTIVE')
AND t.transaction_type_id = (SELECT id FROM transaction_type WHERE code = 'BIND_POLICY')
AND NOT EXISTS (
    SELECT 1 FROM premium_earning pe 
    WHERE pe.policy_id = p.id 
    AND pe.earning_date = CURDATE()
);
```

### 8. Commission Tracking

```sql
-- Commission calculation stored in transactions
INSERT INTO transaction (
    transaction_type_id,
    reference_type,
    reference_id,
    transaction_date,
    total_amount,
    status_id,
    created_by
) VALUES (
    (SELECT id FROM transaction_type WHERE code = 'COMMISSION_NEW'),
    'producer',
    789, -- producer.id
    NOW(),
    62.50, -- 10% of premium
    (SELECT id FROM status WHERE code = 'PENDING'),
    1
);

SET @comm_trans_id = LAST_INSERT_ID();

-- Commission breakdown
INSERT INTO transaction_line (
    transaction_id,
    transaction_line_type_id,
    description,
    debit_amount,
    credit_amount,
    line_order
) VALUES (
    @comm_trans_id,
    (SELECT id FROM transaction_line_type WHERE code = 'AGENT_COMMISSION'),
    'New business commission (10% of $625)',
    62.50, -- Debit (owed to agent)
    0.00,
    1
);

-- Link to policy and producer
INSERT INTO map_policy_transaction (policy_id, transaction_id, created_by, created_at)
VALUES (123, @comm_trans_id, 1, NOW());

INSERT INTO map_producer_transaction (producer_id, transaction_id, created_by, created_at)
VALUES (789, @comm_trans_id, 1, NOW());
```

## Key Benefits of This Approach

1. **Focused on Policy Financials** - Not trying to be a GL system
2. **Uses Existing Structure** - Works with current tables
3. **Clear Money Flow** - Debits and credits show what's owed/paid
4. **Flexible References** - Can link to any entity via reference_type/id
5. **Complete History** - All financial events tracked
6. **Simple Calculations** - Database stores results, not formulas

## What This Approach Does NOT Include

1. **No GL Accounts** - No chart of accounts or journal entries
2. **No Double-Entry Accounting** - Just policy debits/credits
3. **No Financial Statements** - Focus on policy transactions
4. **No Complex Posting** - Transactions are simple records
5. **No Accounting Periods** - Just transaction dates

## Implementation Notes

1. **All Calculations in Code**
   - Premium calculations
   - Proration logic
   - Commission calculations
   - Fee determinations

2. **Transaction Patterns**
   - Every financial event creates a transaction
   - Lines break down the components
   - References link to source entities

3. **Balance Tracking**
   - Sum debits minus credits
   - No running balance field
   - Calculate on demand

4. **Status Management**
   - Transactions have status
   - Only COMPLETED transactions count
   - PENDING for quotes/drafts

## Summary

This approach implements a policy financial transaction system that tracks all money-related events for insurance policies. It uses simple debits and credits in transaction lines to show money flow, references existing data rather than duplicating it, and stores calculation results while keeping logic in the application code. This is NOT a general ledger system but rather a focused solution for insurance policy financial management.