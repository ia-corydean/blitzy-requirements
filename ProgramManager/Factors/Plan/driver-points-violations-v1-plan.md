# Driver Points Violations V1 Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Driver Points Violations V1  
**Category**: Driver Factor  
**Priority**: Low - Legacy violation scoring system  
**Implementation Complexity**: Low  

### Business Requirements Summary
The Driver Points Violations V1 factor represents a legacy violation scoring methodology that may be maintained for historical policy continuity or transition purposes. This factor provides an alternative violation point assignment system that can run in parallel with the current Driver Points Violations system during system migration or for comparative analysis purposes.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing Global Requirements:

#### Leverages GR-73: Motor Vehicle Record Integration
**Integration**: Legacy violation processing alongside current system  
**Dependencies**: Violation data normalization and historical point assignment methods

#### Leverages GR-74: Violation Point Management
**Integration**: Alternative point calculation methodology  
**Dependencies**: Legacy point assignment rules and version management

#### New Requirement: GR-78: Legacy Rating System Management
**Priority**: Low  
**Rationale**: Standards for maintaining and transitioning legacy rating components  

**Core Components**:
- Legacy system version control and maintenance standards
- Historical rating methodology preservation requirements
- Legacy-to-current system migration patterns
- Parallel rating system operation and comparison standards
- Legacy system deprecation and sunset planning

### Integration with Existing Global Requirements
- **GR-65**: Rating Engine Architecture - Legacy system integration with current rating engine
- **GR-41**: Table Schema Requirements - Legacy data preservation and migration patterns
- **GR-20**: Application Business Logic - Legacy service integration patterns

---

## 2. Service Architecture Requirements

### Legacy Violation Processing Services

#### LegacyViolationPointsService
**Purpose**: V1 violation point calculation and legacy methodology  
**Location**: `app/Domain/Rating/Services/Legacy/LegacyViolationPointsService.php`

**Key Methods**:
```php
class LegacyViolationPointsService
{
    public function calculateV1Points(ViolationData $violation): int
    {
        // 1. Apply V1 classification methodology
        // 2. Use legacy point assignment rules
        // 3. Return V1 point assignment for comparison
    }
    
    public function compareV1ToCurrentPoints(int $driverId): PointComparison
    {
        // Compare V1 and current point calculations for analysis
    }
    
    public function getV1FactorFromPoints(int $totalPoints): float
    {
        // Apply V1 factor scale for legacy calculations
    }
}
```

#### LegacyMigrationService
**Purpose**: Migration support and legacy data management  
**Location**: `app/Domain/Rating/Services/Legacy/LegacyMigrationService.php`

**Key Methods**:
```php
class LegacyMigrationService
{
    public function migrateV1ToCurrentPoints(int $driverId): MigrationResult
    {
        // Migrate driver from V1 to current point system
    }
    
    public function validateMigrationConsistency(int $driverId): ValidationResult
    {
        // Validate consistency between V1 and current calculations
    }
    
    public function generateMigrationReport(array $driverIds): MigrationReport
    {
        // Generate comprehensive migration impact report
    }
}
```

---

## 3. Database Schema Requirements

### Legacy Violation Point Tables

#### legacy_violation_point_scale
```sql
CREATE TABLE legacy_violation_point_scale (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    legacy_version VARCHAR(50) NOT NULL DEFAULT 'V1',
    violation_category VARCHAR(100) NOT NULL,
    violation_subcategory VARCHAR(100),
    legacy_points INT NOT NULL,
    legacy_factor DECIMAL(6,4),
    effective_date DATE NOT NULL,
    expiration_date DATE,
    migration_notes TEXT,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_legacy_scale (program_id, legacy_version, violation_category, violation_subcategory, effective_date),
    INDEX idx_legacy_version (legacy_version, program_id),
    INDEX idx_violation_category (violation_category, violation_subcategory),
    INDEX idx_legacy_effective_dates (effective_date, expiration_date)
);

-- V1 Legacy Point Scale for Aguila Dorada
INSERT INTO legacy_violation_point_scale (program_id, legacy_version, violation_category, violation_subcategory, legacy_points, legacy_factor, effective_date) VALUES
-- V1 Speeding Categories (simpler structure)
(1, 'V1', 'SPEEDING', 'MINOR', 1, 1.10, '2020-01-01'),
(1, 'V1', 'SPEEDING', 'MODERATE', 2, 1.20, '2020-01-01'),
(1, 'V1', 'SPEEDING', 'MAJOR', 4, 1.40, '2020-01-01'),

-- V1 Other Violations (broader categories)
(1, 'V1', 'MOVING_VIOLATION', 'STANDARD', 2, 1.20, '2020-01-01'),
(1, 'V1', 'MOVING_VIOLATION', 'SERIOUS', 5, 1.50, '2020-01-01'),
(1, 'V1', 'DUI', 'STANDARD', 10, 3.00, '2020-01-01'),
(1, 'V1', 'LICENSE_VIOLATION', 'STANDARD', 6, 2.00, '2020-01-01'),
(1, 'V1', 'MAJOR_VIOLATION', 'STANDARD', 8, 2.50, '2020-01-01');
```

#### legacy_driver_violation_points
```sql
CREATE TABLE legacy_driver_violation_points (
    id BIGINT PRIMARY KEY,
    driver_id BIGINT NOT NULL,
    violation_id BIGINT NOT NULL,
    legacy_version VARCHAR(50) NOT NULL DEFAULT 'V1',
    legacy_category VARCHAR(100) NOT NULL,
    legacy_subcategory VARCHAR(100),
    legacy_points INT NOT NULL,
    legacy_calculation_date DATE NOT NULL,
    current_points INT, -- For comparison
    point_difference INT, -- Legacy - Current
    migration_status ENUM('PENDING', 'MIGRATED', 'EXCEPTION') DEFAULT 'PENDING',
    migration_notes TEXT,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (driver_id) REFERENCES driver(id),
    FOREIGN KEY (violation_id) REFERENCES driver_violation(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_legacy_violation_points (driver_id, violation_id, legacy_version),
    INDEX idx_driver_legacy_points (driver_id, legacy_version, legacy_calculation_date),
    INDEX idx_migration_status (migration_status, status_id),
    INDEX idx_point_comparison (legacy_points, current_points, point_difference)
);
```

#### legacy_factor_comparison
```sql
CREATE TABLE legacy_factor_comparison (
    id BIGINT PRIMARY KEY,
    driver_id BIGINT NOT NULL,
    comparison_date DATE NOT NULL,
    legacy_total_points INT NOT NULL,
    current_total_points INT NOT NULL,
    legacy_factor DECIMAL(6,4) NOT NULL,
    current_factor DECIMAL(6,4) NOT NULL,
    factor_difference DECIMAL(6,4) NOT NULL, -- Legacy - Current
    percentage_difference DECIMAL(5,2), -- Percentage impact
    recommendation ENUM('KEEP_LEGACY', 'MIGRATE_CURRENT', 'MANUAL_REVIEW') NOT NULL,
    comparison_notes TEXT,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (driver_id) REFERENCES driver(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_driver_comparison (driver_id, comparison_date),
    INDEX idx_comparison_date (comparison_date),
    INDEX idx_factor_difference (factor_difference, percentage_difference),
    INDEX idx_migration_recommendation (recommendation, status_id)
);
```

---

## 4. Legacy Business Logic Requirements

### V1 Point Assignment Methodology
```php
class LegacyViolationPointsService
{
    // V1 Legacy Point Assignment (simplified categories)
    const V1_POINT_MATRIX = [
        // Simplified Speeding Categories
        'SPEEDING_MINOR' => 1,      // Any speeding 1-15 mph
        'SPEEDING_MODERATE' => 2,   // Any speeding 16-30 mph  
        'SPEEDING_MAJOR' => 4,      // Any speeding 31+ mph
        
        // Broad Moving Violations
        'MOVING_STANDARD' => 2,     // Standard moving violations
        'MOVING_SERIOUS' => 5,      // Serious moving violations
        
        // Major Categories
        'DUI_STANDARD' => 10,       // All DUI/DWI violations
        'LICENSE_VIOLATION' => 6,   // License-related violations
        'MAJOR_VIOLATION' => 8,     // Other major violations
    ];
    
    // V1 Factor Scale (simpler progression)
    const V1_FACTOR_SCALE = [
        0 => 1.00,  // Clean record
        1 => 1.10,  // 1 point
        2 => 1.20,  // 2 points
        3 => 1.30,  // 3 points
        4 => 1.40,  // 4 points
        5 => 1.50,  // 5 points
        6 => 2.00,  // 6 points
        8 => 2.50,  // 8 points
        10 => 3.00, // 10+ points (maximum)
    ];
    
    public function calculateV1Points(ViolationData $violation): int
    {
        // Simplified V1 classification
        $category = $this->classifyForV1($violation);
        
        return self::V1_POINT_MATRIX[$category] ?? 2; // Default to 2 points
    }
    
    private function classifyForV1(ViolationData $violation): string
    {
        $description = strtolower($violation->description);
        
        // V1 Speeding Classification (broader categories)
        if (str_contains($description, 'speed')) {
            if ($violation->speed_over_limit <= 15) {
                return 'SPEEDING_MINOR';
            } elseif ($violation->speed_over_limit <= 30) {
                return 'SPEEDING_MODERATE';
            } else {
                return 'SPEEDING_MAJOR';
            }
        }
        
        // V1 DUI Classification
        if (str_contains($description, 'dui') || str_contains($description, 'dwi')) {
            return 'DUI_STANDARD';
        }
        
        // V1 License Violations
        if (str_contains($description, 'suspend') || str_contains($description, 'license')) {
            return 'LICENSE_VIOLATION';
        }
        
        // V1 Major Violations
        if (str_contains($description, 'reckless') || str_contains($description, 'leaving scene')) {
            return 'MAJOR_VIOLATION';
        }
        
        // Default to standard moving violation
        return 'MOVING_STANDARD';
    }
    
    public function getV1FactorFromPoints(int $totalPoints): float
    {
        // Find appropriate V1 factor
        $applicableFactor = 1.00;
        
        foreach (self::V1_FACTOR_SCALE as $points => $factor) {
            if ($totalPoints >= $points) {
                $applicableFactor = $factor;
            }
        }
        
        return $applicableFactor;
    }
}
```

### Migration Comparison Logic
```php
class LegacyMigrationService
{
    public function compareV1ToCurrentPoints(int $driverId): PointComparison
    {
        // Get V1 calculations
        $v1Calculation = $this->legacyService->calculateV1DriverPoints($driverId);
        
        // Get current calculations
        $currentCalculation = $this->currentService->calculateDriverPointsFactor($driverId);
        
        // Calculate differences
        $pointDifference = $v1Calculation->total_points - $currentCalculation->total_points;
        $factorDifference = $v1Calculation->factor_value - $currentCalculation->factor_value;
        $percentageImpact = (($factorDifference / $currentCalculation->factor_value) * 100);
        
        // Determine recommendation
        $recommendation = $this->determineRecommendation($pointDifference, $factorDifference, $percentageImpact);
        
        return new PointComparison([
            'driver_id' => $driverId,
            'v1_points' => $v1Calculation->total_points,
            'current_points' => $currentCalculation->total_points,
            'point_difference' => $pointDifference,
            'v1_factor' => $v1Calculation->factor_value,
            'current_factor' => $currentCalculation->factor_value,
            'factor_difference' => $factorDifference,
            'percentage_impact' => $percentageImpact,
            'recommendation' => $recommendation
        ]);
    }
    
    private function determineRecommendation(int $pointDiff, float $factorDiff, float $percentageImpact): string
    {
        // Recommend keeping legacy if significantly more favorable to customer
        if ($factorDiff < -0.15 && $percentageImpact < -10) {
            return 'KEEP_LEGACY';
        }
        
        // Recommend migration if difference is minimal
        if (abs($percentageImpact) <= 5) {
            return 'MIGRATE_CURRENT';
        }
        
        // Recommend manual review for significant differences
        if (abs($percentageImpact) > 15) {
            return 'MANUAL_REVIEW';
        }
        
        // Default to migration for moderate differences
        return 'MIGRATE_CURRENT';
    }
}
```

---

## 5. API Integration Requirements

### Legacy Comparison Endpoints
```php
// Legacy violation points API endpoints
GET /api/v1/rating/legacy/driver-points/{driverId}/compare
// Compare V1 and current point calculations

POST /api/v1/rating/legacy/migration/analyze
{
    "driver_ids": [123, 456, 789],
    "analysis_type": "IMPACT_ASSESSMENT"
}
// Analyze migration impact for multiple drivers

GET /api/v1/admin/legacy/migration-report/{programId}
// Administrative migration status report

POST /api/v1/admin/legacy/migrate-driver
{
    "driver_id": 123,
    "migration_type": "FORCE_CURRENT",
    "override_reason": "Customer request"
}
// Administrative driver migration
```

### Response Format
```json
{
    "driver_id": 12345,
    "comparison_date": "2025-07-15",
    "point_comparison": {
        "v1_points": 4,
        "current_points": 7,
        "point_difference": -3
    },
    "factor_comparison": {
        "v1_factor": 1.40,
        "current_factor": 2.10,
        "factor_difference": -0.70,
        "percentage_impact": -33.3
    },
    "recommendation": {
        "action": "KEEP_LEGACY",
        "reason": "Current system significantly less favorable to customer",
        "requires_approval": true
    },
    "migration_status": "PENDING",
    "legacy_violations": [
        {
            "violation_id": 67890,
            "v1_category": "SPEEDING_MODERATE",
            "v1_points": 2,
            "current_points": 3,
            "difference": -1
        }
    ]
}
```

---

## 6. Testing Requirements

### Legacy Comparison Testing
```php
class LegacyViolationPointsTest extends TestCase
{
    public function test_v1_classification_accuracy()
    {
        $violation = new ViolationData([
            'description' => 'Speed 18 mph over limit',
            'speed_over_limit' => 18
        ]);
        
        $v1Points = $this->legacyService->calculateV1Points($violation);
        $currentPoints = $this->currentService->assignPointsToViolation($violation);
        
        $this->assertEquals(2, $v1Points); // V1 moderate speeding
        $this->assertEquals(3, $currentPoints); // Current system
    }
    
    public function test_migration_recommendation_logic()
    {
        $comparison = $this->migrationService->compareV1ToCurrentPoints($this->driverId);
        
        // Test recommendation logic based on difference thresholds
        if ($comparison->percentage_impact < -10) {
            $this->assertEquals('KEEP_LEGACY', $comparison->recommendation);
        }
    }
    
    public function test_factor_scale_differences()
    {
        // Test V1 vs current factor scale differences
        $v1Factor = $this->legacyService->getV1FactorFromPoints(4);
        $currentFactor = $this->currentService->determineFactorFromPoints(4);
        
        $this->assertEquals(1.40, $v1Factor); // V1 scale
        $this->assertEquals(1.50, $currentFactor); // Current scale
    }
}
```

---

## 7. Migration Strategy

### Phased Migration Approach
```php
class LegacyMigrationStrategy
{
    public function executeMigrationPhase(string $phase): MigrationResult
    {
        switch ($phase) {
            case 'ANALYSIS':
                return $this->performMigrationAnalysis();
            
            case 'PILOT':
                return $this->executePilotMigration();
            
            case 'GRADUAL':
                return $this->executeGradualMigration();
            
            case 'COMPLETION':
                return $this->completeMigration();
        }
    }
    
    private function performMigrationAnalysis(): MigrationResult
    {
        // Analyze all drivers for migration impact
        $drivers = DB::table('driver')->where('status_id', Status::ACTIVE)->pluck('id');
        
        $migrationImpacts = [];
        foreach ($drivers as $driverId) {
            $comparison = $this->migrationService->compareV1ToCurrentPoints($driverId);
            $migrationImpacts[] = $comparison;
        }
        
        return new MigrationResult([
            'phase' => 'ANALYSIS',
            'total_drivers' => $drivers->count(),
            'favorable_to_legacy' => collect($migrationImpacts)->where('recommendation', 'KEEP_LEGACY')->count(),
            'ready_for_migration' => collect($migrationImpacts)->where('recommendation', 'MIGRATE_CURRENT')->count(),
            'requires_review' => collect($migrationImpacts)->where('recommendation', 'MANUAL_REVIEW')->count()
        ]);
    }
}
```

---

## Implementation Priority: LOW
This factor supports legacy system migration and comparison. Should be implemented only if legacy system transition is required.

## Dependencies
- **Driver Points Factor**: Current system for comparison
- **Driver Points Violations Factor**: Current violation classification

## Estimated Implementation Effort
- **Database Schema**: 2 days
- **Service Layer**: 3 days
- **Migration Logic**: 3 days
- **API Integration**: 1 day
- **Testing**: 2 days
- **Total**: 11 days

This plan provides comprehensive legacy system support while enabling smooth migration to the current violation point methodology when business requirements dictate the transition.