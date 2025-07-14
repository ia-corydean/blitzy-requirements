# LightSpeed V4 - Product Summary

## What is LightSpeed?

LightSpeed V4 is Verisk's flagship comprehensive auto insurance data service that provides insurers with a complete, multi-source view of drivers, vehicles, and associated risks. It's an all-in-one API that aggregates data from DMVs, insurance carriers, credit bureaus, demographic providers, and environmental data sources to deliver everything needed for accurate underwriting and pricing decisions in a single request.

## What Does It Do?

### Primary Functions:
1. **Multi-Source Identity Verification** - Validates driver identity across primary and secondary data sources
2. **Motor Vehicle Reports (MVR)** - Retrieves complete driving records with violations and license status
3. **Comprehensive Risk Scoring** - Provides multiple risk assessment scores and fraud indicators
4. **Insurance History Analysis** - Tracks coverage history and identifies lapses across carriers
5. **Vehicle Intelligence** - Delivers detailed vehicle specs, ownership history, and telematics data
6. **Household Demographics** - Enriches applications with household-level insights
7. **Environmental Risk Analysis** - Assesses location-based risks including weather and traffic patterns
8. **Claims History Integration** - Includes claims data when available

### Key Benefits:
- Single API call replaces multiple vendor integrations
- Reduces underwriting time with pre-integrated data
- Improves risk assessment accuracy with multi-dimensional scoring
- Identifies fraud through cross-source validation
- Enables sophisticated pricing with environmental and demographic factors

## Main Technical Components

### Request Structure:
```
Request
├── Header
│   ├── Authorization (Required)
│   │   ├── OrgId (3-10 characters)
│   │   └── ShipId (3-10 characters)
│   ├── Quoteback (Optional reference)
│   └── RequestOptions (Optional configurations)
└── Body
    ├── Drivers[] (Required, 1-5 drivers)
    │   ├── Identity (Name, DOB, SSN, DL)
    │   └── Attributes (Marital status, homeownership)
    ├── Addresses[] (Optional, max 2)
    ├── PhoneNumbers[] (Optional, max 2)
    └── Vehicles[] (Optional, max 5)
```

### Response Structure:
```
Response
├── Header
│   ├── TransactionId (GUID)
│   └── Quoteback
└── Body
    ├── StatusCode
    └── CompleteQuote
        ├── QuoteScores (Overall risk metrics)
        ├── RiskCheckScoreSummary (Fraud/risk indicators)
        ├── Subjects[] (Driver details with MVR)
        ├── Vehicles[] (Complete vehicle data)
        ├── Policies[] (Insurance history)
        ├── CoverageLapseInformation[]
        ├── HouseholdInformation
        ├── Addresses[] (Verified/enhanced)
        ├── Claims[] (When available)
        └── RiskAnalyzerEnvironmental
```

## Key Data Points Available

### Driver Information:
- **Identity Verification**:
  - EntityScore: Risk assessment score (1-999)
  - Primary/Secondary source validation
  - SSN verification and fraud flags
  - Death index checking

- **Motor Vehicle Report (MVR)**:
  - License class, status, restrictions
  - Issue/expiration dates
  - Physical characteristics
  - Complete violation history:
    - Type (VIOL/SUSP/REIN)
    - Dates (violation and conviction)
    - Points (state and custom)
    - Detailed descriptions
  - Clear/Non-clear status indicator

- **Credit-Based Insurance Score**:
  - InflectionCBIS score
  - Score factors and reason codes
  - No-hit indicators

### Vehicle Intelligence:
- **Basic Information**:
  - VIN validation and decoding
  - Year, Make, Model, trim details
  - Vehicle class and type

- **Ownership & History**:
  - Number of owners
  - Registration status and history
  - Salvage indicators
  - Mileage estimates from multiple sources

- **Advanced Data**:
  - SmartScore (telematics-based driving score)
  - TrueVin verification results
  - VinMaster detailed specifications
  - RiskAnalyzer vehicle-specific risks

### Risk Assessment Components:

- **RiskCheckScoreSummary**:
  - RiskGroup: VERY HIGH/HIGH/MEDIUM/LOW
  - ScoreColor: RED/YELLOW/GREEN
  - TotalScore: Numeric risk value
  - ScoreDecile: 1-10 percentile ranking
  - Fraud indicators and warnings

- **QuoteScores**:
  - Multiple proprietary scoring models
  - Customizable score configurations
  - Decile rankings for peer comparison

### Household & Demographic Data:
- **Household Composition**:
  - Youth counts (11-15, 16-17 age groups)
  - Total household size
  - Education level indicators
  - Years at residence

- **Financial Indicators**:
  - Homeownership status
  - Dwelling type (Single/Multi/Apartment)
  - Net worth bands
  - SOHO (Small Office/Home Office) indicator

### Environmental Risk Analysis:
- **Location-Based Risks**:
  - Weather severity scores
  - Traffic density and composition
  - Proximity to traffic generators
  - Historical loss patterns by coverage type

- **Predictive Components**:
  - Frequency scores (property damage, collision, comprehensive)
  - Severity scores by coverage type
  - Experience trends
  - Composite risk indicators

### Insurance History:
- **Policy Details**:
  - Current and historical policies
  - Coverage types and limits
  - Carrier information with ratings
  - Payment history and methods

- **Coverage Analysis**:
  - Lapse detection with date ranges
  - Days between policies
  - Overlap identification
  - Continuous coverage verification

## Required Information for Requests

### Minimum Requirements:
1. **Authorization**:
   - OrgId (your organization identifier)
   - ShipId (your ship/subdivision identifier)

2. **At least one Driver**:
   - GivenName (first name, 1-20 chars)
   - Surname (last name, 1-30 chars)

### Recommended for Comprehensive Results:
- **Driver Details**:
  - Date of Birth (YYYYMMDD)
  - SSN (9 digits)
  - Driver's License Number and State
  - Marital Status
  - Homeownership indicator

- **Location Information**:
  - Current address (for environmental risk)
  - Previous addresses
  - Phone numbers

- **Vehicle Data**:
  - VINs for all vehicles
  - Basic vehicle info if VIN unknown

## Use Cases

### Primary Insurance Applications:
1. **New Business Underwriting** - Complete risk assessment for new applications
2. **Quick Quote Generation** - Instant pricing with comprehensive data
3. **Fraud Detection** - Multi-source validation identifies inconsistencies
4. **Portfolio Analysis** - Understand risk distribution across book

### Advanced Risk Assessment:
- **Multi-Dimensional Scoring**: Combine MVR, credit, environmental, and demographic factors
- **Household Risk**: Assess total household exposure including young drivers
- **Location Intelligence**: Price based on specific geographic risks
- **Behavioral Indicators**: Use telematics and claims history for precision

### Regulatory Compliance:
- **Fair Credit Reporting Act**: Proper handling of credit-based scores
- **Driver Privacy Protection**: Compliant access to MVR data
- **State-Specific Requirements**: Configurable to meet local regulations

## Response Codes and Processing

### HTTP Status Codes:
- **200**: Success (check body for hit/no-hit status)
- **400**: Bad Request (validation failed)
- **401**: Unauthorized (token expired)
- **403**: Forbidden (invalid credentials)
- **500**: Internal Server Error
- **588**: Bad Response (data error)

### Data Source Indicators:
- **PrimarySourceInfo**: High-confidence verified data
- **SecondarySourceInfo**: Additional supporting data
- **EntityScore**: Composite verification confidence

## Best Practices

1. **Request Optimization**:
   - Provide SSN and DL for best MVR hit rates
   - Include current address for environmental analysis
   - Submit all household drivers together

2. **Response Handling**:
   - Check both status codes and body content
   - Process all risk scores for complete picture
   - Review fraud indicators before proceeding

3. **Data Quality**:
   - Use exact name spelling from documents
   - Provide complete 9-digit SSN (no formatting)
   - Include full VIN when available

4. **Performance**:
   - Response can be large (1000+ lines)
   - Parse incrementally for large responses
   - Cache results appropriately

## Key Differentiators

1. **Comprehensive Coverage**: Most complete data set available in single API
2. **Speed**: Real-time response for instant quoting
3. **Accuracy**: Multi-source validation ensures data quality
4. **Intelligence**: Advanced analytics and scoring built-in
5. **Flexibility**: Configurable to insurer-specific needs

## Data Formats

- **Dates**: YYYYMMDD format exclusively
- **States**: 2-character postal codes
- **SSN**: 9 digits, no dashes or spaces
- **Phone**: 10 digits, no formatting
- **VIN**: Up to 25 characters
- **Boolean**: Y/N or T/F depending on field

This service represents the most advanced insurance data platform available, enabling insurers to make faster, more accurate underwriting decisions while reducing operational costs through consolidation of multiple data sources into a single, intelligent API.