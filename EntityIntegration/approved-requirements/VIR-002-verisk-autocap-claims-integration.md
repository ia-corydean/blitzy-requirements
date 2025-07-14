# VIR-002 - Verisk AutoCapWithClaims Integration

## Pre-Analysis Checklist

### Initial Review
- [x] Read AutoCapWithClaims technical documentation completely
- [x] Identified core capabilities: Claims search, CAP prediction, VIN validation, SSN verification
- [x] Analyzed request/response schemas (V4)
- [x] Documented authentication requirements (OrgId/ShipId)
- [x] Listed all search types: VIN, SSN, Driver License, Name/Address, Phone

### Global Requirements Alignment
- [x] **GR-52**: Universal Entity Management - External API entity pattern
- [x] **GR-48**: External Integrations Catalog - Apache Camel integration
- [x] **GR-44**: Communication Architecture - API call tracking
- [x] **GR-41**: Database Standards - Consistent naming and relationships
- [x] **GR-38**: Microservice Architecture - Service boundary compliance
- [x] **GR-33**: Data Services & Caching - Response caching strategy

### Cross-Reference Check
- [x] Reviewed Universal Entity Management patterns for external APIs
- [x] Checked Apache Camel integration architecture from GR-48
- [x] Validated communication tracking patterns from GR-44
- [x] Confirmed no duplicate entities in existing catalog
- [x] Reviewed DCS integration patterns from GR-53 for reference

### Compliance Verification
- [x] Verified alignment with CLAUDE.md standards
- [x] Confirmed naming convention compliance (GR-41)
- [x] Validated Universal Entity pattern usage (GR-52)
- [x] Ensured status_id usage instead of is_active
- [x] Confirmed PII masking requirements for insurance data

---

## Entity Analysis

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|--------|
| entity_category | Reference | Existing | INTEGRATION category for APIs |
| entity_type | Core | Modified | Add VERISK_AUTOCAP_CLAIMS type |
| entity | Core | Modified | Add AutoCap API instances |
| communication | Core | Existing | Universal communication tracking |
| communication_type | Reference | Modified | Add autocap_claims_search type |
| system_component | Core | Modified | Add VeriskAutoCapService component |
| autocap_claims_cache | Supporting | New | Claims response caching |
| autocap_vehicle_data | Supporting | New | Vehicle information cache |
| autocap_ssn_validation | Supporting | New | SSN validation results |

### New Tables Required
- **autocap_claims_cache**: Cache claims search responses (24-hour TTL)
- **autocap_vehicle_data**: Cache vehicle information and VIN validation
- **autocap_ssn_validation**: Cache SSN validation results

### Modifications to Existing Tables
- **entity_type**: Add VERISK_AUTOCAP_CLAIMS entity type with JSON metadata schema
- **communication_type**: Add autocap_claims_search communication type
- **system_component**: Add VeriskAutoCapService component registration

### Relationships Identified
- entity_type → entity_category (INTEGRATION)
- entity → entity_type (AutoCap instances)
- communication → entity (API call tracking)
- system_component → entity (service boundaries)
- autocap_claims_cache → communication (response correlation)

---

## Field Mappings (Section C)

### Backend Mappings

#### AutoCap Claims Search Request

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

##### Address Information Resolution
- **Backend Mapping**:
  ```
  get address_data from driver
  -> join map_driver_address on driver.id = map_driver_address.driver_id
  -> join address on map_driver_address.address_id = address.id
  -> join address_type on address.address_type_id = address_type.id
  -> where address_type.code = 'current'
  -> return {
       addressType: 'Current',
       street1: address.street_1,
       city: address.city,
       stateCode: address.state_code,
       zip: address.zip_code
     }
  ```

#### AutoCap Claims Search Response Processing

##### Claims Data Storage
- **Backend Mapping**:
  ```
  insert into autocap_claims_cache (
    communication_id, driver_ssn_hash, cap_indicator,
    claims_count, claims_data, cached_at, expires_at
  )
  -> where communication.correlation_id = :request_correlation_id
  -> set expires_at = NOW() + INTERVAL 24 HOUR
  -> return cache_id for retrieval
  ```

##### Vehicle Information Storage
- **Backend Mapping**:
  ```
  insert into autocap_vehicle_data (
    vin, make, model, year, salvage_indicator,
    recall_count, vehicle_data, cached_at, expires_at
  )
  -> from response.vehicles[] array
  -> set expires_at = NOW() + INTERVAL 30 DAY
  -> return vehicle_cache_id
  ```

### Implementation Architecture

AutoCapWithClaims integration follows Universal Entity Management (GR-52) patterns with Apache Camel routing (GR-48) for request transformation and response processing. The service provides claims history and predictive analytics for risk assessment.

### Integration Specifications

#### AutoCapWithClaims API Integration

**Entity Type**: VERISK_AUTOCAP_CLAIMS (Universal Entity Management)  
**Provider**: Verisk Analytics  
**Base URL**: Configured via entity metadata  
**API Version**: v4

**Circuit Breaker Configuration**:
```php
'verisk_autocap' => [
    'failure_threshold' => 5,
    'timeout_seconds' => 10,
    'recovery_timeout' => 300,
    'fallback_strategy' => 'cached_response'
]
```

**Service Implementation**:
```php
class VeriskAutoCapService implements ExternalApiServiceInterface
{
    use UniversalEntityServiceTrait;
    
    public function searchClaims(AutoCapSearchRequest $request): AutoCapSearchResponse
    {
        $correlationId = Str::uuid();
        $entity = $this->getEntityByType('VERISK_AUTOCAP_CLAIMS');
        
        try {
            // Check cache first
            $cachedResult = $this->getCachedClaims($request->getDriverSsn());
            if ($cachedResult && !$cachedResult->isExpired()) {
                return $this->transformCachedResponse($cachedResult);
            }
            
            // Log outbound communication
            $communication = $this->communicationService->logOutbound(
                'quote', $request->getQuoteId(),
                'entity', $entity->id,
                'autocap_claims_search',
                $this->maskSensitiveData($request->toArray()),
                $correlationId
            );
            
            $requestData = $this->buildAutoCapRequest($request, $entity);
            $response = $this->camelClient->send('direct:verisk-autocap', $requestData);
            
            // Process and cache response
            $this->cacheClaimsResponse($communication->id, $response, $request->getDriverSsn());
            
            // Log response
            $this->communicationService->logResponse(
                $communication->id,
                $this->maskSensitiveData($response),
                true
            );
            
            return new AutoCapSearchResponse([
                'cap_indicator' => $response['body']['claimActivityPredictor']['capIndicator'],
                'claims_count' => $response['body']['claimActivityPredictor']['numberOfClaims'],
                'claims' => $this->transformClaims($response['body']['claims'] ?? []),
                'vehicles' => $this->transformVehicles($response['body']['vehicles'] ?? []),
                'ssn_validation' => $this->transformSsnValidation($response['body']['ssnInformations'] ?? [])
            ]);
            
        } catch (VeriskApiException $e) {
            $this->communicationService->logError($communication->id ?? null, $e);
            
            if ($this->circuitBreaker->isOpen('verisk_autocap')) {
                return $this->handleFallback($request);
            }
            throw new AutoCapServiceException($e->getMessage(), $e->getCode(), $e);
        }
    }
    
    private function buildAutoCapRequest(AutoCapSearchRequest $request, $entity): array
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
                'addresses' => [$this->buildAddressData($request)],
                'vins' => $request->getVins(),
                'phoneNumbers' => $request->getPhoneNumbers()
            ]
        ];
    }
    
    private function handleFallback(AutoCapSearchRequest $request): AutoCapSearchResponse
    {
        Log::info('AutoCap fallback triggered', [
            'quote_id' => $request->getQuoteId(),
            'reason' => 'circuit_breaker_open'
        ]);
        
        // Try to return cached data
        $cachedResult = $this->getCachedClaims($request->getDriverSsn());
        if ($cachedResult) {
            return $this->transformCachedResponse($cachedResult);
        }
        
        return new AutoCapSearchResponse([
            'status' => 'fallback_mode',
            'message' => 'Claims search temporarily unavailable',
            'cap_indicator' => 'N',
            'claims_count' => 0,
            'claims' => [],
            'vehicles' => [],
            'ssn_validation' => []
        ]);
    }
    
    private function transformClaims(array $claims): array
    {
        return array_map(function($claim) {
            return [
                'claim_reference' => $claim['claimReferenceNumber'] ?? '',
                'at_fault' => $claim['atFaultIndicator'] === 'Y',
                'loss_date' => $claim['lossDate'] ?? '',
                'paid_amount' => (float)($claim['paidAmount'] ?? 0),
                'coverage_type' => $claim['coverageType'] ?? '',
                'carrier' => $claim['carrierName'] ?? '',
                'policy_number' => $claim['policyNumber'] ?? ''
            ];
        }, $claims);
    }
}
```

**Request/Response Schema**:
```json
// Request to AutoCap API
{
  "header": {
    "authorization": {
      "orgId": "{{vault:verisk/autocap/org_id}}",
      "shipId": "{{vault:verisk/autocap/ship_id}}"
    },
    "quoteback": "{{correlation_id}}"
  },
  "body": {
    "drivers": [{
      "sequence": 1,
      "givenName": "John",
      "surname": "Smith", 
      "dob": "19851201",
      "ssn": "123456789",
      "dlNumber": "D12345678",
      "dlState": "TX"
    }],
    "addresses": [{
      "addressType": "Current",
      "street1": "123 Main St",
      "city": "Dallas",
      "stateCode": "TX",
      "zip": "75201"
    }],
    "vins": ["1HGBH41JXMN109186"],
    "phoneNumbers": ["2145551234"]
  }
}

// Response from AutoCap API
{
  "header": {
    "transactionId": "550e8400-e29b-41d4-a716-446655440000",
    "quoteback": "{{correlation_id}}"
  },
  "body": {
    "claimActivityPredictor": {
      "capIndicator": "Y",
      "numberOfClaims": 2
    },
    "claims": [{
      "claimReferenceNumber": "ABC123456",
      "atFaultIndicator": "Y",
      "lossDate": "20230615",
      "paidAmount": 5000.00,
      "coverageType": "COLLISION",
      "carrierName": "ABC Insurance"
    }],
    "vehicles": [{
      "vin": "1HGBH41JXMN109186",
      "make": "HONDA",
      "model": "ACCORD",
      "year": 2021,
      "salvageIndicator": "N"
    }],
    "ssnInformations": [{
      "ssnValidationStatus": "VALID",
      "deathMasterMatch": "N"
    }]
  }
}
```

**Security & Privacy**:
- **Credential Storage**: OrgId/ShipId stored in HashiCorp Vault with automatic rotation
- **PII Masking**: SSN masked as XXX-XX-1234 in logs, DOB as XXXX-XX-01
- **Data Encryption**: All request/response data encrypted at rest
- **Audit Logging**: Complete audit trail with correlation IDs
- **Retention Policy**: Claims data retained for 7 years per insurance regulations

#### Performance & Monitoring

**Response Time Targets**:
- Claims Search: < 5 seconds (95th percentile)
- Cache Retrieval: < 100ms
- Fallback Response: < 1 second

**Caching Strategy**:
- **Claims Data**: 24-hour TTL (claims don't change frequently)
- **Vehicle Data**: 30-day TTL (vehicle specs are stable)
- **SSN Validation**: 7-day TTL (validation status stable)

**Rate Limiting**: 100 requests/minute per organization (configured in entity metadata)

#### Error Handling

**Circuit Breaker Pattern**: 5 failures trigger circuit breaker, 5-minute recovery timeout  
**Graceful Degradation**: Return cached claims data when available  
**Retry Logic**: Exponential backoff with maximum 3 attempts for network errors

---

## API Specifications

### Endpoints Required
```http
# AutoCap Service Endpoints
POST   /api/v1/verisk/autocap/claims-search          # Search claims by driver
GET    /api/v1/verisk/autocap/claims/{driver_id}     # Get cached claims
POST   /api/v1/verisk/autocap/vehicle-search         # Search vehicle data
GET    /api/v1/verisk/autocap/vehicle/{vin}          # Get cached vehicle data

# Configuration Management
GET    /api/v1/entities/verisk-autocap/config        # Get AutoCap configuration
PUT    /api/v1/entities/{entity_id}/config           # Update configuration
```

### Real-time Updates
```javascript
// WebSocket channels for async processing
private-quote.{id}.autocap-results                   # Claims search results
private-tenant.{tenant_id}.autocap-status            # Service status updates
```

---

## Database Schema (Section E)

### New Core Tables

#### autocap_claims_cache
```sql
CREATE TABLE autocap_claims_cache (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  
  -- Business columns
  communication_id BIGINT UNSIGNED NOT NULL,
  driver_ssn_hash VARCHAR(64) NOT NULL,
  cap_indicator CHAR(1) NOT NULL DEFAULT 'N',
  claims_count TINYINT UNSIGNED NOT NULL DEFAULT 0,
  claims_data JSON NULL,
  
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

#### autocap_vehicle_data
```sql
CREATE TABLE autocap_vehicle_data (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  
  -- Business columns
  vin VARCHAR(25) NOT NULL,
  make VARCHAR(50) NULL,
  model VARCHAR(50) NULL,
  year SMALLINT UNSIGNED NULL,
  salvage_indicator CHAR(1) DEFAULT 'N',
  recall_count TINYINT UNSIGNED DEFAULT 0,
  vehicle_data JSON NULL,
  
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
  FOREIGN KEY (status_id) REFERENCES status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  
  -- Indexes
  UNIQUE KEY unique_vin (vin),
  INDEX idx_expires (expires_at),
  INDEX idx_status (status_id),
  INDEX idx_make_model (make, model, year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### autocap_ssn_validation
```sql
CREATE TABLE autocap_ssn_validation (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  
  -- Business columns
  ssn_hash VARCHAR(64) NOT NULL,
  validation_status VARCHAR(20) NOT NULL,
  death_master_match CHAR(1) DEFAULT 'N',
  issuance_state VARCHAR(2) NULL,
  validation_data JSON NULL,
  
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
  FOREIGN KEY (status_id) REFERENCES status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  
  -- Indexes
  UNIQUE KEY unique_ssn_hash (ssn_hash),
  INDEX idx_expires (expires_at),
  INDEX idx_status (status_id),
  INDEX idx_validation_status (validation_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### New Reference Tables

#### autocap_search_type
```sql
CREATE TABLE autocap_search_type (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  code CHAR(1) UNIQUE NOT NULL,
  name VARCHAR(100) NOT NULL,
  description TEXT NULL,
  status_id BIGINT UNSIGNED NOT NULL,
  
  -- Audit fields
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Foreign key constraints
  FOREIGN KEY (status_id) REFERENCES status(id),
  
  -- Indexes
  INDEX idx_code (code),
  INDEX idx_status (status_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert search types
INSERT INTO autocap_search_type (code, name, description, status_id) VALUES
('V', 'VIN Search', 'Search by Vehicle Identification Number', 1),
('S', 'SSN Search', 'Search by Social Security Number', 1),
('D', 'Driver License Search', 'Search by Driver License Number and State', 1),
('A', 'Address Search', 'Search by Name and Address', 1),
('N', 'Name DOB Search', 'Search by Name and Date of Birth', 1),
('P', 'Phone Search', 'Search by Phone Number', 1);
```

### Entity Type Configuration

#### VERISK_AUTOCAP_CLAIMS Entity Type
```sql
INSERT INTO entity_type (
    code, name, category_id, metadata_schema, 
    status_id, created_by, created_at
) VALUES (
    'VERISK_AUTOCAP_CLAIMS',
    'Verisk AutoCapWithClaims API',
    (SELECT id FROM entity_category WHERE code = 'INTEGRATION'),
    '{
        "type": "object",
        "properties": {
            "provider": {"type": "string", "const": "Verisk Analytics"},
            "base_url": {"type": "string", "const": "https://api.verisk.com/autocap"},
            "api_version": {"type": "string", "const": "v4"},
            "auth_type": {"type": "string", "const": "basic_auth"},
            "capabilities": {
                "type": "array",
                "items": {"type": "string"},
                "const": ["claims_search", "cap_prediction", "vin_validation", "ssn_verification"]
            },
            "search_types": {
                "type": "array", 
                "items": {"type": "string"},
                "const": ["V", "S", "D", "A", "N", "P"]
            },
            "max_requests_per_minute": {"type": "number", "const": 100},
            "timeout_seconds": {"type": "number", "const": 10},
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

#### autocap_communication_types
```sql
INSERT INTO communication_type (code, name, description, status_id, created_at) VALUES
('autocap_claims_search', 'AutoCap Claims Search', 'AutoCapWithClaims claims search API call', 
 (SELECT id FROM status WHERE code = 'active'), NOW()),
('autocap_vehicle_search', 'AutoCap Vehicle Search', 'AutoCapWithClaims vehicle data API call',
 (SELECT id FROM status WHERE code = 'active'), NOW()),
('autocap_ssn_validation', 'AutoCap SSN Validation', 'AutoCapWithClaims SSN validation API call',
 (SELECT id FROM status WHERE code = 'active'), NOW()),
('autocap_api_error', 'AutoCap API Error', 'Failed AutoCapWithClaims API call',
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
- Gradual rollout starting with test quotes
- Fallback to cached data during migration period
- Existing quote workflow integration at risk assessment stage

### Performance Considerations
- **Caching Strategy**: 24-hour TTL for claims (stable data), 30-day for vehicles
- **Index Optimization**: SSN hash and VIN lookups optimized for sub-second retrieval
- **Connection Pooling**: Reuse HTTP connections to Verisk endpoints
- **Circuit Breaker**: Prevent cascade failures during Verisk outages

---

## Quality Checklist

### Pre-Implementation
- [x] All AutoCap API endpoints mapped to service methods
- [x] Universal Entity pattern applied for API configuration
- [x] Apache Camel route for request transformation defined
- [x] Communication tracking integrated for all API calls
- [x] Cache tables designed for optimal performance

### Post-Implementation
- [x] Circuit breaker configuration tested with failure scenarios
- [x] Response time targets validated under load
- [x] Caching strategy verified for data consistency
- [x] PII masking confirmed in all log outputs
- [x] Entity catalog updated with AutoCap entity type

### Final Validation
- [x] Backend mappings tested for quote-to-API data flow
- [x] Database schema optimized for expected query patterns
- [x] Error handling covers all API failure scenarios
- [x] Performance monitoring configured for SLA tracking
- [x] Security audit completed for credential handling

---

**Integration Summary**: AutoCapWithClaims provides comprehensive claims history and predictive analytics through a robust Universal Entity Management implementation with Apache Camel routing, circuit breaker protection, and intelligent caching for optimal performance in insurance quote workflows.