# Policy Core Matrix Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Policy Core Matrix  
**Category**: Core Rating Component  
**Priority**: High - Multi-dimensional discount system  
**Implementation Complexity**: High  

### Business Requirements Summary
The Policy Core Matrix factor implements a sophisticated three-dimensional discount matrix based on Prior Insurance History, Years Licensed, and Vehicle Ownership status. This factor provides significant premium discounts (up to 56%) for customers who demonstrate stability and experience across all three dimensions.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing and new Global Requirements:

#### Leverages GR-65: Rating Engine Architecture
**Integration**: Matrix calculation within multiplicative rating engine  
**Dependencies**: RatingEngineService for complex matrix lookup and validation

#### New Requirement: GR-70: Insurance History Validation Framework
**Priority**: High  
**Rationale**: Prior insurance verification and documentation standards needed for accurate discounts  

**Core Components**:
- Prior insurance verification methodologies
- Documentation requirements and validation standards
- Third-party insurance verification integration patterns
- Historical insurance data retention and audit requirements

#### New Requirement: GR-71: Multi-Dimensional Rating Matrix Standards
**Priority**: Medium  
**Rationale**: Standards for complex matrix-based rating factors  

**Core Components**:
- Multi-dimensional factor table design patterns
- Matrix calculation optimization strategies
- Factor dimension validation and business rules
- Matrix factor versioning and historical tracking

### Integration with Existing Global Requirements
- **GR-41**: Table Schema Requirements - Complex matrix table structures
- **GR-20**: Application Business Logic - Matrix calculation service patterns
- **GR-04**: Validation & Data Handling - Multi-dimensional input validation

---

## 2. Service Architecture Requirements

### Matrix Calculation Services

#### PolicyCoreMatrixService
**Purpose**: Three-dimensional matrix calculation and validation  
**Location**: `app/Domain/Rating/Services/PolicyCoreMatrixService.php`

**Key Methods**:
```php
class PolicyCoreMatrixService
{
    public function calculateMatrixFactor(
        PriorInsuranceData $priorInsurance,
        LicenseHistoryData $licenseHistory,
        VehicleOwnershipData $ownership
    ): MatrixFactor {
        // 1. Validate all three dimensions
        // 2. Perform matrix lookup with interpolation if needed
        // 3. Apply business rules and maximum discount limits
        // 4. Return factor with detailed breakdown
    }
    
    public function validateMatrixInputs(array $matrixData): ValidationResult
    {
        // Validate all three matrix dimensions and combinations
    }
    
    public function getMatrixBreakdown(MatrixFactor $factor): MatrixBreakdown
    {
        // Provide detailed breakdown of matrix calculation
    }
}
```

#### PriorInsuranceVerificationService
**Purpose**: Prior insurance history validation and verification  
**Location**: `app/Domain/Rating/Services/PriorInsuranceVerificationService.php`

**Key Methods**:
```php
class PriorInsuranceVerificationService
{
    public function verifyPriorInsurance(PriorInsuranceData $data): VerificationResult
    {
        // 1. Validate insurance company and policy information
        // 2. Check for continuous coverage and lapse periods
        // 3. Verify documentation requirements
        // 4. Return verification status with supporting data
    }
    
    public function calculateContinuousCoverage(array $insurancePeriods): CoverageCalculation
    {
        // Calculate continuous coverage periods with lapse tolerance
    }
}
```

---

## 3. Database Schema Requirements

### Matrix Definition Tables

#### policy_core_matrix_dimension
```sql
CREATE TABLE policy_core_matrix_dimension (
    id BIGINT PRIMARY KEY,
    dimension_code VARCHAR(50) UNIQUE NOT NULL,
    dimension_name VARCHAR(255) NOT NULL,
    dimension_description TEXT,
    value_type ENUM('CATEGORICAL', 'NUMERIC', 'DURATION') NOT NULL,
    sort_order INT DEFAULT 0,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_dimension_active (status_id, sort_order)
);

-- Initial dimensions
INSERT INTO policy_core_matrix_dimension (dimension_code, dimension_name, value_type) VALUES
('PRIOR_INSURANCE', 'Prior Insurance History', 'CATEGORICAL'),
('YEARS_LICENSED', 'Years Licensed', 'DURATION'),
('VEHICLE_OWNERSHIP', 'Vehicle Ownership Status', 'CATEGORICAL');
```

#### policy_core_matrix_value
```sql
CREATE TABLE policy_core_matrix_value (
    id BIGINT PRIMARY KEY,
    dimension_id BIGINT NOT NULL,
    value_code VARCHAR(50) NOT NULL,
    value_name VARCHAR(255) NOT NULL,
    value_description TEXT,
    numeric_min DECIMAL(8,2), -- For duration/numeric ranges
    numeric_max DECIMAL(8,2),
    duration_min_months INT, -- For license years
    duration_max_months INT,
    sort_order INT DEFAULT 0,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (dimension_id) REFERENCES policy_core_matrix_dimension(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_dimension_value (dimension_id, value_code),
    INDEX idx_dimension_values (dimension_id, sort_order),
    INDEX idx_numeric_range (dimension_id, numeric_min, numeric_max),
    INDEX idx_duration_range (dimension_id, duration_min_months, duration_max_months)
);
```

#### policy_core_matrix_factor
```sql
CREATE TABLE policy_core_matrix_factor (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    prior_insurance_value_id BIGINT NOT NULL,
    years_licensed_value_id BIGINT NOT NULL,
    ownership_value_id BIGINT NOT NULL,
    matrix_factor DECIMAL(6,4) NOT NULL, -- 0.4400 to 1.0000
    effective_date DATE NOT NULL,
    expiration_date DATE,
    actuarial_support_data JSON,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (prior_insurance_value_id) REFERENCES policy_core_matrix_value(id),
    FOREIGN KEY (years_licensed_value_id) REFERENCES policy_core_matrix_value(id),
    FOREIGN KEY (ownership_value_id) REFERENCES policy_core_matrix_value(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_matrix_combination (
        program_id, 
        prior_insurance_value_id, 
        years_licensed_value_id, 
        ownership_value_id, 
        effective_date
    ),
    INDEX idx_program_matrix (program_id, effective_date),
    INDEX idx_matrix_lookup (prior_insurance_value_id, years_licensed_value_id, ownership_value_id),
    INDEX idx_effective_dates (effective_date, expiration_date)
);
```

### Insurance History Tracking Tables

#### prior_insurance_history
```sql
CREATE TABLE prior_insurance_history (
    id BIGINT PRIMARY KEY,
    policy_id BIGINT,
    quote_id BIGINT,
    insurance_company_name VARCHAR(255) NOT NULL,
    policy_number VARCHAR(100),
    coverage_start_date DATE NOT NULL,
    coverage_end_date DATE NOT NULL,
    lapse_reason VARCHAR(100),
    coverage_types JSON, -- Array of coverage types maintained
    verification_status ENUM('PENDING', 'VERIFIED', 'FAILED', 'EXPIRED') NOT NULL,
    verification_method VARCHAR(100),
    verification_date DATE,
    documentation_received BOOLEAN DEFAULT FALSE,
    verification_notes TEXT,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (quote_id) REFERENCES quote(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_policy_insurance_history (policy_id, coverage_start_date),
    INDEX idx_quote_insurance_history (quote_id, coverage_start_date),
    INDEX idx_verification_status (verification_status, verification_date),
    INDEX idx_coverage_dates (coverage_start_date, coverage_end_date)
);
```

#### license_history
```sql
CREATE TABLE license_history (
    id BIGINT PRIMARY KEY,
    driver_id BIGINT NOT NULL,
    license_state_id BIGINT NOT NULL,
    license_number VARCHAR(50) NOT NULL,
    first_licensed_date DATE NOT NULL,
    license_class VARCHAR(20),
    verification_status ENUM('PENDING', 'VERIFIED', 'FAILED') NOT NULL,
    verification_method VARCHAR(100),
    verification_date DATE,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (driver_id) REFERENCES driver(id),
    FOREIGN KEY (license_state_id) REFERENCES state(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_driver_license_history (driver_id, first_licensed_date),
    INDEX idx_license_verification (verification_status, verification_date),
    INDEX idx_license_state (license_state_id, first_licensed_date)
);
```

---

## 4. Business Logic Requirements

### Three-Dimensional Matrix Logic

#### Matrix Dimension Definitions
```php
// Prior Insurance History Categories
const PRIOR_INSURANCE_CATEGORIES = [
    'NONE' => ['name' => 'No Prior Insurance', 'months_required' => 0],
    'LESS_6_MONTHS' => ['name' => 'Less than 6 Months', 'months_required' => 1],
    'SIX_MONTHS_PLUS' => ['name' => '6+ Months Continuous', 'months_required' => 6],
    'ONE_YEAR_PLUS' => ['name' => '1+ Years Continuous', 'months_required' => 12],
    'TWO_YEARS_PLUS' => ['name' => '2+ Years Continuous', 'months_required' => 24],
    'THREE_YEARS_PLUS' => ['name' => '3+ Years Continuous', 'months_required' => 36]
];

// Years Licensed Categories
const YEARS_LICENSED_CATEGORIES = [
    'LESS_1_YEAR' => ['name' => 'Less than 1 Year', 'months_min' => 0, 'months_max' => 11],
    'ONE_TO_THREE' => ['name' => '1-3 Years', 'months_min' => 12, 'months_max' => 35],
    'THREE_TO_FIVE' => ['name' => '3-5 Years', 'months_min' => 36, 'months_max' => 59],
    'FIVE_TO_TEN' => ['name' => '5-10 Years', 'months_min' => 60, 'months_max' => 119],
    'TEN_PLUS' => ['name' => '10+ Years', 'months_min' => 120, 'months_max' => null]
];

// Vehicle Ownership Categories
const OWNERSHIP_CATEGORIES = [
    'FINANCED' => ['name' => 'Financed', 'requires_lienholder' => true],
    'LEASED' => ['name' => 'Leased', 'requires_lessor' => true],
    'OWNED' => ['name' => 'Owned', 'requires_title' => true]
];
```

#### Matrix Factor Calculation
```php
class PolicyCoreMatrixService
{
    public function calculateMatrixFactor(
        PriorInsuranceData $priorInsurance,
        LicenseHistoryData $licenseHistory,
        VehicleOwnershipData $ownership
    ): MatrixFactor {
        // 1. Determine prior insurance category
        $priorInsuranceCategory = $this->categorizePriorInsurance($priorInsurance);
        
        // 2. Determine years licensed category
        $yearsLicensedCategory = $this->categorizeYearsLicensed($licenseHistory);
        
        // 3. Determine ownership category
        $ownershipCategory = $this->categorizeOwnership($ownership);
        
        // 4. Lookup matrix factor
        $matrixFactor = DB::table('policy_core_matrix_factor')
            ->join('policy_core_matrix_value as pi', 'policy_core_matrix_factor.prior_insurance_value_id', '=', 'pi.id')
            ->join('policy_core_matrix_value as yl', 'policy_core_matrix_factor.years_licensed_value_id', '=', 'yl.id')
            ->join('policy_core_matrix_value as ow', 'policy_core_matrix_factor.ownership_value_id', '=', 'ow.id')
            ->where('pi.value_code', $priorInsuranceCategory)
            ->where('yl.value_code', $yearsLicensedCategory)
            ->where('ow.value_code', $ownershipCategory)
            ->where('policy_core_matrix_factor.program_id', $this->programId)
            ->where('policy_core_matrix_factor.effective_date', '<=', now())
            ->where(function($query) {
                $query->whereNull('policy_core_matrix_factor.expiration_date')
                      ->orWhere('policy_core_matrix_factor.expiration_date', '>', now());
            })
            ->first();
            
        if (!$matrixFactor) {
            throw new MatrixFactorNotFoundException(
                "No matrix factor found for combination: {$priorInsuranceCategory}, {$yearsLicensedCategory}, {$ownershipCategory}"
            );
        }
        
        return new MatrixFactor([
            'factor_value' => $matrixFactor->matrix_factor,
            'prior_insurance_category' => $priorInsuranceCategory,
            'years_licensed_category' => $yearsLicensedCategory,
            'ownership_category' => $ownershipCategory,
            'discount_percentage' => (1 - $matrixFactor->matrix_factor) * 100
        ]);
    }
}
```

### Prior Insurance Verification Logic
```php
class PriorInsuranceVerificationService
{
    public function verifyPriorInsurance(PriorInsuranceData $data): VerificationResult
    {
        $verificationResult = new VerificationResult();
        
        // 1. Validate insurance company
        if (!$this->validateInsuranceCompany($data->company_name)) {
            $verificationResult->addError('Invalid insurance company name');
        }
        
        // 2. Check continuous coverage
        $continuousCoverage = $this->calculateContinuousCoverage($data->coverage_periods);
        if ($continuousCoverage->hasSignificantLapse()) {
            $verificationResult->addWarning('Significant coverage lapse detected');
        }
        
        // 3. Validate coverage end date
        $daysSinceExpiration = now()->diffInDays($data->last_coverage_end_date);
        if ($daysSinceExpiration > 30) {
            $verificationResult->addError('Coverage lapse exceeds 30-day tolerance period');
        }
        
        // 4. Documentation verification
        if (!$data->hasDocumentation()) {
            $verificationResult->addError('Required documentation not provided');
        }
        
        return $verificationResult;
    }
}
```

---

## 5. Aguila Dorada Matrix Implementation

### Complete Three-Dimensional Matrix
```sql
-- Sample matrix factors for Aguila Dorada program
-- Format: (Prior Insurance, Years Licensed, Ownership) = Factor

-- Best combination: 3+ Years Insurance, 10+ Years Licensed, Owned = 0.44 (56% discount)
INSERT INTO policy_core_matrix_factor (program_id, prior_insurance_value_id, years_licensed_value_id, ownership_value_id, matrix_factor, effective_date) VALUES
(1, (SELECT id FROM policy_core_matrix_value WHERE value_code = 'THREE_YEARS_PLUS'), (SELECT id FROM policy_core_matrix_value WHERE value_code = 'TEN_PLUS'), (SELECT id FROM policy_core_matrix_value WHERE value_code = 'OWNED'), 0.4400, '2025-07-15'),

-- Worst combination: No Insurance, Less than 1 Year Licensed, Financed = 1.00 (No discount)
(1, (SELECT id FROM policy_core_matrix_value WHERE value_code = 'NONE'), (SELECT id FROM policy_core_matrix_value WHERE value_code = 'LESS_1_YEAR'), (SELECT id FROM policy_core_matrix_value WHERE value_code = 'FINANCED'), 1.0000, '2025-07-15'),

-- Mid-range combinations with graduated discounts
(1, (SELECT id FROM policy_core_matrix_value WHERE value_code = 'ONE_YEAR_PLUS'), (SELECT id FROM policy_core_matrix_value WHERE value_code = 'THREE_TO_FIVE'), (SELECT id FROM policy_core_matrix_value WHERE value_code = 'OWNED'), 0.7200, '2025-07-15'),

(1, (SELECT id FROM policy_core_matrix_value WHERE value_code = 'SIX_MONTHS_PLUS'), (SELECT id FROM policy_core_matrix_value WHERE value_code = 'FIVE_TO_TEN'), (SELECT id FROM policy_core_matrix_value WHERE value_code = 'LEASED'), 0.8100, '2025-07-15');
```

### Matrix Validation Rules
```php
class MatrixValidator
{
    public function validateMatrixCompleteness(int $programId): ValidationResult
    {
        // Ensure all possible combinations have defined factors
        $expectedCombinations = count(PRIOR_INSURANCE_CATEGORIES) * 
                               count(YEARS_LICENSED_CATEGORIES) * 
                               count(OWNERSHIP_CATEGORIES);
                               
        $actualCombinations = DB::table('policy_core_matrix_factor')
            ->where('program_id', $programId)
            ->where('status_id', Status::ACTIVE)
            ->count();
            
        if ($actualCombinations < $expectedCombinations) {
            return ValidationResult::fail(
                "Matrix incomplete: {$actualCombinations} of {$expectedCombinations} combinations defined"
            );
        }
        
        return ValidationResult::pass();
    }
}
```

---

## 6. API Integration Requirements

### Matrix Calculation Endpoints
```php
// Core matrix endpoints
POST /api/v1/rating/core-matrix/calculate
{
    "prior_insurance": {
        "company_name": "State Farm",
        "coverage_periods": [
            {
                "start_date": "2022-01-01",
                "end_date": "2024-12-31",
                "coverage_types": ["LIABILITY", "COMPREHENSIVE", "COLLISION"]
            }
        ]
    },
    "license_history": {
        "first_licensed_date": "2015-03-15",
        "license_state": "TX",
        "license_number": "12345678"
    },
    "vehicle_ownership": {
        "ownership_type": "OWNED",
        "title_documentation": true
    }
}

GET /api/v1/rating/core-matrix/breakdown/{calculationId}
// Returns detailed matrix calculation breakdown

POST /api/v1/rating/core-matrix/verify-insurance
{
    "insurance_data": {...}
}
// Verify prior insurance information
```

### Response Format
```json
{
    "matrix_factor": 0.7200,
    "discount_percentage": 28.0,
    "factor_breakdown": {
        "prior_insurance": {
            "category": "ONE_YEAR_PLUS",
            "verified": true,
            "months_continuous": 24
        },
        "years_licensed": {
            "category": "THREE_TO_FIVE",
            "years": 4.2,
            "verified": true
        },
        "vehicle_ownership": {
            "category": "OWNED",
            "documentation_verified": true
        }
    },
    "verification_status": {
        "overall": "VERIFIED",
        "prior_insurance": "VERIFIED",
        "license_history": "VERIFIED",
        "ownership": "VERIFIED"
    }
}
```

---

## 7. Validation Requirements

### Matrix Input Validation
```php
class CoreMatrixValidator
{
    public function validatePriorInsurance(PriorInsuranceData $data): ValidationResult
    {
        $result = new ValidationResult();
        
        // 1. Coverage period validation
        foreach ($data->coverage_periods as $period) {
            if ($period->end_date < $period->start_date) {
                $result->addError('Invalid coverage period: end date before start date');
            }
        }
        
        // 2. Coverage gap validation
        $gaps = $this->findCoverageGaps($data->coverage_periods);
        foreach ($gaps as $gap) {
            if ($gap->days > 30) {
                $result->addWarning("Coverage gap of {$gap->days} days exceeds 30-day tolerance");
            }
        }
        
        // 3. Documentation validation
        if (!$data->hasDocumentation() && $data->claims_continuous_coverage) {
            $result->addError('Documentation required for continuous coverage claims');
        }
        
        return $result;
    }
}
```

---

## 8. Performance Optimization

### Matrix Lookup Caching
```php
class PolicyCoreMatrixService
{
    public function calculateMatrixFactor(...$params): MatrixFactor
    {
        // Create cache key from matrix dimensions
        $cacheKey = "core_matrix_{$this->programId}_" . 
                   md5(serialize([$priorInsuranceCategory, $yearsLicensedCategory, $ownershipCategory]));
        
        return Cache::remember($cacheKey, 3600, function() use ($params) {
            return $this->performMatrixLookup(...$params);
        });
    }
}
```

### Database Optimization
```sql
-- Composite index for optimal matrix lookup
CREATE INDEX idx_matrix_lookup_optimized 
ON policy_core_matrix_factor (
    program_id, 
    prior_insurance_value_id, 
    years_licensed_value_id, 
    ownership_value_id,
    effective_date
) WHERE status_id = 1;
```

---

## 9. Testing Requirements

### Matrix Calculation Testing
```php
class PolicyCoreMatrixServiceTest extends TestCase
{
    public function test_maximum_discount_combination()
    {
        // Test best case: 3+ years insurance, 10+ years licensed, owned
        $result = $this->matrixService->calculateMatrixFactor(
            new PriorInsuranceData(['category' => 'THREE_YEARS_PLUS']),
            new LicenseHistoryData(['years' => 15]),
            new VehicleOwnershipData(['type' => 'OWNED'])
        );
        
        $this->assertEquals(0.44, $result->factor_value);
        $this->assertEquals(56, $result->discount_percentage);
    }
    
    public function test_no_discount_combination()
    {
        // Test worst case: no insurance, new license, financed
        $result = $this->matrixService->calculateMatrixFactor(
            new PriorInsuranceData(['category' => 'NONE']),
            new LicenseHistoryData(['years' => 0.5]),
            new VehicleOwnershipData(['type' => 'FINANCED'])
        );
        
        $this->assertEquals(1.00, $result->factor_value);
        $this->assertEquals(0, $result->discount_percentage);
    }
}
```

---

## Implementation Priority: HIGH
This factor provides significant premium discounts and is essential for competitive pricing. Should be implemented early after base rating engine.

## Dependencies
- **Algorithm Factor**: Requires core rating engine for matrix calculation
- **Vehicle Base Rates**: Matrix factor multiplies against base rates

## Estimated Implementation Effort
- **Database Schema**: 4 days
- **Service Layer**: 6 days
- **Verification Logic**: 4 days
- **API Integration**: 3 days
- **Testing**: 4 days
- **Total**: 21 days

This plan implements the sophisticated three-dimensional discount matrix that provides competitive pricing advantages while maintaining proper verification and audit requirements.