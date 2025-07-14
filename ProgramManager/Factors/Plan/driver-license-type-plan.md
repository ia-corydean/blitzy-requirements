# Driver License Type Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Driver License Type  
**Category**: Driver Factor  
**Priority**: Medium - License classification risk assessment  
**Implementation Complexity**: Medium  

### Business Requirements Summary
The Driver License Type factor implements risk-based pricing adjustments based on the type and validity of driver's licenses held by policy drivers. This factor accounts for different license classifications (standard, commercial, international, etc.), license status (valid, expired, suspended), and experience levels to provide appropriate risk assessment and premium adjustments.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing and new Global Requirements:

#### Leverages GR-73: Motor Vehicle Record Integration
**Integration**: License verification and status validation through MVR systems  
**Dependencies**: License data validation and multi-state license tracking

#### New Requirement: GR-79: Driver License Management Standards
**Priority**: Medium  
**Rationale**: License classification and validation standards for insurance rating  

**Core Components**:
- License type classification and risk assessment methodology
- License status validation and expiration tracking
- Multi-state license recognition and verification standards
- Commercial license endorsement tracking and rating impact
- International license recognition and restriction management
- License restriction and endorsement impact on risk assessment

#### Leverages GR-72: Demographic Rating Standards
**Integration**: License-based risk factors complementing demographic factors  
**Dependencies**: Age and experience correlation with license type factors

### Integration with Existing Global Requirements
- **GR-65**: Rating Engine Architecture - License factor integration with core rating
- **GR-41**: Table Schema Requirements - License classification and tracking tables
- **GR-04**: Validation & Data Handling - License validation and verification patterns

---

## 2. Service Architecture Requirements

### License Classification Services

#### DriverLicenseTypeService
**Purpose**: License type classification and factor determination  
**Location**: `app/Domain/Rating/Services/DriverLicenseTypeService.php`

**Key Methods**:
```php
class DriverLicenseTypeService
{
    public function calculateLicenseTypeFactor(DriverLicenseData $licenseData): LicenseTypeFactor
    {
        // 1. Classify license type and status
        // 2. Evaluate license restrictions and endorsements
        // 3. Calculate experience-based adjustments
        // 4. Apply license-specific risk factors
        // 5. Return factor with detailed breakdown
    }
    
    public function validateLicenseEligibility(DriverLicenseData $licenseData): ValidationResult
    {
        // Validate license eligibility for insurance coverage
    }
    
    public function classifyLicenseType(string $licenseClass, string $licenseState): LicenseTypeClassification
    {
        // Classify license into standard rating categories
    }
}
```

#### LicenseVerificationService
**Purpose**: License verification and status validation  
**Location**: `app/Domain/Rating/Services/LicenseVerificationService.php`

**Key Methods**:
```php
class LicenseVerificationService
{
    public function verifyLicenseStatus(string $licenseNumber, string $state): LicenseVerificationResult
    {
        // Verify license status through state DMV systems
    }
    
    public function validateLicenseRestrictions(DriverLicenseData $licenseData): RestrictionValidation
    {
        // Validate license restrictions and endorsements
    }
    
    public function checkLicenseExpiration(DriverLicenseData $licenseData): ExpirationCheck
    {
        // Check license expiration and renewal requirements
    }
}
```

---

## 3. Database Schema Requirements

### License Type Management Tables

#### license_type_classification
```sql
CREATE TABLE license_type_classification (
    id BIGINT PRIMARY KEY,
    classification_code VARCHAR(50) UNIQUE NOT NULL,
    classification_name VARCHAR(255) NOT NULL,
    classification_description TEXT,
    license_category ENUM('STANDARD', 'COMMERCIAL', 'MOTORCYCLE', 'INTERNATIONAL', 'RESTRICTED', 'LEARNER') NOT NULL,
    risk_level ENUM('LOW', 'STANDARD', 'HIGH', 'VERY_HIGH') NOT NULL,
    base_factor DECIMAL(6,4) NOT NULL DEFAULT 1.0000,
    requires_verification BOOLEAN DEFAULT TRUE,
    eligibility_restrictions JSON, -- Array of restrictions/requirements
    experience_requirements JSON, -- Experience thresholds and factors
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_license_category (license_category, status_id),
    INDEX idx_risk_level (risk_level, status_id),
    INDEX idx_verification_required (requires_verification, status_id)
);

-- Aguila Dorada license type classifications
INSERT INTO license_type_classification (classification_code, classification_name, license_category, risk_level, base_factor, requires_verification) VALUES
('STANDARD_VALID', 'Standard Valid License', 'STANDARD', 'STANDARD', 1.0000, TRUE),
('STANDARD_EXPIRED', 'Standard Expired License', 'STANDARD', 'HIGH', 1.2500, TRUE),
('COMMERCIAL_CDL', 'Commercial Drivers License', 'COMMERCIAL', 'LOW', 0.9000, TRUE),
('MOTORCYCLE_ONLY', 'Motorcycle License Only', 'MOTORCYCLE', 'HIGH', 1.3000, TRUE),
('INTERNATIONAL', 'International License', 'INTERNATIONAL', 'HIGH', 1.4000, TRUE),
('LEARNER_PERMIT', 'Learner Permit', 'LEARNER', 'VERY_HIGH', 1.7500, TRUE),
('NO_LICENSE', 'No Valid License', 'RESTRICTED', 'VERY_HIGH', 2.0000, FALSE),
('SUSPENDED_LICENSE', 'Suspended License', 'RESTRICTED', 'VERY_HIGH', 3.0000, TRUE);
```

#### license_endorsement_restriction
```sql
CREATE TABLE license_endorsement_restriction (
    id BIGINT PRIMARY KEY,
    endorsement_code VARCHAR(50) NOT NULL,
    endorsement_name VARCHAR(255) NOT NULL,
    endorsement_type ENUM('ENDORSEMENT', 'RESTRICTION', 'CONDITION') NOT NULL,
    factor_modifier DECIMAL(6,4) NOT NULL DEFAULT 1.0000,
    eligibility_impact ENUM('NONE', 'LIMITED', 'INELIGIBLE') NOT NULL DEFAULT 'NONE',
    description TEXT,
    state_specific BOOLEAN DEFAULT FALSE,
    applicable_states JSON, -- Array of state codes if state_specific = true
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_endorsement_code (endorsement_code),
    INDEX idx_endorsement_type (endorsement_type, status_id),
    INDEX idx_eligibility_impact (eligibility_impact),
    INDEX idx_state_specific (state_specific, applicable_states)
);

-- Common license endorsements and restrictions
INSERT INTO license_endorsement_restriction (endorsement_code, endorsement_name, endorsement_type, factor_modifier, eligibility_impact, description) VALUES
('CORRECTIVE_LENSES', 'Corrective Lenses Required', 'RESTRICTION', 1.0000, 'NONE', 'Must wear corrective lenses while driving'),
('DAYLIGHT_ONLY', 'Daylight Driving Only', 'RESTRICTION', 1.1000, 'LIMITED', 'Restricted to daylight hours only'),
('AREA_RESTRICTED', 'Area/Distance Restricted', 'RESTRICTION', 1.0500, 'LIMITED', 'Restricted to specific geographic area'),
('IGNITION_INTERLOCK', 'Ignition Interlock Device', 'CONDITION', 1.5000, 'LIMITED', 'Required ignition interlock device'),
('MEDICAL_REVIEW', 'Medical Review Required', 'CONDITION', 1.2000, 'LIMITED', 'Periodic medical review required'),
('CDL_HAZMAT', 'Hazardous Materials Endorsement', 'ENDORSEMENT', 0.9500, 'NONE', 'Qualified for hazardous materials transport'),
('CDL_PASSENGER', 'Passenger Vehicle Endorsement', 'ENDORSEMENT', 0.9500, 'NONE', 'Qualified for passenger transport'),
('MOTORCYCLE_ENDORSEMENT', 'Motorcycle Endorsement', 'ENDORSEMENT', 1.0000, 'NONE', 'Qualified for motorcycle operation');
```

#### driver_license_factor
```sql
CREATE TABLE driver_license_factor (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    classification_id BIGINT NOT NULL,
    years_licensed_min INT NOT NULL DEFAULT 0,
    years_licensed_max INT, -- NULL for open-ended ranges
    factor_value DECIMAL(6,4) NOT NULL,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    actuarial_justification TEXT,
    regulatory_notes TEXT,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (classification_id) REFERENCES license_type_classification(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_license_factor (
        program_id, 
        classification_id, 
        years_licensed_min, 
        years_licensed_max, 
        effective_date
    ),
    INDEX idx_program_classification (program_id, classification_id),
    INDEX idx_years_licensed_range (years_licensed_min, years_licensed_max),
    INDEX idx_effective_dates (effective_date, expiration_date)
);
```

#### driver_license_history
```sql
CREATE TABLE driver_license_history (
    id BIGINT PRIMARY KEY,
    driver_id BIGINT NOT NULL,
    license_number VARCHAR(100) NOT NULL,
    license_state_id BIGINT NOT NULL,
    license_class VARCHAR(50),
    classification_id BIGINT,
    issue_date DATE,
    expiration_date DATE,
    first_licensed_date DATE,
    endorsements JSON, -- Array of endorsement codes
    restrictions JSON, -- Array of restriction codes
    verification_status ENUM('PENDING', 'VERIFIED', 'FAILED', 'EXPIRED') NOT NULL,
    verification_date DATE,
    verification_method VARCHAR(100),
    effective_date DATE NOT NULL,
    end_date DATE,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (driver_id) REFERENCES driver(id),
    FOREIGN KEY (license_state_id) REFERENCES state(id),
    FOREIGN KEY (classification_id) REFERENCES license_type_classification(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_driver_license_history (driver_id, effective_date),
    INDEX idx_license_verification (verification_status, verification_date),
    INDEX idx_license_expiration (expiration_date, status_id),
    INDEX idx_license_number_state (license_number, license_state_id)
);
```

---

## 4. Business Logic Requirements

### License Type Factor Calculation
```php
class DriverLicenseTypeService
{
    public function calculateLicenseTypeFactor(DriverLicenseData $licenseData): LicenseTypeFactor
    {
        // 1. Get base classification factor
        $classification = $this->classifyLicenseType(
            $licenseData->license_class, 
            $licenseData->license_state
        );
        
        $baseFactor = $classification->base_factor;
        
        // 2. Apply years licensed experience adjustment
        $experienceFactor = $this->calculateExperienceAdjustment(
            $licenseData->years_licensed, 
            $classification
        );
        
        // 3. Apply endorsement/restriction modifiers
        $modifierFactor = $this->calculateEndorsementModifiers(
            $licenseData->endorsements, 
            $licenseData->restrictions
        );
        
        // 4. Apply status adjustments (expired, suspended, etc.)
        $statusFactor = $this->calculateStatusAdjustment($licenseData->license_status);
        
        // 5. Calculate final factor
        $finalFactor = $baseFactor * $experienceFactor * $modifierFactor * $statusFactor;
        
        return new LicenseTypeFactor([
            'driver_id' => $licenseData->driver_id,
            'base_factor' => $baseFactor,
            'experience_factor' => $experienceFactor,
            'modifier_factor' => $modifierFactor,
            'status_factor' => $statusFactor,
            'final_factor' => $finalFactor,
            'classification' => $classification,
            'years_licensed' => $licenseData->years_licensed
        ]);
    }
    
    private function calculateExperienceAdjustment(int $yearsLicensed, LicenseTypeClassification $classification): float
    {
        // Experience-based factor adjustments
        if ($yearsLicensed < 1) {
            return 1.2500; // 25% surcharge for new drivers
        } elseif ($yearsLicensed < 3) {
            return 1.1000; // 10% surcharge for inexperienced drivers
        } elseif ($yearsLicensed >= 10) {
            return 0.9500; // 5% discount for experienced drivers
        }
        
        return 1.0000; // No adjustment for moderate experience
    }
    
    private function calculateEndorsementModifiers(array $endorsements, array $restrictions): float
    {
        $totalModifier = 1.0000;
        
        // Apply endorsement factors (typically favorable)
        foreach ($endorsements as $endorsementCode) {
            $endorsement = DB::table('license_endorsement_restriction')
                ->where('endorsement_code', $endorsementCode)
                ->where('endorsement_type', 'ENDORSEMENT')
                ->where('status_id', Status::ACTIVE)
                ->first();
                
            if ($endorsement) {
                $totalModifier *= $endorsement->factor_modifier;
            }
        }
        
        // Apply restriction factors (typically unfavorable)
        foreach ($restrictions as $restrictionCode) {
            $restriction = DB::table('license_endorsement_restriction')
                ->where('endorsement_code', $restrictionCode)
                ->where('endorsement_type', 'RESTRICTION')
                ->where('status_id', Status::ACTIVE)
                ->first();
                
            if ($restriction) {
                $totalModifier *= $restriction->factor_modifier;
            }
        }
        
        return $totalModifier;
    }
}
```

### License Status Validation
```php
class LicenseVerificationService
{
    public function validateLicenseEligibility(DriverLicenseData $licenseData): ValidationResult
    {
        $result = new ValidationResult();
        
        // 1. Check license expiration
        if ($licenseData->expiration_date && $licenseData->expiration_date < now()) {
            $result->addError('Driver license is expired');
        }
        
        // 2. Check license suspension/revocation
        if (in_array($licenseData->license_status, ['SUSPENDED', 'REVOKED', 'CANCELLED'])) {
            $result->addError("Driver license is {$licenseData->license_status}");
        }
        
        // 3. Validate minimum age requirements
        $minAge = $this->getMinimumAgeForLicenseType($licenseData->license_class);
        if ($licenseData->driver_age < $minAge) {
            $result->addError("Driver age {$licenseData->driver_age} below minimum {$minAge} for license type");
        }
        
        // 4. Check ineligible restrictions
        foreach ($licenseData->restrictions as $restrictionCode) {
            $restriction = DB::table('license_endorsement_restriction')
                ->where('endorsement_code', $restrictionCode)
                ->where('eligibility_impact', 'INELIGIBLE')
                ->first();
                
            if ($restriction) {
                $result->addError("License restriction {$restrictionCode} makes driver ineligible");
            }
        }
        
        return $result;
    }
}
```

### Aguila Dorada License Factor Matrix
```sql
-- License type factors for Aguila Dorada program
INSERT INTO driver_license_factor (program_id, classification_id, years_licensed_min, years_licensed_max, factor_value, effective_date) VALUES
-- Standard Valid License factors by experience
(1, (SELECT id FROM license_type_classification WHERE classification_code = 'STANDARD_VALID'), 0, 0, 1.2500, '2025-07-15'), -- New drivers
(1, (SELECT id FROM license_type_classification WHERE classification_code = 'STANDARD_VALID'), 1, 2, 1.1000, '2025-07-15'), -- 1-2 years
(1, (SELECT id FROM license_type_classification WHERE classification_code = 'STANDARD_VALID'), 3, 9, 1.0000, '2025-07-15'), -- 3-9 years
(1, (SELECT id FROM license_type_classification WHERE classification_code = 'STANDARD_VALID'), 10, NULL, 0.9500, '2025-07-15'), -- 10+ years

-- Commercial License factors (generally favorable)
(1, (SELECT id FROM license_type_classification WHERE classification_code = 'COMMERCIAL_CDL'), 0, 2, 0.9500, '2025-07-15'), -- New CDL
(1, (SELECT id FROM license_type_classification WHERE classification_code = 'COMMERCIAL_CDL'), 3, NULL, 0.9000, '2025-07-15'), -- Experienced CDL

-- High-risk license types
(1, (SELECT id FROM license_type_classification WHERE classification_code = 'LEARNER_PERMIT'), 0, NULL, 1.7500, '2025-07-15'),
(1, (SELECT id FROM license_type_classification WHERE classification_code = 'INTERNATIONAL'), 0, NULL, 1.4000, '2025-07-15'),
(1, (SELECT id FROM license_type_classification WHERE classification_code = 'STANDARD_EXPIRED'), 0, NULL, 1.2500, '2025-07-15'),

-- Ineligible or very high risk
(1, (SELECT id FROM license_type_classification WHERE classification_code = 'NO_LICENSE'), 0, NULL, 2.0000, '2025-07-15'),
(1, (SELECT id FROM license_type_classification WHERE classification_code = 'SUSPENDED_LICENSE'), 0, NULL, 3.0000, '2025-07-15');
```

---

## 5. API Integration Requirements

### License Type Endpoints
```php
// Driver license type API endpoints
GET /api/v1/rating/license-types
// Returns available license type classifications

POST /api/v1/rating/license-type/calculate
{
    "driver_license_data": {
        "license_number": "TX123456789",
        "license_state": "TX",
        "license_class": "C",
        "issue_date": "2020-03-15",
        "expiration_date": "2028-03-15",
        "first_licensed_date": "2015-03-15",
        "endorsements": ["MOTORCYCLE_ENDORSEMENT"],
        "restrictions": ["CORRECTIVE_LENSES"],
        "license_status": "VALID"
    }
}

POST /api/v1/rating/license-type/verify
{
    "license_number": "TX123456789",
    "license_state": "TX",
    "driver_date_of_birth": "1990-05-15"
}
// Verify license through state DMV systems

GET /api/v1/rating/license-type/breakdown/{driverId}
// Get detailed license type factor breakdown
```

### Response Format
```json
{
    "driver_id": 12345,
    "license_type_factor": 1.0450,
    "factor_breakdown": {
        "base_classification": {
            "classification_code": "STANDARD_VALID",
            "classification_name": "Standard Valid License",
            "risk_level": "STANDARD",
            "base_factor": 1.0000
        },
        "experience_adjustment": {
            "years_licensed": 10,
            "experience_factor": 0.9500,
            "adjustment_reason": "10+ years experience discount"
        },
        "endorsements": [
            {
                "endorsement_code": "MOTORCYCLE_ENDORSEMENT",
                "factor_modifier": 1.0000,
                "impact": "No rating impact"
            }
        ],
        "restrictions": [
            {
                "restriction_code": "CORRECTIVE_LENSES",
                "factor_modifier": 1.0000,
                "impact": "No rating impact"
            }
        ],
        "status_adjustment": {
            "license_status": "VALID",
            "status_factor": 1.0000
        }
    },
    "verification_status": {
        "license_verified": true,
        "verification_date": "2025-07-15",
        "verification_method": "DMV_API"
    },
    "eligibility": {
        "eligible": true,
        "restrictions": [],
        "warnings": []
    }
}
```

---

## 6. Performance Requirements

### License Factor Caching
```php
class DriverLicenseTypeService
{
    public function calculateLicenseTypeFactor(DriverLicenseData $licenseData): LicenseTypeFactor
    {
        // Cache license factor calculations
        $cacheKey = "license_factor_{$licenseData->driver_id}_{$licenseData->license_number}";
        
        return Cache::remember($cacheKey, 3600, function() use ($licenseData) {
            return $this->performLicenseFactorCalculation($licenseData);
        });
    }
}
```

### Database Performance
```sql
-- License factor lookup optimization
CREATE INDEX idx_license_factor_lookup 
ON driver_license_factor (
    program_id, 
    classification_id, 
    years_licensed_min, 
    years_licensed_max,
    effective_date
) WHERE status_id = 1;

-- License history lookup optimization
CREATE INDEX idx_driver_current_license 
ON driver_license_history (
    driver_id, 
    effective_date, 
    verification_status
) WHERE end_date IS NULL AND status_id = 1;
```

---

## 7. Testing Requirements

### License Type Factor Testing
```php
class DriverLicenseTypeServiceTest extends TestCase
{
    public function test_standard_license_experienced_driver()
    {
        $licenseData = new DriverLicenseData([
            'license_class' => 'C',
            'license_state' => 'TX',
            'years_licensed' => 12,
            'license_status' => 'VALID',
            'endorsements' => [],
            'restrictions' => []
        ]);
        
        $factor = $this->licenseTypeService->calculateLicenseTypeFactor($licenseData);
        
        $this->assertEquals(0.95, $factor->final_factor); // Experienced driver discount
    }
    
    public function test_commercial_license_factor()
    {
        $licenseData = new DriverLicenseData([
            'license_class' => 'CDL-A',
            'license_state' => 'TX',
            'years_licensed' => 5,
            'license_status' => 'VALID',
            'endorsements' => ['CDL_HAZMAT'],
            'restrictions' => []
        ]);
        
        $factor = $this->licenseTypeService->calculateLicenseTypeFactor($licenseData);
        
        $this->assertLessThan(1.0, $factor->final_factor); // CDL should be favorable
    }
    
    public function test_expired_license_surcharge()
    {
        $licenseData = new DriverLicenseData([
            'license_class' => 'C',
            'license_state' => 'TX',
            'years_licensed' => 5,
            'license_status' => 'EXPIRED',
            'expiration_date' => Carbon::now()->subMonths(2)
        ]);
        
        $factor = $this->licenseTypeService->calculateLicenseTypeFactor($licenseData);
        
        $this->assertGreaterThan(1.0, $factor->final_factor); // Expired license surcharge
    }
}
```

---

## Implementation Priority: MEDIUM
This factor provides important risk assessment based on license types and should be implemented after core driver factors.

## Dependencies
- **Driver Class Factor**: License factors complement demographic factors
- **MVR Integration**: License verification through state systems

## Estimated Implementation Effort
- **Database Schema**: 3 days
- **Service Layer**: 4 days
- **Verification Integration**: 3 days
- **API Integration**: 2 days
- **Testing**: 3 days
- **Total**: 15 days

This plan implements comprehensive license type risk assessment while maintaining proper verification and validation standards for accurate driver risk evaluation.