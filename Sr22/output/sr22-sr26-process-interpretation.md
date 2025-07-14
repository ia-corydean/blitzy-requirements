# SR22/26 Process Interpretation - Aguila Dorada Texas Personal Auto Program

## Overview
This document provides a comprehensive interpretation of the SR22/SR26 process within the Aguila Dorada Texas Personal Auto insurance program. The SR22 process enables drivers to maintain their license following specific violations or offenses, while the SR26 process handles cancellation of SR22 filings. This interpretation serves as the definitive reference for system implementation, business operations, and compliance requirements.

## 1. SR22 Process Specifications

### Purpose and Definition
- **SR22 Requirement**: Mandated for drivers to maintain their driver's license due to specific violations or offenses
- **Legal Function**: Proof of financial responsibility filing required by Texas Department of Public Safety
- **Program Integration**: Available within the Aguila Dorada Texas Personal Auto program for eligible drivers

### SR22 Eligibility Criteria
- **Driver License Requirement**: Must have a Texas Driver's License
- **Policy Status**: Can be added at New Business or by Endorsement
- **Driver Status**: Must be a rated driver on the policy
- **Geographic Restriction**: Texas residents only (aligns with program requirements)

### SR22 Reason Categories
1. **DWI or DUI Conviction** - Driving while intoxicated or under the influence
2. **Driving Without Insurance** - Operating a vehicle without required insurance coverage
3. **Multiple Traffic Offenses in a Short Period** - Accumulation of violations within limited timeframe
4. **At-Fault Accident Without Insurance** - Causing accident while uninsured
5. **License Suspension or Revocation** - Administrative or court-ordered license actions
6. **Court Order or Driving with a Suspended License** - Judicial mandate or violation of suspension

### SR22 Fee Structure
- **Base Fee**: $25.00 per driver requiring SR22
- **Fee Type**: Fully earned upon processing (non-refundable)
- **New Business Payment**: Due with down payment in full
- **Endorsement Payment**: Due with endorsement processing plus any endorsement fee
- **Additional Costs**: May include endorsement fee ($15.00) and additional down payment for premium increases

## 2. SR22 Form Requirements

### Required Data Fields
- **Driver Name**: Full legal name of the driver requiring SR22
- **Address/City/State/Zip**: Complete mailing address
- **Case Number**: Texas Driver's License Number
- **TX Driver's License No.**: Texas DL number (duplicate field for case reference)
- **Date of Birth**: Driver's date of birth
- **Policy Number**: Insurance policy number
- **Effective Date**: SR22 effective date
- **Policy Type**: Owner Policy or Operator Policy (Non-Owner)
- **State**: Texas (fixed value)
- **Name of Insurance Company**: Old American County Mutual (OACM)
- **Date (Issued)**: Document generation date
- **Signature**: Required signature field

### Form Generation Rules
- **System Generated**: Automatically created template with driver information and carrier details
- **Document Placement**: Available in document output for agent/underwriter distribution
- **Portal Access**: Available on insured portal for active policies
- **Distribution Method**: NOT mailed or electronically sent to state by carrier
- **Driver Responsibility**: Driver must provide SR22 to DMV/State for handling

## 3. SR26 Process Specifications

### Purpose and Triggers
- **SR26 Creation**: Generated when SR22 is no longer needed or policy is cancelled
- **Cancellation Scenarios**:
  - Driver no longer requires SR22 to maintain license
  - Policy cancellation for any reason
  - Voluntary discontinuation of SR22 filing

### SR26 Form Requirements
- **Data Fields**: Identical to SR22 form with addition of cancellation effective date
- **Cancellation Effective Date**: Date SR22 filing is terminated
- **System Integration**: Updates state data to reflect policy and SR22 cancellation

### SR26 Processing Rules
- **Automatic Generation**: System creates SR26 upon triggering events
- **State Notification**: Data submitted to state reflects cancellation status
- **Policy Reinstatement**: New SR22 generated if policy is reinstated with new effective date

## 4. Business Rules and Constraints

### Processing Rules
- **New Business**: SR22 can be added during initial policy creation
- **Endorsement**: SR22 can be added via policy endorsement after inception
- **Data Updates**: New SR22 generated when rated driver data changes affecting required fields
- **System Automation**: SR22 template automatically generated and placed in document output

### Non-Owner Policy Rules
- **Availability**: Non-owner policies available ONLY when SR22 is requested
- **Eligibility**: Must meet all other program requirements
- **Restriction**: Not available for standard policies without SR22 requirement

### Prohibited Activities
- **SR22A Filings**: Not permitted on this program
- **State Fee Collection**: No fees collected or accounted for related to state fines
- **Direct State Filing**: Carrier does not file SR22 directly with state

## 5. System Integration Requirements

### Document Management
- **Template Generation**: System automatically creates SR22 template with driver and carrier details
- **Document Storage**: Placed in document output system for agent/underwriter access
- **Portal Integration**: Available on insured portal for active policies
- **Version Control**: New SR22 generated when driver data changes

### State Reporting
- **Reporting Method**: SR22 data captured and reported to state weekly for Insurance Verification
- **Data Elements**: Driver information, policy details, and SR22 status
- **Update Frequency**: Weekly submission schedule
- **Cancellation Reporting**: SR26 data updates state records for policy/SR22 cancellation
  * The insured will send it after we generate it.

### Policy Lifecycle Integration
- **New Business**: SR22 processing integrated with policy binding
- **Endorsements**: SR22 addition/modification via endorsement system
- **Cancellations**: Automatic SR26 generation upon policy cancellation
- **Reinstatements**: New SR22 creation upon policy reinstatement

## 6. Fee Structure and Payment Processing

### SR22 Fee Details
- **Amount**: $25.00 per driver requiring SR22
- **Collection Timing**: Due upon processing (fully earned)
- **Payment Integration**: 
  - New Business: Included with down payment
  - Endorsement: Collected with endorsement processing
- **Additional Fees**: May include $15.00 endorsement fee for mid-term additions

### Fee Processing Rules
- **Earned Status**: Fully earned upon processing (non-refundable)
- **Payment Methods**: Same as policy payment methods (EFT, Credit Card, Standard billing)
- **Down Payment Impact**: May increase required down payment for endorsements
- **Premium Integration**: Combined with any premium increases from SR22 addition

## 7. Compliance and Regulatory Requirements

### Texas State Compliance
- **DPS Integration**: Weekly data reporting to Texas Department of Public Safety
- **Insurance Verification**: Supports state insurance verification system
- **Regulatory Alignment**: Meets Texas requirements for SR22 filings
  - Can the insured just not send it in and the mga is in compliance?

### Documentation Requirements
- **Record Keeping**: Maintain SR22 records per state requirements
- **Audit Trail**: Document all SR22 related transactions and changes
- **Compliance Verification**: Ensure all filings meet state specifications

### Driver Responsibility
- **State Filing**: Driver responsible for providing SR22 to DMV/State
- **Compliance Maintenance**: Driver must maintain SR22 for required period
- **Renewal Obligations**: Driver responsible for maintaining continuous coverage

## 8. Operational Procedures

### Processing Workflow
1. **SR22 Request**: Driver requests SR22 filing
2. **Eligibility Verification**: Confirm driver has Texas DL and is rated on policy
3. **Reason Documentation**: Capture SR22 reason from dropdown options
4. **Fee Collection**: Process $25.00 SR22 fee
5. **System Generation**: Automatic SR22 template creation
6. **Document Delivery**: Provide SR22 to driver via document output/portal
7. **State Reporting**: Include in weekly state data submission

### Endorsement Processing
1. **Request Receipt**: Process SR22 addition request
2. **Premium Impact**: Calculate any premium changes
3. **Fee Calculation**: Add SR22 fee plus endorsement fee
4. **Payment Collection**: Collect total fees and any additional down payment
5. **Document Generation**: Create new SR22 with updated information
6. **State Update**: Include changes in next weekly state report

### Cancellation Processing
1. **Trigger Event**: Policy cancellation or SR22 no longer needed
2. **SR26 Generation**: System automatically creates SR26 form
3. **Effective Date**: Set cancellation effective date
4. **State Notification**: Update state records via weekly reporting
5. **Documentation**: Maintain records of SR22 cancellation

## 9. Cross-References and Dependencies

### Program Integration
- **Base Program**: Aguila Dorada Texas Personal Auto Program (GR-63)
- **Driver Eligibility**: Must meet all program driver eligibility criteria
- **Vehicle Requirements**: Standard program vehicle requirements apply
- **Geographic Restrictions**: Texas residency requirement maintained

### System Dependencies
- **Policy Management System**: Integration with core policy processing
- **Document Generation**: Automated template creation capability
- **State Reporting Interface**: Weekly data submission to Texas DPS
- **Portal Integration**: Insured portal access for active policies

### Regulatory Framework
- **Texas Insurance Code**: Full compliance with state insurance regulations
- **DPS Requirements**: Alignment with Department of Public Safety SR22 specifications
- **Financial Responsibility Laws**: Supports Texas financial responsibility requirements

## Validation Standards
This document serves as the authoritative source for:
- **System Implementation**: Technical requirements for SR22/26 processing
- **Business Operations**: Procedural guidance for agents and underwriters
- **Compliance Verification**: Regulatory compliance measurement
- **Training Reference**: Staff training on SR22/26 processes

## Document Maintenance
- **Updates**: Changes to SR22/26 processes require document updates
- **Versioning**: Maintain version history for audit purposes
- **Approval Process**: All changes require business and compliance approval
- **Distribution**: Updates communicated to all stakeholders and system teams