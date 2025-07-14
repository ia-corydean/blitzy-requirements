# Accounting Global Requirements Generation - Version 6 (Complete Equity-Based System)

## Executive Summary

Version 6 represents the definitive accounting requirements specification, fully embracing the **mandatory equity-based double-entry system** with enhanced payment plan flexibility, dynamic installment scheduling, and comprehensive automation. This version incorporates all previous learnings plus critical new requirements:

1. **True Double-Entry Accounting** - Every dollar is both a debit and credit; Assets = Liabilities + Equity
2. **Dynamic Installment Generation** - Just-in-time creation as payments are received
3. **Date-Driven Payment Options** - Agent-selected due dates with automatic down payment calculation
4. **Full Payment Allocation** - No partial payments; apply to oldest pending installments first
5. **Automated Lifecycle Management** - Notices, fees, cancellations, and reinstatements

## Core Principles (Mandatory)

### 1. **Equity-Based System**
- Every financial transaction creates balanced journal entries
- Assets = Liabilities + Equity must always hold
- Complete audit trail from business event to financial impact
- No shortcuts or single-entry transactions allowed

### 2. **Program-Centric Configuration**
- Each insurance program defines all financial rules
- Adjustments, limits, deductibles, proof rules per program
- Commission schedules program-specific
- Self-service configuration without deployments

### 3. **Audit-First Design**
- Every adjustment, payment, fee writes journal entries
- Header + debit/credit lines for complete traceability
- Permanent retention for bound policies
- Real-time reporting from live tables (no ETL)

### 4. **Modular & Extensible**
- New adjustment types are configuration rows, not code
- Proof rules and commission structures via lookup tables
- Gateway settings configurable per program
- Producer mappings maintained in database

## Enhanced Payment Plan Architecture

### Payment Plan Options (New Requirements)

1. **Percent-Based Down Payment**
   ```sql
   CREATE TABLE payment_plan_template (
     id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
     program_id BIGINT UNSIGNED NOT NULL,
     plan_name VARCHAR(100) NOT NULL,
     plan_type ENUM('PERCENT_DOWN', 'DATE_DRIVEN', 'PAID_IN_FULL'),
     down_payment_percent DECIMAL(5,2), -- e.g., 16.67, 25.00
     installment_count INT,
     installment_fee DECIMAL(10,2), -- e.g., $4.50 per installment
     is_active BOOLEAN DEFAULT TRUE,
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     FOREIGN KEY (program_id) REFERENCES programs(id),
     INDEX idx_plan_program (program_id)
   );
   ```

2. **Date-Driven Down Payment**
   ```sql
   CREATE TABLE date_driven_payment_plan (
     id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
     policy_id BIGINT UNSIGNED NOT NULL,
     agent_selected_date DATE NOT NULL,
     daily_premium_rate DECIMAL(10,4) NOT NULL,
     calculated_down_payment DECIMAL(10,2) NOT NULL,
     days_to_first_payment INT NOT NULL,
     created_by BIGINT UNSIGNED NOT NULL,
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     FOREIGN KEY (policy_id) REFERENCES policies(id),
     INDEX idx_date_plan_policy (policy_id)
   );
   ```

### Dynamic Installment Scheduling

```sql
CREATE TABLE installment (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  payment_plan_id BIGINT UNSIGNED NOT NULL,
  installment_number INT NOT NULL,
  due_date DATE NOT NULL,
  
  -- Itemized components
  premium_amount DECIMAL(10,2) NOT NULL, -- daily_rate × days
  policy_fee_amount DECIMAL(10,2) DEFAULT 0,
  mvcpa_fee_amount DECIMAL(10,2) DEFAULT 0,
  sr22_fee_amount DECIMAL(10,2) DEFAULT 0,
  installment_fee_amount DECIMAL(10,2) DEFAULT 0,
  total_amount DECIMAL(10,2) NOT NULL,
  
  -- Status tracking
  status ENUM('PENDING', 'PARTIALLY_PAID', 'PAID', 'OVERDUE', 'CANCELLED') DEFAULT 'PENDING',
  amount_paid DECIMAL(10,2) DEFAULT 0,
  
  -- Dynamic generation tracking
  generated_from_payment_id BIGINT UNSIGNED, -- Which payment triggered creation
  generation_date TIMESTAMP,
  
  -- Notice tracking
  billing_notice_sent_date DATE,
  late_fee_applied_date DATE,
  cancellation_notice_sent_date DATE,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (payment_plan_id) REFERENCES payment_plans(id),
  FOREIGN KEY (generated_from_payment_id) REFERENCES payments(id),
  INDEX idx_installment_plan (payment_plan_id, installment_number),
  INDEX idx_installment_status_due (status, due_date)
);
```

### Payment Allocation System

```sql
CREATE TABLE payment_allocation (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  payment_id BIGINT UNSIGNED NOT NULL,
  installment_id BIGINT UNSIGNED NOT NULL,
  allocated_amount DECIMAL(10,2) NOT NULL,
  allocation_order INT NOT NULL, -- Order in which installments were paid
  
  -- Journal entry reference
  journal_entry_id BIGINT UNSIGNED NOT NULL,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (payment_id) REFERENCES payments(id),
  FOREIGN KEY (installment_id) REFERENCES installments(id),
  FOREIGN KEY (journal_entry_id) REFERENCES journal_entries(id),
  INDEX idx_allocation_payment (payment_id),
  INDEX idx_allocation_installment (installment_id)
);
```

## Double-Entry Journal System

### Core Journal Tables

```sql
CREATE TABLE journal_entry (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  transaction_id BIGINT UNSIGNED NOT NULL,
  entry_type ENUM('PREMIUM', 'PAYMENT', 'FEE', 'COMMISSION', 'ADJUSTMENT', 'REFUND'),
  entry_date DATE NOT NULL,
  description TEXT NOT NULL,
  source_document VARCHAR(100), -- Policy#, Payment#, etc.
  
  -- Audit trail
  created_by BIGINT UNSIGNED NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  approved_by BIGINT UNSIGNED,
  approved_at TIMESTAMP NULL,
  
  FOREIGN KEY (transaction_id) REFERENCES transactions(id),
  INDEX idx_journal_date (entry_date),
  INDEX idx_journal_type (entry_type)
);

CREATE TABLE journal_line (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  journal_entry_id BIGINT UNSIGNED NOT NULL,
  account_code VARCHAR(20) NOT NULL,
  account_name VARCHAR(100) NOT NULL,
  debit_amount DECIMAL(10,2) DEFAULT 0,
  credit_amount DECIMAL(10,2) DEFAULT 0,
  line_description VARCHAR(255),
  
  FOREIGN KEY (journal_entry_id) REFERENCES journal_entries(id),
  INDEX idx_line_entry (journal_entry_id),
  INDEX idx_line_account (account_code)
);
```

### Chart of Accounts

```sql
CREATE TABLE chart_of_accounts (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  account_code VARCHAR(20) UNIQUE NOT NULL,
  account_name VARCHAR(100) NOT NULL,
  account_type ENUM('ASSET', 'LIABILITY', 'EQUITY', 'REVENUE', 'EXPENSE'),
  parent_account_code VARCHAR(20),
  is_active BOOLEAN DEFAULT TRUE,
  normal_balance ENUM('DEBIT', 'CREDIT'),
  
  INDEX idx_coa_type (account_type),
  INDEX idx_coa_parent (parent_account_code)
);

-- Standard insurance accounts
INSERT INTO chart_of_accounts (account_code, account_name, account_type, normal_balance) VALUES
('1000', 'Cash', 'ASSET', 'DEBIT'),
('1200', 'Premiums Receivable', 'ASSET', 'DEBIT'),
('2000', 'Unearned Premium', 'LIABILITY', 'CREDIT'),
('2100', 'Claims Payable', 'LIABILITY', 'CREDIT'),
('3000', 'Retained Earnings', 'EQUITY', 'CREDIT'),
('4000', 'Premium Revenue', 'REVENUE', 'CREDIT'),
('4100', 'Fee Revenue', 'REVENUE', 'CREDIT'),
('5000', 'Commission Expense', 'EXPENSE', 'DEBIT'),
('5100', 'Claims Expense', 'EXPENSE', 'DEBIT');
```

## Automated Notices and Fees

### Notice Configuration

```sql
CREATE TABLE notice_configuration (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  program_id BIGINT UNSIGNED NOT NULL,
  notice_type ENUM('BILLING', 'LATE_FEE', 'CANCELLATION', 'REINSTATEMENT'),
  days_before_due INT, -- Negative for before, positive for after
  template_id BIGINT UNSIGNED NOT NULL,
  
  -- Fee configuration
  fee_amount DECIMAL(10,2),
  fee_type VARCHAR(50),
  
  is_active BOOLEAN DEFAULT TRUE,
  FOREIGN KEY (program_id) REFERENCES programs(id),
  FOREIGN KEY (template_id) REFERENCES communication_templates(id),
  INDEX idx_notice_program (program_id, notice_type)
);

-- Standard configurations
INSERT INTO notice_configuration (program_id, notice_type, days_before_due, fee_amount) VALUES
(1, 'BILLING', -20, NULL), -- 20 days before due
(1, 'LATE_FEE', 5, 5.00), -- 5 days after due, $5 fee
(1, 'CANCELLATION', 11, NULL), -- 11 days after due
(1, 'REINSTATEMENT', 1, NULL); -- 1 day after cancellation
```

### Automated Processing Service

```php
class AutomatedNoticeService {
    public function processDailyNotices() {
        // Billing notices
        $this->sendBillingNotices();
        
        // Late fees
        $this->applyLateFees();
        
        // Cancellation notices
        $this->sendCancellationNotices();
        
        // Process cancellations at 12:01am
        $this->processCancellations();
    }
    
    private function applyLateFees() {
        $overdueInstallments = Installment::where('status', 'PENDING')
            ->where('due_date', '<=', now()->subDays(5))
            ->whereNull('late_fee_applied_date')
            ->get();
            
        foreach ($overdueInstallments as $installment) {
            // Create late fee adjustment
            $this->createLateFeeAdjustment($installment);
            
            // Create journal entry
            $this->createLateFeeJournalEntry($installment);
            
            // Update installment
            $installment->late_fee_applied_date = now();
            $installment->total_amount += 5.00;
            $installment->save();
        }
    }
}
```

## Financial Adjustments System

### Adjustment Configuration

```sql
CREATE TABLE financial_adjustment_type (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  adjustment_code VARCHAR(20) UNIQUE NOT NULL,
  adjustment_name VARCHAR(100) NOT NULL,
  adjustment_category ENUM('PREMIUM', 'DISCOUNT', 'FEE', 'SURCHARGE', 'REINSTATEMENT', 'ENDORSEMENT', 'NSF', 'CHARGEBACK', 'COMMISSION'),
  calculation_basis ENUM('FLAT', 'PERCENTAGE', 'PRO_RATA', 'FORMULA'),
  
  -- Accounting configuration
  debit_account_code VARCHAR(20) NOT NULL,
  credit_account_code VARCHAR(20) NOT NULL,
  
  is_active BOOLEAN DEFAULT TRUE,
  FOREIGN KEY (debit_account_code) REFERENCES chart_of_accounts(account_code),
  FOREIGN KEY (credit_account_code) REFERENCES chart_of_accounts(account_code)
);

CREATE TABLE map_program_financial_adjustment (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  program_id BIGINT UNSIGNED NOT NULL,
  adjustment_type_id BIGINT UNSIGNED NOT NULL,
  is_required BOOLEAN DEFAULT FALSE,
  default_value DECIMAL(10,2),
  
  FOREIGN KEY (program_id) REFERENCES programs(id),
  FOREIGN KEY (adjustment_type_id) REFERENCES financial_adjustment_types(id),
  UNIQUE KEY uk_program_adjustment (program_id, adjustment_type_id)
);
```

### Proof Rules System

```sql
CREATE TABLE proof_condition_type (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  condition_code VARCHAR(50) UNIQUE NOT NULL,
  condition_name VARCHAR(100) NOT NULL,
  condition_category VARCHAR(50),
  required_document_types JSON, -- Array of document type codes
  validation_rules JSON, -- Rules for automatic validation
  
  is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE map_financial_adjustment_condition (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  adjustment_type_id BIGINT UNSIGNED NOT NULL,
  condition_type_id BIGINT UNSIGNED NOT NULL,
  is_mandatory BOOLEAN DEFAULT TRUE,
  
  FOREIGN KEY (adjustment_type_id) REFERENCES financial_adjustment_types(id),
  FOREIGN KEY (condition_type_id) REFERENCES proof_condition_types(id)
);
```

## Commission Management Enhancement

### Producer Transfer System

```sql
CREATE TABLE producer_transfer (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  policy_id BIGINT UNSIGNED NOT NULL,
  from_producer_id BIGINT UNSIGNED NOT NULL,
  to_producer_id BIGINT UNSIGNED NOT NULL,
  transfer_date DATE NOT NULL,
  transfer_reason TEXT,
  
  -- Journal reference
  journal_entry_id BIGINT UNSIGNED,
  
  -- Audit
  created_by BIGINT UNSIGNED NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  approved_by BIGINT UNSIGNED,
  approved_at TIMESTAMP NULL,
  
  FOREIGN KEY (policy_id) REFERENCES policies(id),
  FOREIGN KEY (from_producer_id) REFERENCES producers(id),
  FOREIGN KEY (to_producer_id) REFERENCES producers(id),
  FOREIGN KEY (journal_entry_id) REFERENCES journal_entries(id),
  INDEX idx_transfer_policy (policy_id)
);
```

### Commission Type Configuration

```sql
CREATE TABLE commission_type (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  commission_code VARCHAR(20) UNIQUE NOT NULL,
  commission_name VARCHAR(100) NOT NULL,
  commission_basis ENUM('NEW_BUSINESS_PERCENT', 'RENEWAL_FLAT', 'OVERRIDE_PERCENT'),
  
  is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE map_producer_commission (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  producer_id BIGINT UNSIGNED NOT NULL,
  program_id BIGINT UNSIGNED NOT NULL,
  commission_type_id BIGINT UNSIGNED NOT NULL,
  rate_value DECIMAL(10,4) NOT NULL, -- Percentage or flat amount
  effective_date DATE NOT NULL,
  expiration_date DATE,
  
  FOREIGN KEY (producer_id) REFERENCES producers(id),
  FOREIGN KEY (program_id) REFERENCES programs(id),
  FOREIGN KEY (commission_type_id) REFERENCES commission_types(id),
  INDEX idx_producer_commission (producer_id, program_id, effective_date)
);
```

## Special Flow Implementations

### Endorsement Processing

```php
class EndorsementService {
    public function processEndorsement($policy, $changes, $effectiveDate) {
        DB::transaction(function() use ($policy, $changes, $effectiveDate) {
            // Calculate pro-rata adjustment
            $adjustment = $this->calculateProRataAdjustment($policy, $changes, $effectiveDate);
            
            // Create journal entry
            $journalEntry = $this->createJournalEntry([
                'type' => 'ENDORSEMENT',
                'description' => 'Policy endorsement effective ' . $effectiveDate,
                'source_document' => $policy->policy_number
            ]);
            
            // Add journal lines
            if ($adjustment > 0) {
                // Additional premium
                $this->addJournalLine($journalEntry, '1200', 'Premiums Receivable', $adjustment, 0);
                $this->addJournalLine($journalEntry, '2000', 'Unearned Premium', 0, $adjustment);
            } else {
                // Return premium
                $this->addJournalLine($journalEntry, '2000', 'Unearned Premium', abs($adjustment), 0);
                $this->addJournalLine($journalEntry, '1200', 'Premiums Receivable', 0, abs($adjustment));
            }
            
            // Update installments if needed
            $this->redistributeInstallments($policy, $adjustment);
        });
    }
}
```

### Reinstatement Processing

```php
class ReinstatementService {
    private $reinstatementWindow = 30; // days
    
    public function processReinstatement($policy, $paymentAmount) {
        // Check reinstatement window
        $daysSinceCancellation = now()->diffInDays($policy->cancellation_date);
        
        if ($daysSinceCancellation > $this->reinstatementWindow) {
            throw new ReinstatementWindowExpiredException();
        }
        
        DB::transaction(function() use ($policy, $paymentAmount) {
            // Create reinstatement fee
            $reinstatementFee = $this->getReinstatementFee($policy);
            
            // Create journal entries
            $journalEntry = $this->createJournalEntry([
                'type' => 'REINSTATEMENT',
                'description' => 'Policy reinstatement',
                'source_document' => $policy->policy_number
            ]);
            
            // Journal lines for reinstatement
            $this->addJournalLine($journalEntry, '1000', 'Cash', $paymentAmount, 0);
            $this->addJournalLine($journalEntry, '4100', 'Fee Revenue', 0, $reinstatementFee);
            $this->addJournalLine($journalEntry, '1200', 'Premiums Receivable', 0, $paymentAmount - $reinstatementFee);
            
            // Generate new installment schedule
            $this->generateReinstatementSchedule($policy, $paymentAmount - $reinstatementFee);
        });
    }
}
```

## Real-Time Reporting

### KPI Calculations

```sql
-- Written Premium
CREATE VIEW vw_written_premium AS
SELECT 
  DATE_FORMAT(created_at, '%Y-%m') as month,
  SUM(CASE WHEN entry_type = 'PREMIUM' THEN credit_amount - debit_amount ELSE 0 END) as written_premium
FROM journal_entry je
JOIN journal_line jl ON je.id = jl.journal_entry_id
WHERE jl.account_code = '2000' -- Unearned Premium
GROUP BY DATE_FORMAT(created_at, '%Y-%m');

-- Earned Premium
CREATE VIEW vw_earned_premium AS
SELECT 
  DATE_FORMAT(entry_date, '%Y-%m') as month,
  SUM(debit_amount) as earned_premium
FROM journal_entry je
JOIN journal_line jl ON je.id = jl.journal_entry_id
WHERE jl.account_code = '2000' -- Unearned Premium
  AND je.entry_type = 'PREMIUM'
GROUP BY DATE_FORMAT(entry_date, '%Y-%m');

-- Cash Collections
CREATE VIEW vw_cash_collections AS
SELECT 
  DATE_FORMAT(entry_date, '%Y-%m') as month,
  SUM(debit_amount) as cash_collected
FROM journal_entry je
JOIN journal_line jl ON je.id = jl.journal_entry_id
WHERE jl.account_code = '1000' -- Cash
  AND je.entry_type = 'PAYMENT'
GROUP BY DATE_FORMAT(entry_date, '%Y-%m');
```

## Questions Requiring Clarification

### 1. Multi-Payment Handling
- When a payment spans multiple installments, should we:
  - Apply policy fees only to the first installment?
  - Distribute fees proportionally across all installments?
  - How do we handle SR-22 fees in multi-installment payments?

### 2. Producer Transfer Timing
- For producer transfers effective mid-month:
  - How do we split earned commission for that month?
  - Should future unearned commission go to new producer immediately?
  - What about commission already paid but not yet earned?

### 3. Reinstatement Fee Structure
- Is the reinstatement fee:
  - A flat amount per program?
  - A percentage of outstanding premium?
  - Variable based on days since cancellation?

### 4. NSF and Chargeback Handling
- For NSF payments that span multiple installments:
  - Do we reverse the entire payment allocation?
  - How do we handle partial NSF (some funds available)?
  - What's the re-presentment strategy?

### 5. Effective Date Changes
- For policies with effective date changes:
  - How do we handle already-sent notices?
  - Should we recalculate the entire payment schedule?
  - What about commission already earned on old dates?

## Implementation Priorities

### Phase 1: Core Double-Entry Foundation (Weeks 1-2)
1. Implement journal entry system
2. Create chart of accounts
3. Build transaction-to-journal mapping
4. Establish audit trail

### Phase 2: Dynamic Payment System (Weeks 3-4)
1. Build just-in-time installment generation
2. Implement payment allocation logic
3. Create date-driven payment plans
4. Add automated redistribution

### Phase 3: Automation Layer (Weeks 5-6)
1. Implement notice generation
2. Add automatic fee application
3. Build cancellation processing
4. Create reinstatement workflow

### Phase 4: Advanced Features (Weeks 7-8)
1. Producer transfer system
2. Complex endorsement handling
3. Real-time reporting views
4. Self-service configuration UI

## Success Criteria

### Accounting Integrity
- [ ] Assets = Liabilities + Equity balanced after every transaction
- [ ] Complete journal entries for all financial events
- [ ] Audit trail allows full transaction reconstruction
- [ ] No orphaned debits or credits

### Operational Excellence
- [ ] Automated notices sent exactly on schedule
- [ ] Fees applied consistently per configuration
- [ ] Cancellations processed at 12:01am precisely
- [ ] Reinstatements allowed within 30-day window

### Performance Targets
- [ ] Journal entry creation < 100ms
- [ ] Payment allocation < 200ms for 12 installments
- [ ] Real-time report generation < 1 second
- [ ] Batch notice processing: 10,000/hour

## Conclusion

Version 6 delivers a complete equity-based accounting system that is:
- **Legally Compliant** - True double-entry with complete audit trails
- **Operationally Efficient** - Automated notices, fees, and workflows
- **Infinitely Flexible** - Configuration-driven without code changes
- **User-Friendly** - Self-service configuration and real-time reporting

This architecture provides the foundation for a modern, scalable insurance accounting system that maintains financial integrity while supporting complex business requirements.

---

**Document Version**: 6.0  
**Date**: 2025-01-07  
**Status**: FINAL - Pending Clarification Questions  
**Key Addition**: Complete equity-based double-entry system with dynamic installment scheduling