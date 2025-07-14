# Algorithm Rate Factor Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Algorithm  
**Category**: Core Rating Component  
**Priority**: Critical - Foundation for all premium calculations  
**Implementation Complexity**: High  

### Business Requirements Summary
The Algorithm rate factor defines the core multiplicative rating methodology that serves as the foundation for all premium calculations in the Aguila Dorada Texas Personal Auto program. This factor establishes the calculation sequence, validation rules, and performance standards for the entire rating engine.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor requires the following new Global Requirements:

#### GR-65: Rating Engine Architecture
**Priority**: Critical  
**Rationale**: Core rating calculation patterns and service architecture needed for all rating factors  

**Core Components**:
- RatingEngineService with multiplicative calculation logic
- Factor validation and lookup infrastructure  
- Premium calculation audit trails
- Performance optimization for rating systems

#### GR-66: Insurance Risk Assessment Framework  
**Priority**: High  
**Rationale**: Risk factor validation and business rule patterns  

**Core Components**:
- Factor range validation and business rules
- Calculation sequence enforcement
- Premium reasonableness checks
- Regulatory compliance validation

### Integration with Existing Global Requirements
- **GR-20**: Application Business Logic - Service architecture patterns for RatingEngineService
- **GR-41**: Table Schema Requirements - Database schema for calculation audit tables
- **GR-18**: Workflow Requirements - Integration with quote and policy workflows
- **GR-33**: Data Services Architecture - Caching strategies for rating calculations

---

## 2. Service Architecture Requirements

### Core Rating Services

#### RatingEngineService
**Purpose**: Central multiplicative rating calculation engine  
**Location**: `app/Domain/Rating/Services/RatingEngineService.php`

**Key Methods**:
```php
class RatingEngineService
{
    public function calculatePremium(PolicyRatingRequest $request): PremiumCalculation
    {
        // 1. Validate all required rating inputs
        // 2. Retrieve territory base rates
        // 3. Apply factors in multiplicative sequence
        // 4. Validate final premium reasonableness
        // 5. Store calculation audit trail
        // 6. Return calculation result with breakdown
    }
    
    public function validateRatingSequence(array $factors): ValidationResult
    {
        // Validate factor calculation sequence and dependencies
    }
    
    public function applyFactorMultiplication(float $basePremium, array $factors): CalculationResult
    {
        // Apply multiplicative factor sequence with audit trail
    }
}
```

#### CalculationAuditService
**Purpose**: Comprehensive audit trail for all rating calculations  
**Location**: `app/Domain/Rating/Services/CalculationAuditService.php`

**Key Methods**:
```php
class CalculationAuditService
{
    public function logCalculationStep(int $calculationId, RatingStep $step): void
    public function getCalculationBreakdown(int $calculationId): CalculationBreakdown
    public function validateCalculationIntegrity(int $calculationId): ValidationResult
}
```

---

## 3. Database Schema Requirements

### Core Calculation Tables

#### premium_calculation
```sql
CREATE TABLE premium_calculation (
    id BIGINT PRIMARY KEY,
    policy_id BIGINT,
    quote_id BIGINT,
    calculation_type ENUM('QUOTE', 'POLICY', 'RENEWAL', 'ADJUSTMENT') NOT NULL,
    base_premium DECIMAL(12,2) NOT NULL,
    total_premium DECIMAL(12,2) NOT NULL,
    calculation_sequence JSON NOT NULL, -- Ordered list of applied factors
    calculation_metadata JSON,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (quote_id) REFERENCES quote(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_policy_calculation (policy_id, created_at),
    INDEX idx_quote_calculation (quote_id, created_at),
    INDEX idx_calculation_type (calculation_type, created_at)
);
```

#### calculation_step
```sql
CREATE TABLE calculation_step (
    id BIGINT PRIMARY KEY,
    calculation_id BIGINT NOT NULL,
    step_number INT NOT NULL,
    factor_type VARCHAR(100) NOT NULL,
    factor_code VARCHAR(100) NOT NULL,
    factor_value DECIMAL(10,6) NOT NULL,
    premium_before DECIMAL(12,2) NOT NULL,
    premium_after DECIMAL(12,2) NOT NULL,
    calculation_method VARCHAR(50) NOT NULL,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (calculation_id) REFERENCES premium_calculation(id),
    
    INDEX idx_calculation_steps (calculation_id, step_number),
    INDEX idx_factor_tracking (factor_type, factor_code, created_at)
);
```

#### calculation_validation
```sql
CREATE TABLE calculation_validation (
    id BIGINT PRIMARY KEY,
    calculation_id BIGINT NOT NULL,
    validation_type VARCHAR(100) NOT NULL,
    validation_result ENUM('PASS', 'WARNING', 'FAIL') NOT NULL,
    validation_message TEXT,
    validation_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (calculation_id) REFERENCES premium_calculation(id),
    
    INDEX idx_calculation_validation (calculation_id, validation_type),
    INDEX idx_validation_results (validation_result, created_at)
);
```

---

## 4. Business Logic Requirements

### Multiplicative Calculation Rules

#### Core Calculation Formula
```php
// Multiplicative rating sequence
$premium = $baseRate;
foreach ($ratingFactors as $factor) {
    $premium *= $factor->value;
    $this->auditService->logCalculationStep($calculationId, [
        'factor_type' => $factor->type,
        'factor_value' => $factor->value,
        'premium_before' => $previousPremium,
        'premium_after' => $premium
    ]);
}
```

#### Factor Application Sequence
1. **Base Rate Selection**: Territory-based foundation rates
2. **Policy Core Matrix**: Three-dimensional discount matrix
3. **Driver Classification**: Demographics and risk factors
4. **Driver Points**: Violations and convictions
5. **Vehicle Factors**: Age, use, make/model adjustments
6. **Coverage Factors**: Limits and deductible selections
7. **Policy Adjustments**: Final policy-level modifications

#### Validation Requirements
- **Factor Completeness**: All required factors must have values
- **Range Validation**: Each factor must fall within acceptable bounds (0.1 to 10.0)
- **Sequence Validation**: Factors must be applied in correct order
- **Result Validation**: Final premium must pass reasonableness checks

### Performance Requirements
- **Calculation Speed**: Complete rating in under 2 seconds
- **Accuracy**: 99.9% calculation accuracy with proper rounding
- **Consistency**: Identical inputs produce identical results
- **Scalability**: Support for high-volume concurrent calculations

---

## 5. API Integration Requirements

### Rating Calculation Endpoints
```php
// Core rating API endpoints
POST /api/v1/rating/calculate
{
    "policy_data": {...},
    "driver_data": [...],
    "vehicle_data": [...],
    "coverage_selections": {...}
}

GET /api/v1/rating/breakdown/{calculation_id}
// Returns detailed factor-by-factor breakdown

POST /api/v1/rating/validate
{
    "rating_inputs": {...}
}
// Validates rating inputs before calculation
```

### Response Format
```json
{
    "calculation_id": 12345,
    "total_premium": 1250.75,
    "base_premium": 800.00,
    "factor_breakdown": [
        {
            "factor_type": "policy_core_matrix",
            "factor_value": 0.85,
            "premium_impact": -120.00
        },
        {
            "factor_type": "driver_class",
            "factor_value": 1.25,
            "premium_impact": 170.00
        }
    ],
    "validation_results": [...],
    "calculation_metadata": {...}
}
```

---

## 6. Caching Strategy

### Multi-Tier Caching Architecture

#### L1 Cache - Application Level
```php
// Rating calculation cache
Cache::remember("rating_calculation_{$policyId}", 3600, function() {
    return $this->ratingEngine->calculatePremium($request);
});

// Factor lookup cache
Cache::remember("rating_factors_{$factorType}_{$programId}", 3600, function() {
    return $this->factorService->getFactorsByType($factorType, $programId);
});
```

#### L2 Cache - Redis
- **Calculation Results**: Policy-specific calculation caching
- **Factor Combinations**: Common factor combination results
- **Validation Rules**: Business rule caching for performance

#### Cache Invalidation Strategy
- **Factor Updates**: Invalidate all related calculation caches
- **Policy Changes**: Invalidate policy-specific calculation cache
- **System Updates**: Selective cache invalidation based on changed components

---

## 7. Validation and Error Handling

### Input Validation Rules
```php
class RatingCalculationRequest extends FormRequest
{
    public function rules()
    {
        return [
            'policy_data.effective_date' => 'required|date',
            'policy_data.term_months' => 'required|integer|in:6,12',
            'policy_data.territory_code' => 'required|exists:rating_territory,territory_code',
            'driver_data.*.age' => 'required|integer|between:16,100',
            'vehicle_data.*.model_year' => 'required|integer|between:1980,2026',
            'coverage_selections.liability_limits' => 'required|valid_liability_limits'
        ];
    }
}
```

### Error Handling Strategy
- **Validation Errors**: Return detailed validation messages
- **Calculation Errors**: Log error and return default/fallback premium
- **System Errors**: Graceful degradation with audit trail
- **Timeout Handling**: Circuit breaker pattern for external dependencies

---

## 8. Testing Requirements

### Unit Testing
```php
class RatingEngineServiceTest extends TestCase
{
    public function test_multiplicative_calculation_accuracy()
    {
        // Test factor multiplication accuracy
    }
    
    public function test_calculation_sequence_validation()
    {
        // Test factor application order
    }
    
    public function test_premium_reasonableness_validation()
    {
        // Test premium bounds checking
    }
}
```

### Integration Testing
- **API Integration**: Rating endpoint testing with complete workflows
- **Database Integration**: Calculation storage and audit trail testing
- **Cache Integration**: Caching performance and consistency testing

### Performance Testing
- **Load Testing**: 1000+ concurrent rating calculations
- **Response Time**: Sub-2-second calculation requirements
- **Memory Usage**: Efficient memory utilization during calculations

---

## 9. Monitoring and Alerting

### Key Performance Indicators
- **Average Calculation Time**: Target <1.5 seconds
- **Calculation Success Rate**: Target >99.9%
- **Cache Hit Rate**: Target >90% for factor lookups
- **Daily Calculation Volume**: Monitor for capacity planning

### Alerting Thresholds
- **Response Time**: >5 seconds for individual calculations
- **Error Rate**: >1% calculation failures
- **Cache Performance**: <80% cache hit rate

### Monitoring Implementation
```php
// Performance monitoring in RatingEngineService
$startTime = microtime(true);
$result = $this->calculatePremium($request);
$calculationTime = microtime(true) - $startTime;

$this->metrics->timing('rating.calculation.duration', $calculationTime);
$this->metrics->increment('rating.calculation.success');
```

---

## 10. Security and Compliance

### Security Requirements
- **Input Sanitization**: All rating inputs sanitized and validated
- **Calculation Integrity**: Cryptographic validation of critical calculations
- **Audit Trail Security**: Tamper-proof calculation audit logs
- **Access Control**: Role-based access to rating administration

### Regulatory Compliance
- **Rate Filing Compliance**: Calculations must match filed rates
- **Actuarial Support**: Statistical justification for all calculation methods
- **Transparency**: Detailed breakdown available for regulatory review
- **Historical Retention**: 7-year retention of calculation audit trails

---

## Implementation Priority: CRITICAL
This factor must be implemented first as it provides the foundation for all other rating factors. The multiplicative calculation engine and audit infrastructure are dependencies for all subsequent factor implementations.

## Dependencies
- **None** - This is the foundational factor
- **Required for**: All other 33 rating factors depend on this implementation

## Estimated Implementation Effort
- **Database Schema**: 2 days
- **Service Layer**: 5 days  
- **API Integration**: 2 days
- **Testing**: 3 days
- **Performance Optimization**: 2 days
- **Total**: 14 days

This plan establishes the core rating engine foundation that all other factors will build upon, ensuring consistent calculation methodology and comprehensive audit capabilities throughout the rating system.