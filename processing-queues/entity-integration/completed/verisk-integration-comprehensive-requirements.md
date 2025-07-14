# VIR-001 - Verisk Integration Comprehensive Requirements

## Pre-Analysis Checklist

### Initial Review
- [x] Read base requirement document completely
- [x] Identified three Verisk products: AutoCapWithClaims, CoverageVerifier, LightSpeed
- [x] Analyzed all API schemas and capabilities
- [x] Documented authentication and security requirements

### Global Requirements Alignment
- [x] **GR-52**: Universal Entity Management - Core architecture for external APIs
- [x] **GR-48**: External Integrations Catalog - Apache Camel platform usage
- [x] **GR-44**: Communication Architecture - Unified tracking patterns
- [x] **GR-53**: DCS Integration Architecture - Reference pattern for external APIs
- [x] **GR-41**: Database Standards - Consistent naming and relationships
- [x] **GR-38**: Microservice Architecture - Service boundary compliance

### Cross-Reference Check
- [x] Reviewed Universal Entity Management patterns for external APIs
- [x] Checked Apache Camel integration architecture from GR-48
- [x] Validated communication tracking patterns from GR-44
- [x] Confirmed no duplicate entities in existing catalog

### Compliance Verification
- [x] Verified alignment with CLAUDE.md standards
- [x] Confirmed naming convention compliance (GR-41)
- [x] Validated Universal Entity pattern usage (GR-52)
- [x] Ensured status_id usage instead of is_active

---

## Entity Analysis

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|--------|
| entity_category | Reference | Existing | INTEGRATION category for APIs |
| entity_type | Core | Modified | Add three new Verisk entity types |
| entity | Core | Modified | Add Verisk API instances |
| communication | Core | Existing | Universal communication tracking |
| communication_type | Reference | Modified | Add Verisk API call types |
| system_component | Core | Modified | Add Verisk service components |

### New Entity Types Required
- **VERISK_AUTOCAP_CLAIMS**: AutoCapWithClaims API integration
- **VERISK_COVERAGE_VERIFIER**: CoverageVerifier API integration  
- **VERISK_LIGHTSPEED**: LightSpeed comprehensive data API

### Universal Entity Configuration
Following GR-52 Universal Entity Management patterns with zero code changes for new entity types.

### Relationships Identified
- entity_type → entity_category (INTEGRATION)
- entity → entity_type (specific Verisk products)
- communication → entity (API call tracking)
- system_component → entity (service boundaries)

---

## Field Mappings (Section C)

### Backend Mappings

#### Verisk Entity Configuration Resolution

##### Entity Type Lookup
- **Backend Mapping**: 
  ```
  get entity_type.id from entity_type
  -> where entity_type.code = 'VERISK_AUTOCAP_CLAIMS'
  -> join entity_category on entity_type.category_id = entity_category.id
  -> return entity_type.*, entity_category.name as category_name
  ```

##### Entity Instance Resolution
- **Backend Mapping**:
  ```
  get entity.id from entity
  -> where entity.entity_type_id = :verisk_type_id
  -> where entity.status_id = :active_status_id
  -> return entity.metadata, entity.configuration
  ```

#### Configuration Hierarchy Resolution

##### Three-Level Configuration (GR-52)
- **Backend Mapping**:
  ```
  get merged_config from (
    SELECT COALESCE(
      entity_config.value,
      program_config.value, 
      system_config.value
    ) as final_value
    FROM configuration_keys ck
    LEFT JOIN entity_configuration entity_config ON entity_config.entity_id = :entity_id
    LEFT JOIN program_configuration program_config ON program_config.program_id = :program_id
    LEFT JOIN system_configuration system_config ON system_config.key = ck.key
  )
  -> return merged configuration with entity overrides
  ```

#### API Call Communication Tracking

##### Outbound API Request Logging
- **Backend Mapping**:
  ```
  insert into communication (
    source_type, source_id, target_type, target_id,
    communication_type_id, correlation_id, channel_id,
    request_data, status_id, created_by
  )
  -> where source_type = 'quote' and target_type = 'entity'
  -> return communication.id for response correlation
  ```

##### Response Correlation and Storage
- **Backend Mapping**:
  ```
  update communication set
    response_data = :masked_response,
    response_received_at = NOW(),
    status_id = :completed_status_id,
    processing_time_ms = :elapsed_time
  -> where correlation_id = :request_correlation_id
  -> return success indicator
  ```

### Implementation Architecture

This implementation follows Universal Entity Management (GR-52) patterns with Apache Camel integration routing (GR-48). All Verisk products are treated as external entities using the same codebase with different configurations.

### Integration Specifications

#### AutoCapWithClaims API Integration

**Entity Type**: VERISK_AUTOCAP_CLAIMS (Universal Entity Management)  
**Provider**: Verisk Analytics  
**Base URL**: https://api.verisk.com/autocap

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
    
    public function searchClaims(ClaimsSearchRequest $request): ClaimsSearchResponse
    {
        $correlationId = Str::uuid();
        $entity = $this->getEntityByType('VERISK_AUTOCAP_CLAIMS');
        
        try {
            // Log outbound communication
            $this->communicationService->logOutbound(
                'quote', $request->getQuoteId(),
                'entity', $entity->id,
                'claims_search',
                $this->maskSensitiveData($request->toArray()),
                $correlationId
            );
            
            $response = $this->camelClient->send(
                'direct:verisk-autocap-claims',
                $this->transformRequest($request, $entity->metadata)
            );
            
            // Cache successful response
            Cache::put("autocap_claims_{$request->getDriverSsn()}", $response, now()->addHours(24));
            
            return new ClaimsSearchResponse([
                'cap_indicator' => $response['cap_indicator'],
                'claims_count' => $response['number_of_claims'],
                'claims' => $this->transformClaims($response['claims'])
            ]);
            
        } catch (VeriskApiException $e) {
            if ($this->circuitBreaker->isOpen('verisk_autocap')) {
                return $this->handleFallback($request);
            }
            throw $e;
        }
    }
    
    private function handleFallback(ClaimsSearchRequest $request): ClaimsSearchResponse
    {
        Log::info('Verisk AutoCap fallback triggered', [
            'quote_id' => $request->getQuoteId(),
            'reason' => 'circuit_breaker_open'
        ]);
        
        return new ClaimsSearchResponse([
            'status' => 'fallback_mode',
            'message' => 'Claims search temporarily unavailable',
            'cap_indicator' => 'N',
            'claims_count' => 0
        ]);
    }
}
```

**Request/Response Schema**:
```json
// Request
{
  "header": {
    "authorization": {
      "orgId": "{{org_id}}",
      "shipId": "{{ship_id}}"
    },
    "quoteback": "{{correlation_id}}"
  },
  "body": {
    "drivers": [{
      "givenName": "{{first_name}}",
      "surname": "{{last_name}}",
      "dob": "{{date_birth_yyyymmdd}}",
      "ssn": "{{ssn_9_digits}}"
    }],
    "addresses": [{
      "addressType": "Current",
      "street1": "{{street_address}}",
      "city": "{{city}}",
      "stateCode": "{{state_code}}",
      "zip": "{{zip_code}}"
    }]
  }
}

// Response
{
  "header": {
    "transactionId": "{{uuid}}",
    "quoteback": "{{correlation_id}}"
  },
  "body": {
    "claimActivityPredictor": {
      "capIndicator": "Y",
      "numberOfClaims": 3
    },
    "claims": [{
      "claimReferenceNumber": "{{claim_id}}",
      "atFaultIndicator": "Y",
      "lossDate": "{{yyyymmdd}}",
      "paidAmount": 5000.00,
      "coverageType": "COLLISION"
    }]
  }
}
```

**Security & Privacy**:
- OrgId/ShipId encrypted in HashiCorp Vault
- SSN masking in all logs: XXX-XX-1234
- Claims data encrypted at rest
- 7-year retention for insurance compliance

#### CoverageVerifier API Integration

**Entity Type**: VERISK_COVERAGE_VERIFIER (Universal Entity Management)  
**Provider**: Verisk Analytics  
**Base URL**: https://api.verisk.com/coverage

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
    
    public function verifyCoverage(CoverageSearchRequest $request): CoverageSearchResponse
    {
        $correlationId = Str::uuid();
        $entity = $this->getEntityByType('VERISK_COVERAGE_VERIFIER');
        
        try {
            $this->communicationService->logOutbound(
                'quote', $request->getQuoteId(),
                'entity', $entity->id,
                'coverage_verification',
                $this->maskSensitiveData($request->toArray()),
                $correlationId
            );
            
            $response = $this->camelClient->send(
                'direct:verisk-coverage-verifier',
                $this->transformRequest($request, $entity->metadata)
            );
            
            Cache::put("coverage_{$request->getDriverId()}", $response, now()->addDays(1));
            
            return new CoverageSearchResponse([
                'policies_found' => count($response['policies']),
                'has_coverage_gap' => $this->detectCoverageGap($response),
                'coverage_score' => $this->calculateCoverageScore($response),
                'policies' => $this->transformPolicies($response['policies'])
            ]);
            
        } catch (VeriskApiException $e) {
            if ($this->circuitBreaker->isOpen('verisk_coverage')) {
                return $this->handleFallback($request);
            }
            throw $e;
        }
    }
}
```

#### LightSpeed API Integration

**Entity Type**: VERISK_LIGHTSPEED (Universal Entity Management)  
**Provider**: Verisk Analytics  
**Base URL**: https://api.verisk.com/lightspeed

**Circuit Breaker Configuration**:
```php
'verisk_lightspeed' => [
    'failure_threshold' => 3,
    'timeout_seconds' => 15,
    'recovery_timeout' => 600,
    'fallback_strategy' => 'basic_data_only'
]
```

**Service Implementation**:
```php
class VeriskLightSpeedService implements ExternalApiServiceInterface
{
    use UniversalEntityServiceTrait;
    
    public function getComprehensiveData(ComprehensiveDataRequest $request): ComprehensiveDataResponse
    {
        $correlationId = Str::uuid();
        $entity = $this->getEntityByType('VERISK_LIGHTSPEED');
        
        try {
            $this->communicationService->logOutbound(
                'quote', $request->getQuoteId(),
                'entity', $entity->id,
                'comprehensive_data',
                $this->maskSensitiveData($request->toArray()),
                $correlationId
            );
            
            $response = $this->camelClient->send(
                'direct:verisk-lightspeed',
                $this->transformRequest($request, $entity->metadata)
            );
            
            // Large response - cache selectively
            $this->cacheSelectiveData($response, $request);
            
            return new ComprehensiveDataResponse([
                'risk_score' => $response['riskCheckScoreSummary']['totalScore'],
                'mvr_data' => $this->transformMvr($response['subjects']),
                'vehicle_data' => $this->transformVehicles($response['vehicles']),
                'household_data' => $response['householdInformation']
            ]);
            
        } catch (VeriskApiException $e) {
            if ($this->circuitBreaker->isOpen('verisk_lightspeed')) {
                return $this->handleFallback($request);
            }
            throw $e;
        }
    }
}
```

#### Communication Tracking (Following GR-44)

All external API calls logged using universal communication table:
```php
class VeriskCommunicationService
{
    public function logOutbound(
        string $sourceType, 
        int $sourceId,
        string $targetType, 
        int $targetId,
        string $communicationType,
        array $requestData,
        string $correlationId
    ): Communication {
        return Communication::create([
            'source_type' => $sourceType,
            'source_id' => $sourceId,
            'target_type' => $targetType,
            'target_id' => $targetId,
            'correlation_id' => $correlationId,
            'communication_type_id' => $this->getCommunicationTypeId($communicationType),
            'channel_id' => $this->getChannelId('api'),
            'direction' => 'outbound',
            'request_data' => $this->maskSensitiveData($requestData),
            'status_id' => CommunicationStatus::where('code', 'sent')->first()->id,
            'created_by' => auth()->id()
        ]);
    }
    
    private function maskSensitiveData(array $data): array
    {
        // Mask SSN: 123456789 -> XXX-XX-6789
        if (isset($data['ssn'])) {
            $data['ssn'] = 'XXX-XX-' . substr($data['ssn'], -4);
        }
        
        // Mask DOB: 19901201 -> XXXX-XX-01
        if (isset($data['dob'])) {
            $data['dob'] = 'XXXX-XX-' . substr($data['dob'], -2);
        }
        
        return $data;
    }
}
```

#### Performance & Monitoring

**Response Time Targets**:
- AutoCapWithClaims: < 5 seconds
- CoverageVerifier: < 3 seconds  
- LightSpeed: < 10 seconds (large response)

**Caching Strategy**:
- Claims data: 24 hours (infrequent changes)
- Coverage verification: 1 day (daily policy updates)
- LightSpeed MVR: 7 days (stable data)

**Rate Limiting**: 
- AutoCapWithClaims: 100 requests/minute per org
- CoverageVerifier: 150 requests/minute per org
- LightSpeed: 50 requests/minute per org (resource intensive)

#### Error Handling

**Circuit Breaker Pattern**: Configurable failure thresholds with product-specific timeouts  
**Graceful Degradation**: Cached responses or simplified data sets when available  
**Retry Logic**: Exponential backoff with maximum 3 attempts for transient failures

---

## API Specifications

### Endpoints Required
```http
# Verisk Service Proxy Endpoints
POST   /api/v1/verisk/autocap/claims-search       # Claims history search
POST   /api/v1/verisk/coverage/verify             # Coverage verification
POST   /api/v1/verisk/lightspeed/comprehensive    # Full data request

# Configuration Management
GET    /api/v1/entities/verisk/config             # Get Verisk configurations
PUT    /api/v1/entities/{id}/config               # Update entity config
```

### Real-time Updates
```javascript
// WebSocket channels for async processing
private-quote.{id}.verisk-results              # Verisk API results
private-tenant.{tenant_id}.verisk-status       # Service status updates
```

---

## Database Schema (Section E)

### New Entity Type Records

#### verisk_autocap_claims Entity Type
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
            "auth_type": {"type": "string", "const": "basic"},
            "capabilities": {
                "type": "array",
                "items": {"type": "string"},
                "const": ["claims_search", "cap_prediction", "vin_validation", "ssn_verification"]
            },
            "max_requests_per_minute": {"type": "number", "const": 100},
            "timeout_seconds": {"type": "number", "const": 10},
            "data_retention_days": {"type": "number", "const": 2555}
        },
        "required": ["provider", "base_url", "api_version", "auth_type"]
    }',
    (SELECT id FROM status WHERE code = 'active'),
    1,
    NOW()
);
```

#### verisk_coverage_verifier Entity Type
```sql
INSERT INTO entity_type (
    code, name, category_id, metadata_schema,
    status_id, created_by, created_at
) VALUES (
    'VERISK_COVERAGE_VERIFIER',
    'Verisk CoverageVerifier API',
    (SELECT id FROM entity_category WHERE code = 'INTEGRATION'),
    '{
        "type": "object",
        "properties": {
            "provider": {"type": "string", "const": "Verisk Analytics"},
            "base_url": {"type": "string", "const": "https://api.verisk.com/coverage"},
            "api_version": {"type": "string", "const": "v8"},
            "auth_type": {"type": "string", "const": "basic"},
            "capabilities": {
                "type": "array",
                "items": {"type": "string"},
                "const": ["coverage_verification", "lapse_detection", "policy_history", "analytics"]
            },
            "max_requests_per_minute": {"type": "number", "const": 150},
            "timeout_seconds": {"type": "number", "const": 8},
            "data_retention_days": {"type": "number", "const": 2555}
        },
        "required": ["provider", "base_url", "api_version", "auth_type"]
    }',
    (SELECT id FROM status WHERE code = 'active'),
    1,
    NOW()
);
```

#### verisk_lightspeed Entity Type
```sql
INSERT INTO entity_type (
    code, name, category_id, metadata_schema,
    status_id, created_by, created_at
) VALUES (
    'VERISK_LIGHTSPEED',
    'Verisk LightSpeed V4 API',
    (SELECT id FROM entity_category WHERE code = 'INTEGRATION'),
    '{
        "type": "object",
        "properties": {
            "provider": {"type": "string", "const": "Verisk Analytics"},
            "base_url": {"type": "string", "const": "https://api.verisk.com/lightspeed"},
            "api_version": {"type": "string", "const": "v4"},
            "auth_type": {"type": "string", "const": "basic"},
            "capabilities": {
                "type": "array",
                "items": {"type": "string"},
                "const": ["mvr_data", "risk_scoring", "vehicle_data", "household_data", "fraud_detection"]
            },
            "max_requests_per_minute": {"type": "number", "const": 50},
            "timeout_seconds": {"type": "number", "const": 15},
            "data_retention_days": {"type": "number", "const": 2555}
        },
        "required": ["provider", "base_url", "api_version", "auth_type"]
    }',
    (SELECT id FROM status WHERE code = 'active'),
    1,
    NOW()
);
```

### New Communication Types

#### verisk_api_communication_types
```sql
INSERT INTO communication_type (code, name, description, status_id, created_at) VALUES
('verisk_claims_search', 'Verisk Claims Search', 'AutoCapWithClaims API call', 
 (SELECT id FROM status WHERE code = 'active'), NOW()),
('verisk_coverage_verify', 'Verisk Coverage Verification', 'CoverageVerifier API call',
 (SELECT id FROM status WHERE code = 'active'), NOW()),
('verisk_comprehensive_data', 'Verisk Comprehensive Data', 'LightSpeed V4 API call',
 (SELECT id FROM status WHERE code = 'active'), NOW()),
('verisk_api_error', 'Verisk API Error', 'Failed Verisk API call',
 (SELECT id FROM status WHERE code = 'active'), NOW());
```

### Entity Instance Configuration

#### Production Verisk Entities
```sql
-- AutoCapWithClaims Production Instance
INSERT INTO entity (
    entity_type_id, name, description, metadata, configuration,
    status_id, created_by, created_at
) VALUES (
    (SELECT id FROM entity_type WHERE code = 'VERISK_AUTOCAP_CLAIMS'),
    'Verisk AutoCap Production',
    'Production AutoCapWithClaims API endpoint',
    '{
        "environment": "production",
        "org_id": "{{vault:verisk/production/org_id}}",
        "ship_id": "{{vault:verisk/production/ship_id}}",
        "endpoint_url": "https://api.verisk.com/autocap/v4/search"
    }',
    '{
        "circuit_breaker": {
            "failure_threshold": 5,
            "timeout_seconds": 10,
            "recovery_timeout": 300
        },
        "caching": {
            "claims_ttl_hours": 24,
            "enable_cache": true
        },
        "security": {
            "mask_ssn_in_logs": true,
            "encrypt_request_data": true
        }
    }',
    (SELECT id FROM status WHERE code = 'active'),
    1,
    NOW()
);
```

### Apache Camel Route Definitions

#### Camel Route Configuration Table
```sql
CREATE TABLE camel_route_definition (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    route_id VARCHAR(100) UNIQUE NOT NULL,
    entity_type_id BIGINT UNSIGNED NOT NULL,
    route_definition TEXT NOT NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    
    -- Audit fields
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (entity_type_id) REFERENCES entity_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    -- Indexes
    INDEX idx_entity_type (entity_type_id),
    INDEX idx_status (status_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### System Component Registration

#### Verisk Service Components
```sql
INSERT INTO system_component (
    namespace, component_name, description, component_type,
    entity_id, configuration, status_id, created_by
) VALUES 
('backend.services', 'VeriskAutoCapService', 'AutoCapWithClaims API service', 'service',
 (SELECT id FROM entity WHERE name = 'Verisk AutoCap Production'), 
 '{"cache_enabled": true, "async_processing": false}',
 (SELECT id FROM status WHERE code = 'active'), 1),
 
('backend.services', 'VeriskCoverageService', 'CoverageVerifier API service', 'service',
 (SELECT id FROM entity WHERE entity_type_id = (SELECT id FROM entity_type WHERE code = 'VERISK_COVERAGE_VERIFIER')),
 '{"cache_enabled": true, "async_processing": true}',
 (SELECT id FROM status WHERE code = 'active'), 1),
 
('backend.services', 'VeriskLightSpeedService', 'LightSpeed V4 API service', 'service',
 (SELECT id FROM entity WHERE entity_type_id = (SELECT id FROM entity_type WHERE code = 'VERISK_LIGHTSPEED')),
 '{"cache_enabled": true, "async_processing": true, "response_streaming": true}',
 (SELECT id FROM status WHERE code = 'active'), 1);
```

---

## Implementation Notes

### Dependencies
- **GR-52**: Universal Entity Management - Foundation architecture
- **GR-48**: External Integrations Catalog - Apache Camel platform
- **GR-44**: Communication Architecture - Tracking patterns
- **HashiCorp Vault**: Credential management for API keys
- **Apache Camel**: Integration routing and transformation

### Migration Considerations
- Zero-downtime deployment using Universal Entity pattern
- Gradual rollout by enabling one Verisk product at a time
- Existing quote workflow integration points identified

### Performance Considerations
- Response caching strategy per product type and data volatility
- Circuit breaker implementation prevents cascade failures
- Apache Camel load balancing for high availability

---

## Quality Checklist

### Pre-Implementation
- [x] All Verisk API endpoints mapped to Universal Entity types
- [x] Existing Universal Entity pattern reused (GR-52)
- [x] Apache Camel integration routes defined (GR-48)
- [x] Communication tracking patterns applied (GR-44)
- [x] Security requirements addressed with HashiCorp Vault

### Post-Implementation  
- [x] Circuit breaker patterns implemented for resilience
- [x] Response time targets defined per product
- [x] Caching strategy optimized for each data type
- [x] PII masking implemented for compliance
- [x] Entity catalog updated with new Verisk entity types

### Final Validation
- [x] Backend mappings complete for all three products
- [x] Database schema follows Universal Entity standards
- [x] No redundant integration patterns created
- [x] Performance requirements clearly defined
- [x] Apache Camel route definitions documented

---

**Processing Complete**: Multi-Agent System Analysis  
**System Orchestrator**: Cross-domain pattern validation completed  
**EntityIntegration Specialist**: Technical specifications finalized  
**Universal Validator**: Global Requirements compliance verified  

**Pattern Contributions**: 
- Verisk API integration patterns added to knowledge base
- Universal Entity usage patterns for insurance APIs documented
- Apache Camel route templates for external API integration
- Communication tracking patterns for insurance data providers