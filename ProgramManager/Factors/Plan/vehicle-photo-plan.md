# Vehicle Photo Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Vehicle Photo  
**Category**: Vehicle Factor  
**Priority**: Medium - Physical damage risk mitigation through documentation  
**Implementation Complexity**: High  

### Business Requirements Summary
The Vehicle Photo factor implements risk-based premium discounts for comprehensive and collision coverage based on vehicle photo submission. This factor provides a 25% discount for customers who submit required vehicle photos, promoting risk assessment accuracy and fraud prevention while requiring robust photo management and compliance monitoring systems.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing and new Global Requirements:

#### Leverages GR-65: Rating Engine Architecture
**Integration**: Photo discount factor calculation within multiplicative rating engine  
**Dependencies**: RatingEngineService for photo compliance-based factor determination

#### Leverages GR-63: Vehicle Photo Requirements (Program Traits)
**Integration**: Photo submission standards and compliance requirements  
**Dependencies**: Photo quality standards, submission timelines, and verification procedures

#### New Requirement: GR-89: Photo Compliance Management Standards
**Priority**: Medium  
**Rationale**: Photo submission tracking and compliance monitoring for discount eligibility  

**Core Components**:
- Photo submission requirement definition and tracking methodology
- Photo quality validation and acceptance criteria standards
- Compliance monitoring and discount management workflows
- Automatic discount application and removal processing
- Photo storage and access security requirements
- Customer communication and notification standards for photo requirements

#### Leverages GR-37: Locking & Action Tracking
**Integration**: Photo submission status changes and discount application/removal audit trails  
**Dependencies**: Photo compliance history tracking and underwriter action logging

### Integration with Existing Global Requirements
- **GR-41**: Table Schema Requirements - Photo compliance and factor tracking table structures
- **GR-20**: Application Business Logic - Photo validation and discount application patterns
- **GR-24**: Data Security - Photo storage security and customer privacy protection

---

## 2. Service Architecture Requirements

### Photo Compliance Management Services

#### VehiclePhotoService
**Purpose**: Photo discount factor calculation and compliance management  
**Location**: `app/Domain/Rating/Services/VehiclePhotoService.php`

**Key Methods**:
```php
class VehiclePhotoService
{
    public function calculatePhotoFactor(VehiclePhotoData $photoData): PhotoFactor
    {
        // 1. Check photo submission compliance status
        // 2. Validate physical damage coverage eligibility
        // 3. Apply automatic discount with compliance tracking
        // 4. Calculate factor for comprehensive and collision coverage
        // 5. Return factor with compliance details and requirements
    }
    
    public function validatePhotoCompliance(int $vehicleId): PhotoComplianceResult
    {
        // Validate current photo submission compliance status
    }
    
    public function applyAutomaticDiscount(VehicleData $vehicleData): DiscountApplicationResult
    {
        // Apply default 25% discount with compliance monitoring
    }
    
    public function removeNonComplianceDiscount(int $vehicleId, string $reason): DiscountRemovalResult
    {
        // Remove discount for non-compliance with audit trail
    }
}
```

#### PhotoComplianceService
**Purpose**: Photo submission tracking and compliance monitoring  
**Location**: `app/Domain/Rating/Services/PhotoComplianceService.php`

**Key Methods**:
```php
class PhotoComplianceService
{
    public function trackPhotoSubmission(PhotoSubmissionData $submissionData): PhotoSubmissionResult
    {
        // Track photo submission with quality validation
    }
    
    public function verifyPhotoQuality(PhotoData $photoData): PhotoQualityResult
    {
        // Verify submitted photos meet quality standards
    }
    
    public function monitorComplianceDeadlines(): Collection
    {
        // Monitor and alert on approaching photo submission deadlines
    }
    
    public function generateComplianceReport(PolicyData $policyData): ComplianceReport
    {
        // Generate photo compliance status report for underwriting
    }
}
```

---

## 3. Database Schema Requirements

### Photo Compliance Management Tables

#### photo_requirement
```sql
CREATE TABLE photo_requirement (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    requirement_code VARCHAR(50) NOT NULL,
    requirement_name VARCHAR(255) NOT NULL,
    requirement_description TEXT,
    photo_count_minimum INT NOT NULL DEFAULT 4,
    photo_angles_required JSON, -- Array of required photo angles
    submission_deadline_days INT NOT NULL DEFAULT 30,
    quality_standards JSON, -- Photo quality requirements
    coverage_dependencies JSON, -- Required coverage types
    discount_percentage DECIMAL(5,2) NOT NULL DEFAULT 25.00,
    automatic_application BOOLEAN DEFAULT TRUE,
    underwriter_verification_required BOOLEAN DEFAULT TRUE,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_program_requirement (program_id, requirement_code, effective_date),
    INDEX idx_program_requirements (program_id, effective_date),
    INDEX idx_automatic_application (automatic_application, status_id)
);

-- Aguila Dorada photo requirements
INSERT INTO photo_requirement (program_id, requirement_code, requirement_name, photo_count_minimum, photo_angles_required, submission_deadline_days, quality_standards, coverage_dependencies, discount_percentage, effective_date) VALUES
(1, 'STANDARD_VEHICLE_PHOTOS', 'Standard Vehicle Photo Requirement', 4, 
 '["FRONT", "REAR", "LEFT_SIDE", "RIGHT_SIDE"]', 30,
 '{"min_resolution": "1024x768", "format": ["JPG", "PNG"], "max_file_size": "5MB", "lighting": "ADEQUATE", "clarity": "CLEAR"}',
 '["COMP", "COLL"]', 25.00, '2025-07-15');
```

#### vehicle_photo_submission
```sql
CREATE TABLE vehicle_photo_submission (
    id BIGINT PRIMARY KEY,
    vehicle_id BIGINT NOT NULL,
    policy_id BIGINT NOT NULL,
    requirement_id BIGINT NOT NULL,
    submission_date DATE NOT NULL,
    submission_deadline DATE NOT NULL,
    photos_submitted INT NOT NULL DEFAULT 0,
    photos_required INT NOT NULL,
    compliance_status ENUM('PENDING', 'COMPLIANT', 'NON_COMPLIANT', 'PARTIAL') NOT NULL,
    quality_verification_status ENUM('PENDING', 'APPROVED', 'REJECTED', 'REQUIRES_RESUBMISSION') NOT NULL DEFAULT 'PENDING',
    quality_verification_date DATE,
    quality_verification_notes TEXT,
    discount_applied BOOLEAN DEFAULT TRUE,
    discount_application_date DATE,
    discount_removal_date DATE,
    discount_removal_reason TEXT,
    photo_storage_references JSON, -- Array of photo file references
    submission_method ENUM('PORTAL', 'EMAIL', 'MOBILE_APP', 'AGENT_UPLOAD') NOT NULL,
    submission_source VARCHAR(255),
    verified_by BIGINT,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(id),
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (requirement_id) REFERENCES photo_requirement(id),
    FOREIGN KEY (verified_by) REFERENCES user(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_vehicle_photo_submissions (vehicle_id, submission_date),
    INDEX idx_compliance_status (compliance_status, quality_verification_status),
    INDEX idx_submission_deadline (submission_deadline, compliance_status),
    INDEX idx_discount_tracking (discount_applied, discount_application_date)
);
```

#### photo_factor
```sql
CREATE TABLE photo_factor (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    coverage_type_id BIGINT NOT NULL,
    photo_submission_status ENUM('SUBMITTED', 'NOT_SUBMITTED', 'NON_COMPLIANT') NOT NULL,
    factor_value DECIMAL(6,4) NOT NULL,
    discount_percentage DECIMAL(5,2), -- Percentage discount (e.g., 25.00 for 25%)
    factor_description TEXT,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (coverage_type_id) REFERENCES coverage_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_photo_factor (
        program_id, 
        coverage_type_id, 
        photo_submission_status, 
        effective_date
    ),
    INDEX idx_program_coverage_factors (program_id, coverage_type_id),
    INDEX idx_submission_status_factors (photo_submission_status, factor_value),
    INDEX idx_effective_dates (effective_date, expiration_date)
);
```

#### photo_compliance_audit
```sql
CREATE TABLE photo_compliance_audit (
    id BIGINT PRIMARY KEY,
    vehicle_id BIGINT NOT NULL,
    policy_id BIGINT NOT NULL,
    submission_id BIGINT,
    audit_date DATE NOT NULL,
    compliance_action ENUM('DISCOUNT_APPLIED', 'DISCOUNT_REMOVED', 'SUBMISSION_APPROVED', 'SUBMISSION_REJECTED', 'DEADLINE_EXTENDED') NOT NULL,
    previous_status VARCHAR(100),
    new_status VARCHAR(100),
    action_reason TEXT,
    premium_impact DECIMAL(10,2), -- Premium change amount
    effective_date DATE,
    performed_by BIGINT,
    customer_notified BOOLEAN DEFAULT FALSE,
    notification_date DATE,
    system_generated BOOLEAN DEFAULT FALSE,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(id),
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (submission_id) REFERENCES vehicle_photo_submission(id),
    FOREIGN KEY (performed_by) REFERENCES user(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_vehicle_compliance_audit (vehicle_id, audit_date),
    INDEX idx_compliance_action (compliance_action, audit_date),
    INDEX idx_premium_impact (premium_impact, effective_date),
    INDEX idx_performed_by (performed_by, audit_date)
);
```

---

## 4. Business Logic Requirements

### Photo Factor Calculation Logic
```php
class VehiclePhotoService
{
    public function calculatePhotoFactor(VehiclePhotoData $photoData): PhotoFactor
    {
        // 1. Check if physical damage coverage exists
        $hasPhysicalDamage = $this->hasPhysicalDamageCoverage($photoData->coverage_types);
        
        if (!$hasPhysicalDamage) {
            return new PhotoFactor([
                'vehicle_id' => $photoData->vehicle_id,
                'factor_value' => 1.0000,
                'applies' => false,
                'reason' => 'No physical damage coverage - photo factor not applicable'
            ]);
        }
        
        // 2. Get current photo compliance status
        $complianceResult = $this->validatePhotoCompliance($photoData->vehicle_id);
        
        // 3. Determine photo submission status
        $submissionStatus = $this->determineSubmissionStatus($complianceResult);
        
        // 4. Get factors for each applicable coverage
        $factorsByTOVCIFactor = [];
        foreach (['COMP', 'COLL'] as $coverageType) {
            if (in_array($coverageType, $photoData->coverage_types)) {
                $factor = $this->getPhotoFactor($coverageType, $submissionStatus);
                $factorsByTOVCIFactor[$coverageType] = $factor;
            }
        }
        
        // 5. Apply automatic discount logic if new business
        if ($photoData->is_new_business && $submissionStatus === 'NOT_SUBMITTED') {
            $this->applyAutomaticDiscount($photoData->vehicle_data);
            $submissionStatus = 'SUBMITTED'; // Treat as submitted for factor calculation
            
            // Update factors to reflect automatic discount
            foreach ($factorsByTOVCIFactor as $coverage => $factor) {
                $factorsByTOVCIFactor[$coverage] = $this->getPhotoFactor($coverage, 'SUBMITTED');
            }
        }
        
        return new PhotoFactor([
            'vehicle_id' => $photoData->vehicle_id,
            'factors_by_coverage' => $factorsByTOVCIFactor,
            'compliance_status' => $complianceResult,
            'submission_status' => $submissionStatus,
            'automatic_discount_applied' => $photoData->is_new_business && $submissionStatus === 'SUBMITTED',
            'compliance_deadline' => $this->getComplianceDeadline($photoData->vehicle_id)
        ]);
    }
    
    private function getPhotoFactor(string $coverageType, string $submissionStatus): float
    {
        $factor = DB::table('photo_factor')
            ->join('coverage_type', 'photo_factor.coverage_type_id', '=', 'coverage_type.id')
            ->where('coverage_type.coverage_code', $coverageType)
            ->where('photo_factor.photo_submission_status', $submissionStatus)
            ->where('photo_factor.program_id', $this->programId)
            ->where('photo_factor.effective_date', '<=', now())
            ->where(function($query) {
                $query->whereNull('photo_factor.expiration_date')
                      ->orWhere('photo_factor.expiration_date', '>', now());
            })
            ->where('photo_factor.status_id', Status::ACTIVE)
            ->value('photo_factor.factor_value');
            
        return $factor ?? 1.0000; // Default to no adjustment if not found
    }
    
    public function applyAutomaticDiscount(VehicleData $vehicleData): DiscountApplicationResult
    {
        // Create photo submission record with automatic discount
        $submissionId = DB::table('vehicle_photo_submission')->insertGetId([
            'vehicle_id' => $vehicleData->vehicle_id,
            'policy_id' => $vehicleData->policy_id,
            'requirement_id' => $this->getActivePhotoRequirement()->id,
            'submission_date' => now(),
            'submission_deadline' => now()->addDays(30), // 30-day deadline
            'photos_submitted' => 0,
            'photos_required' => 4,
            'compliance_status' => 'PENDING',
            'quality_verification_status' => 'PENDING',
            'discount_applied' => true,
            'discount_application_date' => now(),
            'submission_method' => 'SYSTEM_AUTOMATIC',
            'submission_source' => 'Automatic discount application at policy binding',
            'status_id' => Status::ACTIVE,
            'created_by' => $vehicleData->created_by
        ]);
        
        // Create audit record
        DB::table('photo_compliance_audit')->insert([
            'vehicle_id' => $vehicleData->vehicle_id,
            'policy_id' => $vehicleData->policy_id,
            'submission_id' => $submissionId,
            'audit_date' => now(),
            'compliance_action' => 'DISCOUNT_APPLIED',
            'new_status' => 'PENDING_PHOTOS',
            'action_reason' => 'Automatic 25% discount applied at policy binding - photos required within 30 days',
            'premium_impact' => $this->calculatePremiumImpact($vehicleData, 0.7500), // 25% discount
            'effective_date' => now(),
            'performed_by' => $vehicleData->created_by,
            'system_generated' => true,
            'status_id' => Status::ACTIVE
        ]);
        
        return new DiscountApplicationResult([
            'submission_id' => $submissionId,
            'discount_applied' => true,
            'compliance_deadline' => now()->addDays(30),
            'factor_value' => 0.7500
        ]);
    }
}
```

### Photo Compliance Monitoring Logic
```php
class PhotoComplianceService
{
    public function validatePhotoCompliance(int $vehicleId): PhotoComplianceResult
    {
        $submission = DB::table('vehicle_photo_submission')
            ->where('vehicle_id', $vehicleId)
            ->where('status_id', Status::ACTIVE)
            ->orderBy('submission_date', 'desc')
            ->first();
            
        if (!$submission) {
            return new PhotoComplianceResult([
                'compliant' => false,
                'status' => 'NO_SUBMISSION',
                'photos_required' => 4,
                'photos_submitted' => 0
            ]);
        }
        
        // Check deadline compliance
        $deadlinePassed = Carbon::parse($submission->submission_deadline) < now();
        
        // Determine compliance status
        if ($submission->compliance_status === 'COMPLIANT' && $submission->quality_verification_status === 'APPROVED') {
            return new PhotoComplianceResult([
                'compliant' => true,
                'status' => 'COMPLIANT',
                'photos_required' => $submission->photos_required,
                'photos_submitted' => $submission->photos_submitted,
                'verification_date' => $submission->quality_verification_date
            ]);
        }
        
        if ($deadlinePassed && $submission->compliance_status !== 'COMPLIANT') {
            return new PhotoComplianceResult([
                'compliant' => false,
                'status' => 'DEADLINE_EXCEEDED',
                'photos_required' => $submission->photos_required,
                'photos_submitted' => $submission->photos_submitted,
                'deadline' => $submission->submission_deadline
            ]);
        }
        
        return new PhotoComplianceResult([
            'compliant' => false,
            'status' => 'PENDING',
            'photos_required' => $submission->photos_required,
            'photos_submitted' => $submission->photos_submitted,
            'deadline' => $submission->submission_deadline,
            'days_remaining' => Carbon::parse($submission->submission_deadline)->diffInDays(now())
        ]);
    }
    
    public function monitorComplianceDeadlines(): Collection
    {
        // Find submissions approaching deadline or past due
        $deadlineAlerts = DB::table('vehicle_photo_submission')
            ->join('vehicle', 'vehicle_photo_submission.vehicle_id', '=', 'vehicle.id')
            ->join('policy', 'vehicle_photo_submission.policy_id', '=', 'policy.id')
            ->where('vehicle_photo_submission.compliance_status', '!=', 'COMPLIANT')
            ->where('vehicle_photo_submission.status_id', Status::ACTIVE)
            ->where(function($query) {
                // Approaching deadline (7 days) or past due
                $query->where('vehicle_photo_submission.submission_deadline', '<=', now()->addDays(7))
                      ->orWhere('vehicle_photo_submission.submission_deadline', '<', now());
            })
            ->select([
                'vehicle_photo_submission.*',
                'vehicle.vin',
                'policy.policy_number'
            ])
            ->get();
            
        return $deadlineAlerts->map(function($alert) {
            $daysPastDue = Carbon::parse($alert->submission_deadline) < now() 
                ? now()->diffInDays(Carbon::parse($alert->submission_deadline))
                : 0;
                
            return [
                'submission_id' => $alert->id,
                'vehicle_id' => $alert->vehicle_id,
                'policy_number' => $alert->policy_number,
                'vin' => $alert->vin,
                'deadline' => $alert->submission_deadline,
                'days_past_due' => $daysPastDue,
                'action_required' => $daysPastDue > 0 ? 'REMOVE_DISCOUNT' : 'SEND_REMINDER',
                'photos_submitted' => $alert->photos_submitted,
                'photos_required' => $alert->photos_required
            ];
        });
    }
}
```

---

## 5. Aguila Dorada Photo Factor Matrix

### Photo Factor Implementation
```sql
-- Photo factors for Aguila Dorada program
-- Factors apply to Comprehensive and Collision coverage only

-- Photos Submitted (25% discount)
INSERT INTO photo_factor (program_id, coverage_type_id, photo_submission_status, factor_value, discount_percentage, factor_description, effective_date) VALUES
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'COMP'), 'SUBMITTED', 0.7500, 25.00, '25% discount for submitted vehicle photos', '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'COLL'), 'SUBMITTED', 0.7500, 25.00, '25% discount for submitted vehicle photos', '2025-07-15'),

-- Photos Not Submitted (base rate)
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'COMP'), 'NOT_SUBMITTED', 1.0000, 0.00, 'Base rate when photos not submitted', '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'COLL'), 'NOT_SUBMITTED', 1.0000, 0.00, 'Base rate when photos not submitted', '2025-07-15'),

-- Non-Compliant Photos (base rate - discount removed)
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'COMP'), 'NON_COMPLIANT', 1.0000, 0.00, 'Base rate when photos non-compliant or deadline exceeded', '2025-07-15'),
(1, (SELECT id FROM coverage_type WHERE coverage_code = 'COLL'), 'NON_COMPLIANT', 1.0000, 0.00, 'Base rate when photos non-compliant or deadline exceeded', '2025-07-15');
```

---

## 6. API Integration Requirements

### Photo Factor Endpoints
```php
// Photo factor API endpoints
POST /api/v1/rating/photo/calculate
{
    "vehicle_photo_data": {
        "vehicle_id": 12345,
        "coverage_types": ["COMP", "COLL"],
        "is_new_business": true,
        "vehicle_data": {
            "policy_id": 67890,
            "vin": "1HGCM82633A123456"
        }
    }
}

GET /api/v1/rating/photo/compliance/{vehicleId}
// Get current photo compliance status

POST /api/v1/rating/photo/submit
{
    "vehicle_id": 12345,
    "photos": [
        {
            "angle": "FRONT",
            "file_reference": "photo_12345_front.jpg",
            "file_size": "2.5MB",
            "resolution": "1920x1080"
        }
    ],
    "submission_method": "PORTAL"
}

POST /api/v1/rating/photo/verify-quality
{
    "submission_id": 67890,
    "verification_status": "APPROVED",
    "quality_notes": "All photos meet minimum requirements",
    "verified_by": 123
}

GET /api/v1/rating/photo/compliance-alerts
// Get vehicles with upcoming or past due photo deadlines
```

### Response Format
```json
{
    "vehicle_id": 12345,
    "photo_factors": {
        "COMP": 0.7500,
        "COLL": 0.7500
    },
    "factor_details": {
        "submission_status": "SUBMITTED",
        "discount_percentage": 25.00,
        "automatic_discount_applied": true,
        "factor_description": "25% discount for submitted vehicle photos"
    },
    "compliance_status": {
        "compliant": false,
        "status": "PENDING",
        "photos_required": 4,
        "photos_submitted": 0,
        "deadline": "2025-08-14",
        "days_remaining": 23
    },
    "submission_requirements": {
        "photo_angles_required": ["FRONT", "REAR", "LEFT_SIDE", "RIGHT_SIDE"],
        "quality_standards": {
            "min_resolution": "1024x768",
            "max_file_size": "5MB",
            "accepted_formats": ["JPG", "PNG"]
        },
        "submission_deadline": "2025-08-14"
    },
    "premium_impact": {
        "annual_savings": 125.00,
        "discount_at_risk": true,
        "compliance_required": "Photos must be submitted by deadline to retain discount"
    }
}
```

---

## 7. Performance Requirements

### Photo Factor Caching
```php
class VehiclePhotoService
{
    public function calculatePhotoFactor(VehiclePhotoData $photoData): PhotoFactor
    {
        // Cache photo factors by submission status
        $cacheKey = "photo_factor_{$this->programId}_{$photoData->submission_status}";
        
        return Cache::remember($cacheKey, 3600, function() use ($photoData) {
            return $this->performPhotoFactorCalculation($photoData);
        });
    }
}
```

### Database Performance
```sql
-- Photo factor lookup optimization
CREATE INDEX idx_photo_factor_lookup 
ON photo_factor (
    program_id, 
    coverage_type_id, 
    photo_submission_status,
    effective_date
) WHERE status_id = 1;

-- Compliance monitoring optimization
CREATE INDEX idx_compliance_monitoring 
ON vehicle_photo_submission (
    compliance_status, 
    submission_deadline, 
    status_id
) WHERE compliance_status != 'COMPLIANT';

-- Vehicle photo compliance lookup
CREATE INDEX idx_vehicle_photo_compliance 
ON vehicle_photo_submission (
    vehicle_id, 
    submission_date, 
    compliance_status
) WHERE status_id = 1;
```

---

## 8. Testing Requirements

### Photo Factor Testing
```php
class VehiclePhotoServiceTest extends TestCase
{
    public function test_automatic_discount_application()
    {
        $photoData = new VehiclePhotoData([
            'vehicle_id' => 12345,
            'coverage_types' => ['COMP', 'COLL'],
            'is_new_business' => true
        ]);
        
        $factor = $this->photoService->calculatePhotoFactor($photoData);
        
        $this->assertTrue($factor->automatic_discount_applied);
        $this->assertEquals(0.7500, $factor->factors_by_coverage['COMP']);
        $this->assertEquals(0.7500, $factor->factors_by_coverage['COLL']);
        $this->assertEquals('PENDING', $factor->compliance_status->status);
    }
    
    public function test_compliant_photos_discount()
    {
        // Set up vehicle with compliant photo submission
        $this->createCompliantPhotoSubmission(12345);
        
        $photoData = new VehiclePhotoData([
            'vehicle_id' => 12345,
            'coverage_types' => ['COMP', 'COLL'],
            'is_new_business' => false
        ]);
        
        $factor = $this->photoService->calculatePhotoFactor($photoData);
        
        $this->assertTrue($factor->compliance_status->compliant);
        $this->assertEquals(0.7500, $factor->factors_by_coverage['COMP']);
        $this->assertEquals(0.7500, $factor->factors_by_coverage['COLL']);
    }
    
    public function test_non_compliant_discount_removal()
    {
        // Set up vehicle with expired photo deadline
        $this->createExpiredPhotoSubmission(12345);
        
        $photoData = new VehiclePhotoData([
            'vehicle_id' => 12345,
            'coverage_types' => ['COMP', 'COLL'],
            'is_new_business' => false
        ]);
        
        $factor = $this->photoService->calculatePhotoFactor($photoData);
        
        $this->assertFalse($factor->compliance_status->compliant);
        $this->assertEquals(1.0000, $factor->factors_by_coverage['COMP']); // Discount removed
        $this->assertEquals(1.0000, $factor->factors_by_coverage['COLL']); // Discount removed
        $this->assertEquals('DEADLINE_EXCEEDED', $factor->compliance_status->status);
    }
    
    public function test_no_physical_damage_no_factor()
    {
        $photoData = new VehiclePhotoData([
            'vehicle_id' => 12345,
            'coverage_types' => ['BI', 'PD', 'UMBI', 'UMPD'], // No COMP/COLL
            'is_new_business' => true
        ]);
        
        $factor = $this->photoService->calculatePhotoFactor($photoData);
        
        $this->assertFalse($factor->applies);
        $this->assertEquals(1.0000, $factor->factor_value);
        $this->assertEquals('No physical damage coverage - photo factor not applicable', $factor->reason);
    }
}
```

---

## Implementation Priority: MEDIUM
This factor provides fraud prevention and risk assessment benefits but requires complex photo management systems. Should be implemented after core rating factors are operational.

## Dependencies
- **Photo Storage System**: Secure photo storage and retrieval infrastructure
- **Customer Portal**: Photo upload capability for customers
- **Underwriting Tools**: Photo review and verification interfaces
- **GR-63 Implementation**: Vehicle photo requirements from program traits

## Estimated Implementation Effort
- **Database Schema**: 4 days
- **Service Layer**: 5 days
- **Photo Storage Integration**: 4 days
- **Compliance Monitoring**: 3 days
- **Underwriter Tools**: 3 days
- **API Integration**: 2 days
- **Testing**: 4 days
- **Total**: 25 days

This plan implements comprehensive photo-based discount management with automatic application, robust compliance monitoring, and proper audit trails while maintaining customer convenience and operational efficiency for underwriting oversight.