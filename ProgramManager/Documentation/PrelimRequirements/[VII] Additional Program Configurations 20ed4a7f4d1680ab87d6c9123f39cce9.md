# [VII] Additional Program Configurations

## **1 — Policy Configurations**

### **1.1 —**  Agent Commissions

> Pulled from `Agent Default Commissions` in Data Maintenance
> 

Defines how agent commissions are calculated and what percentage options are made available for both New Business and Renewals. Commissions may vary by program and policy term.

**1.1.1 — Commission Calculation Basis**

Specifies **when** commissions are earned and paid to the agent.

| **Calculation Basis** | **Description
`(editable)`** | **Default (Yes/No)
`(editable), only one can be one at once.`** |
| --- | --- | --- |
| **Collected** | Commissions are paid only on premium actually collected from the insured. | Yes |
| **Earned** | Commissions accrue over time in proportion to earned premium. | No |
| **Written** | Commissions are paid upfront when the policy is written, regardless of whether premium is collected. | No |

**1.1.2 — New Business Commissions**

Defines available commission percentage options when a new policy is issued. One default value is displayed first in the agent inquiry commission % dropdown.

| **Label 
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Default
`(editable)`**
 | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- |
| 15% | **`Select from program term options`** | No | On |
| 17% | **`Select from program term options`** | Yes | On |
| 20% | **`Select from program term options`** | No | On |
| `Add commission option` |  |  |  |

**1.1.3 — Renewal Commissions**

Defines commission options when an existing policy is renewed. Often lower than new business rates.

| **Label 
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Default
`(editable)`**
 | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- |
| 10% | **`Select from program term options`** | No | On |
| 12% | **`Select from program term options`** | Yes | On |
| `Add renewal option` |  |  |  |

**1.1.3 — Additional Notes**

- **Defaults** only affect which value appears first in the agent-facing interface; all supported options remain selectable.
- Values are **term-specific**, allowing you to limit certain commission levels to only 6- or 12-month policies.
- Changing the commission basis (Collected, Earned, Written) affects **when** agents are paid but not the % shown.

### **1.2:** Underwriting Questions

> This has been added `net new` to give the team control over underwriting questions in rate, quote, bind.
> 

Underwriting questions are used to identify risk scenarios not captured through standard rating variables. These questions appear during the rate, quote, or bind process. They are not used to calculate premium, but responses may trigger a hard stop, preventing the user from moving forward.

**1.2.1 — Configuration Table**

| **Question
`(editable)`** | **Supported (On/Off)
`(editable)`** | **Is this a hard stop? (Yes/No)
`(editable)`** |
| --- | --- | --- |
| Are there any residents of the household age 15 years or older who are not listed as drivers or as excluded drivers? | On | No |
| Does anyone else not listed on the policy have access to your vehicle? | On | No |
| Has any listed driver had more than one alcohol-related conviction? | On | No |
| Are there any accidents within the last 36 months for any listed driver that are not listed on this application? | On | No |
| Are there any violations within the last 36 months for any listed driver that are not listed in this application? | On | No |
| Are any vehicles on the application NOT registered (titled) to the applicant? | On | No |
| Is any vehicle used for business? | On | No |
| Is any listed vehicle used to carry equipment, materials, or supplies for work? | On | No |
| Is any vehicle used to carry passengers in the course of employment? | On | No |
| Does any listed vehicle make more than five stops per day at different locations in the course of employment? | On | No |
| Is any listed vehicle used to carry passengers for a fee through a Transportation Network Company (e.g., Uber, Lyft)? | On | Yes |
| Is any vehicle modified with special equipment? | On | No |
| Do any drivers have a physical impairment or medical condition that might affect driving ability? | On | No |
| Have you ever been convicted of insurance fraud or denied coverage? | On | No |
| `Add/delete underwriting question` |  |  |

**1.2.2 — Behavioral Logic**

- If **Supported = On**, the question is presented in the rate, quote, or bind flow.
- If **Hard Stop = Yes**, the system will **block quote/bind** and present a customizable rejection message.
- If **Hard Stop = No**, the question is used only for internal flagging or downstream underwriting.

### **1.3: Pre-Bind, Mandatory Endorsements**

This section defines which endorsements must be **signed by all insureds before bind**, during new business. These endorsements are tied to **OACM documents** and are triggered based on the specific coverage or configuration selected. The documents will be managed in `form maintenance.`

| **Label
`(non-editable)`** | **Description
`(non-editable)`** | **Conditions
`(non-editable)`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- |
| `OACM.PhysDam.001` | Physical Damage Ends | Required only if Comp/Coll is selected | On |
| `OACM.YCS.002c` | Your Covered Auto End |  | On |
| `OACM.Storage.004` | Storage |  | On |
| `OACM.DelFee.005` | Delivery for Fee |  | On |
| `OACM.ContLiab.006` | Contractual Liability - Rental |  | On |
| `OACM.AutoTerm.007` | Auto Termination |  | On |
| `OACM.CrimeIntent.008` | Intentional Criminal Acts |  | On |
| `OACM.MisrepFraud.009` | Misrepresentation |  | On |
| `OACM.OutOfState.016a` | Out of State |  | On |
| `OACM.Punitive.018` | Exemplary Damages |  | On |
| `OACM.RentProp-NOAuto.019a` | Rental |  | On |
| `OACM.NoBusiness.020` | Business Use |  | On |
| `OACM.DD.021` | Double Deductible |  | On |
| `OACM.ULD.023` | Unlisted Driver |  | On |
| `OACM.551a` | Mexico Coverage |  | On |

### **1.4: Post-Bind,** Endorsement Configuration

> Pulled from `Endorsement Configuration` in Data Maintenance
> 

This section defines which endorsements can be requested after bind. Each endorsement includes the following flags:

- **Underwriting Supported (On/Off):** Whether the endorsement is available for the Underwriting Team to process within Claims & Policy Management.
- **Producer Supported (On/Off):** Whether the endorsement is available for Producers to process within the Producer Portal.
- **Signature Required (Yes/No):** Whether the endorsement requires a signature from the insured to proceed.

| **Endorsement
`(non-editable)`** | **Producer Supported
`(editable)`** | **Underwriting Supported
`(editable)`** | **Signature Required by Insured
`(editable)`** | **System Automated 
`(non-editable)`** |
| --- | --- | --- | --- | --- |
| Name Correction on Named Insured | Off | On | Yes | No |
| Name Correction on Driver | On | On | Yes | No |
| Revise Policy Effective Date | Off | On | Yes | No |
| Address Change | On | On | Yes | No |
| Email & Phone No Change | On | On | Yes | No |
| Add/Remove HO Discount | On | On | Yes | No |
| Add/Remove Proof of Prior/Transfer | Off | On | Yes | No |
| Add/Remove Multi-Car | Off | On | Yes | Yes |
| Add/Remove EFT Discount | Off | On | Yes | No |
| Add/Remove Paid in Full | Off | On | Yes | Yes |
| Add/Remove Paperless | On | On | Yes | No |
| Add/Remove Early Shopper Discount | Off | On | Yes | Yes |
| Add/Remove Double Deductible Endorsement | Off | On | Yes | No |
| Add/Remove Unlisted Driver Endorsement | Off | On | Yes | No |
| Add Driver | On | On | Yes | No |
| Exclude Driver | On | On | Yes | No |
| Delete Driver | Off | On | Yes | No |
| Update DOB | On | On | Yes | No |
| Update DL No./Type/State/Country | On | On | Yes | No |
| Update Occupation | On | On | Yes | No |
| Update Employer Name | On | On | Yes | No |
| Add Violation | On | On | Yes | No |
| Add SR-22 | On | On | Yes | No |
| Add Vehicle | On | On | Yes | No |
| Remove Vehicle | On | On | Yes | No |
| Update VIN | Off | On | Yes | No |
| Update Garaging Address | On | On | Yes | No |
| Update Lienholder | On | On | Yes | No |
| Add Coverage | On | On | Yes | No |
| Remove Coverage | On | On | Yes | No |
| Update Vehicle Usage | On | On | Yes | No |
| Update/Remove Photo Discount | Off | On | Yes | No |
| Update Vehicle Mileage | Off | On | Yes | No |
| Update Vehicle Owner Name | Off | On | Yes | No |

### **1.5: Non-Owner Configurations**

Defines specific rules and dependencies that apply when a policy is marked as **Non-Owner**.

| **Setting
`(non-editable)`** | **Description
`(non-editable)`** | **Default
`(editable)`** |
| --- | --- | --- |
| **SR-22 Required if Non-Owner** | When enabled, the system will require an SR-22 to be filed if the policy type is set to Non-Owner. If disabled, SR-22 is optional. | Toggle (On/Off) |

### **1.6: Driver Removal Support**

Controls whether agents can use the **"Removed"** status for drivers in the Rate/Quote/Bind flow.

- **If On:**
    - A “Removed Drivers” section will appear in the **Driver Details** step.
    - “Removed” will be available in the driver status dropdown.
    - Agent will be prompted to select a **Reason for Removal**.
- **If Off:**
    - The “Removed Drivers” section will be hidden.
    - The status selector will only include **Included** and **Excluded**.

| **Setting
`(non-editable)`** | **Description
`(non-editable)`** | **Type
`(editable)`**
 | **Default
`(editable)`** |
| --- | --- | --- | --- |
| Allow Driver Removal | Controls whether agents can set a driver’s status to “Removed.” | Toggle (On/Off) | Off |

### **1.7 — Cancellation Effective Date Offset**

Specifies how many calendar days to delay the effective date of cancellation from the current day, to allow for proper notice.

| **Setting
`(non-editable)`** | **Description
`(non-editable)`** | **Number of Days
`(editable)`** |
| --- | --- | --- |
| Cancellation Effective Offset | Determines how many calendar days after the cancellation is initiated the cancellation becomes effective. | Numeric input (e.g. 11) |

### **1.8 — Cancellation Method**

Specifies how premium is calculated upon cancellation.

| **Method
`(non-editable)`** | **Description
`(non-editable)`** | **Default (Yes/No)
`Single-select only`** |
| --- | --- | --- |
| **Pro Rata** | Refunds or adjustments are calculated proportionally based on unused time. | Yes |
| **Short Rate** | Refunds or adjustments use a penalty method, retaining more premium. | No |

### **1.9 — Invoice Notification Days**

Specifies how far in advance to notify the insured of an upcoming installment or premium bill.

| **Setting
`(non-editable)`** | **Description
`(non-editable)`** | **Number of Days
`(editable)`** |
| --- | --- | --- |
| **Invoice Lead Time** | Number of calendar days prior to the due date that the invoice is sent. | Numeric input (e.g. 20) |

## **2 — Claim Configurations**

### **2.1 — Foundational Configurations**

> Pulled from `Claim Program Maintenance` in Data Maintenance
> 

| **Label** | **Description** | **Input Type** | **Notes / Rules** |
| --- | --- | --- | --- |
| Email Adjusters New Assignments | If enabled, sends email alerts to adjusters when a new assignment is created. | Yes / No toggle | Controls notification flow. |

### **2.2 — Standard Reserves**

> Pulled from `Standard Reserves` in Data Maintenance
> 

Standard reserves define the default monetary amounts that are initially set aside for a claim or expense when a loss is reported. These reserves vary based on the **reserve type** (e.g., Claim Reserve or Expense Reserve), **claim status**, and **cause code**. Each row in the reserve matrix assigns dollar values by **coverage line** and is applied when the specified logic matches.

This section helps drive predictable and consistent reserving practices across the claims workflow.

**2.2.1 — Reserve Configuration Table**

| **Reserve
`(editable)`** | **Status
`(editable)`** | **Cause Code
`(editable)`** | **BI
`(editable)`** | **PD
`(editable)`** | **UMBI
`(editable)`** | **UMPD
`(editable)`** | **MED
`(editable)`** | **PIP
`(editable)`** | **COMP
`(editable)`** | **COLL
`(editable)`** | **AEC
`(editable)`** | **TOW
`(editable)`** | **RENTAL
`(editable)`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Default Fallback | - | - | $1.00 | $1.00 | $1.00 | $1.00 | $1.00 | $1.00 | $1.00 | $1.00 | $1.00 | $1.00 | $1.00 | On |
| Claim Reserve | Litigation | 020 | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | On |
| Claim Reserve | Open | 030 | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | On |
| Claim Reserve | Represented | 026 | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | On |
| Expense Reserve | Litigation | ### | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | On |
| Expense Reserve | Open | ### | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | On |
| Expense Reserve | Represented | ### | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | $####.## | On |
| `Add/delete a reserve` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

**2.2.2 — Definitions**

- **Reserve Type**: Indicates whether the row represents a Claim Reserve (indemnity) or Expense Reserve (legal fees, etc.).
- **Status**: Describes the current state of the claim (e.g., Open, Represented, or in Litigation).
- **Cause Code**: Code used to further segment reserves (e.g., by injury type, loss type, etc.).
- **Supported**: Indicates whether the reserve rule is currently active for use in the program.

**2.2.3 — Configuration Guidelines**

- Each combination of **Reserve Type + Status + Cause Code** must be unique.
- Every **coverage line** must have a default dollar value per reserve rule.
- The system will default to the "Fallback" rule if no explicit match is found.

### **2.3 — External Appraisal Link Configuration**

Defines the static upload URLs provided by third-party appraisal vendors. These links are used when the FNOL rep or Adjuster selects **“Use External Appraiser Link”** during an appraisal media request.

This configuration ensures the system can populate and send the correct link. The message is handled separately in `message maintenance`

### **Configuration Options**

- **Vendor Name**
    
    Select from `System entity/offices` list. 
    
- **Static Upload Link**
    
    A non-unique, persistent link hosted by the external appraisal company.
    
- **Supported Program Term(s)**
    
    Multi-select: define which program terms this vendor is available for (e.g., 6-month, 12-month).
    
- **FNOL Appraisal Modal Enabled (Yes/No Toggle)**
    
    Determines if the modal (shown during rate/quote/bind) that allows FNOL reps to send appraisal links is active. When **FNOL Appraisal Modal Enabled** is turned **Off**, the modal will not display to FNOL users at the end of the report-a-loss flow. This allows carriers to control whether media collection is initiated at FNOL or deferred to a later workflow step.
    

### **2.4 — Req CMS Data Validation**

## **3 — Suspense Configurations**

This section defines how suspense tasks are managed, escalated, and resolved based on type and ownership.

### **3.1 — Global Defaults**

| **Setting
`(Non-editable)`** | **Description
`(editable)`** | **Input Type
`(Not editable)`**
 | **Example
`(editable)`**
 |
| --- | --- | --- | --- |
| **Default Suspense Days** | Number of days before a suspense is considered overdue if no override is set. | Numeric input | 5 |
| **Escalation Routing Enabled** | Allows suspense escalation to be routed to a specific manager type. | Yes/No toggle | Yes |

### **3.2 — Policy Suspense Types**

Each row below inherits the global suspense day value unless overridden. If escalation is triggered, the task is routed to the Underwriting Manager.

| **Suspense Type
`(editable)`**
 | **Verbiage
`(editable)`** | **Override Days
`(editable)`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- |
| 515A | Please provide a signed 515A for the following parties | 5 | On |
| Alternate Garaging Address | Please provide garaging address for all vehicles | 7 | On |
| Alternate Garaging Address Due to Claims Activity | Please provide garaging address; claims investigation indicated that the vehicle is garaged at an alternate location | 7 | On |
| Body Shop Estimate | Please provide estimate for the following vehicle that has existing damage | 10 | On |
| Drivers License | Please provide a copy of the following driver’s license, matricula or passport | 5 | On |
| Email Address Verification | Please provide a valid email address to the policyholder | 5 | On |
| Employer/Occupation Verification | Please provide occupation and employer name for the following drivers | 7 | On |
| Military ID | Please provide a copy of the military ID for driver | 7 | On |
| Missing Signature on Application | Please provide the completed signed application | 3 | On |
| Physician Statement | Please provide a copy of the physician’s statement for driver | 10 | On |
| Possible Business Use | Please provide a no business use statement | 7 | On |
| Proof of Prior Insurance | Please provide prior insurance discount proof | 7 | On |
| Proof of Transfer Discount | Please provide transfer discount proof | 7 | On |
| Proof of Homeownership | Please provide proof of homeownership | 7 | On |
| Undisclosed Claim | The following undisclosed claim was identified — provide proof of not at fault to prevent points being assessed | 10 | On |
| Undisclosed Driver | Please provide driver information for the undisclosed driver identified | 5 | On |
| Undisclosed Driver Due to Claims Activity | Please provide driver information for the driver identified during the claims investigation | 5 | On |
| Vehicle Photos | Please provide vehicle photos (each side, odometer, and VIN plate) | 3 | On |
| Vehicle Registration | Please provide a copy of the vehicle registration | 7 | On |
| Vehicle Title Transfer | Please provide title transfer for vehicles | 7 | On |
| VIN Verification | Please provide a valid VIN or copy of the vehicle registration | 5 | On |
| `Add/delete suspense type` | — | — | — |

### **3.3 — Claims Suspense**

Claims suspenses function as **freeform tasks**, not tied to a fixed list of suspense types.

- The system applies the **global suspense day value** for all claim suspense tasks.
- If unresolved within the suspense day window, the task is automatically escalated to the **Claims Manager** and appears in their dashboard queue.

## **4 — Additional Configurations**

### **4.1 — Account Maintenance**

> Pulled from `Account Maintenance` in Data Maintenance
> 

This section defines the financial accounts used within the insurance program. These accounts control where funds are deposited, how claims and refunds are disbursed, and how they relate to associated system entities such as MGAs or claims vendors.

**4.1.1 — Accounts Table**

Each account is configured independently and can be tied to one or more system entities. Common examples include premium trust accounts, claims disbursement accounts, and refund accounts.

| **Account Description `(editable)`** | **Account Number** 
**`(editable)`** | **Bank** 
**`(dropdown)`

`This information is pulled from Bank Maintenance`** | **Positive Pay Enabled** 
**`(Yes/No)`** | **Linked System Entity** **`(dropdown)`

`This information is pulled from our system entity list`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- |
| Claims Account | 110******* | Sunflower Bank | Yes | Aguila Dorada | On |
| Premium Trust – Old American County Mutual | 110******* | Compass Bank | Yes | Aguila Dorada | On |
| Refund Account | 110******* | Wells Fargo | No | Aguila Dorada | On |
| `Add account` |  |  |  |  |  |

**4.2.2 — System Entities/Offices**

> Pulled from `System Client Maintenance` / `Office Maintenance` in Data Maintenace
> 

A system entity is a defined organizational participant in the insurance operation. This may include MGAs, claim offices, or third-party administrators (TPAs). Entities must be added before they can be linked to an account.

**Core Details Collected**

- **Entity ID**: A unique internal identifier (e.g., `002`); system generated.
- **Entity Name**: The full legal name of the organization (e.g., *Prioris Claims Management Solutions*).
- **Entity Type**: Select from predefined types:
    - MGA (Managing General Agent)
    - Claim Office
- **Logo File:** Image upload
- **License Number:**

**Contact Information**

- **Phone**
- **Fax**
- **Email Address**
- **Web Address (URL**

**Business & Reporting Contacts**

- **Business Contact Name**
- **Business Contact Email**
- **Reporting Contact Name**
- **Reporting Contact Email**

**Address Information**

- **Physical Address**
    - Street Address (e.g., 580 Decker Dr Ste 264)
    - City
    - State
    - ZIP Code
- **Mailing Address**
    - PO Box or Street Address
    - City
    - State
    - ZIP Code

**Status**

- **Supported (On/Off)**: Controls whether this entity is active in the system and available for selection when configuring accounts or claims routing.

## **5 — Program Documentation**

Preloaded reference to required regulatory documents (e.g., declarations, FCRA notices). This also includes all of the underwriting documents that are tied to the program.

`<upload documents>`