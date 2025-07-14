# Vehicle County Modifier Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Vehicle County Modifier  
**Category**: Vehicle Factor  
**Priority**: Medium - County-level risk adjustment layer  
**Implementation Complexity**: Medium  

### Business Requirements Summary
The Vehicle County Modifier factor implements additional risk-based pricing adjustments based on the county where vehicles are principally garaged. This factor provides county-level rate modifiers that work in conjunction with ZIP code territory factors to create a more refined geographic risk assessment across all 254 Texas counties.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing and new Global Requirements:

#### Leverages GR-85: Geographic Territory Rating Standards
**Integration**: County-level modifiers as an additional layer to ZIP code territory factors  
**Dependencies**: County-based risk assessment methodology and territorial rating coordination

#### New Requirement: GR-86: County-Level Risk Adjustment Standards
**Priority**: Medium  
**Rationale**: County-based rate modifier methodology for secondary geographic risk assessment  

**Core Components**:
- County-level risk classification and modifier assignment methodology
- County boundary validation and geographic reference standards
- Coverage-specific county modifier application rules
- County risk profile assessment based on regional characteristics
- County modifier versioning and effective date management
- Integration standards with primary territory rating factors

#### Leverages GR-41: Table Schema Requirements
**Integration**: County modifier data structures and geographic relationship management  
**Dependencies**: County reference data and rate modifier table patterns

### Integration with Existing Global Requirements
- **GR-65**: Rating Engine Architecture - County modifier integration with core rating engine
- **GR-20**: Application Business Logic - County classification service patterns
- **GR-04**: Validation & Data Handling - County validation and geographic data verification

---

## 2. Service Architecture Requirements

### County Modifier Services

#### VehicleCountyModifierService
**Purpose**: County-based modifier calculation and regional risk assessment  
**Location**: `app/Domain/Rating/Services/VehicleCountyModifierService.php`

**Key Methods**:
```php
class VehicleCountyModifierService
{
    public function calculateCountyModifier(VehicleCountyData $countyData): CountyModifierFactor
    {
        // 1. Validate county assignment and eligibility
        // 2. Lookup county-specific modifiers by coverage type
        // 3. Apply coverage-specific modifier rules
        // 4. Return modifier factors with county risk profile
        // 5. Include modifier justification and effective dates
    }
    
    public function getCountyByVehicleLocation(VehicleLocationData $locationData): CountyAssignment
    {
        // Determine county from vehicle garaging address
    }
    
    public function validateCountyEligibility(string $countyCode): ValidationResult
    {
        // Validate county is within Texas service area
    }
    
    public function getCountyRiskProfile(string $countyCode): CountyRiskProfile
    {
        // Get comprehensive county risk characteristics
    }
}
```

#### CountyValidationService
**Purpose**: County assignment validation and geographic verification  
**Location**: `app/Domain/Rating/Services/CountyValidationService.php`

**Key Methods**:
```php
class CountyValidationService
{
    public function validateCountyAssignment(VehicleLocationData $locationData): CountyValidationResult
    {
        // Validate county assignment based on address
    }
    
    public function resolveCountyFromAddress(Address $address): CountyResolution
    {
        // Resolve county from complete address information
    }
    
    public function validateCountyBoundaries(string $countyCode, string $zipCode): BoundaryValidation
    {
        // Cross-validate county and ZIP code alignment
    }
}
```

---

## 3. Database Schema Requirements

### County Modifier Management Tables

#### county_risk_classification
```sql
CREATE TABLE county_risk_classification (
    id BIGINT PRIMARY KEY,
    county_id BIGINT NOT NULL,
    classification_code VARCHAR(50) NOT NULL,
    classification_name VARCHAR(255) NOT NULL,
    risk_level ENUM('LOW', 'STANDARD', 'HIGH', 'VERY_HIGH') NOT NULL,
    geographic_characteristics JSON, -- Regional risk factors
    demographic_profile JSON, -- County demographic data
    claims_experience_index DECIMAL(6,4) DEFAULT 1.0000,
    economic_factors JSON, -- Economic indicators affecting risk
    effective_date DATE NOT NULL,
    expiration_date DATE,
    source_model_version VARCHAR(50) NOT NULL, -- e.g., "2017_Tico_Territory_Model"
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (county_id) REFERENCES county(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_county_classification (county_id, classification_code, effective_date),
    INDEX idx_county_risk_level (county_id, risk_level),
    INDEX idx_classification_code (classification_code, status_id),
    INDEX idx_source_model (source_model_version, effective_date)
);

-- Texas county risk classifications for Aguila Dorada
INSERT INTO county_risk_classification (county_id, classification_code, classification_name, risk_level, source_model_version, effective_date) VALUES
-- Standard counties (majority of Texas counties)
((SELECT id FROM county WHERE county_name = 'Andrews'), 'STANDARD_COUNTY', 'Standard Risk County', 'STANDARD', '2017_Tico_Territory_Model', '2025-07-15'),
((SELECT id FROM county WHERE county_name = 'Aransas'), 'STANDARD_COUNTY', 'Standard Risk County', 'STANDARD', '2017_Tico_Territory_Model', '2025-07-15'),
((SELECT id FROM county WHERE county_name = 'Archer'), 'STANDARD_COUNTY', 'Standard Risk County', 'STANDARD', '2017_Tico_Territory_Model', '2025-07-15'),

-- High-risk counties with modifier adjustments
((SELECT id FROM county WHERE county_name = 'Anderson'), 'MODIFIED_COUNTY', 'Modified Risk County', 'HIGH', '2017_Tico_Territory_Model', '2025-07-15'),
((SELECT id FROM county WHERE county_name = 'Angelina'), 'MODIFIED_COUNTY', 'Modified Risk County', 'HIGH', '2017_Tico_Territory_Model', '2025-07-15');
```

#### county_modifier_factor
```sql
CREATE TABLE county_modifier_factor (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    county_id BIGINT NOT NULL,
    coverage_type_id BIGINT NOT NULL,
    modifier_value DECIMAL(6,4) NOT NULL DEFAULT 1.0000,
    modifier_type ENUM('DISCOUNT', 'NEUTRAL', 'SURCHARGE') NOT NULL,
    modifier_percentage DECIMAL(5,2), -- Percentage representation (e.g., -10.00 for 0.90 factor)
    risk_justification TEXT,
    actuarial_support_data JSON,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    source_model_version VARCHAR(50) NOT NULL,
    regulatory_approval_date DATE,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (county_id) REFERENCES county(id),
    FOREIGN KEY (coverage_type_id) REFERENCES coverage_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_county_modifier (
        program_id, 
        county_id, 
        coverage_type_id, 
        effective_date
    ),
    INDEX idx_program_county_modifiers (program_id, county_id),
    INDEX idx_coverage_modifiers (coverage_type_id, modifier_value),
    INDEX idx_modifier_type (modifier_type, status_id),
    INDEX idx_source_model (source_model_version, effective_date)
);
```

#### county_modifier_rule
```sql
CREATE TABLE county_modifier_rule (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    rule_code VARCHAR(50) NOT NULL,
    rule_name VARCHAR(255) NOT NULL,
    rule_description TEXT,
    county_classification VARCHAR(50), -- Links to classification_code
    coverage_applicability JSON, -- Array of coverage codes affected
    modifier_logic TEXT, -- Business rules for modifier application
    priority_order INT DEFAULT 0,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_program_rule (program_id, rule_code, effective_date),
    INDEX idx_county_classification (county_classification, status_id),
    INDEX idx_priority_order (priority_order, effective_date)
);

-- Aguila Dorada county modifier rules
INSERT INTO county_modifier_rule (program_id, rule_code, rule_name, county_classification, coverage_applicability, modifier_logic, effective_date) VALUES
(1, 'STANDARD_COUNTY_NEUTRAL', 'Standard County Neutral Modifier', 'STANDARD_COUNTY', 
 '["BI", "PD", "UMBI", "UMPD", "MED", "PIP", "COMP", "COLL"]', 
 'Apply 1.00 modifier (no adjustment) for all coverages in standard risk counties', '2025-07-15'),
 
(1, 'MODIFIED_COUNTY_DISCOUNT', 'Modified County Selective Discount', 'MODIFIED_COUNTY', 
 '["BI", "PD", "COMP", "COLL"]', 
 'Apply 0.90 modifier (10% discount) for BI/PD/COMP/COLL in high-risk counties requiring adjustment', '2025-07-15'),
 
(1, 'MODIFIED_COUNTY_NEUTRAL_UM', 'Modified County UM Neutral', 'MODIFIED_COUNTY', 
 '["UMBI", "UMPD", "MED", "PIP"]', 
 'Apply 1.00 modifier (no adjustment) for UM/MED/PIP coverages in modified counties', '2025-07-15');
```

---

## 4. Business Logic Requirements

### County Modifier Calculation Logic
```php
class VehicleCountyModifierService
{
    public function calculateCountyModifier(VehicleCountyData $countyData): CountyModifierFactor
    {
        // 1. Resolve county from vehicle location
        $countyAssignment = $this->getCountyByVehicleLocation($countyData->location_data);
        
        // 2. Validate county eligibility
        $eligibilityResult = $this->validateCountyEligibility($countyAssignment->county_code);
        if (!$eligibilityResult->isEligible()) {
            throw new CountyEligibilityException($eligibilityResult->getMessage());
        }
        
        // 3. Get county risk classification
        $countyClassification = $this->getCountyRiskClassification($countyAssignment->county_id);
        
        // 4. Calculate modifiers for each coverage type
        $modifiersByConverage = [];
        foreach ($countyData->coverage_types as $coverageType) {
            $modifier = $this->getCountyModifierFactor(
                $countyAssignment->county_id, 
                $coverageType
            );
            
            $modifiersByConverage[$coverageType] = $modifier;
        }
        
        return new CountyModifierFactor([
            'vehicle_id' => $countyData->vehicle_id,
            'county_code' => $countyAssignment->county_code,
            'county_name' => $countyAssignment->county_name,
            'county_classification' => $countyClassification,
            'modifier_factors' => $modifiersByConverage,
            'risk_profile' => $this->getCountyRiskProfile($countyAssignment->county_code),
            'source_model_version' => $this->getActiveModelVersion()
        ]);
    }
    
    private function getCountyModifierFactor(int $countyId, string $coverageType): float
    {
        $modifier = DB::table('county_modifier_factor')
            ->join('coverage_type', 'county_modifier_factor.coverage_type_id', '=', 'coverage_type.id')
            ->where('county_modifier_factor.county_id', $countyId)
            ->where('coverage_type.coverage_code', $coverageType)
            ->where('county_modifier_factor.program_id', $this->programId)
            ->where('county_modifier_factor.effective_date', '<=', now())
            ->where(function($query) {
                $query->whereNull('county_modifier_factor.expiration_date')
                      ->orWhere('county_modifier_factor.expiration_date', '>', now());
            })
            ->where('county_modifier_factor.status_id', Status::ACTIVE)
            ->value('county_modifier_factor.modifier_value');
            
        return $modifier ?? 1.0000; // Default to no adjustment if not found
    }
    
    public function getCountyByVehicleLocation(VehicleLocationData $locationData): CountyAssignment
    {
        // Primary: Use county if directly provided
        if ($locationData->county_code) {
            return $this->validateCountyCode($locationData->county_code);
        }
        
        // Secondary: Resolve from ZIP code
        if ($locationData->zip_code) {
            return $this->resolveCountyFromZipCode($locationData->zip_code);
        }
        
        // Tertiary: Resolve from full address
        if ($locationData->address) {
            return $this->resolveCountyFromAddress($locationData->address);
        }
        
        throw new CountyResolutionException("Unable to determine county from provided location data");
    }
    
    private function resolveCountyFromZipCode(string $zipCode): CountyAssignment
    {
        $county = DB::table('territory_zip_code')
            ->join('county', 'territory_zip_code.county_id', '=', 'county.id')
            ->where('territory_zip_code.zip_code', $zipCode)
            ->where('territory_zip_code.status_id', Status::ACTIVE)
            ->first();
            
        if (!$county) {
            throw new CountyResolutionException("County not found for ZIP code: {$zipCode}");
        }
        
        return new CountyAssignment([
            'county_id' => $county->county_id,
            'county_code' => $county->county_code,
            'county_name' => $county->county_name,
            'resolution_method' => 'ZIP_CODE'
        ]);
    }
}
```

### County Risk Classification Logic
```php
class CountyRiskAssessmentService
{
    public function getCountyRiskClassification(int $countyId): CountyRiskClassification
    {
        $classification = DB::table('county_risk_classification')
            ->join('county', 'county_risk_classification.county_id', '=', 'county.id')
            ->where('county_risk_classification.county_id', $countyId)
            ->where('county_risk_classification.effective_date', '<=', now())
            ->where(function($query) {
                $query->whereNull('county_risk_classification.expiration_date')
                      ->orWhere('county_risk_classification.expiration_date', '>', now());
            })
            ->where('county_risk_classification.status_id', Status::ACTIVE)
            ->first();
            
        if (!$classification) {
            // Default to standard classification if not found
            return new CountyRiskClassification([
                'county_id' => $countyId,
                'classification_code' => 'STANDARD_COUNTY',
                'classification_name' => 'Standard Risk County',
                'risk_level' => 'STANDARD'
            ]);
        }
        
        return new CountyRiskClassification([
            'county_id' => $classification->county_id,
            'classification_code' => $classification->classification_code,
            'classification_name' => $classification->classification_name,
            'risk_level' => $classification->risk_level,
            'geographic_characteristics' => json_decode($classification->geographic_characteristics, true),
            'demographic_profile' => json_decode($classification->demographic_profile, true),
            'claims_experience_index' => $classification->claims_experience_index
        ]);
    }
}
```

---

## 5. Aguila Dorada County Modifier Matrix

### County Modifier Factor Implementation
```sql
-- County modifier factors for Aguila Dorada program
-- Standard counties (1.00 modifier for all coverages) - represents majority of 254 Texas counties
INSERT INTO county_modifier_factor (program_id, county_id, coverage_type_id, modifier_value, modifier_type, modifier_percentage, effective_date, source_model_version) VALUES
-- Andrews County (Standard County - sample of standard counties)
(1, (SELECT id FROM county WHERE county_name = 'Andrews'), (SELECT id FROM coverage_type WHERE coverage_code = 'BI'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Andrews'), (SELECT id FROM coverage_type WHERE coverage_code = 'PD'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Andrews'), (SELECT id FROM coverage_type WHERE coverage_code = 'UMBI'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Andrews'), (SELECT id FROM coverage_type WHERE coverage_code = 'UMPD'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Andrews'), (SELECT id FROM coverage_type WHERE coverage_code = 'MED'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Andrews'), (SELECT id FROM coverage_type WHERE coverage_code = 'PIP'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Andrews'), (SELECT id FROM coverage_type WHERE coverage_code = 'COMP'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Andrews'), (SELECT id FROM coverage_type WHERE coverage_code = 'COLL'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15', '2017_Tico_Territory_Model'),

-- Anderson County (Modified County - selective 0.90 modifier)
(1, (SELECT id FROM county WHERE county_name = 'Anderson'), (SELECT id FROM coverage_type WHERE coverage_code = 'BI'), 0.9000, 'DISCOUNT', -10.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Anderson'), (SELECT id FROM coverage_type WHERE coverage_code = 'PD'), 0.9000, 'DISCOUNT', -10.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Anderson'), (SELECT id FROM coverage_type WHERE coverage_code = 'UMBI'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Anderson'), (SELECT id FROM coverage_type WHERE coverage_code = 'UMPD'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Anderson'), (SELECT id FROM coverage_type WHERE coverage_code = 'MED'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Anderson'), (SELECT id FROM coverage_type WHERE coverage_code = 'PIP'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Anderson'), (SELECT id FROM coverage_type WHERE coverage_code = 'COMP'), 0.9000, 'DISCOUNT', -10.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Anderson'), (SELECT id FROM coverage_type WHERE coverage_code = 'COLL'), 0.9000, 'DISCOUNT', -10.00, '2025-07-15', '2017_Tico_Territory_Model'),

-- Angelina County (Modified County - selective 0.90 modifier)
(1, (SELECT id FROM county WHERE county_name = 'Angelina'), (SELECT id FROM coverage_type WHERE coverage_code = 'BI'), 0.9000, 'DISCOUNT', -10.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Angelina'), (SELECT id FROM coverage_type WHERE coverage_code = 'PD'), 0.9000, 'DISCOUNT', -10.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Angelina'), (SELECT id FROM coverage_type WHERE coverage_code = 'UMBI'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Angelina'), (SELECT id FROM coverage_type WHERE coverage_code = 'UMPD'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Angelina'), (SELECT id FROM coverage_type WHERE coverage_code = 'MED'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Angelina'), (SELECT id FROM coverage_type WHERE coverage_code = 'PIP'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Angelina'), (SELECT id FROM coverage_type WHERE coverage_code = 'COMP'), 0.9000, 'DISCOUNT', -10.00, '2025-07-15', '2017_Tico_Territory_Model'),
(1, (SELECT id FROM county WHERE county_name = 'Angelina'), (SELECT id FROM coverage_type WHERE coverage_code = 'COLL'), 0.9000, 'DISCOUNT', -10.00, '2025-07-15', '2017_Tico_Territory_Model');

-- Note: Similar patterns would be applied for all 254 Texas counties
-- Most counties receive 1.0000 modifiers (no adjustment)
-- Only Anderson and Angelina counties receive selective 0.9000 modifiers
```

---

## 6. API Integration Requirements

### County Modifier Endpoints
```php
// County modifier API endpoints
POST /api/v1/rating/county-modifier/calculate
{
    "vehicle_county_data": {
        "vehicle_id": 12345,
        "location_data": {
            "county_code": "ANDERSON",
            "zip_code": "75801",
            "address": {
                "street": "123 Main St",
                "city": "Palestine", 
                "state": "TX",
                "zip_code": "75801"
            }
        },
        "coverage_types": ["BI", "PD", "UMBI", "UMPD", "MED", "PIP", "COMP", "COLL"]
    }
}

GET /api/v1/rating/county-modifier/county/{countyCode}
// Get county modifier information and risk profile

POST /api/v1/rating/county-modifier/resolve-county
{
    "location_data": {
        "zip_code": "75801"
    }
}
// Resolve county from ZIP code or address

GET /api/v1/rating/county-modifier/counties
// Get all Texas counties with modifier classifications
```

### Response Format
```json
{
    "vehicle_id": 12345,
    "county_assignment": {
        "county_code": "ANDERSON",
        "county_name": "Anderson County",
        "resolution_method": "ZIP_CODE"
    },
    "county_classification": {
        "classification_code": "MODIFIED_COUNTY",
        "classification_name": "Modified Risk County",
        "risk_level": "HIGH"
    },
    "county_modifiers": {
        "BI": 0.9000,
        "PD": 0.9000,
        "UMBI": 1.0000,
        "UMPD": 1.0000,
        "MED": 1.0000,
        "PIP": 1.0000,
        "COMP": 0.9000,
        "COLL": 0.9000
    },
    "modifier_details": {
        "discount_coverages": ["BI", "PD", "COMP", "COLL"],
        "neutral_coverages": ["UMBI", "UMPD", "MED", "PIP"],
        "total_discount_percentage": -10.00,
        "source_model_version": "2017_Tico_Territory_Model"
    },
    "risk_profile": {
        "geographic_characteristics": ["rural", "forest_prone", "low_population_density"],
        "demographic_profile": ["aging_population", "rural_economy"],
        "claims_experience_index": 0.8500
    }
}
```

---

## 7. Performance Requirements

### County Modifier Caching
```php
class VehicleCountyModifierService
{
    public function calculateCountyModifier(VehicleCountyData $countyData): CountyModifierFactor
    {
        // Cache county modifiers by county code
        $cacheKey = "county_modifier_{$this->programId}_{$countyData->county_code}";
        
        return Cache::remember($cacheKey, 7200, function() use ($countyData) {
            return $this->performCountyModifierCalculation($countyData);
        });
    }
}
```

### Database Performance
```sql
-- County modifier lookup optimization
CREATE INDEX idx_county_modifier_lookup 
ON county_modifier_factor (
    program_id, 
    county_id, 
    coverage_type_id,
    effective_date
) WHERE status_id = 1;

-- County resolution optimization
CREATE INDEX idx_county_zip_resolution 
ON territory_zip_code (
    zip_code, 
    county_id
) WHERE status_id = 1;

-- County classification lookup
CREATE INDEX idx_county_classification_lookup 
ON county_risk_classification (
    county_id, 
    classification_code, 
    effective_date
) WHERE status_id = 1;
```

---

## 8. Testing Requirements

### County Modifier Testing
```php
class VehicleCountyModifierServiceTest extends TestCase
{
    public function test_standard_county_neutral_modifier()
    {
        $countyData = new VehicleCountyData([
            'county_code' => 'ANDREWS',
            'coverage_types' => ['BI', 'PD', 'COMP', 'COLL']
        ]);
        
        $modifier = $this->countyModifierService->calculateCountyModifier($countyData);
        
        $this->assertEquals('ANDREWS', $modifier->county_code);
        $this->assertEquals('STANDARD_COUNTY', $modifier->county_classification->classification_code);
        $this->assertEquals(1.0000, $modifier->modifier_factors['BI']);
        $this->assertEquals(1.0000, $modifier->modifier_factors['PD']);
        $this->assertEquals(1.0000, $modifier->modifier_factors['COMP']);
        $this->assertEquals(1.0000, $modifier->modifier_factors['COLL']);
    }
    
    public function test_modified_county_selective_discount()
    {
        $countyData = new VehicleCountyData([
            'county_code' => 'ANDERSON',
            'coverage_types' => ['BI', 'PD', 'UMBI', 'UMPD', 'COMP', 'COLL']
        ]);
        
        $modifier = $this->countyModifierService->calculateCountyModifier($countyData);
        
        $this->assertEquals('ANDERSON', $modifier->county_code);
        $this->assertEquals('MODIFIED_COUNTY', $modifier->county_classification->classification_code);
        
        // Should have 0.90 discount for BI/PD/COMP/COLL
        $this->assertEquals(0.9000, $modifier->modifier_factors['BI']);
        $this->assertEquals(0.9000, $modifier->modifier_factors['PD']);
        $this->assertEquals(0.9000, $modifier->modifier_factors['COMP']);
        $this->assertEquals(0.9000, $modifier->modifier_factors['COLL']);
        
        // Should remain neutral for UMBI/UMPD
        $this->assertEquals(1.0000, $modifier->modifier_factors['UMBI']);
        $this->assertEquals(1.0000, $modifier->modifier_factors['UMPD']);
    }
    
    public function test_county_resolution_from_zip_code()
    {
        $countyData = new VehicleCountyData([
            'location_data' => new VehicleLocationData(['zip_code' => '75801']), // Anderson County
            'coverage_types' => ['BI']
        ]);
        
        $modifier = $this->countyModifierService->calculateCountyModifier($countyData);
        
        $this->assertEquals('ANDERSON', $modifier->county_assignment->county_code);
        $this->assertEquals('ZIP_CODE', $modifier->county_assignment->resolution_method);
    }
}
```

---

## Implementation Priority: MEDIUM
This factor provides an additional layer of geographic risk assessment and should be implemented after primary territory factors but before policy-level factors.

## Dependencies
- **Vehicle Territory Factor**: County modifiers work in conjunction with ZIP code territory factors
- **County Reference Data**: Complete Texas county database with boundaries
- **Geographic Validation Service**: County assignment and validation capabilities

## Estimated Implementation Effort
- **Database Schema**: 3 days (254 counties × 8 coverage types = 2,032 modifier records)
- **Service Layer**: 3 days
- **County Resolution Logic**: 2 days
- **API Integration**: 2 days
- **Testing**: 2 days
- **Total**: 12 days

This plan implements comprehensive county-level risk adjustment providing an additional geographic risk assessment layer that complements ZIP code territory factors while maintaining simplicity with only two county classifications (standard and modified) affecting specific coverage combinations.