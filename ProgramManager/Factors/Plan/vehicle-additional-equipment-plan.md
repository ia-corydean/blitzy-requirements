# Vehicle Additional Equipment Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Vehicle Additional Equipment Coverage (AEC)  
**Category**: Vehicle Factor  
**Priority**: Low - Optional coverage for specific vehicle types  
**Implementation Complexity**: Medium  

### Business Requirements Summary
The Vehicle Additional Equipment Coverage (AEC) factor implements stated amount coverage for aftermarket equipment, modifications, and customizations on eligible commercial-type vehicles. This coverage provides protection for additional equipment not included in the base vehicle value, with coverage limits from $100 to $3,000 and rating based on stated amount methodology.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing and new Global Requirements:

#### Leverages GR-65: Rating Engine Architecture
**Integration**: AEC coverage calculation within multiplicative rating engine  
**Dependencies**: RatingEngineService for stated amount-based premium calculation

#### New Requirement: GR-90: Additional Equipment Coverage Standards
**Priority**: Low  
**Rationale**: Stated amount coverage methodology for aftermarket vehicle equipment  

**Core Components**:
- Additional equipment coverage eligibility and qualification standards
- Stated amount coverage structure and limit management
- Equipment valuation and coverage coordination methodology
- Deductible alignment with base physical damage coverage
- Vehicle type eligibility and coverage dependency requirements
- Aftermarket equipment classification and coverage scope definition

#### Leverages GR-87: Deductible Management Standards
**Integration**: AEC deductible coordination with base comprehensive and collision coverage  
**Dependencies**: Deductible consistency requirements and validation

### Integration with Existing Global Requirements
- **GR-41**: Table Schema Requirements - Additional equipment coverage and limit tracking
- **GR-20**: Application Business Logic - Coverage eligibility and validation patterns
- **GR-04**: Validation & Data Handling - Vehicle type validation and coverage prerequisites

---

## 2. Service Architecture Requirements

### Additional Equipment Coverage Services

#### VehicleAdditionalEquipmentService
**Purpose**: AEC coverage calculation and equipment management  
**Location**: `app/Domain/Rating/Services/VehicleAdditionalEquipmentService.php`

**Key Methods**:
```php
class VehicleAdditionalEquipmentService
{
    public function calculateAECPremium(AECCoverageData $aecData): AECPremiumResult
    {
        // 1. Validate vehicle eligibility for AEC coverage
        // 2. Verify physical damage coverage prerequisites
        // 3. Calculate premium using stated amount formula
        // 4. Apply payment plan and term factors
        // 5. Return premium with detailed breakdown
    }
    
    public function validateAECEligibility(VehicleData $vehicleData): AECEligibilityResult
    {
        // Validate vehicle type and coverage eligibility for AEC
    }
    
    public function getAvailableLimits(VehicleData $vehicleData): array
    {
        // Get available AEC limit options for eligible vehicle
    }
    
    public function validateDeductibleAlignment(AECCoverageData $aecData): DeductibleValidationResult
    {
        // Validate AEC deductibles match base coverage deductibles
    }
}
```

#### AdditionalEquipmentValidationService
**Purpose**: Equipment coverage validation and business rule enforcement  
**Location**: `app/Domain/Rating/Services/AdditionalEquipmentValidationService.php`

**Key Methods**:
```php
class AdditionalEquipmentValidationService
{
    public function validateVehicleType(VehicleData $vehicleData): VehicleTypeValidation
    {
        // Validate vehicle type qualifies for AEC (panel truck, pickup, van)
    }
    
    public function validatePhysicalDamageCoverage(array $coverageTypes): PhysicalDamageValidation
    {
        // Validate required comprehensive and/or collision coverage exists
    }
    
    public function validateCoverageLimit(int $requestedLimit): LimitValidation
    {
        // Validate requested limit within allowable range and increments
    }
}
```

---

## 3. Database Schema Requirements

### Additional Equipment Coverage Tables

#### aec_coverage_option
```sql
CREATE TABLE aec_coverage_option (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    coverage_limit INT NOT NULL,
    minimum_limit INT NOT NULL DEFAULT 100,
    maximum_limit INT NOT NULL DEFAULT 3000,
    increment_amount INT NOT NULL DEFAULT 100,
    base_rate DECIMAL(10,4) NOT NULL,
    coverage_description TEXT,
    display_order INT DEFAULT 0,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_program_limit (program_id, coverage_limit, effective_date),
    INDEX idx_program_coverage_limits (program_id, coverage_limit),
    INDEX idx_limit_range (minimum_limit, maximum_limit, increment_amount),
    INDEX idx_effective_dates (effective_date, expiration_date)
);

-- Generate AEC coverage options for $100 to $3,000 in $100 increments
-- This would be populated with all available limit options
INSERT INTO aec_coverage_option (program_id, coverage_limit, base_rate, effective_date) VALUES
(1, 100, 25.00, '2025-07-15'),
(1, 200, 25.00, '2025-07-15'),
(1, 300, 25.00, '2025-07-15'),
-- ... continue for all increments up to 3000
(1, 3000, 25.00, '2025-07-15');
```

#### aec_vehicle_eligibility
```sql
CREATE TABLE aec_vehicle_eligibility (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    vehicle_type_code VARCHAR(50) NOT NULL,
    vehicle_type_name VARCHAR(255) NOT NULL,
    vehicle_description TEXT,
    eligibility_status ENUM('ELIGIBLE', 'CONDITIONAL', 'INELIGIBLE') NOT NULL,
    required_coverage_types JSON, -- Array of required physical damage coverage types
    coverage_notes TEXT,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_program_vehicle_type (program_id, vehicle_type_code, effective_date),
    INDEX idx_vehicle_type_eligibility (vehicle_type_code, eligibility_status),
    INDEX idx_program_eligibility (program_id, eligibility_status)
);

-- AEC eligible vehicle types for Aguila Dorada
INSERT INTO aec_vehicle_eligibility (program_id, vehicle_type_code, vehicle_type_name, eligibility_status, required_coverage_types, coverage_notes, effective_date) VALUES
(1, 'PANEL_TRUCK', 'Panel Truck', 'ELIGIBLE', '["COMP", "COLL"]', 'Commercial panel trucks with physical damage coverage', '2025-07-15'),
(1, 'PICKUP_TRUCK', 'Pickup Truck', 'ELIGIBLE', '["COMP", "COLL"]', 'Pickup trucks with comprehensive and/or collision coverage', '2025-07-15'),
(1, 'VAN', 'Van', 'ELIGIBLE', '["COMP", "COLL"]', 'Vans with existing physical damage coverage', '2025-07-15'),
(1, 'SEDAN', 'Sedan', 'INELIGIBLE', '[]', 'Passenger cars not eligible for AEC coverage', '2025-07-15'),
(1, 'SUV', 'SUV', 'INELIGIBLE', '[]', 'Standard SUVs not eligible for AEC coverage', '2025-07-15');
```

#### vehicle_aec_coverage
```sql
CREATE TABLE vehicle_aec_coverage (
    id BIGINT PRIMARY KEY,
    vehicle_id BIGINT NOT NULL,
    policy_id BIGINT NOT NULL,
    coverage_limit INT NOT NULL,
    coverage_premium DECIMAL(10,2) NOT NULL,
    comprehensive_deductible INT,
    collision_deductible INT,
    equipment_description TEXT,
    equipment_value_estimate DECIMAL(10,2),
    equipment_categories JSON, -- Array of equipment types covered
    coverage_effective_date DATE NOT NULL,
    coverage_expiration_date DATE,
    endorsement_number VARCHAR(100),
    base_rate_used DECIMAL(10,4),
    calculation_factors JSON, -- Payment plan, term factors applied
    premium_calculation_details TEXT,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(id),
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_vehicle_aec_coverage (vehicle_id, coverage_effective_date),
    INDEX idx_policy_aec_coverage (policy_id, coverage_effective_date),
    INDEX idx_coverage_limit (coverage_limit, coverage_premium),
    INDEX idx_current_coverage (vehicle_id, coverage_expiration_date) -- For current coverage lookup
);
```

#### aec_equipment_category
```sql
CREATE TABLE aec_equipment_category (
    id BIGINT PRIMARY KEY,
    category_code VARCHAR(50) UNIQUE NOT NULL,
    category_name VARCHAR(255) NOT NULL,
    category_description TEXT,
    equipment_examples JSON, -- Array of typical equipment in this category
    coverage_notes TEXT,
    valuation_guidelines TEXT,
    documentation_requirements TEXT,
    display_order INT DEFAULT 0,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_category_code (category_code, status_id),
    INDEX idx_display_order (display_order, status_id)
);

-- Equipment categories for AEC coverage
INSERT INTO aec_equipment_category (category_code, category_name, equipment_examples, coverage_notes, effective_date) VALUES
('AUDIO_VIDEO', 'Audio/Video Equipment', '["Custom stereo systems", "GPS navigation", "Backup cameras", "Entertainment systems"]', 'Aftermarket audio and video equipment installations', '2025-07-15'),
('TOOL_STORAGE', 'Tool Storage Equipment', '["Tool boxes", "Ladder racks", "Storage compartments", "Cargo organizers"]', 'Professional tool storage and organization equipment', '2025-07-15'),
('LIGHTING', 'Lighting Equipment', '["LED light bars", "Work lights", "Emergency lighting", "Custom headlights"]', 'Aftermarket lighting modifications and additions', '2025-07-15'),
('PERFORMANCE', 'Performance Modifications', '["Cold air intakes", "Exhaust systems", "Suspension modifications", "Engine tuning"]', 'Performance enhancement equipment and modifications', '2025-07-15'),
('COMMUNICATION', 'Communication Equipment', '["Two-way radios", "CB radios", "Antenna systems", "Mobile communication"]', 'Professional communication equipment installations', '2025-07-15'),
('SAFETY', 'Safety Equipment', '["Roll bars", "Safety lighting", "Backup alarms", "Safety accessories"]', 'Additional safety equipment and modifications', '2025-07-15');
```

---

## 4. Business Logic Requirements

### AEC Premium Calculation Logic
```php
class VehicleAdditionalEquipmentService
{
    public function calculateAECPremium(AECCoverageData $aecData): AECPremiumResult
    {
        // 1. Validate vehicle eligibility
        $eligibilityResult = $this->validateAECEligibility($aecData->vehicle_data);
        if (!$eligibilityResult->isEligible()) {
            throw new AECEligibilityException($eligibilityResult->getMessage());
        }
        
        // 2. Validate coverage limit
        $limitValidation = $this->validateCoverageLimit($aecData->coverage_limit);
        if (!$limitValidation->isValid()) {
            throw new AECLimitException($limitValidation->getMessage());
        }
        
        // 3. Get base rate for AEC coverage
        $baseRate = $this->getAECBaseRate();
        
        // 4. Calculate limit factor (Coverage Limit ÷ 100)
        $limitFactor = $aecData->coverage_limit / 100;
        
        // 5. Calculate base premium
        $basePremium = $limitFactor * $baseRate;
        
        // 6. Apply additional factors (payment plan, term)
        $paymentPlanFactor = $aecData->payment_plan_factor ?? 1.0000;
        $termFactor = $aecData->term_factor ?? 1.0000;
        
        // 7. Calculate final premium
        $finalPremium = $basePremium * $paymentPlanFactor * $termFactor;
        
        // 8. Validate deductible alignment
        $deductibleValidation = $this->validateDeductibleAlignment($aecData);
        
        return new AECPremiumResult([
            'vehicle_id' => $aecData->vehicle_id,
            'coverage_limit' => $aecData->coverage_limit,
            'base_rate' => $baseRate,
            'limit_factor' => $limitFactor,
            'base_premium' => $basePremium,
            'payment_plan_factor' => $paymentPlanFactor,
            'term_factor' => $termFactor,
            'final_premium' => $finalPremium,
            'deductible_alignment' => $deductibleValidation,
            'calculation_breakdown' => [
                'formula' => '((Coverage Limit ÷ 100) × Base Rate) × Payment Plan × Term',
                'step_1' => "({$aecData->coverage_limit} ÷ 100) = {$limitFactor}",
                'step_2' => "{$limitFactor} × {$baseRate} = {$basePremium}",
                'step_3' => "{$basePremium} × {$paymentPlanFactor} × {$termFactor} = {$finalPremium}"
            ]
        ]);
    }
    
    private function getAECBaseRate(): float
    {
        $baseRate = DB::table('aec_coverage_option')
            ->where('program_id', $this->programId)
            ->where('effective_date', '<=', now())
            ->where(function($query) {
                $query->whereNull('expiration_date')
                      ->orWhere('expiration_date', '>', now());
            })
            ->where('status_id', Status::ACTIVE)
            ->value('base_rate');
            
        return $baseRate ?? 25.00; // Default base rate if not found
    }
    
    public function validateAECEligibility(VehicleData $vehicleData): AECEligibilityResult
    {
        $result = new AECEligibilityResult();
        
        // 1. Check vehicle type eligibility
        $vehicleTypeEligibility = DB::table('aec_vehicle_eligibility')
            ->where('program_id', $this->programId)
            ->where('vehicle_type_code', $vehicleData->vehicle_type_code)
            ->where('effective_date', '<=', now())
            ->where(function($query) {
                $query->whereNull('expiration_date')
                      ->orWhere('expiration_date', '>', now());
            })
            ->where('status_id', Status::ACTIVE)
            ->first();
            
        if (!$vehicleTypeEligibility || $vehicleTypeEligibility->eligibility_status === 'INELIGIBLE') {
            $result->addError("Vehicle type {$vehicleData->vehicle_type_code} is not eligible for AEC coverage");
            return $result;
        }
        
        // 2. Check physical damage coverage requirements
        $requiredCoverages = json_decode($vehicleTypeEligibility->required_coverage_types, true) ?? [];
        $hasRequiredCoverage = false;
        
        foreach ($requiredCoverages as $requiredCoverage) {
            if (in_array($requiredCoverage, $vehicleData->coverage_types)) {
                $hasRequiredCoverage = true;
                break;
            }
        }
        
        if (!$hasRequiredCoverage) {
            $result->addError("AEC coverage requires comprehensive and/or collision coverage");
            return $result;
        }
        
        $result->setEligible(true);
        $result->setVehicleTypeEligibility($vehicleTypeEligibility);
        
        return $result;
    }
    
    public function validateDeductibleAlignment(AECCoverageData $aecData): DeductibleValidationResult
    {
        $result = new DeductibleValidationResult();
        
        // AEC deductibles must match base comprehensive and collision deductibles
        if ($aecData->comprehensive_deductible && $aecData->base_comprehensive_deductible) {
            if ($aecData->comprehensive_deductible !== $aecData->base_comprehensive_deductible) {
                $result->addError("AEC comprehensive deductible must match base comprehensive deductible");
            }
        }
        
        if ($aecData->collision_deductible && $aecData->base_collision_deductible) {
            if ($aecData->collision_deductible !== $aecData->base_collision_deductible) {
                $result->addError("AEC collision deductible must match base collision deductible");
            }
        }
        
        return $result;
    }
}
```

### Coverage Limit Validation Logic
```php
class AdditionalEquipmentValidationService
{
    public function validateCoverageLimit(int $requestedLimit): LimitValidation
    {
        $result = new LimitValidation();
        
        // Check minimum and maximum limits
        if ($requestedLimit < 100) {
            $result->addError("AEC coverage limit cannot be less than $100");
            return $result;
        }
        
        if ($requestedLimit > 3000) {
            $result->addError("AEC coverage limit cannot exceed $3,000");
            return $result;
        }
        
        // Check increment requirement ($100 increments)
        if ($requestedLimit % 100 !== 0) {
            $result->addError("AEC coverage limit must be in $100 increments");
            return $result;
        }
        
        // Verify limit is available in system
        $limitAvailable = DB::table('aec_coverage_option')
            ->where('program_id', $this->programId)
            ->where('coverage_limit', $requestedLimit)
            ->where('effective_date', '<=', now())
            ->where(function($query) {
                $query->whereNull('expiration_date')
                      ->orWhere('expiration_date', '>', now());
            })
            ->where('status_id', Status::ACTIVE)
            ->exists();
            
        if (!$limitAvailable) {
            $result->addError("Requested AEC limit ${requestedLimit} is not available");
            return $result;
        }
        
        $result->setValid(true);
        return $result;
    }
}
```

---

## 5. API Integration Requirements

### AEC Coverage Endpoints
```php
// AEC coverage API endpoints
POST /api/v1/rating/aec/calculate
{
    "aec_coverage_data": {
        "vehicle_id": 12345,
        "coverage_limit": 1500,
        "vehicle_data": {
            "vehicle_type_code": "PICKUP_TRUCK",
            "coverage_types": ["COMP", "COLL"]
        },
        "payment_plan_factor": 1.0400,
        "term_factor": 1.0000,
        "base_comprehensive_deductible": 500,
        "base_collision_deductible": 500
    }
}

GET /api/v1/rating/aec/eligibility/{vehicleId}
// Check AEC eligibility for specific vehicle

GET /api/v1/rating/aec/limits
// Get available AEC coverage limit options

POST /api/v1/rating/aec/validate-limit
{
    "coverage_limit": 1500
}
// Validate requested coverage limit

GET /api/v1/rating/aec/equipment-categories
// Get available equipment categories for AEC coverage
```

### Response Format
```json
{
    "vehicle_id": 12345,
    "aec_premium_result": {
        "coverage_limit": 1500,
        "annual_premium": 390.00,
        "base_rate": 25.00,
        "limit_factor": 15.0,
        "calculation_breakdown": {
            "formula": "((Coverage Limit ÷ 100) × Base Rate) × Payment Plan × Term",
            "step_1": "(1500 ÷ 100) = 15.0",
            "step_2": "15.0 × 25.00 = 375.00",
            "step_3": "375.00 × 1.0400 × 1.0000 = 390.00"
        }
    },
    "eligibility": {
        "eligible": true,
        "vehicle_type": "PICKUP_TRUCK",
        "required_coverage_met": true,
        "physical_damage_coverage": ["COMP", "COLL"]
    },
    "deductible_alignment": {
        "valid": true,
        "comprehensive_deductible": 500,
        "collision_deductible": 500,
        "alignment_status": "MATCHED"
    },
    "coverage_details": {
        "minimum_limit": 100,
        "maximum_limit": 3000,
        "increment_amount": 100,
        "available_limits": [100, 200, 300, "...", 3000],
        "coverage_basis": "STATED_AMOUNT"
    }
}
```

---

## 6. Performance Requirements

### AEC Coverage Caching
```php
class VehicleAdditionalEquipmentService
{
    public function calculateAECPremium(AECCoverageData $aecData): AECPremiumResult
    {
        // Cache AEC base rates and eligibility rules
        $cacheKey = "aec_base_rate_{$this->programId}";
        
        $baseRate = Cache::remember($cacheKey, 3600, function() {
            return $this->getAECBaseRate();
        });
        
        return $this->performAECCalculation($aecData, $baseRate);
    }
}
```

### Database Performance
```sql
-- AEC eligibility lookup optimization
CREATE INDEX idx_aec_eligibility_lookup 
ON aec_vehicle_eligibility (
    program_id, 
    vehicle_type_code, 
    eligibility_status,
    effective_date
) WHERE status_id = 1;

-- Coverage limit lookup optimization
CREATE INDEX idx_aec_limit_lookup 
ON aec_coverage_option (
    program_id, 
    coverage_limit,
    effective_date
) WHERE status_id = 1;

-- Vehicle AEC coverage lookup
CREATE INDEX idx_vehicle_aec_lookup 
ON vehicle_aec_coverage (
    vehicle_id, 
    coverage_effective_date, 
    coverage_expiration_date
) WHERE status_id = 1;
```

---

## 7. Testing Requirements

### AEC Coverage Testing
```php
class VehicleAdditionalEquipmentServiceTest extends TestCase
{
    public function test_eligible_vehicle_aec_calculation()
    {
        $aecData = new AECCoverageData([
            'vehicle_id' => 12345,
            'coverage_limit' => 1000,
            'vehicle_data' => new VehicleData([
                'vehicle_type_code' => 'PICKUP_TRUCK',
                'coverage_types' => ['COMP', 'COLL']
            ])
        ]);
        
        $result = $this->aecService->calculateAECPremium($aecData);
        
        $this->assertEquals(1000, $result->coverage_limit);
        $this->assertEquals(10.0, $result->limit_factor); // 1000 ÷ 100
        $this->assertEquals(250.00, $result->base_premium); // 10.0 × 25.00
    }
    
    public function test_ineligible_vehicle_type()
    {
        $aecData = new AECCoverageData([
            'vehicle_data' => new VehicleData([
                'vehicle_type_code' => 'SEDAN',
                'coverage_types' => ['COMP', 'COLL']
            ])
        ]);
        
        $this->expectException(AECEligibilityException::class);
        $this->aecService->calculateAECPremium($aecData);
    }
    
    public function test_missing_physical_damage_coverage()
    {
        $aecData = new AECCoverageData([
            'vehicle_data' => new VehicleData([
                'vehicle_type_code' => 'PICKUP_TRUCK',
                'coverage_types' => ['BI', 'PD'] // No COMP/COLL
            ])
        ]);
        
        $this->expectException(AECEligibilityException::class);
        $this->aecService->calculateAECPremium($aecData);
    }
    
    public function test_invalid_coverage_limit()
    {
        $aecData = new AECCoverageData([
            'coverage_limit' => 1550, // Not in $100 increments
            'vehicle_data' => new VehicleData([
                'vehicle_type_code' => 'PICKUP_TRUCK',
                'coverage_types' => ['COMP', 'COLL']
            ])
        ]);
        
        $this->expectException(AECLimitException::class);
        $this->aecService->calculateAECPremium($aecData);
    }
    
    public function test_deductible_alignment_validation()
    {
        $aecData = new AECCoverageData([
            'coverage_limit' => 1000,
            'comprehensive_deductible' => 500,
            'base_comprehensive_deductible' => 250, // Mismatch
            'vehicle_data' => new VehicleData([
                'vehicle_type_code' => 'PICKUP_TRUCK',
                'coverage_types' => ['COMP', 'COLL']
            ])
        ]);
        
        $result = $this->aecService->calculateAECPremium($aecData);
        
        $this->assertFalse($result->deductible_alignment->isValid());
        $this->assertStringContains('must match base', $result->deductible_alignment->getErrors()[0]);
    }
}
```

---

## Implementation Priority: LOW
This factor provides optional coverage for specific vehicle types and can be implemented after core rating factors are operational.

## Dependencies
- **Vehicle Type Classification**: Accurate vehicle type identification for eligibility
- **Physical Damage Coverage**: Comprehensive and collision coverage as prerequisites
- **Deductible Management**: Alignment with base coverage deductibles
- **Endorsement System**: Policy endorsement processing capabilities

## Estimated Implementation Effort
- **Database Schema**: 3 days
- **Service Layer**: 4 days
- **Eligibility Validation**: 2 days
- **Premium Calculation**: 2 days
- **API Integration**: 2 days
- **Testing**: 2 days
- **Total**: 15 days

This plan implements comprehensive additional equipment coverage with proper eligibility validation, stated amount calculation methodology, and deductible coordination while maintaining clear business rules for commercial-type vehicle coverage needs.