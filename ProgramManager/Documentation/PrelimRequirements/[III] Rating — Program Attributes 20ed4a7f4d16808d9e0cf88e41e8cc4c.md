# [III] Rating — Program Attributes

# Policy Fees, Discounts, and Surcharges

## **1 — Payment Options**

### **1.1 —**  Payment Options

This section defines which payment methods are supported in the program, including detailed configuration of installment plan options. These settings control how premiums are structured and paid over time.

| **Payment Plan
`(editable)`** | **Round Factor By
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
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Installment | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| PIF | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| **`*Code updated required to add payment option*`** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

### **1.2 —**  EFT (AutoPay) Support

This configuration controls whether **automatic payments (EFT/AutoPay)** are supported for a given program term. It is **not a payment plan**, but an enhancement layered on top of the chosen plan (e.g., Installment or PIF).

| **EFT
`(editable)`** | **Round Factor By
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
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Yes | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| No | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| **`*Code updated required to add payment option*`** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

### **1.3 —**  Installment Options

If installments are enabled (i.e. `set to "On"`, a program must define one or more supported installment options. Each option includes the total number of installments and required down payment percentage. 

| **Total Installments
`(editable)`** | **Percent Down
`(editable)`** | **Description
`(editable)`** | **Round Factor By
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
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 16.67% | 5 payments with 1/6th down | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 6 | 20.00% | 6 payments with 20% down | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 4 | 25.00% | 4 payments with 25% down | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 2 | 50.00% | 2 payments with 50% down | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete installment option` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

### **1.4 —**  Accepted Payment Methods

Defines how payments are collected for a policy.

| **Label
`(editable)`** | **Description
`(editable)`** | **Round Factor By
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
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Producer E-Check | E-check payment initiated and submitted by the producer.  | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Insured E-Check | E-check payment initiated directly by the insured.  | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Credit Card | Secure credit card payment submitted by the insured.  | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| **`*Code updated required to add payment option*`** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

## **2 — Policy Fees**

These are flat administrative or regulatory fees applied either per policy, per installment, or in response to user-driven actions.

### **2.1 —**  Entity **Based Fees**

Fees that are based on a single entity.

| **Label
`(editable)`** | **Description
`(editable)`** | **Default
`(editable)`** | **Applied Per Entity
`Dropdown; Policy, Driver, Vehicle`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- |
| MGA Fee | A fee charged by the Managing General Agent (MGA) for servicing or administration. | $90.00 | Policy | **`Select from program term options`** | On |
| MVCPA Fee | A state-mandated fee (e.g., Texas MVCPA) that funds motor vehicle crime prevention. | $2.50 | Vehicle | **`Select from program term options`** | On |
| Convenience Fee | Credit card processing fee on the MGA side to cover the expense.  |  - | - | - | - |
|  | Downpayment (also includes “PIF”) | $0.00 | Policy | **`Select from program term options`** | On |
|  | Installment | $0.00 | Policy | **`Select from program term options`** | On |
|  | Endorsement | $0.00 | Policy | **`Select from program term options`** | On |
| **`*Code updated required to an entity based fee*`** |  |  |  |  |  |

### **2.2 —**  Installment Base Fee

Installment fees are configured per available **policy term option**. For each term, the user can define:

- A **base threshold** `(editable)`
- A **per-increment charge** `(editable)`
- The **increment amount** that triggers the charge `(editable)`

**Configuration Inputs**

| **Term**
 | **Base Threshold
`(editable)`** | **Base Fee
`(editable)`** | **Increment Amount
`(editable)`** | **Increment Fee
`(editable)`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- |
| 3 mo | $150 | $3.50 | $100 | $0.50 | On |
| 6 mo | $250 | $3.50 | $125 | $0.50 | On |
| 12 mo | $500 | $3.50 | $250 | $1.00 | On |
| `Select from program term options` |  |  |  |  |  |

**Calculation Logic**

```
Installment Fee = Base Fee + ((Term Premium − Base Threshold) / Increment Amount)) × Increment Fee
```

**Where**

- **Base Fee** = $3.50
- **Base Threshold** = $250
- **Increment Amount** = $125
- **Increment Fee** = $0.50
- **Term Premium** = total premium for the term

**Explanation:**

- Charge **$3.50** for the first **$250** of premium
- Then charge **$0.50** for **each additional $125** (or part thereof) above that

### **Example (Term Premium = $600):**

```
Installment Fee = 3.50 + ceil((600 - 250) / 125) × 0.50
                = 3.50 + ceil(350 / 125) × 0.50
                = 3.50 + 3 × 0.50
                = $5.00
```

### **2.3 —**  Additional Fixed Fees

| **Label
`(editable)`** | **Description
`(editable)`** | **Default
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- |
| NSF | Non-Sufficient Funds fee; a charge that occurs when a payment (typically by check or bank draft) is attempted, but the payer's account doesn't have enough funds to cover the amount. | $25.00 | **`Select from program term options`** | On |
| Late; Past Due Date | 10 days after due date | $5.50 | **`Select from program term options`** | On |
| Endorsement | Adding/Removing Vehicles, Coverage and Drivers | $15.00 | **`Select from program term options`** | On |
| SR-22 | This is charged per SR-22 | $25.00 | **`Select from program term options`** | On |
| **`*Code updated required to add fixed fee*`** |  |  |  |  |

## **3 — Discounts & Surcharges**

Certain discounts or surcharges are applied to policies based on declared behavior, status, or optional selections. These adjustments apply across multiple lines of coverage.

### **3.1 —**  Number of Months Prior Coverage

Used to determine eligibility for prior insurance discounts.

| **Number of Months of Prior Coverage (Min)
`(editable)`** | **Number of Months of Prior Coverage (Max)
`(editable)`** | **Interval
`Dropdown; Days, Months, Years`** | **Round Factor By
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
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 6 | Months | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 6 | 11 | Months | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 12+ |  | Months | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add prior coverage option` |  |  |  |  |  |  |  |  |  |  |  |  |  |

### **3.2 —**  Prior Insurance Verification Level

Used to assess the strength of the prior insurance evidence, which may influence the discount amount. 

| **Label**
**`(editable)`** | **Round Factor By
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
| Prior Insurance (reported by the insured)
 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Transfer (validated by MGA or producer)
 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Verified (confirmed via Lightspeed integration). | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add prior insurance verification level option` |  |  |  |  |  |  |  |  |  |  |  |

### **3.3 —**  Is Insured a Homeowner?

Provides a discount if the insured owns a home.

| Label
**`(editable)`** | **Round Factor By
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
| Yes | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| No | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |

### **3.4 —**  Residence Type

Captures the type of home the insured lives in. Used for rating logic and may impact discount eligibility.

| **Label**
**`(editable)`** | **Round Factor By
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
| Apartment/Condo | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Fixed Mobile Home | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Mobile Home | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Home | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add residence type option` |  |  |  |  |  |  |  |  |  |  |  |

### **3.5 —**  Enroll in Paperless

Indicates if the user opts to receive bills and notices electronically. 

| **Label**
**`(editable)`** | **Round Factor By
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
| Yes | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| No | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add enroll in paperless option` |  |  |  |  |  |  |  |  |  |  |  |

### **3.6 —**  Is this a Non-Owner Policy?

Indicates if the user opts to receive bills and notices electronically. 

| **Label**
**`(editable)`** | **Round Factor By
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
| Yes | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| No | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add non-owner policy option` |  |  |  |  |  |  |  |  |  |  |  |

### **3.7 —**  Deductible Increase Endorsement

Offers a discount for selecting a 'Double Deductible' for the first 90 days of the policy.

| **Label**
**`(editable)`** | **Round Factor By
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
| Yes | 2 | - | - | - | - | - | - | 0.900 | 0.900 | **`Select from program term options`** | On |
| No | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add deductible increase option` |  |  |  |  |  |  |  |  |  |  |  |

### **3.8 —**  Recurring EFT Payments

Enables automatic premium deductions.

| **Label**
**`(editable)`** | **Round Factor By
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
| Yes | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| No | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add recurring EFT payment option` |  |  |  |  |  |  |  |  |  |  |  |

### **3.9 —**  Paying in Full

Discount applied when the full annual premium is paid upfront.

| **Label**
**`(editable)`** | **Round Factor By
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
| Yes | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| No | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add paying in full option` |  |  |  |  |  |  |  |  |  |  |  |

### **3.10 —**  Unlisted Driver

Discount applies when all household drivers are disclosed.

| **Label**
**`(editable)`** | **Round Factor By
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
| Yes | 2 | - | - | - | - | - | - | - | 0.950 | **`Select from program term options`** | On |
| No | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add unlisted driver option` |  |  |  |  |  |  |  |  |  |  |  |

### **3.11 —**  Early Shopper

Early shopper is a policy purchased at least 3 days before policy inception date.

| **Days before policy inception date**
**`(editable)`** | **Round Factor By
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
| 3 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add early shopper option` |  |  |  |  |  |  |  |  |  |  |  |

### **3.12 —**  Multi-Car

Applies a discount if the policy includes two or more vehicles at bind.

| **Multi-Car (Defined as 2+ vehicles on the policy)** | **Round Factor By
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
| Yes | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| No | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |

### **3.13 — Vehicle Photos**

A discount is applied to **Comprehensive (COMP)** and **Collision (COLL)** premiums when a vehicle photo is provided. This serves as a verification mechanism and a fraud deterrent, particularly at the time of policy issuance or renewal.

- **Automatically applied** at **New Business (NB)** and **Renewal** if `VehiclePhoto = Yes`

| **Vehicle Photo Provided?** | **Round Factor By
`(editable)`** | **COMP
`(editable)`** | **COLL
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- |
| No | 2 | #.## | #.## | **`Select from program term options`** | On |
| Yes | 2 | #.## | #.## | **`Select from program term options`** | On |

# Vehicle Attributes

## **4 — Driver<>Vehicle Assignment Method**

This method matches the highest-rated driver to the highest-rated vehicle, aligning risk-based driver attributes with vehicle-level rating factors to determine premium outcomes.

### **4.1 — Assignment Logic**

- Drivers are **ranked by their Driver Factor (used for BI (Bodily Injury))**, which is a composite score based on:

| Attribute
**`Select from available attribute list`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- |
| Driver Class | **`Select from program term options`** | On |
| Points | **`Select from program term options`** | On |
| License Type | **`Select from program term options`** | On |
| `Add/delete attribute` |  |  |
- Vehicles are **ranked by their Vehicle Factor (used for COLL (Collision))**, which is a composite score (i.e. 1.15 × 1.15 x factor x, etc.) based on:

| Attribute
**`Select from available attribute list`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- |
| Model Year | **`Select from program term options`** | On |
| Symbol – Physical Damage | **`Select from program term options`** | On |
| Usage | **`Select from program term options`** | On |
| Coverage Type | **`Select from program term options`** | On |
| Deductibles | **`Select from program term options`** | On |
| Territory | **`Select from program term options`** | On |
| AEC Limit | **`Select from program term options`** | On |
| Photo | **`Select from program term options`** | On |
| `Add/delete attribute`  |  |  |

### **4.2 — Matching Process**

1. **Calculate Driver Factors** for all listed drivers.
2. **Calculate Vehicle Factors** for all listed vehicles.
3. **Sort both lists in descending order** (highest to lowest factor).
4. Assign drivers to vehicles **one-to-one**, starting from top of each list:
    - Highest Driver → Highest Vehicle
    - 2nd Highest Driver → 2nd Highest Vehicle
    - … and so on

If there are **more vehicles than drivers**:

- Each remaining vehicle is assigned an **Unrated Driver (URD)** using the following default values:
    - **Driver Class**: URD
    - **Points**: 0
    - **License Type**: Texas DL

These default driver values are used to calculate the Driver Factor for any unassigned vehicle.

## **5 — Vehicle Mileage Ratio**

Used to adjust premium based on how much a vehicle is driven relative to its expected mileage for its age. This factor is dynamically calculated based on annual mileage and applied to rating lines such as BI, PD, OTC (Comprehensive), and COLL.

### **5.1 — Calculation Process**

1. **Determine the Average Mileage Base**
    - Lookup the vehicle’s age (in whole years) from the **“Vehicle Age → Average Annual Mileage Base”** table.
    - Example: A 3-year-old vehicle has an average mileage base of **15,481**.
2. **Calculate Mileage Ratio**
    
    ```
    Mileage Ratio = Actual Annual Mileage / Average Annual Mileage Base
    ```
    
3. **Round the Result**
    - Round the calculated mileage ratio to **two decimal places**.
4. **Determine the Rating Factor**
    - Use the rounded ratio to **lookup the rating factor** from the **Mileage Ratio Table**, specific to each line of coverage.
    - Example: A mileage ratio of 0.28 yields a factor of **0.748** for BI, PD, OTC, and COLL.

### **5.2 — Table Logic**

Vehicle age and associated average mileage base. 

| **Vehicle Age
`(editable)`** | **Average Mileage Base
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- |
| 1 | 16,570 | **`Select from program term options`** | On |
| 2 | 16,470 | **`Select from program term options`** | On |
| 3 | 15,481 | **`Select from program term options`** | On |
| ... | ... | ... | … |
| 49+ | 6,189 | **`Select from program term options`** | On |
| `Add/delete supported vehicle age` |  |  |  |

Mileage Ratio.

| **Mileage Ratio
`(editable)`** | **Round Factor By
`(editable)`** | **BI
`(editable)`** | **PD
`(editable)`** | **OTC
`(editable)`** | **COLL
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.00 | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 0.01 | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| ... | … | ... | ... | ... | ... |  | … |
| 0.43 | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete mileage ratio` |  |  |  |  |  |  |  |

### **5.3 — Validation Rules**

- The **rounded ratio must exist in the mileage ratio table** to proceed with quoting (or fallback logic applied).
- The factor must be applied **separately per coverage line**, as each may have its own value even for the same ratio.

## **6 — Branded Title & Severe Problem Reports**

Used to apply risk-based surcharges based on title brands or known severe problems with a vehicle. These reports originate from DCS (Data Collection Services) or similar data sources and directly influence the rating for all major lines of coverage.

### **6.1 — Evaluate DCS Fields**

The system checks for values in a specific set of DCS data fields, such as:

| **DCS Field
`(editable)`** | **Trigger Code
`(editable)`** | **Description
`(editable)`** | **Round Factor By
`(editable)`** | BI
**`(editable)`** | PD
**`(editable)`** | UMBI
**`(editable)`** | UMPD
**`(editable)`** | MED
**`(editable)`** | PIP
**`(editable)`** | COMP
**`(editable)`** | COLL
**`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** | **Is this a hard stop? (Yes/No)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DPSStolenFlag | Stolen | Indicates that the Texas Department of Public Safety has identified the vehicle as stolen | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On | No |
| FloodDamageFlag | Flood | Indicates that a salvage title or other title was previously issued for a motor vehicle which has been declared a total loss due to flood damage | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On | No |
| LemonLawFlag | Lemon | If flagged, indicates that the vehicle has been reacquired by the manufacturer in order to resolve Lemon Law complaints or warranty claims under the Manufacturer Buyback provisions | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On | No |
| BondedTitleCode | Bonded | Indicates that a title has been issued by Vehicle Title and Registration (VTR) Division from evidence that a bonded title has been requested | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On | No |
| ReconditionedCode | Reconditioned | Indicates that a salvage title or other title has previously been issued on a vehicle that has, at some time, been a vehicle with a history of a previously issued salvaged title | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On | No |
| ReconstructedFlag | Reconstructed | Indicates that some type of physical modification was made to the vehicle | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On | No |
| TitleRevokedFlag | Revoked | Indicates that a Texas title was revoked by Vehicle Title and Registration (VTR) | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On | No |
| JunkFlag | Junk | Indicates that this vehicle has (an) associated junk record(s) | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On | No |
| Exported | Exported | Indicates that the vehicle has been sold out of state in a condition that is classified "non-repairable." The vehicle may not be re-titled in Texas without a court order | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On | No |
| RegistrationInvalidFlag | Invalid | Indicates that the registration of the vehicle is invalid | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On | No |
| ObsoleteFlag  | Obsolete | If flagged, indicated that this vehicle title has been superseded by a newer title | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On | Yes |
| TitleHotCheckFlag  | Hot Title | Indicates the existence of a hot check for the title application of the vehicle | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On | Yes |
| GovernmentOwnedFlag  | Gov Owned | Indicates that the vehicle is owned by the U.S. government | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On | Yes |
| `Add/delete DCS Data Field` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

### **6.2 — Clean**

If nothing is marked/returned from DCS, then mark as `clean.`

| **Trigger Code
`(editable)`** | **Description
`(editable)`** | **Round Factor By
`(editable)`** | BI
**`(editable)`** | PD
**`(editable)`** | UMBI
**`(editable)`** | UMPD
**`(editable)`** | MED
**`(editable)`** | PIP
**`(editable)`** | COMP
**`(editable)`** | COLL
**`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Clean | Indicates that the vehicle has no problems. | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |

### **6.3 — Assign Rating Factor**

For each coverage line, the matched group entry determines the applicable **rating factor**.

For example:

- A vehicle flagged as **Exported** will receive a **1.15** factor on BI, PD, UMBI, etc., and **1.25** on COMP and COLL.

### **6.4 — Rating Logic**

The system follows a strict rating logic in the order below:

1. **Hard Stops**
    - If any tag is configured as a hard stop, the quote or bind action is blocked and the user is notified.
    - No rating is performed.
2. **Severe Problems**
    - If no hard stop is present, but one or more tags are marked as severe, the system applies the **highest applicable factor** from the set of severe tags per coverage line.
3. **Standard Rating**
    - If no severe tags are found, the system proceeds with rating based on the **clean factors**.

## **7 — Vehicle Length of Ownership**

Used to adjust premium based on how long the insured has owned the vehicle. Longer ownership periods are typically associated with more stable and lower-risk behavior, while recently acquired vehicles carry more uncertainty and thus higher risk.

### **7.1 — Determine Ownership Scenario**

The system determines how ownership length is calculated based on transaction type:

| **Transaction Type** | **Ownership Source** |
| --- | --- |
| New Business | Use **`DCS`** to determine original ownership date. We receive an exact length of ownership and then our system determines which range it falls into. |
| Endorsement | For added vehicles, default to **“0 to 30 Days.”** |
| Renewal | Age the ownership from **original inception date.** |

### **7.2 — Calculate Ownership Duration**

- Based on the determined ownership start date, calculate total number of **days owned**.
- Convert the number of days into one of the **predefined ownership bands**.

### **7.3 — Lookup and Apply Rating Factor**

- Each band is mapped to a specific **rating factor per line of coverage** (BI, PD, OTC, COLL).
- The matching factor is applied during premium calculation.

| Length of Ownership (Min)
**`(editable)`** | Length of Ownership (Max)
**`(editable)`** | **Interval
`Dropdown; Days, Months, Years`** | **Round Factor By
`(editable)`** | **BI
`(editable)`** | **PD
`(editable)`** | **OTC
`(editable)`** | **COLL
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 30 | Days | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 31 | 60 | Days | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 60 | 183 | Days | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 184 | 365 | Days | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 1 | 2 | Years | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 2 | 3 | Years | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 3 | 4 | Years | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 4 | 5 | Years | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 5 | 6 | Years | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 6 | 7 | Years | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 7 | 8 | Years | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 8 | 9+ | Years | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete ownership duration` |  |  |  |  |  |  |  |  |  |

## **8 — Vehicle Model Year**

Used to adjust premiums based on the model year of the vehicle. Newer vehicles typically have higher repair and replacement costs, especially for physical damage coverages, while older vehicles may carry different levels of risk depending on age and safety features.

### **8.1 — Identify Model Year**

- Model Year is collected directly from the vehicle record (usually via VIN decode or manual input).
- If **Model Year > Current Year**, default to **Current Year +** designation (e.g., `2023+`).
- If vehicle is **1989 or older**, map to **"1989 and older"**.
- If the vehicle is **non-owned** (e.g., Non-Owner policy), assign to **"Non-owner"** category.

### **8.2 — Match to Factor Table**

| **Model Year
`(editable)`** | **Round Factor By
`(editable)`** | **BI
`(editable)`** | **PD
`(editable)`** | **COMP
`(editable)`** | **COLL
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2023+ | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 2022 | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 2021 | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| ... | … | ... | ... | ... | ... | … | On |
| 2014 | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 2012 | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| ... |  | ... | ... | ... | ... |  | On |
| 2003 and older | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 1989 and older | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Non-owner | 2 | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete model year` |  |  |  |  |  | **`Select from program term options`** |  |

### **8.3 — Other Behaviour Notes**

- Factor progression is steepest in physical damage (COMP & COLL), where newer vehicles increase costs significantly.
- Vehicles with **missing or invalid model year data** should not be quoted (Model Year must fall between 1989 and the current year + 1.)
- If the model year is beyond the current calendar year (e.g., entered as 2026 during 2025), the system should cap at **"2023+"** or throw a validation error.

## **9 — Physical Damage Symbol Factors**

Symbol factors are used to adjust premiums for physical damage coverages based on a vehicle’s **collision and comprehensive risk rating**. These symbols are derived from external data providers (such as Verisk's VINMASTER) and are mapped to pre-defined rating factors within the program.

### **9.1 — Retrieve Vehicle Symbol**

- For each vehicle, a **physical damage symbol** is obtained using a VIN decode **(which includes information pertaining to make and model)** via third-party services (e.g., Verisk VINMASTER).
- Symbols range from **1 to 75+** depending on the provider.
- There are **different symbol tables** depending on **model year grouping** (2010 & prior vs. 2011 & over).

### **9.2 —** Determine Model Year Band

- Check the vehicle’s model year:
    - If **2010 or earlier**, use the **“2010 & Prior”** column.
    - If **2011 or newer**, use the **“2011 & Over”** column.
- Match the retrieved symbol to the correct row for that band.

### **9.3 — Lookup Factor by Coverage**

- Use the row to apply corresponding rating factors for:
    - **COMP** (Comprehensive)
    - **COLL** (Collision)
    - **UMPD** (Uninsured Motorist Property Damage)

`Note`  Manual symbol overrides should be restricted, only factors are editable.

| **2010 & PRIOR
`Pulled from Verisk's VINMASTER integration`** | **2011 & OVER
`Pulled from Verisk's VINMASTER integration`** | **Round Factor By
`(editable)`** | **COMP
`(editable)`** | **COLL
`(editable)`** | **UMPD
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
|  | 2 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
| 2 | 3 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
| 3 | 4 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
| 4 | 5 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
| 5 | 6 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
|  | 7 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
| 6 | 8 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
| 7 | 10 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
| 8 | 11 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
| 12 | 13 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
|  | 14 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
| 11 | 15 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
|  | 16 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
| 12 | 17 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
|  | 18 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
| 13 | 19 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
|  | 20 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
| 14 | 21 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
|  | 22 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
|  | 23 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
|  | 24 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
| 15 | 25 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
|  | 26 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
|  | 27 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
| 16 | 28 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
|  | 29 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
|  | 30 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
| 17 | 31 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
|  | 32 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
|  | 33 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
|  | 34 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
| 18 | 35 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
|  | 36 | 2 | #.## | #.## | #.## | **`Select from program term options`** | On |
| … | … | … | … | … | … |  | … |

## **10 — Vehicle Usage**

Vehicle usage describes the primary purpose the vehicle serves (e.g., personal, commuting, business, etc.). Different usage types carry different risk levels and therefore apply distinct rating factors across all major lines of coverage.

### **10.1 — Select Usage Type**

The user selects the appropriate usage type from the following options:

- **Pleasure**
- **Commute ≤ 5 mi one way**
- **Commute > 5 mi one way**
- **Business**
- **Non-Owner**
- **Farm**

### **10.2 — Apply Usage-Based Rating Factor**

Each usage type is mapped to specific factors by line of coverage. These factors are applied directly to the base rate for each relevant coverage.

| **Usage Type** | **Round Factor By
`(editable)`** | **BI** | **PD** | **UMBI** | **UMPD** | **MED** | **PIP** | **COMP** | **COLL** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pleasure | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Commute ≤ 5 mi one way | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Commute > 5 mi one way | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Business | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Farm | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Non-Owner | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete usage type` |  |  |  |  |  |  |  |  |  |  |  |

## **11 — Vehicle Lienholder**

This factor accounts for the presence or absence of a **lienholder** on a vehicle. Vehicles with a lienholder (i.e., financed) generally follow stricter coverage requirements and have more predictable risk, while liability-only vehicles may reflect different usage or financial stability.

### **11.1 — Key Definitions**

- **Lienholder = Yes**: The vehicle has an active lienholder (i.e., is financed or leased), and the policyholder is required to carry full physical damage coverage (both Comprehensive and Collision) to protect the lender’s interest.
- **Lienholder = No**: The vehicle is not financed, so there is no lienholder, but the customer has elected to carry full coverage anyway (i.e., COMP and COLL are selected voluntarily).
- **Lienholder = LO**: The vehicle is insured for liability only — no Comprehensive or Collision coverage is selected, regardless of lienholder status.
- **Non-Owner**: Applies to non-owner policies with no listed vehicles

`Note:` Once a lienholder is removed, the previous lienholder-based factor is retained. This prevents pricing manipulation or unintended premium swings.

### **11.2 — Determine Lienholder Status**

- Check if the vehicle has an active lienholder.
- Confirm whether **COMP/COLL** coverages are included.
- Use this to assign `Yes`, `No`, or `LO` status.

### **11.3 — Match Factor Row**

| **Lienholder
`(editable)`** | **Round Factor By
`(editable)`** | **BI
`(editable)`** | **PD
`(editable)`** | **UMBI
`(editable)`** | **UMPD
`(editable)`** | **MED
`(editable)`** | **PIP
`(editable)`** | **OTC
`(editable)`** | **COLL
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Yes | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| No | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| LO | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Non-Owner | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete lienholder type` |  |  |  |  |  |  |  |  |  |  |  |

## **12 — Vehicle Count**

This factor accounts for the number of vehicles tied to a policy.

| **Vehicle Count
`(editable)`**
 | **Round Factor By
`(editable)`** | **BI
`(editable)`** | **PD
`(editable)`** | **UMBI
`(editable)`** | **UMPD
`(editable)`** | **MED
`(editable)`** | **PIP
`(editable)`** | **OTC
`(editable)`** | **COLL
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 2 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 3 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 4+ | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete vehicle count` |  |  |  |  |  |  |  |  |  |  |  |

## **13 — Vehicle Deductible**

The selected deductible level for **Comprehensive (COMP)** and **Collision (COLL)** coverage directly impacts the premium by applying a multiplier. Higher deductibles reduce risk for the insurer and are rewarded with a lower premium.

### **13.1 — Key Rules**

- Applies only to **COMP** and **COLL**
- **Any combination** of deductibles is permitted (e.g., COMP = $500, COLL = $750)

### **13.2 —** Deductible Factor Table

| **Deductible ($)
`(editable)`** | **Round Factor By
`(editable)`** | **COMP
`(editable)`** | **COLL
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- |
| 250 | 2 | #.## | #.## | **`Select from program term options`** | On |
| 500 | 2 | #.## | #.## | **`Select from program term options`** | On |
| 750 | 2 | #.## | #.## | **`Select from program term options`** | On |
| 1000 | 2 | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete deductible option` |  |  |  |  |  |

# Driver Attributes

## **14 — Gender**

| **Label
`(editable)`** | **Description
`(editable)`** | **Round Factor By
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
| Male | Used in combination with age and marital status to determine risk banding and assign driver class code | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Female | Used in combination with age and marital status to determine risk banding and assign driver class code | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete gender option` |  |  |  |  |  |  |  |  |  |  |  |  |

## **15 — Marital Status**

| **Label
`(editable)`** | **Description
`(editable)`** | **Round Factor By
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
| Single | Must be paired logically with other driver on policy if marked married | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Married | Requires at least one other driver on policy marked as married (matched pair) | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete marital status option` |  |  |  |  |  |  |  |  |  |  |  |  |

## **16 — Age**

| **Value
`(editable)`** | **Description
`(editable)`** | **Round Factor By
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
| 15 | Youngest supported driver class assignment | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 99 | Oldest supported driver class assignment | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| None currently excluded. 
`Add/delete exclusion` | All integer values 15 through 99 are currently accepted |  |  |  |  |  |  |  |  |  | **`Select from program term options`** | Off

`Defaults to “On” if an exclusion is added` |

## **17 — License**

### **17.1 —**  License Type

| **Description
`(editable)`** | **Round Factor By
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
| [State] DL | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| [State] ID (Non-DL) | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| U.S. DL  | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Foreign / International DL | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Matricula | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Passport | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| No Driver's License | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete license type` |  |  |  |  |  |  |  |  |  |  |  |

### **17.2 —**  Selection Logic

- If `licenseType ∈ {Foreign / International License, Matricula, Passport}`
    
    **→ Name Supported Countries**
    
    Multi-select dropdown with searchable country list (defaults to ISO country codes). **This determines which international licenses are supported.**  
    
    | **Country Code** | **Country Name** | **Applied for the Following Terms
    `Multi-select`** | **Supported (On/Off)
    `(editable)`** |
    | --- | --- | --- | --- |
    | MX | Mexico | **`Select from program term options`** | On |
    | CA | Canada | **`Select from program term options`** | On |
    | GB | United Kingdom | **`Select from program term options`** | On |
    | IN | India | **`Select from program term options`** | On |
    | PH | Philippines | **`Select from program term options`** | On |
    | CN | China | **`Select from program term options`** | On |
    | NG | Nigeria | **`Select from program term options`** | On |
    | ... | (Remaining ISO list) |  | On |
- If `licenseType = [State] DL, [State] ID (Non-DL)`
    
    **→ Name Supported States**
    
    Multi-select state dropdown (U.S. only). Users can deselect specific states.
    
    | **State Code** | **State Name** | **Applied for the Following Terms
    `Multi-select`** | **Supported (On/Off)
    `(editable)`** |
    | --- | --- | --- | --- |
    | TX | Texas | **`Select from program term options`** | On |
    | CA | California | **`Select from program term options`** | On |
    | FL | Florida | **`Select from program term options`** | On |
    | NY | New York | **`Select from program term options`** | On |
    | IL | Illinois | **`Select from program term options`** | On |
    | GA | Georgia | **`Select from program term options`** | On |
    | AZ | Arizona | **`Select from program term options`** | On |
    | ... | (Remaining states) |  | On |
- If `licenseType = U.S. DL`
    
    → **State selection optional or inferred** from license record, but no additional prompt required
    

### **17.3 —**  Behaviour Notes

- At **Renewal**, the system will run a DSC (Driver Status Check) to detect if an **appropriate state license, based on the respective state chosen for the program,** has been issued, and adjust the rate accordingly.

## **18 — Driver Count**

This factor accounts for the number of drivers tied to a policy

| **Driver Count
`(editable)`**
 | **Round Factor By
`(editable)`** | **BI
`(editable)`** | **PD
`(editable)`** | **UMBI
`(editable)`** | **UMPD
`(editable)`** | **MED
`(editable)`** | **PIP
`(editable)`** | **OTC
`(editable)`** | **COLL
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 2 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 3 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 4+ | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete driver count` |  |  |  |  |  |  |  |  |  |  |  |

## **19 — Employment**

Captures the insured's current employment status. 

| **Label
`(editable)`**
 | **Description
`(editable)`** | **Round Factor By
`(editable)`** | **BI
`(editable)`** | **PD
`(editable)`** | **UMBI
`(editable)`** | **UMPD
`(editable)`** | **MED
`(editable)`** | **PIP
`(editable)`** | **OTC
`(editable)`** | **COLL
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Employed | Actively working for an employer (full-time or part-time). | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Self Employed | Operates their own business or works freelance/independently. | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Retired | No longer employed and receiving retirement income. | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Student | Currently enrolled in school or college full-time or part-time. | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Disabled | Unable to work due to a medical or physical condition. | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Military | Active-duty service member or reservist. | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Homemaker | Not employed outside the home, but managing household responsibilities. | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Unemployed | Not currently employed and not retired. | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete employment option` |  |  |  |  |  |  |  |  |  |  |  |  |

## **20 — Occupation**

Defines acceptable occupations for drivers and insured individuals. All occupation data should be mapped to a standard list using NAICS codes (North American Industry Classification System) to ensure consistency across programs and integrations.

Only asked if `Employed` or `Self-Employed`

| **Label
`(editable)`**
 | **Category
`(editable)`** | **Round Factor By
`(editable)`** | **BI
`(editable)`** | **PD
`(editable)`** | **UMBI
`(editable)`** | **UMPD
`(editable)`** | **MED
`(editable)`** | **PIP
`(editable)`** | **OTC
`(editable)`** | **COLL
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Teacher | Education | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Nurse | Healthcare | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Exotic Dancer | Entertainment | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Bail Bondsman | Legal / Security | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| General Contractor | Construction | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Stunt Performer / Actor | Entertainment | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Unemployed | None | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| ... | ... | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete occupation option` |  |  |  |  |  |  |  |  |  |  |  |  |