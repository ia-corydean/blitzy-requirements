# Driver Points Violations Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Driver Points Violations  
**Category**: Driver Factor  
**Priority**: High - Specific violation type point assignments  
**Implementation Complexity**: Medium  

### Business Requirements Summary
The Driver Points Violations factor provides the detailed violation classification system and specific point assignments that feed into the Driver Points core rating component. This factor establishes the granular violation-to-point mapping that determines the progressive surcharges applied to drivers based on their violation history within the 3-year lookback period.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing Global Requirements:

#### Leverages GR-73: Motor Vehicle Record Integration
**Integration**: Detailed violation classification feeding into MVR processing  
**Dependencies**: Violation type standardization and point assignment methodology

#### Leverages GR-74: Violation Point Management
**Integration**: Specific point assignments and violation categorization  
**Dependencies**: Point calculation algorithms and violation severity classification

#### New Requirement: GR-77: Violation Classification Standards
**Priority**: Medium  
**Rationale**: Standardized violation classification and point assignment methodology  

**Core Components**:
- Violation code standardization across state systems
- Point assignment methodology and severity classification
- Violation description normalization and categorization
- Exception handling for unusual or new violation types
- Violation point adjustment rules and manual override processes

### Integration with Existing Global Requirements
- **GR-65**: Rating Engine Architecture - Violation point integration with core rating
- **GR-41**: Table Schema Requirements - Violation classification table structures
- **GR-20**: Application Business Logic - Violation processing service patterns

---

## 2. Service Architecture Requirements

### Violation Classification Services

#### ViolationPointsService
**Purpose**: Specific violation point assignment and classification  
**Location**: `app/Domain/Rating/Services/ViolationPointsService.php`

**Key Methods**:
```php
class ViolationPointsService
{
    public function assignPointsToViolation(ViolationData $violation): int
    {
        // 1. Classify violation type from description/code
        // 2. Apply base point assignment rules
        // 3. Apply severity modifiers based on circumstances
        // 4. Return final point assignment
    }
    
    public function classifyViolationType(string $violationDescription, string $violationCode): ViolationType
    {
        // Classify violation into standard categories for point assignment
    }
    
    public function validatePointAssignment(ViolationData $violation, int $assignedPoints): ValidationResult
    {
        // Validate point assignment is within expected range for violation type
    }
}
```

#### ViolationNormalizationService
**Purpose**: Violation data normalization across different state formats  
**Location**: `app/Domain/Rating/Services/ViolationNormalizationService.php`

**Key Methods**:
```php
class ViolationNormalizationService
{
    public function normalizeViolationFromState(array $stateViolationData, string $state): NormalizedViolation
    {
        // Normalize violation data from state-specific formats
    }
    
    public function mapViolationCode(string $stateCode, string $state): string
    {
        // Map state-specific violation codes to standard classification
    }
    
    public function extractViolationSeverity(array $violationDetails): ViolationSeverity
    {
        // Extract severity indicators from violation details
    }
}
```

---

## 3. Database Schema Requirements

### Violation Classification Tables

#### violation_classification
```sql
CREATE TABLE violation_classification (
    id BIGINT PRIMARY KEY,
    classification_code VARCHAR(50) UNIQUE NOT NULL,
    classification_name VARCHAR(255) NOT NULL,
    classification_description TEXT,
    severity_level ENUM('MINOR', 'MODERATE', 'MAJOR', 'SERIOUS', 'SEVERE') NOT NULL,
    base_points INT NOT NULL,
    point_range_min INT NOT NULL,
    point_range_max INT NOT NULL,
    affects_eligibility BOOLEAN DEFAULT FALSE,
    requires_underwriting_review BOOLEAN DEFAULT FALSE,
    typical_violations TEXT, -- Examples of violations in this classification
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_classification_severity (severity_level, status_id),
    INDEX idx_classification_points (base_points, status_id),
    INDEX idx_eligibility_impact (affects_eligibility, status_id)
);

-- Aguila Dorada violation classifications
INSERT INTO violation_classification (classification_code, classification_name, severity_level, base_points, point_range_min, point_range_max, affects_eligibility) VALUES
('SPEEDING_MINOR', 'Minor Speeding (1-15 mph over)', 'MINOR', 1, 1, 2, FALSE),
('SPEEDING_MODERATE', 'Moderate Speeding (16-25 mph over)', 'MODERATE', 3, 3, 4, FALSE),
('SPEEDING_MAJOR', 'Major Speeding (26+ mph over)', 'MAJOR', 5, 5, 8, FALSE),
('TRAFFIC_SIGNAL', 'Traffic Signal/Sign Violations', 'MODERATE', 3, 3, 4, FALSE),
('FOLLOWING_TOO_CLOSE', 'Following Too Closely', 'MINOR', 2, 2, 3, FALSE),
('IMPROPER_LANE_CHANGE', 'Improper Lane Change/Use', 'MINOR', 1, 1, 2, FALSE),
('RECKLESS_DRIVING', 'Reckless/Careless Driving', 'MAJOR', 8, 6, 10, FALSE),
('DUI_DWI', 'DUI/DWI/OWI', 'SEVERE', 15, 12, 20, TRUE),
('LEAVING_SCENE', 'Leaving Scene of Accident', 'SERIOUS', 8, 8, 12, TRUE),
('DRIVING_SUSPENDED', 'Driving While Suspended/Revoked', 'SERIOUS', 10, 8, 15, TRUE),
('VEHICULAR_ASSAULT', 'Vehicular Assault/Homicide', 'SEVERE', 20, 15, 25, TRUE),
('RACING', 'Racing/Speed Contest', 'MAJOR', 8, 6, 10, FALSE);
```

#### violation_code_mapping
```sql
CREATE TABLE violation_code_mapping (
    id BIGINT PRIMARY KEY,
    state_id BIGINT NOT NULL,
    state_violation_code VARCHAR(100) NOT NULL,
    state_violation_description VARCHAR(500),
    classification_id BIGINT NOT NULL,
    point_modifier INT DEFAULT 0, -- Adjustment to base points for this specific code
    mapping_confidence ENUM('HIGH', 'MEDIUM', 'LOW') NOT NULL,
    requires_manual_review BOOLEAN DEFAULT FALSE,
    mapping_notes TEXT,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (state_id) REFERENCES state(id),
    FOREIGN KEY (classification_id) REFERENCES violation_classification(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_state_code_mapping (state_id, state_violation_code, effective_date),
    INDEX idx_state_code_lookup (state_id, state_violation_code),
    INDEX idx_classification_mapping (classification_id, status_id),
    INDEX idx_manual_review (requires_manual_review, status_id)
);
```

#### violation_point_modifier
```sql
CREATE TABLE violation_point_modifier (
    id BIGINT PRIMARY KEY,
    modifier_code VARCHAR(50) UNIQUE NOT NULL,
    modifier_name VARCHAR(255) NOT NULL,
    modifier_description TEXT,
    modifier_type ENUM('SPEED_OVER', 'ACCIDENT_INVOLVED', 'SCHOOL_ZONE', 'CONSTRUCTION_ZONE', 'REPEAT_OFFENSE', 'COMMERCIAL_VEHICLE') NOT NULL,
    point_adjustment INT NOT NULL, -- Can be positive or negative
    applies_to_classifications JSON, -- Array of classification codes this modifier applies to
    business_rules JSON, -- Conditions for when modifier applies
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_modifier_type (modifier_type, status_id),
    INDEX idx_point_adjustment (point_adjustment)
);

-- Sample point modifiers
INSERT INTO violation_point_modifier (modifier_code, modifier_name, modifier_type, point_adjustment, applies_to_classifications, business_rules) VALUES
('SPEED_EXCESSIVE', 'Excessive Speed Modifier', 'SPEED_OVER', 2, '["SPEEDING_MINOR", "SPEEDING_MODERATE"]', '{"speed_threshold": 30}'),
('ACCIDENT_INVOLVED', 'Accident Involvement', 'ACCIDENT_INVOLVED', 2, '["SPEEDING_MINOR", "SPEEDING_MODERATE", "TRAFFIC_SIGNAL", "FOLLOWING_TOO_CLOSE"]', '{"accident_at_fault": true}'),
('SCHOOL_ZONE', 'School Zone Violation', 'SCHOOL_ZONE', 1, '["SPEEDING_MINOR", "SPEEDING_MODERATE"]', '{"in_school_zone": true}'),
('REPEAT_OFFENSE', 'Repeat Offense Modifier', 'REPEAT_OFFENSE', 3, '["SPEEDING_MODERATE", "SPEEDING_MAJOR", "DUI_DWI"]', '{"lookback_months": 24, "same_classification": true}');
```

---

## 4. Business Logic Requirements

### Violation Point Assignment Logic

#### Aguila Dorada Point Assignment Matrix
```php
class ViolationPointsService
{
    // Detailed point assignments for Aguila Dorada program
    const VIOLATION_POINT_MATRIX = [
        // Minor Speeding Violations
        'SPEEDING_1_5' => 1,        // 1-5 mph over limit
        'SPEEDING_6_10' => 1,       // 6-10 mph over limit
        'SPEEDING_11_15' => 2,      // 11-15 mph over limit
        
        // Moderate Speeding Violations
        'SPEEDING_16_20' => 3,      // 16-20 mph over limit
        'SPEEDING_21_25' => 3,      // 21-25 mph over limit
        
        // Major Speeding Violations
        'SPEEDING_26_30' => 5,      // 26-30 mph over limit
        'SPEEDING_31_40' => 6,      // 31-40 mph over limit
        'SPEEDING_41_PLUS' => 8,    // 41+ mph over limit
        
        // Traffic Control Violations
        'RED_LIGHT' => 4,           // Running red light
        'STOP_SIGN' => 3,           // Stop sign violation
        'YIELD_FAILURE' => 3,       // Failure to yield
        'WRONG_WAY' => 6,           // Wrong way driving
        
        // Lane/Following Violations
        'FOLLOWING_TOO_CLOSE' => 2, // Following too closely
        'IMPROPER_LANE_CHANGE' => 1, // Improper lane change
        'LANE_VIOLATION' => 1,      // Lane use violation
        'PASSING_VIOLATION' => 2,   // Improper passing
        
        // Serious Moving Violations
        'RECKLESS_DRIVING' => 8,    // Reckless driving
        'CARELESS_DRIVING' => 6,    // Careless driving
        'AGGRESSIVE_DRIVING' => 8,  // Aggressive driving
        'RACING' => 8,              // Racing/speed contest
        
        // DUI/DWI and Related
        'DUI_FIRST' => 15,          // First DUI/DWI
        'DUI_SUBSEQUENT' => 20,     // Subsequent DUI/DWI
        'DUI_COMMERCIAL' => 18,     // DUI in commercial vehicle
        'REFUSING_TEST' => 12,      // Refusing chemical test
        
        // License/Legal Violations
        'DRIVING_SUSPENDED' => 10,  // Driving while suspended
        'DRIVING_REVOKED' => 12,    // Driving while revoked
        'NO_LICENSE' => 8,          // Driving without license
        'EXPIRED_LICENSE' => 2,     // Expired license
        
        // Accident-Related Violations
        'LEAVING_SCENE_INJURY' => 12, // Leaving scene - injury
        'LEAVING_SCENE_PROPERTY' => 8, // Leaving scene - property
        'FAILURE_TO_REPORT' => 3,   // Failure to report accident
        
        // Serious Criminal Violations
        'VEHICULAR_HOMICIDE' => 25, // Vehicular homicide
        'VEHICULAR_ASSAULT' => 20,  // Vehicular assault
        'FELONY_VEHICLE' => 25,     // Felony involving vehicle
        'FLEEING_POLICE' => 15,     // Fleeing/eluding police
        
        // Equipment/Administrative
        'EQUIPMENT_VIOLATION' => 0,  // Equipment violation (non-chargeable)
        'REGISTRATION_VIOLATION' => 0, // Registration violation (non-chargeable)
        'INSURANCE_VIOLATION' => 2,  // No insurance/proof
    ];
    
    public function assignPointsToViolation(ViolationData $violation): int
    {
        // 1. Get base points from classification
        $classification = $this->classifyViolationType(
            $violation->description, 
            $violation->code, 
            $violation->state
        );
        
        $basePoints = $classification->base_points;
        
        // 2. Apply modifiers based on circumstances
        $modifiers = $this->calculateModifiers($violation, $classification);
        $totalModifiers = array_sum($modifiers);
        
        // 3. Calculate final points
        $finalPoints = max(0, $basePoints + $totalModifiers);
        
        // 4. Apply business rule caps
        $finalPoints = min($finalPoints, $classification->point_range_max);
        
        return $finalPoints;
    }
    
    private function calculateModifiers(ViolationData $violation, ViolationClassification $classification): array
    {
        $modifiers = [];
        
        // Speed over limit modifier
        if ($violation->speed_over_limit && $violation->speed_over_limit >= 30) {
            $modifiers['excessive_speed'] = 2;
        }
        
        // Accident involvement modifier
        if ($violation->accident_involved && $violation->at_fault) {
            $modifiers['accident_involved'] = 2;
        }
        
        // School zone modifier
        if ($violation->in_school_zone) {
            $modifiers['school_zone'] = 1;
        }
        
        // Construction zone modifier
        if ($violation->in_construction_zone) {
            $modifiers['construction_zone'] = 1;
        }
        
        // Commercial vehicle modifier
        if ($violation->commercial_vehicle) {
            $modifiers['commercial_vehicle'] = 2;
        }
        
        return $modifiers;
    }
}
```

### Violation Classification Logic
```php
class ViolationClassificationService
{
    public function classifyViolationType(string $description, string $code, string $state): ViolationClassification
    {
        // 1. Try direct code mapping first
        $mapping = DB::table('violation_code_mapping')
            ->join('violation_classification', 'violation_code_mapping.classification_id', '=', 'violation_classification.id')
            ->join('state', 'violation_code_mapping.state_id', '=', 'state.id')
            ->where('state.code', $state)
            ->where('violation_code_mapping.state_violation_code', $code)
            ->where('violation_code_mapping.effective_date', '<=', now())
            ->where(function($query) {
                $query->whereNull('violation_code_mapping.expiration_date')
                      ->orWhere('violation_code_mapping.expiration_date', '>', now());
            })
            ->where('violation_code_mapping.status_id', Status::ACTIVE)
            ->first();
            
        if ($mapping) {
            return new ViolationClassification($mapping);
        }
        
        // 2. Fall back to description-based classification
        return $this->classifyByDescription($description);
    }
    
    private function classifyByDescription(string $description): ViolationClassification
    {
        $description = strtolower($description);
        
        // Speed-related violations
        if (str_contains($description, 'speed')) {
            if (preg_match('/(\d+)\s*mph?\s*over/', $description, $matches)) {
                $speedOver = (int)$matches[1];
                
                if ($speedOver <= 15) {
                    return $this->getClassification('SPEEDING_MINOR');
                } elseif ($speedOver <= 25) {
                    return $this->getClassification('SPEEDING_MODERATE');
                } else {
                    return $this->getClassification('SPEEDING_MAJOR');
                }
            }
            
            return $this->getClassification('SPEEDING_MODERATE'); // Default for speed violations
        }
        
        // DUI/DWI violations
        if (str_contains($description, 'dui') || str_contains($description, 'dwi') || 
            str_contains($description, 'drunk') || str_contains($description, 'intoxicat')) {
            return $this->getClassification('DUI_DWI');
        }
        
        // Traffic signal violations
        if (str_contains($description, 'red light') || str_contains($description, 'traffic signal')) {
            return $this->getClassification('TRAFFIC_SIGNAL');
        }
        
        // Reckless driving
        if (str_contains($description, 'reckless') || str_contains($description, 'careless')) {
            return $this->getClassification('RECKLESS_DRIVING');
        }
        
        // Default classification for unrecognized violations
        return $this->getClassification('TRAFFIC_SIGNAL'); // Moderate default
    }
}
```

---

## 5. State-Specific Integration

### Texas Violation Code Mapping
```sql
-- Texas specific violation code mappings
INSERT INTO violation_code_mapping (state_id, state_violation_code, state_violation_description, classification_id, point_modifier, mapping_confidence) VALUES
-- Texas speeding violations
((SELECT id FROM state WHERE code = 'TX'), 'SPEED001', 'Speed 1-10 MPH over limit', (SELECT id FROM violation_classification WHERE classification_code = 'SPEEDING_MINOR'), 0, 'HIGH'),
((SELECT id FROM state WHERE code = 'TX'), 'SPEED002', 'Speed 11-15 MPH over limit', (SELECT id FROM violation_classification WHERE classification_code = 'SPEEDING_MINOR'), 1, 'HIGH'),
((SELECT id FROM state WHERE code = 'TX'), 'SPEED003', 'Speed 16-25 MPH over limit', (SELECT id FROM violation_classification WHERE classification_code = 'SPEEDING_MODERATE'), 0, 'HIGH'),
((SELECT id FROM state WHERE code = 'TX'), 'SPEED004', 'Speed 26+ MPH over limit', (SELECT id FROM violation_classification WHERE classification_code = 'SPEEDING_MAJOR'), 0, 'HIGH'),

-- Texas traffic control violations
((SELECT id FROM state WHERE code = 'TX'), 'TC001', 'Ran Red Light', (SELECT id FROM violation_classification WHERE classification_code = 'TRAFFIC_SIGNAL'), 0, 'HIGH'),
((SELECT id FROM state WHERE code = 'TX'), 'TC002', 'Stop Sign Violation', (SELECT id FROM violation_classification WHERE classification_code = 'TRAFFIC_SIGNAL'), -1, 'HIGH'),
((SELECT id FROM state WHERE code = 'TX'), 'TC003', 'Failure to Yield', (SELECT id FROM violation_classification WHERE classification_code = 'TRAFFIC_SIGNAL'), -1, 'HIGH'),

-- Texas DUI violations
((SELECT id FROM state WHERE code = 'TX'), 'DWI001', 'Driving While Intoxicated', (SELECT id FROM violation_classification WHERE classification_code = 'DUI_DWI'), 0, 'HIGH'),
((SELECT id FROM state WHERE code = 'TX'), 'DUI001', 'Driving Under Influence', (SELECT id FROM violation_classification WHERE classification_code = 'DUI_DWI'), 0, 'HIGH'),

-- Texas license violations
((SELECT id FROM state WHERE code = 'TX'), 'LIC001', 'Driving While License Suspended', (SELECT id FROM violation_classification WHERE classification_code = 'DRIVING_SUSPENDED'), 0, 'HIGH'),
((SELECT id FROM state WHERE code = 'TX'), 'LIC002', 'Driving While License Revoked', (SELECT id FROM violation_classification WHERE classification_code = 'DRIVING_SUSPENDED'), 2, 'HIGH');
```

---

## 6. API Integration Requirements

### Violation Points Endpoints
```php
// Violation classification and points API endpoints
GET /api/v1/rating/violations/classifications
// Returns all violation classifications and point ranges

POST /api/v1/rating/violations/classify
{
    "violation_description": "Speed 18 mph over limit",
    "violation_code": "SPEED003", 
    "state": "TX",
    "circumstances": {
        "speed_over_limit": 18,
        "accident_involved": false,
        "in_school_zone": false
    }
}
// Classify violation and return point assignment

GET /api/v1/rating/violations/state-codes/{state}
// Returns state-specific violation code mappings

POST /api/v1/admin/violations/map-code
{
    "state_violation_code": "NEW001",
    "classification_code": "SPEEDING_MINOR",
    "mapping_confidence": "MEDIUM"
}
// Administrative endpoint to map new violation codes
```

### Response Format
```json
{
    "violation_classification": {
        "classification_code": "SPEEDING_MODERATE",
        "classification_name": "Moderate Speeding (16-25 mph over)",
        "severity_level": "MODERATE",
        "base_points": 3
    },
    "point_assignment": {
        "base_points": 3,
        "modifiers": [
            {
                "modifier_type": "SPEED_OVER",
                "modifier_name": "Excessive Speed Modifier", 
                "point_adjustment": 0,
                "reason": "Speed 18 mph - below 30 mph threshold"
            }
        ],
        "total_points": 3,
        "final_points": 3
    },
    "mapping_details": {
        "state_code": "TX",
        "state_violation_code": "SPEED003",
        "mapping_confidence": "HIGH",
        "requires_manual_review": false
    }
}
```

---

## 7. Validation Requirements

### Point Assignment Validation
```php
class ViolationPointValidator
{
    public function validatePointAssignment(ViolationData $violation, int $assignedPoints): ValidationResult
    {
        $result = new ValidationResult();
        
        // 1. Validate points are within classification range
        $classification = $this->classificationService->classifyViolationType(
            $violation->description, 
            $violation->code, 
            $violation->state
        );
        
        if ($assignedPoints < $classification->point_range_min) {
            $result->addError("Assigned points {$assignedPoints} below minimum {$classification->point_range_min} for classification");
        }
        
        if ($assignedPoints > $classification->point_range_max) {
            $result->addError("Assigned points {$assignedPoints} exceeds maximum {$classification->point_range_max} for classification");
        }
        
        // 2. Validate severity consistency
        if ($assignedPoints >= 15 && $classification->severity_level !== 'SEVERE') {
            $result->addWarning("High point assignment ({$assignedPoints}) for non-severe classification");
        }
        
        // 3. Validate zero points for non-chargeable violations
        if ($assignedPoints > 0 && !$classification->is_chargeable) {
            $result->addError("Non-chargeable violation cannot have points assigned");
        }
        
        return $result;
    }
}
```

---

## 8. Performance Requirements

### Classification Lookup Performance
```php
class ViolationClassificationService
{
    public function classifyViolationType(string $description, string $code, string $state): ViolationClassification
    {
        // Cache classification results for performance
        $cacheKey = "violation_classification_{$state}_{$code}";
        
        return Cache::remember($cacheKey, 3600, function() use ($description, $code, $state) {
            return $this->performClassificationLookup($description, $code, $state);
        });
    }
}
```

### Database Performance
```sql
-- Violation code mapping lookup optimization
CREATE INDEX idx_violation_code_lookup_optimized 
ON violation_code_mapping (
    state_id, 
    state_violation_code, 
    effective_date,
    classification_id
) WHERE status_id = 1;

-- Classification lookup optimization
CREATE INDEX idx_classification_lookup 
ON violation_classification (
    classification_code, 
    severity_level, 
    base_points
) WHERE status_id = 1;
```

---

## 9. Testing Requirements

### Violation Classification Testing
```php
class ViolationPointsServiceTest extends TestCase
{
    public function test_speeding_violation_classification()
    {
        $violation = new ViolationData([
            'description' => 'Speed 18 mph over limit',
            'code' => 'SPEED003',
            'state' => 'TX',
            'speed_over_limit' => 18
        ]);
        
        $points = $this->violationPointsService->assignPointsToViolation($violation);
        
        $this->assertEquals(3, $points);
    }
    
    public function test_dui_violation_high_points()
    {
        $violation = new ViolationData([
            'description' => 'Driving While Intoxicated',
            'code' => 'DWI001',
            'state' => 'TX'
        ]);
        
        $points = $this->violationPointsService->assignPointsToViolation($violation);
        
        $this->assertEquals(15, $points);
    }
    
    public function test_modifier_application()
    {
        $violation = new ViolationData([
            'description' => 'Speed 35 mph over limit',
            'code' => 'SPEED004',
            'state' => 'TX',
            'speed_over_limit' => 35,
            'accident_involved' => true,
            'at_fault' => true
        ]);
        
        $points = $this->violationPointsService->assignPointsToViolation($violation);
        
        // Base 5 + Excessive Speed 2 + Accident 2 = 9 points
        $this->assertEquals(9, $points);
    }
}
```

---

## Implementation Priority: MEDIUM
This factor provides detailed violation classification supporting the Driver Points core component. Should be implemented after core Driver Points factor.

## Dependencies
- **Driver Points Factor**: Core point calculation engine
- **MVR Integration**: Violation data source

## Estimated Implementation Effort
- **Database Schema**: 3 days
- **Service Layer**: 4 days
- **State Code Mapping**: 3 days
- **API Integration**: 2 days
- **Testing**: 3 days
- **Total**: 15 days

This plan implements comprehensive violation classification and point assignment while supporting the detailed risk assessment requirements of the Driver Points core rating component.