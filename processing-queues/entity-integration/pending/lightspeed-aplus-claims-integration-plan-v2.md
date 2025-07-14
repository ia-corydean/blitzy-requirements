# LightSpeed APlus Claims - Program Manager Integration Plan

**Status:** DRAFT - Awaiting Approval  
**Date:** 2025-01-08  
**Version:** 2.0  
**Domain:** EntityIntegration + ProgramManager  
**Processing Agent:** EntityIntegration Specialist + ProgramManager Specialist  

---

## Pre-Analysis Summary

### Existing Documentation Review
Based on analysis of LightSpeed V4 and Program Manager documentation:

1. **LightSpeed APlus Capabilities**:
   - APlus Auto Report integrated within LightSpeed
   - Claim Activity Predictor (CAP) indicator (Y/N)
   - Number of claims count
   - Detailed claims information with at-fault indicators
   - Claims match reasons and carrier information
   - Located at: `Response.Body.DataSources.APlusAutoReport`

2. **Program Manager Current State**:
   - Violations and Criminal History rating factors exist
   - No current claims-based rating factors
   - Factor grouping system supports multi-attribute combinations
   - Base rates modified by various driver and policy factors

### Global Requirements Alignment
This initiative aligns with key Global Requirements:
- **GR-52**: Universal Entity Management - For managing LightSpeed as external entity
- **GR-48**: External Integrations Catalog - Apache Camel integration
- **GR-44**: Communication Architecture - API call tracking
- **GR-38**: Microservice Architecture - Service boundary compliance
- **GR-41**: Database Standards - Claims factor table design
- **GR-33**: Data Services & Caching - Claims data caching strategy
- **GR-19**: Status Management - Claims verification status tracking

### Integration Gap Analysis
- Program Manager lacks claims history rating factors
- No integration with external claims databases
- CAP indicator not utilized in underwriting decisions
- Missing at-fault claim surcharge structure
- No claims-free discount mechanisms

---

## Objectives

### Primary Goals
1. Integrate APlus claims data into Program Manager rating engine
2. Implement CAP indicator-based underwriting rules
3. Create claims count and at-fault factor tables
4. Enable real-time claims lookup during quote/bind
5. Establish claims-based discount/surcharge structure
6. Implement direct APlus API integration for enhanced data access

### Expected Outcomes
- Improved risk assessment using actual claims history
- Automated underwriting decisions based on CAP indicator
- Competitive advantage through precise claims-based rating
- Reduced manual underwriting for claims verification
- Enhanced fraud detection through claims pattern analysis

---

## Scope and Approach

### In Scope
1. **APlus Claims Integration**:
   - CAP indicator processing
   - Claims count factor application
   - At-fault claim surcharges
   - Claims-free discount eligibility
   - Claim recency factors
   - Direct APlus API integration

2. **Program Manager Enhancements**:
   - New Claims History factor category
   - CAP-based underwriting rules
   - Claims factor grouping
   - Real-time integration during rating

3. **Underwriting Rules**:
   - Hard stops based on CAP indicator
   - Claims threshold configuration
   - At-fault claim limits
   - Time-based claim weighting

### Out of Scope
- Historical claims data migration
- Claims detail storage (only factors stored)
- Claims reporting and analytics (future phase)
- Subrogation tracking

### Technical Approach
- Leverage existing LightSpeed integration for APlus data
- Implement direct APlus API integration as enhanced option
- Extend Program Manager violations section for claims
- Implement configurable underwriting thresholds
- Use communication tracking for audit trail

---

## Implementation Requirements

### Program Manager Configuration

#### New Section: Claims History Rating
Location: **[IV] Rating — Violations & Criminal History**

##### CAP Indicator Configuration
```
| CAP Indicator | Description | Underwriting Action | Hard Stop | Supported |
|---------------|-------------|-------------------|-----------|-----------|
| Y             | High claims risk | Apply surcharge | Yes/No | On |
| N             | Normal risk | Standard rating | No | On |
```

##### Claims Count Factors
```
| Claims Count | Time Period | Round By | BI | PD | UMBI | UMPD | MED | PIP | COMP | COLL | Terms | Supported |
|--------------|-------------|----------|----|----|------|------|-----|-----|------|------|-------|-----------|
| 0            | 36 months   | 2        | 0.95 | 0.95 | 1.00 | 1.00 | 1.00 | 1.00 | 0.95 | 0.95 | 6,12 | On |
| 1            | 36 months   | 2        | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 6,12 | On |
| 2            | 36 months   | 2        | 1.15 | 1.15 | 1.00 | 1.00 | 1.10 | 1.10 | 1.20 | 1.20 | 6,12 | On |
| 3+           | 36 months   | 2        | 1.35 | 1.35 | 1.00 | 1.00 | 1.25 | 1.25 | 1.40 | 1.40 | 6,12 | On |
```

##### At-Fault Claims Factors
```
| At-Fault Count | Time Period | Round By | BI | PD | UMBI | UMPD | MED | PIP | COMP | COLL | Terms | Supported |
|----------------|-------------|----------|----|----|------|------|-----|-----|------|------|-------|-----------|
| 0              | 36 months   | 2        | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 6,12 | On |
| 1              | 36 months   | 2        | 1.25 | 1.25 | 1.00 | 1.00 | 1.15 | 1.15 | 1.30 | 1.30 | 6,12 | On |
| 2+             | 36 months   | 2        | 1.50 | 1.50 | 1.00 | 1.00 | 1.30 | 1.30 | 1.60 | 1.60 | 6,12 | On |
```

#### New Factor Grouping: Claims + Violations
```
Factor Grouping #6: Combined Claims and Violations
Combines: Claims Count + Violation Count + Driver Age
Purpose: Comprehensive driver risk assessment
```

### Integration Architecture

#### Data Flow
```yaml
quote_creation:
  1. driver_information_collected:
     - trigger: SSN/DOB validation
     - action: Queue LightSpeed comprehensive request
  
  2. lightspeed_response:
     - extract: APlusAutoReport from DataSources
     - parse: CAP indicator, claims count, at-fault status
     - cache: Store claims summary with driver
  
  3. direct_aplus_enhancement:
     - trigger: If enabled and additional data needed
     - action: Direct APlus API call for detailed claims
     - merge: Combine with LightSpeed data
  
  4. underwriting_evaluation:
     - check: CAP indicator against program rules
     - decision: Continue or refer/decline
  
  5. rating_calculation:
     - apply: Claims count factors
     - apply: At-fault claim surcharges
     - combine: With other rating factors
```

#### Service Implementation
```php
class ClaimsRatingService
{
    private $lightSpeedService;
    private $aplusDirectService;
    
    public function evaluateClaimsHistory(Driver $driver, Program $program): ClaimsRatingResult
    {
        // Get claims data from LightSpeed cache
        $claimsData = $this->getDriverClaimsData($driver->ssn);
        
        // Enhance with direct APlus if enabled
        if ($program->isAplusDirectEnabled()) {
            $enhancedData = $this->aplusDirectService->getDetailedClaims($driver);
            $claimsData = $this->mergeClaimsData($claimsData, $enhancedData);
        }
        
        // Check CAP indicator first
        if ($claimsData->capIndicator === 'Y') {
            $capRule = $program->getCapIndicatorRule();
            if ($capRule->isHardStop) {
                return ClaimsRatingResult::decline('CAP_INDICATOR_FAIL');
            }
        }
        
        // Calculate claims factors
        $claimsFactors = $this->calculateClaimsFactors(
            $claimsData->claimsCount,
            $claimsData->atFaultCount,
            $program->id
        );
        
        // Check underwriting thresholds
        $underwritingResult = $this->checkUnderwritingRules(
            $claimsData,
            $program->getClaimsThresholds()
        );
        
        return new ClaimsRatingResult([
            'factors' => $claimsFactors,
            'underwriting_status' => $underwritingResult,
            'cap_indicator' => $claimsData->capIndicator,
            'claims_summary' => $claimsData->getSummary(),
            'data_source' => $claimsData->getSource() // 'LIGHTSPEED' or 'APLUS_DIRECT'
        ]);
    }
}

class AplusDirectService
{
    private $aplusClient;
    
    public function getDetailedClaims(Driver $driver): AplusClaimsData
    {
        // Direct APlus API integration
        $request = new AplusRequest([
            'ssn' => $driver->ssn,
            'dob' => $driver->dateOfBirth,
            'license_number' => $driver->licenseNumber,
            'state' => $driver->licenseState
        ]);
        
        $response = $this->aplusClient->getClaims($request);
        
        return $this->parseAplusResponse($response);
    }
}
```

### Database Schema

#### New Tables

##### claims_rating_factors
```sql
CREATE TABLE claims_rating_factors (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    program_id BIGINT UNSIGNED NOT NULL,
    factor_type ENUM('CLAIMS_COUNT', 'AT_FAULT', 'CAP_INDICATOR') NOT NULL,
    factor_value VARCHAR(10) NOT NULL,
    time_period_months TINYINT DEFAULT 36,
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
    UNIQUE KEY unique_program_factor (program_id, factor_type, factor_value),
    INDEX idx_factor_lookup (factor_type, factor_value),
    
    -- Foreign keys
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```

##### claims_underwriting_rules
```sql
CREATE TABLE claims_underwriting_rules (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    program_id BIGINT UNSIGNED NOT NULL,
    rule_type ENUM('CAP_INDICATOR', 'CLAIMS_THRESHOLD', 'AT_FAULT_LIMIT') NOT NULL,
    rule_value VARCHAR(50) NOT NULL,
    action ENUM('ACCEPT', 'REFER', 'DECLINE') NOT NULL,
    is_hard_stop BOOLEAN DEFAULT FALSE,
    message TEXT NULL,
    status_id BIGINT UNSIGNED NOT NULL,
    
    -- Audit fields
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    UNIQUE KEY unique_program_rule (program_id, rule_type, rule_value),
    
    -- Foreign keys
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```

##### driver_claims_cache
```sql
CREATE TABLE driver_claims_cache (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    driver_ssn_hash VARCHAR(64) NOT NULL,
    cap_indicator CHAR(1) NULL,
    total_claims_count TINYINT DEFAULT 0,
    at_fault_count TINYINT DEFAULT 0,
    not_at_fault_count TINYINT DEFAULT 0,
    claims_summary JSON NULL,
    data_source ENUM('LIGHTSPEED', 'APLUS_DIRECT', 'COMBINED') NOT NULL,
    evaluation_date DATE NOT NULL,
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    
    -- Indexes
    UNIQUE KEY unique_ssn_date (driver_ssn_hash, evaluation_date),
    INDEX idx_expires (expires_at)
);
```

##### aplus_api_configuration
```sql
CREATE TABLE aplus_api_configuration (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    program_id BIGINT UNSIGNED NOT NULL,
    api_endpoint VARCHAR(255) NOT NULL,
    api_username VARCHAR(100) NOT NULL,
    api_password_encrypted TEXT NOT NULL,
    api_version VARCHAR(10) DEFAULT 'v1',
    enabled BOOLEAN DEFAULT FALSE,
    use_for_enhancement BOOLEAN DEFAULT TRUE,
    standalone_enabled BOOLEAN DEFAULT FALSE,
    timeout_seconds INT DEFAULT 30,
    retry_attempts TINYINT DEFAULT 3,
    
    -- Audit fields
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    UNIQUE KEY unique_program (program_id),
    
    -- Foreign keys
    FOREIGN KEY (program_id) REFERENCES program(id)
);
```

### Configuration Management

#### Program-Level Settings
```yaml
program_configuration:
  claims_rating:
    enabled: true
    cap_indicator_rules:
      Y: 
        action: "refer"
        hard_stop: false
        message: "High claims activity detected"
      N:
        action: "accept"
    thresholds:
      max_claims_36_months: 3
      max_at_fault_36_months: 2
      claims_free_discount:
        enabled: true
        discount_percent: 5
        qualification_months: 36
    cache_ttl_hours: 24
  
  aplus_direct_integration:
    enabled: true
    use_cases:
      - enhancement  # Enhance LightSpeed data
      - fallback     # When LightSpeed unavailable
      - standalone   # Direct API only
    priority: "lightspeed_first"
    detailed_claims_lookup: true
```

#### Underwriting Questions Enhancement
Add to existing underwriting questions:
```
| Question | Supported | Hard Stop |
|----------|-----------|-----------|
| Has any driver had unreported claims in the last 3 years? | On | Yes |
| CAP Indicator shows high claims activity. Proceed with supervisor approval? | On | No |
```

---

## Integration Points

### Quote/Bind Workflow
1. Driver SSN triggers LightSpeed lookup
2. APlus claims data extraction
3. Optional direct APlus enhancement
4. CAP indicator evaluation
5. Claims factor calculation
6. Underwriting rule application
7. Final rating with claims factors

### Endorsement Processing
- Re-evaluate if driver added
- No re-rate for existing drivers (claims locked at term start)
- Claims data refresh on renewal only

### Renewal Processing
- Fresh claims lookup at renewal
- Compare claims progression
- Apply claims-free discount if eligible

### Direct APlus Integration Points
- Primary: Enhancement of LightSpeed data
- Secondary: Fallback when LightSpeed unavailable
- Optional: Standalone for detailed investigations

---

## Performance Requirements

### Response Times
- Claims data extraction: < 100ms from LightSpeed response
- Direct APlus API call: < 3 seconds
- Factor calculation: < 50ms
- Underwriting evaluation: < 200ms

### Caching Strategy
- 24-hour TTL for claims data (fresh daily)
- Driver-specific caching by SSN hash
- Separate cache for direct APlus results
- Invalidate on driver information changes

### Scalability
- Support 50+ programs with unique claims rules
- Handle 10,000+ daily quotes with claims rating
- Process batch renewals with claims refresh
- Support concurrent direct API calls

---

## Risk Mitigation

### Technical Risks
1. **LightSpeed Data Quality**
   - Mitigation: Direct APlus validation
   - Fallback: Allow manual claims entry

2. **Direct API Performance**
   - Mitigation: Asynchronous processing option
   - Monitoring: Track API response times

3. **Data Privacy**
   - Mitigation: Hash SSN for caching
   - Compliance: Follow PII handling standards

### Business Risks
1. **Over-penalizing Claims**
   - Mitigation: Competitive analysis of factors
   - Testing: A/B test factor impacts

2. **CAP Indicator Reliability**
   - Mitigation: Configurable actions
   - Override: Supervisor approval option

---

## Next Steps After Approval

### Implementation Phases
1. **Phase 1: Infrastructure** (Week 1)
   - Database schema creation
   - Claims data models
   - Caching service setup

2. **Phase 2: Integration** (Week 2)
   - APlus data extraction from LightSpeed
   - Direct APlus API implementation
   - Claims factor engine
   - Underwriting rule engine

3. **Phase 3: Configuration** (Week 3)
   - Program-specific setup
   - Direct API credentials
   - Factor testing
   - UI enhancements

4. **Phase 4: Rollout** (Week 4)
   - Pilot program testing
   - Performance monitoring
   - Gradual program adoption

### Success Metrics
- 100% CAP indicator capture rate
- < 2% rating time increase
- 90% automated underwriting decisions
- 20% improvement in loss ratio prediction
- 95% direct API availability

---

## Approval Required

**This plan requires approval before proceeding with detailed requirements generation.**

Once approved, the multi-agent system will:
1. Generate detailed technical requirements
2. Create underwriting rule specifications
3. Define Program Manager UI updates
4. Establish testing protocols
5. Document claims factor methodology

### Review Checklist
- [ ] Claims factors align with actuarial models
- [ ] CAP indicator rules acceptable
- [ ] Underwriting thresholds appropriate
- [ ] Direct API integration approach approved
- [ ] Privacy compliance confirmed
- [ ] Integration timeline approved

---

**Note**: This plan integrates APlus claims data for enhanced risk assessment with both LightSpeed and direct API options. The claims factors will work in conjunction with existing violation and credit-based factors for comprehensive rating.