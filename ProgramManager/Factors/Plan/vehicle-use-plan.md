# Vehicle Use Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Vehicle Use  
**Category**: Vehicle Factor  
**Priority**: High - Primary vehicle usage classification  
**Implementation Complexity**: Medium  

### Business Requirements Summary
The Vehicle Use factor implements risk-based pricing adjustments based on the primary use classification of insured vehicles. This factor assesses exposure risk based on how vehicles are primarily used (pleasure, commuting, business, farm, etc.), reflecting the correlation between usage patterns and claim frequency, mileage exposure, and operational risk characteristics.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing and new Global Requirements:

#### Leverages GR-65: Rating Engine Architecture
**Integration**: Vehicle use factor calculation within multiplicative rating engine  
**Dependencies**: RatingEngineService for usage-based factor lookup and validation

#### Leverages GR-82: Vehicle Characteristics Assessment Standards
**Integration**: Vehicle usage as key characteristic for risk assessment  
**Dependencies**: Usage classification and risk correlation methodology

#### New Requirement: GR-83: Vehicle Usage Classification Standards
**Priority**: Medium  
**Rationale**: Vehicle usage classification and exposure risk assessment standards  

**Core Components**:
- Vehicle use classification methodology and definitions
- Exposure risk correlation based on usage patterns
- Mileage and operational risk assessment standards
- Business use validation and commercial classification rules
- Usage change tracking and effective date management

### Integration with Existing Global Requirements
- **GR-41**: Table Schema Requirements - Vehicle use classification table structures
- **GR-20**: Application Business Logic - Usage classification service patterns
- **GR-04**: Validation & Data Handling - Usage validation and verification patterns

---

## 2. Service Architecture Requirements

### Vehicle Usage Classification Services

#### VehicleUseService
**Purpose**: Vehicle usage classification and factor determination  
**Location**: `app/Domain/Rating/Services/VehicleUseService.php`

**Key Methods**:
```php
class VehicleUseService
{
    public function calculateVehicleUseFactor(VehicleUseData $useData): VehicleUseFactor
    {
        // 1. Validate usage classification and business rules
        // 2. Assess exposure risk based on usage type
        // 3. Apply mileage-based adjustments if applicable
        // 4. Lookup usage-specific factor from factor table
        // 5. Return factor with usage breakdown and risk assessment
    }
    
    public function classifyVehicleUse(VehicleUseData $useData): VehicleUseClassification
    {
        // Classify vehicle use into standard rating categories
    }
    
    public function validateUsageEligibility(VehicleUseData $useData): ValidationResult
    {
        // Validate usage type meets program eligibility requirements
    }
    
    public function assessExposureRisk(string $useType, ?int $annualMileage): ExposureRiskAssessment
    {
        // Assess exposure risk based on usage and mileage
    }
}
```

#### UsageValidationService
**Purpose**: Vehicle usage validation and business rule enforcement  
**Location**: `app/Domain/Rating/Services/UsageValidationService.php`

**Key Methods**:
```php
class UsageValidationService
{
    public function validateBusinessUse(VehicleUseData $useData): ValidationResult
    {
        // Validate business use classification and requirements
    }
    
    public function validateCommutingDistance(VehicleUseData $useData): ValidationResult
    {
        // Validate commuting distance and classification thresholds
    }
    
    public function checkCommercialClassificationRequired(VehicleUseData $useData): bool
    {
        // Check if usage requires commercial vehicle classification
    }
}
```

---

## 3. Database Schema Requirements

### Vehicle Use Management Tables

#### vehicle_use_type
```sql
CREATE TABLE vehicle_use_type (
    id BIGINT PRIMARY KEY,
    use_code VARCHAR(50) UNIQUE NOT NULL,
    use_name VARCHAR(255) NOT NULL,
    use_description TEXT,
    use_category ENUM('PERSONAL', 'BUSINESS', 'COMMERCIAL', 'FARM', 'SPECIAL') NOT NULL,
    exposure_level ENUM('LOW', 'MODERATE', 'HIGH', 'VERY_HIGH') NOT NULL,
    base_factor DECIMAL(6,4) NOT NULL DEFAULT 1.0000,
    requires_mileage BOOLEAN DEFAULT FALSE,
    max_annual_mileage INT, -- Maximum allowed annual mileage for this use type
    requires_commercial_coverage BOOLEAN DEFAULT FALSE,
    eligibility_restrictions JSON, -- Array of restrictions or requirements
    documentation_required JSON, -- Required documentation for this use type
    display_order INT DEFAULT 0,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_use_category (use_category, status_id),
    INDEX idx_exposure_level (exposure_level, status_id),
    INDEX idx_commercial_required (requires_commercial_coverage, status_id),
    INDEX idx_display_order (display_order, status_id)
);

-- Aguila Dorada vehicle use types
INSERT INTO vehicle_use_type (use_code, use_name, use_category, exposure_level, base_factor, requires_mileage, max_annual_mileage, requires_commercial_coverage, display_order) VALUES
('PLEASURE', 'Pleasure/Personal Use Only', 'PERSONAL', 'LOW', 0.9000, FALSE, 12000, FALSE, 1),
('COMMUTE_SHORT', 'Commuting (Under 15 miles one way)', 'PERSONAL', 'MODERATE', 1.0000, TRUE, 15000, FALSE, 2),
('COMMUTE_LONG', 'Commuting (15+ miles one way)', 'PERSONAL', 'HIGH', 1.1500, TRUE, 25000, FALSE, 3),
('BUSINESS_OCCASIONAL', 'Business Use (Occasional)', 'BUSINESS', 'MODERATE', 1.2000, TRUE, 20000, FALSE, 4),
('BUSINESS_REGULAR', 'Business Use (Regular)', 'BUSINESS', 'HIGH', 1.4000, TRUE, 30000, FALSE, 5),
('BUSINESS_PRIMARY', 'Business Use (Primary)', 'BUSINESS', 'VERY_HIGH', 1.6000, TRUE, 50000, TRUE, 6),
('FARM_PERSONAL', 'Farm Use (Personal)', 'FARM', 'MODERATE', 1.1000, FALSE, 15000, FALSE, 7),
('FARM_COMMERCIAL', 'Farm Use (Commercial)', 'FARM', 'HIGH', 1.3000, TRUE, 25000, TRUE, 8),
('ARTISAN', 'Artisan/Contractor Use', 'BUSINESS', 'HIGH', 1.3500, TRUE, 30000, FALSE, 9),
('DELIVERY', 'Delivery/Service Use', 'COMMERCIAL', 'VERY_HIGH', 2.0000, TRUE, NULL, TRUE, 10);
```

#### vehicle_use_factor
```sql
CREATE TABLE vehicle_use_factor (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    use_type_id BIGINT NOT NULL,
    coverage_type_id BIGINT, -- NULL for all coverages, specific ID for coverage-specific factors
    mileage_tier_min INT, -- Minimum annual mileage for this tier
    mileage_tier_max INT, -- Maximum annual mileage for this tier
    factor_value DECIMAL(6,4) NOT NULL,
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
    FOREIGN KEY (use_type_id) REFERENCES vehicle_use_type(id),
    FOREIGN KEY (coverage_type_id) REFERENCES coverage_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_vehicle_use_factor (
        program_id, 
        use_type_id, 
        coverage_type_id, 
        mileage_tier_min,
        mileage_tier_max,
        effective_date
    ),
    INDEX idx_program_use_factors (program_id, use_type_id),
    INDEX idx_coverage_use_factors (coverage_type_id, use_type_id),
    INDEX idx_mileage_tiers (mileage_tier_min, mileage_tier_max),
    INDEX idx_effective_dates (effective_date, expiration_date)
);
```

#### vehicle_use_history
```sql
CREATE TABLE vehicle_use_history (
    id BIGINT PRIMARY KEY,
    vehicle_id BIGINT NOT NULL,
    use_type_id BIGINT NOT NULL,
    annual_mileage INT,
    commute_distance_miles INT,
    business_use_percentage DECIMAL(5,2), -- Percentage of time used for business
    business_description TEXT,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    change_reason VARCHAR(255),
    verification_status ENUM('PENDING', 'VERIFIED', 'DISPUTED') NOT NULL DEFAULT 'PENDING',
    verification_date DATE,
    verification_method VARCHAR(100),
    documentation_provided BOOLEAN DEFAULT FALSE,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(id),
    FOREIGN KEY (use_type_id) REFERENCES vehicle_use_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_vehicle_use_history (vehicle_id, effective_date),
    INDEX idx_verification_status (verification_status, verification_date),
    INDEX idx_current_use (vehicle_id, expiration_date) -- For current use lookup
);
```

#### vehicle_use_eligibility_rule
```sql
CREATE TABLE vehicle_use_eligibility_rule (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    rule_code VARCHAR(50) NOT NULL,
    rule_name VARCHAR(255) NOT NULL,
    rule_description TEXT,
    use_type_restriction JSON, -- Array of restricted use types
    mileage_threshold INT,
    eligibility_action ENUM('ALLOW', 'RESTRICT', 'DECLINE', 'REQUIRE_COMMERCIAL') NOT NULL,
    additional_requirements JSON, -- Additional requirements for eligibility
    underwriting_required BOOLEAN DEFAULT FALSE,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_program_use_rule (program_id, rule_code, effective_date),
    INDEX idx_program_rules (program_id, effective_date),
    INDEX idx_eligibility_action (eligibility_action)
);

-- Aguila Dorada vehicle use eligibility rules
INSERT INTO vehicle_use_eligibility_rule (program_id, rule_code, rule_name, use_type_restriction, mileage_threshold, eligibility_action, underwriting_required, effective_date) VALUES
(1, 'COMMERCIAL_USE_RESTRICTION', 'Commercial Use Restriction', '["DELIVERY", "TAXI", "RIDESHARE"]', NULL, 'REQUIRE_COMMERCIAL', TRUE, '2025-07-15'),
(1, 'HIGH_MILEAGE_RESTRICTION', 'High Mileage Restriction', '[]', 50000, 'DECLINE', FALSE, '2025-07-15'),
(1, 'BUSINESS_USE_VERIFICATION', 'Business Use Verification', '["BUSINESS_REGULAR", "BUSINESS_PRIMARY"]', NULL, 'RESTRICT', TRUE, '2025-07-15');
```

---

## 4. Business Logic Requirements

### Vehicle Use Factor Calculation
```php
class VehicleUseService
{
    public function calculateVehicleUseFactor(VehicleUseData $useData): VehicleUseFactor
    {
        // 1. Validate usage classification
        $classification = $this->classifyVehicleUse($useData);
        
        // 2. Validate eligibility
        $eligibilityResult = $this->validateUsageEligibility($useData);
        if (!$eligibilityResult->isEligible()) {
            throw new VehicleUseEligibilityException($eligibilityResult->getMessage());
        }
        
        // 3. Get base usage factor
        $baseFactor = $this->getBaseUsageFactor($classification);
        
        // 4. Apply mileage adjustments if applicable
        $mileageAdjustment = $this->calculateMileageAdjustment($useData);
        
        // 5. Apply coverage-specific factors
        $coverageFactors = $this->getCoverageSpecificFactors($classification, $useData->coverage_types);
        
        // 6. Calculate final factors
        $finalFactors = [];
        foreach ($coverageFactors as $coverage => $factor) {
            $finalFactors[$coverage] = $baseFactor * $mileageAdjustment * $factor;
        }
        
        return new VehicleUseFactor([
            'vehicle_id' => $useData->vehicle_id,
            'use_classification' => $classification,
            'base_factor' => $baseFactor,
            'mileage_adjustment' => $mileageAdjustment,
            'factors_by_coverage' => $finalFactors,
            'exposure_assessment' => $this->assessExposureRisk($classification->use_code, $useData->annual_mileage),
            'eligibility_status' => $eligibilityResult->getStatus()
        ]);
    }
    
    public function classifyVehicleUse(VehicleUseData $useData): VehicleUseClassification
    {
        // Auto-classify based on provided usage data
        
        // Business use classification
        if ($useData->business_use_percentage > 0) {
            if ($useData->business_use_percentage >= 75) {
                return $this->getUseClassification('BUSINESS_PRIMARY');
            } elseif ($useData->business_use_percentage >= 25) {
                return $this->getUseClassification('BUSINESS_REGULAR');
            } else {
                return $this->getUseClassification('BUSINESS_OCCASIONAL');
            }
        }
        
        // Commuting classification
        if ($useData->commute_distance_miles > 0) {
            if ($useData->commute_distance_miles >= 15) {
                return $this->getUseClassification('COMMUTE_LONG');
            } else {
                return $this->getUseClassification('COMMUTE_SHORT');
            }
        }
        
        // Farm use classification
        if ($useData->use_type === 'FARM' && $useData->annual_mileage > 15000) {
            return $this->getUseClassification('FARM_COMMERCIAL');
        } elseif ($useData->use_type === 'FARM') {
            return $this->getUseClassification('FARM_PERSONAL');
        }
        
        // Default to pleasure use
        return $this->getUseClassification('PLEASURE');
    }
    
    private function calculateMileageAdjustment(VehicleUseData $useData): float
    {
        if (!$useData->annual_mileage) {
            return 1.0000; // No adjustment if mileage not provided
        }
        
        // Mileage-based adjustment tiers
        $mileageTiers = [
            7500 => 0.9500,   // Low mileage discount
            12000 => 1.0000,  // Base rate
            20000 => 1.0500,  // Moderate increase
            30000 => 1.1500,  // High mileage surcharge
            50000 => 1.3000,  // Very high mileage surcharge
        ];
        
        $adjustment = 1.0000;
        foreach ($mileageTiers as $threshold => $factor) {
            if ($useData->annual_mileage <= $threshold) {
                $adjustment = $factor;
                break;
            }
        }
        
        // Maximum mileage handling
        if ($useData->annual_mileage > 50000) {
            $adjustment = 1.5000; // Maximum surcharge
        }
        
        return $adjustment;
    }
    
    private function getCoverageSpecificFactors(VehicleUseClassification $classification, array $coverageTypes): array
    {
        $factors = [];
        
        foreach ($coverageTypes as $coverageType) {
            // Get coverage-specific factor
            $factor = DB::table('vehicle_use_factor')
                ->join('vehicle_use_type', 'vehicle_use_factor.use_type_id', '=', 'vehicle_use_type.id')
                ->join('coverage_type', 'vehicle_use_factor.coverage_type_id', '=', 'coverage_type.id')
                ->where('vehicle_use_type.use_code', $classification->use_code)
                ->where('coverage_type.coverage_code', $coverageType)
                ->where('vehicle_use_factor.program_id', $this->programId)
                ->where('vehicle_use_factor.effective_date', '<=', now())
                ->where(function($query) {
                    $query->whereNull('vehicle_use_factor.expiration_date')
                          ->orWhere('vehicle_use_factor.expiration_date', '>', now());
                })
                ->where('vehicle_use_factor.status_id', Status::ACTIVE)
                ->value('vehicle_use_factor.factor_value');
                
            $factors[$coverageType] = $factor ?? $classification->base_factor; // Fall back to base factor
        }
        
        return $factors;
    }
}
```

### Usage Validation Logic
```php
class UsageValidationService
{
    public function validateUsageEligibility(VehicleUseData $useData): ValidationResult
    {
        $result = new ValidationResult();
        
        // 1. Check use type eligibility rules
        $eligibilityRules = DB::table('vehicle_use_eligibility_rule')
            ->where('program_id', $this->programId)
            ->where('effective_date', '<=', now())
            ->where(function($query) {
                $query->whereNull('expiration_date')
                      ->orWhere('expiration_date', '>', now());
            })
            ->where('status_id', Status::ACTIVE)
            ->get();
            
        foreach ($eligibilityRules as $rule) {
            $this->applyEligibilityRule($rule, $useData, $result);
        }
        
        // 2. Validate mileage thresholds
        $this->validateMileageThresholds($useData, $result);
        
        // 3. Validate business use requirements
        if ($useData->business_use_percentage > 0) {
            $this->validateBusinessUseRequirements($useData, $result);
        }
        
        return $result;
    }
    
    private function validateBusinessUseRequirements(VehicleUseData $useData, ValidationResult $result): void
    {
        // Business use over 50% requires commercial coverage consideration
        if ($useData->business_use_percentage >= 50) {
            $result->addWarning('High business use percentage may require commercial auto coverage');
        }
        
        // Certain business types require special handling
        $highRiskBusinessTypes = [
            'DELIVERY', 'TRANSPORTATION', 'RIDESHARE', 'TAXI', 'COURIER'
        ];
        
        if (in_array($useData->business_type, $highRiskBusinessTypes)) {
            $result->addError("Business type {$useData->business_type} requires commercial auto policy");
        }
        
        // Business use requires documentation
        if ($useData->business_use_percentage > 25 && !$useData->business_documentation_provided) {
            $result->addWarning('Business use documentation required for verification');
        }
    }
    
    private function validateMileageThresholds(VehicleUseData $useData, ValidationResult $result): void
    {
        if (!$useData->annual_mileage) {
            return; // No validation needed if mileage not provided
        }
        
        // Program maximum mileage
        if ($useData->annual_mileage > 75000) {
            $result->addError('Annual mileage exceeds program maximum (75,000 miles)');
        }
        
        // High mileage warning
        if ($useData->annual_mileage > 50000) {
            $result->addWarning('High annual mileage may affect coverage options and pricing');
        }
        
        // Unrealistic low mileage
        if ($useData->annual_mileage < 1000 && $useData->use_type !== 'PLEASURE') {
            $result->addWarning('Very low mileage inconsistent with reported use type');
        }
    }
}
```

### Aguila Dorada Use Factor Matrix
```sql
-- Vehicle use factors for Aguila Dorada program
INSERT INTO vehicle_use_factor (program_id, use_type_id, coverage_type_id, mileage_tier_min, mileage_tier_max, factor_value, effective_date) VALUES
-- Pleasure use (baseline)
(1, (SELECT id FROM vehicle_use_type WHERE use_code = 'PLEASURE'), NULL, 0, 12000, 0.9000, '2025-07-15'),

-- Commuting factors
(1, (SELECT id FROM vehicle_use_type WHERE use_code = 'COMMUTE_SHORT'), NULL, 0, 15000, 1.0000, '2025-07-15'),
(1, (SELECT id FROM vehicle_use_type WHERE use_code = 'COMMUTE_LONG'), NULL, 15001, 25000, 1.1500, '2025-07-15'),

-- Business use factors (higher for liability)
(1, (SELECT id FROM vehicle_use_type WHERE use_code = 'BUSINESS_OCCASIONAL'), (SELECT id FROM coverage_type WHERE coverage_code = 'LIABILITY'), 0, 20000, 1.2500, '2025-07-15'),
(1, (SELECT id FROM vehicle_use_type WHERE use_code = 'BUSINESS_OCCASIONAL'), (SELECT id FROM coverage_type WHERE coverage_code = 'COMPREHENSIVE'), 0, 20000, 1.1500, '2025-07-15'),
(1, (SELECT id FROM vehicle_use_type WHERE use_code = 'BUSINESS_OCCASIONAL'), (SELECT id FROM coverage_type WHERE coverage_code = 'COLLISION'), 0, 20000, 1.1500, '2025-07-15'),

(1, (SELECT id FROM vehicle_use_type WHERE use_code = 'BUSINESS_REGULAR'), (SELECT id FROM coverage_type WHERE coverage_code = 'LIABILITY'), 0, 30000, 1.4500, '2025-07-15'),
(1, (SELECT id FROM vehicle_use_type WHERE use_code = 'BUSINESS_REGULAR'), (SELECT id FROM coverage_type WHERE coverage_code = 'COMPREHENSIVE'), 0, 30000, 1.3000, '2025-07-15'),
(1, (SELECT id FROM vehicle_use_type WHERE use_code = 'BUSINESS_REGULAR'), (SELECT id FROM coverage_type WHERE coverage_code = 'COLLISION'), 0, 30000, 1.3000, '2025-07-15'),

-- Farm use factors
(1, (SELECT id FROM vehicle_use_type WHERE use_code = 'FARM_PERSONAL'), NULL, 0, 15000, 1.1000, '2025-07-15'),
(1, (SELECT id FROM vehicle_use_type WHERE use_code = 'FARM_COMMERCIAL'), NULL, 0, 25000, 1.3000, '2025-07-15'),

-- Artisan use factors
(1, (SELECT id FROM vehicle_use_type WHERE use_code = 'ARTISAN'), (SELECT id FROM coverage_type WHERE coverage_code = 'LIABILITY'), 0, 30000, 1.4000, '2025-07-15'),
(1, (SELECT id FROM vehicle_use_type WHERE use_code = 'ARTISAN'), (SELECT id FROM coverage_type WHERE coverage_code = 'COMPREHENSIVE'), 0, 30000, 1.2500, '2025-07-15'),
(1, (SELECT id FROM vehicle_use_type WHERE use_code = 'ARTISAN'), (SELECT id FROM coverage_type WHERE coverage_code = 'COLLISION'), 0, 30000, 1.2500, '2025-07-15');
```

---

## 5. API Integration Requirements

### Vehicle Use Endpoints
```php
// Vehicle use API endpoints
POST /api/v1/rating/vehicle-use/calculate
{
    "vehicle_use_data": {
        "vehicle_id": 12345,
        "use_type": "COMMUTE_SHORT",
        "annual_mileage": 12000,
        "commute_distance_miles": 10,
        "business_use_percentage": 0,
        "coverage_types": ["LIABILITY", "COMPREHENSIVE", "COLLISION"]
    }
}

POST /api/v1/rating/vehicle-use/classify
{
    "usage_details": {
        "commute_distance_miles": 20,
        "business_use_percentage": 15,
        "annual_mileage": 18000,
        "business_type": "SALES"
    }
}
// Auto-classify vehicle use based on usage details

GET /api/v1/rating/vehicle-use/types
// Returns available vehicle use types and descriptions

POST /api/v1/rating/vehicle-use/eligibility-check
{
    "use_type": "BUSINESS_REGULAR",
    "annual_mileage": 35000,
    "business_percentage": 60
}
```

### Response Format
```json
{
    "vehicle_id": 12345,
    "use_classification": {
        "use_code": "COMMUTE_SHORT",
        "use_name": "Commuting (Under 15 miles one way)",
        "use_category": "PERSONAL",
        "exposure_level": "MODERATE"
    },
    "use_factors": {
        "LIABILITY": 1.0000,
        "COMPREHENSIVE": 1.0000,
        "COLLISION": 1.0000
    },
    "mileage_assessment": {
        "annual_mileage": 12000,
        "mileage_tier": "STANDARD",
        "mileage_adjustment": 1.0000
    },
    "exposure_risk": {
        "risk_level": "MODERATE",
        "risk_factors": ["Regular commuting exposure", "Moderate annual mileage"],
        "recommendations": ["Consider usage-based insurance options"]
    },
    "eligibility": {
        "eligible": true,
        "restrictions": [],
        "warnings": [],
        "documentation_required": false
    },
    "business_use_analysis": {
        "business_percentage": 0,
        "requires_commercial_coverage": false,
        "verification_required": false
    }
}
```

---

## 6. Performance Requirements

### Use Factor Caching
```php
class VehicleUseService
{
    public function calculateVehicleUseFactor(VehicleUseData $useData): VehicleUseFactor
    {
        // Cache vehicle use factors by use type and mileage tier
        $mileageTier = $this->getMileageTier($useData->annual_mileage);
        $cacheKey = "vehicle_use_factor_{$this->programId}_{$useData->use_type}_{$mileageTier}";
        
        return Cache::remember($cacheKey, 3600, function() use ($useData) {
            return $this->performUseFactorCalculation($useData);
        });
    }
}
```

### Database Performance
```sql
-- Vehicle use factor lookup optimization
CREATE INDEX idx_vehicle_use_lookup 
ON vehicle_use_factor (
    program_id, 
    use_type_id, 
    coverage_type_id,
    mileage_tier_min,
    mileage_tier_max,
    effective_date
) WHERE status_id = 1;

-- Current vehicle use lookup optimization
CREATE INDEX idx_current_vehicle_use 
ON vehicle_use_history (
    vehicle_id, 
    effective_date, 
    expiration_date
) WHERE status_id = 1 AND expiration_date IS NULL;
```

---

## 7. Testing Requirements

### Vehicle Use Factor Testing
```php
class VehicleUseServiceTest extends TestCase
{
    public function test_pleasure_use_discount()
    {
        $useData = new VehicleUseData([
            'use_type' => 'PLEASURE',
            'annual_mileage' => 8000,
            'business_use_percentage' => 0,
            'coverage_types' => ['LIABILITY']
        ]);
        
        $factor = $this->vehicleUseService->calculateVehicleUseFactor($useData);
        
        $this->assertEquals('PLEASURE', $factor->use_classification->use_code);
        $this->assertLessThan(1.0, $factor->factors_by_coverage['LIABILITY']); // Pleasure discount
    }
    
    public function test_business_use_surcharge()
    {
        $useData = new VehicleUseData([
            'use_type' => 'BUSINESS_REGULAR',
            'annual_mileage' => 25000,
            'business_use_percentage' => 50,
            'coverage_types' => ['LIABILITY', 'COMPREHENSIVE']
        ]);
        
        $factor = $this->vehicleUseService->calculateVehicleUseFactor($useData);
        
        $this->assertEquals('BUSINESS_REGULAR', $factor->use_classification->use_code);
        $this->assertGreaterThan(1.0, $factor->factors_by_coverage['LIABILITY']); // Business surcharge
        $this->assertGreaterThan($factor->factors_by_coverage['COMPREHENSIVE'], $factor->factors_by_coverage['LIABILITY']); // Higher liability surcharge
    }
    
    public function test_high_mileage_restriction()
    {
        $useData = new VehicleUseData([
            'use_type' => 'COMMUTE_LONG',
            'annual_mileage' => 60000, // Above program maximum
            'coverage_types' => ['LIABILITY']
        ]);
        
        $eligibility = $this->vehicleUseService->validateUsageEligibility($useData);
        
        $this->assertFalse($eligibility->isEligible());
        $this->assertStringContains('exceeds program maximum', $eligibility->getErrors()[0]);
    }
    
    public function test_auto_classification()
    {
        $useData = new VehicleUseData([
            'commute_distance_miles' => 20,
            'business_use_percentage' => 10,
            'annual_mileage' => 18000
        ]);
        
        $classification = $this->vehicleUseService->classifyVehicleUse($useData);
        
        $this->assertEquals('COMMUTE_LONG', $classification->use_code); // Should classify as long commute
    }
}
```

---

## Implementation Priority: HIGH
This factor is essential for proper vehicle exposure risk assessment and should be implemented early in vehicle factor development.

## Dependencies
- **Vehicle Age Factor**: Use factors may interact with age-based eligibility
- **Driver Assignment Factor**: Usage applies to assigned vehicles

## Estimated Implementation Effort
- **Database Schema**: 3 days
- **Service Layer**: 4 days
- **Classification Logic**: 3 days
- **Validation Framework**: 2 days
- **API Integration**: 2 days
- **Testing**: 3 days
- **Total**: 17 days

This plan implements comprehensive vehicle usage assessment while maintaining proper classification validation and exposure-based risk pricing that reflects the actual operational patterns of insured vehicles.