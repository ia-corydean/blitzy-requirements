# Web Data Service API

# **Overview**

## **Standards**

ISO Claim Partners provides a web services API for programmatically submitting data to the system and requesting status updates.  The service is written using Microsoft Windows Communication Foundation (WCF) and hosted and bound over HTTPS with standards-compliant WSDL, which makes it compatible with a broad range of programming platforms.  Security is transmitted via message-level credentials; WS-Security compatibility is required.

# **API**

The available methods are as follows.

## **SubmitClaim**

Accept a single ClaimData parameter and returns a ClaimResult response.

ClaimResult SubmitClaim(ClaimData claim);

The ClaimResult will indicate the success/fail status of the submission and, if successful, return the claim status.

## **SubmitClaims**

Accepts an array of ClaimData objects and returns a corresponding array of ClaimResult objects.

IList\<ClaimResult\> SubmitClaims(IList\<ClaimData\> claims);

The returned list of ClaimResult objects will correspond to the list of submitted ClaimData objects (although not guaranteed to be in the same order).  Each ClaimResult object will indicate the success/fail status of the submission and, if successful, return the claim status.  It is possible for some submissions to succeed while others fail so it is necessary to check each response to verify successful submission.  You may send data for multiple RREs in a single submission.

## **GetClaimStatus2**

Accepts an RRE ID and an array of internal control numbers (ICNs) and returns a corresponding array of ClaimResult2 objects.

IList\<ClaimResult2\> GetClaimStatus2(string rreId, IList\<string\> icns);

You may only query a single RRE at a time but multiple ICNs for that RRE per request.

## **GetBeneficiaryEnrollment**

Accepts an RRE ID and an array of internal control numbers (ICNs) and returns a corresponding array of BeneficiaryResult objects containing Medicare enrollment information.

IList\<BeneficiaryResult\> GetBeneficiaryEnrollment(string rreId, IList\<string\> icns);

You may only query a single RRE at a time but multiple ICNs for that RRE per request.

## **GetUnsolicitedResponses**

Accepts an RRE ID and an array of internal control numbers (ICNs) and/or a date range from which the unsolicited responses were received and returns a corresponding array of UnsolicitedResult objects containing the unsolicited response file information.

IList\<UnsolicitedResult\> GetUnsolicitedResponses(string rreId, IList\<string\> icns, DateTime? fromDate, DateTime? toDate);

You may only query a single RRE at a time but multiple ICNs for that RRE per request. If you leave the list of ICNs empty, all results within the date range will be returned. If the date range is omitted, results from only the last month will be returned.

# **Data Types**

## **Submission Objects**

### **ClaimData**

This object encompasses the full range of data fields required by CMS for MMSEA Section 111 reporting as well as additional system-use fields.  All of the fields designed to hold CMS data points allow the same maximum size and values as the CMS spec mandates.  Note that the “Required” field in the table below is specific to submitting data via this API.  It is NOT intended to represent data points that are required/not required by CMS for Section 111 reporting.

For adds/updates (SubmitAction \= Upsert), provide all of the data fields on each submission – there is no “merging” of newly posted data with previously sent data.  A complete object should be sent each time.  For deletes, only the RRE ID and ICN are required along with SubmitAction \= Delete.  All other fields will be ignored.

| Field Name | Description | Req’d? | Data Type & Max Size | Rules/Notes |
| :---- | :---- | :---- | :---- | :---- |
| RREID | The RRE ID corresponding to the claim | Yes | String(9) | Digits only |
| ICN | Internal control number.  Uniquely identifies this claim in the system.  Updates to a claim must be submitted using the same ICN | Yes | String(30) |  |
| SubmitAction | Identifies add/update or delete | \*Required for delete | Action enumeration | “Upsert” will add or update – Default  “Delete” will delete |
| AdjusterKey | New Field Identifies adjuster handling claim | No | String(50) | Required for CP Link. |
| OperatingCompanyKey | New Field Identifies the company that has registered as the RRE | Yes | String(50) |  |
| UserRefNumber | User-specified arbitrary data for the claim | No | String(50) |  |
| ClaimStatus | Open/closed status identifier | No | ClaimStatusCode enumeration | Required for CP Link. If a customer is utilizing the CP Link process to programmatically refer claims for conditional payment investigation, only claims with an Open Claim Status will be included in the process (by default). Default is **Unknown.** |
| HICN | Medicare Health Insurance Claim Number | No | String(12) | Do not include dashes. May only contain digits 0 through 9, spaces, and/or letters. No special characters. |
| SSN | Social Security Number | No | String(9) | May contain only numbers. No dashes, hyphens or special characters allowed. |
| LastName | Surname of Injured Party | No | String(40) | First position must be an alphabetic character. Other positions may contain a letter, hyphen, apostrophe or space. |
| FirstName | Given or First Name of Injured Party.  | No | String(30) | May only contain letters and spaces Concurrent spaces are eliminated |
| MiddleInitial | First Letter of injured party middle name | No | String(1) | Upper and lower case letters only |
| Gender | The sex of the injured party | No | Gender Enumeration | May be one of the following: Male Female Unknown |
| DOB | Date of Birth of Injured Party | No | Date | Must contain a valid date prior to the current date. Format is YYYY-MM-DD. Numeric characters only 0 through 9\. No dates over 150 years in the past allowed |
| Street1 | Injured Party Address1 | No | String(75) | Required for Missing Data Smart Search (MDSS). Must contain only letters, numbers and/or spaces.  |
| Street2 | Injured Party Address2 | No | String(75) | Must have at least 2 alpha characters other positions may contain letters, numbers, space, comma, & \- ' . @ \# / ; :.  Must be blank if State \= "FC". |
| City | Injured Party City | No | String(75) | Required for Missing Data Smart Search (MDSS). May only contain letters, space, comma, & \- ' . @ \# / ; :.  Must be blank if State \= "FC". |
| State | Injured Party State | No | String(2) | Required for Missing Data Smart Search (MDSS). Must be US postal abbreviation corresponding to the US state. Use "FC" for foreign country. |
| ZipCode | 5-digit Zip Code for Injured Party | No | String(5) | Required for Missing Data Smart Search (MDSS). Must be 5 numerical digits Must be blank if State \= “FC”. |
| CmsDateOfIncident | Date of Incident as defined by CMS | No | Date | Must be a valid date prior to or equal to the current date. Format is YYYY-MM-DD. Numeric characters only 0 thru 9\. |
| DateOfIncident | Industry Date of Incident | No | Date | Field must contain a valid date prior to or equal to the current date. Format is YYYY-MM-DD. Numeric characters only 0 thru 9\. |
| CauseCode | Alleged Cause of Injury | No | String(7) |  |
| StateOfVenue | US postal abbreviation corresponding to the US state | No | String(2) |  |
| IcdIndicator | ICD-9/ICD-10 coding indicator | No | String(1) | Valid Values:9=ICD-90=ICD-10(blank)=ICD-9 |
| DiagCode01 | Diagnosis Code describing the alleged injury/illness | No | String(7) | Do not include decimals. Code must be on the list of 'valid' or 'included' ICD9 and ICD10 Diagnosis Codes published by CMS.  Valid codes can be found at: [https://www.cob.cms.hhs.gov/Section111/assets/section111/icd9.dx.codes.htm](https://www.cob.cms.hhs.gov/Section111/assets/section111/icd9.dx.codes.htm)  and [https://www.cob.cms.hhs.gov/Section111/assets/section111/icd10.dx.codes.htm](https://www.cob.cms.hhs.gov/Section111/assets/section111/icd10.dx.codes.htm) The value "NOINJ" may be used in limited circumstances.  If used, no other ICD9 or ICD10 codes may be submitted. Any applicable ICD codes should always be included when submitting a claim record. At least 1 ICD code is required for CP Link. |
| DiagCode02 | " | No | String(7) |  |
| DiagCode03 | " | No | String(7) |  |
| DiagCode04 | " | No | String(7) |  |
| DiagCode05 | " | No | String(7) |  |
| DiagCode06 | " | No | String(7) |  |
| DiagCode07 | " | No | String(7) |  |
| DiagCode08 | " | No | String(7) |  |
| DiagCode09 | " | No | String(7) |  |
| DiagCode10 | " | No | String(7) |  |
| DiagCode11 | " | No | String(7) |  |
| DiagCode12 | " | No | String(7) |  |
| DiagCode13 | " | No | String(7) |  |
| DiagCode14 | " | No | String(7) |  |
| DiagCode15 | " | No | String(7) |  |
| DiagCode16 | " | No | String(7) |  |
| DiagCode17 | " | No | String(7) |  |
| DiagCode18 | " | No | String(7) |  |
| DiagCode19 | " | No | String(7) |  |
| SelfInsured | Indication of whether the reportable event involves self-insurance as defined by CMS | No | String(1) | May be one of the following: Y N |
| SelfInsuredType | Identifies whether the self-insured is an organization or an individual. | No | String(1) | Must contain a value of I or O if the Self-Insured Indicator is Y. If the Self-Insured Indicator is N or space, must be blank. |
| PolicyHolderLastName | Surname of policyholder or self-insured | No | String(40) | First position must be an alpha character, other positions may contain letters, hyphens (dashes), apostrophes or spaces. Concurrent spaces are eliminated. |
| PolicyHolderFirstName | Given or First Name of policyholder or self-insured individual.  | No | String(30) | May only contain letters and spaces Concurrent spaces are eliminated. |
| DbaName | "Doing business as" Name of self-insured organization/business | No | String(70) | If supplied, must be at least 2 characters long. May also contain space|,|&|-|'|.|@|\#|/|;|:| |
| LegalName | Legal Name of self-insured organization/business | No | String(70) | If supplied, must be at least 2 characters long.  May also contain space|,|&|-|'|.|@|\#|/|;|:| |
| PlanType | Type of Insurance coverage or line of business provided by the plan policy or self-insurance.  | Yes | String(1) | Valid Values: D \= No-Fault E \= WC L \= Liability |
| PolicyNumber | The unique identifier for the policy under which the underlying claim was filled | No | String(30) | Must be at least 3 characters in length |
| PlanClaimNumber | The unique claim identifier by which the primary plan identifies the claim | Yes | String(30) |  |
| PlanContactDept | Name of Department for the Plan Contact to which claim-related communication and correspondence should be sent.  | No | String(70) |  |
| PlanContactLastName | Surname of individual that should be contacted at the plan for claim-related communication and correspondence | No | String(40) | If not left blank, first position must be an alphabetic character. Other positions may contain a letter, hyphen, apostrophe or space. |
| PlanContactFirstName | Given or first name of individual that should be contacted at the plan for claim-related communication and correspondence | No | String(30) | May only contain letters and spaces. If not left blank, first position must be an alphabetic character. Other positions must contain letters or spaces. |
| PlanContactPhone | Telephone number of individual that should be contacted at the plan for claim-related communication and correspondence | No | String(10) | Must contain 10-digit numeric value. |
| PlanContactExt | Telephone extension number of individual that should be contacted at the plan for claim-related communication and correspondence | No | String(5) |  |
| NoFaultLimit | Dollar amount of limit on no-fault insurance | No | Double | If Plan Insurance Type is D and there is no such dollar limit, send “999999999.99”, otherwise specify amount. Must use decimal. |
| NoFaultExhaust | Date on which limit was reached or benefits exhausted for No-Fault Insurance Limit | No | Date | Format is YYYY-MM-DD |
| RepIndicator | Code indicating the type of attorney/Other representative information provided | No | String(1) | Valid values:A \= AttorneyG \= Guardian/ConservatorP \= Power of AttorneyO \= OtherSpace \= None For CP Link customers, the Representative information provided here will also be utilized in the conditional payment investigation process. |
| RepLastName | Surname of Representative | No | String(40) | Embedded hyphens (dashes), apostrophes and spaces accepted. Concurrent spaces are eliminated. |
| RepFirstName | Given or First Name of representative | No | String(30) | May only contain letters and space. Concurrent spaces are eliminated. |
| RepFirmName | Representative's Firm Name | No | String(70) | If supplied, must be at least 2 alphanumeric characters long.  Concurrent spaces are eliminated. |
| RepTIN | Representative's Federal Tax Identification Number (TIN) | No | String(9) | Digits only, no hyphens. |
| RepAddress1 | First Line of the mailing address for the representative named above.  | No | String(50) | Must contain only letters, numbers and/or spaces. |
| RepAddress2 | Second line of the mailing address of the representative named above | No | String (50)  | Must contain only letters, numbers and/or spaces. Must be blank if State \= "FC". |
| RepCity | Mailing Address city for the representative named above | No | String(30) | Field may contain only alphabetic, Space, Comma, &—' . @ \# / ; : characters. No numeric characters allowed. Must be blank if State \= "FC". |
| RepState | US postal abbreviation corresponding to the US state | No | String(2) | USPS 2 character state abbreviation. Use “FC” for Foreign Country. |
| RepZipCode | 5-digit Zip Code for the Representative named above | No | String(5) | Must be blank if State \= "FC". |
| RepZipPlus4 | 4-digit Zip+4 Code for the Representative | No | String(4) | Must be blank if State \= "FC". |
| RepPhone | Telephone number of the representative named above | No | String(10) | Format with 3-digit area code followed by 7-digit phone number with no dashes or other punctuation. Must be blank if State \= "FC". |
| RepExt | Telephone Extension number of representative named above | No | String(5) | Must be blank if State \= "FC". |
| ORM | Indication of whether there is on-going responsibility for medicals (ORM) | No | TripleState Enumeration | Valid Values: Yes No Unknown |
| OrmTermDate | Date ongoing responsibility for medicals ended, where applicable | No | Date | Format is YYYY-MM-DD.  |
| TpocDate | Date of associated Total Payment Obligation to the Claimant (TPOC) without regard to ongoing responsibility for medicals (ORM). | No | Date | Format is YYYY-MM-DD.  |
| TpocAmount | Total Payment Obligation to the Claimant (TPOC) amount: Dollar amount of the total payment obligation to the claimant. | No | Double | Numeric digits and decimal point only |
| TpocDelayedFunding | If funding for the TPOC Amount 1 is delayed, provide actual or estimated date of funding. | No | Date | Format is YYYY-MM-DD.  |
| TpocDate2 | Date of associated Total Payment Obligation to the Claimant (TPOC) without regard to ongoing responsibility for medicals (ORM). | No | Date | Format is YYYY-MM-DD. |
| TpocAmount2 | Total Payment Obligation to the Claimant (TPOC) amount: Dollar amount of the total payment obligation to the claimant. | No | Double | Numeric digits and decimal point only |
| TpocDelayedFunding2 | If funding for the TPOC Amount 2 is delayed, provide actual or estimated date of funding. | No | Date | Format is YYYY-MM-DD. |
| TpocDate3 | Date of associated Total Payment Obligation to the Claimant (TPOC) without regard to ongoing responsibility for medicals (ORM). | No | Date | Format is YYYY-MM-DD. |
| TpocAmount3 | Total Payment Obligation to the Claimant (TPOC) amount: Dollar amount of the total payment obligation to the claimant. | No | Double | Numeric digits and decimal point only |
| TpocDelayedFunding3 | If funding for the TPOC Amount 3 is delayed, provide actual or estimated date of funding. | No | Date | Format is YYYY-MM-DD. |
| TpocDate4 | Date of associated Total Payment Obligation to the Claimant (TPOC) without regard to ongoing responsibility for medicals (ORM). | No | Date | Format is YYYY-MM-DD. |
| TpocAmount4 | Total Payment Obligation to the Claimant (TPOC) amount: Dollar amount of the total payment obligation to the claimant. | No | Double | Numeric digits and decimal point only |
| TpocDelayedFunding4 | If funding for the TPOC Amount 4 is delayed, provide actual or estimated date of funding. | No | Date | Format is YYYY-MM-DD. |
| TpocDate5 | Date of associated Total Payment Obligation to the Claimant (TPOC) without regard to ongoing responsibility for medicals (ORM). | No | Date | Format is YYYY-MM-DD. |
| TpocAmount5 | Total Payment Obligation to the Claimant (TPOC) amount: Dollar amount of the total payment obligation to the claimant. | No | Double | Numeric digits and decimal point only |
| TpocDelayedFunding5 | If funding for the TPOC Amount 5 is delayed, provide actual or estimated date of funding. | No | Date | Format is YYYY-MM-DD. |
| MsaAmount | Medicare Set-Aside (MSA) Amount | No | Double  | Numeric digits and decimal point only For $0 MSAs, send 0\. If no MSA completed, send 0\. |
| MsaPeriod | Amount of time in years that the MSA is expected to cover the beneficiary | No | Integer | Valid Values: 0-99 |
| PayoutIndicator | Lump Sum or Structured/Annuity Payout Indicator | No | String(1) | Valid Values: S \= Structured/Annuity L \= Lump Sum |
| InitialDeposit | Initial deposit amount | No | Double | Numeric digits and decimal point only |
| AnnualDeposit | Anniversary (annual) Deposit amount | No | Double | Numeric digits and decimal point only |
| CaseControlNo | Case ID for WCMSAs | No | String(15) | 2 alpha characters (WC) with 13 numeric characters following |
| AdminEIN | EIN of Professional Administrator, if applicable | No | String(9) | May contain only numbers |
| PlanContactEmail | Used to pass the plan’s contact e-mail address | No | String(100) |  |
| NonTrauma | Non-trauma indicator to identify claims which involved ingestion, implantation, or exposure (default is ‘Unknown’) | No | TripleState Enumeration | Valid Values: Yes No Unknown |
| SettlementStatus | Identifies the settlement status for MSP service identification | No | String(8) | May be one of the following: Open Proposed Settled |
| TotalProposedSettlementAmount | Total proposed settlement amount | No | Double | Numeric digits and decimal point only |
| AverageWeeklyWage | Beneficiary average weekly wage | No | Double | Numeric digits and decimal point only |
| ImpairmentPercentage | Permanent impairment percentage  | No | Double | Numeric digits and decimal point only Format: 99.90 99.99 100.00 |
| TotalLostTimeDays | Total lost time (in days) | No | Integer | 1 to 4 digits only |
| MedicalReserve | Medical claim reserve | No | Double | Numeric digits and decimal point only |
| Indemnity Reserve | Indemnity claim reserve | No | Double | Numeric digits and decimal point only |
| MedicalTotalPaid | Medical Total Paid | No | Double | Numeric digits and decimal point only |
| ClaimNoteType | Claim note type (P4S) Code indicating  settlement has been encountered in the client source system | No | TripleState Enumeration | Valid Values: **Yes** \- Claim Note Type Indicating Settlement Encountered **No** \- No claim note indicating settlement encountered **Unknown**  Use to indicate if claim is positioned for settlement. Can be configured to be part of CP Link logic. Used for MSA Recommendations. |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

## **Response Objects**

### **ClaimResult**

For each ClaimData object submitted, a corresponding ClaimResult object will be returned.  The ClaimResult contains status information about the submission.  Either an “OK” or “ERROR” confirmation and, if “OK”, a ClaimStatus object with the current status of the claim is returned.

| Field | Description | Data Type |
| :---- | :---- | :---- |
| Status | Either “OK” or “ERROR” depending on the successful processing of the corresponding request. | String |
| StatusDetail | Details of the error if Status \= ERROR | String |
| StatusObject | The current status of the claim in the system (may be NULL if Status \= ERROR) | ClaimStatus |

### **ClaimResult2**

ClaimResult2 contains status information about the most recent submission to the API.  Either an “OK” or “ERROR” confirmation and, if “OK”, a ClaimStatus2 object with the current status of the claim.

| Field | Description | Data Type |
| :---- | :---- | :---- |
| Status | Either “OK” or “ERROR” depending on the successful processing of the corresponding request. | String |
| StatusDetail | Details of the error if Status \= ERROR | String |
| StatusObject | The current status of the claim in the system (may be NULL if Status \= ERROR) | ClaimStatus2 |

### **BeneficiaryResult**

BeneficiaryResult returns enrollment information for a Medicare beneficiary based on data received from CMS in the query response files.  Either an “OK” or “ERROR” confirmation and, if “OK”, a BeneficiaryEnrollment object with the current enrollment information for the beneficiary.

| Field | Description | Data Type |
| :---- | :---- | :---- |
| Status | Either “OK” or “ERROR” depending on the successful processing of the corresponding request. | String |
| StatusDetail | Details of the error if Status \= ERROR | String |
| StatusObject | The current beneficiary enrollment information for the claim in the system (may be NULL if Status \= ERROR) | BeneficiaryEnrollment |

### **ClaimStatus**

Reportable means the claim should have a reportable TPOC or ORM and received a positive query response. IsReady is populated based on the following Validations:

1. IsReportingReady \= 1  
2. Nextactiontype \= Add, Delete/Add, or Update  
3. ReadyToBeReportedFlag \= Y

| Field | Description | Data Type |
| :---- | :---- | :---- |
| RREID | RRE ID submitted on the ClaimData object | String(9) |
| ICN | ICN submitted on the ClaimData object | String(30) |
| UserRefNumber | User-specified arbitrary data for the claim | String(50) |
| HICN | The HICN if the claimant was found to be a Medicare beneficiary | String(12) |
| Reportable | Yes/No flag indicating the reportable status of the claim | Boolean |
| BeneficiaryStatus | Returns the beneficiary status as one of the following values “Yes”, “No”, “Unknown”, or “Dupe” | String(7) BeneficiaryStatus \= Yes, will be eligible for CP Link. |
| IsReady | Yes/No flag indicating whether or not the claim has passed all validation checks and is ready for reporting | Boolean |
| LastCmsSubmitDate | The date this claim was last submitted to CMS, if any | DateTime (nullable) |
| ResponseCodes | List of validation, error, and/or compliance flags | Array of ResponseCode objects |
| NextReportDate | Next scheduled reporting date for this claim | DateTime (nullable) |
| NextQueryDate | Next scheduled query date for this claim | DateTime (nullable) |
| DiagnosisCodeLock | Yes/No flag indicating whether or not the diagnosis codes have been locked by ISO Claim Partners | Boolean |
| IcdVersion | Indicates the ICD coding version selected for the claim (either “9” for ICD-9 or “0” for ICD-10).  Only provided if DiagnosisCodeLock \= TRUE | String(1) |
| DiagnosisCodes | A list of ICD-9/10 diagnosis codes assigned to the claim. Only provided if DiagnosisCodeLock \= TRUE | Dictionary\<int, string\> |
| CPStatus | ISO Claim Partners CP status; one of the following values: CP Search Recommended CP Search In-Process Interim Amount Obtained CP Negotiations In Process Final Demand Received and Submitted CP Resolved and Closed | String(50) |
| CPActionDates | Last CP activity dates | Array of DateTime objects |
| CPInterimAmount | The interim determined CP amount, if any | Double (nullable) |
| FinalDemandAmount | The final demand amount, if any | Double (nullable) |
| MSAStatus | The ISO Claim Partners MSA status; one of the following values: Referral Received In Process Prepared but not CMS Approved Submitted to CMS Approved | String(50) |
| MSAActionDates | Last MSA activity date | Array of DateTime objects |
| MSPRecommendedAmount | The recommended MSP amount, if any | Double (nullable) |
| MSAApprovedAmount | The approved MSA amount, if any | Double (nullable) |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

### **ClaimStatus2**

ClaimStatus2 contains all the fields that ClaimStatus does, plus the additional fields listed below.

| Field | Description | Data Type |
| :---- | :---- | :---- |
| *All fields in ClaimStatus are included in ClaimStatus2 plus the following*  |  |  |
| FirstQueryMatchDate | Date the claimant was first identified as a Medicare beneficiary | DateTime (nullable) |
| LastQueryDate | Date the claimant was last queried for updated beneficiary status and enrollment info | DateTime (nullable) |
| CmsDispos | Disposition code from the last reporting submission to CMS | String(2) |

### **ResponseCode**

| Field | Description | Data Type |
| :---- | :---- | :---- |
| CmsCode | The CMS-provided (or CMS-equivalent) error/compliance code | String(5) |
| CodeType | The code type (“E” for errors, “C” for compliance) | String(1) |
| Description | Detailed description of the error code | String(100) |
| Origin | Identifies the origin of the code; current possible values are: “CMS” for CMS-returned codes “MIRX” for system-generated validation warnings | String(20) |

### **BeneficiaryEnrollment**

| Field | Description | Data Type |
| :---- | :---- | :---- |
| RREID | RRE ID under which the beneficiary’s claim record is filed | String(9) |
| ICN | ICN for the beneficiary’s claim record | String(30) |
| UserRefNumber | User-specified arbitrary data for the claim | String(50) |
| HICN | Medicare-assigned MBI/HICN of the beneficiary | String(12) |
| EnrollmentDataChangeDate | Last date the Medicare enrollment information changed | DateTime (nullable) |
| FirstQueryMatchDate | Date the claimant was first identified as a Medicare beneficiary | DateTime (nullable) |
| LastQueryDate | Date the claimant was last queried for updated beneficiary status and enrollment info | DateTime (nullable) |
| PartA | Medicare Part A enrollment effective and termination dates | EnrollmentDates |
| PartB | Medicare Part B enrollment effective and termination dates | EnrollmentDates |
| PartC | Medicare Part C most recent and prior enrollment information | Array of MapEnrollmentInfo |
| PartD | Medicare Part C most recent and prior enrollment information | Array of MapEnrollmentInfo |

### **EnrollmentDates**

| Field | Description | Data Type |
| :---- | :---- | :---- |
| EffectiveDate | Enrollment effective date | DateTime (nullable) |
| TerminationDate | Enrollment termination date | DateTime (nullable) |

### **MapEnrollmentInfo**

| Field | Description | Data Type |
| :---- | :---- | :---- |
| EffectiveDate | Enrollment effective date | DateTime (nullable) |
| TerminationDate | Enrollment termination date | DateTime (nullable) |
| PlanContractNumber | Plan contract number | String(5) |
| PlanContractName | Plan contract name | String(50) |
| PbpNumber | Plan benefit package number | String(3) |
| PlanContractAddress1 | Plan contract address line 1 | String(55) |
| PlanContractAddress2 | Plan contract address line 2 | String(55) |
| PlanContractCity | Plan contract address city | String(30) |
| PlanContractState | Plan contract address state | String(2) |
| PlanContractZipCode | Plan contract address zip code | String(9) |

# **C\# Code Examples**

Once you have referenced in the web service using the WSDL file, you can instantiate a proxy object and set up the credentials as follows:

DataServiceClient client \= new DataServiceClient();  
client.Endpoint.Address \=  
new System.ServiceModel.EndpointAddress("https://domain/api/DataService.svc");

client.ClientCredentials.UserName.UserName \= "username";  
client.ClientCredentials.UserName.Password \= "P@$$word";

Once you have your proxy, you instantiate a ClaimData transport object, assign its properties, and submit the call to the service.

ClaimData cd \= new ClaimData();  
              
// set the properties of the cd object here

ClaimResult r \= client.SubmitClaim(cd);

The response object processing can be handled however needed.  A simple example (demonstrating a call from a console application) processing the response is below.

private static void OutputResponse(ClaimResult r)  
{  
    Console.WriteLine("Response is: {0} {1}", r.Status, r.StatusDetail);  
    if (r.Status \== "OK")  
    {  
        var s \= r.StatusObject;

        Console.WriteLine("RRE: {0}", s.RREID);  
        Console.WriteLine("ICN: {0}", s.ICN);  
        Console.WriteLine("Beneficiary Status: {0}", s.BeneficiaryStatus);  
        Console.WriteLine("HICN: {0}", s.HICN);  
        Console.WriteLine("Reportable Status: {0}", s.Reportable);  
        Console.WriteLine("User Defined 1: {0}", s.UserDefined1);  
        Console.WriteLine("User Defined 2: {0}", s.UserDefined2);  
        Console.WriteLine("IsReady: {0}\\n\# Errors: {1}", s.IsReady, s.ResponseCodes.Length);  
        foreach (var code in s.ResponseCodes)  
        {  
            Console.WriteLine("  {0} / {1}", code.CmsCode, code.Description);  
        }  
    }  
    else  
        // handle the error here  
}

# **Technical Communications Details**

The API uses TLS 1.2 encryption to secure all communications.  Credentials are passed as part of the SOAP envelope using WS-Security.  If you are using .NET Framework, importing the WSDL file into Visual Studio will automatically configure the proxy to use the proper WS-Security messages.

If you are connecting to the API using a different code platform (including testing tools such as Postman or SoapUI), you will need to make sure you configure the security properly in order to successfully submit requests to the API.  Failing to do so will result in 400 or 500 HTTP responses.

The WS-Security header will look like the following example:

  \<s:Envelope xmlns:s\="http://schemas.xmlsoap.org/soap/envelope/" xmlns:u\="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"\>  
    \<s:Header\>  
      \<o:Security xmlns:o\="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" s:mustUnderstand\="1"\>  
        \<u:Timestamp u:Id\="\_0"\>  
          \<u:Created\>2020-06-24T13:15:00.000Z\</u:Created\>  
          \<u:Expires\>2020-06-24T13:17:00.000Z\</u:Expires\>  
        \</u:Timestamp\>  
        \<o:UsernameToken u:Id\="uuid-0e84f1c6-0be8-439d-a920-673f7257f0b4-50"\>  
          \<o:Username\>assigned-username-here\</o:Username\>  
          \<o:Password Type\="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0\#PasswordText"\>password-here\</o:Password\>  
        \</o:UsernameToken\>  
      \</o:Security\>  
    \</s:Header\>  
    \<s:Body\>  
    :  
    :  
    \</s:Body\>  
\</s:Envelope\>

Important details:

* The **Timestamp** is designed to prevent replay attacks on the API.  The **Created** time should be the time your system formulates the request.  The **Expires** time should be a small interval of time in the future (less than 5 minutes \- 1 minute is typical).  The request must arrive at the server within this time window to be accepted.  If the window is more than 5 minutes, the server may reject the request.  
* **Password** must be specified with the **Type** attribute as shown in the example above.  The password should be sent in standard XML text (i.e. do not Base-64 encode the password).

SoapUI has built-in support for configuring WS-Security headers on requests.  See the following documentation for details: [https://www.soapui.org/soapui-projects/ws-security/](https://www.soapui.org/soapui-projects/ws-security/)

# **Revision History**

2021.08.04	Initial version  
2022.10.25	Added fields for Injured Party address   
2023.08.03	Added endpoint for Unsolicited Response file data  
2024.05.01	Added WCMSA fields  
2024.09.01	Removed fields no longer in use. Note these will still be in wsdl file.  
2025.05.28	Added information on Reportable and IsReady, and updated Req’d for OperatingCompanykey and PlanType. Added additional information for the Data Type Rules/Notes including MDSS and CP Link requirements.

