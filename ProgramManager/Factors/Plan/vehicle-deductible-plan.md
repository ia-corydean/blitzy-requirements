# Vehicle Deductible Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Vehicle Deductible  
**Category**: Vehicle Factor  
**Priority**: High - Physical damage coverage pricing foundation  
**Implementation Complexity**: Medium  

### Business Requirements Summary
The Vehicle Deductible factor implements risk-based pricing adjustments based on the deductible amount selected for comprehensive and collision coverage. This factor reflects the inverse relationship between deductible amounts and claim frequency, providing appropriate premium adjustments that account for the insurer's reduced exposure and the customer's retained risk.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing and new Global Requirements:

#### Leverages GR-65: Rating Engine Architecture
**Integration**: Deductible factor calculation within multiplicative rating engine  
**Dependencies**: RatingEngineService for deductible-based factor lookup and premium adjustment

#### New Requirement: GR-87: Deductible Management Standards
**Priority**: High  
**Rationale**: Deductible selection and risk retention methodology for physical damage coverage  

**Core Components**:
- Deductible option management and factor assignment methodology
- Customer risk retention assessment and premium adjustment standards
- Deductible selection validation and lienholder compliance requirements
- Mid-term deductible change management and endorsement processing
- Physical damage coverage integration and consistency requirements
- Claims cost correlation and deductible impact assessment standards

#### Leverages GR-20: Application Business Logic
**Integration**: Deductible selection logic and coverage validation patterns  
**Dependencies**: Physical damage coverage requirements and customer choice validation

### Integration with Existing Global Requirements
- **GR-41**: Table Schema Requirements - Deductible option and factor table structures
- **GR-04**: Validation & Data Handling - Deductible selection validation and lienholder compliance
- **GR-37**: Locking & Action Tracking - Mid-term deductible change tracking and audit

---

## 2. Service Architecture Requirements

### Deductible Management Services

#### VehicleDeductibleService
**Purpose**: Deductible factor calculation and option management  
**Location**: `app/Domain/Rating/Services/VehicleDeductibleService.php`

**Key Methods**:
```php
class VehicleDeductibleService
{
    public function calculateDeductibleFactor(VehicleDeductibleData $deductibleData): DeductibleFactor
    {
        // 1. Validate deductible selection and consistency
        // 2. Check lienholder restrictions and compliance
        // 3. Lookup deductible factors for comprehensive and collision
        // 4. Calculate premium impact and cost analysis
        // 5. Return factor with deductible breakdown and savings analysis
    }
    
    public function validateDeductibleSelection(DeductibleSelectionData $selectionData): ValidationResult
    {
        // Validate deductible selection meets requirements and restrictions
    }
    
    public function getAvailableDeductibles(VehicleData $vehicleData): array
    {
        // Get available deductible options considering lienholder restrictions
    }
    
    public function calculateCostAnalysis(DeductibleComparisonData $comparisonData): CostAnalysisResult
    {
        // Provide premium vs deductible cost analysis for customer education
    }
}
```

#### DeductibleValidationService
**Purpose**: Deductible selection validation and lienholder compliance  
**Location**: `app/Domain/Rating/Services/DeductibleValidationService.php`

**Key Methods**:
```php
class DeductibleValidationService
{
    public function validateLienholderCompliance(VehicleData $vehicleData, int $deductibleAmount): ValidationResult
    {
        // Validate deductible selection meets lienholder requirements
    }
    
    public function validateConsistentDeductibles(array $coverageDeductibles): ValidationResult
    {
        // Ensure comprehensive and collision use same deductible
    }
    
    public function validateMidTermChange(DeductibleChangeRequest $changeRequest): ValidationResult
    {
        // Validate mid-term deductible change eligibility
    }
}
```

---

## 3. Database Schema Requirements

### Deductible Management Tables

#### deductible_option
```sql
CREATE TABLE deductible_option (
    id BIGINT PRIMARY KEY,
    deductible_amount INT NOT NULL,
    deductible_code VARCHAR(50) UNIQUE NOT NULL,
    deductible_name VARCHAR(255) NOT NULL,
    deductible_description TEXT,
    display_order INT DEFAULT 0,
    is_default BOOLEAN DEFAULT FALSE,
    minimum_vehicle_value DECIMAL(10,2), -- Minimum vehicle value for this deductible
    maximum_vehicle_value DECIMAL(10,2), -- Maximum vehicle value for this deductible
    lienholder_acceptable BOOLEAN DEFAULT TRUE,
    customer_education_notes TEXT,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_deductible_amount (deductible_amount),
    INDEX idx_deductible_amount (deductible_amount, status_id),
    INDEX idx_display_order (display_order, status_id),
    INDEX idx_lienholder_acceptable (lienholder_acceptable, status_id)
);

-- Aguila Dorada deductible options
INSERT INTO deductible_option (deductible_amount, deductible_code, deductible_name, display_order, is_default, lienholder_acceptable) VALUES
(250, 'DEDUCT_250', '$250 Deductible', 1, FALSE, TRUE),
(500, 'DEDUCT_500', '$500 Deductible', 2, TRUE, TRUE),
(750, 'DEDUCT_750', '$750 Deductible', 3, FALSE, TRUE),
(1000, 'DEDUCT_1000', '$1000 Deductible', 4, FALSE, TRUE);
```

#### deductible_factor
```sql
CREATE TABLE deductible_factor (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    deductible_option_id BIGINT NOT NULL,
    coverage_type_id BIGINT NOT NULL,
    factor_value DECIMAL(6,4) NOT NULL,
    discount_percentage DECIMAL(5,2), -- Percentage discount/surcharge (e.g., -20.00 for 20% discount)
    base_factor BOOLEAN DEFAULT FALSE, -- True if this is the base reference factor (1.0000)
    effective_date DATE NOT NULL,
    expiration_date DATE,
    actuarial_justification TEXT,
    claims_impact_analysis TEXT,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (deductible_option_id) REFERENCES deductible_option(id),
    FOREIGN KEY (coverage_type_id) REFERENCES coverage_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_deductible_factor (
        program_id, 
        deductible_option_id, 
        coverage_type_id, 
        effective_date
    ),
    INDEX idx_program_deductible_factors (program_id, deductible_option_id),
    INDEX idx_coverage_deductible_factors (coverage_type_id, factor_value),
    INDEX idx_base_factor (base_factor, status_id),
    INDEX idx_effective_dates (effective_date, expiration_date)
);
```

#### vehicle_deductible_selection
```sql
CREATE TABLE vehicle_deductible_selection (
    id BIGINT PRIMARY KEY,
    vehicle_id BIGINT NOT NULL,
    policy_id BIGINT NOT NULL,
    deductible_option_id BIGINT NOT NULL,
    comprehensive_deductible INT NOT NULL,
    collision_deductible INT NOT NULL,
    selection_date DATE NOT NULL,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    change_reason VARCHAR(255),
    customer_requested BOOLEAN DEFAULT TRUE,
    lienholder_approved BOOLEAN DEFAULT TRUE,
    previous_deductible_amount INT,
    cost_savings_disclosed BOOLEAN DEFAULT FALSE,
    customer_education_provided BOOLEAN DEFAULT FALSE,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(id),
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (deductible_option_id) REFERENCES deductible_option(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_vehicle_deductible_history (vehicle_id, effective_date),
    INDEX idx_policy_deductibles (policy_id, effective_date),
    INDEX idx_current_deductible (vehicle_id, expiration_date) -- For current deductible lookup
);
```

#### lienholder_deductible_restriction
```sql
CREATE TABLE lienholder_deductible_restriction (
    id BIGINT PRIMARY KEY,
    lienholder_id BIGINT NOT NULL,
    maximum_comprehensive_deductible INT NOT NULL,
    maximum_collision_deductible INT NOT NULL,
    restriction_notes TEXT,
    verification_required BOOLEAN DEFAULT FALSE,
    exception_process_available BOOLEAN DEFAULT FALSE,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (lienholder_id) REFERENCES lienholder(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_lienholder_restriction (lienholder_id, effective_date),
    INDEX idx_lienholder_restrictions (lienholder_id, maximum_comprehensive_deductible),
    INDEX idx_maximum_deductibles (maximum_comprehensive_deductible, maximum_collision_deductible)
);

-- Common lienholder deductible restrictions
INSERT INTO lienholder_deductible_restriction (lienholder_id, maximum_comprehensive_deductible, maximum_collision_deductible, restriction_notes, effective_date) VALUES
-- Note: Actual lienholder_ids would be populated based on lienholder database
(1, 1000, 1000, 'Standard bank restriction allowing up to $1000 deductibles', '2025-07-15'),
(2, 500, 500, 'Conservative lender restricting to maximum $500 deductibles', '2025-07-15'),
(3, 1000, 500, 'Lender allowing higher comprehensive deductible but limiting collision', '2025-07-15');
```

---

## 4. Business Logic Requirements

### Deductible Factor Calculation Logic
```php
class VehicleDeductibleService
{
    public function calculateDeductibleFactor(VehicleDeductibleData $deductibleData): DeductibleFactor
    {
        // 1. Validate deductible selection
        $validationResult = $this->validateDeductibleSelection($deductibleData);
        if (!$validationResult->isValid()) {
            throw new DeductibleValidationException($validationResult->getErrors());
        }
        
        // 2. Get deductible option record
        $deductibleOption = $this->getDeductibleOption($deductibleData->deductible_amount);
        
        // 3. Calculate factors for physical damage coverages
        $deductibleFactors = [];
        foreach (['COMP', 'COLL'] as $coverageType) {
            if (in_array($coverageType, $deductibleData->coverage_types)) {
                $factor = $this->getDeductibleFactor($deductibleOption->id, $coverageType);
                $deductibleFactors[$coverageType] = $factor;
            }
        }
        
        // 4. Calculate cost analysis
        $costAnalysis = $this->calculateCostAnalysis($deductibleData);
        
        return new DeductibleFactor([
            'vehicle_id' => $deductibleData->vehicle_id,
            'deductible_amount' => $deductibleData->deductible_amount,
            'deductible_option' => $deductibleOption,
            'deductible_factors' => $deductibleFactors,
            'cost_analysis' => $costAnalysis,
            'lienholder_compliant' => $validationResult->isLienholderCompliant(),
            'selection_date' => now()
        ]);
    }
    
    private function getDeductibleFactor(int $deductibleOptionId, string $coverageType): float
    {
        $factor = DB::table('deductible_factor')
            ->join('coverage_type', 'deductible_factor.coverage_type_id', '=', 'coverage_type.id')
            ->where('deductible_factor.deductible_option_id', $deductibleOptionId)
            ->where('coverage_type.coverage_code', $coverageType)
            ->where('deductible_factor.program_id', $this->programId)
            ->where('deductible_factor.effective_date', '<=', now())
            ->where(function($query) {
                $query->whereNull('deductible_factor.expiration_date')
                      ->orWhere('deductible_factor.expiration_date', '>', now());
            })
            ->where('deductible_factor.status_id', Status::ACTIVE)
            ->value('deductible_factor.factor_value');
            
        return $factor ?? 1.0000; // Default to neutral if not found
    }
    
    public function calculateCostAnalysis(VehicleDeductibleData $deductibleData): CostAnalysisResult
    {
        $selectedOption = $this->getDeductibleOption($deductibleData->deductible_amount);
        $allOptions = $this->getAvailableDeductibles($deductibleData->vehicle_data);
        
        $comparisons = [];
        $basePremium = $deductibleData->base_premium ?? 1000; // Sample base premium for calculation
        
        foreach ($allOptions as $option) {
            $compFactor = $this->getDeductibleFactor($option->id, 'COMP');
            $collFactor = $this->getDeductibleFactor($option->id, 'COLL');
            
            $adjustedPremium = $basePremium * (($compFactor + $collFactor) / 2); // Simplified calculation
            $premiumDifference = $adjustedPremium - ($basePremium * (($this->getDeductibleFactor($selectedOption->id, 'COMP') + $this->getDeductibleFactor($selectedOption->id, 'COLL')) / 2));
            
            $comparisons[] = [
                'deductible_amount' => $option->deductible_amount,
                'annual_premium' => $adjustedPremium,
                'premium_difference' => $premiumDifference,
                'out_of_pocket_difference' => $option->deductible_amount - $selectedOption->deductible_amount,
                'break_even_claims' => $premiumDifference > 0 ? ($premiumDifference / ($selectedOption->deductible_amount - $option->deductible_amount)) : 0
            ];
        }
        
        return new CostAnalysisResult([
            'selected_deductible' => $selectedOption->deductible_amount,
            'comparisons' => $comparisons,
            'recommendation' => $this->generateRecommendation($comparisons),
            'total_cost_scenarios' => $this->calculateTotalCostScenarios($comparisons)
        ]);
    }
}
```

### Deductible Validation Logic
```php
class DeductibleValidationService
{
    public function validateDeductibleSelection(DeductibleSelectionData $selectionData): ValidationResult
    {
        $result = new ValidationResult();
        
        // 1. Validate deductible amount is available option
        $availableOptions = DB::table('deductible_option')
            ->where('status_id', Status::ACTIVE)
            ->pluck('deductible_amount')
            ->toArray();
            
        if (!in_array($selectionData->deductible_amount, $availableOptions)) {
            $result->addError("Invalid deductible amount: {$selectionData->deductible_amount}");
            return $result;
        }
        
        // 2. Check lienholder restrictions
        if ($selectionData->vehicle_data->lienholder_id) {
            $lienholderResult = $this->validateLienholderCompliance(
                $selectionData->vehicle_data, 
                $selectionData->deductible_amount
            );
            $result->merge($lienholderResult);
        }
        
        // 3. Validate consistent deductibles for comp/coll
        if ($selectionData->comprehensive_deductible !== $selectionData->collision_deductible) {
            $result->addError("Comprehensive and collision deductibles must be the same amount");
        }
        
        // 4. Validate against vehicle value (if applicable)
        if ($selectionData->vehicle_data->actual_cash_value) {
            $this->validateDeductibleVsVehicleValue($selectionData, $result);
        }
        
        return $result;
    }
    
    public function validateLienholderCompliance(VehicleData $vehicleData, int $deductibleAmount): ValidationResult
    {
        $result = new ValidationResult();
        
        if (!$vehicleData->lienholder_id) {
            return $result; // No lienholder, no restrictions
        }
        
        $restriction = DB::table('lienholder_deductible_restriction')
            ->where('lienholder_id', $vehicleData->lienholder_id)
            ->where('effective_date', '<=', now())
            ->where(function($query) {
                $query->whereNull('expiration_date')
                      ->orWhere('expiration_date', '>', now());
            })
            ->where('status_id', Status::ACTIVE)
            ->first();
            
        if ($restriction) {
            if ($deductibleAmount > $restriction->maximum_comprehensive_deductible) {
                $result->addError(
                    "Deductible amount {$deductibleAmount} exceeds lienholder maximum of {$restriction->maximum_comprehensive_deductible}"
                );
            }
            
            if ($deductibleAmount > $restriction->maximum_collision_deductible) {
                $result->addError(
                    "Collision deductible amount {$deductibleAmount} exceeds lienholder maximum of {$restriction->maximum_collision_deductible}"
                );
            }
        }
        
        return $result;
    }
}
```

---

## 5. Aguila Dorada Deductible Factor Matrix

### Deductible Factor Implementation
```sql
-- Deductible factors for Aguila Dorada program
-- Factors apply to both Comprehensive and Collision coverage identically

-- $250 Deductible (40% surcharge)
INSERT INTO deductible_factor (program_id, deductible_option_id, coverage_type_id, factor_value, discount_percentage, base_factor, effective_date) VALUES
(1, (SELECT id FROM deductible_option WHERE deductible_amount = 250), (SELECT id FROM coverage_type WHERE coverage_code = 'COMP'), 1.4000, 40.00, FALSE, '2025-07-15'),
(1, (SELECT id FROM deductible_option WHERE deductible_amount = 250), (SELECT id FROM coverage_type WHERE coverage_code = 'COLL'), 1.4000, 40.00, FALSE, '2025-07-15'),

-- $500 Deductible (base rate)
(1, (SELECT id FROM deductible_option WHERE deductible_amount = 500), (SELECT id FROM coverage_type WHERE coverage_code = 'COMP'), 1.0000, 0.00, TRUE, '2025-07-15'),
(1, (SELECT id FROM deductible_option WHERE deductible_amount = 500), (SELECT id FROM coverage_type WHERE coverage_code = 'COLL'), 1.0000, 0.00, TRUE, '2025-07-15'),

-- $750 Deductible (7.5% discount)
(1, (SELECT id FROM deductible_option WHERE deductible_amount = 750), (SELECT id FROM coverage_type WHERE coverage_code = 'COMP'), 0.9250, -7.50, FALSE, '2025-07-15'),
(1, (SELECT id FROM deductible_option WHERE deductible_amount = 750), (SELECT id FROM coverage_type WHERE coverage_code = 'COLL'), 0.9250, -7.50, FALSE, '2025-07-15'),

-- $1000 Deductible (20% discount)
(1, (SELECT id FROM deductible_option WHERE deductible_amount = 1000), (SELECT id FROM coverage_type WHERE coverage_code = 'COMP'), 0.8000, -20.00, FALSE, '2025-07-15'),
(1, (SELECT id FROM deductible_option WHERE deductible_amount = 1000), (SELECT id FROM coverage_type WHERE coverage_code = 'COLL'), 0.8000, -20.00, FALSE, '2025-07-15');
```

---

## 6. API Integration Requirements

### Deductible Factor Endpoints
```php
// Deductible factor API endpoints
GET /api/v1/rating/deductible/options
// Returns available deductible options with factors

POST /api/v1/rating/deductible/calculate
{
    "vehicle_deductible_data": {
        "vehicle_id": 12345,
        "deductible_amount": 500,
        "coverage_types": ["COMP", "COLL"],
        "vehicle_data": {
            "lienholder_id": 123,
            "actual_cash_value": 25000
        },
        "base_premium": 900
    }
}

POST /api/v1/rating/deductible/cost-analysis
{
    "vehicle_id": 12345,
    "current_deductible": 500,
    "annual_premium": 900,
    "expected_claims_per_year": 0.1
}
// Provides comprehensive cost analysis across all deductible options

POST /api/v1/rating/deductible/validate
{
    "deductible_selection": {
        "deductible_amount": 1000,
        "comprehensive_deductible": 1000,
        "collision_deductible": 1000,
        "vehicle_data": {
            "lienholder_id": 123
        }
    }
}
```

### Response Format
```json
{
    "vehicle_id": 12345,
    "deductible_selection": {
        "deductible_amount": 500,
        "deductible_code": "DEDUCT_500",
        "deductible_name": "$500 Deductible"
    },
    "deductible_factors": {
        "COMP": 1.0000,
        "COLL": 1.0000
    },
    "factor_details": {
        "base_factor": true,
        "discount_percentage": 0.00,
        "premium_impact": "Base rate - no adjustment"
    },
    "cost_analysis": {
        "annual_premium_impact": 0.00,
        "deductible_comparisons": [
            {
                "deductible_amount": 250,
                "annual_premium": 1260.00,
                "premium_difference": 360.00,
                "out_of_pocket_difference": -250.00,
                "break_even_claims": 1.44
            },
            {
                "deductible_amount": 750,
                "annual_premium": 832.50,
                "premium_difference": -67.50,
                "out_of_pocket_difference": 250.00,
                "break_even_claims": 0.27
            },
            {
                "deductible_amount": 1000,
                "annual_premium": 720.00,
                "premium_difference": -180.00,
                "out_of_pocket_difference": 500.00,
                "break_even_claims": 0.36
            }
        ],
        "recommendation": {
            "recommended_deductible": 750,
            "rationale": "Best balance of premium savings vs out-of-pocket risk for average claim frequency"
        }
    },
    "validation": {
        "selection_valid": true,
        "lienholder_compliant": true,
        "consistency_check": "PASSED",
        "warnings": []
    }
}
```

---

## 7. Performance Requirements

### Deductible Factor Caching
```php
class VehicleDeductibleService
{
    public function calculateDeductibleFactor(VehicleDeductibleData $deductibleData): DeductibleFactor
    {
        // Cache deductible factors by program and deductible amount
        $cacheKey = "deductible_factor_{$this->programId}_{$deductibleData->deductible_amount}";
        
        return Cache::remember($cacheKey, 3600, function() use ($deductibleData) {
            return $this->performDeductibleFactorCalculation($deductibleData);
        });
    }
}
```

### Database Performance
```sql
-- Deductible factor lookup optimization
CREATE INDEX idx_deductible_factor_lookup 
ON deductible_factor (
    program_id, 
    deductible_option_id, 
    coverage_type_id,
    effective_date
) WHERE status_id = 1;

-- Current vehicle deductible lookup
CREATE INDEX idx_current_vehicle_deductible 
ON vehicle_deductible_selection (
    vehicle_id, 
    effective_date, 
    expiration_date
) WHERE status_id = 1;

-- Lienholder restriction lookup
CREATE INDEX idx_lienholder_deductible_restrictions 
ON lienholder_deductible_restriction (
    lienholder_id, 
    effective_date
) WHERE status_id = 1;
```

---

## 8. Testing Requirements

### Deductible Factor Testing
```php
class VehicleDeductibleServiceTest extends TestCase
{
    public function test_base_deductible_neutral_factor()
    {
        $deductibleData = new VehicleDeductibleData([
            'deductible_amount' => 500,
            'coverage_types' => ['COMP', 'COLL']
        ]);
        
        $factor = $this->deductibleService->calculateDeductibleFactor($deductibleData);
        
        $this->assertEquals(500, $factor->deductible_amount);
        $this->assertEquals(1.0000, $factor->deductible_factors['COMP']);
        $this->assertEquals(1.0000, $factor->deductible_factors['COLL']);
        $this->assertTrue($factor->deductible_option->is_default);
    }
    
    public function test_low_deductible_surcharge()
    {
        $deductibleData = new VehicleDeductibleData([
            'deductible_amount' => 250,
            'coverage_types' => ['COMP', 'COLL']
        ]);
        
        $factor = $this->deductibleService->calculateDeductibleFactor($deductibleData);
        
        $this->assertEquals(250, $factor->deductible_amount);
        $this->assertEquals(1.4000, $factor->deductible_factors['COMP']); // 40% surcharge
        $this->assertEquals(1.4000, $factor->deductible_factors['COLL']); // 40% surcharge
    }
    
    public function test_high_deductible_discount()
    {
        $deductibleData = new VehicleDeductibleData([
            'deductible_amount' => 1000,
            'coverage_types' => ['COMP', 'COLL']
        ]);
        
        $factor = $this->deductibleService->calculateDeductibleFactor($deductibleData);
        
        $this->assertEquals(1000, $factor->deductible_amount);
        $this->assertEquals(0.8000, $factor->deductible_factors['COMP']); // 20% discount
        $this->assertEquals(0.8000, $factor->deductible_factors['COLL']); // 20% discount
    }
    
    public function test_lienholder_restriction_validation()
    {
        $deductibleData = new VehicleDeductibleData([
            'deductible_amount' => 1000,
            'vehicle_data' => new VehicleData(['lienholder_id' => 2]) // Lender with $500 max
        ]);
        
        $this->expectException(DeductibleValidationException::class);
        $this->deductibleService->calculateDeductibleFactor($deductibleData);
    }
    
    public function test_cost_analysis_calculation()
    {
        $deductibleData = new VehicleDeductibleData([
            'deductible_amount' => 500,
            'base_premium' => 900,
            'coverage_types' => ['COMP', 'COLL']
        ]);
        
        $factor = $this->deductibleService->calculateDeductibleFactor($deductibleData);
        
        $this->assertInstanceOf(CostAnalysisResult::class, $factor->cost_analysis);
        $this->assertCount(4, $factor->cost_analysis->comparisons); // All 4 deductible options
        $this->assertNotNull($factor->cost_analysis->recommendation);
    }
}
```

---

## Implementation Priority: HIGH
This factor is essential for physical damage coverage pricing and must be implemented early as it directly affects customer choice and premium calculations.

## Dependencies
- **Physical Damage Coverage Configuration**: Comprehensive and collision coverage definitions
- **Lienholder Management System**: Lienholder restrictions and compliance validation
- **Policy Endorsement System**: Mid-term deductible change processing

## Estimated Implementation Effort
- **Database Schema**: 3 days
- **Service Layer**: 4 days
- **Validation Logic**: 3 days
- **Cost Analysis Engine**: 2 days
- **API Integration**: 2 days
- **Testing**: 3 days
- **Total**: 17 days

This plan implements comprehensive deductible management with proper validation, cost analysis, and customer education features while maintaining lienholder compliance and providing flexible deductible options that align with market standards and customer needs.