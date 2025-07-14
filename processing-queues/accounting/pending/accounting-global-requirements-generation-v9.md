# Accounting Global Requirements Generation - Version 9 (Paysafe Integration)

## Executive Summary

Version 9 enhances the accounting requirements by integrating Paysafe's secure payment tokenization platform while removing batch check processing functionality. The system maintains its foundation on transaction and transaction_line tables, ensuring zero storage of sensitive payment data through Paysafe's token-based architecture. This version incorporates program-configurable grace periods, ACH NACHA file generation for positive pay, and maintains the principle that full minimum down payment is required for all transactions.

## Core Business Principles

### 1. Equity-Based Accounting System
- Every financial transaction must maintain the fundamental accounting equation: Assets = Liabilities + Equity
- All business events must generate balanced journal entries with equal debits and credits
- No single-entry shortcuts or unbalanced transactions permitted
- Complete audit trail from business event to financial impact

### 2. Program-Centric Configuration
- Each insurance program defines its own financial rules and configurations
- Payment plans, fee structures, and commission rates are program-specific
- Grace periods are program-configurable (not fixed at 11/12 days)
- Business rules must be configurable without code changes
- Self-service administration for program managers

### 3. Zero Sensitive Data Storage
- No credit card numbers or bank account details stored in our database
- All payment methods represented by Paysafe tokens
- Payment data secured by Paysafe's PCI-certified infrastructure
- Only tokens and non-sensitive metadata retained locally

### 4. Audit-First Design
- Every financial transaction must be traceable to its originating business event
- Permanent retention of all financial calculations for bound policies
- Complete transparency in premium calculations and fee applications
- Real-time financial reporting without batch processing dependencies

### 5. Modular and Extensible
- New fee types, adjustment reasons, and payment methods through configuration
- Flexible API interface for connecting to payment gateways/providers
- Extensible proof rules and document requirements
- Support for future payment innovations through gateway abstraction

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

### Payment Processing with Paysafe Integration

#### Token-Based Payment Architecture
- **Customer Entry**: Payment information entered through Paysafe's secure hosted fields
- **Direct Transmission**: Data sent directly to Paysafe, bypassing our servers
- **Token Reception**: Paysafe returns unique tokens representing payment methods
- **Local Storage**: Only tokens and non-sensitive metadata stored in our system
- **Payment Processing**: All transactions use tokens through Paysafe's API

#### Payment Method Support
The system must support multiple payment methods through Paysafe tokenization:
- **Credit Card**: Real-time processing with zero-dollar authorization
- **ACH (Insured E-Check)**: Electronic check processing with bank validation
- **Agent E-Check (Sweep)**: Agency account sweep payments
- **Mailed-In Payment**: Physical check and money order processing (single check posting only)

#### What We Store Locally
- Paysafe token (unique identifier)
- Payment method type (card/bank)
- Last 4 digits (for display only)  
- Expiration date (for monitoring)
- Customer-defined nickname
- Verification status and history
- Transaction identifiers and amounts

#### Mailed-In Payment Processing
When processing physical payments, the system must capture:
- **Postmarked Date**: Date payment was mailed (for timeliness determination)
- **Payment Type**: Check or money order
- **Check Number**: For tracking and reconciliation
- **Check Amount**: Payment amount to be applied

#### Payment Application Rules

##### Full Payment Requirement
- **Minimum Down Payment**: Full minimum down payment required for all transactions
- **No Partial Initial Payments**: System rejects any payment less than required minimum
- **Payment Validation**: Real-time verification against policy requirements

##### Payment Allocation Scenario
When payment equals or exceeds the billed invoice amount:
1. Apply payment to the billed unsatisfied invoice
2. If payment exceeds invoice amount:
   - Apply balance to policy balance
   - Recalculate all future bills based on new balance
   - System may eliminate final installments if overpayment is sufficient

##### Insufficient Payment Handling
When payment is less than the billed invoice amount:
1. System validates against full minimum down requirement
2. If payment meets minimum requirements:
   - Determine if payment provides enough premium to carry policy to next due date + grace period
   - If sufficient coverage exists:
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
- **Per-Policy Basis**: All premium payments processed independently per policy

### Cancellation Management

#### Cancellation Timing Rules
- **Program-Configurable Grace Periods**: Each program defines its own grace period (not fixed at 11/12 days)
- Calculate days of coverage based on payment amount
- Determine cancellation effective date to prevent refunds when possible
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
- Design should naturally accommodate future split capability without overcomplication
- No commission advances supported

#### Commission Processing
- Monthly earning schedules for earned basis commissions
- Automatic commission calculation at triggering events
- Support for commission adjustments and corrections
- Producer transfer capability with proper accounting

### Automated Workflows

#### Notice Generation
- **Billing Notices**: Generate 20 days before installment due date
- **Late Notices**: Generate after grace period expiration
- **Cancellation Warnings**: Send based on program-configured grace period
- **Reinstatement Offers**: Available for 30 days post-cancellation

#### Automatic Fee Application
- **Late Fees**: Apply $5 fee 5 days after due date if unpaid
- **NSF Fees**: Apply upon payment rejection
- **Reinstatement Fees**: Apply when processing reinstatements

### Banking Integration

#### ACH NACHA File Generation
- Generate ACH NACHA files for positive pay verification
- Support automated file transmission to banking partners
- Maintain audit trail of all generated files
- Enable timing difference management through positive pay

#### Electronic Banking Features
- Bank account verification through Paysafe
- Electronic funds transfer support
- Check printing capabilities for single checks
- Reconciliation file imports

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

#### Payment Reports
- Daily payment summary by type
- Mailed payment processing log
- Payment allocation details
- Partial payment tracking
- Overpayment redistribution audit
- Token usage analytics

#### Audit Reports
- Transaction detail with full journal entries
- Rate calculation transparency reports
- Fee application audit trails
- Commission calculation details
- Payment allocation history
- Adjustment activity reports

#### Reconciliation Support
- Bank reconciliation capabilities with positive pay
- Commission reconciliation reports
- Premium reconciliation by program
- Payment gateway reconciliation
- General ledger integration support
- ACH file reconciliation

## Integration Requirements

### Paysafe Payment Gateway Integration
- Token-based payment processing
- Real-time payment verification
- Automatic retry logic for failed payments
- Comprehensive payment status tracking
- Support for 100+ payment methods through single integration

### Banking Integration
- ACH NACHA file generation for positive pay
- Bank account verification through Paysafe
- Electronic funds transfer support
- Check printing capabilities (single checks only)

### External System Integration
- General ledger system interfaces
- Commission payment systems
- Document management integration
- Communication system for notices
- Regulatory reporting interfaces

## Program-Specific Configuration

### Cancellation Rules
All cancellation rules are configured at the program level:
- Grace period duration (configurable per program)
- Cancellation calculation methods
- Refund prevention tolerances
- Notice timing requirements

### Program Structure
- One state per program
- Rating is per program
- Policies are rated per program
- All business rules cascade from program configuration

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
- Payment token retention per Paysafe agreements

### Security and Privacy
- Zero storage of sensitive payment data
- Role-based access to financial data
- Reduced PCI compliance scope through tokenization
- Audit logging of all financial operations
- Data masking for non-production environments

## Business Rules Summary

### Payment Rules
1. Full minimum down payment required
2. Payments apply to billed unsatisfied invoices first
3. Overpayments redistribute to policy balance and future bills
4. All payments processed on per-policy basis
5. All payments must create journal entries

### Invoice Rules
1. Bills remain open until fully satisfied
2. Partial payments evaluated against minimum requirements
3. Open invoices trigger cancellation workflows
4. Future bills recalculate based on policy balance changes
5. Invoice aging drives notice generation

### Commission Rules
1. Commission rates from Program Manager
2. No clawbacks after 90 days
3. Monthly earning for earned basis
4. Single producer per policy (future split capability in design)
5. No commission advances

### Fee Rules
1. Fees always apply after premium calculation
2. Application order must be maintained
3. Program-specific fee amounts
4. Waiver requires approval
5. All fees must be journalized

### Cancellation Rules
1. Calculate paid-to date to prevent refunds
2. Program-configurable grace periods
3. Automatic at 12:01 AM on cancellation date
4. 30-day reinstatement window
5. Commission adjustments as appropriate

## Questions for Complete Accounting Implementation

### Refund Prevention Tolerances
1. **Small Refund Threshold**: What dollar amount is considered a "small refund" that should be prevented through cancellation date adjustment?
2. **Date Adjustment Limits**: How many days can the cancellation date be adjusted to prevent refunds?
3. **Customer Communication**: Should customers be notified when cancellation dates are adjusted to prevent refunds?

### Agency Hierarchy Commissions
1. **Override Structure**: Should the system support override commissions where agency principals earn a percentage of their agents' commissions?
2. **Hierarchy Levels**: How many levels of agency hierarchy need commission support?
3. **Override Rates**: Are override commission rates program-specific or agency-specific?

### Payment Gateway Flexibility
1. **Multiple Gateways**: Should the system support multiple payment gateways simultaneously?
2. **Gateway Failover**: Is automatic failover between gateways required?
3. **Alternative Payment Methods**: Which specific alternative payment methods should be gateway-supported?

### Reconciliation Tolerances
1. **Matching Thresholds**: What variance amounts are acceptable for automated reconciliation?
2. **Exception Workflows**: Who approves reconciliation exceptions?
3. **Timing Differences**: How many days of timing difference are acceptable between payment and clearance?

## Success Criteria

### Functional Success
- Complete equity-based accounting with balanced transactions
- Zero storage of sensitive payment data
- Automated payment processing through Paysafe tokens
- Program-configurable business rules
- Full commission calculation support

### Operational Success
- Real-time financial reporting
- Automated notice generation
- Minimal manual intervention required
- Self-service configuration capabilities
- Complete audit transparency

### Security Success
- PCI compliance through tokenization
- Secure payment processing
- Protected customer data
- Comprehensive audit trails
- Reduced security attack surface

### Compliance Success
- Meet all regulatory requirements
- Provide examination-ready audit trails
- Support required financial reports
- Maintain data retention standards
- Enable compliance monitoring

## Conclusion

Version 9 provides a comprehensive accounting system that leverages Paysafe's secure payment infrastructure while maintaining the simplicity of transaction and transaction_line as core tables. The removal of batch check processing streamlines operations while single check posting provides necessary functionality for mailed payments.

The integration of Paysafe's tokenization ensures zero storage of sensitive payment data, significantly reducing PCI compliance scope and security risks. Program-configurable grace periods and business rules provide the flexibility needed for multi-state operations while maintaining consistent accounting practices.

This design positions the system for future payment innovations through its flexible gateway architecture while maintaining the rigor required for financial integrity and regulatory compliance.

---

**Document Version**: 9.0  
**Date**: 2025-01-10  
**Status**: FINAL - Paysafe Integration and Enhanced Security  
**Key Additions**: Paysafe tokenization, removed batch processing, program-configurable grace periods, ACH NACHA for positive pay