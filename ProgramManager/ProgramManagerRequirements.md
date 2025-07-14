# Program Manager Module Requirements

## Executive Summary

The Program Manager module is a comprehensive insurance program configuration system that serves as the central hub for creating, managing, and versioning auto insurance programs. It provides granular control over rating factors, coverage options, geographic territories, integrations, and operational parameters while maintaining regulatory compliance and supporting complex business rules.

## Table of Contents

1. [System Overview](#system-overview)
2. [Functional Requirements](#functional-requirements)
   - [Program Setup & Configuration](#program-setup--configuration)
   - [Coverage & Base Rates](#coverage--base-rates)
   - [Rating Engine](#rating-engine)
   - [Geographic Management](#geographic-management)
   - [Payment & Fee Configuration](#payment--fee-configuration)
   - [Policy Configuration](#policy-configuration)
   - [Claims Configuration](#claims-configuration)
   - [Integrations](#integrations)
3. [Data Models](#data-models)
4. [Business Rules](#business-rules)
5. [Technical Requirements](#technical-requirements)
6. [Non-Functional Requirements](#non-functional-requirements)

## System Overview

### Purpose
The Program Manager module enables insurance carriers to configure and manage their auto insurance programs with complete control over rating logic, coverage options, business rules, and operational workflows.

### Key Capabilities
- Multi-level program hierarchy (Treaty → Treaty Year → Program → Version)
- Comprehensive rating factor configuration
- Geographic territory management at ZIP code level
- Integration with external data providers
- Configurable business rules and eligibility criteria
- Draft/publish workflow with testing capabilities

## Functional Requirements

### Program Setup & Configuration

#### FR-PS-001: Treaty Management
- **Description**: System shall support creation and management of insurance treaties
- **Fields**:
  - Treaty Name (freeform text)
  - Treaty Number (system-generated unique identifier)
  - Insurance Company/Carrier (dropdown from preloaded list)
  - Carrier Appointment Fee (dollar amount)

#### FR-PS-002: Treaty Year Management
- **Description**: System shall support multiple treaty years under each treaty
- **Fields**:
  - Year Label (freeform text, e.g., "Year 1", "2023-2024")
  - Effective Date (date picker)
  - Expiration Date (auto-generated based on next treaty year activation)

#### FR-PS-003: Program Definition
- **Description**: System shall support multiple programs per treaty year
- **Fields**:
  - Program Prefix (system-generated short identifier, e.g., "ADGA")
  - Program Number (system-generated version tracker)
  - Program Description (freeform text)
  - Effective Date (date picker)
  - Max Future Effective Date in Days (dropdown, default 30)
  - End Date (date picker, manually set)
  - State Approval Date (date picker)
  - Program Version Control (system-generated with timestamps and changelogs)

#### FR-PS-004: Program Terms
- **Description**: System shall support configurable policy terms
- **Options**: 6 months, 12 months (additional terms can be added)
- **Configuration**: Each term can be enabled/disabled

### Coverage & Base Rates

#### FR-CB-001: Global Rounding Controls
- **Description**: System shall provide default decimal precision for rating factors
- **Configuration**:
  - Global Round By: 0, 1, 2, or 3 decimal places (default: 2)
  - Can be overridden at individual factor level

#### FR-CB-002: Base Rate Configuration
- **Description**: System shall support base rates for all coverage lines
- **Coverage Lines**:
  - Bodily Injury (BI)
  - Property Damage (PD)
  - Uninsured Motorist - Bodily Injury (UMBI)
  - Uninsured Motorist - Property Damage (UMPD)
  - Medical Payments (MED)
  - Personal Injury Protection (PIP)
  - Comprehensive (COMP)
  - Collision (COLL)
  - Additional Equipment Coverage (AEC)
  - Towing & Labor (TOW)
  - Rental Reimbursement (RENTAL)
- **Configuration**: Each coverage line has:
  - Base rate (dollar amount)
  - Term applicability (multi-select)
  - Supported flag (on/off)
  - Dependencies (e.g., COMP/COLL must be paired)

#### FR-CB-003: Coverage Limits
- **Description**: System shall support configurable limits for each coverage type
- **Limit Types**:
  - **BI Limits**: Per person/per accident structure
  - **PD Limits**: Single limit structure
  - **PIP Limits**: Single limit structure
  - **UMBI/UMPD Limits**: With dependency rules to BI/PD
  - **MED Limits**: Multiple limit options
  - **AEC Limits**: Range-based ($100-$3,000 in $100 increments)
  - **Towing Limits**: Fixed limit options
  - **Rental Limits**: Daily limit/maximum total structure

#### FR-CB-004: Limit Dependencies
- **Description**: System shall enforce coverage limit dependencies
- **Rules**:
  - UMBI limits relationship to BI (must match, ≤, ≥, or independent)
  - UMPD limits relationship to PD (must match, ≤, ≥, or independent)
  - AEC requires COMP or COLL
  - Towing requires COMP or COLL
  - Rental requires COMP or COLL

### Rating Engine

#### FR-RE-001: Individual Rating Factors
- **Description**: System shall support rating factors for individual attributes
- **Categories**:
  
  **Policy-Level Factors**:
  - Payment Options (Installment, PIF)
  - EFT (Electronic Funds Transfer)
  - Number of Months Prior Coverage
  - Prior Insurance Verification Level
  - Is Insured a Homeowner
  - Residence Type
  - Paperless Enrollment
  - Non-Owner Policy
  - Distribution Channel
  
  **Driver-Level Factors**:
  - Gender
  - Marital Status
  - Age (15-99)
  - License Type
  - License State/Country
  - Driver Count
  - Employment Status
  - Occupation
  - Driver Points (0-50+)
  
  **Vehicle-Level Factors**:
  - Model Year
  - Physical Damage Symbol (via VIN)
  - Vehicle Usage
  - Lienholder Status
  - Vehicle Count
  - Deductible Level
  - Mileage Ratio
  - Length of Ownership
  - Branded Title/Severe Problems

#### FR-RE-002: Factor Groupings
- **Description**: System shall support composite factors based on multiple attributes
- **Groupings**:
  1. **Lienholder + Vehicle Count**
  2. **Policy Core Matrix** (Prior Coverage + Verification + Homeowner + Vehicle Count)
  3. **Driver Class** (Gender + Marital Status + Age)
  4. **Policy Driver to Vehicle** (Driver Count + Vehicle Count)
  5. **Renewal Factor** (Renewal Age + Vehicle Count)
  6. **Custom Factor Groupings** (user-defined combinations)

#### FR-RE-003: Rating Order Management
- **Description**: System shall provide configurable rating factor application order
- **Features**:
  - Drag-and-drop interface for factor ordering
  - Visual display of active factors with coverage lines and ranges
  - Consistent order across all policy terms
  - Fees always applied last

#### FR-RE-004: Rate Testing
- **Description**: System shall provide scenario-based rate testing
- **Scenarios**:
  - Simple Policy (single vehicle/driver, clean record)
  - Typical Policy (two drivers, violations, some discounts)
  - Complex Policy (multi-vehicle, diverse drivers, complex coverage)
- **Features**:
  - View inputs for each scenario
  - Run quote with line-by-line calculation log
  - Display running totals and final premium

### Geographic Management

#### FR-GM-001: State Selection
- **Description**: System shall support state-level program availability
- **Configuration**:
  - Single state selection per program
  - Sales tax rate input per state
  - All U.S. states available

#### FR-GM-002: ZIP Code Territory Factors
- **Description**: System shall support ZIP code level rating factors
- **Features**:
  - Google Maps API integration for ZIP/County lookup
  - Manual ZIP code entry option
  - Territory factors per coverage line
  - Term-specific factors
  - County-level organization

### Payment & Fee Configuration

#### FR-PF-001: Payment Plan Options
- **Description**: System shall support multiple payment methods
- **Options**:
  - Installment plans (configurable)
  - Paid in Full (PIF)
  - Electronic Funds Transfer (EFT) as enhancement
- **Installment Configuration**:
  - Total number of installments
  - Down payment percentage
  - Description
  - Factors per coverage line

#### FR-PF-002: Fee Structure
- **Description**: System shall support various fee types
- **Fee Categories**:
  
  **Entity-Based Fees**:
  - MGA Fee (per policy)
  - MVCPA Fee (per vehicle)
  - Convenience Fees (by transaction type)
  
  **Installment Fees**:
  - Base threshold amount
  - Base fee
  - Increment amount and fee
  - Formula: Base Fee + ((Premium - Threshold) / Increment) × Increment Fee
  
  **Fixed Fees**:
  - NSF (Non-Sufficient Funds)
  - Late payment
  - Endorsement
  - SR-22 filing

#### FR-PF-003: Payment Method Acceptance
- **Description**: System shall track accepted payment methods
- **Methods**:
  - Producer E-Check
  - Insured E-Check
  - Credit Card
- **Configuration**: Factors per method and coverage line

### Policy Configuration

#### FR-PC-001: Agent Commission Structure
- **Description**: System shall support configurable commission rates
- **Features**:
  - Calculation basis (Collected, Earned, or Written)
  - New Business commission rates
  - Renewal commission rates
  - Term-specific rates
  - Default rate selection

#### FR-PC-002: Underwriting Questions
- **Description**: System shall support configurable underwriting questions
- **Features**:
  - Question text (editable)
  - Supported flag (on/off)
  - Hard stop configuration (yes/no)
  - Customizable rejection messages for hard stops

#### FR-PC-003: Endorsement Management
- **Description**: System shall support pre-bind and post-bind endorsements
- **Pre-Bind Endorsements**:
  - Mandatory endorsements tied to OACM documents
  - Conditional requirements (e.g., Physical Damage requires COMP/COLL)
  
- **Post-Bind Endorsements**:
  - Producer supported flag
  - Underwriting supported flag
  - Signature requirement flag
  - System automation indicator

#### FR-PC-004: Cancellation Configuration
- **Description**: System shall support cancellation parameters
- **Settings**:
  - Cancellation effective date offset (days)
  - Cancellation method (Pro Rata or Short Rate)
  - Invoice notification lead time

#### FR-PC-005: Additional Policy Settings
- **Description**: System shall support various policy configurations
- **Settings**:
  - Non-Owner SR-22 requirement
  - Driver removal support
  - Invoice lead time

### Claims Configuration

#### FR-CC-001: Claims Program Settings
- **Description**: System shall support basic claims configuration
- **Features**:
  - Email alerts for new adjuster assignments (on/off)

#### FR-CC-002: Standard Reserves
- **Description**: System shall support configurable reserve amounts
- **Configuration**:
  - Reserve type (Claim or Expense)
  - Status (Open, Represented, Litigation)
  - Cause code
  - Dollar amounts per coverage line
  - Default fallback values

#### FR-CC-003: External Appraisal Links
- **Description**: System shall support external appraisal vendor configuration
- **Features**:
  - Vendor selection from system entities
  - Static upload link storage
  - Term applicability
  - FNOL appraisal modal control

### Integrations

#### FR-IN-001: Integration Types
- **Description**: System shall support various third-party integrations
- **Categories**:
  - **Comparative Rater**: ITC/Zywave
  - **Payment Processor**: Paysafe/Tranzpay
  - **Vehicle Data**: Verisk VINMASTER, Lightspeed
  - **Claims Data**: Verisk ISO Claim Search
  - **Driver Data**: DCS (household drivers/vehicles, criminal history)
  - **Communication**: Twilio (SMS), SendGrid (email)
  - **Verification**: TexasSure FRVP, Smarty (address)
  - **Banking**: Positive Pay (Sunflower Bank)
  - **Mapping**: Google Maps API

#### FR-IN-002: Integration Configuration
- **Description**: System shall track integration status and usage
- **Features**:
  - Integration selection per type
  - Usage location (RQB/Program or System)
  - Purpose description
  - Connection status indicator

## Data Models

### DM-001: Program Hierarchy
```
Treaty
├── Treaty Year
│   ├── Program Version 1
│   ├── Program Version 2
│   └── Program Version N
```

### DM-002: Rating Structure
```
Base Rate
├── Individual Factors
├── Factor Groupings
├── Territory Factors
├── Discounts/Surcharges
└── Fees
    = Final Premium
```

### DM-003: Coverage Structure
```
Coverage Line
├── Base Rate
├── Limits
│   ├── Limit Options
│   └── Limit Factors
├── Deductibles (COMP/COLL only)
└── Dependencies
```

## Business Rules

### BR-001: Coverage Dependencies
- COMP and COLL must be selected together (paired requirement)
- AEC requires active COMP or COLL coverage
- Towing & Labor requires active COMP or COLL coverage
- Rental Reimbursement requires active COMP or COLL coverage

### BR-002: Limit Relationships
- UMBI limits must follow configured relationship to BI limits
- UMPD limits must follow configured relationship to PD limits
- AEC limits must be within $100-$3,000 range in $100 increments

### BR-003: Driver Assignment Logic
1. Calculate driver factors (composite of Driver Class, Points, License Type)
2. Calculate vehicle factors (composite of Model Year, Symbol, Usage, etc.)
3. Sort both lists in descending order
4. Assign highest-rated driver to highest-rated vehicle
5. Unassigned vehicles receive Unrated Driver (URD) designation

### BR-004: Mileage Ratio Calculation
```
Mileage Ratio = Actual Annual Mileage / Average Mileage Base (by vehicle age)
Factor = Lookup based on rounded ratio (2 decimal places)
```

### BR-005: Criminal History Processing
- Alcohol-related offenses (Category A) map to DWI violations for rating
- Each alcohol offense counts as separate occurrence
- Misdemeanor (M) and Felony (F) categories used for eligibility only
- No criminal charge descriptions shown to agents

### BR-006: Violation Point Assignment
- Severity levels: Major (6 pts), Severe (5 pts), Major Moving (3-5 pts), Minor (1-2 pts)
- Points vary by occurrence (1st, 2nd, 3rd+)
- Total points map to driver point factors
- Sources: Verisk, DCS, Manual entry

### BR-007: Rate Order Consistency
- Rate order must be identical across all policy terms
- Fees must always be applied last in calculation
- Order affects final premium due to multiplicative factors

### BR-008: Draft vs. Published Programs
- Draft programs not visible to downstream systems
- Draft programs can use Rate Tester and scenario quoting
- Published programs require all validations to pass
- Past-dated drafts must update effective date before publishing

## Technical Requirements

### TR-001: Data Types and Formats
- **Monetary Values**: Support decimal precision with configurable rounding
- **Dates**: Standard date format with timezone support
- **Identifiers**: System-generated unique IDs for treaties, programs
- **Percentages**: Support decimal percentages (e.g., 16.67%)

### TR-002: Integration Protocols
- **APIs**: RESTful services for external integrations
- **Real-time**: Support for real-time data retrieval (Verisk, DCS)
- **Batch**: Support for batch processing where applicable
- **Security**: Secure authentication for all external connections

### TR-003: Validation Requirements
- **Model Year**: Must be between 1989 and current year + 1
- **Driver Age**: Must be between 15 and 99
- **ZIP Codes**: Must be valid for selected state
- **VIN**: Must decode successfully for symbol lookup
- **Factors**: Must have values for all active coverage lines

### TR-004: Performance Requirements
- **Rate Calculation**: Complete within 3 seconds for typical policy
- **Territory Lookup**: ZIP to factor mapping within 1 second
- **Integration Timeouts**: Configurable per integration (max 30 seconds)
- **Bulk Operations**: Support batch updates for territory factors

### TR-005: User Interface Requirements
- **Drag-and-Drop**: For rate order configuration
- **Multi-Select**: For term and state selections
- **Validation**: Real-time validation with clear error messages
- **Preview**: Ability to preview changes before saving
- **Search**: Searchable dropdowns for large lists (occupations, violations)

## Non-Functional Requirements

### NFR-001: Security
- Role-based access control for program configuration
- Audit trail for all program changes
- Encryption for sensitive data (SSN, criminal history)
- PCI compliance for payment processing integrations

### NFR-002: Availability
- 99.9% uptime for production systems
- Scheduled maintenance windows for updates
- Redundancy for critical integrations

### NFR-003: Scalability
- Support for 50+ concurrent program configurations
- Handle 10,000+ ZIP codes per state
- Process 1,000+ rate calculations per minute

### NFR-004: Usability
- Intuitive interface requiring minimal training
- Context-sensitive help for complex configurations
- Validation messages that guide correct data entry
- Ability to clone existing programs as templates

### NFR-005: Compliance
- Maintain regulatory compliance for insurance programs
- Support state-specific requirements
- Audit trail for regulatory reviews
- Version control for historical rate filing

### NFR-006: Data Retention
- Maintain program history for 7 years
- Archive older versions with retrieval capability
- Retain rate test results for 90 days
- Keep integration logs for 30 days

## Appendix A: Glossary

- **AEC**: Additional Equipment Coverage
- **BI**: Bodily Injury
- **COLL**: Collision
- **COMP**: Comprehensive
- **DCS**: Data Collection Services
- **EFT**: Electronic Funds Transfer
- **MED**: Medical Payments
- **MGA**: Managing General Agent
- **MVCPA**: Motor Vehicle Crime Prevention Authority
- **PD**: Property Damage
- **PIF**: Paid in Full
- **PIP**: Personal Injury Protection
- **RQB**: Rate/Quote/Bind
- **UMBI**: Uninsured Motorist Bodily Injury
- **UMPD**: Uninsured Motorist Property Damage
- **URD**: Unrated Driver
- **VIN**: Vehicle Identification Number

## Appendix B: Formula Reference

### Installment Fee Calculation
```
Installment Fee = Base Fee + ceil((Term Premium - Base Threshold) / Increment Amount) × Increment Fee
```

### AEC Premium Calculation
```
Premium = ((AEC Limit / 100) × AEC Base Rate) × Payment Plan Multiplier × Term
```

### Mileage Ratio
```
Mileage Ratio = Actual Annual Mileage / Average Annual Mileage Base
```

### Final Premium Calculation
```
Premium = (((((Base Rate × Factor₁) × Factor₂) × Factor₃) × Factor₄) × Factor₅) × Factor₆... + Fees
```