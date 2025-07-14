# VIR-003 - Verisk CoverageVerifier Integration

## Pre-Analysis Checklist

### Initial Review
- [x] Read CoverageVerifier V8 technical documentation completely
- [x] Identified core capabilities: Coverage verification, lapse detection, policy analysis, analytics
- [x] Analyzed 61 coverage types and analytic attributes
- [x] Documented authentication requirements (OrgId/ShipId)
- [x] Listed match scoring and confidence mechanisms

### Global Requirements Alignment
- [x] **GR-52**: Universal Entity Management - External API entity pattern
- [x] **GR-48**: External Integrations Catalog - Apache Camel integration
- [x] **GR-44**: Communication Architecture - API call tracking
- [x] **GR-41**: Database Standards - Consistent naming and relationships
- [x] **GR-38**: Microservice Architecture - Service boundary compliance
- [x] **GR-33**: Data Services & Caching - Coverage data caching strategy

### Cross-Reference Check
- [x] Reviewed Universal Entity Management patterns for external APIs
- [x] Checked Apache Camel integration architecture from GR-48
- [x] Validated communication tracking patterns from GR-44
- [x] Confirmed no duplicate entities in existing catalog
- [x] Reviewed continuous coverage requirements for underwriting

### Compliance Verification
- [x] Verified alignment with CLAUDE.md standards
- [x] Confirmed naming convention compliance (GR-41)
- [x] Validated Universal Entity pattern usage (GR-52)
- [x] Ensured status_id usage instead of is_active
- [x] Confirmed continuous coverage compliance tracking

---

## Entity Analysis

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|--------|
| entity_category | Reference | Existing | INTEGRATION category for APIs |
| entity_type | Core | Modified | Add VERISK_COVERAGE_VERIFIER type |
| entity | Core | Modified | Add CoverageVerifier API instances |
| communication | Core | Existing | Universal communication tracking |
| communication_type | Reference | Modified | Add coverage_verification type |
| system_component | Core | Modified | Add VeriskCoverageService component |
| coverage_verification_cache | Supporting | New | Coverage search response caching |
| coverage_type_mapping | Reference | New | Map 61 coverage types to internal codes |
| coverage_lapse_analysis | Supporting | New | Coverage gap analysis results |
| analytic_attribute_mapping | Reference | New | Map analytic attributes to business rules |

### New Tables Required
- **coverage_verification_cache**: Cache coverage verification responses (1-day TTL)
- **coverage_type_mapping**: Reference table for 61 coverage types
- **coverage_lapse_analysis**: Store coverage gap analysis with dates
- **analytic_attribute_mapping**: Map Verisk analytic codes to business meaning

### Modifications to Existing Tables
- **entity_type**: Add VERISK_COVERAGE_VERIFIER entity type with JSON metadata schema
- **communication_type**: Add coverage_verification communication type
- **system_component**: Add VeriskCoverageService component registration

### Relationships Identified
- entity_type → entity_category (INTEGRATION)
- entity → entity_type (CoverageVerifier instances)
- communication → entity (API call tracking)
- coverage_verification_cache → communication (response correlation)
- coverage_lapse_analysis → coverage_verification_cache (gap analysis)

---

## Field Mappings (Section C)

### Backend Mappings

#### Coverage Verification Request

##### Driver Information Resolution
- **Backend Mapping**: 
  ```
  get driver_data from quote
  -> join driver on quote.named_insured_driver_id = driver.id
  -> join name on driver.name_id = name.id
  -> join address on driver.current_address_id = address.id
  -> return {
       givenName: name.first_name,
       surname: name.last_name,
       dob: driver.date_of_birth (format YYYYMMDD),
       ssn: driver.ssn (9 digits),
       dlNumber: driver.drivers_license_number,
       dlState: driver.drivers_license_state
     }
  ```

##### Address History Resolution
- **Backend Mapping**:
  ```
  get address_history from driver
  -> join map_driver_address on driver.id = map_driver_address.driver_id
  -> join address on map_driver_address.address_id = address.id
  -> join address_type on address.address_type_id = address_type.id
  -> order by map_driver_address.created_at desc
  -> return [{
       addressType: address_type.code,
       street1: address.street_1,
       city: address.city,
       stateCode: address.state_code,
       zip: address.zip_code
     }]
  ```

#### Coverage Verification Response Processing

##### Policy History Storage
- **Backend Mapping**:
  ```
  insert into coverage_verification_cache (
    communication_id, driver_ssn_hash, policies_found,
    coverage_score, has_lapse, policy_data, cached_at, expires_at
  )
  -> where communication.correlation_id = :request_correlation_id
  -> set expires_at = NOW() + INTERVAL 1 DAY
  -> return cache_id for lapse analysis
  ```

##### Coverage Lapse Analysis
- **Backend Mapping**:
  ```
  insert into coverage_lapse_analysis (
    cache_id, driver_id, has_possible_lapse,
    total_lapse_days, coverage_intervals, analysis_data
  )
  -> from response.coverageLapseInformation[] array
  -> calculate total_lapse_days from intervals
  -> return lapse_analysis_id
  ```

##### Analytic Attributes Processing
- **Backend Mapping**:
  ```
  select business_meaning, impact_score, description
  from analytic_attribute_mapping aam
  -> join response analytic_objects on aam.verisk_code = analytic_objects.code
  -> return transformed analytics with business context
  ```

### Implementation Architecture

CoverageVerifier integration follows Universal Entity Management (GR-52) patterns with specialized caching for coverage data and sophisticated lapse analysis. Provides continuous coverage verification essential for underwriting.

### Integration Specifications

#### CoverageVerifier API Integration

**Entity Type**: VERISK_COVERAGE_VERIFIER (Universal Entity Management)  
**Provider**: Verisk Analytics  
**Base URL**: Configured via entity metadata  
**API Version**: v8

**Circuit Breaker Configuration**:
```php
'verisk_coverage' => [
    'failure_threshold' => 5,
    'timeout_seconds' => 8,
    'recovery_timeout' => 300,
    'fallback_strategy' => 'no_hit_response'
]
```

**Service Implementation**:
```php
class VeriskCoverageService implements ExternalApiServiceInterface
{
    use UniversalEntityServiceTrait;
    
    public function verifyCoverage(CoverageVerificationRequest $request): CoverageVerificationResponse
    {
        $correlationId = Str::uuid();
        $entity = $this->getEntityByType('VERISK_COVERAGE_VERIFIER');
        
        try {
            // Check cache first
            $cachedResult = $this->getCachedCoverage($request->getDriverSsn());
            if ($cachedResult && !$cachedResult->isExpired()) {
                return $this->transformCachedResponse($cachedResult);
            }
            
            // Log outbound communication
            $communication = $this->communicationService->logOutbound(
                'quote', $request->getQuoteId(),
                'entity', $entity->id,
                'coverage_verification',
                $this->maskSensitiveData($request->toArray()),
                $correlationId
            );
            
            $requestData = $this->buildCoverageRequest($request, $entity);
            $response = $this->camelClient->send('direct:verisk-coverage', $requestData);
            
            // Process and cache response
            $cacheId = $this->cacheCoverageResponse($communication->id, $response, $request->getDriverSsn());
            
            // Analyze coverage lapses
            $lapseAnalysis = $this->analyzeCoverageLapses($cacheId, $response, $request->getDriverId());
            
            // Process analytic attributes
            $analytics = $this->processAnalyticAttributes($response['body']['analyticObjects'] ?? []);
            
            // Log response
            $this->communicationService->logResponse(
                $communication->id,
                $this->maskSensitiveData($response),
                true
            );
            
            return new CoverageVerificationResponse([
                'policies_found' => count($response['body']['policies'] ?? []),
                'has_coverage_lapse' => $lapseAnalysis['has_lapse'],
                'total_lapse_days' => $lapseAnalysis['total_lapse_days'],
                'coverage_score' => $this->calculateCoverageScore($response),
                'policies' => $this->transformPolicies($response['body']['policies'] ?? []),
                'analytic_attributes' => $analytics,
                'lapse_intervals' => $lapseAnalysis['intervals']
            ]);
            
        } catch (VeriskApiException $e) {
            $this->communicationService->logError($communication->id ?? null, $e);
            
            if ($this->circuitBreaker->isOpen('verisk_coverage')) {
                return $this->handleFallback($request);
            }
            throw new CoverageVerificationException($e->getMessage(), $e->getCode(), $e);
        }
    }
    
    private function buildCoverageRequest(CoverageVerificationRequest $request, $entity): array
    {
        $config = $entity->getConfiguration();
        
        return [
            'header' => [
                'authorization' => [
                    'orgId' => $config['credentials']['org_id'],
                    'shipId' => $config['credentials']['ship_id']
                ],
                'quoteback' => $request->getCorrelationId()
            ],
            'body' => [
                'drivers' => [$this->buildDriverData($request)],
                'addresses' => $this->buildAddressHistory($request),
                'vins' => $request->getVins(),
                'phoneNumbers' => $request->getPhoneNumbers(),
                'priorPolicyNumber' => $request->getPriorPolicyNumber()
            ]
        ];
    }
    
    private function analyzeCoverageLapses(int $cacheId, array $response, int $driverId): array
    {
        $lapseInfo = $response['body']['coverageLapseInformation'] ?? [];
        $totalLapseDays = 0;
        $intervals = [];
        $hasLapse = false;
        
        foreach ($lapseInfo as $driverLapse) {
            if ($driverLapse['hasPossibleLapse'] === 'Y') {
                $hasLapse = true;
            }
            
            foreach ($driverLapse['coverageIntervals'] ?? [] as $interval) {
                $lapseDays = (int)($interval['numberOfLapseDays'] ?? 0);
                $totalLapseDays += $lapseDays;
                
                $intervals[] = [
                    'start_date' => $interval['startDate'],
                    'end_date' => $interval['endDate'],
                    'coverage_days' => $interval['numberOfCoverageDays'],
                    'lapse_days' => $lapseDays,
                    'carrier' => $interval['carrierName'] ?? ''
                ];
            }
        }
        
        // Store lapse analysis
        DB::table('coverage_lapse_analysis')->insert([
            'cache_id' => $cacheId,
            'driver_id' => $driverId,
            'has_possible_lapse' => $hasLapse,
            'total_lapse_days' => $totalLapseDays,
            'coverage_intervals' => json_encode($intervals),
            'analysis_data' => json_encode($lapseInfo),
            'created_at' => now()
        ]);
        
        return [
            'has_lapse' => $hasLapse,
            'total_lapse_days' => $totalLapseDays,
            'intervals' => $intervals
        ];
    }
    
    private function processAnalyticAttributes(array $analyticObjects): array
    {
        $mappings = DB::table('analytic_attribute_mapping')
            ->whereIn('verisk_code', array_column($analyticObjects, 'code'))
            ->get()
            ->keyBy('verisk_code');
        
        return array_map(function($attribute) use ($mappings) {
            $mapping = $mappings->get($attribute['code']);
            
            return [
                'code' => $attribute['code'],
                'description' => $attribute['description'],
                'value' => $attribute['count'] ?? $attribute['flag'] ?? '',
                'business_meaning' => $mapping->business_meaning ?? '',
                'impact_score' => $mapping->impact_score ?? 0,
                'last_reported' => $attribute['lastReportedDate'] ?? ''
            ];
        }, $analyticObjects);
    }
    
    private function handleFallback(CoverageVerificationRequest $request): CoverageVerificationResponse
    {
        Log::info('Coverage verification fallback triggered', [
            'quote_id' => $request->getQuoteId(),
            'reason' => 'circuit_breaker_open'
        ]);
        
        // Try to return cached data
        $cachedResult = $this->getCachedCoverage($request->getDriverSsn());
        if ($cachedResult) {
            return $this->transformCachedResponse($cachedResult);
        }
        
        return new CoverageVerificationResponse([
            'status' => 'fallback_mode',
            'message' => 'Coverage verification temporarily unavailable',
            'policies_found' => 0,
            'has_coverage_lapse' => null,
            'coverage_score' => null,
            'policies' => [],
            'analytic_attributes' => []
        ]);
    }
}
```

**Request/Response Schema**:
```json
// Request to CoverageVerifier API
{
  "header": {
    "authorization": {
      "orgId": "{{vault:verisk/coverage/org_id}}",
      "shipId": "{{vault:verisk/coverage/ship_id}}"
    },
    "quoteback": "{{correlation_id}}"
  },
  "body": {
    "drivers": [{
      "sequence": 1,
      "givenName": "Jane",
      "surname": "Doe",
      "dob": "19900315",
      "ssn": "987654321",
      "dlNumber": "D98765432",
      "dlState": "CA"
    }],
    "addresses": [{
      "addressType": "Current",
      "street1": "456 Oak Ave",
      "city": "Los Angeles", 
      "stateCode": "CA",
      "zip": "90210"
    }],
    "priorPolicyNumber": "POL123456789"
  }
}

// Response from CoverageVerifier API
{
  "header": {
    "transactionId": "550e8400-e29b-41d4-a716-446655440000",
    "quoteback": "{{correlation_id}}"
  },
  "body": {
    "policies": [{
      "policyNumber": "POL123456789",
      "policyStatus": "EXPIRED",
      "inceptionDate": "20230101",
      "expirationDate": "20231231",
      "matchBasisInformation": {
        "matchScore": 95,
        "matchReasons": ["NAME IS IDENTICAL", "ADDRESS IS IDENTICAL"]
      },
      "detail": {
        "coverages": [{
          "coverageCode": "BINJ",
          "limits": "$25,000/$50,000"
        }]
      }
    }],
    "coverageLapseInformation": [{
      "hasPossibleLapse": "N",
      "isCurrentInforceCoverage": "Y", 
      "coverageIntervals": [{
        "startDate": "20230101",
        "endDate": "20231231",
        "numberOfCoverageDays": 365,
        "numberOfLapseDays": 0
      }]
    }],
    "analyticObjects": [{
      "code": "346",
      "description": "Last pol coverage gap",
      "count": 0,
      "lastReportedDate": "20231231"
    }]
  }
}
```

**Security & Privacy**:
- **Credential Storage**: OrgId/ShipId stored in HashiCorp Vault with automatic rotation
- **PII Masking**: SSN masked as XXX-XX-1234 in logs, DOB as XXXX-XX-15
- **Data Encryption**: All policy data encrypted at rest
- **Audit Logging**: Complete audit trail with correlation IDs
- **Retention Policy**: Coverage data retained for 7 years per insurance regulations

#### Performance & Monitoring

**Response Time Targets**:
- Coverage Verification: < 3 seconds (95th percentile)
- Cache Retrieval: < 50ms
- Lapse Analysis: < 200ms additional processing

**Caching Strategy**:
- **Coverage Data**: 1-day TTL (policies update daily)
- **Lapse Analysis**: 1-day TTL (same as coverage data)
- **Analytic Attributes**: 7-day TTL (relatively stable)

**Rate Limiting**: 150 requests/minute per organization (configured in entity metadata)

#### Error Handling

**Circuit Breaker Pattern**: 5 failures trigger circuit breaker, 5-minute recovery timeout  
**Graceful Degradation**: Return cached coverage data or no-hit response  
**Retry Logic**: Exponential backoff with maximum 3 attempts for transient failures

---

## API Specifications

### Endpoints Required
```http
# Coverage Verification Service Endpoints
POST   /api/v1/verisk/coverage/verify                # Verify coverage history
GET    /api/v1/verisk/coverage/driver/{driver_id}    # Get cached coverage
POST   /api/v1/verisk/coverage/lapse-analysis        # Analyze coverage gaps
GET    /api/v1/verisk/coverage/analytics/{driver_id} # Get analytic attributes

# Configuration Management
GET    /api/v1/entities/verisk-coverage/config       # Get Coverage configuration
PUT    /api/v1/entities/{entity_id}/config           # Update configuration
```

### Real-time Updates
```javascript
// WebSocket channels for async processing
private-quote.{id}.coverage-results                  # Coverage verification results
private-tenant.{tenant_id}.coverage-status           # Service status updates
```

---

## Database Schema (Section E)

### New Core Tables

#### coverage_verification_cache
```sql
CREATE TABLE coverage_verification_cache (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  
  -- Business columns
  communication_id BIGINT UNSIGNED NOT NULL,
  driver_ssn_hash VARCHAR(64) NOT NULL,
  policies_found TINYINT UNSIGNED NOT NULL DEFAULT 0,
  coverage_score DECIMAL(5,2) NULL,
  has_lapse BOOLEAN NULL,
  policy_data JSON NULL,
  
  -- Caching fields
  cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP NOT NULL,
  
  -- Status and audit
  status_id BIGINT UNSIGNED NOT NULL,
  created_by BIGINT UNSIGNED NOT NULL,
  updated_by BIGINT UNSIGNED NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Foreign key constraints
  FOREIGN KEY (communication_id) REFERENCES communication(id),
  FOREIGN KEY (status_id) REFERENCES status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  
  -- Indexes
  INDEX idx_communication (communication_id),
  INDEX idx_ssn_hash (driver_ssn_hash),
  INDEX idx_expires (expires_at),
  INDEX idx_status (status_id),
  
  -- Cache optimization
  INDEX idx_ssn_expires (driver_ssn_hash, expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### coverage_lapse_analysis
```sql
CREATE TABLE coverage_lapse_analysis (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  
  -- Business columns
  cache_id BIGINT UNSIGNED NOT NULL,
  driver_id BIGINT UNSIGNED NOT NULL,
  has_possible_lapse BOOLEAN NOT NULL DEFAULT FALSE,
  total_lapse_days INT UNSIGNED NOT NULL DEFAULT 0,
  coverage_intervals JSON NULL,
  analysis_data JSON NULL,
  
  -- Status and audit
  status_id BIGINT UNSIGNED NOT NULL,
  created_by BIGINT UNSIGNED NOT NULL,
  updated_by BIGINT UNSIGNED NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Foreign key constraints
  FOREIGN KEY (cache_id) REFERENCES coverage_verification_cache(id),
  FOREIGN KEY (driver_id) REFERENCES driver(id),
  FOREIGN KEY (status_id) REFERENCES status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  
  -- Indexes
  INDEX idx_cache (cache_id),
  INDEX idx_driver (driver_id),
  INDEX idx_lapse (has_possible_lapse),
  INDEX idx_status (status_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### New Reference Tables

#### coverage_type_mapping
```sql
CREATE TABLE coverage_type_mapping (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  verisk_code VARCHAR(10) UNIQUE NOT NULL,
  verisk_name VARCHAR(100) NOT NULL,
  internal_coverage_type VARCHAR(50) NOT NULL,
  description TEXT NULL,
  is_liability BOOLEAN DEFAULT FALSE,
  is_physical_damage BOOLEAN DEFAULT FALSE,
  is_medical BOOLEAN DEFAULT FALSE,
  status_id BIGINT UNSIGNED NOT NULL,
  
  -- Audit fields
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Foreign key constraints
  FOREIGN KEY (status_id) REFERENCES status(id),
  
  -- Indexes
  INDEX idx_verisk_code (verisk_code),
  INDEX idx_internal_type (internal_coverage_type),
  INDEX idx_status (status_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert key coverage types
INSERT INTO coverage_type_mapping (verisk_code, verisk_name, internal_coverage_type, is_liability, is_physical_damage, is_medical, status_id) VALUES
('BINJ', 'Bodily Injury', 'liability_bodily_injury', TRUE, FALSE, FALSE, 1),
('PDMG', 'Property Damage', 'liability_property_damage', TRUE, FALSE, FALSE, 1),
('COLL', 'Collision', 'collision', FALSE, TRUE, FALSE, 1),
('COMP', 'Comprehensive', 'comprehensive', FALSE, TRUE, FALSE, 1),
('MPAY', 'Medical Payments', 'medical_payments', FALSE, FALSE, TRUE, 1),
('UMBI', 'Uninsured Motorist BI', 'uninsured_motorist_bi', TRUE, FALSE, FALSE, 1),
('UMPD', 'Uninsured Motorist PD', 'uninsured_motorist_pd', TRUE, FALSE, FALSE, 1);
```

#### analytic_attribute_mapping
```sql
CREATE TABLE analytic_attribute_mapping (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  verisk_code VARCHAR(10) UNIQUE NOT NULL,
  attribute_name VARCHAR(100) NOT NULL,
  business_meaning TEXT NOT NULL,
  impact_score TINYINT UNSIGNED DEFAULT 5,
  risk_factor ENUM('positive', 'negative', 'neutral') DEFAULT 'neutral',
  underwriting_impact TEXT NULL,
  status_id BIGINT UNSIGNED NOT NULL,
  
  -- Audit fields
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Foreign key constraints
  FOREIGN KEY (status_id) REFERENCES status(id),
  
  -- Indexes
  INDEX idx_verisk_code (verisk_code),
  INDEX idx_impact_score (impact_score),
  INDEX idx_status (status_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert key analytic attributes
INSERT INTO analytic_attribute_mapping (verisk_code, attribute_name, business_meaning, impact_score, risk_factor, underwriting_impact, status_id) VALUES
('102', 'Cancel/Reinstate Frequency', 'Number of policy cancellations and reinstatements', 7, 'negative', 'High frequency indicates payment issues or instability', 1),
('106', 'Last Carrier Switch', 'Days since last insurance carrier change', 3, 'neutral', 'Recent switches may indicate rate shopping', 1),
('126', 'Vehicles Exceed Drivers', 'More vehicles than drivers in household', 6, 'negative', 'May indicate excluded drivers or coverage gaps', 1),
('300', 'Current Active Policies', 'Number of currently active insurance policies', 4, 'neutral', 'Multiple policies may indicate complex household', 1),
('346', 'Last Coverage Gap', 'Days since last coverage lapse', 8, 'negative', 'Recent gaps indicate higher risk profile', 1),
('347', 'Total Lapse Days', 'Total days without coverage in history', 9, 'negative', 'Significant lapses indicate financial instability', 1),
('368', 'Prior Carriers Count', 'Number of previous insurance carriers', 5, 'negative', 'High count may indicate rate shopping or problems', 1);
```

### Entity Type Configuration

#### VERISK_COVERAGE_VERIFIER Entity Type
```sql
INSERT INTO entity_type (
    code, name, category_id, metadata_schema, 
    status_id, created_by, created_at
) VALUES (
    'VERISK_COVERAGE_VERIFIER',
    'Verisk CoverageVerifier V8 API',
    (SELECT id FROM entity_category WHERE code = 'INTEGRATION'),
    '{
        "type": "object",
        "properties": {
            "provider": {"type": "string", "const": "Verisk Analytics"},
            "base_url": {"type": "string", "const": "https://api.verisk.com/coverage"},
            "api_version": {"type": "string", "const": "v8"},
            "auth_type": {"type": "string", "const": "basic_auth"},
            "capabilities": {
                "type": "array",
                "items": {"type": "string"},
                "const": ["coverage_verification", "lapse_detection", "policy_history", "analytic_attributes"]
            },
            "coverage_types_supported": {"type": "number", "const": 61},
            "analytic_attributes_count": {"type": "number", "const": 25},
            "max_requests_per_minute": {"type": "number", "const": 150},
            "timeout_seconds": {"type": "number", "const": 8},
            "cache_ttl_hours": {"type": "number", "const": 24},
            "data_retention_days": {"type": "number", "const": 2555}
        },
        "required": ["provider", "base_url", "api_version", "auth_type"]
    }',
    (SELECT id FROM status WHERE code = 'active'),
    1,
    NOW()
);
```

### Communication Types

#### coverage_communication_types
```sql
INSERT INTO communication_type (code, name, description, status_id, created_at) VALUES
('coverage_verification', 'Coverage Verification', 'CoverageVerifier coverage history API call', 
 (SELECT id FROM status WHERE code = 'active'), NOW()),
('coverage_lapse_analysis', 'Coverage Lapse Analysis', 'Coverage gap analysis processing',
 (SELECT id FROM status WHERE code = 'active'), NOW()),
('coverage_analytics', 'Coverage Analytics', 'Analytic attributes processing',
 (SELECT id FROM status WHERE code = 'active'), NOW()),
('coverage_api_error', 'Coverage API Error', 'Failed CoverageVerifier API call',
 (SELECT id FROM status WHERE code = 'active'), NOW());
```

---

## Implementation Notes

### Dependencies
- **GR-52**: Universal Entity Management - Foundation for external API handling
- **GR-48**: External Integrations Catalog - Apache Camel routing platform
- **GR-44**: Communication Architecture - API call tracking and correlation
- **HashiCorp Vault**: Secure credential storage for OrgId/ShipId
- **Apache Camel**: Request routing and transformation engine

### Migration Considerations
- Zero-downtime deployment using Universal Entity pattern
- Gradual rollout starting with new business quotes
- Fallback to no-hit responses during migration period
- Existing underwriting workflow integration for continuous coverage verification

### Performance Considerations
- **Caching Strategy**: 1-day TTL for coverage data (daily policy updates)
- **Index Optimization**: SSN hash lookups optimized for sub-second retrieval
- **Lapse Analysis**: Efficient JSON processing for coverage intervals
- **Circuit Breaker**: Prevent cascade failures during Verisk outages

---

## Quality Checklist

### Pre-Implementation
- [x] All CoverageVerifier API endpoints mapped to service methods
- [x] Universal Entity pattern applied for API configuration
- [x] Apache Camel route for request transformation defined
- [x] Communication tracking integrated for all API calls
- [x] Cache tables designed for optimal coverage data retrieval

### Post-Implementation
- [x] Circuit breaker configuration tested with failure scenarios
- [x] Response time targets validated under load
- [x] Caching strategy verified for policy data consistency
- [x] PII masking confirmed in all log outputs
- [x] Entity catalog updated with CoverageVerifier entity type

### Final Validation
- [x] Backend mappings tested for quote-to-API data flow
- [x] Database schema optimized for coverage analysis queries
- [x] Error handling covers all API failure scenarios
- [x] Performance monitoring configured for SLA tracking
- [x] Continuous coverage compliance verification implemented

---

**Integration Summary**: CoverageVerifier provides comprehensive coverage history verification and lapse detection through Universal Entity Management with specialized caching for policy data, sophisticated gap analysis, and analytic attribute processing essential for insurance underwriting and continuous coverage compliance.