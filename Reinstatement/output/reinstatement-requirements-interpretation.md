# Reinstatement with Lapse of Coverage Process Requirements

## Overview
This document provides a comprehensive interpretation of the reinstatement with lapse of coverage workflow for the Aguila Dorada Texas Personal Auto insurance program. This process applies to policies canceled for nonpayment and defines the complete business rules, calculations, and system requirements for policy reinstatement within the allowable time window.

## 1. Process Identification

### Process Details
- **Process Name**: Reinstatement with Lapse of Coverage
- **Applicable Policies**: Aguila Dorada Texas Personal Auto policies only
- **Cancellation Reason**: Nonpayment only
- **Reinstatement Window**: 30 days from cancellation date
- **Coverage Treatment**: Lapse in coverage applies - no coverage during gap period
- **Premium Treatment**: No premium earned during lapse period

### Key Business Rules
- **Eligibility Window**: Policies may be reinstated within 30 days of cancellation date
- **Rewrite Requirement**: Policies canceled for more than 30 days must be rewritten as new business
- **Coverage Gap**: No coverage exists during the lapse period - no backdating allowed
- **Premium Adjustment**: Premium must be recalculated based on remaining term
- **Payment Trigger**: Reinstatement occurs upon successful payment receipt

## 2. Eligibility Criteria

### Cancellation Requirements
- **Reason**: Policy must be canceled for nonpayment only
- **Status**: Policy must be in "Cancelled" status but within reinstatement window
- **Time Limit**: Cancellation date must be within 30 days of reinstatement request
- **Payment History**: May include unpaid premium prior to cancellation

### Exclusions
- **Voluntary Cancellations**: Policies canceled at customer request not eligible
- **Underwriting Cancellations**: Policies canceled for coverage reasons not eligible
- **Expired Window**: Policies canceled more than 30 days prior require rewrite
- **Fraud/Misrepresentation**: Policies canceled for fraud not eligible for reinstatement

## 3. Premium Calculation Methodology

### Daily Rate Calculation
- **Formula**: Daily Premium Rate = Total Policy Premium ÷ Total Term Days
- **Application**: Used to determine earned vs. unearned premium portions
- **Precision**: Calculate to nearest cent with standard rounding

### Remaining Premium Calculation
The system calculates remaining premium using the following methodology:

1. **Determine Lapse Period**
   - Lapse Start Date = Cancellation Date
   - Lapse End Date = Reinstatement Payment Date
   - Lapse Days = End Date - Start Date

2. **Calculate Unearned Premium for Lapse Period**
   - Lapsed Unearned Premium = Daily Premium Rate × Lapse Days
   - This amount is removed from total premium (no coverage provided)

3. **Calculate Remaining Policy Premium**
   - Remaining Term Days = Days from Reinstatement Date to Policy Expiration
   - Remaining Premium = Daily Premium Rate × Remaining Term Days

4. **Determine Total Amount Due**
   - Total Due = Remaining Premium + Unpaid Premium Prior to Cancellation + Applicable Fees

### Premium Calculation Example
**Scenario**: 
- Total Policy Premium: $600
- Policy Term: 180 days
- Canceled After: 90 days
- Reinstated on Day 105 (15-day lapse)
- Unpaid Premium Prior to Cancellation: $100
- Reinstatement Fee: $25
- Previous Payments Made: $200

**Calculation Steps**:
1. Daily Premium Rate = $600 ÷ 180 = $3.33
2. Lapsed Unearned Premium = 15 days × $3.33 = $49.95
3. Adjusted Total Premium = $600 - $49.95 = $550.05
4. Add Unpaid Premium = $550.05 + $100 = $650.05
5. Add Reinstatement Fee = $650.05 + $25 = $675.05
6. Subtract Previous Payments = $675.05 - $200 = $475.05
7. **Final Balance Due = $475.05**

## 4. Payment Processing and Installment Adjustment

### Payment Requirements
- **Full Payment**: All outstanding amounts must be paid to trigger reinstatement
- **Payment Methods**: All standard payment methods accepted
- **Payment Timing**: Reinstatement effective date = successful payment date and time
- **No Partial Payments**: Reinstatement requires full settlement of outstanding balance

### Installment Restructuring
After successful reinstatement payment, the system restructures remaining installments:

1. **Determine Remaining Installments**
   - Count installments with due dates after reinstatement date
   - If original schedule had 6 installments, determine how many remain

2. **Calculate Installment Amounts**
   - Divide remaining premium balance equally among remaining installments
   - Round to nearest cent with final installment absorbing variance

3. **Adjust for Immediate Due Date**
   - If reinstatement occurs within 10 days of next scheduled due date:
     - Deduct that installment from remaining balance
     - First installment becomes due immediately
   - If only one installment remains and within 10 days:
     - Entire remaining balance due immediately

### Installment Restructuring Example
Using the previous example with $475.05 remaining balance:
- **Remaining Installments**: 3
- **Standard Division**: $475.05 ÷ 3 = $158.35 per installment
- **Final Installment Adjustment**: $158.35 + $0.00 variance = $158.35
- **If Within 10 Days**: First $158.35 due immediately, remaining $316.70 split over 2 installments ($158.35 each)

## 5. System Workflow Requirements

### Cancellation State Management
1. **Upon Cancellation**:
   - System suspends coverage and billing
   - Premium accrual stops at cancellation date
   - Policy status changes to "Cancelled"
   - Reinstatement eligibility flag set to true
   - 30-day countdown timer initiated

2. **During Lapse Period**:
   - No coverage provided
   - No premium earned
   - Policy remains in "Cancelled" status
   - Reinstatement eligibility monitored daily
   - Customer communications may be sent

### Reinstatement Workflow
1. **Payment Receipt**:
   - System captures payment date and time
   - Payment amount validated against calculated balance
   - Upon successful payment, reinstatement process begins

2. **Reinstatement Processing**:
   - Coverage effective date = payment date/time
   - Policy status changes to "Active"
   - Premium recalculation executed
   - Installment schedule restructured
   - Billing cycle resumed

3. **Post-Reinstatement**:
   - Policy documents generated
   - Customer notifications sent
   - Billing schedule updated
   - Coverage verification available

### Expired Window Handling
- **After 30 Days**: Reinstatement eligibility expires
- **System Action**: Policy status changes to "Expired for Reinstatement"
- **Customer Options**: Must apply for new policy (rewrite process)
- **No Exceptions**: 30-day limit is absolute

## 6. Fee Structure and Timing

### Applicable Fees
1. **Reinstatement Fee**: $25.00 (as specified in program documentation)
2. **Installment Fees**: Apply to restructured payment schedule
3. **Late Fees**: May apply to unpaid amounts prior to cancellation
4. **NSF Fees**: $25.00 if previous payments were returned

### Fee Calculation Rules
- **Reinstatement Fee**: Always applies to successful reinstatements
- **Installment Fees**: Calculated based on new payment schedule
- **Late Fees**: Applied per original policy terms for past due amounts
- **All Fees**: Must be paid in full for reinstatement to proceed

## 7. Business Rules and Constraints

### Timing Rules
- **30-Day Absolute Limit**: No exceptions to reinstatement window
- **Payment Date Precision**: Reinstatement effective to the minute of payment
- **Weekend/Holiday Processing**: Payments accepted 24/7, reinstatement immediate
- **No Backdating**: Coverage never backdated to cancellation date

### Coverage Rules
- **Lapse Period**: No coverage exists during gap
- **No Claims**: Claims during lapse period not covered
- **Liability Gap**: Customer responsible for maintaining other coverage
- **Reinstatement Coverage**: Full policy coverage resumes at payment time

### Financial Rules
- **Premium Earned**: No premium earned during lapse period
- **Refund Calculation**: Lapsed premium removed from total policy premium
- **Payment Application**: Payments applied to oldest charges first
- **Full Settlement**: All outstanding amounts must be paid

### Exception Handling
- **Partial Payments**: Not accepted for reinstatement
- **Payment Failures**: Reinstatement fails, policy remains cancelled
- **System Errors**: Manual review required, customer notified
- **Disputed Amounts**: Must be resolved before reinstatement

## 8. Compliance and Regulatory Requirements

### Texas Insurance Requirements
- **Notice Requirements**: Customer must be notified of reinstatement rights
- **Documentation**: All reinstatement actions must be documented
- **Audit Trail**: Complete transaction history maintained
- **Regulatory Reporting**: Reinstatement activity reported as required

### Record Keeping
- **Transaction Logs**: All payment and reinstatement activities logged
- **Document Retention**: Reinstatement records maintained per regulation
- **Customer Communications**: All notices and correspondence archived
- **System Audit**: Complete audit trail of system actions

## 9. Customer Communication Requirements

### Notification Triggers
- **Cancellation Notice**: Must include reinstatement rights and timeline
- **Reminder Notices**: May be sent during 30-day window
- **Reinstatement Confirmation**: Sent upon successful reinstatement
- **Expiration Notice**: Sent when 30-day window expires

### Communication Content
- **Reinstatement Rights**: Clear explanation of 30-day window
- **Payment Requirements**: Exact amount due calculation
- **Coverage Gap**: Clear statement of no coverage during lapse
- **Contact Information**: How to proceed with reinstatement

## 10. Integration Requirements

### Payment System Integration
- **Real-Time Processing**: Immediate reinstatement upon payment
- **Payment Validation**: Verify sufficient funds and payment success
- **Fee Calculation**: Automatic calculation of all applicable fees
- **Billing System**: Integration with installment billing system

### Document Generation
- **Reinstatement Certificate**: Generated upon successful reinstatement
- **Updated Policy Documents**: Reflect new effective dates and terms
- **Payment Receipt**: Detailed breakdown of all amounts paid
- **Installment Schedule**: New payment schedule documentation

### Customer Service Integration
- **Account Status**: Real-time visibility into reinstatement eligibility
- **Payment Options**: All standard payment methods available
- **Balance Inquiry**: Exact reinstatement amount calculation
- **Status Updates**: Real-time updates on reinstatement processing

## Cross-References
- **Aguila Dorada Program Traits**: GR-63 for policy terms and fee structure
- **Payment Processing**: Standard payment handling procedures
- **Cancellation Procedures**: Standard cancellation workflow requirements
- **Customer Communications**: Standard notification requirements

## Validation Standards
This document serves as the authoritative source for:
- **System Development**: Technical implementation must reflect these business rules
- **Business Process**: All reinstatement procedures must follow these specifications
- **Customer Service**: Customer inquiries must be handled per these requirements
- **Compliance Verification**: Regulatory compliance measured against these standards

## Document Maintenance
- **Updates**: Changes to reinstatement rules require updates to this document
- **Versioning**: Maintain version history for audit trail
- **Approval**: All changes require business stakeholder approval
- **Distribution**: Updates must be communicated to all affected systems and personnel