# CoverageVerifier - Product Summary

## What is CoverageVerifier?

CoverageVerifier (CV) Version 8 is Verisk's specialized insurance coverage verification service that helps insurers verify prior auto insurance coverage history. It identifies coverage lapses, provides detailed policy information from contributing carriers, and delivers analytic scores to support underwriting decisions. The service is critical for assessing risk based on an applicant's insurance history and ensuring continuous coverage compliance.

## What Does It Do?

### Primary Functions:
1. **Coverage History Verification** - Confirms prior insurance coverage across multiple carriers
2. **Lapse Detection** - Identifies gaps in insurance coverage with precise date ranges
3. **Policy Detail Retrieval** - Provides comprehensive policy information including coverages, limits, and vehicles
4. **Analytics and Scoring** - Delivers risk assessment attributes and scores based on insurance behavior
5. **Multi-Carrier Search** - Searches across participating insurance carriers for complete history

### Key Benefits:
- Validates continuous coverage for better risk assessment
- Identifies coverage gaps that may indicate higher risk
- Provides detailed policy information for accurate quoting
- Helps detect policy shopping behavior and carrier switching patterns
- Enables compliance with state continuous coverage requirements

## Main Technical Components

### Request Structure:
```
Request
├── Header
│   ├── Authorization (Required)
│   │   ├── OrgId (3-10 characters)
│   │   └── ShipId (3-10 characters)
│   ├── Quoteback (Optional, echoed in response)
│   └── RequestOptions (Optional key-value pairs)
└── Body
    ├── Drivers[] (1-5 drivers, Required)
    │   ├── Personal Info (Name required, DOB/SSN optional)
    │   └── License Info (DL Number/State optional)
    ├── Addresses[] (1-3 addresses, Required)
    │   └── Must include at least one "Current" type
    ├── VINS[] (Optional)
    ├── PhoneNumbers[] (Optional, max 2)
    └── PriorPolicyNumber (Optional)
```

### Response Structure:
```
Response
├── Header
│   ├── TransactionId (GUID)
│   └── Quoteback
└── Body
    ├── Policies[] (Found policy records)
    │   ├── Policy Information
    │   ├── Match Scoring
    │   ├── Current Details
    │   └── Historical Data
    ├── CoverageLapseInformation[] (Per driver)
    │   ├── Lapse Indicators
    │   └── Coverage Intervals
    ├── AnalyticObjects[] (Risk attributes)
    └── CustomElements[] (Additional data)
```

## Key Data Points Available

### Policy Information:
- **Policy Identification**: Number, status, dates (inception, expiration, cancellation)
- **Transaction History**: Renewals, endorsements, cancellations with reasons
- **Carrier Details**: Name, AM Best ratings, NAIC code
- **Premium Information**: Payment methods, amounts, billing details

### Coverage Types (61 Types Including):
- **Liability Coverage**:
  - BINJ: Bodily Injury (e.g., $10,000/$25,000)
  - PDMG: Property Damage
  - CBSL: Combined Single Limit
  - PINJ: Personal Injury Protection
  
- **Physical Damage**:
  - COLL: Collision (with deductibles)
  - COMP: Comprehensive (with deductibles)
  - GLSS: Glass Coverage
  
- **Uninsured/Underinsured**:
  - UMBI/UMPD: Uninsured Motorist
  - UDBI/UDPD: Underinsured Motorist
  
- **Additional Coverage**:
  - TOWL: Towing & Labor
  - RENT: Rental Reimbursement
  - ROAD: Roadside Assistance

### Analytic Attributes (Key Examples):
- **102**: Frequency of cancel/reinstate activity
- **106**: Days since last carrier switch
- **126/127**: Vehicles exceed drivers / Drivers exceed vehicles
- **300**: Current active policy count
- **346**: Last policy coverage gap (days)
- **347**: Total lapse days across history
- **360**: Total coverage overlap days
- **368**: Number of prior carriers

### Coverage Lapse Analysis:
- **Per Driver Assessment**:
  - HasPossibleLapse (Y/N indicator)
  - IsCurrentInforceCoverage (Y/N)
  - Detailed coverage intervals with dates
  - Number of lapse days between policies
  - Total coverage days

### Vehicle Information:
- Year, Make, Model, VIN
- Vehicle class and type codes
- Business use indicators
- Anti-theft devices
- Territory codes

### Driver/Subject Information:
- Personal details (name, DOB, gender, marital status)
- Driver's license information
- Relationship to policyholder
- SSN (when available)

## Required Information for Requests

### Minimum Requirements:
1. **Authorization**:
   - OrgId (your organization ID)
   - ShipId (your ship/subdivision ID)

2. **At least one Driver**:
   - Sequence number (1-5)
   - GivenName (first name, 1-20 chars)
   - Surname (last name, 1-30 chars)

3. **At least one Address**:
   - Must include at least one "Current" type address
   - Street1, City, StateCode required
   - Zip optional but recommended

### Recommended for Better Match Rates:
- **Driver Information**:
  - Date of Birth (YYYYMMDD format)
  - SSN (up to 9 digits)
  - Current Driver's License Number and State
  - Previous Driver's License (if applicable)

- **Additional Data**:
  - Prior policy number
  - Multiple addresses (current, previous, mailing)
  - Phone numbers
  - Vehicle VINs

## Use Cases

### Primary Insurance Applications:
1. **New Business Verification** - Confirm continuous coverage for new applicants
2. **Rate Determination** - Use coverage history and lapses for accurate pricing
3. **Underwriting Decisions** - Assess risk based on insurance behavior patterns
4. **State Compliance** - Meet continuous coverage verification requirements

### Risk Indicators from Analytics:
- **Policy Shopping**: Frequent carrier changes may indicate rate shopping
- **Coverage Gaps**: Lapses may indicate financial instability or risk-taking behavior
- **Coverage Changes**: Reductions in coverage limits may signal financial stress
- **Vehicle/Driver Mismatch**: More vehicles than drivers or vice versa

## Important Analytics Explained

### Key Attribute Codes:
- **346 (Last Coverage Gap)**: Days between policies - higher values indicate longer uninsured periods
- **300 (Active Policies)**: Multiple active policies may indicate household complexity
- **368 (Prior Carriers)**: High count may indicate instability or rate shopping
- **102 (Cancel/Reinstate)**: Frequency indicates payment issues or instability

### Risk Scoring:
- Three proprietary scores (ScoreName1, ScoreName2, ScoreName3)
- Values typically range 0-999
- Higher scores generally indicate better risk

## Response Codes and Matching

### HTTP Status Codes:
- **200**: Success (check response body for actual results)
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **500**: Internal Server Error
- **588**: Validation Error

### Match Scoring:
- **Match Score**: 1-100 (higher is better match confidence)
- **Match Reasons**: Specific fields that matched (e.g., "NAME IS IDENTICAL", "ADDRESS IS IDENTICAL")
- **Search Type**: Always "P" for Person search

## Best Practices

1. **Data Quality**:
   - Provide complete current address for best results
   - Include DOB and DL information when available
   - Use exact name spelling as appears on documents

2. **Coverage Analysis**:
   - Review both HasPossibleLapse and actual lapse days
   - Check coverage intervals for patterns
   - Consider overlap periods as well as gaps

3. **Risk Assessment**:
   - Combine multiple analytic attributes for comprehensive view
   - Consider both current and historical policy information
   - Review carrier switching patterns

4. **Compliance**:
   - Document continuous coverage for state requirements
   - Maintain audit trail of verification attempts
   - Handle no-hit scenarios appropriately

## Data Format Requirements

- **Dates**: Always YYYYMMDD format
- **States**: 2-character abbreviations
- **Names**: Alphanumeric only, proper case recommended
- **Addresses**: Standardized format preferred
- **Case Sensitivity**: System is generally case-insensitive

This service is essential for insurance underwriting, providing verified coverage history that helps insurers make informed decisions about risk and pricing while ensuring regulatory compliance.