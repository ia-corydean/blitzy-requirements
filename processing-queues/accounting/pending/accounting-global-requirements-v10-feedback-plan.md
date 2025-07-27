# Accounting Global Requirements V10 - Feedback Response Plan

## Executive Summary

This document addresses comprehensive feedback from the Program Manager on the Accounting Global Requirements Generation V10 document. The feedback reveals several areas requiring clarification, simplification, and enhancement to better align with business operations and user needs.

### Major Themes Identified
1. **Payment Flexibility**: Need for partial payment support contrary to current "full payment only" requirement
2. **Role-Based Permissions**: Backdating and approval hierarchies need role-based controls
3. **Commission Simplification**: Current agency hierarchy too complex for implementation
4. **Banking Clarifications**: Confusion between Positive Pay reports and NACHA files
5. **Business Rule Specifics**: Many calculations and processes need detailed formulas and examples

## Detailed Feedback Analysis

### 1. Payment Processing Clarifications

#### 1.1 Partial Payment Support
**Current Requirement:** "Full Payment Allocation Only: No partial payment acceptance at transaction level" (Line 108)

**PM Feedback:** 
- Why would we not allow a partial payment on a regular payment?
- What are benefits and drawbacks of accommodating this?
- How much additional complexity would it add to the system?

**Proposed Response:**
- **Benefits of Partial Payments:**
  - Improved customer retention (avoid cancellations)
  - Better cash flow management
  - Flexibility during financial hardship
  - Industry-standard practice
  
- **Drawbacks:**
  - Increased accounting complexity
  - More complex aging reports
  - Complicated cancellation calculations
  - Potential for accumulating shortfalls
  
- **Complexity Assessment:** Moderate (3-4 weeks additional development)
  - Payment allocation logic
  - Aging report modifications
  - Cancellation date calculations
  - Collection tracking

**Recommended Update:** 
```
"Support configurable partial payment acceptance with:
- Minimum payment thresholds by program
- Automatic application to oldest charges first
- Clear shortfall tracking and reporting
- Configurable rules for cancellation prevention"
```

#### 1.2 Backdating Permissions

- should be able to backdate payments in the back office.

**Current Requirement:** "No Backdating: Coverage cannot be backdated to cancellation date" (Line 149)

**PM Feedback:** Back office user with role permissions should be able to back date.

**Proposed Update:**
```
"Coverage Backdating Rules:
- Standard users: No backdating permitted
- Back office users with BACKDATE_COVERAGE permission: May backdate with:
  - Maximum backdate period (configurable by program)
  - Required reason code and documentation
  - Supervisor approval for dates beyond X days
  - Complete audit trail with user, timestamp, and justification"
```

#### 1.3 Payment Gateway Outage Handling
**Current Requirement:** Agent sweep only during complete outages

**PM Confirmation Needed:**
- Is agent sweep the ONLY acceptable payment method during outages?
  - We should be able to batch all forms of payment when down.
    - post the payments that end up successfully going through
    - notify producer if the payment is not authorixed ro succesful. etc..
    - Have rate limiting rules around policies during outages
      - If we lock the policy, ensure to auto unlick policy when the payment is processed either success or deny.
- Should we queue other payment attempts or reject immediately?
- How long should we maintain the queue before manual intervention?
  - As soon as service is restored.

### 2. Reinstatement Calculation Updates

#### 2.1 Daily Premium Rate Formula
**Current:** "Calculate daily premium rate: Total Premium ÷ Total Term Days" (Line 152)

**PM Feedback:** Should be Pure Premium (minus fees) ÷ Total Term Days

**Proposed Update:**
```
"Daily Premium Rate Calculation:
Formula: (Total Premium - All Fees) ÷ Total Term Days
Where:
- Total Premium = Full term premium before any fees
- All Fees = Policy fee + MVCPA + SR22 + all other fees
- Total Term Days = Number of days in policy period"
```

#### 2.2 Unpaid Premium Clarification
**Current:** "Add unpaid premium from before cancellation" (Line 155)

**PM Feedback:** Not sure I understand this item.

**Proposed Clarification:**
```
"Outstanding Balance Collection:
If the policy had unpaid amounts at cancellation:
- Example: Policy cancelled for non-payment with $150 past due
- This $150 must be collected WITH the reinstatement premium
- Prevents reinstatement without clearing prior debt
- Ensures account is brought fully current"
```

#### 2.3 Previous Payments Credit
**Current:** "Subtract any payments previously collected" (Line 157)

**PM Feedback:** Please explain

**Proposed Clarification:**
```
"Payment Credit Application:
Credit payments made during original term to avoid double-charging:
- Example: 6-month policy, customer paid 3 months before cancellation
- Reinstatement calculation credits the 3 months already paid
- Customer only pays for remaining term plus fees
- Prevents duplicate premium collection"
```

#### 2.4 First Reinstatement Payment
**Current:** "First payment deducted from balance and due immediately" (Line 162)

**PM Feedback:** What is the calculation for the amount due?

**Proposed Formula:**
```
"First Reinstatement Payment Calculation:
Amount Due = A + B + C + D
Where:
A = Past due amount from before cancellation
B = Reinstatement fee (program configured)
C = Next regular installment amount
D = Any equity shortage to meet minimum requirements"
- define what the requirements are for calculating equity on a policy.
```

### 3. Endorsement Management Revisions

#### 3.1 Premium Impact Clarification
**Current:** "Premium Impact: Total premium based on accepting mandatory endorsements" (Line 173)

**PM Feedback:** Premium Impact would only be for Double Ded and Unlisted Driver.

**Proposed Update:**
```
"Endorsement Premium Impacts:
- Double Deductible (OACM.DD.021): Provides premium discount
- Unlisted Driver (OACM.ULD.023): Provides premium discount
- All other endorsements: No premium impact (coverage modifications only)"
```

#### 3.2 Physical Damage Endorsement Handling
**Current:** Listed as optional endorsements (Line 178)

**PM Feedback:** These should be on the required signed form just marked NA if not applicable.

**Proposed Update:**
```
"Endorsement Disclosure Requirements:
- ALL endorsements appear on mandatory disclosure form
- Physical damage endorsements marked 'N/A' when coverage not selected
- Customer signature required acknowledging all endorsements
- Form must be complete before binding allowed"
```

#### 3.3 Fee Tracking Expansion
**Current:** "Track endorsement fees separately from premium" (Line 191)
- look more into this on current structure
**PM Feedback:** Should we track all fees separate from premium?

**Proposed Update:**
```
"Comprehensive Fee Tracking:
- Track ALL fees separately from premium
- Maintain individual fee line items for:
  - Policy fees
  - Transaction fees
  - Service fees
  - Compliance fees (SR22, MVCPA)
- Enables accurate commission calculations (premium only)
- Supports detailed financial reporting"
```

#### 3.4 Endorsement with Pending Invoice
**Current:** "Recalculate remaining installments after endorsement" (Line 194)
- dia's feedback.
**PM Feedback:** Do we need to flush this out for down requirements and how to handle if there is a pending invoice for Ends.

**Proposed Detailed Process:**
```
"Endorsement Processing with Pending Invoices:
Scenario 1 - Invoice Due Soon (within X days):
- Hold endorsement until invoice paid
- Or process with effective date after invoice due date

Scenario 2 - Premium Increase:
- Generate supplemental invoice immediately
- Add amount to next regular invoice
- Recalculate all future installments

Scenario 3 - Premium Decrease:
- Apply credit to next invoice
- Recalculate remaining installments
- Option to refund if paid-in-full"
```

### 4. Payment Plan Management Adjustments

#### 4.1 Installment Count Factors
**Current:** "Flexible Installment Counts: Support various installment options (4, 5, 6, 12 payments)" (Line 201)

**PM Feedback:** Do we need to include that this will be based off the down payment and policy term.

**Proposed Update:**
```
"Payment Plan Determination:
Installment count options based on:
- Down payment percentage (minimum thresholds)
- Policy term length (6 vs 12 months)
- Program-specific rules
- State regulations
Example: 25% down on 12-month policy = max 11 installments"
```

#### 4.2 Invoice Generation Rules
**Current:** "Subsequent installments generated just-in-time as previous ones are paid" (Line 206)

**PM Feedback:** 
- Rule 1: Should be 20 days prior to payment unless time between today's date and due date are less than 20 and send immediately
- Rule 2: If return mail flag is applied for bad address suppress future bills until address is updated
  - 20 days should be a program level congifuration
**Proposed Update:**
```
"Invoice Generation Business Rules:
Rule 1 - Timing:
- Generate 20 days before due date (standard)
- If less than 20 days to due date: Generate immediately
- Maintain 2-3 future installments for visibility

Rule 2 - Delivery Suppression:
- Return mail flag = suppress all future paper invoices
- Continue generating in system for tracking
- Resume delivery when address updated
- Electronic delivery continues if opted-in"
```

### 5. Cancellation Management Updates

#### 5.1 Payment Extension Rules
**Current:** "Prevent cancellation if payment extends coverage beyond grace period" (Line 232)

**PM Feedback:** This should only happen if the payment extends coverage to the next due date + the program defined grace period.

**Proposed Update:**
- Explain this further. General rule is we create the cancellation, but extends the timeframe, not prenent cancellation.
  - Should not intervene into the next billing cycle.
```
"Cancellation Prevention Logic:
Payment prevents cancellation ONLY when:
- Payment amount covers premium through next due date
- PLUS program-defined grace period
- Example: Next due 3/15, grace period 11 days
- Payment must cover through 3/26 to prevent cancellation"
```
### 6. Commission Management Simplification

#### 6.1 Commission Basis Clarification
**Current:** "Collected Basis: Commission calculated as payments are collected" (Line 264)

**PM Feedback:** Commissions are paid on premium only not fees.

**Proposed Update:**
```
"Commission Calculation Basis:
- Commissions calculated on PREMIUM ONLY
- Excludes ALL fees:
  - Policy fees
  - Installment fees  
  - Transaction fees
  - Compliance fees
- Clear separation in accounting required"
```

#### 6.2 Agency Hierarchy Simplification
**Current:** Complex individual agent hierarchy (Lines 273-283)

**PM Feedback:** This is a pretty complex process. Do we really want to pay to an individual? Should pay at agency level with override ability.

**Proposed Simplified Structure:**
```
"Simplified Commission Structure:
Primary Level: Agency
- All commissions paid to agency entity
- Agency handles internal distribution

Override Options:
- Pay to Principal (agency owner)
- Pay to Master Agency
- Program-specific override rules

Benefits:
- Simplified reconciliation
- Reduced payment processing
- Clearer audit trails
- Agency autonomy for splits"
```

#### 6.3 Commission Payment Methods
**Current:** "Check printing for commission payments" (Line 289)

**PM Feedback:** Add NACHA File for Commission Payment. Should include daily agent sweep transactions.

**Proposed Update:**
```
"Commission Payment Processing:
1. Monthly Commission Payments:
   - Generate NACHA file for ACH payments
   - Check printing for non-ACH agencies
   
2. Daily Agent Sweep Processing:
   - Create daily NACHA file for:
     - Premium collection debits
     - Commission payment credits
     - NSF reversals
   - Automated FTP transmission to bank
   - Confirmation file processing"
```

#### 6.4 90-Day Clawback Period
**Current:** "No clawbacks after 90 days" (Line 270)

**PM Feedback:** 90 days from what date? Just want to make sure I understand this logic.
- if 60 days and no production send suspense to rep to follow up.
- send invoice
- Look into this more.

**Proposed Clarification:**
```
"Commission Clawback Rules:
- 90-day protection period starts from POLICY EFFECTIVE DATE
- Not from payment date or commission date
- Example: Policy effective 1/1, commission paid 1/15
- Clawback protection starts 4/1 (90 days from 1/1)
- Cancellations after 4/1 = no commission recovery"
```

### 7. Notice Generation Corrections

#### 7.1 Cancellation Notice Process
**Current:** "Cancellation Warnings: Send based on program-configured grace period" (Line 296)

**PM Feedback:** Is this the intent to cancel? There is no late notice and then a cancel.

**Proposed Update:**
```
"Streamlined Cancellation Notice Process:
- NO separate late payment notice
- Single cancellation notice only
- Generated evening of missed payment
- Mailed next business day
- Contains:
  - Amount due to reinstate
  - Cancellation effective date
  - Reinstatement deadline (30 days)
  - Payment methods accepted"
```

### 8. Banking Integration Clarifications

#### 8.1 Positive Pay vs NACHA Files
**Current:** "Generate ACH NACHA files for positive pay verification" (Line 309)
- have this look at the positive pay documentation
**PM Feedback:** Positive pay is just a report pdf file. NACHA is the clearing house file.

**Proposed Correction:**
```
"Banking File Generation:
1. Positive Pay Reports:
   - PDF format for bank
   - Lists all checks issued
   - Used for fraud prevention
   - Daily or weekly generation

2. NACHA Files (separate):
   - ACH payment instructions
   - Electronic payment clearing
   - Includes:
     - Customer payment collections
     - Commission disbursements
     - Daily agent sweeps
   - Transmitted via secure FTP"
```

### 9. Additional Questions and Clarifications

#### 9.1 Reconciliation Approval Hierarchy
**Current:** "Approval Hierarchy: Based on variance amount" (Line 388)

**PM Feedback:** Would like to clarify what this means exactly? Like premium write off?

**Proposed Clarification:**
```
"Reconciliation Variance Approvals:
Covers discrepancies in:
- Payment mismatches (collected vs recorded)
- Premium adjustments/write-offs
- Commission calculation differences
- Fee reconciliation variances

Approval Levels:
- Level 1 ($0-$50): Accounting Clerk
- Level 2 ($50-$500): Supervisor  
- Level 3 ($500+): Controller/Manager"
```

#### 9.2 EFT Information Storage
**Current:** "Zero storage of sensitive payment data" (Line 24)

**PM Feedback:** Maybe a dumb question but where will the EFT info reside?

**Proposed Clarification:**
```
"Payment Data Security Architecture:
What Paysafe Stores:
- Actual account numbers
- Routing numbers
- Card numbers
- Security codes

What We Store:
- Paysafe tokens (meaningless without Paysafe)
- Last 4 digits (display only)
- Payment method type
- Nickname/description

Result: Full PCI compliance with zero sensitive data exposure"
```

### 10. New Requirements from PM Feedback

#### 10.1 NSF/Chargeback Processing
**PM Input:** If NSF or chargeback, user manually reverses payment, recalculates, adds NSF fee, and handles cancellation scenarios.

**New Requirement Section:**
```
"NSF and Chargeback Handling:
Process Flow:
1. Payment reversal notification received
2. User manually reverses payment
3. System recalculates account balance
4. NSF fee automatically applied
5. Cancellation logic:
   - If NSF was for reinstatement: Auto-cancel to original date
   - If NSF for regular payment: Generate new cancellation notice
6. Complete audit trail maintained"
```

#### 10.2 Payment Plan Modifications
**PM Input:** Payment plans should not be changed midterm, can adjust due date with equity requirements.
- Payment plan changes should not change however if you apply additional premium, it can recalculate the installment count which technically changes your payment plan. Thoughts?

**New Requirement Section:**
```
"Payment Plan Change Restrictions:
- No mid-term installment count changes
- Due date changes allowed with:
  - Equity calculation to ensure coverage
  - Additional payment if equity short
  - No refund if equity surplus
- Maintains original payment plan structure"
```

#### 10.3 Commission Statement Requirements
**PM Input:** Commission Statement Sample will be provided

**Action Item:**
```
"Commission Statement Format:
- Awaiting sample from PM
- Will include required data elements
- Format for electronic delivery
- Archive requirements"
```

#### 10.4 Negative Commission Handling
**PM Input:** Detailed process for carrying negative balances

**New Requirement Section:**
```
"Negative Commission Processing:
Monthly Process:
1. Calculate total earned commissions
2. Subtract any chargebacks/adjustments
3. If negative: Carry balance forward
4. Apply against next month's earnings
5. After 90 days no activity:
   - Generate notice to agency
   - Request payment for balance due
   - Establish payment plan if needed"
```

#### 10.5 Refund Processing Rules
**PM Input:** Texas program specifics and timing requirements

**New Requirement Section:**
```
"Refund Processing Requirements:
Texas Programs:
- All cancellations are pro-rated
- Calculate unearned premium precisely
- No minimum refund threshold

Processing Rules:
- Refund method can differ from payment method
- Manager approval authority for all amounts
- 15-day SLA for insured-requested cancellations
- Electronic refunds preferred when possible"
```

## Outstanding Questions for PM

1. **Partial Payments**
   - Should we accept partial down payments or only for installments?
   - Minimum partial payment amounts?
   - How many partial payments before cancellation?

2. **Commission Timing Details**
   - Exact cutoff date for monthly commission runs?
   - How to handle commissions for mid-month producer changes?
   - Override commission approval process?

3. **Return Mail Process**
   - How long after return mail before marking "bad address"?
   - Alternative notification requirements during suppression?
   - Re-activation process for corrected addresses?

4. **Backdating Limits**
   - Maximum number of days for backdating?
   - Which specific events can be backdated?
   - Different limits for different user roles?

5. **Payment Method Changes**
   - New signed form requirements - what specific format?
   - Electronic signature acceptable?
   - Storage and retrieval requirements?

6. **Agent Sweep Specifications**
   - Timing for daily sweep files?
   - Separate files for debits and credits?
   - Confirmation/reconciliation process?

## Implementation Impact Summary

### High Complexity Changes
1. Partial payment support - Affects entire payment pipeline
2. Commission hierarchy simplification - Major refactoring needed
3. NACHA file generation - New integration required

### Medium Complexity Changes
1. Enhanced backdating with permissions - Role system updates
2. Invoice suppression rules - Delivery logic changes
3. NSF automated handling - New workflow processes

### Low Complexity Changes
1. Formula clarifications - Documentation only
2. Fee tracking separation - Database schema adjustment
3. Notice consolidation - Template changes

## Recommended Next Steps

1. **Immediate Actions**
   - Schedule PM review meeting for this plan
   - Prioritize high-impact clarifications
   - Begin drafting V11 with agreed changes

2. **Documentation Needs**
   - Create calculation examples for all formulas
   - Develop process flow diagrams
   - Write user stories for complex scenarios

3. **Technical Planning**
   - Assess database schema impacts
   - Plan API changes for partial payments
   - Design NACHA file interface

4. **Timeline Estimate**
   - V11 draft: 1 week after PM approval
   - Technical design: 2 weeks
   - Implementation: 8-10 weeks for all changes

---

**Document Status:** DRAFT - Pending PM Review
**Created:** 2025-01-16
**Next Review:** [To be scheduled with PM]