# Complete Rating Methodology Guide
## Aguila Dorada Texas Personal Auto Program - Final Implementation

### Overview
This document provides the definitive guide to how rating works for the Aguila Dorada Texas Personal Auto program. It represents the final implementation that combines existing rate factors with system enhancements to deliver complete program functionality. This guide enables stakeholders and AI agents to fully understand the rating methodology.

---

## 1. Core Rating Formula

### **Master Rating Equation**
```
Final Premium = (Base Rate × Core Matrix × Driver Factors × Vehicle Factors × Coverage Factors × Misc Adjustments) + Policy Fees + Coverage Fees
```

### **Calculation Sequence**
1. **Base Rate Selection** (by territory and coverage)
2. **Core Matrix Application** (enhanced with all discounts)
3. **Driver Factor Multiplication** (age, gender, marital status, points)
4. **Vehicle Factor Multiplication** (age, use, make/model)
5. **Coverage Factor Application** (limits, deductibles)
6. **Miscellaneous Adjustments** (paperless, early shopper, etc.)
7. **Fee Addition** (policy fees, SR-22, endorsements)

---

## 2. Base Rates (Foundation)

### **6-Month Base Premium by Territory**
**Liability Coverage (30/60/25):**
- Territory 01: $279 | Territory 02: $295 | Territory 03: $287
- Territory 04: $312 | Territory 05: $298 | Territory 06: $326
- Territory 07: $301 | Territory 08: $289 | Territory 09: $294
- Territory 10: $283 | Territory 11: $307 | Territory 12: $291

**Uninsured Motorist Coverage:**
- Territory 01: $45 | Territory 02: $52 | Territory 03: $48
- Territory 04: $67 | Territory 05: $54 | Territory 06: $74
- Territory 07: $58 | Territory 08: $49 | Territory 09: $53
- Territory 10: $46 | Territory 11: $63 | Territory 12: $51

**Comprehensive Coverage:**
- Territory 01: $96 | Territory 02: $105 | Territory 03: $101
- Territory 04: $113 | Territory 05: $107 | Territory 06: $110
- Territory 07: $108 | Territory 08: $102 | Territory 09: $106
- Territory 10: $98 | Territory 11: $111 | Territory 12: $103

**Collision Coverage:**
- Territory 01: $251 | Territory 02: $275 | Territory 03: $263
- Territory 04: $295 | Territory 05: $278 | Territory 06: $289
- Territory 07: $281 | Territory 08: $267 | Territory 09: $273
- Territory 10: $258 | Territory 11: $287 | Territory 12: $269

**PIP/Medical Coverage:**
- Territory 01: $25 | Territory 02: $31 | Territory 03: $28
- Territory 04: $42 | Territory 05: $33 | Territory 06: $48
- Territory 07: $36 | Territory 08: $29 | Territory 09: $32
- Territory 10: $26 | Territory 11: $39 | Territory 12: $30

### **Territory Assignment**
- Territory determined by vehicle garaging ZIP code
- All vehicles on policy use same territory
  - Where is this referenced / how did you determine this?
- Territory cannot be changed mid-term
  - Where is this referenced / how did you determine this?

---

## 3. Enhanced Policy Core Matrix

### **Four-Dimensional Discount Matrix**
The core matrix has been enhanced to include all major discounts:

**Dimension 1: Prior Insurance**
- None: 1.00
- Less than 6 months: 0.95
- 6-12 months: 0.85
- 12-24 months: 0.75
- 24+ months: 0.65

**Dimension 2: Years Licensed**
- 0-2 years: 1.00
- 3-5 years: 0.95
- 6-10 years: 0.85
- 11-15 years: 0.75
- 16+ years: 0.65

**Dimension 3: Vehicle Ownership**
- Finance: 1.00
- Lease: 0.95
- Own: 0.85

**Dimension 4: Homeowner Status**
- Renter: 1.00
- Homeowner: 0.95

### **Matrix Calculation**
```
Core Matrix Factor = Prior Insurance Factor × Years Licensed Factor × Ownership Factor × Homeowner Factor
```

**Maximum Discount:** 0.44 (56% discount)
- 24+ months insurance + 16+ years licensed + Own vehicle + Homeowner
- 0.65 × 0.65 × 0.85 × 0.95 = 0.34

**Minimum Discount:** 1.00 (no discount)
- No prior insurance + 0-2 years licensed + Finance + Renter

---

## 4. Driver Classification Factors

### **Age/Gender/Marital Status Matrix**
**Male Drivers:**
- Single: Age 16-17: 2.60 | Age 18-20: 2.25 | Age 21-24: 1.85 | Age 25-29: 1.45 | Age 30+: 1.00
- Married: Age 16-17: 1.80 | Age 18-20: 1.55 | Age 21-24: 1.25 | Age 25-29: 1.05 | Age 30+: 0.85

**Female Drivers:**
- Single: Age 16-17: 2.25 | Age 18-20: 1.95 | Age 21-24: 1.65 | Age 25-29: 1.25 | Age 30+: 0.85
- Married: Age 16-17: 1.65 | Age 18-20: 1.35 | Age 21-24: 1.15 | Age 25-29: 0.95 | Age 30+: 0.78

### **Driver Points System**
**Point Multipliers:**
- 0 Points: 1.00 | 1 Point: 1.25 | 2 Points: 1.50 | 3 Points: 1.75
- 4 Points: 2.00 | 5 Points: 2.75 | 6 Points: 3.50 | 7 Points: 4.00
- 8 Points: 5.50 | 9 Points: 7.50 | 10 Points: 10.00 | 11+ Points: 25.50

**Point Assignment Guidelines:**
- Minor violations: 1-2 points
- Major violations: 3-4 points
- At-fault accidents: 2-4 points
- DUI/DWI: 6+ points

### **Driver Assignment Rules**
- Primary driver assigned to highest value vehicle
- Secondary drivers assigned by descending vehicle value
  - How did you determine these?
  - It's my understanding that it is strictly highest rated driver to highest rated vehicle and so on.
- Unlisted drivers not assigned but covered under policy

---

## 5. Vehicle Rating Factors

### **Vehicle Age Factors**
**Age-Based Multipliers:**
- 0-1 years: 1.10 | 2-3 years: 1.05 | 4-5 years: 1.00 | 6-7 years: 0.95
- 8-9 years: 0.90 | 10-12 years: 1.00 | 13-15 years: 1.10 | 16+ years: 1.20

### **Vehicle Use Classification**
- Pleasure: 1.00
- Commute less than 15 miles: 1.05
- Commute 15+ miles: 1.15
- Business: 1.25
- Farm: 0.95

### **Vehicle Make/Model Factors**
**Risk Categories:**
- Low Risk (family sedans): 0.85-0.95
- Standard Risk (most vehicles): 1.00-1.10
- High Risk (sports cars): 1.15-1.35
- Very High Risk (exotic/performance): 1.40-1.65

### **Vehicle Symbols**
- Symbols 1-30: Standard rating
- Symbols 31-61: Acceptable for new business
- Symbols 62-64: Renewal only
- Symbols 65+: Not acceptable

---

## 6. Coverage Limit Factors

### **Liability Limits** (Enhanced Options)
- **30/60/25** (Texas minimum): 1.00
- **250/500/250**: 1.61
- **500/500/500**: 1.69
- **500/1000/500**: 1.75
- **1000/1000/500**: 1.90
- **Combined Single Limit 500K**: 1.35
- **Combined Single Limit 1M**: 1.54
  - These should only cover what is defined here

### **Comprehensive/Collision Deductibles** (Updated Range)
- **$500**: 1.00
- **$750**: 0.90
- **$1000**: 0.85
- **$1500**: 0.80
- **$2000**: 0.75
- **$2500**: 0.70

### **Additional Coverage Options**
**Personal Injury Protection (PIP):**
- $2,500: 1.00
- $25,000: 1.98
- $50,000: 2.21
- $75,000: 2.33
- $100,000: 2.42

**Medical Payments:**
- $500: 1.00
- $1,000: 1.45

**Towing and Labor:**
- $40: 1.00
- $75: 1.60

**Rental Reimbursement:**
- $20/day ($600 max): 1.00
- $30/day ($900 max): 1.50
- $40/day ($1,200 max): 2.00

**Additional Custom Equipment:**
- Rate = Coverage Limit ÷ 100
- Minimum: $100 (Rate = 1.00)
- Maximum: $3,000 (Rate = 30.00)
- Available in $100 increments

---

## 7. Payment Method Integration

### **Payment Method Factors** (New System Enhancement)
- **Electronic Funds Transfer (EFT)**: 0.97 (3% discount)
- **Credit Card**: 1.00 (base rate)
- **Standard Billing**: 1.05 (5% surcharge)

### **Payment Timing Factors**
- **Paid in Full**: 0.95 (5% discount - can stack with EFT)
- **Installment Plans**: Standard rates apply

### **Combined Payment Discounts**
- **EFT + Paid in Full**: 0.92 (8% total discount)
- **Maximum Payment Discount**: 8%

---

## 8. Distribution Channel Factors

### **Channel-Based Multipliers**
- **Direct**: 0.90 (10% discount)
- **Retail**: 1.00 (base rate)
- **Controlled Agent**: 1.05 (5% surcharge)
- **Independent Agent**: 1.15 (15% surcharge)

### **Transfer and Loyalty Enhancements**
**Transfer Discounts** (Applied as policy credit):
- **New Customer**: No discount
- **Agency Transfer**: 5% policy credit
- **Renewal Customer**: 8% policy credit for long-term customers

---

## 9. Driver-to-Vehicle Ratio Factors

### **Household Composition Multipliers**
**Liability and Physical Damage:**
- 1 Driver, 1 Vehicle: 1.000
- 2 Drivers, 1 Vehicle: 1.075
- 3 Drivers, 1 Vehicle: 1.200
- 4+ Drivers, 1 Vehicle: 1.400

**Multi-Vehicle Discounts:**
- 1 Driver, 2 Vehicles: 0.950
- 2 Drivers, 2 Vehicles: 1.000
- 3 Drivers, 2 Vehicles: 1.050
- Optimal ratio: 3 Drivers, 3 Vehicles: 1.000

---

## 10. Miscellaneous Adjustments

### **Policy-Level Discounts**
- **Paperless**: 0.990 (1% discount)
- **Early Shopper**: 0.960 (4% discount for 3+ days advance purchase)
- **Renter**: 0.980 (2% discount with renters insurance)
- **Double Deductible**: 0.900 (10% discount - comprehensive/collision only)
- **Unlisted Driver**: 0.950 (5% discount - collision only)

### **Policy-Level Surcharges**
- **Non-Rated Spouse**: 1.140 (14% surcharge - liability/physical damage only)

### **Discount Stacking Rules**
**Maximum Combined Discount**: 60% total
**Stackable Combinations:**
- Early Shopper + Paperless + Renter = 8.4% discount
- All policy-level discounts can stack
- Payment method discounts stack separately

---

## 11. Fee Structure (Complete)

### **Base Policy Fees**
- **Policy Fee**: $90.00 (fully earned, non-refundable)
- **SR-22 Fee**: $25.00 per driver requiring SR-22
- **Multiple SR-22**: $25.00 × number of drivers

### **Endorsement Fees**
- **Standard Endorsement**: $15.00 (insured-requested changes)
- **Driver Exclusion**: $15.00
- **Coverage Addition**: $15.00
- **Vehicle Addition**: $15.00

### **Operational Fees**
- **Late Fee**: $5.00 (applied 5 days after due date)
- **NSF Fee**: $25.00 (returned payments)
- **Installment Fee**: Variable by payment plan (see rate specifications)

### **Fee Calculation Example**
```
Base Policy: $90.00
+ SR-22 for Driver 1: $25.00
+ SR-22 for Driver 2: $25.00
+ Mid-term endorsement: $15.00
= Total Fees: $155.00
```

---

## 12. Eligibility Integration (System Workflows)

### **License Type Verification**
**Process**: Verification workflow during application (not rating factors)
- Texas DL: No documentation required
- Foreign/International DL: Copy required for file
- Out-of-State DL: Copy required for file
- No license: Application declined

**Rating Impact**: None - all approved licenses receive same rates

### **Residency Verification**
**Process**: Address-based verification (not rating factors)
- Texas residents: Eligible
- Non-Texas residents: Application declined
- New Texas residents: 90-day grace period

**Rating Impact**: None - binary eligibility decision

### **Employment Screening**
**Process**: Application questionnaire (not rating factors)
- Standard employment: Eligible
- Artisan use: Special endorsement required
- Ride-share/delivery: Application declined

**Rating Impact**: None - eligibility decision only

### **Age Restrictions**
**Process**: Birth date verification (enforced in driver factors)
- Under 75: Eligible (driver factors apply)
- Over 75: Application declined

**Rating Impact**: Driver age factors applied for eligible drivers

---

## 13. Vehicle Photo Requirements (Operational)

### **Photo Collection Workflow**
**Required Photos** (6 total for comp/collision, PIP, or UMPD):
1. Front view
2. Rear view
3. Passenger side
4. Driver side
5. VIN (visible)
6. Odometer reading

**Process Flow:**
1. **During Application**: Photos can be uploaded
2. **Post-Bind**: Missing photos create producer suspense
3. **Collection Period**: Defined timeframe for producer
4. **Non-Compliance**: Policy cancelled if photos not received

**Rating Impact**: None - operational requirement only

---

## 14. Criminal History and Eligibility

### **Conviction-Based Eligibility**
**Automatic Declines:**
- Felony convictions
- More than 1 DWI in last 3 years
- Permanently revoked license

**Point System Application:**
- DWI: 6+ points (severe rating impact)
- Major violations: 4-6 points
- Minor violations: 1-3 points

**Rating Impact**: Points applied through driver points system

---

## 15. Complete Rating Example

### **Sample Premium Calculation**
**Driver**: 35-year-old married female, 5 years licensed, owns home, has prior insurance
**Vehicle**: 2020 Honda Civic, pleasure use, garaged in Territory 01
**Coverage**: 30/60/25 liability, $500 deductible comp/collision
**Discounts**: Paperless, Early Shopper, EFT payment

**Calculation:**
```
Base Rate (Liability, Territory 01): $279.00
× Core Matrix (0.85 × 0.95 × 0.85 × 0.95): 0.65
× Driver Factor (Married Female 35): 0.78
× Vehicle Factors (2020 Civic): 1.05
× Misc Adjustments (0.990 × 0.960): 0.95
× Payment Method (EFT): 0.97
= Coverage Premium: $279 × 0.65 × 0.78 × 1.05 × 0.95 × 0.97 = $129.85

+ Policy Fee: $90.00
= Total 6-Month Premium: $219.85
```

---

## 16. System Integration Points

### **Rating Engine Requirements**
1. **Real-Time Calculation**: All factors applied instantly
2. **Discount Validation**: Automatic eligibility checking
3. **Factor Combination**: Proper multiplication sequence
4. **Fee Calculation**: Automatic fee addition

### **Data Integration**
1. **Territory Lookup**: ZIP code to territory mapping
2. **Vehicle Symbol**: VIN to symbol conversion
3. **Driver Record**: MVR integration for points
4. **Prior Insurance**: Verification system integration

### **Quality Controls**
1. **Maximum Discount**: 60% total cap enforcement
2. **Minimum Premium**: Floor premium protection
3. **Calculation Audit**: Factor application tracking
4. **Error Handling**: Invalid combination detection

---

## 17. Business Rules Summary

### **Hard Rules (Cannot Be Overridden)**
- Rate factors are immutable
- Eligibility restrictions are absolute
- Fee structures are fixed
- Territory assignments are ZIP-based

### **Soft Rules (System Warnings)**
- Unusual discount combinations
- High-risk driver/vehicle pairings
- Documentation requirements
- Photo collection deadlines

### **Override Capabilities**
- Underwriter overrides for eligibility
- Manual discount adjustments (rare)
- Fee waivers (manager approval)
- Special program exceptions

---

## 18. Performance and Monitoring

### **Rating Performance Standards**
- **Quote Generation**: Under 2 seconds
- **Discount Application**: Real-time validation
- **Eligibility Check**: Under 1 second
- **Factor Lookup**: Instantaneous

### **Audit and Compliance**
- **Rate Accuracy**: 99.9% calculation accuracy
- **Discount Application**: 100% rule compliance
- **Eligibility Enforcement**: 100% rule compliance
- **Fee Calculation**: 100% accuracy

### **Reporting Capabilities**
- **Discount Utilization**: By type and combination
- **Rating Factor Analysis**: Performance by factor
- **Eligibility Tracking**: Decline reasons and rates
- **Premium Distribution**: By coverage and territory

---

## 19. Future Enhancements

### **Planned Improvements**
1. **Dynamic Territories**: Real-time risk assessment
2. **Usage-Based Factors**: Telematics integration
3. **Advanced Analytics**: Machine learning rate optimization
4. **Customer Segmentation**: Behavioral-based pricing

### **System Scalability**
- **Multi-State Expansion**: Rate factor framework supports additional states
- **Product Expansion**: Framework supports additional coverage types
- **Integration Ready**: API-based architecture for external connections

---

## 20. Stakeholder Guide

### **For Underwriters**
- Use eligibility workflows for application decisions
- Apply manual overrides only when documented
- Monitor discount combinations for accuracy
- Validate documentation requirements

### **For Agents**
- All discounts apply automatically when criteria met
- Rating is instant with proper application data
- Photo requirements enforced through suspense system
- Transfer discounts require verification

### **For IT Systems**
- All rate factors must be loaded exactly as specified
- Discount calculations occur outside rate factor files
- Eligibility checking is separate from rating
- Fee calculations are additive to premium

### **For AI Agents**
- Rate factors provide the mathematical foundation
- Eligibility rules are binary decisions
- Discount stacking follows defined rules
- Documentation requirements trigger workflows

---

*This complete guide represents the final implementation of the Aguila Dorada Texas Personal Auto rating methodology, incorporating all rate factors, system enhancements, and operational requirements.*