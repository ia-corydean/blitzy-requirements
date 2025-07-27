# Accounting Global Requirements Generation - Version 10 (Enhanced Clarity)

## Executive Summary

Version 10 refines the accounting requirements by incorporating detailed reinstatement and endorsement processes, clarifying payment requirements, and addressing all stakeholder questions. The system maintains its foundation on transaction and transaction_line tables while ensuring full minimum down payment requirements and program-configurable business rules. External system integrations are designed for future readiness rather than immediate implementation, maintaining flexibility for growth.

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
- Small refund thresholds are program-configurable
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
- 7-year historical retention for all financial transactions
- Complete transparency in premium calculations and fee applications
- Real-time financial reporting without batch processing dependencies

### 5. Modular and Extensible
- New fee types, adjustment reasons, and payment methods through configuration
- Flexible API interface for future payment gateway connections
- Extensible proof rules and document requirements
- Support for future payment innovations through gateway abstraction
- Internal system architecture ready for future external integrations

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
- **Agent E-Check (Sweep)**: Agency account sweep payments (batch-capable during outages)
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
- **Clear Rejection Messages**: Inform customer of exact amount required

##### Payment Allocation for Sufficient Payments
When payment equals or exceeds the billed invoice amount:
1. Apply payment to the billed unsatisfied invoice
2. If payment exceeds invoice amount:
   - Apply balance to policy balance
   - Recalculate all future bills based on new balance
   - System may eliminate final installments if overpayment is sufficient

##### Payment Processing Rules
- **Full Payment Allocation Only**: No partial payment acceptance at transaction level
- **Oldest-First Application**: Payments apply to oldest pending installments first
- **Multi-Installment Payments**: Single payment can satisfy multiple installments
- **Overpayment Handling**: Excess amounts redistribute across remaining installments
- **Equity-Based Redistribution**: Overpayments may eliminate final installments
- **Per-Policy Basis**: All premium payments processed independently per policy

##### Payment Gateway Outage Handling
When all payment gateways are unavailable:
- **Agent Sweep Only Mode**: System restricts payment methods to agent sweep exclusively
- **Batch Queue Management**: Agent sweep payments queued for later processing
- **Customer Payment Blocking**: Direct customer payments temporarily disabled
- **Clear Communication**: Customers and agents notified of payment restrictions
- **Automatic Recovery**: Queued payments process automatically when gateway restored
- **Audit Trail**: Complete logging of outage periods and queued transactions

### Check Printing Capabilities

The system must support single check printing for:
- **Refund Checks**: Print checks for customer refunds
- **Commission Checks**: Print checks for producer commission payments
- **Claim Payment Checks**: Print checks for claim settlements
- **Vendor Payment Checks**: Print checks for vendor services

Check printing features include:
- Check number tracking and sequencing
- MICR encoding support
- Signature line management
- Stub information with payment details
- Void and reprint capabilities
- Check register maintenance

### Reinstatement Management

Based on documented reinstatement requirements, the system must support:

#### Reinstatement Eligibility
- **30-Day Window**: Policies canceled for nonpayment may be reinstated within 30 days
- **No Coverage During Lapse**: No coverage and no premium earned during lapse period
- **Payment Triggered**: Reinstatement initiated upon successful payment
- **Real-Time Effective Date**: Payment date and time becomes reinstatement effective date
- **No Backdating**: Coverage cannot be backdated to cancellation date

#### Premium Recalculation Process
1. Calculate daily premium rate: Total Premium ÷ Total Term Days
2. Determine remaining days: Reinstatement Date to Policy Expiration
3. Calculate remaining premium: Daily Premium × Remaining Days
4. Add unpaid premium from before cancellation
5. Add applicable fees (reinstatement fee, installment fees)
6. Subtract any payments previously collected

#### Installment Adjustment Rules
- Divide remaining premium equally among remaining installments
- If reinstatement within 10 days of next due date:
  - First payment deducted from balance and due immediately
  - If only one installment remains, entire balance due upfront
- Generate new payment schedule from reinstatement date

### Endorsement Management

Based on documented program requirements, the system must support:

#### Mandatory Endorsements
- **Required Coverage Modifications**: Endorsements that change standard policy coverage
- **Disclosure Requirements**: Signed disclosure form required before binding
- **Premium Impact**: Total premium based on accepting mandatory endorsements
- **Examples**: OACM.YCA.002c (Newly Acquired Automobile)

#### Optional Endorsements
- **Coverage-Based Inclusion**: Added based on coverage selections
- **Physical Damage Endorsements**: 
  - OACM.PhysDam.001 - included with Comp & Collision
  - OACM.DD.021 - Double Deductible (provides discount)
  - OACM.ULD.023 - Unlisted Driver (provides discount)
- **Business Use Endorsements**: OACM.NoBusiness.020 when no business use

#### Endorsement Fees
- **AP Endorsement Fee**: $15.00 assessed for endorsements at insured request
- **SR-22 Fee**: $25.00 for each driver requiring SR-22
- **Fee Application**: Added to transaction at time of endorsement

#### Endorsement Accounting
- Create balanced journal entries for premium changes
- Track endorsement fees separately from premium
- Maintain audit trail of all endorsements
- Support mid-term premium adjustments
- Recalculate remaining installments after endorsement

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

### Cancellation Management

#### Cancellation Timing Rules
- **Program-Configurable Grace Periods**: Each program defines its own grace period
- Calculate days of coverage based on payment amount
- Determine cancellation effective date considering refund prevention
- Automatic cancellation processing at 12:01 AM on cancellation date

#### Cancellation Date Adjustment
- **Purpose**: Adjust cancellation date by a few days to consume remaining premium
- **Goal**: Prevent small refunds that cost more to process than their value
- **Limits**: Program-configurable maximum days for adjustment
- **Customer Notice**: Notify customers when dates are adjusted for this purpose

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
- Single producer per policy (system design accommodates future splits)

#### Agency Hierarchy and Override Commissions
- **Override Structure**: Agency principals earn a percentage of their agents' commissions
- **Hierarchy Levels**: Support 2-3 levels:
  - Level 1: Individual Agent
  - Level 2: Agency
  - Level 3: Master Agency or Managing General Agent (MGA)
- **Override Rates**: 
  - Program level defines available commission structures
  - Agency agreements specify override percentages
  - Both program-specific and agency-specific rates apply

#### Commission Processing
- Monthly earning schedules for earned basis commissions
- Automatic commission calculation at triggering events
- Support for commission adjustments and corrections
- Producer transfer capability with proper accounting
- Check printing for commission payments

### Automated Workflows

#### Notice Generation
- **Billing Notices**: Generate 20 days before installment due date
- **Late Notices**: Generate after grace period expiration
- **Cancellation Warnings**: Send based on program-configured grace period
- **Reinstatement Offers**: Available for 30 days post-cancellation
- **Endorsement Confirmations**: Send after endorsement processing

#### Automatic Fee Application
- **Late Fees**: Apply $5 fee 5 days after due date if unpaid
- **NSF Fees**: Apply upon payment rejection
- **Reinstatement Fees**: Apply when processing reinstatements
- **Endorsement Fees**: Apply based on endorsement type

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

### Payment Gateway Management

#### Multiple Gateway Support
- **Program-Level Configuration**: Each program can have different gateways
- **Primary and Fallback**: Each program supports main gateway and fallback
- **Gateway Types**: Support for multiple payment processors simultaneously
- **Configuration Storage**: Gateway settings stored at program level

#### Gateway Failover
- **Automatic Failover**: Program-configurable option for automatic switching
- **Manual Override**: Ability to manually switch gateways
- **Failure Tracking**: Monitor gateway performance and failures
- **Alert Mechanisms**: Notify administrators of gateway issues
- **Agent Sweep Priority**: When primary gateway is down and no backup gateway available:
  - Only allow agent sweep payments (batched for later processing)
  - Block direct customer card/ACH payments to prevent failures
  - Queue agent sweep payments for bulk processing when gateway restored
  - Display clear messaging about payment restrictions
  - Maintain system stability during complete outage

#### Alternative Payment Methods
Gateway architecture must support future payment innovations:
- Digital wallets (Apple Pay, Google Pay, PayPal)
- Buy Now Pay Later services
- Cryptocurrency payments
- Payment plan providers
- International payment methods

### Special Business Processes

#### Endorsements
- Pro-rata premium adjustments for coverage changes
- Mid-term addition/removal of vehicles, drivers, or coverages
- Automatic recalculation of remaining installments
- Proper accounting for premium increases or decreases
- Support for mandatory and optional endorsements

#### Reinstatements
- Accept reinstatements within 30-day window
- Calculate reinstatement fees based on program rules
- Generate new payment schedule from reinstatement date
- Maintain complete audit trail of lapse period
- No coverage during lapse period

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
- Payment reversals

#### Adjustment Requirements
- All adjustments must create balanced journal entries
- Require appropriate authorization based on amount
- Include detailed reason codes and documentation
- Maintain complete audit trail
- Support bulk adjustments for system corrections

### Reconciliation Management

#### Reconciliation Tolerances
- **Matching Thresholds**: Acceptable variance for automated matching
  - Example: $0.01 to $1.00 variance allowed
  - Program-configurable thresholds
  - Different thresholds for different transaction types
- **Manual Review**: Transactions outside tolerance require review

#### Exception Workflows
- **Approval Hierarchy**: Based on variance amount
  - Level 1: Accounting clerk ($0-$50)
  - Level 2: Accounting supervisor ($50-$500)
  - Level 3: Controller ($500+)
- **Documentation Requirements**: Explanation required for all exceptions
- **Audit Trail**: Complete history of reconciliation decisions

#### Timing Differences
- **Acceptable Delays**: Days between payment initiation and clearance
  - ACH: 2-5 business days
  - Credit Card: 1-3 business days
  - Checks: 5-10 business days
- **Pending Status**: Maintain pending status during clearance
- **Automatic Matching**: Match when payment clears within window

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
- Overpayment redistribution audit
- Token usage analytics
- Check register reports

#### Audit Reports
- Transaction detail with full journal entries
- Rate calculation transparency reports
- Fee application audit trails
- Commission calculation details
- Payment allocation history
- Adjustment activity reports
- Reconciliation exception reports

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
- Bank reconciliation file imports

### Future-Ready External System Integration
The internal system architecture supports future integration with:
- **General Ledger Systems**: Export capability for financial data
- **Commission Payment Systems**: Automated commission distribution
- **Document Management Systems**: Leverage internal document architecture
- **Communication Systems**: Use internal notification framework
- **Regulatory Reporting Interfaces**: Generate required compliance reports

All integrations designed for "when we are ready" implementation without core system changes.

## Program-Specific Configuration

### Cancellation Rules
All cancellation rules are configured at the program level:
- Grace period duration (configurable per program)
- Cancellation calculation methods
- Refund prevention tolerances
- Small refund thresholds
- Maximum days for date adjustment
- Notice timing requirements

### Commission Configuration
- **Program Level**: Defines available commission rates and structures
- **Producer Level**: Assigns specific rates from program options
- **Override Rates**: Both program and agency-specific
- **Special Rates**: Program can offer special commission rates

### Program Structure
- One state per program
- Rating is per program
- Policies are rated per program
- All business rules cascade from program configuration
- Gateway configuration per program

## Compliance Requirements

### Regulatory Compliance
- Support state-specific fee requirements
- Maintain audit trails for regulatory examinations
- Generate required financial reports
- Support rate filing documentation
- Enable compliance monitoring

### Data Retention
- Permanent retention for bound policy calculations
- 7-year historical retention for financial transactions
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
1. Full minimum down payment required (no exceptions)
2. Payments apply to billed unsatisfied invoices first
3. Overpayments redistribute to policy balance and future bills
4. All payments processed on per-policy basis
5. All payments must create journal entries

### Invoice Rules
1. Bills remain open until fully satisfied
2. No partial payment acceptance for minimum requirements
3. Open invoices trigger cancellation workflows
4. Future bills recalculate based on policy balance changes
5. Invoice aging drives notice generation

### Commission Rules
1. Commission rates from Program Manager
2. No clawbacks after 90 days
3. Monthly earning for earned basis
4. Single producer per policy (future split capability in design)
5. Support for agency hierarchy and overrides
6. No commission advances

### Fee Rules
1. Fees always apply after premium calculation
2. Application order must be maintained
3. Program-specific fee amounts
4. Waiver requires approval
5. All fees must be journalized

### Cancellation Rules
1. Calculate paid-to date to prevent refunds when possible
2. Program-configurable grace periods
3. Automatic at 12:01 AM on cancellation date
4. 30-day reinstatement window
5. Commission adjustments as appropriate
6. Date adjustment for refund prevention

## Additional Questions for Complete Accounting Implementation

### Payment Processing
1. **Payment Reversals/Chargebacks**: How should the system handle payment reversals and chargebacks? What accounting entries are required?
2. **Payment Gateway Outage Preferences**:
   - Should agent sweep be the only allowed payment method during complete outages?
   - What notification messages should customers see during outages?
   - How long should sweep payments be queued before manual intervention?
   - Should there be a maximum queue size for sweep payments?
3. **Payment Plan Modifications**: What rules govern changes to payment plans mid-term? Can installment counts be changed?
4. **Payment Retry Logic**: For failed electronic payments, how many retry attempts and at what intervals?
5. **Payment Method Changes**: Can customers change payment methods mid-term? What restrictions apply?

### Commission Management
1. **Commission Adjustments**: What are the rules for commission adjustments after policy changes (endorsements, cancellations)?
2. **Commission Payment Timing**: When are commissions actually paid out? Monthly? Upon collection?
3. **Commission Statements**: What information must be included on commission statements?
4. **Negative Commissions**: How are commission chargebacks handled for cancellations?

### Refund Processing
1. **Partial Refund Calculations**: How should partial refunds be calculated for mid-term cancellations?
2. **Refund Methods**: Must refunds use the original payment method or can they be issued differently?
3. **Refund Approval**: What approval levels are required for different refund amounts?
4. **Refund Timing**: What are the SLA requirements for processing refunds?

### Audit Requirements
1. **Audit Trail Details**: What specific data points must be captured for payment processing audit trails?
2. **Audit Report Frequency**: How often must audit reports be generated and reviewed?
3. **Audit Data Access**: Who should have access to audit data and reports?
4. **Audit Retention**: Are there specific retention requirements beyond the 7-year standard?

### Reconciliation
1. **Daily Reconciliation**: What specific reconciliation processes must run daily?
2. **Month-End Close**: What are the month-end closing procedures and deadlines?
3. **Variance Investigation**: What documentation is required for reconciliation variances?
4. **System Integration**: How should reconciliation integrate with future GL systems?

## Success Criteria

### Functional Success
- Complete equity-based accounting with balanced transactions
- Zero storage of sensitive payment data
- Automated payment processing through Paysafe tokens
- Program-configurable business rules
- Full commission calculation support with hierarchy
- Comprehensive reinstatement and endorsement processing

### Operational Success
- Real-time financial reporting
- Automated notice generation
- Minimal manual intervention required
- Self-service configuration capabilities
- Complete audit transparency
- Efficient reconciliation processes

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

Version 10 provides a comprehensive accounting system that addresses all stakeholder feedback while maintaining simplicity through the transaction and transaction_line core architecture. The system enforces full minimum down payment requirements while providing flexibility for program-specific configurations.

The incorporation of detailed reinstatement and endorsement processes ensures compliance with business requirements while the future-ready integration architecture allows for growth without core system changes. Enhanced reconciliation and commission hierarchy support provides the sophistication needed for modern insurance operations.

This design maintains the security benefits of Paysafe tokenization while adding clarity around payment processing, refund prevention, and operational workflows. The additional questions will help refine implementation details while maintaining the solid foundation established in this document.

---

**Document Version**: 10.0  
**Date**: 2025-01-10  
**Status**: FINAL - Enhanced with Reinstatement, Endorsements, and Clarifications  
**Key Additions**: Detailed reinstatement process, comprehensive endorsement support, commission hierarchy, reconciliation workflows, expanded clarification questions