# Accounting Global Requirements Generation - Version 8 (Enhanced Payment Workflows)

## Executive Summary

Version 8 enhances the accounting requirements with detailed payment workflow specifications from the Make A Payment documentation. The system maintains its foundation on transaction and transaction_line tables while providing comprehensive payment processing capabilities for both online and mailed-in payments. This version ensures we keep the accounting foundation simple while supporting complex business requirements.

## Core Business Principles

### 1. Equity-Based Accounting System
- Every financial transaction must maintain the fundamental accounting equation: Assets = Liabilities + Equity
- All business events must generate balanced journal entries with equal debits and credits
- No single-entry shortcuts or unbalanced transactions permitted
- Complete audit trail from business event to financial impact

### 2. Program-Centric Configuration
- Each insurance program defines its own financial rules and configurations
- Payment plans, fee structures, and commission rates are program-specific
- Business rules must be configurable without code changes
- Self-service administration for program managers

### 3. Audit-First Design
- Every financial transaction must be traceable to its originating business event
- Permanent retention of all financial calculations for bound policies
- Complete transparency in premium calculations and fee applications
- Real-time financial reporting without batch processing dependencies

### 4. Modular and Extensible
- New fee types, adjustment reasons, and payment methods through configuration
- Flexible commission structures supporting various calculation bases
- Extensible proof rules and document requirements
- Gateway integration flexibility for payment processors

## Functional Requirements

### Transaction Management

#### Core Transaction Requirements
- Support for all insurance business events: quotes, bindings, endorsements, cancellations, reinstatements
- Transaction types must include: PREMIUM, FEE, COMMISSION, PAYMENT, ADJUSTMENT, REFUND
- Each transaction must capture the complete context of the business event
- Transactions must be immutable once created (no edits, only adjustments)

#### Transaction Components
- Every transaction must break down into detailed line items
- Line items must specify: account classification, debit/credit amounts, component type
- Component types include: PREMIUM, POLICY_FEE, MVCPA_FEE, SR22_FEE, INSTALLMENT_FEE, COMMISSION, TAX
- Support for jurisdiction-specific fee requirements

### Payment Processing Workflows

#### Payment Method Support
The system must support multiple payment methods with consistent processing rules:
- **Credit Card**: Real-time processing through payment gateway
- **ACH (Insured E-Check)**: Electronic check processing from insureds
- **Agent E-Check (Sweep)**: Agency account sweep payments
- **Mailed-In Payment**: Physical check and money order processing

#### Mailed-In Payment Processing
When processing physical payments, the system must capture:
- **Postmarked Date**: Date payment was mailed (for timeliness determination)
- **Payment Type**: Check or money order
- **Check Number**: For tracking and reconciliation
- **Check Amount**: Payment amount to be applied

#### Payment Application Rules

##### Full Payment Scenario
When payment equals or exceeds the billed invoice amount:
1. Apply payment to the billed unsatisfied invoice
2. If payment exceeds invoice amount:
   - Apply balance to policy balance
   - Recalculate all future bills based on new balance
   - System may eliminate final installments if overpayment is sufficient

##### Partial Payment Scenario
When payment is less than the billed invoice amount:
1. System must determine if payment provides enough premium to carry policy to next due date + 11/12 days
2. If sufficient coverage exists:
   - Satisfy the current bill
   - Apply shortage to policy balance
   - Recalculate all future bills
3. If insufficient coverage:
   - Apply payment to current bill
   - Leave difference as open invoice
   - If cancellation not already pending:
     - Calculate paid-to date
     - Process cancellation based on paid-to date
     - Prevent unnecessary refunds

#### Batch Payment Processing

##### Batch Payment Functionality
- Separate function for processing multiple mailed payments simultaneously
- System automatically generates batch numbers for tracking
- Running batch total for reconciliation
- Report view of all posted items in batch

##### Required Batch Fields
- Policy Number
- Postmarked Date
- Payment Type
- Check Number
- Check Amount

##### System-Generated Batch Fields
- Batch Number (auto-generated)
- Batch Total (running tally)
- Processing timestamp

##### Policy Validation Display
When entering policy number, system must display:
- Name of Insured
- Address
- Policy Status (Active, Pending, or Cancelled)
- Payment Due Date
- Payment Amount Due

### Payment Plan Management

#### Payment Plan Options
- **Percent-Based Down Payment Plans**: Support standard percentages (16.67%, 25%, 50%, 100%)
- **Date-Driven Payment Plans**: Allow agents to select specific due dates with automatic down payment calculation
- **Flexible Installment Counts**: Support various installment options (4, 5, 6, 12 payments)
- **Paid-in-Full Options**: Single payment with appropriate discounts

#### Dynamic Installment Generation
- First installment must be created at policy binding
- Subsequent installments generated just-in-time as previous ones are paid
- System must maintain 2-3 future installments for visibility
- Each installment must show itemized components:
  - Premium portion (calculated as daily rate × days in period)
  - Applicable fees broken down by type
  - Total amount due

#### Payment Processing Rules
- **Full Payment Allocation Only**: No partial payment acceptance at transaction level
- **Oldest-First Application**: Payments apply to oldest pending installments first
- **Multi-Installment Payments**: Single payment can satisfy multiple installments
- **Overpayment Handling**: Excess amounts redistribute across remaining installments
- **Equity-Based Redistribution**: Overpayments may eliminate final installments

### Cancellation Management

#### Cancellation Timing Rules
- Calculate days of coverage based on payment amount
- Determine cancellation effective date to prevent refunds when possible
- 11/12 day grace period calculation for pending cancellations
- Automatic cancellation processing at 12:01 AM on cancellation date

#### Paid-To Date Calculations
- System must calculate exact paid-to date based on:
  - Premium paid
  - Daily premium rate
  - Days of coverage provided
- Prevent cancellation if payment extends coverage beyond grace period

### Fee Management

#### Fee Application Order
Based on Program Manager requirements, fees must be applied in this specific order:
1. Base premium calculation (after all rating factors)
2. Policy fee
3. MVCPA fee (per vehicle)
4. Installment fee (if applicable)
5. Transaction-specific fees
6. Event-triggered fees (NSF, late, endorsement, SR-22)

#### Fee Categories
- **Policy-Level Fees**: Applied once per policy
- **Entity-Based Fees**: Applied per entity (e.g., per vehicle for MVCPA)
- **Transaction Fees**: Based on transaction type
- **Event-Triggered Fees**: Applied when specific events occur
- **Installment Fees**: Applied to each payment installment

#### Fee Configuration Requirements
- All fee amounts must be program-configurable
- Support for flat fees and percentage-based fees
- Complex formula support for installment fees
- Fee waiver capability with approval workflow
- Audit trail for all fee applications and waivers

### Commission Management

#### Commission Calculation Bases
- **Written Basis**: Commission calculated at policy binding
- **Earned Basis**: Commission recognized monthly over policy term
- **Collected Basis**: Commission calculated as payments are collected

#### Commission Structure Requirements
- Support for new business and renewal commission rates
- Program-specific default rates with producer-level overrides
- Term-specific commission rates (6-month vs 12-month policies)
- No commission clawbacks after 90 days
- Single producer per policy (no commission splits)

#### Commission Processing
- Monthly earning schedules for earned basis commissions
- Automatic commission calculation at triggering events
- Support for commission adjustments and corrections
- Producer transfer capability with proper accounting

### Automated Workflows

#### Notice Generation
- **Billing Notices**: Generate 20 days before installment due date
- **Late Notices**: Generate after grace period expiration
- **Cancellation Warnings**: Send 11 days after due date for non-payment
- **Reinstatement Offers**: Available for 30 days post-cancellation

#### Automatic Fee Application
- **Late Fees**: Apply $5 fee 5 days after due date if unpaid
- **NSF Fees**: Apply upon payment rejection
- **Reinstatement Fees**: Apply when processing reinstatements

### Special Business Processes

#### Endorsements
- Pro-rata premium adjustments for coverage changes
- Mid-term addition/removal of vehicles, drivers, or coverages
- Automatic recalculation of remaining installments
- Proper accounting for premium increases or decreases

#### Reinstatements
- Accept reinstatements within 30-day window
- Calculate reinstatement fees based on program rules
- Generate new payment schedule from reinstatement date
- Maintain complete audit trail of lapse period

#### Effective Date Changes
- Support policy effective date modifications
- Recalculate premium based on new term
- Adjust payment schedules accordingly
- No reversal of existing transactions

#### Producer Transfers
- Transfer policy servicing between producers
- Determine commission rights based on transfer date
- Maintain historical producer relationships
- Generate appropriate accounting entries

### Financial Adjustments

#### Adjustment Types
- Premium adjustments (increases/decreases)
- Fee waivers with approval workflow
- Commission corrections
- Refund processing
- NSF and chargeback handling

#### Adjustment Requirements
- All adjustments must create balanced journal entries
- Require appropriate authorization based on amount
- Include detailed reason codes and documentation
- Maintain complete audit trail
- Support bulk adjustments for system corrections

### Reporting Requirements

#### Real-Time Financial Reports
- Written premium by period
- Earned premium recognition
- Cash collections summary
- Outstanding receivables aging
- Commission liability tracking
- Fee revenue analysis
- Batch payment reconciliation reports

#### Payment Reports
- Daily payment summary by type
- Mailed payment processing log
- Batch totals and reconciliation
- Payment allocation details
- Partial payment tracking
- Overpayment redistribution audit

#### Audit Reports
- Transaction detail with full journal entries
- Rate calculation transparency reports
- Fee application audit trails
- Commission calculation details
- Payment allocation history
- Adjustment activity reports

#### Reconciliation Support
- Bank reconciliation capabilities
- Commission reconciliation reports
- Premium reconciliation by program
- Payment gateway reconciliation
- General ledger integration support
- Batch payment reconciliation

## Integration Requirements

### Payment Gateway Integration
- Support for multiple payment processors
- Real-time payment verification
- Tokenization for stored payment methods
- Automatic retry logic for failed payments
- Comprehensive payment status tracking

### Banking Integration
- ACH processing for agent payments
- Positive Pay file generation
- Bank account verification
- Electronic funds transfer support
- Check printing capabilities (limited scope)
- Check imaging integration (future consideration)

### External System Integration
- General ledger system interfaces
- Commission payment systems
- Document management integration
- Communication system for notices
- Regulatory reporting interfaces

## Compliance Requirements

### Regulatory Compliance
- Support state-specific fee requirements
- Maintain audit trails for regulatory examinations
- Generate required financial reports
- Support rate filing documentation
- Enable compliance monitoring

### Data Retention
- Permanent retention for bound policy calculations
- 7-year retention for financial transactions
- 90-day retention for quote calculations
- Audit log retention per regulatory requirements
- Payment documentation retention standards

### Security and Privacy
- Role-based access to financial data
- Encryption of sensitive financial information
- PCI compliance for payment data
- Audit logging of all financial operations
- Data masking for non-production environments

## Business Rules Summary

### Payment Rules
1. Payments apply to billed unsatisfied invoices first
2. Overpayments redistribute to policy balance and future bills
3. Partial payments evaluated for coverage sufficiency
4. Cancellation prevention when payment extends coverage
5. All payments must create journal entries

### Invoice Rules
1. Bills remain open until fully satisfied
2. Partial payments may satisfy bills if coverage sufficient
3. Open invoices trigger cancellation workflows
4. Future bills recalculate based on policy balance changes
5. Invoice aging drives notice generation

### Batch Processing Rules
1. Each batch receives unique system-generated number
2. Batch totals maintained for reconciliation
3. Policy validation required before payment posting
4. Report generation for all batch items
5. Audit trail for batch processing

### Commission Rules
1. Commission rates from Program Manager
2. No clawbacks after 90 days
3. Monthly earning for earned basis
4. Single producer per policy
5. Transfer capability with accounting

### Fee Rules
1. Fees always apply after premium calculation
2. Application order must be maintained
3. Program-specific fee amounts
4. Waiver requires approval
5. All fees must be journalized

### Cancellation Rules
1. Calculate paid-to date to prevent refunds
2. 11/12 day grace period standard
3. Automatic at 12:01 AM on cancellation date
4. 30-day reinstatement window
5. Commission adjustments as appropriate

## Questions for Complete Accounting Gameplan

### Payment Processing Questions
1. **Check Imaging Integration**: Should the system integrate with bank check imaging systems for Day 2 functionality?
2. **Payment Rejection Handling**: How should the system handle partial NSF situations where some funds are available?
3. **Payment Priority**: When multiple policies have payments due, what determines application priority?

### Cancellation Logic Questions
1. **Grace Period Variability**: Is the 11/12 day grace period fixed or program-configurable?
2. **Refund Prevention**: What are acceptable tolerances for cancellation date adjustment to prevent small refunds?
3. **Multi-State Operations**: How do state-specific cancellation rules override standard logic?

### Batch Processing Questions
1. **Batch Reversal**: What is the process for reversing an entire batch if errors are discovered?
2. **Partial Batch Posting**: Can batches be partially posted if some payments have errors?
3. **Batch Approval**: Is management approval required for batches over certain thresholds?

### Commission Questions
1. **Split Commissions**: While currently single producer, should the system be designed to support future splits?
2. **Commission Advances**: How should the system handle commission advances or draws?
3. **Hierarchy Commissions**: Should the system support agency hierarchy override commissions?

### Reconciliation Questions
1. **Timing Differences**: How should the system handle timing differences between payment posting and bank clearance?
2. **Automated Matching**: What tolerance levels are acceptable for automated payment matching?
3. **Exception Handling**: What workflow should handle reconciliation exceptions?

### Future Considerations
1. **Electronic Payment Growth**: How should the system prepare for decreasing physical check volume?
2. **Real-Time Payments**: Should the system prepare for instant payment networks?
3. **Cryptocurrency**: Should the architecture consider future alternative payment methods?

## Success Criteria

### Functional Success
- Complete equity-based accounting with balanced transactions
- Automated payment processing and allocation
- Intelligent partial payment handling
- Comprehensive batch payment capabilities
- Full commission calculation support

### Operational Success
- Real-time financial reporting
- Automated notice generation
- Minimal manual intervention required
- Self-service configuration capabilities
- Complete audit transparency

### Compliance Success
- Meet all regulatory requirements
- Provide examination-ready audit trails
- Support required financial reports
- Maintain data retention standards
- Enable compliance monitoring

## Conclusion

Version 8 provides a comprehensive accounting system that balances simplicity with functionality. By maintaining transaction and transaction_line as the core tables, the system stays architecturally clean while supporting complex payment workflows, intelligent payment allocation, and comprehensive batch processing capabilities.

The addition of detailed payment workflows ensures the system can handle both modern electronic payments and traditional mailed payments efficiently. The focus on preventing unnecessary refunds through intelligent cancellation date calculation demonstrates fiscal responsibility while maintaining compliance requirements.

This design provides the flexibility needed for insurance operations while maintaining the rigor required for financial integrity and regulatory compliance.

---

**Document Version**: 8.0  
**Date**: 2025-01-07  
**Status**: FINAL - Enhanced with Payment Workflows  
**Key Addition**: Comprehensive payment processing workflows and batch capabilities