**Sample Request**

{

	"Header": {

		"Authorization": {

			"OrgId": "123456",

			"ShipId": "123456"

		},

		"Quoteback": "QuoteBack001"

	},

	"Body": {

		"Drivers": \[{

			"Sequence": "1",

			"GivenName": "REYNA",

			"Surname": "SUZUKI",

			"DOB": "19651111"

		},

		{

			"Sequence": "2",

			"GivenName": "ROBERT",

			"Surname": "SUZUKI",

			"SSN": "445673013",

			"DLNumber": "A453626348760",

			"DLState": "FL"

		},

		{

			"Sequence": "3",

			"GivenName": "MARK",

			"Surname": "DRURY",

			"SSN": "021500113"

		}\],

		"Addresses": \[{

			"AddressType": "Current",

			"Street1": "204 SW TERRY RD",

			"Street2": "TRLR 56",

			"City": "COUPEVILLE",

			"StateCode": "WA"

		},

		{

			"AddressType": "Mailing",

			"Street1": "8223 VINELAND AVE",

			"City": "ORLANDO",

			"StateCode": "FL",

			"Zip": "32821"

		}\],

		"VINS": \["1FDRE14W22HA18769",

		"3H1JC30674D307598",

		"KL1TD626X5B306244",

		"1G6KD52B2RU253323",

		"2FMDA5342XBC30752"\],

		"PhoneNumbers": \["4078260610"\]

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

    "Header": {

        "Quoteback": "QuoteBack001",

        "TransactionId": "32e7f169-9cab-46c7-84e6-1720413b1e4c"

    },

    "Body": {

        "ClaimActivityPredictor": {

            "CapIndicator": "Y",

            "NumberOfClaims": "2"

        },

        "Claims": \[{

            "ClaimReferenceNumber": "7QA00522761",

            "CarrierClaimNumber": "200822233411",

            "MatchReasons": \[{

                "Code": "V",

                "Description": "VIN Search Type"

            }\],

            "AtFaultIndicator": {

                "Code": "B",

                "Description": "Bodily Injury, Fault \>51%"

            },

            "CAAtFaultIndicators": \[{

                "Description": "Legal Cause \> 51%",

                "Value": "Y"

            }, {

                "Description": "Complied with CCR section 2632.13(c)(1-6)",

                "Value": "Y"

            }, {

                "Description": "Complied with CCR section 2632.13(d)",

                "Value": "Y"

            }, {

                "Description": "PD \> $1,000 or Bodily Injury / Death Occurred",

                "Value": "Y"

            }, {

                "Description": "Driver principally-at-fault for PD or BI",

                "Value": "Y"

            }\],

            "Insurer": {

                "CompanyId": "Z995",

                "OfficeId": "00000",

                "Name": "INSURANCE SERVICES OFFICE, INC",

                "AMBEST": "00001",

                "Address": {

                    "Street1": "545 WASHINGTON BLVD ",

                    "Street2": "",

                    "City": "JERSEY CITY",

                    "StateCode": "NJ",

                    "Zip": "07310",

                    "CountryCode": "US"

                },

                "Phone": "7323880332"

            },

            "Policy": {

                "PolicyNumber": "053369887",

                "PolicyType": {

                    "Code": "PAPP",

                    "Description": "Personal Auto"

                }

            },

            "MatchByInputDriverNumber": "0",

            "Subjects": \[{

                "IndvidualOrBusinessIndicator": "I",

                "GivenName": "JOHNATHAN",

                "Surname": "MACE",

                "DOB": "19510202",

                "Gender": "M",

                "DLNumber": "M2012078",

                "DLState": "CA",

                "SSNInformation": {

                    "SSN": "000007797",

                    "SSNValidation": {

                        "Code": "P",

                        "Description": "SSN was issued prior to DOB"

                    },

                    "IssuedFromYear": "1936",

                    "IssuedToYear": "1950",

                    "IssuedStateCode": "NE"

                },

                "RoleInClaim": {

                    "Code": "IN",

                    "Description": "Insured"

                },

                "Address": {

                    "Street1": "891 Palm Ln ",

                    "Street2": "",

                    "City": "Petaluma",

                    "StateCode": "CA",

                    "Zip": "94954",

                    "CountryCode": "US"

                },

                "SequenceInInputDrivers": "0",

                "SubjectAkas": \[\]

            }, {

                "IndvidualOrBusinessIndicator": "I",

                "GivenName": "JOHNATHAN",

                "Surname": "MACE",

                "DOB": "19510202",

                "Gender": "",

                "DLNumber": "M2012078",

                "DLState": "CA",

                "RoleInClaim": {

                    "Code": "SA",

                    "Description": "Insured Driver Same as Insured"

                },

                "Address": {

                    "Street1": "891 Palm Ln ",

                    "Street2": "",

                    "City": "Petaluma",

                    "StateCode": "CA",

                    "Zip": "94954",

                    "CountryCode": "US"

                },

                "SequenceInInputDrivers": "0",

                "SubjectAkas": \[\]

            }\],

            "LossInformation": {

                "LossDate": "20151005",

                "LossTime": "0000",

                "LossCode": "0000",

                "LossDescription": "",

                "Address": {

                    "Street1": "",

                    "Street2": "",

                    "City": "",

                    "StateCode": "",

                    "Zip": "",

                    "CountryCode": ""

                },

                "CatastropheNumber": "",

                "EmergencyAgency": "",

                "PoliceReportNumber": "",

                "Losses": \[{

                    "CoverageType": {

                        "Code": "COLL",

                        "Description": "Collision"

                    },

                    "LossType": {

                        "Code": "COLL",

                        "Description": "Collision"

                    },

                    "DispositionStatus": {

                        "Code": "C",

                        "Description": "Closed"

                    },

                    "Amount": "1500",

                    "ClaimStandardizationCode": "B18APA332060U000"

                }\]

            },

            "ClaimStandardizationCode": "B18APA332060U000",

            "Vehicles": \[{

                "Make": "CADILLAC",

                "Model": "DEVILLE",

                "Year": "1994",

                "VIN": "1G6KD52B2RU253323",

                "VINValidation": {

                    "Code": "P",

                    "Description": "Pass"

                },

                "VehicleColor": "",

                "OdometerReading": "",

                "LicensePlateNumber": "",

                "LicensePlateStateCode": "",

                "LastRegisteredYear": "",

                "SuitIndicator": {},

                "Catastrophes": \[\]

            }\]

        }, {

            "ClaimReferenceNumber": "0QA00524244",

            "CarrierClaimNumber": "ALST1008",

            "MatchReasons": \[{

                "Code": "P",

                "Description": "Phone Number Search"

            }, {

                "Code": "S",

                "Description": "SSN Search Type"

            }, {

                "Code": "D",

                "Description": "Driver License and State Search Type"

            }, {

                "Code": "A",

                "Description": "Name and Address Search Type"

            }, {

                "Code": "N",

                "Description": "Name and Date of Birth Search Type"

            }\],

            "AtFaultIndicator": {

                "Code": "Y",

                "Description": "Insured at Fault"

            },

            "CAAtFaultIndicators": \[\],

            "Insurer": {

                "CompanyId": "Z995",

                "OfficeId": "00000",

                "Name": "INSURANCE SERVICES OFFICE, INC",

                "AMBEST": "00001",

                "Address": {

                    "Street1": "545 WASHINGTON BLVD ",

                    "Street2": "",

                    "City": "JERSEY CITY",

                    "StateCode": "NJ",

                    "Zip": "07310",

                    "CountryCode": "US"

                },

                "Phone": "7323880332"

            },

            "Policy": {

                "PolicyNumber": "ALLST1001",

                "PolicyType": {

                    "Code": "PAPP",

                    "Description": "Personal Auto"

                },

                "OriginalInceptionDate": "20130814",

                "ExpirationDate": "20140815",

                "PolicyRenewal": {

                    "Code": "Y",

                    "Description": "Renewal"

                },

                "DriverAssignedRisk": {

                    "Code": "Y",

                    "Description": "Yes assigned risk policy"

                }

            },

            "DriverRelationToPolicyHolder": {

                "Code": "SP",

                "Description": "Spouse"

            },

            "MatchByInputDriverNumber": "2",

            "DisputeStatement": "The consumer is disputing that the claim should not be reported         due to the accident not being his fault",

            "Subjects": \[{

                "IndvidualOrBusinessIndicator": "I",

                "GivenName": "ROBERT",

                "Surname": "SUZUKI",

                "MiddleName": "Y",

                "DOB": "19980101",

                "Gender": "M",

                "DLNumber": "A453626348760",

                "DLState": "FL",

                "SSNInformation": {

                    "SSN": "000000113",

                    "SSNValidation": {

                        "Code": "D",

                        "Description": "Death Master indicates SSN Number was Assigned to an Individual that has been reported as being Deceased"

                    },

                    "IssuedFromYear": "1973",

                    "IssuedToYear": "1974",

                    "IssuedStateCode": "MA",

                    "DeathMaster": {

                        "GivenName": "MARK",

                        "Surname": "DRURY",

                        "NameIndicator": "N",

                        "DateOfDeath": "20011226",

                        "City": "PITTSFIELD",

                        "StateCode": "MA"

                    }

                },

                "RoleInClaim": {

                    "Code": "IN",

                    "Description": "Insured with 2 Aliases"

                },

                "Address": {

                    "Street1": "8223 VINELAND AVE ",

                    "Street2": "A208",

                    "City": "ORLANDO",

                    "StateCode": "FL",

                    "Zip": "32821",

                    "CountryCode": "US"

                },

                "SequenceInInputDrivers": "2",

                "PhoneNumbers": \[{

                    "PhoneType": "H",

                    "Number": "3055071048"

                }\],

                "SubjectAkas": \[{

                    "IndvidualOrBusinessIndicator": "I",

                    "GivenName": "ROB",

                    "Surname": "SUZUKI",

                    "MiddleName": "Y",

                    "Gender": ""

                }, {

                    "IndvidualOrBusinessIndicator": "I",

                    "GivenName": "ROBBY",

                    "Surname": "SUZUKI",

                    "MiddleName": "Y",

                    "Gender": ""

                }\]

            }, {

                "IndvidualOrBusinessIndicator": "I",

                "GivenName": "REYNA",

                "Surname": "SUZUKI",

                "MiddleName": "R",

                "DOB": "19651111",

                "Gender": "F",

                "DLNumber": "A453626348767",

                "DLState": "FL",

                "RoleInClaim": {

                    "Code": "SI",

                    "Description": "Second Insured"

                },

                "Address": {

                    "Street1": "8223 VINELAND AVE ",

                    "Street2": "A208",

                    "City": "ORLANDO",

                    "StateCode": "FL",

                    "Zip": "32821",

                    "CountryCode": "US"

                },

                "SequenceInInputDrivers": "1",

                "PhoneNumbers": \[{

                    "PhoneType": "H",

                    "Number": "4078260643"

                }\],

                "SubjectAkas": \[\]

            }, {

                "IndvidualOrBusinessIndicator": "I",

                "GivenName": "REYNA",

                "Surname": "SUZUKI",

                "MiddleName": "R",

                "DOB": "19681020",

                "Gender": "F",

                "DLNumber": "A453626348767",

                "DLState": "FL",

                "RoleInClaim": {

                    "Code": "ID",

                    "Description": "Insured Driver"

                },

                "Address": {

                    "Street1": "8223 VINELAND AVE ",

                    "Street2": "A208",

                    "City": "ORLANDO",

                    "StateCode": "FL",

                    "Zip": "32821",

                    "CountryCode": "US"

                },

                "SequenceInInputDrivers": "1",

                "PhoneNumbers": \[{

                    "PhoneType": "H",

                    "Number": "4078260643"

                }\],

                "SubjectAkas": \[\]

            }, {

                "IndvidualOrBusinessIndicator": "I",

                "GivenName": "STEPHAN",

                "Surname": "AKITA",

                "MiddleName": "S",

                "Gender": "",

                "RoleInClaim": {

                    "Code": "CL",

                    "Description": "Claimant"

                },

                "Address": {

                    "Street1": ""

                },

                "Occupation": "",

                "SequenceInInputDrivers": "0",

                "SubjectAkas": \[\]

            }, {

                "IndvidualOrBusinessIndicator": "I",

                "GivenName": "STEPHAN",

                "Surname": "AKITA",

                "MiddleName": "S",

                "Gender": "",

                "RoleInClaim": {

                    "Code": "CD",

                    "Description": "Claimant Driver"

                },

                "Address": {

                    "Street1": ""

                },

                "Occupation": "",

                "SequenceInInputDrivers": "0",

                "SubjectAkas": \[\]

            }\],

            "LossInformation": {

                "LossDate": "20140228",

                "LossTime": "0830",

                "LossCode": "0000",

                "LossDescription": "TOTALED",

                "Address": {

                    "Street1": "9814 INTERNATIONAL DR ",

                    "Street2": "B23",

                    "City": "ORLANDO",

                    "StateCode": "FL",

                    "Zip": "32819",

                    "CountryCode": "USA"

                },

                "DueToCatastrophe": {

                    "Code": "Y",

                    "Description": "Catastrophe related"

                },

                "CatastropheNumber": "355",

                "EmergencyAgency": "POLICE",

                "PoliceReportNumber": "I89898912",

                "OriginalSubmittalDate": "20140212",

                "Losses": \[{

                    "CoverageType": {

                        "Code": "COLL",

                        "Description": "Collision"

                    },

                    "LossType": {

                        "Code": "COLL",

                        "Description": "Collision"

                    },

                    "DispositionStatus": {

                        "Code": "O",

                        "Description": "Open"

                    },

                    "Amount": "1700",

                    "ClaimStandardizationCode": "Y18APA151079Y199"

                }, {

                    "CoverageType": {

                        "Code": "COMP",

                        "Description": "Comprehensive"

                    },

                    "LossType": {

                        "Code": "V\&MM",

                        "Description": "Vandalism & Mysterious Mischief"

                    },

                    "DispositionStatus": {

                        "Code": "O",

                        "Description": "Open"

                    },

                    "Amount": "1700",

                    "ClaimStandardizationCode": "Y19BPA151070Y000"

                }, {

                    "CoverageType": {

                        "Code": "GGKP",

                        "Description": "Garagekeepers"

                    },

                    "LossType": {

                        "Code": "COLL",

                        "Description": "Collision"

                    },

                    "DispositionStatus": {

                        "Code": "O",

                        "Description": "Open"

                    },

                    "Amount": "1700",

                    "ClaimStandardizationCode": "Y18DPA151070Y000"

                }, {

                    "CoverageType": {

                        "Code": "LIAB",

                        "Description": "Liability"

                    },

                    "LossType": {

                        "Code": "BI",

                        "Description": "Body injury"

                    },

                    "DispositionStatus": {

                        "Code": "O",

                        "Description": "Open"

                    },

                    "Amount": "1700",

                    "ClaimStandardizationCode": "Y02EPA151079Y199"

                }\]

            },

            "ClaimStandardizationCode": "Y99MPA951090Y000",

            "Vehicles": \[{

                "Make": "TOYOTASE",

                "Model": "RAV4",

                "Year": "2008",

                "VIN": "JF4SG63628M108614",

                "VINValidation": {

                    "Code": "F",

                    "Description": "Fail"

                },

                "VehicleType": {

                    "Code": "LT",

                    "Description": "Light Duty Truck"

                },

                "VehicleStyle": {

                    "Code": "AC",

                    "Description": "Auto Carrier"

                },

                "VehicleColor": "BLK",

                "TheftType": {

                    "Code": "P",

                    "Description": "Partial Theft"

                },

                "OdometerReading": "8909890",

                "LicensePlateType": {

                    "Code": "DX",

                    "Description": "Disabled Person"

                },

                "LicensePlateNumber": "XPE5321",

                "LicensePlateStateCode": "FL",

                "LastRegisteredYear": "2012",

                "AntiTheftDeviceType": {

                    "Code": "03",

                    "Description": "Passive Disabling Device"

                },

                "PointOfImpact": {

                    "Code": "11",

                    "Description": "Left Front Corner"

                },

                "DriverAirbagStatus": {

                    "Code": "D",

                    "Description": "Deployed"

                },

                "PassengerAirbagStatus": {

                    "Code": "D",

                    "Description": "Deployed"

                },

                "LeftAirbagStatus": {

                    "Code": "D",

                    "Description": "Deployed"

                },

                "RightAirbagStatus": {

                    "Code": "D",

                    "Description": "Deployed"

                },

                "SuitIndicator": {},

                "LossDegree": {

                    "Code": "T",

                    "Description": "Totaled"

                },

                "Catastrophes": \[\]

            }, {

                "Make": "FORD",

                "Model": "F150 SERIES",

                "Year": "1997",

                "VIN": "1FTDF18W4VNB75411",

                "VINValidation": {

                    "Code": "P",

                    "Description": "Pass"

                },

                "VehicleType": {

                    "Code": "LT",

                    "Description": "Light Duty Truck"

                },

                "VehicleStyle": {

                    "Code": "AC",

                    "Description": "Auto Carrier"

                },

                "VehicleColor": "BLK",

                "TheftType": {

                    "Code": "P",

                    "Description": "Partial Theft"

                },

                "OdometerReading": "",

                "LicensePlateType": {

                    "Code": "DX",

                    "Description": "Disabled Person"

                },

                "LicensePlateNumber": "XPE5321",

                "LicensePlateStateCode": "FL",

                "LastRegisteredYear": "2012",

                "AntiTheftDeviceType": {

                    "Code": "03",

                    "Description": "Passive Disabling Device"

                },

                "PointOfImpact": {

                    "Code": "11",

                    "Description": "Left Front Corner"

                },

                "DriverAirbagStatus": {

                    "Code": "D",

                    "Description": "Deployed"

                },

                "PassengerAirbagStatus": {

                    "Code": "D",

                    "Description": "Deployed"

                },

                "LeftAirbagStatus": {

                    "Code": "D",

                    "Description": "Deployed"

                },

                "RightAirbagStatus": {

                    "Code": "D",

                    "Description": "Deployed"

                },

                "SuitIndicator": {},

                "LossDegree": {

                    "Code": "T",

                    "Description": "Totaled"

                },

                "Catastrophes": \[{

                    "Name": "FLOOD",

                    "CatastropheDate": "20041025",

                    "CompanyProvider": "ISO/MISSISSIPPI MOTOR VEHICLE LICENSING BUREAU",

                    "DmvAssignments": \[{

                        "Code": "F",

                        "Description": "Flood Title"

                    }\],

                    "LicensePlateType": "",

                    "OwnerZip": "",

                    "TitleStateCode": "",

                    "CustomerId": "M795"

                }\]

            }\]

        }\],

        "Vehicles": \[{

            "Make": "FORD",

            "Model": "EC1",

            "Year": "2002",

            "VIN": "1FDRE14W22HA18769",

            "VINValidation": {

                "Code": "P",

                "Description": "Pass"

            },

            "Catastrophes": \[\],

            "Salvages": \[{

                "IsVINMissing": " ",

                "IsEngineMissing": " ",

                "IsTransmissionMissing": " ",

                "SalvageDate": "20161001",

                "ActualAmount": "      ",

                "ReceivedAmount": "      ",

                "AppraisedAmount": "      ",

                "IsSalvageWithOwner": " ",

                "CauseOfLoss": {

                    "Code": " "

                },

                "CashForClunkers": {

                    "OccurrenceDate": "20161010",

                    "PurchaseDescription": "CASH FOR CLUNKERS"

                }

            }, {

                "IsVINMissing": " ",

                "IsEngineMissing": " ",

                "IsTransmissionMissing": " ",

                "SalvageDate": "20161001",

                "ActualAmount": "      ",

                "ReceivedAmount": "      ",

                "AppraisedAmount": "      ",

                "IsSalvageWithOwner": " ",

                "CauseOfLoss": {

                    "Code": " "

                },

                "CashForClunkers": {

                    "OccurrenceDate": "20161010",

                    "PurchaseDescription": "CASH FOR CLUNKERS"

                }

            }\],

            "EventDataRecorderAvailable": "N",

            "EstimateInformation": {

                "EstimateAvailable": "N",

                "ActivityDate": "",

                "LossDate": "",

                "Mileage": "0"

            },

            "NoticesOfRecall": \[\],

            "VINDecoding": \[{

                "VINCharacter": "1",

                "Description": "Country of Origin",

                "Value": "UNITED STATES OF AMERICA"

            }, {

                "VINCharacter": "F",

                "Description": "Manufacturer",

                "Value": "FORD   FORD",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "D",

                "Description": "Vehicle Type",

                "Value": "INCOMPLETE VEHICLE",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "R",

                "Description": "Gross Vehicle Weight",

                "Value": "6,001-7,000 GVWR W/SEC.GEN.AIR BAGS",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "E14",

                "Description": "Series",

                "Value": "ECONOLINE E150 4X2 VAN",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "W",

                "Description": "Engine",

                "Value": "4.6L EFI-SOHC V8",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "2",

                "Description": "Check Digit",

                "Value": "Check Digit Matches"

            }, {

                "VINCharacter": "2",

                "Description": "Year",

                "Value": "2002"

            }, {

                "VINCharacter": "H",

                "Description": "Plant",

                "Value": "LORAIN, OH",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "A18769",

                "Description": "Serial Number",

                "Value": "Sequence in Range"

            }\]

        }, {

            "Make": "HOND",

            "Model": "",

            "Year": "2004",

            "VIN": "3H1JC30674D307598",

            "VINValidation": {

                "Code": "F",

                "Description": "Fail"

            },

            "Catastrophes": \[\],

            "Salvages": \[\],

            "OCRA": {

                "OccurrenceDate": "",

                "FileNumber": "L0435600027"

            },

            "EventDataRecorderAvailable": "",

            "EstimateInformation": {

                "EstimateAvailable": "N",

                "ActivityDate": "",

                "LossDate": "",

                "Mileage": "0"

            },

            "NoticesOfRecall": \[\],

            "VINDecoding": \[{

                "VINCharacter": "3",

                "Description": "Country of Origin",

                "Value": "MEXICO"

            }, {

                "VINCharacter": "H",

                "Description": "Manufacturer",

                "Value": "HOND   HONDA"

            }, {

                "VINCharacter": "1",

                "Description": "Vehicle Type",

                "Value": "MOTORCYCLE"

            }, {

                "VINCharacter": "JC306",

                "Description": "Model",

                "Value": "Invalid Digit",

                "InvalidDigitIndicator": "\*"

            }, {

                "VINCharacter": "7",

                "Description": "Check Digit",

                "Value": "Check Digit Matches"

            }, {

                "VINCharacter": "4",

                "Description": "Year",

                "Value": "2004"

            }, {

                "VINCharacter": "D",

                "Description": "Plant",

                "Value": "MEXICO",

                "InvalidDigitIndicator": "\*"

            }, {

                "VINCharacter": "307598",

                "Description": "Serial Number",

                "Value": "Out of Range",

                "InvalidDigitIndicator": "\*"

            }\]

        }, {

            "Make": "CHEV",

            "Model": "AVO",

            "Year": "2005",

            "VIN": "KL1TD626X5B306244",

            "VINValidation": {

                "Code": "P",

                "Description": "Pass"

            },

            "Catastrophes": \[\],

            "Salvages": \[\],

            "EventDataRecorderAvailable": "N",

            "EstimateInformation": {

                "EstimateAvailable": "N",

                "ActivityDate": "",

                "LossDate": "",

                "Mileage": "0"

            },

            "NoticesOfRecall": \[\],

            "VINDecoding": \[{

                "VINCharacter": "K",

                "Description": "Country of Origin",

                "Value": "KOREA;ISRAEL"

            }, {

                "VINCharacter": "L",

                "Description": "Manufacturer",

                "Value": "CHEV   GENERAL MOTORS/GMDAT",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "1",

                "Description": "Division",

                "Value": "CHEVROLET",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "TD",

                "Description": "Line",

                "Value": "AVEO BASE/LS",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "6",

                "Description": "Body Style",

                "Value": "4 DR SEDAN/4DR LIFT GATE",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "2",

                "Description": "Restraint System",

                "Value": "MANUAL/W DR./ PASS.INFLATABLE(FRNT)",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "6",

                "Description": "Engine",

                "Value": "1.6L L4 DOHC",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "X",

                "Description": "Check Digit",

                "Value": "Check Digit Matches"

            }, {

                "VINCharacter": "5",

                "Description": "Year",

                "Value": "2005"

            }, {

                "VINCharacter": "B",

                "Description": "Plant",

                "Value": "BUPYEONG, SOUTH KOREA",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "306244",

                "Description": "Serial Number",

                "Value": "Sequence in Range"

            }\]

        }, {

            "Make": "CADI",

            "Model": "DEV",

            "Year": "1994",

            "VIN": "1G6KD52B2RU253323",

            "VINValidation": {

                "Code": "P",

                "Description": "Pass"

            },

            "Catastrophes": \[\],

            "Salvages": \[\],

            "EventDataRecorderAvailable": "N",

            "EstimateInformation": {

                "EstimateAvailable": "Y",

                "ActivityDate": "19940403",

                "LossDate": "19940501",

                "Mileage": "63265"

            },

            "NoticesOfRecall": \[\],

            "VINDecoding": \[{

                "VINCharacter": "1",

                "Description": "Country of Origin",

                "Value": "UNITED STATES OF AMERICA"

            }, {

                "VINCharacter": "G",

                "Description": "Manufacturer",

                "Value": "CADI   GENERAL MOTORS",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "6",

                "Description": "Division",

                "Value": "CADILLAC",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "KD",

                "Description": "Line",

                "Value": "DEVILLE",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "5",

                "Description": "Body Style",

                "Value": "4 DR SEDAN",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "2",

                "Description": "Restraint System",

                "Value": "MANUAL W/DRIVER / PASS. AIR BAGS",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "B",

                "Description": "Engine",

                "Value": "4.9L V8 MFI",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "2",

                "Description": "Check Digit",

                "Value": "Check Digit Matches"

            }, {

                "VINCharacter": "R",

                "Description": "Year",

                "Value": "1994"

            }, {

                "VINCharacter": "U",

                "Description": "Plant",

                "Value": "HAMTRAMCK, MI",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "253323",

                "Description": "Serial Number",

                "Value": "Sequence in Range"

            }\]

        }, {

            "Make": "FORD",

            "Model": "WIN",

            "Year": "1999",

            "VIN": "2FMDA5342XBC30752",

            "VINValidation": {

                "Code": "P",

                "Description": "Pass"

            },

            "Catastrophes": \[\],

            "Salvages": \[{

                "IsVINMissing": " ",

                "IsEngineMissing": " ",

                "IsTransmissionMissing": " ",

                "SalvageDate": "20161001",

                "ActualAmount": "      ",

                "ReceivedAmount": "      ",

                "AppraisedAmount": "      ",

                "IsSalvageWithOwner": " ",

                "CauseOfLoss": {

                    "Code": " "

                },

                "CashForClunkers": {

                    "OccurrenceDate": "20090715",

                    "PurchaseDescription": "CASH FOR CLUNKERS"

                }

            }\],

            "EventDataRecorderAvailable": "N",

            "EstimateInformation": {

                "EstimateAvailable": "N",

                "ActivityDate": "",

                "LossDate": "",

                "Mileage": "0"

            },

            "NoticesOfRecall": \[{

                "RecallId": "01V261000",

                "ComponentInfo": "VISIBILITY:WINDSHIELD WIPER/WASHER:MOTOR",

                "RecallSummary": "VEHICLE DESCRIPTION:  MINI VANS.    CONTAMINANTS SUCH AS WATER, SALT, AND WINDSHIELD WASHER SOLUTION CAN ENTER THE WIPER MOTOR COVER ASSEMBLY THROUGH PINHOLES ON THE EXTERIOR OF THE COVER THAT ARE USED IN THE MOLDING PROCESS.  IN ADDITION, ON CERTAIN OF THE VEHICLES BUILT BETWEEN FEBRUARY AND AUGUST",

                "RecallDate": "20010815",

                "NumberOfUnitsRecalled": "598256",

                "ManufactureRecallInfo": "FORD MOTOR COMPANY",

                "RecallConsequences": "SWITCH MALFUNCTION IS MOST LIKELY TO OCCUR WHEN THE INTERMITTENT SETTING OF THE WIPERS IS BEING USED, OR WHEN SNOW OR ICE OBSTRUCTS THE BLADES FROM RETURNING TO THE \\"PARKED\\" POSITION AT THE BOTTOM OF THE WINDSHIELD.  LOSS OF VISIBILITY WHILE DRIVING INCREASES THE RISK OF A CRASH."

            }, {

                "RecallId": "01V262000",

                "ComponentInfo": "EQUIPMENT:ELECTRICAL:AIR CONDITIONER",

                "RecallSummary": "VEHICLE DESCRIPTION:  MINI VANS EQUIPPED WITH AUXILIARY REAR AIR-CONDITIONING.  IF THE AUXILIARY AIR-CONDITIONING BLOWER MOTOR STOPS TURNING WHILE IN THE MEDIUM-LOW BLOWER SPEED SETTING, THERE IS THE POTENTIAL THAT THE RESISTOR MAY BECOME HOT AND SMOKE.",

                "RecallDate": "20010815",

                "NumberOfUnitsRecalled": "413245",

                "ManufactureRecallInfo": "FORD MOTOR COMPANY",

                "RecallConsequences": "THE MOTOR COULD POTENTIALLY CATCH ON FIRE."

            }, {

                "RecallId": "00V351000",

                "ComponentInfo": "ELECTRICAL SYSTEM:WIRING:INTERIOR/UNDER DASH",

                "RecallSummary": "VEHICLE DESCRIPTION:  MINIVANS BUILT WITH INSTRUMENT CLUSTERS WITHOUT THE MESSAGE CENTER,  FAIL TO COMPLY WITH THE REQUIREMENTS OF STANDARD NO. 118, \\"POWER-OPERATED WINDOW, PARTITION, AND ROOF PANEL SYSTEMS.\\"    THE POWER WINDOWS MAY BE OPERABLE AFTER THE IGNITION HAS BEEN TURNED TO THE \\"OFF\\" POSITI",

                "RecallDate": "20001030",

                "NumberOfUnitsRecalled": "180000",

                "ManufactureRecallInfo": "FORD MOTOR COMPANY",

                "RecallConsequences": "THE STANDARD REQUIRES THAT POWER OPERATED WINDOWS MAY BE CLOSED ONLY WHEN THE KEY IS IN THE \\"ON,\\" \\"START,\\" OR \\"ACCESSORY\\" POSITIONS, OR DURING THE INTERVAL BETWEEN THE TIME THE KEY IS TURNED OFF, AND THE OPENING OF EITHER OF THE VEHICLE'S FRONT DOORS."

            }, {

                "RecallId": "99V147000",

                "ComponentInfo": "SERVICE BRAKES, HYDRAULIC:FOUNDATION COMPONENTS:MASTER CYLINDER",

                "RecallSummary": "VEHICLE DESCRIPTION:  MINIVANS.  THE BRAKE FLUID MASTER CYLINDER IS RECESSED AND ORIENTED IN THE ENGINE COMPARTMENT SO THAT THE BRAKE FLUID WARNING STATEMENT EMBOSSED ON BOTH THE TOP OF THE FILLER CAP AND THE SIDE OF THE RESERVOIR BODY ARE NOT ENTIRELY VISIBLE BY DIRECT VIEW.  THESE VEHICLES MAY NOT",

                "RecallDate": "19990614",

                "NumberOfUnitsRecalled": "789723",

                "ManufactureRecallInfo": "FORD MOTOR COMPANY",

                "RecallConsequences": ""

            }\],

            "VINDecoding": \[{

                "VINCharacter": "2",

                "Description": "Country of Origin",

                "Value": "CANADA"

            }, {

                "VINCharacter": "F",

                "Description": "Manufacturer",

                "Value": "FORD   FORD",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "M",

                "Description": "Vehicle Type",

                "Value": "MULTI PURPOSE VEHICLE",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "D",

                "Description": "Gross Vehicle Weight",

                "Value": "5,001-6,000 GVWR HYDRAULIC BRAKES",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "A53",

                "Description": "Series",

                "Value": "WINDSTAR SEL 4DR WAGON",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "4",

                "Description": "Engine",

                "Value": "3.8L EFI-SPI V6",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "2",

                "Description": "Check Digit",

                "Value": "Check Digit Matches"

            }, {

                "VINCharacter": "X",

                "Description": "Year",

                "Value": "1999"

            }, {

                "VINCharacter": "B",

                "Description": "Plant",

                "Value": "OAKVILLE, ON (CANADA)",

                "InvalidDigitIndicator": ""

            }, {

                "VINCharacter": "C30752",

                "Description": "Serial Number",

                "Value": "Sequence in Range"

            }\]

        }\],

        "SSNInformations": \[{

            "SSN": "000003013",

            "SSNValidation": {

                "Code": "V",

                "Description": "SSN has been Verified and Issued"

            },

            "IssuedFromYear": "2011",

            "IssuedToYear": "0000",

            "IssuedStateCode": "UU"

        }\],

        "CustomElements": \[\]

    }

}

**Failure Response**

{

    "transactionId": "8c5e728f-6c6e-4e50-987b-12c06432103e",

    "statusCode": 403,

    "errors": \[

        "Access Denied"

    \]

}