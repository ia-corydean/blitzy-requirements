# Final Accounting Global Requirements Implementation Plan

## Executive Summary
This final plan incorporates all feedback from plan2.md and provides a streamlined approach that maximizes table consolidation while maintaining audit trails and performance. The plan addresses all clarifications and includes comprehensive database design following established architectural patterns.

## 1. Consolidated Feedback Implementation

### 1.1 Commission Structure - FINAL
- **Commission clawback**: **No** - Commissions are not recovered on mid-term cancellations
- **Multi-level commission splits**: **No** - Single producer per policy for commission payments

### 1.2 Updated Timeline Requirements - FINAL
- **Month-end close**: **3 business days** after month-end for premium reconciliation
- **Year-end close**: **7 business days** after year-end for annual reporting
- **Treaty reporting**: **Monthly, Quarterly, Yearly** for reinsurance treaty settlements
- **Audit lock**: Prevent changes to closed periods without special permissions

### 1.3 Check Processing - FINAL
- **Signature requirements**: **Manual signature images** should be stored and used for check printing
- **NACHA scope**: **Only for Positive Pay** processing with Sunflower Bank

### 1.4 Database Consolidation Strategy
Following the principle of using `transaction` and `transaction_line` tables with `transaction_type` for maximum consolidation while maintaining performance and audit capabilities.

## 2. Explained Requirements

### 2.1 Paysafe Outage Mitigation Explanations

#### Graceful Degradation - Manual Payment Entry
When Paysafe is unavailable:
- **Manual payment entry interface**: Staff can record payment details (amount, method, reference number, date)
  - Our current interfaces should be disable while an outage happens.
- **Validation rules**: Basic validation without real-time gateway verification
- **Temporary status**: Payments marked as "MANUAL_PENDING" until gateway verification
- **Batch processing**: When Paysafe resumes, manual payments are validated and processed in batch
- **Reconciliation**: Manual payments reconciled against bank deposits and gateway confirmations

#### Customer Communication - Automated Notifications
- **Outage detection**: Automated monitoring triggers notification system
  - This should be configurable on the program whether the auto notices should go out.
- **Multi-channel alerts**: Email, SMS, and portal notifications to affected customers
- **Status updates**: Real-time updates on portal about payment processing availability
- **Alternative instructions**: Guidance on alternative payment methods (phone, mail)
- **Resolution notifications**: Automated alerts when services are restored

### 2.2 Check Processing Table Explanations
* ACH and CC are all processed via paysafe.
* Currently only Positive Pay is processed via Sunflower.
* Future Agent Sweeps should be net in a daily ACH file created by the system and auto sent to the secure site to the Bank.

#### positive_pay_export Table
**Purpose**: Tracks daily exports of issued checks to Sunflower Bank for fraud prevention
- **Export tracking**: File name, generation date, number of checks, total amount
- **Bank reconciliation**: Verification that exported checks match bank records
- **Exception handling**: Track checks that don't clear or are flagged by the bank
- **Audit trail**: Complete history of all Positive Pay file transmissions

#### ach_file Table
**Purpose**: Tracks ACH file transmissions to Sunflower Bank for Positive Pay processing only
- **File metadata**: File name, creation date, transmission status, record count
- **Transmission tracking**: SFTP upload confirmation, bank acknowledgment
- **Error handling**: Track failed transmissions, retries, and resolution
- **Compliance**: Maintain required records for ACH processing regulations

#### ach_transaction Table
**Purpose**: Individual ACH transaction details within each file
- **Transaction details**: Amount, account information, transaction code, addenda
- **Status tracking**: Pending, transmitted, settled, returned, failed
- **Return processing**: NSF, account closed, invalid account handling
- **Reconciliation**: Match ACH settlements with bank confirmations

**Consolidation Analysis**: This table should remain separate from the main `transaction` table because:
- ACH processing has specific data elements (SEC codes, addenda records)
- Different lifecycle from accounting transactions
- Regulatory reporting requirements specific to ACH
- Performance optimization for ACH file generation

## 3. Optimized Database Schema Design

### 3.1 Core Accounting Tables (Consolidated Approach)

#### transaction Table
**Purpose**: Universal transaction header for ALL financial activities
- **Fields**: id, transaction_type_id, source_type, source_id, reference_number, amount, effective_date, status_id
- **Transaction Types**: PREMIUM, PAYMENT, COMMISSION, FEE, ADJUSTMENT, REFUND, CHARGEBACK
- **Consolidates**: Previously separate payment_allocation, commission_transaction tables

#### transaction_line Table  
**Purpose**: Detailed accounting entries for double-entry bookkeeping
- **Fields**: transaction_id, account_id, debit_amount, credit_amount, description
- **Usage**: Every transaction has corresponding debit/credit entries
- **Audit**: Complete trail of all financial movements

#### payment_allocation Table - EXPLAINED
**Purpose**: Tracks how payments are applied across multiple invoices/policies
- **Why needed**: A single payment may cover multiple invoices, partial payments, prepayments
- **Fields**: payment_transaction_id, invoice_id, allocated_amount, allocation_date
- **Example**: $500 payment covers $300 from Invoice A + $200 from Invoice B
- **Cannot consolidate**: Different business purpose than general transactions

#### commission, commission_type, commission_schedule Tables
**Updated Structure** (instead of commission_rate):
- **commission**: Individual commission calculations and payments
- **commission_type**: PERCENTAGE, FLAT_FEE, TIERED (future expansion)
- **commission_schedule**: When commissions are paid (IMMEDIATE, MONTHLY, QUARTERLY)

#### map_producer_commission Table
**Purpose**: Associates producers with specific commission rates per program
- **Fields**: producer_id, program_id, commission_id, effective_date, expiration_date
- **Following established pattern**: Uses map_ prefix for relationships

### 3.2 Check Processing Tables

#### check_stock Table
- **Purpose**: Inventory management for physical check stock
- **Fields**: stock_id, starting_check_number, ending_check_number, current_check_number, status_id

#### check_register Table  
- **Purpose**: Record of all issued checks
- **Fields**: check_number, transaction_id, payee_name, amount, issue_date, status_id, signature_image_path

#### signature Table
- **Purpose**: Store manual signature images for check printing
- **Fields**: id, user_id, signature_image_path, image_format, created_date, is_active

### 3.3 Positive Pay Processing Tables

#### positive_pay_export Table
- **Purpose**: Daily export files sent to Sunflower Bank
- **Fields**: export_date, file_name, file_path, check_count, total_amount, transmission_status

#### ach_file Table (Positive Pay Only)
- **Purpose**: ACH file transmission tracking for Positive Pay
- **Fields**: file_name, creation_date, transmission_date, record_count, file_size, status_id

#### ach_transaction Table (Positive Pay Only)
- **Purpose**: Individual Positive Pay transactions
- **Fields**: ach_file_id, check_number, amount, account_number, transaction_code, status_id

## 4. Updated Global Requirements Structure

### 4.1 Core Accounting Requirements (54-accounting-financial-management.md)
- Chart of accounts with insurance-specific classifications
- Universal transaction processing (transaction/transaction_line)
- Double-entry bookkeeping with real-time balance calculations
- Accounting period management with 3/7 business day close timelines
- Premium earning calculations and unearned premium reserves

### 4.2 Transaction Processing Architecture (55-transaction-processing-architecture.md)
- Consolidated transaction table with transaction_type classifications
- Real-time and batch processing capabilities
- Transaction reversal and correction workflows
- Payment allocation across multiple invoices/policies
- Performance optimization for high-volume processing

### 4.3 Payment Gateway Integration (56-payment-gateway-integration.md)
- Paysafe integration with graceful degradation capabilities
- Manual payment entry during outages
- Automated customer communications during service disruptions
- PCI DSS compliance and secure data handling
- Payment reconciliation and exception handling

### 4.4 Billing and Invoicing Architecture (57-billing-invoicing-architecture.md)
- Automated billing with 3-day month-end close requirement
- Invoice generation with configurable templates
- Late fee calculation and penalty processing
- Multi-channel delivery (email, print, portal)
- Payment allocation logic for complex scenarios

### 4.5 Premium and Fee Management (58-premium-fee-calculations.md)
- Premium calculation with rating factors
- Program-specific commission rates (no clawbacks)
- Fee types and calculation methods
- Multi-level approval workflows for adjustments
- Monthly/quarterly/yearly treaty reporting

### 4.6 Payment Plan Management (59-payment-plan-installments.md)
- payment_plan and payment_plan_type entities
- Down payment calculations (percentage/date-based)
- Dynamic installment generation
- Payment allocation algorithms
- Grace period management

### 4.7 Check Printing and Positive Pay (60-check-printing-positive-pay.md)
**UPDATED SCOPE**
- Check printing with manual signature image storage
- Check stock management and MICR encoding
- Positive Pay file generation for Sunflower Bank (NACHA format)
- Daily export scheduling and bank reconciliation
- ACH processing **ONLY for Positive Pay** functionality

### 4.8 Financial Reporting Analytics (61-financial-reporting-analytics.md)
- Real-time premium analytics (written/earned/collected)
- Receivables aging and collection reporting
- Commission reporting with monthly/quarterly schedules
- Monthly/quarterly/yearly treaty reporting
- Financial KPI dashboards and regulatory compliance

### 4.9 Compliance and Audit (62-accounting-compliance-audit.md)
- Complete audit trail with 7-year retention
- PCI DSS compliance for payment processing
- Role-based access controls
- Financial data encryption and security
- Regulatory reporting compliance

## 5. Additional Questions for Final Clarification

### 5.1 Manual Payment Entry Process
- **Field requirements**: What specific fields should be captured for manual payments (amount, method, reference, customer info)?
- **Approval workflow**: Should manual payments require supervisory approval before posting?
- **Reconciliation process**: How should manual payments be matched with bank deposits?

### 5.2 Signature Management Details
- **Image formats**: What formats should be supported (PNG, JPG, PDF)?
- **Image specifications**: Resolution, file size limits, color vs. black & white?
- **Signature updates**: How often can signatures be updated, and what approval is needed?
- **Verification**: Should there be signature comparison/validation capabilities?

### 5.3 Positive Pay File Specifications
- **Data elements**: What specific fields are required in the Positive Pay export?
- **File format**: Fixed-width, CSV, or XML format preference?
- **Transmission schedule**: Daily, business days only, or other frequency?
- **Exception handling**: Process for bank rejections or discrepancies?

### 5.4 Commission Payment Schedule
- **Payment frequency**: Are producer commissions paid monthly, quarterly, or on policy effective dates?
- **Payment method**: ACH, check, or both options available?
- **Commission statements**: Detailed statements with commission calculations required?

## 6. Implementation Deliverables

Upon final approval, I will create:

1. **Nine Global Requirement Files** (54-62) with consolidated database design
2. **Updated Entity Catalog** with all accounting entities and optimized relationships
3. **Architectural Decision Records** documenting consolidation decisions
4. **Complete Database Schema** with optimized table structure
5. **Service Interface Definitions** for all accounting services
6. **Integration Specifications** for Paysafe, check printing, and Positive Pay
7. **Security and Compliance Documentation** for PCI DSS and financial regulations

This final approach provides maximum consolidation while maintaining performance, audit capabilities, and regulatory compliance requirements.