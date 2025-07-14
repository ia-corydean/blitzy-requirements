# [V] Rating — Factor Grouping

# Factor Groups

## **1 — (Factor Grouping #1) Lienholder + Vehicle Count**

This factor grouping accounts for the presence or absence of a **lienholder** on a vehicle, in combination with the **number of vehicles** on the policy. 

| **Lienholder
`Pulled from existing Lienholder Attribute`

`Options are multiselect`** | **Vehicle Count
`Pulled from existing Vehicle Count Attribute`

`Options are multiselect`** | **Round Factor By
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
| Yes | 1 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| No | 1 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| LO | 1 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Yes | 2 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| No | 2 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| LO | 2 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Yes | 3 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| No | 3 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| LO | 3 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Yes | 4+ | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| No | 4+ | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| LO | 4+ | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Non-Owner | — | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete combination factor` |  |  |  |  |  |  |  |  |  |  |  |  |

## **2 — (Factor Grouping #2) Policy Core Matrix**

This factor grouping is a combination of **`Number of Months Prior Coverage`, `Prior Insurance Verification Level`, `Is Insured a Homeowner?`, `Vehicle Count`**

| **Number of Months Prior Coverage
`Pulled from existing Number of Months Prior Coverage Attribute`

`Options are multiselect`** | **Prior Insurance Verification Level
`Pulled from existing Prior Insurance Verification Level Attribute`

`Options are multiselect`**
 | **Is Insured a Homeowner?
`Pulled from existing Is Insured a Homeowner? Attribute`

`Options are multiselect`** | **Vehicle Count
`Pulled from existing Vehicle Count Attribute`

`Options are multiselect`** | **Round Factor By
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
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0-6 Months | Prior Insurance (reported by the insured)
 | No | 1 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 6-11 Months | Transfer (validated by MGA or producer)
 | Yes | 1 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 12+ | Verified (confirmed via third-party integration or database check). | No | 1 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 0-6 Months | Prior Insurance (reported by the insured)
 | Yes | 1 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 6-11 Months | Transfer (validated by MGA or producer)
 | No | 1 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 12+ | Verified (confirmed via third-party integration or database check). | Yes | 1 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 0-6 Months | Prior Insurance (reported by the insured)
 | No | 1 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 6-11 Months | Transfer (validated by MGA or producer)
 | Yes | 1 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 12+ | Verified (confirmed via third-party integration or database check). | No | 2, 3, 4+ | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 0-6 Months | Prior Insurance (reported by the insured)
 | Yes | 2, 3, 4+ | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 6-11 Months | Transfer (validated by MGA or producer)
 | No | 2, 3, 4+ | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 12+ | Verified (confirmed via third-party integration or database check). | Yes | 2, 3, 4+ | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 0-6 Months | Prior Insurance (reported by the insured) | No | 2, 3, 4+ | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete combination factor` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

## **3 — (Factor Grouping #3) Driver Class**

Driver class factors are applied based on the **driver's age**, **gender**, and **marital status**. Each valid combination results in a unique driver class code, which maps to a set of rating factors used across all coverage lines.

### **3.1 — Driver Class Table**

| **Gender
`Pulled from existing Gender Attribute`

`Options are multiselect`** | **Marital Status
`Pulled from existing Martial Status Attribute`

`Options are multiselect`** | **Age
`Pulled from existing Age Attribute`

`Options are multiselect`** | **Round Factor By
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
| Female | Married | 35 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Female | Single | 35 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Male | Married | 35 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| Male | Single | 35 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| — | — | — | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete combination factor` |  |  |  |  |  |  |  |  |  |  |  |  |  |

### **3.2 — Unrated Driver**

→ `URD` (Unrated Driver) with a flat factor.

| **Label** | **Description** | **Round Factor By
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
| Vehicle with No Assignment | Used when there are more vehicles than drivers on the policy | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |

## **4 — (Factor Grouping #4) Policy Driver to Vehicle**

Group factor applied based on the **driver count and vehicle count**. 

| **Driver Count
`Pulled from existing Driver Count Attribute`

`Options are multiselect`** | **Vehicle Count
`Pulled from existing Vehicle Count Attribute`

`Options are multiselect`** | **Round Factor By
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
| 1 | 1 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 2 | 1 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 3 | 1 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 4+ | 1 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 1 | 2 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 2 | 2 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 3 | 2 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 4+ | 2 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 1 | 3 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 2 | 3 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 3 | 3 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 4+ | 3 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 1 | 4+ | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 2 | 4+ | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 3 | 4+ | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 4+ | 4+ | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete combination factor` |  |  |  |  |  |  |  |  |  |  |  |  |

## **5 — (Factor Grouping #5) Renewal Factor**

This factor rewards long-term policyholders by reducing premiums at each renewal milestone based on:

- **Renewal Age** (length of time since policy inception)
- **Number of Vehicles on the Policy**
- The system must calculate the time since policy inception, not just prior term end date.

| **Value**
**`(editable)`** | **Interval
`Dropdown; Days, Months, Years`** | **Vehicles
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
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | Months | 1 | 3 | #.### | #.### | #.### | #.### | #.### | #.### | #.### | #.### | **`Select from program term options`** | On |
| 6 | Months | 1 | 3 | #.### | #.### | #.### | #.### | #.### | #.### | #.### | #.### | **`Select from program term options`** | On |
| ... | Months | ... | … | ... | ... | ... | ... | ... | ... | ... | ... | … | On |
| 30+ | Months | 3+ | 3 | #.### | #.### | #.### | #.### | #.### | #.### | #.### | #.### | **`Select from program term options`** | On |
| `Add/delete renewal factor` |  |  |  |  |  |  |  |  |  |  |  |  |  |

## **6 — (Factor Grouping #X) Add Custom Factor Grouping**

**Step 1: Select Attributes**
Choose two or more previously defined attributes. These should be attributes where the combination creates meaningful risk differentiation beyond what individual factors would capture.

**Step 2: Define Attribute Combinations**
Create rows for each relevant combination of attribute values. In the example shown, the Lienholder and Vehicle Count attributes create combinations like:

- Lienholder: Yes + Vehicle Count: 1
- Lienholder: No + Vehicle Count: 2
- Lienholder: LO + Vehicle Count: 4+

**Step 3: Assign Factors**
For each combination row, assign rating factors across all applicable coverage lines (BI, PD, UMBI, UMPD, MED, PIP, OTC, COLL). The factors reflect how that specific combination of attributes affects risk for each coverage type.

**Step 4: Configure Application Rules**
Set whether the factor grouping applies to specific policy terms and define any supporting logic for how the system should handle the combinations during rating calculations.

Factor groupings support advanced modeling where **individual attributes alone are not sufficient** to capture the desired risk logic, allowing insurers to create more precise and actuarially sound rating structures.