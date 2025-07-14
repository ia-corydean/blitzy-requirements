# Accounting Infrastructure Support Documentation

## Executive Summary

This document outlines the comprehensive supporting infrastructure required for implementing the 9 Global Requirements (GR-54 through GR-62) for accounting functionality. The analysis is based on plan4.md and emphasizes maximum integration with existing infrastructure while adding comprehensive accounting capabilities.

## 1. Database Schema Extensions

### 1.1 Core Financial Tables (Extend Existing)

#### Extend Transaction Table (Existing)
```sql
-- Add accounting-specific transaction types
ALTER TABLE transaction ADD COLUMN transaction_subtype VARCHAR(50) AFTER transaction_type;
ALTER TABLE transaction ADD COLUMN journal_entry_id BIGINT UNSIGNED NULL AFTER transaction_subtype;
ALTER TABLE transaction ADD COLUMN account_code VARCHAR(20) NULL AFTER journal_entry_id;

-- New transaction types for accounting
INSERT INTO transaction_type (code, name, description) VALUES
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
('ADJUSTMENT_MANUAL', 'Manual Adjustment', 'Administrative manual adjustments');
```

#### New Accounting Core Tables
```sql
-- Chart of Accounts
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

-- Journal Entries (Double-Entry Foundation)
CREATE TABLE journal_entry (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    entry_number VARCHAR(50) UNIQUE NOT NULL,
    entry_date DATE NOT NULL,
    effective_date DATE NOT NULL,
    policy_id BIGINT UNSIGNED NULL,
    quote_id BIGINT UNSIGNED NULL,
    payment_id BIGINT UNSIGNED NULL,
    reference_type VARCHAR(50) NULL,
    reference_id BIGINT UNSIGNED NULL,
    description TEXT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    is_posted BOOLEAN DEFAULT FALSE,
    posted_at TIMESTAMP NULL,
    posted_by BIGINT UNSIGNED NULL,
    is_reversed BOOLEAN DEFAULT FALSE,
    reversed_by_entry_id BIGINT UNSIGNED NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (quote_id) REFERENCES quote(id),
    FOREIGN KEY (payment_id) REFERENCES payment(id),
    FOREIGN KEY (reversed_by_entry_id) REFERENCES journal_entry(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    FOREIGN KEY (posted_by) REFERENCES user(id),
    
    INDEX idx_entry_number (entry_number),
    INDEX idx_entry_date (entry_date),
    INDEX idx_policy (policy_id),
    INDEX idx_payment (payment_id),
    INDEX idx_reference (reference_type, reference_id)
);

-- Journal Entry Lines (Transaction Details)
CREATE TABLE journal_entry_line (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    journal_entry_id BIGINT UNSIGNED NOT NULL,
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
    
    FOREIGN KEY (journal_entry_id) REFERENCES journal_entry(id),
    FOREIGN KEY (account_id) REFERENCES chart_of_accounts(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_journal_entry (journal_entry_id),
    INDEX idx_account (account_id),
    INDEX idx_component_type (component_type),
    
    CONSTRAINT chk_debit_credit CHECK (
        (debit_amount > 0 AND credit_amount = 0) OR 
        (credit_amount > 0 AND debit_amount = 0)
    )
);
```

### 1.2 Payment Plan and Installment Tables
```sql
-- Payment Plans
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

### 1.3 Reinstatement Integration Tables (GR-64)
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
    journal_entry_id BIGINT UNSIGNED NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (journal_entry_id) REFERENCES journal_entry(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_policy (policy_id),
    INDEX idx_reinstatement_date (reinstatement_date),
    INDEX idx_cancellation_date (cancellation_date)
);
```

### 1.4 SR22 Fee Management Tables (GR-10)
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

-- SR22 Fee Transactions
CREATE TABLE sr22_fee_transaction (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    policy_id BIGINT UNSIGNED NOT NULL,
    sr22_filing_id BIGINT UNSIGNED NOT NULL,
    fee_schedule_id BIGINT UNSIGNED NOT NULL,
    transaction_id BIGINT UNSIGNED NOT NULL,
    journal_entry_id BIGINT UNSIGNED NULL,
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
    FOREIGN KEY (journal_entry_id) REFERENCES journal_entry(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    INDEX idx_policy (policy_id),
    INDEX idx_sr22_filing (sr22_filing_id),
    INDEX idx_transaction_date (transaction_date)
);
```

### 1.5 Reference Tables
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
```

## 2. Service Layer Architecture

### 2.1 Core Accounting Services
```php
namespace App\Services\Accounting;

// Core Accounting Service (Extends Existing Patterns)
class AccountingService
{
    public function __construct(
        private PaymentService $paymentService,
        private EmailService $emailService,
        private ReinstatementService $reinstatementService,
        private JournalEntryService $journalEntryService,
        private ChartOfAccountsService $chartOfAccountsService
    ) {}
    
    // Main accounting operations
    public function processPayment(Payment $payment): JournalEntry;
    public function processRefund(Refund $refund): JournalEntry;
    public function processChargeback(Chargeback $chargeback): JournalEntry;
    public function calculateCommissions(Policy $policy): array;
    public function generateFinancialStatement(Carbon $startDate, Carbon $endDate): array;
}

// Journal Entry Service
class JournalEntryService
{
    public function createEntry(array $data): JournalEntry;
    public function addLine(JournalEntry $entry, array $lineData): JournalEntryLine;
    public function postEntry(JournalEntry $entry): bool;
    public function reverseEntry(JournalEntry $entry, string $reason): JournalEntry;
    public function validateBalance(JournalEntry $entry): bool;
}

// Payment Plan Service
class PaymentPlanService
{
    public function createPaymentPlan(Policy $policy, array $planData): PaymentPlan;
    public function generateInstallments(PaymentPlan $plan): Collection;
    public function processPaymentToInstallment(Payment $payment): array;
    public function restructureForReinstatement(PaymentPlan $plan, ReinstatementCalculation $calc): PaymentPlan;
}

// Reinstatement Service (GR-64 Integration)
class ReinstatementService
{
    public function calculateReinstatementAmount(Policy $policy, Carbon $date): ReinstatementCalculation;
    public function processReinstatementPayment(Payment $payment): Policy;
    public function createReinstatementJournalEntry(ReinstatementCalculation $calc): JournalEntry;
    public function restructurePaymentPlan(Policy $policy, ReinstatementCalculation $calc): PaymentPlan;
}

// SR22 Fee Service (GR-10 Integration)
class SR22FeeService
{
    public function calculateSR22Fees(Policy $policy, SR22Filing $filing): array;
    public function processSR22Payment(Payment $payment, SR22Filing $filing): SR22FeeTransaction;
    public function createSR22JournalEntry(SR22FeeTransaction $transaction): JournalEntry;
    public function scheduleSR22Renewals(SR22Filing $filing): Collection;
}

// Billing Service
class BillingService
{
    public function generateInvoice(Policy $policy, array $charges): Invoice;
    public function sendBillingNotice(Policy $policy, Installment $installment): bool;
    public function processLateFees(Collection $overdueInstallments): array;
    public function sendReinstatementNotice(Policy $policy, ReinstatementCalculation $calc): bool;
}
```

### 2.2 Integration Services
```php
// Payment Gateway Integration (Universal Entity Management - GR-52)
class PaymentGatewayService
{
    public function __construct(
        private UniversalEntityService $entityService
    ) {}
    
    // Paysafe integration using universal entity management
    public function processPayment(PaymentMethod $method, Decimal $amount): PaymentResult;
    public function verifyPaymentMethod(PaymentMethod $method): VerificationResult;
    public function handleChargeback(Payment $payment): ChargebackResult;
    public function processRefund(Payment $originalPayment, Decimal $amount): RefundResult;
}

// Bank Integration Service (Sunflower Bank - GR-52)
class BankIntegrationService
{
    public function __construct(
        private UniversalEntityService $entityService
    ) {}
    
    // Check printing and positive pay
    public function submitPositivePayFile(Collection $checks): PositivePayResult;
    public function printChecks(Collection $refunds): CheckPrintResult;
    public function reconcileBankStatement(BankStatement $statement): ReconciliationResult;
}
```

## 3. API Endpoints (RESTful Extensions)

### 3.1 Accounting API Routes
```php
// In routes/api.php (following existing patterns)
Route::prefix('accounting')->middleware(['auth:sanctum'])->group(function () {
    // Core Accounting
    Route::get('/transactions', [AccountingController::class, 'getTransactions']);
    Route::get('/journal-entries', [JournalEntryController::class, 'index']);
    Route::post('/journal-entries', [JournalEntryController::class, 'store']);
    Route::put('/journal-entries/{id}/post', [JournalEntryController::class, 'post']);
    
    // Chart of Accounts
    Route::get('/chart-of-accounts', [ChartOfAccountsController::class, 'index']);
    Route::post('/chart-of-accounts', [ChartOfAccountsController::class, 'store']);
    Route::put('/chart-of-accounts/{id}', [ChartOfAccountsController::class, 'update']);
    
    // Payment Plans
    Route::get('/payment-plans', [PaymentPlanController::class, 'index']);
    Route::post('/payment-plans', [PaymentPlanController::class, 'store']);
    Route::get('/payment-plans/{id}/installments', [PaymentPlanController::class, 'getInstallments']);
    Route::post('/payment-plans/{id}/restructure', [PaymentPlanController::class, 'restructure']);
    
    // Reinstatement (GR-64)
    Route::post('/reinstatement/calculate', [ReinstatementController::class, 'calculate']);
    Route::post('/reinstatement/process', [ReinstatementController::class, 'process']);
    Route::get('/reinstatement/{policyId}/eligibility', [ReinstatementController::class, 'checkEligibility']);
    
    // SR22 Fees (GR-10)
    Route::get('/sr22/fees/{stateId}', [SR22Controller::class, 'getFees']);
    Route::post('/sr22/fees/calculate', [SR22Controller::class, 'calculateFees']);
    Route::post('/sr22/fees/process', [SR22Controller::class, 'processFees']);
    
    // Billing
    Route::get('/billing/overdue', [BillingController::class, 'getOverdueAccounts']);
    Route::post('/billing/late-fees', [BillingController::class, 'processLateFees']);
    Route::post('/billing/notices', [BillingController::class, 'sendNotices']);
    
    // Financial Reporting
    Route::get('/reports/balance-sheet', [ReportingController::class, 'balanceSheet']);
    Route::get('/reports/income-statement', [ReportingController::class, 'incomeStatement']);
    Route::get('/reports/cash-flow', [ReportingController::class, 'cashFlow']);
    Route::get('/reports/receivables', [ReportingController::class, 'receivablesAging']);
});
```

## 4. External Integration Requirements

### 4.1 Universal Entity Management Integration (GR-52)
```sql
-- Payment Gateway Entities
INSERT INTO entity_type (category_id, code, name, metadata_schema) VALUES
((SELECT id FROM entity_category WHERE code = 'INTEGRATION'), 'PAYSAFE_GATEWAY', 'Paysafe Payment Gateway', 
'{"api_key": "string", "merchant_id": "string", "environment": "enum:sandbox,production", "webhook_url": "url"}'),

((SELECT id FROM entity_category WHERE code = 'INTEGRATION'), 'SUNFLOWER_BANK', 'Sunflower Bank Integration',
'{"routing_number": "string", "account_number": "string", "positive_pay_format": "enum:standard,enhanced"}');

-- Entity instances for accounting integrations
INSERT INTO entity (entity_type_id, name, metadata) VALUES
((SELECT id FROM entity_type WHERE code = 'PAYSAFE_GATEWAY'), 'Production Paysafe Gateway',
'{"api_key": "vault:paysafe_prod_key", "merchant_id": "12345", "environment": "production", "webhook_url": "https://api.company.com/webhooks/paysafe"}'),

((SELECT id FROM entity_type WHERE code = 'SUNFLOWER_BANK'), 'Primary Operating Account',
'{"routing_number": "103100195", "account_number": "vault:bank_account", "positive_pay_format": "enhanced"}');
```

### 4.2 Communication Integration (GR-44)
```sql
-- Accounting-specific communication templates
INSERT INTO communication_template (code, name, type, subject_template, body_template) VALUES
('PREMIUM_DUE', 'Premium Due Notice', 'EMAIL', 'Premium Payment Due - Policy @policy(policy_number)', 
'Your premium payment of @currency(amount_due) is due on @date(due_date). Please make payment to avoid late fees.'),

('LATE_FEE_NOTICE', 'Late Fee Applied', 'EMAIL', 'Late Fee Applied - Policy @policy(policy_number)',
'A late fee of @currency(late_fee) has been applied to your account due to overdue payment.'),

('REINSTATEMENT_AVAILABLE', 'Policy Reinstatement Available', 'EMAIL', 'Reinstate Your Policy - @policy(policy_number)',
'Your policy can be reinstated for @currency(reinstatement_amount). Coverage will be effective upon payment.'),

('SR22_FEE_DUE', 'SR22 Filing Fee Due', 'EMAIL', 'SR22 Filing Fee Due - @policy(policy_number)',
'Your SR22 filing fee of @currency(sr22_fee) is due on @date(due_date) to maintain your filing status.');
```

## 5. Expected Changes to Existing Files

### 5.1 Global Requirements Updates

#### GR-54: Core Accounting and Financial Management
- **New File**: Complete double-entry accounting foundation
- **Integration**: Extend existing Transaction/Payment infrastructure
- **Dependencies**: GR-41 (schema), GR-37 (audit), GR-52 (entities)

#### GR-55: Transaction Processing Architecture  
- **Updates to GR-20**: Add accounting transaction types to business logic
- **Updates to GR-18**: Add accounting workflow transitions
- **Integration**: Extend existing Transaction model and PaymentService

#### GR-56: Payment Gateway Integration
- **Updates to GR-52**: Add Paysafe and bank entity types
- **Integration**: Universal entity management for payment services
- **Dependencies**: GR-44 (communication), GR-48 (external integrations)

#### GR-57: Billing and Invoicing Architecture
- **Updates to GR-44**: Add billing communication templates
- **Integration**: Extend existing EmailService for billing communications
- **Dependencies**: GR-21 (real-time updates for billing status)

#### GR-58: Premium and Fee Management
- **Updates to GR-64**: Integration with reinstatement premium calculations
- **Updates to GR-10**: Integration with SR22 fee processing
- **Integration**: Rate calculation integration with program-specific factors

#### GR-59: Payment Plan Management
- **Updates to GR-64**: Reinstatement payment plan restructuring
- **Integration**: Extend existing payment infrastructure for installments
- **Dependencies**: GR-20 (business logic), GR-18 (workflows)

#### GR-60: Check Printing and Positive Pay
- **Updates to GR-52**: Sunflower Bank entity configuration
- **Integration**: Bank integration using universal entity management
- **Dependencies**: GR-48 (external integrations), GR-44 (communication)

#### GR-61: Financial Reporting and Analytics
- **Updates to GR-33**: Extend analytics and reporting infrastructure
- **Integration**: Real-time financial KPI integration
- **Dependencies**: GR-21 (real-time updates), GR-02 (data management)

#### GR-62: Compliance and Audit
- **Updates to GR-37**: Complete integration with action tracking
- **Updates to GR-51**: Enhanced compliance requirements
- **Integration**: Existing security and access control patterns

### 5.2 Infrastructure Codebase Updates

#### Backend Models (/app/Models/)
```php
// Extend existing models
class Transaction extends Model {
    // Add accounting-specific relationships
    public function journalEntry(): BelongsTo;
    public function accountCode(): BelongsTo;
}

class Payment extends Model {
    // Add installment processing
    public function installments(): BelongsToMany;
    public function paymentPlan(): BelongsTo;
}

class Policy extends Model {
    // Add accounting relationships
    public function paymentPlan(): HasOne;
    public function reinstatementCalculations(): HasMany;
    public function sr22FeeTransactions(): HasMany;
}
```

#### Service Extensions (/app/Services/)
- **PaymentService**: Add installment processing methods
- **EmailService**: Add billing notification templates
- **PolicyService**: Add reinstatement integration methods
- **UniversalEntityService**: Add payment gateway configurations

#### Controller Extensions (/app/Http/Controllers/)
- **PaymentController**: Add installment payment processing
- **PolicyController**: Add reinstatement calculation endpoints
- **New Controllers**: Accounting, Billing, Reporting controllers

#### API Routes (routes/api.php, routes/portal_api.php)
- Add accounting endpoint groups
- Extend payment endpoints for installment processing
- Add reporting endpoints for financial analytics

### 5.3 Database Migration Files
```php
// New migrations required
- create_chart_of_accounts_table.php
- create_journal_entry_table.php
- create_journal_entry_line_table.php
- create_payment_plan_table.php
- create_installment_table.php
- create_reinstatement_calculation_table.php (from GR-64)
- create_sr22_fee_schedule_table.php
- create_sr22_fee_transaction_table.php
- add_accounting_fields_to_transaction_table.php
- create_accounting_reference_tables.php
```

### 5.4 Configuration Updates
```php
// config/services.php - Payment gateway configurations
'paysafe' => [
    'entity_type' => 'PAYSAFE_GATEWAY',
    'default_entity' => 'Production Paysafe Gateway',
],

'sunflower_bank' => [
    'entity_type' => 'SUNFLOWER_BANK', 
    'default_entity' => 'Primary Operating Account',
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
```

## 6. Integration Testing Requirements

### 6.1 Unit Tests
- JournalEntryService balance validation
- PaymentPlanService installment generation
- ReinstatementService premium calculations
- SR22FeeService fee calculations

### 6.2 Integration Tests
- Payment processing with journal entry creation
- Reinstatement workflow end-to-end
- SR22 fee processing with policy billing
- Communication template rendering

### 6.3 Performance Tests
- Chart of accounts queries (<500ms)
- Journal entry posting (<200ms)
- Payment plan generation (<1s)
- Financial report generation (<5s)

## 7. Compliance and Security Requirements

### 7.1 Audit Trail (GR-37 Integration)
```sql
-- Action types for accounting operations
INSERT INTO action_type (code, name, description) VALUES
('JOURNAL_ENTRY_CREATED', 'Journal Entry Created', 'New journal entry created'),
('JOURNAL_ENTRY_POSTED', 'Journal Entry Posted', 'Journal entry posted to ledger'),
('PAYMENT_PROCESSED', 'Payment Processed', 'Payment processed with journal entry'),
('REINSTAMENT_CALCULATED', 'Reinstatement Calculated', 'Reinstatement amount calculated'),
('SR22_FEE_PROCESSED', 'SR22 Fee Processed', 'SR22 fee processed and billed');
```

### 7.2 Data Retention
- Financial records: 7 years (insurance regulatory compliance)
- Journal entries: Permanent retention
- Payment transactions: 7 years
- Audit logs: 7 years with PII masking

### 7.3 Access Control
- Chart of accounts: Admin/Finance roles only
- Journal entry posting: Finance Manager role
- Payment processing: Finance/Customer Service roles
- Financial reporting: Finance/Management roles

## 8. Success Criteria and Validation

### 8.1 Integration Success Criteria
- [ ] All accounting services extend existing infrastructure patterns
- [ ] Database schema follows GR-41 standards
- [ ] APIs follow existing RESTful conventions
- [ ] Service layer follows existing dependency injection patterns
- [ ] Action tracking provides complete audit trail (GR-37)

### 8.2 Functional Success Criteria
- [ ] Double-entry accounting maintains balanced journal entries
- [ ] Payment plan generation and restructuring works correctly
- [ ] Reinstatement calculations integrate with GR-64 requirements
- [ ] SR22 fee processing integrates with GR-10 requirements
- [ ] Communication templates render correctly with insurance helpers

### 8.3 Performance Success Criteria
- [ ] Chart of accounts queries complete in <500ms
- [ ] Journal entry posting completes in <200ms
- [ ] Payment plan generation completes in <1s
- [ ] Financial reports generate in <5s
- [ ] Real-time balance updates maintain accuracy

This infrastructure support documentation provides the complete foundation needed to implement the accounting Global Requirements while maintaining maximum integration with existing systems and following all established patterns and standards.