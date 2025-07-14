# Driver Assignment Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Driver Assignment  
**Category**: Core Rating Component  
**Priority**: High - Driver-to-vehicle assignment and rating methodology  
**Implementation Complexity**: Medium  

### Business Requirements Summary
The Driver Assignment factor establishes the methodology for assigning drivers to vehicles and applying rating factors at the appropriate level. This factor ensures that each driver's individual risk characteristics are properly applied to their assigned vehicles while maintaining proper primary driver designation and rating accuracy across multiple driver and vehicle combinations.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing and new Global Requirements:

#### Leverages GR-65: Rating Engine Architecture
**Integration**: Driver assignment logic within multiplicative rating engine  
**Dependencies**: RatingEngineService for driver-vehicle factor application coordination

#### New Requirement: GR-76: Driver-Vehicle Assignment Standards
**Priority**: High  
**Rationale**: Driver assignment methodology and rating application standards  

**Core Components**:
- Primary driver designation rules and validation
- Multiple driver assignment methodology
- Rating factor application hierarchy (driver vs vehicle vs policy level)
- Assignment change tracking and effective date management
- Business rules for driver eligibility and assignment restrictions

#### Leverages GR-20: Application Business Logic
**Integration**: Assignment validation and business rule patterns  
**Dependencies**: Driver assignment service patterns and validation logic

### Integration with Existing Global Requirements
- **GR-41**: Table Schema Requirements - Driver assignment and mapping table structures
- **GR-19**: Table Relationships - Driver-vehicle association patterns
- **GR-18**: Workflow Requirements - Assignment change workflow integration

---

## 2. Service Architecture Requirements

### Driver Assignment Services

#### DriverAssignmentService
**Purpose**: Driver-to-vehicle assignment management and validation  
**Location**: `app/Domain/Rating/Services/DriverAssignmentService.php`

**Key Methods**:
```php
class DriverAssignmentService
{
    public function assignDriverToVehicle(int $driverId, int $vehicleId, bool $isPrimary = false): AssignmentResult
    {
        // 1. Validate driver eligibility for assignment
        // 2. Check vehicle assignment capacity
        // 3. Handle primary driver designation
        // 4. Create or update assignment record
        // 5. Return assignment result with validation status
    }
    
    public function validateDriverAssignments(int $policyId): ValidationResult
    {
        // Validate all driver assignments for policy completeness and business rules
    }
    
    public function getPrimaryDriver(int $vehicleId): ?Driver
    {
        // Retrieve primary driver for vehicle
    }
    
    public function getAssignmentBreakdown(int $policyId): AssignmentBreakdown
    {
        // Provide detailed breakdown of all driver-vehicle assignments
    }
}
```

#### AssignmentValidationService
**Purpose**: Driver assignment validation and business rule enforcement  
**Location**: `app/Domain/Rating/Services/AssignmentValidationService.php`

**Key Methods**:
```php
class AssignmentValidationService
{
    public function validatePrimaryDriverRequirement(int $vehicleId): ValidationResult
    {
        // Ensure each vehicle has exactly one primary driver
    }
    
    public function validateDriverEligibility(int $driverId, int $vehicleId): ValidationResult
    {
        // Validate driver eligibility for vehicle assignment
    }
    
    public function validateAssignmentCapacity(int $policyId): ValidationResult
    {
        // Validate assignment capacity and coverage for all drivers/vehicles
    }
}
```

---

## 3. Database Schema Requirements

### Driver Assignment Management Tables

#### driver_vehicle_assignment
```sql
CREATE TABLE driver_vehicle_assignment (
    id BIGINT PRIMARY KEY,
    policy_id BIGINT,
    quote_id BIGINT,
    driver_id BIGINT NOT NULL,
    vehicle_id BIGINT NOT NULL,
    is_primary_driver BOOLEAN DEFAULT FALSE,
    assignment_type ENUM('PRIMARY', 'SECONDARY', 'OCCASIONAL', 'EXCLUDED') NOT NULL,
    assignment_percentage DECIMAL(5,2), -- For usage-based assignments
    effective_date DATE NOT NULL,
    expiration_date DATE,
    assignment_reason VARCHAR(255),
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (quote_id) REFERENCES quote(id),
    FOREIGN KEY (driver_id) REFERENCES driver(id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_driver_vehicle_assignment (policy_id, driver_id, vehicle_id, effective_date),
    INDEX idx_policy_assignments (policy_id, effective_date),
    INDEX idx_driver_assignments (driver_id, effective_date),
    INDEX idx_vehicle_assignments (vehicle_id, is_primary_driver),
    INDEX idx_primary_drivers (vehicle_id, is_primary_driver, effective_date),
    
    -- Business rule constraint: Only one primary driver per vehicle at a time
    CONSTRAINT chk_primary_driver_unique 
        UNIQUE (vehicle_id, is_primary_driver, effective_date) 
        WHERE is_primary_driver = TRUE
);
```

#### assignment_validation_rule
```sql
CREATE TABLE assignment_validation_rule (
    id BIGINT PRIMARY KEY,
    rule_code VARCHAR(50) UNIQUE NOT NULL,
    rule_name VARCHAR(255) NOT NULL,
    rule_description TEXT,
    rule_type ENUM('DRIVER_ELIGIBILITY', 'VEHICLE_CAPACITY', 'PRIMARY_DRIVER', 'COVERAGE_REQUIREMENT') NOT NULL,
    validation_logic JSON NOT NULL,
    error_message VARCHAR(500),
    warning_message VARCHAR(500),
    is_blocking BOOLEAN DEFAULT TRUE,
    applies_to_program_ids JSON, -- Array of program IDs
    effective_date DATE NOT NULL,
    expiration_date DATE,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_rule_type (rule_type, status_id),
    INDEX idx_program_rules (applies_to_program_ids, effective_date),
    INDEX idx_blocking_rules (is_blocking, status_id)
);
```

#### assignment_rating_application
```sql
CREATE TABLE assignment_rating_application (
    id BIGINT PRIMARY KEY,
    assignment_id BIGINT NOT NULL,
    rating_factor_type VARCHAR(100) NOT NULL,
    application_method ENUM('DRIVER_LEVEL', 'VEHICLE_LEVEL', 'ASSIGNMENT_LEVEL') NOT NULL,
    factor_weight DECIMAL(5,4) DEFAULT 1.0000,
    application_notes TEXT,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (assignment_id) REFERENCES driver_vehicle_assignment(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_assignment_rating (assignment_id, rating_factor_type),
    INDEX idx_application_method (application_method, status_id),
    INDEX idx_rating_effective_dates (effective_date, expiration_date)
);
```

---

## 4. Business Logic Requirements

### Primary Driver Assignment Rules
```php
class DriverAssignmentService
{
    public function assignPrimaryDriver(int $driverId, int $vehicleId): AssignmentResult
    {
        // 1. Validate driver eligibility
        $eligibilityResult = $this->validateDriverEligibility($driverId, $vehicleId);
        if (!$eligibilityResult->isValid()) {
            return AssignmentResult::failure($eligibilityResult->getErrors());
        }
        
        // 2. Check for existing primary driver
        $existingPrimary = $this->getPrimaryDriver($vehicleId);
        if ($existingPrimary && $existingPrimary->id !== $driverId) {
            // Remove existing primary designation
            $this->updateAssignment($existingPrimary->id, $vehicleId, ['is_primary_driver' => false]);
        }
        
        // 3. Create or update assignment
        $assignment = DB::table('driver_vehicle_assignment')->updateOrInsert(
            [
                'driver_id' => $driverId,
                'vehicle_id' => $vehicleId,
                'effective_date' => now()->format('Y-m-d')
            ],
            [
                'is_primary_driver' => true,
                'assignment_type' => 'PRIMARY',
                'status_id' => Status::ACTIVE,
                'updated_by' => auth()->id()
            ]
        );
        
        return AssignmentResult::success($assignment);
    }
}
```

### Assignment Validation Rules
```php
class AssignmentValidationService
{
    public function validateDriverAssignments(int $policyId): ValidationResult
    {
        $result = new ValidationResult();
        
        // 1. Validate each vehicle has a primary driver
        $vehiclesWithoutPrimary = DB::table('vehicle')
            ->leftJoin('driver_vehicle_assignment', function($join) {
                $join->on('vehicle.id', '=', 'driver_vehicle_assignment.vehicle_id')
                     ->where('driver_vehicle_assignment.is_primary_driver', true)
                     ->where('driver_vehicle_assignment.status_id', Status::ACTIVE);
            })
            ->where('vehicle.policy_id', $policyId)
            ->whereNull('driver_vehicle_assignment.id')
            ->pluck('vehicle.id');
            
        if ($vehiclesWithoutPrimary->isNotEmpty()) {
            $result->addError("Vehicles without primary driver: " . $vehiclesWithoutPrimary->implode(', '));
        }
        
        // 2. Validate no driver is assigned to more than reasonable number of vehicles
        $driversWithTooManyAssignments = DB::table('driver_vehicle_assignment')
            ->select('driver_id', DB::raw('COUNT(*) as assignment_count'))
            ->where('policy_id', $policyId)
            ->where('status_id', Status::ACTIVE)
            ->groupBy('driver_id')
            ->having('assignment_count', '>', 5) // Business rule: max 5 vehicles per driver
            ->pluck('driver_id');
            
        if ($driversWithTooManyAssignments->isNotEmpty()) {
            $result->addWarning("Drivers with excessive vehicle assignments: " . $driversWithTooManyAssignments->implode(', '));
        }
        
        // 3. Validate named insured is assigned to at least one vehicle
        $namedInsured = DB::table('driver')
            ->where('policy_id', $policyId)
            ->where('is_named_insured', true)
            ->first();
            
        if ($namedInsured) {
            $namedInsuredAssignments = DB::table('driver_vehicle_assignment')
                ->where('driver_id', $namedInsured->id)
                ->where('status_id', Status::ACTIVE)
                ->count();
                
            if ($namedInsuredAssignments === 0) {
                $result->addError('Named insured must be assigned to at least one vehicle');
            }
        }
        
        return $result;
    }
}
```

### Rating Factor Application Logic
```php
class AssignmentRatingService
{
    public function applyDriverFactorsToVehicle(int $driverId, int $vehicleId): array
    {
        $appliedFactors = [];
        
        // Get driver assignment details
        $assignment = DB::table('driver_vehicle_assignment')
            ->where('driver_id', $driverId)
            ->where('vehicle_id', $vehicleId)
            ->where('status_id', Status::ACTIVE)
            ->first();
            
        if (!$assignment) {
            throw new AssignmentNotFoundException("No assignment found for driver {$driverId} and vehicle {$vehicleId}");
        }
        
        // Apply driver-level factors to vehicle
        $driverFactors = [
            'driver_class' => $this->driverClassService->calculateDriverClassFactor($driverId),
            'driver_points' => $this->driverPointsService->calculateDriverPointsFactor($driverId)
        ];
        
        foreach ($driverFactors as $factorType => $factor) {
            // Apply factor with assignment weight if not primary driver
            $weightedFactor = $assignment->is_primary_driver 
                ? $factor 
                : $this->applyAssignmentWeight($factor, $assignment->assignment_percentage);
                
            $appliedFactors[$factorType] = $weightedFactor;
        }
        
        return $appliedFactors;
    }
    
    private function applyAssignmentWeight(float $factor, ?float $assignmentPercentage): float
    {
        if (!$assignmentPercentage) {
            return $factor; // Full factor if no percentage specified
        }
        
        // Weighted factor calculation: 1 + ((factor - 1) * weight)
        $factorImpact = $factor - 1.0;
        $weightedImpact = $factorImpact * ($assignmentPercentage / 100.0);
        
        return 1.0 + $weightedImpact;
    }
}
```

---

## 5. Assignment Workflow Integration

### Assignment Change Management
```php
class AssignmentWorkflowService
{
    public function processAssignmentChange(AssignmentChangeRequest $request): WorkflowResult
    {
        // 1. Validate change request
        $validationResult = $this->validateAssignmentChange($request);
        if (!$validationResult->isValid()) {
            return WorkflowResult::failure($validationResult->getErrors());
        }
        
        // 2. Calculate rating impact
        $ratingImpact = $this->calculateRatingImpact($request);
        
        // 3. Apply assignment changes
        DB::transaction(function() use ($request) {
            // End current assignments
            $this->endCurrentAssignments($request->policy_id, $request->effective_date);
            
            // Create new assignments
            foreach ($request->new_assignments as $assignment) {
                $this->createAssignment($assignment);
            }
        });
        
        // 4. Trigger rating recalculation
        $this->ratingService->recalculatePolicyPremium($request->policy_id);
        
        // 5. Log assignment change
        $this->auditService->logAssignmentChange($request);
        
        return WorkflowResult::success([
            'assignment_changes' => $request->new_assignments,
            'rating_impact' => $ratingImpact
        ]);
    }
}
```

---

## 6. API Integration Requirements

### Driver Assignment Endpoints
```php
// Driver assignment API endpoints
GET /api/v1/rating/assignments/{policyId}
// Returns current driver-vehicle assignments

POST /api/v1/rating/assignments
{
    "policy_id": 12345,
    "assignments": [
        {
            "driver_id": 678,
            "vehicle_id": 901,
            "is_primary_driver": true,
            "assignment_type": "PRIMARY"
        },
        {
            "driver_id": 679,
            "vehicle_id": 901,
            "is_primary_driver": false,
            "assignment_type": "SECONDARY",
            "assignment_percentage": 25.0
        }
    ]
}

POST /api/v1/rating/assignments/validate
{
    "policy_id": 12345,
    "assignments": [...]
}
// Validate assignment configuration

PUT /api/v1/rating/assignments/{assignmentId}/primary
// Designate driver as primary for vehicle
```

### Response Format
```json
{
    "policy_id": 12345,
    "assignment_summary": {
        "total_drivers": 2,
        "total_vehicles": 2,
        "total_assignments": 3,
        "primary_assignments": 2
    },
    "assignments": [
        {
            "assignment_id": 11111,
            "driver_id": 678,
            "driver_name": "John Smith",
            "vehicle_id": 901,
            "vehicle_description": "2020 Honda Civic",
            "is_primary_driver": true,
            "assignment_type": "PRIMARY",
            "assignment_percentage": 100.0,
            "effective_date": "2025-07-15"
        },
        {
            "assignment_id": 11112,
            "driver_id": 679,
            "driver_name": "Jane Smith",
            "vehicle_id": 901,
            "vehicle_description": "2020 Honda Civic",
            "is_primary_driver": false,
            "assignment_type": "SECONDARY",
            "assignment_percentage": 25.0,
            "effective_date": "2025-07-15"
        }
    ],
    "validation_results": {
        "primary_driver_coverage": "PASS",
        "assignment_capacity": "PASS",
        "named_insured_assignment": "PASS"
    }
}
```

---

## 7. Validation Requirements

### Assignment Business Rule Validation
```php
class AssignmentValidator
{
    public function validateAssignmentBusinessRules(int $policyId): ValidationResult
    {
        $result = new ValidationResult();
        
        // Rule 1: Each vehicle must have exactly one primary driver
        $vehiclesPrimaryDriverCount = DB::table('driver_vehicle_assignment')
            ->select('vehicle_id', DB::raw('COUNT(*) as primary_count'))
            ->where('policy_id', $policyId)
            ->where('is_primary_driver', true)
            ->where('status_id', Status::ACTIVE)
            ->groupBy('vehicle_id')
            ->get();
            
        foreach ($vehiclesPrimaryDriverCount as $vehicle) {
            if ($vehicle->primary_count !== 1) {
                $result->addError("Vehicle {$vehicle->vehicle_id} has {$vehicle->primary_count} primary drivers (must be exactly 1)");
            }
        }
        
        // Rule 2: Named insured must be primary driver on at least one vehicle
        $namedInsuredPrimaryCount = DB::table('driver_vehicle_assignment')
            ->join('driver', 'driver_vehicle_assignment.driver_id', '=', 'driver.id')
            ->where('driver_vehicle_assignment.policy_id', $policyId)
            ->where('driver.is_named_insured', true)
            ->where('driver_vehicle_assignment.is_primary_driver', true)
            ->where('driver_vehicle_assignment.status_id', Status::ACTIVE)
            ->count();
            
        if ($namedInsuredPrimaryCount === 0) {
            $result->addError('Named insured must be primary driver on at least one vehicle');
        }
        
        // Rule 3: No driver can be primary on more than 3 vehicles (business rule)
        $driversExcessivePrimary = DB::table('driver_vehicle_assignment')
            ->select('driver_id', DB::raw('COUNT(*) as primary_count'))
            ->where('policy_id', $policyId)
            ->where('is_primary_driver', true)
            ->where('status_id', Status::ACTIVE)
            ->groupBy('driver_id')
            ->having('primary_count', '>', 3)
            ->pluck('driver_id');
            
        if ($driversExcessivePrimary->isNotEmpty()) {
            $result->addWarning("Drivers with excessive primary assignments: " . $driversExcessivePrimary->implode(', '));
        }
        
        return $result;
    }
}
```

---

## 8. Performance Optimization

### Assignment Lookup Caching
```php
class DriverAssignmentService
{
    public function getPolicyAssignments(int $policyId): Collection
    {
        $cacheKey = "policy_assignments_{$policyId}";
        
        return Cache::remember($cacheKey, 1800, function() use ($policyId) {
            return $this->loadPolicyAssignments($policyId);
        });
    }
    
    public function invalidateAssignmentCache(int $policyId): void
    {
        Cache::forget("policy_assignments_{$policyId}");
        
        // Also invalidate related rating caches
        Cache::forget("policy_rating_{$policyId}");
    }
}
```

### Database Performance
```sql
-- Assignment lookup optimization
CREATE INDEX idx_assignment_lookup_optimized 
ON driver_vehicle_assignment (
    policy_id, 
    driver_id, 
    vehicle_id, 
    is_primary_driver,
    effective_date
) WHERE status_id = 1;

-- Primary driver lookup optimization
CREATE INDEX idx_primary_driver_lookup 
ON driver_vehicle_assignment (
    vehicle_id, 
    is_primary_driver, 
    effective_date
) WHERE is_primary_driver = TRUE AND status_id = 1;
```

---

## 9. Testing Requirements

### Assignment Logic Testing
```php
class DriverAssignmentServiceTest extends TestCase
{
    public function test_primary_driver_assignment()
    {
        // Test primary driver assignment and uniqueness
        $assignment1 = $this->assignmentService->assignPrimaryDriver($this->driver1Id, $this->vehicle1Id);
        $this->assertTrue($assignment1->isSuccess());
        
        // Attempt to assign different primary driver to same vehicle
        $assignment2 = $this->assignmentService->assignPrimaryDriver($this->driver2Id, $this->vehicle1Id);
        $this->assertTrue($assignment2->isSuccess());
        
        // Verify first driver is no longer primary
        $primaryDriver = $this->assignmentService->getPrimaryDriver($this->vehicle1Id);
        $this->assertEquals($this->driver2Id, $primaryDriver->id);
    }
    
    public function test_assignment_validation()
    {
        // Test assignment business rule validation
        $result = $this->assignmentValidator->validateAssignmentBusinessRules($this->policyId);
        $this->assertTrue($result->isValid());
    }
    
    public function test_rating_factor_application()
    {
        // Test driver factors applied to assigned vehicle
        $factors = $this->assignmentRatingService->applyDriverFactorsToVehicle(
            $this->driverId, 
            $this->vehicleId
        );
        
        $this->assertArrayHasKey('driver_class', $factors);
        $this->assertArrayHasKey('driver_points', $factors);
    }
}
```

---

## Implementation Priority: HIGH
This factor is essential for proper driver-vehicle rating coordination and must be implemented as part of the core rating components.

## Dependencies
- **Driver Class Factor**: Driver factors applied through assignments
- **Driver Points Factor**: Driver factors applied through assignments
- **Vehicle Factors**: Assignment coordination with vehicle-level factors

## Estimated Implementation Effort
- **Database Schema**: 3 days
- **Service Layer**: 5 days
- **Validation Logic**: 3 days
- **API Integration**: 2 days
- **Testing**: 3 days
- **Total**: 16 days

This plan implements comprehensive driver-vehicle assignment management while ensuring proper rating factor application and business rule compliance throughout the assignment process.