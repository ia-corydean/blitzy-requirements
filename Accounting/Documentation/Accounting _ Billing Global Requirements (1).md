### Introduction

Our billing and accounting platform must support the full lifecycle of insurance transactions—premiums, discounts, fees, surcharges, payments, installments, reinstatements, endorsements, commissions, NSF/chargebacks, refunds and producer transfers—in a way that is entirely data-driven, equity-based, and auditable. All business rules live in configuration tables (no code changes), and every money movement is recorded in a balanced, double-entry ledger.

### Key Principles

* Equity-Based  
   Every dollar is a debit and a credit; Assets \= Liabilities \+ Equity always holds.

* Program-Centric  
   Each insurance “program” defines exactly which adjustments, limits, deductibles, proof rules, and commission schedules apply.

* Audit-First  
   Every adjustment, payment, fee, refund, etc. writes a journal entry (header \+ debit/credit lines) that can be traced back to the originating business event.

* Self-Service Configuration  
   Product teams use an Admin UI to define adjustments, proof conditions, liability limits, payment plans, commission rules, producer mappings and gateway settings—no deployments.

* Modular & Extensible  
   New adjustment types, proof rules, or commission structures are simply new rows in lookup and mapping tables.

* Real-Time Reporting  
   All KPIs are calculated directly from the live tables—no overnight ETL or separate “fact” store.

### Core Business Processes

1. Define Financial Adjustments

   * Set up types (Premium, Discount, Fee, Surcharge, Reinstatement, Endorsement, NSF, Chargeback, Commission).

   * Choose calculation basis (Flat, Percentage, Pro-Rata).

   * Map each to Programs

2. Enforce Proof Rules

   * Define condition types (e.g. prior-experience, multi-car).

   * Associate them with adjustments, including required document types.

3. Issue & Apply Adjustments

   * On quote/bind/endorsement, apply the relevant adjustments.

   * System journals a transaction and balanced transaction line entries for each.

4. Schedule & Collect Installments

   * Automatically create installment records based on term length and due-day.

   * Apply payments to installments, updating status (Pending, Partially Paid, Paid, Overdue).

5. Handle Special Flows

   * Reinstatements: charge a reinstatement fee and schedule new installments.

   * Endorsements: calculate pro-rata premium adjustments.

   * NSF & Chargebacks: charge NSF fees; reverse entries on chargeback.

   * Refunds: generate reversing journal entries.

6. Manage Commissions & Producer Transfers

   * Define commission types (New Business %, Renewal Flat Fee, etc.) and rates.

   * Map rates to producers per program.

   * Record actual commissions on policies.

   * Transfer a policy’s producer, with optional journal note.

7. Agent (Producer) Payment Integration  
   * Integrate ACH/credit-card gateway for agent remittances.

   * Journal all gateway interactions and post resulting cash movements.

8. Policy Modifications

   * Effective-Date Changes: compute and journal net premium delta without reversing history.

   * Producer Transfers: update mappings without touching past transactions.

*All tables include:*

* Primary Key (id)

* Foreign Keys to related entities

* status\_id for Active/Deprecated/Retired

* Audit Fields (created\_by, created\_at, updated\_by, updated\_at)

* Description where needed

### Reporting & Data Point Identification

All of the following KPIs are calculated by querying and aggregating live tables—no separate ETL layer:

* Written Premium: sum of applied Premium adjustments for a period.

* Earned Premium: pro-rata allocation of written premium over coverage dates.

* Collected Premium: sum of payments applied to premium receivables.

* Outstanding Receivables: receivables balance \= premiums \+ fees \+ surcharges – payments.

* Next Payment Amount & Due Date: upcoming installment’s amount – paid\_amount and due\_date.

* Installments Remaining: count of installments not fully paid.

* Total Term Remaining Balance: net balance across all future installments.

* Late Fees Assessed: sum of NSF/Late Fee adjustments for overdue installments.

* Reinstatement Charges: total of Reinstatement adjustments applied.

* Commission Payable: sum of commission amount per producer.

* Producer Transfers: count and details of changes.

* Refunds Issued: sum of Refund transactions reversing revenue.