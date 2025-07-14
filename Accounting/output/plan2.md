# Updated Accounting Global Requirements Implementation Plan

## Executive Summary
This updated plan incorporates all feedback from the initial plan review and addresses the additional requirements for check printing and ACH processing. The plan now includes specific clarifications and addresses all questions raised in the feedback.

## 1. Feedback Incorporation Summary

### 1.1 Table Structure Updates
- **transaction** instead of journal_entry (for headers)
- **transaction_line** instead of journal_entry_line (for details)  
- **payment_plan** and **payment_plan_type** instead of payment_schedule
- **Check printing process** requirement added
- **Positive Pay exports** for ACH NACHA file format

### 1.2 Clarified Requirements
- **Multi-currency**: Not required initially
- **Financial year**: Both calendar year and configurable treaty term reporting
- **Commission structure**: Program-specific defaults + special producer commissions (percentage-based)
- **Payment gateway**: Paysafe only, no failover required
- **Accounting software integration**: Infrastructure should support future integration
- **Export formats**: ACH NACHA Positive Pay exports required

## 2. Additional Questions for Clarification

### 2.1 Commission Structure Details
- **Commission clawback**: When a policy cancels mid-term, should previously paid commissions be recovered from the producer?
  - No.
- **Multi-level commission splits**: Are there scenarios where commissions need to be split between multiple producers (e.g., referring agent + writing agent)?
  - No.

### 2.2 Month-End/Year-End Close Procedures
**Recommendations:**
- **Month-end close**: 3 business days after month-end for premium reconciliation
- **Year-end close**: 7 business days after year-end for annual reporting
- **Treaty reporting**: Monthly, Quarterly, Yearly for reinsurance treaty settlements
- **Audit lock**: Prevent changes to closed periods without special permissions

### 2.3 Paysafe Outage Mitigation
**Recommendations:**
- **Graceful degradation**: Allow manual payment entry during outages
  - Explain.
- **Queue management**: Store payment requests for processing when service resumes
- **Customer communication**: Automated notifications about temporary payment issues
  - Explain.
- **Reporting**: Track outage impact on payment collection

### 2.4 Check Printing Requirements
- **Check stock management**: Track check numbers, void checks, reconciliation
- **Positive Pay file format**: Daily export of issued checks for bank reconciliation
- **MICR encoding**: Magnetic ink character recognition for bank processing
- **Signature requirements**: Electronic signatures vs. manual signing process
  - Image of manual signature should be stored and used.
- **Check distribution**: Mail handling, delivery confirmation

### 2.5 ACH NACHA Processing
The NACHA file requirements are only for processing Positive Pay with Sunflower.

Based on the ACH NACHA file specifications:
- **Producer commission payments**: ACH CCD (Corporate Credit/Debit) format
- **Premium collections**: ACH PPD (Prearranged Payment and Deposit) format
- **File transmission**: SFTP to Sunflower Bank with specific formatting
- **Return processing**: Handle ACH returns (NSF, account closed, etc.)
- **Settlement timing**: T+1 settlement for ACH transactions

## 3. Updated Global Requirements Structure

### 3.1 Core Accounting Requirements (54-accounting-financial-management.md)
- Chart of accounts with insurance-specific account types
- Double-entry transaction processing (transaction/transaction_line)
- General ledger with real-time balance calculations
- Financial statement generation and trial balance
- Accounting period management with closing procedures
- Premium earning calculations and unearned premium reserves

### 3.2 Transaction Processing Architecture (55-transaction-processing-architecture.md)
- Transaction header/detail structure with audit trails
- Real-time transaction posting with validation
- Batch processing for large volume imports
- Transaction reversal and correction workflows
- Idempotency controls for duplicate prevention
- Performance optimization for high-volume processing

### 3.3 Payment Gateway Integration (56-payment-gateway-integration.md)
- Paysafe integration using universal entity pattern
- Payment method verification and validation
- Authorization, capture, and settlement processes
- Comprehensive error handling and retry logic
- PCI DSS compliance and secure data handling
- Payment reconciliation and reporting

### 3.4 Billing and Invoicing Architecture (57-billing-invoicing-architecture.md)
- Automated billing cycle management
- Invoice generation with configurable templates
- Late fee calculation and penalty processing
- Cancellation and reinstatement workflows
- Multi-channel delivery (email, print, portal)
- Payment application and allocation logic

### 3.5 Premium and Fee Management (58-premium-fee-calculations.md)
- Base premium calculation with rating factors
- Discount and surcharge application rules
- Fee types and calculation methods
- Commission calculation with program-specific rates
- Premium earning patterns and reserves
- Multi-level approval workflows for adjustments

### 3.6 Payment Plan Management (59-payment-plan-installments.md)
- payment_plan and payment_plan_type entities
- Down payment calculation options (percentage/date-based)
- Dynamic installment generation
- Payment allocation algorithms (oldest-first)
- Partial payment handling and grace periods
- Payment plan modification workflows

### 3.7 Check Printing and ACH Processing (60-check-printing-ach-processing.md)
**NEW REQUIREMENT**
- Check printing workflow and stock management
- MICR encoding and bank reconciliation
- Positive Pay file generation (ACH NACHA format)
- Producer commission ACH payments (CCD format)
- Premium collection ACH processing (PPD format)
- ACH return processing and exception handling

### 3.8 Financial Reporting Analytics (61-financial-reporting-analytics.md)
- Real-time premium analytics (written/earned/collected)
- Receivables aging and collection reporting
- Commission reporting and producer statements
- Financial KPI dashboards and metrics
- Regulatory reporting formats
- Treaty reporting for reinsurance settlements

### 3.9 Compliance and Audit (62-accounting-compliance-audit.md)
- Complete audit trail with 7-year retention
- PCI DSS compliance for payment data
- Role-based access controls and permissions
- Financial data encryption and security
- Regulatory reporting compliance
- Data privacy and protection controls

## 4. Updated Database Schema Design

### 4.1 Core Accounting Tables
- `account` - Chart of accounts with insurance classifications
- `transaction` - Transaction headers (renamed from journal_entry)
- `transaction_line` - Transaction details (renamed from journal_entry_line)
- `invoice` - Invoice headers with billing information
- `invoice_line` - Invoice line items and details
- `payment_plan` - Payment plan definitions (renamed from payment_schedule)
- `payment_plan_type` - Payment plan classifications
- `payment_allocation` - Payment application tracking
  - Can this be combined with transaction and transaction_line with a transaction_type of Payment?
  - go into more detail on the purpose of this table.

### 4.2 Check Processing Tables
- `check_stock` - Check inventory management
- `check_register` - Issued check tracking
- `positive_pay_export` - Daily check export tracking
  - Explain.
- `ach_file` - ACH file transmission tracking
  - Explain.
- `ach_transaction` - Individual ACH transaction details
  - Explain.
  - Can this be consolidated with transaction?

### 4.3 Commission Management Tables
- `commission_rate` - Program and producer-specific rates
  - change to commission and commission_type and commission_schedule
- `commission_transaction` - Commission calculations and payments
  - Explain.
  - Can this be consolidated with transaction?
- `producer_commission_schedule` - Payment schedules for producers
  - see above suggestion
  - should this be a map_ table?

## 5. Integration Architecture

### 5.1 Universal Entity Patterns
- **PAYSAFE_GATEWAY**: Payment processing entity type
- **SUNFLOWER_BANK**: ACH processing entity type
  - Only for processing Positive Pay for now.
- **CHECK_PRINTING_SERVICE**: Check fulfillment entity type

### 5.2 Service Layer Architecture
- `AccountingService` - Core accounting operations
- `BillingService` - Billing and invoicing
- `PaymentPlanService` - Payment plan management
- `CheckPrintingService` - Check processing workflows
- `ACHProcessingService` - ACH file generation and processing
- `CommissionService` - Commission calculations and payments
- `FinancialReportingService` - Report generation

### 5.3 Event-Driven Processing
- Payment processing events for real-time updates
- Commission calculation triggers on policy changes
- Automated billing cycle events
- Check printing workflow automation
- ACH file generation and transmission scheduling

## 6. Security and Compliance

### 6.1 PCI DSS Compliance
- Secure payment data handling and encryption
- Access controls and audit logging
- Network security and data transmission
- Regular security assessments and updates

### 6.2 Financial Data Protection
- Encryption at rest and in transit
- Role-based access controls
- Complete audit trails with timestamps
- Data retention policies (7-year minimum)

## 7. Performance and Scalability

### 7.1 High-Volume Processing
- Batch processing for large transaction volumes
- Real-time processing for individual transactions
- Optimized database indexing and query performance
- Caching strategies for frequently accessed data

### 7.2 Monitoring and Alerting
- Transaction processing monitoring
- Payment gateway performance tracking
- Financial reconciliation alerts
- System health and availability monitoring

## 8. Implementation Deliverables

Upon approval, I will create:

1. **Nine Global Requirement Files** (54-62) covering all accounting aspects
2. **Updated Entity Catalog** with accounting entities and check/ACH processing
3. **Architectural Decision Records** for accounting decisions
4. **Database Migration Scripts** (conceptual) for all accounting tables
5. **Service Interface Definitions** for all accounting services
6. **Integration Specifications** for Paysafe, check printing, and ACH processing
7. **Security and Compliance Documentation** for PCI DSS and financial regulations

This comprehensive approach ensures the accounting system will handle all insurance financial operations including premium processing, commission payments, check printing, ACH processing, and complete regulatory compliance.