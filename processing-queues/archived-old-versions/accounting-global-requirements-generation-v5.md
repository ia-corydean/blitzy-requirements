# Accounting Global Requirements Generation - Version 5 (Final Integration)

## Executive Summary

Version 5 represents the culmination of accounting requirements analysis, incorporating user feedback, Program Manager deep integration, and comprehensive research into fee stacking, commission handling, and audit requirements. This version provides clear, actionable specifications based on the understanding that:

1. **Policies are legal contracts** - Once bound, rates and terms are locked for the policy period
2. **Accounting is the foundation** - Flexible infrastructure supporting Program Manager configurations
3. **Equity-based payment system** - Allows dynamic redistribution of payments
4. **Complete audit transparency** - Every calculation step must be permanently preserved

## Key Clarifications from User Feedback

### Rate Change Philosophy
- **Rate changes affect only new business and renewals** - Existing policies maintain their original rates
- **Legal contract principle** - Bound policies represent fixed agreements for their term
- **Re-rating triggers**: Endorsements, renewals, and changes during RQB (Rate/Quote/Bind)
- **No mid-term rate adjustments** - Protects both insurer and insured

### Commission Processing Clarifications
- **EARNED basis uses monthly schedule** - Commissions recognized monthly over policy term
- **Cancellation handling** (Suggested approach):
  - **Pro-rata cancellations**: Return unearned commission proportionally
  - **Short-rate cancellations**: Apply penalty percentage to commission return
  - **Minimum earned period**: First 30 days commission always retained
- **No clawbacks after 90 days** - Provides producer income stability

### Payment System Flexibility
- **Equity-based redistribution** - Overpayments automatically spread across remaining installments
- **Dynamic payment plans** - System adjusts when payments exceed invoiced amounts
- **Due date modifications** - Allowed without changing core payment structure
- **No additional fees for redistribution** - Customer-friendly approach

## Enhanced Entity Analysis (Based on Research)

### Core Accounting Entities with Program Integration

1. **Transaction** (Final Structure)
   ```sql
   CREATE TABLE transaction (
     id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
     policy_id BIGINT UNSIGNED NOT NULL,
     program_version_id BIGINT UNSIGNED NOT NULL,
     transaction_type ENUM('PREMIUM', 'FEE', 'COMMISSION', 'PAYMENT', 'ADJUSTMENT'),
     transaction_subtype VARCHAR(50), -- Specific fee types, etc.
     amount DECIMAL(10,2) NOT NULL,
     
     -- Rating calculation audit
     base_premium DECIMAL(10,2),
     rate_calculation_log JSON NOT NULL, -- Complete step-by-step
     factor_application_order JSON NOT NULL, -- Exact sequence applied
     territory_snapshot JSON, -- ZIP-level factors at transaction time
     
     -- Fee calculation details
     fee_stack_order JSON, -- Order fees were applied
     fee_calculations JSON, -- Individual fee formulas/amounts
     
     -- Audit fields
     created_by BIGINT UNSIGNED NOT NULL,
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     
     FOREIGN KEY (policy_id) REFERENCES policies(id),
     INDEX idx_transaction_policy (policy_id),
     INDEX idx_transaction_type (transaction_type),
     INDEX idx_transaction_created (created_at)
   );
   ```

2. **RateCalculationLog** (Permanent Audit Trail)
   ```sql
   CREATE TABLE rate_calculation_log (
     id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
     transaction_id BIGINT UNSIGNED NOT NULL,
     step_number INT NOT NULL,
     step_description VARCHAR(255) NOT NULL,
     base_value DECIMAL(10,4) NOT NULL,
     factor_name VARCHAR(100),
     factor_value DECIMAL(10,6),
     running_total DECIMAL(10,4) NOT NULL,
     coverage_lines_affected JSON, -- Which coverages this factor applied to
     calculation_precision INT DEFAULT 3, -- Decimal places used
     
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     FOREIGN KEY (transaction_id) REFERENCES transactions(id),
     INDEX idx_calculation_transaction (transaction_id, step_number)
   );
   ```

3. **FeeApplication** (Fee Stacking Tracker)
   ```sql
   CREATE TABLE fee_application (
     id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
     transaction_id BIGINT UNSIGNED NOT NULL,
     fee_order INT NOT NULL, -- Application sequence
     fee_type ENUM('POLICY', 'MVCPA', 'INSTALLMENT', 'NSF', 'LATE', 'ENDORSEMENT', 'SR22'),
     base_amount DECIMAL(10,2),
     calculation_method VARCHAR(50), -- 'FLAT', 'PER_ENTITY', 'FORMULA'
     calculation_details JSON, -- Formula components for installment fees
     entity_count INT, -- For per-entity fees like MVCPA
     final_amount DECIMAL(10,2) NOT NULL,
     waived BOOLEAN DEFAULT FALSE,
     waive_reason VARCHAR(255),
     
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     FOREIGN KEY (transaction_id) REFERENCES transactions(id),
     INDEX idx_fee_transaction (transaction_id, fee_order)
   );
   ```

4. **PaymentPlanAdjustment** (Equity-Based Tracking)
   ```sql
   CREATE TABLE payment_plan_adjustment (
     id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
     payment_plan_id BIGINT UNSIGNED NOT NULL,
     adjustment_type ENUM('OVERPAYMENT', 'DUE_DATE_CHANGE', 'ENDORSEMENT', 'EFT_CHANGE'),
     original_installment_count INT,
     new_installment_count INT,
     redistribution_amount DECIMAL(10,2),
     affected_installments JSON, -- Which installments were modified
     adjustment_reason TEXT,
     
     created_by BIGINT UNSIGNED NOT NULL,
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     FOREIGN KEY (payment_plan_id) REFERENCES payment_plans(id),
     INDEX idx_adjustment_plan (payment_plan_id)
   );
   ```

5. **CommissionEarningSchedule** (Monthly Earning Tracker)
   ```sql
   CREATE TABLE commission_earning_schedule (
     id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
     commission_id BIGINT UNSIGNED NOT NULL,
     earning_month DATE NOT NULL,
     earned_amount DECIMAL(10,2) NOT NULL,
     payment_status ENUM('PENDING', 'SCHEDULED', 'PAID', 'CANCELLED'),
     cancellation_adjustment DECIMAL(10,2), -- For pro-rata/short-rate
     payment_date DATE,
     
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     FOREIGN KEY (commission_id) REFERENCES commissions(id),
     INDEX idx_earning_commission (commission_id, earning_month)
   );
   ```

### Fee Stacking Order (From Documentation Research)

Based on Program Manager documentation, the **definitive fee application order** is:

1. **Base Premium Calculation** (all multiplicative factors)
2. **Policy Fee** ($90 for 6-month policies)
3. **MVCPA Fee** ($2.50 per vehicle)
4. **Installment Fee** (if applicable, using progressive formula)
5. **Transaction Fees** (convenience fees by type)
6. **Event-Triggered Fees** (NSF, Late, Endorsement, SR-22)

**Critical Rule**: Fees are ALWAYS additive and applied AFTER all multiplicative rating factors.

### Commission Cancellation Handling (Recommendations)

1. **Pro-Rata Cancellations**
   ```
   Returned Commission = (Unearned Days / Total Days) × Total Commission
   Minimum Earned = MAX(30 days commission, 10% of total)
   ```

2. **Short-Rate Cancellations**
   ```
   Short Rate Penalty Table:
   - 0-30 days: 0% penalty (minimum earned period)
   - 31-60 days: 10% penalty
   - 61-90 days: 25% penalty
   - 91-180 days: 35% penalty
   - 181+ days: 40% penalty
   
   Returned Commission = Unearned Commission × (1 - Penalty Rate)
   ```

3. **Earned Basis Adjustments**
   - Stop future earning schedule entries
   - Calculate earned-to-date vs paid-to-date
   - Create adjustment transaction for difference

## Implementation Requirements (Final)

### Service Architecture Updates

1. **RatingCalculationService** (Enhanced)
   ```php
   class RatingCalculationService {
       public function calculatePremium($quote, $program) {
           $log = new RateCalculationLog();
           $runningTotal = $this->getBasePremium($quote, $program);
           
           // Apply factors in program-defined order
           foreach ($program->getRatingOrder() as $factor) {
               $factorValue = $this->getFactorValue($factor, $quote);
               $newTotal = $runningTotal * $factorValue;
               
               $log->addStep([
                   'description' => $factor->getName(),
                   'base_value' => $runningTotal,
                   'factor_value' => $factorValue,
                   'running_total' => round($newTotal, 3),
                   'coverage_lines' => $factor->getCoverageLines()
               ]);
               
               $runningTotal = $newTotal;
           }
           
           return ['premium' => round($runningTotal), 'log' => $log];
       }
   }
   ```

2. **FeeStackingService** (New)
   ```php
   class FeeStackingService {
       private $feeOrder = [
           'POLICY' => 1,
           'MVCPA' => 2,
           'INSTALLMENT' => 3,
           'CONVENIENCE' => 4,
           'NSF' => 5,
           'LATE' => 6,
           'ENDORSEMENT' => 7,
           'SR22' => 8
       ];
       
       public function applyFees($transaction, $policy, $program) {
           $fees = [];
           $totalFees = 0;
           
           // Apply fees in defined order
           foreach ($this->feeOrder as $feeType => $order) {
               if ($this->feeApplies($feeType, $transaction, $policy)) {
                   $fee = $this->calculateFee($feeType, $policy, $program);
                   $fees[] = [
                       'order' => $order,
                       'type' => $feeType,
                       'amount' => $fee['amount'],
                       'calculation' => $fee['details']
                   ];
                   $totalFees += $fee['amount'];
               }
           }
           
           return ['fees' => $fees, 'total' => $totalFees];
       }
   }
   ```

3. **EquityPaymentService** (New)
   ```php
   class EquityPaymentService {
       public function processOverpayment($payment, $paymentPlan) {
           $overpayment = $payment->amount - $payment->invoiced_amount;
           
           if ($overpayment > 0) {
               $remainingInstallments = $paymentPlan->getRemainingInstallments();
               $redistributionAmount = $overpayment / count($remainingInstallments);
               
               foreach ($remainingInstallments as $installment) {
                   $installment->amount -= $redistributionAmount;
                   $installment->save();
               }
               
               // Check if last installment can be removed
               $lastInstallment = end($remainingInstallments);
               if ($lastInstallment->amount <= 0) {
                   $lastInstallment->status = 'PAID_BY_OVERPAYMENT';
                   $lastInstallment->save();
               }
               
               // Log adjustment
               PaymentPlanAdjustment::create([
                   'payment_plan_id' => $paymentPlan->id,
                   'adjustment_type' => 'OVERPAYMENT',
                   'redistribution_amount' => $overpayment,
                   'affected_installments' => $remainingInstallments->pluck('id')
               ]);
           }
       }
   }
   ```

### Business Rules (Final Specifications)

1. **Rate Locking Rules**
   - Rates locked at bind time using ProgramSnapshot
   - Endorsements use original program version unless re-rate triggered
   - Renewals always use current program version
   - Territory changes apply only at renewal

2. **EFT Discount Management**
   - Applied immediately when customer enrolls
   - Removable only via endorsement
   - Failures create suspense for underwriting review
   - Failed EFT doesn't automatically remove discount

3. **Fee Waiver Authority**
   - Handled through Underwriting system
   - Requires approval workflow
   - Maintains audit trail of waiver reason
   - Doesn't affect fee stacking order

4. **Installment Fee Formula** (From Documentation)
   ```
   For 6-month policies:
   Base Fee = $3.50 (for first $250 of premium)
   Additional = $0.50 per $125 increment above $250
   
   Example: $600 premium
   - First $250: $3.50
   - Next $350: ceil(350/125) × $0.50 = 3 × $0.50 = $1.50
   - Total: $3.50 + $1.50 = $5.00
   ```

### Regulatory Reporting Format (Recommendations)

1. **Transaction Detail Report**
   ```
   Policy#|Trans Date|Type|Program Version|Base Premium|Total Factors|Fees|Final Amount|Calculation Hash
   ```

2. **Rate Calculation Audit Report**
   ```
   Policy#|Step|Description|Base|Factor|New Total|Coverage Lines|Precision
   ```

3. **Commission Tracking Report**
   ```
   Producer#|Policy#|Basis|Rate|Premium Base|Commission|Earned Date|Paid Date|Status
   ```

4. **Fee Application Report**
   ```
   Policy#|Fee Type|Order Applied|Calculation Method|Base Amount|Entity Count|Final Amount|Waived
   ```

## Audit and Compliance Requirements (Final)

### Permanent Retention Requirements
- **All bound policy calculations** - Retained forever
- **All endorsement calculations** - Retained forever
- **Quote calculations** - Retained 90 days (unless bound)
- **Program snapshots** - Retained forever for bound policies

### Calculation Transparency Standards
Every rate calculation must capture:
1. Program version and configuration snapshot
2. Base premium by coverage line
3. Each factor applied in sequence with:
   - Factor name and value
   - Coverage lines affected
   - Running total after application
   - Decimal precision used
4. Fee application order and amounts
5. Total premium components breakdown
6. Calculation timestamp and hash for verification

### Program Version Audit Trail
- Track all program changes with version numbers
- Log who published and when
- Maintain revision history with change descriptions
- Show which policies used which program version
- Enable reconstruction of any historical calculation

## Migration Path from v4 to v5

### Database Enhancements
1. Add rate_calculation_log table for permanent audit trails
2. Add fee_application table for fee stacking tracking
3. Add payment_plan_adjustment for equity-based changes
4. Add commission_earning_schedule for monthly tracking
5. Enhance transaction table with calculation fields

### Service Layer Updates
1. Implement RatingCalculationService with full logging
2. Create FeeStackingService with proper ordering
3. Add EquityPaymentService for overpayment handling
4. Enhance CommissionService with earning schedules
5. Update all services to create permanent audit trails

### Business Logic Implementation
1. Enforce rate locking at bind time
2. Implement equity-based payment redistribution
3. Add commission cancellation calculations
4. Create EFT failure suspense workflow
5. Build comprehensive audit reports

## Success Criteria (Final)

### Functional Success
- [ ] Every calculation reproducible from audit logs
- [ ] Equity-based payments redistribute automatically
- [ ] Commission earning schedules track monthly
- [ ] Fee stacking follows documented order exactly
- [ ] Rate changes never affect in-force policies

### Technical Success  
- [ ] Permanent audit trails for all bound policies
- [ ] Sub-second fee calculation performance
- [ ] Real-time payment redistribution
- [ ] Comprehensive regulatory reports available
- [ ] Zero data loss for financial calculations

### Compliance Success
- [ ] Meet all regulatory audit requirements
- [ ] Provide complete calculation transparency
- [ ] Support examiner reconstruction of any transaction
- [ ] Maintain legal contract integrity for policies
- [ ] Enable historical rate analysis and reporting

## Conclusion

Version 5 represents a complete, implementation-ready specification that:
- Respects policies as legal contracts with locked rates
- Provides flexible, equity-based payment management
- Ensures complete calculation transparency and permanent audit trails
- Integrates seamlessly with Program Manager configurations
- Supports all regulatory and compliance requirements

The accounting infrastructure serves as the foundation that Program Manager builds upon, flexible enough to support any configuration while maintaining rigorous financial controls and audit capabilities.

---

**Document Version**: 5.0  
**Date**: 2025-01-07  
**Status**: FINAL - Ready for Implementation  
**Research Completed**: Fee stacking order, program version management, audit requirements