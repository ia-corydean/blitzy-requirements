# Vehicle Coverage Type Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Vehicle Coverage Type  
**Category**: Vehicle Factor  
**Priority**: High - Lienholder and fleet-based risk assessment  
**Implementation Complexity**: High  

### Business Requirements Summary
The Vehicle Coverage Type factor implements risk-based pricing adjustments based on the combination of lienholder status and vehicle count on the policy. This factor recognizes the risk differences between financed vs. unfinanced vehicles, the benefits of multi-vehicle policies, and the reduced exposure of liability-only coverage, while incorporating a unique lienholder rate continuation benefit.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing and new Global Requirements:

#### Leverages GR-65: Rating Engine Architecture
**Integration**: Coverage type factor calculation within multiplicative rating engine  
**Dependencies**: RatingEngineService for lienholder status and vehicle count-based factor determination

#### New Requirement: GR-88: Lienholder and Fleet Risk Assessment Standards
**Priority**: High  
**Rationale**: Lienholder status and vehicle count-based risk evaluation for comprehensive pricing  

**Core Components**:
- Lienholder status tracking and risk assessment methodology
- Multi-vehicle fleet effect analysis and discount application
- Coverage election impact assessment (full coverage vs. liability-only)
- Historical lienholder rate continuation management
- Vehicle count-based risk distribution analysis
- Coverage type factor versioning and effective date management

#### Leverages GR-37: Locking & Action Tracking
**Integration**: Lienholder status changes and historical tracking for rate continuation  
**Dependencies**: Historical lienholder status preservation and change audit trails

### Integration with Existing Global Requirements
- **GR-41**: Table Schema Requirements - Lienholder and coverage type factor table structures
- **GR-20**: Application Business Logic - Coverage type classification and factor application patterns
- **GR-04**: Validation & Data Handling - Lienholder status validation and coverage verification

---

## 2. Service Architecture Requirements

### Coverage Type Assessment Services

#### VehicleCoverageTypeService
**Purpose**: Coverage type factor calculation based on lienholder status and vehicle count  
**Location**: `app/Domain/Rating/Services/VehicleCoverageTypeService.php`

**Key Methods**:
```php
class VehicleCoverageTypeService
{
    public function calculateCoverageTypeFactor(VehicleCoverageTypeData $coverageData): CoverageTypeFactor
    {
        // 1. Determine current and historical lienholder status
        // 2. Calculate policy vehicle count and coverage elections
        // 3. Classify coverage type category (Yes/No/LO/Non-Owner)
        // 4. Apply lienholder rate continuation rules if applicable
        // 5. Return factor with detailed breakdown and justification
    }
    
    public function classifyCoverageType(PolicyCoverageData $policyData): CoverageTypeClassification
    {
        // Classify policy into coverage type categories based on lienholder and coverage
    }
    
    public function validateLienholderRateContinuation(VehicleData $vehicleData): LienholderContinuationResult
    {
        // Validate eligibility for continued lienholder rate after payoff
    }
    
    public function calculateFleetEffect(PolicyData $policyData): FleetEffectAnalysis
    {
        // Analyze multi-vehicle benefits and risk distribution
    }
}
```

#### LienholderStatusService
**Purpose**: Lienholder status management and historical tracking  
**Location**: `app/Domain/Rating/Services/LienholderStatusService.php`

**Key Methods**:
```php
class LienholderStatusService
{
    public function getCurrentLienholderStatus(int $vehicleId): LienholderStatus
    {
        // Get current lienholder status for vehicle
    }
    
    public function getHistoricalLienholderStatus(int $vehicleId): Collection
    {
        // Get historical lienholder status for rate continuation analysis
    }
    
    public function trackLienholderChange(LienholderChangeData $changeData): LienholderChangeResult
    {
        // Track lienholder status changes and preserve rate continuation eligibility
    }
    
    public function determineRateContinuationEligibility(int $vehicleId): RateContinuationEligibility
    {
        // Determine if vehicle qualifies for continued lienholder rate
    }
}
```

---

## 3. Database Schema Requirements

### Coverage Type Management Tables

#### coverage_type_classification
```sql
CREATE TABLE coverage_type_classification (
    id BIGINT PRIMARY KEY,
    classification_code VARCHAR(50) UNIQUE NOT NULL,
    classification_name VARCHAR(255) NOT NULL,
    classification_description TEXT,
    lienholder_required BOOLEAN NOT NULL,
    physical_damage_required BOOLEAN NOT NULL,
    vehicle_count_applicable BOOLEAN DEFAULT TRUE,
    risk_level ENUM('LOW', 'STANDARD', 'HIGH') NOT NULL,
    display_order INT DEFAULT 0,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_classification_code (classification_code, status_id),
    INDEX idx_lienholder_physical_damage (lienholder_required, physical_damage_required),
    INDEX idx_risk_level (risk_level, status_id)
);

-- Coverage type classifications for Aguila Dorada
INSERT INTO coverage_type_classification (classification_code, classification_name, lienholder_required, physical_damage_required, risk_level) VALUES
('YES', 'With Lienholder', TRUE, TRUE, 'STANDARD'),
('NO', 'Without Lienholder', FALSE, TRUE, 'HIGH'),
('LO', 'Liability Only', FALSE, FALSE, 'LOW'),
('NON_OWNER', 'Non-Owner Policy', FALSE, FALSE, 'STANDARD');
```

#### vehicle_count_tier
```sql
CREATE TABLE vehicle_count_tier (
    id BIGINT PRIMARY KEY,
    tier_code VARCHAR(50) UNIQUE NOT NULL,
    tier_name VARCHAR(255) NOT NULL,
    vehicle_count_min INT NOT NULL,
    vehicle_count_max INT, -- NULL for open-ended (4+)
    fleet_effect_description TEXT,
    risk_distribution_factor DECIMAL(6,4) DEFAULT 1.0000,
    display_order INT DEFAULT 0,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_vehicle_count_range (vehicle_count_min, vehicle_count_max),
    INDEX idx_tier_code (tier_code, status_id),
    INDEX idx_vehicle_count_range (vehicle_count_min, vehicle_count_max)
);

-- Vehicle count tiers for Aguila Dorada
INSERT INTO vehicle_count_tier (tier_code, tier_name, vehicle_count_min, vehicle_count_max, fleet_effect_description) VALUES
('SINGLE', 'Single Vehicle', 1, 1, 'Individual vehicle - highest risk concentration'),
('TWO', 'Two Vehicles', 2, 2, 'Dual vehicle - moderate risk distribution'),
('THREE', 'Three Vehicles', 3, 3, 'Three vehicle - improved risk distribution'),
('FOUR_PLUS', 'Four or More Vehicles', 4, NULL, 'Fleet - maximum risk distribution benefits');
```

#### coverage_type_factor
```sql
CREATE TABLE coverage_type_factor (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    classification_id BIGINT NOT NULL,
    vehicle_count_tier_id BIGINT NOT NULL,
    factor_value DECIMAL(6,4) NOT NULL,
    factor_type ENUM('SURCHARGE', 'NEUTRAL', 'DISCOUNT') NOT NULL,
    percentage_adjustment DECIMAL(5,2), -- Percentage (e.g., 30.00 for 30% surcharge, -20.00 for 20% discount)
    applies_to_all_coverages BOOLEAN DEFAULT TRUE,
    coverage_type_restrictions JSON, -- Specific coverages if not all
    effective_date DATE NOT NULL,
    expiration_date DATE,
    actuarial_justification TEXT,
    business_rules_notes TEXT,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (classification_id) REFERENCES coverage_type_classification(id),
    FOREIGN KEY (vehicle_count_tier_id) REFERENCES vehicle_count_tier(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_coverage_type_factor (
        program_id, 
        classification_id, 
        vehicle_count_tier_id, 
        effective_date
    ),
    INDEX idx_program_classification_factors (program_id, classification_id),
    INDEX idx_vehicle_count_factors (vehicle_count_tier_id, factor_value),
    INDEX idx_factor_type (factor_type, percentage_adjustment),
    INDEX idx_effective_dates (effective_date, expiration_date)
);
```

#### lienholder_status_history
```sql
CREATE TABLE lienholder_status_history (
    id BIGINT PRIMARY KEY,
    vehicle_id BIGINT NOT NULL,
    policy_id BIGINT NOT NULL,
    lienholder_id BIGINT,
    lienholder_status ENUM('ACTIVE', 'PAID_OFF', 'TRANSFERRED', 'NONE') NOT NULL,
    status_change_date DATE NOT NULL,
    previous_lienholder_id BIGINT,
    rate_continuation_eligible BOOLEAN DEFAULT FALSE,
    rate_continuation_start_date DATE,
    rate_continuation_reason TEXT,
    change_source ENUM('CUSTOMER_REPORT', 'LIENHOLDER_NOTICE', 'SYSTEM_UPDATE', 'UNDERWRITING_REVIEW') NOT NULL,
    verification_status ENUM('PENDING', 'VERIFIED', 'DISPUTED') NOT NULL DEFAULT 'PENDING',
    verification_date DATE,
    documentation_provided BOOLEAN DEFAULT FALSE,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(id),
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (lienholder_id) REFERENCES lienholder(id),
    FOREIGN KEY (previous_lienholder_id) REFERENCES lienholder(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_vehicle_lienholder_history (vehicle_id, status_change_date),
    INDEX idx_rate_continuation_eligible (vehicle_id, rate_continuation_eligible),
    INDEX idx_lienholder_status (lienholder_status, verification_status),
    INDEX idx_change_source (change_source, status_change_date)
);
```

---

## 4. Business Logic Requirements

### Coverage Type Factor Calculation Logic
```php
class VehicleCoverageTypeService
{
    public function calculateCoverageTypeFactor(VehicleCoverageTypeData $coverageData): CoverageTypeFactor
    {
        // 1. Classify coverage type based on lienholder and coverage elections
        $coverageClassification = $this->classifyCoverageType($coverageData);
        
        // 2. Determine vehicle count tier
        $vehicleCountTier = $this->getVehicleCountTier($coverageData->policy_vehicle_count);
        
        // 3. Check for lienholder rate continuation eligibility
        $rateContinuation = $this->validateLienholderRateContinuation($coverageData);
        
        // 4. Get base factor from matrix
        $baseFactor = $this->getCoverageTypeFactor(
            $coverageClassification->classification_id,
            $vehicleCountTier->id
        );
        
        // 5. Apply rate continuation if eligible
        $finalFactor = $this->applyRateContinuation($baseFactor, $rateContinuation);
        
        return new CoverageTypeFactor([
            'vehicle_id' => $coverageData->vehicle_id,
            'policy_id' => $coverageData->policy_id,
            'coverage_classification' => $coverageClassification,
            'vehicle_count_tier' => $vehicleCountTier,
            'base_factor' => $baseFactor,
            'final_factor' => $finalFactor,
            'rate_continuation' => $rateContinuation,
            'fleet_effect_analysis' => $this->calculateFleetEffect($coverageData)
        ]);
    }
    
    public function classifyCoverageType(VehicleCoverageTypeData $coverageData): CoverageTypeClassification
    {
        // Check for non-owner policy first
        if ($coverageData->policy_type === 'NON_OWNER') {
            return $this->getClassification('NON_OWNER');
        }
        
        // Check lienholder status (including rate continuation)
        $currentLienholder = $this->lienholderStatusService->getCurrentLienholderStatus($coverageData->vehicle_id);
        $rateContinuationEligible = $this->lienholderStatusService->determineRateContinuationEligibility($coverageData->vehicle_id);
        
        // If currently has lienholder OR eligible for rate continuation
        if ($currentLienholder->hasActiveLienholder() || $rateContinuationEligible->isEligible()) {
            return $this->getClassification('YES');
        }
        
        // Check for comprehensive and collision coverage
        $hasPhysicalDamage = $this->hasComprehensiveAndCollision($coverageData->coverage_elections);
        
        if ($hasPhysicalDamage) {
            return $this->getClassification('NO'); // No lienholder but has physical damage
        } else {
            return $this->getClassification('LO'); // Liability only
        }
    }
    
    private function getCoverageTypeFactor(int $classificationId, int $vehicleCountTierId): float
    {
        $factor = DB::table('coverage_type_factor')
            ->where('program_id', $this->programId)
            ->where('classification_id', $classificationId)
            ->where('vehicle_count_tier_id', $vehicleCountTierId)
            ->where('effective_date', '<=', now())
            ->where(function($query) {
                $query->whereNull('expiration_date')
                      ->orWhere('expiration_date', '>', now());
            })
            ->where('status_id', Status::ACTIVE)
            ->value('factor_value');
            
        return $factor ?? 1.0000; // Default to neutral if not found
    }
    
    private function applyRateContinuation(float $baseFactor, LienholderContinuationResult $rateContinuation): float
    {
        // If eligible for rate continuation and current factor is higher than lienholder rate
        if ($rateContinuation->isEligible()) {
            $lienholderFactor = 1.0000; // Lienholder rate is always 1.0000
            
            // Use the more favorable rate (lower factor)
            return min($baseFactor, $lienholderFactor);
        }
        
        return $baseFactor;
    }
}
```

### Lienholder Rate Continuation Logic
```php
class LienholderStatusService
{
    public function determineRateContinuationEligibility(int $vehicleId): RateContinuationEligibility
    {
        // Get historical lienholder status
        $lienholderHistory = DB::table('lienholder_status_history')
            ->where('vehicle_id', $vehicleId)
            ->where('status_id', Status::ACTIVE)
            ->orderBy('status_change_date', 'desc')
            ->get();
            
        // Check if vehicle ever had a lienholder
        $hadLienholder = $lienholderHistory->where('lienholder_status', 'ACTIVE')->isNotEmpty();
        
        if (!$hadLienholder) {
            return new RateContinuationEligibility([
                'eligible' => false,
                'reason' => 'Vehicle never had a lienholder'
            ]);
        }
        
        // Check if lienholder was paid off (enabling rate continuation)
        $paidOffRecord = $lienholderHistory->where('lienholder_status', 'PAID_OFF')->first();
        
        if ($paidOffRecord) {
            return new RateContinuationEligibility([
                'eligible' => true,
                'reason' => 'Previous lienholder paid off - rate continuation applies',
                'continuation_start_date' => $paidOffRecord->status_change_date,
                'original_lienholder_id' => $paidOffRecord->previous_lienholder_id
            ]);
        }
        
        return new RateContinuationEligibility([
            'eligible' => false,
            'reason' => 'No qualifying lienholder payoff found'
        ]);
    }
    
    public function trackLienholderChange(LienholderChangeData $changeData): LienholderChangeResult
    {
        // Create historical record
        $historyRecord = DB::table('lienholder_status_history')->insertGetId([
            'vehicle_id' => $changeData->vehicle_id,
            'policy_id' => $changeData->policy_id,
            'lienholder_id' => $changeData->new_lienholder_id,
            'lienholder_status' => $changeData->new_status,
            'status_change_date' => $changeData->change_date,
            'previous_lienholder_id' => $changeData->previous_lienholder_id,
            'rate_continuation_eligible' => $changeData->new_status === 'PAID_OFF',
            'rate_continuation_start_date' => $changeData->new_status === 'PAID_OFF' ? $changeData->change_date : null,
            'rate_continuation_reason' => $changeData->new_status === 'PAID_OFF' ? 'Lienholder paid off - continuing favorable rate per business rule' : null,
            'change_source' => $changeData->change_source,
            'verification_status' => $changeData->verification_status ?? 'PENDING',
            'status_id' => Status::ACTIVE,
            'created_by' => $changeData->created_by
        ]);
        
        return new LienholderChangeResult([
            'history_record_id' => $historyRecord,
            'rate_continuation_activated' => $changeData->new_status === 'PAID_OFF',
            'previous_factor_preserved' => $changeData->new_status === 'PAID_OFF'
        ]);
    }
}
```

---

## 5. Aguila Dorada Coverage Type Factor Matrix

### Coverage Type Factor Implementation
```sql
-- Coverage type factors for Aguila Dorada program
-- Matrix: Classification (YES/NO/LO/NON_OWNER) × Vehicle Count (1/2/3/4+)

-- YES (With Lienholder) - All vehicle counts get 1.0000 (base rate)
INSERT INTO coverage_type_factor (program_id, classification_id, vehicle_count_tier_id, factor_value, factor_type, percentage_adjustment, effective_date) VALUES
(1, (SELECT id FROM coverage_type_classification WHERE classification_code = 'YES'), (SELECT id FROM vehicle_count_tier WHERE tier_code = 'SINGLE'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15'),
(1, (SELECT id FROM coverage_type_classification WHERE classification_code = 'YES'), (SELECT id FROM vehicle_count_tier WHERE tier_code = 'TWO'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15'),
(1, (SELECT id FROM coverage_type_classification WHERE classification_code = 'YES'), (SELECT id FROM vehicle_count_tier WHERE tier_code = 'THREE'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15'),
(1, (SELECT id FROM coverage_type_classification WHERE classification_code = 'YES'), (SELECT id FROM vehicle_count_tier WHERE tier_code = 'FOUR_PLUS'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15'),

-- NO (Without Lienholder) - Single vehicle higher surcharge, multi-vehicle reduced surcharge
(1, (SELECT id FROM coverage_type_classification WHERE classification_code = 'NO'), (SELECT id FROM vehicle_count_tier WHERE tier_code = 'SINGLE'), 1.3000, 'SURCHARGE', 30.00, '2025-07-15'),
(1, (SELECT id FROM coverage_type_classification WHERE classification_code = 'NO'), (SELECT id FROM vehicle_count_tier WHERE tier_code = 'TWO'), 1.1000, 'SURCHARGE', 10.00, '2025-07-15'),
(1, (SELECT id FROM coverage_type_classification WHERE classification_code = 'NO'), (SELECT id FROM vehicle_count_tier WHERE tier_code = 'THREE'), 1.1000, 'SURCHARGE', 10.00, '2025-07-15'),
(1, (SELECT id FROM coverage_type_classification WHERE classification_code = 'NO'), (SELECT id FROM vehicle_count_tier WHERE tier_code = 'FOUR_PLUS'), 1.1000, 'SURCHARGE', 10.00, '2025-07-15'),

-- LO (Liability Only) - Consistent 20% discount across all vehicle counts
(1, (SELECT id FROM coverage_type_classification WHERE classification_code = 'LO'), (SELECT id FROM vehicle_count_tier WHERE tier_code = 'SINGLE'), 0.8000, 'DISCOUNT', -20.00, '2025-07-15'),
(1, (SELECT id FROM coverage_type_classification WHERE classification_code = 'LO'), (SELECT id FROM vehicle_count_tier WHERE tier_code = 'TWO'), 0.8000, 'DISCOUNT', -20.00, '2025-07-15'),
(1, (SELECT id FROM coverage_type_classification WHERE classification_code = 'LO'), (SELECT id FROM vehicle_count_tier WHERE tier_code = 'THREE'), 0.8000, 'DISCOUNT', -20.00, '2025-07-15'),
(1, (SELECT id FROM coverage_type_classification WHERE classification_code = 'LO'), (SELECT id FROM vehicle_count_tier WHERE tier_code = 'FOUR_PLUS'), 0.8000, 'DISCOUNT', -20.00, '2025-07-15'),

-- NON_OWNER - Base rate (1.0000) - only single vehicle count applies
(1, (SELECT id FROM coverage_type_classification WHERE classification_code = 'NON_OWNER'), (SELECT id FROM vehicle_count_tier WHERE tier_code = 'SINGLE'), 1.0000, 'NEUTRAL', 0.00, '2025-07-15');
```

---

## 6. API Integration Requirements

### Coverage Type Factor Endpoints
```php
// Coverage type factor API endpoints
POST /api/v1/rating/coverage-type/calculate
{
    "vehicle_coverage_type_data": {
        "vehicle_id": 12345,
        "policy_id": 67890,
        "policy_vehicle_count": 2,
        "coverage_elections": ["BI", "PD", "UMBI", "UMPD", "COMP", "COLL"],
        "lienholder_id": 123,
        "policy_type": "STANDARD"
    }
}

POST /api/v1/rating/coverage-type/classify
{
    "classification_data": {
        "has_lienholder": false,
        "has_physical_damage": true,
        "vehicle_count": 1,
        "policy_type": "STANDARD"
    }
}

GET /api/v1/rating/coverage-type/lienholder-continuation/{vehicleId}
// Check lienholder rate continuation eligibility

POST /api/v1/rating/coverage-type/lienholder-change
{
    "lienholder_change": {
        "vehicle_id": 12345,
        "policy_id": 67890,
        "previous_lienholder_id": 123,
        "new_lienholder_id": null,
        "new_status": "PAID_OFF",
        "change_date": "2025-07-15",
        "change_source": "CUSTOMER_REPORT"
    }
}
```

### Response Format
```json
{
    "vehicle_id": 12345,
    "policy_id": 67890,
    "coverage_type_factor": 1.1000,
    "coverage_classification": {
        "classification_code": "NO",
        "classification_name": "Without Lienholder",
        "risk_level": "HIGH"
    },
    "vehicle_count_analysis": {
        "policy_vehicle_count": 2,
        "tier_code": "TWO",
        "tier_name": "Two Vehicles",
        "fleet_effect": "Moderate risk distribution - reduced surcharge"
    },
    "factor_breakdown": {
        "base_classification_factor": 1.1000,
        "vehicle_count_adjustment": "10% surcharge (reduced from 30% for single vehicle)",
        "factor_type": "SURCHARGE",
        "percentage_adjustment": 10.00
    },
    "lienholder_analysis": {
        "current_lienholder": null,
        "rate_continuation_eligible": false,
        "rate_continuation_reason": "No qualifying lienholder payoff history",
        "historical_lienholder_benefit": false
    },
    "risk_assessment": {
        "risk_factors": ["Unfinanced vehicle", "Optional physical damage coverage"],
        "risk_mitigation": ["Multi-vehicle policy reduces risk concentration"],
        "premium_impact": "10% surcharge for unfinanced vehicle with physical damage coverage"
    }
}
```

---

## 7. Performance Requirements

### Coverage Type Factor Caching
```php
class VehicleCoverageTypeService
{
    public function calculateCoverageTypeFactor(VehicleCoverageTypeData $coverageData): CoverageTypeFactor
    {
        // Cache coverage type factors by classification and vehicle count
        $cacheKey = "coverage_type_factor_{$this->programId}_{$coverageData->classification_code}_{$coverageData->vehicle_count_tier}";
        
        return Cache::remember($cacheKey, 3600, function() use ($coverageData) {
            return $this->performCoverageTypeFactorCalculation($coverageData);
        });
    }
}
```

### Database Performance
```sql
-- Coverage type factor lookup optimization
CREATE INDEX idx_coverage_type_factor_lookup 
ON coverage_type_factor (
    program_id, 
    classification_id, 
    vehicle_count_tier_id,
    effective_date
) WHERE status_id = 1;

-- Lienholder status history lookup
CREATE INDEX idx_lienholder_status_lookup 
ON lienholder_status_history (
    vehicle_id, 
    lienholder_status, 
    status_change_date
) WHERE status_id = 1;

-- Rate continuation eligibility lookup
CREATE INDEX idx_rate_continuation_lookup 
ON lienholder_status_history (
    vehicle_id, 
    rate_continuation_eligible, 
    rate_continuation_start_date
) WHERE status_id = 1;
```

---

## 8. Testing Requirements

### Coverage Type Factor Testing
```php
class VehicleCoverageTypeServiceTest extends TestCase
{
    public function test_lienholder_base_rate()
    {
        $coverageData = new VehicleCoverageTypeData([
            'lienholder_id' => 123,
            'policy_vehicle_count' => 1,
            'coverage_elections' => ['BI', 'PD', 'COMP', 'COLL']
        ]);
        
        $factor = $this->coverageTypeService->calculateCoverageTypeFactor($coverageData);
        
        $this->assertEquals('YES', $factor->coverage_classification->classification_code);
        $this->assertEquals(1.0000, $factor->final_factor);
        $this->assertEquals('NEUTRAL', $factor->factor_type);
    }
    
    public function test_unfinanced_single_vehicle_surcharge()
    {
        $coverageData = new VehicleCoverageTypeData([
            'lienholder_id' => null,
            'policy_vehicle_count' => 1,
            'coverage_elections' => ['BI', 'PD', 'COMP', 'COLL']
        ]);
        
        $factor = $this->coverageTypeService->calculateCoverageTypeFactor($coverageData);
        
        $this->assertEquals('NO', $factor->coverage_classification->classification_code);
        $this->assertEquals(1.3000, $factor->final_factor); // 30% surcharge
        $this->assertEquals('SURCHARGE', $factor->factor_type);
    }
    
    public function test_multi_vehicle_reduced_surcharge()
    {
        $coverageData = new VehicleCoverageTypeData([
            'lienholder_id' => null,
            'policy_vehicle_count' => 2,
            'coverage_elections' => ['BI', 'PD', 'COMP', 'COLL']
        ]);
        
        $factor = $this->coverageTypeService->calculateCoverageTypeFactor($coverageData);
        
        $this->assertEquals('NO', $factor->coverage_classification->classification_code);
        $this->assertEquals(1.1000, $factor->final_factor); // 10% surcharge (reduced from 30%)
        $this->assertEquals('SURCHARGE', $factor->factor_type);
    }
    
    public function test_liability_only_discount()
    {
        $coverageData = new VehicleCoverageTypeData([
            'lienholder_id' => null,
            'policy_vehicle_count' => 1,
            'coverage_elections' => ['BI', 'PD', 'UMBI', 'UMPD'] // No COMP/COLL
        ]);
        
        $factor = $this->coverageTypeService->calculateCoverageTypeFactor($coverageData);
        
        $this->assertEquals('LO', $factor->coverage_classification->classification_code);
        $this->assertEquals(0.8000, $factor->final_factor); // 20% discount
        $this->assertEquals('DISCOUNT', $factor->factor_type);
    }
    
    public function test_lienholder_rate_continuation()
    {
        // Set up vehicle with historical lienholder that was paid off
        $this->createLienholderHistory(12345, 'PAID_OFF');
        
        $coverageData = new VehicleCoverageTypeData([
            'vehicle_id' => 12345,
            'lienholder_id' => null, // Currently no lienholder
            'policy_vehicle_count' => 1,
            'coverage_elections' => ['BI', 'PD', 'COMP', 'COLL']
        ]);
        
        $factor = $this->coverageTypeService->calculateCoverageTypeFactor($coverageData);
        
        $this->assertTrue($factor->rate_continuation->isEligible());
        $this->assertEquals(1.0000, $factor->final_factor); // Should get lienholder rate
        $this->assertEquals('Rate continuation - previous lienholder paid off', $factor->rate_continuation->reason);
    }
}
```

---

## Implementation Priority: HIGH
This factor is critical for accurate risk assessment based on lienholder status and fleet effects. Must be implemented early as it affects all coverage types and includes complex business rules.

## Dependencies
- **Lienholder Management System**: Current and historical lienholder tracking
- **Policy Structure Management**: Vehicle count calculation and coverage elections
- **Historical Data Migration**: Existing lienholder status history for rate continuation

## Estimated Implementation Effort
- **Database Schema**: 4 days
- **Service Layer**: 5 days
- **Lienholder Tracking**: 3 days
- **Rate Continuation Logic**: 3 days
- **API Integration**: 2 days
- **Testing**: 4 days
- **Total**: 21 days

This plan implements comprehensive coverage type risk assessment including the unique lienholder rate continuation benefit, multi-vehicle fleet effects, and proper classification of all coverage scenarios while maintaining detailed historical tracking for audit and customer benefit purposes.