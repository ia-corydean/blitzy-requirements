## Installment Process: Detailed Global Requirements

### Introduction & Scope

The installment subsystem extends our equity-based accounting framework to manage payment schedules for policies. It must support dynamic scheduling, partial/full payments, just-in-time installment creation, and full double-entry audit trails—all driven by configuration tables or YAML, never code.

### Goals & Key Principles

* Equity-Based Installments  
   Every installment’s planned amount and actual payments produce matching debit/credit legs so that Assets \= Liabilities \+ Equity holds continuously.

* Just-In-Time Scheduling  
   Persist only term metadata (term\_months, due\_day). Generate the first installment on bind; generate subsequent installments only when prior ones are paid (with a light cron for N-lookahead).

* Partial &Full-Payment Support  
   Allow a single payment to allocate across multiple installments; detect when one is fully paid to trigger the next installment.

* Real-Time & Batch Processing

  * *Real-Time* via recordPayment()

  * *Batch* via imports → processBatchPayments()

* Itemized Components  
   Record planned breakdown (premium slice, fees, discounts); actual postings journal through transaction\_line with reference\_type \= 'installment'.

* Program-Centric Control  
   Each program.id drives term definitions, allowed adjustments, and instruments via mapping tables.

* Audit-First Invocation  
   Every action writes a transaction header and balanced transaction\_line legs, linked to the relevant installment and payment records.

* Typed, Method-Based APIs  
   Business logic calls DTO getters (e.g. getNextInstallmentDate()), never raw arrays.

* Permission-First  
   All installment features gated by component keys enforced via roles & gates.

### Architectural Overview

#### 3.2 Core Orchestrator

1. Initialize Context  
    Load program\_id, policy\_id, term metadata, and payment instrument config.

2. Scheduling Triggers

   * On Bind → scheduleFirstInstallment()

   * On Full-Payment → generateNextInstallment() listener

   * Cron Look-Ahead → ensure ≥ N future installments

3. Payment Events

   * Real-Time

   * Batch:

4. Audit & Persistence

### 4\. Data Model & Tables

*All tables use singular names, map\_ prefixes for join tables, \_type suffixes for lookup tables, status\_id, and audit fields (created\_by, created\_at, updated\_by, updated\_at).*

### 5\. Scheduling & Generation Workflow

#### 5.1 First Installment

* Read for term\_value and due\_day.

* Compute net balance \= (Total Premium \+ Fees – Down Payment).

* Divide by term\_value → per-installment amount.

* Insert installment \#1 with due\_date \= inception\_date \+ due\_day.

* Populate to capture component breakdown.

#### 5.2 Next Installment

* On Full Payment: Listener detects installment is paid generateNextInstallment()

* Cron Look-Ahead: Ensure at least 2 future installments exist by comparing COUNT(\*) \< term\_value.

### 6\. Payment & Allocation Workflow

#### 6.1 Real-Time Payment

* recordPayment(PaymentDTO) → create transaction \+ transaction\_line.

* Create payment record.

* Call allocation routine:

#### 6.2 Batch Payment

* Load file.

* processBatchPayments() parses each record → create payment, transaction, then allocate as above.

#### 6.3 Partial Payments

* Same allocation logic; any unallocated remainder stays in AR until next allocation.

### 7\. Reporting & Data Point Identification

| Metric | Source Tables | Calculation |
| :---- | ----- | ----- |
| Next Payment Amount & Date
| Installments Remaining
| Term Remaining Balance
| Current Due Amount
| Future Scheduled Count
| Overdue Installments
| Component Breakdown (Planned)
| Component Breakdown (Actual)

### Why This Design?

* Minimal Storage: Only live installments are stored—no pre-population.

* Dynamic Precision: Term metadata \+ JIT generation means accurate “remaining” counts.

* Complete Auditability: Each scheduling and payment event journals entries and mappings for full trace.

* Configurable & Scalable: New term types, adjustments, or instruments require only new lookup/mapping rows—no code.

* Performance: Simple queries over a small number of tables deliver real-time dashboards and proactive reminders.