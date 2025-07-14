# Accounting Infrastructure Support Documentation - Updated

## Executive Summary

This updated document incorporates comprehensive feedback from plan.md, plan2.md, and plan3.md to outline the supporting infrastructure required for implementing the 9 Global Requirements (GR-54 through GR-62) for accounting functionality. The analysis emphasizes maximum integration with existing infrastructure, database consolidation strategies, and comprehensive accounting capabilities including check printing and Positive Pay processing.

## 1. Database Schema Extensions - Updated

### 1.1 Core Financial Tables (Consolidated Approach)

#### Extend Transaction Table (Existing)
```sql
-- Add accounting-specific fields to existing transaction table
ALTER TABLE transaction ADD COLUMN transaction_subtype VARCHAR(50) AFTER transaction_type;
ALTER TABLE transaction ADD COLUMN account_code VARCHAR(20) NULL AFTER transaction_subtype;
ALTER TABLE transaction ADD COLUMN effective_date DATE NULL AFTER account_code;
ALTER TABLE transaction ADD COLUMN is_posted BOOLEAN DEFAULT FALSE AFTER effective_date;
ALTER TABLE transaction ADD COLUMN posted_at TIMESTAMP NULL AFTER is_posted;
ALTER TABLE transaction ADD COLUMN posted_by BIGINT UNSIGNED NULL AFTER posted_at;

-- New transaction types for accounting (consolidated approach)
INSERT INTO transaction_type (code, name, description) VALUES
('PREMIUM', 'Premium Transaction', 'Policy premium transactions'),
('PREMIUM_ADJ', 'Premium Adjustment', 'Policy premium adjustments and corrections'),
('REINSTATEMENT', 'Reinstatement Premium', 'Policy reinstatement premium adjustment'),
('SR22_FEE', 'SR22 Filing Fee', 'SR22 financial responsibility filing fee'),
('SR26_FEE', 'SR26 Cancellation Fee', 'SR22 cancellation processing fee'),
('COMMISSION', 'Commission Payment', 'Producer commission payments'),
('CHARGEBACK', 'Payment Chargeback', 'Payment chargeback processing'),
('REFUND', 'Customer Refund', 'Customer refund processing'),
('LATE_FEE', 'Late Payment Fee', 'Late payment penalty fees'),
('NSF_FEE', 'NSF Fee', 'Non-sufficient funds fee'),
('INSTALLMENT_FEE', 'Installment Fee', 'Payment plan installment fee'),
('ADJUSTMENT_MANUAL', 'Manual Adjustment', 'Administrative manual adjustments'),
('PAYMENT', 'Payment Receipt', 'Customer payment receipts'),
('FEE', 'General Fee', 'General fees and charges');

-- Add foreign key for posted_by
ALTER TABLE transaction ADD FOREIGN KEY (posted_by) REFERENCES user(id);
```

#### Transaction Line Table (Double-Entry Foundation)
```sql
-- Use transaction_line for double-entry accounting details
CREATE TABLE transaction_line (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_id BIGINT UNSIGNED NOT NULL,
    account_id BIGINT UNSIGNED NOT NULL,
    line_description VARCHAR(255) NOT NULL,
    debit_amount DECIMAL(10,2) DEFAULT 0,
    credit_amount DECIMAL(10,2) DEFAULT 0,
    component_type VARCHAR(50) NULL, -- PREMIUM, FEE, TAX, COMMISSION
    line_order INTEGER NOT NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (account_id) REFERENCES chart_of_accounts(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_transaction (transaction_id),
    INDEX idx_account (account_id),
    INDEX idx_component_type (component_type),
    
    CONSTRAINT chk_debit_credit CHECK (
        (debit_amount > 0 AND credit_amount = 0) OR 
        (credit_amount > 0 AND debit_amount = 0)
    )
);
```

#### Chart of Accounts
```sql
-- Chart of Accounts (unchanged from original)
CREATE TABLE chart_of_accounts (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    account_code VARCHAR(20) UNIQUE NOT NULL,
    account_name VARCHAR(100) NOT NULL,
    account_type_id BIGINT UNSIGNED NOT NULL,
    parent_account_id BIGINT UNSIGNED NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_system_account BOOLEAN DEFAULT FALSE,
    normal_balance ENUM('DEBIT', 'CREDIT') NOT NULL,
    description TEXT NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (account_type_id) REFERENCES account_type(id),
    FOREIGN KEY (parent_account_id) REFERENCES chart_of_accounts(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_account_code (account_code),
    INDEX idx_account_type (account_type_id),
    INDEX idx_parent_account (parent_account_id)
);
```

### 1.2 Payment Plan and Installment Tables
```sql
-- Payment Plans (updated from payment_schedule to payment_plan)
CREATE TABLE payment_plan (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    policy_id BIGINT UNSIGNED NOT NULL,
    plan_type_id BIGINT UNSIGNED NOT NULL,
    total_premium DECIMAL(10,2) NOT NULL,
    down_payment_amount DECIMAL(10,2) NOT NULL,
    number_of_installments INTEGER NOT NULL,
    installment_fee DECIMAL(10,2) DEFAULT 0,
    start_date DATE NOT NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (plan_type_id) REFERENCES payment_plan_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_policy (policy_id),
    INDEX idx_plan_type (plan_type_id),
    INDEX idx_start_date (start_date)
);

-- Payment Plan Types
CREATE TABLE payment_plan_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    down_payment_percentage DECIMAL(5,2) NOT NULL,
    max_installments INTEGER NOT NULL,
    installment_fee DECIMAL(10,2) DEFAULT 0,
    description TEXT NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_code (code)
);

-- Installments
CREATE TABLE installment (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    payment_plan_id BIGINT UNSIGNED NOT NULL,
    installment_number INTEGER NOT NULL,
    due_date DATE NOT NULL,
    premium_amount DECIMAL(10,2) NOT NULL,
    fee_amount DECIMAL(10,2) DEFAULT 0,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    paid_amount DECIMAL(10,2) DEFAULT 0,
    balance_amount DECIMAL(10,2) NOT NULL,
    is_paid BOOLEAN DEFAULT FALSE,
    paid_date DATE NULL,
    late_fee_amount DECIMAL(10,2) DEFAULT 0,
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (payment_plan_id) REFERENCES payment_plan(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_payment_plan (payment_plan_id),
    INDEX idx_due_date (due_date),
    INDEX idx_installment_number (installment_number),
    INDEX idx_is_paid (is_paid),
    
    UNIQUE KEY uk_plan_installment (payment_plan_id, installment_number)
);
```

### 1.3 Payment Allocation Table - EXPLAINED
```sql
-- Payment Allocation (remains separate - cannot be consolidated)
CREATE TABLE payment_allocation (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    payment_transaction_id BIGINT UNSIGNED NOT NULL,
    invoice_id BIGINT UNSIGNED NULL,
    installment_id BIGINT UNSIGNED NULL,
    policy_id BIGINT UNSIGNED NULL,
    allocated_amount DECIMAL(10,2) NOT NULL,
    allocation_date DATE NOT NULL,
    allocation_type ENUM('INVOICE', 'INSTALLMENT', 'PREPAYMENT', 'CREDIT') NOT NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (payment_transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (invoice_id) REFERENCES invoice(id),
    FOREIGN KEY (installment_id) REFERENCES installment(id),
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_payment_transaction (payment_transaction_id),
    INDEX idx_invoice (invoice_id),
    INDEX idx_installment (installment_id),
    INDEX idx_allocation_date (allocation_date)
);

/*
WHY PAYMENT_ALLOCATION CANNOT BE CONSOLIDATED WITH TRANSACTION:
1. Different Business Purpose: Payment allocation tracks how a single payment 
   is distributed across multiple invoices/installments, while transactions 
   record individual financial events.

2. Complex Relationships: One payment may cover multiple invoices, partial 
   payments, prepayments, or credits requiring detailed allocation tracking.

3. Example Scenario: 
   - Customer pays $500
   - Allocation 1: $300 to Invoice A
   - Allocation 2: $200 to Invoice B
   - Transaction records the $500 payment
   - Allocations track the distribution

4. Reporting Requirements: Insurance regulations require detailed tracking 
   of how payments are applied to specific coverage periods and charges.

5. Performance: Separate table optimizes queries for payment application 
   logic and receivables management.
*/
```

### 1.4 Commission Management Tables - UPDATED STRUCTURE
```sql
-- Commission Types
CREATE TABLE commission_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT NULL,
    calculation_method ENUM('PERCENTAGE', 'FLAT_FEE', 'TIERED') NOT NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_code (code)
);

-- Commission Schedules  
CREATE TABLE commission_schedule (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    payment_frequency ENUM('IMMEDIATE', 'MONTHLY', 'QUARTERLY', 'ANNUALLY') NOT NULL,
    payment_delay_days INTEGER DEFAULT 0,
    description TEXT NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_code (code)
);

-- Commission (individual commission calculations)
CREATE TABLE commission (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    policy_id BIGINT UNSIGNED NOT NULL,
    producer_id BIGINT UNSIGNED NOT NULL,
    commission_type_id BIGINT UNSIGNED NOT NULL,
    commission_schedule_id BIGINT UNSIGNED NOT NULL,
    transaction_id BIGINT UNSIGNED NULL, -- Links to commission payment transaction
    premium_amount DECIMAL(10,2) NOT NULL,
    commission_rate DECIMAL(8,4) NOT NULL,
    commission_amount DECIMAL(10,2) NOT NULL,
    earned_date DATE NOT NULL,
    payment_date DATE NULL,
    is_paid BOOLEAN DEFAULT FALSE,
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (producer_id) REFERENCES producer(id),
    FOREIGN KEY (commission_type_id) REFERENCES commission_type(id),
    FOREIGN KEY (commission_schedule_id) REFERENCES commission_schedule(id),
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_policy (policy_id),
    INDEX idx_producer (producer_id),
    INDEX idx_earned_date (earned_date),
    INDEX idx_payment_date (payment_date),
    INDEX idx_is_paid (is_paid)
);

-- Map Producer Commission (program-specific commission rates)
CREATE TABLE map_producer_commission (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    producer_id BIGINT UNSIGNED NOT NULL,
    program_id BIGINT UNSIGNED NOT NULL,
    commission_type_id BIGINT UNSIGNED NOT NULL,
    commission_schedule_id BIGINT UNSIGNED NOT NULL,
    commission_rate DECIMAL(8,4) NOT NULL,
    effective_date DATE NOT NULL,
    expiration_date DATE NULL,
    is_default BOOLEAN DEFAULT FALSE,
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (producer_id) REFERENCES producer(id),
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (commission_type_id) REFERENCES commission_type(id),
    FOREIGN KEY (commission_schedule_id) REFERENCES commission_schedule(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_producer (producer_id),
    INDEX idx_program (program_id),
    INDEX idx_effective_date (effective_date),
    UNIQUE KEY uk_producer_program_date (producer_id, program_id, effective_date)
);

/*
COMMISSION BUSINESS RULES (from feedback):
1. Commission clawback: NO - No recovery on mid-term cancellations
2. Multi-level commission splits: NO - Single producer per policy
3. Program-specific defaults + special producer rates supported
4. Percentage-based calculations only (no flat fees initially)
*/
```

### 1.5 Check Processing Tables - NEW
```sql
-- Check Stock Management
CREATE TABLE check_stock (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    stock_name VARCHAR(100) NOT NULL,
    starting_check_number BIGINT NOT NULL,
    ending_check_number BIGINT NOT NULL,
    current_check_number BIGINT NOT NULL,
    checks_remaining INTEGER NOT NULL,
    check_format ENUM('STANDARD', 'VOUCHER', 'LASER') NOT NULL,
    micr_encoding VARCHAR(100) NOT NULL, -- Bank routing and account information
    is_active BOOLEAN DEFAULT TRUE,
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_check_number_range (starting_check_number, ending_check_number),
    INDEX idx_current_check_number (current_check_number)
);

-- Signature Storage for Manual Check Signing
CREATE TABLE signature (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    signature_title VARCHAR(100) NOT NULL, -- e.g., "CFO", "Treasurer"
    signature_image_path VARCHAR(500) NOT NULL,
    image_format ENUM('PNG', 'JPG', 'PDF') NOT NULL,
    image_width INTEGER NOT NULL,
    image_height INTEGER NOT NULL,
    file_size INTEGER NOT NULL,
    effective_date DATE NOT NULL,
    expiration_date DATE NULL,
    is_active BOOLEAN DEFAULT TRUE,
    approval_required BOOLEAN DEFAULT TRUE,
    approved_by BIGINT UNSIGNED NULL,
    approved_at TIMESTAMP NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (approved_by) REFERENCES user(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_user (user_id),
    INDEX idx_effective_date (effective_date),
    INDEX idx_is_active (is_active)
);

-- Check Register
CREATE TABLE check_register (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    check_number BIGINT UNIQUE NOT NULL,
    check_stock_id BIGINT UNSIGNED NOT NULL,
    transaction_id BIGINT UNSIGNED NOT NULL,
    payee_name VARCHAR(200) NOT NULL,
    payee_address TEXT NULL,
    check_amount DECIMAL(10,2) NOT NULL,
    check_memo VARCHAR(200) NULL,
    issue_date DATE NOT NULL,
    signature_id BIGINT UNSIGNED NOT NULL,
    print_date DATE NULL,
    printed_by BIGINT UNSIGNED NULL,
    is_void BOOLEAN DEFAULT FALSE,
    void_reason TEXT NULL,
    void_date DATE NULL,
    void_by BIGINT UNSIGNED NULL,
    clear_date DATE NULL,
    clear_amount DECIMAL(10,2) NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (check_stock_id) REFERENCES check_stock(id),
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (signature_id) REFERENCES signature(id),
    FOREIGN KEY (printed_by) REFERENCES user(id),
    FOREIGN KEY (void_by) REFERENCES user(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_check_number (check_number),
    INDEX idx_issue_date (issue_date),
    INDEX idx_payee_name (payee_name),
    INDEX idx_is_void (is_void)
);
```

### 1.6 Positive Pay Processing Tables - LIMITED SCOPE
```sql
-- Positive Pay Export (Daily exports to Sunflower Bank)
CREATE TABLE positive_pay_export (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    export_date DATE NOT NULL,
    file_name VARCHAR(200) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    check_count INTEGER NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    starting_check_number BIGINT NOT NULL,
    ending_check_number BIGINT NOT NULL,
    file_format ENUM('NACHA', 'CSV', 'FIXED_WIDTH') NOT NULL,
    transmission_method ENUM('SFTP', 'EMAIL', 'PORTAL') NOT NULL,
    transmitted_at TIMESTAMP NULL,
    transmitted_by BIGINT UNSIGNED NULL,
    bank_acknowledgment_received BOOLEAN DEFAULT FALSE,
    acknowledgment_date DATE NULL,
    exceptions_count INTEGER DEFAULT 0,
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (transmitted_by) REFERENCES user(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_export_date (export_date),
    INDEX idx_file_name (file_name),
    INDEX idx_transmitted_at (transmitted_at),
    UNIQUE KEY uk_export_date (export_date)
);

/*
POSITIVE_PAY_EXPORT TABLE PURPOSE:
- Tracks daily exports of issued checks to Sunflower Bank for fraud prevention
- Export tracking: File name, generation date, number of checks, total amount
- Bank reconciliation: Verification that exported checks match bank records
- Exception handling: Track checks that don't clear or are flagged by the bank
- Audit trail: Complete history of all Positive Pay file transmissions
*/

-- ACH File (For Positive Pay processing only - not full ACH)
CREATE TABLE ach_file (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    positive_pay_export_id BIGINT UNSIGNED NOT NULL,
    file_name VARCHAR(200) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    creation_date DATE NOT NULL,
    transmission_date DATE NULL,
    record_count INTEGER NOT NULL,
    file_size INTEGER NOT NULL, -- bytes
    nacha_format_version VARCHAR(10) NOT NULL DEFAULT '8.2',
    immediate_destination VARCHAR(10) NOT NULL, -- Bank routing number
    immediate_origin VARCHAR(10) NOT NULL, -- Company identification
    file_control_total DECIMAL(15,2) NOT NULL,
    transmission_status ENUM('PENDING', 'TRANSMITTED', 'ACKNOWLEDGED', 'REJECTED', 'FAILED') NOT NULL,
    bank_response_code VARCHAR(10) NULL,
    bank_response_message TEXT NULL,
    retry_count INTEGER DEFAULT 0,
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (positive_pay_export_id) REFERENCES positive_pay_export(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_positive_pay_export (positive_pay_export_id),
    INDEX idx_creation_date (creation_date),
    INDEX idx_transmission_status (transmission_status)
);

/*
ACH_FILE TABLE PURPOSE:
- Tracks ACH file transmissions to Sunflower Bank for Positive Pay processing only
- File metadata: File name, creation date, transmission status, record count
- Transmission tracking: SFTP upload confirmation, bank acknowledgment
- Error handling: Track failed transmissions, retries, and resolution
- Compliance: Maintain required records for ACH processing regulations
*/

-- ACH Transaction (Individual Positive Pay transactions)
CREATE TABLE ach_transaction (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ach_file_id BIGINT UNSIGNED NOT NULL,
    check_register_id BIGINT UNSIGNED NOT NULL,
    transaction_code VARCHAR(3) NOT NULL, -- ACH transaction code
    check_number BIGINT NOT NULL,
    check_amount DECIMAL(10,2) NOT NULL,
    account_number VARCHAR(17) NOT NULL, -- Masked for security
    routing_number VARCHAR(9) NOT NULL,
    payee_name VARCHAR(22) NOT NULL, -- NACHA field limit
    addenda_information VARCHAR(80) NULL,
    trace_number VARCHAR(15) NOT NULL,
    settlement_date DATE NULL,
    return_code VARCHAR(3) NULL, -- ACH return reason code
    return_description VARCHAR(100) NULL,
    status ENUM('PENDING', 'TRANSMITTED', 'SETTLED', 'RETURNED', 'FAILED') NOT NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (ach_file_id) REFERENCES ach_file(id),
    FOREIGN KEY (check_register_id) REFERENCES check_register(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_ach_file (ach_file_id),
    INDEX idx_check_register (check_register_id),
    INDEX idx_check_number (check_number),
    INDEX idx_settlement_date (settlement_date),
    INDEX idx_status (status)
);

/*
ACH_TRANSACTION TABLE PURPOSE:
- Individual ACH transaction details within each Positive Pay file
- Transaction details: Amount, account information, transaction code, addenda
- Status tracking: Pending, transmitted, settled, returned, failed
- Return processing: NSF, account closed, invalid account handling
- Reconciliation: Match ACH settlements with bank confirmations

CONSOLIDATION ANALYSIS: This table should remain separate from the main transaction table because:
1. ACH processing has specific data elements (SEC codes, addenda records, trace numbers)
2. Different lifecycle from accounting transactions (NACHA processing requirements)
3. Regulatory reporting requirements specific to ACH and Positive Pay
4. Performance optimization for ACH file generation and bank reconciliation
5. Limited scope: Only for Positive Pay, not general ACH processing
*/
```

### 1.7 Reinstatement Integration Tables (GR-64) - UNCHANGED
```sql
-- Reinstatement Calculations (from GR-64)
CREATE TABLE reinstatement_calculation (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    policy_id BIGINT UNSIGNED NOT NULL,
    cancellation_date DATE NOT NULL,
    reinstatement_date DATE NOT NULL,
    lapse_days INTEGER NOT NULL,
    original_premium DECIMAL(10,2) NOT NULL,
    daily_premium_rate DECIMAL(8,4) NOT NULL,
    lapsed_premium DECIMAL(10,2) NOT NULL,
    adjusted_premium DECIMAL(10,2) NOT NULL,
    unpaid_premium DECIMAL(10,2) DEFAULT 0,
    reinstatement_fees DECIMAL(10,2) DEFAULT 0,
    total_due DECIMAL(10,2) NOT NULL,
    transaction_id BIGINT UNSIGNED NULL, -- Links to reinstatement transaction
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_policy (policy_id),
    INDEX idx_reinstatement_date (reinstatement_date),
    INDEX idx_cancellation_date (cancellation_date)
);
```

### 1.8 SR22 Fee Management Tables (GR-10) - UNCHANGED
```sql
-- SR22 Fee Schedules
CREATE TABLE sr22_fee_schedule (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    state_id BIGINT UNSIGNED NOT NULL,
    fee_type_id BIGINT UNSIGNED NOT NULL,
    filing_fee DECIMAL(10,2) NOT NULL,
    processing_fee DECIMAL(10,2) DEFAULT 0,
    effective_date DATE NOT NULL,
    expiration_date DATE NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (state_id) REFERENCES state(id),
    FOREIGN KEY (fee_type_id) REFERENCES sr22_fee_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_state (state_id),
    INDEX idx_fee_type (fee_type_id),
    INDEX idx_effective_date (effective_date)
);

-- SR22 Fee Types
CREATE TABLE sr22_fee_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT NULL,
    is_recurring BOOLEAN DEFAULT FALSE,
    billing_frequency_months INTEGER NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_code (code)
);

-- SR22 Fee Transactions
CREATE TABLE sr22_fee_transaction (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    policy_id BIGINT UNSIGNED NOT NULL,
    sr22_filing_id BIGINT UNSIGNED NOT NULL,
    fee_schedule_id BIGINT UNSIGNED NOT NULL,
    transaction_id BIGINT UNSIGNED NOT NULL,
    fee_amount DECIMAL(10,2) NOT NULL,
    processing_fee DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    transaction_date DATE NOT NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (sr22_filing_id) REFERENCES sr22_filing(id),
    FOREIGN KEY (fee_schedule_id) REFERENCES sr22_fee_schedule(id),
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_policy (policy_id),
    INDEX idx_sr22_filing (sr22_filing_id),
    INDEX idx_transaction_date (transaction_date)
);
```

### 1.9 Reference Tables
```sql
-- Account Types
CREATE TABLE account_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT NULL,
    financial_statement_category ENUM('ASSET', 'LIABILITY', 'EQUITY', 'REVENUE', 'EXPENSE') NOT NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_code (code),
    INDEX idx_category (financial_statement_category)
);

-- Manual Payment Types (for outage scenarios)
CREATE TABLE manual_payment_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT NULL,
    requires_approval BOOLEAN DEFAULT TRUE,
    validation_rules JSON NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_code (code)
);
```

## 2. Service Layer Architecture - Updated

### 2.1 Core Accounting Services
```php
namespace App\Services\Accounting;

// Core Accounting Service (Enhanced with Manual Processing)
class AccountingService
{
    public function __construct(
        private PaymentService $paymentService,
        private EmailService $emailService,
        private ReinstatementService $reinstatementService,
        private TransactionService $transactionService,
        private ChartOfAccountsService $chartOfAccountsService,
        private ManualPaymentService $manualPaymentService
    ) {}
    
    // Enhanced accounting operations
    public function processPayment(Payment $payment): Transaction;
    public function processRefund(Refund $refund): Transaction;
    public function processChargeback(Chargeback $chargeback): Transaction;
    public function calculateCommissions(Policy $policy): array;
    public function generateFinancialStatement(Carbon $startDate, Carbon $endDate): array;
    
    // NEW: Manual payment processing for outages
    public function recordManualPayment(array $data): ManualPayment;
    public function processManualPaymentBatch(Collection $manualPayments): array;
}

// Transaction Service (Replaces JournalEntryService)
class TransactionService
{
    public function createTransaction(array $data): Transaction;
    public function addTransactionLine(Transaction $transaction, array $lineData): TransactionLine;
    public function postTransaction(Transaction $transaction): bool;
    public function reverseTransaction(Transaction $transaction, string $reason): Transaction;
    public function validateBalance(Transaction $transaction): bool;
    
    // NEW: Enhanced transaction processing
    public function createDoubleEntryTransaction(array $entries): Transaction;
    public function bulkPostTransactions(Collection $transactions): array;
}

// Payment Plan Service (Enhanced)
class PaymentPlanService
{
    public function createPaymentPlan(Policy $policy, array $planData): PaymentPlan;
    public function generateInstallments(PaymentPlan $plan): Collection;
    public function processPaymentToInstallment(Payment $payment): array;
    public function restructureForReinstatement(PaymentPlan $plan, ReinstatementCalculation $calc): PaymentPlan;
    
    // NEW: Enhanced installment management
    public function calculateLateFees(Collection $overdueInstallments): array;
    public function applyPaymentAllocation(Payment $payment, array $allocations): Collection;
}

// Commission Service (Updated Structure)
class CommissionService
{
    public function calculateCommission(Policy $policy, Producer $producer): Commission;
    public function processCommissionPayment(Commission $commission): Transaction;
    public function generateCommissionStatement(Producer $producer, Carbon $startDate, Carbon $endDate): array;
    public function getCommissionSchedule(Producer $producer, Program $program): CommissionSchedule;
    
    // NEW: Program-specific commission handling
    public function getDefaultCommissionRate(Program $program): Decimal;
    public function getProducerSpecificRate(Producer $producer, Program $program): Decimal;
    public function processMonthlyCommissions(): array;
    public function processQuarterlyCommissions(): array;
}

// Check Printing Service (NEW)
class CheckPrintingService
{
    public function __construct(
        private TransactionService $transactionService,
        private PositivePayService $positivePayService
    ) {}
    
    public function printCheck(Transaction $transaction, array $checkData): CheckRegister;
    public function getNextCheckNumber(CheckStock $stock): int;
    public function voidCheck(CheckRegister $check, string $reason): bool;
    public function getActiveSignature(User $user): Signature;
    public function generateCheckBatch(Collection $transactions): Collection;
    
    // Check stock management
    public function createCheckStock(array $stockData): CheckStock;
    public function updateCheckStock(CheckStock $stock): bool;
    public function trackCheckUsage(CheckStock $stock, int $checksUsed): bool;
}

// Positive Pay Service (NEW - LIMITED SCOPE)
class PositivePayService
{
    public function __construct(
        private UniversalEntityService $entityService,
        private CheckPrintingService $checkPrintingService
    ) {}
    
    // Positive Pay file generation (Sunflower Bank only)
    public function generateDailyPositivePayFile(Carbon $date): PositivePayExport;
    public function transmitPositivePayFile(PositivePayExport $export): bool;
    public function processPositivePayExceptions(array $exceptions): array;
    public function reconcilePositivePayFile(PositivePayExport $export): array;
    
    // NACHA file processing (Positive Pay only)
    public function generateNACHAFile(PositivePayExport $export): ACHFile;
    public function transmitACHFile(ACHFile $file): bool;
    public function processACHReturns(Collection $returns): array;
}

// Manual Payment Service (NEW - Outage Handling)
class ManualPaymentService
{
    public function __construct(
        private PaymentService $paymentService,
        private NotificationService $notificationService
    ) {}
    
    // Manual payment entry during Paysafe outages
    public function recordManualPayment(array $paymentData): ManualPayment;
    public function validateManualPayment(ManualPayment $payment): ValidationResult;
    public function approveManualPayment(ManualPayment $payment, User $approver): bool;
    public function processManualPaymentsBatch(Collection $payments): BatchResult;
    
    // Outage management
    public function detectPaymentOutage(): bool;
    public function notifyCustomersOfOutage(): bool;
    public function enableManualPaymentMode(): bool;
    public function disableManualPaymentMode(): bool;
}

// Billing Service (Enhanced)
class BillingService
{
    public function __construct(
        private TransactionService $transactionService,
        private NotificationService $notificationService,
        private PaymentPlanService $paymentPlanService
    ) {}
    
    public function generateInvoice(Policy $policy, array $charges): Invoice;
    public function sendBillingNotice(Policy $policy, Installment $installment): bool;
    public function processLateFees(Collection $overdueInstallments): array;
    public function sendReinstatementNotice(Policy $policy, ReinstatementCalculation $calc): bool;
    
    // NEW: Enhanced billing operations
    public function processMonthEndClose(): CloseResult; // 3 business days
    public function processYearEndClose(): CloseResult; // 7 business days
    public function generateTreatyReporting(string $frequency): array; // Monthly/Quarterly/Yearly
    public function lockAccountingPeriod(Carbon $periodEnd): bool;
}
```

### 2.2 Integration Services
```php
// Payment Gateway Service (Enhanced with Outage Handling)
class PaymentGatewayService
{
    public function __construct(
        private UniversalEntityService $entityService,
        private ManualPaymentService $manualPaymentService,
        private NotificationService $notificationService
    ) {}
    
    // Enhanced Paysafe integration
    public function processPayment(PaymentMethod $method, Decimal $amount): PaymentResult;
    public function verifyPaymentMethod(PaymentMethod $method): VerificationResult;
    public function handleChargeback(Payment $payment): ChargebackResult;
    public function processRefund(Payment $originalPayment, Decimal $amount): RefundResult;
    
    // NEW: Outage handling and graceful degradation
    public function checkGatewayStatus(): GatewayStatus;
    public function enableGracefulDegradation(): bool;
    public function disableGracefulDegradation(): bool;
    public function queuePaymentForProcessing(array $paymentData): QueuedPayment;
    public function processQueuedPayments(): BatchResult;
    
    // Customer communication during outages
    public function notifyPaymentOutage(array $customers): bool;
    public function notifyPaymentRestoration(array $customers): bool;
}

// Bank Integration Service (Enhanced for Positive Pay)
class BankIntegrationService
{
    public function __construct(
        private UniversalEntityService $entityService,
        private PositivePayService $positivePayService
    ) {}
    
    // Sunflower Bank integration (Positive Pay focus)
    public function submitPositivePayFile(PositivePayExport $export): PositivePayResult;
    public function receivePositivePayResponse(string $responseFile): array;
    public function reconcileBankStatement(BankStatement $statement): ReconciliationResult;
    
    // Future: Agent sweep ACH processing
    public function generateAgentSweepACH(Carbon $date): ACHFile;
    public function transmitACHFile(ACHFile $file): TransmissionResult;
}

// Notification Service (Enhanced for Outages)
class NotificationService
{
    public function __construct(
        private CommunicationService $communicationService
    ) {}
    
    // Outage notifications (configurable per program)
    public function notifyPaymentOutage(Collection $customers, Program $program): array;
    public function notifyPaymentRestoration(Collection $customers): array;
    public function sendPaymentStatusUpdate(Customer $customer, Payment $payment): bool;
    
    // Enhanced billing notifications
    public function sendInstallmentReminder(Installment $installment): bool;
    public function sendLateFeeNotice(Installment $installment): bool;
    public function sendReinstatementOpportunity(Policy $policy): bool;
}
```

## 3. API Endpoints (RESTful Extensions) - Updated

### 3.1 Accounting API Routes
```php
// In routes/api.php (following existing patterns)
Route::prefix('accounting')->middleware(['auth:sanctum'])->group(function () {
    // Core Accounting (using transaction table)
    Route::get('/transactions', [AccountingController::class, 'getTransactions']);
    Route::post('/transactions', [TransactionController::class, 'store']);
    Route::put('/transactions/{id}/post', [TransactionController::class, 'post']);
    Route::put('/transactions/{id}/reverse', [TransactionController::class, 'reverse']);
    
    // Chart of Accounts
    Route::get('/chart-of-accounts', [ChartOfAccountsController::class, 'index']);
    Route::post('/chart-of-accounts', [ChartOfAccountsController::class, 'store']);
    Route::put('/chart-of-accounts/{id}', [ChartOfAccountsController::class, 'update']);
    
    // Payment Plans
    Route::get('/payment-plans', [PaymentPlanController::class, 'index']);
    Route::post('/payment-plans', [PaymentPlanController::class, 'store']);
    Route::get('/payment-plans/{id}/installments', [PaymentPlanController::class, 'getInstallments']);
    Route::post('/payment-plans/{id}/restructure', [PaymentPlanController::class, 'restructure']);
    
    // Payment Allocation
    Route::get('/payment-allocations', [PaymentAllocationController::class, 'index']);
    Route::post('/payment-allocations', [PaymentAllocationController::class, 'store']);
    Route::get('/payments/{id}/allocations', [PaymentAllocationController::class, 'getByPayment']);
    
    // Commission Management
    Route::get('/commissions', [CommissionController::class, 'index']);
    Route::post('/commissions/calculate', [CommissionController::class, 'calculate']);
    Route::post('/commissions/pay', [CommissionController::class, 'processPayment']);
    Route::get('/producers/{id}/commissions', [CommissionController::class, 'getByProducer']);
    Route::get('/commission-rates', [CommissionController::class, 'getRates']);
    
    // Reinstatement (GR-64)
    Route::post('/reinstatement/calculate', [ReinstatementController::class, 'calculate']);
    Route::post('/reinstatement/process', [ReinstatementController::class, 'process']);
    Route::get('/reinstatement/{policyId}/eligibility', [ReinstatementController::class, 'checkEligibility']);
    
    // SR22 Fees (GR-10)
    Route::get('/sr22/fees/{stateId}', [SR22Controller::class, 'getFees']);
    Route::post('/sr22/fees/calculate', [SR22Controller::class, 'calculateFees']);
    Route::post('/sr22/fees/process', [SR22Controller::class, 'processFees']);
    
    // Check Printing (NEW)
    Route::get('/checks', [CheckController::class, 'index']);
    Route::post('/checks/print', [CheckController::class, 'print']);
    Route::put('/checks/{id}/void', [CheckController::class, 'void']);
    Route::get('/check-stock', [CheckController::class, 'getStock']);
    Route::post('/check-stock', [CheckController::class, 'createStock']);
    
    // Signatures (NEW)
    Route::get('/signatures', [SignatureController::class, 'index']);
    Route::post('/signatures', [SignatureController::class, 'store']);
    Route::put('/signatures/{id}/approve', [SignatureController::class, 'approve']);
    Route::get('/signatures/active', [SignatureController::class, 'getActive']);
    
    // Positive Pay (NEW)
    Route::get('/positive-pay/exports', [PositivePayController::class, 'getExports']);
    Route::post('/positive-pay/generate', [PositivePayController::class, 'generateFile']);
    Route::post('/positive-pay/transmit', [PositivePayController::class, 'transmitFile']);
    Route::get('/positive-pay/{id}/status', [PositivePayController::class, 'getStatus']);
    
    // Manual Payments (NEW - Outage Handling)
    Route::post('/manual-payments', [ManualPaymentController::class, 'store']);
    Route::get('/manual-payments/pending', [ManualPaymentController::class, 'getPending']);
    Route::put('/manual-payments/{id}/approve', [ManualPaymentController::class, 'approve']);
    Route::post('/manual-payments/batch-process', [ManualPaymentController::class, 'processBatch']);
    
    // Gateway Status (NEW)
    Route::get('/gateway/status', [PaymentGatewayController::class, 'getStatus']);
    Route::post('/gateway/enable-manual-mode', [PaymentGatewayController::class, 'enableManualMode']);
    Route::post('/gateway/disable-manual-mode', [PaymentGatewayController::class, 'disableManualMode']);
    
    // Billing
    Route::get('/billing/overdue', [BillingController::class, 'getOverdueAccounts']);
    Route::post('/billing/late-fees', [BillingController::class, 'processLateFees']);
    Route::post('/billing/notices', [BillingController::class, 'sendNotices']);
    Route::post('/billing/month-end-close', [BillingController::class, 'monthEndClose']);
    Route::post('/billing/year-end-close', [BillingController::class, 'yearEndClose']);
    
    // Financial Reporting
    Route::get('/reports/balance-sheet', [ReportingController::class, 'balanceSheet']);
    Route::get('/reports/income-statement', [ReportingController::class, 'incomeStatement']);
    Route::get('/reports/cash-flow', [ReportingController::class, 'cashFlow']);
    Route::get('/reports/receivables', [ReportingController::class, 'receivablesAging']);
    Route::get('/reports/treaty/{frequency}', [ReportingController::class, 'treatyReporting']);
});
```

## 4. External Integration Requirements - Updated

### 4.1 Universal Entity Management Integration (GR-52)
```sql
-- Payment Gateway Entities (Enhanced for outage handling)
INSERT INTO entity_type (category_id, code, name, metadata_schema) VALUES
((SELECT id FROM entity_category WHERE code = 'INTEGRATION'), 'PAYSAFE_GATEWAY', 'Paysafe Payment Gateway', 
'{"api_key": "string", "merchant_id": "string", "environment": "enum:sandbox,production", "webhook_url": "url", "timeout_seconds": "integer", "retry_attempts": "integer", "outage_notification_enabled": "boolean"}'),

((SELECT id FROM entity_category WHERE code = 'INTEGRATION'), 'SUNFLOWER_BANK', 'Sunflower Bank Integration',
'{"routing_number": "string", "account_number": "string", "positive_pay_format": "enum:nacha,csv,fixed_width", "sftp_host": "string", "sftp_username": "string", "transmission_schedule": "string"}'),

((SELECT id FROM entity_category WHERE code = 'INTEGRATION'), 'CHECK_PRINTING_SERVICE', 'Check Printing Service',
'{"printer_type": "enum:laser,impact", "check_format": "enum:standard,voucher", "micr_font": "string", "signature_required": "boolean"}');

-- Entity instances for accounting integrations
INSERT INTO entity (entity_type_id, name, metadata) VALUES
((SELECT id FROM entity_type WHERE code = 'PAYSAFE_GATEWAY'), 'Production Paysafe Gateway',
'{"api_key": "vault:paysafe_prod_key", "merchant_id": "12345", "environment": "production", "webhook_url": "https://api.company.com/webhooks/paysafe", "timeout_seconds": 30, "retry_attempts": 3, "outage_notification_enabled": true}'),

((SELECT id FROM entity_type WHERE code = 'SUNFLOWER_BANK'), 'Primary Operating Account',
'{"routing_number": "103100195", "account_number": "vault:bank_account", "positive_pay_format": "nacha", "sftp_host": "secure.sunflowerbank.com", "sftp_username": "company_user", "transmission_schedule": "daily_9am"}'),

((SELECT id FROM entity_type WHERE code = 'CHECK_PRINTING_SERVICE'), 'Main Check Printer',
'{"printer_type": "laser", "check_format": "standard", "micr_font": "E13B", "signature_required": true}');
```

### 4.2 Communication Integration (GR-44) - Enhanced
```sql
-- Accounting-specific communication templates (Enhanced for outages)
INSERT INTO communication_template (code, name, type, subject_template, body_template) VALUES
('PREMIUM_DUE', 'Premium Due Notice', 'EMAIL', 'Premium Payment Due - Policy @policy(policy_number)', 
'Your premium payment of @currency(amount_due) is due on @date(due_date). Please make payment to avoid late fees.'),

('LATE_FEE_NOTICE', 'Late Fee Applied', 'EMAIL', 'Late Fee Applied - Policy @policy(policy_number)',
'A late fee of @currency(late_fee) has been applied to your account due to overdue payment.'),

('REINSTATEMENT_AVAILABLE', 'Policy Reinstatement Available', 'EMAIL', 'Reinstate Your Policy - @policy(policy_number)',
'Your policy can be reinstated for @currency(reinstatement_amount). Coverage will be effective upon payment.'),

('SR22_FEE_DUE', 'SR22 Filing Fee Due', 'EMAIL', 'SR22 Filing Fee Due - @policy(policy_number)',
'Your SR22 filing fee of @currency(sr22_fee) is due on @date(due_date) to maintain your filing status.'),

-- NEW: Outage communication templates
('PAYMENT_OUTAGE_NOTICE', 'Payment System Temporary Unavailable', 'EMAIL', 'Payment System Maintenance - @policy(policy_number)',
'Our payment system is temporarily unavailable. You may still make payments by phone at (555) 123-4567 or by mail. We apologize for any inconvenience.'),

('PAYMENT_RESTORED_NOTICE', 'Payment System Restored', 'EMAIL', 'Payment System Restored - @policy(policy_number)',
'Our payment system has been restored and is now accepting online payments. Thank you for your patience.'),

('MANUAL_PAYMENT_CONFIRMATION', 'Payment Recorded', 'EMAIL', 'Payment Confirmation - @policy(policy_number)',
'We have recorded your payment of @currency(payment_amount). Your payment will be processed once our system is fully restored.'),

-- NEW: Commission communication templates
('COMMISSION_STATEMENT', 'Monthly Commission Statement', 'EMAIL', 'Commission Statement - @date(statement_period)',
'Your commission statement for @date(statement_period) is attached. Total commission: @currency(total_commission).'),

('COMMISSION_PAYMENT_NOTICE', 'Commission Payment Processed', 'EMAIL', 'Commission Payment - @date(payment_date)',
'Your commission payment of @currency(commission_amount) has been processed and will be deposited on @date(deposit_date).');
```

## 5. Expected Changes to Existing Files - Updated

### 5.1 Global Requirements Updates

#### GR-54: Core Accounting and Financial Management (NEW)
- **Complete double-entry accounting foundation using transaction/transaction_line**
- **Integration**: Extend existing Transaction/Payment infrastructure
- **Dependencies**: GR-41 (schema), GR-37 (audit), GR-52 (entities)
- **Business Rules**: 3-day month-end close, 7-day year-end close

#### GR-55: Transaction Processing Architecture (NEW)
- **Updates to GR-20**: Add accounting transaction types to business logic
- **Updates to GR-18**: Add accounting workflow transitions
- **Integration**: Consolidate using existing Transaction model and transaction_line table
- **Enhanced**: Manual transaction processing during outages

#### GR-56: Payment Gateway Integration (NEW)
- **Updates to GR-52**: Add Paysafe entity types with outage handling metadata
- **Integration**: Universal entity management for payment services
- **Dependencies**: GR-44 (communication), GR-48 (external integrations)
- **Enhanced**: Graceful degradation and manual payment entry

#### GR-57: Billing and Invoicing Architecture (NEW)
- **Updates to GR-44**: Add billing and outage communication templates
- **Integration**: Extend existing EmailService for billing communications
- **Dependencies**: GR-21 (real-time updates for billing status)
- **Enhanced**: Automated period close procedures

#### GR-58: Premium and Fee Management (NEW)
- **Updates to GR-64**: Integration with reinstatement premium calculations
- **Updates to GR-10**: Integration with SR22 fee processing
- **Integration**: Rate calculation integration with program-specific factors
- **Business Rules**: No commission clawbacks, single producer per policy

#### GR-59: Payment Plan Management (NEW)
- **Updates to GR-64**: Reinstatement payment plan restructuring
- **Integration**: Extend existing payment infrastructure for installments
- **Dependencies**: GR-20 (business logic), GR-18 (workflows)
- **Enhanced**: Payment allocation across multiple invoices

#### GR-60: Check Printing and Positive Pay (NEW - UPDATED SCOPE)
- **Updates to GR-52**: Sunflower Bank and check printing entity configuration
- **Integration**: Bank integration using universal entity management
- **Dependencies**: GR-48 (external integrations), GR-44 (communication)
- **Limited Scope**: Positive Pay only, manual signature images, NACHA format

#### GR-61: Financial Reporting and Analytics (NEW)
- **Updates to GR-33**: Extend analytics and reporting infrastructure
- **Integration**: Real-time financial KPI integration
- **Dependencies**: GR-21 (real-time updates), GR-02 (data management)
- **Enhanced**: Treaty reporting (monthly/quarterly/yearly)

#### GR-62: Compliance and Audit (NEW)
- **Updates to GR-37**: Complete integration with action tracking
- **Updates to GR-51**: Enhanced compliance requirements
- **Integration**: Existing security and access control patterns
- **Enhanced**: 7-year retention, PCI DSS compliance

### 5.2 Infrastructure Codebase Updates

#### Backend Models (/app/Models/)
```php
// Extend existing models
class Transaction extends Model {
    // Add accounting-specific relationships
    public function transactionLines(): HasMany;
    public function accountCode(): BelongsTo;
    public function isPosted(): bool;
    public function postTransaction(): bool;
    public function reverseTransaction(): Transaction;
}

class Payment extends Model {
    // Add installment processing
    public function installments(): BelongsToMany;
    public function paymentPlan(): BelongsTo;
    public function allocations(): HasMany;
    public function manualEntry(): HasOne;
}

class Policy extends Model {
    // Add accounting relationships
    public function paymentPlan(): HasOne;
    public function reinstatementCalculations(): HasMany;
    public function sr22FeeTransactions(): HasMany;
    public function commissions(): HasMany;
}

// NEW Models
class Commission extends Model;
class PaymentPlan extends Model;
class Installment extends Model;
class PaymentAllocation extends Model;
class CheckRegister extends Model;
class PositivePayExport extends Model;
class ManualPayment extends Model;
```

#### Service Extensions (/app/Services/)
- **PaymentService**: Add installment processing and manual payment methods
- **EmailService**: Add billing notification templates and outage communications
- **PolicyService**: Add reinstatement integration methods
- **UniversalEntityService**: Add payment gateway and bank configurations
- **NEW**: CheckPrintingService, PositivePayService, ManualPaymentService

#### Controller Extensions (/app/Http/Controllers/)
- **PaymentController**: Add installment payment processing and manual entry
- **PolicyController**: Add reinstatement calculation endpoints
- **NEW Controllers**: Accounting, Billing, Reporting, Check, Commission controllers

#### API Routes (routes/api.php, routes/portal_api.php)
- Add comprehensive accounting endpoint groups
- Extend payment endpoints for installment and manual processing
- Add reporting endpoints for financial analytics
- Add check printing and Positive Pay endpoints

### 5.3 Database Migration Files
```php
// New migrations required
- alter_transaction_table_for_accounting.php
- create_transaction_line_table.php
- create_chart_of_accounts_table.php
- create_payment_plan_table.php
- create_installment_table.php
- create_payment_allocation_table.php
- create_commission_tables.php
- create_check_processing_tables.php
- create_positive_pay_tables.php
- create_manual_payment_tables.php
- create_reinstatement_calculation_table.php (from GR-64)
- create_sr22_fee_tables.php
- create_accounting_reference_tables.php
```

### 5.4 Configuration Updates
```php
// config/services.php - Payment gateway configurations
'paysafe' => [
    'entity_type' => 'PAYSAFE_GATEWAY',
    'default_entity' => 'Production Paysafe Gateway',
    'outage_detection_enabled' => true,
    'manual_mode_threshold' => 5, // failures
],

'sunflower_bank' => [
    'entity_type' => 'SUNFLOWER_BANK', 
    'default_entity' => 'Primary Operating Account',
    'positive_pay_schedule' => 'daily',
    'nacha_format_version' => '8.2',
],

// config/accounting.php - New configuration file
'chart_of_accounts' => [
    'auto_create_missing' => false,
    'validate_balance' => true,
],
'payment_plans' => [
    'default_installments' => 11,
    'max_installments' => 11,
    'late_fee_grace_days' => 10,
],
'commission' => [
    'clawback_enabled' => false, // No clawbacks per feedback
    'default_schedule' => 'MONTHLY',
    'multi_level_splits' => false, // Single producer per policy
],
'period_close' => [
    'month_end_deadline_days' => 3,
    'year_end_deadline_days' => 7,
    'lock_closed_periods' => true,
],
'manual_payments' => [
    'enabled_during_outage' => true,
    'requires_approval' => true,
    'batch_processing_enabled' => true,
],
'check_printing' => [
    'signature_storage_enabled' => true,
    'signature_formats' => ['PNG', 'JPG'],
    'micr_validation_enabled' => true,
],
'positive_pay' => [
    'daily_export_enabled' => true,
    'export_format' => 'NACHA',
    'transmission_method' => 'SFTP',
    'bank_entity' => 'SUNFLOWER_BANK',
],
```

## 6. Business Rules and Clarifications - FINAL

### 6.1 Commission Processing Rules (FROM FEEDBACK)
- **Commission clawback**: **NO** - Commissions are not recovered on mid-term cancellations
- **Multi-level commission splits**: **NO** - Single producer per policy for commission payments
- **Commission structure**: Program-specific defaults + special producer commissions (percentage-based)
- **Payment frequency**: Monthly, quarterly, or annual based on commission schedule

### 6.2 Timeline Requirements (FROM FEEDBACK)
- **Month-end close**: **3 business days** after month-end for premium reconciliation
- **Year-end close**: **7 business days** after year-end for annual reporting
- **Treaty reporting**: **Monthly, Quarterly, Yearly** for reinsurance treaty settlements
- **Audit lock**: Prevent changes to closed periods without special permissions

### 6.3 Check Processing Rules (FROM FEEDBACK)
- **Signature requirements**: **Manual signature images** should be stored and used for check printing
- **NACHA scope**: **Only for Positive Pay** processing with Sunflower Bank
- **Check printing**: Standard format with MICR encoding, daily Positive Pay exports

### 6.4 Paysafe Outage Handling (FROM FEEDBACK)
#### Manual Payment Entry Process
- **Interface behavior**: Current payment interfaces should be **disabled** during outages
- **Staff workflow**: Manual payment entry interface for authorized staff only
- **Validation**: Basic validation without real-time gateway verification
- **Status tracking**: Payments marked as "MANUAL_PENDING" until gateway verification
- **Batch processing**: When Paysafe resumes, manual payments validated and processed in batch

#### Customer Communication (Configurable)
- **Program-specific**: Auto notices should be **configurable per program** whether they go out
- **Multi-channel alerts**: Email, SMS, and portal notifications to affected customers
- **Status updates**: Real-time updates on portal about payment processing availability
- **Alternative instructions**: Guidance on phone and mail payment methods
- **Resolution notifications**: Automated alerts when services are restored

### 6.5 Database Consolidation Strategy
- **Primary approach**: Use existing `transaction` table with enhanced `transaction_type` classifications
- **Double-entry**: Use `transaction_line` table for detailed accounting entries
- **Specialized tables**: Keep separate for ACH/Positive Pay due to regulatory requirements
- **Payment allocation**: Remains separate due to complex business requirements

## 7. Integration Testing Requirements - Updated

### 7.1 Unit Tests
- TransactionService balance validation and posting
- PaymentPlanService installment generation and restructuring
- ReinstatementService premium calculations (GR-64 integration)
- SR22FeeService fee calculations (GR-10 integration)
- CheckPrintingService check generation and MICR validation
- PositivePayService NACHA file generation
- ManualPaymentService validation and batch processing

### 7.2 Integration Tests
- Payment processing with transaction/transaction_line creation
- Manual payment entry and batch processing workflow
- Commission calculation and payment processing
- Reinstatement workflow end-to-end with payment plan restructuring
- SR22 fee processing with policy billing integration
- Check printing with signature and Positive Pay integration
- Communication template rendering for all scenarios

### 7.3 Performance Tests
- Chart of accounts queries (<500ms)
- Transaction posting (<200ms)
- Payment plan generation (<1s)
- Financial report generation (<5s)
- Positive Pay file generation (<30s for daily volume)
- Manual payment batch processing (<2min for 100 payments)

### 7.4 Outage Simulation Tests
- Paysafe outage detection and manual mode activation
- Manual payment entry workflow during outages
- Customer notification system during outages
- Batch processing when services are restored
- Data consistency between manual and automated processing

## 8. Security and Compliance Requirements - Enhanced

### 8.1 Audit Trail (GR-37 Integration) - Enhanced
```sql
-- Action types for accounting operations (Enhanced)
INSERT INTO action_type (code, name, description) VALUES
('TRANSACTION_CREATED', 'Transaction Created', 'New financial transaction created'),
('TRANSACTION_POSTED', 'Transaction Posted', 'Transaction posted to ledger'),
('TRANSACTION_REVERSED', 'Transaction Reversed', 'Transaction reversed with reason'),
('PAYMENT_PROCESSED', 'Payment Processed', 'Payment processed with transaction'),
('MANUAL_PAYMENT_ENTERED', 'Manual Payment Entered', 'Manual payment entered during outage'),
('MANUAL_PAYMENT_APPROVED', 'Manual Payment Approved', 'Manual payment approved for processing'),
('COMMISSION_CALCULATED', 'Commission Calculated', 'Commission amount calculated'),
('COMMISSION_PAID', 'Commission Paid', 'Commission payment processed'),
('REINSTATEMENT_CALCULATED', 'Reinstatement Calculated', 'Reinstatement amount calculated'),
('SR22_FEE_PROCESSED', 'SR22 Fee Processed', 'SR22 fee processed and billed'),
('CHECK_PRINTED', 'Check Printed', 'Check printed and registered'),
('CHECK_VOIDED', 'Check Voided', 'Check voided with reason'),
('POSITIVE_PAY_EXPORTED', 'Positive Pay Exported', 'Positive Pay file exported to bank'),
('PERIOD_CLOSED', 'Accounting Period Closed', 'Accounting period closed and locked');
```

### 8.2 Data Retention - Enhanced
- **Financial records**: 7 years (insurance regulatory compliance)
- **Transaction records**: Permanent retention for legal requirements
- **Payment transactions**: 7 years with detailed audit trail
- **Manual payment records**: 7 years with approval documentation
- **Check records**: 7 years with MICR and signature information
- **Positive Pay files**: 7 years for bank reconciliation compliance
- **Commission records**: 7 years for producer audit requirements
- **Audit logs**: 7 years with PII masking for privacy compliance

### 8.3 Access Control - Enhanced
- **Chart of accounts**: Admin/Finance roles only
- **Transaction posting**: Finance Manager role with dual approval for large amounts
- **Manual payment entry**: Finance/Customer Service roles with supervisory approval
- **Check printing**: Finance Manager role with signature authority
- **Commission processing**: Finance/Producer Management roles
- **Positive Pay processing**: Finance Manager role only
- **Period close operations**: Finance Manager role with audit oversight
- **Financial reporting**: Finance/Management roles with data access restrictions

## 9. Success Criteria and Validation - Updated

### 9.1 Integration Success Criteria
- [ ] All accounting services extend existing infrastructure patterns
- [ ] Database schema follows GR-41 standards with consolidated approach
- [ ] APIs follow existing RESTful conventions and route organization
- [ ] Service layer follows existing dependency injection patterns
- [ ] Action tracking provides complete audit trail (GR-37)
- [ ] Universal entity management used for all external services (GR-52)

### 9.2 Functional Success Criteria
- [ ] Double-entry accounting maintains balanced transactions
- [ ] Payment plan generation and restructuring works correctly
- [ ] Manual payment entry functions during Paysafe outages
- [ ] Customer notifications work correctly for outage scenarios
- [ ] Reinstatement calculations integrate with GR-64 requirements
- [ ] SR22 fee processing integrates with GR-10 requirements
- [ ] Check printing with manual signatures functions correctly
- [ ] Positive Pay file generation meets Sunflower Bank requirements
- [ ] Commission calculations follow program-specific rules (no clawbacks)

### 9.3 Performance Success Criteria
- [ ] Chart of accounts queries complete in <500ms
- [ ] Transaction posting completes in <200ms
- [ ] Payment plan generation completes in <1s
- [ ] Financial reports generate in <5s
- [ ] Manual payment batch processing completes in <2min for 100 payments
- [ ] Positive Pay file generation completes in <30s for daily volume
- [ ] Real-time balance updates maintain accuracy

### 9.4 Business Rules Validation
- [ ] Month-end close completes within 3 business days
- [ ] Year-end close completes within 7 business days
- [ ] Commission clawbacks are disabled (no recovery on cancellations)
- [ ] Single producer commission structure enforced
- [ ] Program-specific commission rates applied correctly
- [ ] Manual payment interfaces disabled during outages as configured
- [ ] Customer outage notifications configurable per program

This updated infrastructure support documentation provides the complete foundation needed to implement the accounting Global Requirements while incorporating all feedback from plan.md, plan2.md, and plan3.md. The approach emphasizes maximum integration with existing systems, database consolidation strategies, enhanced outage handling, and comprehensive accounting capabilities including check printing and Positive Pay processing.