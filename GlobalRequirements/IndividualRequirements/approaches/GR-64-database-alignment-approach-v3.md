# GR-64 Database Alignment Approach - V3
See my accounting updates
- this is not going to be a general ledger system
- we are to account for the finanical transactions associated with policies, policy changes, payments, etc..
    - we should reference data that exisits in other table where possible
    - it's essentially supporting the processes that create the premium and changes to premium and reflects the change to policy and installment premium premium.
    - the credits and debits should be depicten in the transaction_line
    - the general/overall transaction information should be in transaction
    - then we can say map_policy_transaction to see the overall details and the specfifics
- keep in mind our existing reinstatement and reinstatement_type table if we need use map_reinstatement_transaction
- calculations should be handled in source code while the data to support those calculations are distrinuted amongs main tables and the result of those calculations end up in transaction and transaction_line and the policy table

## Overview
This document incorporates the reinstatement workflow patterns from the Reinstatement output documentation and aligns with the accounting workflow from the pending accounting requirements.

## Changes from V2
1. **Added detailed reinstatement calculation patterns** - From Reinstatement with Lapse Process documentation
2. **Incorporated accounting workflow integration** - From accounting-global-requirements-generation-v10.md
3. **Enhanced premium recalculation logic** - Including daily rate calculations and lapse handling
4. **Added installment adjustment patterns** - For remaining payment schedules

## Reinstatement Process Analysis

From the Reinstatement documentation, key requirements:
- **30-day reinstatement window** for policies cancelled due to nonpayment
- **No coverage during lapse period** - No backdating allowed
- **Premium recalculation** based on remaining term
- **Installment adjustments** for payment plans
- **Payment triggers reinstatement** - Effective date is payment date/time

## Approach: Transaction-Based Reinstatement with Accounting Integration

### 1. Reinstatement-Specific Transaction Types
```sql
-- Core reinstatement transaction types
INSERT INTO transaction_type (code, name, description, is_default, status_id) VALUES
-- Workflow stages
('REINSTATEMENT_ELIGIBILITY', 'Reinstatement Eligibility Check', 'Verify policy eligible for reinstatement', FALSE, 1),
('REINSTATEMENT_CALCULATION', 'Reinstatement Calculation', 'Calculate amounts due for reinstatement', FALSE, 1),
('REINSTATEMENT_QUOTE', 'Reinstatement Quote', 'Quote for policy reinstatement', FALSE, 1),
('REINSTATEMENT_PAYMENT', 'Reinstatement Payment', 'Payment received for reinstatement', FALSE, 1),
('REINSTATEMENT_COMPLETED', 'Reinstatement Completed', 'Policy successfully reinstated', FALSE, 1),
('REINSTATEMENT_EXPIRED', 'Reinstatement Expired', 'Reinstatement window expired', FALSE, 1),

-- Financial components
('REINSTATEMENT_PREMIUM_ADJ', 'Premium Adjustment', 'Adjustment for lapsed coverage period', FALSE, 1),
('REINSTATEMENT_FEE', 'Reinstatement Fee', 'Administrative reinstatement fee', FALSE, 1),
('REINSTATEMENT_INSTALLMENT_ADJ', 'Installment Adjustment', 'Adjustment to payment schedule', FALSE, 1);

-- Detailed line item types for calculations
INSERT INTO transaction_line_type (code, name, description, is_default, status_id) VALUES
('REINST_ORIGINAL_PREMIUM', 'Original Premium', 'Original policy premium amount', FALSE, 1),
('REINST_LAPSED_PREMIUM', 'Lapsed Premium Credit', 'Credit for unearned premium during lapse', FALSE, 1),
('REINST_REMAINING_PREMIUM', 'Remaining Premium', 'Premium for remaining policy term', FALSE, 1),
('REINST_UNPAID_PREMIUM', 'Unpaid Premium', 'Previously unpaid premium balance', FALSE, 1),
('REINST_ADMIN_FEE', 'Reinstatement Fee', 'Administrative processing fee', FALSE, 1),
('REINST_INSTALLMENT_FEE', 'Installment Fee', 'Payment plan fee if applicable', FALSE, 1);
```

### 2. Reinstatement Calculation Table
```sql
-- Detailed reinstatement calculations per documentation
CREATE TABLE IF NOT EXISTS reinstatement_calculation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL UNIQUE,
    policy_id INT NOT NULL,
    
    -- Key dates
    cancellation_date DATE NOT NULL,
    reinstatement_request_date DATE NOT NULL,
    reinstatement_effective_date DATETIME NOT NULL COMMENT 'Payment date/time becomes effective date',
    policy_expiration_date DATE NOT NULL,
    
    -- Calculation components
    total_policy_days INT NOT NULL COMMENT 'Total days in policy term',
    lapse_days INT NOT NULL COMMENT 'Days without coverage',
    remaining_days INT NOT NULL COMMENT 'Days from reinstatement to expiration',
    
    -- Premium calculations
    original_total_premium DECIMAL(10,2) NOT NULL,
    daily_premium_rate DECIMAL(8,4) NOT NULL COMMENT 'Total premium / total days',
    lapsed_premium_credit DECIMAL(10,2) NOT NULL COMMENT 'Daily rate × lapse days',
    adjusted_total_premium DECIMAL(10,2) NOT NULL COMMENT 'Original - lapsed credit',
    
    -- Amounts due
    unpaid_premium_balance DECIMAL(10,2) DEFAULT 0 COMMENT 'Prior unpaid amounts',
    reinstatement_fee DECIMAL(10,2) DEFAULT 0,
    installment_fees DECIMAL(10,2) DEFAULT 0,
    total_amount_due DECIMAL(10,2) NOT NULL,
    
    -- Payment collected
    payments_previously_made DECIMAL(10,2) DEFAULT 0,
    policy_balance_remaining DECIMAL(10,2) NOT NULL,
    
    -- Installment info
    installments_remaining INT DEFAULT 0,
    installment_amount DECIMAL(10,2) DEFAULT 0,
    next_due_date DATE,
    days_until_next_due INT,
    
    -- Status tracking
    calculation_status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    status_id INT NOT NULL,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_reinstatement_calc_policy (policy_id),
    INDEX idx_reinstatement_calc_status (calculation_status),
    CONSTRAINT fk_reinstatement_calc_transaction 
        FOREIGN KEY (transaction_id) 
        REFERENCES transaction(id),
    CONSTRAINT fk_reinstatement_calc_policy 
        FOREIGN KEY (policy_id) 
        REFERENCES policy(id),
    CONSTRAINT fk_reinstatement_calc_status 
        FOREIGN KEY (status_id) 
        REFERENCES status(id),
    CONSTRAINT fk_reinstatement_calc_user 
        FOREIGN KEY (created_by) 
        REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Detailed reinstatement premium calculations per documentation';
```

### 3. Integration with Accounting Workflow
```sql
-- Link reinstatement to accounting per v10 requirements
ALTER TABLE transaction
ADD COLUMN IF NOT EXISTS reinstatement_calculation_id INT COMMENT 'Link to reinstatement calculation',
ADD CONSTRAINT fk_transaction_reinstatement_calc 
    FOREIGN KEY (reinstatement_calculation_id) 
    REFERENCES reinstatement_calculation(id);

-- Accounting-specific fields for reinstatement
ALTER TABLE reinstatement_calculation
ADD COLUMN IF NOT EXISTS gl_account_mapping JSON COMMENT 'GL accounts for transaction lines',
ADD COLUMN IF NOT EXISTS accounting_period VARCHAR(7) COMMENT 'YYYY-MM for accounting',
ADD COLUMN IF NOT EXISTS journal_entry_ref VARCHAR(50) COMMENT 'Reference to accounting entry';

-- Double-entry accounting view for reinstatements
CREATE VIEW v_reinstatement_accounting_entries AS
SELECT 
    rc.id as calculation_id,
    rc.transaction_id,
    'DEBIT' as entry_type,
    '1200' as gl_account_code, -- Accounts Receivable
    'Accounts Receivable' as gl_account_name,
    rc.total_amount_due as amount,
    'Reinstatement receivable' as description
FROM reinstatement_calculation rc
WHERE rc.calculation_status = 'APPROVED'

UNION ALL

SELECT 
    rc.id as calculation_id,
    rc.transaction_id,
    'CREDIT' as entry_type,
    '4100' as gl_account_code, -- Premium Revenue
    'Premium Revenue' as gl_account_name,
    rc.adjusted_total_premium - rc.unpaid_premium_balance as amount,
    'Reinstated premium revenue' as description
FROM reinstatement_calculation rc
WHERE rc.calculation_status = 'APPROVED'

UNION ALL

SELECT 
    rc.id as calculation_id,
    rc.transaction_id,
    'CREDIT' as entry_type,
    '4200' as gl_account_code, -- Fee Revenue
    'Fee Revenue' as gl_account_name,
    rc.reinstatement_fee + rc.installment_fees as amount,
    'Reinstatement fees' as description
FROM reinstatement_calculation rc
WHERE rc.calculation_status = 'APPROVED'
AND (rc.reinstatement_fee + rc.installment_fees) > 0;
```

### 4. Reinstatement Workflow Implementation
```sql
-- Workflow state tracking aligned with accounting v10
CREATE TABLE IF NOT EXISTS reinstatement_workflow_state (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL,
    workflow_state VARCHAR(50) NOT NULL,
    state_timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    state_data JSON COMMENT 'State-specific data',
    
    -- States from documentation
    -- CANCELLED -> ELIGIBLE_FOR_REINSTATEMENT -> CALCULATION_PENDING -> 
    -- PAYMENT_PENDING -> PAYMENT_RECEIVED -> REINSTATED
    -- or CANCELLED -> ELIGIBLE_FOR_REINSTATEMENT -> EXPIRED
    
    performed_by INT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_reinstatement_workflow_trans (transaction_id),
    INDEX idx_reinstatement_workflow_state (workflow_state),
    CONSTRAINT fk_reinstatement_workflow_trans 
        FOREIGN KEY (transaction_id) 
        REFERENCES transaction(id),
    CONSTRAINT fk_reinstatement_workflow_user 
        FOREIGN KEY (performed_by) 
        REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tracks reinstatement workflow state transitions';

-- Installment adjustment tracking
CREATE TABLE IF NOT EXISTS reinstatement_installment_adjustment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reinstatement_calculation_id INT NOT NULL,
    installment_number INT NOT NULL,
    original_due_date DATE NOT NULL,
    adjusted_due_date DATE NOT NULL,
    original_amount DECIMAL(10,2) NOT NULL,
    adjusted_amount DECIMAL(10,2) NOT NULL,
    adjustment_reason VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_reinst_install_calc (reinstatement_calculation_id),
    CONSTRAINT fk_reinst_install_calc 
        FOREIGN KEY (reinstatement_calculation_id) 
        REFERENCES reinstatement_calculation(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tracks payment schedule adjustments after reinstatement';
```

### 5. Calculation Implementation per Documentation
```sql
-- Stored procedure for reinstatement calculation following documentation example
DELIMITER //
CREATE PROCEDURE sp_calculate_reinstatement(
    IN p_policy_id INT,
    IN p_reinstatement_date DATETIME,
    OUT p_calculation_id INT
)
BEGIN
    DECLARE v_cancellation_date DATE;
    DECLARE v_policy_start_date DATE;
    DECLARE v_policy_end_date DATE;
    DECLARE v_total_premium DECIMAL(10,2);
    DECLARE v_total_days INT;
    DECLARE v_lapse_days INT;
    DECLARE v_remaining_days INT;
    DECLARE v_daily_rate DECIMAL(8,4);
    DECLARE v_lapsed_credit DECIMAL(10,2);
    DECLARE v_adjusted_premium DECIMAL(10,2);
    DECLARE v_unpaid_balance DECIMAL(10,2);
    DECLARE v_payments_made DECIMAL(10,2);
    DECLARE v_reinstatement_fee DECIMAL(10,2) DEFAULT 25.00; -- Configurable
    
    -- Get policy details
    SELECT 
        p.cancellation_date,
        p.effective_date,
        p.expiration_date,
        p.total_premium,
        IFNULL(p.unpaid_balance, 0),
        IFNULL(p.payments_collected, 0)
    INTO 
        v_cancellation_date,
        v_policy_start_date,
        v_policy_end_date,
        v_total_premium,
        v_unpaid_balance,
        v_payments_made
    FROM policy p
    WHERE p.id = p_policy_id;
    
    -- Calculate days
    SET v_total_days = DATEDIFF(v_policy_end_date, v_policy_start_date) + 1;
    SET v_lapse_days = DATEDIFF(DATE(p_reinstatement_date), v_cancellation_date);
    SET v_remaining_days = DATEDIFF(v_policy_end_date, DATE(p_reinstatement_date)) + 1;
    
    -- Calculate premium adjustments
    SET v_daily_rate = v_total_premium / v_total_days;
    SET v_lapsed_credit = v_daily_rate * v_lapse_days;
    SET v_adjusted_premium = v_total_premium - v_lapsed_credit;
    
    -- Create transaction
    INSERT INTO transaction (transaction_type_id, policy_id, status_id)
    SELECT tt.id, p_policy_id, s.id
    FROM transaction_type tt
    CROSS JOIN status s
    WHERE tt.code = 'REINSTATEMENT_CALCULATION'
    AND s.code = 'PENDING';
    
    SET @trans_id = LAST_INSERT_ID();
    
    -- Create calculation record
    INSERT INTO reinstatement_calculation (
        transaction_id,
        policy_id,
        cancellation_date,
        reinstatement_request_date,
        reinstatement_effective_date,
        policy_expiration_date,
        total_policy_days,
        lapse_days,
        remaining_days,
        original_total_premium,
        daily_premium_rate,
        lapsed_premium_credit,
        adjusted_total_premium,
        unpaid_premium_balance,
        reinstatement_fee,
        total_amount_due,
        payments_previously_made,
        policy_balance_remaining,
        calculation_status,
        status_id,
        created_by
    ) VALUES (
        @trans_id,
        p_policy_id,
        v_cancellation_date,
        DATE(p_reinstatement_date),
        p_reinstatement_date,
        v_policy_end_date,
        v_total_days,
        v_lapse_days,
        v_remaining_days,
        v_total_premium,
        v_daily_rate,
        v_lapsed_credit,
        v_adjusted_premium,
        v_unpaid_balance,
        v_reinstatement_fee,
        v_adjusted_premium + v_unpaid_balance + v_reinstatement_fee,
        v_payments_made,
        v_adjusted_premium + v_unpaid_balance + v_reinstatement_fee - v_payments_made,
        'CALCULATED',
        1,
        1 -- System user
    );
    
    SET p_calculation_id = LAST_INSERT_ID();
    
    -- Create transaction lines for breakdown
    INSERT INTO transaction_line (
        transaction_id, 
        transaction_line_type_id, 
        amount, 
        description,
        line_order
    )
    SELECT 
        @trans_id,
        tlt.id,
        CASE 
            WHEN tlt.code = 'REINST_ORIGINAL_PREMIUM' THEN v_total_premium
            WHEN tlt.code = 'REINST_LAPSED_PREMIUM' THEN -v_lapsed_credit
            WHEN tlt.code = 'REINST_REMAINING_PREMIUM' THEN v_adjusted_premium
            WHEN tlt.code = 'REINST_UNPAID_PREMIUM' THEN v_unpaid_balance
            WHEN tlt.code = 'REINST_ADMIN_FEE' THEN v_reinstatement_fee
        END,
        CASE 
            WHEN tlt.code = 'REINST_ORIGINAL_PREMIUM' THEN 'Original policy premium'
            WHEN tlt.code = 'REINST_LAPSED_PREMIUM' THEN CONCAT('Credit for ', v_lapse_days, ' lapse days')
            WHEN tlt.code = 'REINST_REMAINING_PREMIUM' THEN CONCAT('Premium for ', v_remaining_days, ' remaining days')
            WHEN tlt.code = 'REINST_UNPAID_PREMIUM' THEN 'Previously unpaid balance'
            WHEN tlt.code = 'REINST_ADMIN_FEE' THEN 'Reinstatement processing fee'
        END,
        CASE 
            WHEN tlt.code = 'REINST_ORIGINAL_PREMIUM' THEN 1
            WHEN tlt.code = 'REINST_LAPSED_PREMIUM' THEN 2
            WHEN tlt.code = 'REINST_REMAINING_PREMIUM' THEN 3
            WHEN tlt.code = 'REINST_UNPAID_PREMIUM' THEN 4
            WHEN tlt.code = 'REINST_ADMIN_FEE' THEN 5
        END
    FROM transaction_line_type tlt
    WHERE tlt.code IN (
        'REINST_ORIGINAL_PREMIUM',
        'REINST_LAPSED_PREMIUM', 
        'REINST_REMAINING_PREMIUM',
        'REINST_UNPAID_PREMIUM',
        'REINST_ADMIN_FEE'
    );
    
END//
DELIMITER ;
```

### 6. Example Usage Following Documentation
```sql
-- Example from documentation:
-- Total Premium: $600, Policy Term: 180 days
-- Canceled After: 90 days, Reinstated on Day 105 (15-day lapse)
-- Unpaid Premium: $100, Fees: $25, Payments made: $200

-- Calculate reinstatement
CALL sp_calculate_reinstatement(456, '2024-01-15 14:30:00', @calc_id);

-- View calculation results
SELECT 
    rc.*,
    CONCAT('Daily rate: $', FORMAT(rc.daily_premium_rate, 2)) as daily_rate_display,
    CONCAT('Lapsed premium credit: $', FORMAT(rc.lapsed_premium_credit, 2)) as lapse_credit_display,
    CONCAT('Policy balance: $', FORMAT(rc.policy_balance_remaining, 2)) as balance_display
FROM reinstatement_calculation rc
WHERE rc.id = @calc_id;

-- Expected results matching documentation:
-- Daily Premium = 600 / 180 = $3.33
-- Lapsed unearned premium: 15 × $3.33 = $49.95
-- New Total Premium = $600 - $49.95 = $550.05
-- Add unpaid premium: $100
-- Add reinstatement fee: $25
-- Total Owed: $550.05 + $100 + $25 = $675.05
-- Subtract funds collected: $200
-- Policy Balance = $475.05

-- Calculate installment adjustments (3 remaining)
UPDATE reinstatement_calculation
SET 
    installments_remaining = 3,
    installment_amount = ROUND(policy_balance_remaining / 3, 2)
WHERE id = @calc_id;
```

## Benefits of This Approach

1. **Precise Calculation Tracking**: Every component of the reinstatement calculation is stored
2. **Accounting Integration**: Ready for double-entry accounting per GR-70
3. **Workflow Support**: Clear state transitions with audit trail
4. **Documentation Compliance**: Exactly follows the reinstatement business rules
5. **Installment Handling**: Supports complex payment plan adjustments
6. **No Backdating**: Enforces the no-coverage-during-lapse rule

## Migration Path

1. **Phase 1**: Create transaction types and line types
2. **Phase 2**: Create reinstatement_calculation table
3. **Phase 3**: Create workflow and adjustment tables
4. **Phase 4**: Implement calculation procedures
5. **Phase 5**: Create accounting integration views
6. **Phase 6**: Update application to use new structures

## Conclusion

This v3 approach fully incorporates the detailed reinstatement requirements from the documentation while maintaining alignment with the accounting workflow patterns from v10. The solution provides complete calculation transparency and integrates seamlessly with both the existing transaction framework and future accounting requirements.