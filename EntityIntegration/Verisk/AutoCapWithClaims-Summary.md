# AutoCapWithClaims - Product Summary

## What is AutoCapWithClaims?

AutoCapWithClaims is Verisk's comprehensive vehicle claims history and activity prediction service. It combines historical claims data with predictive analytics to help insurance companies assess risk during the underwriting process. The service provides a complete view of an applicant's claims history across multiple insurance carriers, along with detailed vehicle information and identity verification.

## What Does It Do?

### Primary Functions:
1. **Claims History Search** - Retrieves comprehensive auto insurance claims data from contributing carriers
2. **Claim Activity Predictor (CAP)** - Uses advanced analytics to predict future claim likelihood based on historical patterns
3. **Vehicle Information Services** - Provides detailed vehicle data including VIN validation, salvage history, recalls, and theft records
4. **Identity Verification** - Validates Social Security Numbers and checks against death master records

### Key Benefits:
- Helps identify high-risk applicants with multiple prior claims
- Detects potential fraud through SSN validation and death master checks
- Provides complete vehicle history including salvage and catastrophe involvement
- Enables accurate risk assessment and appropriate pricing

## Main Technical Components

### Request Structure:
```
Request
├── Header
│   ├── Authorization (Required)
│   │   ├── OrgId (Organization ID, 3-10 characters)
│   │   └── ShipId (Ship ID, 3-10 characters)
│   └── Quoteback (Optional reference string)
└── Body
    ├── Drivers (Required, array of driver information)
    ├── Addresses (Required, at least one address)
    ├── VINS (Optional, Vehicle Identification Numbers)
    ├── PhoneNumbers (Optional)
    └── PriorPolicyNumber (Optional)
```

### Response Structure:
```
Response
├── Header
│   ├── TransactionId (Unique identifier)
│   └── Quoteback (Echoed from request)
└── Body
    ├── ClaimActivityPredictor (CAP indicator and claim count)
    ├── Claims (Detailed claims history)
    ├── Vehicles (Complete vehicle information)
    └── SSNInformations (SSN validation results)
```

## Key Data Points Available

### Claims Data:
- **Claim Details**: Reference numbers, carrier information, policy numbers
- **Fault Determination**: At-fault indicators (including California-specific)
- **Coverage Types**: Collision, Comprehensive, Bodily Injury, Property Damage, etc.
- **Loss Information**: Date, time, location, description, amounts (paid/reserved)
- **Involved Parties**: All drivers/vehicles involved in each claim
- **Claim Status**: Open/Closed status with dates

### Vehicle Information:
- **Basic Details**: Year, Make, Model, VIN validation status
- **History**: Salvage titles, catastrophe involvement, theft records
- **Safety**: Recall notices with detailed descriptions, airbag deployment
- **Ownership**: Cash for Clunkers participation, odometer readings
- **Damage**: Point of impact, total loss indicators

### Identity Verification:
- **SSN Validation**: Format validation and issuance verification
- **Death Master Check**: Identifies if SSN belongs to deceased individual
- **Match Confidence**: How well the provided data matches found records

### Risk Indicators:
- **CAP Score**: Predictive indicator of future claim likelihood
- **Claim Count**: Total number of historical claims (0-99)
- **Match Reasons**: How the system matched the individual to claims
- **Dispute Statements**: Any disputes filed regarding claims

## Required Information for Requests

### Minimum Requirements:
1. **Authorization Credentials**:
   - OrgId (your organization identifier)
   - ShipId (your ship/subdivision identifier)

2. **At least one Driver** with:
   - Sequence number (1-5)
   - Name OR SSN OR Driver's License

3. **At least one Address** (can be empty but array must exist)

### Recommended Information (Improves Match Rates):
- **Full Driver Details**:
  - Complete name (First, Middle, Last, Suffix)
  - Date of Birth (YYYYMMDD format)
  - Social Security Number (9 digits)
  - Driver's License Number and State
  - Previous License information

- **Complete Address History**:
  - Current address
  - Previous addresses
  - Mailing address (if different)

- **Vehicle Information**:
  - VINs for all vehicles
  - Prior policy number

- **Contact Information**:
  - Phone numbers

## Search Types

The system performs multiple search types based on provided data:
- **V**: VIN Search - Finds claims associated with specific vehicles
- **S**: SSN Search - Matches claims by Social Security Number
- **D**: Driver License Search - Uses DL number and state
- **A**: Name and Address Search - Matches by personal information
- **N**: Name and DOB Search - Uses name and birth date
- **P**: Phone Number Search - Finds claims by phone number

## Use Cases

### Primary Insurance Uses:
1. **New Business Underwriting** - Assess risk for new policy applications
2. **Policy Renewal** - Review claims history at renewal time
3. **Rate Determination** - Use claims history to calculate appropriate premiums
4. **Fraud Detection** - Identify potential fraud through SSN validation and death checks

### Risk Assessment Applications:
- Identify frequent claimants
- Detect undisclosed claims
- Verify vehicle history and condition
- Validate applicant identity

## Response Codes and Error Handling

- **200**: Success (empty body indicates no claims found)
- **400**: Bad Request (formatting or validation issues)
- **401**: Unauthorized (expired authentication token)
- **403**: Forbidden (invalid credentials)
- **500**: Internal Server Error
- **588**: Bad Response (data validation error)

## Important Notes

1. **Data Formats**:
   - All dates use YYYYMMDD format
   - SSN must be 9 digits (no dashes or spaces)
   - State codes are 2-character abbreviations

2. **Limits**:
   - Maximum 5 drivers per request
   - Claims history typically goes back 5-7 years
   - Response includes up to 99 claims

3. **Privacy Compliance**:
   - Service complies with Driver's Privacy Protection Act
   - Personal information is only provided for permissible uses
   - All data transmission is encrypted

4. **Best Practices**:
   - Provide as much identifying information as possible for best match rates
   - Use multiple search criteria to ensure comprehensive results
   - Review all claims, not just at-fault incidents
   - Check vehicle history even if no claims are found

This service is essential for accurate risk assessment and pricing in auto insurance, providing a comprehensive view of an applicant's claims history and vehicle information in a single API call.