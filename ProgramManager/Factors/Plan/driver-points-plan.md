# Driver Points Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Driver Points  
**Category**: Core Rating Component  
**Priority**: High - Violation and conviction risk assessment  
**Implementation Complexity**: High  

### Business Requirements Summary
The Driver Points factor implements a progressive multiplier system based on motor vehicle violations and convictions within a 3-year lookback period. This factor provides risk-based pricing that ranges from base rates (1.00 for clean records) to extremely high surcharges (25.50 for serious violations), reflecting the statistical relationship between driving violations and claim frequency.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing and new Global Requirements:

#### Leverages GR-65: Rating Engine Architecture
**Integration**: Violation point calculation within multiplicative rating engine  
**Dependencies**: RatingEngineService for point accumulation and factor lookup

#### New Requirement: GR-73: Motor Vehicle Record Integration
**Priority**: Critical  
**Rationale**: MVR integration and violation tracking standards for accurate risk assessment  

**Core Components**:
- State MVR API integration patterns
- Violation classification and point assignment standards
- Conviction date tracking and 3-year lookback implementation
- Multi-state violation coordination and data normalization
- Third-party MVR service integration architecture

#### New Requirement: GR-74: Violation Point Management
**Priority**: High  
**Rationale**: Point calculation and factor assignment standards  

**Core Components**:
- Violation point assignment methodology
- Progressive factor calculation algorithms
- Point accumulation and expiration tracking
- Exception handling for unusual violations
- Manual override and underwriting exception processes

### Integration with Existing Global Requirements
- **GR-53**: DCS Integration Architecture - MVR data integration patterns
- **GR-41**: Table Schema Requirements - Violation and point tracking tables
- **GR-20**: Application Business Logic - Point calculation service patterns

---

## 2. Service Architecture Requirements

### Violation Point Services

#### DriverPointsService
**Purpose**: Driver violation point calculation and factor determination  
**Location**: `app/Domain/Rating/Services/DriverPointsService.php`

**Key Methods**:
```php
class DriverPointsService
{
    public function calculateDriverPointsFactor(int $driverId, Carbon $effectiveDate): DriverPointsFactor
    {
        // 1. Retrieve all violations within 3-year lookback period
        // 2. Calculate total point accumulation
        // 3. Apply progressive factor scale
        // 4. Return factor with violation breakdown
    }
    
    public function calculateTotalPoints(Collection $violations, Carbon $effectiveDate): int
    {
        // Calculate total points from active violations within lookback period
    }
    
    public function determineFactorFromPoints(int $totalPoints): float
    {
        // Apply progressive factor scale based on total points
    }
    
    public function getViolationBreakdown(int $driverId, Carbon $effectiveDate): ViolationBreakdown
    {
        // Provide detailed breakdown of violations and point assignments
    }
}
```

#### MVRIntegrationService
**Purpose**: Motor Vehicle Record integration and violation data retrieval  
**Location**: `app/Domain/Rating/Services/MVRIntegrationService.php`

**Key Methods**:
```php
class MVRIntegrationService
{
    public function retrieveDriverMVR(string $licenseNumber, string $state): MVRResult
    {
        // Integrate with state MVR systems to retrieve violation history
    }
    
    public function normalizeViolationData(array $mvrData): Collection
    {
        // Normalize violation data from multiple state formats
    }
    
    public function validateConvictionDate(ViolationData $violation): ValidationResult
    {
        // Validate conviction dates and court information
    }
}
```

#### ViolationClassificationService
**Purpose**: Violation classification and point assignment  
**Location**: `app/Domain/Rating/Services/ViolationClassificationService.php`

**Key Methods**:
```php
class ViolationClassificationService
{
    public function classifyViolation(ViolationData $violation): ViolationClassification
    {
        // Classify violation type and assign appropriate points
    }
    
    public function assignPoints(string $violationType, array $violationDetails): int
    {
        // Assign points based on violation severity and type
    }
    
    public function validateViolationEligibility(ViolationData $violation): bool
    {
        // Validate if violation counts toward rating (final conviction only)
    }
}
```

---

## 3. Database Schema Requirements

### Violation Point Management Tables

#### violation_type
```sql
CREATE TABLE violation_type (
    id BIGINT PRIMARY KEY,
    violation_code VARCHAR(50) UNIQUE NOT NULL,
    violation_name VARCHAR(255) NOT NULL,
    violation_description TEXT,
    severity_level ENUM('MINOR', 'MODERATE', 'MAJOR', 'SERIOUS') NOT NULL,
    base_points INT NOT NULL,
    is_chargeable BOOLEAN DEFAULT TRUE,
    requires_conviction BOOLEAN DEFAULT TRUE,
    affects_eligibility BOOLEAN DEFAULT FALSE,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_violation_severity (severity_level, status_id),
    INDEX idx_chargeable_violations (is_chargeable, status_id)
);
```

#### driver_violation
```sql
CREATE TABLE driver_violation (
    id BIGINT PRIMARY KEY,
    driver_id BIGINT NOT NULL,
    violation_type_id BIGINT NOT NULL,
    violation_date DATE NOT NULL,
    conviction_date DATE,
    citation_number VARCHAR(100),
    court_jurisdiction VARCHAR(255),
    fine_amount DECIMAL(8,2),
    points_assigned INT NOT NULL,
    violation_state_id BIGINT NOT NULL,
    mvr_source VARCHAR(100),
    mvr_retrieved_date DATE,
    is_final_conviction BOOLEAN DEFAULT FALSE,
    affects_rating BOOLEAN DEFAULT TRUE,
    manual_override BOOLEAN DEFAULT FALSE,
    override_reason TEXT,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (driver_id) REFERENCES driver(id),
    FOREIGN KEY (violation_type_id) REFERENCES violation_type(id),
    FOREIGN KEY (violation_state_id) REFERENCES state(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_driver_violations (driver_id, conviction_date),
    INDEX idx_rating_violations (driver_id, affects_rating, conviction_date),
    INDEX idx_conviction_dates (conviction_date, is_final_conviction),
    INDEX idx_mvr_source (mvr_source, mvr_retrieved_date)
);
```

#### driver_points_calculation
```sql
CREATE TABLE driver_points_calculation (
    id BIGINT PRIMARY KEY,
    driver_id BIGINT NOT NULL,
    calculation_date DATE NOT NULL,
    lookback_start_date DATE NOT NULL,
    lookback_end_date DATE NOT NULL,
    total_points INT NOT NULL,
    point_factor DECIMAL(6,4) NOT NULL,
    active_violations_count INT NOT NULL,
    calculation_metadata JSON,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (driver_id) REFERENCES driver(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_driver_point_history (driver_id, calculation_date),
    INDEX idx_calculation_lookup (driver_id, lookback_start_date, lookback_end_date),
    INDEX idx_point_totals (total_points, point_factor)
);
```

#### driver_points_factor_scale
```sql
CREATE TABLE driver_points_factor_scale (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    points_min INT NOT NULL,
    points_max INT, -- NULL for open-ended ranges
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
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_points_range (program_id, points_min, effective_date),
    INDEX idx_program_scale (program_id, effective_date),
    INDEX idx_points_lookup (points_min, points_max),
    INDEX idx_effective_dates (effective_date, expiration_date)
);
```

---

## 4. Business Logic Requirements

### Point Calculation Logic

#### 3-Year Lookback Implementation
```php
class DriverPointsService
{
    public function calculateDriverPointsFactor(int $driverId, Carbon $effectiveDate): DriverPointsFactor
    {
        // 1. Define 3-year lookback period
        $lookbackStart = $effectiveDate->copy()->subYears(3);
        $lookbackEnd = $effectiveDate;
        
        // 2. Retrieve all violations within lookback period
        $violations = DB::table('driver_violation')
            ->join('violation_type', 'driver_violation.violation_type_id', '=', 'violation_type.id')
            ->where('driver_violation.driver_id', $driverId)
            ->where('driver_violation.affects_rating', true)
            ->where('driver_violation.is_final_conviction', true)
            ->where('driver_violation.conviction_date', '>=', $lookbackStart)
            ->where('driver_violation.conviction_date', '<', $lookbackEnd)
            ->where('driver_violation.status_id', Status::ACTIVE)
            ->get();
        
        // 3. Calculate total points
        $totalPoints = $violations->sum('points_assigned');
        
        // 4. Determine factor from points
        $factor = $this->determineFactorFromPoints($totalPoints);
        
        // 5. Store calculation for audit
        $this->storePointsCalculation($driverId, $totalPoints, $factor, $lookbackStart, $lookbackEnd);
        
        return new DriverPointsFactor([
            'driver_id' => $driverId,
            'total_points' => $totalPoints,
            'factor_value' => $factor,
            'violation_count' => $violations->count(),
            'lookback_period' => "{$lookbackStart->format('Y-m-d')} to {$lookbackEnd->format('Y-m-d')}",
            'violations' => $violations
        ]);
    }
}
```

#### Progressive Factor Scale
```php
class DriverPointsService
{
    public function determineFactorFromPoints(int $totalPoints): float
    {
        // Aguila Dorada progressive point scale
        $pointScale = [
            0 => 1.00,      // Clean record
            1 => 1.15,      // 1 point - 15% surcharge
            2 => 1.25,      // 2 points - 25% surcharge
            3 => 1.35,      // 3 points - 35% surcharge
            4 => 1.50,      // 4 points - 50% surcharge
            5 => 1.65,      // 5 points - 65% surcharge
            6 => 1.85,      // 6 points - 85% surcharge
            7 => 2.10,      // 7 points - 110% surcharge
            8 => 2.40,      // 8 points - 140% surcharge
            9 => 2.75,      // 9 points - 175% surcharge
            10 => 3.15,     // 10 points - 215% surcharge
            15 => 5.75,     // 15 points - 475% surcharge
            20 => 12.50,    // 20 points - 1150% surcharge
            25 => 25.50     // 25+ points - 2450% surcharge (maximum)
        ];
        
        // Find appropriate factor for point total
        $applicableFactor = 1.00;
        foreach ($pointScale as $points => $factor) {
            if ($totalPoints >= $points) {
                $applicableFactor = $factor;
            } else {
                break;
            }
        }
        
        return $applicableFactor;
    }
}
```

### Violation Classification Logic
```php
class ViolationClassificationService
{
    // Aguila Dorada violation point assignments
    const VIOLATION_POINTS = [
        // Minor Violations (1-2 points)
        'SPEEDING_1_10' => 1,           // Speeding 1-10 mph over
        'SPEEDING_11_15' => 2,          // Speeding 11-15 mph over
        'IMPROPER_LANE_CHANGE' => 1,    // Improper lane change
        'FOLLOWING_TOO_CLOSE' => 2,     // Following too closely
        
        // Moderate Violations (3-4 points)
        'SPEEDING_16_25' => 3,          // Speeding 16-25 mph over
        'FAILURE_TO_YIELD' => 3,        // Failure to yield
        'RUNNING_RED_LIGHT' => 4,       // Running red light
        'STOP_SIGN_VIOLATION' => 3,     // Stop sign violation
        
        // Major Violations (5-8 points)
        'SPEEDING_26_PLUS' => 5,        // Speeding 26+ mph over
        'RECKLESS_DRIVING' => 8,        // Reckless driving
        'RACING' => 8,                  // Racing on highway
        'LEAVING_SCENE' => 8,           // Leaving scene of accident
        
        // Serious Violations (10+ points)
        'DUI_DWI' => 15,               // DUI/DWI conviction
        'DRIVING_SUSPENDED' => 10,      // Driving while suspended
        'VEHICULAR_ASSAULT' => 20,      // Vehicular assault
        'FELONY_INVOLVING_VEHICLE' => 25 // Felony involving vehicle
    ];
    
    public function assignPoints(string $violationType, array $violationDetails): int
    {
        $basePoints = self::VIOLATION_POINTS[$violationType] ?? 0;
        
        // Apply modifiers based on violation details
        if (isset($violationDetails['speed_over_limit'])) {
            $speedOver = $violationDetails['speed_over_limit'];
            if ($speedOver >= 30) {
                $basePoints = max($basePoints, 6); // Minimum 6 points for excessive speed
            }
        }
        
        // Accident involvement modifier
        if ($violationDetails['accident_involved'] ?? false) {
            $basePoints += 2; // Additional 2 points for accident involvement
        }
        
        return $basePoints;
    }
}
```

---

## 5. MVR Integration Requirements

### State MVR API Integration
```php
class MVRIntegrationService
{
    public function retrieveDriverMVR(string $licenseNumber, string $state): MVRResult
    {
        // Integration with state-specific MVR systems
        switch ($state) {
            case 'TX':
                return $this->retrieveTexasMVR($licenseNumber);
            case 'CA':
                return $this->retrieveCaliforniaMVR($licenseNumber);
            default:
                return $this->retrieveGenericMVR($licenseNumber, $state);
        }
    }
    
    private function retrieveTexasMVR(string $licenseNumber): MVRResult
    {
        // Texas DPS MVR integration
        $response = $this->httpClient->post('https://mvr.txdps.state.tx.us/api/v1/records', [
            'license_number' => $licenseNumber,
            'api_key' => $this->getTexasMVRApiKey(),
            'request_type' => 'FULL_RECORD'
        ]);
        
        return $this->normalizeTexasMVRResponse($response);
    }
    
    public function normalizeViolationData(array $mvrData): Collection
    {
        $violations = collect();
        
        foreach ($mvrData['violations'] as $violation) {
            $normalizedViolation = [
                'violation_code' => $this->mapViolationCode($violation['code']),
                'violation_date' => Carbon::parse($violation['date']),
                'conviction_date' => isset($violation['conviction_date']) 
                    ? Carbon::parse($violation['conviction_date']) 
                    : null,
                'description' => $violation['description'],
                'court' => $violation['court'] ?? null,
                'fine_amount' => $violation['fine'] ?? null,
                'state' => $violation['state']
            ];
            
            $violations->push($normalizedViolation);
        }
        
        return $violations;
    }
}
```

### Third-Party MVR Service Integration
```php
class ThirdPartyMVRService
{
    // Integration with services like LexisNexis, Verisk, etc.
    public function retrieveMVRFromLexisNexis(string $licenseNumber, string $state): MVRResult
    {
        $response = $this->httpClient->post('https://api.lexisnexis.com/mvr/v1/search', [
            'headers' => [
                'Authorization' => 'Bearer ' . $this->getLexisNexisToken(),
                'Content-Type' => 'application/json'
            ],
            'json' => [
                'license_number' => $licenseNumber,
                'state' => $state,
                'search_type' => 'COMPREHENSIVE'
            ]
        ]);
        
        return $this->normalizeLexisNexisResponse($response);
    }
}
```

---

## 6. Validation Requirements

### Violation Data Validation
```php
class DriverViolationValidator
{
    public function validateViolationData(ViolationData $violation): ValidationResult
    {
        $result = new ValidationResult();
        
        // 1. Conviction date validation
        if ($violation->conviction_date && $violation->conviction_date < $violation->violation_date) {
            $result->addError('Conviction date cannot be before violation date');
        }
        
        // 2. Future date validation
        if ($violation->conviction_date && $violation->conviction_date->isFuture()) {
            $result->addError('Conviction date cannot be in the future');
        }
        
        // 3. Final conviction requirement
        if (!$violation->is_final_conviction && $violation->affects_rating) {
            $result->addError('Only final convictions can affect rating');
        }
        
        // 4. Point assignment validation
        if ($violation->points_assigned < 0 || $violation->points_assigned > 25) {
            $result->addError('Point assignment must be between 0 and 25');
        }
        
        return $result;
    }
    
    public function validatePointCalculation(int $driverId, int $totalPoints): ValidationResult
    {
        $result = new ValidationResult();
        
        // Maximum points validation
        if ($totalPoints > 50) {
            $result->addWarning("Unusually high point total: {$totalPoints} points");
        }
        
        // Point consistency validation
        $calculatedPoints = $this->recalculatePoints($driverId);
        if ($calculatedPoints !== $totalPoints) {
            $result->addError("Point calculation inconsistency: calculated {$calculatedPoints}, provided {$totalPoints}");
        }
        
        return $result;
    }
}
```

---

## 7. API Integration Requirements

### Driver Points Endpoints
```php
// Driver points calculation endpoints
POST /api/v1/rating/driver-points/calculate
{
    "driver_id": 12345,
    "effective_date": "2025-07-15"
}

GET /api/v1/rating/driver-points/breakdown/{driverId}
// Returns detailed violation and points breakdown

POST /api/v1/rating/driver-points/mvr-update
{
    "driver_id": 12345,
    "license_number": "TX123456789",
    "state": "TX"
}
// Trigger MVR update for driver

GET /api/v1/admin/violations/{driverId}
// Administrative violation management
```

### Response Format
```json
{
    "driver_id": 12345,
    "calculation_date": "2025-07-15",
    "total_points": 7,
    "point_factor": 2.10,
    "surcharge_percentage": 110.0,
    "lookback_period": {
        "start_date": "2022-07-15",
        "end_date": "2025-07-15"
    },
    "active_violations": [
        {
            "violation_id": 67890,
            "violation_type": "SPEEDING_16_25",
            "violation_date": "2023-05-10",
            "conviction_date": "2023-08-15",
            "points_assigned": 3,
            "description": "Speeding 18 mph over limit",
            "court": "Travis County Municipal Court"
        },
        {
            "violation_id": 67891,
            "violation_type": "RUNNING_RED_LIGHT",
            "violation_date": "2024-02-20",
            "conviction_date": "2024-04-10",
            "points_assigned": 4,
            "description": "Running red light at intersection"
        }
    ],
    "mvr_last_updated": "2025-07-01"
}
```

---

## 8. Performance Requirements

### Point Calculation Optimization
```php
class DriverPointsService
{
    public function calculateDriverPointsFactor(int $driverId, Carbon $effectiveDate): DriverPointsFactor
    {
        // Check for cached calculation within 24 hours
        $cacheKey = "driver_points_{$driverId}_{$effectiveDate->format('Y-m-d')}";
        
        return Cache::remember($cacheKey, 86400, function() use ($driverId, $effectiveDate) {
            return $this->performPointsCalculation($driverId, $effectiveDate);
        });
    }
}
```

### Database Performance
```sql
-- Optimized violation lookup for point calculation
CREATE INDEX idx_violation_points_calculation 
ON driver_violation (
    driver_id, 
    conviction_date, 
    affects_rating, 
    is_final_conviction,
    points_assigned
) WHERE status_id = 1;

-- Points factor scale lookup optimization
CREATE INDEX idx_points_factor_lookup 
ON driver_points_factor_scale (
    program_id, 
    points_min, 
    points_max,
    effective_date
) WHERE status_id = 1;
```

---

## 9. Testing Requirements

### Point Calculation Testing
```php
class DriverPointsServiceTest extends TestCase
{
    public function test_clean_record_factor()
    {
        // Test clean record: 0 points = 1.00 factor
        $factor = $this->driverPointsService->calculateDriverPointsFactor(
            $this->cleanDriverId, 
            Carbon::parse('2025-07-15')
        );
        
        $this->assertEquals(0, $factor->total_points);
        $this->assertEquals(1.00, $factor->factor_value);
    }
    
    public function test_maximum_factor()
    {
        // Test maximum factor: 25+ points = 25.50 factor
        $factor = $this->driverPointsService->calculateDriverPointsFactor(
            $this->highRiskDriverId, 
            Carbon::parse('2025-07-15')
        );
        
        $this->assertGreaterThanOrEqual(25, $factor->total_points);
        $this->assertEquals(25.50, $factor->factor_value);
    }
    
    public function test_three_year_lookback()
    {
        // Test 3-year lookback period exclusion
        $effectiveDate = Carbon::parse('2025-07-15');
        $oldViolationDate = Carbon::parse('2022-01-01'); // More than 3 years
        
        $factor = $this->driverPointsService->calculateDriverPointsFactor(
            $this->driverWithOldViolations, 
            $effectiveDate
        );
        
        // Old violations should not be included
        $this->assertEquals(0, $factor->total_points);
    }
}
```

---

## Implementation Priority: HIGH
This factor is critical for risk assessment and premium accuracy. Must be implemented early with proper MVR integration.

## Dependencies
- **Algorithm Factor**: Requires core rating engine for point factor calculation
- **Driver Class Factor**: Driver points multiply with demographic factors

## Estimated Implementation Effort
- **Database Schema**: 4 days
- **Service Layer**: 6 days
- **MVR Integration**: 5 days
- **Validation Logic**: 3 days
- **API Integration**: 3 days
- **Testing**: 4 days
- **Total**: 25 days

This plan implements comprehensive violation tracking and point-based risk assessment while maintaining proper MVR integration and regulatory compliance for accurate driver risk evaluation.