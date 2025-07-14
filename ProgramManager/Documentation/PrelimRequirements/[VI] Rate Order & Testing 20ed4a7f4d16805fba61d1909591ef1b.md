# [VI] Rate Order & Testing

Rate Order determines the exact sequence in which rating factors are applied to the base rate for each line of coverage. Since each factor is multiplicative, changing the order will change the final premium (especially when multiple >1.0 factors are involved).

## 1 — Approach for Managing Rate Order

### **1.1 — Detailed Factor Order Builder (Enhanced Drag & Drop UI)**

Each program should allow the user to define a single, master rate order that applies consistently across all policy terms. **The interface should display only variables that are currently "On" with:**

- **Attribute** (e.g., "Payment Options") (see [[I] Program Definitions](https://www.notion.so/I-Program-Definitions-20ed4a7f4d1680649025dc06a669cc49?pvs=21) for more information)
- **Variable** (e.g., "Installment")
- **Coverage Lines Applied** (e.g., "BI, PD, COLL")
- **Factor Range** (e.g., "1.00 - 1.08")

### **1.2 — Enhanced UI Interaction Example**

Using the Payment Options example, users see a detailed drag-and-drop interface showing only active variables:

```
[Base Rate]
→ [Payment Options - Installment] - Applied to: BI, PD, COLL - Range: 0.90-1.15
→ [Payment Options - PIF] - Applied to: BI, PD, COLL - Range: 0.90-1.15
→ [Payment Options - EFT] - Applied to: BI, PD, COLL - Range: 0.90-1.15
→ ...
→ ...
→ ...
```

### **1.3 — Rate Order Consistency**

⚠️ **Important**: The rate order remains **identical across all policy terms** (6-month, 12-month, etc.). This ensures consistent risk evaluation and prevents rating anomalies between different term lengths.

⚠️ **Critical**: Fees must always come last in the calculation order, after all multiplicative factors have been applied.

The system uses this exact sequence for all calculations:

```

Premium = (((((Base Rate × Variable₁) × Variable₂) × Variable₃) × Variable₄) × Variable₅) × Variable₆...

```

## **2 —** Scenario-Based Rate Testing

### **2.1 — Overview Panel**

Offer three pre-configured example profiles:

| **Scenario** | **Label** | **Description** | **Complexity** |
| --- | --- | --- | --- |
| SCENARIO_1 | Simple Policy | Single vehicle, single driver, clean record, no discounts, 6 month term | Low |
| SCENARIO_2 | Typical Policy | Two drivers, prior violations, some discounts, 6 month term | Medium |
| SCENARIO_3 | Complex Policy | Multi-vehicle household, diverse drivers, complex coverage mix, 12 month term | High |

Each scenario includes a **“View Inputs”** button and a **“Run Quote”** button.

### **2.2 — Clicking “View Inputs”**

Opens a read-only side panel or modal with the full profile details used to run that test.

**Example: Typical Policy (Medium)**

- **Driver 1**: Age 32, Full License, 2 points, Married
- **Driver 2**: Age 29, Permit, Clean Record
- **Vehicle 1**: 2019 Honda Civic, Commute > 5 mi, Owned 3 years
- **Policy**: BI, PD, UMBI, COMP, COLL selected
- **Discounts**: Paperless, EFT
- **Prior Coverage**: 12+ months
- …

### **2.3 — Clicking “Run Quote”**

- System pulls base rates + rating factors
- Applies them according to the defined **rate order**
- Returns a **line-by-line cost breakdown** for each coverage (similar to quote preview)

### **2.4 — Sample Calculation Log**

This is completed for each “scenario”.

| **Step** | **Description** | **Value Applied** | **Running Total** |
| --- | --- | --- | --- |
| 1 | **Base Rate** | $334.47 | $334.47 |
| 2 | Vehicle Usage Factor | × 1.10 | $367.92 |
| 3 | Vehicle Mileage Ratio Factor | × 1.04 | $382.63 |
| 4 | Driver Class Factor | × 1.00 | $382.63 |
| 5 | Driver Points Factor | × 1.05 | $401.76 |
| 6 | Policy Term Factor | × 0.98 | $393.72 |
| 7 | Payment Plan Factor | × 0.97 | $381.91 |
| 8 | Paperless Discount | × 0.95 | $362.81 |
| 9 | **Rounded Total (3 decimals)** | — | $362.810 |
| 10 | **Final Rounded Premium** | — | **$363** |

### **2.5 — Sample Output Panel**

This is completed for each “scenario”.

<aside>
<img src="https://www.notion.so/icons/photo-landscape_gray.svg" alt="https://www.notion.so/icons/photo-landscape_gray.svg" width="40px" />

![image.png](%5BVI%5D%20Rate%20Order%20&%20Testing%2020ed4a7f4d16805fba61d1909591ef1b/image.png)

</aside>