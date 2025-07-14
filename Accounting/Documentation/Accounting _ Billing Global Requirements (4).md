**Installment Process: A Less-Technical, End-to-End Overview**

---

### **Why Installments Exist**

* **Customer Affordability & Retention**  
   Allow policyholders to spread their premium and fees over time, reducing up-front burden and improving renewal rates.

* **Program Flexibility**  
   Enable different programs to offer unique plans (percent down, custom due-date, number of installments) without writing code.

* **Auditable & Data-Driven**  
   Every schedule, payment, and fee is driven by configuration tables and fully journaled so you can trace exactly how each dollar moved.

---

### **Core Ideas**

#### **1\. Payment Plan Options**

* **Percent-Based Down-Payment**: e.g. 16.67%, 25%, or Paid-in-Full.

* **Date-Driven Down-Payment**: Agent picks a specific due date; system calculates required down-payment based on daily premium.

* **Installment Count & Fee**: Configure number of installments (4, 5, 6, etc.) and per-installment fees (e.g. $4.50) in lookup tables.

#### **2\. Dynamic (“Just-In-Time”) Scheduling**

* Store only **term metadata** (`term_months`, `due_day`) in `map_program_term`.

* **First installment** is generated at bind.

* **Next installments** spawn automatically when each prior one hits “Paid” (or via a light cron that keeps 2-3 future rows).

#### **3\. Itemized Components**

* Each installment breaks down into:

  * Premium slice (daily\_rate × days)

  * Policy fee, MCVPA fee, SR22 fee

  * Installment fee

#### **4\. Partial & Full-Payment Allocation**

* A single payment can span multiple installments.

* System applies to oldest “Pending” installments first, updating each to Partially Paid or Paid.

* Upon full payment of an installment, the next installment is created.

#### **5\. Automated Notices & Fees**

* **Billing Notices**: generate 20 days before due date.

* **Late Fee**: apply a $5 adjustment 5 days past due if unpaid.

* **Cancellation Process**: send notice 11 days after due date; cancel at 12:01am if still unpaid.

* **Reinstatement Window**: allow a new bind within 30 days post-cancellation.

---

### **How an Installment Workflow Flows**

1. **Plan Selection**  
    Agent chooses term (e.g. 6-month), down-payment option (percent or custom date).

2. **Calculate Down-Payment**

   * Compute daily premium: Premium ÷ days in term.

   * If percent: daily\_rate × term\_days × pct.

   * If custom date: daily\_rate × (days\_to\_date \+ cancellation\_grace).

   * Add configured fees (policy, MCVPA, SR22).

3. **Schedule First Installment**

   * Create **`installment#1`** with due\_date \= bind\_date \+ due\_day offset.

   * Log its component breakdown.

4. **On Payment**

   * **recordPayment()** creates a payment record, journals `transaction` \+ `transaction_line`.

   * Allocate across open installments, updating each installment’s `paid_amount` and `status_id`.

   * If an installment becomes “Paid,” trigger **`generateNextInstallment()`**.

5. **Cron Look-Ahead**

   * Nightly job ensures at least 2 future installments exist by comparing count against `term_months`.

6. **Notices & Fees**

   * 20-day billing notice: query installments where `due_date – 20 days = today`.

   * Late fee: apply $5 adjustment when `due_date + 5 days = today` and still unpaid.

   * Cancellation notice: when `due_date + 11 days = today`.

   * Cancel policy at 12:01am if unpaid beyond that date.

7. **Reinstatement**

   * System allows a bind within 30 days of cancellation; treats via standard reinstatement workflow (no new code).

---