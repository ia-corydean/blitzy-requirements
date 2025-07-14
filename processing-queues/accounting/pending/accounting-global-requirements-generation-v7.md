# Accounting Global Requirements Generation - Version 7 (Business Requirements)

## Executive Summary

Version 7 presents the accounting requirements as pure business specifications, focusing on WHAT the system must accomplish rather than HOW it will be implemented. The accounting system serves as the financial foundation for the insurance platform, built on the principle of equity-based double-entry bookkeeping with complete audit transparency.

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
- **Full Payment Allocation Only**: No partial payment acceptance
- **Oldest-First Application**: Payments apply to oldest pending installments first
- **Multi-Installment Payments**: Single payment can satisfy multiple installments
- **Overpayment Handling**: Excess amounts redistribute across remaining installments
- **Equity-Based Redistribution**: Overpayments may eliminate final installments

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

#### Cancellation Processing
- Automatic cancellation at 12:01 AM on specified cancellation date
- Generate final accounting entries for cancellation
- Calculate and process any refunds due
- Maintain reinstatement eligibility window

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

### Security and Privacy
- Role-based access to financial data
- Encryption of sensitive financial information
- PCI compliance for payment data
- Audit logging of all financial operations
- Data masking for non-production environments

## Business Rules Summary

### Payment Rules
1. No partial payments accepted
2. Payments apply oldest-first
3. Overpayments redistribute automatically
4. Payment plans locked at binding (except for equity adjustments)
5. All payments must create journal entries

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
1. Automatic at 12:01 AM on cancellation date
2. 30-day reinstatement window
3. Pro-rata or short-rate calculation options
4. Refunds processed automatically
5. Commission adjustments as appropriate

## Success Criteria

### Functional Success
- Complete equity-based accounting with balanced transactions
- Automated payment processing and allocation
- Dynamic installment generation
- Comprehensive fee management
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

These requirements define a comprehensive accounting system that maintains financial integrity while supporting the complex needs of insurance operations. The focus on equity-based accounting, program-centric configuration, and complete audit transparency ensures both operational efficiency and regulatory compliance.

The system design emphasizes configuration over customization, allowing business users to adapt the system to changing needs without technical intervention. By building on the foundation of transaction and transaction_line concepts, the system provides the flexibility needed while maintaining the rigor required for financial operations.

---

**Document Version**: 7.0  
**Date**: 2025-01-07  
**Status**: FINAL - Business Requirements Only  
**Key Focus**: Simplified, implementation-agnostic requirements specification