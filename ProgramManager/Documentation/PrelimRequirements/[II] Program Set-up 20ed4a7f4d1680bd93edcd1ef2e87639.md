# [II] Program Set-up

## **1 — Select Program-Level Details**

This section defines all essential metadata and operational parameters for an insurance program. These settings govern how the program is identified, activated, versioned, and distributed.

### **1.1 — Treaty Definition**

| **Field** | **Description** | **Input Type** |
| --- | --- | --- |
| **Treaty Name** | Lorem ipsum | Freeform text area |
| **Treaty Number** | Auto-generated unique identifier for each treaty.  | System-generated |
| **Insurance Company / Carrier** | The licensed insurer backing the program (e.g., “Old American”). | Dropdown (preloaded list) |
| **Carrier Appointment Fee** | This is the fee amount that is tied to the Insurance Company / Carrier.  | Dollar amount |

### **1.2 — Treaty Years**

A timeline-style or list interface under the treaty, where the user adds 1 or more treaty years.

| **Field** | **Description** | **Input Type** |
| --- | --- | --- |
| **Year Label** | e.g., "Year 1", "2023–2024", etc. | Freeform text area |
| **Effective Date** | The effective date for the treaty year. | Date picker |
| **Expiration Date** | Automatically set by the system based on the activation of the next treaty year. | Auto-generated |

### **1.3 — Add Programs per Treaty Year**

| **Field** | **Description** | **Input Type** |
| --- | --- | --- |
| **Program Prefix** | A short identifier (e.g., `ADGA`) used for internal reference and policy number formatting. | System-generated |
| **Program Number** | Tracks the current version of the program. | System-generated |
| **Program Description** | Narrative explanation of the program's focus, target market, or unique features. | Freeform text area |
| **Effective Date** | Date when the program becomes available for quoting/binding. | Date picker |
| **Max Future Effective Date (in Days)** | The maximum number of days into the future that a policy’s effective date can be set.

- Default is 30 days | Dropdown (preloaded list) |
| **End Date** | This is a manually set end date for the respective program.  | Date picker |
| **State Approval Date** | Date when the program was formally approved by the regulating state insurance department. | Date picker |
| **Program Version Control** | Tracks the current version of the program and its revision history. Includes timestamps, changelogs, etc. | System-generated |

### **1.4 — Program Terms**

Policy term determines the duration of coverage and may impact rating factors across all coverage lines. Most commonly, terms are set to either 6 or 12 months.

| **Value**
**`(editable)`** | **Interval
`Always Months`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- |
| 6 | Months | On |
| `Add/delete term` |  |  |

## **2 — Coverage Base Rates & Limits**

The limits section defines available coverage levels for each line of insurance, allowing users to activate or deactivate individual lines of coverage and assign corresponding base premiums. For each limit option, a factor is applied to the base rate, with these base rates forming the foundation for all factor-driven adjustments in the rating calculation.

### **2.1 — Global Rounding Controls**

Defines the default decimal precision used when applying rating factors, unless overridden at the row level. 

| **Label
`(non-editable)`** | **Description
`(non-editable)`** | **Allowed Values
`(editable)`** | **Round Factor By Default
`(editable)`** |
| --- | --- | --- | --- |
| Global Round By | Sets the default number of decimal places for all rating factor calculations, unless a row-specific override is defined. | 0, 1, 2, 3 | 2 |

### **2.2 — Base Rates**

Note: `*Base Premium includes a discount of -0.5% for OACM.Punitive.018 (Rev 2013 01)`

| **Label
`(editable)`** | **Base Rate
`(editable)`** | **Dependencies** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- |
| Bodily Injury (Liability) | $347.51 |  | **`Select from program term options`** | On |
| Property Damage (Liability) | $384.98 |  | **`Select from program term options`** | On |
| UM – Bodily Injury | $81.73 | This **must** match the limits, or be **less than**, what is outlined for BI. | **`Select from program term options`** | On |
| UM – Property Damage | $105.08 | This **must** match the limits, or be **less than**, what is outlined for PD. | **`Select from program term options`** | On |
| Medical Payments | $29.19 |  | **`Select from program term options`** | On |
| Personal Injury Protection (PIP) | $175.14 |  | **`Select from program term options`** | On |
| Comprehensive | $261.82 | Paired with COLL. | **`Select from program term options`** | On |
| Collision | $987.32 | Paired with COMP. | **`Select from program term options`** | On |
| Additional Equipment Coverage | $3.27 | Must have COLL and COMP in order to have AEC coverage. | **`Select from program term options`** | On |
| Towing & Labor | $20.00 | Must have COLL and COMP in order to have TL coverage. | **`Select from program term options`** | On |
| Rental Reimbursement | $45.00 | Must have COLL and COMP in order to have RR coverage. | **`Select from program term options`** | On |
| `Add/delete supported coverage line` |  |  |  |  |

### **2.3 — Bodily Injury (BI) Limits**

| **Limit per Person
`(editable)`** | **Limit per Accident
`(editable)`** | **Label
`System Generated`** | **Round Factor By
`(editable)`** | **Factor
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- |
| $30,000 | $60,000 | $30,000 / $60,000 | 2 | 1.05 | **`Select from program term options`** | On |
| `Add/delete BI limit` |  |  |  |  |  |  |

### **2.4 — Property Damage (PD) Limits**

| **Limit
`(editable)`** | **Round Factor By
`(editable)`** | **Factor
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- |
| $25,000 | 2 | #.## | **`Select from program term options`** | On |
| `Add/delete PD limit` |  |  |  |  |

### **2.5 — PIP Limits**

| **Limit
`(editable)`** | **Round Factor By
`(editable)`** | **Factor
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- |
| $2,500 | 2 | #.## | **`Select from program term options`** | On |
| `Add/delete PIP limit` |  |  |  |  |

### **2.6 — UMBI Limits**

**2.6.1 — UMBI Limit Dependency Rule**

Defines the relationship between **UMBI** and **BI** limits.

| **Setting
`Not editable`** | **Description
`Not editable`** | **Default
`(editable)`

`Only one default can be selected`** |
| --- | --- | --- |
| **Must match BI** | UMBI limit options must exactly match the BI limits. | Off |
| **Can be less than or equal to BI** | UMBI limits must be less than or equal to BI limits. | On |
| **Can be greater than or equal to BI** | UMBI limits must be greater than or equal to BI limits. | Off |
| **Independent** | No dependency; UMBI limits can be set freely regardless of BI. | Off |

**2.6.2 — UMBI Limit Dependency Rule**

| **Limit per Person
`(editable)`** | **Limit per Accident
`(editable)`** | **Label
`System Generated`** | **Round Factor By
`(editable)`** | **Factor
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- |
| $30,000 | $60,000 | $30,000 / $60,000 | 2 | #.## | **`Select from program term options`** | On |
| `Add/delete UMBI limit` |  |  |  |  |  |  |

### **2.7 — UMPD Limits**

**2.7.1 — UMPD Limit Dependency Rule**

Defines the relationship between **UMPD** and **PD** limits.

| **Setting
`Not editable`** | **Description
`Not editable`** | **Default
`(editable)`

`Only one default can be selected`** |
| --- | --- | --- |
| **Must match PD** | UMPD limit options must exactly match the PD limits. | Off |
| **Can be less than or equal to PD** | UMPD limits must be less than or equal to PD limits. | On |
| **Can be greater than or equal to PD** | UMPD limits must be greater than or equal to PD limits. | Off |
| **Independent** | No dependency; UMPD limits can be set freely regardless of PD. | Off |

**2.6.2 — UMPD Limit Dependency Rule**

| **Limit
`(editable)`** | **Round Factor By
`(editable)`** | **Factor
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- |
| $25,000 | 2 | #.## | **`Select from program term options`** | On |
| `Add/delete UMPD limit` |  |  |  |  |

### **2.8 — MED Limits**

| **Limit
`(editable)`** | **Round Factor By
`(editable)`** | **Factor
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- |
| $500 | 2 | #.## | **`Select from program term options`** | On |
| $1,000 | 2 | #.## | **`Select from program term options`** | On |
| `Add/delete MED limit` |  |  |  |  |

### **2.9 — Additional Equipment Coverage (AEC)**

Additional Equipment Coverage (AEC) allows policyholders to insure **custom or aftermarket equipment** added to a panel truck, pickup, or van on a **stated amount basis**. This is an optional endorsement that must be explicitly selected.

**Eligibility & Rules**

- AEC is only available for vehicles **insured for physical damage** (i.e., must have **Comprehensive or Collision** coverage).
- The **AEC deductible** must match the selected COMP & COLL deductibles.

**Define Base Rate & Coverage Range**

| AEC Base Rate
**`(editable)`** | $3.27 |
| --- | --- |

| **Min Limit
`(editable)`** | **Max Limit
`(editable)`** | **Increment
`(editable)`** |
| --- | --- | --- |
| $100 | $3,000 | $100 |

**Rating Formula**

```
Premium = ((AEC Limit / 100) * AEC Base Rate) * Payment Plan Multiplier * Term
```

- **Payment Plan Multiplier (Pulled from `Payment Plan` section)**: Applied based on selected payment plan (i.e. Installment, PIF, EFT), pulled from the `AEC` column.
- **Term (Pulled from `Term` section)**: Policy term factor (e.g., 1.00 for 6-month term)

**Validation Rules**

- AEC can only be selected if **COMP or COLL** is also selected.
- Limit must be within the define range and in the defined increments.

### **2.10 — Towing Limits**

| **Limit
`(editable)`** | **Round Factor By
`(editable)`** | **Factor
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- |
| $40 | 2 | #.## | **`Select from program term options`** | On |
| $75 | 2 | #.## | **`Select from program term options`** | On |
| `Add/delete Towing limit` |  |  |  |  |

### **2.11 — Rental Limits**

| **Daily Limit
`(editable)`** | **Maximum Total
`(editable)`** | **Round Factor By
`(editable)`** | **Factor
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- |
| $20 | $600 | 2 | #.## | **`Select from program term options`** | On |
| $30 | $900 | 2 | #.## | **`Select from program term options`** | On |
| $40 | $1,200 | 2 | #.## | **`Select from program term options`** | On |
| `Add/delete Rental limit` |  |  |  |  |  |

## **3 — Policy Term & Renewal Rating**

### **3.1 — Policy Term Rating Table**

| **Value**
**`(editable)`** | **Interval
`Always Months`** | **Round Factor By
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
`(editable)`

Also include a column “on/off” option** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | Months | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | On |
| `Add/delete term from available options` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

## **4 — Add Supported Program Geographies**

Allows users to define which geographic regions are supported by the program. Territory factors are geographic multipliers applied to rating calculations based on the **ZIP code** and optionally the **county** in which the vehicle is garaged. These factors reflect historical claim frequency, severity, medical costs, and other local risk variables tied to location.

### **4.1 — Program State Selection**

Single-select state dropdown (U.S. only). **This determines which state are supported by the program. For V1, this will be limited to Texas only.** 

`Note` A user is only able to select one state per program.

| **State Code
`(non-editable)`** | **State Name
`(non-editable)`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- |
| TX | Texas | On |
| CA | California | Off |
| FL | Florida | Off |
| NY | New York | Off |
| IL | Illinois | Off |
| GA | Georgia | Off |
| AZ | Arizona | Off |
| ... | (Remaining states) | Off |

**Once state is selected, input sales tax rate:** 

| **Label
`(non-editable)`** | **Description
`(non-editable)`** | **Input Type
`(editable)`** |
| --- | --- | --- |
| Sales Tax | Sales tax applied to certain states, used in the total loss worksheet. | Percentage (i.e. 13%) |

### **4.2 — ZIP Code Selection (Powered by Google Maps API)**

- **Integration:** Powered by Google Maps API.
- **Result Display**:
    - `ZIP Code`
    - `County`
- **Supported:** All counties are supported by default, with the ability to deselect. ZIP code is tied to the **garaging address**, not mailing or billing addresses.
- **Manual Entry**: Users may manually add a ZIP code row if a valid ZIP is not found via search

| **ZIP** | **County** | **Round Factor By
`(editable)`** | **BI
`(editable)`** | **PD
`(editable)`** | **UMBI
`(editable)`** | **UMPD
`(editable)`** | **MED
`(editable)`** | **PIP
`(editable)`** | **COMP
`(editable)`** | **COLL
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 75148 | ANDERSON | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 75751 | ANDERSON | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 75904 | ANGELINA | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 76310 | ARCHER | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 79019 | ARMSTRONG | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| … | … |  | … | … | … | … | … | … | … | … | … | … |
| `Add/delete zip code` |  |  |  |  |  |  |  |  |  |  |  |  |

## **5 — Policy Distribution Channel**

Adjusts rates based on how the policy was sold—whether through a retail agency, captive producer, independent agent, or direct-to-consumer. For our version, only `Agent-Assisted` will be relevant.

### **5.1 — Rating Table**

| **Channel** | **Round Factor By
`(editable)`** | **BI
`(editable)`** | **PD
`(editable)`** | **UMBI
`(editable)`** | **UMPD
`(editable)`** | **MED
`(editable)`** | **PIP
`(editable)`** | **COMP
`(editable)`** | **COLL
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Agent Assisted | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| **`*Code updated required to add distribution channel*`** |  |  |  |  |  |  |  |  |  |  |  |

### **6 — Program Integrations**

This section defines and configures the third-party integrations connected to the program. Each integration includes a pre-defined type, the specific integration selected, where it’s used, and its purpose.

<aside>
<img src="https://www.notion.so/icons/report_red.svg" alt="https://www.notion.so/icons/report_red.svg" width="40px" />

INCOMPLETE

</aside>

| **Integration Type
`(Non-Editable)`** | **Integration** 
**`(Editable)`**

**`Dropdown` — Next three columns update based on this selection.** | **Used In
`(Non-Editable)`** | **Purpose
`(Non-Editable)`** | **Connected
`(Non-Editable)`

`System generated`** |
| --- | --- | --- | --- | --- |
| Comparative Rater | ITC / Zywave | RQB/Program | Prefill quote data using external rater platforms like TurboRater or EZLynx. | `⭘ Connected / ⭘ Not Connected` |
| Payment Processor | Paysafe / Tranzpay | System | Facilitate premium payments through electronic fund transfers and card processing. | `⭘ Connected / ⭘ Not Connected` |
| Vehicle Symbols | Verisk VINMASTER | RQB/Program | Lookup ISO vehicle symbol and rating values for VINs. | `⭘ Connected / ⭘ Not Connected` |
| Vehicle Prefill | Verisk Lightspeed | RQB/Program | Prefill vehicle and driver info using carrier-grade data. | `⭘ Connected / ⭘ Not Connected` |
| CMS Reporting | **[TBD]** | System | Generate regulatory claim reports for submission to state or partner systems. | `⭘ Connected / ⭘ Not Connected` |
| Prior Claim Lookup | Verisk ISO Claim Search | RQB/Program | Search prior claims associated with the applicant or VIN. | `⭘ Connected / ⭘ Not Connected` |
| Household Driver Lookup | DCS | RQB/Program | Return list of licensed drivers at a household address for inclusion. | `⭘ Connected / ⭘ Not Connected` |
| Household Vehicle Lookup | DCS | RQB/Program | Return list of vehicles registered to a household. | `⭘ Connected / ⭘ Not Connected` |
| Criminal History Lookup | DCS | RQB/Program | Search public criminal history records tied to applicant. | `⭘ Connected / ⭘ Not Connected` |
| Mail Processor | DMP | System | Print and mail policy documents, notices, and checks. | `⭘ Connected / ⭘ Not Connected` |
| Positive Pay | Sunflower Bank | System | Adds banking fraud prevention via positive pay rules for issued checks. | `⭘ Connected / ⭘ Not Connected` |
| Real-Time Verification | TexasSure FRVP | System | Confirms whether a vehicle has valid insurance through state APIs. | `⭘ Connected / ⭘ Not Connected` |
| Messaging (SMS) | Twilio | System | Sends outbound SMS for FNOL, renewal, verification, and other workflows. | `⭘ Connected / ⭘ Not Connected` |
| Address Verification | Smarty | System | Validates and standardizes residential and mailing addresses. | `⭘ Connected / ⭘ Not Connected` |
| Mapping API | Google Maps | System | Supports map-based reporting, distance-to-work, or zip validation. | `⭘ Connected / ⭘ Not Connected` |
| Email Delivery | SendGrid | System | Sends system-generated emails like verification links and documents. | `⭘ Connected / ⭘ Not Connected` |