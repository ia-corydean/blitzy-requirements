# Policy Limits Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Policy Limits  
**Category**: Core Rating Component  
**Priority**: High - Coverage selection factor application  
**Implementation Complexity**: Medium  

### Business Requirements Summary
The Policy Limits factor implements coverage-specific multipliers based on selected liability limits, physical damage deductibles, and other coverage options. This factor ensures proper premium adjustment for different coverage levels while maintaining regulatory compliance with Texas minimum requirements and dependency rules between coverage types.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing and new Global Requirements:

#### Leverages GR-65: Rating Engine Architecture
**Integration**: Coverage limit factor calculation within multiplicative rating engine  
**Dependencies**: RatingEngineService for coverage-specific factor lookup and validation

#### New Requirement: GR-75: Insurance Coverage Standards
**Priority**: High  
**Rationale**: Coverage limit validation and regulatory compliance standards  

**Core Components**:
- State minimum coverage requirement validation
- Coverage dependency rules and validation
- Limit selection business rules and restrictions
- Deductible option management and validation
- Regulatory compliance tracking for coverage requirements

#### Leverages GR-04: Validation & Data Handling
**Integration**: Coverage selection validation patterns  
**Dependencies**: Limit validation rules, coverage dependency checking

### Integration with Existing Global Requirements
- **GR-41**: Table Schema Requirements - Coverage and limit factor table structures
- **GR-20**: Application Business Logic - Coverage calculation service patterns
- **GR-19**: Table Relationships - Coverage association and dependency patterns

---

## 2. Service Architecture Requirements

### Coverage Limit Services

#### PolicyLimitsService
**Purpose**: Coverage limit factor calculation and validation  
**Location**: `app/Domain/Rating/Services/PolicyLimitsService.php`

**Key Methods**:
```php
class PolicyLimitsService
{
    public function calculateLimitsFactor(CoverageSelections $selections): PolicyLimitsFactor
    {
        // 1. Validate coverage selections and dependencies
        // 2. Calculate individual coverage factors
        // 3. Apply coverage combination rules
        // 4. Return combined limits factor with breakdown
    }
    
    public function validateCoverageSelections(CoverageSelections $selections): ValidationResult
    {
        // Validate coverage limits, dependencies, and regulatory requirements
    }
    
    public function getCoverageFactorBreakdown(CoverageSelections $selections): CoverageBreakdown
    {
        // Provide detailed breakdown of coverage factors
    }
}
```

#### CoverageValidationService
**Purpose**: Coverage selection validation and dependency checking  
**Location**: `app/Domain/Rating/Services/CoverageValidationService.php`

**Key Methods**:
```php
class CoverageValidationService
{
    public function validateTexasMinimums(CoverageSelections $selections): ValidationResult
    {
        // Validate against Texas minimum requirements (30/60/25)
    }
    
    public function validateCoverageDependencies(CoverageSelections $selections): ValidationResult
    {
        // Validate coverage dependencies (comp/collision, etc.)
    }
    
    public function validateLienholderRequirements(CoverageSelections $selections, VehicleData $vehicle): ValidationResult
    {
        // Validate lienholder coverage requirements
    }
}
```

---

## 3. Database Schema Requirements

### Coverage and Limit Management Tables

#### coverage_type
```sql
CREATE TABLE coverage_type (
    id BIGINT PRIMARY KEY,
    coverage_code VARCHAR(50) UNIQUE NOT NULL,
    coverage_name VARCHAR(255) NOT NULL,
    coverage_description TEXT,
    coverage_category ENUM('LIABILITY', 'PHYSICAL_DAMAGE', 'PIP', 'OTHER') NOT NULL,
    is_required BOOLEAN DEFAULT FALSE,
    has_limits BOOLEAN DEFAULT TRUE,
    has_deductible BOOLEAN DEFAULT FALSE,
    limit_type ENUM('SPLIT', 'COMBINED', 'FIXED', 'VARIABLE') NOT NULL,
    calculation_basis ENUM('FLAT', 'PER_VEHICLE', 'PER_DRIVER', 'COMBINED') NOT NULL,
    display_order INT DEFAULT 0,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_coverage_category (coverage_category, status_id),
    INDEX idx_required_coverage (is_required, status_id),
    INDEX idx_display_order (display_order, status_id)
);

-- Aguila Dorada coverage types
INSERT INTO coverage_type (coverage_code, coverage_name, coverage_category, is_required, has_limits, has_deductible, limit_type, calculation_basis) VALUES
('LIABILITY', 'Bodily Injury & Property Damage', 'LIABILITY', TRUE, TRUE, FALSE, 'SPLIT', 'COMBINED'),
('COMPREHENSIVE', 'Comprehensive', 'PHYSICAL_DAMAGE', FALSE, FALSE, TRUE, 'FIXED', 'PER_VEHICLE'),
('COLLISION', 'Collision', 'PHYSICAL_DAMAGE', FALSE, FALSE, TRUE, 'FIXED', 'PER_VEHICLE'),
('PIP', 'Personal Injury Protection', 'PIP', FALSE, TRUE, FALSE, 'FIXED', 'COMBINED'),
('MEDICAL_PAYMENTS', 'Medical Payments', 'OTHER', FALSE, TRUE, FALSE, 'FIXED', 'COMBINED'),
('UNINSURED_MOTORIST', 'Uninsured Motorist', 'LIABILITY', FALSE, TRUE, FALSE, 'SPLIT', 'COMBINED'),
('UNDERINSURED_MOTORIST', 'Underinsured Motorist', 'LIABILITY', FALSE, TRUE, FALSE, 'SPLIT', 'COMBINED');
```

#### coverage_limit_option
```sql
CREATE TABLE coverage_limit_option (
    id BIGINT PRIMARY KEY,
    coverage_type_id BIGINT NOT NULL,
    program_id BIGINT NOT NULL,
    limit_display VARCHAR(100) NOT NULL,
    bodily_injury_per_person DECIMAL(10,2),
    bodily_injury_per_accident DECIMAL(10,2),
    property_damage_per_accident DECIMAL(10,2),
    combined_single_limit DECIMAL(10,2),
    medical_limit DECIMAL(10,2),
    is_minimum_required BOOLEAN DEFAULT FALSE,
    is_available BOOLEAN DEFAULT TRUE,
    display_order INT DEFAULT 0,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (coverage_type_id) REFERENCES coverage_type(id),
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_program_coverage_limit (program_id, coverage_type_id, limit_display),
    INDEX idx_program_limits (program_id, coverage_type_id),
    INDEX idx_minimum_limits (is_minimum_required, status_id),
    INDEX idx_available_limits (is_available, display_order)
);
```

#### deductible_option
```sql
CREATE TABLE deductible_option (
    id BIGINT PRIMARY KEY,
    coverage_type_id BIGINT NOT NULL,
    program_id BIGINT NOT NULL,
    deductible_amount DECIMAL(8,2) NOT NULL,
    deductible_display VARCHAR(50) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    is_default BOOLEAN DEFAULT FALSE,
    display_order INT DEFAULT 0,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (coverage_type_id) REFERENCES coverage_type(id),
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_program_coverage_deductible (program_id, coverage_type_id, deductible_amount),
    INDEX idx_program_deductibles (program_id, coverage_type_id),
    INDEX idx_available_deductibles (is_available, display_order)
);
```

#### coverage_limit_factor
```sql
CREATE TABLE coverage_limit_factor (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    coverage_type_id BIGINT NOT NULL,
    limit_option_id BIGINT,
    deductible_option_id BIGINT,
    factor_value DECIMAL(6,4) NOT NULL,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    actuarial_justification TEXT,
    regulatory_filing_ref VARCHAR(100),
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (coverage_type_id) REFERENCES coverage_type(id),
    FOREIGN KEY (limit_option_id) REFERENCES coverage_limit_option(id),
    FOREIGN KEY (deductible_option_id) REFERENCES deductible_option(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_coverage_factor (
        program_id, 
        coverage_type_id, 
        limit_option_id, 
        deductible_option_id, 
        effective_date
    ),
    INDEX idx_program_coverage_factors (program_id, coverage_type_id, effective_date),
    INDEX idx_limit_factors (limit_option_id, effective_date),
    INDEX idx_deductible_factors (deductible_option_id, effective_date)
);
```

---

## 4. Business Logic Requirements

### Texas Minimum Requirements Validation
```php
class CoverageValidationService
{
    public function validateTexasMinimums(CoverageSelections $selections): ValidationResult
    {
        $result = new ValidationResult();
        
        // Texas minimum liability requirements: 30/60/25
        $liability = $selections->getCoverage('LIABILITY');
        
        if (!$liability || !$liability->isSelected()) {
            $result->addError('Liability coverage is required in Texas');
            return $result;
        }
        
        // Validate minimum limits
        if ($liability->bodily_injury_per_person < 30000) {
            $result->addError('Minimum bodily injury per person is $30,000');
        }
        
        if ($liability->bodily_injury_per_accident < 60000) {
            $result->addError('Minimum bodily injury per accident is $60,000');
        }
        
        if ($liability->property_damage_per_accident < 25000) {
            $result->addError('Minimum property damage is $25,000');
        }
        
        return $result;
    }
}
```

### Coverage Dependency Rules
```php
class CoverageValidationService
{
    public function validateCoverageDependencies(CoverageSelections $selections): ValidationResult
    {
        $result = new ValidationResult();
        
        // Comprehensive and Collision must be purchased together
        $comprehensive = $selections->getCoverage('COMPREHENSIVE');
        $collision = $selections->getCoverage('COLLISION');
        
        if ($comprehensive && $comprehensive->isSelected() && 
            (!$collision || !$collision->isSelected())) {
            $result->addError('Collision coverage required when Comprehensive is selected');
        }
        
        if ($collision && $collision->isSelected() && 
            (!$comprehensive || !$comprehensive->isSelected())) {
            $result->addError('Comprehensive coverage required when Collision is selected');
        }
        
        // Same deductible requirement for Comp/Collision
        if ($comprehensive && $collision && 
            $comprehensive->isSelected() && $collision->isSelected()) {
            if ($comprehensive->deductible_amount !== $collision->deductible_amount) {
                $result->addError('Comprehensive and Collision must have the same deductible');
            }
        }
        
        // PIP and Medical Payments are mutually exclusive
        $pip = $selections->getCoverage('PIP');
        $medpay = $selections->getCoverage('MEDICAL_PAYMENTS');
        
        if ($pip && $pip->isSelected() && $medpay && $medpay->isSelected()) {
            $result->addError('PIP and Medical Payments cannot both be selected');
        }
        
        return $result;
    }
}
```

### Limit Factor Calculation
```php
class PolicyLimitsService
{
    public function calculateLimitsFactor(CoverageSelections $selections): PolicyLimitsFactor
    {
        $totalFactor = 1.0;
        $coverageBreakdown = [];
        
        foreach ($selections->getAllCoverages() as $coverage) {
            if (!$coverage->isSelected()) {
                continue;
            }
            
            // Get factor for coverage limit/deductible combination
            $factor = $this->getCoverageFactor($coverage);
            
            $coverageBreakdown[] = [
                'coverage_code' => $coverage->coverage_code,
                'limit_display' => $coverage->limit_display,
                'deductible_display' => $coverage->deductible_display ?? 'N/A',
                'factor_value' => $factor,
                'factor_impact' => $factor - 1.0
            ];
            
            // Apply multiplicative factor
            $totalFactor *= $factor;
        }
        
        return new PolicyLimitsFactor([
            'total_factor' => $totalFactor,
            'coverage_breakdown' => $coverageBreakdown,
            'total_impact_percentage' => ($totalFactor - 1.0) * 100
        ]);
    }
    
    private function getCoverageFactor(CoverageSelection $coverage): float
    {
        $factor = DB::table('coverage_limit_factor')
            ->where('program_id', $this->programId)
            ->where('coverage_type_id', $coverage->coverage_type_id)
            ->where('limit_option_id', $coverage->limit_option_id)
            ->where('deductible_option_id', $coverage->deductible_option_id)
            ->where('effective_date', '<=', now())
            ->where(function($query) {
                $query->whereNull('expiration_date')
                      ->orWhere('expiration_date', '>', now());
            })
            ->where('status_id', Status::ACTIVE)
            ->value('factor_value');
            
        return $factor ?? 1.0; // Default to 1.0 if no factor found
    }
}
```

---

## 5. Aguila Dorada Coverage Configuration

### Standard Coverage Options
```sql
-- Liability Limit Options for Aguila Dorada
INSERT INTO coverage_limit_option (coverage_type_id, program_id, limit_display, bodily_injury_per_person, bodily_injury_per_accident, property_damage_per_accident, is_minimum_required, display_order) VALUES
((SELECT id FROM coverage_type WHERE coverage_code = 'LIABILITY'), 1, '30/60/25', 30000.00, 60000.00, 25000.00, TRUE, 1),
((SELECT id FROM coverage_type WHERE coverage_code = 'LIABILITY'), 1, '50/100/50', 50000.00, 100000.00, 50000.00, FALSE, 2),
((SELECT id FROM coverage_type WHERE coverage_code = 'LIABILITY'), 1, '100/300/100', 100000.00, 300000.00, 100000.00, FALSE, 3),
((SELECT id FROM coverage_type WHERE coverage_code = 'LIABILITY'), 1, '250/500/250', 250000.00, 500000.00, 250000.00, FALSE, 4),
((SELECT id FROM coverage_type WHERE coverage_code = 'LIABILITY'), 1, '500/1000/500', 500000.00, 1000000.00, 500000.00, FALSE, 5);

-- Physical Damage Deductible Options
INSERT INTO deductible_option (coverage_type_id, program_id, deductible_amount, deductible_display, display_order) VALUES
((SELECT id FROM coverage_type WHERE coverage_code = 'COMPREHENSIVE'), 1, 250.00, '$250', 1),
((SELECT id FROM coverage_type WHERE coverage_code = 'COMPREHENSIVE'), 1, 500.00, '$500', 2),
((SELECT id FROM coverage_type WHERE coverage_code = 'COMPREHENSIVE'), 1, 1000.00, '$1,000', 3),
((SELECT id FROM coverage_type WHERE coverage_code = 'COMPREHENSIVE'), 1, 2500.00, '$2,500', 4),

((SELECT id FROM coverage_type WHERE coverage_code = 'COLLISION'), 1, 250.00, '$250', 1),
((SELECT id FROM coverage_type WHERE coverage_code = 'COLLISION'), 1, 500.00, '$500', 2),
((SELECT id FROM coverage_type WHERE coverage_code = 'COLLISION'), 1, 1000.00, '$1,000', 3),
((SELECT id FROM coverage_type WHERE coverage_code = 'COLLISION'), 1, 2500.00, '$2,500', 4);

-- PIP Limit Options
INSERT INTO coverage_limit_option (coverage_type_id, program_id, limit_display, medical_limit, display_order) VALUES
((SELECT id FROM coverage_type WHERE coverage_code = 'PIP'), 1, '$2,500', 2500.00, 1),
((SELECT id FROM coverage_type WHERE coverage_code = 'PIP'), 1, '$5,000', 5000.00, 2),
((SELECT id FROM coverage_type WHERE coverage_code = 'PIP'), 1, '$10,000', 10000.00, 3);
```

### Sample Limit Factors
```sql
-- Liability limit factors (higher limits = higher factors)
INSERT INTO coverage_limit_factor (program_id, coverage_type_id, limit_option_id, factor_value, effective_date) VALUES
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'LIABILITY'), (SELECT id FROM coverage_limit_option WHERE limit_display = '30/60/25'), 1.0000, '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'LIABILITY'), (SELECT id FROM coverage_limit_option WHERE limit_display = '50/100/50'), 1.1500, '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'LIABILITY'), (SELECT id FROM coverage_limit_option WHERE limit_display = '100/300/100'), 1.3000, '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'LIABILITY'), (SELECT id FROM coverage_limit_option WHERE limit_display = '250/500/250'), 1.5000, '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'LIABILITY'), (SELECT id FROM coverage_limit_option WHERE limit_display = '500/1000/500'), 1.7500, '2025-07-15'),

-- Comprehensive deductible factors (higher deductibles = lower factors)
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'COMPREHENSIVE'), NULL, (SELECT id FROM deductible_option WHERE deductible_amount = 250.00), 1.2000, '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'COMPREHENSIVE'), NULL, (SELECT id FROM deductible_option WHERE deductible_amount = 500.00), 1.0000, '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'COMPREHENSIVE'), NULL, (SELECT id FROM deductible_option WHERE deductible_amount = 1000.00), 0.8500, '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'COMPREHENSIVE'), NULL, (SELECT id FROM deductible_option WHERE deductible_amount = 2500.00), 0.7000, '2025-07-15'),

-- Collision deductible factors (same as comprehensive)
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'COLLISION'), NULL, (SELECT id FROM deductible_option WHERE deductible_amount = 250.00), 1.2000, '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'COLLISION'), NULL, (SELECT id FROM deductible_option WHERE deductible_amount = 500.00), 1.0000, '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'COLLISION'), NULL, (SELECT id FROM deductible_option WHERE deductible_amount = 1000.00), 0.8500, '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'COLLISION'), NULL, (SELECT id FROM deductible_option WHERE deductible_amount = 2500.00), 0.7000, '2025-07-15');
```

---

## 6. API Integration Requirements

### Coverage Selection Endpoints
```php
// Coverage limits API endpoints
GET /api/v1/rating/coverage-options/{programId}
// Returns available coverage options and limits

POST /api/v1/rating/coverage/calculate
{
    "coverage_selections": [
        {
            "coverage_code": "LIABILITY",
            "limit_option_id": 123,
            "selected": true
        },
        {
            "coverage_code": "COMPREHENSIVE",
            "deductible_option_id": 456,
            "selected": true
        },
        {
            "coverage_code": "COLLISION",
            "deductible_option_id": 456,
            "selected": true
        }
    ]
}

POST /api/v1/rating/coverage/validate
{
    "coverage_selections": [...],
    "vehicle_data": {...}
}
// Validate coverage selections and dependencies
```

### Response Format
```json
{
    "limits_factor": 1.2750,
    "total_impact_percentage": 27.5,
    "coverage_breakdown": [
        {
            "coverage_code": "LIABILITY",
            "coverage_name": "Bodily Injury & Property Damage",
            "limit_display": "100/300/100",
            "factor_value": 1.3000,
            "factor_impact": 30.0
        },
        {
            "coverage_code": "COMPREHENSIVE",
            "coverage_name": "Comprehensive",
            "deductible_display": "$500",
            "factor_value": 1.0000,
            "factor_impact": 0.0
        },
        {
            "coverage_code": "COLLISION",
            "coverage_name": "Collision",
            "deductible_display": "$500",
            "factor_value": 1.0000,
            "factor_impact": 0.0
        }
    ],
    "validation_results": {
        "texas_minimums": "PASS",
        "coverage_dependencies": "PASS",
        "lienholder_requirements": "PASS"
    }
}
```

---

## 7. Performance Optimization

### Coverage Factor Caching
```php
class PolicyLimitsService
{
    public function getCoverageFactor(CoverageSelection $coverage): float
    {
        $cacheKey = "coverage_factor_{$this->programId}_{$coverage->coverage_type_id}_" .
                   "{$coverage->limit_option_id}_{$coverage->deductible_option_id}";
        
        return Cache::remember($cacheKey, 3600, function() use ($coverage) {
            return $this->lookupCoverageFactor($coverage);
        });
    }
}
```

### Database Performance
```sql
-- Coverage factor lookup optimization
CREATE INDEX idx_coverage_factor_lookup 
ON coverage_limit_factor (
    program_id, 
    coverage_type_id, 
    limit_option_id, 
    deductible_option_id,
    effective_date
) WHERE status_id = 1;
```

---

## 8. Testing Requirements

### Coverage Validation Testing
```php
class PolicyLimitsServiceTest extends TestCase
{
    public function test_texas_minimum_validation()
    {
        $selections = new CoverageSelections([
            'LIABILITY' => [
                'bodily_injury_per_person' => 30000,
                'bodily_injury_per_accident' => 60000,
                'property_damage_per_accident' => 25000
            ]
        ]);
        
        $result = $this->coverageValidator->validateTexasMinimums($selections);
        $this->assertTrue($result->isValid());
    }
    
    public function test_comprehensive_collision_dependency()
    {
        $selections = new CoverageSelections([
            'COMPREHENSIVE' => ['selected' => true, 'deductible' => 500],
            'COLLISION' => ['selected' => false]
        ]);
        
        $result = $this->coverageValidator->validateCoverageDependencies($selections);
        $this->assertFalse($result->isValid());
        $this->assertStringContains('Collision coverage required', $result->getErrors()[0]);
    }
}
```

---

## Implementation Priority: HIGH
This factor is essential for proper coverage-based pricing and regulatory compliance.

## Dependencies
- **Algorithm Factor**: Requires core rating engine for limit factor calculation
- **Coverage Type Setup**: Requires coverage types and options configuration

## Estimated Implementation Effort
- **Database Schema**: 3 days
- **Service Layer**: 4 days
- **Validation Logic**: 3 days
- **API Integration**: 2 days
- **Testing**: 3 days
- **Total**: 15 days

This plan implements comprehensive coverage limit factor management while ensuring regulatory compliance and proper coverage dependency validation.