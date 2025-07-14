# Vehicle Age Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Vehicle Age  
**Category**: Vehicle Factor  
**Priority**: High - Core vehicle risk assessment  
**Implementation Complexity**: Medium  

### Business Requirements Summary
The Vehicle Age factor implements risk-based pricing adjustments based on the age of insured vehicles, calculated from model year to policy effective date. This factor reflects the correlation between vehicle age and claim frequency/severity, providing appropriate premium adjustments that account for safety features, repair costs, theft susceptibility, and overall risk characteristics that change with vehicle age.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing and new Global Requirements:

#### Leverages GR-65: Rating Engine Architecture
**Integration**: Vehicle age factor calculation within multiplicative rating engine  
**Dependencies**: RatingEngineService for age-based factor lookup and validation

#### New Requirement: GR-82: Vehicle Characteristics Assessment Standards
**Priority**: Medium  
**Rationale**: Vehicle physical characteristics and age-based risk evaluation standards  

**Core Components**:
- Vehicle age calculation methodology and model year validation
- Age-based risk correlation and factor assignment standards
- Vehicle eligibility thresholds and age restrictions
- Safety feature evolution and technology impact assessment
- Depreciation and repair cost correlation with age factors

#### Leverages GR-53: DCS Integration Architecture
**Integration**: Vehicle age verification through VIN decoding and vehicle data services  
**Dependencies**: VIN decoding for accurate model year determination

### Integration with Existing Global Requirements
- **GR-41**: Table Schema Requirements - Vehicle age factor table structures
- **GR-20**: Application Business Logic - Age calculation service patterns
- **GR-04**: Validation & Data Handling - Model year and age validation rules

---

## 2. Service Architecture Requirements

### Vehicle Age Assessment Services

#### VehicleAgeService
**Purpose**: Vehicle age calculation and factor determination  
**Location**: `app/Domain/Rating/Services/VehicleAgeService.php`

**Key Methods**:
```php
class VehicleAgeService
{
    public function calculateVehicleAgeFactor(VehicleAgeData $vehicleData): VehicleAgeFactor
    {
        // 1. Calculate vehicle age from model year to effective date
        // 2. Validate vehicle age against eligibility thresholds
        // 3. Lookup age-based factor from factor table
        // 4. Apply special considerations for classic/antique vehicles
        // 5. Return factor with age breakdown and risk assessment
    }
    
    public function validateVehicleAgeEligibility(VehicleAgeData $vehicleData): ValidationResult
    {
        // Validate vehicle age meets program eligibility requirements
    }
    
    public function calculateVehicleAge(int $modelYear, Carbon $effectiveDate): int
    {
        // Calculate vehicle age with consistent methodology
    }
    
    public function determineAgeCategory(int $vehicleAge): string
    {
        // Categorize vehicle age into rating brackets
    }
}
```

#### VehicleDataVerificationService
**Purpose**: Vehicle data verification and model year validation  
**Location**: `app/Domain/Rating/Services/VehicleDataVerificationService.php`

**Key Methods**:
```php
class VehicleDataVerificationService
{
    public function verifyModelYear(string $vin): ModelYearVerification
    {
        // Verify model year through VIN decoding
    }
    
    public function validateVehicleData(VehicleData $vehicleData): ValidationResult
    {
        // Validate vehicle data consistency and accuracy
    }
    
    public function checkEligibilityRestrictions(VehicleAgeData $vehicleData): EligibilityCheck
    {
        // Check age-based eligibility restrictions
    }
}
```

---

## 3. Database Schema Requirements

### Vehicle Age Management Tables

#### vehicle_age_category
```sql
CREATE TABLE vehicle_age_category (
    id BIGINT PRIMARY KEY,
    category_code VARCHAR(50) UNIQUE NOT NULL,
    category_name VARCHAR(255) NOT NULL,
    category_description TEXT,
    age_min INT NOT NULL,
    age_max INT, -- NULL for open-ended ranges
    risk_level ENUM('LOW', 'MODERATE', 'HIGH', 'VERY_HIGH') NOT NULL,
    eligibility_status ENUM('ELIGIBLE', 'LIMITED', 'INELIGIBLE') NOT NULL,
    special_considerations TEXT,
    display_order INT DEFAULT 0,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_age_range (age_min, age_max),
    INDEX idx_age_range (age_min, age_max),
    INDEX idx_eligibility (eligibility_status, status_id),
    INDEX idx_display_order (display_order, status_id)
);

-- Aguila Dorada vehicle age categories
INSERT INTO vehicle_age_category (category_code, category_name, age_min, age_max, risk_level, eligibility_status, display_order) VALUES
('AGE_0_3', 'New/Recent (0-3 years)', 0, 3, 'LOW', 'ELIGIBLE', 1),
('AGE_4_7', 'Modern (4-7 years)', 4, 7, 'MODERATE', 'ELIGIBLE', 2),
('AGE_8_12', 'Mature (8-12 years)', 8, 12, 'MODERATE', 'ELIGIBLE', 3),
('AGE_13_15', 'Older (13-15 years)', 13, 15, 'HIGH', 'ELIGIBLE', 4),
('AGE_16_20', 'Very Old (16-20 years)', 16, 20, 'VERY_HIGH', 'LIMITED', 5),
('AGE_21_PLUS', 'Antique (21+ years)', 21, NULL, 'VERY_HIGH', 'INELIGIBLE', 6),
('AGE_CLASSIC', 'Classic/Collector (25+ years)', 25, NULL, 'MODERATE', 'LIMITED', 7);
```

#### vehicle_age_factor
```sql
CREATE TABLE vehicle_age_factor (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    age_category_id BIGINT NOT NULL,
    coverage_type_id BIGINT, -- NULL for all coverages, specific ID for coverage-specific factors
    factor_value DECIMAL(6,4) NOT NULL,
    applies_to_physical_damage BOOLEAN DEFAULT TRUE,
    applies_to_liability BOOLEAN DEFAULT TRUE,
    minimum_factor DECIMAL(6,4), -- Minimum factor cap
    maximum_factor DECIMAL(6,4), -- Maximum factor cap
    effective_date DATE NOT NULL,
    expiration_date DATE,
    actuarial_justification TEXT,
    eligibility_notes TEXT,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (age_category_id) REFERENCES vehicle_age_category(id),
    FOREIGN KEY (coverage_type_id) REFERENCES coverage_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_vehicle_age_factor (
        program_id, 
        age_category_id, 
        coverage_type_id, 
        effective_date
    ),
    INDEX idx_program_age_factors (program_id, age_category_id),
    INDEX idx_coverage_age_factors (coverage_type_id, age_category_id),
    INDEX idx_physical_damage_factors (applies_to_physical_damage, age_category_id),
    INDEX idx_effective_dates (effective_date, expiration_date)
);
```

#### vehicle_age_eligibility_rule
```sql
CREATE TABLE vehicle_age_eligibility_rule (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    rule_code VARCHAR(50) NOT NULL,
    rule_name VARCHAR(255) NOT NULL,
    rule_description TEXT,
    age_threshold INT NOT NULL,
    coverage_restriction JSON, -- Array of restricted coverage types
    eligibility_action ENUM('ALLOW', 'RESTRICT', 'DECLINE') NOT NULL,
    exception_criteria JSON, -- Conditions for exceptions
    underwriting_required BOOLEAN DEFAULT FALSE,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_program_age_rule (program_id, rule_code, effective_date),
    INDEX idx_age_threshold (age_threshold, eligibility_action),
    INDEX idx_program_rules (program_id, effective_date)
);

-- Aguila Dorada vehicle age eligibility rules
INSERT INTO vehicle_age_eligibility_rule (program_id, rule_code, rule_name, age_threshold, coverage_restriction, eligibility_action, underwriting_required, effective_date) VALUES
(1, 'PHYSICAL_DAMAGE_AGE_LIMIT', 'Physical Damage Age Limit', 20, '["COMPREHENSIVE", "COLLISION"]', 'RESTRICT', FALSE, '2025-07-15'),
(1, 'ANTIQUE_VEHICLE_RESTRICTION', 'Antique Vehicle Restriction', 25, '["COMPREHENSIVE", "COLLISION"]', 'DECLINE', TRUE, '2025-07-15'),
(1, 'CLASSIC_VEHICLE_EXCEPTION', 'Classic Vehicle Exception', 25, '[]', 'ALLOW', TRUE, '2025-07-15');
```

---

## 4. Business Logic Requirements

### Vehicle Age Calculation Logic
```php
class VehicleAgeService
{
    public function calculateVehicleAge(int $modelYear, Carbon $effectiveDate): int
    {
        // Standard vehicle age calculation: current year - model year
        $currentYear = $effectiveDate->year;
        
        // Handle future model years (next year models)
        if ($modelYear > $currentYear) {
            return 0; // Future model year = 0 age
        }
        
        return $currentYear - $modelYear;
    }
    
    public function calculateVehicleAgeFactor(VehicleAgeData $vehicleData): VehicleAgeFactor
    {
        // 1. Calculate vehicle age
        $vehicleAge = $this->calculateVehicleAge(
            $vehicleData->model_year, 
            $vehicleData->effective_date
        );
        
        // 2. Validate eligibility
        $eligibilityResult = $this->validateVehicleAgeEligibility($vehicleData);
        if (!$eligibilityResult->isEligible()) {
            throw new VehicleAgeEligibilityException($eligibilityResult->getMessage());
        }
        
        // 3. Determine age category
        $ageCategory = $this->determineAgeCategory($vehicleAge);
        
        // 4. Get factor by coverage type
        $factors = $this->getAgeFactorsByCoverage($ageCategory, $vehicleData->coverage_types);
        
        // 5. Apply special considerations
        $adjustedFactors = $this->applySpecialConsiderations($factors, $vehicleData);
        
        return new VehicleAgeFactor([
            'vehicle_id' => $vehicleData->vehicle_id,
            'model_year' => $vehicleData->model_year,
            'vehicle_age' => $vehicleAge,
            'age_category' => $ageCategory,
            'factors_by_coverage' => $adjustedFactors,
            'eligibility_status' => $eligibilityResult->getStatus(),
            'special_considerations' => $this->getSpecialConsiderations($vehicleData)
        ]);
    }
    
    public function determineAgeCategory(int $vehicleAge): string
    {
        $category = DB::table('vehicle_age_category')
            ->where('age_min', '<=', $vehicleAge)
            ->where(function($query) use ($vehicleAge) {
                $query->whereNull('age_max')
                      ->orWhere('age_max', '>=', $vehicleAge);
            })
            ->where('status_id', Status::ACTIVE)
            ->orderBy('age_min')
            ->first();
            
        return $category ? $category->category_code : 'AGE_21_PLUS'; // Default to oldest category
    }
    
    private function getAgeFactorsByCoverage(string $ageCategory, array $coverageTypes): array
    {
        $factors = [];
        
        foreach ($coverageTypes as $coverageType) {
            // Get coverage-specific factor first
            $factor = DB::table('vehicle_age_factor')
                ->join('vehicle_age_category', 'vehicle_age_factor.age_category_id', '=', 'vehicle_age_category.id')
                ->join('coverage_type', 'vehicle_age_factor.coverage_type_id', '=', 'coverage_type.id')
                ->where('vehicle_age_category.category_code', $ageCategory)
                ->where('coverage_type.coverage_code', $coverageType)
                ->where('vehicle_age_factor.program_id', $this->programId)
                ->where('vehicle_age_factor.effective_date', '<=', now())
                ->where(function($query) {
                    $query->whereNull('vehicle_age_factor.expiration_date')
                          ->orWhere('vehicle_age_factor.expiration_date', '>', now());
                })
                ->where('vehicle_age_factor.status_id', Status::ACTIVE)
                ->value('vehicle_age_factor.factor_value');
                
            // Fall back to general factor if no coverage-specific factor
            if (!$factor) {
                $factor = DB::table('vehicle_age_factor')
                    ->join('vehicle_age_category', 'vehicle_age_factor.age_category_id', '=', 'vehicle_age_category.id')
                    ->where('vehicle_age_category.category_code', $ageCategory)
                    ->whereNull('vehicle_age_factor.coverage_type_id') // General factor
                    ->where('vehicle_age_factor.program_id', $this->programId)
                    ->where('vehicle_age_factor.effective_date', '<=', now())
                    ->where(function($query) {
                        $query->whereNull('vehicle_age_factor.expiration_date')
                              ->orWhere('vehicle_age_factor.expiration_date', '>', now());
                    })
                    ->where('vehicle_age_factor.status_id', Status::ACTIVE)
                    ->value('vehicle_age_factor.factor_value');
            }
            
            $factors[$coverageType] = $factor ?? 1.0000; // Default to 1.0 if no factor found
        }
        
        return $factors;
    }
}
```

### Eligibility Validation Logic
```php
class VehicleAgeEligibilityService
{
    public function validateVehicleAgeEligibility(VehicleAgeData $vehicleData): ValidationResult
    {
        $result = new ValidationResult();
        $vehicleAge = $this->vehicleAgeService->calculateVehicleAge(
            $vehicleData->model_year, 
            $vehicleData->effective_date
        );
        
        // 1. Check age-based eligibility rules
        $eligibilityRules = DB::table('vehicle_age_eligibility_rule')
            ->where('program_id', $this->programId)
            ->where('age_threshold', '<=', $vehicleAge)
            ->where('effective_date', '<=', now())
            ->where(function($query) {
                $query->whereNull('expiration_date')
                      ->orWhere('expiration_date', '>', now());
            })
            ->where('status_id', Status::ACTIVE)
            ->get();
            
        foreach ($eligibilityRules as $rule) {
            $this->applyEligibilityRule($rule, $vehicleData, $result);
        }
        
        // 2. Check coverage-specific restrictions
        $this->validateCoverageRestrictions($vehicleAge, $vehicleData->coverage_types, $result);
        
        // 3. Check special vehicle type considerations
        $this->validateSpecialVehicleTypes($vehicleData, $result);
        
        return $result;
    }
    
    private function applyEligibilityRule(object $rule, VehicleAgeData $vehicleData, ValidationResult $result): void
    {
        $restrictedCoverages = json_decode($rule->coverage_restriction, true) ?? [];
        
        switch ($rule->eligibility_action) {
            case 'DECLINE':
                if (empty($restrictedCoverages)) {
                    $result->addError("Vehicle age exceeds program eligibility (Rule: {$rule->rule_name})");
                } else {
                    foreach ($restrictedCoverages as $coverage) {
                        if (in_array($coverage, $vehicleData->coverage_types)) {
                            $result->addError("Coverage {$coverage} not available for vehicle age (Rule: {$rule->rule_name})");
                        }
                    }
                }
                break;
                
            case 'RESTRICT':
                foreach ($restrictedCoverages as $coverage) {
                    if (in_array($coverage, $vehicleData->coverage_types)) {
                        $result->addWarning("Coverage {$coverage} restricted for vehicle age (Rule: {$rule->rule_name})");
                    }
                }
                break;
                
            case 'ALLOW':
                // Special allowance rule (e.g., classic vehicle exception)
                if ($rule->underwriting_required) {
                    $result->addWarning("Vehicle requires underwriting review (Rule: {$rule->rule_name})");
                }
                break;
        }
    }
}
```

### Aguila Dorada Age Factor Matrix
```sql
-- Vehicle age factors for Aguila Dorada program
INSERT INTO vehicle_age_factor (program_id, age_category_id, coverage_type_id, factor_value, applies_to_physical_damage, applies_to_liability, effective_date) VALUES
-- General factors (apply to all coverages)
(1, (SELECT id FROM vehicle_age_category WHERE category_code = 'AGE_0_3'), NULL, 1.1000, TRUE, TRUE, '2025-07-15'), -- New vehicles: 10% surcharge
(1, (SELECT id FROM vehicle_age_category WHERE category_code = 'AGE_4_7'), NULL, 1.0000, TRUE, TRUE, '2025-07-15'), -- Modern vehicles: Base rate
(1, (SELECT id FROM vehicle_age_category WHERE category_code = 'AGE_8_12'), NULL, 0.9500, TRUE, TRUE, '2025-07-15'), -- Mature vehicles: 5% discount
(1, (SELECT id FROM vehicle_age_category WHERE category_code = 'AGE_13_15'), NULL, 0.9000, TRUE, TRUE, '2025-07-15'), -- Older vehicles: 10% discount
(1, (SELECT id FROM vehicle_age_category WHERE category_code = 'AGE_16_20'), NULL, 0.8500, TRUE, FALSE, '2025-07-15'), -- Very old: 15% discount liability only

-- Physical damage specific factors (higher variation)
(1, (SELECT id FROM vehicle_age_category WHERE category_code = 'AGE_0_3'), (SELECT id FROM coverage_type WHERE coverage_code = 'COMPREHENSIVE'), 1.2000, TRUE, FALSE, '2025-07-15'),
(1, (SELECT id FROM vehicle_age_category WHERE category_code = 'AGE_0_3'), (SELECT id FROM coverage_type WHERE coverage_code = 'COLLISION'), 1.1500, TRUE, FALSE, '2025-07-15'),
(1, (SELECT id FROM vehicle_age_category WHERE category_code = 'AGE_4_7'), (SELECT id FROM coverage_type WHERE coverage_code = 'COMPREHENSIVE'), 1.0000, TRUE, FALSE, '2025-07-15'),
(1, (SELECT id FROM vehicle_age_category WHERE category_code = 'AGE_4_7'), (SELECT id FROM coverage_type WHERE coverage_code = 'COLLISION'), 1.0000, TRUE, FALSE, '2025-07-15'),
(1, (SELECT id FROM vehicle_age_category WHERE category_code = 'AGE_8_12'), (SELECT id FROM coverage_type WHERE coverage_code = 'COMPREHENSIVE'), 0.8500, TRUE, FALSE, '2025-07-15'),
(1, (SELECT id FROM vehicle_age_category WHERE category_code = 'AGE_8_12'), (SELECT id FROM coverage_type WHERE coverage_code = 'COLLISION'), 0.9000, TRUE, FALSE, '2025-07-15'),
(1, (SELECT id FROM vehicle_age_category WHERE category_code = 'AGE_13_15'), (SELECT id FROM coverage_type WHERE coverage_code = 'COMPREHENSIVE'), 0.7500, TRUE, FALSE, '2025-07-15'),
(1, (SELECT id FROM vehicle_age_category WHERE category_code = 'AGE_13_15'), (SELECT id FROM coverage_type WHERE coverage_code = 'COLLISION'), 0.8000, TRUE, FALSE, '2025-07-15');
```

---

## 5. API Integration Requirements

### Vehicle Age Endpoints
```php
// Vehicle age API endpoints
POST /api/v1/rating/vehicle-age/calculate
{
    "vehicle_data": {
        "vehicle_id": 12345,
        "model_year": 2018,
        "vin": "1HGCM82633A123456",
        "coverage_types": ["LIABILITY", "COMPREHENSIVE", "COLLISION"]
    },
    "effective_date": "2025-07-15"
}

GET /api/v1/rating/vehicle-age/eligibility-check/{modelYear}
// Check eligibility for specific model year

POST /api/v1/rating/vehicle-age/verify-model-year
{
    "vin": "1HGCM82633A123456"
}
// Verify model year through VIN decoding

GET /api/v1/rating/vehicle-age/categories
// Returns vehicle age categories and thresholds
```

### Response Format
```json
{
    "vehicle_id": 12345,
    "model_year": 2018,
    "vehicle_age": 7,
    "age_category": {
        "category_code": "AGE_4_7",
        "category_name": "Modern (4-7 years)",
        "risk_level": "MODERATE"
    },
    "age_factors": {
        "LIABILITY": 1.0000,
        "COMPREHENSIVE": 1.0000,
        "COLLISION": 1.0000
    },
    "eligibility": {
        "eligible": true,
        "restrictions": [],
        "warnings": [],
        "underwriting_required": false
    },
    "verification": {
        "model_year_verified": true,
        "vin_decoded": true,
        "verification_source": "VIN_DECODE"
    },
    "risk_assessment": {
        "theft_risk": "MODERATE",
        "repair_cost_risk": "MODERATE",
        "safety_rating": "MODERN_STANDARDS"
    }
}
```

---

## 6. Performance Requirements

### Age Factor Caching
```php
class VehicleAgeService
{
    public function calculateVehicleAgeFactor(VehicleAgeData $vehicleData): VehicleAgeFactor
    {
        // Cache vehicle age factors by model year and program
        $cacheKey = "vehicle_age_factor_{$this->programId}_{$vehicleData->model_year}";
        
        return Cache::remember($cacheKey, 3600, function() use ($vehicleData) {
            return $this->performAgeFactorCalculation($vehicleData);
        });
    }
}
```

### Database Performance
```sql
-- Vehicle age factor lookup optimization
CREATE INDEX idx_vehicle_age_lookup 
ON vehicle_age_factor (
    program_id, 
    age_category_id, 
    coverage_type_id,
    effective_date
) WHERE status_id = 1;

-- Age category lookup optimization
CREATE INDEX idx_age_category_range 
ON vehicle_age_category (age_min, age_max, status_id);
```

---

## 7. Testing Requirements

### Vehicle Age Factor Testing
```php
class VehicleAgeServiceTest extends TestCase
{
    public function test_new_vehicle_surcharge()
    {
        $vehicleData = new VehicleAgeData([
            'model_year' => 2025, // Current year + 1
            'effective_date' => Carbon::parse('2025-07-15'),
            'coverage_types' => ['LIABILITY', 'COMPREHENSIVE']
        ]);
        
        $factor = $this->vehicleAgeService->calculateVehicleAgeFactor($vehicleData);
        
        $this->assertEquals(0, $factor->vehicle_age); // Future model year
        $this->assertEquals('AGE_0_3', $factor->age_category);
        $this->assertGreaterThan(1.0, $factor->factors_by_coverage['COMPREHENSIVE']); // New vehicle surcharge
    }
    
    public function test_old_vehicle_physical_damage_restriction()
    {
        $vehicleData = new VehicleAgeData([
            'model_year' => 2000, // 25 years old
            'effective_date' => Carbon::parse('2025-07-15'),
            'coverage_types' => ['LIABILITY', 'COMPREHENSIVE', 'COLLISION']
        ]);
        
        $eligibility = $this->vehicleAgeService->validateVehicleAgeEligibility($vehicleData);
        
        $this->assertFalse($eligibility->isEligible());
        $this->assertStringContains('Physical Damage', $eligibility->getErrors()[0]);
    }
    
    public function test_mature_vehicle_discount()
    {
        $vehicleData = new VehicleAgeData([
            'model_year' => 2015, // 10 years old
            'effective_date' => Carbon::parse('2025-07-15'),
            'coverage_types' => ['LIABILITY']
        ]);
        
        $factor = $this->vehicleAgeService->calculateVehicleAgeFactor($vehicleData);
        
        $this->assertEquals(10, $factor->vehicle_age);
        $this->assertEquals('AGE_8_12', $factor->age_category);
        $this->assertLessThan(1.0, $factor->factors_by_coverage['LIABILITY']); // Discount for mature vehicle
    }
}
```

---

## Implementation Priority: HIGH
This factor is essential for proper vehicle risk assessment and should be implemented early in vehicle factor development.

## Dependencies
- **VIN Decoding Integration**: Model year verification through VIN services
- **Vehicle Base Rates**: Age factors apply to base vehicle rates

## Estimated Implementation Effort
- **Database Schema**: 3 days
- **Service Layer**: 4 days
- **VIN Integration**: 2 days
- **Eligibility Logic**: 2 days
- **API Integration**: 2 days
- **Testing**: 3 days
- **Total**: 16 days

This plan implements comprehensive vehicle age assessment while maintaining proper eligibility validation and risk-based pricing adjustments that reflect the changing risk characteristics of vehicles as they age.