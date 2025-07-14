## **Payment Plan & Installment Process: Global Requirements**

All billing & accounting operations for installment plans must integrate seamlessly with our equity-based, data-driven framework. Every calculation and schedule is driven by configuration tables (no code changes), and every money movement is fully auditable via double-entry journals.

---

### **1\. Goals & Key Principles**

* **Equity-Based Scheduling**  
   Every installment—and its payments—produce balanced debit/credit legs so that Assets \= Liabilities \+ Equity always holds.

* **Dynamic Term Configuration**  
   Store only term metadata (`term_months`, `due_day`) in lookup/mapping tables; derive all dates and amounts at runtime or via just-in-time generation.

* **Flexible Down-Payment Calculation**  
   • **Percent-Based**: e.g. 16.67% of net premium.  
   • **Date-Driven**: calculate by multiplying daily premium by days until an arbitrary due date.

* **Itemized Installment Components**  
   Each installment breaks down into premium slice, policy fee, MCVPA fee, installment fee, SR22, etc., configured per program.

* **Partial & Full-Payment Allocation**  
   Payments may span multiple installments; full-payment events trigger generation of the next installment.

* **Real-Time & Batch Processing**  
   • **Real-Time**: `recordPayment()` allocates instantly via the gateway.  
   • **Batch**: import files into `payment_batch` → `processBatchPayments()`.

* **Automated Notices & Fees**  
   • Generate billing notices 20 days before due date.  
   • Post a $5 late fee 5 days past due.  
   • Schedule cancellation notice 11 days after due date; cancel at 12:01 am if unpaid.  
   • Allow reinstatement within 30 days of cancellation.

* **Program-Centric Control**  
   All term, fee, and instrument rules scoped by `program.id` via mapping tables—no code changes.

---

### **2\. Core Processes**

#### **2.1 Payment Plan Setup**

1. Agent selects term (e.g. 6-month) and down-payment option (percent or custom due-date).

2. System reads `term_value`, `due_day`.

3. **Pure Premium** \= Premium ÷ days in term → daily\_rate.

4. **Down-Payment** \=

   * *Percent:* daily\_rate × term\_days × selected\_pct

   * *Date-Driven:* daily\_rate × (days\_to\_due \+ cancellation\_grace)

5. Add fees (policy fee, MCVPA, SR22, etc.) to derive down-payment due at bind.

#### **2.2 Installment Scheduling**

* **First Installment** (bind):

  * Create `installment#1` with due\_date \= inception\_date \+ `due_day_offset` (20 days or custom).

  * Allocate component amounts.

* **Subsequent Installments**:

  * On each installment reaching “Paid,” listener fires `generateNextInstallment()` → create next installment \#N+1 due \+30 days.

  * Cron ensures at least 2 future installments exist.

#### **2.3 Payment Recording & Allocation**

* **recordPayment(PaymentDTO)**:

  
* **processBatchPayments(BatchPaymentDTO)**:

  

#### **2.4 Notices, Late Fees & Cancellation**

* **20-Day Billing Notice**: scheduled job queries installments where `due_date - INTERVAL 20 DAY = CURRENT_DATE` → enqueue notice.

* **Late Fee**: if `CURRENT_DATE = due_date + INTERVAL 5 DAY` and still unpaid → apply a $5 “Late Fee” adjustment and journal it.

* **Cancellation Notice**: if no payment by `due_date + INTERVAL 11 DAY` → generate cancellation notice.

* **Policy Cancel**: at 12:01 am on `due_date + INTERVAL 11 DAY` if still unpaid.

* **Reinstatement**: allow bind of a new policy within 30 days — treat via standard reinstatement workflow.

---

### **3\. Data Model & Tables**

#### **3.1 Term & Program Mapping**

| Table | Key Columns & Purpose |
| ----- | ----- |
| **term\_type** | id, name (e.g. “Duration”), status\_id, audit… |
| **term** | id, term\_type\_id → term\_type(id), term\_value INT, description, status\_id, audit… |

#### **3.5 Transaction & Ledger**

| Table | Key Columns |
| ----- | ----- |
| **transaction** | id, policy\_id, transaction\_type\_id, date, description, status\_id, audit… |
| **transaction\_line** | id, transaction\_id, account\_id, debit\_amount, credit\_amount, reference\_type='installment', reference\_id=installment.id, status\_id, audit… |

---

### **4\. Reporting & Data Point Identification**

| Metric | Source Tables | Calculation Summary |
| ----- | ----- | ----- |
| **Next Payment Amount & Due Date** |
| **Installments Remaining** |
| **Term Remaining Balance** |
| **Current Due Amount** |
| **Overdue Installments & Late Fees** |
| **Cancellation Notices** |
| **Reinstatable Policies** |

---

### **5\. Why This Design?**

* **No Pre-Populated Waste**: Only active and upcoming installments persist.

* **Dynamic Precision**: Term metadata \+ JIT generation keeps schedules accurate.

* **Full Audit Trail**: Each planned component and actual payment is journaled and traceable.

* **Configurable at Runtime**: New term types, fee rules, or payment instruments require only DB/YAML updates, not code changes.

* **Real-Time Visibility & Automation**: Minimal, indexed tables support fast queries for reminders, late fees, and cancellations.

