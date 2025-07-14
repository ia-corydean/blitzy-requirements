**Sample Request**

\<Request\>  
    \<Header\>  
        \<Authorization\>  
            \<OrgId\>111111\</OrgId\>  
            \<ShipId\>111111\</ShipId\>  
        \</Authorization\>  
        \<Quoteback\>LSP-Sample request\</Quoteback\>  
    \</Header\>  
    \<Body\>  
        \<Drivers\>  
            \<Driver\>  
                \<GivenName\>YUKI\</GivenName\>  
                \<Surname\>BONZHEIM\</Surname\>  
                \<DOB\>19900311\</DOB\>  
            \</Driver\>  
        \</Drivers\>  
        \<Addresses\>  
            \<Address\>  
                \<AddressType\>Current\</AddressType\>  
                \<Street1\>7827 ADELAIDE LP\</Street1\>  
                \<City\>NEW PORT RICHEY\</City\>  
                \<StateCode\>FL\</StateCode\>  
                \<Zip\>34655\</Zip\>  
            \</Address\>  
        \</Addresses\>  
    \</Body\>  
\</Request\>

**Response Codes**

* 200 (Success):  Upon successful call, the service will return a 200 response along with the data requested. No hits will return an empty body with http status 200\.  
* 400 (Bad Request): There was a problem with the formatted request to the service.   
* 401 (Unauthorized): The access\_token you provided has expired and is no longer valid. Please retrieve a new one from the Security Token Service  
* 403 (Forbidden): The credentials supplied on the request are not authorized to access this resource.  
* 588 (Bad Response): An error occurred while performing response validation.  
* 500 (Internal Server Error): An error occurred while processing the request.

**Sample Response**

 

\<Response xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"\>

    \<Header\>

        \<TransactionId\>15446763-7f06-4452-b988-f77fb994a494\</TransactionId\>

        \<Quoteback\>LSP-Sample request\</Quoteback\>

    \</Header\>

    \<Body\>

        \<StatusCode\>200\</StatusCode\>

        \<CompleteQuote\>

            \<QuoteScores\>

                \<ApplicationCompletenessCode\>A3\</ApplicationCompletenessCode\>

                \<RatingCompletenessCode\>ACA\</RatingCompletenessCode\>

            \</QuoteScores\>

            \<Messages\>

                \<Message\>

                    \<Code\>101\</Code\>

                    \<Description\>Vehicles, applicant, and additional subjects found.\</Description\>

                \</Message\>

            \</Messages\>

            \<RiskCheckScoreSummary\>

                \<RiskGroup\>VERY HIGH\</RiskGroup\>

                \<ScoreColor\>RED\</ScoreColor\>

                \<TotalScore\>3588\</TotalScore\>

                \<IsCRAWarning\>false\</IsCRAWarning\>

                \<IsFraudIndicator\>false\</IsFraudIndicator\>

                \<ScoreDecile\>8\</ScoreDecile\>

                \<CreditHeader\>N\</CreditHeader\>

            \</RiskCheckScoreSummary\>

            \<Policies\>

                \<Policy\>

                    \<Carrier\>

                        \<Name\>INSURANCE SERVICES O\</Name\>

                        \<AMBEST\>99999\</AMBEST\>

                        \<NAIC\>00000\</NAIC\>

                    \</Carrier\>

                    \<PolicyNumber\>VRSKLSP201810021001\</PolicyNumber\>

                    \<PolicyStatus\>INFORCE\</PolicyStatus\>

                    \<PolicyType\>

                        \<Code\>AU\</Code\>

                        \<Description\>Auto\</Description\>

                    \</PolicyType\>

                    \<CompOnlyPolicy\>N\</CompOnlyPolicy\>

                    \<PolicyReportedDate\>20230213\</PolicyReportedDate\>

                    \<InceptionDate\>20170301\</InceptionDate\>

                    \<LastReportedTermEffectiveDate\>20230105\</LastReportedTermEffectiveDate\>

                    \<LastReportedTermExpirationDate\>20240105\</LastReportedTermExpirationDate\>

                    \<NumberOfCancellations\>0\</NumberOfCancellations\>

                    \<NumberOfRenewals\>3\</NumberOfRenewals\>

                    \<MatchBasisInformation\>

                        \<MatchScore\>100\</MatchScore\>

                        \<SearchType\>

                            \<Code\>P\</Code\>

                            \<Description\>Person\</Description\>

                        \</SearchType\>

                        \<MatchReasons\>

                            \<MatchReason\>NAME IS IDENTICAL\</MatchReason\>

                            \<MatchReason\>ADDRESS IS IDENTICAL\</MatchReason\>

                            \<MatchReason\>ZIP IS IDENTICAL\</MatchReason\>

                        \</MatchReasons\>

                    \</MatchBasisInformation\>

                    \<Coverages\>

                        \<Coverage\>

                            \<CoverageType\>

                                \<Code\>BINJ\</Code\>

                                \<Description\>Bodily Injury\</Description\>

                            \</CoverageType\>

                            \<IndividualLimitAmount\>40000\</IndividualLimitAmount\>

                            \<OccurrenceLimitAmount\>80000\</OccurrenceLimitAmount\>

                            \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                            \<FromDate\>20230105\</FromDate\>

                            \<ToDate\>20240105\</ToDate\>

                        \</Coverage\>

                        \<Coverage\>

                            \<CoverageType\>

                                \<Code\>CBSL\</Code\>

                                \<Description\>CSL (BI \&amp; PD)\</Description\>

                            \</CoverageType\>

                            \<IndividualLimitAmount\>0\</IndividualLimitAmount\>

                            \<OccurrenceLimitAmount\>0\</OccurrenceLimitAmount\>

                            \<CombinedSingleLimitAmount\>80000\</CombinedSingleLimitAmount\>

                            \<FromDate\>20230105\</FromDate\>

                            \<ToDate\>20240105\</ToDate\>

                        \</Coverage\>

                        \<Coverage\>

                            \<CoverageType\>

                                \<Code\>PDMG\</Code\>

                                \<Description\>Property Damage\</Description\>

                            \</CoverageType\>

                            \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                            \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                            \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                            \<FromDate\>20230105\</FromDate\>

                            \<ToDate\>20240105\</ToDate\>

                        \</Coverage\>

                        \<Coverage\>

                            \<CoverageType\>

                                \<Code\>UMPD\</Code\>

                                \<Description\>Uninsured Motorist (PD)\</Description\>

                            \</CoverageType\>

                            \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                            \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                            \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                            \<FromDate\>20230105\</FromDate\>

                            \<ToDate\>20240105\</ToDate\>

                        \</Coverage\>

                        \<Coverage\>

                            \<CoverageType\>

                                \<Code\>PINJ\</Code\>

                                \<Description\>Personal Injury\</Description\>

                            \</CoverageType\>

                            \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                            \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                            \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                            \<FromDate\>20230105\</FromDate\>

                            \<ToDate\>20240105\</ToDate\>

                        \</Coverage\>

                    \</Coverages\>

                    \<PolicyHolders\>

                        \<PolicyHolder\>

                            \<GivenName\>DOUGLAS\</GivenName\>

                            \<MiddleName\>J\</MiddleName\>

                            \<Surname\>BONZHEIM\</Surname\>

                            \<DOB\>19760101\</DOB\>

                            \<DLNumber\>M888777666555\</DLNumber\>

                            \<DLState\>FL\</DLState\>

                        \</PolicyHolder\>

                        \<PolicyHolder\>

                            \<GivenName\>LORNA\</GivenName\>

                            \<MiddleName\>P\</MiddleName\>

                            \<Surname\>BONZHEIM\</Surname\>

                            \<DOB\>20030923\</DOB\>

                            \<DLNumber\>B640693682100\</DLNumber\>

                            \<DLState\>FL\</DLState\>

                        \</PolicyHolder\>

                    \</PolicyHolders\>

                    \<PhoneNumbers\>

                        \<PhoneNumber\>

                            \<PhoneType\>H\</PhoneType\>

                            \<Number\>1112223335\</Number\>

                            \<Extension\>0000\</Extension\>

                        \</PhoneNumber\>

                    \</PhoneNumbers\>

                    \<Addresses\>

                        \<Address\>

                            \<AddressType\>Mailing\</AddressType\>

                            \<Street1\>7827 Adelaide Loop\</Street1\>

                            \<City\>New Port Richey\</City\>

                            \<StateCode\>FL\</StateCode\>

                            \<Zip\>34655\</Zip\>

                            \<FromDate\>20230105\</FromDate\>

                            \<ToDate\>20240105\</ToDate\>

                        \</Address\>

                    \</Addresses\>

                \</Policy\>

            \</Policies\>

            \<CoverageLapseInformation\>

                \<SearchPerson\>

                    \<GivenName\>YUKI\</GivenName\>

                    \<Surname\>BONZHEIM\</Surname\>

                    \<InputDriverSequenceNumber\>1\</InputDriverSequenceNumber\>

                    \<HasPossibleLapse\>N\</HasPossibleLapse\>

                    \<IsCurrentInforceCoverage\>Y\</IsCurrentInforceCoverage\>

                    \<CoverageIntervals\>

                        \<CoverageInterval\>

                            \<Carrier\>

                                \<Name\>INSURANCE SERVICES O\</Name\>

                                \<AMBEST\>99999\</AMBEST\>

                                \<NAIC\>00000\</NAIC\>

                                \<FinancialAMBEST\>99999\</FinancialAMBEST\>

                            \</Carrier\>

                            \<StartDate\>20220105\</StartDate\>

                            \<EndDate\>20240105\</EndDate\>

                            \<NumberOfCoverageDays\>628\</NumberOfCoverageDays\>

                            \<HasBreakFromPriorCoverage\>NA\</HasBreakFromPriorCoverage\>

                            \<NumberOfLapseDays\>0\</NumberOfLapseDays\>

                        \</CoverageInterval\>

                    \</CoverageIntervals\>

                \</SearchPerson\>

            \</CoverageLapseInformation\>

            \<Addresses\>

                \<Address\>

                    \<AddressType\>Current Standardized\</AddressType\>

                    \<Street1\>7827 Adelaide Loop\</Street1\>

                    \<City\>New Port Richey\</City\>

                    \<StateCode\>FL\</StateCode\>

                    \<Zip\>346552733\</Zip\>

                    \<CountyName\>Pasco\</CountyName\>

                    \<FIPSCountyCd\>12101\</FIPSCountyCd\>

                    \<DPVFootnote\>AABB\</DPVFootnote\>

                    \<RecordType\>S\</RecordType\>

                    \<AddressResultCodes\>

                        \<AddressResultCode\>AC11\</AddressResultCode\>

                        \<AddressResultCode\>AS01\</AddressResultCode\>

                    \</AddressResultCodes\>

                    \<Latitude\>28.211155\</Latitude\>

                    \<Longitude\>-82.684826\</Longitude\>

                \</Address\>

            \</Addresses\>

            \<HouseholdInformation\>

                \<Youths11to15\>4\</Youths11to15\>

                \<Youths16to17\>4\</Youths16to17\>

                \<DwellingType\>S\</DwellingType\>

                \<HomeOwner\>T\</HomeOwner\>

                \<LengthofResidence\>2\</LengthofResidence\>

                \<HouseholdEducation\>5\</HouseholdEducation\>

                \<SOHOIndicatorHousehold\>Y\</SOHOIndicatorHousehold\>

                \<HouseholdSize\>5\</HouseholdSize\>

                \<NetWorth\>B\</NetWorth\>

            \</HouseholdInformation\>

            \<Subjects\>

                \<Subject\>

                    \<Sequence\>1\</Sequence\>

                    \<DataSource\>Principal\</DataSource\>

                    \<IsSubjectVerified\>true\</IsSubjectVerified\>

                    \<IsSubjectActiveDuringMostRecentTerm\>true\</IsSubjectActiveDuringMostRecentTerm\>

                    \<EntityScore\>95\</EntityScore\>

                    \<GivenName\>YUKI\</GivenName\>

                    \<MiddleName\>R\</MiddleName\>

                    \<Surname\>BONZHEIM\</Surname\>

                    \<PrimarySourceInfo\>

                        \<DOB\>19900311\</DOB\>

                        \<Gender\>M\</Gender\>

                        \<MaritalStatus\>S\</MaritalStatus\>

                        \<DLNumber\>T520103597610\</DLNumber\>

                        \<DLState\>FL\</DLState\>

                        \<RelationToPolicyHolder\>LD\</RelationToPolicyHolder\>

                        \<RelationToInsured\>O\</RelationToInsured\>

                        \<FromDate\>20230105\</FromDate\>

                        \<ToDate\>20240105\</ToDate\>

                    \</PrimarySourceInfo\>

                    \<SecondarySourceInfo\>

                        \<DOB\>19900311\</DOB\>

                        \<Gender\>M\</Gender\>

                        \<MaritalStatus\>S\</MaritalStatus\>

                        \<MatchType\>N\</MatchType\>

                        \<VerificationDate\>20220715\</VerificationDate\>

                        \<VerificationRange\>2\</VerificationRange\>

                        \<DriverAssuranceScore\>D1\</DriverAssuranceScore\>

                        \<InternalDriverCode\>7\</InternalDriverCode\>

                    \</SecondarySourceInfo\>

                    \<ReasonCodeDetails\>

                        \<Reason\>

                            \<Code\>ID-1.11\</Code\>

                            \<Description\>No identity located or poor match on primary data source.\</Description\>

                        \</Reason\>

                        \<Reason\>

                            \<Code\>ID-1.12\</Code\>

                            \<Description\>Social Security Number not validated.\</Description\>

                        \</Reason\>

                        \<Reason\>

                            \<Code\>ID-1.13\</Code\>

                            \<Description\>Date of Birth not validated.\</Description\>

                        \</Reason\>

                        \<Reason\>

                            \<Code\>ID-1.31\</Code\>

                            \<Description\>Input Address(es), including current and former, did not match to any of the addresses contained in the primary data source.\</Description\>

                        \</Reason\>

                        \<Reason\>

                            \<Code\>AG-2.17\</Code\>

                            \<Description\>Input Address(es) including current and former did not match to any of the addresses contained in the primary data source.\</Description\>

                        \</Reason\>

                    \</ReasonCodeDetails\>

                    \<ActionMessages\>

                        \<ActionMessage\>Ask for Drivers License and Utility Bill\</ActionMessage\>

                    \</ActionMessages\>

                    \<MotorVehicleReports\>

                        \<MotorVehicleReport\>

                            \<Status\>

                                \<Code\>V\</Code\>

                                \<Description\>NON-CLEAR report\</Description\>

                            \</Status\>

                            \<ViolationsType\>

                                \<Code\>C\</Code\>

                                \<Description\>Report passed through Custom violation code/point process\</Description\>

                                \<PointTotal\>0\</PointTotal\>

                            \</ViolationsType\>

                            \<DMVReportDate\>20201120\</DMVReportDate\>

                            \<DriversPrivacyProtectionActFlag\>N\</DriversPrivacyProtectionActFlag\>

                            \<Driver\>

                                \<Name\>BONZHEIM, YUKI\</Name\>

                                \<CityStateZip\>NEW PORT RICHEY, FL 34655\</CityStateZip\>

                                \<Street1\>7827 ADELAIDE LP\</Street1\>

                                \<DLNumber\>T520103597610\</DLNumber\>

                                \<DLState\>FL\</DLState\>

                                \<DOB\>19900311\</DOB\>

                                \<Gender\>M\</Gender\>

                                \<Height\>6'1\</Height\>

                                \<License\>

                                    \<Class\>E\</Class\>

                                    \<Status\>VALID\</Status\>

                                    \<IssuedDate\>20131001\</IssuedDate\>

                                    \<ExpirationDate\>20210801\</ExpirationDate\>

                                    \<OriginalIssueDate\>20001201\</OriginalIssueDate\>

                                \</License\>

                                \<Detail\>Order Number : 935983239 \- OrderType : MvrIndicator \- REQUESTED AS: YUKI                      BONZHEIM                  DOB: 03111990  LICENSE : T520103597610 PERS:01: ACTIVE          VALID   E              1001201308012021 LIC CLASS: E                       DESC: OPERATOR LIC STATUS: VALID LIC ISSUED: 10/01/2021 LIC EXPIRES: 08/01/2029 PERS:02: EXPIRED         EXPIRED ID CARD        1201200910012014 LIC CLASS: ID CARD                 DESC: ID CARD LIC STATUS: EXPIRED LIC ISSUED: 12/01/2009 LIC EXPIRES: 10/01/2014 AS OF NOVEMBER 20, 2020 AT 9:50:20 AM, DRIVER PRIVILEGE T520-103-59-761-0 IS VALID. PERSONAL INFORMATION IS PROTECTED PURSUANT TO THE DRIVER PRIVACY PROTECTION ACT. ENTRIES BELOW ARE A THREE YEAR RECORD. ORIGINAL ISSUE DATE: 12/01/2000 REAL ID COMPLIANT ORGAN DONOR US CITIZEN BLOCKED PERSONAL INFORMATION BLOCKED FOR MAILING LIST PERSON HAS A DIGITAL IMAGE ELIGIBLE TO ELECT DRIVER SCHOOL.  DRIVER HAS MADE 2 ELECTIONS. LAST ELECTION WAS ON 02/01/2012. VIOLATIONS COMMITTED WHILE A CDL HOLDER OR IN A CMV VEHICLE ARE NOT ELIGIBLE FOR DRIVING SCHOOL ELECTION. COUNTY: MIAMI-DADE RESIDENTIAL ADDRESS: 2570 NW 48TH ST  MIAMI, FL  33142  COUNTY: MIAMI-DADE ISSUANCE HISTORY: LIC CLASS: ID CARD   ISSUE DATE: 12/01/1996   ISSUE TYPE: DUPLICATE LIC CLASS: ID CARD   ISSUE DATE: 12/01/2000   ISSUE TYPE: DUPLICATE LIC CLASS: CLASS E   ISSUE DATE: 05/01/2002   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 02/01/2003   ISSUE TYPE: DUPLICATE LIC CLASS: ID CARD   ISSUE DATE: 07/01/2006   ISSUE TYPE: DUPLICATE LIC CLASS: CLASS E   ISSUE DATE: 04/01/2009   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 02/01/2010   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 02/01/2010   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 08/01/2012   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 10/01/2013   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 10/01/2014   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 03/01/2018   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 10/01/2020   ISSUE TYPE: CDR/CDT CLEARANCE EXAMS TAKEN: VISION               DATE TAKEN: 10/01/2021   COUNT: 2   STATUS: PASS ROAD SIGN            DATE TAKEN: 12/01/2021   COUNT: 1   STATUS: PASS ROAD RULES           DATE TAKEN: 12/01/2020   COUNT: 3   STATUS: PASS DRIVING              DATE TAKEN: 12/01/2020   COUNT: 1   STATUS: PASS This report is generated for insurance purposes only and may not be used for any other purpose.  The use and dissemination of the report and information in it must comply with your iiX agreement and the  Fair Credit Reporting Act, the Driver's Privacy Protection Act, and any applicable state statute(s).  The data in the report from the applicable state agency or service bureau is provided through iiX "as is." \--- Customer-defined MVR scoring has been applied to this record.  Customer  is solely responsible for the application and use of the resulting score.\</Detail\>

                                \<Violations\>

                                    \<Violation\>

                                        \<Type\>SUSP\</Type\>

                                        \<ViolationDate\>20220301\</ViolationDate\>

                                        \<CustomCode\>130110\</CustomCode\>

                                        \<CustomPoints\>3\</CustomPoints\>

                                        \<Detail\>Order Number : 935983239 \- FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 720198716 NOTICED PROVIDED: 12/01/2021 ADDED TO RECORD: 12/01/2021 SANCTION CODE: 7\</Detail\>

                                    \</Violation\>

                                    \<Violation\>

                                        \<Type\>REIN\</Type\>

                                        \<ConvictionDate\>20220301\</ConvictionDate\>

                                        \<CustomCode\>330130\</CustomCode\>

                                        \<CustomPoints\>-3\</CustomPoints\>

                                        \<Detail\>Order Number : 935983239 \- REINSTATED\</Detail\>

                                    \</Violation\>

                                    \<Violation\>

                                        \<Type\>SUSP\</Type\>

                                        \<ViolationDate\>20211001\</ViolationDate\>

                                        \<CustomCode\>130110\</CustomCode\>

                                        \<CustomPoints\>3\</CustomPoints\>

                                        \<Detail\>Order Number : 935983239 \- FR-REGISTRATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 830175467 NOTICED PROVIDED: 09/01/2021 ADDED TO RECORD: 09/01/2021 SANCTION CODE: 8\</Detail\>

                                    \</Violation\>

                                    \<Violation\>

                                        \<Type\>REIN\</Type\>

                                        \<ConvictionDate\>20211001\</ConvictionDate\>

                                        \<CustomCode\>330130\</CustomCode\>

                                        \<CustomPoints\>-3\</CustomPoints\>

                                        \<Detail\>Order Number : 935983239 \- REINSTATED\</Detail\>

                                    \</Violation\>

                                    \<Violation\>

                                        \<Type\>VIOL\</Type\>

                                        \<ViolationDate\>20200201\</ViolationDate\>

                                        \<ConvictionDate\>20200601\</ConvictionDate\>

                                        \<StateAssignedPoints\>0\</StateAssignedPoints\>

                                        \<CustomCode\>425100\</CustomCode\>

                                        \<CustomPoints\>0\</CustomPoints\>

                                        \<Detail\>Order Number : 935983239 \- 316.0083 RED LIGHT CAMERA DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 23 CITATION NUMBER: A5OJ78E COUNTY: MIAMI-DADE STATE: FL ADDED TO RECORD: 06/01/2020 DISPOSITION CODE: 547\</Detail\>

                                    \</Violation\>

                                    \<Violation\>

                                        \<Type\>VIOL\</Type\>

                                        \<ViolationDate\>20190201\</ViolationDate\>

                                        \<ConvictionDate\>20190801\</ConvictionDate\>

                                        \<StateAssignedPoints\>0\</StateAssignedPoints\>

                                        \<CustomCode\>425100\</CustomCode\>

                                        \<CustomPoints\>0\</CustomPoints\>

                                        \<Detail\>Order Number : 935983239 \- 316.0083 RED LIGHT CAMERA DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 24 CITATION NUMBER: AADQWXE COUNTY: MIAMI-DADE STATE: FL ADDED TO RECORD: 08/01/2019 DISPOSITION CODE: 547\</Detail\>

                                    \</Violation\>

                                \</Violations\>

                            \</Driver\>

                        \</MotorVehicleReport\>

                    \</MotorVehicleReports\>

                \</Subject\>

                \<Subject\>

                    \<Sequence\>2\</Sequence\>

                    \<DataSource\>Principal\</DataSource\>

                    \<IsSubjectVerified\>true\</IsSubjectVerified\>

                    \<IsSubjectActiveDuringMostRecentTerm\>true\</IsSubjectActiveDuringMostRecentTerm\>

                    \<EntityScore\>95\</EntityScore\>

                    \<GivenName\>DOUGLAS\</GivenName\>

                    \<MiddleName\>J\</MiddleName\>

                    \<Surname\>BONZHEIM\</Surname\>

                    \<PrimarySourceInfo\>

                        \<DOB\>19760101\</DOB\>

                        \<Gender\>M\</Gender\>

                        \<MaritalStatus\>M\</MaritalStatus\>

                        \<DLNumber\>M888777666555\</DLNumber\>

                        \<DLState\>FL\</DLState\>

                        \<SSN\>491487807\</SSN\>

                        \<RelationToPolicyHolder\>PP\</RelationToPolicyHolder\>

                        \<RelationToInsured\>I\</RelationToInsured\>

                        \<FromDate\>20230105\</FromDate\>

                        \<ToDate\>20240105\</ToDate\>

                    \</PrimarySourceInfo\>

                    \<SecondarySourceInfo\>

                        \<DOB\>19760101\</DOB\>

                        \<Gender\>M\</Gender\>

                        \<MaritalStatus\>S\</MaritalStatus\>

                        \<MatchType\>N\</MatchType\>

                        \<VerificationDate\>20220715\</VerificationDate\>

                        \<VerificationRange\>2\</VerificationRange\>

                        \<DriverAssuranceScore\>D1\</DriverAssuranceScore\>

                        \<InternalDriverCode\>7\</InternalDriverCode\>

                    \</SecondarySourceInfo\>

                    \<MotorVehicleReports\>

                        \<MotorVehicleReport\>

                            \<Status\>

                                \<Code\>V\</Code\>

                                \<Description\>NON-CLEAR report\</Description\>

                            \</Status\>

                            \<ViolationsType\>

                                \<Code\>C\</Code\>

                                \<Description\>Report passed through Custom violation code/point process\</Description\>

                                \<PointTotal\>4\</PointTotal\>

                            \</ViolationsType\>

                            \<DMVReportDate\>20201120\</DMVReportDate\>

                            \<DriversPrivacyProtectionActFlag\>N\</DriversPrivacyProtectionActFlag\>

                            \<Driver\>

                                \<Name\>BONZHEIM, DOUGLAS\</Name\>

                                \<CityStateZip\>NEW PORT RICHEY, FL 34655\</CityStateZip\>

                                \<Street1\>7827 ADELAIDE LP\</Street1\>

                                \<DLNumber\>M888777666555\</DLNumber\>

                                \<DLState\>FL\</DLState\>

                                \<DOB\>19760101\</DOB\>

                                \<Gender\>M\</Gender\>

                                \<Height\>5'10\</Height\>

                                \<License\>

                                    \<Class\>E\</Class\>

                                    \<Status\>VALID P\</Status\>

                                    \<IssuedDate\>20220401\</IssuedDate\>

                                    \<ExpirationDate\>20300601\</ExpirationDate\>

                                    \<OriginalIssueDate\>20000401\</OriginalIssueDate\>

                                \</License\>

                                \<Detail\>Order Number : 935983240 \- OrderType : MvrIndicator \- REQUESTED AS: DOUGLAS        J          BONZHEIM                  DOB: 01011976  LICENSE : M888777666555 PERS:01: ACTIVE          VALID P E              0401202206012030 LIC CLASS: E                       DESC: OPERATOR LIC STATUS: VALID PENDING LIC ISSUED: 04/01/2022 LIC EXPIRES: 06/01/2030 PERS:02: EXPIRED         EXPIRED ID CARD        0601201805012019 LIC CLASS: ID CARD                 DESC: ID CARD LIC STATUS: EXPIRED LIC ISSUED: 06/01/2018 LIC EXPIRES: 05/01/2019 AS OF NOVEMBER 20, 2020 AT 9:39:55 AM, DRIVER PRIVILEGE M888-777-66-655-5 IS VALID PENDING SANCTION(S). PERSONAL INFORMATION IS PROTECTED PURSUANT TO THE DRIVER PRIVACY PROTECTION ACT. ENTRIES BELOW ARE A THREE YEAR RECORD. ORIGINAL ISSUE DATE: 04/01/2000 REAL ID COMPLIANT US CITIZEN RECORD APPEARS IN NATIONAL DRIVER REGISTER BLOCKED PERSONAL INFORMATION BLOCKED FOR MAILING LIST PERSON HAS A DIGITAL IMAGE ELIGIBLE TO ELECT DRIVER SCHOOL.  DRIVER HAS MADE 0 ELECTIONS. VIOLATIONS COMMITTED WHILE A CDL HOLDER OR IN A CMV VEHICLE ARE NOT ELIGIBLE FOR DRIVING SCHOOL ELECTION. COUNTY: CLAY RESIDENTIAL ADDRESS: 4493 PLANTATION OAKS BLVD 1641  ORANGE PARK, FL  32065  COUNTY: CLAY ISSUANCE HISTORY: LIC CLASS: CLASS D   ISSUE DATE: 06/01/2001   ISSUE TYPE: DUPLICATE LIC CLASS: ID CARD   ISSUE DATE: 02/01/2003   ISSUE TYPE: DUPLICATE LIC CLASS: CLASS E   ISSUE DATE: 05/01/2015   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 06/01/2017   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 04/01/2018   ISSUE TYPE: REPLACEMENT LIC CLASS: ID CARD   ISSUE DATE: 02/01/2019   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 05/01/2019   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 12/01/2019   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 06/01/2020   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 09/01/2020   ISSUE TYPE: CDR/CDT CLEARANCE EXAMS TAKEN: VISION               DATE TAKEN: 04/01/2014   COUNT: 1   STATUS: PASS ROAD SIGN            DATE TAKEN: 08/01/2000   COUNT: 1   STATUS: PASS ROAD RULES           DATE TAKEN: 08/01/2000   COUNT: 4   STATUS: PASS DRIVING              DATE TAKEN: 04/01/2000   COUNT: 1   STATUS: RECIPROCATED This report is generated for insurance purposes only and may not be used for any other purpose.  The use and dissemination of the report and information in it must comply with your iiX agreement and the  Fair Credit Reporting Act, the Driver's Privacy Protection Act, and any applicable state statute(s).  The data in the report from the applicable state agency or service bureau is provided through iiX "as is." \--- Customer-defined MVR scoring has been applied to this record.  Customer  is solely responsible for the application and use of the resulting score.\</Detail\>

                                \<Violations\>

                                    \<Violation\>

                                        \<Type\>SUSP\</Type\>

                                        \<ViolationDate\>20220801\</ViolationDate\>

                                        \<CustomCode\>130110\</CustomCode\>

                                        \<CustomPoints\>3\</CustomPoints\>

                                        \<Detail\>Order Number : 935983240 \- FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 730177824 NOTICED PROVIDED: 07/01/2022 ADDED TO RECORD: 07/01/2022 SANCTION CODE: 7\</Detail\>

                                    \</Violation\>

                                    \<Violation\>

                                        \<Type\>REIN\</Type\>

                                        \<ConvictionDate\>20220901\</ConvictionDate\>

                                        \<CustomCode\>330130\</CustomCode\>

                                        \<CustomPoints\>-3\</CustomPoints\>

                                        \<Detail\>Order Number : 935983240 \- REINSTATED\</Detail\>

                                    \</Violation\>

                                    \<Violation\>

                                        \<Type\>SUSP\</Type\>

                                        \<ViolationDate\>20211201\</ViolationDate\>

                                        \<CustomCode\>130110\</CustomCode\>

                                        \<CustomPoints\>3\</CustomPoints\>

                                        \<Detail\>Order Number : 935983240 \- FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) PENDING SUSPENSION CASE NUMBER 730183044 NOTICED PROVIDED: 11/01/2021 ACTION REQUIRED: YES ADDED TO RECORD: 11/01/2021 SANCTION CODE: 7\</Detail\>

                                    \</Violation\>

                                    \<Violation\>

                                        \<Type\>VIOL\</Type\>

                                        \<ViolationDate\>20200701\</ViolationDate\>

                                        \<ConvictionDate\>20210101\</ConvictionDate\>

                                        \<StateAssignedPoints\>0\</StateAssignedPoints\>

                                        \<CustomCode\>555110\</CustomCode\>

                                        \<CustomPoints\>0\</CustomPoints\>

                                        \<Detail\>Order Number : 935983240 \- OPERATING MV NO PROOF OF INSURANCE DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 10 CITATION NUMBER: A0JO2AE COUNTY: DUVAL ADDED TO RECORD: 02/01/2021 DISPOSITION CODE: 280\</Detail\>

                                    \</Violation\>

                                    \<Violation\>

                                        \<Type\>VIOL\</Type\>

                                        \<ViolationDate\>20201201\</ViolationDate\>

                                        \<ConvictionDate\>20210101\</ConvictionDate\>

                                        \<StateAssignedPoints\>0\</StateAssignedPoints\>

                                        \<CustomCode\>425100\</CustomCode\>

                                        \<CustomPoints\>1\</CustomPoints\>

                                        \<Detail\>Order Number : 935983240 \- 316.0083 RED LIGHT CAMERA DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 11 CITATION NUMBER: A0IBDGE COUNTY: DUVAL ADDED TO RECORD: 02/01/2021 DISPOSITION CODE: 547\</Detail\>

                                    \</Violation\>

                                    \<Violation\>

                                        \<Type\>VIOL\</Type\>

                                        \<ViolationDate\>20200701\</ViolationDate\>

                                        \<ConvictionDate\>20210201\</ConvictionDate\>

                                        \<StateAssignedPoints\>0\</StateAssignedPoints\>

                                        \<CustomCode\>428300\</CustomCode\>

                                        \<CustomPoints\>0\</CustomPoints\>

                                        \<Detail\>Order Number : 935983240 \- SEAT BELT VIOLATION DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 12 CITATION NUMBER: A0JO2YE COUNTY: DUVAL ADDED TO RECORD: 02/01/2021 DISPOSITION CODE: 407\</Detail\>

                                    \</Violation\>

                                    \<Violation\>

                                        \<Type\>VIOL\</Type\>

                                        \<ViolationDate\>20200301\</ViolationDate\>

                                        \<ConvictionDate\>20200501\</ConvictionDate\>

                                        \<StateAssignedPoints\>3\</StateAssignedPoints\>

                                        \<CustomCode\>131240\</CustomCode\>

                                        \<CustomPoints\>0\</CustomPoints\>

                                        \<Detail\>Order Number : 935983240 \- DRIV WHILE LIC CANC/REV/SUSP DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 14 CITATION NUMBER: A0GLVGE COUNTY: DUVAL ADDED TO RECORD: 05/01/2020 DISPOSITION CODE: 609\</Detail\>

                                    \</Violation\>

                                \</Violations\>

                            \</Driver\>

                        \</MotorVehicleReport\>

                        \<MotorVehicleReport\>

                            \<Status\>

                                \<Code\>N\</Code\>

                                \<Description\>NOT FOUND\</Description\>

                            \</Status\>

                            \<ViolationsType\>

                                \<Code\>N\</Code\>

                                \<Description\>Not Coded\</Description\>

                            \</ViolationsType\>

                            \<Driver\>

                                \<DLNumber\>T123654125803\</DLNumber\>

                                \<DLState\>FL\</DLState\>

                                \<Detail\>Order Number : 935983246 \- OrderType : MvrIndicator \- \</Detail\>

                            \</Driver\>

                        \</MotorVehicleReport\>

                    \</MotorVehicleReports\>

                \</Subject\>

                \<Subject\>

                    \<Sequence\>3\</Sequence\>

                    \<DataSource\>Principal\</DataSource\>

                    \<IsSubjectVerified\>true\</IsSubjectVerified\>

                    \<IsSubjectActiveDuringMostRecentTerm\>true\</IsSubjectActiveDuringMostRecentTerm\>

                    \<EntityScore\>95\</EntityScore\>

                    \<GivenName\>LORNA\</GivenName\>

                    \<MiddleName\>P\</MiddleName\>

                    \<Surname\>BONZHEIM\</Surname\>

                    \<PrimarySourceInfo\>

                        \<DOB\>20030923\</DOB\>

                        \<Gender\>F\</Gender\>

                        \<MaritalStatus\>M\</MaritalStatus\>

                        \<DLNumber\>B640693682100\</DLNumber\>

                        \<DLState\>FL\</DLState\>

                        \<RelationToPolicyHolder\>SP\</RelationToPolicyHolder\>

                        \<RelationToInsured\>S\</RelationToInsured\>

                        \<FromDate\>20230105\</FromDate\>

                        \<ToDate\>20240105\</ToDate\>

                    \</PrimarySourceInfo\>

                    \<SecondarySourceInfo\>

                        \<DOB\>20030923\</DOB\>

                        \<Gender\>M\</Gender\>

                        \<MaritalStatus\>M\</MaritalStatus\>

                        \<MatchType\>N\</MatchType\>

                        \<VerificationDate\>20220315\</VerificationDate\>

                        \<VerificationRange\>2\</VerificationRange\>

                        \<DriverAssuranceScore\>D1\</DriverAssuranceScore\>

                        \<InternalDriverCode\>7\</InternalDriverCode\>

                    \</SecondarySourceInfo\>

                    \<MotorVehicleReports\>

                        \<MotorVehicleReport\>

                            \<Status\>

                                \<Code\>V\</Code\>

                                \<Description\>NON-CLEAR report\</Description\>

                            \</Status\>

                            \<ViolationsType\>

                                \<Code\>C\</Code\>

                                \<Description\>Report passed through Custom violation code/point process\</Description\>

                                \<PointTotal\>2\</PointTotal\>

                            \</ViolationsType\>

                            \<DMVReportDate\>20201120\</DMVReportDate\>

                            \<DriversPrivacyProtectionActFlag\>N\</DriversPrivacyProtectionActFlag\>

                            \<Driver\>

                                \<Name\>BONZHEIM, LORNA\</Name\>

                                \<CityStateZip\>NEW PORT RICHEY, FL 34655\</CityStateZip\>

                                \<Street1\>7827 ADELAIDE LP\</Street1\>

                                \<DLNumber\>B640693682100\</DLNumber\>

                                \<DLState\>FL\</DLState\>

                                \<DOB\>20030923\</DOB\>

                                \<Gender\>F\</Gender\>

                                \<Height\>5'6\</Height\>

                                \<License\>

                                    \<Class\>E\</Class\>

                                    \<Status\>VALID\</Status\>

                                    \<IssuedDate\>20220301\</IssuedDate\>

                                    \<ExpirationDate\>20300701\</ExpirationDate\>

                                    \<OriginalIssueDate\>20010301\</OriginalIssueDate\>

                                    \<Restriction\>A\</Restriction\>

                                \</License\>

                                \<Detail\>Order Number : 935983244 \- OrderType : MvrIndicator \- REQUESTED AS: LORNA          P          BONZHEIM                  DOB: 09232003  LICENSE : B640693682100 PERS:01: ACTIVE          VALID   E              0301202207012030                A LIC CLASS: E                       DESC: OPERATOR LIC STATUS: VALID LIC ISSUED: 03/01/2022 LIC EXPIRES: 07/01/2030 LIC RESTR: A                          DESC: CORRECTIVE LENSES PERS:02: EXPIRED         EXPIRED ID CARD        0901200312012017 LIC CLASS: ID CARD                 DESC: ID CARD LIC STATUS: EXPIRED LIC ISSUED: 09/01/2003 LIC EXPIRES: 12/01/2017 AS OF NOVEMBER 20, 2020 AT 9:45:15 AM, DRIVER PRIVILEGE B640-693-68-210-0 IS VALID. PERSONAL INFORMATION IS PROTECTED PURSUANT TO THE DRIVER PRIVACY PROTECTION ACT. ENTRIES BELOW ARE A THREE YEAR RECORD. ORIGINAL ISSUE DATE: 03/01/2001 REAL ID COMPLIANT US CITIZEN BLOCKED PERSONAL INFORMATION BLOCKED FOR MAILING LIST PERSON HAS A DIGITAL IMAGE ELIGIBLE TO ELECT DRIVER SCHOOL.  DRIVER HAS MADE 2 ELECTIONS. LAST ELECTION WAS ON 06/01/2002. VIOLATIONS COMMITTED WHILE A CDL HOLDER OR IN A CMV VEHICLE ARE NOT ELIGIBLE FOR DRIVING SCHOOL ELECTION. COUNTY: BROWARD RESIDENTIAL ADDRESS: 7923 NW 18TH ST APT 203  MARGATE, FL  33063  COUNTY: BROWARD ISSUANCE HISTORY: LIC CLASS: CLASS E   ISSUE DATE: 09/01/2001   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 06/01/2002   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 06/01/2002   ISSUE TYPE: REPLACEMENT LIC CLASS: ID CARD   ISSUE DATE: 06/01/2002   ISSUE TYPE: DUPLICATE LIC CLASS: CLASS E   ISSUE DATE: 03/01/2004   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 06/01/2006   ISSUE TYPE: ADDRESS CHANGE LIC CLASS: CLASS E   ISSUE DATE: 12/01/2017   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 12/01/2019   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 06/01/2020   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 08/01/2020   ISSUE TYPE: CDR/CDT CLEARANCE EXAMS TAKEN: VISION               DATE TAKEN: 03/01/2022   COUNT: 1   STATUS: PASS ROAD SIGN            DATE TAKEN: 03/01/2022   COUNT: 9   STATUS: RECIPROCATED ROAD RULES           DATE TAKEN: 03/01/2022   COUNT: 3   STATUS: PASS DRIVING              DATE TAKEN: 09/01/2021   COUNT: 4   STATUS: PASS This report is generated for insurance purposes only and may not be used for any other purpose.  The use and dissemination of the report and information in it must comply with your iiX agreement and the  Fair Credit Reporting Act, the Driver's Privacy Protection Act, and any applicable state statute(s).  The data in the report from the applicable state agency or service bureau is provided through iiX "as is." \--- Customer-defined MVR scoring has been applied to this record.  Customer  is solely responsible for the application and use of the resulting score.\</Detail\>

                                \<Violations\>

                                    \<Violation\>

                                        \<Type\>SUSP\</Type\>

                                        \<ViolationDate\>20210701\</ViolationDate\>

                                        \<CustomCode\>130110\</CustomCode\>

                                        \<CustomPoints\>3\</CustomPoints\>

                                        \<Detail\>Order Number : 935983244 \- FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 730115590 NOTICED PROVIDED: 06/01/2021 ADDED TO RECORD: 06/01/2021 SANCTION CODE: 7\</Detail\>

                                    \</Violation\>

                                    \<Violation\>

                                        \<Type\>REIN\</Type\>

                                        \<ConvictionDate\>20211201\</ConvictionDate\>

                                        \<CustomCode\>330130\</CustomCode\>

                                        \<CustomPoints\>-3\</CustomPoints\>

                                        \<Detail\>Order Number : 935983244 \- REINSTATED\</Detail\>

                                    \</Violation\>

                                    \<Violation\>

                                        \<Type\>SUSP\</Type\>

                                        \<ViolationDate\>20200401\</ViolationDate\>

                                        \<CustomCode\>130110\</CustomCode\>

                                        \<CustomPoints\>0\</CustomPoints\>

                                        \<Detail\>Order Number : 935983244 \- FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 730195358 NOTICED PROVIDED: 04/01/2020 ADDED TO RECORD: 04/01/2020 SANCTION CODE: 7\</Detail\>

                                    \</Violation\>

                                    \<Violation\>

                                        \<Type\>REIN\</Type\>

                                        \<ConvictionDate\>20200601\</ConvictionDate\>

                                        \<CustomCode\>330130\</CustomCode\>

                                        \<CustomPoints\>0\</CustomPoints\>

                                        \<Detail\>Order Number : 935983244 \- REINSTATED\</Detail\>

                                    \</Violation\>

                                    \<Violation\>

                                        \<Type\>SUSP\</Type\>

                                        \<ViolationDate\>20200801\</ViolationDate\>

                                        \<CustomCode\>130110\</CustomCode\>

                                        \<CustomPoints\>0\</CustomPoints\>

                                        \<Detail\>Order Number : 935983244 \- FR-REGISTRATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 830111729 NOTICED PROVIDED: 07/01/2020 ADDED TO RECORD: 07/01/2020 SANCTION CODE: 8\</Detail\>

                                    \</Violation\>

                                    \<Violation\>

                                        \<Type\>REIN\</Type\>

                                        \<ConvictionDate\>20200801\</ConvictionDate\>

                                        \<CustomCode\>330130\</CustomCode\>

                                        \<CustomPoints\>0\</CustomPoints\>

                                        \<Detail\>Order Number : 935983244 \- REINSTATED\</Detail\>

                                    \</Violation\>

                                    \<Violation\>

                                        \<Type\>VIOL\</Type\>

                                        \<ViolationDate\>20220201\</ViolationDate\>

                                        \<ConvictionDate\>20220501\</ConvictionDate\>

                                        \<StateAssignedPoints\>4\</StateAssignedPoints\>

                                        \<CustomCode\>424300\</CustomCode\>

                                        \<CustomPoints\>1\</CustomPoints\>

                                        \<Detail\>Order Number : 935983244 \- FAIL TO YIELD UNSIGNED INTERSECTION DISPOSITION WAS GUILTY COUNTY COURT CRASH INDICATED VIOLATION NUMBER: 5 CITATION NUMBER: A0LU14E COUNTY: BROWARD ADDED TO RECORD: 05/01/2022 DISPOSITION CODE: 513\</Detail\>

                                    \</Violation\>

                                    \<Violation\>

                                        \<Type\>VIOL\</Type\>

                                        \<ViolationDate\>20211201\</ViolationDate\>

                                        \<ConvictionDate\>20220201\</ConvictionDate\>

                                        \<StateAssignedPoints\>0\</StateAssignedPoints\>

                                        \<CustomCode\>536400\</CustomCode\>

                                        \<CustomPoints\>1\</CustomPoints\>

                                        \<Detail\>Order Number : 935983244 \- EXPIRED TAG \- 6 MOS OR LESS DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 6 CITATION NUMBER: AR9P4UE COUNTY: BROWARD STATE: FL ADDED TO RECORD: 02/01/2022 DISPOSITION CODE: 473\</Detail\>

                                    \</Violation\>

                                \</Violations\>

                            \</Driver\>

                        \</MotorVehicleReport\>

                    \</MotorVehicleReports\>

                \</Subject\>

                \<Subject\>

                    \<Sequence\>4\</Sequence\>

                    \<DataSource\>Principal\</DataSource\>

                    \<IsSubjectVerified\>true\</IsSubjectVerified\>

                    \<IsSubjectActiveDuringMostRecentTerm\>true\</IsSubjectActiveDuringMostRecentTerm\>

                    \<EntityScore\>90\</EntityScore\>

                    \<GivenName\>MALIA\</GivenName\>

                    \<MiddleName\>R\</MiddleName\>

                    \<Surname\>BONZHEIM\</Surname\>

                    \<PrimarySourceInfo\>

                        \<DOB\>19990120\</DOB\>

                        \<Gender\>F\</Gender\>

                        \<MaritalStatus\>S\</MaritalStatus\>

                        \<DLNumber\>S420665834256\</DLNumber\>

                        \<DLState\>FL\</DLState\>

                        \<RelationToPolicyHolder\>LD\</RelationToPolicyHolder\>

                        \<FromDate\>20230105\</FromDate\>

                        \<ToDate\>20240105\</ToDate\>

                    \</PrimarySourceInfo\>

                    \<SecondarySourceInfo\>

                        \<DOB\>19900720\</DOB\>

                        \<Gender\>F\</Gender\>

                        \<MaritalStatus\>S\</MaritalStatus\>

                        \<MatchType\>N\</MatchType\>

                        \<VerificationDate\>20220815\</VerificationDate\>

                        \<VerificationRange\>2\</VerificationRange\>

                        \<DriverAssuranceScore\>D1\</DriverAssuranceScore\>

                        \<InternalDriverCode\>7\</InternalDriverCode\>

                    \</SecondarySourceInfo\>

                    \<MotorVehicleReports\>

                        \<MotorVehicleReport\>

                            \<Status\>

                                \<Code\>N\</Code\>

                                \<Description\>NOT FOUND\</Description\>

                            \</Status\>

                            \<ViolationsType\>

                                \<Code\>N\</Code\>

                                \<Description\>Not Coded\</Description\>

                            \</ViolationsType\>

                            \<Driver\>

                                \<DLNumber\>S420665834256\</DLNumber\>

                                \<DLState\>FL\</DLState\>

                                \<Detail\>Order Number : 935983243 \- OrderType : MvrIndicator \- \</Detail\>

                            \</Driver\>

                        \</MotorVehicleReport\>

                    \</MotorVehicleReports\>

                \</Subject\>

                \<Subject\>

                    \<Sequence\>5\</Sequence\>

                    \<DataSource\>Principal\</DataSource\>

                    \<IsSubjectVerified\>true\</IsSubjectVerified\>

                    \<IsSubjectActiveDuringMostRecentTerm\>true\</IsSubjectActiveDuringMostRecentTerm\>

                    \<EntityScore\>90\</EntityScore\>

                    \<GivenName\>MARKUS\</GivenName\>

                    \<MiddleName\>G\</MiddleName\>

                    \<Surname\>BONZHEIM\</Surname\>

                    \<PrimarySourceInfo\>

                        \<DOB\>20010311\</DOB\>

                        \<Gender\>F\</Gender\>

                        \<MaritalStatus\>S\</MaritalStatus\>

                        \<DLNumber\>P420665934225\</DLNumber\>

                        \<DLState\>FL\</DLState\>

                        \<RelationToPolicyHolder\>LD\</RelationToPolicyHolder\>

                        \<FromDate\>20230105\</FromDate\>

                        \<ToDate\>20240105\</ToDate\>

                    \</PrimarySourceInfo\>

                    \<SecondarySourceInfo\>

                        \<DOB\>20010311\</DOB\>

                        \<Gender\>M\</Gender\>

                        \<MaritalStatus\>S\</MaritalStatus\>

                        \<MatchType\>N\</MatchType\>

                        \<VerificationDate\>20220315\</VerificationDate\>

                        \<VerificationRange\>2\</VerificationRange\>

                        \<DriverAssuranceScore\>D1\</DriverAssuranceScore\>

                        \<InternalDriverCode\>7\</InternalDriverCode\>

                    \</SecondarySourceInfo\>

                    \<MotorVehicleReports\>

                        \<MotorVehicleReport\>

                            \<Status\>

                                \<Code\>N\</Code\>

                                \<Description\>NOT FOUND\</Description\>

                            \</Status\>

                            \<ViolationsType\>

                                \<Code\>N\</Code\>

                                \<Description\>Not Coded\</Description\>

                            \</ViolationsType\>

                            \<Driver\>

                                \<DLNumber\>P420665934225\</DLNumber\>

                                \<DLState\>FL\</DLState\>

                                \<Detail\>Order Number : 935983241 \- OrderType : MvrIndicator \- \</Detail\>

                            \</Driver\>

                        \</MotorVehicleReport\>

                    \</MotorVehicleReports\>

                \</Subject\>

                \<Subject\>

                    \<Sequence\>6\</Sequence\>

                    \<DataSource\>Principal\</DataSource\>

                    \<IsSubjectVerified\>true\</IsSubjectVerified\>

                    \<IsSubjectActiveDuringMostRecentTerm\>true\</IsSubjectActiveDuringMostRecentTerm\>

                    \<EntityScore\>90\</EntityScore\>

                    \<GivenName\>MINDI\</GivenName\>

                    \<MiddleName\>H\</MiddleName\>

                    \<Surname\>BONZHEIM\</Surname\>

                    \<PrimarySourceInfo\>

                        \<DOB\>19901113\</DOB\>

                        \<Gender\>F\</Gender\>

                        \<MaritalStatus\>S\</MaritalStatus\>

                        \<DLNumber\>R420622534333\</DLNumber\>

                        \<DLState\>FL\</DLState\>

                        \<RelationToPolicyHolder\>LD\</RelationToPolicyHolder\>

                        \<FromDate\>20230105\</FromDate\>

                        \<ToDate\>20240105\</ToDate\>

                    \</PrimarySourceInfo\>

                    \<SecondarySourceInfo\>

                        \<DOB\>19901113\</DOB\>

                        \<Gender\>F\</Gender\>

                        \<MaritalStatus\>S\</MaritalStatus\>

                        \<MatchType\>N\</MatchType\>

                        \<VerificationDate\>20220815\</VerificationDate\>

                        \<VerificationRange\>2\</VerificationRange\>

                        \<DriverAssuranceScore\>D1\</DriverAssuranceScore\>

                        \<InternalDriverCode\>7\</InternalDriverCode\>

                    \</SecondarySourceInfo\>

                    \<MotorVehicleReports\>

                        \<MotorVehicleReport\>

                            \<Status\>

                                \<Code\>N\</Code\>

                                \<Description\>NOT FOUND\</Description\>

                            \</Status\>

                            \<ViolationsType\>

                                \<Code\>N\</Code\>

                                \<Description\>Not Coded\</Description\>

                            \</ViolationsType\>

                            \<Driver\>

                                \<DLNumber\>R420622534333\</DLNumber\>

                                \<DLState\>FL\</DLState\>

                                \<Detail\>Order Number : 935983242 \- OrderType : MvrIndicator \- \</Detail\>

                            \</Driver\>

                        \</MotorVehicleReport\>

                    \</MotorVehicleReports\>

                \</Subject\>

                \<Subject\>

                    \<Sequence\>7\</Sequence\>

                    \<DataSource\>Principal\</DataSource\>

                    \<IsSubjectVerified\>false\</IsSubjectVerified\>

                    \<IsSubjectActiveDuringMostRecentTerm\>true\</IsSubjectActiveDuringMostRecentTerm\>

                    \<EntityScore\>85\</EntityScore\>

                    \<GivenName\>RHETT\</GivenName\>

                    \<MiddleName\>K\</MiddleName\>

                    \<Surname\>BONZHEIM\</Surname\>

                    \<PrimarySourceInfo\>

                        \<DOB\>19900720\</DOB\>

                        \<Gender\>F\</Gender\>

                        \<MaritalStatus\>S\</MaritalStatus\>

                        \<DLNumber\>L420625834362\</DLNumber\>

                        \<DLState\>FL\</DLState\>

                        \<RelationToPolicyHolder\>LD\</RelationToPolicyHolder\>

                        \<FromDate\>20230105\</FromDate\>

                        \<ToDate\>20240105\</ToDate\>

                    \</PrimarySourceInfo\>

                    \<MotorVehicleReports\>

                        \<MotorVehicleReport\>

                            \<Status\>

                                \<Code\>N\</Code\>

                                \<Description\>NOT FOUND\</Description\>

                            \</Status\>

                            \<ViolationsType\>

                                \<Code\>N\</Code\>

                                \<Description\>Not Coded\</Description\>

                            \</ViolationsType\>

                            \<Driver\>

                                \<DLNumber\>L420625834362\</DLNumber\>

                                \<DLState\>FL\</DLState\>

                                \<Detail\>Order Number : 935983245 \- OrderType : MvrIndicator \- \</Detail\>

                            \</Driver\>

                        \</MotorVehicleReport\>

                    \</MotorVehicleReports\>

                \</Subject\>

            \</Subjects\>

            \<Vehicles\>

                \<Vehicle\>

                    \<Sequence\>1\</Sequence\>

                    \<DataSource\>Principal\</DataSource\>

                    \<IsVehicleVerified\>true\</IsVehicleVerified\>

                    \<IsVehicleActiveDuringMostRecentTerm\>true\</IsVehicleActiveDuringMostRecentTerm\>

                    \<EntityScore\>60\</EntityScore\>

                    \<VIN\>1G5CT18B5F8530675\</VIN\>

                    \<VehiclePolicyData\>

                        \<Year\>1985\</Year\>

                        \<Make\>GMC\</Make\>

                        \<Model\>UT\</Model\>

                        \<BusinessUse\>Y\</BusinessUse\>

                        \<ClassCode\>000000\</ClassCode\>

                        \<CollisionDeductibleAmount\>1000\</CollisionDeductibleAmount\>

                        \<ComprehensiveDeductibleAmount\>500\</ComprehensiveDeductibleAmount\>

                        \<FromDate\>20230105\</FromDate\>

                        \<ToDate\>20240105\</ToDate\>

                        \<CollisionIndicator\>Y\</CollisionIndicator\>

                        \<ComprehensiveIndicator\>Y\</ComprehensiveIndicator\>

                        \<Coverages\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>BINJ\</Code\>

                                    \<Description\>Bodily Injury\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>40000\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>80000\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>PDMG\</Code\>

                                    \<Description\>Property Damage\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>CBSL\</Code\>

                                    \<Description\>CSL (BI \&amp; PD)\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>0\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>0\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>80000\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>UMPD\</Code\>

                                    \<Description\>Uninsured Motorist (PD)\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>PINJ\</Code\>

                                    \<Description\>Personal Injury\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                        \</Coverages\>

                    \</VehiclePolicyData\>

                    \<RegistrationData\>

                        \<VINMatch\>Y\</VINMatch\>

                        \<ValidVINIndicator\>Y\</ValidVINIndicator\>

                        \<VINChangeIndicator\>N\</VINChangeIndicator\>

                        \<VIN\>1G5CT18B5F8530675\</VIN\>

                        \<VehicleTypeCode\>T\</VehicleTypeCode\>

                        \<VehicleTypeDesc\>Truck\</VehicleTypeDesc\>

                        \<ModelYear\>1985\</ModelYear\>

                        \<Make\>GMC\</Make\>

                        \<MakeDesc\>GMC\</MakeDesc\>

                        \<Model\>S15\</Model\>

                        \<BodyStyleCode\>UT\</BodyStyleCode\>

                        \<BodyStyleDesc\>Sport Utility Vehicle\</BodyStyleDesc\>

                        \<StateOfRegistration\>CO\</StateOfRegistration\>

                        \<TransactionDate\>20060119\</TransactionDate\>

                        \<ExpirationDate\>20211212\</ExpirationDate\>

                        \<PlateTypeCode\>Z\</PlateTypeCode\>

                        \<PlateTypeDesc\>Regular\</PlateTypeDesc\>

                        \<LicensePlateNumber\>112MPE\</LicensePlateNumber\>

                        \<IsBranded\>false\</IsBranded\>

                        \<LeaseInd\>N\</LeaseInd\>

                        \<NameCode1\>A\</NameCode1\>

                        \<NameCodeDesc1\>Owner\</NameCodeDesc1\>

                        \<NameTitleCode1\>3\</NameTitleCode1\>

                        \<NameTitleDesc1\>MS\</NameTitleDesc1\>

                        \<RegisteredOwnerName\>

                            \<GivenName\>RHONDA\</GivenName\>

                            \<MiddleName\>R\</MiddleName\>

                            \<Surname\>GARCILASCO\</Surname\>

                        \</RegisteredOwnerName\>

                        \<Address\>

                            \<AddressType\>S\</AddressType\>

                            \<Street1\>4341 W CENTER AVE APT B\</Street1\>

                            \<City\>DENVER\</City\>

                            \<StateCode\>CO\</StateCode\>

                            \<Zip\>80219\</Zip\>

                        \</Address\>

                    \</RegistrationData\>

                    \<NumberofVehicleOwners\>1\</NumberofVehicleOwners\>

                    \<IsVehicleSalvage\>false\</IsVehicleSalvage\>

                    \<SupplementalCatClaimIndicator\>N\</SupplementalCatClaimIndicator\>

                    \<ReasonCodeDetails\>

                        \<Reason\>

                            \<Code\>AG-2.22\</Code\>

                            \<Description\>Vehicle has out of state Registration.  \</Description\>

                        \</Reason\>

                        \<Reason\>

                            \<Code\>AO-5.01\</Code\>

                            \<Description\>Vehicle is not owned by Policy Holder or any Driver on the Policy.\</Description\>

                        \</Reason\>

                    \</ReasonCodeDetails\>

                    \<ActionMessages\>

                        \<ActionMessage\>Ask for Vehicle Registration\</ActionMessage\>

                    \</ActionMessages\>

                    \<Mileage\>

                        \<Sources\>

                            \<Source\>

                                \<Name\>VeriskMileageModel\</Name\>

                                \<Miles\>3743\</Miles\>

                            \</Source\>

                        \</Sources\>

                    \</Mileage\>

                    \<SmartScore\>

                        \<EnrollmentStatus\>EN\</EnrollmentStatus\>

                        \<EnrollmentDate\>2022-01-01 05:00:41.394\</EnrollmentDate\>

                        \<ProductEnrollmentStatus\>EN\</ProductEnrollmentStatus\>

                        \<ScoreStatus\>SU\</ScoreStatus\>

                        \<ScoreType\>Recent\</ScoreType\>

                        \<Score\>85\</Score\>

                        \<ScoreStartDate\>2022-11-14 00:00:00.000\</ScoreStartDate\>

                        \<ScoreEndDate\>2023-01-22 23:59:59.000\</ScoreEndDate\>

                    \</SmartScore\>

                    \<VinMaster\>

                        \<Vehicles\>

                            \<Vehicle\>

                                \<VIN\>1G5CT18B\&amp;F\</VIN\>

                                \<FullModelYear\>1985\</FullModelYear\>

                                \<Make\>GMC\</Make\>

                                \<MakeDescription\>GMC\</MakeDescription\>

                                \<BasicModelName\>JIMMY S-15\</BasicModelName\>

                                \<FullModelName\>JIMMY S-15\</FullModelName\>

                                \<BodyStyle\>UTIL 4X4\</BodyStyle\>

                                \<BodyStyleDescription\>Utility Vehicle \- Four-Wheel Drive\</BodyStyleDescription\>

                                \<EngineSize\>173\</EngineSize\>

                                \<EngineCylinders\>6\</EngineCylinders\>

                                \<EngineCylindersDescription\>Six-Cylinder Engine\</EngineCylindersDescription\>

                                \<EngineTypeDescription\>Other Type of Engine\</EngineTypeDescription\>

                                \<FourWheelDriveIndicator\>4\</FourWheelDriveIndicator\>

                                \<FourWheelDriveIndicatorDescription\>Vehicle is four-wheel drive\</FourWheelDriveIndicatorDescription\>

                                \<Restraint\>A\</Restraint\>

                                \<RestraintDescription\>Driver \&amp; Front Passenger Active Restraints\</RestraintDescription\>

                                \<AntiLockBrakes\>N\</AntiLockBrakes\>

                                \<AntiLockBrakesDescription\>Anti-Lock Brakes are not available\</AntiLockBrakesDescription\>

                                \<AntiTheftIndicatorDescription\>Field not added to VINMASTER until model year 1990\</AntiTheftIndicatorDescription\>

                                \<ElectronicStabilityControlDescription\>Field not added to VINMASTER until model year 1995\</ElectronicStabilityControlDescription\>

                                \<DaytimeRunningLightIndicatorDescription\>Field not added to VINMASTER until model year 1995\</DaytimeRunningLightIndicatorDescription\>

                                \<RecordType\>S\</RecordType\>

                                \<PriceNewSymbol\_27SymbolTable\_OnePosition\>J\</PriceNewSymbol\_27SymbolTable\_OnePosition\>

                                \<PriceNewSymbol\_27SymbolTable\_TwoPositions\>10\</PriceNewSymbol\_27SymbolTable\_TwoPositions\>

                                \<PriceNew\_Min\>10001.00\</PriceNew\_Min\>

                                \<PriceNew\_Max\>12500.99\</PriceNew\_Max\>

                                \<PhysicalDamage\>

                                    \<CombinedVSRSymbol\_OnePosition\>J\</CombinedVSRSymbol\_OnePosition\>

                                    \<CombinedVSRSymbol\_TwoPositions\>10\</CombinedVSRSymbol\_TwoPositions\>

                                \</PhysicalDamage\>

                            \</Vehicle\>

                        \</Vehicles\>

                    \</VinMaster\>

                    \<RiskAnalyzer\>

                        \<Vehicles\>

                            \<Vehicle\>

                                \<VIN\>1G5CT18B\&amp;F\</VIN\>

                                \<ModelYear\>1985\</ModelYear\>

                                \<DistributionDate\>2212\</DistributionDate\>

                                \<Restraint\>A\</Restraint\>

                                \<AntiLockBrakes\>N\</AntiLockBrakes\>

                                \<EngineCylinders\>6\</EngineCylinders\>

                                \<Make\>GMC\</Make\>

                                \<BasicModelName\>JIMMY S-15\</BasicModelName\>

                                \<BodyStyle\>UTIL 4X4\</BodyStyle\>

                                \<EngineSize\>173\</EngineSize\>

                                \<FourWheelDriveIndicator\>4\</FourWheelDriveIndicator\>

                                \<PayloadCapacity\>0\</PayloadCapacity\>

                                \<FullModelName\>JIMMY S-15\</FullModelName\>

                                \<Wheelbase\>0\</Wheelbase\>

                                \<CurbWeight\>0\</CurbWeight\>

                                \<GrossVehicleWeight\>0\</GrossVehicleWeight\>

                                \<Height\>0\</Height\>

                                \<Horsepower\>0\</Horsepower\>

                                \<StateException\>TX\</StateException\>

                                \<NCICCode\>GMC\</NCICCode\>

                                \<Length\>0\</Length\>

                                \<Width\>0\</Width\>

                                \<BaseMSRP\>10001\</BaseMSRP\>

                                \<SpecialHandlingIndicator\>N\</SpecialHandlingIndicator\>

                                \<InterimIndicator\>N\</InterimIndicator\>

                                \<ReleaseDate\>2303\</ReleaseDate\>

                                \<PhysicalDamage\>

                                    \<RiskAnalyzerCollisionIndicatedSymbol\>BC\</RiskAnalyzerCollisionIndicatedSymbol\>

                                    \<RiskAnalyzerComprehensiveIndicatedSymbol\>AB\</RiskAnalyzerComprehensiveIndicatedSymbol\>

                                    \<RiskAnalyzerCollisionRatingSymbol\>BC\</RiskAnalyzerCollisionRatingSymbol\>

                                    \<RiskAnalyzerComprehensiveRatingSymbol\>AB\</RiskAnalyzerComprehensiveRatingSymbol\>

                                    \<RiskAnalyzerComprehensiveNonGlassRatingSymbol\>AB\</RiskAnalyzerComprehensiveNonGlassRatingSymbol\>

                                    \<RiskAnalyzerCollisionCappingIndicator\>N\</RiskAnalyzerCollisionCappingIndicator\>

                                    \<RiskAnalyzerComprehensiveCappingIndicator\>N\</RiskAnalyzerComprehensiveCappingIndicator\>

                                    \<RiskAnalyzerComprehensiveNonGlassCappingIndicator\>N\</RiskAnalyzerComprehensiveNonGlassCappingIndicator\>

                                    \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbol\>AB\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbol\>

                                \</PhysicalDamage\>

                                \<Liability\>

                                    \<RiskAnalyzerMedicalPaymentsIndicatedSymbol\>FB\</RiskAnalyzerMedicalPaymentsIndicatedSymbol\>

                                    \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbol\>VB\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbol\>

                                    \<RiskAnalyzerSingleLimitIndicatedSymbol\>JF\</RiskAnalyzerSingleLimitIndicatedSymbol\>

                                    \<RiskAnalyzerBodilyInjuryRatingSymbol\>JH\</RiskAnalyzerBodilyInjuryRatingSymbol\>

                                    \<RiskAnalyzerPropertyDamageRatingSymbol\>JC\</RiskAnalyzerPropertyDamageRatingSymbol\>

                                    \<RiskAnalyzerMedicalPaymentsRatingSymbol\>FB\</RiskAnalyzerMedicalPaymentsRatingSymbol\>

                                    \<RiskAnalyzerPersonalInjuryProtectionRatingSymbol\>VB\</RiskAnalyzerPersonalInjuryProtectionRatingSymbol\>

                                    \<RiskAnalyzerSingleLimitRatingSymbol\>JF\</RiskAnalyzerSingleLimitRatingSymbol\>

                                    \<RiskAnalyzerBodilyInjuryCappingIndicator\>N\</RiskAnalyzerBodilyInjuryCappingIndicator\>

                                    \<RiskAnalyzerPropertyDamageCappingIndicator\>N\</RiskAnalyzerPropertyDamageCappingIndicator\>

                                    \<RiskAnalyzerMedicalPaymentsCappingIndicator\>N\</RiskAnalyzerMedicalPaymentsCappingIndicator\>

                                    \<RiskAnalyzerPersonalInjuryProtectionCappingIndicator\>N\</RiskAnalyzerPersonalInjuryProtectionCappingIndicator\>

                                    \<RiskAnalyzerBodilyInjuryIndicatedSymbol\>JH\</RiskAnalyzerBodilyInjuryIndicatedSymbol\>

                                    \<RiskAnalyzerPropertyDamageIndicatedSymbol\>JC\</RiskAnalyzerPropertyDamageIndicatedSymbol\>

                                    \<RiskAnalyzerSingleLimitCappingIndicator\>N\</RiskAnalyzerSingleLimitCappingIndicator\>

                                \</Liability\>

                            \</Vehicle\>

                        \</Vehicles\>

                    \</RiskAnalyzer\>

                \</Vehicle\>

                \<Vehicle\>

                    \<Sequence\>2\</Sequence\>

                    \<DataSource\>Principal\</DataSource\>

                    \<IsVehicleVerified\>true\</IsVehicleVerified\>

                    \<IsVehicleActiveDuringMostRecentTerm\>true\</IsVehicleActiveDuringMostRecentTerm\>

                    \<EntityScore\>60\</EntityScore\>

                    \<VIN\>3GNFK16T9YG218125\</VIN\>

                    \<VehiclePolicyData\>

                        \<Year\>2000\</Year\>

                        \<Make\>CHEV\</Make\>

                        \<Model\>K1S\</Model\>

                        \<BusinessUse\>Y\</BusinessUse\>

                        \<ClassCode\>000000\</ClassCode\>

                        \<CollisionDeductibleAmount\>1000\</CollisionDeductibleAmount\>

                        \<ComprehensiveDeductibleAmount\>500\</ComprehensiveDeductibleAmount\>

                        \<FromDate\>20230105\</FromDate\>

                        \<ToDate\>20240105\</ToDate\>

                        \<CollisionIndicator\>Y\</CollisionIndicator\>

                        \<ComprehensiveIndicator\>Y\</ComprehensiveIndicator\>

                        \<Coverages\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>BINJ\</Code\>

                                    \<Description\>Bodily Injury\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>40000\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>80000\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>PDMG\</Code\>

                                    \<Description\>Property Damage\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>CBSL\</Code\>

                                    \<Description\>CSL (BI \&amp; PD)\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>0\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>0\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>80000\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>UMPD\</Code\>

                                    \<Description\>Uninsured Motorist (PD)\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>PINJ\</Code\>

                                    \<Description\>Personal Injury\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                        \</Coverages\>

                    \</VehiclePolicyData\>

                    \<RegistrationData\>

                        \<VINMatch\>Y\</VINMatch\>

                        \<ValidVINIndicator\>Y\</ValidVINIndicator\>

                        \<VINChangeIndicator\>N\</VINChangeIndicator\>

                        \<VIN\>3GNFK16T9YG218125\</VIN\>

                        \<VehicleTypeCode\>T\</VehicleTypeCode\>

                        \<VehicleTypeDesc\>Truck\</VehicleTypeDesc\>

                        \<ModelYear\>2000\</ModelYear\>

                        \<Make\>CHE\</Make\>

                        \<MakeDesc\>CHEVROLET\</MakeDesc\>

                        \<Model\>SUBURBAN\</Model\>

                        \<BodyStyleCode\>UT\</BodyStyleCode\>

                        \<BodyStyleDesc\>Sport Utility Vehicle\</BodyStyleDesc\>

                        \<StateOfRegistration\>KY\</StateOfRegistration\>

                        \<TransactionDate\>20101203\</TransactionDate\>

                        \<ExpirationDate\>20210601\</ExpirationDate\>

                        \<PlateTypeCode\>Z\</PlateTypeCode\>

                        \<PlateTypeDesc\>Regular\</PlateTypeDesc\>

                        \<LicensePlateNumber\>1KMC11\</LicensePlateNumber\>

                        \<IsBranded\>false\</IsBranded\>

                        \<LeaseInd\>N\</LeaseInd\>

                        \<NameCode1\>A\</NameCode1\>

                        \<NameCodeDesc1\>Owner\</NameCodeDesc1\>

                        \<NameTitleCode1\>1\</NameTitleCode1\>

                        \<NameTitleDesc1\>MR\</NameTitleDesc1\>

                        \<RegisteredOwnerName\>

                            \<GivenName\>JOHNSON\</GivenName\>

                            \<Surname\>JONNIE\</Surname\>

                        \</RegisteredOwnerName\>

                        \<Address\>

                            \<AddressType\>S\</AddressType\>

                            \<Street1\>2700 NEW HOLD RD\</Street1\>

                            \<City\>PADUCAH\</City\>

                            \<StateCode\>KY\</StateCode\>

                            \<Zip\>42001\</Zip\>

                        \</Address\>

                    \</RegistrationData\>

                    \<NumberofVehicleOwners\>1\</NumberofVehicleOwners\>

                    \<IsVehicleSalvage\>false\</IsVehicleSalvage\>

                    \<SupplementalCatClaimIndicator\>N\</SupplementalCatClaimIndicator\>

                    \<ReasonCodeDetails\>

                        \<Reason\>

                            \<Code\>AG-2.22\</Code\>

                            \<Description\>Vehicle has out of state Registration.  \</Description\>

                        \</Reason\>

                        \<Reason\>

                            \<Code\>AO-5.01\</Code\>

                            \<Description\>Vehicle is not owned by Policy Holder or any Driver on the Policy.\</Description\>

                        \</Reason\>

                    \</ReasonCodeDetails\>

                    \<ActionMessages\>

                        \<ActionMessage\>Ask for Vehicle Registration\</ActionMessage\>

                    \</ActionMessages\>

                    \<Mileage\>

                        \<Sources\>

                            \<Source\>

                                \<Name\>VeriskMileageModel\</Name\>

                                \<Miles\>8218\</Miles\>

                            \</Source\>

                        \</Sources\>

                    \</Mileage\>

                    \<SmartScore\>

                        \<EnrollmentStatus\>EN\</EnrollmentStatus\>

                        \<EnrollmentDate\>2022-01-01 05:00:41.394\</EnrollmentDate\>

                        \<ProductEnrollmentStatus\>EN\</ProductEnrollmentStatus\>

                        \<ScoreStatus\>SU\</ScoreStatus\>

                        \<ScoreType\>Recent\</ScoreType\>

                        \<Score\>100\</Score\>

                        \<ScoreStartDate\>2022-11-21 00:00:00.000\</ScoreStartDate\>

                        \<ScoreEndDate\>2023-01-29 23:59:59.000\</ScoreEndDate\>

                    \</SmartScore\>

                    \<VinMaster\>

                        \<Vehicles\>

                            \<Vehicle\>

                                \<VIN\>3GN\&amp;K16T\&amp;Y\</VIN\>

                                \<FullModelYear\>2000\</FullModelYear\>

                                \<Make\>CHEV\</Make\>

                                \<MakeDescription\>CHEVROLET\</MakeDescription\>

                                \<BasicModelName\>SUBURBAN\</BasicModelName\>

                                \<FullModelName\>SUBURBAN 1500 BASE/LS/LT\</FullModelName\>

                                \<BodyStyle\>UTL4X44D\</BodyStyle\>

                                \<BodyStyleDescription\>Utility Vehicle \- Four-Wheel Drive 4-Door\</BodyStyleDescription\>

                                \<CurbWeight\>05123\</CurbWeight\>

                                \<Horsepower\>0285\</Horsepower\>

                                \<GrossVehicleWeight\>07200\</GrossVehicleWeight\>

                                \<PayloadCapacity\>2077\</PayloadCapacity\>

                                \<Height\>073.3\</Height\>

                                \<EngineSize\>5.3\</EngineSize\>

                                \<Wheelbase\>130.0\</Wheelbase\>

                                \<EngineCylinders\>8\</EngineCylinders\>

                                \<EngineCylindersDescription\>Eight-Cylinder Engine\</EngineCylindersDescription\>

                                \<EngineTypeDescription\>Other Type of Engine\</EngineTypeDescription\>

                                \<FourWheelDriveIndicator\>4\</FourWheelDriveIndicator\>

                                \<FourWheelDriveIndicatorDescription\>Vehicle is four-wheel drive\</FourWheelDriveIndicatorDescription\>

                                \<Restraint\>S\</Restraint\>

                                \<RestraintDescription\>Driver \&amp; Front Passenger Front \&amp; Side Airbags\</RestraintDescription\>

                                \<ClassCode\>93\</ClassCode\>

                                \<ClassCodeDescription\>Large Utility\</ClassCodeDescription\>

                                \<TonnageIndicator\>15\</TonnageIndicator\>

                                \<TonnageIndicatorDescription\>3.75 tons (07001 to 07500 lbs)\</TonnageIndicatorDescription\>

                                \<AntiLockBrakes\>S\</AntiLockBrakes\>

                                \<AntiLockBrakesDescription\>Anti-Lock Brakes are standard equipment\</AntiLockBrakesDescription\>

                                \<AntiTheftIndicator\>P\</AntiTheftIndicator\>

                                \<AntiTheftIndicatorDescription\>Passive Disabling\</AntiTheftIndicatorDescription\>

                                \<ElectronicStabilityControl\>N\</ElectronicStabilityControl\>

                                \<ElectronicStabilityControlDescription\>Electronic Stability Control is not available\</ElectronicStabilityControlDescription\>

                                \<DaytimeRunningLightIndicator\>S\</DaytimeRunningLightIndicator\>

                                \<DaytimeRunningLightIndicatorDescription\>Daytime Running Lights Standard Equipment\</DaytimeRunningLightIndicatorDescription\>

                                \<CircularNumber\>0001\</CircularNumber\>

                                \<RecordType\>S\</RecordType\>

                                \<PriceNewSymbol\_27SymbolTable\_OnePosition\>P\</PriceNewSymbol\_27SymbolTable\_OnePosition\>

                                \<PriceNewSymbol\_27SymbolTable\_TwoPositions\>21\</PriceNewSymbol\_27SymbolTable\_TwoPositions\>

                                \<PriceNew\_Min\>36001.00\</PriceNew\_Min\>

                                \<PriceNew\_Max\>40000.99\</PriceNew\_Max\>

                                \<PhysicalDamage\>

                                    \<CombinedVSRSymbol\_OnePosition\>F\</CombinedVSRSymbol\_OnePosition\>

                                    \<CombinedVSRSymbol\_TwoPositions\>13\</CombinedVSRSymbol\_TwoPositions\>

                                \</PhysicalDamage\>

                            \</Vehicle\>

                        \</Vehicles\>

                    \</VinMaster\>

                    \<RiskAnalyzer\>

                        \<Vehicles\>

                            \<Vehicle\>

                                \<VIN\>3GN\&amp;K16T\&amp;Y\</VIN\>

                                \<ModelYear\>2000\</ModelYear\>

                                \<DistributionDate\>2212\</DistributionDate\>

                                \<Restraint\>S\</Restraint\>

                                \<AntiLockBrakes\>S\</AntiLockBrakes\>

                                \<EngineCylinders\>8\</EngineCylinders\>

                                \<Make\>CHEV\</Make\>

                                \<BasicModelName\>SUBURBAN\</BasicModelName\>

                                \<BodyStyle\>UTL4X44D\</BodyStyle\>

                                \<EngineSize\>5.3\</EngineSize\>

                                \<FourWheelDriveIndicator\>4\</FourWheelDriveIndicator\>

                                \<ElectronicStabilityControl\>N\</ElectronicStabilityControl\>

                                \<TonnageIndicator\>15\</TonnageIndicator\>

                                \<PayloadCapacity\>2077\</PayloadCapacity\>

                                \<FullModelName\>SUBURBAN 1500 BASE/LS/LT\</FullModelName\>

                                \<DaytimeRunningLightIndicator\>S\</DaytimeRunningLightIndicator\>

                                \<Wheelbase\>130\</Wheelbase\>

                                \<ClassCode\>93\</ClassCode\>

                                \<AntiTheftIndicator\>P\</AntiTheftIndicator\>

                                \<CurbWeight\>5123\</CurbWeight\>

                                \<GrossVehicleWeight\>7200\</GrossVehicleWeight\>

                                \<Height\>73.3\</Height\>

                                \<Horsepower\>285\</Horsepower\>

                                \<StateException\>TX\</StateException\>

                                \<NCICCode\>CHEV\</NCICCode\>

                                \<Length\>0\</Length\>

                                \<Width\>0\</Width\>

                                \<BaseMSRP\>36001\</BaseMSRP\>

                                \<SpecialHandlingIndicator\>N\</SpecialHandlingIndicator\>

                                \<InterimIndicator\>N\</InterimIndicator\>

                                \<ReleaseDate\>2303\</ReleaseDate\>

                                \<PhysicalDamage\>

                                    \<RiskAnalyzerCollisionIndicatedSymbol\>EJ\</RiskAnalyzerCollisionIndicatedSymbol\>

                                    \<RiskAnalyzerComprehensiveIndicatedSymbol\>DG\</RiskAnalyzerComprehensiveIndicatedSymbol\>

                                    \<RiskAnalyzerCollisionRatingSymbol\>EJ\</RiskAnalyzerCollisionRatingSymbol\>

                                    \<RiskAnalyzerComprehensiveRatingSymbol\>DG\</RiskAnalyzerComprehensiveRatingSymbol\>

                                    \<RiskAnalyzerComprehensiveNonGlassRatingSymbol\>DG\</RiskAnalyzerComprehensiveNonGlassRatingSymbol\>

                                    \<RiskAnalyzerCollisionCappingIndicator\>N\</RiskAnalyzerCollisionCappingIndicator\>

                                    \<RiskAnalyzerComprehensiveCappingIndicator\>N\</RiskAnalyzerComprehensiveCappingIndicator\>

                                    \<RiskAnalyzerComprehensiveNonGlassCappingIndicator\>N\</RiskAnalyzerComprehensiveNonGlassCappingIndicator\>

                                    \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbol\>DG\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbol\>

                                \</PhysicalDamage\>

                                \<Liability\>

                                    \<RiskAnalyzerMedicalPaymentsIndicatedSymbol\>FE\</RiskAnalyzerMedicalPaymentsIndicatedSymbol\>

                                    \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbol\>EH\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbol\>

                                    \<RiskAnalyzerSingleLimitIndicatedSymbol\>MK\</RiskAnalyzerSingleLimitIndicatedSymbol\>

                                    \<RiskAnalyzerBodilyInjuryRatingSymbol\>LH\</RiskAnalyzerBodilyInjuryRatingSymbol\>

                                    \<RiskAnalyzerPropertyDamageRatingSymbol\>MN\</RiskAnalyzerPropertyDamageRatingSymbol\>

                                    \<RiskAnalyzerMedicalPaymentsRatingSymbol\>FE\</RiskAnalyzerMedicalPaymentsRatingSymbol\>

                                    \<RiskAnalyzerPersonalInjuryProtectionRatingSymbol\>EH\</RiskAnalyzerPersonalInjuryProtectionRatingSymbol\>

                                    \<RiskAnalyzerSingleLimitRatingSymbol\>MK\</RiskAnalyzerSingleLimitRatingSymbol\>

                                    \<RiskAnalyzerBodilyInjuryCappingIndicator\>N\</RiskAnalyzerBodilyInjuryCappingIndicator\>

                                    \<RiskAnalyzerPropertyDamageCappingIndicator\>N\</RiskAnalyzerPropertyDamageCappingIndicator\>

                                    \<RiskAnalyzerMedicalPaymentsCappingIndicator\>N\</RiskAnalyzerMedicalPaymentsCappingIndicator\>

                                    \<RiskAnalyzerPersonalInjuryProtectionCappingIndicator\>N\</RiskAnalyzerPersonalInjuryProtectionCappingIndicator\>

                                    \<RiskAnalyzerBodilyInjuryIndicatedSymbol\>LH\</RiskAnalyzerBodilyInjuryIndicatedSymbol\>

                                    \<RiskAnalyzerPropertyDamageIndicatedSymbol\>MN\</RiskAnalyzerPropertyDamageIndicatedSymbol\>

                                    \<RiskAnalyzerSingleLimitCappingIndicator\>N\</RiskAnalyzerSingleLimitCappingIndicator\>

                                \</Liability\>

                            \</Vehicle\>

                        \</Vehicles\>

                    \</RiskAnalyzer\>

                \</Vehicle\>

                \<Vehicle\>

                    \<Sequence\>3\</Sequence\>

                    \<DataSource\>Principal\</DataSource\>

                    \<IsVehicleVerified\>true\</IsVehicleVerified\>

                    \<IsVehicleActiveDuringMostRecentTerm\>true\</IsVehicleActiveDuringMostRecentTerm\>

                    \<EntityScore\>60\</EntityScore\>

                    \<VIN\>1HGCM56306A148752\</VIN\>

                    \<VehiclePolicyData\>

                        \<Year\>2006\</Year\>

                        \<Make\>HOND\</Make\>

                        \<Model\>ASE\</Model\>

                        \<BusinessUse\>N\</BusinessUse\>

                        \<ClassCode\>000000\</ClassCode\>

                        \<CollisionDeductibleAmount\>1000\</CollisionDeductibleAmount\>

                        \<ComprehensiveDeductibleAmount\>500\</ComprehensiveDeductibleAmount\>

                        \<FromDate\>20230105\</FromDate\>

                        \<ToDate\>20240105\</ToDate\>

                        \<CollisionIndicator\>Y\</CollisionIndicator\>

                        \<ComprehensiveIndicator\>Y\</ComprehensiveIndicator\>

                        \<Coverages\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>BINJ\</Code\>

                                    \<Description\>Bodily Injury\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>40000\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>80000\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>PDMG\</Code\>

                                    \<Description\>Property Damage\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>CBSL\</Code\>

                                    \<Description\>CSL (BI \&amp; PD)\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>0\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>0\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>80000\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>UMPD\</Code\>

                                    \<Description\>Uninsured Motorist (PD)\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>PINJ\</Code\>

                                    \<Description\>Personal Injury\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                        \</Coverages\>

                    \</VehiclePolicyData\>

                    \<RegistrationData\>

                        \<VINMatch\>Y\</VINMatch\>

                        \<ValidVINIndicator\>Y\</ValidVINIndicator\>

                        \<VINChangeIndicator\>N\</VINChangeIndicator\>

                        \<VIN\>1HGCM56306A148752\</VIN\>

                        \<VehicleTypeCode\>P\</VehicleTypeCode\>

                        \<VehicleTypeDesc\>Passenger Car\</VehicleTypeDesc\>

                        \<ModelYear\>2006\</ModelYear\>

                        \<Make\>HON\</Make\>

                        \<MakeDesc\>HONDA\</MakeDesc\>

                        \<Model\>ACCORD\</Model\>

                        \<BodyStyleCode\>SD\</BodyStyleCode\>

                        \<BodyStyleDesc\>Sedan\</BodyStyleDesc\>

                        \<StateOfRegistration\>CO\</StateOfRegistration\>

                        \<TransactionDate\>20091028\</TransactionDate\>

                        \<ExpirationDate\>20211231\</ExpirationDate\>

                        \<PlateTypeCode\>Z\</PlateTypeCode\>

                        \<PlateTypeDesc\>Regular\</PlateTypeDesc\>

                        \<LicensePlateNumber\>403OAK\</LicensePlateNumber\>

                        \<IsBranded\>true\</IsBranded\>

                        \<BrandedTitleState1\>CO\</BrandedTitleState1\>

                        \<BrandedTitleDate1\>20150815\</BrandedTitleDate1\>

                        \<BrandedTitleCode1\>H\</BrandedTitleCode1\>

                        \<BrandedTitleDesc1\>REBUILT\</BrandedTitleDesc1\>

                        \<BrandedTitleState2\>OR\</BrandedTitleState2\>

                        \<BrandedTitleDate2\>20150615\</BrandedTitleDate2\>

                        \<BrandedTitleCode2\>J\</BrandedTitleCode2\>

                        \<BrandedTitleDesc2\>SALVAGE\</BrandedTitleDesc2\>

                        \<LeaseInd\>N\</LeaseInd\>

                        \<NameCode1\>A\</NameCode1\>

                        \<NameCodeDesc1\>Owner\</NameCodeDesc1\>

                        \<NameTitleCode1\>1\</NameTitleCode1\>

                        \<NameTitleDesc1\>MR\</NameTitleDesc1\>

                        \<RegisteredOwnerName\>

                            \<GivenName\>JAMES\</GivenName\>

                            \<MiddleName\>W\</MiddleName\>

                            \<Surname\>LEYDEN\</Surname\>

                        \</RegisteredOwnerName\>

                        \<Address\>

                            \<AddressType\>S\</AddressType\>

                            \<Street1\>10558 PAINT PL\</Street1\>

                            \<City\>LITTLETON\</City\>

                            \<StateCode\>CO\</StateCode\>

                            \<Zip\>80125\</Zip\>

                        \</Address\>

                    \</RegistrationData\>

                    \<NumberofVehicleOwners\>1\</NumberofVehicleOwners\>

                    \<IsVehicleSalvage\>true\</IsVehicleSalvage\>

                    \<SupplementalCatClaimIndicator\>N\</SupplementalCatClaimIndicator\>

                    \<ReasonCodeDetails\>

                        \<Reason\>

                            \<Code\>AG-2.22\</Code\>

                            \<Description\>Vehicle has out of state Registration.  \</Description\>

                        \</Reason\>

                        \<Reason\>

                            \<Code\>AO-5.01\</Code\>

                            \<Description\>Vehicle is not owned by Policy Holder or any Driver on the Policy.\</Description\>

                        \</Reason\>

                        \<Reason\>

                            \<Code\>MI-7.01\</Code\>

                            \<Description\>The vehicle has a salvage, flood or junk title\</Description\>

                        \</Reason\>

                    \</ReasonCodeDetails\>

                    \<ActionMessages\>

                        \<ActionMessage\>Ask for Vehicle Registration\</ActionMessage\>

                    \</ActionMessages\>

                    \<Mileage\>

                        \<Sources\>

                            \<Source\>

                                \<Name\>VeriskMileageModel\</Name\>

                                \<Miles\>11059\</Miles\>

                            \</Source\>

                        \</Sources\>

                    \</Mileage\>

                    \<VinMaster\>

                        \<Vehicles\>

                            \<Vehicle\>

                                \<VIN\>1HGCM563\&amp;6\</VIN\>

                                \<FullModelYear\>2006\</FullModelYear\>

                                \<Make\>HOND\</Make\>

                                \<MakeDescription\>HONDA\</MakeDescription\>

                                \<BasicModelName\>ACCORD\</BasicModelName\>

                                \<FullModelName\>ACCORD SE\</FullModelName\>

                                \<BodyStyle\>SEDAN 4D\</BodyStyle\>

                                \<BodyStyleDescription\>4-Door Sedan\</BodyStyleDescription\>

                                \<CurbWeight\>03197\</CurbWeight\>

                                \<Horsepower\>0166\</Horsepower\>

                                \<GrossVehicleWeight\>00000\</GrossVehicleWeight\>

                                \<PayloadCapacity\>0000\</PayloadCapacity\>

                                \<Height\>057.2\</Height\>

                                \<EngineSize\>2.4\</EngineSize\>

                                \<Wheelbase\>107.9\</Wheelbase\>

                                \<EngineCylinders\>4\</EngineCylinders\>

                                \<EngineCylindersDescription\>Four-Cylinder Engine\</EngineCylindersDescription\>

                                \<EngineTypeDescription\>Other Type of Engine\</EngineTypeDescription\>

                                \<FourWheelDriveIndicatorDescription\>Vehicle is not four-wheel drive\</FourWheelDriveIndicatorDescription\>

                                \<Restraint\>R\</Restraint\>

                                \<RestraintDescription\>Driver \&amp; Front Passenger Front, Side \&amp; Head Airbags, Rear Passenger Head Airbags\</RestraintDescription\>

                                \<ClassCode\>34\</ClassCode\>

                                \<ClassCodeDescription\>Midsize 4-Door\</ClassCodeDescription\>

                                \<VMPerformanceIndicatorDescription\>Standard\</VMPerformanceIndicatorDescription\>

                                \<TonnageIndicator\>00\</TonnageIndicator\>

                                \<TonnageIndicatorDescription\>N/A\</TonnageIndicatorDescription\>

                                \<AntiLockBrakes\>S\</AntiLockBrakes\>

                                \<AntiLockBrakesDescription\>Anti-Lock Brakes are standard equipment\</AntiLockBrakesDescription\>

                                \<AntiTheftIndicator\>P\</AntiTheftIndicator\>

                                \<AntiTheftIndicatorDescription\>Passive Disabling\</AntiTheftIndicatorDescription\>

                                \<ElectronicStabilityControl\>O\</ElectronicStabilityControl\>

                                \<ElectronicStabilityControlDescription\>Electronic Stability Control is optional equipment\</ElectronicStabilityControlDescription\>

                                \<DaytimeRunningLightIndicator\>S\</DaytimeRunningLightIndicator\>

                                \<DaytimeRunningLightIndicatorDescription\>Daytime Running Lights Standard Equipment\</DaytimeRunningLightIndicatorDescription\>

                                \<CircularNumber\>0512\</CircularNumber\>

                                \<RecordType\>S\</RecordType\>

                                \<PriceNewSymbol\_27SymbolTable\_OnePosition\>G\</PriceNewSymbol\_27SymbolTable\_OnePosition\>

                                \<PriceNewSymbol\_27SymbolTable\_TwoPositions\>14\</PriceNewSymbol\_27SymbolTable\_TwoPositions\>

                                \<PriceNew\_Min\>20001.00\</PriceNew\_Min\>

                                \<PriceNew\_Max\>22000.99\</PriceNew\_Max\>

                                \<PhysicalDamage\>

                                    \<CombinedVSRSymbol\_OnePosition\>E\</CombinedVSRSymbol\_OnePosition\>

                                    \<CombinedVSRSymbol\_TwoPositions\>12\</CombinedVSRSymbol\_TwoPositions\>

                                \</PhysicalDamage\>

                            \</Vehicle\>

                        \</Vehicles\>

                    \</VinMaster\>

                    \<RiskAnalyzer\>

                        \<Vehicles\>

                            \<Vehicle\>

                                \<VIN\>1HGCM563\&amp;6\</VIN\>

                                \<ModelYear\>2006\</ModelYear\>

                                \<DistributionDate\>2212\</DistributionDate\>

                                \<Restraint\>R\</Restraint\>

                                \<AntiLockBrakes\>S\</AntiLockBrakes\>

                                \<EngineCylinders\>4\</EngineCylinders\>

                                \<Make\>HOND\</Make\>

                                \<BasicModelName\>ACCORD\</BasicModelName\>

                                \<BodyStyle\>SEDAN 4D\</BodyStyle\>

                                \<EngineSize\>2.4\</EngineSize\>

                                \<ElectronicStabilityControl\>O\</ElectronicStabilityControl\>

                                \<TonnageIndicator\>00\</TonnageIndicator\>

                                \<PayloadCapacity\>0\</PayloadCapacity\>

                                \<FullModelName\>ACCORD SE\</FullModelName\>

                                \<DaytimeRunningLightIndicator\>S\</DaytimeRunningLightIndicator\>

                                \<Wheelbase\>107.9\</Wheelbase\>

                                \<ClassCode\>34\</ClassCode\>

                                \<AntiTheftIndicator\>P\</AntiTheftIndicator\>

                                \<CurbWeight\>3197\</CurbWeight\>

                                \<GrossVehicleWeight\>0\</GrossVehicleWeight\>

                                \<Height\>57.2\</Height\>

                                \<Horsepower\>166\</Horsepower\>

                                \<NCICCode\>HOND\</NCICCode\>

                                \<Chassis\>U\</Chassis\>

                                \<Length\>0\</Length\>

                                \<Width\>0\</Width\>

                                \<BaseMSRP\>20001\</BaseMSRP\>

                                \<SpecialHandlingIndicator\>N\</SpecialHandlingIndicator\>

                                \<InterimIndicator\>N\</InterimIndicator\>

                                \<SpecialInfoSelector\>M\</SpecialInfoSelector\>

                                \<ModelSeriesInfo\>CURB\</ModelSeriesInfo\>

                                \<ReleaseDate\>2303\</ReleaseDate\>

                                \<PhysicalDamage\>

                                    \<RiskAnalyzerCollisionIndicatedSymbol\>DM\</RiskAnalyzerCollisionIndicatedSymbol\>

                                    \<RiskAnalyzerComprehensiveIndicatedSymbol\>CE\</RiskAnalyzerComprehensiveIndicatedSymbol\>

                                    \<RiskAnalyzerCollisionRatingSymbol\>DM\</RiskAnalyzerCollisionRatingSymbol\>

                                    \<RiskAnalyzerComprehensiveRatingSymbol\>CE\</RiskAnalyzerComprehensiveRatingSymbol\>

                                    \<RiskAnalyzerComprehensiveNonGlassRatingSymbol\>CF\</RiskAnalyzerComprehensiveNonGlassRatingSymbol\>

                                    \<RiskAnalyzerCollisionCappingIndicator\>N\</RiskAnalyzerCollisionCappingIndicator\>

                                    \<RiskAnalyzerComprehensiveCappingIndicator\>N\</RiskAnalyzerComprehensiveCappingIndicator\>

                                    \<RiskAnalyzerComprehensiveNonGlassCappingIndicator\>N\</RiskAnalyzerComprehensiveNonGlassCappingIndicator\>

                                    \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbol\>CF\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbol\>

                                \</PhysicalDamage\>

                                \<Liability\>

                                    \<RiskAnalyzerMedicalPaymentsIndicatedSymbol\>NR\</RiskAnalyzerMedicalPaymentsIndicatedSymbol\>

                                    \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbol\>MM\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbol\>

                                    \<RiskAnalyzerSingleLimitIndicatedSymbol\>ML\</RiskAnalyzerSingleLimitIndicatedSymbol\>

                                    \<RiskAnalyzerBodilyInjuryRatingSymbol\>ML\</RiskAnalyzerBodilyInjuryRatingSymbol\>

                                    \<RiskAnalyzerPropertyDamageRatingSymbol\>MK\</RiskAnalyzerPropertyDamageRatingSymbol\>

                                    \<RiskAnalyzerMedicalPaymentsRatingSymbol\>NR\</RiskAnalyzerMedicalPaymentsRatingSymbol\>

                                    \<RiskAnalyzerPersonalInjuryProtectionRatingSymbol\>MM\</RiskAnalyzerPersonalInjuryProtectionRatingSymbol\>

                                    \<RiskAnalyzerSingleLimitRatingSymbol\>ML\</RiskAnalyzerSingleLimitRatingSymbol\>

                                    \<RiskAnalyzerBodilyInjuryCappingIndicator\>N\</RiskAnalyzerBodilyInjuryCappingIndicator\>

                                    \<RiskAnalyzerPropertyDamageCappingIndicator\>N\</RiskAnalyzerPropertyDamageCappingIndicator\>

                                    \<RiskAnalyzerMedicalPaymentsCappingIndicator\>N\</RiskAnalyzerMedicalPaymentsCappingIndicator\>

                                    \<RiskAnalyzerPersonalInjuryProtectionCappingIndicator\>N\</RiskAnalyzerPersonalInjuryProtectionCappingIndicator\>

                                    \<RiskAnalyzerBodilyInjuryIndicatedSymbol\>ML\</RiskAnalyzerBodilyInjuryIndicatedSymbol\>

                                    \<RiskAnalyzerPropertyDamageIndicatedSymbol\>MK\</RiskAnalyzerPropertyDamageIndicatedSymbol\>

                                    \<RiskAnalyzerSingleLimitCappingIndicator\>N\</RiskAnalyzerSingleLimitCappingIndicator\>

                                \</Liability\>

                            \</Vehicle\>

                        \</Vehicles\>

                    \</RiskAnalyzer\>

                \</Vehicle\>

                \<Vehicle\>

                    \<Sequence\>4\</Sequence\>

                    \<DataSource\>Principal\</DataSource\>

                    \<IsVehicleVerified\>true\</IsVehicleVerified\>

                    \<IsVehicleActiveDuringMostRecentTerm\>true\</IsVehicleActiveDuringMostRecentTerm\>

                    \<EntityScore\>60\</EntityScore\>

                    \<VIN\>1GKER23788J291227\</VIN\>

                    \<VehiclePolicyData\>

                        \<Year\>2008\</Year\>

                        \<Make\>GMC\</Make\>

                        \<Model\>S1F\</Model\>

                        \<BusinessUse\>Y\</BusinessUse\>

                        \<ClassCode\>000000\</ClassCode\>

                        \<CollisionDeductibleAmount\>1000\</CollisionDeductibleAmount\>

                        \<ComprehensiveDeductibleAmount\>500\</ComprehensiveDeductibleAmount\>

                        \<FromDate\>20230105\</FromDate\>

                        \<ToDate\>20240105\</ToDate\>

                        \<CollisionIndicator\>Y\</CollisionIndicator\>

                        \<ComprehensiveIndicator\>Y\</ComprehensiveIndicator\>

                        \<Coverages\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>BINJ\</Code\>

                                    \<Description\>Bodily Injury\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>40000\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>80000\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>PDMG\</Code\>

                                    \<Description\>Property Damage\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>CBSL\</Code\>

                                    \<Description\>CSL (BI \&amp; PD)\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>0\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>0\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>80000\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>UMPD\</Code\>

                                    \<Description\>Uninsured Motorist (PD)\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                            \<Coverage\>

                                \<CoverageType\>

                                    \<Code\>PINJ\</Code\>

                                    \<Description\>Personal Injury\</Description\>

                                \</CoverageType\>

                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                \<FromDate\>20230105\</FromDate\>

                                \<ToDate\>20240105\</ToDate\>

                            \</Coverage\>

                        \</Coverages\>

                    \</VehiclePolicyData\>

                    \<RegistrationData\>

                        \<VINMatch\>Y\</VINMatch\>

                        \<ValidVINIndicator\>Y\</ValidVINIndicator\>

                        \<VINChangeIndicator\>N\</VINChangeIndicator\>

                        \<VIN\>1GKER23788J291227\</VIN\>

                        \<VehicleTypeCode\>T\</VehicleTypeCode\>

                        \<VehicleTypeDesc\>Truck\</VehicleTypeDesc\>

                        \<ModelYear\>2008\</ModelYear\>

                        \<Make\>GMC\</Make\>

                        \<MakeDesc\>GMC\</MakeDesc\>

                        \<Model\>ACADIA\</Model\>

                        \<BodyStyleCode\>UT\</BodyStyleCode\>

                        \<BodyStyleDesc\>Sport Utility Vehicle\</BodyStyleDesc\>

                        \<StateOfRegistration\>TX\</StateOfRegistration\>

                        \<TransactionDate\>20090801\</TransactionDate\>

                        \<ExpirationDate\>20210331\</ExpirationDate\>

                        \<PlateTypeCode\>Z\</PlateTypeCode\>

                        \<PlateTypeDesc\>Regular\</PlateTypeDesc\>

                        \<LicensePlateNumber\>JRR530\</LicensePlateNumber\>

                        \<IsBranded\>false\</IsBranded\>

                        \<LeaseInd\>N\</LeaseInd\>

                        \<NameCode1\>A\</NameCode1\>

                        \<NameCodeDesc1\>Owner\</NameCodeDesc1\>

                        \<NameTitleCode1\>1\</NameTitleCode1\>

                        \<NameTitleDesc1\>MR\</NameTitleDesc1\>

                        \<RegisteredOwnerName\>

                            \<GivenName\>ROBERT\</GivenName\>

                            \<MiddleName\>J\</MiddleName\>

                            \<Surname\>PATTERSON\</Surname\>

                        \</RegisteredOwnerName\>

                        \<Address\>

                            \<AddressType\>S\</AddressType\>

                            \<Street1\>121 CHAPEL HILL DR\</Street1\>

                            \<City\>PROSPER\</City\>

                            \<StateCode\>TX\</StateCode\>

                            \<Zip\>75078\</Zip\>

                        \</Address\>

                    \</RegistrationData\>

                    \<NumberofVehicleOwners\>1\</NumberofVehicleOwners\>

                    \<IsVehicleSalvage\>false\</IsVehicleSalvage\>

                    \<SupplementalCatClaimIndicator\>N\</SupplementalCatClaimIndicator\>

                    \<ReasonCodeDetails\>

                        \<Reason\>

                            \<Code\>AG-2.22\</Code\>

                            \<Description\>Vehicle has out of state Registration.  \</Description\>

                        \</Reason\>

                        \<Reason\>

                            \<Code\>AO-5.01\</Code\>

                            \<Description\>Vehicle is not owned by Policy Holder or any Driver on the Policy.\</Description\>

                        \</Reason\>

                    \</ReasonCodeDetails\>

                    \<ActionMessages\>

                        \<ActionMessage\>Ask for Vehicle Registration\</ActionMessage\>

                    \</ActionMessages\>

                    \<Mileage\>

                        \<Sources\>

                            \<Source\>

                                \<Name\>VeriskMileageModel\</Name\>

                                \<Miles\>11080\</Miles\>

                            \</Source\>

                        \</Sources\>

                    \</Mileage\>

                    \<SmartScore\>

                        \<EnrollmentStatus\>EN\</EnrollmentStatus\>

                        \<EnrollmentDate\>2022-01-01 05:00:41.394\</EnrollmentDate\>

                        \<ProductEnrollmentStatus\>EN\</ProductEnrollmentStatus\>

                        \<ScoreStatus\>SU\</ScoreStatus\>

                        \<ScoreType\>Recent\</ScoreType\>

                        \<Score\>86\</Score\>

                        \<ScoreStartDate\>2022-11-21 00:00:00.000\</ScoreStartDate\>

                        \<ScoreEndDate\>2023-01-29 23:59:59.000\</ScoreEndDate\>

                    \</SmartScore\>

                    \<VinMaster\>

                        \<Vehicles\>

                            \<Vehicle\>

                                \<VIN\>1GK\&amp;R237\&amp;8\</VIN\>

                                \<FullModelYear\>2008\</FullModelYear\>

                                \<Make\>GMC\</Make\>

                                \<MakeDescription\>GMC\</MakeDescription\>

                                \<BasicModelName\>ACADIA\</BasicModelName\>

                                \<FullModelName\>ACADIA SLT1\</FullModelName\>

                                \<BodyStyle\>UTL4X24D\</BodyStyle\>

                                \<BodyStyleDescription\>Utility Vehicle \- Two-Wheel Drive 4-Door\</BodyStyleDescription\>

                                \<CurbWeight\>04722\</CurbWeight\>

                                \<Horsepower\>0275\</Horsepower\>

                                \<GrossVehicleWeight\>06400\</GrossVehicleWeight\>

                                \<PayloadCapacity\>1678\</PayloadCapacity\>

                                \<Height\>069.9\</Height\>

                                \<EngineSize\>3.6\</EngineSize\>

                                \<Wheelbase\>118.9\</Wheelbase\>

                                \<EngineCylinders\>6\</EngineCylinders\>

                                \<EngineCylindersDescription\>Six-Cylinder Engine\</EngineCylindersDescription\>

                                \<EngineTypeDescription\>Other Type of Engine\</EngineTypeDescription\>

                                \<FourWheelDriveIndicatorDescription\>Vehicle is not four-wheel drive\</FourWheelDriveIndicatorDescription\>

                                \<Restraint\>R\</Restraint\>

                                \<RestraintDescription\>Driver \&amp; Front Passenger Front, Side \&amp; Head Airbags, Rear Passenger Head Airbags\</RestraintDescription\>

                                \<ClassCode\>93\</ClassCode\>

                                \<ClassCodeDescription\>Large Utility\</ClassCodeDescription\>

                                \<VMPerformanceIndicatorDescription\>Standard\</VMPerformanceIndicatorDescription\>

                                \<TonnageIndicator\>13\</TonnageIndicator\>

                                \<TonnageIndicatorDescription\>3.25 tons (06001 to 06500 lbs)\</TonnageIndicatorDescription\>

                                \<AntiLockBrakes\>S\</AntiLockBrakes\>

                                \<AntiLockBrakesDescription\>Anti-Lock Brakes are standard equipment\</AntiLockBrakesDescription\>

                                \<AntiTheftIndicator\>P\</AntiTheftIndicator\>

                                \<AntiTheftIndicatorDescription\>Passive Disabling\</AntiTheftIndicatorDescription\>

                                \<ElectronicStabilityControl\>S\</ElectronicStabilityControl\>

                                \<ElectronicStabilityControlDescription\>Electronic Stability Control is standard equipment\</ElectronicStabilityControlDescription\>

                                \<DaytimeRunningLightIndicator\>S\</DaytimeRunningLightIndicator\>

                                \<DaytimeRunningLightIndicatorDescription\>Daytime Running Lights Standard Equipment\</DaytimeRunningLightIndicatorDescription\>

                                \<CircularNumber\>1010\</CircularNumber\>

                                \<RecordType\>S\</RecordType\>

                                \<PriceNewSymbol\_27SymbolTable\_OnePosition\>N\</PriceNewSymbol\_27SymbolTable\_OnePosition\>

                                \<PriceNewSymbol\_27SymbolTable\_TwoPositions\>20\</PriceNewSymbol\_27SymbolTable\_TwoPositions\>

                                \<PriceNew\_Min\>33001.00\</PriceNew\_Min\>

                                \<PriceNew\_Max\>36000.99\</PriceNew\_Max\>

                                \<PhysicalDamage\>

                                    \<CombinedVSRSymbol\_OnePosition\>E\</CombinedVSRSymbol\_OnePosition\>

                                    \<CombinedVSRSymbol\_TwoPositions\>12\</CombinedVSRSymbol\_TwoPositions\>

                                \</PhysicalDamage\>

                            \</Vehicle\>

                        \</Vehicles\>

                    \</VinMaster\>

                    \<RiskAnalyzer\>

                        \<Vehicles\>

                            \<Vehicle\>

                                \<VIN\>1GK\&amp;R237\&amp;8\</VIN\>

                                \<ModelYear\>2008\</ModelYear\>

                                \<DistributionDate\>2212\</DistributionDate\>

                                \<Restraint\>R\</Restraint\>

                                \<AntiLockBrakes\>S\</AntiLockBrakes\>

                                \<EngineCylinders\>6\</EngineCylinders\>

                                \<Make\>GMC\</Make\>

                                \<BasicModelName\>ACADIA\</BasicModelName\>

                                \<BodyStyle\>UTL4X24D\</BodyStyle\>

                                \<EngineSize\>3.6\</EngineSize\>

                                \<ElectronicStabilityControl\>S\</ElectronicStabilityControl\>

                                \<TonnageIndicator\>13\</TonnageIndicator\>

                                \<PayloadCapacity\>1678\</PayloadCapacity\>

                                \<FullModelName\>ACADIA SLT1\</FullModelName\>

                                \<DaytimeRunningLightIndicator\>S\</DaytimeRunningLightIndicator\>

                                \<Wheelbase\>118.9\</Wheelbase\>

                                \<ClassCode\>93\</ClassCode\>

                                \<AntiTheftIndicator\>P\</AntiTheftIndicator\>

                                \<CurbWeight\>4722\</CurbWeight\>

                                \<GrossVehicleWeight\>6400\</GrossVehicleWeight\>

                                \<Height\>69.9\</Height\>

                                \<Horsepower\>275\</Horsepower\>

                                \<NCICCode\>GMC\</NCICCode\>

                                \<Chassis\>U\</Chassis\>

                                \<Length\>200.7\</Length\>

                                \<Width\>78.2\</Width\>

                                \<BaseMSRP\>34270\</BaseMSRP\>

                                \<SpecialHandlingIndicator\>N\</SpecialHandlingIndicator\>

                                \<InterimIndicator\>N\</InterimIndicator\>

                                \<ReleaseDate\>2303\</ReleaseDate\>

                                \<PhysicalDamage\>

                                    \<RiskAnalyzerCollisionIndicatedSymbol\>DJ\</RiskAnalyzerCollisionIndicatedSymbol\>

                                    \<RiskAnalyzerComprehensiveIndicatedSymbol\>CM\</RiskAnalyzerComprehensiveIndicatedSymbol\>

                                    \<RiskAnalyzerCollisionRatingSymbol\>DJ\</RiskAnalyzerCollisionRatingSymbol\>

                                    \<RiskAnalyzerComprehensiveRatingSymbol\>CM\</RiskAnalyzerComprehensiveRatingSymbol\>

                                    \<RiskAnalyzerComprehensiveNonGlassRatingSymbol\>CN\</RiskAnalyzerComprehensiveNonGlassRatingSymbol\>

                                    \<RiskAnalyzerCollisionCappingIndicator\>N\</RiskAnalyzerCollisionCappingIndicator\>

                                    \<RiskAnalyzerComprehensiveCappingIndicator\>N\</RiskAnalyzerComprehensiveCappingIndicator\>

                                    \<RiskAnalyzerComprehensiveNonGlassCappingIndicator\>N\</RiskAnalyzerComprehensiveNonGlassCappingIndicator\>

                                    \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbol\>CN\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbol\>

                                \</PhysicalDamage\>

                                \<Liability\>

                                    \<RiskAnalyzerMedicalPaymentsIndicatedSymbol\>GE\</RiskAnalyzerMedicalPaymentsIndicatedSymbol\>

                                    \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbol\>FK\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbol\>

                                    \<RiskAnalyzerSingleLimitIndicatedSymbol\>KK\</RiskAnalyzerSingleLimitIndicatedSymbol\>

                                    \<RiskAnalyzerBodilyInjuryRatingSymbol\>KL\</RiskAnalyzerBodilyInjuryRatingSymbol\>

                                    \<RiskAnalyzerPropertyDamageRatingSymbol\>LK\</RiskAnalyzerPropertyDamageRatingSymbol\>

                                    \<RiskAnalyzerMedicalPaymentsRatingSymbol\>GE\</RiskAnalyzerMedicalPaymentsRatingSymbol\>

                                    \<RiskAnalyzerPersonalInjuryProtectionRatingSymbol\>FK\</RiskAnalyzerPersonalInjuryProtectionRatingSymbol\>

                                    \<RiskAnalyzerSingleLimitRatingSymbol\>KK\</RiskAnalyzerSingleLimitRatingSymbol\>

                                    \<RiskAnalyzerBodilyInjuryCappingIndicator\>N\</RiskAnalyzerBodilyInjuryCappingIndicator\>

                                    \<RiskAnalyzerPropertyDamageCappingIndicator\>N\</RiskAnalyzerPropertyDamageCappingIndicator\>

                                    \<RiskAnalyzerMedicalPaymentsCappingIndicator\>N\</RiskAnalyzerMedicalPaymentsCappingIndicator\>

                                    \<RiskAnalyzerPersonalInjuryProtectionCappingIndicator\>N\</RiskAnalyzerPersonalInjuryProtectionCappingIndicator\>

                                    \<RiskAnalyzerBodilyInjuryIndicatedSymbol\>KL\</RiskAnalyzerBodilyInjuryIndicatedSymbol\>

                                    \<RiskAnalyzerPropertyDamageIndicatedSymbol\>LK\</RiskAnalyzerPropertyDamageIndicatedSymbol\>

                                    \<RiskAnalyzerSingleLimitCappingIndicator\>N\</RiskAnalyzerSingleLimitCappingIndicator\>

                                \</Liability\>

                            \</Vehicle\>

                        \</Vehicles\>

                    \</RiskAnalyzer\>

                \</Vehicle\>

            \</Vehicles\>

            \<ClaimActivityPredictor\>

                \<CapIndicator\>Y\</CapIndicator\>

                \<NumberOfClaims\>2\</NumberOfClaims\>

            \</ClaimActivityPredictor\>

            \<Claims\>

                \<Claim\>

                    \<ClaimReferenceNumber\>4QA00526856\</ClaimReferenceNumber\>

                    \<CarrierClaimNumber\>VRLSAP20181002102\</CarrierClaimNumber\>

                    \<MatchReasons\>

                        \<MatchReason\>

                            \<Code\>V\</Code\>

                            \<Description\>VIN Search Type\</Description\>

                        \</MatchReason\>

                        \<MatchReason\>

                            \<Code\>N\</Code\>

                            \<Description\>Name and Date of Birth Search Type\</Description\>

                        \</MatchReason\>

                    \</MatchReasons\>

                    \<AtFaultIndicator\>

                        \<Code\>N\</Code\>

                        \<Description\>Insured not at fault\</Description\>

                    \</AtFaultIndicator\>

                    \<Insurer\>

                        \<Name\>INSURANCE SERVICES OFFICE, INC\</Name\>

                        \<AMBEST\>00001\</AMBEST\>

                    \</Insurer\>

                    \<PolicyType\>

                        \<Code\>PAPP\</Code\>

                        \<Description\>Personal Auto\</Description\>

                    \</PolicyType\>

                    \<OriginalInceptionDate\>20221001\</OriginalInceptionDate\>

                    \<ExpirationDate\>20241001\</ExpirationDate\>

                    \<MatchByInputDriverNumber\>2\</MatchByInputDriverNumber\>

                    \<Subjects\>

                        \<Subject\>

                            \<Sequence\>2\</Sequence\>

                            \<GivenName\>DOUGLAS\</GivenName\>

                            \<MiddleName\>J\</MiddleName\>

                            \<Surname\>BONZHEIM\</Surname\>

                            \<RoleInClaim\>

                                \<Code\>IN\</Code\>

                                \<Description\>Insured\</Description\>

                            \</RoleInClaim\>

                        \</Subject\>

                        \<Subject\>

                            \<Sequence\>2\</Sequence\>

                            \<GivenName\>DOUGLAS\</GivenName\>

                            \<MiddleName\>J\</MiddleName\>

                            \<Surname\>BONZHEIM\</Surname\>

                            \<RoleInClaim\>

                                \<Code\>SA\</Code\>

                                \<Description\>Insured Driver Same as Insured\</Description\>

                            \</RoleInClaim\>

                        \</Subject\>

                        \<Subject\>

                            \<Sequence\>0\</Sequence\>

                            \<GivenName\>ELISA\</GivenName\>

                            \<MiddleName\>M\</MiddleName\>

                            \<Surname\>ALMADA\</Surname\>

                            \<RoleInClaim\>

                                \<Code\>CL\</Code\>

                                \<Description\>Claimant\</Description\>

                            \</RoleInClaim\>

                        \</Subject\>

                        \<Subject\>

                            \<Sequence\>0\</Sequence\>

                            \<GivenName\>KATY\</GivenName\>

                            \<Surname\>PERRY\</Surname\>

                            \<RoleInClaim\>

                                \<Code\>CD\</Code\>

                                \<Description\>Claimant Driver\</Description\>

                            \</RoleInClaim\>

                        \</Subject\>

                    \</Subjects\>

                    \<LossInformation\>

                        \<LossDate\>20230115\</LossDate\>

                        \<LossTime\>0000\</LossTime\>

                        \<Losses\>

                            \<Loss\>

                                \<CoverageType\>

                                    \<Code\>LIAB\</Code\>

                                    \<Description\>Liability\</Description\>

                                \</CoverageType\>

                                \<LossType\>

                                    \<Code\>BI\</Code\>

                                    \<Description\>Body injury\</Description\>

                                \</LossType\>

                                \<DispositionStatus\>

                                    \<Code\>C\</Code\>

                                    \<Description\>Closed\</Description\>

                                \</DispositionStatus\>

                                \<Amount\>2000\</Amount\>

                                \<ClaimStandardizationCode\>N02EPA308071U111\</ClaimStandardizationCode\>

                            \</Loss\>

                        \</Losses\>

                    \</LossInformation\>

                    \<ClaimStandardizationCode\>N02EPA308071U111\</ClaimStandardizationCode\>

                    \<Vehicles\>

                        \<Vehicle\>

                            \<Make\>GENERAL MOTORS CORP\</Make\>

                            \<Model\>ACADIA\</Model\>

                            \<Year\>2008\</Year\>

                            \<VIN\>1GKER23788J291227\</VIN\>

                            \<Catastrophes /\>

                        \</Vehicle\>

                    \</Vehicles\>

                \</Claim\>

                \<Claim\>

                    \<ClaimReferenceNumber\>3IA00527548\</ClaimReferenceNumber\>

                    \<CarrierClaimNumber\>VRLSAP20181002101\</CarrierClaimNumber\>

                    \<MatchReasons\>

                        \<MatchReason\>

                            \<Code\>V\</Code\>

                            \<Description\>VIN Search Type\</Description\>

                        \</MatchReason\>

                        \<MatchReason\>

                            \<Code\>Y\</Code\>

                            \<Description\>Policy Number search\</Description\>

                        \</MatchReason\>

                        \<MatchReason\>

                            \<Code\>N\</Code\>

                            \<Description\>Name and Date of Birth Search Type\</Description\>

                        \</MatchReason\>

                        \<MatchReason\>

                            \<Code\>A\</Code\>

                            \<Description\>Name and Address Search Type\</Description\>

                        \</MatchReason\>

                    \</MatchReasons\>

                    \<AtFaultIndicator\>

                        \<Code\>Y\</Code\>

                        \<Description\>Insured at Fault\</Description\>

                    \</AtFaultIndicator\>

                    \<Insurer\>

                        \<Name\>INSURANCE SERVICES OFFICE, INC\</Name\>

                        \<AMBEST\>00001\</AMBEST\>

                    \</Insurer\>

                    \<PolicyNumber\>VRSKLSP201810021001\</PolicyNumber\>

                    \<PolicyType\>

                        \<Code\>PAPP\</Code\>

                        \<Description\>Personal Auto\</Description\>

                    \</PolicyType\>

                    \<OriginalInceptionDate\>20200105\</OriginalInceptionDate\>

                    \<ExpirationDate\>20240105\</ExpirationDate\>

                    \<MatchByInputDriverNumber\>2\</MatchByInputDriverNumber\>

                    \<Subjects\>

                        \<Subject\>

                            \<Sequence\>2\</Sequence\>

                            \<GivenName\>DOUGLAS\</GivenName\>

                            \<MiddleName\>J\</MiddleName\>

                            \<Surname\>BONZHEIM\</Surname\>

                            \<RoleInClaim\>

                                \<Code\>IN\</Code\>

                                \<Description\>Insured\</Description\>

                            \</RoleInClaim\>

                        \</Subject\>

                        \<Subject\>

                            \<Sequence\>2\</Sequence\>

                            \<GivenName\>DOUGLAS\</GivenName\>

                            \<MiddleName\>J\</MiddleName\>

                            \<Surname\>BONZHEIM\</Surname\>

                            \<RoleInClaim\>

                                \<Code\>SA\</Code\>

                                \<Description\>Insured Driver Same as Insured\</Description\>

                            \</RoleInClaim\>

                        \</Subject\>

                    \</Subjects\>

                    \<LossInformation\>

                        \<LossDate\>20221225\</LossDate\>

                        \<LossTime\>0000\</LossTime\>

                        \<Losses\>

                            \<Loss\>

                                \<CoverageType\>

                                    \<Code\>UM\</Code\>

                                    \<Description\>Uninsured Motorist\</Description\>

                                \</CoverageType\>

                                \<LossType\>

                                    \<Code\>UMPD\</Code\>

                                    \<Description\>Uninsured Motorist Property Damage\</Description\>

                                \</LossType\>

                                \<DispositionStatus\>

                                    \<Code\>C\</Code\>

                                    \<Description\>Closed\</Description\>

                                \</DispositionStatus\>

                                \<Amount\>2000\</Amount\>

                                \<ClaimStandardizationCode\>Y12JPA309070U000\</ClaimStandardizationCode\>

                            \</Loss\>

                        \</Losses\>

                    \</LossInformation\>

                    \<ClaimStandardizationCode\>Y12JPA309070U000\</ClaimStandardizationCode\>

                    \<Vehicles\>

                        \<Vehicle\>

                            \<Make\>GENERAL MOTORS CORP\</Make\>

                            \<Model\>ACADIA\</Model\>

                            \<Year\>2008\</Year\>

                            \<VIN\>1GKER23788J291227\</VIN\>

                            \<Catastrophes /\>

                        \</Vehicle\>

                    \</Vehicles\>

                \</Claim\>

            \</Claims\>

        \</CompleteQuote\>

        \<DataSources\>

            \<RiskCheckPointOfSaleReport\>

                \<Header\>

                    \<TransactionId\>63b0dca4-096b-4720-86e6-1e1a353c5e29\</TransactionId\>

                    \<Quoteback\>15446763-7f06-4452-b988-f77fb994a494\</Quoteback\>

                \</Header\>

                \<Body\>

                    \<StatusCode\>200\</StatusCode\>

                    \<ScoreSummary\>

                        \<RiskGroup\>VERY HIGH\</RiskGroup\>

                        \<ScoreColor\>RED\</ScoreColor\>

                        \<TotalScore\>3588\</TotalScore\>

                        \<IsCRAWarning\>false\</IsCRAWarning\>

                        \<IsFraudIndicator\>false\</IsFraudIndicator\>

                        \<ScoreDecile\>

                            \<Code\>8\</Code\>

                            \<Description\>3500 to 3999\</Description\>

                        \</ScoreDecile\>

                    \</ScoreSummary\>

                    \<ScoreDetails\>

                        \<ExceptionDetails\>

                            \<EntityType\>Subject\</EntityType\>

                            \<EntityNumber\>1\</EntityNumber\>

                            \<ReasonCodeDetails\>

                                \<ReasonCodeDetail\>

                                    \<Reason\>

                                        \<Code\>ID-1.11\</Code\>

                                        \<Description\>No identity located or poor match on primary data source.\</Description\>

                                    \</Reason\>

                                    \<ActionMessage\>Ask for Drivers License and Utility Bill\</ActionMessage\>

                                \</ReasonCodeDetail\>

                                \<ReasonCodeDetail\>

                                    \<Reason\>

                                        \<Code\>ID-1.12\</Code\>

                                        \<Description\>Social Security Number not validated.\</Description\>

                                    \</Reason\>

                                    \<ActionMessage\>Ask for Drivers License and Utility Bill\</ActionMessage\>

                                \</ReasonCodeDetail\>

                                \<ReasonCodeDetail\>

                                    \<Reason\>

                                        \<Code\>ID-1.13\</Code\>

                                        \<Description\>Date of Birth not validated.\</Description\>

                                    \</Reason\>

                                    \<ActionMessage\>Ask for Drivers License  \</ActionMessage\>

                                \</ReasonCodeDetail\>

                                \<ReasonCodeDetail\>

                                    \<Reason\>

                                        \<Code\>ID-1.31\</Code\>

                                        \<Description\>Input Address(es), including current and former, did not match to any of the addresses contained in the primary data source.\</Description\>

                                    \</Reason\>

                                    \<ActionMessage\>Ask for Utility Bill\</ActionMessage\>

                                \</ReasonCodeDetail\>

                                \<ReasonCodeDetail\>

                                    \<Reason\>

                                        \<Code\>AG-2.17\</Code\>

                                        \<Description\>Input Address(es) including current and former did not match to any of the addresses contained in the primary data source.\</Description\>

                                    \</Reason\>

                                    \<ActionMessage\>Ask for Utility Bill\</ActionMessage\>

                                \</ReasonCodeDetail\>

                            \</ReasonCodeDetails\>

                        \</ExceptionDetails\>

                        \<ExceptionDetails\>

                            \<EntityType\>Vehicle\</EntityType\>

                            \<EntityNumber\>1\</EntityNumber\>

                            \<ReasonCodeDetails\>

                                \<ReasonCodeDetail\>

                                    \<Reason\>

                                        \<Code\>AG-2.22\</Code\>

                                        \<Description\>Vehicle has out of state Registration.  \</Description\>

                                    \</Reason\>

                                    \<ActionMessage\>Take No Action\</ActionMessage\>

                                \</ReasonCodeDetail\>

                                \<ReasonCodeDetail\>

                                    \<Reason\>

                                        \<Code\>AO-5.01\</Code\>

                                        \<Description\>Vehicle is not owned by Policy Holder or any Driver on the Policy.\</Description\>

                                    \</Reason\>

                                    \<ActionMessage\>Ask for Vehicle Registration\</ActionMessage\>

                                \</ReasonCodeDetail\>

                            \</ReasonCodeDetails\>

                        \</ExceptionDetails\>

                        \<ExceptionDetails\>

                            \<EntityType\>Vehicle\</EntityType\>

                            \<EntityNumber\>2\</EntityNumber\>

                            \<ReasonCodeDetails\>

                                \<ReasonCodeDetail\>

                                    \<Reason\>

                                        \<Code\>AG-2.22\</Code\>

                                        \<Description\>Vehicle has out of state Registration.  \</Description\>

                                    \</Reason\>

                                    \<ActionMessage\>Take No Action\</ActionMessage\>

                                \</ReasonCodeDetail\>

                                \<ReasonCodeDetail\>

                                    \<Reason\>

                                        \<Code\>AO-5.01\</Code\>

                                        \<Description\>Vehicle is not owned by Policy Holder or any Driver on the Policy.\</Description\>

                                    \</Reason\>

                                    \<ActionMessage\>Ask for Vehicle Registration\</ActionMessage\>

                                \</ReasonCodeDetail\>

                            \</ReasonCodeDetails\>

                        \</ExceptionDetails\>

                        \<ExceptionDetails\>

                            \<EntityType\>Vehicle\</EntityType\>

                            \<EntityNumber\>3\</EntityNumber\>

                            \<ReasonCodeDetails\>

                                \<ReasonCodeDetail\>

                                    \<Reason\>

                                        \<Code\>AG-2.22\</Code\>

                                        \<Description\>Vehicle has out of state Registration.  \</Description\>

                                    \</Reason\>

                                    \<ActionMessage\>Take No Action\</ActionMessage\>

                                \</ReasonCodeDetail\>

                                \<ReasonCodeDetail\>

                                    \<Reason\>

                                        \<Code\>AO-5.01\</Code\>

                                        \<Description\>Vehicle is not owned by Policy Holder or any Driver on the Policy.\</Description\>

                                    \</Reason\>

                                    \<ActionMessage\>Ask for Vehicle Registration\</ActionMessage\>

                                \</ReasonCodeDetail\>

                                \<ReasonCodeDetail\>

                                    \<Reason\>

                                        \<Code\>MI-7.01\</Code\>

                                        \<Description\>The vehicle has a salvage, flood or junk title\</Description\>

                                    \</Reason\>

                                    \<ActionMessage\>Ask for Vehicle Registration\</ActionMessage\>

                                \</ReasonCodeDetail\>

                            \</ReasonCodeDetails\>

                        \</ExceptionDetails\>

                        \<ExceptionDetails\>

                            \<EntityType\>Vehicle\</EntityType\>

                            \<EntityNumber\>4\</EntityNumber\>

                            \<ReasonCodeDetails\>

                                \<ReasonCodeDetail\>

                                    \<Reason\>

                                        \<Code\>AG-2.22\</Code\>

                                        \<Description\>Vehicle has out of state Registration.  \</Description\>

                                    \</Reason\>

                                    \<ActionMessage\>Take No Action\</ActionMessage\>

                                \</ReasonCodeDetail\>

                                \<ReasonCodeDetail\>

                                    \<Reason\>

                                        \<Code\>AO-5.01\</Code\>

                                        \<Description\>Vehicle is not owned by Policy Holder or any Driver on the Policy.\</Description\>

                                    \</Reason\>

                                    \<ActionMessage\>Ask for Vehicle Registration\</ActionMessage\>

                                \</ReasonCodeDetail\>

                            \</ReasonCodeDetails\>

                        \</ExceptionDetails\>

                    \</ScoreDetails\>

                    \<Address\>

                        \<AddressType\>Standardized\</AddressType\>

                        \<Street1\>7827 Adelaide Loop\</Street1\>

                        \<City\>New Port Richey\</City\>

                        \<StateCode\>FL\</StateCode\>

                        \<Zip\>346552733\</Zip\>

                        \<CountyName\>Pasco\</CountyName\>

                        \<FIPSCountyCd\>101\</FIPSCountyCd\>

                        \<DPVFootnote\>AABB\</DPVFootnote\>

                        \<RecordType\>S\</RecordType\>

                        \<HygieneError\>AS01\</HygieneError\>

                        \<DPVVacant\>N\</DPVVacant\>

                    \</Address\>

                    \<HouseholdInformation\>

                        \<Youths11to15\>4\</Youths11to15\>

                        \<Youths16to17\>4\</Youths16to17\>

                        \<DwellingType\>S\</DwellingType\>

                        \<HomeOwner\>T\</HomeOwner\>

                        \<LengthofResidence\>2\</LengthofResidence\>

                        \<HouseholdEducation\>5\</HouseholdEducation\>

                        \<SOHOIndicatorHousehold\>Y\</SOHOIndicatorHousehold\>

                        \<HouseholdSize\>5\</HouseholdSize\>

                        \<NetWorth\>B\</NetWorth\>

                    \</HouseholdInformation\>

                    \<Subjects\>

                        \<Subject\>

                            \<Sequence\>1\</Sequence\>

                            \<Source\>Secondary\</Source\>

                            \<GivenName\>Yuki\</GivenName\>

                            \<Surname\>BONZHEIM\</Surname\>

                            \<DOB\>19900311\</DOB\>

                            \<Gender\>M\</Gender\>

                            \<MaritalStatus\>S\</MaritalStatus\>

                            \<MatchType\>N\</MatchType\>

                            \<VerificationDate\>20220715\</VerificationDate\>

                            \<VerificationRange\>2\</VerificationRange\>

                            \<DriverAssuranceScore\>D1\</DriverAssuranceScore\>

                            \<InternalDriverCode\>7\</InternalDriverCode\>

                        \</Subject\>

                        \<Subject\>

                            \<Sequence\>2\</Sequence\>

                            \<Source\>Secondary\</Source\>

                            \<GivenName\>DOUGLAS\</GivenName\>

                            \<MiddleName\>J\</MiddleName\>

                            \<Surname\>BONZHEIM\</Surname\>

                            \<DOB\>19760101\</DOB\>

                            \<Gender\>M\</Gender\>

                            \<MaritalStatus\>S\</MaritalStatus\>

                            \<MatchType\>N\</MatchType\>

                            \<VerificationDate\>20220715\</VerificationDate\>

                            \<VerificationRange\>2\</VerificationRange\>

                            \<DriverAssuranceScore\>D1\</DriverAssuranceScore\>

                            \<InternalDriverCode\>7\</InternalDriverCode\>

                        \</Subject\>

                        \<Subject\>

                            \<Sequence\>3\</Sequence\>

                            \<Source\>Secondary\</Source\>

                            \<GivenName\>Lorna\</GivenName\>

                            \<MiddleName\>P\</MiddleName\>

                            \<Surname\>BONZHEIM\</Surname\>

                            \<DOB\>20030923\</DOB\>

                            \<Gender\>M\</Gender\>

                            \<MaritalStatus\>M\</MaritalStatus\>

                            \<MatchType\>N\</MatchType\>

                            \<VerificationDate\>20220315\</VerificationDate\>

                            \<VerificationRange\>2\</VerificationRange\>

                            \<DriverAssuranceScore\>D1\</DriverAssuranceScore\>

                            \<InternalDriverCode\>7\</InternalDriverCode\>

                        \</Subject\>

                        \<Subject\>

                            \<Sequence\>4\</Sequence\>

                            \<Source\>Secondary\</Source\>

                            \<GivenName\>Rhett\</GivenName\>

                            \<MiddleName\>R\</MiddleName\>

                            \<Surname\>BONZHEIM\</Surname\>

                            \<DOB\>19900720\</DOB\>

                            \<Gender\>F\</Gender\>

                            \<MaritalStatus\>S\</MaritalStatus\>

                            \<MatchType\>N\</MatchType\>

                            \<VerificationDate\>20220815\</VerificationDate\>

                            \<VerificationRange\>2\</VerificationRange\>

                            \<DriverAssuranceScore\>D1\</DriverAssuranceScore\>

                            \<InternalDriverCode\>7\</InternalDriverCode\>

                        \</Subject\>

                        \<Subject\>

                            \<Sequence\>5\</Sequence\>

                            \<Source\>Secondary\</Source\>

                            \<GivenName\>Markus\</GivenName\>

                            \<MiddleName\>G\</MiddleName\>

                            \<Surname\>BONZHEIM\</Surname\>

                            \<DOB\>20010311\</DOB\>

                            \<Gender\>M\</Gender\>

                            \<MaritalStatus\>S\</MaritalStatus\>

                            \<MatchType\>N\</MatchType\>

                            \<VerificationDate\>20220315\</VerificationDate\>

                            \<VerificationRange\>2\</VerificationRange\>

                            \<DriverAssuranceScore\>D1\</DriverAssuranceScore\>

                            \<InternalDriverCode\>7\</InternalDriverCode\>

                        \</Subject\>

                        \<Subject\>

                            \<Sequence\>6\</Sequence\>

                            \<Source\>Secondary\</Source\>

                            \<GivenName\>Mindi\</GivenName\>

                            \<MiddleName\>H\</MiddleName\>

                            \<Surname\>BONZHEIM\</Surname\>

                            \<DOB\>19901113\</DOB\>

                            \<Gender\>F\</Gender\>

                            \<MaritalStatus\>S\</MaritalStatus\>

                            \<MatchType\>N\</MatchType\>

                            \<VerificationDate\>20220815\</VerificationDate\>

                            \<VerificationRange\>2\</VerificationRange\>

                            \<DriverAssuranceScore\>D1\</DriverAssuranceScore\>

                            \<InternalDriverCode\>7\</InternalDriverCode\>

                        \</Subject\>

                    \</Subjects\>

                    \<Vehicles\>

                        \<Vehicle\>

                            \<Sequence\>1\</Sequence\>

                            \<VINMatch\>Y\</VINMatch\>

                            \<DataSource\>GOV\</DataSource\>

                            \<ValidVINIndicator\>Y\</ValidVINIndicator\>

                            \<VINChangeIndicator\>N\</VINChangeIndicator\>

                            \<VIN\>1G5CT18B5F8530675\</VIN\>

                            \<VehicleTypeCode\>T\</VehicleTypeCode\>

                            \<VehicleTypeDesc\>Truck\</VehicleTypeDesc\>

                            \<ModelYear\>1985\</ModelYear\>

                            \<Make\>GMC\</Make\>

                            \<MakeDesc\>GMC\</MakeDesc\>

                            \<Model\>S15\</Model\>

                            \<BodyStyleCode\>UT\</BodyStyleCode\>

                            \<BodyStyleDesc\>Sport Utility Vehicle\</BodyStyleDesc\>

                            \<StateOfRegistration\>CO\</StateOfRegistration\>

                            \<TransactionDate\>20060119\</TransactionDate\>

                            \<ExpirationDate\>20211212\</ExpirationDate\>

                            \<PlateTypeCode\>Z\</PlateTypeCode\>

                            \<PlateTypeDesc\>Regular\</PlateTypeDesc\>

                            \<LicensePlateNumber\>112MPE\</LicensePlateNumber\>

                            \<IsBranded\>false\</IsBranded\>

                            \<LeaseInd\>N\</LeaseInd\>

                            \<NameCode1\>A\</NameCode1\>

                            \<NameCodeDesc1\>Owner\</NameCodeDesc1\>

                            \<NameTitleCode1\>3\</NameTitleCode1\>

                            \<NameTitleDesc1\>MS\</NameTitleDesc1\>

                            \<RegisteredOwnerName\>

                                \<GivenName\>RHONDA\</GivenName\>

                                \<MiddleName\>R\</MiddleName\>

                                \<Surname\>GARCILASCO\</Surname\>

                            \</RegisteredOwnerName\>

                            \<Address\>

                                \<AddressType\>S\</AddressType\>

                                \<Street1\>4341 W CENTER AVE APT B\</Street1\>

                                \<City\>DENVER\</City\>

                                \<StateCode\>CO\</StateCode\>

                                \<Zip\>80219\</Zip\>

                            \</Address\>

                        \</Vehicle\>

                        \<Vehicle\>

                            \<Sequence\>2\</Sequence\>

                            \<VINMatch\>Y\</VINMatch\>

                            \<DataSource\>GOV\</DataSource\>

                            \<ValidVINIndicator\>Y\</ValidVINIndicator\>

                            \<VINChangeIndicator\>N\</VINChangeIndicator\>

                            \<VIN\>3GNFK16T9YG218125\</VIN\>

                            \<VehicleTypeCode\>T\</VehicleTypeCode\>

                            \<VehicleTypeDesc\>Truck\</VehicleTypeDesc\>

                            \<ModelYear\>2000\</ModelYear\>

                            \<Make\>CHE\</Make\>

                            \<MakeDesc\>CHEVROLET\</MakeDesc\>

                            \<Model\>SUBURBAN\</Model\>

                            \<BodyStyleCode\>UT\</BodyStyleCode\>

                            \<BodyStyleDesc\>Sport Utility Vehicle\</BodyStyleDesc\>

                            \<StateOfRegistration\>KY\</StateOfRegistration\>

                            \<TransactionDate\>20101203\</TransactionDate\>

                            \<ExpirationDate\>20210601\</ExpirationDate\>

                            \<PlateTypeCode\>Z\</PlateTypeCode\>

                            \<PlateTypeDesc\>Regular\</PlateTypeDesc\>

                            \<LicensePlateNumber\>1KMC11\</LicensePlateNumber\>

                            \<IsBranded\>false\</IsBranded\>

                            \<LeaseInd\>N\</LeaseInd\>

                            \<NameCode1\>A\</NameCode1\>

                            \<NameCodeDesc1\>Owner\</NameCodeDesc1\>

                            \<NameTitleCode1\>1\</NameTitleCode1\>

                            \<NameTitleDesc1\>MR\</NameTitleDesc1\>

                            \<RegisteredOwnerName\>

                                \<GivenName\>JOHNSON\</GivenName\>

                                \<Surname\>JONNIE\</Surname\>

                            \</RegisteredOwnerName\>

                            \<Address\>

                                \<AddressType\>S\</AddressType\>

                                \<Street1\>2700 NEW HOLD RD\</Street1\>

                                \<City\>PADUCAH\</City\>

                                \<StateCode\>KY\</StateCode\>

                                \<Zip\>42001\</Zip\>

                            \</Address\>

                        \</Vehicle\>

                        \<Vehicle\>

                            \<Sequence\>3\</Sequence\>

                            \<VINMatch\>Y\</VINMatch\>

                            \<DataSource\>GOV\</DataSource\>

                            \<ValidVINIndicator\>Y\</ValidVINIndicator\>

                            \<VINChangeIndicator\>N\</VINChangeIndicator\>

                            \<VIN\>1HGCM56306A148752\</VIN\>

                            \<VehicleTypeCode\>P\</VehicleTypeCode\>

                            \<VehicleTypeDesc\>Passenger Car\</VehicleTypeDesc\>

                            \<ModelYear\>2006\</ModelYear\>

                            \<Make\>HON\</Make\>

                            \<MakeDesc\>HONDA\</MakeDesc\>

                            \<Model\>ACCORD\</Model\>

                            \<BodyStyleCode\>SD\</BodyStyleCode\>

                            \<BodyStyleDesc\>Sedan\</BodyStyleDesc\>

                            \<StateOfRegistration\>CO\</StateOfRegistration\>

                            \<TransactionDate\>20091028\</TransactionDate\>

                            \<ExpirationDate\>20211231\</ExpirationDate\>

                            \<PlateTypeCode\>Z\</PlateTypeCode\>

                            \<PlateTypeDesc\>Regular\</PlateTypeDesc\>

                            \<LicensePlateNumber\>403OAK\</LicensePlateNumber\>

                            \<IsBranded\>true\</IsBranded\>

                            \<BrandedTitleState1\>CO\</BrandedTitleState1\>

                            \<BrandedTitleDate1\>20150815\</BrandedTitleDate1\>

                            \<BrandedTitleCode1\>H\</BrandedTitleCode1\>

                            \<BrandedTitleDesc1\>REBUILT\</BrandedTitleDesc1\>

                            \<BrandedTitleState2\>OR\</BrandedTitleState2\>

                            \<BrandedTitleDate2\>20150615\</BrandedTitleDate2\>

                            \<BrandedTitleCode2\>J\</BrandedTitleCode2\>

                            \<BrandedTitleDesc2\>SALVAGE\</BrandedTitleDesc2\>

                            \<LeaseInd\>N\</LeaseInd\>

                            \<NameCode1\>A\</NameCode1\>

                            \<NameCodeDesc1\>Owner\</NameCodeDesc1\>

                            \<NameTitleCode1\>1\</NameTitleCode1\>

                            \<NameTitleDesc1\>MR\</NameTitleDesc1\>

                            \<RegisteredOwnerName\>

                                \<GivenName\>JAMES\</GivenName\>

                                \<MiddleName\>W\</MiddleName\>

                                \<Surname\>LEYDEN\</Surname\>

                            \</RegisteredOwnerName\>

                            \<Address\>

                                \<AddressType\>S\</AddressType\>

                                \<Street1\>10558 PAINT PL\</Street1\>

                                \<City\>LITTLETON\</City\>

                                \<StateCode\>CO\</StateCode\>

                                \<Zip\>80125\</Zip\>

                            \</Address\>

                        \</Vehicle\>

                        \<Vehicle\>

                            \<Sequence\>4\</Sequence\>

                            \<VINMatch\>Y\</VINMatch\>

                            \<DataSource\>GOV\</DataSource\>

                            \<ValidVINIndicator\>Y\</ValidVINIndicator\>

                            \<VINChangeIndicator\>N\</VINChangeIndicator\>

                            \<VIN\>1GKER23788J291227\</VIN\>

                            \<VehicleTypeCode\>T\</VehicleTypeCode\>

                            \<VehicleTypeDesc\>Truck\</VehicleTypeDesc\>

                            \<ModelYear\>2008\</ModelYear\>

                            \<Make\>GMC\</Make\>

                            \<MakeDesc\>GMC\</MakeDesc\>

                            \<Model\>ACADIA\</Model\>

                            \<BodyStyleCode\>UT\</BodyStyleCode\>

                            \<BodyStyleDesc\>Sport Utility Vehicle\</BodyStyleDesc\>

                            \<StateOfRegistration\>TX\</StateOfRegistration\>

                            \<TransactionDate\>20090801\</TransactionDate\>

                            \<ExpirationDate\>20210331\</ExpirationDate\>

                            \<PlateTypeCode\>Z\</PlateTypeCode\>

                            \<PlateTypeDesc\>Regular\</PlateTypeDesc\>

                            \<LicensePlateNumber\>JRR530\</LicensePlateNumber\>

                            \<IsBranded\>false\</IsBranded\>

                            \<LeaseInd\>N\</LeaseInd\>

                            \<NameCode1\>A\</NameCode1\>

                            \<NameCodeDesc1\>Owner\</NameCodeDesc1\>

                            \<NameTitleCode1\>1\</NameTitleCode1\>

                            \<NameTitleDesc1\>MR\</NameTitleDesc1\>

                            \<RegisteredOwnerName\>

                                \<GivenName\>ROBERT\</GivenName\>

                                \<MiddleName\>J\</MiddleName\>

                                \<Surname\>PATTERSON\</Surname\>

                            \</RegisteredOwnerName\>

                            \<Address\>

                                \<AddressType\>S\</AddressType\>

                                \<Street1\>121 CHAPEL HILL DR\</Street1\>

                                \<City\>PROSPER\</City\>

                                \<StateCode\>TX\</StateCode\>

                                \<Zip\>75078\</Zip\>

                            \</Address\>

                        \</Vehicle\>

                    \</Vehicles\>

                    \<CreditHeader\>

                        \<Code\>N\</Code\>

                        \<Description\>No credit header (e.g. no SSN)\</Description\>

                    \</CreditHeader\>

                    \<AdditionalData\>

                        \<DataAttribute\>

                            \<Key\>Youth16-17\</Key\>

                            \<Value\>4\</Value\>

                        \</DataAttribute\>

                        \<DataAttribute\>

                            \<Key\>Y\</Key\>

                            \<Value\>VehOwnrExp\</Value\>

                        \</DataAttribute\>

                    \</AdditionalData\>

                    \<CustomElements /\>

                \</Body\>

            \</RiskCheckPointOfSaleReport\>

            \<CoverageVerifierReport\>

                \<Header\>

                    \<TransactionId\>530604bd-ba8c-499e-a332-2227dc34d1e8\</TransactionId\>

                    \<Quoteback\>15446763-7f06-4452-b988-f77fb994a494\</Quoteback\>

                \</Header\>

                \<Body\>

                    \<Policies\>

                        \<Policy\>

                            \<Detail\>

                                \<PolicyInformation\>

                                    \<PolicyType\>

                                        \<Code\>AU\</Code\>

                                        \<Description\>Auto\</Description\>

                                    \</PolicyType\>

                                    \<TermEffectiveDate\>20230105\</TermEffectiveDate\>

                                    \<TermExpirationDate\>20240105\</TermExpirationDate\>

                                    \<PolicyHolders\>

                                        \<PolicyHolder\>

                                            \<GivenName\>DOUGLAS\</GivenName\>

                                            \<MiddleName\>J\</MiddleName\>

                                            \<Surname\>BONZHEIM\</Surname\>

                                            \<DOB\>19760101\</DOB\>

                                            \<DLNumber\>M888777666555\</DLNumber\>

                                            \<DLState\>FL\</DLState\>

                                        \</PolicyHolder\>

                                        \<PolicyHolder\>

                                            \<GivenName\>LORNA\</GivenName\>

                                            \<MiddleName\>P\</MiddleName\>

                                            \<Surname\>BONZHEIM\</Surname\>

                                            \<DOB\>20030923\</DOB\>

                                            \<DLNumber\>B640693682100\</DLNumber\>

                                            \<DLState\>FL\</DLState\>

                                        \</PolicyHolder\>

                                    \</PolicyHolders\>

                                    \<PhoneNumbers\>

                                        \<PhoneNumber\>

                                            \<PhoneType\>H\</PhoneType\>

                                            \<Number\>1112223335\</Number\>

                                            \<Extension\>0000\</Extension\>

                                        \</PhoneNumber\>

                                    \</PhoneNumbers\>

                                \</PolicyInformation\>

                                \<Subjects\>

                                    \<Subject\>

                                        \<DriverSequenceId\>0\</DriverSequenceId\>

                                        \<GivenName\>DOUGLAS\</GivenName\>

                                        \<MiddleName\>J\</MiddleName\>

                                        \<Surname\>BONZHEIM\</Surname\>

                                        \<DOB\>19760101\</DOB\>

                                        \<SSN\>491487807\</SSN\>

                                        \<Gender\>M\</Gender\>

                                        \<MaritalStatus\>M\</MaritalStatus\>

                                        \<DLNumber\>M888777666555\</DLNumber\>

                                        \<DLState\>FL\</DLState\>

                                        \<RelationToPolicyHolder\>

                                            \<Code\>PP\</Code\>

                                            \<Description\>Primary Policyholder\</Description\>

                                        \</RelationToPolicyHolder\>

                                        \<RelationToInsured\>

                                            \<Code\>I\</Code\>

                                            \<Description\>Insured\</Description\>

                                        \</RelationToInsured\>

                                        \<FromDate\>20230105\</FromDate\>

                                        \<ToDate\>20240105\</ToDate\>

                                    \</Subject\>

                                    \<Subject\>

                                        \<DriverSequenceId\>0\</DriverSequenceId\>

                                        \<GivenName\>LORNA\</GivenName\>

                                        \<MiddleName\>P\</MiddleName\>

                                        \<Surname\>BONZHEIM\</Surname\>

                                        \<DOB\>20030923\</DOB\>

                                        \<Gender\>F\</Gender\>

                                        \<MaritalStatus\>M\</MaritalStatus\>

                                        \<DLNumber\>B640693682100\</DLNumber\>

                                        \<DLState\>FL\</DLState\>

                                        \<RelationToPolicyHolder\>

                                            \<Code\>SP\</Code\>

                                            \<Description\>Secondary Policyholder\</Description\>

                                        \</RelationToPolicyHolder\>

                                        \<RelationToInsured\>

                                            \<Code\>S\</Code\>

                                            \<Description\>Spouse\</Description\>

                                        \</RelationToInsured\>

                                        \<FromDate\>20230105\</FromDate\>

                                        \<ToDate\>20240105\</ToDate\>

                                    \</Subject\>

                                    \<Subject\>

                                        \<DriverSequenceId\>0\</DriverSequenceId\>

                                        \<GivenName\>MALIA\</GivenName\>

                                        \<MiddleName\>R\</MiddleName\>

                                        \<Surname\>BONZHEIM\</Surname\>

                                        \<DOB\>19990120\</DOB\>

                                        \<Gender\>F\</Gender\>

                                        \<MaritalStatus\>S\</MaritalStatus\>

                                        \<DLNumber\>S420665834256\</DLNumber\>

                                        \<DLState\>FL\</DLState\>

                                        \<RelationToPolicyHolder\>

                                            \<Code\>LD\</Code\>

                                            \<Description\>Listed Driver\</Description\>

                                        \</RelationToPolicyHolder\>

                                        \<FromDate\>20230105\</FromDate\>

                                        \<ToDate\>20240105\</ToDate\>

                                    \</Subject\>

                                    \<Subject\>

                                        \<DriverSequenceId\>0\</DriverSequenceId\>

                                        \<GivenName\>MARKUS\</GivenName\>

                                        \<MiddleName\>G\</MiddleName\>

                                        \<Surname\>BONZHEIM\</Surname\>

                                        \<DOB\>20010311\</DOB\>

                                        \<Gender\>F\</Gender\>

                                        \<MaritalStatus\>S\</MaritalStatus\>

                                        \<DLNumber\>P420665934225\</DLNumber\>

                                        \<DLState\>FL\</DLState\>

                                        \<RelationToPolicyHolder\>

                                            \<Code\>LD\</Code\>

                                            \<Description\>Listed Driver\</Description\>

                                        \</RelationToPolicyHolder\>

                                        \<FromDate\>20230105\</FromDate\>

                                        \<ToDate\>20240105\</ToDate\>

                                    \</Subject\>

                                    \<Subject\>

                                        \<DriverSequenceId\>0\</DriverSequenceId\>

                                        \<GivenName\>MINDI\</GivenName\>

                                        \<MiddleName\>H\</MiddleName\>

                                        \<Surname\>BONZHEIM\</Surname\>

                                        \<DOB\>19901113\</DOB\>

                                        \<Gender\>F\</Gender\>

                                        \<MaritalStatus\>S\</MaritalStatus\>

                                        \<DLNumber\>R420622534333\</DLNumber\>

                                        \<DLState\>FL\</DLState\>

                                        \<RelationToPolicyHolder\>

                                            \<Code\>LD\</Code\>

                                            \<Description\>Listed Driver\</Description\>

                                        \</RelationToPolicyHolder\>

                                        \<FromDate\>20230105\</FromDate\>

                                        \<ToDate\>20240105\</ToDate\>

                                    \</Subject\>

                                    \<Subject\>

                                        \<DriverSequenceId\>0\</DriverSequenceId\>

                                        \<GivenName\>RHETT\</GivenName\>

                                        \<MiddleName\>K\</MiddleName\>

                                        \<Surname\>BONZHEIM\</Surname\>

                                        \<DOB\>19900720\</DOB\>

                                        \<Gender\>F\</Gender\>

                                        \<MaritalStatus\>S\</MaritalStatus\>

                                        \<DLNumber\>L420625834362\</DLNumber\>

                                        \<DLState\>FL\</DLState\>

                                        \<RelationToPolicyHolder\>

                                            \<Code\>LD\</Code\>

                                            \<Description\>Listed Driver\</Description\>

                                        \</RelationToPolicyHolder\>

                                        \<FromDate\>20230105\</FromDate\>

                                        \<ToDate\>20240105\</ToDate\>

                                    \</Subject\>

                                    \<Subject\>

                                        \<DriverSequenceId\>1\</DriverSequenceId\>

                                        \<GivenName\>YUKI\</GivenName\>

                                        \<MiddleName\>R\</MiddleName\>

                                        \<Surname\>BONZHEIM\</Surname\>

                                        \<DOB\>19900311\</DOB\>

                                        \<Gender\>M\</Gender\>

                                        \<MaritalStatus\>S\</MaritalStatus\>

                                        \<DLNumber\>T520103597610\</DLNumber\>

                                        \<DLState\>FL\</DLState\>

                                        \<RelationToPolicyHolder\>

                                            \<Code\>LD\</Code\>

                                            \<Description\>Listed Driver\</Description\>

                                        \</RelationToPolicyHolder\>

                                        \<RelationToInsured\>

                                            \<Code\>O\</Code\>

                                            \<Description\>Other Related\</Description\>

                                        \</RelationToInsured\>

                                        \<FromDate\>20230105\</FromDate\>

                                        \<ToDate\>20240105\</ToDate\>

                                    \</Subject\>

                                \</Subjects\>

                                \<Carrier\>

                                    \<FinancialAMBEST\>99999\</FinancialAMBEST\>

                                    \<Name\>INSURANCE SERVICES O\</Name\>

                                    \<AMBEST\>99999\</AMBEST\>

                                    \<NAIC\>00000\</NAIC\>

                                \</Carrier\>

                                \<MailingAddress\>

                                    \<Street1\>7827 Adelaide Loop\</Street1\>

                                    \<City\>New Port Richey\</City\>

                                    \<StateCode\>FL\</StateCode\>

                                    \<Zip\>34655\</Zip\>

                                    \<CountryCode\>US\</CountryCode\>

                                    \<FromDate\>20230105\</FromDate\>

                                    \<ToDate\>20240105\</ToDate\>

                                \</MailingAddress\>

                                \<Coverages\>

                                    \<Coverage\>

                                        \<CoverageType\>

                                            \<Code\>BINJ\</Code\>

                                            \<Description\>Bodily Injury\</Description\>

                                        \</CoverageType\>

                                        \<IndividualLimitAmount\>40000\</IndividualLimitAmount\>

                                        \<OccurrenceLimitAmount\>80000\</OccurrenceLimitAmount\>

                                        \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                        \<FromDate\>20230105\</FromDate\>

                                        \<ToDate\>20240105\</ToDate\>

                                    \</Coverage\>

                                    \<Coverage\>

                                        \<CoverageType\>

                                            \<Code\>CBSL\</Code\>

                                            \<Description\>CSL (BI \&amp; PD)\</Description\>

                                        \</CoverageType\>

                                        \<IndividualLimitAmount\>0\</IndividualLimitAmount\>

                                        \<OccurrenceLimitAmount\>0\</OccurrenceLimitAmount\>

                                        \<CombinedSingleLimitAmount\>80000\</CombinedSingleLimitAmount\>

                                        \<FromDate\>20230105\</FromDate\>

                                        \<ToDate\>20240105\</ToDate\>

                                    \</Coverage\>

                                    \<Coverage\>

                                        \<CoverageType\>

                                            \<Code\>PDMG\</Code\>

                                            \<Description\>Property Damage\</Description\>

                                        \</CoverageType\>

                                        \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                        \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                        \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                        \<FromDate\>20230105\</FromDate\>

                                        \<ToDate\>20240105\</ToDate\>

                                    \</Coverage\>

                                    \<Coverage\>

                                        \<CoverageType\>

                                            \<Code\>UMPD\</Code\>

                                            \<Description\>Uninsured Motorist (PD)\</Description\>

                                        \</CoverageType\>

                                        \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                        \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                        \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                        \<FromDate\>20230105\</FromDate\>

                                        \<ToDate\>20240105\</ToDate\>

                                    \</Coverage\>

                                    \<Coverage\>

                                        \<CoverageType\>

                                            \<Code\>PINJ\</Code\>

                                            \<Description\>Personal Injury\</Description\>

                                        \</CoverageType\>

                                        \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                        \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                        \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                        \<FromDate\>20230105\</FromDate\>

                                        \<ToDate\>20240105\</ToDate\>

                                    \</Coverage\>

                                \</Coverages\>

                                \<Vehicles\>

                                    \<Vehicle\>

                                        \<Year\>1985\</Year\>

                                        \<Make\>GMC\</Make\>

                                        \<Model\>UT\</Model\>

                                        \<VIN\>1G5CT18B5F8530675\</VIN\>

                                        \<ClassCode\>000000\</ClassCode\>

                                        \<BusinessUse\>Y\</BusinessUse\>

                                        \<CollisionDeductibleAmount\>1000\</CollisionDeductibleAmount\>

                                        \<ComprehensiveDeductibleAmount\>500\</ComprehensiveDeductibleAmount\>

                                        \<FromDate\>20230105\</FromDate\>

                                        \<ToDate\>20240105\</ToDate\>

                                        \<CollisionIndicator\>Y\</CollisionIndicator\>

                                        \<ComprehensiveIndicator\>Y\</ComprehensiveIndicator\>

                                        \<Coverages\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>BINJ\</Code\>

                                                    \<Description\>Bodily Injury\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>40000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>80000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>PDMG\</Code\>

                                                    \<Description\>Property Damage\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>CBSL\</Code\>

                                                    \<Description\>CSL (BI \&amp; PD)\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>0\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>0\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>80000\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>UMPD\</Code\>

                                                    \<Description\>Uninsured Motorist (PD)\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>PINJ\</Code\>

                                                    \<Description\>Personal Injury\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                        \</Coverages\>

                                    \</Vehicle\>

                                    \<Vehicle\>

                                        \<Year\>2000\</Year\>

                                        \<Make\>CHEV\</Make\>

                                        \<Model\>K1S\</Model\>

                                        \<VIN\>3GNFK16T9YG218125\</VIN\>

                                        \<ClassCode\>000000\</ClassCode\>

                                        \<BusinessUse\>Y\</BusinessUse\>

                                        \<CollisionDeductibleAmount\>1000\</CollisionDeductibleAmount\>

                                        \<ComprehensiveDeductibleAmount\>500\</ComprehensiveDeductibleAmount\>

                                        \<FromDate\>20230105\</FromDate\>

                                        \<ToDate\>20240105\</ToDate\>

                                        \<CollisionIndicator\>Y\</CollisionIndicator\>

                                        \<ComprehensiveIndicator\>Y\</ComprehensiveIndicator\>

                                        \<Coverages\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>BINJ\</Code\>

                                                    \<Description\>Bodily Injury\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>40000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>80000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>PDMG\</Code\>

                                                    \<Description\>Property Damage\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>CBSL\</Code\>

                                                    \<Description\>CSL (BI \&amp; PD)\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>0\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>0\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>80000\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>UMPD\</Code\>

                                                    \<Description\>Uninsured Motorist (PD)\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>PINJ\</Code\>

                                                    \<Description\>Personal Injury\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                        \</Coverages\>

                                    \</Vehicle\>

                                    \<Vehicle\>

                                        \<Year\>2006\</Year\>

                                        \<Make\>HOND\</Make\>

                                        \<Model\>ASE\</Model\>

                                        \<VIN\>1HGCM56306A148752\</VIN\>

                                        \<ClassCode\>000000\</ClassCode\>

                                        \<BusinessUse\>N\</BusinessUse\>

                                        \<CollisionDeductibleAmount\>1000\</CollisionDeductibleAmount\>

                                        \<ComprehensiveDeductibleAmount\>500\</ComprehensiveDeductibleAmount\>

                                        \<FromDate\>20230105\</FromDate\>

                                        \<ToDate\>20240105\</ToDate\>

                                        \<CollisionIndicator\>Y\</CollisionIndicator\>

                                        \<ComprehensiveIndicator\>Y\</ComprehensiveIndicator\>

                                        \<Coverages\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>BINJ\</Code\>

                                                    \<Description\>Bodily Injury\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>40000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>80000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>PDMG\</Code\>

                                                    \<Description\>Property Damage\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>CBSL\</Code\>

                                                    \<Description\>CSL (BI \&amp; PD)\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>0\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>0\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>80000\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>UMPD\</Code\>

                                                    \<Description\>Uninsured Motorist (PD)\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>PINJ\</Code\>

                                                    \<Description\>Personal Injury\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                        \</Coverages\>

                                    \</Vehicle\>

                                    \<Vehicle\>

                                        \<Year\>2008\</Year\>

                                        \<Make\>GMC\</Make\>

                                        \<Model\>S1F\</Model\>

                                        \<VIN\>1GKER23788J291227\</VIN\>

                                        \<ClassCode\>000000\</ClassCode\>

                                        \<BusinessUse\>Y\</BusinessUse\>

                                        \<CollisionDeductibleAmount\>1000\</CollisionDeductibleAmount\>

                                        \<ComprehensiveDeductibleAmount\>500\</ComprehensiveDeductibleAmount\>

                                        \<FromDate\>20230105\</FromDate\>

                                        \<ToDate\>20240105\</ToDate\>

                                        \<CollisionIndicator\>Y\</CollisionIndicator\>

                                        \<ComprehensiveIndicator\>Y\</ComprehensiveIndicator\>

                                        \<Coverages\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>BINJ\</Code\>

                                                    \<Description\>Bodily Injury\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>40000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>80000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>PDMG\</Code\>

                                                    \<Description\>Property Damage\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>CBSL\</Code\>

                                                    \<Description\>CSL (BI \&amp; PD)\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>0\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>0\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>80000\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>UMPD\</Code\>

                                                    \<Description\>Uninsured Motorist (PD)\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>PINJ\</Code\>

                                                    \<Description\>Personal Injury\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20230105\</FromDate\>

                                                \<ToDate\>20240105\</ToDate\>

                                            \</Coverage\>

                                        \</Coverages\>

                                    \</Vehicle\>

                                \</Vehicles\>

                            \</Detail\>

                            \<History\>

                                \<PolicyInformations\>

                                    \<PolicyInformation\>

                                        \<PolicyType\>

                                            \<Code\>AU\</Code\>

                                            \<Description\>Auto\</Description\>

                                        \</PolicyType\>

                                        \<PolicyHolders\>

                                            \<PolicyHolder\>

                                                \<GivenName\>DOUGLAS\</GivenName\>

                                                \<MiddleName\>J\</MiddleName\>

                                                \<Surname\>BONZHEIM\</Surname\>

                                                \<DOB\>19760101\</DOB\>

                                                \<DLNumber\>M888777666555\</DLNumber\>

                                                \<DLState\>FL\</DLState\>

                                            \</PolicyHolder\>

                                            \<PolicyHolder\>

                                                \<GivenName\>LORNA\</GivenName\>

                                                \<MiddleName\>P\</MiddleName\>

                                                \<Surname\>BONZHEIM\</Surname\>

                                                \<DOB\>20030923\</DOB\>

                                                \<DLNumber\>B640693682100\</DLNumber\>

                                                \<DLState\>FL\</DLState\>

                                            \</PolicyHolder\>

                                        \</PolicyHolders\>

                                        \<PhoneNumbers\>

                                            \<PhoneNumber\>

                                                \<PhoneType\>H\</PhoneType\>

                                                \<Number\>1112223335\</Number\>

                                                \<Extension\>0000\</Extension\>

                                            \</PhoneNumber\>

                                        \</PhoneNumbers\>

                                        \<FromDate\>20200105\</FromDate\>

                                        \<ToDate\>20230105\</ToDate\>

                                    \</PolicyInformation\>

                                \</PolicyInformations\>

                                \<Subjects\>

                                    \<Subject\>

                                        \<DriverSequenceId\>0\</DriverSequenceId\>

                                        \<GivenName\>DOUGLAS\</GivenName\>

                                        \<MiddleName\>J\</MiddleName\>

                                        \<Surname\>BONZHEIM\</Surname\>

                                        \<DOB\>19760101\</DOB\>

                                        \<SSN\>491487807\</SSN\>

                                        \<Gender\>M\</Gender\>

                                        \<MaritalStatus\>M\</MaritalStatus\>

                                        \<DLNumber\>M888777666555\</DLNumber\>

                                        \<DLState\>FL\</DLState\>

                                        \<RelationToPolicyHolder\>

                                            \<Code\>PP\</Code\>

                                            \<Description\>Primary Policyholder\</Description\>

                                        \</RelationToPolicyHolder\>

                                        \<RelationToInsured\>

                                            \<Code\>I\</Code\>

                                            \<Description\>Insured\</Description\>

                                        \</RelationToInsured\>

                                        \<FromDate\>20220105\</FromDate\>

                                        \<ToDate\>20230105\</ToDate\>

                                    \</Subject\>

                                    \<Subject\>

                                        \<DriverSequenceId\>0\</DriverSequenceId\>

                                        \<GivenName\>LORNA\</GivenName\>

                                        \<MiddleName\>P\</MiddleName\>

                                        \<Surname\>BONZHEIM\</Surname\>

                                        \<DOB\>20030923\</DOB\>

                                        \<Gender\>F\</Gender\>

                                        \<MaritalStatus\>M\</MaritalStatus\>

                                        \<DLNumber\>B640693682100\</DLNumber\>

                                        \<DLState\>FL\</DLState\>

                                        \<RelationToPolicyHolder\>

                                            \<Code\>SP\</Code\>

                                            \<Description\>Secondary Policyholder\</Description\>

                                        \</RelationToPolicyHolder\>

                                        \<RelationToInsured\>

                                            \<Code\>S\</Code\>

                                            \<Description\>Spouse\</Description\>

                                        \</RelationToInsured\>

                                        \<FromDate\>20220105\</FromDate\>

                                        \<ToDate\>20230105\</ToDate\>

                                    \</Subject\>

                                    \<Subject\>

                                        \<DriverSequenceId\>1\</DriverSequenceId\>

                                        \<GivenName\>YUKI\</GivenName\>

                                        \<MiddleName\>R\</MiddleName\>

                                        \<Surname\>BONZHEIM\</Surname\>

                                        \<DOB\>19900311\</DOB\>

                                        \<Gender\>M\</Gender\>

                                        \<MaritalStatus\>S\</MaritalStatus\>

                                        \<DLNumber\>T520103597610\</DLNumber\>

                                        \<DLState\>FL\</DLState\>

                                        \<RelationToPolicyHolder\>

                                            \<Code\>LD\</Code\>

                                            \<Description\>Listed Driver\</Description\>

                                        \</RelationToPolicyHolder\>

                                        \<RelationToInsured\>

                                            \<Code\>O\</Code\>

                                            \<Description\>Other Related\</Description\>

                                        \</RelationToInsured\>

                                        \<FromDate\>20220105\</FromDate\>

                                        \<ToDate\>20230105\</ToDate\>

                                    \</Subject\>

                                    \<Subject\>

                                        \<DriverSequenceId\>0\</DriverSequenceId\>

                                        \<GivenName\>DOUGLAS\</GivenName\>

                                        \<MiddleName\>J\</MiddleName\>

                                        \<Surname\>BONZHEIM\</Surname\>

                                        \<DOB\>19760101\</DOB\>

                                        \<MaritalStatus\>S\</MaritalStatus\>

                                        \<DLNumber\>T123654125803\</DLNumber\>

                                        \<DLState\>FL\</DLState\>

                                        \<RelationToPolicyHolder\>

                                            \<Code\>PP\</Code\>

                                            \<Description\>Primary Policyholder\</Description\>

                                        \</RelationToPolicyHolder\>

                                        \<RelationToInsured\>

                                            \<Code\>I\</Code\>

                                            \<Description\>Insured\</Description\>

                                        \</RelationToInsured\>

                                        \<FromDate\>20200105\</FromDate\>

                                        \<ToDate\>20220105\</ToDate\>

                                    \</Subject\>

                                    \<Subject\>

                                        \<DriverSequenceId\>0\</DriverSequenceId\>

                                        \<GivenName\>MALIA\</GivenName\>

                                        \<MiddleName\>R\</MiddleName\>

                                        \<Surname\>BONZHEIM\</Surname\>

                                        \<DOB\>19990120\</DOB\>

                                        \<Gender\>F\</Gender\>

                                        \<MaritalStatus\>S\</MaritalStatus\>

                                        \<DLNumber\>S420665834256\</DLNumber\>

                                        \<DLState\>FL\</DLState\>

                                        \<RelationToPolicyHolder\>

                                            \<Code\>LD\</Code\>

                                            \<Description\>Listed Driver\</Description\>

                                        \</RelationToPolicyHolder\>

                                        \<FromDate\>20200105\</FromDate\>

                                        \<ToDate\>20230105\</ToDate\>

                                    \</Subject\>

                                    \<Subject\>

                                        \<DriverSequenceId\>0\</DriverSequenceId\>

                                        \<GivenName\>MARKUS\</GivenName\>

                                        \<MiddleName\>G\</MiddleName\>

                                        \<Surname\>BONZHEIM\</Surname\>

                                        \<DOB\>20010311\</DOB\>

                                        \<Gender\>F\</Gender\>

                                        \<MaritalStatus\>S\</MaritalStatus\>

                                        \<DLNumber\>P420665934225\</DLNumber\>

                                        \<DLState\>FL\</DLState\>

                                        \<RelationToPolicyHolder\>

                                            \<Code\>LD\</Code\>

                                            \<Description\>Listed Driver\</Description\>

                                        \</RelationToPolicyHolder\>

                                        \<FromDate\>20200105\</FromDate\>

                                        \<ToDate\>20230105\</ToDate\>

                                    \</Subject\>

                                    \<Subject\>

                                        \<DriverSequenceId\>0\</DriverSequenceId\>

                                        \<GivenName\>MINDI\</GivenName\>

                                        \<MiddleName\>H\</MiddleName\>

                                        \<Surname\>BONZHEIM\</Surname\>

                                        \<DOB\>19901113\</DOB\>

                                        \<Gender\>F\</Gender\>

                                        \<MaritalStatus\>S\</MaritalStatus\>

                                        \<DLNumber\>R420622534333\</DLNumber\>

                                        \<DLState\>FL\</DLState\>

                                        \<RelationToPolicyHolder\>

                                            \<Code\>LD\</Code\>

                                            \<Description\>Listed Driver\</Description\>

                                        \</RelationToPolicyHolder\>

                                        \<FromDate\>20200105\</FromDate\>

                                        \<ToDate\>20230105\</ToDate\>

                                    \</Subject\>

                                    \<Subject\>

                                        \<DriverSequenceId\>0\</DriverSequenceId\>

                                        \<GivenName\>RHETT\</GivenName\>

                                        \<MiddleName\>K\</MiddleName\>

                                        \<Surname\>BONZHEIM\</Surname\>

                                        \<DOB\>19900720\</DOB\>

                                        \<Gender\>F\</Gender\>

                                        \<MaritalStatus\>S\</MaritalStatus\>

                                        \<DLNumber\>L420625834362\</DLNumber\>

                                        \<DLState\>FL\</DLState\>

                                        \<RelationToPolicyHolder\>

                                            \<Code\>LD\</Code\>

                                            \<Description\>Listed Driver\</Description\>

                                        \</RelationToPolicyHolder\>

                                        \<FromDate\>20200105\</FromDate\>

                                        \<ToDate\>20230105\</ToDate\>

                                    \</Subject\>

                                    \<Subject\>

                                        \<DriverSequenceId\>0\</DriverSequenceId\>

                                        \<GivenName\>ALIZA\</GivenName\>

                                        \<Surname\>BONZHEIM\</Surname\>

                                        \<DOB\>19800510\</DOB\>

                                        \<Gender\>F\</Gender\>

                                        \<DLNumber\>P889515754987\</DLNumber\>

                                        \<DLState\>FL\</DLState\>

                                        \<RelationToPolicyHolder\>

                                            \<Code\>SP\</Code\>

                                            \<Description\>Secondary Policyholder\</Description\>

                                        \</RelationToPolicyHolder\>

                                        \<RelationToInsured\>

                                            \<Code\>S\</Code\>

                                            \<Description\>Spouse\</Description\>

                                        \</RelationToInsured\>

                                        \<FromDate\>20200105\</FromDate\>

                                        \<ToDate\>20220105\</ToDate\>

                                    \</Subject\>

                                    \<Subject\>

                                        \<DriverSequenceId\>0\</DriverSequenceId\>

                                        \<GivenName\>EDGAR\</GivenName\>

                                        \<MiddleName\>R\</MiddleName\>

                                        \<Surname\>RAMIREZ\</Surname\>

                                        \<DOB\>19700501\</DOB\>

                                        \<DLNumber\>D134241554599\</DLNumber\>

                                        \<DLState\>FL\</DLState\>

                                        \<RelationToPolicyHolder\>

                                            \<Code\>LD\</Code\>

                                            \<Description\>Listed Driver\</Description\>

                                        \</RelationToPolicyHolder\>

                                        \<RelationToInsured\>

                                            \<Code\>O\</Code\>

                                            \<Description\>Other Related\</Description\>

                                        \</RelationToInsured\>

                                        \<FromDate\>20200105\</FromDate\>

                                        \<ToDate\>20220105\</ToDate\>

                                    \</Subject\>

                                \</Subjects\>

                                \<MailingAddresses\>

                                    \<MailingAddress\>

                                        \<Street1\>7827 Adelaide Loop\</Street1\>

                                        \<City\>New Port Richey\</City\>

                                        \<StateCode\>FL\</StateCode\>

                                        \<Zip\>34655\</Zip\>

                                        \<CountryCode\>US\</CountryCode\>

                                        \<FromDate\>20200105\</FromDate\>

                                        \<ToDate\>20230105\</ToDate\>

                                    \</MailingAddress\>

                                \</MailingAddresses\>

                                \<Coverages\>

                                    \<Coverage\>

                                        \<CoverageType\>

                                            \<Code\>BINJ\</Code\>

                                            \<Description\>Bodily Injury\</Description\>

                                        \</CoverageType\>

                                        \<IndividualLimitAmount\>40000\</IndividualLimitAmount\>

                                        \<OccurrenceLimitAmount\>80000\</OccurrenceLimitAmount\>

                                        \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                        \<FromDate\>20200105\</FromDate\>

                                        \<ToDate\>20230105\</ToDate\>

                                    \</Coverage\>

                                    \<Coverage\>

                                        \<CoverageType\>

                                            \<Code\>CBSL\</Code\>

                                            \<Description\>CSL (BI \&amp; PD)\</Description\>

                                        \</CoverageType\>

                                        \<IndividualLimitAmount\>0\</IndividualLimitAmount\>

                                        \<OccurrenceLimitAmount\>0\</OccurrenceLimitAmount\>

                                        \<CombinedSingleLimitAmount\>80000\</CombinedSingleLimitAmount\>

                                        \<FromDate\>20220105\</FromDate\>

                                        \<ToDate\>20230105\</ToDate\>

                                    \</Coverage\>

                                    \<Coverage\>

                                        \<CoverageType\>

                                            \<Code\>MAPD\</Code\>

                                            \<Description\>MASS. OPTIONAL PROPERTY DAMAGE LIAB\</Description\>

                                        \</CoverageType\>

                                        \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                        \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                        \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                        \<FromDate\>20200105\</FromDate\>

                                        \<ToDate\>20210105\</ToDate\>

                                    \</Coverage\>

                                    \<Coverage\>

                                        \<CoverageType\>

                                            \<Code\>PDMG\</Code\>

                                            \<Description\>Property Damage\</Description\>

                                        \</CoverageType\>

                                        \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                        \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                        \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                        \<FromDate\>20200105\</FromDate\>

                                        \<ToDate\>20230105\</ToDate\>

                                    \</Coverage\>

                                    \<Coverage\>

                                        \<CoverageType\>

                                            \<Code\>PINJ\</Code\>

                                            \<Description\>Personal Injury\</Description\>

                                        \</CoverageType\>

                                        \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                        \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                        \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                        \<FromDate\>20200105\</FromDate\>

                                        \<ToDate\>20220105\</ToDate\>

                                    \</Coverage\>

                                    \<Coverage\>

                                        \<CoverageType\>

                                            \<Code\>UMPD\</Code\>

                                            \<Description\>Uninsured Motorist (PD)\</Description\>

                                        \</CoverageType\>

                                        \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                        \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                        \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                        \<FromDate\>20220105\</FromDate\>

                                        \<ToDate\>20230105\</ToDate\>

                                    \</Coverage\>

                                    \<Coverage\>

                                        \<CoverageType\>

                                            \<Code\>UMPD\</Code\>

                                            \<Description\>Uninsured Motorist (PD)\</Description\>

                                        \</CoverageType\>

                                        \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                        \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                        \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                        \<FromDate\>20200105\</FromDate\>

                                        \<ToDate\>20210105\</ToDate\>

                                    \</Coverage\>

                                \</Coverages\>

                                \<Vehicles\>

                                    \<Vehicle\>

                                        \<Year\>1985\</Year\>

                                        \<Make\>GMC\</Make\>

                                        \<Model\>UT\</Model\>

                                        \<VIN\>1G5CT18B5F8530675\</VIN\>

                                        \<ClassCode\>000000\</ClassCode\>

                                        \<BusinessUse\>Y\</BusinessUse\>

                                        \<CollisionDeductibleAmount\>1000\</CollisionDeductibleAmount\>

                                        \<ComprehensiveDeductibleAmount\>500\</ComprehensiveDeductibleAmount\>

                                        \<FromDate\>20220105\</FromDate\>

                                        \<ToDate\>20230105\</ToDate\>

                                        \<CollisionIndicator\>Y\</CollisionIndicator\>

                                        \<ComprehensiveIndicator\>Y\</ComprehensiveIndicator\>

                                        \<Coverages\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>BINJ\</Code\>

                                                    \<Description\>Bodily Injury\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>40000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>80000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20220105\</FromDate\>

                                                \<ToDate\>20230105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>PDMG\</Code\>

                                                    \<Description\>Property Damage\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20220105\</FromDate\>

                                                \<ToDate\>20230105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>CBSL\</Code\>

                                                    \<Description\>CSL (BI \&amp; PD)\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>0\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>0\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>80000\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20220105\</FromDate\>

                                                \<ToDate\>20230105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>UMPD\</Code\>

                                                    \<Description\>Uninsured Motorist (PD)\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20220105\</FromDate\>

                                                \<ToDate\>20230105\</ToDate\>

                                            \</Coverage\>

                                        \</Coverages\>

                                    \</Vehicle\>

                                    \<Vehicle\>

                                        \<Year\>2000\</Year\>

                                        \<Make\>CHEV\</Make\>

                                        \<Model\>K1S\</Model\>

                                        \<VIN\>3GNFK16T9YG218125\</VIN\>

                                        \<ClassCode\>000000\</ClassCode\>

                                        \<BusinessUse\>Y\</BusinessUse\>

                                        \<CollisionDeductibleAmount\>1000\</CollisionDeductibleAmount\>

                                        \<ComprehensiveDeductibleAmount\>500\</ComprehensiveDeductibleAmount\>

                                        \<FromDate\>20220105\</FromDate\>

                                        \<ToDate\>20230105\</ToDate\>

                                        \<CollisionIndicator\>Y\</CollisionIndicator\>

                                        \<ComprehensiveIndicator\>Y\</ComprehensiveIndicator\>

                                        \<Coverages\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>BINJ\</Code\>

                                                    \<Description\>Bodily Injury\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>40000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>80000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20220105\</FromDate\>

                                                \<ToDate\>20230105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>PDMG\</Code\>

                                                    \<Description\>Property Damage\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20220105\</FromDate\>

                                                \<ToDate\>20230105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>CBSL\</Code\>

                                                    \<Description\>CSL (BI \&amp; PD)\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>0\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>0\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>80000\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20220105\</FromDate\>

                                                \<ToDate\>20230105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>UMPD\</Code\>

                                                    \<Description\>Uninsured Motorist (PD)\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20220105\</FromDate\>

                                                \<ToDate\>20230105\</ToDate\>

                                            \</Coverage\>

                                        \</Coverages\>

                                    \</Vehicle\>

                                    \<Vehicle\>

                                        \<Year\>2006\</Year\>

                                        \<Make\>HOND\</Make\>

                                        \<Model\>ASE\</Model\>

                                        \<VIN\>1HGCM56306A148752\</VIN\>

                                        \<ClassCode\>000000\</ClassCode\>

                                        \<BusinessUse\>N\</BusinessUse\>

                                        \<CollisionDeductibleAmount\>1000\</CollisionDeductibleAmount\>

                                        \<ComprehensiveDeductibleAmount\>500\</ComprehensiveDeductibleAmount\>

                                        \<FromDate\>20220105\</FromDate\>

                                        \<ToDate\>20230105\</ToDate\>

                                        \<CollisionIndicator\>Y\</CollisionIndicator\>

                                        \<ComprehensiveIndicator\>Y\</ComprehensiveIndicator\>

                                        \<Coverages\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>BINJ\</Code\>

                                                    \<Description\>Bodily Injury\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>40000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>80000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20220105\</FromDate\>

                                                \<ToDate\>20230105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>PDMG\</Code\>

                                                    \<Description\>Property Damage\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20220105\</FromDate\>

                                                \<ToDate\>20230105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>CBSL\</Code\>

                                                    \<Description\>CSL (BI \&amp; PD)\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>0\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>0\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>80000\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20220105\</FromDate\>

                                                \<ToDate\>20230105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>UMPD\</Code\>

                                                    \<Description\>Uninsured Motorist (PD)\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20220105\</FromDate\>

                                                \<ToDate\>20230105\</ToDate\>

                                            \</Coverage\>

                                        \</Coverages\>

                                    \</Vehicle\>

                                    \<Vehicle\>

                                        \<Year\>2008\</Year\>

                                        \<Make\>GMC\</Make\>

                                        \<Model\>S1F\</Model\>

                                        \<VIN\>1GKER23788J291227\</VIN\>

                                        \<ClassCode\>000000\</ClassCode\>

                                        \<CollisionDeductibleAmount\>1000\</CollisionDeductibleAmount\>

                                        \<ComprehensiveDeductibleAmount\>500\</ComprehensiveDeductibleAmount\>

                                        \<FromDate\>20200105\</FromDate\>

                                        \<ToDate\>20220105\</ToDate\>

                                        \<CollisionIndicator\>Y\</CollisionIndicator\>

                                        \<ComprehensiveIndicator\>Y\</ComprehensiveIndicator\>

                                        \<Coverages\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>BINJ\</Code\>

                                                    \<Description\>Bodily Injury\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>40000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>80000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20200105\</FromDate\>

                                                \<ToDate\>20220105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>PDMG\</Code\>

                                                    \<Description\>Property Damage\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20200105\</FromDate\>

                                                \<ToDate\>20220105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>PINJ\</Code\>

                                                    \<Description\>Personal Injury\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20200105\</FromDate\>

                                                \<ToDate\>20220105\</ToDate\>

                                            \</Coverage\>

                                        \</Coverages\>

                                    \</Vehicle\>

                                    \<Vehicle\>

                                        \<Year\>2008\</Year\>

                                        \<Make\>GMC\</Make\>

                                        \<Model\>S1F\</Model\>

                                        \<VIN\>1GKER23788J291227\</VIN\>

                                        \<ClassCode\>000000\</ClassCode\>

                                        \<BusinessUse\>Y\</BusinessUse\>

                                        \<CollisionDeductibleAmount\>1000\</CollisionDeductibleAmount\>

                                        \<ComprehensiveDeductibleAmount\>500\</ComprehensiveDeductibleAmount\>

                                        \<FromDate\>20220105\</FromDate\>

                                        \<ToDate\>20230105\</ToDate\>

                                        \<CollisionIndicator\>Y\</CollisionIndicator\>

                                        \<ComprehensiveIndicator\>Y\</ComprehensiveIndicator\>

                                        \<Coverages\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>BINJ\</Code\>

                                                    \<Description\>Bodily Injury\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>40000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>80000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20220105\</FromDate\>

                                                \<ToDate\>20230105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>PDMG\</Code\>

                                                    \<Description\>Property Damage\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20220105\</FromDate\>

                                                \<ToDate\>20230105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>CBSL\</Code\>

                                                    \<Description\>CSL (BI \&amp; PD)\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>0\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>0\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>80000\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20220105\</FromDate\>

                                                \<ToDate\>20230105\</ToDate\>

                                            \</Coverage\>

                                            \<Coverage\>

                                                \<CoverageType\>

                                                    \<Code\>UMPD\</Code\>

                                                    \<Description\>Uninsured Motorist (PD)\</Description\>

                                                \</CoverageType\>

                                                \<IndividualLimitAmount\>20000\</IndividualLimitAmount\>

                                                \<OccurrenceLimitAmount\>40000\</OccurrenceLimitAmount\>

                                                \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                                                \<FromDate\>20220105\</FromDate\>

                                                \<ToDate\>20230105\</ToDate\>

                                            \</Coverage\>

                                        \</Coverages\>

                                    \</Vehicle\>

                                \</Vehicles\>

                                \<TransactionInformations\>

                                    \<TransactionInformation\>

                                        \<TransactionType\>

                                            \<Code\>NB\</Code\>

                                            \<Description\>New Business\</Description\>

                                        \</TransactionType\>

                                        \<EffectiveDate\>20200105\</EffectiveDate\>

                                    \</TransactionInformation\>

                                    \<TransactionInformation\>

                                        \<TransactionType\>

                                            \<Code\>RW\</Code\>

                                            \<Description\>Renewal\</Description\>

                                        \</TransactionType\>

                                        \<EffectiveDate\>20210105\</EffectiveDate\>

                                    \</TransactionInformation\>

                                    \<TransactionInformation\>

                                        \<TransactionType\>

                                            \<Code\>RW\</Code\>

                                            \<Description\>Renewal\</Description\>

                                        \</TransactionType\>

                                        \<EffectiveDate\>20220105\</EffectiveDate\>

                                    \</TransactionInformation\>

                                \</TransactionInformations\>

                            \</History\>

                            \<PolicyNumber\>VRSKLSP201810021001\</PolicyNumber\>

                            \<PolicyStatus\>INFORCE\</PolicyStatus\>

                            \<PolicyReportedDate\>20230213\</PolicyReportedDate\>

                            \<InceptionDate\>20170301\</InceptionDate\>

                            \<LastReportedTermEffectiveDate\>20230105\</LastReportedTermEffectiveDate\>

                            \<LastReportedTermExpirationDate\>20240105\</LastReportedTermExpirationDate\>

                            \<NumberOfCancellations\>0\</NumberOfCancellations\>

                            \<NumberOfRenewals\>3\</NumberOfRenewals\>

                            \<MatchBasisInformation\>

                                \<MatchScore\>100\</MatchScore\>

                                \<SearchType\>

                                    \<Code\>P\</Code\>

                                    \<Description\>Person\</Description\>

                                \</SearchType\>

                                \<MatchReasons\>

                                    \<MatchReason\>NAME IS IDENTICAL\</MatchReason\>

                                    \<MatchReason\>ADDRESS IS IDENTICAL\</MatchReason\>

                                    \<MatchReason\>ZIP IS IDENTICAL\</MatchReason\>

                                \</MatchReasons\>

                            \</MatchBasisInformation\>

                        \</Policy\>

                    \</Policies\>

                    \<CoverageLapseInformation\>

                        \<SearchPerson\>

                            \<CoverageIntervals\>

                                \<CoverageInterval\>

                                    \<Carrier\>

                                        \<FinancialAMBEST\>99999\</FinancialAMBEST\>

                                        \<Name\>INSURANCE SERVICES O\</Name\>

                                        \<AMBEST\>99999\</AMBEST\>

                                        \<NAIC\>00000\</NAIC\>

                                    \</Carrier\>

                                    \<StartDate\>20220105\</StartDate\>

                                    \<EndDate\>20240105\</EndDate\>

                                    \<NumberOfCoverageDays\>628\</NumberOfCoverageDays\>

                                    \<HasBreakFromPriorCoverage\>NA\</HasBreakFromPriorCoverage\>

                                    \<NumberOfLapseDays\>0\</NumberOfLapseDays\>

                                \</CoverageInterval\>

                            \</CoverageIntervals\>

                            \<GivenName\>YUKI\</GivenName\>

                            \<Surname\>BONZHEIM\</Surname\>

                            \<InputDriverSequenceNumber\>1\</InputDriverSequenceNumber\>

                            \<HasPossibleLapse\>N\</HasPossibleLapse\>

                            \<IsCurrentInforceCoverage\>Y\</IsCurrentInforceCoverage\>

                        \</SearchPerson\>

                    \</CoverageLapseInformation\>

                \</Body\>

            \</CoverageVerifierReport\>

            \<APlusAutoReport\>

                \<Header\>

                    \<Quoteback\>15446763-7f06-4452-b988-f77fb994a494\</Quoteback\>

                    \<TransactionId\>f91f424a-e848-4d0f-a575-e03cf73766bb\</TransactionId\>

                \</Header\>

                \<Body\>

                    \<ClaimActivityPredictor\>

                        \<CapIndicator\>Y\</CapIndicator\>

                        \<NumberOfClaims\>2\</NumberOfClaims\>

                    \</ClaimActivityPredictor\>

                    \<Claims\>

                        \<Claim\>

                            \<ClaimReferenceNumber\>4QA00526856\</ClaimReferenceNumber\>

                            \<CarrierClaimNumber\>VRLSAP20181002102\</CarrierClaimNumber\>

                            \<MatchReasons\>

                                \<MatchReason\>

                                    \<Code\>V\</Code\>

                                    \<Description\>VIN Search Type\</Description\>

                                \</MatchReason\>

                                \<MatchReason\>

                                    \<Code\>N\</Code\>

                                    \<Description\>Name and Date of Birth Search Type\</Description\>

                                \</MatchReason\>

                            \</MatchReasons\>

                            \<AtFaultIndicator\>

                                \<Code\>N\</Code\>

                                \<Description\>Insured not at fault\</Description\>

                            \</AtFaultIndicator\>

                            \<Insurer\>

                                \<Name\>INSURANCE SERVICES OFFICE, INC\</Name\>

                                \<AMBEST\>00001\</AMBEST\>

                                \<Address\>

                                    \<Street1\>545 WASHINGTON BLVD\</Street1\>

                                    \<City\>JERSEY CITY\</City\>

                                    \<StateCode\>NJ\</StateCode\>

                                    \<Zip\>07310\</Zip\>

                                    \<CountryCode\>US\</CountryCode\>

                                \</Address\>

                                \<Phone\>7323880332\</Phone\>

                            \</Insurer\>

                            \<Policy\>

                                \<PolicyType\>

                                    \<Code\>PAPP\</Code\>

                                    \<Description\>Personal Auto\</Description\>

                                \</PolicyType\>

                                \<OriginalInceptionDate\>20221001\</OriginalInceptionDate\>

                                \<ExpirationDate\>20241001\</ExpirationDate\>

                            \</Policy\>

                            \<MatchByInputDriverNumber\>2\</MatchByInputDriverNumber\>

                            \<Subjects\>

                                \<Subject\>

                                    \<GivenName\>DOUGLAS\</GivenName\>

                                    \<Surname\>BONZHEIM\</Surname\>

                                    \<MiddleName\>J\</MiddleName\>

                                    \<DOB\>19760101\</DOB\>

                                    \<DLNumber\>D852424151335\</DLNumber\>

                                    \<DLState\>FL\</DLState\>

                                    \<RoleInClaim\>

                                        \<Code\>IN\</Code\>

                                        \<Description\>Insured\</Description\>

                                    \</RoleInClaim\>

                                    \<Address\>

                                        \<Street1\>329 WOODSTEAD LN\</Street1\>

                                        \<City\>LONGWOOD\</City\>

                                        \<StateCode\>FL\</StateCode\>

                                        \<Zip\>32779\</Zip\>

                                    \</Address\>

                                    \<SequenceInInputDrivers\>2\</SequenceInInputDrivers\>

                                \</Subject\>

                                \<Subject\>

                                    \<GivenName\>DOUGLAS\</GivenName\>

                                    \<Surname\>BONZHEIM\</Surname\>

                                    \<MiddleName\>J\</MiddleName\>

                                    \<DOB\>19760101\</DOB\>

                                    \<DLNumber\>D852424151335\</DLNumber\>

                                    \<DLState\>FL\</DLState\>

                                    \<RoleInClaim\>

                                        \<Code\>SA\</Code\>

                                        \<Description\>Insured Driver Same as Insured\</Description\>

                                    \</RoleInClaim\>

                                    \<Address\>

                                        \<Street1\>329 WOODSTEAD LN\</Street1\>

                                        \<City\>LONGWOOD\</City\>

                                        \<StateCode\>FL\</StateCode\>

                                        \<Zip\>32779\</Zip\>

                                    \</Address\>

                                    \<SequenceInInputDrivers\>2\</SequenceInInputDrivers\>

                                \</Subject\>

                                \<Subject\>

                                    \<GivenName\>ELISA\</GivenName\>

                                    \<Surname\>ALMADA\</Surname\>

                                    \<MiddleName\>M\</MiddleName\>

                                    \<DOB\>19820501\</DOB\>

                                    \<Gender\>M\</Gender\>

                                    \<DLNumber\>V910235269825\</DLNumber\>

                                    \<DLState\>FL\</DLState\>

                                    \<RoleInClaim\>

                                        \<Code\>CL\</Code\>

                                        \<Description\>Claimant\</Description\>

                                    \</RoleInClaim\>

                                    \<Address\>

                                        \<Street1\>2511 16TH STREET CT W\</Street1\>

                                        \<City\>BRADENTON\</City\>

                                        \<StateCode\>FL\</StateCode\>

                                        \<Zip\>34205\</Zip\>

                                    \</Address\>

                                    \<SequenceInInputDrivers\>0\</SequenceInInputDrivers\>

                                \</Subject\>

                                \<Subject\>

                                    \<GivenName\>KATY\</GivenName\>

                                    \<Surname\>PERRY\</Surname\>

                                    \<DOB\>19751108\</DOB\>

                                    \<DLNumber\>E914883836547\</DLNumber\>

                                    \<DLState\>FL\</DLState\>

                                    \<RoleInClaim\>

                                        \<Code\>CD\</Code\>

                                        \<Description\>Claimant Driver\</Description\>

                                    \</RoleInClaim\>

                                    \<Address\>

                                        \<Street1\>2002 KINGSTON\</Street1\>

                                        \<City\>JACKSONVILLE\</City\>

                                        \<StateCode\>FL\</StateCode\>

                                        \<Zip\>32209\</Zip\>

                                    \</Address\>

                                    \<SequenceInInputDrivers\>0\</SequenceInInputDrivers\>

                                \</Subject\>

                            \</Subjects\>

                            \<LossInformation\>

                                \<LossDate\>20230115\</LossDate\>

                                \<LossTime\>0000\</LossTime\>

                                \<Losses\>

                                    \<Loss\>

                                        \<CoverageType\>

                                            \<Code\>LIAB\</Code\>

                                            \<Description\>Liability\</Description\>

                                        \</CoverageType\>

                                        \<LossType\>

                                            \<Code\>BI\</Code\>

                                            \<Description\>Body injury\</Description\>

                                        \</LossType\>

                                        \<DispositionStatus\>

                                            \<Code\>C\</Code\>

                                            \<Description\>Closed\</Description\>

                                        \</DispositionStatus\>

                                        \<Amount\>2000\</Amount\>

                                        \<ClaimStandardizationCode\>N02EPA308071U111\</ClaimStandardizationCode\>

                                    \</Loss\>

                                \</Losses\>

                            \</LossInformation\>

                            \<ClaimStandardizationCode\>N02EPA308071U111\</ClaimStandardizationCode\>

                            \<Vehicles\>

                                \<Vehicle\>

                                    \<Make\>GENERAL MOTORS CORP\</Make\>

                                    \<Model\>ACADIA\</Model\>

                                    \<Year\>2008\</Year\>

                                    \<VIN\>1GKER23788J291227\</VIN\>

                                    \<VINValidation\>

                                        \<Code\>P\</Code\>

                                        \<Description\>Pass\</Description\>

                                    \</VINValidation\>

                                \</Vehicle\>

                            \</Vehicles\>

                        \</Claim\>

                        \<Claim\>

                            \<ClaimReferenceNumber\>3IA00527548\</ClaimReferenceNumber\>

                            \<CarrierClaimNumber\>VRLSAP20181002101\</CarrierClaimNumber\>

                            \<MatchReasons\>

                                \<MatchReason\>

                                    \<Code\>V\</Code\>

                                    \<Description\>VIN Search Type\</Description\>

                                \</MatchReason\>

                                \<MatchReason\>

                                    \<Code\>Y\</Code\>

                                    \<Description\>Policy Number search\</Description\>

                                \</MatchReason\>

                                \<MatchReason\>

                                    \<Code\>N\</Code\>

                                    \<Description\>Name and Date of Birth Search Type\</Description\>

                                \</MatchReason\>

                                \<MatchReason\>

                                    \<Code\>A\</Code\>

                                    \<Description\>Name and Address Search Type\</Description\>

                                \</MatchReason\>

                            \</MatchReasons\>

                            \<AtFaultIndicator\>

                                \<Code\>Y\</Code\>

                                \<Description\>Insured at Fault\</Description\>

                            \</AtFaultIndicator\>

                            \<Insurer\>

                                \<Name\>INSURANCE SERVICES OFFICE, INC\</Name\>

                                \<AMBEST\>00001\</AMBEST\>

                                \<Address\>

                                    \<Street1\>545 WASHINGTON BLVD\</Street1\>

                                    \<City\>JERSEY CITY\</City\>

                                    \<StateCode\>NJ\</StateCode\>

                                    \<Zip\>07310\</Zip\>

                                    \<CountryCode\>US\</CountryCode\>

                                \</Address\>

                                \<Phone\>7323880332\</Phone\>

                            \</Insurer\>

                            \<Policy\>

                                \<PolicyNumber\>VRSKLSP201810021001\</PolicyNumber\>

                                \<PolicyType\>

                                    \<Code\>PAPP\</Code\>

                                    \<Description\>Personal Auto\</Description\>

                                \</PolicyType\>

                                \<OriginalInceptionDate\>20200105\</OriginalInceptionDate\>

                                \<ExpirationDate\>20240105\</ExpirationDate\>

                            \</Policy\>

                            \<MatchByInputDriverNumber\>2\</MatchByInputDriverNumber\>

                            \<Subjects\>

                                \<Subject\>

                                    \<GivenName\>DOUGLAS\</GivenName\>

                                    \<Surname\>BONZHEIM\</Surname\>

                                    \<MiddleName\>J\</MiddleName\>

                                    \<DOB\>19760101\</DOB\>

                                    \<DLNumber\>D852424151335\</DLNumber\>

                                    \<DLState\>FL\</DLState\>

                                    \<RoleInClaim\>

                                        \<Code\>IN\</Code\>

                                        \<Description\>Insured\</Description\>

                                    \</RoleInClaim\>

                                    \<Address\>

                                        \<Street1\>7827 ADELAIDE LP\</Street1\>

                                        \<City\>NEW PORT RICHEY\</City\>

                                        \<StateCode\>FL\</StateCode\>

                                        \<Zip\>34655\</Zip\>

                                    \</Address\>

                                    \<SequenceInInputDrivers\>2\</SequenceInInputDrivers\>

                                \</Subject\>

                                \<Subject\>

                                    \<GivenName\>DOUGLAS\</GivenName\>

                                    \<Surname\>BONZHEIM\</Surname\>

                                    \<MiddleName\>J\</MiddleName\>

                                    \<DOB\>19760101\</DOB\>

                                    \<DLNumber\>D852424151335\</DLNumber\>

                                    \<DLState\>FL\</DLState\>

                                    \<RoleInClaim\>

                                        \<Code\>SA\</Code\>

                                        \<Description\>Insured Driver Same as Insured\</Description\>

                                    \</RoleInClaim\>

                                    \<Address\>

                                        \<Street1\>7827 ADELAIDE LP\</Street1\>

                                        \<City\>NEW PORT RICHEY\</City\>

                                        \<StateCode\>FL\</StateCode\>

                                        \<Zip\>34655\</Zip\>

                                    \</Address\>

                                    \<SequenceInInputDrivers\>2\</SequenceInInputDrivers\>

                                \</Subject\>

                            \</Subjects\>

                            \<LossInformation\>

                                \<LossDate\>20221225\</LossDate\>

                                \<LossTime\>0000\</LossTime\>

                                \<Losses\>

                                    \<Loss\>

                                        \<CoverageType\>

                                            \<Code\>UM\</Code\>

                                            \<Description\>Uninsured Motorist\</Description\>

                                        \</CoverageType\>

                                        \<LossType\>

                                            \<Code\>UMPD\</Code\>

                                            \<Description\>Uninsured Motorist Property Damage\</Description\>

                                        \</LossType\>

                                        \<DispositionStatus\>

                                            \<Code\>C\</Code\>

                                            \<Description\>Closed\</Description\>

                                        \</DispositionStatus\>

                                        \<Amount\>2000\</Amount\>

                                        \<ClaimStandardizationCode\>Y12JPA309070U000\</ClaimStandardizationCode\>

                                    \</Loss\>

                                \</Losses\>

                            \</LossInformation\>

                            \<ClaimStandardizationCode\>Y12JPA309070U000\</ClaimStandardizationCode\>

                            \<Vehicles\>

                                \<Vehicle\>

                                    \<Make\>GENERAL MOTORS CORP\</Make\>

                                    \<Model\>ACADIA\</Model\>

                                    \<Year\>2008\</Year\>

                                    \<VIN\>1GKER23788J291227\</VIN\>

                                    \<VINValidation\>

                                        \<Code\>P\</Code\>

                                        \<Description\>Pass\</Description\>

                                    \</VINValidation\>

                                \</Vehicle\>

                            \</Vehicles\>

                        \</Claim\>

                    \</Claims\>

                    \<Vehicles\>

                        \<Vehicle\>

                            \<Make\>GMC\</Make\>

                            \<Model\>SC4\</Model\>

                            \<Year\>1985\</Year\>

                            \<VIN\>1G5CT18B5F8530675\</VIN\>

                            \<VINValidation\>

                                \<Code\>P\</Code\>

                                \<Description\>Pass\</Description\>

                            \</VINValidation\>

                            \<EstimateInformation\>

                                \<EstimateAvailable\>N\</EstimateAvailable\>

                                \<Mileage\>0\</Mileage\>

                            \</EstimateInformation\>

                            \<VINDecoding\>

                                \<VINUnit\>

                                    \<VINCharacter\>1\</VINCharacter\>

                                    \<Description\>Country of Origin\</Description\>

                                    \<Value\>UNITED STATES OF AMERICA\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>G\</VINCharacter\>

                                    \<Description\>Make\</Description\>

                                    \<Value\>Undetermined \*\</Value\>

                                    \<InvalidDigitIndicator\>\*\</InvalidDigitIndicator\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>5\</VINCharacter\>

                                    \<Description\>\* Undetermined \*\</Description\>

                                    \<Value\>Undetermined \*\</Value\>

                                    \<InvalidDigitIndicator\>\*\</InvalidDigitIndicator\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>C\</VINCharacter\>

                                    \<Description\>\* Undetermined \*\</Description\>

                                    \<Value\>Undetermined \*\</Value\>

                                    \<InvalidDigitIndicator\>\*\</InvalidDigitIndicator\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>T\</VINCharacter\>

                                    \<Description\>\* Undetermined \*\</Description\>

                                    \<Value\>Undetermined \*\</Value\>

                                    \<InvalidDigitIndicator\>\*\</InvalidDigitIndicator\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>1\</VINCharacter\>

                                    \<Description\>\* Undetermined \*\</Description\>

                                    \<Value\>Undetermined \*\</Value\>

                                    \<InvalidDigitIndicator\>\*\</InvalidDigitIndicator\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>8\</VINCharacter\>

                                    \<Description\>\* Undetermined \*\</Description\>

                                    \<Value\>Undetermined \*\</Value\>

                                    \<InvalidDigitIndicator\>\*\</InvalidDigitIndicator\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>B\</VINCharacter\>

                                    \<Description\>\* Undetermined \*\</Description\>

                                    \<Value\>Undetermined \*\</Value\>

                                    \<InvalidDigitIndicator\>\*\</InvalidDigitIndicator\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>5\</VINCharacter\>

                                    \<Description\>Check Digit\</Description\>

                                    \<Value\>Check Digit Matches\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>F\</VINCharacter\>

                                    \<Description\>Year\</Description\>

                                    \<Value\>Undetermined \*\</Value\>

                                    \<InvalidDigitIndicator\>\*\</InvalidDigitIndicator\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>8\</VINCharacter\>

                                    \<Description\>\* Undetermined \*\</Description\>

                                    \<Value\>Undetermined \*\</Value\>

                                    \<InvalidDigitIndicator\>\*\</InvalidDigitIndicator\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>530675\</VINCharacter\>

                                    \<Description\>Sequence Number\</Description\>

                                    \<Value\>Range Undetermined\</Value\>

                                    \<InvalidDigitIndicator\>\*\</InvalidDigitIndicator\>

                                \</VINUnit\>

                            \</VINDecoding\>

                        \</Vehicle\>

                        \<Vehicle\>

                            \<Make\>CHEV\</Make\>

                            \<Model\>SUB\</Model\>

                            \<Year\>2000\</Year\>

                            \<VIN\>3GNFK16T9YG218125\</VIN\>

                            \<VINValidation\>

                                \<Code\>P\</Code\>

                                \<Description\>Pass\</Description\>

                            \</VINValidation\>

                            \<EventDataRecorderAvailable\>Y\</EventDataRecorderAvailable\>

                            \<EstimateInformation\>

                                \<EstimateAvailable\>N\</EstimateAvailable\>

                                \<Mileage\>0\</Mileage\>

                            \</EstimateInformation\>

                            \<NoticesOfRecall\>

                                \<NoticeOfRecall\>

                                    \<RecallId\>05V379000\</RecallId\>

                                    \<ComponentInfo\>SERVICE BRAKES, HYDRAULIC:ANTILOCK/TRACTION CONTROL/ELECTRONIC LIMITED SLIP                                                                           \</ComponentInfo\>

                                    \<RecallSummary\>CERTAIN PICKUP TRUCKS AND SPORT UTILITY VEHICLES MAY EXPERIENCE UNWANTED ANTILOCK BRAKE SYSTEM (ABS) ACTIVATION.  THIS CONDITION IS MORE LIKELY TO OCCUR IN ENVIRONMENTALLY CORROSIVE AREAS.   THIS RECALL WILL BE LAUNCHED IN THE "SALT BELT" STATES OF CONNECTICUT, DELAWARE, ILLINOIS, INDIANA, IOWA, MAR\</RecallSummary\>

                                    \<RecallDate\>20050829\</RecallDate\>

                                    \<NumberOfUnitsRecalled\>1353718\</NumberOfUnitsRecalled\>

                                    \<ManufactureRecallInfo\>GENERAL MOTORS CORP.\</ManufactureRecallInfo\>

                                    \<RecallConsequences\>THIS CAN CAUSE INCREASED STOPPING DISTANCES DURING LOW-SPEED BRAKE APPLICATIONS, WHICH COULD RESULT IN A CRASH.                                                                                                                                                                                             \</RecallConsequences\>

                                \</NoticeOfRecall\>

                                \<NoticeOfRecall\>

                                    \<RecallId\>05V155000\</RecallId\>

                                    \<ComponentInfo\>FUEL SYSTEM, GASOLINE:DELIVERY:FUEL PUMP                                                                                                              \</ComponentInfo\>

                                    \<RecallSummary\>CERTAIN TRUCKS AND SPORT UTILITY VEHICLES WERE BUILT WITH FUEL MODULE RESERVOIR ASSEMBLIES THAT CONTAIN FUEL PUMP WIRES CONNECTORS MAY OVERHEAT UNDER CERTAIN  OPERATING CONDITIONS.                                                                                                                        \</RecallSummary\>

                                    \<RecallDate\>20050414\</RecallDate\>

                                    \<NumberOfUnitsRecalled\>316508\</NumberOfUnitsRecalled\>

                                    \<ManufactureRecallInfo\>GENERAL MOTORS CORP.\</ManufactureRecallInfo\>

                                    \<RecallConsequences\>IF THE IGNITION CIRCUIT WIRE IS EXPOSED, THE FUEL PUMP FUSE WILL BLOW, DISABLING THE FUEL PUMP AND CAUSING AN ENGINE STALL OR NO-START CONDITION.  IF SUFFICIENT HEAT IS CONDUCTED TO THE PASS-THROUGH CONNECTOR, A  HOLE IN THE CONNECTOR MAY RESULT, WHICH MAY CAUSE A 'SERVICE ENGINE SOON' LIGHT TO BE I\</RecallConsequences\>

                                \</NoticeOfRecall\>

                                \<NoticeOfRecall\>

                                    \<RecallId\>05V005000\</RecallId\>

                                    \<ComponentInfo\>POWER TRAIN:DRIVELINE:DRIVESHAFT                                                                                                                      \</ComponentInfo\>

                                    \<RecallSummary\>SOME PICKUP TRUCKS, VANS, AND SPORT UTILITY VEHICLES EQUIPPED WITH A HYDRAULIC PUMP DRIVESHAFT THAT CAN FRACTURE, RESULTING IN IMMEDIATE LOSS OF HYDRAULIC POWER STEERING ASSIST.  ON CERTAIN VEHICLES EQUIPPED WITH HYDRO-BOOST POWER BRAKES, THE SAME CONDITION CAN RESULT IN LOSS OF POWER ASSIST FOR BRA\</RecallSummary\>

                                    \<RecallDate\>20050107\</RecallDate\>

                                    \<NumberOfUnitsRecalled\>98221\</NumberOfUnitsRecalled\>

                                    \<ManufactureRecallInfo\>GENERAL MOTORS CORP.\</ManufactureRecallInfo\>

                                    \<RecallConsequences\>AN INOPERATIVE PUMP CAN CAUSE INCREASED STEERING EFFORT, AND IN HYDRO-BOOST EQUIPPED VEHICLES ALSO INCREASED BRAKING EFFORT, BUT DOES NOT COMPLETELY ELIMINATE THE ABILITY TO STEER OR SLOW THE VEHICLE.                                                                                                    \</RecallConsequences\>

                                \</NoticeOfRecall\>

                                \<NoticeOfRecall\>

                                    \<RecallId\>03V094000\</RecallId\>

                                    \<ComponentInfo\>STRUCTURE                                                                                                                                             \</ComponentInfo\>

                                    \<RecallSummary\>CERTAIN PICKUP TRUCK, VAN, AND MINI VAN CONVERSIONS EQUIPPED WITH SOUTHERN COMFORT BUILT RUNNING BOARDS THAT CONTAIN CERTAIN COURTESY LIGHTS MANUFACTURED BY AMERICAN TECHNOLOGY COMPONENTS, INC.  THESE UNITS CONTAIN A COURTESY LIGHT OR LIGHTS THAT MIGHT OVERHEAT WHEN THE WIRE HARNESS IS EXPOSED TO EX\</RecallSummary\>

                                    \<RecallDate\>20030307\</RecallDate\>

                                    \<NumberOfUnitsRecalled\>3674\</NumberOfUnitsRecalled\>

                                    \<ManufactureRecallInfo\>SOUTHERN COMFORT CONVERSIONS\</ManufactureRecallInfo\>

                                    \<RecallConsequences\>THIS OVERHEATING CONDITION CAN CAUSE THE RUNNING BOARD TO MELT OR CAUSE A FIRE.                                                                                                                                                                                                                             \</RecallConsequences\>

                                \</NoticeOfRecall\>

                                \<NoticeOfRecall\>

                                    \<RecallId\>02V178000\</RecallId\>

                                    \<ComponentInfo\>AIR BAGS:FRONTAL:SENSOR/CONTROL MODULE                                                                                                                \</ComponentInfo\>

                                    \<RecallSummary\>ON CERTAIN PICKUP AND UTILITY TRUCKS, SOME OF THESE VEHICLES HAVE AN AIR BAG SENSING DIAGNOSTIC MODULE (SDM) WHICH CONTAINS AN ANOMALY THAT COULD RESULT IN THE DRIVER AND PASSENGER'S AIR BAG FAILING TO DEPLOY DURING CERTAIN FRONTAL CRASHES.                                                            \</RecallSummary\>

                                    \<RecallDate\>20020701\</RecallDate\>

                                    \<NumberOfUnitsRecalled\>525254\</NumberOfUnitsRecalled\>

                                    \<ManufactureRecallInfo\>GENERAL MOTORS CORP.\</ManufactureRecallInfo\>

                                    \<RecallConsequences\>IN A VEHICLE CRASH, FRONT SEAT OCCUPANTS MAY RECEIVE MORE SEVERE INJURIES.                                                                                                                                                                                                                                  \</RecallConsequences\>

                                \</NoticeOfRecall\>

                            \</NoticesOfRecall\>

                            \<VINDecoding\>

                                \<VINUnit\>

                                    \<VINCharacter\>3\</VINCharacter\>

                                    \<Description\>Country of Origin\</Description\>

                                    \<Value\>MEXICO\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>G\</VINCharacter\>

                                    \<Description\>Manufacturer\</Description\>

                                    \<Value\>CHEV   GENERAL MOTORS\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>N\</VINCharacter\>

                                    \<Description\>Vehicle Type\</Description\>

                                    \<Value\>MULTI PURPOSE VEHICLE\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>F\</VINCharacter\>

                                    \<Description\>Gross Vehicle Weight\</Description\>

                                    \<Value\>7001-8000 GVWR   HYDRAULIC BRAKES\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>K1\</VINCharacter\>

                                    \<Description\>Series\</Description\>

                                    \<Value\>FULL SIZE TRUCK 4X4, 1500 (1/2 TON)\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>6\</VINCharacter\>

                                    \<Description\>Body Style\</Description\>

                                    \<Value\>SUBURBAN\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>T\</VINCharacter\>

                                    \<Description\>Engine\</Description\>

                                    \<Value\>5.3L V8 MFI, IRON\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>9\</VINCharacter\>

                                    \<Description\>Check Digit\</Description\>

                                    \<Value\>Check Digit Matches\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>Y\</VINCharacter\>

                                    \<Description\>Year\</Description\>

                                    \<Value\>2000\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>G\</VINCharacter\>

                                    \<Description\>Plant\</Description\>

                                    \<Value\>SILAO, MEXICO\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>218125\</VINCharacter\>

                                    \<Description\>Serial Number\</Description\>

                                    \<Value\>Sequence in Range\</Value\>

                                \</VINUnit\>

                            \</VINDecoding\>

                        \</Vehicle\>

                        \<Vehicle\>

                            \<Make\>HOND\</Make\>

                            \<Model\>ACC\</Model\>

                            \<Year\>2006\</Year\>

                            \<VIN\>1HGCM56306A148752\</VIN\>

                            \<VINValidation\>

                                \<Code\>P\</Code\>

                                \<Description\>Pass\</Description\>

                            \</VINValidation\>

                            \<EventDataRecorderAvailable\>N\</EventDataRecorderAvailable\>

                            \<EstimateInformation\>

                                \<EstimateAvailable\>Y\</EstimateAvailable\>

                                \<ActivityDate\>20161020\</ActivityDate\>

                                \<LossDate\>20160827\</LossDate\>

                                \<Mileage\>113489\</Mileage\>

                            \</EstimateInformation\>

                            \<NoticesOfRecall\>

                                \<NoticeOfRecall\>

                                    \<RecallId\>19V499000\</RecallId\>

                                    \<ComponentInfo\>AIR BAGS:FRONTAL:DRIVER SIDE:INFLATOR MODULE                                                                                                          \</ComponentInfo\>

                                    \<RecallSummary\>Honda (American Honda Motor Co.) is recalling certain 2003 Acura 3.2CL, 2002-2003 3.2TL, 2003-2006 MDX, 2001-2007 Honda Accord, 2001-2005 Civic, 2003-2005 Civic Hybrid, 2001-2005 Civic GX NGV, 2002-2006 CR-V, 2003-2011 Element, 2002-2004 Odyssey, 2003-2008 Pilot and 2006 Ridgeline vehicles.      The\</RecallSummary\>

                                    \<RecallDate\>20190627\</RecallDate\>

                                    \<NumberOfUnitsRecalled\>3947\</NumberOfUnitsRecalled\>

                                    \<ManufactureRecallInfo\>Honda (American Honda Motor Co.)\</ManufactureRecallInfo\>

                                    \<RecallConsequences\>An inflator explosion may result in sharp metal fragments striking the driver or other occupants resulting in serious injury or death.                                                                                                                                                                      \</RecallConsequences\>

                                \</NoticeOfRecall\>

                                \<NoticeOfRecall\>

                                    \<RecallId\>19V501000\</RecallId\>

                                    \<ComponentInfo\>AIR BAGS:FRONTAL:PASSENGER SIDE:INFLATOR MODULE                                                                                                       \</ComponentInfo\>

                                    \<RecallSummary\>Honda (American Honda Motor Co.) is recalling certain 2003-2006 Acura MDX, 2005-2012 RL, 2003-2007 Honda Accord, 2001-2005 Civic, 2003-2005 Civic Hybrid, 2001-2005 Civic GX NGV, 2002-2006 CR-V, 2003-2011 Element, 2007-2008 Fit, 2002-2004 Odyssey, 2003-2008 Pilot, and 2006-2014 Ridgeline vehicles.   \</RecallSummary\>

                                    \<RecallDate\>20190627\</RecallDate\>

                                    \<NumberOfUnitsRecalled\>1657752\</NumberOfUnitsRecalled\>

                                    \<ManufactureRecallInfo\>Honda (American Honda Motor Co.)\</ManufactureRecallInfo\>

                                    \<RecallConsequences\>An inflator explosion may result in sharp metal fragments striking the driver or other occupants resulting in serious injury or death.                                                                                                                                                                      \</RecallConsequences\>

                                \</NoticeOfRecall\>

                                \<NoticeOfRecall\>

                                    \<RecallId\>19V182000\</RecallId\>

                                    \<ComponentInfo\>AIR BAGS:FRONTAL:DRIVER SIDE:INFLATOR MODULE                                                                                                          \</ComponentInfo\>

                                    \<RecallSummary\>Honda (American Honda Motor Co.) is recalling specific 2003 Acura 3.2CL, 2013-2016 ILX, 2013-2014 ILX Hybrid, 2003-2006 MDX, 2007-2016 RDX, 2002-2003 3.2TL, 2004-2006, and 2009-2014 TL, 2010-2013 ZDX and 2001-2007 and 2009 Honda Accord, 2001-2005 Civic, 2003-2005 Civic Hybrid, 2001-2005 Civic GX NGV\</RecallSummary\>

                                    \<RecallDate\>20190306\</RecallDate\>

                                    \<NumberOfUnitsRecalled\>1101534\</NumberOfUnitsRecalled\>

                                    \<ManufactureRecallInfo\>Honda (American Honda Motor Co.)\</ManufactureRecallInfo\>

                                    \<RecallConsequences\>An explosion of an inflator within the driver frontal air bag module may result in sharp metal fragments striking the driver, front seat passenger or other occupants resulting in serious injury or death.                                                                                                 \</RecallConsequences\>

                                \</NoticeOfRecall\>

                                \<NoticeOfRecall\>

                                    \<RecallId\>18V268000\</RecallId\>

                                    \<ComponentInfo\>AIR BAGS:FRONTAL:PASSENGER SIDE:INFLATOR MODULE                                                                                                       \</ComponentInfo\>

                                    \<RecallSummary\>Honda (American Honda Motor Co.) is recalling certain 2003-2012 Honda Accord and Pilot, 2010 Accord Crosstour, 2001-2011 Civic, 2002-2011 CR-V, 2003-2004, 2006-2008 and 2011 Element, 2007 and 2009-2013 Fit, 2010-2012 Insight, 2002-2004 Odyssey, and 2012 Ridgeline vehicles.  The front passenger air b\</RecallSummary\>

                                    \<RecallDate\>20180426\</RecallDate\>

                                    \<NumberOfUnitsRecalled\>1335\</NumberOfUnitsRecalled\>

                                    \<ManufactureRecallInfo\>Honda (American Honda Motor Co.)\</ManufactureRecallInfo\>

                                    \<RecallConsequences\>An incorrectly installed air bag may deploy improperly in the event of a crash, increasing the risk of injury.                                                                                                                                                                                              \</RecallConsequences\>

                                \</NoticeOfRecall\>

                                \<NoticeOfRecall\>

                                    \<RecallId\>16V178000\</RecallId\>

                                    \<ComponentInfo\>AIR BAGS:FRONTAL:PASSENGER SIDE:INFLATOR MODULE                                                                                                       \</ComponentInfo\>

                                    \<RecallSummary\>Honda (American Honda Motor Co.) is recalling certain model year 2004-2007 Accord vehicles manufactured October 1, 2003, to August 17, 2007\.  The affected vehicles may have been assembled with an incorrect passenger frontal air bag module that does not comply with the advanced air bag requirements. \</RecallSummary\>

                                    \<RecallDate\>20160330\</RecallDate\>

                                    \<NumberOfUnitsRecalled\>11602\</NumberOfUnitsRecalled\>

                                    \<ManufactureRecallInfo\>Honda (American Honda Motor Co.)\</ManufactureRecallInfo\>

                                    \<RecallConsequences\>An air bag module does not meet the advanced air bag requirements can increase the risk of injury or death in the event of a crash.                                                                                                                                                                         \</RecallConsequences\>

                                \</NoticeOfRecall\>

                            \</NoticesOfRecall\>

                            \<VINDecoding\>

                                \<VINUnit\>

                                    \<VINCharacter\>1\</VINCharacter\>

                                    \<Description\>Country of Origin\</Description\>

                                    \<Value\>UNITED STATES OF AMERICA\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>H\</VINCharacter\>

                                    \<Description\>Manufacturer\</Description\>

                                    \<Value\>HOND   HONDA\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>G\</VINCharacter\>

                                    \<Description\>Vehicle Type\</Description\>

                                    \<Value\>PASSENGER CAR\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>CM563\</VINCharacter\>

                                    \<Description\>Model\</Description\>

                                    \<Value\>ACCORD SE/4DR SD/5A/6 AIR BAGS\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>0\</VINCharacter\>

                                    \<Description\>Check Digit\</Description\>

                                    \<Value\>Check Digit Matches\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>6\</VINCharacter\>

                                    \<Description\>Year\</Description\>

                                    \<Value\>2006\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>A\</VINCharacter\>

                                    \<Description\>Plant\</Description\>

                                    \<Value\>MARYSVILLE, OH\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>148752\</VINCharacter\>

                                    \<Description\>Serial Number\</Description\>

                                    \<Value\>Sequence in Range\</Value\>

                                \</VINUnit\>

                            \</VINDecoding\>

                        \</Vehicle\>

                        \<Vehicle\>

                            \<Make\>GMC\</Make\>

                            \<Model\>ACA\</Model\>

                            \<Year\>2008\</Year\>

                            \<VIN\>1GKER23788J291227\</VIN\>

                            \<VINValidation\>

                                \<Code\>P\</Code\>

                                \<Description\>Pass\</Description\>

                            \</VINValidation\>

                            \<EventDataRecorderAvailable\>Y\</EventDataRecorderAvailable\>

                            \<EstimateInformation\>

                                \<EstimateAvailable\>N\</EstimateAvailable\>

                                \<Mileage\>0\</Mileage\>

                            \</EstimateInformation\>

                            \<NoticesOfRecall\>

                                \<NoticeOfRecall\>

                                    \<RecallId\>15V415000\</RecallId\>

                                    \<ComponentInfo\>STRUCTURE:BODY:HATCHBACK/LIFTGATE                                                                                                                     \</ComponentInfo\>

                                    \<RecallSummary\>General Motors LLC (GM) is recalling certain model year 2008-2012 Buick Enclave vehicles manufactured January 3, 2007, to February 29, 2012, 2009-2012 Chevrolet Traverse vehicles manufactured July 6, 2008, to March 9, 2012, 2007-2012 GMC Acadia vehicles manufactured September 15, 2006, to February 2\</RecallSummary\>

                                    \<RecallDate\>20150630\</RecallDate\>

                                    \<NumberOfUnitsRecalled\>691144\</NumberOfUnitsRecalled\>

                                    \<ManufactureRecallInfo\>General Motors LLC\</ManufactureRecallInfo\>

                                    \<RecallConsequences\>If the open liftgate unexpectedly falls, it may strike a person, increasing their risk of injury.                                                                                                                                                                                                           \</RecallConsequences\>

                                \</NoticeOfRecall\>

                                \<NoticeOfRecall\>

                                    \<RecallId\>14V118000\</RecallId\>

                                    \<ComponentInfo\>AIR BAGS:SIDE/WINDOW                                                                                                                                  \</ComponentInfo\>

                                    \<RecallSummary\>General Motors LLC (GM) is recalling certain model year 2008-2013 Buick Enclave and GMC Acadia and 2009-2013 Chevrolet Traverse and 2008-2010 Saturn Outlook vehicles.  In the affected vehicles, increased resistance in the driver and passenger seat mounted side impact air bag (SIAB) wiring harnesses \</RecallSummary\>

                                    \<RecallDate\>20140317\</RecallDate\>

                                    \<NumberOfUnitsRecalled\>1176407\</NumberOfUnitsRecalled\>

                                    \<ManufactureRecallInfo\>General Motors LLC\</ManufactureRecallInfo\>

                                    \<RecallConsequences\>Failure of the side impact air bags and seat belt pretensioners to deploy in a crash increase the risk of injury to the driver and front seat occupant.                                                                                                                                                     \</RecallConsequences\>

                                \</NoticeOfRecall\>

                                \<NoticeOfRecall\>

                                    \<RecallId\>10V240000\</RecallId\>

                                    \<ComponentInfo\>ELECTRICAL SYSTEM                                                                                                                                     \</ComponentInfo\>

                                    \<RecallSummary\>GM IS RECALLING CERTAIN MODEL YEAR 2006-2009 BUICK, LUCERNE; CADILLAC DTS; HUMMER H2; MODEL YEAR 2008-2009 BUICK ENCLAVE; CADILLAC CTS; MODEL YEAR 2007-2009 CADILLAC ESCALADE, ESCALADE ESV, ESCALADE EXT; CHEVROLET AVALANCHE, SILVERADO, SUBURBAN, TAHOE; GMC ACADIA, SIERRA, YUKON, YUKON XL; SATURN OUT\</RecallSummary\>

                                    \<RecallDate\>20100604\</RecallDate\>

                                    \<NumberOfUnitsRecalled\>1365070\</NumberOfUnitsRecalled\>

                                    \<ManufactureRecallInfo\>GENERAL MOTORS CORP.\</ManufactureRecallInfo\>

                                    \<RecallConsequences\>IT IS POSSIBLE FOR THE HEATED WASHER MODULE TO IGNITE AND A FIRE MAY OCCUR.                                                                                                                                                                                                                                 \</RecallConsequences\>

                                \</NoticeOfRecall\>

                                \<NoticeOfRecall\>

                                    \<RecallId\>08V441000\</RecallId\>

                                    \<ComponentInfo\>ELECTRICAL SYSTEM                                                                                                                                     \</ComponentInfo\>

                                    \<RecallSummary\>GM IS RECALLING 857,735 MY 2006-2008 BUICK LUCERNE; CADILLAC DTS; HUMMER H2; MY 2007-2008 CADILLAC ESCALADE, ESCALADE ESV, ESCALADE EXT; CHEVROLET AVALANCHE, SILVERADO, SUBURBAN, TAHOE; GMC ACADIA, SIERRA, YUKON, YUKON XL, SATURN OUTLOOK; AND MY 2008 BUICK ENCLAVE VEHICLES EQUIPPED WITH A HEATED WIP\</RecallSummary\>

                                    \<RecallDate\>20080828\</RecallDate\>

                                    \<NumberOfUnitsRecalled\>857735\</NumberOfUnitsRecalled\>

                                    \<ManufactureRecallInfo\>GENERAL MOTORS CORP.\</ManufactureRecallInfo\>

                                    \<RecallConsequences\>THIS MAY CAUSE OTHER ELECTRICAL FEATURES TO MALFUNCTION, CREATE AN ODOR, OR CAUSE SMOKE INCREASING THE RISK OF A FIRE.                                                                                                                                                                                      \</RecallConsequences\>

                                \</NoticeOfRecall\>

                                \<NoticeOfRecall\>

                                    \<RecallId\>08V410000\</RecallId\>

                                    \<ComponentInfo\>VISIBILITY:WINDSHIELD WIPER/WASHER:LINKAGES                                                                                                           \</ComponentInfo\>

                                    \<RecallSummary\>GM IS RECALLING 88,809 MY 2008 BUICK ENCLAVE, AND MY 2007-2008 GMC ACADIA AND SATURN OUTLOOK VEHICLES CURRENTLY OR PREVIOUSLY REGISTERED IN THE FOLLOWING STATES:  ALASKA, COLORADO, CONNECTICUT, DELAWARE, IDAHO, ILLINOIS, INDIANA, IOWA, MAINE, MARYLAND, MASSACHUSETTS, MICHIGAN, MINNESOTA, MONTANA, NE\</RecallSummary\>

                                    \<RecallDate\>20080814\</RecallDate\>

                                    \<NumberOfUnitsRecalled\>88809\</NumberOfUnitsRecalled\>

                                    \<ManufactureRecallInfo\>GENERAL MOTORS CORP.\</ManufactureRecallInfo\>

                                    \<RecallConsequences\>IF THIS WERE TO OCCUR, DRIVER VISIBILITY COULD BE REDUCED, WHICH COULD RESULT IN A VEHICLE CRASH.                                                                                                                                                                                                           \</RecallConsequences\>

                                \</NoticeOfRecall\>

                            \</NoticesOfRecall\>

                            \<VINDecoding\>

                                \<VINUnit\>

                                    \<VINCharacter\>1\</VINCharacter\>

                                    \<Description\>Country of Origin\</Description\>

                                    \<Value\>UNITED STATES OF AMERICA\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>G\</VINCharacter\>

                                    \<Description\>Manufacturer\</Description\>

                                    \<Value\>GMC    GENERAL MOTORS CORPORATION\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>K\</VINCharacter\>

                                    \<Description\>Vehicle Type\</Description\>

                                    \<Value\>GMC MPV\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>E\</VINCharacter\>

                                    \<Description\>Gross Vehicle Weight\</Description\>

                                    \<Value\>6001-7000 GVWR   HYDRAULIC BRAKES\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>R2\</VINCharacter\>

                                    \<Description\>Series\</Description\>

                                    \<Value\>ACADIA 1/2 TON FWD SLT(1)\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>3\</VINCharacter\>

                                    \<Description\>Body Style\</Description\>

                                    \<Value\>4D:ENV/YKN/DNLI/CRW/ACAD/TYPHN(KL6)\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>7\</VINCharacter\>

                                    \<Description\>Engine\</Description\>

                                    \<Value\>3.6L V6 SFI ALUM 60 DEG\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>8\</VINCharacter\>

                                    \<Description\>Check Digit\</Description\>

                                    \<Value\>Check Digit Matches\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>8\</VINCharacter\>

                                    \<Description\>Year\</Description\>

                                    \<Value\>2008\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>J\</VINCharacter\>

                                    \<Description\>Plant\</Description\>

                                    \<Value\>JNSVL, WI(YUKON)/LANSING,MI(ACADIA)\</Value\>

                                \</VINUnit\>

                                \<VINUnit\>

                                    \<VINCharacter\>291227\</VINCharacter\>

                                    \<Description\>Serial Number\</Description\>

                                    \<Value\>Sequence in Range\</Value\>

                                \</VINUnit\>

                            \</VINDecoding\>

                        \</Vehicle\>

                    \</Vehicles\>

                    \<SSNInformations\>

                        \<SSNInformation\>

                            \<SSN\>000000000\</SSN\>

                            \<SSNValidation\>

                                \<Code\>I\</Code\>

                                \<Description\>SSN Invalid\</Description\>

                            \</SSNValidation\>

                        \</SSNInformation\>

                        \<SSNInformation\>

                            \<SSN\>000007807\</SSN\>

                            \<SSNValidation\>

                                \<Code\>V\</Code\>

                                \<Description\>SSN has been Verified and Issued\</Description\>

                            \</SSNValidation\>

                        \</SSNInformation\>

                    \</SSNInformations\>

                \</Body\>

            \</APlusAutoReport\>

            \<AllMotorVehicleReports\>

                \<IndividualMotorVehicleReport\>

                    \<Header\>

                        \<Quoteback\>15446763-7f06-4452-b988-f77fb994a494\</Quoteback\>

                        \<TransactionId\>0617fab6-5732-462c-814a-6ab0d33901fe\</TransactionId\>

                    \</Header\>

                    \<Body\>

                        \<OrderNumber\>935983239\</OrderNumber\>

                        \<MotorVehicleReports\>

                            \<MotorVehicleReport\>

                                \<Identifier\>538984825\</Identifier\>

                                \<Status\>

                                    \<Code\>V\</Code\>

                                    \<Description\>NON-CLEAR report\</Description\>

                                \</Status\>

                                \<ViolationsType\>

                                    \<Code\>C\</Code\>

                                    \<Description\>Report passed through Custom violation code/point process\</Description\>

                                    \<PointTotal\>   0\</PointTotal\>

                                \</ViolationsType\>

                                \<DMVReportDate\>20201120\</DMVReportDate\>

                                \<ArchiveFlag\>N\</ArchiveFlag\>

                                \<DriversPrivacyProtectionActFlag\>N\</DriversPrivacyProtectionActFlag\>

                                \<Driver\>

                                    \<Name\>BONZHEIM, YUKI\</Name\>

                                    \<Address\>

                                        \<Street1\>7827 ADELAIDE LP\</Street1\>

                                        \<CityStateZip\>NEW PORT RICHEY, FL 34655\</CityStateZip\>

                                    \</Address\>

                                    \<DLNumber\>T520103597610\</DLNumber\>

                                    \<DLState\>FL\</DLState\>

                                    \<DOB\>19900311\</DOB\>

                                    \<Gender\>M\</Gender\>

                                    \<Height\>6'1\</Height\>

                                    \<License\>

                                        \<Class\>E\</Class\>

                                        \<Status\>VALID\</Status\>

                                        \<IssuedDate\>20131001\</IssuedDate\>

                                        \<ExpirationDate\>20210801\</ExpirationDate\>

                                        \<OriginalIssueDate\>20001201\</OriginalIssueDate\>

                                    \</License\>

                                    \<Detail\>OrderType : MvrIndicator \- REQUESTED AS: YUKI                      BONZHEIM                  DOB: 03111990  LICENSE : T520103597610 PERS:01: ACTIVE          VALID   E              1001201308012021 LIC CLASS: E                       DESC: OPERATOR LIC STATUS: VALID LIC ISSUED: 10/01/2021 LIC EXPIRES: 08/01/2029 PERS:02: EXPIRED         EXPIRED ID CARD        1201200910012014 LIC CLASS: ID CARD                 DESC: ID CARD LIC STATUS: EXPIRED LIC ISSUED: 12/01/2009 LIC EXPIRES: 10/01/2014 AS OF NOVEMBER 20, 2020 AT 9:50:20 AM, DRIVER PRIVILEGE T520-103-59-761-0 IS VALID. PERSONAL INFORMATION IS PROTECTED PURSUANT TO THE DRIVER PRIVACY PROTECTION ACT. ENTRIES BELOW ARE A THREE YEAR RECORD. ORIGINAL ISSUE DATE: 12/01/2000 REAL ID COMPLIANT ORGAN DONOR US CITIZEN BLOCKED PERSONAL INFORMATION BLOCKED FOR MAILING LIST PERSON HAS A DIGITAL IMAGE ELIGIBLE TO ELECT DRIVER SCHOOL.  DRIVER HAS MADE 2 ELECTIONS. LAST ELECTION WAS ON 02/01/2012. VIOLATIONS COMMITTED WHILE A CDL HOLDER OR IN A CMV VEHICLE ARE NOT ELIGIBLE FOR DRIVING SCHOOL ELECTION. COUNTY: MIAMI-DADE RESIDENTIAL ADDRESS: 2570 NW 48TH ST  MIAMI, FL  33142  COUNTY: MIAMI-DADE ISSUANCE HISTORY: LIC CLASS: ID CARD   ISSUE DATE: 12/01/1996   ISSUE TYPE: DUPLICATE LIC CLASS: ID CARD   ISSUE DATE: 12/01/2000   ISSUE TYPE: DUPLICATE LIC CLASS: CLASS E   ISSUE DATE: 05/01/2002   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 02/01/2003   ISSUE TYPE: DUPLICATE LIC CLASS: ID CARD   ISSUE DATE: 07/01/2006   ISSUE TYPE: DUPLICATE LIC CLASS: CLASS E   ISSUE DATE: 04/01/2009   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 02/01/2010   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 02/01/2010   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 08/01/2012   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 10/01/2013   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 10/01/2014   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 03/01/2018   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 10/01/2020   ISSUE TYPE: CDR/CDT CLEARANCE EXAMS TAKEN: VISION               DATE TAKEN: 10/01/2021   COUNT: 2   STATUS: PASS ROAD SIGN            DATE TAKEN: 12/01/2021   COUNT: 1   STATUS: PASS ROAD RULES           DATE TAKEN: 12/01/2020   COUNT: 3   STATUS: PASS DRIVING              DATE TAKEN: 12/01/2020   COUNT: 1   STATUS: PASS This report is generated for insurance purposes only and may not be used for any other purpose.  The use and dissemination of the report and information in it must comply with your iiX agreement and the  Fair Credit Reporting Act, the Driver's Privacy Protection Act, and any applicable state statute(s).  The data in the report from the applicable state agency or service bureau is provided through iiX "as is." \--- Customer-defined MVR scoring has been applied to this record.  Customer  is solely responsible for the application and use of the resulting score.\</Detail\>

                                    \<Violations\>

                                        \<Violation\>

                                            \<Type\>SUSP\</Type\>

                                            \<ViolationDate\>20220301\</ViolationDate\>

                                            \<CustomCode\>130110\</CustomCode\>

                                            \<CustomPoints\>3\</CustomPoints\>

                                            \<Detail\>FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 720198716 NOTICED PROVIDED: 12/01/2021 ADDED TO RECORD: 12/01/2021 SANCTION CODE: 7\</Detail\>

                                        \</Violation\>

                                        \<Violation\>

                                            \<Type\>REIN\</Type\>

                                            \<ConvictionDate\>20220301\</ConvictionDate\>

                                            \<CustomCode\>330130\</CustomCode\>

                                            \<CustomPoints\>-3\</CustomPoints\>

                                            \<Detail\>REINSTATED\</Detail\>

                                        \</Violation\>

                                        \<Violation\>

                                            \<Type\>SUSP\</Type\>

                                            \<ViolationDate\>20211001\</ViolationDate\>

                                            \<CustomCode\>130110\</CustomCode\>

                                            \<CustomPoints\>3\</CustomPoints\>

                                            \<Detail\>FR-REGISTRATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 830175467 NOTICED PROVIDED: 09/01/2021 ADDED TO RECORD: 09/01/2021 SANCTION CODE: 8\</Detail\>

                                        \</Violation\>

                                        \<Violation\>

                                            \<Type\>REIN\</Type\>

                                            \<ConvictionDate\>20211001\</ConvictionDate\>

                                            \<CustomCode\>330130\</CustomCode\>

                                            \<CustomPoints\>-3\</CustomPoints\>

                                            \<Detail\>REINSTATED\</Detail\>

                                        \</Violation\>

                                        \<Violation\>

                                            \<Type\>VIOL\</Type\>

                                            \<ViolationDate\>20200201\</ViolationDate\>

                                            \<ConvictionDate\>20200601\</ConvictionDate\>

                                            \<StateAssignedPoints\>0\</StateAssignedPoints\>

                                            \<CustomCode\>425100\</CustomCode\>

                                            \<CustomPoints\>0\</CustomPoints\>

                                            \<Detail\>316.0083 RED LIGHT CAMERA DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 23 CITATION NUMBER: A5OJ78E COUNTY: MIAMI-DADE STATE: FL ADDED TO RECORD: 06/01/2020 DISPOSITION CODE: 547\</Detail\>

                                        \</Violation\>

                                        \<Violation\>

                                            \<Type\>VIOL\</Type\>

                                            \<ViolationDate\>20190201\</ViolationDate\>

                                            \<ConvictionDate\>20190801\</ConvictionDate\>

                                            \<StateAssignedPoints\>0\</StateAssignedPoints\>

                                            \<CustomCode\>425100\</CustomCode\>

                                            \<CustomPoints\>0\</CustomPoints\>

                                            \<Detail\>316.0083 RED LIGHT CAMERA DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 24 CITATION NUMBER: AADQWXE COUNTY: MIAMI-DADE STATE: FL ADDED TO RECORD: 08/01/2019 DISPOSITION CODE: 547\</Detail\>

                                        \</Violation\>

                                    \</Violations\>

                                \</Driver\>

                            \</MotorVehicleReport\>

                        \</MotorVehicleReports\>

                    \</Body\>

                    \<StatusCode\>200\</StatusCode\>

                \</IndividualMotorVehicleReport\>

                \<IndividualMotorVehicleReport\>

                    \<Header\>

                        \<Quoteback\>15446763-7f06-4452-b988-f77fb994a494\</Quoteback\>

                        \<TransactionId\>1a17fb0d-7070-40c7-8aa0-f7fe7e47bf9d\</TransactionId\>

                    \</Header\>

                    \<Body\>

                        \<OrderNumber\>935983240\</OrderNumber\>

                        \<MotorVehicleReports\>

                            \<MotorVehicleReport\>

                                \<Identifier\>538984826\</Identifier\>

                                \<Status\>

                                    \<Code\>V\</Code\>

                                    \<Description\>NON-CLEAR report\</Description\>

                                \</Status\>

                                \<ViolationsType\>

                                    \<Code\>C\</Code\>

                                    \<Description\>Report passed through Custom violation code/point process\</Description\>

                                    \<PointTotal\>   4\</PointTotal\>

                                \</ViolationsType\>

                                \<DMVReportDate\>20201120\</DMVReportDate\>

                                \<ArchiveFlag\>N\</ArchiveFlag\>

                                \<DriversPrivacyProtectionActFlag\>N\</DriversPrivacyProtectionActFlag\>

                                \<Driver\>

                                    \<Name\>BONZHEIM, DOUGLAS\</Name\>

                                    \<Address\>

                                        \<Street1\>7827 ADELAIDE LP\</Street1\>

                                        \<CityStateZip\>NEW PORT RICHEY, FL 34655\</CityStateZip\>

                                    \</Address\>

                                    \<DLNumber\>M888777666555\</DLNumber\>

                                    \<DLState\>FL\</DLState\>

                                    \<DOB\>19760101\</DOB\>

                                    \<Gender\>M\</Gender\>

                                    \<Height\>5'10\</Height\>

                                    \<License\>

                                        \<Class\>E\</Class\>

                                        \<Status\>VALID P\</Status\>

                                        \<IssuedDate\>20220401\</IssuedDate\>

                                        \<ExpirationDate\>20300601\</ExpirationDate\>

                                        \<OriginalIssueDate\>20000401\</OriginalIssueDate\>

                                    \</License\>

                                    \<Detail\>OrderType : MvrIndicator \- REQUESTED AS: DOUGLAS        J          BONZHEIM                  DOB: 01011976  LICENSE : M888777666555 PERS:01: ACTIVE          VALID P E              0401202206012030 LIC CLASS: E                       DESC: OPERATOR LIC STATUS: VALID PENDING LIC ISSUED: 04/01/2022 LIC EXPIRES: 06/01/2030 PERS:02: EXPIRED         EXPIRED ID CARD        0601201805012019 LIC CLASS: ID CARD                 DESC: ID CARD LIC STATUS: EXPIRED LIC ISSUED: 06/01/2018 LIC EXPIRES: 05/01/2019 AS OF NOVEMBER 20, 2020 AT 9:39:55 AM, DRIVER PRIVILEGE M888-777-66-655-5 IS VALID PENDING SANCTION(S). PERSONAL INFORMATION IS PROTECTED PURSUANT TO THE DRIVER PRIVACY PROTECTION ACT. ENTRIES BELOW ARE A THREE YEAR RECORD. ORIGINAL ISSUE DATE: 04/01/2000 REAL ID COMPLIANT US CITIZEN RECORD APPEARS IN NATIONAL DRIVER REGISTER BLOCKED PERSONAL INFORMATION BLOCKED FOR MAILING LIST PERSON HAS A DIGITAL IMAGE ELIGIBLE TO ELECT DRIVER SCHOOL.  DRIVER HAS MADE 0 ELECTIONS. VIOLATIONS COMMITTED WHILE A CDL HOLDER OR IN A CMV VEHICLE ARE NOT ELIGIBLE FOR DRIVING SCHOOL ELECTION. COUNTY: CLAY RESIDENTIAL ADDRESS: 4493 PLANTATION OAKS BLVD 1641  ORANGE PARK, FL  32065  COUNTY: CLAY ISSUANCE HISTORY: LIC CLASS: CLASS D   ISSUE DATE: 06/01/2001   ISSUE TYPE: DUPLICATE LIC CLASS: ID CARD   ISSUE DATE: 02/01/2003   ISSUE TYPE: DUPLICATE LIC CLASS: CLASS E   ISSUE DATE: 05/01/2015   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 06/01/2017   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 04/01/2018   ISSUE TYPE: REPLACEMENT LIC CLASS: ID CARD   ISSUE DATE: 02/01/2019   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 05/01/2019   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 12/01/2019   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 06/01/2020   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 09/01/2020   ISSUE TYPE: CDR/CDT CLEARANCE EXAMS TAKEN: VISION               DATE TAKEN: 04/01/2014   COUNT: 1   STATUS: PASS ROAD SIGN            DATE TAKEN: 08/01/2000   COUNT: 1   STATUS: PASS ROAD RULES           DATE TAKEN: 08/01/2000   COUNT: 4   STATUS: PASS DRIVING              DATE TAKEN: 04/01/2000   COUNT: 1   STATUS: RECIPROCATED This report is generated for insurance purposes only and may not be used for any other purpose.  The use and dissemination of the report and information in it must comply with your iiX agreement and the  Fair Credit Reporting Act, the Driver's Privacy Protection Act, and any applicable state statute(s).  The data in the report from the applicable state agency or service bureau is provided through iiX "as is." \--- Customer-defined MVR scoring has been applied to this record.  Customer  is solely responsible for the application and use of the resulting score.\</Detail\>

                                    \<Violations\>

                                        \<Violation\>

                                            \<Type\>SUSP\</Type\>

                                            \<ViolationDate\>20220801\</ViolationDate\>

                                            \<CustomCode\>130110\</CustomCode\>

                                            \<CustomPoints\>3\</CustomPoints\>

                                            \<Detail\>FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 730177824 NOTICED PROVIDED: 07/01/2022 ADDED TO RECORD: 07/01/2022 SANCTION CODE: 7\</Detail\>

                                        \</Violation\>

                                        \<Violation\>

                                            \<Type\>REIN\</Type\>

                                            \<ConvictionDate\>20220901\</ConvictionDate\>

                                            \<CustomCode\>330130\</CustomCode\>

                                            \<CustomPoints\>-3\</CustomPoints\>

                                            \<Detail\>REINSTATED\</Detail\>

                                        \</Violation\>

                                        \<Violation\>

                                            \<Type\>SUSP\</Type\>

                                            \<ViolationDate\>20211201\</ViolationDate\>

                                            \<CustomCode\>130110\</CustomCode\>

                                            \<CustomPoints\>3\</CustomPoints\>

                                            \<Detail\>FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) PENDING SUSPENSION CASE NUMBER 730183044 NOTICED PROVIDED: 11/01/2021 ACTION REQUIRED: YES ADDED TO RECORD: 11/01/2021 SANCTION CODE: 7\</Detail\>

                                        \</Violation\>

                                        \<Violation\>

                                            \<Type\>VIOL\</Type\>

                                            \<ViolationDate\>20200701\</ViolationDate\>

                                            \<ConvictionDate\>20210101\</ConvictionDate\>

                                            \<StateAssignedPoints\>0\</StateAssignedPoints\>

                                            \<CustomCode\>555110\</CustomCode\>

                                            \<CustomPoints\>0\</CustomPoints\>

                                            \<Detail\>OPERATING MV NO PROOF OF INSURANCE DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 10 CITATION NUMBER: A0JO2AE COUNTY: DUVAL ADDED TO RECORD: 02/01/2021 DISPOSITION CODE: 280\</Detail\>

                                        \</Violation\>

                                        \<Violation\>

                                            \<Type\>VIOL\</Type\>

                                            \<ViolationDate\>20201201\</ViolationDate\>

                                            \<ConvictionDate\>20210101\</ConvictionDate\>

                                            \<StateAssignedPoints\>0\</StateAssignedPoints\>

                                            \<CustomCode\>425100\</CustomCode\>

                                            \<CustomPoints\>1\</CustomPoints\>

                                            \<Detail\>316.0083 RED LIGHT CAMERA DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 11 CITATION NUMBER: A0IBDGE COUNTY: DUVAL ADDED TO RECORD: 02/01/2021 DISPOSITION CODE: 547\</Detail\>

                                        \</Violation\>

                                        \<Violation\>

                                            \<Type\>VIOL\</Type\>

                                            \<ViolationDate\>20200701\</ViolationDate\>

                                            \<ConvictionDate\>20210201\</ConvictionDate\>

                                            \<StateAssignedPoints\>0\</StateAssignedPoints\>

                                            \<CustomCode\>428300\</CustomCode\>

                                            \<CustomPoints\>0\</CustomPoints\>

                                            \<Detail\>SEAT BELT VIOLATION DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 12 CITATION NUMBER: A0JO2YE COUNTY: DUVAL ADDED TO RECORD: 02/01/2021 DISPOSITION CODE: 407\</Detail\>

                                        \</Violation\>

                                        \<Violation\>

                                            \<Type\>VIOL\</Type\>

                                            \<ViolationDate\>20200301\</ViolationDate\>

                                            \<ConvictionDate\>20200501\</ConvictionDate\>

                                            \<StateAssignedPoints\>3\</StateAssignedPoints\>

                                            \<CustomCode\>131240\</CustomCode\>

                                            \<CustomPoints\>0\</CustomPoints\>

                                            \<Detail\>DRIV WHILE LIC CANC/REV/SUSP DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 14 CITATION NUMBER: A0GLVGE COUNTY: DUVAL ADDED TO RECORD: 05/01/2020 DISPOSITION CODE: 609\</Detail\>

                                        \</Violation\>

                                    \</Violations\>

                                \</Driver\>

                            \</MotorVehicleReport\>

                        \</MotorVehicleReports\>

                    \</Body\>

                    \<StatusCode\>200\</StatusCode\>

                \</IndividualMotorVehicleReport\>

                \<IndividualMotorVehicleReport\>

                    \<Header\>

                        \<Quoteback\>15446763-7f06-4452-b988-f77fb994a494\</Quoteback\>

                        \<TransactionId\>3dd57ca9-6bb6-4317-9da6-6fef28b1e023\</TransactionId\>

                    \</Header\>

                    \<Body\>

                        \<OrderNumber\>935983244\</OrderNumber\>

                        \<MotorVehicleReports\>

                            \<MotorVehicleReport\>

                                \<Identifier\>538984827\</Identifier\>

                                \<Status\>

                                    \<Code\>V\</Code\>

                                    \<Description\>NON-CLEAR report\</Description\>

                                \</Status\>

                                \<ViolationsType\>

                                    \<Code\>C\</Code\>

                                    \<Description\>Report passed through Custom violation code/point process\</Description\>

                                    \<PointTotal\>   2\</PointTotal\>

                                \</ViolationsType\>

                                \<DMVReportDate\>20201120\</DMVReportDate\>

                                \<ArchiveFlag\>N\</ArchiveFlag\>

                                \<DriversPrivacyProtectionActFlag\>N\</DriversPrivacyProtectionActFlag\>

                                \<Driver\>

                                    \<Name\>BONZHEIM, LORNA\</Name\>

                                    \<Address\>

                                        \<Street1\>7827 ADELAIDE LP\</Street1\>

                                        \<CityStateZip\>NEW PORT RICHEY, FL 34655\</CityStateZip\>

                                    \</Address\>

                                    \<DLNumber\>B640693682100\</DLNumber\>

                                    \<DLState\>FL\</DLState\>

                                    \<DOB\>20030923\</DOB\>

                                    \<Gender\>F\</Gender\>

                                    \<Height\>5'6\</Height\>

                                    \<License\>

                                        \<Class\>E\</Class\>

                                        \<Status\>VALID\</Status\>

                                        \<IssuedDate\>20220301\</IssuedDate\>

                                        \<ExpirationDate\>20300701\</ExpirationDate\>

                                        \<OriginalIssueDate\>20010301\</OriginalIssueDate\>

                                        \<Restriction\>A\</Restriction\>

                                    \</License\>

                                    \<Detail\>OrderType : MvrIndicator \- REQUESTED AS: LORNA          P          BONZHEIM                  DOB: 09232003  LICENSE : B640693682100 PERS:01: ACTIVE          VALID   E              0301202207012030                A LIC CLASS: E                       DESC: OPERATOR LIC STATUS: VALID LIC ISSUED: 03/01/2022 LIC EXPIRES: 07/01/2030 LIC RESTR: A                          DESC: CORRECTIVE LENSES PERS:02: EXPIRED         EXPIRED ID CARD        0901200312012017 LIC CLASS: ID CARD                 DESC: ID CARD LIC STATUS: EXPIRED LIC ISSUED: 09/01/2003 LIC EXPIRES: 12/01/2017 AS OF NOVEMBER 20, 2020 AT 9:45:15 AM, DRIVER PRIVILEGE B640-693-68-210-0 IS VALID. PERSONAL INFORMATION IS PROTECTED PURSUANT TO THE DRIVER PRIVACY PROTECTION ACT. ENTRIES BELOW ARE A THREE YEAR RECORD. ORIGINAL ISSUE DATE: 03/01/2001 REAL ID COMPLIANT US CITIZEN BLOCKED PERSONAL INFORMATION BLOCKED FOR MAILING LIST PERSON HAS A DIGITAL IMAGE ELIGIBLE TO ELECT DRIVER SCHOOL.  DRIVER HAS MADE 2 ELECTIONS. LAST ELECTION WAS ON 06/01/2002. VIOLATIONS COMMITTED WHILE A CDL HOLDER OR IN A CMV VEHICLE ARE NOT ELIGIBLE FOR DRIVING SCHOOL ELECTION. COUNTY: BROWARD RESIDENTIAL ADDRESS: 7923 NW 18TH ST APT 203  MARGATE, FL  33063  COUNTY: BROWARD ISSUANCE HISTORY: LIC CLASS: CLASS E   ISSUE DATE: 09/01/2001   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 06/01/2002   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 06/01/2002   ISSUE TYPE: REPLACEMENT LIC CLASS: ID CARD   ISSUE DATE: 06/01/2002   ISSUE TYPE: DUPLICATE LIC CLASS: CLASS E   ISSUE DATE: 03/01/2004   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 06/01/2006   ISSUE TYPE: ADDRESS CHANGE LIC CLASS: CLASS E   ISSUE DATE: 12/01/2017   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 12/01/2019   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 06/01/2020   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 08/01/2020   ISSUE TYPE: CDR/CDT CLEARANCE EXAMS TAKEN: VISION               DATE TAKEN: 03/01/2022   COUNT: 1   STATUS: PASS ROAD SIGN            DATE TAKEN: 03/01/2022   COUNT: 9   STATUS: RECIPROCATED ROAD RULES           DATE TAKEN: 03/01/2022   COUNT: 3   STATUS: PASS DRIVING              DATE TAKEN: 09/01/2021   COUNT: 4   STATUS: PASS This report is generated for insurance purposes only and may not be used for any other purpose.  The use and dissemination of the report and information in it must comply with your iiX agreement and the  Fair Credit Reporting Act, the Driver's Privacy Protection Act, and any applicable state statute(s).  The data in the report from the applicable state agency or service bureau is provided through iiX "as is." \--- Customer-defined MVR scoring has been applied to this record.  Customer  is solely responsible for the application and use of the resulting score.\</Detail\>

                                    \<Violations\>

                                        \<Violation\>

                                            \<Type\>SUSP\</Type\>

                                            \<ViolationDate\>20210701\</ViolationDate\>

                                            \<CustomCode\>130110\</CustomCode\>

                                            \<CustomPoints\>3\</CustomPoints\>

                                            \<Detail\>FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 730115590 NOTICED PROVIDED: 06/01/2021 ADDED TO RECORD: 06/01/2021 SANCTION CODE: 7\</Detail\>

                                        \</Violation\>

                                        \<Violation\>

                                            \<Type\>REIN\</Type\>

                                            \<ConvictionDate\>20211201\</ConvictionDate\>

                                            \<CustomCode\>330130\</CustomCode\>

                                            \<CustomPoints\>-3\</CustomPoints\>

                                            \<Detail\>REINSTATED\</Detail\>

                                        \</Violation\>

                                        \<Violation\>

                                            \<Type\>SUSP\</Type\>

                                            \<ViolationDate\>20200401\</ViolationDate\>

                                            \<CustomCode\>130110\</CustomCode\>

                                            \<CustomPoints\>0\</CustomPoints\>

                                            \<Detail\>FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 730195358 NOTICED PROVIDED: 04/01/2020 ADDED TO RECORD: 04/01/2020 SANCTION CODE: 7\</Detail\>

                                        \</Violation\>

                                        \<Violation\>

                                            \<Type\>REIN\</Type\>

                                            \<ConvictionDate\>20200601\</ConvictionDate\>

                                            \<CustomCode\>330130\</CustomCode\>

                                            \<CustomPoints\>0\</CustomPoints\>

                                            \<Detail\>REINSTATED\</Detail\>

                                        \</Violation\>

                                        \<Violation\>

                                            \<Type\>SUSP\</Type\>

                                            \<ViolationDate\>20200801\</ViolationDate\>

                                            \<CustomCode\>130110\</CustomCode\>

                                            \<CustomPoints\>0\</CustomPoints\>

                                            \<Detail\>FR-REGISTRATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 830111729 NOTICED PROVIDED: 07/01/2020 ADDED TO RECORD: 07/01/2020 SANCTION CODE: 8\</Detail\>

                                        \</Violation\>

                                        \<Violation\>

                                            \<Type\>REIN\</Type\>

                                            \<ConvictionDate\>20200801\</ConvictionDate\>

                                            \<CustomCode\>330130\</CustomCode\>

                                            \<CustomPoints\>0\</CustomPoints\>

                                            \<Detail\>REINSTATED\</Detail\>

                                        \</Violation\>

                                        \<Violation\>

                                            \<Type\>VIOL\</Type\>

                                            \<ViolationDate\>20220201\</ViolationDate\>

                                            \<ConvictionDate\>20220501\</ConvictionDate\>

                                            \<StateAssignedPoints\>4\</StateAssignedPoints\>

                                            \<CustomCode\>424300\</CustomCode\>

                                            \<CustomPoints\>1\</CustomPoints\>

                                            \<Detail\>FAIL TO YIELD UNSIGNED INTERSECTION DISPOSITION WAS GUILTY COUNTY COURT CRASH INDICATED VIOLATION NUMBER: 5 CITATION NUMBER: A0LU14E COUNTY: BROWARD ADDED TO RECORD: 05/01/2022 DISPOSITION CODE: 513\</Detail\>

                                        \</Violation\>

                                        \<Violation\>

                                            \<Type\>VIOL\</Type\>

                                            \<ViolationDate\>20211201\</ViolationDate\>

                                            \<ConvictionDate\>20220201\</ConvictionDate\>

                                            \<StateAssignedPoints\>0\</StateAssignedPoints\>

                                            \<CustomCode\>536400\</CustomCode\>

                                            \<CustomPoints\>1\</CustomPoints\>

                                            \<Detail\>EXPIRED TAG \- 6 MOS OR LESS DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 6 CITATION NUMBER: AR9P4UE COUNTY: BROWARD STATE: FL ADDED TO RECORD: 02/01/2022 DISPOSITION CODE: 473\</Detail\>

                                        \</Violation\>

                                    \</Violations\>

                                \</Driver\>

                            \</MotorVehicleReport\>

                        \</MotorVehicleReports\>

                    \</Body\>

                    \<StatusCode\>200\</StatusCode\>

                \</IndividualMotorVehicleReport\>

                \<IndividualMotorVehicleReport\>

                    \<Header\>

                        \<Quoteback\>15446763-7f06-4452-b988-f77fb994a494\</Quoteback\>

                        \<TransactionId\>21e16889-3477-4eb6-8dd4-3e84e7782b02\</TransactionId\>

                    \</Header\>

                    \<Body\>

                        \<OrderNumber\>935983243\</OrderNumber\>

                        \<MotorVehicleReports\>

                            \<MotorVehicleReport\>

                                \<Status\>

                                    \<Code\>N\</Code\>

                                    \<Description\>NOT FOUND\</Description\>

                                \</Status\>

                                \<ViolationsType\>

                                    \<Code\>N\</Code\>

                                    \<Description\>Not Coded\</Description\>

                                \</ViolationsType\>

                                \<Driver\>

                                    \<DLNumber\>S420665834256\</DLNumber\>

                                    \<DLState\>FL\</DLState\>

                                    \<Detail\>OrderType : MvrIndicator \- \</Detail\>

                                \</Driver\>

                            \</MotorVehicleReport\>

                        \</MotorVehicleReports\>

                    \</Body\>

                    \<StatusCode\>200\</StatusCode\>

                \</IndividualMotorVehicleReport\>

                \<IndividualMotorVehicleReport\>

                    \<Header\>

                        \<Quoteback\>15446763-7f06-4452-b988-f77fb994a494\</Quoteback\>

                        \<TransactionId\>086e1269-53e0-4079-9b2d-81813b270ca5\</TransactionId\>

                    \</Header\>

                    \<Body\>

                        \<OrderNumber\>935983241\</OrderNumber\>

                        \<MotorVehicleReports\>

                            \<MotorVehicleReport\>

                                \<Status\>

                                    \<Code\>N\</Code\>

                                    \<Description\>NOT FOUND\</Description\>

                                \</Status\>

                                \<ViolationsType\>

                                    \<Code\>N\</Code\>

                                    \<Description\>Not Coded\</Description\>

                                \</ViolationsType\>

                                \<Driver\>

                                    \<DLNumber\>P420665934225\</DLNumber\>

                                    \<DLState\>FL\</DLState\>

                                    \<Detail\>OrderType : MvrIndicator \- \</Detail\>

                                \</Driver\>

                            \</MotorVehicleReport\>

                        \</MotorVehicleReports\>

                    \</Body\>

                    \<StatusCode\>200\</StatusCode\>

                \</IndividualMotorVehicleReport\>

                \<IndividualMotorVehicleReport\>

                    \<Header\>

                        \<Quoteback\>15446763-7f06-4452-b988-f77fb994a494\</Quoteback\>

                        \<TransactionId\>68fc41ef-5462-4709-8111-be4adcc0516e\</TransactionId\>

                    \</Header\>

                    \<Body\>

                        \<OrderNumber\>935983242\</OrderNumber\>

                        \<MotorVehicleReports\>

                            \<MotorVehicleReport\>

                                \<Status\>

                                    \<Code\>N\</Code\>

                                    \<Description\>NOT FOUND\</Description\>

                                \</Status\>

                                \<ViolationsType\>

                                    \<Code\>N\</Code\>

                                    \<Description\>Not Coded\</Description\>

                                \</ViolationsType\>

                                \<Driver\>

                                    \<DLNumber\>R420622534333\</DLNumber\>

                                    \<DLState\>FL\</DLState\>

                                    \<Detail\>OrderType : MvrIndicator \- \</Detail\>

                                \</Driver\>

                            \</MotorVehicleReport\>

                        \</MotorVehicleReports\>

                    \</Body\>

                    \<StatusCode\>200\</StatusCode\>

                \</IndividualMotorVehicleReport\>

                \<IndividualMotorVehicleReport\>

                    \<Header\>

                        \<Quoteback\>15446763-7f06-4452-b988-f77fb994a494\</Quoteback\>

                        \<TransactionId\>f2f8c5ef-672d-4713-87e6-c837bf6d05dc\</TransactionId\>

                    \</Header\>

                    \<Body\>

                        \<OrderNumber\>935983245\</OrderNumber\>

                        \<MotorVehicleReports\>

                            \<MotorVehicleReport\>

                                \<Status\>

                                    \<Code\>N\</Code\>

                                    \<Description\>NOT FOUND\</Description\>

                                \</Status\>

                                \<ViolationsType\>

                                    \<Code\>N\</Code\>

                                    \<Description\>Not Coded\</Description\>

                                \</ViolationsType\>

                                \<Driver\>

                                    \<DLNumber\>L420625834362\</DLNumber\>

                                    \<DLState\>FL\</DLState\>

                                    \<Detail\>OrderType : MvrIndicator \- \</Detail\>

                                \</Driver\>

                            \</MotorVehicleReport\>

                        \</MotorVehicleReports\>

                    \</Body\>

                    \<StatusCode\>200\</StatusCode\>

                \</IndividualMotorVehicleReport\>

                \<IndividualMotorVehicleReport\>

                    \<Header\>

                        \<Quoteback\>15446763-7f06-4452-b988-f77fb994a494\</Quoteback\>

                        \<TransactionId\>ce3a354d-8e89-48dc-9335-760697d46c2b\</TransactionId\>

                    \</Header\>

                    \<Body\>

                        \<OrderNumber\>935983246\</OrderNumber\>

                        \<MotorVehicleReports\>

                            \<MotorVehicleReport\>

                                \<Status\>

                                    \<Code\>N\</Code\>

                                    \<Description\>NOT FOUND\</Description\>

                                \</Status\>

                                \<ViolationsType\>

                                    \<Code\>N\</Code\>

                                    \<Description\>Not Coded\</Description\>

                                \</ViolationsType\>

                                \<Driver\>

                                    \<DLNumber\>T123654125803\</DLNumber\>

                                    \<DLState\>FL\</DLState\>

                                    \<Detail\>OrderType : MvrIndicator \- \</Detail\>

                                \</Driver\>

                            \</MotorVehicleReport\>

                        \</MotorVehicleReports\>

                    \</Body\>

                    \<StatusCode\>200\</StatusCode\>

                \</IndividualMotorVehicleReport\>

            \</AllMotorVehicleReports\>

            \<VinMasterReports\>

                \<VinMasterReport\>

                    \<Header\>

                        \<TransactionId\>887b879f-761c-4b0e-9146-a3df086bd3c0\</TransactionId\>

                        \<Quoteback\>15446763-7f06-4452-b988-f77fb994a494\</Quoteback\>

                    \</Header\>

                    \<Body\>

                        \<Body\>

                            \<RequestedVIN\>1G5CT18B5F8530675\</RequestedVIN\>

                            \<Message\>LPMP Symbols not available for model years before 1998.\</Message\>

                            \<VIN\>1G5CT18B\&amp;F\</VIN\>

                            \<ModelYear\>85\</ModelYear\>

                            \<ISOUse\>4223\</ISOUse\>

                            \<Restraint\>A\</Restraint\>

                            \<AntiLockBrakes\>N\</AntiLockBrakes\>

                            \<EngineCylinders\>6\</EngineCylinders\>

                            \<CombinedVSRSymbol\_OnePosition\>J\</CombinedVSRSymbol\_OnePosition\>

                            \<PriceNewSymbol\_27SymbolTable\_OnePosition\>J\</PriceNewSymbol\_27SymbolTable\_OnePosition\>

                            \<Make\>GMC\</Make\>

                            \<BasicModelName\>JIMMY S-15\</BasicModelName\>

                            \<BodyStyle\>UTIL 4X4\</BodyStyle\>

                            \<EngineSize\>173\</EngineSize\>

                            \<FourWheelDriveIndicator\>4\</FourWheelDriveIndicator\>

                            \<FullModelName\>JIMMY S-15\</FullModelName\>

                            \<NCICCode\>GMC\</NCICCode\>

                            \<CombinedVSRSymbol\_TwoPositions\>10\</CombinedVSRSymbol\_TwoPositions\>

                            \<PriceNewSymbol\_27SymbolTable\_TwoPositions\>10\</PriceNewSymbol\_27SymbolTable\_TwoPositions\>

                            \<VINChangeIndicatorDescription\>No Change to VIN\</VINChangeIndicatorDescription\>

                            \<RestraintDescription\>Driver \&amp; Front Passenger Active Restraints\</RestraintDescription\>

                            \<AntiLockBrakesDescription\>Anti-Lock Brakes are not available\</AntiLockBrakesDescription\>

                            \<EngineCylindersDescription\>Six-Cylinder Engine\</EngineCylindersDescription\>

                            \<EngineTypeDescription\>Other Type of Engine\</EngineTypeDescription\>

                            \<SymbolChangeIndicatorDescription\>No change to the Symbol fields\</SymbolChangeIndicatorDescription\>

                            \<FieldChangeIndicatorDescription\>Field not added to VINMASTER until model year 1995\</FieldChangeIndicatorDescription\>

                            \<MakeDescription\>GMC\</MakeDescription\>

                            \<CountrywidePerformanceDescription\>Standard Performance\</CountrywidePerformanceDescription\>

                            \<NonVSRPerformanceDescription\>Standard Performance\</NonVSRPerformanceDescription\>

                            \<BodyStyleDescription\>Utility Vehicle \- Four-Wheel Drive\</BodyStyleDescription\>

                            \<FourWheelDriveIndicatorDescription\>Vehicle is four-wheel drive\</FourWheelDriveIndicatorDescription\>

                            \<ElectronicStabilityControlDescription\>Field not added to VINMASTER until model year 1995\</ElectronicStabilityControlDescription\>

                            \<DaytimeRunningLightIndicatorDescription\>Field not added to VINMASTER until model year 1995\</DaytimeRunningLightIndicatorDescription\>

                            \<NCICCodeDescription\>GMC\</NCICCodeDescription\>

                            \<AntiTheftIndicatorDescription\>Field not added to VINMASTER until model year 1990\</AntiTheftIndicatorDescription\>

                            \<PriceNew\_Min\>10001.00\</PriceNew\_Min\>

                            \<PriceNew\_Max\>12500.99\</PriceNew\_Max\>

                            \<FullModelYear\>1985\</FullModelYear\>

                            \<RecordType\>S\</RecordType\>

                        \</Body\>

                        \<Body\>

                            \<RequestedVIN\>1GKER23788J291227\</RequestedVIN\>

                            \<Message\>Specify LPMPFiling value for LPMP Symbols.\</Message\>

                            \<VIN\>1GK\&amp;R237\&amp;8\</VIN\>

                            \<ModelYear\>08\</ModelYear\>

                            \<ISOUse\>4375\</ISOUse\>

                            \<EffectiveDate\>1010\</EffectiveDate\>

                            \<Restraint\>R\</Restraint\>

                            \<AntiLockBrakes\>S\</AntiLockBrakes\>

                            \<EngineCylinders\>6\</EngineCylinders\>

                            \<CombinedVSRSymbol\_OnePosition\>E\</CombinedVSRSymbol\_OnePosition\>

                            \<PriceNewSymbol\_27SymbolTable\_OnePosition\>N\</PriceNewSymbol\_27SymbolTable\_OnePosition\>

                            \<Make\>GMC\</Make\>

                            \<BasicModelName\>ACADIA\</BasicModelName\>

                            \<BodyStyle\>UTL4X24D\</BodyStyle\>

                            \<EngineSize\>3.6\</EngineSize\>

                            \<ElectronicStabilityControl\>S\</ElectronicStabilityControl\>

                            \<TonnageIndicator\>13\</TonnageIndicator\>

                            \<PayloadCapacity\>1678\</PayloadCapacity\>

                            \<FullModelName\>ACADIA SLT1\</FullModelName\>

                            \<DaytimeRunningLightIndicator\>S\</DaytimeRunningLightIndicator\>

                            \<NCICCode\>GMC\</NCICCode\>

                            \<CircularNumber\>1010\</CircularNumber\>

                            \<CombinedVSRSymbol\_TwoPositions\>12\</CombinedVSRSymbol\_TwoPositions\>

                            \<PriceNewSymbol\_27SymbolTable\_TwoPositions\>20\</PriceNewSymbol\_27SymbolTable\_TwoPositions\>

                            \<Wheelbase\>118.9\</Wheelbase\>

                            \<ClassCode\>93\</ClassCode\>

                            \<AntiTheftIndicator\>P\</AntiTheftIndicator\>

                            \<CurbWeight\>04722\</CurbWeight\>

                            \<GrossVehicleWeight\>06400\</GrossVehicleWeight\>

                            \<Height\>069.9\</Height\>

                            \<Horsepower\>0275\</Horsepower\>

                            \<VINChangeIndicatorDescription\>No Change to VIN\</VINChangeIndicatorDescription\>

                            \<RestraintDescription\>Driver \&amp; Front Passenger Front, Side \&amp; Head Airbags, Rear Passenger Head Airbags\</RestraintDescription\>

                            \<AntiLockBrakesDescription\>Anti-Lock Brakes are standard equipment\</AntiLockBrakesDescription\>

                            \<EngineCylindersDescription\>Six-Cylinder Engine\</EngineCylindersDescription\>

                            \<EngineTypeDescription\>Other Type of Engine\</EngineTypeDescription\>

                            \<SymbolChangeIndicatorDescription\>No change to the Symbol fields\</SymbolChangeIndicatorDescription\>

                            \<FieldChangeIndicatorDescription\>No change to Information fields\</FieldChangeIndicatorDescription\>

                            \<MakeDescription\>GMC\</MakeDescription\>

                            \<BodyStyleDescription\>Utility Vehicle \- Two-Wheel Drive 4-Door\</BodyStyleDescription\>

                            \<FourWheelDriveIndicatorDescription\>Vehicle is not four-wheel drive\</FourWheelDriveIndicatorDescription\>

                            \<VMPerformanceIndicatorDescription\>Standard\</VMPerformanceIndicatorDescription\>

                            \<ElectronicStabilityControlDescription\>Electronic Stability Control is standard equipment\</ElectronicStabilityControlDescription\>

                            \<TonnageIndicatorDescription\>3.25 tons (06001 to 06500 lbs)\</TonnageIndicatorDescription\>

                            \<DaytimeRunningLightIndicatorDescription\>Daytime Running Lights Standard Equipment\</DaytimeRunningLightIndicatorDescription\>

                            \<NCICCodeDescription\>GMC\</NCICCodeDescription\>

                            \<ClassCodeDescription\>Large Utility\</ClassCodeDescription\>

                            \<AntiTheftIndicatorDescription\>Passive Disabling\</AntiTheftIndicatorDescription\>

                            \<PriceNew\_Min\>33001.00\</PriceNew\_Min\>

                            \<PriceNew\_Max\>36000.99\</PriceNew\_Max\>

                            \<FullModelYear\>2008\</FullModelYear\>

                            \<RecordType\>S\</RecordType\>

                        \</Body\>

                        \<Body\>

                            \<RequestedVIN\>1HGCM56306A148752\</RequestedVIN\>

                            \<Message\>Specify LPMPFiling value for LPMP Symbols.\</Message\>

                            \<VIN\>1HGCM563\&amp;6\</VIN\>

                            \<ModelYear\>06\</ModelYear\>

                            \<ISOUse\>5503\</ISOUse\>

                            \<Restraint\>R\</Restraint\>

                            \<AntiLockBrakes\>S\</AntiLockBrakes\>

                            \<EngineCylinders\>4\</EngineCylinders\>

                            \<CombinedVSRSymbol\_OnePosition\>E\</CombinedVSRSymbol\_OnePosition\>

                            \<PriceNewSymbol\_27SymbolTable\_OnePosition\>G\</PriceNewSymbol\_27SymbolTable\_OnePosition\>

                            \<Make\>HOND\</Make\>

                            \<BasicModelName\>ACCORD\</BasicModelName\>

                            \<BodyStyle\>SEDAN 4D\</BodyStyle\>

                            \<EngineSize\>2.4\</EngineSize\>

                            \<ElectronicStabilityControl\>O\</ElectronicStabilityControl\>

                            \<TonnageIndicator\>00\</TonnageIndicator\>

                            \<PayloadCapacity\>0000\</PayloadCapacity\>

                            \<FullModelName\>ACCORD SE\</FullModelName\>

                            \<DaytimeRunningLightIndicator\>S\</DaytimeRunningLightIndicator\>

                            \<NCICCode\>HOND\</NCICCode\>

                            \<CircularNumber\>0512\</CircularNumber\>

                            \<CombinedVSRSymbol\_TwoPositions\>12\</CombinedVSRSymbol\_TwoPositions\>

                            \<PriceNewSymbol\_27SymbolTable\_TwoPositions\>14\</PriceNewSymbol\_27SymbolTable\_TwoPositions\>

                            \<Wheelbase\>107.9\</Wheelbase\>

                            \<ClassCode\>34\</ClassCode\>

                            \<AntiTheftIndicator\>P\</AntiTheftIndicator\>

                            \<CurbWeight\>03197\</CurbWeight\>

                            \<GrossVehicleWeight\>00000\</GrossVehicleWeight\>

                            \<Height\>057.2\</Height\>

                            \<Horsepower\>0166\</Horsepower\>

                            \<VINChangeIndicatorDescription\>No Change to VIN\</VINChangeIndicatorDescription\>

                            \<RestraintDescription\>Driver \&amp; Front Passenger Front, Side \&amp; Head Airbags, Rear Passenger Head Airbags\</RestraintDescription\>

                            \<AntiLockBrakesDescription\>Anti-Lock Brakes are standard equipment\</AntiLockBrakesDescription\>

                            \<EngineCylindersDescription\>Four-Cylinder Engine\</EngineCylindersDescription\>

                            \<EngineTypeDescription\>Other Type of Engine\</EngineTypeDescription\>

                            \<SymbolChangeIndicatorDescription\>No change to the Symbol fields\</SymbolChangeIndicatorDescription\>

                            \<FieldChangeIndicatorDescription\>No change to Information fields\</FieldChangeIndicatorDescription\>

                            \<MakeDescription\>HONDA\</MakeDescription\>

                            \<BodyStyleDescription\>4-Door Sedan\</BodyStyleDescription\>

                            \<FourWheelDriveIndicatorDescription\>Vehicle is not four-wheel drive\</FourWheelDriveIndicatorDescription\>

                            \<VMPerformanceIndicatorDescription\>Standard\</VMPerformanceIndicatorDescription\>

                            \<ElectronicStabilityControlDescription\>Electronic Stability Control is optional equipment\</ElectronicStabilityControlDescription\>

                            \<TonnageIndicatorDescription\>N/A\</TonnageIndicatorDescription\>

                            \<DaytimeRunningLightIndicatorDescription\>Daytime Running Lights Standard Equipment\</DaytimeRunningLightIndicatorDescription\>

                            \<NCICCodeDescription\>HONDA\</NCICCodeDescription\>

                            \<ClassCodeDescription\>Midsize 4-Door\</ClassCodeDescription\>

                            \<AntiTheftIndicatorDescription\>Passive Disabling\</AntiTheftIndicatorDescription\>

                            \<PriceNew\_Min\>20001.00\</PriceNew\_Min\>

                            \<PriceNew\_Max\>22000.99\</PriceNew\_Max\>

                            \<FullModelYear\>2006\</FullModelYear\>

                            \<RecordType\>S\</RecordType\>

                        \</Body\>

                        \<Body\>

                            \<RequestedVIN\>3GNFK16T9YG218125\</RequestedVIN\>

                            \<Message\>Specify LPMPFiling value for LPMP Symbols.\</Message\>

                            \<VIN\>3GN\&amp;K16T\&amp;Y\</VIN\>

                            \<ModelYear\>00\</ModelYear\>

                            \<ISOUse\>2452\</ISOUse\>

                            \<Restraint\>S\</Restraint\>

                            \<AntiLockBrakes\>S\</AntiLockBrakes\>

                            \<EngineCylinders\>8\</EngineCylinders\>

                            \<CombinedVSRSymbol\_OnePosition\>F\</CombinedVSRSymbol\_OnePosition\>

                            \<PriceNewSymbol\_27SymbolTable\_OnePosition\>P\</PriceNewSymbol\_27SymbolTable\_OnePosition\>

                            \<Make\>CHEV\</Make\>

                            \<BasicModelName\>SUBURBAN\</BasicModelName\>

                            \<BodyStyle\>UTL4X44D\</BodyStyle\>

                            \<EngineSize\>5.3\</EngineSize\>

                            \<FourWheelDriveIndicator\>4\</FourWheelDriveIndicator\>

                            \<ElectronicStabilityControl\>N\</ElectronicStabilityControl\>

                            \<TonnageIndicator\>15\</TonnageIndicator\>

                            \<PayloadCapacity\>2077\</PayloadCapacity\>

                            \<FullModelName\>SUBURBAN 1500 BASE/LS/LT\</FullModelName\>

                            \<DaytimeRunningLightIndicator\>S\</DaytimeRunningLightIndicator\>

                            \<NCICCode\>CHEV\</NCICCode\>

                            \<CircularNumber\>0001\</CircularNumber\>

                            \<CombinedVSRSymbol\_TwoPositions\>13\</CombinedVSRSymbol\_TwoPositions\>

                            \<PriceNewSymbol\_27SymbolTable\_TwoPositions\>21\</PriceNewSymbol\_27SymbolTable\_TwoPositions\>

                            \<Wheelbase\>130.0\</Wheelbase\>

                            \<ClassCode\>93\</ClassCode\>

                            \<AntiTheftIndicator\>P\</AntiTheftIndicator\>

                            \<CurbWeight\>05123\</CurbWeight\>

                            \<GrossVehicleWeight\>07200\</GrossVehicleWeight\>

                            \<Height\>073.3\</Height\>

                            \<Horsepower\>0285\</Horsepower\>

                            \<VINChangeIndicatorDescription\>No Change to VIN\</VINChangeIndicatorDescription\>

                            \<RestraintDescription\>Driver \&amp; Front Passenger Front \&amp; Side Airbags\</RestraintDescription\>

                            \<AntiLockBrakesDescription\>Anti-Lock Brakes are standard equipment\</AntiLockBrakesDescription\>

                            \<EngineCylindersDescription\>Eight-Cylinder Engine\</EngineCylindersDescription\>

                            \<EngineTypeDescription\>Other Type of Engine\</EngineTypeDescription\>

                            \<SymbolChangeIndicatorDescription\>No change to the Symbol fields\</SymbolChangeIndicatorDescription\>

                            \<FieldChangeIndicatorDescription\>No change to Information fields\</FieldChangeIndicatorDescription\>

                            \<MakeDescription\>CHEVROLET\</MakeDescription\>

                            \<CountrywidePerformanceDescription\>Standard Performance\</CountrywidePerformanceDescription\>

                            \<BodyStyleDescription\>Utility Vehicle \- Four-Wheel Drive 4-Door\</BodyStyleDescription\>

                            \<FourWheelDriveIndicatorDescription\>Vehicle is four-wheel drive\</FourWheelDriveIndicatorDescription\>

                            \<ElectronicStabilityControlDescription\>Electronic Stability Control is not available\</ElectronicStabilityControlDescription\>

                            \<TonnageIndicatorDescription\>3.75 tons (07001 to 07500 lbs)\</TonnageIndicatorDescription\>

                            \<DaytimeRunningLightIndicatorDescription\>Daytime Running Lights Standard Equipment\</DaytimeRunningLightIndicatorDescription\>

                            \<NCICCodeDescription\>CHEVROLET\</NCICCodeDescription\>

                            \<ClassCodeDescription\>Large Utility\</ClassCodeDescription\>

                            \<AntiTheftIndicatorDescription\>Passive Disabling\</AntiTheftIndicatorDescription\>

                            \<PriceNew\_Min\>36001.00\</PriceNew\_Min\>

                            \<PriceNew\_Max\>40000.99\</PriceNew\_Max\>

                            \<FullModelYear\>2000\</FullModelYear\>

                            \<RecordType\>S\</RecordType\>

                        \</Body\>

                    \</Body\>

                \</VinMasterReport\>

            \</VinMasterReports\>

            \<VesmReport\>

                \<VisResponse\>

                    \<ResponseHeader\>

                        \<TransactionId\>2f6994f5-6e3f-444e-8b21-5b25f41b06d7\</TransactionId\>

                        \<StatusCd\>200\</StatusCd\>

                        \<StatusDescription\>Success\</StatusDescription\>

                    \</ResponseHeader\>

                    \<ResponseBody\>

                        \<SmartScoreResult\>

                            \<Vehicles\>

                                \<Vehicle\>

                                    \<ResponseVin\>1G5CT18B5F8530675\</ResponseVin\>

                                    \<ResponseFirstName\>DOUGLAS\</ResponseFirstName\>

                                    \<ResponseLastName\>BONZHEIM\</ResponseLastName\>

                                    \<ResponseAddress\>

                                        \<Street\>7827 ADELAIDE LP\</Street\>

                                        \<City\>NEW PORT RICHEY\</City\>

                                        \<State\>FL\</State\>

                                        \<Country\>US\</Country\>

                                        \<PostalCd\>34655\</PostalCd\>

                                    \</ResponseAddress\>

                                    \<Make\>GMC\</Make\>

                                    \<Model\>S15\</Model\>

                                    \<Year\>1985\</Year\>

                                    \<EnrollmentStatus\>EN\</EnrollmentStatus\>

                                    \<EnrollmentDate\>2022-01-01 05:00:41.394\</EnrollmentDate\>

                                    \<ScoreStatus\>SU\</ScoreStatus\>

                                    \<ScoreType\>Recent\</ScoreType\>

                                    \<Score\>85\</Score\>

                                    \<ScoreStartDate\>2022-11-14 00:00:00.000\</ScoreStartDate\>

                                    \<ScoreEndDate\>2023-01-22 23:59:59.000\</ScoreEndDate\>

                                    \<ProductEnrollmentStatus\>EN\</ProductEnrollmentStatus\>

                                \</Vehicle\>

                                \<Vehicle\>

                                    \<ResponseVin\>3GNFK16T9YG218125\</ResponseVin\>

                                    \<ResponseFirstName\>DOUGLAS\</ResponseFirstName\>

                                    \<ResponseLastName\>BONZHEIM\</ResponseLastName\>

                                    \<ResponseAddress\>

                                        \<Street\>7827 ADELAIDE LP\</Street\>

                                        \<City\>NEW PORT RICHEY\</City\>

                                        \<State\>FL\</State\>

                                        \<Country\>US\</Country\>

                                        \<PostalCd\>34655\</PostalCd\>

                                    \</ResponseAddress\>

                                    \<Make\>CHEV\</Make\>

                                    \<Model\>SUBURBAN\</Model\>

                                    \<Year\>2000\</Year\>

                                    \<EnrollmentStatus\>EN\</EnrollmentStatus\>

                                    \<EnrollmentDate\>2022-01-01 05:00:41.394\</EnrollmentDate\>

                                    \<ScoreStatus\>SU\</ScoreStatus\>

                                    \<ScoreType\>Recent\</ScoreType\>

                                    \<Score\>100\</Score\>

                                    \<ScoreStartDate\>2022-11-21 00:00:00.000\</ScoreStartDate\>

                                    \<ScoreEndDate\>2023-01-29 23:59:59.000\</ScoreEndDate\>

                                    \<ProductEnrollmentStatus\>EN\</ProductEnrollmentStatus\>

                                \</Vehicle\>

                                \<Vehicle\>

                                    \<ResponseVin\>1GKER23788J291227\</ResponseVin\>

                                    \<ResponseFirstName\>DOUGLAS\</ResponseFirstName\>

                                    \<ResponseLastName\>BONZHEIM\</ResponseLastName\>

                                    \<ResponseAddress\>

                                        \<Street\>7827 ADELAIDE LP\</Street\>

                                        \<City\>NEW PORT RICHEY\</City\>

                                        \<State\>FL\</State\>

                                        \<Country\>US\</Country\>

                                        \<PostalCd\>34655\</PostalCd\>

                                    \</ResponseAddress\>

                                    \<Make\>GMC\</Make\>

                                    \<Model\>ACADIA\</Model\>

                                    \<Year\>2008\</Year\>

                                    \<EnrollmentStatus\>EN\</EnrollmentStatus\>

                                    \<EnrollmentDate\>2022-01-01 05:00:41.394\</EnrollmentDate\>

                                    \<ScoreStatus\>SU\</ScoreStatus\>

                                    \<ScoreType\>Recent\</ScoreType\>

                                    \<Score\>86\</Score\>

                                    \<ScoreStartDate\>2022-11-21 00:00:00.000\</ScoreStartDate\>

                                    \<ScoreEndDate\>2023-01-29 23:59:59.000\</ScoreEndDate\>

                                    \<ProductEnrollmentStatus\>EN\</ProductEnrollmentStatus\>

                                \</Vehicle\>

                            \</Vehicles\>

                        \</SmartScoreResult\>

                    \</ResponseBody\>

                \</VisResponse\>

            \</VesmReport\>

            \<MileageReport\>

                \<Header\>

                    \<TransactionId\>01376303-a4bb-4a96-b564-4700b44850fb\</TransactionId\>

                    \<Quoteback\>15446763-7f06-4452-b988-f77fb994a494\</Quoteback\>

                \</Header\>

                \<Body\>

                    \<StatusCode\>200\</StatusCode\>

                    \<MileageReports\>

                        \<MileageReport\>

                            \<Vin\>1GKER23788J291227\</Vin\>

                            \<EstimateAnnualMiles\>

                                \<Sources\>

                                    \<Source\>

                                        \<Name\>VeriskMileageModel\</Name\>

                                        \<Miles\>11080\</Miles\>

                                    \</Source\>

                                \</Sources\>

                            \</EstimateAnnualMiles\>

                        \</MileageReport\>

                        \<MileageReport\>

                            \<Vin\>1HGCM56306A148752\</Vin\>

                            \<EstimateAnnualMiles\>

                                \<Sources\>

                                    \<Source\>

                                        \<Name\>VeriskMileageModel\</Name\>

                                        \<Miles\>11059\</Miles\>

                                    \</Source\>

                                \</Sources\>

                            \</EstimateAnnualMiles\>

                        \</MileageReport\>

                        \<MileageReport\>

                            \<Vin\>3GNFK16T9YG218125\</Vin\>

                            \<EstimateAnnualMiles\>

                                \<Sources\>

                                    \<Source\>

                                        \<Name\>VeriskMileageModel\</Name\>

                                        \<Miles\>8218\</Miles\>

                                    \</Source\>

                                \</Sources\>

                            \</EstimateAnnualMiles\>

                        \</MileageReport\>

                        \<MileageReport\>

                            \<Vin\>1G5CT18B5F8530675\</Vin\>

                            \<EstimateAnnualMiles\>

                                \<Sources\>

                                    \<Source\>

                                        \<Name\>VeriskMileageModel\</Name\>

                                        \<Miles\>3743\</Miles\>

                                    \</Source\>

                                \</Sources\>

                            \</EstimateAnnualMiles\>

                        \</MileageReport\>

                    \</MileageReports\>

                \</Body\>

            \</MileageReport\>

            \<InflectionCBISReport\>

                \<Header\>

                    \<TransactionId\>39c99d0d-ba61-49fd-806d-318143a67659\</TransactionId\>

                    \<Quoteback\>15446763-7f06-4452-b988-f77fb994a494\</Quoteback\>

                \</Header\>

                \<Body\>

                    \<StatusCode\>200\</StatusCode\>

                    \<Status\>completed\</Status\>

                    \<Consumers\>

                        \<EquifaxUSConsumerCreditReport\>

                            \<EquifaxUSConsumerCreditReportElement\>

                                \<Identifier\>Individual Report 1\</Identifier\>

                                \<CustomerReferenceNumber\>39C99D0DBA6149FD806D\</CustomerReferenceNumber\>

                                \<CustomerNumber\>999ZZ61019\</CustomerNumber\>

                                \<ConsumerReferralCode\>181\</ConsumerReferralCode\>

                                \<MultipleReportIndicator\>F\</MultipleReportIndicator\>

                                \<ECOAInquiryType\>I\</ECOAInquiryType\>

                                \<HitCode\>

                                    \<Code\>2\</Code\>

                                    \<Description\>No-Hit\</Description\>

                                \</HitCode\>

                            \</EquifaxUSConsumerCreditReportElement\>

                        \</EquifaxUSConsumerCreditReport\>

                    \</Consumers\>

                    \<Links\>

                        \<Link\>

                            \<Identifier\>Individual Report 1\</Identifier\>

                            \<Type\>GET\</Type\>

                            \<Href\>/business/consumer-credit/v1/reports/credit-report/11477435-df45-cc70-9d11-0c62619144db\</Href\>

                        \</Link\>

                    \</Links\>

                \</Body\>

            \</InflectionCBISReport\>

            \<RiskAnalyzerReports\>

                \<RiskAnalyzerReport\>

                    \<Header\>

                        \<Quoteback\>15446763-7f06-4452-b988-f77fb994a494\</Quoteback\>

                        \<TransactionId\>adb819e9-a741-458c-97c6-6960ccdb1d3b\</TransactionId\>

                    \</Header\>

                    \<Body\>

                        \<Body\>

                            \<RequestedVin\>1G5CT18B5F8530675\</RequestedVin\>

                            \<Vehicle\>

                                \<VIN\>1G5CT18B\&amp;F\</VIN\>

                                \<ModelYear\>1985\</ModelYear\>

                                \<DistributionDate\>2212\</DistributionDate\>

                                \<Restraint\>A\</Restraint\>

                                \<AntiLockBrakes\>N\</AntiLockBrakes\>

                                \<EngineCylinders\>6\</EngineCylinders\>

                                \<Make\>GMC\</Make\>

                                \<BasicModelName\>JIMMY S-15\</BasicModelName\>

                                \<BodyStyle\>UTIL 4X4\</BodyStyle\>

                                \<EngineSize\>173\</EngineSize\>

                                \<FourWheelDriveIndicator\>4\</FourWheelDriveIndicator\>

                                \<PayloadCapacity\>0\</PayloadCapacity\>

                                \<FullModelName\>JIMMY S-15\</FullModelName\>

                                \<Wheelbase\>0\</Wheelbase\>

                                \<CurbWeight\>0\</CurbWeight\>

                                \<GrossVehicleWeight\>0\</GrossVehicleWeight\>

                                \<Height\>0\</Height\>

                                \<Horsepower\>0\</Horsepower\>

                                \<StateException\>TX\</StateException\>

                                \<NCICCode\>GMC\</NCICCode\>

                                \<Length\>0\</Length\>

                                \<Width\>0\</Width\>

                                \<BaseMSRP\>10001\</BaseMSRP\>

                                \<SpecialHandlingIndicator\>N\</SpecialHandlingIndicator\>

                                \<InterimIndicator\>N\</InterimIndicator\>

                                \<ReleaseDate\>2303\</ReleaseDate\>

                            \</Vehicle\>

                            \<PhysicalDamage\>

                                \<RiskAnalyzerCollisionIndicatedSymbol\>BC\</RiskAnalyzerCollisionIndicatedSymbol\>

                                \<RiskAnalyzerComprehensiveIndicatedSymbol\>AB\</RiskAnalyzerComprehensiveIndicatedSymbol\>

                                \<RiskAnalyzerCollisionIndicatedSymbolRelativity\>0.5992\</RiskAnalyzerCollisionIndicatedSymbolRelativity\>

                                \<RiskAnalyzerComprehensiveIndicatedSymbolRelativity\>0.4702\</RiskAnalyzerComprehensiveIndicatedSymbolRelativity\>

                                \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar1\>0.6375\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerCollisionRatingSymbolRelativity\>0.5992\</RiskAnalyzerCollisionRatingSymbolRelativity\>

                                \<RiskAnalyzerCollisionRatingSymbol\>BC\</RiskAnalyzerCollisionRatingSymbol\>

                                \<RiskAnalyzerComprehensiveRatingSymbolRelativity\>0.4702\</RiskAnalyzerComprehensiveRatingSymbolRelativity\>

                                \<RiskAnalyzerComprehensiveRatingSymbol\>AB\</RiskAnalyzerComprehensiveRatingSymbol\>

                                \<RiskAnalyzerComprehensiveNonGlassRatingSymbolRelativity\>0.4702\</RiskAnalyzerComprehensiveNonGlassRatingSymbolRelativity\>

                                \<RiskAnalyzerComprehensiveNonGlassRatingSymbol\>AB\</RiskAnalyzerComprehensiveNonGlassRatingSymbol\>

                                \<RiskAnalyzerCollisionIndicatedSymbolRelativityChar1\>0.7375\</RiskAnalyzerCollisionIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerComprehensiveIndicatedSymbolRelativityChar1\>0.6375\</RiskAnalyzerComprehensiveIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerCollisionIndicatedSymbolRelativityChar2\>0.8125\</RiskAnalyzerCollisionIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerComprehensiveIndicatedSymbolRelativityChar2\>0.7375\</RiskAnalyzerComprehensiveIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerCollisionCappingIndicator\>N\</RiskAnalyzerCollisionCappingIndicator\>

                                \<RiskAnalyzerComprehensiveCappingIndicator\>N\</RiskAnalyzerComprehensiveCappingIndicator\>

                                \<RiskAnalyzerComprehensiveNonGlassCappingIndicator\>N\</RiskAnalyzerComprehensiveNonGlassCappingIndicator\>

                                \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar2\>0.7375\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbol\>AB\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbol\>

                                \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativity\>0.4702\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativity\>

                            \</PhysicalDamage\>

                            \<Liability\>

                                \<RiskAnalyzerMedicalPaymentsIndicatedSymbol\>FB\</RiskAnalyzerMedicalPaymentsIndicatedSymbol\>

                                \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbol\>VB\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbol\>

                                \<RiskAnalyzerSingleLimitIndicatedSymbol\>JF\</RiskAnalyzerSingleLimitIndicatedSymbol\>

                                \<RiskAnalyzerBodilyInjuryIndicatedSymbolRelativity\>0.9263\</RiskAnalyzerBodilyInjuryIndicatedSymbolRelativity\>

                                \<RiskAnalyzerPropertyDamageIndicatedSymbolRelativity\>0.7922\</RiskAnalyzerPropertyDamageIndicatedSymbolRelativity\>

                                \<RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativity\>0.6638\</RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativity\>

                                \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativity\>0.885\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativity\>

                                \<RiskAnalyzerSingleLimitIndicatedSymbolRelativity\>0.8775\</RiskAnalyzerSingleLimitIndicatedSymbolRelativity\>

                                \<RiskAnalyzerBodilyInjuryRatingSymbolRelativity\>0.9263\</RiskAnalyzerBodilyInjuryRatingSymbolRelativity\>

                                \<RiskAnalyzerBodilyInjuryRatingSymbol\>JH\</RiskAnalyzerBodilyInjuryRatingSymbol\>

                                \<RiskAnalyzerPropertyDamageRatingSymbolRelativity\>0.7922\</RiskAnalyzerPropertyDamageRatingSymbolRelativity\>

                                \<RiskAnalyzerPropertyDamageRatingSymbol\>JC\</RiskAnalyzerPropertyDamageRatingSymbol\>

                                \<RiskAnalyzerMedicalPaymentsRatingSymbolRelativity\>0.6638\</RiskAnalyzerMedicalPaymentsRatingSymbolRelativity\>

                                \<RiskAnalyzerMedicalPaymentsRatingSymbol\>FB\</RiskAnalyzerMedicalPaymentsRatingSymbol\>

                                \<RiskAnalyzerPersonalInjuryProtectionRatingSymbolRelativity\>0.885\</RiskAnalyzerPersonalInjuryProtectionRatingSymbolRelativity\>

                                \<RiskAnalyzerPersonalInjuryProtectionRatingSymbol\>VB\</RiskAnalyzerPersonalInjuryProtectionRatingSymbol\>

                                \<RiskAnalyzerSingleLimitRatingSymbolRelativity\>0.8775\</RiskAnalyzerSingleLimitRatingSymbolRelativity\>

                                \<RiskAnalyzerSingleLimitRatingSymbol\>JF\</RiskAnalyzerSingleLimitRatingSymbol\>

                                \<RiskAnalyzerBodilyInjuryCappingIndicator\>N\</RiskAnalyzerBodilyInjuryCappingIndicator\>

                                \<RiskAnalyzerPropertyDamageCappingIndicator\>N\</RiskAnalyzerPropertyDamageCappingIndicator\>

                                \<RiskAnalyzerMedicalPaymentsCappingIndicator\>N\</RiskAnalyzerMedicalPaymentsCappingIndicator\>

                                \<RiskAnalyzerPersonalInjuryProtectionCappingIndicator\>N\</RiskAnalyzerPersonalInjuryProtectionCappingIndicator\>

                                \<RiskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar1\>0.975\</RiskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerPropertyDamageIndicatedSymbolRelativityChar1\>0.975\</RiskAnalyzerPropertyDamageIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar1\>0.9\</RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar1\>1.2\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerSingleLimitIndicatedSymbolRelativityChar1\>0.975\</RiskAnalyzerSingleLimitIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar2\>0.95\</RiskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerPropertyDamageIndicatedSymbolRelativityChar2\>0.8125\</RiskAnalyzerPropertyDamageIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar2\>0.7375\</RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar2\>0.7375\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerSingleLimitIndicatedSymbolRelativityChar2\>0.9\</RiskAnalyzerSingleLimitIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerBodilyInjuryIndicatedSymbol\>JH\</RiskAnalyzerBodilyInjuryIndicatedSymbol\>

                                \<RiskAnalyzerPropertyDamageIndicatedSymbol\>JC\</RiskAnalyzerPropertyDamageIndicatedSymbol\>

                                \<RiskAnalyzerSingleLimitCappingIndicator\>N\</RiskAnalyzerSingleLimitCappingIndicator\>

                            \</Liability\>

                        \</Body\>

                    \</Body\>

                \</RiskAnalyzerReport\>

                \<RiskAnalyzerReport\>

                    \<Header\>

                        \<Quoteback\>15446763-7f06-4452-b988-f77fb994a494\</Quoteback\>

                        \<TransactionId\>c036e717-6cb1-4f27-9d75-daa459aaf6d4\</TransactionId\>

                    \</Header\>

                    \<Body\>

                        \<Body\>

                            \<RequestedVin\>3GNFK16T9YG218125\</RequestedVin\>

                            \<Vehicle\>

                                \<VIN\>3GN\&amp;K16T\&amp;Y\</VIN\>

                                \<ModelYear\>2000\</ModelYear\>

                                \<DistributionDate\>2212\</DistributionDate\>

                                \<Restraint\>S\</Restraint\>

                                \<AntiLockBrakes\>S\</AntiLockBrakes\>

                                \<EngineCylinders\>8\</EngineCylinders\>

                                \<Make\>CHEV\</Make\>

                                \<BasicModelName\>SUBURBAN\</BasicModelName\>

                                \<BodyStyle\>UTL4X44D\</BodyStyle\>

                                \<EngineSize\>5.3\</EngineSize\>

                                \<FourWheelDriveIndicator\>4\</FourWheelDriveIndicator\>

                                \<ElectronicStabilityControl\>N\</ElectronicStabilityControl\>

                                \<TonnageIndicator\>15\</TonnageIndicator\>

                                \<PayloadCapacity\>2077\</PayloadCapacity\>

                                \<FullModelName\>SUBURBAN 1500 BASE/LS/LT\</FullModelName\>

                                \<DaytimeRunningLightIndicator\>S\</DaytimeRunningLightIndicator\>

                                \<Wheelbase\>130\</Wheelbase\>

                                \<ClassCode\>93\</ClassCode\>

                                \<AntiTheftIndicator\>P\</AntiTheftIndicator\>

                                \<CurbWeight\>5123\</CurbWeight\>

                                \<GrossVehicleWeight\>7200\</GrossVehicleWeight\>

                                \<Height\>73.3\</Height\>

                                \<Horsepower\>285\</Horsepower\>

                                \<StateException\>TX\</StateException\>

                                \<NCICCode\>CHEV\</NCICCode\>

                                \<Length\>0\</Length\>

                                \<Width\>0\</Width\>

                                \<BaseMSRP\>36001\</BaseMSRP\>

                                \<SpecialHandlingIndicator\>N\</SpecialHandlingIndicator\>

                                \<InterimIndicator\>N\</InterimIndicator\>

                                \<ReleaseDate\>2303\</ReleaseDate\>

                            \</Vehicle\>

                            \<PhysicalDamage\>

                                \<RiskAnalyzerCollisionIndicatedSymbol\>EJ\</RiskAnalyzerCollisionIndicatedSymbol\>

                                \<RiskAnalyzerComprehensiveIndicatedSymbol\>DG\</RiskAnalyzerComprehensiveIndicatedSymbol\>

                                \<RiskAnalyzerCollisionIndicatedSymbolRelativity\>0.8531\</RiskAnalyzerCollisionIndicatedSymbolRelativity\>

                                \<RiskAnalyzerComprehensiveIndicatedSymbolRelativity\>0.7863\</RiskAnalyzerComprehensiveIndicatedSymbolRelativity\>

                                \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar1\>0.85\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerCollisionRatingSymbolRelativity\>0.8531\</RiskAnalyzerCollisionRatingSymbolRelativity\>

                                \<RiskAnalyzerCollisionRatingSymbol\>EJ\</RiskAnalyzerCollisionRatingSymbol\>

                                \<RiskAnalyzerComprehensiveRatingSymbolRelativity\>0.7863\</RiskAnalyzerComprehensiveRatingSymbolRelativity\>

                                \<RiskAnalyzerComprehensiveRatingSymbol\>DG\</RiskAnalyzerComprehensiveRatingSymbol\>

                                \<RiskAnalyzerComprehensiveNonGlassRatingSymbolRelativity\>0.7863\</RiskAnalyzerComprehensiveNonGlassRatingSymbolRelativity\>

                                \<RiskAnalyzerComprehensiveNonGlassRatingSymbol\>DG\</RiskAnalyzerComprehensiveNonGlassRatingSymbol\>

                                \<RiskAnalyzerCollisionIndicatedSymbolRelativityChar1\>0.875\</RiskAnalyzerCollisionIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerComprehensiveIndicatedSymbolRelativityChar1\>0.85\</RiskAnalyzerComprehensiveIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerCollisionIndicatedSymbolRelativityChar2\>0.975\</RiskAnalyzerCollisionIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerComprehensiveIndicatedSymbolRelativityChar2\>0.925\</RiskAnalyzerComprehensiveIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerCollisionCappingIndicator\>N\</RiskAnalyzerCollisionCappingIndicator\>

                                \<RiskAnalyzerComprehensiveCappingIndicator\>N\</RiskAnalyzerComprehensiveCappingIndicator\>

                                \<RiskAnalyzerComprehensiveNonGlassCappingIndicator\>N\</RiskAnalyzerComprehensiveNonGlassCappingIndicator\>

                                \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar2\>0.925\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbol\>DG\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbol\>

                                \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativity\>0.7863\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativity\>

                            \</PhysicalDamage\>

                            \<Liability\>

                                \<RiskAnalyzerMedicalPaymentsIndicatedSymbol\>FE\</RiskAnalyzerMedicalPaymentsIndicatedSymbol\>

                                \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbol\>EH\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbol\>

                                \<RiskAnalyzerSingleLimitIndicatedSymbol\>MK\</RiskAnalyzerSingleLimitIndicatedSymbol\>

                                \<RiskAnalyzerBodilyInjuryIndicatedSymbolRelativity\>0.9738\</RiskAnalyzerBodilyInjuryIndicatedSymbolRelativity\>

                                \<RiskAnalyzerPropertyDamageIndicatedSymbolRelativity\>1.1288\</RiskAnalyzerPropertyDamageIndicatedSymbolRelativity\>

                                \<RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativity\>0.7875\</RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativity\>

                                \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativity\>0.8313\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativity\>

                                \<RiskAnalyzerSingleLimitIndicatedSymbolRelativity\>1.05\</RiskAnalyzerSingleLimitIndicatedSymbolRelativity\>

                                \<RiskAnalyzerBodilyInjuryRatingSymbolRelativity\>0.9738\</RiskAnalyzerBodilyInjuryRatingSymbolRelativity\>

                                \<RiskAnalyzerBodilyInjuryRatingSymbol\>LH\</RiskAnalyzerBodilyInjuryRatingSymbol\>

                                \<RiskAnalyzerPropertyDamageRatingSymbolRelativity\>1.1288\</RiskAnalyzerPropertyDamageRatingSymbolRelativity\>

                                \<RiskAnalyzerPropertyDamageRatingSymbol\>MN\</RiskAnalyzerPropertyDamageRatingSymbol\>

                                \<RiskAnalyzerMedicalPaymentsRatingSymbolRelativity\>0.7875\</RiskAnalyzerMedicalPaymentsRatingSymbolRelativity\>

                                \<RiskAnalyzerMedicalPaymentsRatingSymbol\>FE\</RiskAnalyzerMedicalPaymentsRatingSymbol\>

                                \<RiskAnalyzerPersonalInjuryProtectionRatingSymbolRelativity\>0.8313\</RiskAnalyzerPersonalInjuryProtectionRatingSymbolRelativity\>

                                \<RiskAnalyzerPersonalInjuryProtectionRatingSymbol\>EH\</RiskAnalyzerPersonalInjuryProtectionRatingSymbol\>

                                \<RiskAnalyzerSingleLimitRatingSymbolRelativity\>1.05\</RiskAnalyzerSingleLimitRatingSymbolRelativity\>

                                \<RiskAnalyzerSingleLimitRatingSymbol\>MK\</RiskAnalyzerSingleLimitRatingSymbol\>

                                \<RiskAnalyzerBodilyInjuryCappingIndicator\>N\</RiskAnalyzerBodilyInjuryCappingIndicator\>

                                \<RiskAnalyzerPropertyDamageCappingIndicator\>N\</RiskAnalyzerPropertyDamageCappingIndicator\>

                                \<RiskAnalyzerMedicalPaymentsCappingIndicator\>N\</RiskAnalyzerMedicalPaymentsCappingIndicator\>

                                \<RiskAnalyzerPersonalInjuryProtectionCappingIndicator\>N\</RiskAnalyzerPersonalInjuryProtectionCappingIndicator\>

                                \<RiskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar1\>1.025\</RiskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerPropertyDamageIndicatedSymbolRelativityChar1\>1.05\</RiskAnalyzerPropertyDamageIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar1\>0.9\</RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar1\>0.875\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerSingleLimitIndicatedSymbolRelativityChar1\>1.05\</RiskAnalyzerSingleLimitIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar2\>0.95\</RiskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerPropertyDamageIndicatedSymbolRelativityChar2\>1.075\</RiskAnalyzerPropertyDamageIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar2\>0.875\</RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar2\>0.95\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerSingleLimitIndicatedSymbolRelativityChar2\>1\</RiskAnalyzerSingleLimitIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerBodilyInjuryIndicatedSymbol\>LH\</RiskAnalyzerBodilyInjuryIndicatedSymbol\>

                                \<RiskAnalyzerPropertyDamageIndicatedSymbol\>MN\</RiskAnalyzerPropertyDamageIndicatedSymbol\>

                                \<RiskAnalyzerSingleLimitCappingIndicator\>N\</RiskAnalyzerSingleLimitCappingIndicator\>

                            \</Liability\>

                        \</Body\>

                    \</Body\>

                \</RiskAnalyzerReport\>

                \<RiskAnalyzerReport\>

                    \<Header\>

                        \<Quoteback\>15446763-7f06-4452-b988-f77fb994a494\</Quoteback\>

                        \<TransactionId\>6b9bcd0e-c019-4219-b791-e7132315a397\</TransactionId\>

                    \</Header\>

                    \<Body\>

                        \<Body\>

                            \<RequestedVin\>1HGCM56306A148752\</RequestedVin\>

                            \<Vehicle\>

                                \<VIN\>1HGCM563\&amp;6\</VIN\>

                                \<ModelYear\>2006\</ModelYear\>

                                \<DistributionDate\>2212\</DistributionDate\>

                                \<Restraint\>R\</Restraint\>

                                \<AntiLockBrakes\>S\</AntiLockBrakes\>

                                \<EngineCylinders\>4\</EngineCylinders\>

                                \<Make\>HOND\</Make\>

                                \<BasicModelName\>ACCORD\</BasicModelName\>

                                \<BodyStyle\>SEDAN 4D\</BodyStyle\>

                                \<EngineSize\>2.4\</EngineSize\>

                                \<ElectronicStabilityControl\>O\</ElectronicStabilityControl\>

                                \<TonnageIndicator\>00\</TonnageIndicator\>

                                \<PayloadCapacity\>0\</PayloadCapacity\>

                                \<FullModelName\>ACCORD SE\</FullModelName\>

                                \<DaytimeRunningLightIndicator\>S\</DaytimeRunningLightIndicator\>

                                \<Wheelbase\>107.9\</Wheelbase\>

                                \<ClassCode\>34\</ClassCode\>

                                \<AntiTheftIndicator\>P\</AntiTheftIndicator\>

                                \<CurbWeight\>3197\</CurbWeight\>

                                \<GrossVehicleWeight\>0\</GrossVehicleWeight\>

                                \<Height\>57.2\</Height\>

                                \<Horsepower\>166\</Horsepower\>

                                \<NCICCode\>HOND\</NCICCode\>

                                \<Chassis\>U\</Chassis\>

                                \<Length\>0\</Length\>

                                \<Width\>0\</Width\>

                                \<BaseMSRP\>20001\</BaseMSRP\>

                                \<SpecialHandlingIndicator\>N\</SpecialHandlingIndicator\>

                                \<InterimIndicator\>N\</InterimIndicator\>

                                \<SpecialInfoSelector\>M\</SpecialInfoSelector\>

                                \<ModelSeriesInfo\>CURB\</ModelSeriesInfo\>

                                \<ReleaseDate\>2303\</ReleaseDate\>

                            \</Vehicle\>

                            \<PhysicalDamage\>

                                \<RiskAnalyzerCollisionIndicatedSymbol\>DM\</RiskAnalyzerCollisionIndicatedSymbol\>

                                \<RiskAnalyzerComprehensiveIndicatedSymbol\>CE\</RiskAnalyzerComprehensiveIndicatedSymbol\>

                                \<RiskAnalyzerCollisionIndicatedSymbolRelativity\>0.8925\</RiskAnalyzerCollisionIndicatedSymbolRelativity\>

                                \<RiskAnalyzerComprehensiveIndicatedSymbolRelativity\>0.7109\</RiskAnalyzerComprehensiveIndicatedSymbolRelativity\>

                                \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar1\>0.8125\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerCollisionRatingSymbolRelativity\>0.8925\</RiskAnalyzerCollisionRatingSymbolRelativity\>

                                \<RiskAnalyzerCollisionRatingSymbol\>DM\</RiskAnalyzerCollisionRatingSymbol\>

                                \<RiskAnalyzerComprehensiveRatingSymbolRelativity\>0.7109\</RiskAnalyzerComprehensiveRatingSymbolRelativity\>

                                \<RiskAnalyzerComprehensiveRatingSymbol\>CE\</RiskAnalyzerComprehensiveRatingSymbol\>

                                \<RiskAnalyzerComprehensiveNonGlassRatingSymbolRelativity\>0.7313\</RiskAnalyzerComprehensiveNonGlassRatingSymbolRelativity\>

                                \<RiskAnalyzerComprehensiveNonGlassRatingSymbol\>CF\</RiskAnalyzerComprehensiveNonGlassRatingSymbol\>

                                \<RiskAnalyzerCollisionIndicatedSymbolRelativityChar1\>0.85\</RiskAnalyzerCollisionIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerComprehensiveIndicatedSymbolRelativityChar1\>0.8125\</RiskAnalyzerComprehensiveIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerCollisionIndicatedSymbolRelativityChar2\>1.05\</RiskAnalyzerCollisionIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerComprehensiveIndicatedSymbolRelativityChar2\>0.875\</RiskAnalyzerComprehensiveIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerCollisionCappingIndicator\>N\</RiskAnalyzerCollisionCappingIndicator\>

                                \<RiskAnalyzerComprehensiveCappingIndicator\>N\</RiskAnalyzerComprehensiveCappingIndicator\>

                                \<RiskAnalyzerComprehensiveNonGlassCappingIndicator\>N\</RiskAnalyzerComprehensiveNonGlassCappingIndicator\>

                                \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar2\>0.9\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbol\>CF\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbol\>

                                \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativity\>0.7313\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativity\>

                            \</PhysicalDamage\>

                            \<Liability\>

                                \<RiskAnalyzerMedicalPaymentsIndicatedSymbol\>NR\</RiskAnalyzerMedicalPaymentsIndicatedSymbol\>

                                \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbol\>MM\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbol\>

                                \<RiskAnalyzerSingleLimitIndicatedSymbol\>ML\</RiskAnalyzerSingleLimitIndicatedSymbol\>

                                \<RiskAnalyzerBodilyInjuryIndicatedSymbolRelativity\>1.0763\</RiskAnalyzerBodilyInjuryIndicatedSymbolRelativity\>

                                \<RiskAnalyzerPropertyDamageIndicatedSymbolRelativity\>1.05\</RiskAnalyzerPropertyDamageIndicatedSymbolRelativity\>

                                \<RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativity\>1.2094\</RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativity\>

                                \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativity\>1.1025\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativity\>

                                \<RiskAnalyzerSingleLimitIndicatedSymbolRelativity\>1.0763\</RiskAnalyzerSingleLimitIndicatedSymbolRelativity\>

                                \<RiskAnalyzerBodilyInjuryRatingSymbolRelativity\>1.0763\</RiskAnalyzerBodilyInjuryRatingSymbolRelativity\>

                                \<RiskAnalyzerBodilyInjuryRatingSymbol\>ML\</RiskAnalyzerBodilyInjuryRatingSymbol\>

                                \<RiskAnalyzerPropertyDamageRatingSymbolRelativity\>1.05\</RiskAnalyzerPropertyDamageRatingSymbolRelativity\>

                                \<RiskAnalyzerPropertyDamageRatingSymbol\>MK\</RiskAnalyzerPropertyDamageRatingSymbol\>

                                \<RiskAnalyzerMedicalPaymentsRatingSymbolRelativity\>1.2094\</RiskAnalyzerMedicalPaymentsRatingSymbolRelativity\>

                                \<RiskAnalyzerMedicalPaymentsRatingSymbol\>NR\</RiskAnalyzerMedicalPaymentsRatingSymbol\>

                                \<RiskAnalyzerPersonalInjuryProtectionRatingSymbolRelativity\>1.1025\</RiskAnalyzerPersonalInjuryProtectionRatingSymbolRelativity\>

                                \<RiskAnalyzerPersonalInjuryProtectionRatingSymbol\>MM\</RiskAnalyzerPersonalInjuryProtectionRatingSymbol\>

                                \<RiskAnalyzerSingleLimitRatingSymbolRelativity\>1.0763\</RiskAnalyzerSingleLimitRatingSymbolRelativity\>

                                \<RiskAnalyzerSingleLimitRatingSymbol\>ML\</RiskAnalyzerSingleLimitRatingSymbol\>

                                \<RiskAnalyzerBodilyInjuryCappingIndicator\>N\</RiskAnalyzerBodilyInjuryCappingIndicator\>

                                \<RiskAnalyzerPropertyDamageCappingIndicator\>N\</RiskAnalyzerPropertyDamageCappingIndicator\>

                                \<RiskAnalyzerMedicalPaymentsCappingIndicator\>N\</RiskAnalyzerMedicalPaymentsCappingIndicator\>

                                \<RiskAnalyzerPersonalInjuryProtectionCappingIndicator\>N\</RiskAnalyzerPersonalInjuryProtectionCappingIndicator\>

                                \<RiskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar1\>1.05\</RiskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerPropertyDamageIndicatedSymbolRelativityChar1\>1.05\</RiskAnalyzerPropertyDamageIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar1\>1.075\</RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar1\>1.05\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerSingleLimitIndicatedSymbolRelativityChar1\>1.05\</RiskAnalyzerSingleLimitIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar2\>1.025\</RiskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerPropertyDamageIndicatedSymbolRelativityChar2\>1\</RiskAnalyzerPropertyDamageIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar2\>1.125\</RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar2\>1.05\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerSingleLimitIndicatedSymbolRelativityChar2\>1.025\</RiskAnalyzerSingleLimitIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerBodilyInjuryIndicatedSymbol\>ML\</RiskAnalyzerBodilyInjuryIndicatedSymbol\>

                                \<RiskAnalyzerPropertyDamageIndicatedSymbol\>MK\</RiskAnalyzerPropertyDamageIndicatedSymbol\>

                                \<RiskAnalyzerSingleLimitCappingIndicator\>N\</RiskAnalyzerSingleLimitCappingIndicator\>

                            \</Liability\>

                        \</Body\>

                    \</Body\>

                \</RiskAnalyzerReport\>

                \<RiskAnalyzerReport\>

                    \<Header\>

                        \<Quoteback\>15446763-7f06-4452-b988-f77fb994a494\</Quoteback\>

                        \<TransactionId\>2c16f3be-6fa0-4f94-8971-21eff907c9b6\</TransactionId\>

                    \</Header\>

                    \<Body\>

                        \<Body\>

                            \<RequestedVin\>1GKER23788J291227\</RequestedVin\>

                            \<Vehicle\>

                                \<VIN\>1GK\&amp;R237\&amp;8\</VIN\>

                                \<ModelYear\>2008\</ModelYear\>

                                \<DistributionDate\>2212\</DistributionDate\>

                                \<Restraint\>R\</Restraint\>

                                \<AntiLockBrakes\>S\</AntiLockBrakes\>

                                \<EngineCylinders\>6\</EngineCylinders\>

                                \<Make\>GMC\</Make\>

                                \<BasicModelName\>ACADIA\</BasicModelName\>

                                \<BodyStyle\>UTL4X24D\</BodyStyle\>

                                \<EngineSize\>3.6\</EngineSize\>

                                \<ElectronicStabilityControl\>S\</ElectronicStabilityControl\>

                                \<TonnageIndicator\>13\</TonnageIndicator\>

                                \<PayloadCapacity\>1678\</PayloadCapacity\>

                                \<FullModelName\>ACADIA SLT1\</FullModelName\>

                                \<DaytimeRunningLightIndicator\>S\</DaytimeRunningLightIndicator\>

                                \<Wheelbase\>118.9\</Wheelbase\>

                                \<ClassCode\>93\</ClassCode\>

                                \<AntiTheftIndicator\>P\</AntiTheftIndicator\>

                                \<CurbWeight\>4722\</CurbWeight\>

                                \<GrossVehicleWeight\>6400\</GrossVehicleWeight\>

                                \<Height\>69.9\</Height\>

                                \<Horsepower\>275\</Horsepower\>

                                \<NCICCode\>GMC\</NCICCode\>

                                \<Chassis\>U\</Chassis\>

                                \<Length\>200.7\</Length\>

                                \<Width\>78.2\</Width\>

                                \<BaseMSRP\>34270\</BaseMSRP\>

                                \<SpecialHandlingIndicator\>N\</SpecialHandlingIndicator\>

                                \<InterimIndicator\>N\</InterimIndicator\>

                                \<ReleaseDate\>2303\</ReleaseDate\>

                            \</Vehicle\>

                            \<PhysicalDamage\>

                                \<RiskAnalyzerCollisionIndicatedSymbol\>DJ\</RiskAnalyzerCollisionIndicatedSymbol\>

                                \<RiskAnalyzerComprehensiveIndicatedSymbol\>CM\</RiskAnalyzerComprehensiveIndicatedSymbol\>

                                \<RiskAnalyzerCollisionIndicatedSymbolRelativity\>0.8288\</RiskAnalyzerCollisionIndicatedSymbolRelativity\>

                                \<RiskAnalyzerComprehensiveIndicatedSymbolRelativity\>0.8531\</RiskAnalyzerComprehensiveIndicatedSymbolRelativity\>

                                \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar1\>0.8125\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerCollisionRatingSymbolRelativity\>0.8288\</RiskAnalyzerCollisionRatingSymbolRelativity\>

                                \<RiskAnalyzerCollisionRatingSymbol\>DJ\</RiskAnalyzerCollisionRatingSymbol\>

                                \<RiskAnalyzerComprehensiveRatingSymbolRelativity\>0.8531\</RiskAnalyzerComprehensiveRatingSymbolRelativity\>

                                \<RiskAnalyzerComprehensiveRatingSymbol\>CM\</RiskAnalyzerComprehensiveRatingSymbol\>

                                \<RiskAnalyzerComprehensiveNonGlassRatingSymbolRelativity\>0.8734\</RiskAnalyzerComprehensiveNonGlassRatingSymbolRelativity\>

                                \<RiskAnalyzerComprehensiveNonGlassRatingSymbol\>CN\</RiskAnalyzerComprehensiveNonGlassRatingSymbol\>

                                \<RiskAnalyzerCollisionIndicatedSymbolRelativityChar1\>0.85\</RiskAnalyzerCollisionIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerComprehensiveIndicatedSymbolRelativityChar1\>0.8125\</RiskAnalyzerComprehensiveIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerCollisionIndicatedSymbolRelativityChar2\>0.975\</RiskAnalyzerCollisionIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerComprehensiveIndicatedSymbolRelativityChar2\>1.05\</RiskAnalyzerComprehensiveIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerCollisionCappingIndicator\>N\</RiskAnalyzerCollisionCappingIndicator\>

                                \<RiskAnalyzerComprehensiveCappingIndicator\>N\</RiskAnalyzerComprehensiveCappingIndicator\>

                                \<RiskAnalyzerComprehensiveNonGlassCappingIndicator\>N\</RiskAnalyzerComprehensiveNonGlassCappingIndicator\>

                                \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar2\>1.075\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbol\>CN\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbol\>

                                \<RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativity\>0.8734\</RiskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativity\>

                            \</PhysicalDamage\>

                            \<Liability\>

                                \<RiskAnalyzerMedicalPaymentsIndicatedSymbol\>GE\</RiskAnalyzerMedicalPaymentsIndicatedSymbol\>

                                \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbol\>FK\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbol\>

                                \<RiskAnalyzerSingleLimitIndicatedSymbol\>KK\</RiskAnalyzerSingleLimitIndicatedSymbol\>

                                \<RiskAnalyzerBodilyInjuryIndicatedSymbolRelativity\>1.025\</RiskAnalyzerBodilyInjuryIndicatedSymbolRelativity\>

                                \<RiskAnalyzerPropertyDamageIndicatedSymbolRelativity\>1.025\</RiskAnalyzerPropertyDamageIndicatedSymbolRelativity\>

                                \<RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativity\>0.8094\</RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativity\>

                                \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativity\>0.9\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativity\>

                                \<RiskAnalyzerSingleLimitIndicatedSymbolRelativity\>1\</RiskAnalyzerSingleLimitIndicatedSymbolRelativity\>

                                \<RiskAnalyzerBodilyInjuryRatingSymbolRelativity\>1.025\</RiskAnalyzerBodilyInjuryRatingSymbolRelativity\>

                                \<RiskAnalyzerBodilyInjuryRatingSymbol\>KL\</RiskAnalyzerBodilyInjuryRatingSymbol\>

                                \<RiskAnalyzerPropertyDamageRatingSymbolRelativity\>1.025\</RiskAnalyzerPropertyDamageRatingSymbolRelativity\>

                                \<RiskAnalyzerPropertyDamageRatingSymbol\>LK\</RiskAnalyzerPropertyDamageRatingSymbol\>

                                \<RiskAnalyzerMedicalPaymentsRatingSymbolRelativity\>0.8094\</RiskAnalyzerMedicalPaymentsRatingSymbolRelativity\>

                                \<RiskAnalyzerMedicalPaymentsRatingSymbol\>GE\</RiskAnalyzerMedicalPaymentsRatingSymbol\>

                                \<RiskAnalyzerPersonalInjuryProtectionRatingSymbolRelativity\>0.9\</RiskAnalyzerPersonalInjuryProtectionRatingSymbolRelativity\>

                                \<RiskAnalyzerPersonalInjuryProtectionRatingSymbol\>FK\</RiskAnalyzerPersonalInjuryProtectionRatingSymbol\>

                                \<RiskAnalyzerSingleLimitRatingSymbolRelativity\>1\</RiskAnalyzerSingleLimitRatingSymbolRelativity\>

                                \<RiskAnalyzerSingleLimitRatingSymbol\>KK\</RiskAnalyzerSingleLimitRatingSymbol\>

                                \<RiskAnalyzerBodilyInjuryCappingIndicator\>N\</RiskAnalyzerBodilyInjuryCappingIndicator\>

                                \<RiskAnalyzerPropertyDamageCappingIndicator\>N\</RiskAnalyzerPropertyDamageCappingIndicator\>

                                \<RiskAnalyzerMedicalPaymentsCappingIndicator\>N\</RiskAnalyzerMedicalPaymentsCappingIndicator\>

                                \<RiskAnalyzerPersonalInjuryProtectionCappingIndicator\>N\</RiskAnalyzerPersonalInjuryProtectionCappingIndicator\>

                                \<RiskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar1\>1\</RiskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerPropertyDamageIndicatedSymbolRelativityChar1\>1.025\</RiskAnalyzerPropertyDamageIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar1\>0.925\</RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar1\>0.9\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerSingleLimitIndicatedSymbolRelativityChar1\>1\</RiskAnalyzerSingleLimitIndicatedSymbolRelativityChar1\>

                                \<RiskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar2\>1.025\</RiskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerPropertyDamageIndicatedSymbolRelativityChar2\>1\</RiskAnalyzerPropertyDamageIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar2\>0.875\</RiskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar2\>1\</RiskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerSingleLimitIndicatedSymbolRelativityChar2\>1\</RiskAnalyzerSingleLimitIndicatedSymbolRelativityChar2\>

                                \<RiskAnalyzerBodilyInjuryIndicatedSymbol\>KL\</RiskAnalyzerBodilyInjuryIndicatedSymbol\>

                                \<RiskAnalyzerPropertyDamageIndicatedSymbol\>LK\</RiskAnalyzerPropertyDamageIndicatedSymbol\>

                                \<RiskAnalyzerSingleLimitCappingIndicator\>N\</RiskAnalyzerSingleLimitCappingIndicator\>

                            \</Liability\>

                        \</Body\>

                    \</Body\>

                \</RiskAnalyzerReport\>

            \</RiskAnalyzerReports\>

        \</DataSources\>

    \</Body\>

\</Response\>

**Failure Response**

\<UnsuccessfulResponseModel

    xmlns:xsd="http://www.w3.org/2001/XMLSchema"

    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\>

    \<TransactionId\>94c0ebde-2da8-4627-a13a-b6bc9a5fbfe9\</TransactionId\>

    \<StatusCode\>403\</StatusCode\>

    \<Errors\>

        \<string\>Access Denied\</string\>

    \</Errors\>

\</UnsuccessfulResponseModel\>

