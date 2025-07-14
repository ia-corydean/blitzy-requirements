**Sample Request**

{  
    "header": {  
        "authorization": {  
            "orgId": "111111",  
            "shipId": "111111"  
        },  
        "quoteback": "LSP-Sample request"  
    },  
    "body": {  
        "drivers": \[  
            {  
                "givenName": "YUKI",  
                "surname": "BONZHEIM",  
                "dob": "19900311"  
            }  
        \],  
        "addresses": \[  
            {  
                "hasApplicantMovedRecently": "N",  
                "addressType": "Current",  
                "street1": "7827 ADELAIDE LP",  
                "city": "NEW PORT RICHEY",  
                "stateCode": "FL",  
                "zip": "34655"  
            }  
        \]  
    }  
}

}

**Response Codes**

* 200 (Success):  Upon successful call, the service will return a 200 response along with the data requested. No hits will return an empty body with http status 200\.  
* 400 (Bad Request): There was a problem with the formatted request to the service.   
* 401 (Unauthorized): The access\_token you provided has expired and is no longer valid. Please retrieve a new one from the Security Token Service  
* 403 (Forbidden): The credentials supplied on the request are not authorized to access this resource.  
* 588 (Bad Response): An error occurred while performing response validation.  
* 500 (Internal Server Error): An error occurred while processing the request.

**Sample Response**

        {

    "header": {

        "transactionId": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57",

        "quoteback": "LSP-Sample request"

    },

    "body": {

        "statusCode": 200,

        "completeQuote": {

            "quoteScores": {

                "applicationCompletenessCode": "A3",

                "ratingCompletenessCode": "ACA"

            },

            "messages": \[

                {

                    "code": "101",

                    "description": "Vehicles, applicant, and additional subjects found."

                }

            \],

            "riskCheckScoreSummary": {

                "riskGroup": "VERY HIGH",

                "scoreColor": "RED",

                "totalScore": "3588",

                "isCraWarning": false,

                "isFraudIndicator": false,

                "scoreDecile": "8",

                "creditHeader": "N"

            },

            "policies": \[

                {

                    "carrier": {

                        "name": "INSURANCE SERVICES O",

                        "ambest": "99999",

                        "naic": "00000"

                    },

                    "policyNumber": "VRSKLSP201810021001",

                    "policyStatus": "INFORCE",

                    "policyType": {

                        "code": "AU",

                        "description": "Auto"

                    },

                    "compOnlyPolicy": "N",

                    "policyReportedDate": "20230213",

                    "inceptionDate": "20170301",

                    "lastReportedTermEffectiveDate": "20230105",

                    "lastReportedTermExpirationDate": "20240105",

                    "numberOfCancellations": "0",

                    "numberOfRenewals": "3",

                    "matchBasisInformationModel": {

                        "matchScore": "100",

                        "searchType": {

                            "code": "P",

                            "description": "Person"

                        },

                        "matchReasons": \[

                            "NAME IS IDENTICAL",

                            "ADDRESS IS IDENTICAL",

                            "ZIP IS IDENTICAL"

                        \]

                    },

                    "coverages": \[

                        {

                            "coverageType": {

                                "code": "BINJ",

                                "description": "Bodily Injury"

                            },

                            "individualLimitAmount": "40000",

                            "occurrenceLimitAmount": "80000",

                            "combinedSingleLimitAmount": "0",

                            "fromDate": "20230105",

                            "toDate": "20240105"

                        },

                        {

                            "coverageType": {

                                "code": "CBSL",

                                "description": "CSL (BI & PD)"

                            },

                            "individualLimitAmount": "0",

                            "occurrenceLimitAmount": "0",

                            "combinedSingleLimitAmount": "80000",

                            "fromDate": "20230105",

                            "toDate": "20240105"

                        },

                        {

                            "coverageType": {

                                "code": "PDMG",

                                "description": "Property Damage"

                            },

                            "individualLimitAmount": "20000",

                            "occurrenceLimitAmount": "40000",

                            "combinedSingleLimitAmount": "0",

                            "fromDate": "20230105",

                            "toDate": "20240105"

                        },

                        {

                            "coverageType": {

                                "code": "UMPD",

                                "description": "Uninsured Motorist (PD)"

                            },

                            "individualLimitAmount": "20000",

                            "occurrenceLimitAmount": "40000",

                            "combinedSingleLimitAmount": "0",

                            "fromDate": "20230105",

                            "toDate": "20240105"

                        },

                        {

                            "coverageType": {

                                "code": "PINJ",

                                "description": "Personal Injury"

                            },

                            "individualLimitAmount": "20000",

                            "occurrenceLimitAmount": "40000",

                            "combinedSingleLimitAmount": "0",

                            "fromDate": "20230105",

                            "toDate": "20240105"

                        }

                    \],

                    "policyHolders": \[

                        {

                            "givenName": "DOUGLAS",

                            "middleName": "J",

                            "surname": "BONZHEIM",

                            "dob": "19760101",

                            "dlNumber": "M888777666555",

                            "dlState": "FL"

                        },

                        {

                            "givenName": "LORNA",

                            "middleName": "P",

                            "surname": "BONZHEIM",

                            "dob": "20030923",

                            "dlNumber": "B640693682100",

                            "dlState": "FL"

                        }

                    \],

                    "phoneNumbers": \[

                        {

                            "phoneType": "H",

                            "number": "1112223335",

                            "extension": "0000"

                        }

                    \],

                    "addresses": \[

                        {

                            "addressType": "Mailing",

                            "street1": "7827 Adelaide Loop",

                            "city": "New Port Richey",

                            "stateCode": "FL",

                            "zip": "34655",

                            "fromDate": "20230105",

                            "toDate": "20240105"

                        }

                    \]

                }

            \],

            "coverageLapseInformation": \[

                {

                    "givenName": "YUKI",

                    "surname": "BONZHEIM",

                    "inputDriverSequenceNumber": "1",

                    "hasPossibleLapse": "N",

                    "isCurrentInforceCoverage": "Y",

                    "coverageIntervals": \[

                        {

                            "carrier": {

                                "name": "INSURANCE SERVICES O",

                                "ambest": "99999",

                                "naic": "00000",

                                "financialAmbest": "99999"

                            },

                            "startDate": "20220105",

                            "endDate": "20240105",

                            "numberOfCoverageDays": "628",

                            "hasBreakFromPriorCoverage": "NA",

                            "numberOfLapseDays": "0"

                        }

                    \]

                }

            \],

            "addresses": \[

                {

                    "addressType": "Current Standardized",

                    "street1": "7827 Adelaide Loop",

                    "city": "New Port Richey",

                    "stateCode": "FL",

                    "zip": "346552733",

                    "countyName": "Pasco",

                    "fipsCountyCd": "12101",

                    "dpvFootnote": "AABB",

                    "recordType": "S",

                    "addressResultCodes": \[

                        "AC11",

                        "AS01"

                    \],

                    "latitude": "28.211155",

                    "longitude": "-82.684826"

                }

            \],

            "householdInformation": {

                "youths11to15": "4",

                "youths16to17": "4",

                "dwellingType": "S",

                "homeOwner": "T",

                "lengthofResidence": "2",

                "householdEducation": "5",

                "sohoIndicatorHousehold": "Y",

                "householdSize": "5",

                "netWorth": "B"

            },

            "subjects": \[

                {

                    "sequence": "1",

                    "dataSource": "Principal",

                    "isSubjectVerified": true,

                    "isSubjectActiveDuringMostRecentTerm": true,

                    "entityScore": "95",

                    "givenName": "YUKI",

                    "middleName": "R",

                    "surname": "BONZHEIM",

                    "primarySourceInfo": {

                        "dob": "19900311",

                        "gender": "M",

                        "maritalStatus": "S",

                        "dlNumber": "T520103597610",

                        "dlState": "FL",

                        "relationToPolicyHolder": "LD",

                        "relationToInsured": "O",

                        "fromDate": "20230105",

                        "toDate": "20240105"

                    },

                    "secondarySourceInfo": {

                        "dob": "19900311",

                        "gender": "M",

                        "maritalStatus": "S",

                        "matchType": "N",

                        "verificationDate": "20220715",

                        "verificationRange": "2",

                        "driverAssuranceScore": "D1",

                        "internalDriverCode": "7"

                    },

                    "reasonCodeDetails": \[

                        {

                            "code": "ID-1.11",

                            "description": "No identity located or poor match on primary data source."

                        },

                        {

                            "code": "ID-1.12",

                            "description": "Social Security Number not validated."

                        },

                        {

                            "code": "ID-1.13",

                            "description": "Date of Birth not validated."

                        },

                        {

                            "code": "ID-1.31",

                            "description": "Input Address(es), including current and former, did not match to any of the addresses contained in the primary data source."

                        },

                        {

                            "code": "AG-2.17",

                            "description": "Input Address(es) including current and former did not match to any of the addresses contained in the primary data source."

                        }

                    \],

                    "actionMessages": \[

                        "Ask for Drivers License and Utility Bill"

                    \],

                    "motorVehicleReports": \[

                        {

                            "status": {

                                "code": "V",

                                "description": "NON-CLEAR report"

                            },

                            "violationsType": {

                                "code": "C",

                                "description": "Report passed through Custom violation code/point process",

                                "pointTotal": "0"

                            },

                            "dmvReportDate": "20201120",

                            "driversPrivacyProtectionActFlag": "N",

                            "driver": {

                                "name": "BONZHEIM, YUKI",

                                "cityStateZip": "NEW PORT RICHEY, FL 34655",

                                "street1": "7827 ADELAIDE LP",

                                "dlNumber": "T520103597610",

                                "dlState": "FL",

                                "dob": "19900311",

                                "gender": "M",

                                "height": "6'1",

                                "license": {

                                    "class": "E",

                                    "status": "VALID",

                                    "issuedDate": "20131001",

                                    "expirationDate": "20210801",

                                    "originalIssueDate": "20001201",

                                    "restriction": null

                                },

                                "detail": "Order Number : 935981072 \- OrderType : MvrIndicator \- REQUESTED AS: YUKI                      BONZHEIM                  DOB: 03111990  LICENSE : T520103597610 PERS:01: ACTIVE          VALID   E              1001201308012021 LIC CLASS: E                       DESC: OPERATOR LIC STATUS: VALID LIC ISSUED: 10/01/2021 LIC EXPIRES: 08/01/2029 PERS:02: EXPIRED         EXPIRED ID CARD        1201200910012014 LIC CLASS: ID CARD                 DESC: ID CARD LIC STATUS: EXPIRED LIC ISSUED: 12/01/2009 LIC EXPIRES: 10/01/2014 AS OF NOVEMBER 20, 2020 AT 9:50:20 AM, DRIVER PRIVILEGE T520-103-59-761-0 IS VALID. PERSONAL INFORMATION IS PROTECTED PURSUANT TO THE DRIVER PRIVACY PROTECTION ACT. ENTRIES BELOW ARE A THREE YEAR RECORD. ORIGINAL ISSUE DATE: 12/01/2000 REAL ID COMPLIANT ORGAN DONOR US CITIZEN BLOCKED PERSONAL INFORMATION BLOCKED FOR MAILING LIST PERSON HAS A DIGITAL IMAGE ELIGIBLE TO ELECT DRIVER SCHOOL.  DRIVER HAS MADE 2 ELECTIONS. LAST ELECTION WAS ON 02/01/2012. VIOLATIONS COMMITTED WHILE A CDL HOLDER OR IN A CMV VEHICLE ARE NOT ELIGIBLE FOR DRIVING SCHOOL ELECTION. COUNTY: MIAMI-DADE RESIDENTIAL ADDRESS: 2570 NW 48TH ST  MIAMI, FL  33142  COUNTY: MIAMI-DADE ISSUANCE HISTORY: LIC CLASS: ID CARD   ISSUE DATE: 12/01/1996   ISSUE TYPE: DUPLICATE LIC CLASS: ID CARD   ISSUE DATE: 12/01/2000   ISSUE TYPE: DUPLICATE LIC CLASS: CLASS E   ISSUE DATE: 05/01/2002   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 02/01/2003   ISSUE TYPE: DUPLICATE LIC CLASS: ID CARD   ISSUE DATE: 07/01/2006   ISSUE TYPE: DUPLICATE LIC CLASS: CLASS E   ISSUE DATE: 04/01/2009   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 02/01/2010   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 02/01/2010   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 08/01/2012   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 10/01/2013   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 10/01/2014   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 03/01/2018   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 10/01/2020   ISSUE TYPE: CDR/CDT CLEARANCE EXAMS TAKEN: VISION               DATE TAKEN: 10/01/2021   COUNT: 2   STATUS: PASS ROAD SIGN            DATE TAKEN: 12/01/2021   COUNT: 1   STATUS: PASS ROAD RULES           DATE TAKEN: 12/01/2020   COUNT: 3   STATUS: PASS DRIVING              DATE TAKEN: 12/01/2020   COUNT: 1   STATUS: PASS This report is generated for insurance purposes only and may not be used for any other purpose.  The use and dissemination of the report and information in it must comply with your iiX agreement and the  Fair Credit Reporting Act, the Driver's Privacy Protection Act, and any applicable state statute(s).  The data in the report from the applicable state agency or service bureau is provided through iiX \\"as is.\\" \--- Customer-defined MVR scoring has been applied to this record.  Customer  is solely responsible for the application and use of the resulting score.",

                                "violations": \[

                                    {

                                        "type": "SUSP",

                                        "violationDate": "20220301",

                                        "customCode": "130110",

                                        "customPoints": "3",

                                        "detail": "Order Number : 935981072 \- FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 720198716 NOTICED PROVIDED: 12/01/2021 ADDED TO RECORD: 12/01/2021 SANCTION CODE: 7"

                                    },

                                    {

                                        "type": "REIN",

                                        "convictionDate": "20220301",

                                        "customCode": "330130",

                                        "customPoints": "-3",

                                        "detail": "Order Number : 935981072 \- REINSTATED"

                                    },

                                    {

                                        "type": "SUSP",

                                        "violationDate": "20211001",

                                        "customCode": "130110",

                                        "customPoints": "3",

                                        "detail": "Order Number : 935981072 \- FR-REGISTRATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 830175467 NOTICED PROVIDED: 09/01/2021 ADDED TO RECORD: 09/01/2021 SANCTION CODE: 8"

                                    },

                                    {

                                        "type": "REIN",

                                        "convictionDate": "20211001",

                                        "customCode": "330130",

                                        "customPoints": "-3",

                                        "detail": "Order Number : 935981072 \- REINSTATED"

                                    },

                                    {

                                        "type": "VIOL",

                                        "violationDate": "20200201",

                                        "convictionDate": "20200601",

                                        "stateAssignedPoints": "0",

                                        "customCode": "425100",

                                        "customPoints": "0",

                                        "detail": "Order Number : 935981072 \- 316.0083 RED LIGHT CAMERA DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 23 CITATION NUMBER: A5OJ78E COUNTY: MIAMI-DADE STATE: FL ADDED TO RECORD: 06/01/2020 DISPOSITION CODE: 547"

                                    },

                                    {

                                        "type": "VIOL",

                                        "violationDate": "20190201",

                                        "convictionDate": "20190801",

                                        "stateAssignedPoints": "0",

                                        "customCode": "425100",

                                        "customPoints": "0",

                                        "detail": "Order Number : 935981072 \- 316.0083 RED LIGHT CAMERA DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 24 CITATION NUMBER: AADQWXE COUNTY: MIAMI-DADE STATE: FL ADDED TO RECORD: 08/01/2019 DISPOSITION CODE: 547"

                                    }

                                \]

                            }

                        }

                    \]

                },

                {

                    "sequence": "2",

                    "dataSource": "Principal",

                    "isSubjectVerified": true,

                    "isSubjectActiveDuringMostRecentTerm": true,

                    "entityScore": "95",

                    "givenName": "DOUGLAS",

                    "middleName": "J",

                    "surname": "BONZHEIM",

                    "primarySourceInfo": {

                        "dob": "19760101",

                        "gender": "M",

                        "maritalStatus": "M",

                        "dlNumber": "M888777666555",

                        "dlState": "FL",

                        "ssn": "491487807",

                        "relationToPolicyHolder": "PP",

                        "relationToInsured": "I",

                        "fromDate": "20230105",

                        "toDate": "20240105"

                    },

                    "secondarySourceInfo": {

                        "dob": "19760101",

                        "gender": "M",

                        "maritalStatus": "S",

                        "matchType": "N",

                        "verificationDate": "20220715",

                        "verificationRange": "2",

                        "driverAssuranceScore": "D1",

                        "internalDriverCode": "7"

                    },

                    "motorVehicleReports": \[

                        {

                            "status": {

                                "code": "V",

                                "description": "NON-CLEAR report"

                            },

                            "violationsType": {

                                "code": "C",

                                "description": "Report passed through Custom violation code/point process",

                                "pointTotal": "4"

                            },

                            "dmvReportDate": "20201120",

                            "driversPrivacyProtectionActFlag": "N",

                            "driver": {

                                "name": "BONZHEIM, DOUGLAS",

                                "cityStateZip": "NEW PORT RICHEY, FL 34655",

                                "street1": "7827 ADELAIDE LP",

                                "dlNumber": "M888777666555",

                                "dlState": "FL",

                                "dob": "19760101",

                                "gender": "M",

                                "height": "5'10",

                                "license": {

                                    "class": "E",

                                    "status": "VALID P",

                                    "issuedDate": "20220401",

                                    "expirationDate": "20300601",

                                    "originalIssueDate": "20000401",

                                    "restriction": null

                                },

                                "detail": "Order Number : 935981071 \- OrderType : MvrIndicator \- REQUESTED AS: DOUGLAS        J          BONZHEIM                  DOB: 01011976  LICENSE : M888777666555 PERS:01: ACTIVE          VALID P E              0401202206012030 LIC CLASS: E                       DESC: OPERATOR LIC STATUS: VALID PENDING LIC ISSUED: 04/01/2022 LIC EXPIRES: 06/01/2030 PERS:02: EXPIRED         EXPIRED ID CARD        0601201805012019 LIC CLASS: ID CARD                 DESC: ID CARD LIC STATUS: EXPIRED LIC ISSUED: 06/01/2018 LIC EXPIRES: 05/01/2019 AS OF NOVEMBER 20, 2020 AT 9:39:55 AM, DRIVER PRIVILEGE M888-777-66-655-5 IS VALID PENDING SANCTION(S). PERSONAL INFORMATION IS PROTECTED PURSUANT TO THE DRIVER PRIVACY PROTECTION ACT. ENTRIES BELOW ARE A THREE YEAR RECORD. ORIGINAL ISSUE DATE: 04/01/2000 REAL ID COMPLIANT US CITIZEN RECORD APPEARS IN NATIONAL DRIVER REGISTER BLOCKED PERSONAL INFORMATION BLOCKED FOR MAILING LIST PERSON HAS A DIGITAL IMAGE ELIGIBLE TO ELECT DRIVER SCHOOL.  DRIVER HAS MADE 0 ELECTIONS. VIOLATIONS COMMITTED WHILE A CDL HOLDER OR IN A CMV VEHICLE ARE NOT ELIGIBLE FOR DRIVING SCHOOL ELECTION. COUNTY: CLAY RESIDENTIAL ADDRESS: 4493 PLANTATION OAKS BLVD 1641  ORANGE PARK, FL  32065  COUNTY: CLAY ISSUANCE HISTORY: LIC CLASS: CLASS D   ISSUE DATE: 06/01/2001   ISSUE TYPE: DUPLICATE LIC CLASS: ID CARD   ISSUE DATE: 02/01/2003   ISSUE TYPE: DUPLICATE LIC CLASS: CLASS E   ISSUE DATE: 05/01/2015   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 06/01/2017   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 04/01/2018   ISSUE TYPE: REPLACEMENT LIC CLASS: ID CARD   ISSUE DATE: 02/01/2019   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 05/01/2019   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 12/01/2019   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 06/01/2020   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 09/01/2020   ISSUE TYPE: CDR/CDT CLEARANCE EXAMS TAKEN: VISION               DATE TAKEN: 04/01/2014   COUNT: 1   STATUS: PASS ROAD SIGN            DATE TAKEN: 08/01/2000   COUNT: 1   STATUS: PASS ROAD RULES           DATE TAKEN: 08/01/2000   COUNT: 4   STATUS: PASS DRIVING              DATE TAKEN: 04/01/2000   COUNT: 1   STATUS: RECIPROCATED This report is generated for insurance purposes only and may not be used for any other purpose.  The use and dissemination of the report and information in it must comply with your iiX agreement and the  Fair Credit Reporting Act, the Driver's Privacy Protection Act, and any applicable state statute(s).  The data in the report from the applicable state agency or service bureau is provided through iiX \\"as is.\\" \--- Customer-defined MVR scoring has been applied to this record.  Customer  is solely responsible for the application and use of the resulting score.",

                                "violations": \[

                                    {

                                        "type": "SUSP",

                                        "violationDate": "20220801",

                                        "customCode": "130110",

                                        "customPoints": "3",

                                        "detail": "Order Number : 935981071 \- FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 730177824 NOTICED PROVIDED: 07/01/2022 ADDED TO RECORD: 07/01/2022 SANCTION CODE: 7"

                                    },

                                    {

                                        "type": "REIN",

                                        "convictionDate": "20220901",

                                        "customCode": "330130",

                                        "customPoints": "-3",

                                        "detail": "Order Number : 935981071 \- REINSTATED"

                                    },

                                    {

                                        "type": "SUSP",

                                        "violationDate": "20211201",

                                        "customCode": "130110",

                                        "customPoints": "3",

                                        "detail": "Order Number : 935981071 \- FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) PENDING SUSPENSION CASE NUMBER 730183044 NOTICED PROVIDED: 11/01/2021 ACTION REQUIRED: YES ADDED TO RECORD: 11/01/2021 SANCTION CODE: 7"

                                    },

                                    {

                                        "type": "VIOL",

                                        "violationDate": "20200701",

                                        "convictionDate": "20210101",

                                        "stateAssignedPoints": "0",

                                        "customCode": "555110",

                                        "customPoints": "0",

                                        "detail": "Order Number : 935981071 \- OPERATING MV NO PROOF OF INSURANCE DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 10 CITATION NUMBER: A0JO2AE COUNTY: DUVAL ADDED TO RECORD: 02/01/2021 DISPOSITION CODE: 280"

                                    },

                                    {

                                        "type": "VIOL",

                                        "violationDate": "20201201",

                                        "convictionDate": "20210101",

                                        "stateAssignedPoints": "0",

                                        "customCode": "425100",

                                        "customPoints": "1",

                                        "detail": "Order Number : 935981071 \- 316.0083 RED LIGHT CAMERA DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 11 CITATION NUMBER: A0IBDGE COUNTY: DUVAL ADDED TO RECORD: 02/01/2021 DISPOSITION CODE: 547"

                                    },

                                    {

                                        "type": "VIOL",

                                        "violationDate": "20200701",

                                        "convictionDate": "20210201",

                                        "stateAssignedPoints": "0",

                                        "customCode": "428300",

                                        "customPoints": "0",

                                        "detail": "Order Number : 935981071 \- SEAT BELT VIOLATION DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 12 CITATION NUMBER: A0JO2YE COUNTY: DUVAL ADDED TO RECORD: 02/01/2021 DISPOSITION CODE: 407"

                                    },

                                    {

                                        "type": "VIOL",

                                        "violationDate": "20200301",

                                        "convictionDate": "20200501",

                                        "stateAssignedPoints": "3",

                                        "customCode": "131240",

                                        "customPoints": "0",

                                        "detail": "Order Number : 935981071 \- DRIV WHILE LIC CANC/REV/SUSP DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 14 CITATION NUMBER: A0GLVGE COUNTY: DUVAL ADDED TO RECORD: 05/01/2020 DISPOSITION CODE: 609"

                                    }

                                \]

                            }

                        },

                        {

                            "status": {

                                "code": "N",

                                "description": "NOT FOUND"

                            },

                            "violationsType": {

                                "code": "N",

                                "description": "Not Coded"

                            },

                            "driver": {

                                "dlNumber": "T123654125803",

                                "dlState": "FL",

                                "detail": "Order Number : 935981069 \- OrderType : MvrIndicator \- "

                            }

                        }

                    \]

                },

                {

                    "sequence": "3",

                    "dataSource": "Principal",

                    "isSubjectVerified": true,

                    "isSubjectActiveDuringMostRecentTerm": true,

                    "entityScore": "95",

                    "givenName": "LORNA",

                    "middleName": "P",

                    "surname": "BONZHEIM",

                    "primarySourceInfo": {

                        "dob": "20030923",

                        "gender": "F",

                        "maritalStatus": "M",

                        "dlNumber": "B640693682100",

                        "dlState": "FL",

                        "relationToPolicyHolder": "SP",

                        "relationToInsured": "S",

                        "fromDate": "20230105",

                        "toDate": "20240105"

                    },

                    "secondarySourceInfo": {

                        "dob": "20030923",

                        "gender": "M",

                        "maritalStatus": "M",

                        "matchType": "N",

                        "verificationDate": "20220315",

                        "verificationRange": "2",

                        "driverAssuranceScore": "D1",

                        "internalDriverCode": "7"

                    },

                    "motorVehicleReports": \[

                        {

                            "status": {

                                "code": "V",

                                "description": "NON-CLEAR report"

                            },

                            "violationsType": {

                                "code": "C",

                                "description": "Report passed through Custom violation code/point process",

                                "pointTotal": "2"

                            },

                            "dmvReportDate": "20201120",

                            "driversPrivacyProtectionActFlag": "N",

                            "driver": {

                                "name": "BONZHEIM, LORNA",

                                "cityStateZip": "NEW PORT RICHEY, FL 34655",

                                "street1": "7827 ADELAIDE LP",

                                "dlNumber": "B640693682100",

                                "dlState": "FL",

                                "dob": "20030923",

                                "gender": "F",

                                "height": "5'6",

                                "license": {

                                    "class": "E",

                                    "status": "VALID",

                                    "issuedDate": "20220301",

                                    "expirationDate": "20300701",

                                    "originalIssueDate": "20010301",

                                    "restriction": "A"

                                },

                                "detail": "Order Number : 935981070 \- OrderType : MvrIndicator \- REQUESTED AS: LORNA          P          BONZHEIM                  DOB: 09232003  LICENSE : B640693682100 PERS:01: ACTIVE          VALID   E              0301202207012030                A LIC CLASS: E                       DESC: OPERATOR LIC STATUS: VALID LIC ISSUED: 03/01/2022 LIC EXPIRES: 07/01/2030 LIC RESTR: A                          DESC: CORRECTIVE LENSES PERS:02: EXPIRED         EXPIRED ID CARD        0901200312012017 LIC CLASS: ID CARD                 DESC: ID CARD LIC STATUS: EXPIRED LIC ISSUED: 09/01/2003 LIC EXPIRES: 12/01/2017 AS OF NOVEMBER 20, 2020 AT 9:45:15 AM, DRIVER PRIVILEGE B640-693-68-210-0 IS VALID. PERSONAL INFORMATION IS PROTECTED PURSUANT TO THE DRIVER PRIVACY PROTECTION ACT. ENTRIES BELOW ARE A THREE YEAR RECORD. ORIGINAL ISSUE DATE: 03/01/2001 REAL ID COMPLIANT US CITIZEN BLOCKED PERSONAL INFORMATION BLOCKED FOR MAILING LIST PERSON HAS A DIGITAL IMAGE ELIGIBLE TO ELECT DRIVER SCHOOL.  DRIVER HAS MADE 2 ELECTIONS. LAST ELECTION WAS ON 06/01/2002. VIOLATIONS COMMITTED WHILE A CDL HOLDER OR IN A CMV VEHICLE ARE NOT ELIGIBLE FOR DRIVING SCHOOL ELECTION. COUNTY: BROWARD RESIDENTIAL ADDRESS: 7923 NW 18TH ST APT 203  MARGATE, FL  33063  COUNTY: BROWARD ISSUANCE HISTORY: LIC CLASS: CLASS E   ISSUE DATE: 09/01/2001   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 06/01/2002   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 06/01/2002   ISSUE TYPE: REPLACEMENT LIC CLASS: ID CARD   ISSUE DATE: 06/01/2002   ISSUE TYPE: DUPLICATE LIC CLASS: CLASS E   ISSUE DATE: 03/01/2004   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 06/01/2006   ISSUE TYPE: ADDRESS CHANGE LIC CLASS: CLASS E   ISSUE DATE: 12/01/2017   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 12/01/2019   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 06/01/2020   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 08/01/2020   ISSUE TYPE: CDR/CDT CLEARANCE EXAMS TAKEN: VISION               DATE TAKEN: 03/01/2022   COUNT: 1   STATUS: PASS ROAD SIGN            DATE TAKEN: 03/01/2022   COUNT: 9   STATUS: RECIPROCATED ROAD RULES           DATE TAKEN: 03/01/2022   COUNT: 3   STATUS: PASS DRIVING              DATE TAKEN: 09/01/2021   COUNT: 4   STATUS: PASS This report is generated for insurance purposes only and may not be used for any other purpose.  The use and dissemination of the report and information in it must comply with your iiX agreement and the  Fair Credit Reporting Act, the Driver's Privacy Protection Act, and any applicable state statute(s).  The data in the report from the applicable state agency or service bureau is provided through iiX \\"as is.\\" \--- Customer-defined MVR scoring has been applied to this record.  Customer  is solely responsible for the application and use of the resulting score.",

                                "violations": \[

                                    {

                                        "type": "SUSP",

                                        "violationDate": "20210701",

                                        "customCode": "130110",

                                        "customPoints": "3",

                                        "detail": "Order Number : 935981070 \- FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 730115590 NOTICED PROVIDED: 06/01/2021 ADDED TO RECORD: 06/01/2021 SANCTION CODE: 7"

                                    },

                                    {

                                        "type": "REIN",

                                        "convictionDate": "20211201",

                                        "customCode": "330130",

                                        "customPoints": "-3",

                                        "detail": "Order Number : 935981070 \- REINSTATED"

                                    },

                                    {

                                        "type": "SUSP",

                                        "violationDate": "20200401",

                                        "customCode": "130110",

                                        "customPoints": "0",

                                        "detail": "Order Number : 935981070 \- FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 730195358 NOTICED PROVIDED: 04/01/2020 ADDED TO RECORD: 04/01/2020 SANCTION CODE: 7"

                                    },

                                    {

                                        "type": "REIN",

                                        "convictionDate": "20200601",

                                        "customCode": "330130",

                                        "customPoints": "0",

                                        "detail": "Order Number : 935981070 \- REINSTATED"

                                    },

                                    {

                                        "type": "SUSP",

                                        "violationDate": "20200801",

                                        "customCode": "130110",

                                        "customPoints": "0",

                                        "detail": "Order Number : 935981070 \- FR-REGISTRATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 830111729 NOTICED PROVIDED: 07/01/2020 ADDED TO RECORD: 07/01/2020 SANCTION CODE: 8"

                                    },

                                    {

                                        "type": "REIN",

                                        "convictionDate": "20200801",

                                        "customCode": "330130",

                                        "customPoints": "0",

                                        "detail": "Order Number : 935981070 \- REINSTATED"

                                    },

                                    {

                                        "type": "VIOL",

                                        "violationDate": "20220201",

                                        "convictionDate": "20220501",

                                        "stateAssignedPoints": "4",

                                        "customCode": "424300",

                                        "customPoints": "1",

                                        "detail": "Order Number : 935981070 \- FAIL TO YIELD UNSIGNED INTERSECTION DISPOSITION WAS GUILTY COUNTY COURT CRASH INDICATED VIOLATION NUMBER: 5 CITATION NUMBER: A0LU14E COUNTY: BROWARD ADDED TO RECORD: 05/01/2022 DISPOSITION CODE: 513"

                                    },

                                    {

                                        "type": "VIOL",

                                        "violationDate": "20211201",

                                        "convictionDate": "20220201",

                                        "stateAssignedPoints": "0",

                                        "customCode": "536400",

                                        "customPoints": "1",

                                        "detail": "Order Number : 935981070 \- EXPIRED TAG \- 6 MOS OR LESS DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 6 CITATION NUMBER: AR9P4UE COUNTY: BROWARD STATE: FL ADDED TO RECORD: 02/01/2022 DISPOSITION CODE: 473"

                                    }

                                \]

                            }

                        }

                    \]

                },

                {

                    "sequence": "4",

                    "dataSource": "Principal",

                    "isSubjectVerified": true,

                    "isSubjectActiveDuringMostRecentTerm": true,

                    "entityScore": "90",

                    "givenName": "MALIA",

                    "middleName": "R",

                    "surname": "BONZHEIM",

                    "primarySourceInfo": {

                        "dob": "19990120",

                        "gender": "F",

                        "maritalStatus": "S",

                        "dlNumber": "S420665834256",

                        "dlState": "FL",

                        "relationToPolicyHolder": "LD",

                        "fromDate": "20230105",

                        "toDate": "20240105"

                    },

                    "secondarySourceInfo": {

                        "dob": "19900720",

                        "gender": "F",

                        "maritalStatus": "S",

                        "matchType": "N",

                        "verificationDate": "20220815",

                        "verificationRange": "2",

                        "driverAssuranceScore": "D1",

                        "internalDriverCode": "7"

                    },

                    "motorVehicleReports": \[

                        {

                            "status": {

                                "code": "N",

                                "description": "NOT FOUND"

                            },

                            "violationsType": {

                                "code": "N",

                                "description": "Not Coded"

                            },

                            "driver": {

                                "dlNumber": "S420665834256",

                                "dlState": "FL",

                                "detail": "Order Number : 935981068 \- OrderType : MvrIndicator \- "

                            }

                        }

                    \]

                },

                {

                    "sequence": "5",

                    "dataSource": "Principal",

                    "isSubjectVerified": true,

                    "isSubjectActiveDuringMostRecentTerm": true,

                    "entityScore": "90",

                    "givenName": "MARKUS",

                    "middleName": "G",

                    "surname": "BONZHEIM",

                    "primarySourceInfo": {

                        "dob": "20010311",

                        "gender": "F",

                        "maritalStatus": "S",

                        "dlNumber": "P420665934225",

                        "dlState": "FL",

                        "relationToPolicyHolder": "LD",

                        "fromDate": "20230105",

                        "toDate": "20240105"

                    },

                    "secondarySourceInfo": {

                        "dob": "20010311",

                        "gender": "M",

                        "maritalStatus": "S",

                        "matchType": "N",

                        "verificationDate": "20220315",

                        "verificationRange": "2",

                        "driverAssuranceScore": "D1",

                        "internalDriverCode": "7"

                    },

                    "motorVehicleReports": \[

                        {

                            "status": {

                                "code": "N",

                                "description": "NOT FOUND"

                            },

                            "violationsType": {

                                "code": "N",

                                "description": "Not Coded"

                            },

                            "driver": {

                                "dlNumber": "P420665934225",

                                "dlState": "FL",

                                "detail": "Order Number : 935981077 \- OrderType : MvrIndicator \- "

                            }

                        }

                    \]

                },

                {

                    "sequence": "6",

                    "dataSource": "Principal",

                    "isSubjectVerified": true,

                    "isSubjectActiveDuringMostRecentTerm": true,

                    "entityScore": "90",

                    "givenName": "MINDI",

                    "middleName": "H",

                    "surname": "BONZHEIM",

                    "primarySourceInfo": {

                        "dob": "19901113",

                        "gender": "F",

                        "maritalStatus": "S",

                        "dlNumber": "R420622534333",

                        "dlState": "FL",

                        "relationToPolicyHolder": "LD",

                        "fromDate": "20230105",

                        "toDate": "20240105"

                    },

                    "secondarySourceInfo": {

                        "dob": "19901113",

                        "gender": "F",

                        "maritalStatus": "S",

                        "matchType": "N",

                        "verificationDate": "20220815",

                        "verificationRange": "2",

                        "driverAssuranceScore": "D1",

                        "internalDriverCode": "7"

                    },

                    "motorVehicleReports": \[

                        {

                            "status": {

                                "code": "N",

                                "description": "NOT FOUND"

                            },

                            "violationsType": {

                                "code": "N",

                                "description": "Not Coded"

                            },

                            "driver": {

                                "dlNumber": "R420622534333",

                                "dlState": "FL",

                                "detail": "Order Number : 935981075 \- OrderType : MvrIndicator \- "

                            }

                        }

                    \]

                },

                {

                    "sequence": "7",

                    "dataSource": "Principal",

                    "isSubjectVerified": false,

                    "isSubjectActiveDuringMostRecentTerm": true,

                    "entityScore": "85",

                    "givenName": "RHETT",

                    "middleName": "K",

                    "surname": "BONZHEIM",

                    "primarySourceInfo": {

                        "dob": "19900720",

                        "gender": "F",

                        "maritalStatus": "S",

                        "dlNumber": "L420625834362",

                        "dlState": "FL",

                        "relationToPolicyHolder": "LD",

                        "fromDate": "20230105",

                        "toDate": "20240105"

                    },

                    "motorVehicleReports": \[

                        {

                            "status": {

                                "code": "N",

                                "description": "NOT FOUND"

                            },

                            "violationsType": {

                                "code": "N",

                                "description": "Not Coded"

                            },

                            "driver": {

                                "dlNumber": "L420625834362",

                                "dlState": "FL",

                                "detail": "Order Number : 935981073 \- OrderType : MvrIndicator \- "

                            }

                        }

                    \]

                }

            \],

            "vehicles": \[

                {

                    "sequence": "1",

                    "dataSource": "Principal",

                    "isVehicleVerified": true,

                    "isVehicleActiveDuringMostRecentTerm": true,

                    "entityScore": "60",

                    "vin": "1G5CT18B5F8530675",

                    "vehiclePolicyData": {

                        "year": "1985",

                        "make": "GMC",

                        "model": "UT",

                        "businessUse": "Y",

                        "classCode": "000000",

                        "collisionDeductibleAmount": "1000",

                        "comprehensiveDeductibleAmount": "500",

                        "fromDate": "20230105",

                        "toDate": "20240105",

                        "collisionIndicator": "Y",

                        "comprehensiveIndicator": "Y",

                        "coverages": \[

                            {

                                "coverageType": {

                                    "code": "BINJ",

                                    "description": "Bodily Injury"

                                },

                                "individualLimitAmount": "40000",

                                "occurrenceLimitAmount": "80000",

                                "combinedSingleLimitAmount": "0",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            },

                            {

                                "coverageType": {

                                    "code": "PDMG",

                                    "description": "Property Damage"

                                },

                                "individualLimitAmount": "20000",

                                "occurrenceLimitAmount": "40000",

                                "combinedSingleLimitAmount": "0",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            },

                            {

                                "coverageType": {

                                    "code": "CBSL",

                                    "description": "CSL (BI & PD)"

                                },

                                "individualLimitAmount": "0",

                                "occurrenceLimitAmount": "0",

                                "combinedSingleLimitAmount": "80000",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            },

                            {

                                "coverageType": {

                                    "code": "UMPD",

                                    "description": "Uninsured Motorist (PD)"

                                },

                                "individualLimitAmount": "20000",

                                "occurrenceLimitAmount": "40000",

                                "combinedSingleLimitAmount": "0",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            },

                            {

                                "coverageType": {

                                    "code": "PINJ",

                                    "description": "Personal Injury"

                                },

                                "individualLimitAmount": "20000",

                                "occurrenceLimitAmount": "40000",

                                "combinedSingleLimitAmount": "0",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            }

                        \]

                    },

                    "registrationData": {

                        "vinMatch": "Y",

                        "validVINIndicator": "Y",

                        "vinChangeIndicator": "N",

                        "vin": "1G5CT18B5F8530675",

                        "vehicleTypeCode": "T",

                        "vehicleTypeDesc": "Truck",

                        "modelYear": "1985",

                        "make": "GMC",

                        "makeDesc": "GMC",

                        "model": "S15",

                        "bodyStyleCode": "UT",

                        "bodyStyleDesc": "Sport Utility Vehicle",

                        "stateOfRegistration": "CO",

                        "transactionDate": "20060119",

                        "expirationDate": "20211212",

                        "plateTypeCode": "Z",

                        "plateTypeDesc": "Regular",

                        "licensePlateNumber": "112MPE",

                        "isBranded": false,

                        "leaseInd": "N",

                        "nameCode1": "A",

                        "nameCodeDesc1": "Owner",

                        "nameTitleCode1": "3",

                        "nameTitleDesc1": "MS",

                        "registeredOwnerName": {

                            "givenName": "RHONDA",

                            "middleName": "R",

                            "surname": "GARCILASCO"

                        },

                        "address": {

                            "addressType": "S",

                            "street1": "4341 W CENTER AVE APT B",

                            "city": "DENVER",

                            "stateCode": "CO",

                            "zip": "80219"

                        }

                    },

                    "numberofVehicleOwners": 1,

                    "isVehicleSalvage": false,

                    "supplementalCatClaimIndicator": "N",

                    "reasonCodeDetails": \[

                        {

                            "code": "AG-2.22",

                            "description": "Vehicle has out of state Registration.  "

                        },

                        {

                            "code": "AO-5.01",

                            "description": "Vehicle is not owned by Policy Holder or any Driver on the Policy."

                        }

                    \],

                    "actionMessages": \[

                        "Ask for Vehicle Registration"

                    \],

                    "mileage": {

                        "sources": \[

                            {

                                "name": "VeriskMileageModel",

                                "miles": "3743"

                            }

                        \]

                    },

                    "smartScore": {

                        "enrollmentStatus": "EN",

                        "enrollmentDate": "2022-01-01 05:00:41.394",

                        "productEnrollmentStatus": "EN",

                        "scoreStatus": "SU",

                        "scoreType": "Recent",

                        "score": "85",

                        "scoreStartDate": "2022-11-14 00:00:00.000",

                        "scoreEndDate": "2023-01-22 23:59:59.000"

                    },

                    "vinMaster": {

                        "vehicles": \[

                            {

                                "vin": "1G5CT18B\&F",

                                "fullModelYear": "1985",

                                "make": "GMC",

                                "makeDescription": "GMC",

                                "basicModelName": "JIMMY S-15",

                                "fullModelName": "JIMMY S-15",

                                "bodyStyle": "UTIL 4X4",

                                "bodyStyleDescription": "Utility Vehicle \- Four-Wheel Drive",

                                "engineSize": "173",

                                "engineCylinders": "6",

                                "engineCylindersDescription": "Six-Cylinder Engine",

                                "engineTypeDescription": "Other Type of Engine",

                                "fourWheelDriveIndicator": "4",

                                "fourWheelDriveIndicatorDescription": "Vehicle is four-wheel drive",

                                "restraint": "A",

                                "restraintDescription": "Driver & Front Passenger Active Restraints",

                                "antiLockBrakes": "N",

                                "antiLockBrakesDescription": "Anti-Lock Brakes are not available",

                                "antiTheftIndicatorDescription": "Field not added to VINMASTER until model year 1990",

                                "electronicStabilityControlDescription": "Field not added to VINMASTER until model year 1995",

                                "daytimeRunningLightIndicatorDescription": "Field not added to VINMASTER until model year 1995",

                                "recordType": "S",

                                "priceNewSymbol\_27SymbolTable\_OnePosition": "J",

                                "priceNewSymbol\_27SymbolTable\_TwoPositions": "10",

                                "priceNew\_Min": "10001.00",

                                "priceNew\_Max": "12500.99",

                                "physicalDamage": {

                                    "combinedVSRSymbol\_OnePosition": "J",

                                    "combinedVSRSymbol\_TwoPositions": "10"

                                }

                            }

                        \]

                    },

                    "riskAnalyzer": {

                        "vehicles": \[

                            {

                                "vin": "1G5CT18B\&F",

                                "modelYear": "1985",

                                "distributionDate": "2212",

                                "restraint": "A",

                                "antiLockBrakes": "N",

                                "engineCylinders": "6",

                                "make": "GMC",

                                "basicModelName": "JIMMY S-15",

                                "bodyStyle": "UTIL 4X4",

                                "engineSize": "173",

                                "fourWheelDriveIndicator": "4",

                                "payloadCapacity": "0",

                                "fullModelName": "JIMMY S-15",

                                "wheelbase": "0",

                                "curbWeight": "0",

                                "grossVehicleWeight": "0",

                                "height": "0",

                                "horsepower": "0",

                                "stateException": "TX",

                                "ncicCode": "GMC",

                                "length": "0",

                                "width": "0",

                                "baseMSRP": "10001",

                                "specialHandlingIndicator": "N",

                                "interimIndicator": "N",

                                "releaseDate": "2303",

                                "physicalDamage": {

                                    "riskAnalyzerCollisionIndicatedSymbol": "BC",

                                    "riskAnalyzerComprehensiveIndicatedSymbol": "AB",

                                    "riskAnalyzerCollisionRatingSymbol": "BC",

                                    "riskAnalyzerComprehensiveRatingSymbol": "AB",

                                    "riskAnalyzerComprehensiveNonGlassRatingSymbol": "AB",

                                    "riskAnalyzerCollisionCappingIndicator": "N",

                                    "riskAnalyzerComprehensiveCappingIndicator": "N",

                                    "riskAnalyzerComprehensiveNonGlassCappingIndicator": "N",

                                    "riskAnalyzerComprehensiveNonGlassIndicatedSymbol": "AB"

                                },

                                "liability": {

                                    "riskAnalyzerMedicalPaymentsIndicatedSymbol": "FB",

                                    "riskAnalyzerPersonalInjuryProtectionIndicatedSymbol": "VB",

                                    "riskAnalyzerSingleLimitIndicatedSymbol": "JF",

                                    "riskAnalyzerBodilyInjuryRatingSymbol": "JH",

                                    "riskAnalyzerPropertyDamageRatingSymbol": "JC",

                                    "riskAnalyzerMedicalPaymentsRatingSymbol": "FB",

                                    "riskAnalyzerPersonalInjuryProtectionRatingSymbol": "VB",

                                    "riskAnalyzerSingleLimitRatingSymbol": "JF",

                                    "riskAnalyzerBodilyInjuryCappingIndicator": "N",

                                    "riskAnalyzerPropertyDamageCappingIndicator": "N",

                                    "riskAnalyzerMedicalPaymentsCappingIndicator": "N",

                                    "riskAnalyzerPersonalInjuryProtectionCappingIndicator": "N",

                                    "riskAnalyzerBodilyInjuryIndicatedSymbol": "JH",

                                    "riskAnalyzerPropertyDamageIndicatedSymbol": "JC",

                                    "riskAnalyzerSingleLimitCappingIndicator": "N"

                                }

                            }

                        \]

                    }

                },

                {

                    "sequence": "2",

                    "dataSource": "Principal",

                    "isVehicleVerified": true,

                    "isVehicleActiveDuringMostRecentTerm": true,

                    "entityScore": "60",

                    "vin": "3GNFK16T9YG218125",

                    "vehiclePolicyData": {

                        "year": "2000",

                        "make": "CHEV",

                        "model": "K1S",

                        "businessUse": "Y",

                        "classCode": "000000",

                        "collisionDeductibleAmount": "1000",

                        "comprehensiveDeductibleAmount": "500",

                        "fromDate": "20230105",

                        "toDate": "20240105",

                        "collisionIndicator": "Y",

                        "comprehensiveIndicator": "Y",

                        "coverages": \[

                            {

                                "coverageType": {

                                    "code": "BINJ",

                                    "description": "Bodily Injury"

                                },

                                "individualLimitAmount": "40000",

                                "occurrenceLimitAmount": "80000",

                                "combinedSingleLimitAmount": "0",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            },

                            {

                                "coverageType": {

                                    "code": "PDMG",

                                    "description": "Property Damage"

                                },

                                "individualLimitAmount": "20000",

                                "occurrenceLimitAmount": "40000",

                                "combinedSingleLimitAmount": "0",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            },

                            {

                                "coverageType": {

                                    "code": "CBSL",

                                    "description": "CSL (BI & PD)"

                                },

                                "individualLimitAmount": "0",

                                "occurrenceLimitAmount": "0",

                                "combinedSingleLimitAmount": "80000",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            },

                            {

                                "coverageType": {

                                    "code": "UMPD",

                                    "description": "Uninsured Motorist (PD)"

                                },

                                "individualLimitAmount": "20000",

                                "occurrenceLimitAmount": "40000",

                                "combinedSingleLimitAmount": "0",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            },

                            {

                                "coverageType": {

                                    "code": "PINJ",

                                    "description": "Personal Injury"

                                },

                                "individualLimitAmount": "20000",

                                "occurrenceLimitAmount": "40000",

                                "combinedSingleLimitAmount": "0",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            }

                        \]

                    },

                    "registrationData": {

                        "vinMatch": "Y",

                        "validVINIndicator": "Y",

                        "vinChangeIndicator": "N",

                        "vin": "3GNFK16T9YG218125",

                        "vehicleTypeCode": "T",

                        "vehicleTypeDesc": "Truck",

                        "modelYear": "2000",

                        "make": "CHE",

                        "makeDesc": "CHEVROLET",

                        "model": "SUBURBAN",

                        "bodyStyleCode": "UT",

                        "bodyStyleDesc": "Sport Utility Vehicle",

                        "stateOfRegistration": "KY",

                        "transactionDate": "20101203",

                        "expirationDate": "20210601",

                        "plateTypeCode": "Z",

                        "plateTypeDesc": "Regular",

                        "licensePlateNumber": "1KMC11",

                        "isBranded": false,

                        "leaseInd": "N",

                        "nameCode1": "A",

                        "nameCodeDesc1": "Owner",

                        "nameTitleCode1": "1",

                        "nameTitleDesc1": "MR",

                        "registeredOwnerName": {

                            "givenName": "JOHNSON",

                            "surname": "JONNIE"

                        },

                        "address": {

                            "addressType": "S",

                            "street1": "2700 NEW HOLD RD",

                            "city": "PADUCAH",

                            "stateCode": "KY",

                            "zip": "42001"

                        }

                    },

                    "numberofVehicleOwners": 1,

                    "isVehicleSalvage": false,

                    "supplementalCatClaimIndicator": "N",

                    "reasonCodeDetails": \[

                        {

                            "code": "AG-2.22",

                            "description": "Vehicle has out of state Registration.  "

                        },

                        {

                            "code": "AO-5.01",

                            "description": "Vehicle is not owned by Policy Holder or any Driver on the Policy."

                        }

                    \],

                    "actionMessages": \[

                        "Ask for Vehicle Registration"

                    \],

                    "mileage": {

                        "sources": \[

                            {

                                "name": "VeriskMileageModel",

                                "miles": "8218"

                            }

                        \]

                    },

                    "smartScore": {

                        "enrollmentStatus": "EN",

                        "enrollmentDate": "2022-01-01 05:00:41.394",

                        "productEnrollmentStatus": "EN",

                        "scoreStatus": "SU",

                        "scoreType": "Recent",

                        "score": "100",

                        "scoreStartDate": "2022-11-21 00:00:00.000",

                        "scoreEndDate": "2023-01-29 23:59:59.000"

                    },

                    "vinMaster": {

                        "vehicles": \[

                            {

                                "vin": "3GN\&K16T\&Y",

                                "fullModelYear": "2000",

                                "make": "CHEV",

                                "makeDescription": "CHEVROLET",

                                "basicModelName": "SUBURBAN",

                                "fullModelName": "SUBURBAN 1500 BASE/LS/LT",

                                "bodyStyle": "UTL4X44D",

                                "bodyStyleDescription": "Utility Vehicle \- Four-Wheel Drive 4-Door",

                                "curbWeight": "05123",

                                "horsepower": "0285",

                                "grossVehicleWeight": "07200",

                                "payloadCapacity": "2077",

                                "height": "073.3",

                                "engineSize": "5.3",

                                "wheelbase": "130.0",

                                "engineCylinders": "8",

                                "engineCylindersDescription": "Eight-Cylinder Engine",

                                "engineTypeDescription": "Other Type of Engine",

                                "fourWheelDriveIndicator": "4",

                                "fourWheelDriveIndicatorDescription": "Vehicle is four-wheel drive",

                                "restraint": "S",

                                "restraintDescription": "Driver & Front Passenger Front & Side Airbags",

                                "classCode": "93",

                                "classCodeDescription": "Large Utility",

                                "tonnageIndicator": "15",

                                "tonnageIndicatorDescription": "3.75 tons (07001 to 07500 lbs)",

                                "antiLockBrakes": "S",

                                "antiLockBrakesDescription": "Anti-Lock Brakes are standard equipment",

                                "antiTheftIndicator": "P",

                                "antiTheftIndicatorDescription": "Passive Disabling",

                                "electronicStabilityControl": "N",

                                "electronicStabilityControlDescription": "Electronic Stability Control is not available",

                                "daytimeRunningLightIndicator": "S",

                                "daytimeRunningLightIndicatorDescription": "Daytime Running Lights Standard Equipment",

                                "circularNumber": "0001",

                                "recordType": "S",

                                "priceNewSymbol\_27SymbolTable\_OnePosition": "P",

                                "priceNewSymbol\_27SymbolTable\_TwoPositions": "21",

                                "priceNew\_Min": "36001.00",

                                "priceNew\_Max": "40000.99",

                                "physicalDamage": {

                                    "combinedVSRSymbol\_OnePosition": "F",

                                    "combinedVSRSymbol\_TwoPositions": "13"

                                }

                            }

                        \]

                    },

                    "riskAnalyzer": {

                        "vehicles": \[

                            {

                                "vin": "3GN\&K16T\&Y",

                                "modelYear": "2000",

                                "distributionDate": "2212",

                                "restraint": "S",

                                "antiLockBrakes": "S",

                                "engineCylinders": "8",

                                "make": "CHEV",

                                "basicModelName": "SUBURBAN",

                                "bodyStyle": "UTL4X44D",

                                "engineSize": "5.3",

                                "fourWheelDriveIndicator": "4",

                                "electronicStabilityControl": "N",

                                "tonnageIndicator": "15",

                                "payloadCapacity": "2077",

                                "fullModelName": "SUBURBAN 1500 BASE/LS/LT",

                                "daytimeRunningLightIndicator": "S",

                                "wheelbase": "130",

                                "classCode": "93",

                                "antiTheftIndicator": "P",

                                "curbWeight": "5123",

                                "grossVehicleWeight": "7200",

                                "height": "73.3",

                                "horsepower": "285",

                                "stateException": "TX",

                                "ncicCode": "CHEV",

                                "length": "0",

                                "width": "0",

                                "baseMSRP": "36001",

                                "specialHandlingIndicator": "N",

                                "interimIndicator": "N",

                                "releaseDate": "2303",

                                "physicalDamage": {

                                    "riskAnalyzerCollisionIndicatedSymbol": "EJ",

                                    "riskAnalyzerComprehensiveIndicatedSymbol": "DG",

                                    "riskAnalyzerCollisionRatingSymbol": "EJ",

                                    "riskAnalyzerComprehensiveRatingSymbol": "DG",

                                    "riskAnalyzerComprehensiveNonGlassRatingSymbol": "DG",

                                    "riskAnalyzerCollisionCappingIndicator": "N",

                                    "riskAnalyzerComprehensiveCappingIndicator": "N",

                                    "riskAnalyzerComprehensiveNonGlassCappingIndicator": "N",

                                    "riskAnalyzerComprehensiveNonGlassIndicatedSymbol": "DG"

                                },

                                "liability": {

                                    "riskAnalyzerMedicalPaymentsIndicatedSymbol": "FE",

                                    "riskAnalyzerPersonalInjuryProtectionIndicatedSymbol": "EH",

                                    "riskAnalyzerSingleLimitIndicatedSymbol": "MK",

                                    "riskAnalyzerBodilyInjuryRatingSymbol": "LH",

                                    "riskAnalyzerPropertyDamageRatingSymbol": "MN",

                                    "riskAnalyzerMedicalPaymentsRatingSymbol": "FE",

                                    "riskAnalyzerPersonalInjuryProtectionRatingSymbol": "EH",

                                    "riskAnalyzerSingleLimitRatingSymbol": "MK",

                                    "riskAnalyzerBodilyInjuryCappingIndicator": "N",

                                    "riskAnalyzerPropertyDamageCappingIndicator": "N",

                                    "riskAnalyzerMedicalPaymentsCappingIndicator": "N",

                                    "riskAnalyzerPersonalInjuryProtectionCappingIndicator": "N",

                                    "riskAnalyzerBodilyInjuryIndicatedSymbol": "LH",

                                    "riskAnalyzerPropertyDamageIndicatedSymbol": "MN",

                                    "riskAnalyzerSingleLimitCappingIndicator": "N"

                                }

                            }

                        \]

                    }

                },

                {

                    "sequence": "3",

                    "dataSource": "Principal",

                    "isVehicleVerified": true,

                    "isVehicleActiveDuringMostRecentTerm": true,

                    "entityScore": "60",

                    "vin": "1HGCM56306A148752",

                    "vehiclePolicyData": {

                        "year": "2006",

                        "make": "HOND",

                        "model": "ASE",

                        "businessUse": "N",

                        "classCode": "000000",

                        "collisionDeductibleAmount": "1000",

                        "comprehensiveDeductibleAmount": "500",

                        "fromDate": "20230105",

                        "toDate": "20240105",

                        "collisionIndicator": "Y",

                        "comprehensiveIndicator": "Y",

                        "coverages": \[

                            {

                                "coverageType": {

                                    "code": "BINJ",

                                    "description": "Bodily Injury"

                                },

                                "individualLimitAmount": "40000",

                                "occurrenceLimitAmount": "80000",

                                "combinedSingleLimitAmount": "0",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            },

                            {

                                "coverageType": {

                                    "code": "PDMG",

                                    "description": "Property Damage"

                                },

                                "individualLimitAmount": "20000",

                                "occurrenceLimitAmount": "40000",

                                "combinedSingleLimitAmount": "0",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            },

                            {

                                "coverageType": {

                                    "code": "CBSL",

                                    "description": "CSL (BI & PD)"

                                },

                                "individualLimitAmount": "0",

                                "occurrenceLimitAmount": "0",

                                "combinedSingleLimitAmount": "80000",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            },

                            {

                                "coverageType": {

                                    "code": "UMPD",

                                    "description": "Uninsured Motorist (PD)"

                                },

                                "individualLimitAmount": "20000",

                                "occurrenceLimitAmount": "40000",

                                "combinedSingleLimitAmount": "0",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            },

                            {

                                "coverageType": {

                                    "code": "PINJ",

                                    "description": "Personal Injury"

                                },

                                "individualLimitAmount": "20000",

                                "occurrenceLimitAmount": "40000",

                                "combinedSingleLimitAmount": "0",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            }

                        \]

                    },

                    "registrationData": {

                        "vinMatch": "Y",

                        "validVINIndicator": "Y",

                        "vinChangeIndicator": "N",

                        "vin": "1HGCM56306A148752",

                        "vehicleTypeCode": "P",

                        "vehicleTypeDesc": "Passenger Car",

                        "modelYear": "2006",

                        "make": "HON",

                        "makeDesc": "HONDA",

                        "model": "ACCORD",

                        "bodyStyleCode": "SD",

                        "bodyStyleDesc": "Sedan",

                        "stateOfRegistration": "CO",

                        "transactionDate": "20091028",

                        "expirationDate": "20211231",

                        "plateTypeCode": "Z",

                        "plateTypeDesc": "Regular",

                        "licensePlateNumber": "403OAK",

                        "isBranded": true,

                        "brandedTitleState1": "CO",

                        "brandedTitleDate1": "20150815",

                        "brandedTitleCode1": "H",

                        "brandedTitleDesc1": "REBUILT",

                        "brandedTitleState2": "OR",

                        "brandedTitleDate2": "20150615",

                        "brandedTitleCode2": "J",

                        "brandedTitleDesc2": "SALVAGE",

                        "leaseInd": "N",

                        "nameCode1": "A",

                        "nameCodeDesc1": "Owner",

                        "nameTitleCode1": "1",

                        "nameTitleDesc1": "MR",

                        "registeredOwnerName": {

                            "givenName": "JAMES",

                            "middleName": "W",

                            "surname": "LEYDEN"

                        },

                        "address": {

                            "addressType": "S",

                            "street1": "10558 PAINT PL",

                            "city": "LITTLETON",

                            "stateCode": "CO",

                            "zip": "80125"

                        }

                    },

                    "numberofVehicleOwners": 1,

                    "isVehicleSalvage": true,

                    "supplementalCatClaimIndicator": "N",

                    "reasonCodeDetails": \[

                        {

                            "code": "AG-2.22",

                            "description": "Vehicle has out of state Registration.  "

                        },

                        {

                            "code": "AO-5.01",

                            "description": "Vehicle is not owned by Policy Holder or any Driver on the Policy."

                        },

                        {

                            "code": "MI-7.01",

                            "description": "The vehicle has a salvage, flood or junk title"

                        }

                    \],

                    "actionMessages": \[

                        "Ask for Vehicle Registration"

                    \],

                    "mileage": {

                        "sources": \[

                            {

                                "name": "VeriskMileageModel",

                                "miles": "11059"

                            }

                        \]

                    },

                    "vinMaster": {

                        "vehicles": \[

                            {

                                "vin": "1HGCM563&6",

                                "fullModelYear": "2006",

                                "make": "HOND",

                                "makeDescription": "HONDA",

                                "basicModelName": "ACCORD",

                                "fullModelName": "ACCORD SE",

                                "bodyStyle": "SEDAN 4D",

                                "bodyStyleDescription": "4-Door Sedan",

                                "curbWeight": "03197",

                                "horsepower": "0166",

                                "grossVehicleWeight": "00000",

                                "payloadCapacity": "0000",

                                "height": "057.2",

                                "engineSize": "2.4",

                                "wheelbase": "107.9",

                                "engineCylinders": "4",

                                "engineCylindersDescription": "Four-Cylinder Engine",

                                "engineTypeDescription": "Other Type of Engine",

                                "fourWheelDriveIndicatorDescription": "Vehicle is not four-wheel drive",

                                "restraint": "R",

                                "restraintDescription": "Driver & Front Passenger Front, Side & Head Airbags, Rear Passenger Head Airbags",

                                "classCode": "34",

                                "classCodeDescription": "Midsize 4-Door",

                                "vmPerformanceIndicatorDescription": "Standard",

                                "tonnageIndicator": "00",

                                "tonnageIndicatorDescription": "N/A",

                                "antiLockBrakes": "S",

                                "antiLockBrakesDescription": "Anti-Lock Brakes are standard equipment",

                                "antiTheftIndicator": "P",

                                "antiTheftIndicatorDescription": "Passive Disabling",

                                "electronicStabilityControl": "O",

                                "electronicStabilityControlDescription": "Electronic Stability Control is optional equipment",

                                "daytimeRunningLightIndicator": "S",

                                "daytimeRunningLightIndicatorDescription": "Daytime Running Lights Standard Equipment",

                                "circularNumber": "0512",

                                "recordType": "S",

                                "priceNewSymbol\_27SymbolTable\_OnePosition": "G",

                                "priceNewSymbol\_27SymbolTable\_TwoPositions": "14",

                                "priceNew\_Min": "20001.00",

                                "priceNew\_Max": "22000.99",

                                "physicalDamage": {

                                    "combinedVSRSymbol\_OnePosition": "E",

                                    "combinedVSRSymbol\_TwoPositions": "12"

                                }

                            }

                        \]

                    },

                    "riskAnalyzer": {

                        "vehicles": \[

                            {

                                "vin": "1HGCM563&6",

                                "modelYear": "2006",

                                "distributionDate": "2212",

                                "restraint": "R",

                                "antiLockBrakes": "S",

                                "engineCylinders": "4",

                                "make": "HOND",

                                "basicModelName": "ACCORD",

                                "bodyStyle": "SEDAN 4D",

                                "engineSize": "2.4",

                                "electronicStabilityControl": "O",

                                "tonnageIndicator": "00",

                                "payloadCapacity": "0",

                                "fullModelName": "ACCORD SE",

                                "daytimeRunningLightIndicator": "S",

                                "wheelbase": "107.9",

                                "classCode": "34",

                                "antiTheftIndicator": "P",

                                "curbWeight": "3197",

                                "grossVehicleWeight": "0",

                                "height": "57.2",

                                "horsepower": "166",

                                "ncicCode": "HOND",

                                "chassis": "U",

                                "length": "0",

                                "width": "0",

                                "baseMSRP": "20001",

                                "specialHandlingIndicator": "N",

                                "interimIndicator": "N",

                                "specialInfoSelector": "M",

                                "modelSeriesInfo": "CURB",

                                "releaseDate": "2303",

                                "physicalDamage": {

                                    "riskAnalyzerCollisionIndicatedSymbol": "DM",

                                    "riskAnalyzerComprehensiveIndicatedSymbol": "CE",

                                    "riskAnalyzerCollisionRatingSymbol": "DM",

                                    "riskAnalyzerComprehensiveRatingSymbol": "CE",

                                    "riskAnalyzerComprehensiveNonGlassRatingSymbol": "CF",

                                    "riskAnalyzerCollisionCappingIndicator": "N",

                                    "riskAnalyzerComprehensiveCappingIndicator": "N",

                                    "riskAnalyzerComprehensiveNonGlassCappingIndicator": "N",

                                    "riskAnalyzerComprehensiveNonGlassIndicatedSymbol": "CF"

                                },

                                "liability": {

                                    "riskAnalyzerMedicalPaymentsIndicatedSymbol": "NR",

                                    "riskAnalyzerPersonalInjuryProtectionIndicatedSymbol": "MM",

                                    "riskAnalyzerSingleLimitIndicatedSymbol": "ML",

                                    "riskAnalyzerBodilyInjuryRatingSymbol": "ML",

                                    "riskAnalyzerPropertyDamageRatingSymbol": "MK",

                                    "riskAnalyzerMedicalPaymentsRatingSymbol": "NR",

                                    "riskAnalyzerPersonalInjuryProtectionRatingSymbol": "MM",

                                    "riskAnalyzerSingleLimitRatingSymbol": "ML",

                                    "riskAnalyzerBodilyInjuryCappingIndicator": "N",

                                    "riskAnalyzerPropertyDamageCappingIndicator": "N",

                                    "riskAnalyzerMedicalPaymentsCappingIndicator": "N",

                                    "riskAnalyzerPersonalInjuryProtectionCappingIndicator": "N",

                                    "riskAnalyzerBodilyInjuryIndicatedSymbol": "ML",

                                    "riskAnalyzerPropertyDamageIndicatedSymbol": "MK",

                                    "riskAnalyzerSingleLimitCappingIndicator": "N"

                                }

                            }

                        \]

                    }

                },

                {

                    "sequence": "4",

                    "dataSource": "Principal",

                    "isVehicleVerified": true,

                    "isVehicleActiveDuringMostRecentTerm": true,

                    "entityScore": "60",

                    "vin": "1GKER23788J291227",

                    "vehiclePolicyData": {

                        "year": "2008",

                        "make": "GMC",

                        "model": "S1F",

                        "businessUse": "Y",

                        "classCode": "000000",

                        "collisionDeductibleAmount": "1000",

                        "comprehensiveDeductibleAmount": "500",

                        "fromDate": "20230105",

                        "toDate": "20240105",

                        "collisionIndicator": "Y",

                        "comprehensiveIndicator": "Y",

                        "coverages": \[

                            {

                                "coverageType": {

                                    "code": "BINJ",

                                    "description": "Bodily Injury"

                                },

                                "individualLimitAmount": "40000",

                                "occurrenceLimitAmount": "80000",

                                "combinedSingleLimitAmount": "0",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            },

                            {

                                "coverageType": {

                                    "code": "PDMG",

                                    "description": "Property Damage"

                                },

                                "individualLimitAmount": "20000",

                                "occurrenceLimitAmount": "40000",

                                "combinedSingleLimitAmount": "0",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            },

                            {

                                "coverageType": {

                                    "code": "CBSL",

                                    "description": "CSL (BI & PD)"

                                },

                                "individualLimitAmount": "0",

                                "occurrenceLimitAmount": "0",

                                "combinedSingleLimitAmount": "80000",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            },

                            {

                                "coverageType": {

                                    "code": "UMPD",

                                    "description": "Uninsured Motorist (PD)"

                                },

                                "individualLimitAmount": "20000",

                                "occurrenceLimitAmount": "40000",

                                "combinedSingleLimitAmount": "0",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            },

                            {

                                "coverageType": {

                                    "code": "PINJ",

                                    "description": "Personal Injury"

                                },

                                "individualLimitAmount": "20000",

                                "occurrenceLimitAmount": "40000",

                                "combinedSingleLimitAmount": "0",

                                "fromDate": "20230105",

                                "toDate": "20240105"

                            }

                        \]

                    },

                    "registrationData": {

                        "vinMatch": "Y",

                        "validVINIndicator": "Y",

                        "vinChangeIndicator": "N",

                        "vin": "1GKER23788J291227",

                        "vehicleTypeCode": "T",

                        "vehicleTypeDesc": "Truck",

                        "modelYear": "2008",

                        "make": "GMC",

                        "makeDesc": "GMC",

                        "model": "ACADIA",

                        "bodyStyleCode": "UT",

                        "bodyStyleDesc": "Sport Utility Vehicle",

                        "stateOfRegistration": "TX",

                        "transactionDate": "20090801",

                        "expirationDate": "20210331",

                        "plateTypeCode": "Z",

                        "plateTypeDesc": "Regular",

                        "licensePlateNumber": "JRR530",

                        "isBranded": false,

                        "leaseInd": "N",

                        "nameCode1": "A",

                        "nameCodeDesc1": "Owner",

                        "nameTitleCode1": "1",

                        "nameTitleDesc1": "MR",

                        "registeredOwnerName": {

                            "givenName": "ROBERT",

                            "middleName": "J",

                            "surname": "PATTERSON"

                        },

                        "address": {

                            "addressType": "S",

                            "street1": "121 CHAPEL HILL DR",

                            "city": "PROSPER",

                            "stateCode": "TX",

                            "zip": "75078"

                        }

                    },

                    "numberofVehicleOwners": 1,

                    "isVehicleSalvage": false,

                    "supplementalCatClaimIndicator": "N",

                    "reasonCodeDetails": \[

                        {

                            "code": "AG-2.22",

                            "description": "Vehicle has out of state Registration.  "

                        },

                        {

                            "code": "AO-5.01",

                            "description": "Vehicle is not owned by Policy Holder or any Driver on the Policy."

                        }

                    \],

                    "actionMessages": \[

                        "Ask for Vehicle Registration"

                    \],

                    "mileage": {

                        "sources": \[

                            {

                                "name": "VeriskMileageModel",

                                "miles": "11080"

                            }

                        \]

                    },

                    "smartScore": {

                        "enrollmentStatus": "EN",

                        "enrollmentDate": "2022-01-01 05:00:41.394",

                        "productEnrollmentStatus": "EN",

                        "scoreStatus": "SU",

                        "scoreType": "Recent",

                        "score": "86",

                        "scoreStartDate": "2022-11-21 00:00:00.000",

                        "scoreEndDate": "2023-01-29 23:59:59.000"

                    },

                    "vinMaster": {

                        "vehicles": \[

                            {

                                "vin": "1GK\&R237&8",

                                "fullModelYear": "2008",

                                "make": "GMC",

                                "makeDescription": "GMC",

                                "basicModelName": "ACADIA",

                                "fullModelName": "ACADIA SLT1",

                                "bodyStyle": "UTL4X24D",

                                "bodyStyleDescription": "Utility Vehicle \- Two-Wheel Drive 4-Door",

                                "curbWeight": "04722",

                                "horsepower": "0275",

                                "grossVehicleWeight": "06400",

                                "payloadCapacity": "1678",

                                "height": "069.9",

                                "engineSize": "3.6",

                                "wheelbase": "118.9",

                                "engineCylinders": "6",

                                "engineCylindersDescription": "Six-Cylinder Engine",

                                "engineTypeDescription": "Other Type of Engine",

                                "fourWheelDriveIndicatorDescription": "Vehicle is not four-wheel drive",

                                "restraint": "R",

                                "restraintDescription": "Driver & Front Passenger Front, Side & Head Airbags, Rear Passenger Head Airbags",

                                "classCode": "93",

                                "classCodeDescription": "Large Utility",

                                "vmPerformanceIndicatorDescription": "Standard",

                                "tonnageIndicator": "13",

                                "tonnageIndicatorDescription": "3.25 tons (06001 to 06500 lbs)",

                                "antiLockBrakes": "S",

                                "antiLockBrakesDescription": "Anti-Lock Brakes are standard equipment",

                                "antiTheftIndicator": "P",

                                "antiTheftIndicatorDescription": "Passive Disabling",

                                "electronicStabilityControl": "S",

                                "electronicStabilityControlDescription": "Electronic Stability Control is standard equipment",

                                "daytimeRunningLightIndicator": "S",

                                "daytimeRunningLightIndicatorDescription": "Daytime Running Lights Standard Equipment",

                                "circularNumber": "1010",

                                "recordType": "S",

                                "priceNewSymbol\_27SymbolTable\_OnePosition": "N",

                                "priceNewSymbol\_27SymbolTable\_TwoPositions": "20",

                                "priceNew\_Min": "33001.00",

                                "priceNew\_Max": "36000.99",

                                "physicalDamage": {

                                    "combinedVSRSymbol\_OnePosition": "E",

                                    "combinedVSRSymbol\_TwoPositions": "12"

                                }

                            }

                        \]

                    },

                    "riskAnalyzer": {

                        "vehicles": \[

                            {

                                "vin": "1GK\&R237&8",

                                "modelYear": "2008",

                                "distributionDate": "2212",

                                "restraint": "R",

                                "antiLockBrakes": "S",

                                "engineCylinders": "6",

                                "make": "GMC",

                                "basicModelName": "ACADIA",

                                "bodyStyle": "UTL4X24D",

                                "engineSize": "3.6",

                                "electronicStabilityControl": "S",

                                "tonnageIndicator": "13",

                                "payloadCapacity": "1678",

                                "fullModelName": "ACADIA SLT1",

                                "daytimeRunningLightIndicator": "S",

                                "wheelbase": "118.9",

                                "classCode": "93",

                                "antiTheftIndicator": "P",

                                "curbWeight": "4722",

                                "grossVehicleWeight": "6400",

                                "height": "69.9",

                                "horsepower": "275",

                                "ncicCode": "GMC",

                                "chassis": "U",

                                "length": "200.7",

                                "width": "78.2",

                                "baseMSRP": "34270",

                                "specialHandlingIndicator": "N",

                                "interimIndicator": "N",

                                "releaseDate": "2303",

                                "physicalDamage": {

                                    "riskAnalyzerCollisionIndicatedSymbol": "DJ",

                                    "riskAnalyzerComprehensiveIndicatedSymbol": "CM",

                                    "riskAnalyzerCollisionRatingSymbol": "DJ",

                                    "riskAnalyzerComprehensiveRatingSymbol": "CM",

                                    "riskAnalyzerComprehensiveNonGlassRatingSymbol": "CN",

                                    "riskAnalyzerCollisionCappingIndicator": "N",

                                    "riskAnalyzerComprehensiveCappingIndicator": "N",

                                    "riskAnalyzerComprehensiveNonGlassCappingIndicator": "N",

                                    "riskAnalyzerComprehensiveNonGlassIndicatedSymbol": "CN"

                                },

                                "liability": {

                                    "riskAnalyzerMedicalPaymentsIndicatedSymbol": "GE",

                                    "riskAnalyzerPersonalInjuryProtectionIndicatedSymbol": "FK",

                                    "riskAnalyzerSingleLimitIndicatedSymbol": "KK",

                                    "riskAnalyzerBodilyInjuryRatingSymbol": "KL",

                                    "riskAnalyzerPropertyDamageRatingSymbol": "LK",

                                    "riskAnalyzerMedicalPaymentsRatingSymbol": "GE",

                                    "riskAnalyzerPersonalInjuryProtectionRatingSymbol": "FK",

                                    "riskAnalyzerSingleLimitRatingSymbol": "KK",

                                    "riskAnalyzerBodilyInjuryCappingIndicator": "N",

                                    "riskAnalyzerPropertyDamageCappingIndicator": "N",

                                    "riskAnalyzerMedicalPaymentsCappingIndicator": "N",

                                    "riskAnalyzerPersonalInjuryProtectionCappingIndicator": "N",

                                    "riskAnalyzerBodilyInjuryIndicatedSymbol": "KL",

                                    "riskAnalyzerPropertyDamageIndicatedSymbol": "LK",

                                    "riskAnalyzerSingleLimitCappingIndicator": "N"

                                }

                            }

                        \]

                    }

                }

            \],

            "claimActivityPredictor": {

                "capIndicator": "Y",

                "numberOfClaims": "2"

            },

            "claims": \[

                {

                    "claimReferenceNumber": "4QA00526856",

                    "carrierClaimNumber": "VRLSAP20181002102",

                    "matchReasons": \[

                        {

                            "code": "V",

                            "description": "VIN Search Type"

                        },

                        {

                            "code": "N",

                            "description": "Name and Date of Birth Search Type"

                        }

                    \],

                    "atFaultIndicator": {

                        "code": "N",

                        "description": "Insured not at fault"

                    },

                    "insurer": {

                        "name": "INSURANCE SERVICES OFFICE, INC",

                        "ambest": "00001"

                    },

                    "policyType": {

                        "code": "PAPP",

                        "description": "Personal Auto"

                    },

                    "originalInceptionDate": "20221001",

                    "expirationDate": "20241001",

                    "matchByInputDriverNumber": "2",

                    "subjects": \[

                        {

                            "sequence": "2",

                            "givenName": "DOUGLAS",

                            "middleName": "J",

                            "surname": "BONZHEIM",

                            "roleInClaim": {

                                "code": "IN",

                                "description": "Insured"

                            }

                        },

                        {

                            "sequence": "2",

                            "givenName": "DOUGLAS",

                            "middleName": "J",

                            "surname": "BONZHEIM",

                            "roleInClaim": {

                                "code": "SA",

                                "description": "Insured Driver Same as Insured"

                            }

                        },

                        {

                            "sequence": "0",

                            "givenName": "ELISA",

                            "middleName": "M",

                            "surname": "ALMADA",

                            "roleInClaim": {

                                "code": "CL",

                                "description": "Claimant"

                            }

                        },

                        {

                            "sequence": "0",

                            "givenName": "KATY",

                            "surname": "PERRY",

                            "roleInClaim": {

                                "code": "CD",

                                "description": "Claimant Driver"

                            }

                        }

                    \],

                    "lossInformation": {

                        "lossDate": "20230115",

                        "lossTime": "0000",

                        "losses": \[

                            {

                                "coverageType": {

                                    "code": "LIAB",

                                    "description": "Liability"

                                },

                                "lossType": {

                                    "code": "BI",

                                    "description": "Body injury"

                                },

                                "dispositionStatus": {

                                    "code": "C",

                                    "description": "Closed"

                                },

                                "amount": "2000",

                                "claimStandardizationCode": "N02EPA308071U111"

                            }

                        \]

                    },

                    "claimStandardizationCode": "N02EPA308071U111",

                    "vehicles": \[

                        {

                            "make": "GENERAL MOTORS CORP",

                            "model": "ACADIA",

                            "year": "2008",

                            "vin": "1GKER23788J291227",

                            "catastrophes": \[\]

                        }

                    \]

                },

                {

                    "claimReferenceNumber": "3IA00527548",

                    "carrierClaimNumber": "VRLSAP20181002101",

                    "matchReasons": \[

                        {

                            "code": "V",

                            "description": "VIN Search Type"

                        },

                        {

                            "code": "Y",

                            "description": "Policy Number search"

                        },

                        {

                            "code": "N",

                            "description": "Name and Date of Birth Search Type"

                        },

                        {

                            "code": "A",

                            "description": "Name and Address Search Type"

                        }

                    \],

                    "atFaultIndicator": {

                        "code": "Y",

                        "description": "Insured at Fault"

                    },

                    "insurer": {

                        "name": "INSURANCE SERVICES OFFICE, INC",

                        "ambest": "00001"

                    },

                    "policyNumber": "VRSKLSP201810021001",

                    "policyType": {

                        "code": "PAPP",

                        "description": "Personal Auto"

                    },

                    "originalInceptionDate": "20200105",

                    "expirationDate": "20240105",

                    "matchByInputDriverNumber": "2",

                    "subjects": \[

                        {

                            "sequence": "2",

                            "givenName": "DOUGLAS",

                            "middleName": "J",

                            "surname": "BONZHEIM",

                            "roleInClaim": {

                                "code": "IN",

                                "description": "Insured"

                            }

                        },

                        {

                            "sequence": "2",

                            "givenName": "DOUGLAS",

                            "middleName": "J",

                            "surname": "BONZHEIM",

                            "roleInClaim": {

                                "code": "SA",

                                "description": "Insured Driver Same as Insured"

                            }

                        }

                    \],

                    "lossInformation": {

                        "lossDate": "20221225",

                        "lossTime": "0000",

                        "losses": \[

                            {

                                "coverageType": {

                                    "code": "UM",

                                    "description": "Uninsured Motorist"

                                },

                                "lossType": {

                                    "code": "UMPD",

                                    "description": "Uninsured Motorist Property Damage"

                                },

                                "dispositionStatus": {

                                    "code": "C",

                                    "description": "Closed"

                                },

                                "amount": "2000",

                                "claimStandardizationCode": "Y12JPA309070U000"

                            }

                        \]

                    },

                    "claimStandardizationCode": "Y12JPA309070U000",

                    "vehicles": \[

                        {

                            "make": "GENERAL MOTORS CORP",

                            "model": "ACADIA",

                            "year": "2008",

                            "vin": "1GKER23788J291227",

                            "catastrophes": \[\]

                        }

                    \]

                }

            \]

        },

        "dataSources": {

            "riskCheckPointOfSaleReport": {

                "header": {

                    "transactionId": "4f1a0fc2-ba0c-48dc-a3bc-93ae84cd62f1",

                    "quoteback": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57"

                },

                "body": {

                    "statusCode": 200,

                    "scoreSummary": {

                        "riskGroup": "VERY HIGH",

                        "scoreColor": "RED",

                        "totalScore": "3588",

                        "isCRAWarning": false,

                        "isFraudIndicator": false,

                        "scoreDecile": {

                            "code": "8",

                            "description": "3500 to 3999"

                        }

                    },

                    "scoreDetails": \[

                        {

                            "entityType": "Subject",

                            "entityNumber": "1",

                            "reasonCodeDetails": \[

                                {

                                    "reason": {

                                        "code": "ID-1.11",

                                        "description": "No identity located or poor match on primary data source."

                                    },

                                    "actionMessage": "Ask for Drivers License and Utility Bill"

                                },

                                {

                                    "reason": {

                                        "code": "ID-1.12",

                                        "description": "Social Security Number not validated."

                                    },

                                    "actionMessage": "Ask for Drivers License and Utility Bill"

                                },

                                {

                                    "reason": {

                                        "code": "ID-1.13",

                                        "description": "Date of Birth not validated."

                                    },

                                    "actionMessage": "Ask for Drivers License  "

                                },

                                {

                                    "reason": {

                                        "code": "ID-1.31",

                                        "description": "Input Address(es), including current and former, did not match to any of the addresses contained in the primary data source."

                                    },

                                    "actionMessage": "Ask for Utility Bill"

                                },

                                {

                                    "reason": {

                                        "code": "AG-2.17",

                                        "description": "Input Address(es) including current and former did not match to any of the addresses contained in the primary data source."

                                    },

                                    "actionMessage": "Ask for Utility Bill"

                                }

                            \]

                        },

                        {

                            "entityType": "Vehicle",

                            "entityNumber": "1",

                            "reasonCodeDetails": \[

                                {

                                    "reason": {

                                        "code": "AG-2.22",

                                        "description": "Vehicle has out of state Registration.  "

                                    },

                                    "actionMessage": "Take No Action"

                                },

                                {

                                    "reason": {

                                        "code": "AO-5.01",

                                        "description": "Vehicle is not owned by Policy Holder or any Driver on the Policy."

                                    },

                                    "actionMessage": "Ask for Vehicle Registration"

                                }

                            \]

                        },

                        {

                            "entityType": "Vehicle",

                            "entityNumber": "2",

                            "reasonCodeDetails": \[

                                {

                                    "reason": {

                                        "code": "AG-2.22",

                                        "description": "Vehicle has out of state Registration.  "

                                    },

                                    "actionMessage": "Take No Action"

                                },

                                {

                                    "reason": {

                                        "code": "AO-5.01",

                                        "description": "Vehicle is not owned by Policy Holder or any Driver on the Policy."

                                    },

                                    "actionMessage": "Ask for Vehicle Registration"

                                }

                            \]

                        },

                        {

                            "entityType": "Vehicle",

                            "entityNumber": "3",

                            "reasonCodeDetails": \[

                                {

                                    "reason": {

                                        "code": "AG-2.22",

                                        "description": "Vehicle has out of state Registration.  "

                                    },

                                    "actionMessage": "Take No Action"

                                },

                                {

                                    "reason": {

                                        "code": "AO-5.01",

                                        "description": "Vehicle is not owned by Policy Holder or any Driver on the Policy."

                                    },

                                    "actionMessage": "Ask for Vehicle Registration"

                                },

                                {

                                    "reason": {

                                        "code": "MI-7.01",

                                        "description": "The vehicle has a salvage, flood or junk title"

                                    },

                                    "actionMessage": "Ask for Vehicle Registration"

                                }

                            \]

                        },

                        {

                            "entityType": "Vehicle",

                            "entityNumber": "4",

                            "reasonCodeDetails": \[

                                {

                                    "reason": {

                                        "code": "AG-2.22",

                                        "description": "Vehicle has out of state Registration.  "

                                    },

                                    "actionMessage": "Take No Action"

                                },

                                {

                                    "reason": {

                                        "code": "AO-5.01",

                                        "description": "Vehicle is not owned by Policy Holder or any Driver on the Policy."

                                    },

                                    "actionMessage": "Ask for Vehicle Registration"

                                }

                            \]

                        }

                    \],

                    "address": {

                        "addressType": "Standardized",

                        "street1": "7827 Adelaide Loop",

                        "city": "New Port Richey",

                        "stateCode": "FL",

                        "zip": "346552733",

                        "countyName": "Pasco",

                        "fipsCountyCd": "101",

                        "dpvFootnote": "AABB",

                        "recordType": "S",

                        "hygieneError": "AS01",

                        "dpvVacant": "N"

                    },

                    "householdInformation": {

                        "youths11to15": "4",

                        "youths16to17": "4",

                        "dwellingType": "S",

                        "homeOwner": "T",

                        "lengthofResidence": "2",

                        "householdEducation": "5",

                        "sohoIndicatorHousehold": "Y",

                        "householdSize": "5",

                        "netWorth": "B"

                    },

                    "subjects": \[

                        {

                            "sequence": "1",

                            "source": "Secondary",

                            "givenName": "Yuki",

                            "surname": "BONZHEIM",

                            "dob": "19900311",

                            "gender": "M",

                            "maritalStatus": "S",

                            "matchType": "N",

                            "verificationDate": "20220715",

                            "verificationRange": "2",

                            "driverAssuranceScore": "D1",

                            "internalDriverCode": "7"

                        },

                        {

                            "sequence": "2",

                            "source": "Secondary",

                            "givenName": "DOUGLAS",

                            "middleName": "J",

                            "surname": "BONZHEIM",

                            "dob": "19760101",

                            "gender": "M",

                            "maritalStatus": "S",

                            "matchType": "N",

                            "verificationDate": "20220715",

                            "verificationRange": "2",

                            "driverAssuranceScore": "D1",

                            "internalDriverCode": "7"

                        },

                        {

                            "sequence": "3",

                            "source": "Secondary",

                            "givenName": "Lorna",

                            "middleName": "P",

                            "surname": "BONZHEIM",

                            "dob": "20030923",

                            "gender": "M",

                            "maritalStatus": "M",

                            "matchType": "N",

                            "verificationDate": "20220315",

                            "verificationRange": "2",

                            "driverAssuranceScore": "D1",

                            "internalDriverCode": "7"

                        },

                        {

                            "sequence": "4",

                            "source": "Secondary",

                            "givenName": "Rhett",

                            "middleName": "R",

                            "surname": "BONZHEIM",

                            "dob": "19900720",

                            "gender": "F",

                            "maritalStatus": "S",

                            "matchType": "N",

                            "verificationDate": "20220815",

                            "verificationRange": "2",

                            "driverAssuranceScore": "D1",

                            "internalDriverCode": "7"

                        },

                        {

                            "sequence": "5",

                            "source": "Secondary",

                            "givenName": "Markus",

                            "middleName": "G",

                            "surname": "BONZHEIM",

                            "dob": "20010311",

                            "gender": "M",

                            "maritalStatus": "S",

                            "matchType": "N",

                            "verificationDate": "20220315",

                            "verificationRange": "2",

                            "driverAssuranceScore": "D1",

                            "internalDriverCode": "7"

                        },

                        {

                            "sequence": "6",

                            "source": "Secondary",

                            "givenName": "Mindi",

                            "middleName": "H",

                            "surname": "BONZHEIM",

                            "dob": "19901113",

                            "gender": "F",

                            "maritalStatus": "S",

                            "matchType": "N",

                            "verificationDate": "20220815",

                            "verificationRange": "2",

                            "driverAssuranceScore": "D1",

                            "internalDriverCode": "7"

                        }

                    \],

                    "vehicles": \[

                        {

                            "sequence": "1",

                            "vinMatch": "Y",

                            "dataSource": "GOV",

                            "validVINIndicator": "Y",

                            "vinChangeIndicator": "N",

                            "vin": "1G5CT18B5F8530675",

                            "vehicleTypeCode": "T",

                            "vehicleTypeDesc": "Truck",

                            "modelYear": "1985",

                            "make": "GMC",

                            "makeDesc": "GMC",

                            "model": "S15",

                            "bodyStyleCode": "UT",

                            "bodyStyleDesc": "Sport Utility Vehicle",

                            "stateOfRegistration": "CO",

                            "transactionDate": "20060119",

                            "expirationDate": "20211212",

                            "plateTypeCode": "Z",

                            "plateTypeDesc": "Regular",

                            "licensePlateNumber": "112MPE",

                            "isBranded": false,

                            "leaseInd": "N",

                            "nameCode1": "A",

                            "nameCodeDesc1": "Owner",

                            "nameTitleCode1": "3",

                            "nameTitleDesc1": "MS",

                            "registeredOwnerName": {

                                "givenName": "RHONDA",

                                "middleName": "R",

                                "surname": "GARCILASCO"

                            },

                            "address": {

                                "addressType": "S",

                                "street1": "4341 W CENTER AVE APT B",

                                "city": "DENVER",

                                "stateCode": "CO",

                                "zip": "80219"

                            }

                        },

                        {

                            "sequence": "2",

                            "vinMatch": "Y",

                            "dataSource": "GOV",

                            "validVINIndicator": "Y",

                            "vinChangeIndicator": "N",

                            "vin": "3GNFK16T9YG218125",

                            "vehicleTypeCode": "T",

                            "vehicleTypeDesc": "Truck",

                            "modelYear": "2000",

                            "make": "CHE",

                            "makeDesc": "CHEVROLET",

                            "model": "SUBURBAN",

                            "bodyStyleCode": "UT",

                            "bodyStyleDesc": "Sport Utility Vehicle",

                            "stateOfRegistration": "KY",

                            "transactionDate": "20101203",

                            "expirationDate": "20210601",

                            "plateTypeCode": "Z",

                            "plateTypeDesc": "Regular",

                            "licensePlateNumber": "1KMC11",

                            "isBranded": false,

                            "leaseInd": "N",

                            "nameCode1": "A",

                            "nameCodeDesc1": "Owner",

                            "nameTitleCode1": "1",

                            "nameTitleDesc1": "MR",

                            "registeredOwnerName": {

                                "givenName": "JOHNSON",

                                "surname": "JONNIE"

                            },

                            "address": {

                                "addressType": "S",

                                "street1": "2700 NEW HOLD RD",

                                "city": "PADUCAH",

                                "stateCode": "KY",

                                "zip": "42001"

                            }

                        },

                        {

                            "sequence": "3",

                            "vinMatch": "Y",

                            "dataSource": "GOV",

                            "validVINIndicator": "Y",

                            "vinChangeIndicator": "N",

                            "vin": "1HGCM56306A148752",

                            "vehicleTypeCode": "P",

                            "vehicleTypeDesc": "Passenger Car",

                            "modelYear": "2006",

                            "make": "HON",

                            "makeDesc": "HONDA",

                            "model": "ACCORD",

                            "bodyStyleCode": "SD",

                            "bodyStyleDesc": "Sedan",

                            "stateOfRegistration": "CO",

                            "transactionDate": "20091028",

                            "expirationDate": "20211231",

                            "plateTypeCode": "Z",

                            "plateTypeDesc": "Regular",

                            "licensePlateNumber": "403OAK",

                            "isBranded": true,

                            "brandedTitleState1": "CO",

                            "brandedTitleDate1": "20150815",

                            "brandedTitleCode1": "H",

                            "brandedTitleDesc1": "REBUILT",

                            "brandedTitleState2": "OR",

                            "brandedTitleDate2": "20150615",

                            "brandedTitleCode2": "J",

                            "brandedTitleDesc2": "SALVAGE",

                            "leaseInd": "N",

                            "nameCode1": "A",

                            "nameCodeDesc1": "Owner",

                            "nameTitleCode1": "1",

                            "nameTitleDesc1": "MR",

                            "registeredOwnerName": {

                                "givenName": "JAMES",

                                "middleName": "W",

                                "surname": "LEYDEN"

                            },

                            "address": {

                                "addressType": "S",

                                "street1": "10558 PAINT PL",

                                "city": "LITTLETON",

                                "stateCode": "CO",

                                "zip": "80125"

                            }

                        },

                        {

                            "sequence": "4",

                            "vinMatch": "Y",

                            "dataSource": "GOV",

                            "validVINIndicator": "Y",

                            "vinChangeIndicator": "N",

                            "vin": "1GKER23788J291227",

                            "vehicleTypeCode": "T",

                            "vehicleTypeDesc": "Truck",

                            "modelYear": "2008",

                            "make": "GMC",

                            "makeDesc": "GMC",

                            "model": "ACADIA",

                            "bodyStyleCode": "UT",

                            "bodyStyleDesc": "Sport Utility Vehicle",

                            "stateOfRegistration": "TX",

                            "transactionDate": "20090801",

                            "expirationDate": "20210331",

                            "plateTypeCode": "Z",

                            "plateTypeDesc": "Regular",

                            "licensePlateNumber": "JRR530",

                            "isBranded": false,

                            "leaseInd": "N",

                            "nameCode1": "A",

                            "nameCodeDesc1": "Owner",

                            "nameTitleCode1": "1",

                            "nameTitleDesc1": "MR",

                            "registeredOwnerName": {

                                "givenName": "ROBERT",

                                "middleName": "J",

                                "surname": "PATTERSON"

                            },

                            "address": {

                                "addressType": "S",

                                "street1": "121 CHAPEL HILL DR",

                                "city": "PROSPER",

                                "stateCode": "TX",

                                "zip": "75078"

                            }

                        }

                    \],

                    "creditHeader": {

                        "code": "N",

                        "description": "No credit header (e.g. no SSN)"

                    },

                    "additionalData": \[

                        {

                            "key": "Youth16-17",

                            "value": "4"

                        },

                        {

                            "key": "Y",

                            "value": "VehOwnrExp"

                        }

                    \],

                    "customElements": \[\]

                }

            },

            "coverageVerifierReport": {

                "header": {

                    "transactionId": "e324f828-a192-4bb7-b75a-8968617c0b44",

                    "quoteback": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57"

                },

                "body": {

                    "policies": \[

                        {

                            "detail": {

                                "policyInformation": {

                                    "policyType": {

                                        "code": "AU",

                                        "description": "Auto"

                                    },

                                    "termEffectiveDate": "20230105",

                                    "termExpirationDate": "20240105",

                                    "policyHolders": \[

                                        {

                                            "givenName": "DOUGLAS",

                                            "middleName": "J",

                                            "surname": "BONZHEIM",

                                            "dob": "19760101",

                                            "dlNumber": "M888777666555",

                                            "dlState": "FL"

                                        },

                                        {

                                            "givenName": "LORNA",

                                            "middleName": "P",

                                            "surname": "BONZHEIM",

                                            "dob": "20030923",

                                            "dlNumber": "B640693682100",

                                            "dlState": "FL"

                                        }

                                    \],

                                    "phoneNumbers": \[

                                        {

                                            "phoneType": "H",

                                            "number": "1112223335",

                                            "extension": "0000"

                                        }

                                    \]

                                },

                                "subjects": \[

                                    {

                                        "driverSequenceId": "0",

                                        "givenName": "DOUGLAS",

                                        "middleName": "J",

                                        "surname": "BONZHEIM",

                                        "dob": "19760101",

                                        "ssn": "491487807",

                                        "gender": "M",

                                        "maritalStatus": "M",

                                        "dlNumber": "M888777666555",

                                        "dlState": "FL",

                                        "relationToPolicyHolder": {

                                            "code": "PP",

                                            "description": "Primary Policyholder"

                                        },

                                        "relationToInsured": {

                                            "code": "I",

                                            "description": "Insured"

                                        },

                                        "fromDate": "20230105",

                                        "toDate": "20240105"

                                    },

                                    {

                                        "driverSequenceId": "0",

                                        "givenName": "LORNA",

                                        "middleName": "P",

                                        "surname": "BONZHEIM",

                                        "dob": "20030923",

                                        "gender": "F",

                                        "maritalStatus": "M",

                                        "dlNumber": "B640693682100",

                                        "dlState": "FL",

                                        "relationToPolicyHolder": {

                                            "code": "SP",

                                            "description": "Secondary Policyholder"

                                        },

                                        "relationToInsured": {

                                            "code": "S",

                                            "description": "Spouse"

                                        },

                                        "fromDate": "20230105",

                                        "toDate": "20240105"

                                    },

                                    {

                                        "driverSequenceId": "0",

                                        "givenName": "MALIA",

                                        "middleName": "R",

                                        "surname": "BONZHEIM",

                                        "dob": "19990120",

                                        "gender": "F",

                                        "maritalStatus": "S",

                                        "dlNumber": "S420665834256",

                                        "dlState": "FL",

                                        "relationToPolicyHolder": {

                                            "code": "LD",

                                            "description": "Listed Driver"

                                        },

                                        "fromDate": "20230105",

                                        "toDate": "20240105"

                                    },

                                    {

                                        "driverSequenceId": "0",

                                        "givenName": "MARKUS",

                                        "middleName": "G",

                                        "surname": "BONZHEIM",

                                        "dob": "20010311",

                                        "gender": "F",

                                        "maritalStatus": "S",

                                        "dlNumber": "P420665934225",

                                        "dlState": "FL",

                                        "relationToPolicyHolder": {

                                            "code": "LD",

                                            "description": "Listed Driver"

                                        },

                                        "fromDate": "20230105",

                                        "toDate": "20240105"

                                    },

                                    {

                                        "driverSequenceId": "0",

                                        "givenName": "MINDI",

                                        "middleName": "H",

                                        "surname": "BONZHEIM",

                                        "dob": "19901113",

                                        "gender": "F",

                                        "maritalStatus": "S",

                                        "dlNumber": "R420622534333",

                                        "dlState": "FL",

                                        "relationToPolicyHolder": {

                                            "code": "LD",

                                            "description": "Listed Driver"

                                        },

                                        "fromDate": "20230105",

                                        "toDate": "20240105"

                                    },

                                    {

                                        "driverSequenceId": "0",

                                        "givenName": "RHETT",

                                        "middleName": "K",

                                        "surname": "BONZHEIM",

                                        "dob": "19900720",

                                        "gender": "F",

                                        "maritalStatus": "S",

                                        "dlNumber": "L420625834362",

                                        "dlState": "FL",

                                        "relationToPolicyHolder": {

                                            "code": "LD",

                                            "description": "Listed Driver"

                                        },

                                        "fromDate": "20230105",

                                        "toDate": "20240105"

                                    },

                                    {

                                        "driverSequenceId": "1",

                                        "givenName": "YUKI",

                                        "middleName": "R",

                                        "surname": "BONZHEIM",

                                        "dob": "19900311",

                                        "gender": "M",

                                        "maritalStatus": "S",

                                        "dlNumber": "T520103597610",

                                        "dlState": "FL",

                                        "relationToPolicyHolder": {

                                            "code": "LD",

                                            "description": "Listed Driver"

                                        },

                                        "relationToInsured": {

                                            "code": "O",

                                            "description": "Other Related"

                                        },

                                        "fromDate": "20230105",

                                        "toDate": "20240105"

                                    }

                                \],

                                "carrier": {

                                    "financialAMBEST": "99999",

                                    "name": "INSURANCE SERVICES O",

                                    "ambest": "99999",

                                    "naic": "00000"

                                },

                                "mailingAddress": {

                                    "fromDate": "20230105",

                                    "toDate": "20240105",

                                    "street1": "7827 Adelaide Loop",

                                    "city": "New Port Richey",

                                    "stateCode": "FL",

                                    "zip": "34655",

                                    "countryCode": "US"

                                },

                                "coverages": \[

                                    {

                                        "coverageType": {

                                            "code": "BINJ",

                                            "description": "Bodily Injury"

                                        },

                                        "individualLimitAmount": "40000",

                                        "occurrenceLimitAmount": "80000",

                                        "combinedSingleLimitAmount": "0",

                                        "fromDate": "20230105",

                                        "toDate": "20240105"

                                    },

                                    {

                                        "coverageType": {

                                            "code": "CBSL",

                                            "description": "CSL (BI & PD)"

                                        },

                                        "individualLimitAmount": "0",

                                        "occurrenceLimitAmount": "0",

                                        "combinedSingleLimitAmount": "80000",

                                        "fromDate": "20230105",

                                        "toDate": "20240105"

                                    },

                                    {

                                        "coverageType": {

                                            "code": "PDMG",

                                            "description": "Property Damage"

                                        },

                                        "individualLimitAmount": "20000",

                                        "occurrenceLimitAmount": "40000",

                                        "combinedSingleLimitAmount": "0",

                                        "fromDate": "20230105",

                                        "toDate": "20240105"

                                    },

                                    {

                                        "coverageType": {

                                            "code": "UMPD",

                                            "description": "Uninsured Motorist (PD)"

                                        },

                                        "individualLimitAmount": "20000",

                                        "occurrenceLimitAmount": "40000",

                                        "combinedSingleLimitAmount": "0",

                                        "fromDate": "20230105",

                                        "toDate": "20240105"

                                    },

                                    {

                                        "coverageType": {

                                            "code": "PINJ",

                                            "description": "Personal Injury"

                                        },

                                        "individualLimitAmount": "20000",

                                        "occurrenceLimitAmount": "40000",

                                        "combinedSingleLimitAmount": "0",

                                        "fromDate": "20230105",

                                        "toDate": "20240105"

                                    }

                                \],

                                "vehicles": \[

                                    {

                                        "year": "1985",

                                        "make": "GMC",

                                        "model": "UT",

                                        "vin": "1G5CT18B5F8530675",

                                        "classCode": "000000",

                                        "businessUse": "Y",

                                        "collisionDeductibleAmount": "1000",

                                        "comprehensiveDeductibleAmount": "500",

                                        "fromDate": "20230105",

                                        "toDate": "20240105",

                                        "collisionIndicator": "Y",

                                        "comprehensiveIndicator": "Y",

                                        "coverages": \[

                                            {

                                                "coverageType": {

                                                    "code": "BINJ",

                                                    "description": "Bodily Injury"

                                                },

                                                "individualLimitAmount": "40000",

                                                "occurrenceLimitAmount": "80000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "PDMG",

                                                    "description": "Property Damage"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "CBSL",

                                                    "description": "CSL (BI & PD)"

                                                },

                                                "individualLimitAmount": "0",

                                                "occurrenceLimitAmount": "0",

                                                "combinedSingleLimitAmount": "80000",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "UMPD",

                                                    "description": "Uninsured Motorist (PD)"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "PINJ",

                                                    "description": "Personal Injury"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            }

                                        \]

                                    },

                                    {

                                        "year": "2000",

                                        "make": "CHEV",

                                        "model": "K1S",

                                        "vin": "3GNFK16T9YG218125",

                                        "classCode": "000000",

                                        "businessUse": "Y",

                                        "collisionDeductibleAmount": "1000",

                                        "comprehensiveDeductibleAmount": "500",

                                        "fromDate": "20230105",

                                        "toDate": "20240105",

                                        "collisionIndicator": "Y",

                                        "comprehensiveIndicator": "Y",

                                        "coverages": \[

                                            {

                                                "coverageType": {

                                                    "code": "BINJ",

                                                    "description": "Bodily Injury"

                                                },

                                                "individualLimitAmount": "40000",

                                                "occurrenceLimitAmount": "80000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "PDMG",

                                                    "description": "Property Damage"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "CBSL",

                                                    "description": "CSL (BI & PD)"

                                                },

                                                "individualLimitAmount": "0",

                                                "occurrenceLimitAmount": "0",

                                                "combinedSingleLimitAmount": "80000",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "UMPD",

                                                    "description": "Uninsured Motorist (PD)"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "PINJ",

                                                    "description": "Personal Injury"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            }

                                        \]

                                    },

                                    {

                                        "year": "2006",

                                        "make": "HOND",

                                        "model": "ASE",

                                        "vin": "1HGCM56306A148752",

                                        "classCode": "000000",

                                        "businessUse": "N",

                                        "collisionDeductibleAmount": "1000",

                                        "comprehensiveDeductibleAmount": "500",

                                        "fromDate": "20230105",

                                        "toDate": "20240105",

                                        "collisionIndicator": "Y",

                                        "comprehensiveIndicator": "Y",

                                        "coverages": \[

                                            {

                                                "coverageType": {

                                                    "code": "BINJ",

                                                    "description": "Bodily Injury"

                                                },

                                                "individualLimitAmount": "40000",

                                                "occurrenceLimitAmount": "80000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "PDMG",

                                                    "description": "Property Damage"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "CBSL",

                                                    "description": "CSL (BI & PD)"

                                                },

                                                "individualLimitAmount": "0",

                                                "occurrenceLimitAmount": "0",

                                                "combinedSingleLimitAmount": "80000",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "UMPD",

                                                    "description": "Uninsured Motorist (PD)"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "PINJ",

                                                    "description": "Personal Injury"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            }

                                        \]

                                    },

                                    {

                                        "year": "2008",

                                        "make": "GMC",

                                        "model": "S1F",

                                        "vin": "1GKER23788J291227",

                                        "classCode": "000000",

                                        "businessUse": "Y",

                                        "collisionDeductibleAmount": "1000",

                                        "comprehensiveDeductibleAmount": "500",

                                        "fromDate": "20230105",

                                        "toDate": "20240105",

                                        "collisionIndicator": "Y",

                                        "comprehensiveIndicator": "Y",

                                        "coverages": \[

                                            {

                                                "coverageType": {

                                                    "code": "BINJ",

                                                    "description": "Bodily Injury"

                                                },

                                                "individualLimitAmount": "40000",

                                                "occurrenceLimitAmount": "80000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "PDMG",

                                                    "description": "Property Damage"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "CBSL",

                                                    "description": "CSL (BI & PD)"

                                                },

                                                "individualLimitAmount": "0",

                                                "occurrenceLimitAmount": "0",

                                                "combinedSingleLimitAmount": "80000",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "UMPD",

                                                    "description": "Uninsured Motorist (PD)"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "PINJ",

                                                    "description": "Personal Injury"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20230105",

                                                "toDate": "20240105"

                                            }

                                        \]

                                    }

                                \]

                            },

                            "history": {

                                "policyInformations": \[

                                    {

                                        "policyType": {

                                            "code": "AU",

                                            "description": "Auto"

                                        },

                                        "policyHolders": \[

                                            {

                                                "givenName": "DOUGLAS",

                                                "middleName": "J",

                                                "surname": "BONZHEIM",

                                                "dob": "19760101",

                                                "dlNumber": "M888777666555",

                                                "dlState": "FL"

                                            },

                                            {

                                                "givenName": "LORNA",

                                                "middleName": "P",

                                                "surname": "BONZHEIM",

                                                "dob": "20030923",

                                                "dlNumber": "B640693682100",

                                                "dlState": "FL"

                                            }

                                        \],

                                        "phoneNumbers": \[

                                            {

                                                "phoneType": "H",

                                                "number": "1112223335",

                                                "extension": "0000"

                                            }

                                        \],

                                        "fromDate": "20200105",

                                        "toDate": "20230105"

                                    }

                                \],

                                "subjects": \[

                                    {

                                        "driverSequenceId": "0",

                                        "givenName": "DOUGLAS",

                                        "middleName": "J",

                                        "surname": "BONZHEIM",

                                        "dob": "19760101",

                                        "ssn": "491487807",

                                        "gender": "M",

                                        "maritalStatus": "M",

                                        "dlNumber": "M888777666555",

                                        "dlState": "FL",

                                        "relationToPolicyHolder": {

                                            "code": "PP",

                                            "description": "Primary Policyholder"

                                        },

                                        "relationToInsured": {

                                            "code": "I",

                                            "description": "Insured"

                                        },

                                        "fromDate": "20220105",

                                        "toDate": "20230105"

                                    },

                                    {

                                        "driverSequenceId": "0",

                                        "givenName": "LORNA",

                                        "middleName": "P",

                                        "surname": "BONZHEIM",

                                        "dob": "20030923",

                                        "gender": "F",

                                        "maritalStatus": "M",

                                        "dlNumber": "B640693682100",

                                        "dlState": "FL",

                                        "relationToPolicyHolder": {

                                            "code": "SP",

                                            "description": "Secondary Policyholder"

                                        },

                                        "relationToInsured": {

                                            "code": "S",

                                            "description": "Spouse"

                                        },

                                        "fromDate": "20220105",

                                        "toDate": "20230105"

                                    },

                                    {

                                        "driverSequenceId": "1",

                                        "givenName": "YUKI",

                                        "middleName": "R",

                                        "surname": "BONZHEIM",

                                        "dob": "19900311",

                                        "gender": "M",

                                        "maritalStatus": "S",

                                        "dlNumber": "T520103597610",

                                        "dlState": "FL",

                                        "relationToPolicyHolder": {

                                            "code": "LD",

                                            "description": "Listed Driver"

                                        },

                                        "relationToInsured": {

                                            "code": "O",

                                            "description": "Other Related"

                                        },

                                        "fromDate": "20220105",

                                        "toDate": "20230105"

                                    },

                                    {

                                        "driverSequenceId": "0",

                                        "givenName": "DOUGLAS",

                                        "middleName": "J",

                                        "surname": "BONZHEIM",

                                        "dob": "19760101",

                                        "maritalStatus": "S",

                                        "dlNumber": "T123654125803",

                                        "dlState": "FL",

                                        "relationToPolicyHolder": {

                                            "code": "PP",

                                            "description": "Primary Policyholder"

                                        },

                                        "relationToInsured": {

                                            "code": "I",

                                            "description": "Insured"

                                        },

                                        "fromDate": "20200105",

                                        "toDate": "20220105"

                                    },

                                    {

                                        "driverSequenceId": "0",

                                        "givenName": "MALIA",

                                        "middleName": "R",

                                        "surname": "BONZHEIM",

                                        "dob": "19990120",

                                        "gender": "F",

                                        "maritalStatus": "S",

                                        "dlNumber": "S420665834256",

                                        "dlState": "FL",

                                        "relationToPolicyHolder": {

                                            "code": "LD",

                                            "description": "Listed Driver"

                                        },

                                        "fromDate": "20200105",

                                        "toDate": "20230105"

                                    },

                                    {

                                        "driverSequenceId": "0",

                                        "givenName": "MARKUS",

                                        "middleName": "G",

                                        "surname": "BONZHEIM",

                                        "dob": "20010311",

                                        "gender": "F",

                                        "maritalStatus": "S",

                                        "dlNumber": "P420665934225",

                                        "dlState": "FL",

                                        "relationToPolicyHolder": {

                                            "code": "LD",

                                            "description": "Listed Driver"

                                        },

                                        "fromDate": "20200105",

                                        "toDate": "20230105"

                                    },

                                    {

                                        "driverSequenceId": "0",

                                        "givenName": "MINDI",

                                        "middleName": "H",

                                        "surname": "BONZHEIM",

                                        "dob": "19901113",

                                        "gender": "F",

                                        "maritalStatus": "S",

                                        "dlNumber": "R420622534333",

                                        "dlState": "FL",

                                        "relationToPolicyHolder": {

                                            "code": "LD",

                                            "description": "Listed Driver"

                                        },

                                        "fromDate": "20200105",

                                        "toDate": "20230105"

                                    },

                                    {

                                        "driverSequenceId": "0",

                                        "givenName": "RHETT",

                                        "middleName": "K",

                                        "surname": "BONZHEIM",

                                        "dob": "19900720",

                                        "gender": "F",

                                        "maritalStatus": "S",

                                        "dlNumber": "L420625834362",

                                        "dlState": "FL",

                                        "relationToPolicyHolder": {

                                            "code": "LD",

                                            "description": "Listed Driver"

                                        },

                                        "fromDate": "20200105",

                                        "toDate": "20230105"

                                    },

                                    {

                                        "driverSequenceId": "0",

                                        "givenName": "ALIZA",

                                        "surname": "BONZHEIM",

                                        "dob": "19800510",

                                        "gender": "F",

                                        "dlNumber": "P889515754987",

                                        "dlState": "FL",

                                        "relationToPolicyHolder": {

                                            "code": "SP",

                                            "description": "Secondary Policyholder"

                                        },

                                        "relationToInsured": {

                                            "code": "S",

                                            "description": "Spouse"

                                        },

                                        "fromDate": "20200105",

                                        "toDate": "20220105"

                                    },

                                    {

                                        "driverSequenceId": "0",

                                        "givenName": "EDGAR",

                                        "middleName": "R",

                                        "surname": "RAMIREZ",

                                        "dob": "19700501",

                                        "dlNumber": "D134241554599",

                                        "dlState": "FL",

                                        "relationToPolicyHolder": {

                                            "code": "LD",

                                            "description": "Listed Driver"

                                        },

                                        "relationToInsured": {

                                            "code": "O",

                                            "description": "Other Related"

                                        },

                                        "fromDate": "20200105",

                                        "toDate": "20220105"

                                    }

                                \],

                                "mailingAddresses": \[

                                    {

                                        "fromDate": "20200105",

                                        "toDate": "20230105",

                                        "street1": "7827 Adelaide Loop",

                                        "city": "New Port Richey",

                                        "stateCode": "FL",

                                        "zip": "34655",

                                        "countryCode": "US"

                                    }

                                \],

                                "coverages": \[

                                    {

                                        "coverageType": {

                                            "code": "BINJ",

                                            "description": "Bodily Injury"

                                        },

                                        "individualLimitAmount": "40000",

                                        "occurrenceLimitAmount": "80000",

                                        "combinedSingleLimitAmount": "0",

                                        "fromDate": "20200105",

                                        "toDate": "20230105"

                                    },

                                    {

                                        "coverageType": {

                                            "code": "CBSL",

                                            "description": "CSL (BI & PD)"

                                        },

                                        "individualLimitAmount": "0",

                                        "occurrenceLimitAmount": "0",

                                        "combinedSingleLimitAmount": "80000",

                                        "fromDate": "20220105",

                                        "toDate": "20230105"

                                    },

                                    {

                                        "coverageType": {

                                            "code": "MAPD",

                                            "description": "MASS. OPTIONAL PROPERTY DAMAGE LIAB"

                                        },

                                        "individualLimitAmount": "20000",

                                        "occurrenceLimitAmount": "40000",

                                        "combinedSingleLimitAmount": "0",

                                        "fromDate": "20200105",

                                        "toDate": "20210105"

                                    },

                                    {

                                        "coverageType": {

                                            "code": "PDMG",

                                            "description": "Property Damage"

                                        },

                                        "individualLimitAmount": "20000",

                                        "occurrenceLimitAmount": "40000",

                                        "combinedSingleLimitAmount": "0",

                                        "fromDate": "20200105",

                                        "toDate": "20230105"

                                    },

                                    {

                                        "coverageType": {

                                            "code": "PINJ",

                                            "description": "Personal Injury"

                                        },

                                        "individualLimitAmount": "20000",

                                        "occurrenceLimitAmount": "40000",

                                        "combinedSingleLimitAmount": "0",

                                        "fromDate": "20200105",

                                        "toDate": "20220105"

                                    },

                                    {

                                        "coverageType": {

                                            "code": "UMPD",

                                            "description": "Uninsured Motorist (PD)"

                                        },

                                        "individualLimitAmount": "20000",

                                        "occurrenceLimitAmount": "40000",

                                        "combinedSingleLimitAmount": "0",

                                        "fromDate": "20220105",

                                        "toDate": "20230105"

                                    },

                                    {

                                        "coverageType": {

                                            "code": "UMPD",

                                            "description": "Uninsured Motorist (PD)"

                                        },

                                        "individualLimitAmount": "20000",

                                        "occurrenceLimitAmount": "40000",

                                        "combinedSingleLimitAmount": "0",

                                        "fromDate": "20200105",

                                        "toDate": "20210105"

                                    }

                                \],

                                "vehicles": \[

                                    {

                                        "year": "1985",

                                        "make": "GMC",

                                        "model": "UT",

                                        "vin": "1G5CT18B5F8530675",

                                        "classCode": "000000",

                                        "businessUse": "Y",

                                        "collisionDeductibleAmount": "1000",

                                        "comprehensiveDeductibleAmount": "500",

                                        "fromDate": "20220105",

                                        "toDate": "20230105",

                                        "collisionIndicator": "Y",

                                        "comprehensiveIndicator": "Y",

                                        "coverages": \[

                                            {

                                                "coverageType": {

                                                    "code": "BINJ",

                                                    "description": "Bodily Injury"

                                                },

                                                "individualLimitAmount": "40000",

                                                "occurrenceLimitAmount": "80000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20220105",

                                                "toDate": "20230105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "PDMG",

                                                    "description": "Property Damage"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20220105",

                                                "toDate": "20230105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "CBSL",

                                                    "description": "CSL (BI & PD)"

                                                },

                                                "individualLimitAmount": "0",

                                                "occurrenceLimitAmount": "0",

                                                "combinedSingleLimitAmount": "80000",

                                                "fromDate": "20220105",

                                                "toDate": "20230105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "UMPD",

                                                    "description": "Uninsured Motorist (PD)"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20220105",

                                                "toDate": "20230105"

                                            }

                                        \]

                                    },

                                    {

                                        "year": "2000",

                                        "make": "CHEV",

                                        "model": "K1S",

                                        "vin": "3GNFK16T9YG218125",

                                        "classCode": "000000",

                                        "businessUse": "Y",

                                        "collisionDeductibleAmount": "1000",

                                        "comprehensiveDeductibleAmount": "500",

                                        "fromDate": "20220105",

                                        "toDate": "20230105",

                                        "collisionIndicator": "Y",

                                        "comprehensiveIndicator": "Y",

                                        "coverages": \[

                                            {

                                                "coverageType": {

                                                    "code": "BINJ",

                                                    "description": "Bodily Injury"

                                                },

                                                "individualLimitAmount": "40000",

                                                "occurrenceLimitAmount": "80000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20220105",

                                                "toDate": "20230105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "PDMG",

                                                    "description": "Property Damage"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20220105",

                                                "toDate": "20230105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "CBSL",

                                                    "description": "CSL (BI & PD)"

                                                },

                                                "individualLimitAmount": "0",

                                                "occurrenceLimitAmount": "0",

                                                "combinedSingleLimitAmount": "80000",

                                                "fromDate": "20220105",

                                                "toDate": "20230105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "UMPD",

                                                    "description": "Uninsured Motorist (PD)"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20220105",

                                                "toDate": "20230105"

                                            }

                                        \]

                                    },

                                    {

                                        "year": "2006",

                                        "make": "HOND",

                                        "model": "ASE",

                                        "vin": "1HGCM56306A148752",

                                        "classCode": "000000",

                                        "businessUse": "N",

                                        "collisionDeductibleAmount": "1000",

                                        "comprehensiveDeductibleAmount": "500",

                                        "fromDate": "20220105",

                                        "toDate": "20230105",

                                        "collisionIndicator": "Y",

                                        "comprehensiveIndicator": "Y",

                                        "coverages": \[

                                            {

                                                "coverageType": {

                                                    "code": "BINJ",

                                                    "description": "Bodily Injury"

                                                },

                                                "individualLimitAmount": "40000",

                                                "occurrenceLimitAmount": "80000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20220105",

                                                "toDate": "20230105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "PDMG",

                                                    "description": "Property Damage"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20220105",

                                                "toDate": "20230105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "CBSL",

                                                    "description": "CSL (BI & PD)"

                                                },

                                                "individualLimitAmount": "0",

                                                "occurrenceLimitAmount": "0",

                                                "combinedSingleLimitAmount": "80000",

                                                "fromDate": "20220105",

                                                "toDate": "20230105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "UMPD",

                                                    "description": "Uninsured Motorist (PD)"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20220105",

                                                "toDate": "20230105"

                                            }

                                        \]

                                    },

                                    {

                                        "year": "2008",

                                        "make": "GMC",

                                        "model": "S1F",

                                        "vin": "1GKER23788J291227",

                                        "classCode": "000000",

                                        "collisionDeductibleAmount": "1000",

                                        "comprehensiveDeductibleAmount": "500",

                                        "fromDate": "20200105",

                                        "toDate": "20220105",

                                        "collisionIndicator": "Y",

                                        "comprehensiveIndicator": "Y",

                                        "coverages": \[

                                            {

                                                "coverageType": {

                                                    "code": "BINJ",

                                                    "description": "Bodily Injury"

                                                },

                                                "individualLimitAmount": "40000",

                                                "occurrenceLimitAmount": "80000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20200105",

                                                "toDate": "20220105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "PDMG",

                                                    "description": "Property Damage"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20200105",

                                                "toDate": "20220105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "PINJ",

                                                    "description": "Personal Injury"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20200105",

                                                "toDate": "20220105"

                                            }

                                        \]

                                    },

                                    {

                                        "year": "2008",

                                        "make": "GMC",

                                        "model": "S1F",

                                        "vin": "1GKER23788J291227",

                                        "classCode": "000000",

                                        "businessUse": "Y",

                                        "collisionDeductibleAmount": "1000",

                                        "comprehensiveDeductibleAmount": "500",

                                        "fromDate": "20220105",

                                        "toDate": "20230105",

                                        "collisionIndicator": "Y",

                                        "comprehensiveIndicator": "Y",

                                        "coverages": \[

                                            {

                                                "coverageType": {

                                                    "code": "BINJ",

                                                    "description": "Bodily Injury"

                                                },

                                                "individualLimitAmount": "40000",

                                                "occurrenceLimitAmount": "80000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20220105",

                                                "toDate": "20230105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "PDMG",

                                                    "description": "Property Damage"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20220105",

                                                "toDate": "20230105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "CBSL",

                                                    "description": "CSL (BI & PD)"

                                                },

                                                "individualLimitAmount": "0",

                                                "occurrenceLimitAmount": "0",

                                                "combinedSingleLimitAmount": "80000",

                                                "fromDate": "20220105",

                                                "toDate": "20230105"

                                            },

                                            {

                                                "coverageType": {

                                                    "code": "UMPD",

                                                    "description": "Uninsured Motorist (PD)"

                                                },

                                                "individualLimitAmount": "20000",

                                                "occurrenceLimitAmount": "40000",

                                                "combinedSingleLimitAmount": "0",

                                                "fromDate": "20220105",

                                                "toDate": "20230105"

                                            }

                                        \]

                                    }

                                \],

                                "transactionInformations": \[

                                    {

                                        "transactionType": {

                                            "code": "NB",

                                            "description": "New Business"

                                        },

                                        "effectiveDate": "20200105"

                                    },

                                    {

                                        "transactionType": {

                                            "code": "RW",

                                            "description": "Renewal"

                                        },

                                        "effectiveDate": "20210105"

                                    },

                                    {

                                        "transactionType": {

                                            "code": "RW",

                                            "description": "Renewal"

                                        },

                                        "effectiveDate": "20220105"

                                    }

                                \]

                            },

                            "policyNumber": "VRSKLSP201810021001",

                            "policyStatus": "INFORCE",

                            "policyReportedDate": "20230213",

                            "inceptionDate": "20170301",

                            "lastReportedTermEffectiveDate": "20230105",

                            "lastReportedTermExpirationDate": "20240105",

                            "numberOfCancellations": "0",

                            "numberOfRenewals": "3",

                            "matchBasisInformation": {

                                "matchScore": "100",

                                "searchType": {

                                    "code": "P",

                                    "description": "Person"

                                },

                                "matchReasons": \[

                                    "NAME IS IDENTICAL",

                                    "ADDRESS IS IDENTICAL",

                                    "ZIP IS IDENTICAL"

                                \]

                            }

                        }

                    \],

                    "coverageLapseInformation": \[

                        {

                            "coverageIntervals": \[

                                {

                                    "carrier": {

                                        "financialAMBEST": "99999",

                                        "name": "INSURANCE SERVICES O",

                                        "ambest": "99999",

                                        "naic": "00000"

                                    },

                                    "startDate": "20220105",

                                    "endDate": "20240105",

                                    "numberOfCoverageDays": "628",

                                    "hasBreakFromPriorCoverage": "NA",

                                    "numberOfLapseDays": "0"

                                }

                            \],

                            "givenName": "YUKI",

                            "surname": "BONZHEIM",

                            "inputDriverSequenceNumber": "1",

                            "hasPossibleLapse": "N",

                            "isCurrentInforceCoverage": "Y"

                        }

                    \]

                }

            },

            "aPlusAutoReport": {

                "header": {

                    "quoteback": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57",

                    "transactionId": "2f77ff29-81db-4fba-885f-7186f70b5e34"

                },

                "body": {

                    "claimActivityPredictor": {

                        "capIndicator": "Y",

                        "numberOfClaims": "2"

                    },

                    "claims": \[

                        {

                            "claimReferenceNumber": "4QA00526856",

                            "carrierClaimNumber": "VRLSAP20181002102",

                            "matchReasons": \[

                                {

                                    "code": "V",

                                    "description": "VIN Search Type"

                                },

                                {

                                    "code": "N",

                                    "description": "Name and Date of Birth Search Type"

                                }

                            \],

                            "atFaultIndicator": {

                                "code": "N",

                                "description": "Insured not at fault"

                            },

                            "insurer": {

                                "companyId": "Z995",

                                "officeId": "00000",

                                "name": "INSURANCE SERVICES OFFICE, INC",

                                "ambest": "00001",

                                "address": {

                                    "street1": "545 WASHINGTON BLVD",

                                    "city": "JERSEY CITY",

                                    "stateCode": "NJ",

                                    "zip": "07310",

                                    "countryCode": "US"

                                },

                                "phone": "7323880332"

                            },

                            "policy": {

                                "policyType": {

                                    "code": "PAPP",

                                    "description": "Personal Auto"

                                },

                                "originalInceptionDate": "20221001",

                                "expirationDate": "20241001"

                            },

                            "matchByInputDriverNumber": "2",

                            "subjects": \[

                                {

                                    "indvidualOrBusinessIndicator": "I",

                                    "givenName": "DOUGLAS",

                                    "surname": "BONZHEIM",

                                    "middleName": "J",

                                    "dob": "19760101",

                                    "dlNumber": "D852424151335",

                                    "dlState": "FL",

                                    "roleInClaim": {

                                        "code": "IN",

                                        "description": "Insured"

                                    },

                                    "address": {

                                        "street1": "329 WOODSTEAD LN",

                                        "city": "LONGWOOD",

                                        "stateCode": "FL",

                                        "zip": "32779"

                                    },

                                    "sequenceInInputDrivers": "2"

                                },

                                {

                                    "indvidualOrBusinessIndicator": "I",

                                    "givenName": "DOUGLAS",

                                    "surname": "BONZHEIM",

                                    "middleName": "J",

                                    "dob": "19760101",

                                    "dlNumber": "D852424151335",

                                    "dlState": "FL",

                                    "roleInClaim": {

                                        "code": "SA",

                                        "description": "Insured Driver Same as Insured"

                                    },

                                    "address": {

                                        "street1": "329 WOODSTEAD LN",

                                        "city": "LONGWOOD",

                                        "stateCode": "FL",

                                        "zip": "32779"

                                    },

                                    "sequenceInInputDrivers": "2"

                                },

                                {

                                    "indvidualOrBusinessIndicator": "I",

                                    "givenName": "ELISA",

                                    "surname": "ALMADA",

                                    "middleName": "M",

                                    "dob": "19820501",

                                    "gender": "M",

                                    "dlNumber": "V910235269825",

                                    "dlState": "FL",

                                    "roleInClaim": {

                                        "code": "CL",

                                        "description": "Claimant"

                                    },

                                    "address": {

                                        "street1": "2511 16TH STREET CT W",

                                        "city": "BRADENTON",

                                        "stateCode": "FL",

                                        "zip": "34205"

                                    },

                                    "sequenceInInputDrivers": "0"

                                },

                                {

                                    "indvidualOrBusinessIndicator": "I",

                                    "givenName": "KATY",

                                    "surname": "PERRY",

                                    "dob": "19751108",

                                    "dlNumber": "E914883836547",

                                    "dlState": "FL",

                                    "roleInClaim": {

                                        "code": "CD",

                                        "description": "Claimant Driver"

                                    },

                                    "address": {

                                        "street1": "2002 KINGSTON",

                                        "city": "JACKSONVILLE",

                                        "stateCode": "FL",

                                        "zip": "32209"

                                    },

                                    "sequenceInInputDrivers": "0"

                                }

                            \],

                            "lossInformation": {

                                "lossDate": "20230115",

                                "lossTime": "0000",

                                "lossCode": "0000",

                                "losses": \[

                                    {

                                        "coverageType": {

                                            "code": "LIAB",

                                            "description": "Liability"

                                        },

                                        "lossType": {

                                            "code": "BI",

                                            "description": "Body injury"

                                        },

                                        "dispositionStatus": {

                                            "code": "C",

                                            "description": "Closed"

                                        },

                                        "amount": "2000",

                                        "claimStandardizationCode": "N02EPA308071U111"

                                    }

                                \]

                            },

                            "claimStandardizationCode": "N02EPA308071U111",

                            "vehicles": \[

                                {

                                    "make": "GENERAL MOTORS CORP",

                                    "model": "ACADIA",

                                    "year": "2008",

                                    "vin": "1GKER23788J291227",

                                    "vinValidation": {

                                        "code": "P",

                                        "description": "Pass"

                                    }

                                }

                            \]

                        },

                        {

                            "claimReferenceNumber": "3IA00527548",

                            "carrierClaimNumber": "VRLSAP20181002101",

                            "matchReasons": \[

                                {

                                    "code": "V",

                                    "description": "VIN Search Type"

                                },

                                {

                                    "code": "Y",

                                    "description": "Policy Number search"

                                },

                                {

                                    "code": "N",

                                    "description": "Name and Date of Birth Search Type"

                                },

                                {

                                    "code": "A",

                                    "description": "Name and Address Search Type"

                                }

                            \],

                            "atFaultIndicator": {

                                "code": "Y",

                                "description": "Insured at Fault"

                            },

                            "insurer": {

                                "companyId": "Z995",

                                "officeId": "00000",

                                "name": "INSURANCE SERVICES OFFICE, INC",

                                "ambest": "00001",

                                "address": {

                                    "street1": "545 WASHINGTON BLVD",

                                    "city": "JERSEY CITY",

                                    "stateCode": "NJ",

                                    "zip": "07310",

                                    "countryCode": "US"

                                },

                                "phone": "7323880332"

                            },

                            "policy": {

                                "policyNumber": "VRSKLSP201810021001",

                                "policyType": {

                                    "code": "PAPP",

                                    "description": "Personal Auto"

                                },

                                "originalInceptionDate": "20200105",

                                "expirationDate": "20240105"

                            },

                            "matchByInputDriverNumber": "2",

                            "subjects": \[

                                {

                                    "indvidualOrBusinessIndicator": "I",

                                    "givenName": "DOUGLAS",

                                    "surname": "BONZHEIM",

                                    "middleName": "J",

                                    "dob": "19760101",

                                    "dlNumber": "D852424151335",

                                    "dlState": "FL",

                                    "roleInClaim": {

                                        "code": "IN",

                                        "description": "Insured"

                                    },

                                    "address": {

                                        "street1": "7827 ADELAIDE LP",

                                        "city": "NEW PORT RICHEY",

                                        "stateCode": "FL",

                                        "zip": "34655"

                                    },

                                    "sequenceInInputDrivers": "2"

                                },

                                {

                                    "indvidualOrBusinessIndicator": "I",

                                    "givenName": "DOUGLAS",

                                    "surname": "BONZHEIM",

                                    "middleName": "J",

                                    "dob": "19760101",

                                    "dlNumber": "D852424151335",

                                    "dlState": "FL",

                                    "roleInClaim": {

                                        "code": "SA",

                                        "description": "Insured Driver Same as Insured"

                                    },

                                    "address": {

                                        "street1": "7827 ADELAIDE LP",

                                        "city": "NEW PORT RICHEY",

                                        "stateCode": "FL",

                                        "zip": "34655"

                                    },

                                    "sequenceInInputDrivers": "2"

                                }

                            \],

                            "lossInformation": {

                                "lossDate": "20221225",

                                "lossTime": "0000",

                                "lossCode": "0000",

                                "losses": \[

                                    {

                                        "coverageType": {

                                            "code": "UM",

                                            "description": "Uninsured Motorist"

                                        },

                                        "lossType": {

                                            "code": "UMPD",

                                            "description": "Uninsured Motorist Property Damage"

                                        },

                                        "dispositionStatus": {

                                            "code": "C",

                                            "description": "Closed"

                                        },

                                        "amount": "2000",

                                        "claimStandardizationCode": "Y12JPA309070U000"

                                    }

                                \]

                            },

                            "claimStandardizationCode": "Y12JPA309070U000",

                            "vehicles": \[

                                {

                                    "make": "GENERAL MOTORS CORP",

                                    "model": "ACADIA",

                                    "year": "2008",

                                    "vin": "1GKER23788J291227",

                                    "vinValidation": {

                                        "code": "P",

                                        "description": "Pass"

                                    }

                                }

                            \]

                        }

                    \],

                    "vehicles": \[

                        {

                            "make": "GMC",

                            "model": "SC4",

                            "year": "1985",

                            "vin": "1G5CT18B5F8530675",

                            "vinValidation": {

                                "code": "P",

                                "description": "Pass"

                            },

                            "estimateInformation": {

                                "estimateAvailable": "N",

                                "mileage": "0"

                            },

                            "vinDecoding": \[

                                {

                                    "vinCharacter": "1",

                                    "description": "Country of Origin",

                                    "value": "UNITED STATES OF AMERICA"

                                },

                                {

                                    "vinCharacter": "G",

                                    "description": "Make",

                                    "value": "Undetermined \*",

                                    "invalidDigitIndicator": "\*"

                                },

                                {

                                    "vinCharacter": "5",

                                    "description": "\* Undetermined \*",

                                    "value": "Undetermined \*",

                                    "invalidDigitIndicator": "\*"

                                },

                                {

                                    "vinCharacter": "C",

                                    "description": "\* Undetermined \*",

                                    "value": "Undetermined \*",

                                    "invalidDigitIndicator": "\*"

                                },

                                {

                                    "vinCharacter": "T",

                                    "description": "\* Undetermined \*",

                                    "value": "Undetermined \*",

                                    "invalidDigitIndicator": "\*"

                                },

                                {

                                    "vinCharacter": "1",

                                    "description": "\* Undetermined \*",

                                    "value": "Undetermined \*",

                                    "invalidDigitIndicator": "\*"

                                },

                                {

                                    "vinCharacter": "8",

                                    "description": "\* Undetermined \*",

                                    "value": "Undetermined \*",

                                    "invalidDigitIndicator": "\*"

                                },

                                {

                                    "vinCharacter": "B",

                                    "description": "\* Undetermined \*",

                                    "value": "Undetermined \*",

                                    "invalidDigitIndicator": "\*"

                                },

                                {

                                    "vinCharacter": "5",

                                    "description": "Check Digit",

                                    "value": "Check Digit Matches"

                                },

                                {

                                    "vinCharacter": "F",

                                    "description": "Year",

                                    "value": "Undetermined \*",

                                    "invalidDigitIndicator": "\*"

                                },

                                {

                                    "vinCharacter": "8",

                                    "description": "\* Undetermined \*",

                                    "value": "Undetermined \*",

                                    "invalidDigitIndicator": "\*"

                                },

                                {

                                    "vinCharacter": "530675",

                                    "description": "Sequence Number",

                                    "value": "Range Undetermined",

                                    "invalidDigitIndicator": "\*"

                                }

                            \]

                        },

                        {

                            "make": "CHEV",

                            "model": "SUB",

                            "year": "2000",

                            "vin": "3GNFK16T9YG218125",

                            "vinValidation": {

                                "code": "P",

                                "description": "Pass"

                            },

                            "eventDataRecorderAvailable": "Y",

                            "estimateInformation": {

                                "estimateAvailable": "N",

                                "mileage": "0"

                            },

                            "noticesOfRecall": \[

                                {

                                    "recallId": "05V379000",

                                    "componentInfo": "SERVICE BRAKES, HYDRAULIC:ANTILOCK/TRACTION CONTROL/ELECTRONIC LIMITED SLIP                                                                           ",

                                    "recallSummary": "CERTAIN PICKUP TRUCKS AND SPORT UTILITY VEHICLES MAY EXPERIENCE UNWANTED ANTILOCK BRAKE SYSTEM (ABS) ACTIVATION.  THIS CONDITION IS MORE LIKELY TO OCCUR IN ENVIRONMENTALLY CORROSIVE AREAS.   THIS RECALL WILL BE LAUNCHED IN THE \\"SALT BELT\\" STATES OF CONNECTICUT, DELAWARE, ILLINOIS, INDIANA, IOWA, MAR",

                                    "recallDate": "20050829",

                                    "numberOfUnitsRecalled": "1353718",

                                    "manufactureRecallInfo": "GENERAL MOTORS CORP.",

                                    "recallConsequences": "THIS CAN CAUSE INCREASED STOPPING DISTANCES DURING LOW-SPEED BRAKE APPLICATIONS, WHICH COULD RESULT IN A CRASH.                                                                                                                                                                                             "

                                },

                                {

                                    "recallId": "05V155000",

                                    "componentInfo": "FUEL SYSTEM, GASOLINE:DELIVERY:FUEL PUMP                                                                                                              ",

                                    "recallSummary": "CERTAIN TRUCKS AND SPORT UTILITY VEHICLES WERE BUILT WITH FUEL MODULE RESERVOIR ASSEMBLIES THAT CONTAIN FUEL PUMP WIRES CONNECTORS MAY OVERHEAT UNDER CERTAIN  OPERATING CONDITIONS.                                                                                                                        ",

                                    "recallDate": "20050414",

                                    "numberOfUnitsRecalled": "316508",

                                    "manufactureRecallInfo": "GENERAL MOTORS CORP.",

                                    "recallConsequences": "IF THE IGNITION CIRCUIT WIRE IS EXPOSED, THE FUEL PUMP FUSE WILL BLOW, DISABLING THE FUEL PUMP AND CAUSING AN ENGINE STALL OR NO-START CONDITION.  IF SUFFICIENT HEAT IS CONDUCTED TO THE PASS-THROUGH CONNECTOR, A  HOLE IN THE CONNECTOR MAY RESULT, WHICH MAY CAUSE A 'SERVICE ENGINE SOON' LIGHT TO BE I"

                                },

                                {

                                    "recallId": "05V005000",

                                    "componentInfo": "POWER TRAIN:DRIVELINE:DRIVESHAFT                                                                                                                      ",

                                    "recallSummary": "SOME PICKUP TRUCKS, VANS, AND SPORT UTILITY VEHICLES EQUIPPED WITH A HYDRAULIC PUMP DRIVESHAFT THAT CAN FRACTURE, RESULTING IN IMMEDIATE LOSS OF HYDRAULIC POWER STEERING ASSIST.  ON CERTAIN VEHICLES EQUIPPED WITH HYDRO-BOOST POWER BRAKES, THE SAME CONDITION CAN RESULT IN LOSS OF POWER ASSIST FOR BRA",

                                    "recallDate": "20050107",

                                    "numberOfUnitsRecalled": "98221",

                                    "manufactureRecallInfo": "GENERAL MOTORS CORP.",

                                    "recallConsequences": "AN INOPERATIVE PUMP CAN CAUSE INCREASED STEERING EFFORT, AND IN HYDRO-BOOST EQUIPPED VEHICLES ALSO INCREASED BRAKING EFFORT, BUT DOES NOT COMPLETELY ELIMINATE THE ABILITY TO STEER OR SLOW THE VEHICLE.                                                                                                    "

                                },

                                {

                                    "recallId": "03V094000",

                                    "componentInfo": "STRUCTURE                                                                                                                                             ",

                                    "recallSummary": "CERTAIN PICKUP TRUCK, VAN, AND MINI VAN CONVERSIONS EQUIPPED WITH SOUTHERN COMFORT BUILT RUNNING BOARDS THAT CONTAIN CERTAIN COURTESY LIGHTS MANUFACTURED BY AMERICAN TECHNOLOGY COMPONENTS, INC.  THESE UNITS CONTAIN A COURTESY LIGHT OR LIGHTS THAT MIGHT OVERHEAT WHEN THE WIRE HARNESS IS EXPOSED TO EX",

                                    "recallDate": "20030307",

                                    "numberOfUnitsRecalled": "3674",

                                    "manufactureRecallInfo": "SOUTHERN COMFORT CONVERSIONS",

                                    "recallConsequences": "THIS OVERHEATING CONDITION CAN CAUSE THE RUNNING BOARD TO MELT OR CAUSE A FIRE.                                                                                                                                                                                                                             "

                                },

                                {

                                    "recallId": "02V178000",

                                    "componentInfo": "AIR BAGS:FRONTAL:SENSOR/CONTROL MODULE                                                                                                                ",

                                    "recallSummary": "ON CERTAIN PICKUP AND UTILITY TRUCKS, SOME OF THESE VEHICLES HAVE AN AIR BAG SENSING DIAGNOSTIC MODULE (SDM) WHICH CONTAINS AN ANOMALY THAT COULD RESULT IN THE DRIVER AND PASSENGER'S AIR BAG FAILING TO DEPLOY DURING CERTAIN FRONTAL CRASHES.                                                            ",

                                    "recallDate": "20020701",

                                    "numberOfUnitsRecalled": "525254",

                                    "manufactureRecallInfo": "GENERAL MOTORS CORP.",

                                    "recallConsequences": "IN A VEHICLE CRASH, FRONT SEAT OCCUPANTS MAY RECEIVE MORE SEVERE INJURIES.                                                                                                                                                                                                                                  "

                                }

                            \],

                            "vinDecoding": \[

                                {

                                    "vinCharacter": "3",

                                    "description": "Country of Origin",

                                    "value": "MEXICO"

                                },

                                {

                                    "vinCharacter": "G",

                                    "description": "Manufacturer",

                                    "value": "CHEV   GENERAL MOTORS"

                                },

                                {

                                    "vinCharacter": "N",

                                    "description": "Vehicle Type",

                                    "value": "MULTI PURPOSE VEHICLE"

                                },

                                {

                                    "vinCharacter": "F",

                                    "description": "Gross Vehicle Weight",

                                    "value": "7001-8000 GVWR   HYDRAULIC BRAKES"

                                },

                                {

                                    "vinCharacter": "K1",

                                    "description": "Series",

                                    "value": "FULL SIZE TRUCK 4X4, 1500 (1/2 TON)"

                                },

                                {

                                    "vinCharacter": "6",

                                    "description": "Body Style",

                                    "value": "SUBURBAN"

                                },

                                {

                                    "vinCharacter": "T",

                                    "description": "Engine",

                                    "value": "5.3L V8 MFI, IRON"

                                },

                                {

                                    "vinCharacter": "9",

                                    "description": "Check Digit",

                                    "value": "Check Digit Matches"

                                },

                                {

                                    "vinCharacter": "Y",

                                    "description": "Year",

                                    "value": "2000"

                                },

                                {

                                    "vinCharacter": "G",

                                    "description": "Plant",

                                    "value": "SILAO, MEXICO"

                                },

                                {

                                    "vinCharacter": "218125",

                                    "description": "Serial Number",

                                    "value": "Sequence in Range"

                                }

                            \]

                        },

                        {

                            "make": "HOND",

                            "model": "ACC",

                            "year": "2006",

                            "vin": "1HGCM56306A148752",

                            "vinValidation": {

                                "code": "P",

                                "description": "Pass"

                            },

                            "eventDataRecorderAvailable": "N",

                            "estimateInformation": {

                                "estimateAvailable": "Y",

                                "activityDate": "20161020",

                                "lossDate": "20160827",

                                "mileage": "113489"

                            },

                            "noticesOfRecall": \[

                                {

                                    "recallId": "19V499000",

                                    "componentInfo": "AIR BAGS:FRONTAL:DRIVER SIDE:INFLATOR MODULE                                                                                                          ",

                                    "recallSummary": "Honda (American Honda Motor Co.) is recalling certain 2003 Acura 3.2CL, 2002-2003 3.2TL, 2003-2006 MDX, 2001-2007 Honda Accord, 2001-2005 Civic, 2003-2005 Civic Hybrid, 2001-2005 Civic GX NGV, 2002-2006 CR-V, 2003-2011 Element, 2002-2004 Odyssey, 2003-2008 Pilot and 2006 Ridgeline vehicles.      The",

                                    "recallDate": "20190627",

                                    "numberOfUnitsRecalled": "3947",

                                    "manufactureRecallInfo": "Honda (American Honda Motor Co.)",

                                    "recallConsequences": "An inflator explosion may result in sharp metal fragments striking the driver or other occupants resulting in serious injury or death.                                                                                                                                                                      "

                                },

                                {

                                    "recallId": "19V501000",

                                    "componentInfo": "AIR BAGS:FRONTAL:PASSENGER SIDE:INFLATOR MODULE                                                                                                       ",

                                    "recallSummary": "Honda (American Honda Motor Co.) is recalling certain 2003-2006 Acura MDX, 2005-2012 RL, 2003-2007 Honda Accord, 2001-2005 Civic, 2003-2005 Civic Hybrid, 2001-2005 Civic GX NGV, 2002-2006 CR-V, 2003-2011 Element, 2007-2008 Fit, 2002-2004 Odyssey, 2003-2008 Pilot, and 2006-2014 Ridgeline vehicles.   ",

                                    "recallDate": "20190627",

                                    "numberOfUnitsRecalled": "1657752",

                                    "manufactureRecallInfo": "Honda (American Honda Motor Co.)",

                                    "recallConsequences": "An inflator explosion may result in sharp metal fragments striking the driver or other occupants resulting in serious injury or death.                                                                                                                                                                      "

                                },

                                {

                                    "recallId": "19V182000",

                                    "componentInfo": "AIR BAGS:FRONTAL:DRIVER SIDE:INFLATOR MODULE                                                                                                          ",

                                    "recallSummary": "Honda (American Honda Motor Co.) is recalling specific 2003 Acura 3.2CL, 2013-2016 ILX, 2013-2014 ILX Hybrid, 2003-2006 MDX, 2007-2016 RDX, 2002-2003 3.2TL, 2004-2006, and 2009-2014 TL, 2010-2013 ZDX and 2001-2007 and 2009 Honda Accord, 2001-2005 Civic, 2003-2005 Civic Hybrid, 2001-2005 Civic GX NGV",

                                    "recallDate": "20190306",

                                    "numberOfUnitsRecalled": "1101534",

                                    "manufactureRecallInfo": "Honda (American Honda Motor Co.)",

                                    "recallConsequences": "An explosion of an inflator within the driver frontal air bag module may result in sharp metal fragments striking the driver, front seat passenger or other occupants resulting in serious injury or death.                                                                                                 "

                                },

                                {

                                    "recallId": "18V268000",

                                    "componentInfo": "AIR BAGS:FRONTAL:PASSENGER SIDE:INFLATOR MODULE                                                                                                       ",

                                    "recallSummary": "Honda (American Honda Motor Co.) is recalling certain 2003-2012 Honda Accord and Pilot, 2010 Accord Crosstour, 2001-2011 Civic, 2002-2011 CR-V, 2003-2004, 2006-2008 and 2011 Element, 2007 and 2009-2013 Fit, 2010-2012 Insight, 2002-2004 Odyssey, and 2012 Ridgeline vehicles.  The front passenger air b",

                                    "recallDate": "20180426",

                                    "numberOfUnitsRecalled": "1335",

                                    "manufactureRecallInfo": "Honda (American Honda Motor Co.)",

                                    "recallConsequences": "An incorrectly installed air bag may deploy improperly in the event of a crash, increasing the risk of injury.                                                                                                                                                                                              "

                                },

                                {

                                    "recallId": "16V178000",

                                    "componentInfo": "AIR BAGS:FRONTAL:PASSENGER SIDE:INFLATOR MODULE                                                                                                       ",

                                    "recallSummary": "Honda (American Honda Motor Co.) is recalling certain model year 2004-2007 Accord vehicles manufactured October 1, 2003, to August 17, 2007\.  The affected vehicles may have been assembled with an incorrect passenger frontal air bag module that does not comply with the advanced air bag requirements. ",

                                    "recallDate": "20160330",

                                    "numberOfUnitsRecalled": "11602",

                                    "manufactureRecallInfo": "Honda (American Honda Motor Co.)",

                                    "recallConsequences": "An air bag module does not meet the advanced air bag requirements can increase the risk of injury or death in the event of a crash.                                                                                                                                                                         "

                                }

                            \],

                            "vinDecoding": \[

                                {

                                    "vinCharacter": "1",

                                    "description": "Country of Origin",

                                    "value": "UNITED STATES OF AMERICA"

                                },

                                {

                                    "vinCharacter": "H",

                                    "description": "Manufacturer",

                                    "value": "HOND   HONDA"

                                },

                                {

                                    "vinCharacter": "G",

                                    "description": "Vehicle Type",

                                    "value": "PASSENGER CAR"

                                },

                                {

                                    "vinCharacter": "CM563",

                                    "description": "Model",

                                    "value": "ACCORD SE/4DR SD/5A/6 AIR BAGS"

                                },

                                {

                                    "vinCharacter": "0",

                                    "description": "Check Digit",

                                    "value": "Check Digit Matches"

                                },

                                {

                                    "vinCharacter": "6",

                                    "description": "Year",

                                    "value": "2006"

                                },

                                {

                                    "vinCharacter": "A",

                                    "description": "Plant",

                                    "value": "MARYSVILLE, OH"

                                },

                                {

                                    "vinCharacter": "148752",

                                    "description": "Serial Number",

                                    "value": "Sequence in Range"

                                }

                            \]

                        },

                        {

                            "make": "GMC",

                            "model": "ACA",

                            "year": "2008",

                            "vin": "1GKER23788J291227",

                            "vinValidation": {

                                "code": "P",

                                "description": "Pass"

                            },

                            "eventDataRecorderAvailable": "Y",

                            "estimateInformation": {

                                "estimateAvailable": "N",

                                "mileage": "0"

                            },

                            "noticesOfRecall": \[

                                {

                                    "recallId": "15V415000",

                                    "componentInfo": "STRUCTURE:BODY:HATCHBACK/LIFTGATE                                                                                                                     ",

                                    "recallSummary": "General Motors LLC (GM) is recalling certain model year 2008-2012 Buick Enclave vehicles manufactured January 3, 2007, to February 29, 2012, 2009-2012 Chevrolet Traverse vehicles manufactured July 6, 2008, to March 9, 2012, 2007-2012 GMC Acadia vehicles manufactured September 15, 2006, to February 2",

                                    "recallDate": "20150630",

                                    "numberOfUnitsRecalled": "691144",

                                    "manufactureRecallInfo": "General Motors LLC",

                                    "recallConsequences": "If the open liftgate unexpectedly falls, it may strike a person, increasing their risk of injury.                                                                                                                                                                                                           "

                                },

                                {

                                    "recallId": "14V118000",

                                    "componentInfo": "AIR BAGS:SIDE/WINDOW                                                                                                                                  ",

                                    "recallSummary": "General Motors LLC (GM) is recalling certain model year 2008-2013 Buick Enclave and GMC Acadia and 2009-2013 Chevrolet Traverse and 2008-2010 Saturn Outlook vehicles.  In the affected vehicles, increased resistance in the driver and passenger seat mounted side impact air bag (SIAB) wiring harnesses ",

                                    "recallDate": "20140317",

                                    "numberOfUnitsRecalled": "1176407",

                                    "manufactureRecallInfo": "General Motors LLC",

                                    "recallConsequences": "Failure of the side impact air bags and seat belt pretensioners to deploy in a crash increase the risk of injury to the driver and front seat occupant.                                                                                                                                                     "

                                },

                                {

                                    "recallId": "10V240000",

                                    "componentInfo": "ELECTRICAL SYSTEM                                                                                                                                     ",

                                    "recallSummary": "GM IS RECALLING CERTAIN MODEL YEAR 2006-2009 BUICK, LUCERNE; CADILLAC DTS; HUMMER H2; MODEL YEAR 2008-2009 BUICK ENCLAVE; CADILLAC CTS; MODEL YEAR 2007-2009 CADILLAC ESCALADE, ESCALADE ESV, ESCALADE EXT; CHEVROLET AVALANCHE, SILVERADO, SUBURBAN, TAHOE; GMC ACADIA, SIERRA, YUKON, YUKON XL; SATURN OUT",

                                    "recallDate": "20100604",

                                    "numberOfUnitsRecalled": "1365070",

                                    "manufactureRecallInfo": "GENERAL MOTORS CORP.",

                                    "recallConsequences": "IT IS POSSIBLE FOR THE HEATED WASHER MODULE TO IGNITE AND A FIRE MAY OCCUR.                                                                                                                                                                                                                                 "

                                },

                                {

                                    "recallId": "08V441000",

                                    "componentInfo": "ELECTRICAL SYSTEM                                                                                                                                     ",

                                    "recallSummary": "GM IS RECALLING 857,735 MY 2006-2008 BUICK LUCERNE; CADILLAC DTS; HUMMER H2; MY 2007-2008 CADILLAC ESCALADE, ESCALADE ESV, ESCALADE EXT; CHEVROLET AVALANCHE, SILVERADO, SUBURBAN, TAHOE; GMC ACADIA, SIERRA, YUKON, YUKON XL, SATURN OUTLOOK; AND MY 2008 BUICK ENCLAVE VEHICLES EQUIPPED WITH A HEATED WIP",

                                    "recallDate": "20080828",

                                    "numberOfUnitsRecalled": "857735",

                                    "manufactureRecallInfo": "GENERAL MOTORS CORP.",

                                    "recallConsequences": "THIS MAY CAUSE OTHER ELECTRICAL FEATURES TO MALFUNCTION, CREATE AN ODOR, OR CAUSE SMOKE INCREASING THE RISK OF A FIRE.                                                                                                                                                                                      "

                                },

                                {

                                    "recallId": "08V410000",

                                    "componentInfo": "VISIBILITY:WINDSHIELD WIPER/WASHER:LINKAGES                                                                                                           ",

                                    "recallSummary": "GM IS RECALLING 88,809 MY 2008 BUICK ENCLAVE, AND MY 2007-2008 GMC ACADIA AND SATURN OUTLOOK VEHICLES CURRENTLY OR PREVIOUSLY REGISTERED IN THE FOLLOWING STATES:  ALASKA, COLORADO, CONNECTICUT, DELAWARE, IDAHO, ILLINOIS, INDIANA, IOWA, MAINE, MARYLAND, MASSACHUSETTS, MICHIGAN, MINNESOTA, MONTANA, NE",

                                    "recallDate": "20080814",

                                    "numberOfUnitsRecalled": "88809",

                                    "manufactureRecallInfo": "GENERAL MOTORS CORP.",

                                    "recallConsequences": "IF THIS WERE TO OCCUR, DRIVER VISIBILITY COULD BE REDUCED, WHICH COULD RESULT IN A VEHICLE CRASH.                                                                                                                                                                                                           "

                                }

                            \],

                            "vinDecoding": \[

                                {

                                    "vinCharacter": "1",

                                    "description": "Country of Origin",

                                    "value": "UNITED STATES OF AMERICA"

                                },

                                {

                                    "vinCharacter": "G",

                                    "description": "Manufacturer",

                                    "value": "GMC    GENERAL MOTORS CORPORATION"

                                },

                                {

                                    "vinCharacter": "K",

                                    "description": "Vehicle Type",

                                    "value": "GMC MPV"

                                },

                                {

                                    "vinCharacter": "E",

                                    "description": "Gross Vehicle Weight",

                                    "value": "6001-7000 GVWR   HYDRAULIC BRAKES"

                                },

                                {

                                    "vinCharacter": "R2",

                                    "description": "Series",

                                    "value": "ACADIA 1/2 TON FWD SLT(1)"

                                },

                                {

                                    "vinCharacter": "3",

                                    "description": "Body Style",

                                    "value": "4D:ENV/YKN/DNLI/CRW/ACAD/TYPHN(KL6)"

                                },

                                {

                                    "vinCharacter": "7",

                                    "description": "Engine",

                                    "value": "3.6L V6 SFI ALUM 60 DEG"

                                },

                                {

                                    "vinCharacter": "8",

                                    "description": "Check Digit",

                                    "value": "Check Digit Matches"

                                },

                                {

                                    "vinCharacter": "8",

                                    "description": "Year",

                                    "value": "2008"

                                },

                                {

                                    "vinCharacter": "J",

                                    "description": "Plant",

                                    "value": "JNSVL, WI(YUKON)/LANSING,MI(ACADIA)"

                                },

                                {

                                    "vinCharacter": "291227",

                                    "description": "Serial Number",

                                    "value": "Sequence in Range"

                                }

                            \]

                        }

                    \],

                    "ssnInformations": \[

                        {

                            "ssn": "000000000",

                            "ssnValidation": {

                                "code": "I",

                                "description": "SSN Invalid"

                            }

                        },

                        {

                            "ssn": "000007807",

                            "ssnValidation": {

                                "code": "V",

                                "description": "SSN has been Verified and Issued"

                            }

                        }

                    \]

                }

            },

            "allMotorVehicleReports": \[

                {

                    "header": {

                        "quoteback": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57",

                        "transactionId": "2c74e980-8b94-45ea-973a-20570efe3ea7"

                    },

                    "body": {

                        "orderNumber": "935981072",

                        "motorVehicleReports": \[

                            {

                                "identifier": "538982760",

                                "status": {

                                    "code": "V",

                                    "description": "NON-CLEAR report"

                                },

                                "violationsType": {

                                    "code": "C",

                                    "description": "Report passed through Custom violation code/point process",

                                    "pointTotal": "   0"

                                },

                                "dmvReportDate": "20201120",

                                "archiveFlag": "N",

                                "driversPrivacyProtectionActFlag": "N",

                                "driver": {

                                    "name": "BONZHEIM, YUKI",

                                    "address": {

                                        "street1": "7827 ADELAIDE LP",

                                        "cityStateZip": "NEW PORT RICHEY, FL 34655"

                                    },

                                    "dlNumber": "T520103597610",

                                    "dlState": "FL",

                                    "dob": "19900311",

                                    "gender": "M",

                                    "height": "6'1",

                                    "license": {

                                        "class": "E",

                                        "status": "VALID",

                                        "IssuedDate": "20131001",

                                        "ExpirationDate": "20210801",

                                        "OriginalIssueDate": "20001201"

                                    },

                                    "detail": "OrderType : MvrIndicator \- REQUESTED AS: YUKI                      BONZHEIM                  DOB: 03111990  LICENSE : T520103597610 PERS:01: ACTIVE          VALID   E              1001201308012021 LIC CLASS: E                       DESC: OPERATOR LIC STATUS: VALID LIC ISSUED: 10/01/2021 LIC EXPIRES: 08/01/2029 PERS:02: EXPIRED         EXPIRED ID CARD        1201200910012014 LIC CLASS: ID CARD                 DESC: ID CARD LIC STATUS: EXPIRED LIC ISSUED: 12/01/2009 LIC EXPIRES: 10/01/2014 AS OF NOVEMBER 20, 2020 AT 9:50:20 AM, DRIVER PRIVILEGE T520-103-59-761-0 IS VALID. PERSONAL INFORMATION IS PROTECTED PURSUANT TO THE DRIVER PRIVACY PROTECTION ACT. ENTRIES BELOW ARE A THREE YEAR RECORD. ORIGINAL ISSUE DATE: 12/01/2000 REAL ID COMPLIANT ORGAN DONOR US CITIZEN BLOCKED PERSONAL INFORMATION BLOCKED FOR MAILING LIST PERSON HAS A DIGITAL IMAGE ELIGIBLE TO ELECT DRIVER SCHOOL.  DRIVER HAS MADE 2 ELECTIONS. LAST ELECTION WAS ON 02/01/2012. VIOLATIONS COMMITTED WHILE A CDL HOLDER OR IN A CMV VEHICLE ARE NOT ELIGIBLE FOR DRIVING SCHOOL ELECTION. COUNTY: MIAMI-DADE RESIDENTIAL ADDRESS: 2570 NW 48TH ST  MIAMI, FL  33142  COUNTY: MIAMI-DADE ISSUANCE HISTORY: LIC CLASS: ID CARD   ISSUE DATE: 12/01/1996   ISSUE TYPE: DUPLICATE LIC CLASS: ID CARD   ISSUE DATE: 12/01/2000   ISSUE TYPE: DUPLICATE LIC CLASS: CLASS E   ISSUE DATE: 05/01/2002   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 02/01/2003   ISSUE TYPE: DUPLICATE LIC CLASS: ID CARD   ISSUE DATE: 07/01/2006   ISSUE TYPE: DUPLICATE LIC CLASS: CLASS E   ISSUE DATE: 04/01/2009   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 02/01/2010   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 02/01/2010   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 08/01/2012   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 10/01/2013   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 10/01/2014   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 03/01/2018   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 10/01/2020   ISSUE TYPE: CDR/CDT CLEARANCE EXAMS TAKEN: VISION               DATE TAKEN: 10/01/2021   COUNT: 2   STATUS: PASS ROAD SIGN            DATE TAKEN: 12/01/2021   COUNT: 1   STATUS: PASS ROAD RULES           DATE TAKEN: 12/01/2020   COUNT: 3   STATUS: PASS DRIVING              DATE TAKEN: 12/01/2020   COUNT: 1   STATUS: PASS This report is generated for insurance purposes only and may not be used for any other purpose.  The use and dissemination of the report and information in it must comply with your iiX agreement and the  Fair Credit Reporting Act, the Driver's Privacy Protection Act, and any applicable state statute(s).  The data in the report from the applicable state agency or service bureau is provided through iiX \\"as is.\\" \--- Customer-defined MVR scoring has been applied to this record.  Customer  is solely responsible for the application and use of the resulting score.",

                                    "violations": \[

                                        {

                                            "violationType": "SUSP",

                                            "violationDate": "20220301",

                                            "customCode": "130110",

                                            "customPoints": "3",

                                            "detail": "FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 720198716 NOTICED PROVIDED: 12/01/2021 ADDED TO RECORD: 12/01/2021 SANCTION CODE: 7"

                                        },

                                        {

                                            "violationType": "REIN",

                                            "convictionDate": "20220301",

                                            "customCode": "330130",

                                            "customPoints": "-3",

                                            "detail": "REINSTATED"

                                        },

                                        {

                                            "violationType": "SUSP",

                                            "violationDate": "20211001",

                                            "customCode": "130110",

                                            "customPoints": "3",

                                            "detail": "FR-REGISTRATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 830175467 NOTICED PROVIDED: 09/01/2021 ADDED TO RECORD: 09/01/2021 SANCTION CODE: 8"

                                        },

                                        {

                                            "violationType": "REIN",

                                            "convictionDate": "20211001",

                                            "customCode": "330130",

                                            "customPoints": "-3",

                                            "detail": "REINSTATED"

                                        },

                                        {

                                            "violationType": "VIOL",

                                            "violationDate": "20200201",

                                            "convictionDate": "20200601",

                                            "stateAssignedPoints": "0",

                                            "customCode": "425100",

                                            "customPoints": "0",

                                            "detail": "316.0083 RED LIGHT CAMERA DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 23 CITATION NUMBER: A5OJ78E COUNTY: MIAMI-DADE STATE: FL ADDED TO RECORD: 06/01/2020 DISPOSITION CODE: 547"

                                        },

                                        {

                                            "violationType": "VIOL",

                                            "violationDate": "20190201",

                                            "convictionDate": "20190801",

                                            "stateAssignedPoints": "0",

                                            "customCode": "425100",

                                            "customPoints": "0",

                                            "detail": "316.0083 RED LIGHT CAMERA DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 24 CITATION NUMBER: AADQWXE COUNTY: MIAMI-DADE STATE: FL ADDED TO RECORD: 08/01/2019 DISPOSITION CODE: 547"

                                        }

                                    \]

                                }

                            }

                        \]

                    },

                    "statusCode": 200

                },

                {

                    "header": {

                        "quoteback": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57",

                        "transactionId": "4c8b4365-4f7e-4079-907a-3c5433789713"

                    },

                    "body": {

                        "orderNumber": "935981071",

                        "motorVehicleReports": \[

                            {

                                "identifier": "538982762",

                                "status": {

                                    "code": "V",

                                    "description": "NON-CLEAR report"

                                },

                                "violationsType": {

                                    "code": "C",

                                    "description": "Report passed through Custom violation code/point process",

                                    "pointTotal": "   4"

                                },

                                "dmvReportDate": "20201120",

                                "archiveFlag": "N",

                                "driversPrivacyProtectionActFlag": "N",

                                "driver": {

                                    "name": "BONZHEIM, DOUGLAS",

                                    "address": {

                                        "street1": "7827 ADELAIDE LP",

                                        "cityStateZip": "NEW PORT RICHEY, FL 34655"

                                    },

                                    "dlNumber": "M888777666555",

                                    "dlState": "FL",

                                    "dob": "19760101",

                                    "gender": "M",

                                    "height": "5'10",

                                    "license": {

                                        "class": "E",

                                        "status": "VALID P",

                                        "IssuedDate": "20220401",

                                        "ExpirationDate": "20300601",

                                        "OriginalIssueDate": "20000401"

                                    },

                                    "detail": "OrderType : MvrIndicator \- REQUESTED AS: DOUGLAS        J          BONZHEIM                  DOB: 01011976  LICENSE : M888777666555 PERS:01: ACTIVE          VALID P E              0401202206012030 LIC CLASS: E                       DESC: OPERATOR LIC STATUS: VALID PENDING LIC ISSUED: 04/01/2022 LIC EXPIRES: 06/01/2030 PERS:02: EXPIRED         EXPIRED ID CARD        0601201805012019 LIC CLASS: ID CARD                 DESC: ID CARD LIC STATUS: EXPIRED LIC ISSUED: 06/01/2018 LIC EXPIRES: 05/01/2019 AS OF NOVEMBER 20, 2020 AT 9:39:55 AM, DRIVER PRIVILEGE M888-777-66-655-5 IS VALID PENDING SANCTION(S). PERSONAL INFORMATION IS PROTECTED PURSUANT TO THE DRIVER PRIVACY PROTECTION ACT. ENTRIES BELOW ARE A THREE YEAR RECORD. ORIGINAL ISSUE DATE: 04/01/2000 REAL ID COMPLIANT US CITIZEN RECORD APPEARS IN NATIONAL DRIVER REGISTER BLOCKED PERSONAL INFORMATION BLOCKED FOR MAILING LIST PERSON HAS A DIGITAL IMAGE ELIGIBLE TO ELECT DRIVER SCHOOL.  DRIVER HAS MADE 0 ELECTIONS. VIOLATIONS COMMITTED WHILE A CDL HOLDER OR IN A CMV VEHICLE ARE NOT ELIGIBLE FOR DRIVING SCHOOL ELECTION. COUNTY: CLAY RESIDENTIAL ADDRESS: 4493 PLANTATION OAKS BLVD 1641  ORANGE PARK, FL  32065  COUNTY: CLAY ISSUANCE HISTORY: LIC CLASS: CLASS D   ISSUE DATE: 06/01/2001   ISSUE TYPE: DUPLICATE LIC CLASS: ID CARD   ISSUE DATE: 02/01/2003   ISSUE TYPE: DUPLICATE LIC CLASS: CLASS E   ISSUE DATE: 05/01/2015   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 06/01/2017   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 04/01/2018   ISSUE TYPE: REPLACEMENT LIC CLASS: ID CARD   ISSUE DATE: 02/01/2019   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 05/01/2019   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 12/01/2019   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 06/01/2020   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 09/01/2020   ISSUE TYPE: CDR/CDT CLEARANCE EXAMS TAKEN: VISION               DATE TAKEN: 04/01/2014   COUNT: 1   STATUS: PASS ROAD SIGN            DATE TAKEN: 08/01/2000   COUNT: 1   STATUS: PASS ROAD RULES           DATE TAKEN: 08/01/2000   COUNT: 4   STATUS: PASS DRIVING              DATE TAKEN: 04/01/2000   COUNT: 1   STATUS: RECIPROCATED This report is generated for insurance purposes only and may not be used for any other purpose.  The use and dissemination of the report and information in it must comply with your iiX agreement and the  Fair Credit Reporting Act, the Driver's Privacy Protection Act, and any applicable state statute(s).  The data in the report from the applicable state agency or service bureau is provided through iiX \\"as is.\\" \--- Customer-defined MVR scoring has been applied to this record.  Customer  is solely responsible for the application and use of the resulting score.",

                                    "violations": \[

                                        {

                                            "violationType": "SUSP",

                                            "violationDate": "20220801",

                                            "customCode": "130110",

                                            "customPoints": "3",

                                            "detail": "FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 730177824 NOTICED PROVIDED: 07/01/2022 ADDED TO RECORD: 07/01/2022 SANCTION CODE: 7"

                                        },

                                        {

                                            "violationType": "REIN",

                                            "convictionDate": "20220901",

                                            "customCode": "330130",

                                            "customPoints": "-3",

                                            "detail": "REINSTATED"

                                        },

                                        {

                                            "violationType": "SUSP",

                                            "violationDate": "20211201",

                                            "customCode": "130110",

                                            "customPoints": "3",

                                            "detail": "FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) PENDING SUSPENSION CASE NUMBER 730183044 NOTICED PROVIDED: 11/01/2021 ACTION REQUIRED: YES ADDED TO RECORD: 11/01/2021 SANCTION CODE: 7"

                                        },

                                        {

                                            "violationType": "VIOL",

                                            "violationDate": "20200701",

                                            "convictionDate": "20210101",

                                            "stateAssignedPoints": "0",

                                            "customCode": "555110",

                                            "customPoints": "0",

                                            "detail": "OPERATING MV NO PROOF OF INSURANCE DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 10 CITATION NUMBER: A0JO2AE COUNTY: DUVAL ADDED TO RECORD: 02/01/2021 DISPOSITION CODE: 280"

                                        },

                                        {

                                            "violationType": "VIOL",

                                            "violationDate": "20201201",

                                            "convictionDate": "20210101",

                                            "stateAssignedPoints": "0",

                                            "customCode": "425100",

                                            "customPoints": "1",

                                            "detail": "316.0083 RED LIGHT CAMERA DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 11 CITATION NUMBER: A0IBDGE COUNTY: DUVAL ADDED TO RECORD: 02/01/2021 DISPOSITION CODE: 547"

                                        },

                                        {

                                            "violationType": "VIOL",

                                            "violationDate": "20200701",

                                            "convictionDate": "20210201",

                                            "stateAssignedPoints": "0",

                                            "customCode": "428300",

                                            "customPoints": "0",

                                            "detail": "SEAT BELT VIOLATION DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 12 CITATION NUMBER: A0JO2YE COUNTY: DUVAL ADDED TO RECORD: 02/01/2021 DISPOSITION CODE: 407"

                                        },

                                        {

                                            "violationType": "VIOL",

                                            "violationDate": "20200301",

                                            "convictionDate": "20200501",

                                            "stateAssignedPoints": "3",

                                            "customCode": "131240",

                                            "customPoints": "0",

                                            "detail": "DRIV WHILE LIC CANC/REV/SUSP DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 14 CITATION NUMBER: A0GLVGE COUNTY: DUVAL ADDED TO RECORD: 05/01/2020 DISPOSITION CODE: 609"

                                        }

                                    \]

                                }

                            }

                        \]

                    },

                    "statusCode": 200

                },

                {

                    "header": {

                        "quoteback": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57",

                        "transactionId": "2f474259-cc2c-4535-af23-1f6599b7727c"

                    },

                    "body": {

                        "orderNumber": "935981070",

                        "motorVehicleReports": \[

                            {

                                "identifier": "538982761",

                                "status": {

                                    "code": "V",

                                    "description": "NON-CLEAR report"

                                },

                                "violationsType": {

                                    "code": "C",

                                    "description": "Report passed through Custom violation code/point process",

                                    "pointTotal": "   2"

                                },

                                "dmvReportDate": "20201120",

                                "archiveFlag": "N",

                                "driversPrivacyProtectionActFlag": "N",

                                "driver": {

                                    "name": "BONZHEIM, LORNA",

                                    "address": {

                                        "street1": "7827 ADELAIDE LP",

                                        "cityStateZip": "NEW PORT RICHEY, FL 34655"

                                    },

                                    "dlNumber": "B640693682100",

                                    "dlState": "FL",

                                    "dob": "20030923",

                                    "gender": "F",

                                    "height": "5'6",

                                    "license": {

                                        "class": "E",

                                        "status": "VALID",

                                        "IssuedDate": "20220301",

                                        "ExpirationDate": "20300701",

                                        "OriginalIssueDate": "20010301",

                                        "restriction": "A"

                                    },

                                    "detail": "OrderType : MvrIndicator \- REQUESTED AS: LORNA          P          BONZHEIM                  DOB: 09232003  LICENSE : B640693682100 PERS:01: ACTIVE          VALID   E              0301202207012030                A LIC CLASS: E                       DESC: OPERATOR LIC STATUS: VALID LIC ISSUED: 03/01/2022 LIC EXPIRES: 07/01/2030 LIC RESTR: A                          DESC: CORRECTIVE LENSES PERS:02: EXPIRED         EXPIRED ID CARD        0901200312012017 LIC CLASS: ID CARD                 DESC: ID CARD LIC STATUS: EXPIRED LIC ISSUED: 09/01/2003 LIC EXPIRES: 12/01/2017 AS OF NOVEMBER 20, 2020 AT 9:45:15 AM, DRIVER PRIVILEGE B640-693-68-210-0 IS VALID. PERSONAL INFORMATION IS PROTECTED PURSUANT TO THE DRIVER PRIVACY PROTECTION ACT. ENTRIES BELOW ARE A THREE YEAR RECORD. ORIGINAL ISSUE DATE: 03/01/2001 REAL ID COMPLIANT US CITIZEN BLOCKED PERSONAL INFORMATION BLOCKED FOR MAILING LIST PERSON HAS A DIGITAL IMAGE ELIGIBLE TO ELECT DRIVER SCHOOL.  DRIVER HAS MADE 2 ELECTIONS. LAST ELECTION WAS ON 06/01/2002. VIOLATIONS COMMITTED WHILE A CDL HOLDER OR IN A CMV VEHICLE ARE NOT ELIGIBLE FOR DRIVING SCHOOL ELECTION. COUNTY: BROWARD RESIDENTIAL ADDRESS: 7923 NW 18TH ST APT 203  MARGATE, FL  33063  COUNTY: BROWARD ISSUANCE HISTORY: LIC CLASS: CLASS E   ISSUE DATE: 09/01/2001   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 06/01/2002   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 06/01/2002   ISSUE TYPE: REPLACEMENT LIC CLASS: ID CARD   ISSUE DATE: 06/01/2002   ISSUE TYPE: DUPLICATE LIC CLASS: CLASS E   ISSUE DATE: 03/01/2004   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 06/01/2006   ISSUE TYPE: ADDRESS CHANGE LIC CLASS: CLASS E   ISSUE DATE: 12/01/2017   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 12/01/2019   ISSUE TYPE: REPLACEMENT LIC CLASS: CLASS E   ISSUE DATE: 06/01/2020   ISSUE TYPE: CDR/CDT CLEARANCE LIC CLASS: CLASS E   ISSUE DATE: 08/01/2020   ISSUE TYPE: CDR/CDT CLEARANCE EXAMS TAKEN: VISION               DATE TAKEN: 03/01/2022   COUNT: 1   STATUS: PASS ROAD SIGN            DATE TAKEN: 03/01/2022   COUNT: 9   STATUS: RECIPROCATED ROAD RULES           DATE TAKEN: 03/01/2022   COUNT: 3   STATUS: PASS DRIVING              DATE TAKEN: 09/01/2021   COUNT: 4   STATUS: PASS This report is generated for insurance purposes only and may not be used for any other purpose.  The use and dissemination of the report and information in it must comply with your iiX agreement and the  Fair Credit Reporting Act, the Driver's Privacy Protection Act, and any applicable state statute(s).  The data in the report from the applicable state agency or service bureau is provided through iiX \\"as is.\\" \--- Customer-defined MVR scoring has been applied to this record.  Customer  is solely responsible for the application and use of the resulting score.",

                                    "violations": \[

                                        {

                                            "violationType": "SUSP",

                                            "violationDate": "20210701",

                                            "customCode": "130110",

                                            "customPoints": "3",

                                            "detail": "FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 730115590 NOTICED PROVIDED: 06/01/2021 ADDED TO RECORD: 06/01/2021 SANCTION CODE: 7"

                                        },

                                        {

                                            "violationType": "REIN",

                                            "convictionDate": "20211201",

                                            "customCode": "330130",

                                            "customPoints": "-3",

                                            "detail": "REINSTATED"

                                        },

                                        {

                                            "violationType": "SUSP",

                                            "violationDate": "20200401",

                                            "customCode": "130110",

                                            "customPoints": "0",

                                            "detail": "FR-CANCELLATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 730195358 NOTICED PROVIDED: 04/01/2020 ADDED TO RECORD: 04/01/2020 SANCTION CODE: 7"

                                        },

                                        {

                                            "violationType": "REIN",

                                            "convictionDate": "20200601",

                                            "customCode": "330130",

                                            "customPoints": "0",

                                            "detail": "REINSTATED"

                                        },

                                        {

                                            "violationType": "SUSP",

                                            "violationDate": "20200801",

                                            "customCode": "130110",

                                            "customPoints": "0",

                                            "detail": "FR-REGISTRATION PERSONAL INJURY PROTECTION/PROPERTY DAMAGE LIABILITY(PIP) SUSPENSION CASE NUMBER 830111729 NOTICED PROVIDED: 07/01/2020 ADDED TO RECORD: 07/01/2020 SANCTION CODE: 8"

                                        },

                                        {

                                            "violationType": "REIN",

                                            "convictionDate": "20200801",

                                            "customCode": "330130",

                                            "customPoints": "0",

                                            "detail": "REINSTATED"

                                        },

                                        {

                                            "violationType": "VIOL",

                                            "violationDate": "20220201",

                                            "convictionDate": "20220501",

                                            "stateAssignedPoints": "4",

                                            "customCode": "424300",

                                            "customPoints": "1",

                                            "detail": "FAIL TO YIELD UNSIGNED INTERSECTION DISPOSITION WAS GUILTY COUNTY COURT CRASH INDICATED VIOLATION NUMBER: 5 CITATION NUMBER: A0LU14E COUNTY: BROWARD ADDED TO RECORD: 05/01/2022 DISPOSITION CODE: 513"

                                        },

                                        {

                                            "violationType": "VIOL",

                                            "violationDate": "20211201",

                                            "convictionDate": "20220201",

                                            "stateAssignedPoints": "0",

                                            "customCode": "536400",

                                            "customPoints": "1",

                                            "detail": "EXPIRED TAG \- 6 MOS OR LESS DISPOSITION WAS GUILTY COUNTY COURT VIOLATION NUMBER: 6 CITATION NUMBER: AR9P4UE COUNTY: BROWARD STATE: FL ADDED TO RECORD: 02/01/2022 DISPOSITION CODE: 473"

                                        }

                                    \]

                                }

                            }

                        \]

                    },

                    "statusCode": 200

                },

                {

                    "header": {

                        "quoteback": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57",

                        "transactionId": "0438c73a-1ab4-462a-90a6-ed0b67f92dd7"

                    },

                    "body": {

                        "orderNumber": "935981068",

                        "motorVehicleReports": \[

                            {

                                "status": {

                                    "code": "N",

                                    "description": "NOT FOUND"

                                },

                                "violationsType": {

                                    "code": "N",

                                    "description": "Not Coded"

                                },

                                "driver": {

                                    "dlNumber": "S420665834256",

                                    "dlState": "FL",

                                    "detail": "OrderType : MvrIndicator \- "

                                }

                            }

                        \]

                    },

                    "statusCode": 200

                },

                {

                    "header": {

                        "quoteback": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57",

                        "transactionId": "d1d6dcd6-9568-4c9d-9068-f7522365a9b9"

                    },

                    "body": {

                        "orderNumber": "935981077",

                        "motorVehicleReports": \[

                            {

                                "status": {

                                    "code": "N",

                                    "description": "NOT FOUND"

                                },

                                "violationsType": {

                                    "code": "N",

                                    "description": "Not Coded"

                                },

                                "driver": {

                                    "dlNumber": "P420665934225",

                                    "dlState": "FL",

                                    "detail": "OrderType : MvrIndicator \- "

                                }

                            }

                        \]

                    },

                    "statusCode": 200

                },

                {

                    "header": {

                        "quoteback": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57",

                        "transactionId": "d9098699-2d86-4b89-8374-3d4afdc2dcf6"

                    },

                    "body": {

                        "orderNumber": "935981075",

                        "motorVehicleReports": \[

                            {

                                "status": {

                                    "code": "N",

                                    "description": "NOT FOUND"

                                },

                                "violationsType": {

                                    "code": "N",

                                    "description": "Not Coded"

                                },

                                "driver": {

                                    "dlNumber": "R420622534333",

                                    "dlState": "FL",

                                    "detail": "OrderType : MvrIndicator \- "

                                }

                            }

                        \]

                    },

                    "statusCode": 200

                },

                {

                    "header": {

                        "quoteback": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57",

                        "transactionId": "ff23414c-be5c-4268-831f-b061d969de72"

                    },

                    "body": {

                        "orderNumber": "935981073",

                        "motorVehicleReports": \[

                            {

                                "status": {

                                    "code": "N",

                                    "description": "NOT FOUND"

                                },

                                "violationsType": {

                                    "code": "N",

                                    "description": "Not Coded"

                                },

                                "driver": {

                                    "dlNumber": "L420625834362",

                                    "dlState": "FL",

                                    "detail": "OrderType : MvrIndicator \- "

                                }

                            }

                        \]

                    },

                    "statusCode": 200

                },

                {

                    "header": {

                        "quoteback": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57",

                        "transactionId": "5445f6aa-5ec9-4c41-92ef-7efc1ec32aaf"

                    },

                    "body": {

                        "orderNumber": "935981069",

                        "motorVehicleReports": \[

                            {

                                "status": {

                                    "code": "N",

                                    "description": "NOT FOUND"

                                },

                                "violationsType": {

                                    "code": "N",

                                    "description": "Not Coded"

                                },

                                "driver": {

                                    "dlNumber": "T123654125803",

                                    "dlState": "FL",

                                    "detail": "OrderType : MvrIndicator \- "

                                }

                            }

                        \]

                    },

                    "statusCode": 200

                }

            \],

            "vinMasterReport": \[

                {

                    "header": {

                        "transactionId": "16e6749a-647e-4efc-abe8-215afaca0043",

                        "quoteback": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57"

                    },

                    "body": \[

                        {

                            "requestedVIN": "1G5CT18B5F8530675",

                            "message": "LPMP Symbols not available for model years before 1998.",

                            "vin": "1G5CT18B\&F",

                            "modelYear": "85",

                            "isoUse": "4223",

                            "restraint": "A",

                            "antiLockBrakes": "N",

                            "engineCylinders": "6",

                            "combinedVSRSymbol\_OnePosition": "J",

                            "priceNewSymbol\_27SymbolTable\_OnePosition": "J",

                            "make": "GMC",

                            "basicModelName": "JIMMY S-15",

                            "bodyStyle": "UTIL 4X4",

                            "engineSize": "173",

                            "fourWheelDriveIndicator": "4",

                            "fullModelName": "JIMMY S-15",

                            "ncicCode": "GMC",

                            "combinedVSRSymbol\_TwoPositions": "10",

                            "priceNewSymbol\_27SymbolTable\_TwoPositions": "10",

                            "vinChangeIndicatorDescription": "No Change to VIN",

                            "restraintDescription": "Driver & Front Passenger Active Restraints",

                            "antiLockBrakesDescription": "Anti-Lock Brakes are not available",

                            "engineCylindersDescription": "Six-Cylinder Engine",

                            "engineTypeDescription": "Other Type of Engine",

                            "symbolChangeIndicatorDescription": "No change to the Symbol fields",

                            "fieldChangeIndicatorDescription": "Field not added to VINMASTER until model year 1995",

                            "makeDescription": "GMC",

                            "countrywidePerformanceDescription": "Standard Performance",

                            "nonVSRPerformanceDescription": "Standard Performance",

                            "bodyStyleDescription": "Utility Vehicle \- Four-Wheel Drive",

                            "fourWheelDriveIndicatorDescription": "Vehicle is four-wheel drive",

                            "electronicStabilityControlDescription": "Field not added to VINMASTER until model year 1995",

                            "daytimeRunningLightIndicatorDescription": "Field not added to VINMASTER until model year 1995",

                            "ncicCodeDescription": "GMC",

                            "antiTheftIndicatorDescription": "Field not added to VINMASTER until model year 1990",

                            "priceNew\_Min": "10001.00",

                            "priceNew\_Max": "12500.99",

                            "fullModelYear": "1985",

                            "recordType": "S"

                        },

                        {

                            "requestedVIN": "1GKER23788J291227",

                            "message": "Specify LPMPFiling value for LPMP Symbols.",

                            "vin": "1GK\&R237&8",

                            "modelYear": "08",

                            "isoUse": "4375",

                            "effectiveDate": "1010",

                            "restraint": "R",

                            "antiLockBrakes": "S",

                            "engineCylinders": "6",

                            "combinedVSRSymbol\_OnePosition": "E",

                            "priceNewSymbol\_27SymbolTable\_OnePosition": "N",

                            "make": "GMC",

                            "basicModelName": "ACADIA",

                            "bodyStyle": "UTL4X24D",

                            "engineSize": "3.6",

                            "electronicStabilityControl": "S",

                            "tonnageIndicator": "13",

                            "payloadCapacity": "1678",

                            "fullModelName": "ACADIA SLT1",

                            "daytimeRunningLightIndicator": "S",

                            "ncicCode": "GMC",

                            "circularNumber": "1010",

                            "combinedVSRSymbol\_TwoPositions": "12",

                            "priceNewSymbol\_27SymbolTable\_TwoPositions": "20",

                            "wheelbase": "118.9",

                            "classCode": "93",

                            "antiTheftIndicator": "P",

                            "curbWeight": "04722",

                            "grossVehicleWeight": "06400",

                            "height": "069.9",

                            "horsepower": "0275",

                            "vinChangeIndicatorDescription": "No Change to VIN",

                            "restraintDescription": "Driver & Front Passenger Front, Side & Head Airbags, Rear Passenger Head Airbags",

                            "antiLockBrakesDescription": "Anti-Lock Brakes are standard equipment",

                            "engineCylindersDescription": "Six-Cylinder Engine",

                            "engineTypeDescription": "Other Type of Engine",

                            "symbolChangeIndicatorDescription": "No change to the Symbol fields",

                            "fieldChangeIndicatorDescription": "No change to Information fields",

                            "makeDescription": "GMC",

                            "bodyStyleDescription": "Utility Vehicle \- Two-Wheel Drive 4-Door",

                            "fourWheelDriveIndicatorDescription": "Vehicle is not four-wheel drive",

                            "vmPerformanceIndicatorDescription": "Standard",

                            "electronicStabilityControlDescription": "Electronic Stability Control is standard equipment",

                            "tonnageIndicatorDescription": "3.25 tons (06001 to 06500 lbs)",

                            "daytimeRunningLightIndicatorDescription": "Daytime Running Lights Standard Equipment",

                            "ncicCodeDescription": "GMC",

                            "classCodeDescription": "Large Utility",

                            "antiTheftIndicatorDescription": "Passive Disabling",

                            "priceNew\_Min": "33001.00",

                            "priceNew\_Max": "36000.99",

                            "fullModelYear": "2008",

                            "recordType": "S"

                        },

                        {

                            "requestedVIN": "1HGCM56306A148752",

                            "message": "Specify LPMPFiling value for LPMP Symbols.",

                            "vin": "1HGCM563&6",

                            "modelYear": "06",

                            "isoUse": "5503",

                            "restraint": "R",

                            "antiLockBrakes": "S",

                            "engineCylinders": "4",

                            "combinedVSRSymbol\_OnePosition": "E",

                            "priceNewSymbol\_27SymbolTable\_OnePosition": "G",

                            "make": "HOND",

                            "basicModelName": "ACCORD",

                            "bodyStyle": "SEDAN 4D",

                            "engineSize": "2.4",

                            "electronicStabilityControl": "O",

                            "tonnageIndicator": "00",

                            "payloadCapacity": "0000",

                            "fullModelName": "ACCORD SE",

                            "daytimeRunningLightIndicator": "S",

                            "ncicCode": "HOND",

                            "circularNumber": "0512",

                            "combinedVSRSymbol\_TwoPositions": "12",

                            "priceNewSymbol\_27SymbolTable\_TwoPositions": "14",

                            "wheelbase": "107.9",

                            "classCode": "34",

                            "antiTheftIndicator": "P",

                            "curbWeight": "03197",

                            "grossVehicleWeight": "00000",

                            "height": "057.2",

                            "horsepower": "0166",

                            "vinChangeIndicatorDescription": "No Change to VIN",

                            "restraintDescription": "Driver & Front Passenger Front, Side & Head Airbags, Rear Passenger Head Airbags",

                            "antiLockBrakesDescription": "Anti-Lock Brakes are standard equipment",

                            "engineCylindersDescription": "Four-Cylinder Engine",

                            "engineTypeDescription": "Other Type of Engine",

                            "symbolChangeIndicatorDescription": "No change to the Symbol fields",

                            "fieldChangeIndicatorDescription": "No change to Information fields",

                            "makeDescription": "HONDA",

                            "bodyStyleDescription": "4-Door Sedan",

                            "fourWheelDriveIndicatorDescription": "Vehicle is not four-wheel drive",

                            "vmPerformanceIndicatorDescription": "Standard",

                            "electronicStabilityControlDescription": "Electronic Stability Control is optional equipment",

                            "tonnageIndicatorDescription": "N/A",

                            "daytimeRunningLightIndicatorDescription": "Daytime Running Lights Standard Equipment",

                            "ncicCodeDescription": "HONDA",

                            "classCodeDescription": "Midsize 4-Door",

                            "antiTheftIndicatorDescription": "Passive Disabling",

                            "priceNew\_Min": "20001.00",

                            "priceNew\_Max": "22000.99",

                            "fullModelYear": "2006",

                            "recordType": "S"

                        },

                        {

                            "requestedVIN": "3GNFK16T9YG218125",

                            "message": "Specify LPMPFiling value for LPMP Symbols.",

                            "vin": "3GN\&K16T\&Y",

                            "modelYear": "00",

                            "isoUse": "2452",

                            "restraint": "S",

                            "antiLockBrakes": "S",

                            "engineCylinders": "8",

                            "combinedVSRSymbol\_OnePosition": "F",

                            "priceNewSymbol\_27SymbolTable\_OnePosition": "P",

                            "make": "CHEV",

                            "basicModelName": "SUBURBAN",

                            "bodyStyle": "UTL4X44D",

                            "engineSize": "5.3",

                            "fourWheelDriveIndicator": "4",

                            "electronicStabilityControl": "N",

                            "tonnageIndicator": "15",

                            "payloadCapacity": "2077",

                            "fullModelName": "SUBURBAN 1500 BASE/LS/LT",

                            "daytimeRunningLightIndicator": "S",

                            "ncicCode": "CHEV",

                            "circularNumber": "0001",

                            "combinedVSRSymbol\_TwoPositions": "13",

                            "priceNewSymbol\_27SymbolTable\_TwoPositions": "21",

                            "wheelbase": "130.0",

                            "classCode": "93",

                            "antiTheftIndicator": "P",

                            "curbWeight": "05123",

                            "grossVehicleWeight": "07200",

                            "height": "073.3",

                            "horsepower": "0285",

                            "vinChangeIndicatorDescription": "No Change to VIN",

                            "restraintDescription": "Driver & Front Passenger Front & Side Airbags",

                            "antiLockBrakesDescription": "Anti-Lock Brakes are standard equipment",

                            "engineCylindersDescription": "Eight-Cylinder Engine",

                            "engineTypeDescription": "Other Type of Engine",

                            "symbolChangeIndicatorDescription": "No change to the Symbol fields",

                            "fieldChangeIndicatorDescription": "No change to Information fields",

                            "makeDescription": "CHEVROLET",

                            "countrywidePerformanceDescription": "Standard Performance",

                            "bodyStyleDescription": "Utility Vehicle \- Four-Wheel Drive 4-Door",

                            "fourWheelDriveIndicatorDescription": "Vehicle is four-wheel drive",

                            "electronicStabilityControlDescription": "Electronic Stability Control is not available",

                            "tonnageIndicatorDescription": "3.75 tons (07001 to 07500 lbs)",

                            "daytimeRunningLightIndicatorDescription": "Daytime Running Lights Standard Equipment",

                            "ncicCodeDescription": "CHEVROLET",

                            "classCodeDescription": "Large Utility",

                            "antiTheftIndicatorDescription": "Passive Disabling",

                            "priceNew\_Min": "36001.00",

                            "priceNew\_Max": "40000.99",

                            "fullModelYear": "2000",

                            "recordType": "S"

                        }

                    \]

                }

            \],

            "vesmReport": {

                "visResponse": {

                    "responseHeader": {

                        "transactionId": "7824a021-f95f-4868-9c93-b6d6a4927ace",

                        "statusCd": "200",

                        "statusDescription": "Success"

                    },

                    "responseBody": {

                        "smartScoreResult": {

                            "vehicles": \[

                                {

                                    "responseVin": "1G5CT18B5F8530675",

                                    "responseFirstName": "DOUGLAS",

                                    "responseLastName": "BONZHEIM",

                                    "responseAddress": {

                                        "street": "7827 ADELAIDE LP",

                                        "city": "NEW PORT RICHEY",

                                        "state": "FL",

                                        "country": "US",

                                        "postalCd": "34655"

                                    },

                                    "make": "GMC",

                                    "model": "S15",

                                    "year": "1985",

                                    "enrollmentStatus": "EN",

                                    "enrollmentDate": "2022-01-01 05:00:41.394",

                                    "scoreStatus": "SU",

                                    "scoreType": "Recent",

                                    "score": "85",

                                    "scoreStartDate": "2022-11-14 00:00:00.000",

                                    "scoreEndDate": "2023-01-22 23:59:59.000",

                                    "productEnrollmentStatus": "EN"

                                },

                                {

                                    "responseVin": "3GNFK16T9YG218125",

                                    "responseFirstName": "DOUGLAS",

                                    "responseLastName": "BONZHEIM",

                                    "responseAddress": {

                                        "street": "7827 ADELAIDE LP",

                                        "city": "NEW PORT RICHEY",

                                        "state": "FL",

                                        "country": "US",

                                        "postalCd": "34655"

                                    },

                                    "make": "CHEV",

                                    "model": "SUBURBAN",

                                    "year": "2000",

                                    "enrollmentStatus": "EN",

                                    "enrollmentDate": "2022-01-01 05:00:41.394",

                                    "scoreStatus": "SU",

                                    "scoreType": "Recent",

                                    "score": "100",

                                    "scoreStartDate": "2022-11-21 00:00:00.000",

                                    "scoreEndDate": "2023-01-29 23:59:59.000",

                                    "productEnrollmentStatus": "EN"

                                },

                                {

                                    "responseVin": "1GKER23788J291227",

                                    "responseFirstName": "DOUGLAS",

                                    "responseLastName": "BONZHEIM",

                                    "responseAddress": {

                                        "street": "7827 ADELAIDE LP",

                                        "city": "NEW PORT RICHEY",

                                        "state": "FL",

                                        "country": "US",

                                        "postalCd": "34655"

                                    },

                                    "make": "GMC",

                                    "model": "ACADIA",

                                    "year": "2008",

                                    "enrollmentStatus": "EN",

                                    "enrollmentDate": "2022-01-01 05:00:41.394",

                                    "scoreStatus": "SU",

                                    "scoreType": "Recent",

                                    "score": "86",

                                    "scoreStartDate": "2022-11-21 00:00:00.000",

                                    "scoreEndDate": "2023-01-29 23:59:59.000",

                                    "productEnrollmentStatus": "EN"

                                }

                            \]

                        }

                    }

                }

            },

            "mileageReport": {

                "header": {

                    "transactionId": "dc1702d1-bead-4b7a-9ce0-a0d2c7c79479",

                    "quoteback": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57"

                },

                "body": {

                    "statusCode": 200,

                    "mileageReports": \[

                        {

                            "vin": "1GKER23788J291227",

                            "message": null,

                            "estimateAnnualMiles": {

                                "sources": \[

                                    {

                                        "name": "VeriskMileageModel",

                                        "miles": "11080"

                                    }

                                \]

                            }

                        },

                        {

                            "vin": "1HGCM56306A148752",

                            "message": null,

                            "estimateAnnualMiles": {

                                "sources": \[

                                    {

                                        "name": "VeriskMileageModel",

                                        "miles": "11059"

                                    }

                                \]

                            }

                        },

                        {

                            "vin": "3GNFK16T9YG218125",

                            "message": null,

                            "estimateAnnualMiles": {

                                "sources": \[

                                    {

                                        "name": "VeriskMileageModel",

                                        "miles": "8218"

                                    }

                                \]

                            }

                        },

                        {

                            "vin": "1G5CT18B5F8530675",

                            "message": null,

                            "estimateAnnualMiles": {

                                "sources": \[

                                    {

                                        "name": "VeriskMileageModel",

                                        "miles": "3743"

                                    }

                                \]

                            }

                        }

                    \]

                }

            },

            "inflectionCBISReport": {

                "header": {

                    "transactionId": "d94fada0-0f0e-4e36-b62d-96ad74d5966a",

                    "quoteback": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57"

                },

                "body": {

                    "statusCode": 200,

                    "status": "completed",

                    "consumers": {

                        "equifaxUSConsumerCreditReport": \[

                            {

                                "identifier": "Individual Report 1",

                                "customerReferenceNumber": "D94FADA00F0E4E36B62D",

                                "customerNumber": "999ZZ61019",

                                "consumerReferralCode": "181",

                                "multipleReportIndicator": "F",

                                "ecoaInquiryType": "I",

                                "hitCode": {

                                    "code": "2",

                                    "description": "No-Hit"

                                }

                            }

                        \]

                    },

                    "links": \[

                        {

                            "identifier": "Individual Report 1",

                            "type": "GET",

                            "href": "/business/consumer-credit/v1/reports/credit-report/ee9adc19-e5c8-4ef9-51fd-14c83e8e08ce"

                        }

                    \]

                }

            },

            "riskAnalyzerReports": \[

                {

                    "header": {

                        "quoteback": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57",

                        "transactionId": "40082828-8430-4e5b-96d9-32f79fd02fd2"

                    },

                    "body": \[

                        {

                            "requestedVin": "1G5CT18B5F8530675",

                            "vehicle": {

                                "vin": "1G5CT18B\&F",

                                "modelYear": "1985",

                                "distributionDate": "2212",

                                "restraint": "A",

                                "antiLockBrakes": "N",

                                "engineCylinders": "6",

                                "make": "GMC",

                                "basicModelName": "JIMMY S-15",

                                "bodyStyle": "UTIL 4X4",

                                "engineSize": "173",

                                "fourWheelDriveIndicator": "4",

                                "payloadCapacity": "0",

                                "fullModelName": "JIMMY S-15",

                                "wheelbase": "0",

                                "curbWeight": "0",

                                "grossVehicleWeight": "0",

                                "height": "0",

                                "horsepower": "0",

                                "stateException": "TX",

                                "ncicCode": "GMC",

                                "length": "0",

                                "width": "0",

                                "baseMSRP": "10001",

                                "specialHandlingIndicator": "N",

                                "interimIndicator": "N",

                                "releaseDate": "2303"

                            },

                            "physicalDamage": {

                                "riskAnalyzerCollisionIndicatedSymbol": "BC",

                                "riskAnalyzerComprehensiveIndicatedSymbol": "AB",

                                "riskAnalyzerCollisionIndicatedSymbolRelativity": "0.5992",

                                "riskAnalyzerComprehensiveIndicatedSymbolRelativity": "0.4702",

                                "riskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar1": "0.6375",

                                "riskAnalyzerCollisionRatingSymbolRelativity": "0.5992",

                                "riskAnalyzerCollisionRatingSymbol": "BC",

                                "riskAnalyzerComprehensiveRatingSymbolRelativity": "0.4702",

                                "riskAnalyzerComprehensiveRatingSymbol": "AB",

                                "riskAnalyzerComprehensiveNonGlassRatingSymbolRelativity": "0.4702",

                                "riskAnalyzerComprehensiveNonGlassRatingSymbol": "AB",

                                "riskAnalyzerCollisionIndicatedSymbolRelativityChar1": "0.7375",

                                "riskAnalyzerComprehensiveIndicatedSymbolRelativityChar1": "0.6375",

                                "riskAnalyzerCollisionIndicatedSymbolRelativityChar2": "0.8125",

                                "riskAnalyzerComprehensiveIndicatedSymbolRelativityChar2": "0.7375",

                                "riskAnalyzerCollisionCappingIndicator": "N",

                                "riskAnalyzerComprehensiveCappingIndicator": "N",

                                "riskAnalyzerComprehensiveNonGlassCappingIndicator": "N",

                                "riskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar2": "0.7375",

                                "riskAnalyzerComprehensiveNonGlassIndicatedSymbol": "AB",

                                "riskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativity": "0.4702"

                            },

                            "liability": {

                                "riskAnalyzerMedicalPaymentsIndicatedSymbol": "FB",

                                "riskAnalyzerPersonalInjuryProtectionIndicatedSymbol": "VB",

                                "riskAnalyzerSingleLimitIndicatedSymbol": "JF",

                                "riskAnalyzerBodilyInjuryIndicatedSymbolRelativity": "0.9263",

                                "riskAnalyzerPropertyDamageIndicatedSymbolRelativity": "0.7922",

                                "riskAnalyzerMedicalPaymentsIndicatedSymbolRelativity": "0.6638",

                                "riskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativity": "0.885",

                                "riskAnalyzerSingleLimitIndicatedSymbolRelativity": "0.8775",

                                "riskAnalyzerBodilyInjuryRatingSymbolRelativity": "0.9263",

                                "riskAnalyzerBodilyInjuryRatingSymbol": "JH",

                                "riskAnalyzerPropertyDamageRatingSymbolRelativity": "0.7922",

                                "riskAnalyzerPropertyDamageRatingSymbol": "JC",

                                "riskAnalyzerMedicalPaymentsRatingSymbolRelativity": "0.6638",

                                "riskAnalyzerMedicalPaymentsRatingSymbol": "FB",

                                "riskAnalyzerPersonalInjuryProtectionRatingSymbolRelativity": "0.885",

                                "riskAnalyzerPersonalInjuryProtectionRatingSymbol": "VB",

                                "riskAnalyzerSingleLimitRatingSymbolRelativity": "0.8775",

                                "riskAnalyzerSingleLimitRatingSymbol": "JF",

                                "riskAnalyzerBodilyInjuryCappingIndicator": "N",

                                "riskAnalyzerPropertyDamageCappingIndicator": "N",

                                "riskAnalyzerMedicalPaymentsCappingIndicator": "N",

                                "riskAnalyzerPersonalInjuryProtectionCappingIndicator": "N",

                                "riskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar1": "0.975",

                                "riskAnalyzerPropertyDamageIndicatedSymbolRelativityChar1": "0.975",

                                "riskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar1": "0.9",

                                "riskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar1": "1.2",

                                "riskAnalyzerSingleLimitIndicatedSymbolRelativityChar1": "0.975",

                                "riskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar2": "0.95",

                                "riskAnalyzerPropertyDamageIndicatedSymbolRelativityChar2": "0.8125",

                                "riskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar2": "0.7375",

                                "riskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar2": "0.7375",

                                "riskAnalyzerSingleLimitIndicatedSymbolRelativityChar2": "0.9",

                                "riskAnalyzerBodilyInjuryIndicatedSymbol": "JH",

                                "riskAnalyzerPropertyDamageIndicatedSymbol": "JC",

                                "riskAnalyzerSingleLimitCappingIndicator": "N"

                            }

                        }

                    \]

                },

                {

                    "header": {

                        "quoteback": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57",

                        "transactionId": "14e9f971-2667-4570-ba05-2490c5f517d2"

                    },

                    "body": \[

                        {

                            "requestedVin": "3GNFK16T9YG218125",

                            "vehicle": {

                                "vin": "3GN\&K16T\&Y",

                                "modelYear": "2000",

                                "distributionDate": "2212",

                                "restraint": "S",

                                "antiLockBrakes": "S",

                                "engineCylinders": "8",

                                "make": "CHEV",

                                "basicModelName": "SUBURBAN",

                                "bodyStyle": "UTL4X44D",

                                "engineSize": "5.3",

                                "fourWheelDriveIndicator": "4",

                                "electronicStabilityControl": "N",

                                "tonnageIndicator": "15",

                                "payloadCapacity": "2077",

                                "fullModelName": "SUBURBAN 1500 BASE/LS/LT",

                                "daytimeRunningLightIndicator": "S",

                                "wheelbase": "130",

                                "classCode": "93",

                                "antiTheftIndicator": "P",

                                "curbWeight": "5123",

                                "grossVehicleWeight": "7200",

                                "height": "73.3",

                                "horsepower": "285",

                                "stateException": "TX",

                                "ncicCode": "CHEV",

                                "length": "0",

                                "width": "0",

                                "baseMSRP": "36001",

                                "specialHandlingIndicator": "N",

                                "interimIndicator": "N",

                                "releaseDate": "2303"

                            },

                            "physicalDamage": {

                                "riskAnalyzerCollisionIndicatedSymbol": "EJ",

                                "riskAnalyzerComprehensiveIndicatedSymbol": "DG",

                                "riskAnalyzerCollisionIndicatedSymbolRelativity": "0.8531",

                                "riskAnalyzerComprehensiveIndicatedSymbolRelativity": "0.7863",

                                "riskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar1": "0.85",

                                "riskAnalyzerCollisionRatingSymbolRelativity": "0.8531",

                                "riskAnalyzerCollisionRatingSymbol": "EJ",

                                "riskAnalyzerComprehensiveRatingSymbolRelativity": "0.7863",

                                "riskAnalyzerComprehensiveRatingSymbol": "DG",

                                "riskAnalyzerComprehensiveNonGlassRatingSymbolRelativity": "0.7863",

                                "riskAnalyzerComprehensiveNonGlassRatingSymbol": "DG",

                                "riskAnalyzerCollisionIndicatedSymbolRelativityChar1": "0.875",

                                "riskAnalyzerComprehensiveIndicatedSymbolRelativityChar1": "0.85",

                                "riskAnalyzerCollisionIndicatedSymbolRelativityChar2": "0.975",

                                "riskAnalyzerComprehensiveIndicatedSymbolRelativityChar2": "0.925",

                                "riskAnalyzerCollisionCappingIndicator": "N",

                                "riskAnalyzerComprehensiveCappingIndicator": "N",

                                "riskAnalyzerComprehensiveNonGlassCappingIndicator": "N",

                                "riskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar2": "0.925",

                                "riskAnalyzerComprehensiveNonGlassIndicatedSymbol": "DG",

                                "riskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativity": "0.7863"

                            },

                            "liability": {

                                "riskAnalyzerMedicalPaymentsIndicatedSymbol": "FE",

                                "riskAnalyzerPersonalInjuryProtectionIndicatedSymbol": "EH",

                                "riskAnalyzerSingleLimitIndicatedSymbol": "MK",

                                "riskAnalyzerBodilyInjuryIndicatedSymbolRelativity": "0.9738",

                                "riskAnalyzerPropertyDamageIndicatedSymbolRelativity": "1.1288",

                                "riskAnalyzerMedicalPaymentsIndicatedSymbolRelativity": "0.7875",

                                "riskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativity": "0.8313",

                                "riskAnalyzerSingleLimitIndicatedSymbolRelativity": "1.05",

                                "riskAnalyzerBodilyInjuryRatingSymbolRelativity": "0.9738",

                                "riskAnalyzerBodilyInjuryRatingSymbol": "LH",

                                "riskAnalyzerPropertyDamageRatingSymbolRelativity": "1.1288",

                                "riskAnalyzerPropertyDamageRatingSymbol": "MN",

                                "riskAnalyzerMedicalPaymentsRatingSymbolRelativity": "0.7875",

                                "riskAnalyzerMedicalPaymentsRatingSymbol": "FE",

                                "riskAnalyzerPersonalInjuryProtectionRatingSymbolRelativity": "0.8313",

                                "riskAnalyzerPersonalInjuryProtectionRatingSymbol": "EH",

                                "riskAnalyzerSingleLimitRatingSymbolRelativity": "1.05",

                                "riskAnalyzerSingleLimitRatingSymbol": "MK",

                                "riskAnalyzerBodilyInjuryCappingIndicator": "N",

                                "riskAnalyzerPropertyDamageCappingIndicator": "N",

                                "riskAnalyzerMedicalPaymentsCappingIndicator": "N",

                                "riskAnalyzerPersonalInjuryProtectionCappingIndicator": "N",

                                "riskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar1": "1.025",

                                "riskAnalyzerPropertyDamageIndicatedSymbolRelativityChar1": "1.05",

                                "riskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar1": "0.9",

                                "riskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar1": "0.875",

                                "riskAnalyzerSingleLimitIndicatedSymbolRelativityChar1": "1.05",

                                "riskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar2": "0.95",

                                "riskAnalyzerPropertyDamageIndicatedSymbolRelativityChar2": "1.075",

                                "riskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar2": "0.875",

                                "riskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar2": "0.95",

                                "riskAnalyzerSingleLimitIndicatedSymbolRelativityChar2": "1",

                                "riskAnalyzerBodilyInjuryIndicatedSymbol": "LH",

                                "riskAnalyzerPropertyDamageIndicatedSymbol": "MN",

                                "riskAnalyzerSingleLimitCappingIndicator": "N"

                            }

                        }

                    \]

                },

                {

                    "header": {

                        "quoteback": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57",

                        "transactionId": "a28d6dd1-4012-48c6-b771-55d5c5f36a70"

                    },

                    "body": \[

                        {

                            "requestedVin": "1HGCM56306A148752",

                            "vehicle": {

                                "vin": "1HGCM563&6",

                                "modelYear": "2006",

                                "distributionDate": "2212",

                                "restraint": "R",

                                "antiLockBrakes": "S",

                                "engineCylinders": "4",

                                "make": "HOND",

                                "basicModelName": "ACCORD",

                                "bodyStyle": "SEDAN 4D",

                                "engineSize": "2.4",

                                "electronicStabilityControl": "O",

                                "tonnageIndicator": "00",

                                "payloadCapacity": "0",

                                "fullModelName": "ACCORD SE",

                                "daytimeRunningLightIndicator": "S",

                                "wheelbase": "107.9",

                                "classCode": "34",

                                "antiTheftIndicator": "P",

                                "curbWeight": "3197",

                                "grossVehicleWeight": "0",

                                "height": "57.2",

                                "horsepower": "166",

                                "ncicCode": "HOND",

                                "chassis": "U",

                                "length": "0",

                                "width": "0",

                                "baseMSRP": "20001",

                                "specialHandlingIndicator": "N",

                                "interimIndicator": "N",

                                "specialInfoSelector": "M",

                                "modelSeriesInfo": "CURB",

                                "releaseDate": "2303"

                            },

                            "physicalDamage": {

                                "riskAnalyzerCollisionIndicatedSymbol": "DM",

                                "riskAnalyzerComprehensiveIndicatedSymbol": "CE",

                                "riskAnalyzerCollisionIndicatedSymbolRelativity": "0.8925",

                                "riskAnalyzerComprehensiveIndicatedSymbolRelativity": "0.7109",

                                "riskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar1": "0.8125",

                                "riskAnalyzerCollisionRatingSymbolRelativity": "0.8925",

                                "riskAnalyzerCollisionRatingSymbol": "DM",

                                "riskAnalyzerComprehensiveRatingSymbolRelativity": "0.7109",

                                "riskAnalyzerComprehensiveRatingSymbol": "CE",

                                "riskAnalyzerComprehensiveNonGlassRatingSymbolRelativity": "0.7313",

                                "riskAnalyzerComprehensiveNonGlassRatingSymbol": "CF",

                                "riskAnalyzerCollisionIndicatedSymbolRelativityChar1": "0.85",

                                "riskAnalyzerComprehensiveIndicatedSymbolRelativityChar1": "0.8125",

                                "riskAnalyzerCollisionIndicatedSymbolRelativityChar2": "1.05",

                                "riskAnalyzerComprehensiveIndicatedSymbolRelativityChar2": "0.875",

                                "riskAnalyzerCollisionCappingIndicator": "N",

                                "riskAnalyzerComprehensiveCappingIndicator": "N",

                                "riskAnalyzerComprehensiveNonGlassCappingIndicator": "N",

                                "riskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar2": "0.9",

                                "riskAnalyzerComprehensiveNonGlassIndicatedSymbol": "CF",

                                "riskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativity": "0.7313"

                            },

                            "liability": {

                                "riskAnalyzerMedicalPaymentsIndicatedSymbol": "NR",

                                "riskAnalyzerPersonalInjuryProtectionIndicatedSymbol": "MM",

                                "riskAnalyzerSingleLimitIndicatedSymbol": "ML",

                                "riskAnalyzerBodilyInjuryIndicatedSymbolRelativity": "1.0763",

                                "riskAnalyzerPropertyDamageIndicatedSymbolRelativity": "1.05",

                                "riskAnalyzerMedicalPaymentsIndicatedSymbolRelativity": "1.2094",

                                "riskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativity": "1.1025",

                                "riskAnalyzerSingleLimitIndicatedSymbolRelativity": "1.0763",

                                "riskAnalyzerBodilyInjuryRatingSymbolRelativity": "1.0763",

                                "riskAnalyzerBodilyInjuryRatingSymbol": "ML",

                                "riskAnalyzerPropertyDamageRatingSymbolRelativity": "1.05",

                                "riskAnalyzerPropertyDamageRatingSymbol": "MK",

                                "riskAnalyzerMedicalPaymentsRatingSymbolRelativity": "1.2094",

                                "riskAnalyzerMedicalPaymentsRatingSymbol": "NR",

                                "riskAnalyzerPersonalInjuryProtectionRatingSymbolRelativity": "1.1025",

                                "riskAnalyzerPersonalInjuryProtectionRatingSymbol": "MM",

                                "riskAnalyzerSingleLimitRatingSymbolRelativity": "1.0763",

                                "riskAnalyzerSingleLimitRatingSymbol": "ML",

                                "riskAnalyzerBodilyInjuryCappingIndicator": "N",

                                "riskAnalyzerPropertyDamageCappingIndicator": "N",

                                "riskAnalyzerMedicalPaymentsCappingIndicator": "N",

                                "riskAnalyzerPersonalInjuryProtectionCappingIndicator": "N",

                                "riskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar1": "1.05",

                                "riskAnalyzerPropertyDamageIndicatedSymbolRelativityChar1": "1.05",

                                "riskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar1": "1.075",

                                "riskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar1": "1.05",

                                "riskAnalyzerSingleLimitIndicatedSymbolRelativityChar1": "1.05",

                                "riskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar2": "1.025",

                                "riskAnalyzerPropertyDamageIndicatedSymbolRelativityChar2": "1",

                                "riskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar2": "1.125",

                                "riskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar2": "1.05",

                                "riskAnalyzerSingleLimitIndicatedSymbolRelativityChar2": "1.025",

                                "riskAnalyzerBodilyInjuryIndicatedSymbol": "ML",

                                "riskAnalyzerPropertyDamageIndicatedSymbol": "MK",

                                "riskAnalyzerSingleLimitCappingIndicator": "N"

                            }

                        }

                    \]

                },

                {

                    "header": {

                        "quoteback": "e22fc1f7-b9bf-4c56-8e39-3bc0ccaf6e57",

                        "transactionId": "fc108b42-3fba-4a32-9db5-1582bb22ac95"

                    },

                    "body": \[

                        {

                            "requestedVin": "1GKER23788J291227",

                            "vehicle": {

                                "vin": "1GK\&R237&8",

                                "modelYear": "2008",

                                "distributionDate": "2212",

                                "restraint": "R",

                                "antiLockBrakes": "S",

                                "engineCylinders": "6",

                                "make": "GMC",

                                "basicModelName": "ACADIA",

                                "bodyStyle": "UTL4X24D",

                                "engineSize": "3.6",

                                "electronicStabilityControl": "S",

                                "tonnageIndicator": "13",

                                "payloadCapacity": "1678",

                                "fullModelName": "ACADIA SLT1",

                                "daytimeRunningLightIndicator": "S",

                                "wheelbase": "118.9",

                                "classCode": "93",

                                "antiTheftIndicator": "P",

                                "curbWeight": "4722",

                                "grossVehicleWeight": "6400",

                                "height": "69.9",

                                "horsepower": "275",

                                "ncicCode": "GMC",

                                "chassis": "U",

                                "length": "200.7",

                                "width": "78.2",

                                "baseMSRP": "34270",

                                "specialHandlingIndicator": "N",

                                "interimIndicator": "N",

                                "releaseDate": "2303"

                            },

                            "physicalDamage": {

                                "riskAnalyzerCollisionIndicatedSymbol": "DJ",

                                "riskAnalyzerComprehensiveIndicatedSymbol": "CM",

                                "riskAnalyzerCollisionIndicatedSymbolRelativity": "0.8288",

                                "riskAnalyzerComprehensiveIndicatedSymbolRelativity": "0.8531",

                                "riskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar1": "0.8125",

                                "riskAnalyzerCollisionRatingSymbolRelativity": "0.8288",

                                "riskAnalyzerCollisionRatingSymbol": "DJ",

                                "riskAnalyzerComprehensiveRatingSymbolRelativity": "0.8531",

                                "riskAnalyzerComprehensiveRatingSymbol": "CM",

                                "riskAnalyzerComprehensiveNonGlassRatingSymbolRelativity": "0.8734",

                                "riskAnalyzerComprehensiveNonGlassRatingSymbol": "CN",

                                "riskAnalyzerCollisionIndicatedSymbolRelativityChar1": "0.85",

                                "riskAnalyzerComprehensiveIndicatedSymbolRelativityChar1": "0.8125",

                                "riskAnalyzerCollisionIndicatedSymbolRelativityChar2": "0.975",

                                "riskAnalyzerComprehensiveIndicatedSymbolRelativityChar2": "1.05",

                                "riskAnalyzerCollisionCappingIndicator": "N",

                                "riskAnalyzerComprehensiveCappingIndicator": "N",

                                "riskAnalyzerComprehensiveNonGlassCappingIndicator": "N",

                                "riskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativityChar2": "1.075",

                                "riskAnalyzerComprehensiveNonGlassIndicatedSymbol": "CN",

                                "riskAnalyzerComprehensiveNonGlassIndicatedSymbolRelativity": "0.8734"

                            },

                            "liability": {

                                "riskAnalyzerMedicalPaymentsIndicatedSymbol": "GE",

                                "riskAnalyzerPersonalInjuryProtectionIndicatedSymbol": "FK",

                                "riskAnalyzerSingleLimitIndicatedSymbol": "KK",

                                "riskAnalyzerBodilyInjuryIndicatedSymbolRelativity": "1.025",

                                "riskAnalyzerPropertyDamageIndicatedSymbolRelativity": "1.025",

                                "riskAnalyzerMedicalPaymentsIndicatedSymbolRelativity": "0.8094",

                                "riskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativity": "0.9",

                                "riskAnalyzerSingleLimitIndicatedSymbolRelativity": "1",

                                "riskAnalyzerBodilyInjuryRatingSymbolRelativity": "1.025",

                                "riskAnalyzerBodilyInjuryRatingSymbol": "KL",

                                "riskAnalyzerPropertyDamageRatingSymbolRelativity": "1.025",

                                "riskAnalyzerPropertyDamageRatingSymbol": "LK",

                                "riskAnalyzerMedicalPaymentsRatingSymbolRelativity": "0.8094",

                                "riskAnalyzerMedicalPaymentsRatingSymbol": "GE",

                                "riskAnalyzerPersonalInjuryProtectionRatingSymbolRelativity": "0.9",

                                "riskAnalyzerPersonalInjuryProtectionRatingSymbol": "FK",

                                "riskAnalyzerSingleLimitRatingSymbolRelativity": "1",

                                "riskAnalyzerSingleLimitRatingSymbol": "KK",

                                "riskAnalyzerBodilyInjuryCappingIndicator": "N",

                                "riskAnalyzerPropertyDamageCappingIndicator": "N",

                                "riskAnalyzerMedicalPaymentsCappingIndicator": "N",

                                "riskAnalyzerPersonalInjuryProtectionCappingIndicator": "N",

                                "riskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar1": "1",

                                "riskAnalyzerPropertyDamageIndicatedSymbolRelativityChar1": "1.025",

                                "riskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar1": "0.925",

                                "riskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar1": "0.9",

                                "riskAnalyzerSingleLimitIndicatedSymbolRelativityChar1": "1",

                                "riskAnalyzerBodilyInjuryIndicatedSymbolRelativityChar2": "1.025",

                                "riskAnalyzerPropertyDamageIndicatedSymbolRelativityChar2": "1",

                                "riskAnalyzerMedicalPaymentsIndicatedSymbolRelativityChar2": "0.875",

                                "riskAnalyzerPersonalInjuryProtectionIndicatedSymbolRelativityChar2": "1",

                                "riskAnalyzerSingleLimitIndicatedSymbolRelativityChar2": "1",

                                "riskAnalyzerBodilyInjuryIndicatedSymbol": "KL",

                                "riskAnalyzerPropertyDamageIndicatedSymbol": "LK",

                                "riskAnalyzerSingleLimitCappingIndicator": "N"

                            }

                        }

                    \]

                }

            \]

        }

    }

}

 

**Failure Response**

{

    "transactionId": "01914e5b-245a-4da5-9cfd-33252359c660 ",

    "statusCode": 403,

    "errors": \[

        "Access Denied"

    \]

}