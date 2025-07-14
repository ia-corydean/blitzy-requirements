This is in response to Aime/workspace/requirements/processing-queues/accounting/pending/accounting-global-requirements-generation-v5.md
- Ensure these items below are accounted for in the requirements above in some capacity.
- generate a -v6 file that includes any updates or provides any questions for me to answer.

- equity based system is manditory
- Payment Plan Options
  - Percent-Based Down-Payment: e.g. 16.67%, 25%, or Paid-in-Full.
- Date-Driven Down-Payment: Agent picks a specific due date; system calculates required down-payment based on daily premium.
- Installment Count & Fee: Configure number of installments (4, 5, 6, etc.) and per-installment fees (e.g. $4.50) in lookup tables.
  - Dynamic (“Just-In-Time”) Scheduling
- First installment is generated at bind.
- Next installments spawn automatically when each prior one hits “Paid” (or via a light cron that keeps 2-3 future rows).
  - Itemized Components
- Each installment breaks down into:
- Premium slice (daily_rate × days)
- Policy fee, MCVPA fee, SR22 fee
- Installment fee
- Full-Payment Allocation. No partial payments allowed
- A single payment can span multiple installments.
- System applies to oldest “Pending” installments first, updating each to Partially Paid or Paid.
- Upon full payment of an installment, the next installment is created.
- Automated Notices & Fees
- Billing Notices: generate 20 days before due date.
- Late Fee: apply a $5 adjustment 5 days past due if unpaid.
- Cancellation Process: send notice 11 days after due date; cancel at 12:01am if still unpaid. Reinstatement Window: allow a new bind within 30 days post-cancellation.
- Endorsements, Renewals, Non Renewals, Cancellations, etc..
  
Key Principles
* Equity-Based Every dollar is a debit and a credit; Assets = Liabilities + Equity always holds.
* Program-Centric Each insurance “program” defines exactly which adjustments, limits, deductibles, proof rules, and commission schedules apply.
* Audit-First Every adjustment, payment, fee, refund, etc. writes a journal entry (header + debit/credit lines) that can be traced back to the originating business event.
* Self-Service Configuration Product teams use an Admin UI to define adjustments, proof conditions, liability limits, payment plans, commission rules, producer mappings and gateway settings—no deployments.
* Modular & Extensible New adjustment types, proof rules, or commission structures are simply new rows in lookup and mapping tables.
* Real-Time Reporting All KPIs are calculated directly from the live tables—no overnight ETL or separate “fact” store.
  Core Business Processes
1. Define Financial Adjustments
    * Set up types (Premium, Discount, Fee, Surcharge, Reinstatement, Endorsement, NSF, Chargeback, Commission).
    * Choose calculation basis (Flat, Percentage, Pro-Rata).
    * Map each to Programs via map_program_financial_adjustment.
2. Enforce Proof Rules
    * Define condition types (e.g. prior-experience, multi-car).
    * Associate them with adjustments (map_financial_adjustment_condition), including required document types.
3. Issue & Apply Adjustments
    * On quote/bind/endorsement, apply the relevant adjustments.
    * System journals a transaction and balanced transaction_line entries for each.
4. Schedule & Collect Installments
    * Automatically create installment records based on term length and due-day.
    * Apply payments to installments (map_installment_transaction), updating status (Pending, Partially Paid, Paid, Overdue).
5. Handle Special Flows
    * Reinstatements: charge a reinstatement fee and schedule new installments.
    * Endorsements: calculate pro-rata premium adjustments.
    * NSF & Chargebacks: charge NSF fees; reverse entries on chargeback.
    * Refunds: generate reversing journal entries.
6. Manage Commissions & Producer Transfers
    * Define commission types (New Business %, Renewal Flat Fee, etc.) and rates.
    * Map rates to producers per program (map_producer_commission).
    * Record actual commissions on policies (map_policy_commission).
    * Transfer a policy’s producer via map_producer_policy, with optional journal note.
7. Agent (Producer) Payment Integration
    * Integrate ACH/credit-card gateway for agent remittances.
    * Journal all gateway interactions and post resulting cash movements.
8. Policy Modifications
    * Effective-Date Changes: compute and journal net premium delta without reversing history.
    * Producer Transfers: update mappings without touching past transactions.