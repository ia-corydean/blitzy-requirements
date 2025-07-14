**Request body, Example Value Schema**

\<Request\>

    \<Header\>

        \<Authorization\>

            \<OrgId\>111111\</OrgId\>

            \<ShipId\>111111\</ShipId\>

        \</Authorization\>

        \<Quoteback\>QB123456\</Quoteback\>

        \<RequestOptions\>

            \<RequestOption\>

                \<Key\>\</Key\>

                \<Value\>\</Value\>

            \</RequestOption\>

        \</RequestOptions\>

    \</Header\>

    \<Body\>

        \<Drivers\>

            \<Driver\>

                \<Sequence\>1\</Sequence\>

                \<GivenName\>JosephineALONE\</GivenName\>

                \<Surname\>MillerALONE\</Surname\>

            \</Driver\>

        \</Drivers\>

        \<Addresses\>

            \<Address\>

                \<AddressType\>Current\</AddressType\>

                \<Street1\>8115 W Oatman Rd\</Street1\>

                \<City\>Tuscaloosa\</City\>

                \<StateCode\>AL\</StateCode\>

                \<Zip\>35401\</Zip\>

            \</Address\>

        \</Addresses\>

    \</Body\>

\</Request\>

**Response, Example Value Schema**

* **Success: Upon successful call, the service will return a 200 response along with the data requested. No hits will return an empty body with http status 200\.**

\<Response xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"\>

  \<Header\>

    \<TransactionId\>f062735d-bac5-492f-856a-0c3fa316f263\</TransactionId\>

    \<Quoteback\>QB123456\</Quoteback\>

  \</Header\>

  \<Body\>

    \<Policies\>

      \<Policy\>

        \<PolicyNumber\>ALVRSK2017112001\</PolicyNumber\>

        \<PolicyStatus\>EXPIRED\</PolicyStatus\>

        \<PolicyReportedDate\>20180226\</PolicyReportedDate\>

        \<InceptionDate\>20190111\</InceptionDate\>

        \<LastReportedTermEffectiveDate\>20190111\</LastReportedTermEffectiveDate\>

        \<LastReportedTermExpirationDate\>20200111\</LastReportedTermExpirationDate\>

        \<NumberOfCancellations\>0\</NumberOfCancellations\>

        \<NumberOfRenewals\>0\</NumberOfRenewals\>

        \<NumberOfEndorsements\>0\</NumberOfEndorsements\>

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

        \</MatchBasisInformation\>        \<Detail\>

          \<PolicyInformation\>

            \<PolicyType\>

              \<Code\>AU\</Code\>

              \<Description\>Auto\</Description\>

            \</PolicyType\>

            \<TermEffectiveDate\>20190111\</TermEffectiveDate\>

            \<TermExpirationDate\>20200111\</TermExpirationDate\>

            \<PolicyHolders\>

              \<PolicyHolder\>

                \<GivenName\>JOSEPHINEALONE\</GivenName\>

                \<MiddleName\>A\</MiddleName\>

                \<Surname\>MILLERALONE\</Surname\>

                \<DOB\>19411224\</DOB\>

                \<DLNumber\>9758318\</DLNumber\>

                \<DLState\>AL\</DLState\>

              \</PolicyHolder\>

            \</PolicyHolders\>

          \</PolicyInformation\>

          \<Subjects\>

            \<Subject\>

              \<GivenName\>JOSEPHINEALONE\</GivenName\>

              \<MiddleName\>A\</MiddleName\>

              \<Surname\>MILLERALONE\</Surname\>

              \<DOB\>19411224\</DOB\>

              \<Gender\>F\</Gender\>

              \<MaritalStatus\>S\</MaritalStatus\>

              \<DLNumber\>9758318\</DLNumber\>

              \<DLState\>AL\</DLState\>

              \<RelationToPolicyHolder\>

                \<Code\>PP\</Code\>

                \<Description\>Primary Policyholder\</Description\>

              \</RelationToPolicyHolder\>

              \<RelationToInsured\>

                \<Code\>I\</Code\>

                \<Description\>Insured\</Description\>

              \</RelationToInsured\>

              \<FromDate\>20190111\</FromDate\>

              \<ToDate\>20200111\</ToDate\>

              \<DriverSequenceId\>1\</DriverSequenceId\>

            \</Subject\>

          \</Subjects\>

          \<Carrier\>

            \<Name\>INSURANCE SERVICES O\</Name\>

            \<AMBEST\>99999\</AMBEST\>

            \<NAIC\>00000\</NAIC\>

            \<FinancialAMBEST\>99999\</FinancialAMBEST\>

          \</Carrier\>

          \<MailingAddress\>

            \<Street1\>W 8115 Oatman Rd\</Street1\>

            \<City\>Tuscaloosa\</City\>

            \<StateCode\>AL\</StateCode\>

            \<Zip\>35401\</Zip\>

            \<CountryCode\>US\</CountryCode\>

            \<FromDate\>20190111\</FromDate\>

            \<ToDate\>20200111\</ToDate\>

          \</MailingAddress\>

          \<Coverages\>

            \<Coverage\>

              \<CoverageType\>

                \<Code\>BINJ\</Code\>

                \<Description\>Bodily Injury\</Description\>

              \</CoverageType\>

              \<IndividualLimitAmount\>10000\</IndividualLimitAmount\>

              \<OccurrenceLimitAmount\>25000\</OccurrenceLimitAmount\>

              \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

              \<FromDate\>20190111\</FromDate\>

              \<ToDate\>20200111\</ToDate\>

            \</Coverage\>

            \<Coverage\>

              \<CoverageType\>

                \<Code\>PINJ\</Code\>

                \<Description\>Personal Injury\</Description\>

              \</CoverageType\>

              \<IndividualLimitAmount\>25000\</IndividualLimitAmount\>

              \<OccurrenceLimitAmount\>50000\</OccurrenceLimitAmount\>

              \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

              \<FromDate\>20190111\</FromDate\>

              \<ToDate\>20200111\</ToDate\>

            \</Coverage\>

          \</Coverages\>

          \<Vehicles\>

            \<Vehicle\>

              \<Year\>1987\</Year\>

              \<Make\>ACURA\</Make\>

              \<Model\>LEGEND\</Model\>

              \<VIN\>I0ZYX89TMON984281\</VIN\>

              \<ClassCode\>000000\</ClassCode\>

              \<CollisionDeductibleAmount\>1000\</CollisionDeductibleAmount\>

              \<ComprehensiveDeductibleAmount\>500\</ComprehensiveDeductibleAmount\>

              \<FromDate\>20190111\</FromDate\>

              \<ToDate\>20200111\</ToDate\>

              \<CollisionIndicator\>N\</CollisionIndicator\>

              \<ComprehensiveIndicator\>N\</ComprehensiveIndicator\>

              \<Coverages\>

                \<Coverage\>

                  \<CoverageType\>

                    \<Code\>BINJ\</Code\>

                    \<Description\>Bodily Injury\</Description\>

                  \</CoverageType\>

                  \<IndividualLimitAmount\>10000\</IndividualLimitAmount\>

                  \<OccurrenceLimitAmount\>25000\</OccurrenceLimitAmount\>

                  \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                  \<FromDate\>20190111\</FromDate\>

                  \<ToDate\>20200111\</ToDate\>

                \</Coverage\>

                \<Coverage\>

                  \<CoverageType\>

                    \<Code\>PINJ\</Code\>

                    \<Description\>Personal Injury\</Description\>

                  \</CoverageType\>

                  \<IndividualLimitAmount\>25000\</IndividualLimitAmount\>

                  \<OccurrenceLimitAmount\>50000\</OccurrenceLimitAmount\>

                  \<CombinedSingleLimitAmount\>0\</CombinedSingleLimitAmount\>

                  \<FromDate\>20190111\</FromDate\>

                  \<ToDate\>20200111\</ToDate\>

                \</Coverage\>

              \</Coverages\>

            \</Vehicle\>

          \</Vehicles\>

        \</Detail\>

        \<History /\>

      \</Policy\>

    \</Policies\>

    \<CoverageLapseInformation\>

      \<SearchPerson\>

        \<GivenName\>JosephineALONE\</GivenName\>

        \<Surname\>MillerALONE\</Surname\>

        \<InputDriverSequenceNumber\>1\</InputDriverSequenceNumber\>

        \<HasPossibleLapse\>N\</HasPossibleLapse\>

        \<IsCurrentInforceCoverage\>N\</IsCurrentInforceCoverage\>

        \<CoverageIntervals\>

          \<CoverageInterval\>

            \<Carrier\>

              \<Name\>INSURANCE SERVICES O\</Name\>

              \<AMBEST\>99999\</AMBEST\>

              \<NAIC\>00000\</NAIC\>

              \<FinancialAMBEST\>99999\</FinancialAMBEST\>

            \</Carrier\>

            \<StartDate\>20190111\</StartDate\>

            \<EndDate\>20200111\</EndDate\>

            \<NumberOfCoverageDays\>365\</NumberOfCoverageDays\>

            \<HasBreakFromPriorCoverage\>NA\</HasBreakFromPriorCoverage\>

            \<NumberOfLapseDays\>0\</NumberOfLapseDays\>

          \</CoverageInterval\>

        \</CoverageIntervals\>

      \</SearchPerson\>

    \</CoverageLapseInformation\>

    \<AnalyticObjects\>

      \<SearchPersonAO\>

        \<GivenName\>JosephineALONE\</GivenName\>

        \<Surname\>MillerALONE\</Surname\>

        \<InputDriverSequenceNumber\>1\</InputDriverSequenceNumber\>

        \<ChangeAttributes\>

          \<ChangeAttribute\>

            \<Code\>346\</Code\>

            \<Description\>Last pol coverage gap\</Description\>

            \<Count\>1718\</Count\>

            \<LastReportedDate\>20190111\</LastReportedDate\>

          \</ChangeAttribute\>

          \<ChangeAttribute\>

            \<Code\>300\</Code\>

            \<Description\>Current active policy count\</Description\>

            \<Count\>0\</Count\>

          \</ChangeAttribute\>

          \<ChangeAttribute\>

            \<Code\>126\</Code\>

            \<Description\>Vehicles exceed drivers beg\</Description\>

            \<Flag\>0\</Flag\>

            \<LastReportedDate\>20190111\</LastReportedDate\>

          \</ChangeAttribute\>

          \<ChangeAttribute\>

            \<Code\>127\</Code\>

            \<Description\>Drivers exceed vehicles beg\</Description\>

            \<Flag\>0\</Flag\>

            \<LastReportedDate\>20190111\</LastReportedDate\>

          \</ChangeAttribute\>

        \</ChangeAttributes\>

        \<Scores\>

          \<Score\>

            \<Name\>ScoreName1\</Name\>

            \<Value\>100\</Value\>

          \</Score\>

          \<Score\>

            \<Name\>ScoreName2\</Name\>

            \<Value\>100\</Value\>

          \</Score\>

          \<Score\>

            \<Name\>ScoreName3\</Name\>

            \<Value\>100\</Value\>

          \</Score\>

        \</Scores\>

      \</SearchPersonAO\>

    \</AnalyticObjects\>

  \</Body\>

\</Response\>

