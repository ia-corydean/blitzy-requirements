**Request body, Example Value Schema**

{

  "Header": {

    "Authorization": {

      "OrgId": "111111",

      "ShipId": "111111"

    },

    "QuoteBack": "QB123456"

  },

  "Body": {

    "Drivers": \[

      {

        "Sequence": 1,

        "GivenName": "JosephineALONE",

        "Surname": "MillerALONE"

      }

    \],

    "Addresses": \[

      {

        "AddressType": "Current",

        "Street1": "8115 W Oatman Rd",

        "City": "Tuscaloosa",

        "StateCode": "AL",

        "Zip": "35401"

      }

    \]

  }

}

**Response Success, Example Value Schema**

* **Success: Upon successful call, the service will return a 200 response along with the data requested. No hits will return an empty body with http status 200\.**

{

  "body": {

    "policies": \[

      {

        "detail": {

          "policyInformation": {

            "policyType": {

              "code": "AU",

              "description": "Auto"

            },

            "termEffectiveDate": "20190111",

            "termExpirationDate": "20200111",

            "premiumInformation": null,

            "policyHolders": \[

              {

                "givenName": "JOSEPHINEALONE",

                "middleName": "A",

                "surname": "MILLERALONE",

                "nameSuffix": null,

                "dob": "19411224",

                "dlNumber": "9758318",

                "dlState": "AL"

              }

            \],

            "phoneNumbers": null,

            "fromDate": null,

            "toDate": null

          },

          "subjects": \[

            {

              "driverSequenceId": "1",

              "givenName": "JOSEPHINEALONE",

              "middleName": "A",

              "surname": "MILLERALONE",

              "nameSuffix": null,

              "dob": "19411224",

              "ssn": null,

              "gender": "F",

              "maritalStatus": "S",

              "dlNumber": "9758318",

              "dlState": "AL",

              "relationToPolicyHolder": {

                "code": "PP",

                "description": "Primary Policyholder"

              },

              "relationToInsured": {

                "code": "I",

                "description": "Insured"

              },

              "fromDate": "20190111",

              "toDate": "20200111"

            }

          \],

          "carrier": {

            "financialAMBEST": "99999",

            "name": "INSURANCE SERVICES O",

            "ambest": "99999",

            "naic": "00000"

          },

          "mailingAddress": {

            "fromDate": "20190111",

            "toDate": "20200111",

            "street1": "W 8115 Oatman Rd",

            "street2": null,

            "city": "Tuscaloosa",

            "stateCode": "AL",

            "zip": "35401",

            "countryCode": "US"

          },

          "coverages": \[

            {

              "coverageType": {

                "code": "BINJ",

                "description": "Bodily Injury"

              },

              "individualLimitAmount": "10000",

              "occurrenceLimitAmount": "25000",

              "combinedSingleLimitAmount": "0",

              "fromDate": "20190111",

              "toDate": "20200111"

            },

            {

              "coverageType": {

                "code": "PINJ",

                "description": "Personal Injury"

              },

              "individualLimitAmount": "25000",

              "occurrenceLimitAmount": "50000",

              "combinedSingleLimitAmount": "0",

              "fromDate": "20190111",

              "toDate": "20200111"

            }

          \],

          "vehicles": \[

            {

              "year": "1987",

              "make": "ACURA",

              "model": "LEGEND",

              "vin": "I0ZYX89TMON984281",

              "vehicleTypeCode": null,

              "classCode": "000000",

              "businessUse": null,

              "territoryCode": null,

              "collisionDeductibleAmount": "1000",

              "comprehensiveDeductibleAmount": "500",

              "fromDate": "20190111",

              "toDate": "20200111",

              "collisionIndicator": "N",

              "collisionIndividualLimitAmount": null,

              "collisionOccurenceLimitAmount": null,

              "comprehensiveIndicator": "N",

              "comprehensiveIndividualLimitAmount": null,

              "comprehensiveOccurenceLimitAmount": null,

              "coverages": \[

                {

                  "coverageType": {

                    "code": "BINJ",

                    "description": "Bodily Injury"

                  },

                  "individualLimitAmount": "10000",

                  "occurrenceLimitAmount": "25000",

                  "combinedSingleLimitAmount": "0",

                  "fromDate": "20190111",

                  "toDate": "20200111"

                },

                {

                  "coverageType": {

                    "code": "PINJ",

                    "description": "Personal Injury"

                  },

                  "individualLimitAmount": "25000",

                  "occurrenceLimitAmount": "50000",

                  "combinedSingleLimitAmount": "0",

                  "fromDate": "20190111",

                  "toDate": "20200111"

                }

              \]

            }

          \],

          "garageLocations": null,

          "financeInformations": null

        },

        "history": {

          "policyInformations": null,

          "subjects": null,

          "mailingAddresses": null,

          "coverages": null,

          "vehicles": null,

          "garageLocations": null,

          "financeInformations": null,

          "transactionInformations": null

        },

        "policyNumber": "ALVRSK2017112001",

        "policyStatus": "EXPIRED",

        "policyReportedDate": "20180226",

        "inceptionDate": "20190111",

        "lastReportedTermEffectiveDate": "20190111",

        "lastReportedTermExpirationDate": "20200111",

        "numberOfCancellations": "0",

        "numberOfRenewals": "0",

        "numberOfEndorsements": "0",

        "cancellationDate": null,

        "disputeStatement": null,

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

            "startDate": "20190111",

            "endDate": "20200111",

            "numberOfCoverageDays": "365",

            "hasBreakFromPriorCoverage": "NA",

            "numberOfLapseDays": "0"

          }

        \],

        "givenName": "JosephineALONE",

        "middleName": null,

        "surname": "MillerALONE",

        "nameSuffix": null,

        "inputDriverSequenceNumber": "1",

        "hasPossibleLapse": "N",

        "isCurrentInforceCoverage": "N"

      }

    \],

    "analyticObjects": \[

      {

        "givenName": "JosephineALONE",

        "middleName": null,

        "surname": "MillerALONE",

        "inputDriverSequenceNumber": "1",

        "changeAttributes": \[

          {

            "code": "346",

            "description": "Last pol coverage gap",

            "count": "1720",

            "flag": null,

            "lastReportedDate": "20190111"

          },

          {

            "code": "300",

            "description": "Current active policy count",

            "count": "0",

            "flag": null,

            "lastReportedDate": null

          },

          {

            "code": "126",

            "description": "Vehicles exceed drivers beg",

            "count": null,

            "flag": "0",

            "lastReportedDate": "20190111"

          },

          {

            "code": "127",

            "description": "Drivers exceed vehicles beg",

            "count": null,

            "flag": "0",

            "lastReportedDate": "20190111"

          }

        \],

        "scores": \[

          {

            "name": "ScoreName1",

            "value": "100"

          },

          {

            "name": "ScoreName2",

            "value": "100"

          },

          {

            "name": "ScoreName3",

            "value": "100"

          }

        \]

      }

    \],

    "customElements": null

  },

  "header": {

    "transactionId": "a64bd4f7-7e51-4d20-81ec-8a08c78ed4b7",

    "quoteback": "QB123456"

  }

}

