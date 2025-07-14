# LightSpeed Coverage Verifier - Program Manager Integration Plan

**Status:** DRAFT - Awaiting Approval  
**Date:** 2025-01-08  
**Version:** 1.0  
**Domain:** EntityIntegration + ProgramManager  
**Processing Agent:** EntityIntegration Specialist + ProgramManager Specialist  

---

## Pre-Analysis Summary

### Existing Documentation Review
Based on analysis of LightSpeed V4 and Program Manager documentation:

1. **LightSpeed Coverage Verifier Capabilities**:
   - CoverageVerifierReport in DataSources
   - Coverage lapse information with date ranges
   - Policy history and status tracking
   - Continuous coverage verification
   - Located at: `Response.Body.DataSources.CoverageVerifierReport`
   - Also: `Response.Body.CompleteQuote.CoverageLapseInformation`

2. **Program Manager Current State**:
   - Prior Insurance Verification Levels: "Prior Insurance", "Transfer", "Verified"
   - Policy Core Matrix uses verification level for rating
   - Number of Months Prior Coverage tracking (0-6, 6-11, 12+)
   - No automated verification currently implemented

### Global Requirements Alignment
This initiative aligns with key Global Requirements:
- **GR-52**: Universal Entity Management - For managing LightSpeed as external entity
- **GR-48**: External Integrations Catalog - Apache Camel integration
- **GR-44**: Communication Architecture - API call tracking
- **GR-19**: Status Management - Coverage verification status
- **GR-41**: Database Standards - Coverage history table design
- **GR-33**: Data Services & Caching - Coverage data caching strategy

### Integration Gap Analysis
- Manual verification process for prior coverage
- No real-time coverage lapse detection
- Missing automated verification status upgrade
- No continuous coverage tracking
- Limited coverage history visibility

---

## Objectives

### Primary Goals
1. Automate prior insurance verification using Coverage Verifier
2. Integrate coverage lapse detection into rating
3. Upgrade verification status from "Prior Insurance" to "Verified" automatically
4. Implement continuous coverage tracking
5. Enable coverage history visibility for underwriting

### Expected Outcomes
- 90% reduction in manual coverage verification
- Improved rating accuracy with verified coverage data
- Real-time lapse detection preventing coverage gaps
- Enhanced fraud prevention through verification
- Streamlined underwriting with automated verification

---

## Scope and Approach

### In Scope
1. **Coverage Verifier Integration**:
   - Prior coverage verification
   - Coverage lapse detection
   - Policy history retrieval
   - Continuous coverage validation
   - Verification status automation

2. **Program Manager Enhancements**:
   - Automated verification level upgrade
   - Coverage lapse factors
   - Enhanced Policy Core Matrix
   - Real-time verification during quote

3. **Rating Enhancements**:
   - Verified coverage discounts
   - Lapse surcharges
   - Continuous coverage rewards
   - Gap penalty calculations

### Out of Scope
- Historical coverage data migration
- Manual verification override (future phase)
- Competitor carrier analysis
- Coverage limit verification
- Multi-state coverage tracking

### Technical Approach
- Leverage LightSpeed for Coverage Verifier data
- Enhance Prior Insurance Verification Level logic
- Implement automated status upgrades
- Create lapse-based rating factors

---

## Implementation Requirements

### Program Manager Configuration

#### Enhanced Prior Insurance Verification Levels
```
Current State:
- Prior Insurance (reported by insured)
- Transfer (validated by MGA or producer)
- Verified (confirmed via third-party)

Enhanced State:
- Prior Insurance (reported by insured)
- Transfer (validated by MGA or producer)
- Verified - Coverage Verifier (automated via LightSpeed)
- Verified - Manual (confirmed via other means)
```

#### Coverage Lapse Factors
New factor category in Policy Core Matrix:

```
| Coverage Status | Lapse Days | Round By | BI | PD | UMBI | UMPD | MED | PIP | COMP | COLL | Terms | Supported |
|-----------------|------------|----------|----|----|------|------|-----|-----|------|------|-------|-----------|
| Continuous      | 0          | 2        | 0.95 | 0.95 | 1.00 | 1.00 | 0.98 | 0.98 | 0.95 | 0.95 | 6,12 | On |
| Minor Lapse     | 1-30       | 2        | 1.05 | 1.05 | 1.00 | 1.00 | 1.02 | 1.02 | 1.05 | 1.05 | 6,12 | On |
| Major Lapse     | 31-60      | 2        | 1.15 | 1.15 | 1.00 | 1.00 | 1.05 | 1.05 | 1.15 | 1.15 | 6,12 | On |
| Severe Lapse    | 61+        | 2        | 1.25 | 1.25 | 1.00 | 1.00 | 1.10 | 1.10 | 1.25 | 1.25 | 6,12 | On |
| No Prior        | N/A        | 2        | 1.30 | 1.30 | 1.00 | 1.00 | 1.15 | 1.15 | 1.30 | 1.30 | 6,12 | On |
```

#### Enhanced Policy Core Matrix Integration
Modify existing Factor Grouping #2 to include verified status bonus:

```
| Months Prior | Verification Level | Homeowner | Vehicles | Round By | BI | PD | ... | Supported |
|--------------|-------------------|-----------|----------|----------|----|----|-----|-----------|
| 12+          | Verified - Coverage Verifier | Yes | 1 | 2 | 0.90 | 0.90 | ... | On |
| 12+          | Verified - Coverage Verifier | No  | 1 | 2 | 0.92 | 0.92 | ... | On |
| 12+          | Prior Insurance   | Yes | 1 | 2 | 0.95 | 0.95 | ... | On |
| 12+          | Prior Insurance   | No  | 1 | 2 | 0.97 | 0.97 | ... | On |
```

### Integration Architecture

#### Data Flow
```yaml
quote_creation:
  1. prior_insurance_entered:
     - trigger: Carrier/policy number provided
     - action: Queue coverage verification
  
  2. lightspeed_response:
     - extract: CoverageVerifierReport
     - parse: Coverage dates, lapses, policy status
     - evaluate: Continuous coverage status
  
  3. verification_processing:
     - compare: Reported vs verified coverage
     - upgrade: Verification level if matched
     - calculate: Lapse days if gaps exist
  
  4. rating_calculation:
     - apply: Verified coverage discount
     - apply: Lapse surcharges if applicable
     - use: Enhanced verification level in matrix
```

#### Service Implementation
```php
class CoverageVerificationService
{
    public function verifyCoverage(Quote $quote, Program $program): CoverageVerificationResult
    {
        // Get coverage data from LightSpeed
        $coverageData = $this->getCoverageVerifierData($quote);
        
        // Verify reported prior insurance
        $verificationResult = $this->verifyReportedCoverage(
            $quote->getPriorInsurance(),
            $coverageData
        );
        
        // Calculate coverage gaps
        $lapseAnalysis = $this->analyzeCoverageLapses(
            $coverageData->getCoverageLapseInformation()
        );
        
        // Update verification status
        if ($verificationResult->isVerified()) {
            $quote->setPriorInsuranceVerificationLevel('VERIFIED_COVERAGE_VERIFIER');
            
            // Apply verification timestamp
            $quote->setPriorInsuranceVerifiedAt(now());
        }
        
        // Calculate rating factors
        $factors = [
            'verification_level_factor' => $this->getVerificationLevelFactor(
                $quote->getPriorInsuranceVerificationLevel(),
                $program
            ),
            'lapse_factor' => $this->getLapseFactor(
                $lapseAnalysis->getTotalLapseDays(),
                $program
            )
        ];
        
        return new CoverageVerificationResult([
            'verified' => $verificationResult->isVerified(),
            'verification_level' => $quote->getPriorInsuranceVerificationLevel(),
            'lapse_days' => $lapseAnalysis->getTotalLapseDays(),
            'continuous_coverage' => $lapseAnalysis->hasContinuousCoverage(),
            'factors' => $factors,
            'coverage_history' => $coverageData->getPolicies()
        ]);
    }
    
    private function verifyReportedCoverage($reported, $verified): VerificationResult
    {
        // Match logic
        $carrierMatch = $this->matchCarrier(
            $reported->getCarrierName(),
            $verified->getCarriers()
        );
        
        $policyMatch = $this->matchPolicy(
            $reported->getPolicyNumber(),
            $verified->getPolicies()
        );
        
        $dateMatch = $this->matchCoverageDates(
            $reported->getExpirationDate(),
            $verified->getCoveragePeriods()
        );
        
        return new VerificationResult([
            'verified' => $carrierMatch && ($policyMatch || $dateMatch),
            'confidence_score' => $this->calculateConfidence(
                $carrierMatch,
                $policyMatch,
                $dateMatch
            ),
            'match_details' => [
                'carrier' => $carrierMatch,
                'policy' => $policyMatch,
                'dates' => $dateMatch
            ]
        ]);
    }
}
```

### Database Schema

#### New Tables

##### coverage_verification_log
```sql
CREATE TABLE coverage_verification_log (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    quote_id BIGINT UNSIGNED NOT NULL,
    driver_id BIGINT UNSIGNED NOT NULL,
    verification_status ENUM('UNVERIFIED', 'VERIFIED', 'MISMATCH', 'NO_DATA') NOT NULL,
    reported_carrier VARCHAR(255) NULL,
    reported_policy_number VARCHAR(50) NULL,
    reported_expiration_date DATE NULL,
    verified_carrier VARCHAR(255) NULL,
    verified_policy_number VARCHAR(50) NULL,
    verified_expiration_date DATE NULL,
    confidence_score DECIMAL(5,2) NULL,
    total_lapse_days INT DEFAULT 0,
    has_continuous_coverage BOOLEAN DEFAULT FALSE,
    coverage_history JSON NULL,
    verified_at TIMESTAMP NULL,
    
    -- Audit fields
    created_by BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_quote (quote_id),
    INDEX idx_driver (driver_id),
    INDEX idx_verification_date (verified_at),
    
    -- Foreign keys
    FOREIGN KEY (quote_id) REFERENCES quote(id),
    FOREIGN KEY (driver_id) REFERENCES driver(id),
    FOREIGN KEY (created_by) REFERENCES user(id)
);
```

##### coverage_lapse_factors
```sql
CREATE TABLE coverage_lapse_factors (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    program_id BIGINT UNSIGNED NOT NULL,
    lapse_category VARCHAR(20) NOT NULL,
    min_lapse_days INT NOT NULL,
    max_lapse_days INT NULL,
    bi_factor DECIMAL(5,2) DEFAULT 1.00,
    pd_factor DECIMAL(5,2) DEFAULT 1.00,
    umbi_factor DECIMAL(5,2) DEFAULT 1.00,
    umpd_factor DECIMAL(5,2) DEFAULT 1.00,
    med_factor DECIMAL(5,2) DEFAULT 1.00,
    pip_factor DECIMAL(5,2) DEFAULT 1.00,
    comp_factor DECIMAL(5,2) DEFAULT 1.00,
    coll_factor DECIMAL(5,2) DEFAULT 1.00,
    round_factor_by TINYINT DEFAULT 2,
    applicable_terms JSON NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    
    -- Audit fields
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    UNIQUE KEY unique_program_lapse (program_id, lapse_category),
    INDEX idx_lapse_days (min_lapse_days, max_lapse_days),
    
    -- Foreign keys
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```

##### coverage_verification_cache
```sql
CREATE TABLE coverage_verification_cache (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    lookup_key VARCHAR(255) NOT NULL, -- Hash of name + DOB + prior carrier
    policies_found INT DEFAULT 0,
    has_coverage_lapse BOOLEAN DEFAULT FALSE,
    total_lapse_days INT DEFAULT 0,
    coverage_data JSON NULL,
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    
    -- Indexes
    UNIQUE KEY unique_lookup (lookup_key),
    INDEX idx_expires (expires_at)
);
```

### Configuration Management

#### Program-Level Settings
```yaml
program_configuration:
  coverage_verification:
    enabled: true
    auto_upgrade_verification: true
    verification_benefits:
      verified_discount_percent: 5
      continuous_coverage_bonus: 3
    lapse_penalties:
      minor_lapse_threshold: 30
      major_lapse_threshold: 60
      max_penalty_percent: 25
    matching_rules:
      carrier_match_required: false
      policy_match_weight: 0.7
      date_match_weight: 0.3
      min_confidence_score: 0.8
    cache_ttl_hours: 24
```

#### UI Enhancements
```
Prior Insurance Section:
- [New] Verification Status: [Icon] Verified via Coverage Verifier
- [New] Coverage History: [View Details]
- [New] Lapse Information: No gaps detected ✓
- [Enhanced] Verification Level: Automatically upgraded
```

---

## Integration Points

### Quote/Bind Workflow
1. Prior insurance information collection
2. Automatic Coverage Verifier lookup
3. Real-time verification and upgrade
4. Lapse detection and factor application
5. Display verification status to agent

### Underwriting Review
- Coverage history visibility
- Lapse details for risk assessment
- Verification confidence score
- Override options for edge cases

### Renewal Processing
- Re-verify coverage at renewal
- Track continuous coverage with carrier
- Apply loyalty discounts for verified continuous coverage

---

## Performance Requirements

### Response Times
- Coverage verification: < 200ms from LightSpeed data
- Lapse calculation: < 50ms
- Factor application: < 100ms

### Caching Strategy
- 24-hour TTL for coverage verification
- Key by name + DOB + carrier hash
- Invalidate on driver info changes

### Scalability
- Support 100+ concurrent verifications
- Handle 20,000+ daily quote verifications
- Batch processing for renewals

---

## Risk Mitigation

### Technical Risks
1. **Matching Accuracy**
   - Mitigation: Configurable confidence thresholds
   - Fallback: Manual verification option

2. **False Positives**
   - Mitigation: Conservative matching rules
   - Review: Underwriter oversight for mismatches

3. **Data Availability**
   - Mitigation: Graceful degradation
   - Alternative: Traditional verification levels

### Business Risks
1. **Over-reliance on Automation**
   - Mitigation: Audit trail and overrides
   - Monitoring: Verification accuracy metrics

2. **Competitive Disclosure**
   - Mitigation: Aggregate carrier data only
   - Privacy: No detailed policy information stored

---

## Next Steps After Approval

### Implementation Phases
1. **Phase 1: Infrastructure** (Week 1)
   - Database schema setup
   - Verification service framework
   - Cache implementation

2. **Phase 2: Integration** (Week 2)
   - Coverage Verifier data extraction
   - Matching algorithm implementation
   - Lapse calculation engine

3. **Phase 3: Configuration** (Week 3)
   - Program-specific rules
   - UI enhancements
   - Factor testing

4. **Phase 4: Rollout** (Week 4)
   - Pilot program testing
   - Accuracy monitoring
   - Full deployment

### Success Metrics
- 90% auto-verification rate
- 95% verification accuracy
- 50% reduction in manual reviews
- 15% improvement in quote-to-bind ratio

---

## Approval Required

**This plan requires approval before proceeding with detailed requirements generation.**

Once approved, the multi-agent system will:
1. Generate detailed technical requirements
2. Create matching algorithm specifications
3. Define verification UI workflows
4. Establish testing protocols
5. Document verification methodology

### Review Checklist
- [ ] Verification approach acceptable
- [ ] Lapse factors align with risk models
- [ ] Privacy considerations addressed
- [ ] UI enhancements approved
- [ ] Timeline achievable

---

**Note**: This plan automates prior insurance verification using LightSpeed's Coverage Verifier data. The verification will enhance rating accuracy while reducing manual underwriting effort.