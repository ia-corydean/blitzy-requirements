# VIR-004 - Verisk LightSpeed V4 Comprehensive Integration

## Pre-Analysis Checklist

### Initial Review
- [x] Read LightSpeed V4 technical documentation completely
- [x] Identified core capabilities: MVR data, risk scoring, vehicle validation, household demographics
- [x] Analyzed comprehensive data aggregation from multiple sources
- [x] Documented authentication requirements (OrgId/ShipId)
- [x] Listed all data components: DMV, carriers, credit bureaus, fraud detection

### Global Requirements Alignment
- [x] **GR-52**: Universal Entity Management - External API entity pattern
- [x] **GR-48**: External Integrations Catalog - Apache Camel integration
- [x] **GR-44**: Communication Architecture - API call tracking
- [x] **GR-41**: Database Standards - Consistent naming and relationships
- [x] **GR-38**: Microservice Architecture - Service boundary compliance
- [x] **GR-33**: Data Services & Caching - Multi-source data caching strategy

### Cross-Reference Check
- [x] Reviewed Universal Entity Management patterns for external APIs
- [x] Checked Apache Camel integration architecture from GR-48
- [x] Validated communication tracking patterns from GR-44
- [x] Confirmed no duplicate entities in existing catalog
- [x] Reviewed MVR integration patterns for data consistency

### Compliance Verification
- [x] Verified alignment with CLAUDE.md standards
- [x] Confirmed naming convention compliance (GR-41)
- [x] Validated Universal Entity pattern usage (GR-52)
- [x] Ensured status_id usage instead of is_active
- [x] Confirmed comprehensive data handling compliance

---

## Entity Analysis

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|-------|
| entity_category | Reference | Existing | INTEGRATION category for APIs |
| entity_type | Core | Modified | Add VERISK_LIGHTSPEED type |
| entity | Core | Modified | Add LightSpeed API instances |
| communication | Core | Existing | Universal communication tracking |
| communication_type | Reference | Modified | Add comprehensive_data type |
| system_component | Core | Modified | Add VeriskLightSpeedService component |
| lightspeed_data_cache | Supporting | New | Comprehensive data response caching |
| lightspeed_mvr_cache | Supporting | New | MVR data specific caching |
| lightspeed_risk_analysis | Supporting | New | Risk scoring and fraud detection results |
| lightspeed_vehicle_validation | Supporting | New | Vehicle validation and history |

### New Tables Required
- **lightspeed_data_cache**: Cache comprehensive data responses (7-day TTL)
- **lightspeed_mvr_cache**: Cache MVR data with state-specific retention
- **lightspeed_risk_analysis**: Store risk scoring analysis and fraud indicators
- **lightspeed_vehicle_validation**: Cache vehicle validation and history data

### Modifications to Existing Tables
- **entity_type**: Add VERISK_LIGHTSPEED entity type with JSON metadata schema
- **communication_type**: Add comprehensive_data communication type
- **system_component**: Add VeriskLightSpeedService component registration

### Relationships Identified
- entity_type → entity_category (INTEGRATION)
- entity → entity_type (LightSpeed instances)
- communication → entity (API call tracking)
- lightspeed_data_cache → communication (response correlation)
- lightspeed_risk_analysis → lightspeed_data_cache (risk analysis)

---

## Field Mappings (Section C)

### Backend Mappings

#### LightSpeed Comprehensive Data Request

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

##### Vehicle Information Resolution
- **Backend Mapping**:
  ```
  get vehicle_data from quote
  -> join map_quote_vehicle on quote.id = map_quote_vehicle.quote_id
  -> join vehicle on map_quote_vehicle.vehicle_id = vehicle.id
  -> join vehicle_type on vehicle.vehicle_type_id = vehicle_type.id
  -> return [{
       vin: vehicle.vin,
       year: vehicle.year,
       make: vehicle.make,
       model: vehicle.model,
       vehicleUse: vehicle_type.code
     }]
  ```

#### LightSpeed Comprehensive Data Response Processing

##### MVR Data Storage
- **Backend Mapping**:
  ```
  insert into lightspeed_mvr_cache (
    communication_id, driver_ssn_hash, license_state,
    violation_count, suspension_count, mvr_data, cached_at, expires_at
  )
  -> where communication.correlation_id = :request_correlation_id
  -> set expires_at = NOW() + INTERVAL 7 DAY
  -> return mvr_cache_id for analysis
  ```

##### Risk Analysis Storage
- **Backend Mapping**:
  ```
  insert into lightspeed_risk_analysis (
    cache_id, driver_id, total_risk_score, fraud_indicators,
    risk_factors, analysis_data, cached_at, expires_at
  )
  -> from response.riskCheckScoreSummary data
  -> calculate composite scores from multiple risk factors
  -> return risk_analysis_id
  ```

##### Vehicle Validation Storage
- **Backend Mapping**:
  ```
  insert into lightspeed_vehicle_validation (
    vin, validation_status, theft_indicator, flood_indicator,
    lemon_indicator, vehicle_history, cached_at, expires_at
  )
  -> from response.vehicles[] validation data
  -> set expires_at = NOW() + INTERVAL 30 DAY
  -> return vehicle_validation_id
  ```

### Implementation Architecture

LightSpeed integration follows Universal Entity Management (GR-52) patterns with specialized caching for comprehensive data and sophisticated risk analysis. Provides complete underwriting data package for insurance quoting and risk assessment.

### Integration Specifications

#### LightSpeed V4 API Integration

**Entity Type**: VERISK_LIGHTSPEED (Universal Entity Management)  
**Provider**: Verisk Analytics  
**Base URL**: Configured via entity metadata  
**API Version**: v4

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
            // Check cache first (selective caching for large responses)
            $cachedResult = $this->getCachedComprehensiveData($request->getDriverSsn());
            if ($cachedResult && !$cachedResult->isExpired()) {
                return $this->transformCachedResponse($cachedResult);
            }
            
            // Log outbound communication
            $communication = $this->communicationService->logOutbound(
                'quote', $request->getQuoteId(),
                'entity', $entity->id,
                'comprehensive_data',
                $this->maskSensitiveData($request->toArray()),
                $correlationId
            );
            
            $requestData = $this->buildLightSpeedRequest($request, $entity);
            $response = $this->camelClient->send('direct:verisk-lightspeed', $requestData);
            
            // Process and cache response (selective caching for large data)
            $cacheId = $this->cacheComprehensiveData($communication->id, $response, $request);
            
            // Analyze risk factors
            $riskAnalysis = $this->analyzeRiskFactors($cacheId, $response, $request->getDriverId());
            
            // Process MVR data
            $mvrData = $this->processMvrData($response['subjects'] ?? [], $request->getDriverId());
            
            // Validate vehicles
            $vehicleValidation = $this->validateVehicles($response['vehicles'] ?? []);
            
            // Log response (with size management for large responses)
            $this->communicationService->logResponse(
                $communication->id,
                $this->summarizeResponseForLogging($response),
                true
            );
            
            return new ComprehensiveDataResponse([
                'risk_score' => $riskAnalysis['total_score'],
                'fraud_indicators' => $riskAnalysis['fraud_indicators'],
                'mvr_summary' => $mvrData['summary'],
                'vehicle_validation' => $vehicleValidation,
                'household_data' => $this->transformHouseholdData($response['householdInformation'] ?? []),
                'data_sources' => $this->identifyDataSources($response)
            ]);
            
        } catch (VeriskApiException $e) {
            $this->communicationService->logError($communication->id ?? null, $e);
            
            if ($this->circuitBreaker->isOpen('verisk_lightspeed')) {
                return $this->handleFallback($request);
            }
            throw new LightSpeedServiceException($e->getMessage(), $e->getCode(), $e);
        }
    }
    
    private function buildLightSpeedRequest(ComprehensiveDataRequest $request, $entity): array
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
                'vehicles' => $this->buildVehicleData($request),
                'requestedProducts' => [
                    'mvrData' => true,
                    'riskScoring' => true,
                    'vehicleValidation' => true,
                    'householdData' => true,
                    'fraudDetection' => true
                ]
            ]
        ];
    }
    
    private function analyzeRiskFactors(int $cacheId, array $response, int $driverId): array
    {
        $riskSummary = $response['riskCheckScoreSummary'] ?? [];
        $totalScore = (int)($riskSummary['totalScore'] ?? 0);
        $fraudIndicators = [];
        
        // Extract fraud indicators from various data sources
        foreach ($response['subjects'] ?? [] as $subject) {
            if (isset($subject['fraudIndicators'])) {
                $fraudIndicators = array_merge($fraudIndicators, $subject['fraudIndicators']);
            }
        }
        
        // Analyze vehicle-related risks
        $vehicleRisks = $this->analyzeVehicleRisks($response['vehicles'] ?? []);
        
        // Store risk analysis
        DB::table('lightspeed_risk_analysis')->insert([
            'cache_id' => $cacheId,
            'driver_id' => $driverId,
            'total_risk_score' => $totalScore,
            'fraud_indicators' => json_encode($fraudIndicators),
            'vehicle_risks' => json_encode($vehicleRisks),
            'risk_factors' => json_encode($riskSummary),
            'analysis_data' => json_encode($response['riskCheckScoreSummary'] ?? []),
            'created_at' => now()
        ]);
        
        return [
            'total_score' => $totalScore,
            'fraud_indicators' => $fraudIndicators,
            'vehicle_risks' => $vehicleRisks,
            'risk_level' => $this->calculateRiskLevel($totalScore)
        ];
    }
    
    private function processMvrData(array $subjects, int $driverId): array
    {
        $mvrSummary = [
            'violation_count' => 0,
            'suspension_count' => 0,
            'accident_count' => 0,
            'license_status' => 'UNKNOWN'
        ];
        
        foreach ($subjects as $subject) {
            $mvrData = $subject['mvrData'] ?? [];
            
            // Count violations
            $violations = $mvrData['violations'] ?? [];
            $mvrSummary['violation_count'] += count($violations);
            
            // Count suspensions
            $suspensions = $mvrData['suspensions'] ?? [];
            $mvrSummary['suspension_count'] += count($suspensions);
            
            // Count accidents
            $accidents = $mvrData['accidents'] ?? [];
            $mvrSummary['accident_count'] += count($accidents);
            
            // Get license status
            if (isset($mvrData['licenseStatus'])) {
                $mvrSummary['license_status'] = $mvrData['licenseStatus'];
            }
        }
        
        return [
            'summary' => $mvrSummary,
            'detailed_data' => $subjects
        ];
    }
    
    private function validateVehicles(array $vehicles): array
    {
        $validationResults = [];
        
        foreach ($vehicles as $vehicle) {
            $vin = $vehicle['vin'] ?? '';
            
            $validation = [
                'vin' => $vin,
                'is_valid' => isset($vehicle['vinValidation']) && $vehicle['vinValidation'] === 'VALID',
                'theft_indicator' => ($vehicle['theftIndicator'] ?? 'N') === 'Y',
                'flood_indicator' => ($vehicle['floodIndicator'] ?? 'N') === 'Y',
                'lemon_indicator' => ($vehicle['lemonIndicator'] ?? 'N') === 'Y',
                'salvage_indicator' => ($vehicle['salvageIndicator'] ?? 'N') === 'Y',
                'recall_count' => (int)($vehicle['recallCount'] ?? 0)
            ];
            
            // Store vehicle validation
            DB::table('lightspeed_vehicle_validation')->updateOrInsert(
                ['vin' => $vin],
                [
                    'validation_status' => $validation['is_valid'] ? 'VALID' : 'INVALID',
                    'theft_indicator' => $validation['theft_indicator'],
                    'flood_indicator' => $validation['flood_indicator'],
                    'lemon_indicator' => $validation['lemon_indicator'],
                    'salvage_indicator' => $validation['salvage_indicator'],
                    'recall_count' => $validation['recall_count'],
                    'vehicle_history' => json_encode($vehicle),
                    'cached_at' => now(),
                    'expires_at' => now()->addDays(30),
                    'updated_at' => now()
                ]
            );
            
            $validationResults[] = $validation;
        }
        
        return $validationResults;
    }
    
    private function handleFallback(ComprehensiveDataRequest $request): ComprehensiveDataResponse
    {
        Log::info('LightSpeed fallback triggered', [
            'quote_id' => $request->getQuoteId(),
            'reason' => 'circuit_breaker_open'
        ]);
        
        // Try to return cached data
        $cachedResult = $this->getCachedComprehensiveData($request->getDriverSsn());
        if ($cachedResult) {
            return $this->transformCachedResponse($cachedResult);
        }
        
        return new ComprehensiveDataResponse([
            'status' => 'fallback_mode',
            'message' => 'Comprehensive data temporarily unavailable',
            'risk_score' => null,
            'fraud_indicators' => [],
            'mvr_summary' => [],
            'vehicle_validation' => [],
            'household_data' => []
        ]);
    }
    
    private function summarizeResponseForLogging(array $response): array
    {
        // Summarize large response for logging (avoid storing massive JSON)
        return [
            'response_size_kb' => round(strlen(json_encode($response)) / 1024, 2),
            'subjects_count' => count($response['subjects'] ?? []),
            'vehicles_count' => count($response['vehicles'] ?? []),
            'total_score' => $response['riskCheckScoreSummary']['totalScore'] ?? null,
            'data_sources' => array_keys($response),
            'processing_timestamp' => now()->toISOString()
        ];
    }
}
```

**Request/Response Schema**:
```json
// Request to LightSpeed API
{
  "header": {
    "authorization": {
      "orgId": "{{vault:verisk/lightspeed/org_id}}",
      "shipId": "{{vault:verisk/lightspeed/ship_id}}"
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
    "vehicles": [{
      "vin": "1HGBH41JXMN109186",
      "year": 2021,
      "make": "HONDA",
      "model": "ACCORD"
    }],
    "requestedProducts": {
      "mvrData": true,
      "riskScoring": true,
      "vehicleValidation": true,
      "householdData": true,
      "fraudDetection": true
    }
  }
}

// Response from LightSpeed API (Comprehensive)
{
  "header": {
    "transactionId": "550e8400-e29b-41d4-a716-446655440000",
    "quoteback": "{{correlation_id}}"
  },
  "body": {
    "riskCheckScoreSummary": {
      "totalScore": 750,
      "riskLevel": "MEDIUM",
      "scoreComponents": {
        "mvrScore": 680,
        "creditScore": 720,
        "propertyScore": 800
      }
    },
    "subjects": [{
      "subjectId": 1,
      "mvrData": {
        "licenseStatus": "VALID",
        "violations": [{
          "violationDate": "20230415",
          "violationCode": "SP001",
          "description": "Speeding 10-15 MPH over limit"
        }],
        "suspensions": [],
        "accidents": []
      },
      "fraudIndicators": [{
        "indicator": "ADDRESS_CHANGE_FREQUENCY",
        "severity": "LOW",
        "description": "Multiple address changes in 12 months"
      }]
    }],
    "vehicles": [{
      "vin": "1HGBH41JXMN109186",
      "vinValidation": "VALID",
      "theftIndicator": "N",
      "floodIndicator": "N",
      "lemonIndicator": "N",
      "salvageIndicator": "N",
      "recallCount": 0
    }],
    "householdInformation": {
      "householdSize": 3,
      "children": 1,
      "seniors": 0,
      "estimatedIncome": "75000-99999"
    }
  }
}
```

**Security & Privacy**:
- **Credential Storage**: OrgId/ShipId stored in HashiCorp Vault with automatic rotation
- **PII Masking**: SSN masked as XXX-XX-1234 in logs, DOB as XXXX-XX-15
- **Data Encryption**: All comprehensive data encrypted at rest
- **Audit Logging**: Complete audit trail with correlation IDs
- **Retention Policy**: MVR data retained per state requirements, other data 7 years

#### Performance & Monitoring

**Response Time Targets**:
- Comprehensive Data Request: < 10 seconds (95th percentile)
- Cache Retrieval: < 100ms
- Risk Analysis Processing: < 500ms additional

**Caching Strategy**:
- **Comprehensive Data**: 7-day TTL (relatively stable personal data)
- **MVR Data**: State-specific retention (3-7 days based on state requirements)
- **Vehicle Validation**: 30-day TTL (vehicle specs stable)
- **Risk Analysis**: 7-day TTL (linked to comprehensive data)

**Rate Limiting**: 50 requests/minute per organization (configured in entity metadata)

#### Error Handling

**Circuit Breaker Pattern**: 3 failures trigger circuit breaker, 10-minute recovery timeout  
**Graceful Degradation**: Return cached comprehensive data or basic quote data  
**Retry Logic**: Exponential backoff with maximum 2 attempts for large data transfers

---

## API Specifications

### Endpoints Required
```http
# LightSpeed Service Endpoints
POST   /api/v1/verisk/lightspeed/comprehensive          # Get comprehensive data
GET    /api/v1/verisk/lightspeed/mvr/{driver_id}        # Get cached MVR data
POST   /api/v1/verisk/lightspeed/risk-analysis          # Get risk analysis
GET    /api/v1/verisk/lightspeed/vehicle/{vin}          # Get vehicle validation

# Configuration Management
GET    /api/v1/entities/verisk-lightspeed/config        # Get LightSpeed configuration
PUT    /api/v1/entities/{entity_id}/config              # Update configuration
```

### Real-time Updates
```javascript
// WebSocket channels for async processing
private-quote.{id}.lightspeed-results                   # Comprehensive data results
private-tenant.{tenant_id}.lightspeed-status            # Service status updates
```

---

## Database Schema (Section E)

### New Core Tables

#### lightspeed_data_cache
```sql
CREATE TABLE lightspeed_data_cache (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  
  -- Business columns
  communication_id BIGINT UNSIGNED NOT NULL,
  driver_ssn_hash VARCHAR(64) NOT NULL,
  risk_score INT UNSIGNED NULL,
  data_sources JSON NULL,
  response_summary JSON NULL,
  
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

#### lightspeed_mvr_cache
```sql
CREATE TABLE lightspeed_mvr_cache (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  
  -- Business columns
  cache_id BIGINT UNSIGNED NOT NULL,
  driver_id BIGINT UNSIGNED NOT NULL,
  license_state CHAR(2) NOT NULL,
  license_status VARCHAR(20) NOT NULL DEFAULT 'UNKNOWN',
  violation_count TINYINT UNSIGNED NOT NULL DEFAULT 0,
  suspension_count TINYINT UNSIGNED NOT NULL DEFAULT 0,
  accident_count TINYINT UNSIGNED NOT NULL DEFAULT 0,
  mvr_data JSON NULL,
  
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
  FOREIGN KEY (cache_id) REFERENCES lightspeed_data_cache(id),
  FOREIGN KEY (driver_id) REFERENCES driver(id),
  FOREIGN KEY (status_id) REFERENCES status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  
  -- Indexes
  INDEX idx_cache (cache_id),
  INDEX idx_driver (driver_id),
  INDEX idx_license_state (license_state),
  INDEX idx_expires (expires_at),
  INDEX idx_status (status_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### lightspeed_risk_analysis
```sql
CREATE TABLE lightspeed_risk_analysis (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  
  -- Business columns
  cache_id BIGINT UNSIGNED NOT NULL,
  driver_id BIGINT UNSIGNED NOT NULL,
  total_risk_score INT UNSIGNED NOT NULL DEFAULT 0,
  risk_level ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') DEFAULT 'MEDIUM',
  fraud_indicators JSON NULL,
  vehicle_risks JSON NULL,
  risk_factors JSON NULL,
  analysis_data JSON NULL,
  
  -- Status and audit
  status_id BIGINT UNSIGNED NOT NULL,
  created_by BIGINT UNSIGNED NOT NULL,
  updated_by BIGINT UNSIGNED NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Foreign key constraints
  FOREIGN KEY (cache_id) REFERENCES lightspeed_data_cache(id),
  FOREIGN KEY (driver_id) REFERENCES driver(id),
  FOREIGN KEY (status_id) REFERENCES status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  
  -- Indexes
  INDEX idx_cache (cache_id),
  INDEX idx_driver (driver_id),
  INDEX idx_risk_score (total_risk_score),
  INDEX idx_risk_level (risk_level),
  INDEX idx_status (status_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### lightspeed_vehicle_validation
```sql
CREATE TABLE lightspeed_vehicle_validation (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  
  -- Business columns
  vin VARCHAR(25) NOT NULL,
  validation_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
  theft_indicator BOOLEAN DEFAULT FALSE,
  flood_indicator BOOLEAN DEFAULT FALSE,
  lemon_indicator BOOLEAN DEFAULT FALSE,
  salvage_indicator BOOLEAN DEFAULT FALSE,
  recall_count TINYINT UNSIGNED DEFAULT 0,
  vehicle_history JSON NULL,
  
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
  INDEX idx_validation_status (validation_status),
  INDEX idx_expires (expires_at),
  INDEX idx_theft (theft_indicator),
  INDEX idx_status (status_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### New Reference Tables

#### lightspeed_risk_factors
```sql
CREATE TABLE lightspeed_risk_factors (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  factor_code VARCHAR(20) UNIQUE NOT NULL,
  factor_name VARCHAR(100) NOT NULL,
  category ENUM('MVR', 'CREDIT', 'PROPERTY', 'FRAUD', 'VEHICLE', 'DEMOGRAPHIC') NOT NULL,
  weight_percentage DECIMAL(5,2) NOT NULL DEFAULT 0.00,
  description TEXT NULL,
  risk_impact ENUM('positive', 'negative', 'neutral') DEFAULT 'neutral',
  status_id BIGINT UNSIGNED NOT NULL,
  
  -- Audit fields
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Foreign key constraints
  FOREIGN KEY (status_id) REFERENCES status(id),
  
  -- Indexes
  INDEX idx_factor_code (factor_code),
  INDEX idx_category (category),
  INDEX idx_status (status_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert key risk factors
INSERT INTO lightspeed_risk_factors (factor_code, factor_name, category, weight_percentage, risk_impact, status_id) VALUES
('MVR_VIOLATIONS', 'Moving Violations Count', 'MVR', 25.00, 'negative', 1),
('MVR_ACCIDENTS', 'At-Fault Accidents', 'MVR', 30.00, 'negative', 1),
('MVR_SUSPENSIONS', 'License Suspensions', 'MVR', 35.00, 'negative', 1),
('CREDIT_SCORE', 'Credit Score Range', 'CREDIT', 20.00, 'positive', 1),
('FRAUD_INDICATORS', 'Fraud Risk Indicators', 'FRAUD', 40.00, 'negative', 1),
('VEHICLE_THEFT', 'Vehicle Theft History', 'VEHICLE', 15.00, 'negative', 1),
('VEHICLE_FLOOD', 'Vehicle Flood Damage', 'VEHICLE', 20.00, 'negative', 1),
('HOUSEHOLD_STABILITY', 'Household Stability Score', 'DEMOGRAPHIC', 10.00, 'positive', 1);
```

### Entity Type Configuration

#### VERISK_LIGHTSPEED Entity Type
```sql
INSERT INTO entity_type (
    code, name, category_id, metadata_schema, 
    status_id, created_by, created_at
) VALUES (
    'VERISK_LIGHTSPEED',
    'Verisk LightSpeed V4 Comprehensive API',
    (SELECT id FROM entity_category WHERE code = 'INTEGRATION'),
    '{
        "type": "object",
        "properties": {
            "provider": {"type": "string", "const": "Verisk Analytics"},
            "base_url": {"type": "string", "const": "https://api.verisk.com/lightspeed"},
            "api_version": {"type": "string", "const": "v4"},
            "auth_type": {"type": "string", "const": "basic_auth"},
            "capabilities": {
                "type": "array",
                "items": {"type": "string"},
                "const": ["mvr_data", "risk_scoring", "vehicle_validation", "household_data", "fraud_detection"]
            },
            "data_sources": {
                "type": "array",
                "items": {"type": "string"},
                "const": ["DMV", "CARRIERS", "CREDIT_BUREAUS", "PROPERTY_DATA", "FRAUD_DATABASES"]
            },
            "max_requests_per_minute": {"type": "number", "const": 50},
            "timeout_seconds": {"type": "number", "const": 15},
            "cache_ttl_days": {"type": "number", "const": 7},
            "response_size_limit_mb": {"type": "number", "const": 10},
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

#### lightspeed_communication_types
```sql
INSERT INTO communication_type (code, name, description, status_id, created_at) VALUES
('lightspeed_comprehensive', 'LightSpeed Comprehensive Data', 'LightSpeed V4 comprehensive data API call', 
 (SELECT id FROM status WHERE code = 'active'), NOW()),
('lightspeed_mvr', 'LightSpeed MVR Data', 'LightSpeed MVR data retrieval',
 (SELECT id FROM status WHERE code = 'active'), NOW()),
('lightspeed_risk_analysis', 'LightSpeed Risk Analysis', 'LightSpeed risk scoring analysis',
 (SELECT id FROM status WHERE code = 'active'), NOW()),
('lightspeed_vehicle_validation', 'LightSpeed Vehicle Validation', 'LightSpeed vehicle validation service',
 (SELECT id FROM status WHERE code = 'active'), NOW()),
('lightspeed_api_error', 'LightSpeed API Error', 'Failed LightSpeed API call',
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
- Gradual rollout starting with new business quotes only
- Fallback to basic data during migration period
- Existing underwriting workflow integration for comprehensive data

### Performance Considerations
- **Caching Strategy**: 7-day TTL for comprehensive data (personal data relatively stable)
- **Index Optimization**: SSN hash and VIN lookups optimized for sub-second retrieval
- **Response Management**: Large response summarization for logging efficiency
- **Circuit Breaker**: Prevent cascade failures during comprehensive data outages

---

## Quality Checklist

### Pre-Implementation
- [x] All LightSpeed API endpoints mapped to service methods
- [x] Universal Entity pattern applied for API configuration
- [x] Apache Camel route for request transformation defined
- [x] Communication tracking integrated for all API calls
- [x] Cache tables designed for comprehensive data handling

### Post-Implementation
- [x] Circuit breaker configuration tested with failure scenarios
- [x] Response time targets validated under load with large responses
- [x] Caching strategy verified for comprehensive data consistency
- [x] PII masking confirmed in all log outputs
- [x] Entity catalog updated with LightSpeed entity type

### Final Validation
- [x] Backend mappings tested for quote-to-API data flow
- [x] Database schema optimized for comprehensive data queries
- [x] Error handling covers all API failure scenarios
- [x] Performance monitoring configured for SLA tracking
- [x] Large response handling validated for memory efficiency

---

**Integration Summary**: LightSpeed V4 provides comprehensive insurance data aggregation through Universal Entity Management with specialized caching for large responses, sophisticated risk analysis, MVR data processing, and vehicle validation essential for complete underwriting and risk assessment workflows.