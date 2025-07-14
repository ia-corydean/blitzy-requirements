# Vehicle Territory Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Vehicle Territory  
**Category**: Vehicle Factor  
**Priority**: High - Geographic risk assessment foundation  
**Implementation Complexity**: High  

### Business Requirements Summary
The Vehicle Territory factor implements risk-based pricing adjustments based on the ZIP code where vehicles are principally garaged. This factor provides coverage-specific rate multipliers for all 2,836 Texas ZIP codes across 254 counties, reflecting localized risk patterns, claims experience, and geographic characteristics that influence claim frequency and severity.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing and new Global Requirements:

#### Leverages GR-65: Rating Engine Architecture
**Integration**: Territory factor calculation within multiplicative rating engine  
**Dependencies**: RatingEngineService for ZIP code-based factor lookup and validation

#### New Requirement: GR-85: Geographic Territory Rating Standards
**Priority**: High  
**Rationale**: ZIP code-based territory rating methodology and geographic risk assessment  

**Core Components**:
- ZIP code-based territory classification and risk correlation methodology
- County-level geographic reference and cross-validation systems
- Coverage-specific territory factor assignment and application standards
- Geographic risk assessment based on claims experience and demographic patterns
- Territory boundary validation and ZIP code assignment verification
- Geographic data integrity and validation standards

#### Leverages GR-33: Data Services Architecture
**Integration**: ZIP code validation and territory data caching  
**Dependencies**: Geographic data services and territory lookup optimization

### Integration with Existing Global Requirements
- **GR-41**: Table Schema Requirements - Territory factor table structures and geographic relationships
- **GR-20**: Application Business Logic - Territory classification service patterns
- **GR-04**: Validation & Data Handling - ZIP code validation and geographic data verification

---

## 2. Service Architecture Requirements

### Territory Rating Services

#### VehicleTerritoryService
**Purpose**: Territory-based factor calculation and geographic risk assessment  
**Location**: `app/Domain/Rating/Services/VehicleTerritoryService.php`

**Key Methods**:
```php
class VehicleTerritoryService
{
    public function calculateTerritoryFactor(VehicleTerritoryData $territoryData): TerritoryFactor
    {
        // 1. Validate and normalize ZIP code format
        // 2. Lookup territory factors by ZIP code and coverage types
        // 3. Apply factor caps and floors per coverage type
        // 4. Return comprehensive territory factor breakdown
        // 5. Include county reference and geographic metadata
    }
    
    public function validateZipCodeEligibility(string $zipCode): ValidationResult
    {
        // Validate ZIP code is within Texas service territory
    }
    
    public function getTerritoryFactors(string $zipCode, array $coverageTypes): array
    {
        // Get coverage-specific factors for ZIP code
    }
    
    public function getCountyByZipCode(string $zipCode): CountyReference
    {
        // Get county information for ZIP code reference
    }
}
```

#### GeographicValidationService
**Purpose**: ZIP code validation and geographic data verification  
**Location**: `app/Domain/Rating/Services/GeographicValidationService.php`

**Key Methods**:
```php
class GeographicValidationService
{
    public function validateZipCode(string $zipCode): ZipCodeValidation
    {
        // Validate ZIP code format and existence in Texas
    }
    
    public function validateServiceTerritory(string $zipCode): ServiceTerritoryCheck
    {
        // Verify ZIP code is within approved service territory
    }
    
    public function getCoverageAvailability(string $zipCode): CoverageAvailability
    {
        // Check coverage availability restrictions by territory
    }
}
```

---

## 3. Database Schema Requirements

### Territory Management Tables

#### territory_zip_code
```sql
CREATE TABLE territory_zip_code (
    id BIGINT PRIMARY KEY,
    zip_code VARCHAR(5) UNIQUE NOT NULL,
    zip_code_plus4 VARCHAR(10), -- Extended ZIP for precision if needed
    county_id BIGINT NOT NULL,
    state_id BIGINT NOT NULL,
    territory_name VARCHAR(255),
    service_area ENUM('ACTIVE', 'LIMITED', 'EXCLUDED') NOT NULL DEFAULT 'ACTIVE',
    geographic_region ENUM('URBAN', 'SUBURBAN', 'RURAL', 'METRO') NOT NULL,
    population_density ENUM('VERY_HIGH', 'HIGH', 'MODERATE', 'LOW', 'VERY_LOW') NOT NULL,
    risk_profile ENUM('LOW', 'MODERATE', 'HIGH', 'VERY_HIGH') NOT NULL,
    claims_frequency_index DECIMAL(6,4) DEFAULT 1.0000,
    claims_severity_index DECIMAL(6,4) DEFAULT 1.0000,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    territory_model_version VARCHAR(50) NOT NULL, -- e.g., "2017_Tico_Territory_Model"
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (county_id) REFERENCES county(id),
    FOREIGN KEY (state_id) REFERENCES state(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_zip_code_lookup (zip_code, status_id),
    INDEX idx_county_territories (county_id, service_area),
    INDEX idx_geographic_profile (geographic_region, population_density),
    INDEX idx_risk_profile (risk_profile, claims_frequency_index),
    INDEX idx_territory_model (territory_model_version, effective_date)
);

-- Texas ZIP codes for Aguila Dorada program
-- Note: Sample entries - full dataset includes all 2,836 Texas ZIP codes
INSERT INTO territory_zip_code (zip_code, county_id, state_id, geographic_region, population_density, risk_profile, claims_frequency_index, claims_severity_index, territory_model_version, effective_date) VALUES
('75001', (SELECT id FROM county WHERE county_name = 'Collin'), (SELECT id FROM state WHERE state_code = 'TX'), 'SUBURBAN', 'HIGH', 'MODERATE', 1.0500, 1.0300, '2017_Tico_Territory_Model', '2025-07-15'),
('77003', (SELECT id FROM county WHERE county_name = 'Harris'), (SELECT id FROM state WHERE state_code = 'TX'), 'URBAN', 'VERY_HIGH', 'HIGH', 1.2800, 1.1500, '2017_Tico_Territory_Model', '2025-07-15'),
('76380', (SELECT id FROM county WHERE county_name = 'Archer'), (SELECT id FROM state WHERE state_code = 'TX'), 'RURAL', 'LOW', 'LOW', 0.7500, 0.8200, '2017_Tico_Territory_Model', '2025-07-15'),
('78026', (SELECT id FROM county WHERE county_name = 'Atascosa'), (SELECT id FROM state WHERE state_code = 'TX'), 'RURAL', 'LOW', 'MODERATE', 0.8800, 0.9200, '2017_Tico_Territory_Model', '2025-07-15');
```

#### territory_factor
```sql
CREATE TABLE territory_factor (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    zip_code_id BIGINT NOT NULL,
    coverage_type_id BIGINT NOT NULL,
    factor_value DECIMAL(6,4) NOT NULL,
    factor_floor DECIMAL(6,4), -- Minimum factor cap (e.g., 0.500 for UMBI/UMPD)
    factor_ceiling DECIMAL(6,4), -- Maximum factor cap (e.g., 1.500 for UMBI/UMPD, 2.000 for COMP)
    risk_justification TEXT,
    actuarial_support_data JSON, -- Supporting claims data and statistics
    effective_date DATE NOT NULL,
    expiration_date DATE,
    territory_model_version VARCHAR(50) NOT NULL,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (zip_code_id) REFERENCES territory_zip_code(id),
    FOREIGN KEY (coverage_type_id) REFERENCES coverage_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_territory_factor (
        program_id, 
        zip_code_id, 
        coverage_type_id, 
        effective_date
    ),
    INDEX idx_program_zip_factors (program_id, zip_code_id),
    INDEX idx_coverage_factors (coverage_type_id, factor_value),
    INDEX idx_factor_range (factor_value, factor_floor, factor_ceiling),
    INDEX idx_territory_model (territory_model_version, effective_date)
);
```

#### territory_factor_cap_rule
```sql
CREATE TABLE territory_factor_cap_rule (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    coverage_type_id BIGINT NOT NULL,
    minimum_factor DECIMAL(6,4) NOT NULL DEFAULT 0.0000,
    maximum_factor DECIMAL(6,4) NOT NULL DEFAULT 10.0000,
    cap_justification TEXT,
    regulatory_requirement TEXT,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (coverage_type_id) REFERENCES coverage_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_coverage_cap_rule (program_id, coverage_type_id, effective_date),
    INDEX idx_program_caps (program_id, effective_date),
    INDEX idx_coverage_caps (coverage_type_id, maximum_factor)
);

-- Aguila Dorada territory factor caps
INSERT INTO territory_factor_cap_rule (program_id, coverage_type_id, minimum_factor, maximum_factor, cap_justification, effective_date) VALUES
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'UMBI'), 0.5000, 1.5000, 'Regulatory cap for uninsured motorist coverage', '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'UMPD'), 0.5000, 1.5000, 'Regulatory cap for uninsured motorist property damage', '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'MED'), 0.0000, 1.5000, 'Medical payments coverage cap', '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'PIP'), 0.0000, 1.5000, 'Personal injury protection coverage cap', '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'COMP'), 0.0000, 2.0000, 'Comprehensive coverage cap', '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'BI'), 0.0000, 10.0000, 'No specific cap for bodily injury liability', '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'PD'), 0.0000, 10.0000, 'No specific cap for property damage liability', '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'COLL'), 0.0000, 10.0000, 'No specific cap for collision coverage', '2025-07-15');
```

---

## 4. Business Logic Requirements

### Territory Factor Calculation Logic
```php
class VehicleTerritoryService
{
    public function calculateTerritoryFactor(VehicleTerritoryData $territoryData): TerritoryFactor
    {
        $zipCode = $this->normalizeZipCode($territoryData->zip_code);
        
        // 1. Validate ZIP code eligibility
        $eligibilityResult = $this->validateZipCodeEligibility($zipCode);
        if (!$eligibilityResult->isEligible()) {
            throw new TerritoryEligibilityException($eligibilityResult->getMessage());
        }
        
        // 2. Get ZIP code territory record
        $zipCodeTerritory = $this->getZipCodeTerritory($zipCode);
        
        // 3. Calculate factors for each coverage type
        $factorsByTerritoryFactor = [];
        foreach ($territoryData->coverage_types as $coverageType) {
            $rawFactor = $this->getRawTerritoryFactor($zipCodeTerritory->id, $coverageType);
            $cappedFactor = $this->applyFactorCaps($rawFactor, $coverageType);
            
            $factorsByTerritoryFactor[$coverageType] = $cappedFactor;
        }
        
        return new TerritoryFactor([
            'vehicle_id' => $territoryData->vehicle_id,
            'zip_code' => $zipCode,
            'county_name' => $zipCodeTerritory->county_name,
            'territory_factors' => $factorsByTerritoryFactor,
            'geographic_profile' => [
                'region' => $zipCodeTerritory->geographic_region,
                'population_density' => $zipCodeTerritory->population_density,
                'risk_profile' => $zipCodeTerritory->risk_profile
            ],
            'territory_model_version' => $zipCodeTerritory->territory_model_version
        ]);
    }
    
    private function getRawTerritoryFactor(int $zipCodeId, string $coverageType): float
    {
        return DB::table('territory_factor')
            ->join('coverage_type', 'territory_factor.coverage_type_id', '=', 'coverage_type.id')
            ->where('territory_factor.zip_code_id', $zipCodeId)
            ->where('coverage_type.coverage_code', $coverageType)
            ->where('territory_factor.program_id', $this->programId)
            ->where('territory_factor.effective_date', '<=', now())
            ->where(function($query) {
                $query->whereNull('territory_factor.expiration_date')
                      ->orWhere('territory_factor.expiration_date', '>', now());
            })
            ->where('territory_factor.status_id', Status::ACTIVE)
            ->value('territory_factor.factor_value') ?? 1.0000;
    }
    
    private function applyFactorCaps(float $rawFactor, string $coverageType): float
    {
        $capRule = DB::table('territory_factor_cap_rule')
            ->join('coverage_type', 'territory_factor_cap_rule.coverage_type_id', '=', 'coverage_type.id')
            ->where('coverage_type.coverage_code', $coverageType)
            ->where('territory_factor_cap_rule.program_id', $this->programId)
            ->where('territory_factor_cap_rule.effective_date', '<=', now())
            ->where(function($query) {
                $query->whereNull('territory_factor_cap_rule.expiration_date')
                      ->orWhere('territory_factor_cap_rule.expiration_date', '>', now());
            })
            ->where('territory_factor_cap_rule.status_id', Status::ACTIVE)
            ->first();
            
        if (!$capRule) {
            return $rawFactor; // No caps defined
        }
        
        // Apply minimum and maximum caps
        $cappedFactor = max($capRule->minimum_factor, $rawFactor);
        $cappedFactor = min($capRule->maximum_factor, $cappedFactor);
        
        return $cappedFactor;
    }
    
    public function normalizeZipCode(string $zipCode): string
    {
        // Remove any non-numeric characters and ensure 5-digit format
        $cleanZip = preg_replace('/[^0-9]/', '', $zipCode);
        
        if (strlen($cleanZip) === 9) {
            return substr($cleanZip, 0, 5); // Take first 5 digits if ZIP+4 provided
        }
        
        if (strlen($cleanZip) === 5) {
            return $cleanZip;
        }
        
        throw new InvalidZipCodeException("Invalid ZIP code format: {$zipCode}");
    }
}
```

### Geographic Validation Logic
```php
class GeographicValidationService
{
    public function validateZipCodeEligibility(string $zipCode): ValidationResult
    {
        $result = new ValidationResult();
        
        // 1. Validate ZIP code format
        if (!$this->isValidZipCodeFormat($zipCode)) {
            $result->addError("Invalid ZIP code format: {$zipCode}");
            return $result;
        }
        
        // 2. Check if ZIP code exists in territory database
        $zipCodeTerritory = DB::table('territory_zip_code')
            ->where('zip_code', $zipCode)
            ->where('status_id', Status::ACTIVE)
            ->first();
            
        if (!$zipCodeTerritory) {
            $result->addError("ZIP code {$zipCode} not found in service territory");
            return $result;
        }
        
        // 3. Check service area availability
        if ($zipCodeTerritory->service_area === 'EXCLUDED') {
            $result->addError("ZIP code {$zipCode} is excluded from coverage");
            return $result;
        }
        
        if ($zipCodeTerritory->service_area === 'LIMITED') {
            $result->addWarning("ZIP code {$zipCode} has limited coverage availability");
        }
        
        // 4. Validate effective dates
        if ($zipCodeTerritory->expiration_date && Carbon::parse($zipCodeTerritory->expiration_date) < now()) {
            $result->addError("ZIP code {$zipCode} territory data has expired");
        }
        
        return $result;
    }
    
    private function isValidZipCodeFormat(string $zipCode): bool
    {
        // Accept 5-digit or 9-digit (ZIP+4) formats
        return preg_match('/^\d{5}(-\d{4})?$/', $zipCode) === 1;
    }
}
```

---

## 5. Aguila Dorada Territory Factors

### Sample Territory Factor Matrix
```sql
-- Territory factors for Aguila Dorada program (sample entries)
-- Full implementation requires all 2,836 Texas ZIP codes × 8 coverage types = 22,688 factor records

-- Low-risk rural territory (ZIP 76380, Archer County)
INSERT INTO territory_factor (program_id, zip_code_id, coverage_type_id, factor_value, factor_floor, factor_ceiling, effective_date) VALUES
(1, (SELECT id FROM territory_zip_code WHERE zip_code = '76380'), (SELECT id FROM coverage_type WHERE coverage_code = 'BI'), 0.5210, NULL, NULL, '2025-07-15'),
(1, (SELECT id FROM territory_zip_code WHERE zip_code = '76380'), (SELECT id FROM coverage_type WHERE coverage_code = 'PD'), 0.5870, NULL, NULL, '2025-07-15'),
(1, (SELECT id FROM territory_zip_code WHERE zip_code = '76380'), (SELECT id FROM coverage_type WHERE coverage_code = 'UMBI'), 0.5000, 0.5000, 1.5000, '2025-07-15'),
(1, (SELECT id FROM territory_zip_code WHERE zip_code = '76380'), (SELECT id FROM coverage_type WHERE coverage_code = 'UMPD'), 0.5000, 0.5000, 1.5000, '2025-07-15'),
(1, (SELECT id FROM territory_zip_code WHERE zip_code = '76380'), (SELECT id FROM coverage_type WHERE coverage_code = 'MED'), 0.5620, NULL, 1.5000, '2025-07-15'),
(1, (SELECT id FROM territory_zip_code WHERE zip_code = '76380'), (SELECT id FROM coverage_type WHERE coverage_code = 'PIP'), 0.5620, NULL, 1.5000, '2025-07-15'),
(1, (SELECT id FROM territory_zip_code WHERE zip_code = '76380'), (SELECT id FROM coverage_type WHERE coverage_code = 'COMP'), 2.0000, NULL, 2.0000, '2025-07-15'),
(1, (SELECT id FROM territory_zip_code WHERE zip_code = '76380'), (SELECT id FROM coverage_type WHERE coverage_code = 'COLL'), 0.7540, NULL, NULL, '2025-07-15'),

-- High-risk urban territory (ZIP 77003, Harris County)
(1, (SELECT id FROM territory_zip_code WHERE zip_code = '77003'), (SELECT id FROM coverage_type WHERE coverage_code = 'BI'), 1.2770, NULL, NULL, '2025-07-15'),
(1, (SELECT id FROM territory_zip_code WHERE zip_code = '77003'), (SELECT id FROM coverage_type WHERE coverage_code = 'PD'), 1.2640, NULL, NULL, '2025-07-15'),
(1, (SELECT id FROM territory_zip_code WHERE zip_code = '77003'), (SELECT id FROM coverage_type WHERE coverage_code = 'UMBI'), 1.4130, 0.5000, 1.5000, '2025-07-15'),
(1, (SELECT id FROM territory_zip_code WHERE zip_code = '77003'), (SELECT id FROM coverage_type WHERE coverage_code = 'UMPD'), 1.5000, 0.5000, 1.5000, '2025-07-15'),
(1, (SELECT id FROM territory_zip_code WHERE zip_code = '77003'), (SELECT id FROM coverage_type WHERE coverage_code = 'MED'), 1.5000, NULL, 1.5000, '2025-07-15'),
(1, (SELECT id FROM territory_zip_code WHERE zip_code = '77003'), (SELECT id FROM coverage_type WHERE coverage_code = 'PIP'), 1.5000, NULL, 1.5000, '2025-07-15'),
(1, (SELECT id FROM territory_zip_code WHERE zip_code = '77003'), (SELECT id FROM coverage_type WHERE coverage_code = 'COMP'), 1.0000, NULL, 2.0000, '2025-07-15'),
(1, (SELECT id FROM territory_zip_code WHERE zip_code = '77003'), (SELECT id FROM coverage_type WHERE coverage_code = 'COLL'), 1.4790, NULL, NULL, '2025-07-15');
```

---

## 6. API Integration Requirements

### Territory Factor Endpoints
```php
// Territory factor API endpoints
POST /api/v1/rating/territory/calculate
{
    "vehicle_territory_data": {
        "vehicle_id": 12345,
        "zip_code": "75001",
        "coverage_types": ["BI", "PD", "UMBI", "UMPD", "MED", "PIP", "COMP", "COLL"]
    }
}

GET /api/v1/rating/territory/validate/{zipCode}
// Validate ZIP code eligibility and service area

GET /api/v1/rating/territory/lookup/{zipCode}
// Get territory information and county for ZIP code

POST /api/v1/rating/territory/batch-lookup
{
    "zip_codes": ["75001", "77003", "78026"],
    "coverage_types": ["BI", "PD", "COMP", "COLL"]
}
// Batch territory factor lookup for multiple ZIP codes
```

### Response Format
```json
{
    "vehicle_id": 12345,
    "zip_code": "75001",
    "territory_info": {
        "county_name": "Collin County",
        "geographic_region": "SUBURBAN",
        "population_density": "HIGH",
        "risk_profile": "MODERATE",
        "service_area": "ACTIVE"
    },
    "territory_factors": {
        "BI": 1.0500,
        "PD": 1.0300,
        "UMBI": 1.1200,
        "UMPD": 1.0800,
        "MED": 1.0900,
        "PIP": 1.0900,
        "COMP": 1.1500,
        "COLL": 1.0700
    },
    "factor_details": {
        "territory_model_version": "2017_Tico_Territory_Model",
        "effective_date": "2025-07-15",
        "caps_applied": [
            {
                "coverage": "UMBI",
                "original_factor": 1.1200,
                "capped_factor": 1.1200,
                "cap_limit": 1.5000
            }
        ]
    },
    "validation": {
        "zip_code_valid": true,
        "service_area_eligible": true,
        "territory_data_current": true
    }
}
```

---

## 7. Performance Requirements

### Territory Factor Caching
```php
class VehicleTerritoryService
{
    public function calculateTerritoryFactor(VehicleTerritoryData $territoryData): TerritoryFactor
    {
        // Cache territory factors by ZIP code
        $cacheKey = "territory_factor_{$this->programId}_{$territoryData->zip_code}";
        
        return Cache::remember($cacheKey, 3600, function() use ($territoryData) {
            return $this->performTerritoryFactorCalculation($territoryData);
        });
    }
}
```

### Database Performance
```sql
-- Territory factor lookup optimization (critical for 22,688 factor records)
CREATE INDEX idx_territory_factor_lookup 
ON territory_factor (
    program_id, 
    zip_code_id, 
    coverage_type_id,
    effective_date
) WHERE status_id = 1;

-- ZIP code territory lookup optimization
CREATE INDEX idx_zip_code_territory_lookup 
ON territory_zip_code (
    zip_code, 
    service_area, 
    effective_date
) WHERE status_id = 1;

-- County cross-reference optimization
CREATE INDEX idx_county_zip_lookup 
ON territory_zip_code (
    county_id, 
    zip_code
) WHERE status_id = 1;
```

---

## 8. Testing Requirements

### Territory Factor Testing
```php
class VehicleTerritoryServiceTest extends TestCase
{
    public function test_low_risk_rural_territory()
    {
        $territoryData = new VehicleTerritoryData([
            'zip_code' => '76380', // Archer County
            'coverage_types' => ['BI', 'PD', 'COMP']
        ]);
        
        $factor = $this->territoryService->calculateTerritoryFactor($territoryData);
        
        $this->assertEquals('76380', $factor->zip_code);
        $this->assertEquals('Archer', $factor->county_name);
        $this->assertLessThan(1.0, $factor->territory_factors['BI']); // Rural discount
        $this->assertEquals(2.0000, $factor->territory_factors['COMP']); // At cap
    }
    
    public function test_high_risk_urban_territory()
    {
        $territoryData = new VehicleTerritoryData([
            'zip_code' => '77003', // Harris County urban
            'coverage_types' => ['BI', 'UMBI', 'UMPD']
        ]);
        
        $factor = $this->territoryService->calculateTerritoryFactor($territoryData);
        
        $this->assertEquals('77003', $factor->zip_code);
        $this->assertGreaterThan(1.0, $factor->territory_factors['BI']); // Urban surcharge
        $this->assertEquals(1.5000, $factor->territory_factors['UMPD']); // At cap
    }
    
    public function test_factor_caps_enforcement()
    {
        $territoryData = new VehicleTerritoryData([
            'zip_code' => '77003',
            'coverage_types' => ['UMBI', 'UMPD', 'COMP']
        ]);
        
        $factor = $this->territoryService->calculateTerritoryFactor($territoryData);
        
        // Verify caps are properly applied
        $this->assertLessThanOrEqual(1.5000, $factor->territory_factors['UMBI']);
        $this->assertLessThanOrEqual(1.5000, $factor->territory_factors['UMPD']);
        $this->assertLessThanOrEqual(2.0000, $factor->territory_factors['COMP']);
    }
    
    public function test_invalid_zip_code_handling()
    {
        $territoryData = new VehicleTerritoryData([
            'zip_code' => '99999', // Invalid ZIP
            'coverage_types' => ['BI']
        ]);
        
        $this->expectException(TerritoryEligibilityException::class);
        $this->territoryService->calculateTerritoryFactor($territoryData);
    }
}
```

---

## Implementation Priority: HIGH
This factor is foundational for geographic risk assessment and must be implemented early as it affects all coverage types and provides the base for other territorial adjustments.

## Dependencies
- **County Database**: Complete Texas county reference data
- **Coverage Type Configuration**: All 8 coverage types defined in system
- **ZIP Code Validation Service**: Address validation and normalization

## Estimated Implementation Effort
- **Database Schema**: 5 days (22,688 territory factor records)
- **Service Layer**: 4 days
- **Geographic Validation**: 3 days
- **Performance Optimization**: 3 days
- **API Integration**: 2 days
- **Testing**: 4 days
- **Total**: 21 days

This plan implements comprehensive territory-based risk assessment covering all 2,836 Texas ZIP codes while maintaining proper factor caps, geographic validation, and high-performance lookups for the large territory factor dataset.