# Driver Class Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Driver Class  
**Category**: Core Rating Component  
**Priority**: High - Demographic risk assessment foundation  
**Implementation Complexity**: Medium  

### Business Requirements Summary
The Driver Class factor implements a comprehensive three-dimensional rating matrix based on driver age, gender, and marital status. This factor provides risk-based pricing that ranges from significant discounts (22% for married females 30+) to substantial surcharges (160% for single males 16-17), reflecting actuarial loss experience across demographic categories.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing and new Global Requirements:

#### Leverages GR-65: Rating Engine Architecture
**Integration**: Demographic factor calculation within multiplicative rating engine  
**Dependencies**: RatingEngineService for age/gender/marital status factor lookup

#### New Requirement: GR-72: Demographic Rating Standards
**Priority**: High  
**Rationale**: Age, gender, and marital status rating standards with regulatory compliance  

**Core Components**:
- Demographic data validation and verification standards
- Age calculation and birthday rule implementation
- Gender classification and documentation requirements
- Marital status verification and change management
- Anti-discrimination compliance for demographic rating

#### Leverages GR-04: Validation & Data Handling
**Integration**: Driver demographic validation patterns  
**Dependencies**: Age range validation, gender classification rules

### Integration with Existing Global Requirements
- **GR-41**: Table Schema Requirements - Driver class factor table structures
- **GR-20**: Application Business Logic - Demographic calculation service patterns
- **GR-53**: DCS Integration Architecture - Driver verification data integration

---

## 2. Service Architecture Requirements

### Demographic Rating Services

#### DriverClassService
**Purpose**: Driver demographic factor calculation and validation  
**Location**: `app/Domain/Rating/Services/DriverClassService.php`

**Key Methods**:
```php
class DriverClassService
{
    public function calculateDriverClassFactor(DriverDemographics $demographics): DriverClassFactor
    {
        // 1. Validate driver demographic data
        // 2. Calculate age as of policy effective date
        // 3. Determine gender classification
        // 4. Verify marital status category
        // 5. Lookup factor from three-dimensional matrix
        // 6. Return factor with demographic breakdown
    }
    
    public function validateDriverDemographics(DriverDemographics $demographics): ValidationResult
    {
        // Validate age, gender, and marital status combinations
    }
    
    public function calculateAgeAtEffectiveDate(Carbon $birthDate, Carbon $effectiveDate): int
    {
        // Calculate driver age with proper date handling
    }
}
```

#### DemographicVerificationService
**Purpose**: Driver demographic data verification and validation  
**Location**: `app/Domain/Rating/Services/DemographicVerificationService.php`

**Key Methods**:
```php
class DemographicVerificationService
{
    public function verifyDriverAge(Carbon $birthDate, string $licenseNumber): VerificationResult
    {
        // Verify age against driver's license data
    }
    
    public function verifyMaritalStatus(int $driverId, string $maritalStatus): VerificationResult
    {
        // Verify marital status with documentation requirements
    }
    
    public function validateGenderClassification(string $gender): ValidationResult
    {
        // Validate gender classification against license data
    }
}
```

---

## 3. Database Schema Requirements

### Driver Class Factor Tables

#### driver_class_dimension
```sql
CREATE TABLE driver_class_dimension (
    id BIGINT PRIMARY KEY,
    dimension_code VARCHAR(50) UNIQUE NOT NULL,
    dimension_name VARCHAR(255) NOT NULL,
    dimension_type ENUM('AGE', 'GENDER', 'MARITAL_STATUS') NOT NULL,
    validation_rules JSON,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_dimension_type (dimension_type, status_id)
);

-- Initialize core dimensions
INSERT INTO driver_class_dimension (dimension_code, dimension_name, dimension_type) VALUES
('AGE_CATEGORY', 'Age Category', 'AGE'),
('GENDER', 'Gender', 'GENDER'),
('MARITAL_STATUS', 'Marital Status', 'MARITAL_STATUS');
```

#### driver_class_age_category
```sql
CREATE TABLE driver_class_age_category (
    id BIGINT PRIMARY KEY,
    category_code VARCHAR(50) UNIQUE NOT NULL,
    category_name VARCHAR(255) NOT NULL,
    min_age INT NOT NULL,
    max_age INT, -- NULL for open-ended ranges
    display_order INT DEFAULT 0,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_age_range (min_age, max_age),
    INDEX idx_display_order (display_order, status_id)
);

-- Aguila Dorada age categories
INSERT INTO driver_class_age_category (category_code, category_name, min_age, max_age, display_order) VALUES
('AGE_16_17', '16-17 years', 16, 17, 1),
('AGE_18_20', '18-20 years', 18, 20, 2),
('AGE_21_24', '21-24 years', 21, 24, 3),
('AGE_25_29', '25-29 years', 25, 29, 4),
('AGE_30_PLUS', '30+ years', 30, NULL, 5);
```

#### driver_class_factor
```sql
CREATE TABLE driver_class_factor (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    age_category_id BIGINT NOT NULL,
    gender ENUM('M', 'F') NOT NULL,
    marital_status ENUM('SINGLE', 'MARRIED') NOT NULL,
    factor_value DECIMAL(6,4) NOT NULL, -- 0.7800 to 2.6000
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
    FOREIGN KEY (age_category_id) REFERENCES driver_class_age_category(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_driver_class_factor (
        program_id, 
        age_category_id, 
        gender, 
        marital_status, 
        effective_date
    ),
    INDEX idx_program_factors (program_id, effective_date),
    INDEX idx_demographic_lookup (age_category_id, gender, marital_status),
    INDEX idx_effective_dates (effective_date, expiration_date)
);
```

### Driver Demographic Tracking

#### driver_demographic_history
```sql
CREATE TABLE driver_demographic_history (
    id BIGINT PRIMARY KEY,
    driver_id BIGINT NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('M', 'F') NOT NULL,
    marital_status ENUM('SINGLE', 'MARRIED', 'DIVORCED', 'WIDOWED', 'SEPARATED') NOT NULL,
    verification_status ENUM('PENDING', 'VERIFIED', 'FAILED') NOT NULL,
    verification_method VARCHAR(100),
    verification_date DATE,
    documentation_type VARCHAR(100),
    effective_date DATE NOT NULL,
    expiration_date DATE,
    change_reason VARCHAR(255),
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (driver_id) REFERENCES driver(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_driver_demographics (driver_id, effective_date),
    INDEX idx_verification_status (verification_status, verification_date),
    INDEX idx_demographic_changes (driver_id, change_reason, effective_date)
);
```

---

## 4. Business Logic Requirements

### Age Category Determination
```php
class DriverClassService
{
    public function determineAgeCategory(Carbon $birthDate, Carbon $effectiveDate): string
    {
        $age = $this->calculateAgeAtEffectiveDate($birthDate, $effectiveDate);
        
        // Age category logic based on Aguila Dorada interpretation
        if ($age >= 16 && $age <= 17) {
            return 'AGE_16_17';
        } elseif ($age >= 18 && $age <= 20) {
            return 'AGE_18_20';
        } elseif ($age >= 21 && $age <= 24) {
            return 'AGE_21_24';
        } elseif ($age >= 25 && $age <= 29) {
            return 'AGE_25_29';
        } elseif ($age >= 30) {
            return 'AGE_30_PLUS';
        } else {
            throw new InvalidAgeException("Driver age {$age} is below minimum age requirement");
        }
    }
    
    public function calculateAgeAtEffectiveDate(Carbon $birthDate, Carbon $effectiveDate): int
    {
        // Calculate age as of policy effective date
        return $birthDate->diffInYears($effectiveDate);
    }
}
```

### Marital Status Processing
```php
class DriverClassService
{
    public function normalizeMaritalStatus(string $maritalStatus): string
    {
        // Normalize marital status to binary classification for rating
        $normalized = strtoupper(trim($maritalStatus));
        
        switch ($normalized) {
            case 'MARRIED':
                return 'MARRIED';
            case 'SINGLE':
            case 'DIVORCED':
            case 'WIDOWED':
            case 'SEPARATED':
            case 'NEVER_MARRIED':
                return 'SINGLE';
            default:
                throw new InvalidMaritalStatusException("Invalid marital status: {$maritalStatus}");
        }
    }
}
```

### Aguila Dorada Factor Matrix
```sql
-- Complete driver class factor matrix for Aguila Dorada program
-- All factors from the interpretation document

-- Single Male Drivers
INSERT INTO driver_class_factor (program_id, age_category_id, gender, marital_status, factor_value, effective_date) VALUES
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_16_17'), 'M', 'SINGLE', 2.6000, '2025-07-15'),
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_18_20'), 'M', 'SINGLE', 2.2500, '2025-07-15'),
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_21_24'), 'M', 'SINGLE', 1.8500, '2025-07-15'),
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_25_29'), 'M', 'SINGLE', 1.4500, '2025-07-15'),
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_30_PLUS'), 'M', 'SINGLE', 1.0000, '2025-07-15'),

-- Married Male Drivers
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_16_17'), 'M', 'MARRIED', 1.8000, '2025-07-15'),
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_18_20'), 'M', 'MARRIED', 1.5500, '2025-07-15'),
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_21_24'), 'M', 'MARRIED', 1.2500, '2025-07-15'),
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_25_29'), 'M', 'MARRIED', 1.0500, '2025-07-15'),
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_30_PLUS'), 'M', 'MARRIED', 0.8500, '2025-07-15'),

-- Single Female Drivers
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_16_17'), 'F', 'SINGLE', 2.2500, '2025-07-15'),
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_18_20'), 'F', 'SINGLE', 1.9500, '2025-07-15'),
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_21_24'), 'F', 'SINGLE', 1.6500, '2025-07-15'),
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_25_29'), 'F', 'SINGLE', 1.2500, '2025-07-15'),
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_30_PLUS'), 'F', 'SINGLE', 0.8500, '2025-07-15'),

-- Married Female Drivers
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_16_17'), 'F', 'MARRIED', 1.6500, '2025-07-15'),
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_18_20'), 'F', 'MARRIED', 1.3500, '2025-07-15'),
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_21_24'), 'F', 'MARRIED', 1.1500, '2025-07-15'),
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_25_29'), 'F', 'MARRIED', 0.9500, '2025-07-15'),
(1, (SELECT id FROM driver_class_age_category WHERE category_code = 'AGE_30_PLUS'), 'F', 'MARRIED', 0.7800, '2025-07-15');
```

---

## 5. Validation Requirements

### Demographic Data Validation
```php
class DriverDemographicsValidator
{
    public function validateDriverAge(Carbon $birthDate, Carbon $effectiveDate): ValidationResult
    {
        $result = new ValidationResult();
        $age = $birthDate->diffInYears($effectiveDate);
        
        // Texas minimum driving age validation
        if ($age < 16) {
            $result->addError("Driver age {$age} is below Texas minimum driving age of 16");
        }
        
        // Maximum reasonable age validation
        if ($age > 100) {
            $result->addWarning("Driver age {$age} exceeds typical range, please verify");
        }
        
        // Future birth date validation
        if ($birthDate->isAfter($effectiveDate)) {
            $result->addError("Birth date cannot be after policy effective date");
        }
        
        return $result;
    }
    
    public function validateGender(string $gender): ValidationResult
    {
        $result = new ValidationResult();
        $validGenders = ['M', 'F', 'MALE', 'FEMALE'];
        
        if (!in_array(strtoupper($gender), $validGenders)) {
            $result->addError("Invalid gender classification: {$gender}");
        }
        
        return $result;
    }
    
    public function validateMaritalStatus(string $maritalStatus): ValidationResult
    {
        $result = new ValidationResult();
        $validStatuses = ['SINGLE', 'MARRIED', 'DIVORCED', 'WIDOWED', 'SEPARATED'];
        
        if (!in_array(strtoupper($maritalStatus), $validStatuses)) {
            $result->addError("Invalid marital status: {$maritalStatus}");
        }
        
        return $result;
    }
}
```

### Documentation Requirements
```php
class DemographicDocumentationValidator
{
    public function validateAgeVerification(DriverDemographics $demographics): ValidationResult
    {
        $result = new ValidationResult();
        
        // Driver's license verification for age
        if (!$demographics->hasDriversLicense()) {
            $result->addError("Driver's license required for age verification");
        }
        
        // Age consistency check with license
        if ($demographics->hasDriversLicense()) {
            $licenseAge = $this->extractAgeFromLicense($demographics->driversLicense);
            $providedAge = $demographics->age;
            
            if (abs($licenseAge - $providedAge) > 1) {
                $result->addError("Age inconsistency between provided age and driver's license");
            }
        }
        
        return $result;
    }
    
    public function validateMaritalStatusDocumentation(DriverDemographics $demographics): ValidationResult
    {
        $result = new ValidationResult();
        
        // Marriage certificate required for married discount
        if ($demographics->maritalStatus === 'MARRIED' && !$demographics->hasMarriageCertificate()) {
            $result->addError("Marriage certificate required for married driver discount");
        }
        
        return $result;
    }
}
```

---

## 6. API Integration Requirements

### Driver Class Calculation Endpoints
```php
// Driver class factor endpoints
POST /api/v1/rating/driver-class/calculate
{
    "driver_demographics": {
        "date_of_birth": "1990-05-15",
        "gender": "M",
        "marital_status": "MARRIED"
    },
    "policy_effective_date": "2025-07-15"
}

GET /api/v1/rating/driver-class/factors/{programId}
// Returns complete driver class factor matrix

POST /api/v1/rating/driver-class/validate
{
    "demographics": {...}
}
// Validate driver demographic data

GET /api/v1/rating/driver-class/breakdown/{driverId}
// Get detailed driver class factor breakdown
```

### Response Format
```json
{
    "driver_id": 12345,
    "factor_value": 1.2500,
    "surcharge_percentage": 25.0,
    "demographic_breakdown": {
        "age": {
            "birth_date": "1990-05-15",
            "age_at_effective_date": 35,
            "age_category": "AGE_30_PLUS"
        },
        "gender": {
            "classification": "M",
            "verified": true
        },
        "marital_status": {
            "status": "MARRIED",
            "verified": true,
            "documentation_provided": true
        }
    },
    "factor_details": {
        "category_combination": "Male, 30+, Married",
        "risk_level": "LOW",
        "discount_applied": true
    }
}
```

---

## 7. Performance Optimization

### Factor Lookup Caching
```php
class DriverClassService
{
    public function calculateDriverClassFactor(DriverDemographics $demographics): DriverClassFactor
    {
        // Create cache key from demographic combination
        $cacheKey = "driver_class_{$this->programId}_" . 
                   md5("{$demographics->ageCategory}_{$demographics->gender}_{$demographics->maritalStatus}");
        
        return Cache::remember($cacheKey, 3600, function() use ($demographics) {
            return $this->lookupDriverClassFactor($demographics);
        });
    }
}
```

### Database Performance
```sql
-- Optimized driver class factor lookup
CREATE INDEX idx_driver_class_lookup_optimized 
ON driver_class_factor (
    program_id, 
    age_category_id, 
    gender, 
    marital_status,
    effective_date
) WHERE status_id = 1;

-- Age category lookup optimization
CREATE INDEX idx_age_category_range 
ON driver_class_age_category (min_age, max_age, status_id);
```

---

## 8. Testing Requirements

### Factor Calculation Testing
```php
class DriverClassServiceTest extends TestCase
{
    public function test_highest_risk_factor()
    {
        // Test highest risk: Single Male 16-17
        $demographics = new DriverDemographics([
            'date_of_birth' => Carbon::parse('2008-01-01'),
            'gender' => 'M',
            'marital_status' => 'SINGLE'
        ]);
        
        $factor = $this->driverClassService->calculateDriverClassFactor($demographics);
        
        $this->assertEquals(2.60, $factor->factor_value);
        $this->assertEquals(160, $factor->surcharge_percentage);
    }
    
    public function test_lowest_risk_factor()
    {
        // Test lowest risk: Married Female 30+
        $demographics = new DriverDemographics([
            'date_of_birth' => Carbon::parse('1990-01-01'),
            'gender' => 'F',
            'marital_status' => 'MARRIED'
        ]);
        
        $factor = $this->driverClassService->calculateDriverClassFactor($demographics);
        
        $this->assertEquals(0.78, $factor->factor_value);
        $this->assertEquals(-22, $factor->discount_percentage);
    }
    
    public function test_age_calculation_accuracy()
    {
        // Test age calculation on birthday
        $birthDate = Carbon::parse('1990-07-15');
        $effectiveDate = Carbon::parse('2025-07-15'); // Exactly 35 years
        
        $age = $this->driverClassService->calculateAgeAtEffectiveDate($birthDate, $effectiveDate);
        
        $this->assertEquals(35, $age);
    }
}
```

---

## 9. Regulatory Compliance

### Anti-Discrimination Compliance
- **Age Discrimination**: Factors based on actuarial data and regulatory approval
- **Gender Discrimination**: Compliance with state regulations on gender-based rating
- **Marital Status**: Legitimate actuarial basis for marital status factors
- **Documentation**: Complete actuarial justification for all demographic factors

### Texas Insurance Regulations
- **Factor Range Limits**: All factors within Texas-approved ranges
- **Rate Filing Compliance**: Factors match regulatory filing submissions
- **Actuarial Support**: Statistical justification for all demographic categories
- **Periodic Review**: Regular validation of factor effectiveness and fairness

---

## Implementation Priority: HIGH
This factor is essential for competitive risk-based pricing and must be implemented early in the rating system development.

## Dependencies
- **Algorithm Factor**: Requires core rating engine for factor calculation
- **Vehicle Base Rates**: Driver class factors multiply against base rates

## Estimated Implementation Effort
- **Database Schema**: 3 days
- **Service Layer**: 4 days
- **Validation Logic**: 3 days
- **API Integration**: 2 days
- **Testing**: 3 days
- **Total**: 15 days

This plan implements comprehensive demographic rating while maintaining regulatory compliance and providing the risk-based pricing differentials essential for competitive insurance pricing.