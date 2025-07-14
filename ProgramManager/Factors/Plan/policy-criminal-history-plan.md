# Policy Criminal History Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Policy Criminal History  
**Category**: Driver Factor  
**Priority**: Medium - Criminal background risk assessment  
**Implementation Complexity**: High  

### Business Requirements Summary
The Policy Criminal History factor implements risk-based pricing adjustments based on criminal background checks for policy drivers. This factor assesses non-traffic criminal convictions that may indicate increased risk for insurance fraud, claims patterns, or overall risk profile, while maintaining compliance with state regulations and anti-discrimination requirements.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing and new Global Requirements:

#### Leverages GR-73: Motor Vehicle Record Integration
**Integration**: Criminal history verification through background check systems  
**Dependencies**: Multi-state criminal database integration and verification standards

#### New Requirement: GR-80: Criminal Background Assessment Standards
**Priority**: Medium  
**Rationale**: Criminal history evaluation standards with regulatory compliance  

**Core Components**:
- Criminal conviction classification and severity assessment
- Background check integration and verification methodology
- Regulatory compliance for criminal history use in insurance
- Anti-discrimination compliance and protected class considerations
- Data retention and privacy requirements for criminal history
- Criminal history factor assignment and risk correlation standards

#### New Requirement: GR-81: Insurance Fraud Risk Assessment
**Priority**: Medium  
**Rationale**: Fraud risk evaluation standards based on criminal history patterns  

**Core Components**:
- Fraud risk correlation methodology for criminal history types
- Insurance-specific criminal conviction evaluation
- Financial crime and fraud conviction impact assessment
- Risk mitigation strategies for high-risk criminal backgrounds

### Integration with Existing Global Requirements
- **GR-65**: Rating Engine Architecture - Criminal history factor integration
- **GR-24**: Data Security - Sensitive criminal data protection requirements
- **GR-04**: Validation & Data Handling - Background check validation patterns

---

## 2. Service Architecture Requirements

### Criminal History Assessment Services

#### CriminalHistoryService
**Purpose**: Criminal background assessment and factor determination  
**Location**: `app/Domain/Rating/Services/CriminalHistoryService.php`

**Key Methods**:
```php
class CriminalHistoryService
{
    public function calculateCriminalHistoryFactor(DriverCriminalData $criminalData): CriminalHistoryFactor
    {
        // 1. Classify criminal convictions by type and severity
        // 2. Apply lookback period restrictions (7-year standard)
        // 3. Calculate risk factors based on conviction patterns
        // 4. Apply regulatory compliance filters
        // 5. Return factor with detailed breakdown and justification
    }
    
    public function assessFraudRisk(array $criminalConvictions): FraudRiskAssessment
    {
        // Assess insurance fraud risk based on criminal history patterns
    }
    
    public function validateRegulatoryCompliance(CriminalHistoryFactor $factor): ValidationResult
    {
        // Validate criminal history use complies with state regulations
    }
}
```

#### BackgroundCheckService
**Purpose**: Criminal background verification and data integration  
**Location**: `app/Domain/Rating/Services/BackgroundCheckService.php`

**Key Methods**:
```php
class BackgroundCheckService
{
    public function performBackgroundCheck(DriverIdentityData $identityData): BackgroundCheckResult
    {
        // Perform comprehensive criminal background check
    }
    
    public function verifyConvictionDetails(CriminalConviction $conviction): ConvictionVerification
    {
        // Verify conviction details through court records
    }
    
    public function normalizeConvictionData(array $backgroundData): Collection
    {
        // Normalize criminal data from multiple background check sources
    }
}
```

---

## 3. Database Schema Requirements

### Criminal History Management Tables

#### criminal_conviction_type
```sql
CREATE TABLE criminal_conviction_type (
    id BIGINT PRIMARY KEY,
    conviction_code VARCHAR(50) UNIQUE NOT NULL,
    conviction_name VARCHAR(255) NOT NULL,
    conviction_description TEXT,
    conviction_category ENUM('FELONY', 'MISDEMEANOR', 'VIOLATION', 'INFRACTION') NOT NULL,
    crime_type ENUM('VIOLENT', 'PROPERTY', 'FINANCIAL', 'DRUG', 'TRAFFIC', 'OTHER') NOT NULL,
    severity_level ENUM('LOW', 'MODERATE', 'HIGH', 'SEVERE') NOT NULL,
    insurance_relevance ENUM('HIGH', 'MODERATE', 'LOW', 'NONE') NOT NULL,
    fraud_risk_indicator BOOLEAN DEFAULT FALSE,
    base_factor DECIMAL(6,4) NOT NULL DEFAULT 1.0000,
    lookback_years INT NOT NULL DEFAULT 7,
    affects_eligibility BOOLEAN DEFAULT FALSE,
    requires_underwriting_review BOOLEAN DEFAULT FALSE,
    regulatory_notes TEXT,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_conviction_category (conviction_category, crime_type),
    INDEX idx_severity_level (severity_level, insurance_relevance),
    INDEX idx_fraud_indicator (fraud_risk_indicator, status_id),
    INDEX idx_eligibility_impact (affects_eligibility, status_id)
);

-- Criminal conviction type classifications
INSERT INTO criminal_conviction_type (conviction_code, conviction_name, conviction_category, crime_type, severity_level, insurance_relevance, fraud_risk_indicator, base_factor, affects_eligibility) VALUES
-- Financial crimes (high insurance relevance)
('INSURANCE_FRAUD', 'Insurance Fraud', 'FELONY', 'FINANCIAL', 'SEVERE', 'HIGH', TRUE, 3.0000, TRUE),
('IDENTITY_THEFT', 'Identity Theft', 'FELONY', 'FINANCIAL', 'HIGH', 'HIGH', TRUE, 2.5000, TRUE),
('CREDIT_CARD_FRAUD', 'Credit Card Fraud', 'FELONY', 'FINANCIAL', 'HIGH', 'HIGH', TRUE, 2.0000, FALSE),
('CHECK_FRAUD', 'Check Fraud', 'MISDEMEANOR', 'FINANCIAL', 'MODERATE', 'MODERATE', TRUE, 1.5000, FALSE),
('EMBEZZLEMENT', 'Embezzlement', 'FELONY', 'FINANCIAL', 'HIGH', 'HIGH', TRUE, 2.2000, FALSE),

-- Property crimes (moderate insurance relevance)
('BURGLARY', 'Burglary', 'FELONY', 'PROPERTY', 'HIGH', 'MODERATE', FALSE, 1.7500, FALSE),
('THEFT', 'Theft/Larceny', 'MISDEMEANOR', 'PROPERTY', 'MODERATE', 'MODERATE', FALSE, 1.3000, FALSE),
('VANDALISM', 'Vandalism/Property Damage', 'MISDEMEANOR', 'PROPERTY', 'LOW', 'LOW', FALSE, 1.1000, FALSE),

-- Violent crimes (moderate insurance relevance for character assessment)
('ASSAULT', 'Assault', 'MISDEMEANOR', 'VIOLENT', 'MODERATE', 'MODERATE', FALSE, 1.4000, FALSE),
('DOMESTIC_VIOLENCE', 'Domestic Violence', 'MISDEMEANOR', 'VIOLENT', 'MODERATE', 'MODERATE', FALSE, 1.3000, FALSE),

-- Drug crimes (low insurance relevance unless driving-related)
('DRUG_POSSESSION', 'Drug Possession', 'MISDEMEANOR', 'DRUG', 'LOW', 'LOW', FALSE, 1.1000, FALSE),
('DRUG_TRAFFICKING', 'Drug Trafficking', 'FELONY', 'DRUG', 'HIGH', 'MODERATE', FALSE, 1.6000, FALSE),

-- Traffic-related crimes (covered by separate traffic violation factors)
('HIT_AND_RUN', 'Hit and Run', 'FELONY', 'TRAFFIC', 'HIGH', 'HIGH', FALSE, 2.5000, TRUE),
('VEHICULAR_HOMICIDE', 'Vehicular Homicide', 'FELONY', 'TRAFFIC', 'SEVERE', 'HIGH', FALSE, 5.0000, TRUE),

-- Minor violations (minimal insurance relevance)
('PUBLIC_INTOXICATION', 'Public Intoxication', 'MISDEMEANOR', 'OTHER', 'LOW', 'NONE', FALSE, 1.0000, FALSE),
('DISORDERLY_CONDUCT', 'Disorderly Conduct', 'MISDEMEANOR', 'OTHER', 'LOW', 'NONE', FALSE, 1.0000, FALSE);
```

#### driver_criminal_history
```sql
CREATE TABLE driver_criminal_history (
    id BIGINT PRIMARY KEY,
    driver_id BIGINT NOT NULL,
    conviction_type_id BIGINT NOT NULL,
    conviction_date DATE NOT NULL,
    court_jurisdiction VARCHAR(255),
    case_number VARCHAR(100),
    conviction_description TEXT,
    sentence_details TEXT,
    fine_amount DECIMAL(10,2),
    conviction_state_id BIGINT,
    affects_rating BOOLEAN DEFAULT TRUE,
    lookback_expiration_date DATE, -- When conviction expires for rating purposes
    background_check_source VARCHAR(100),
    background_check_date DATE,
    verification_status ENUM('PENDING', 'VERIFIED', 'DISPUTED', 'EXPIRED') NOT NULL,
    verification_notes TEXT,
    manual_override BOOLEAN DEFAULT FALSE,
    override_reason TEXT,
    privacy_restriction BOOLEAN DEFAULT FALSE, -- For sealed/expunged records
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (driver_id) REFERENCES driver(id),
    FOREIGN KEY (conviction_type_id) REFERENCES criminal_conviction_type(id),
    FOREIGN KEY (conviction_state_id) REFERENCES state(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_driver_criminal_history (driver_id, conviction_date),
    INDEX idx_rating_convictions (driver_id, affects_rating, lookback_expiration_date),
    INDEX idx_verification_status (verification_status, background_check_date),
    INDEX idx_conviction_type (conviction_type_id, conviction_date),
    INDEX idx_lookback_expiration (lookback_expiration_date, affects_rating)
);
```

#### criminal_history_factor
```sql
CREATE TABLE criminal_history_factor (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    conviction_type_id BIGINT NOT NULL,
    conviction_count_min INT NOT NULL DEFAULT 1,
    conviction_count_max INT, -- NULL for open-ended ranges
    years_since_conviction_min INT NOT NULL DEFAULT 0,
    years_since_conviction_max INT NOT NULL DEFAULT 7,
    factor_value DECIMAL(6,4) NOT NULL,
    eligibility_restriction BOOLEAN DEFAULT FALSE,
    underwriting_required BOOLEAN DEFAULT FALSE,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    actuarial_justification TEXT,
    regulatory_compliance_notes TEXT,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (conviction_type_id) REFERENCES criminal_conviction_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_criminal_history_factor (
        program_id, 
        conviction_type_id, 
        conviction_count_min, 
        conviction_count_max,
        years_since_conviction_min,
        years_since_conviction_max,
        effective_date
    ),
    INDEX idx_program_conviction_factors (program_id, conviction_type_id),
    INDEX idx_conviction_count_range (conviction_count_min, conviction_count_max),
    INDEX idx_years_since_range (years_since_conviction_min, years_since_conviction_max),
    INDEX idx_eligibility_factors (eligibility_restriction, underwriting_required)
);
```

---

## 4. Business Logic Requirements

### Criminal History Factor Calculation
```php
class CriminalHistoryService
{
    public function calculateCriminalHistoryFactor(DriverCriminalData $criminalData): CriminalHistoryFactor
    {
        $driverId = $criminalData->driver_id;
        $effectiveDate = $criminalData->effective_date;
        
        // 1. Get all relevant criminal convictions within lookback period
        $relevantConvictions = $this->getRelevantConvictions($driverId, $effectiveDate);
        
        if ($relevantConvictions->isEmpty()) {
            return new CriminalHistoryFactor([
                'driver_id' => $driverId,
                'factor_value' => 1.0000,
                'conviction_count' => 0,
                'risk_level' => 'CLEAN',
                'eligibility_impact' => 'NONE'
            ]);
        }
        
        // 2. Group convictions by type and calculate aggregate factors
        $convictionGroups = $relevantConvictions->groupBy('conviction_type_id');
        $totalFactor = 1.0000;
        $eligibilityRestrictions = [];
        $underwritingRequired = false;
        
        foreach ($convictionGroups as $convictionTypeId => $convictions) {
            $convictionType = DB::table('criminal_conviction_type')
                ->where('id', $convictionTypeId)
                ->first();
                
            // Calculate factor for this conviction type
            $typeFactor = $this->calculateConvictionTypeFactor(
                $convictionType, 
                $convictions, 
                $effectiveDate
            );
            
            $totalFactor *= $typeFactor->factor_value;
            
            if ($typeFactor->affects_eligibility) {
                $eligibilityRestrictions[] = $convictionType->conviction_name;
            }
            
            if ($typeFactor->requires_underwriting) {
                $underwritingRequired = true;
            }
        }
        
        // 3. Apply regulatory compliance caps and minimums
        $totalFactor = $this->applyRegulatoryLimits($totalFactor, $relevantConvictions);
        
        return new CriminalHistoryFactor([
            'driver_id' => $driverId,
            'factor_value' => $totalFactor,
            'conviction_count' => $relevantConvictions->count(),
            'conviction_breakdown' => $this->generateConvictionBreakdown($relevantConvictions),
            'risk_level' => $this->assessRiskLevel($totalFactor),
            'eligibility_restrictions' => $eligibilityRestrictions,
            'underwriting_required' => $underwritingRequired,
            'fraud_risk_score' => $this->calculateFraudRiskScore($relevantConvictions)
        ]);
    }
    
    private function getRelevantConvictions(int $driverId, Carbon $effectiveDate): Collection
    {
        return DB::table('driver_criminal_history')
            ->join('criminal_conviction_type', 'driver_criminal_history.conviction_type_id', '=', 'criminal_conviction_type.id')
            ->where('driver_criminal_history.driver_id', $driverId)
            ->where('driver_criminal_history.affects_rating', true)
            ->where('driver_criminal_history.verification_status', 'VERIFIED')
            ->where('driver_criminal_history.lookback_expiration_date', '>=', $effectiveDate)
            ->where('driver_criminal_history.privacy_restriction', false) // Exclude sealed/expunged
            ->where('criminal_conviction_type.insurance_relevance', '!=', 'NONE')
            ->where('driver_criminal_history.status_id', Status::ACTIVE)
            ->get();
    }
    
    private function calculateConvictionTypeFactor(
        object $convictionType, 
        Collection $convictions, 
        Carbon $effectiveDate
    ): ConvictionTypeFactor {
        $convictionCount = $convictions->count();
        $mostRecentConviction = $convictions->sortByDesc('conviction_date')->first();
        $yearsSinceConviction = $effectiveDate->diffInYears(Carbon::parse($mostRecentConviction->conviction_date));
        
        // Get factor from database based on count and years since conviction
        $factor = DB::table('criminal_history_factor')
            ->where('program_id', $this->programId)
            ->where('conviction_type_id', $convictionType->id)
            ->where('conviction_count_min', '<=', $convictionCount)
            ->where(function($query) use ($convictionCount) {
                $query->whereNull('conviction_count_max')
                      ->orWhere('conviction_count_max', '>=', $convictionCount);
            })
            ->where('years_since_conviction_min', '<=', $yearsSinceConviction)
            ->where('years_since_conviction_max', '>=', $yearsSinceConviction)
            ->where('effective_date', '<=', $effectiveDate)
            ->where(function($query) use ($effectiveDate) {
                $query->whereNull('expiration_date')
                      ->orWhere('expiration_date', '>', $effectiveDate);
            })
            ->where('status_id', Status::ACTIVE)
            ->first();
            
        return new ConvictionTypeFactor([
            'conviction_type' => $convictionType,
            'conviction_count' => $convictionCount,
            'years_since_conviction' => $yearsSinceConviction,
            'factor_value' => $factor->factor_value ?? $convictionType->base_factor,
            'affects_eligibility' => $factor->eligibility_restriction ?? false,
            'requires_underwriting' => $factor->underwriting_required ?? false
        ]);
    }
}
```

### Fraud Risk Assessment
```php
class FraudRiskAssessmentService
{
    public function calculateFraudRiskScore(Collection $convictions): FraudRiskScore
    {
        $riskScore = 0;
        $riskFactors = [];
        
        foreach ($convictions as $conviction) {
            // Insurance fraud convictions = highest risk
            if ($conviction->conviction_code === 'INSURANCE_FRAUD') {
                $riskScore += 100;
                $riskFactors[] = 'Previous insurance fraud conviction';
            }
            
            // Financial crimes = high risk
            if (in_array($conviction->conviction_code, ['IDENTITY_THEFT', 'CREDIT_CARD_FRAUD', 'EMBEZZLEMENT'])) {
                $riskScore += 50;
                $riskFactors[] = "Financial crime: {$conviction->conviction_name}";
            }
            
            // Multiple financial convictions = compounding risk
            $financialConvictions = $convictions->whereIn('crime_type', ['FINANCIAL'])->count();
            if ($financialConvictions > 1) {
                $riskScore += ($financialConvictions - 1) * 25;
                $riskFactors[] = "Multiple financial crime convictions ({$financialConvictions})";
            }
            
            // Recent convictions = higher risk
            $yearsSince = now()->diffInYears(Carbon::parse($conviction->conviction_date));
            if ($yearsSince <= 2) {
                $riskScore += 30;
                $riskFactors[] = "Recent conviction (within 2 years)";
            }
        }
        
        // Determine risk level
        $riskLevel = $this->determineRiskLevel($riskScore);
        
        return new FraudRiskScore([
            'risk_score' => $riskScore,
            'risk_level' => $riskLevel,
            'risk_factors' => $riskFactors,
            'requires_special_handling' => $riskScore >= 75,
            'recommended_actions' => $this->getRecommendedActions($riskLevel)
        ]);
    }
    
    private function determineRiskLevel(int $riskScore): string
    {
        if ($riskScore >= 100) {
            return 'EXTREME';
        } elseif ($riskScore >= 75) {
            return 'HIGH';
        } elseif ($riskScore >= 50) {
            return 'MODERATE';
        } elseif ($riskScore >= 25) {
            return 'LOW';
        } else {
            return 'MINIMAL';
        }
    }
}
```

---

## 5. Regulatory Compliance Requirements

### Anti-Discrimination Compliance
```php
class CriminalHistoryComplianceService
{
    public function validateRegulatoryCompliance(CriminalHistoryFactor $factor): ValidationResult
    {
        $result = new ValidationResult();
        
        // 1. Validate lookback period compliance (typically 7 years max)
        $this->validateLookbackPeriod($factor, $result);
        
        // 2. Validate conviction types are insurance-relevant
        $this->validateInsuranceRelevance($factor, $result);
        
        // 3. Validate protected class considerations
        $this->validateProtectedClassCompliance($factor, $result);
        
        // 4. Validate state-specific restrictions
        $this->validateStateRestrictions($factor, $result);
        
        return $result;
    }
    
    private function validateProtectedClassCompliance(CriminalHistoryFactor $factor, ValidationResult $result): void
    {
        // Ensure criminal history factors don't disproportionately impact protected classes
        
        // Check for convictions that may have disparate impact
        $protectedClassImpactConvictions = [
            'DRUG_POSSESSION',  // May disproportionately impact certain demographics
            'PUBLIC_INTOXICATION',
            'DISORDERLY_CONDUCT'
        ];
        
        foreach ($factor->conviction_breakdown as $conviction) {
            if (in_array($conviction->conviction_code, $protectedClassImpactConvictions)) {
                $result->addWarning(
                    "Conviction type {$conviction->conviction_code} may require disparate impact analysis"
                );
            }
        }
    }
    
    private function validateStateRestrictions(CriminalHistoryFactor $factor, ValidationResult $result): void
    {
        // Texas-specific criminal history restrictions
        
        // Texas prohibits use of certain conviction types
        $prohibitedInTexas = [
            'MARIJUANA_POSSESSION', // Texas has specific restrictions on marijuana convictions
        ];
        
        foreach ($factor->conviction_breakdown as $conviction) {
            if (in_array($conviction->conviction_code, $prohibitedInTexas)) {
                $result->addError(
                    "Conviction type {$conviction->conviction_code} prohibited for insurance rating in Texas"
                );
            }
        }
    }
}
```

### Data Privacy and Security
```php
class CriminalHistoryPrivacyService
{
    public function applyCriminalHistoryPrivacyControls(DriverCriminalData $criminalData): PrivacyControlledData
    {
        // 1. Mask sensitive details in stored data
        $maskedData = $this->maskSensitiveDetails($criminalData);
        
        // 2. Apply data retention policies
        $retentionPolicies = $this->applyRetentionPolicies($maskedData);
        
        // 3. Implement access controls
        $accessControls = $this->implementAccessControls($retentionPolicies);
        
        return new PrivacyControlledData($accessControls);
    }
    
    private function maskSensitiveDetails(DriverCriminalData $criminalData): DriverCriminalData
    {
        // Mask specific case details while preserving rating-relevant information
        $criminalData->case_number = $this->maskCaseNumber($criminalData->case_number);
        $criminalData->court_jurisdiction = $this->maskCourtDetails($criminalData->court_jurisdiction);
        $criminalData->sentence_details = null; // Remove sensitive sentence details
        
        return $criminalData;
    }
}
```

---

## 6. API Integration Requirements

### Criminal History Endpoints
```php
// Criminal history API endpoints
POST /api/v1/rating/criminal-history/calculate
{
    "driver_id": 12345,
    "effective_date": "2025-07-15",
    "include_fraud_assessment": true
}

POST /api/v1/rating/criminal-history/background-check
{
    "driver_identity": {
        "first_name": "John",
        "last_name": "Smith",
        "date_of_birth": "1990-05-15",
        "ssn_last_4": "1234",
        "previous_addresses": [...]
    },
    "check_scope": "COMPREHENSIVE"
}

GET /api/v1/rating/criminal-history/compliance-check/{driverId}
// Validate regulatory compliance for criminal history usage

POST /api/v1/admin/criminal-history/override
{
    "driver_id": 12345,
    "conviction_id": 67890,
    "override_type": "EXCLUDE_FROM_RATING",
    "justification": "Conviction sealed by court order"
}
```

### Response Format
```json
{
    "driver_id": 12345,
    "criminal_history_factor": 1.5000,
    "risk_assessment": {
        "risk_level": "MODERATE",
        "conviction_count": 2,
        "fraud_risk_score": {
            "score": 45,
            "level": "LOW",
            "factors": ["Financial crime conviction over 3 years old"]
        }
    },
    "conviction_breakdown": [
        {
            "conviction_type": "CHECK_FRAUD",
            "conviction_date": "2020-03-15",
            "years_since": 5,
            "factor_contribution": 1.3000,
            "affects_eligibility": false
        },
        {
            "conviction_type": "THEFT",
            "conviction_date": "2019-08-22",
            "years_since": 6,
            "factor_contribution": 1.1500,
            "affects_eligibility": false
        }
    ],
    "compliance_status": {
        "regulatory_compliant": true,
        "lookback_compliant": true,
        "protected_class_impact": "NONE",
        "state_restrictions": "NONE"
    },
    "underwriting_requirements": {
        "requires_review": false,
        "special_handling": false,
        "eligibility_restrictions": []
    }
}
```

---

## 7. Testing Requirements

### Criminal History Factor Testing
```php
class CriminalHistoryServiceTest extends TestCase
{
    public function test_clean_criminal_history()
    {
        $factor = $this->criminalHistoryService->calculateCriminalHistoryFactor(
            new DriverCriminalData(['driver_id' => $this->cleanDriverId])
        );
        
        $this->assertEquals(1.0000, $factor->factor_value);
        $this->assertEquals('CLEAN', $factor->risk_level);
        $this->assertEquals(0, $factor->conviction_count);
    }
    
    public function test_insurance_fraud_conviction()
    {
        $criminalData = new DriverCriminalData([
            'driver_id' => $this->fraudDriverId,
            'convictions' => [
                ['conviction_type' => 'INSURANCE_FRAUD', 'conviction_date' => '2022-01-15']
            ]
        ]);
        
        $factor = $this->criminalHistoryService->calculateCriminalHistoryFactor($criminalData);
        
        $this->assertGreaterThan(2.0, $factor->factor_value);
        $this->assertTrue($factor->underwriting_required);
        $this->assertContains('INSURANCE_FRAUD', $factor->eligibility_restrictions);
    }
    
    public function test_lookback_period_compliance()
    {
        $oldConviction = new DriverCriminalData([
            'driver_id' => $this->testDriverId,
            'convictions' => [
                ['conviction_type' => 'THEFT', 'conviction_date' => '2015-01-01'] // Over 7 years old
            ]
        ]);
        
        $factor = $this->criminalHistoryService->calculateCriminalHistoryFactor($oldConviction);
        
        $this->assertEquals(1.0000, $factor->factor_value); // Should not affect rating
    }
}
```

---

## Implementation Priority: MEDIUM
This factor provides important risk assessment for fraud and character evaluation. Should be implemented after primary driver factors.

## Dependencies
- **Background Check Integration**: Third-party criminal background services
- **Driver Class Factor**: Criminal history complements demographic factors

## Estimated Implementation Effort
- **Database Schema**: 4 days
- **Service Layer**: 6 days
- **Background Check Integration**: 4 days
- **Compliance Framework**: 3 days
- **API Integration**: 2 days
- **Testing**: 3 days
- **Total**: 22 days

This plan implements comprehensive criminal history risk assessment while maintaining strict regulatory compliance and privacy protection standards for sensitive criminal background data.