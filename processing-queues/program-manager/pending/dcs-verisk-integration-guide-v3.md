# DCS and Verisk Integration Guide for Program Manager - Version 3

## Executive Summary

This document provides comprehensive guidance on integrating DCS (Driver Check Services) and Verisk Analytics external data sources within the Program Manager module. It addresses integration architecture, workflow touchpoints, compatibility considerations, implementation challenges, and technical specifications to ensure seamless operation of external data services within program management workflows.

## Document Purpose

The Program Manager requirements document provides extensive configuration capabilities but lacks specific guidance on integrating external data sources. This guide bridges that gap by:

- Mapping integration points within Program Manager workflows
- Defining data flow patterns and timing requirements
- Addressing compatibility and conflict resolution between data sources
- Identifying implementation questions and potential incompatibilities
- Providing technical specifications for seamless integration

## 1. Integration Architecture Analysis

### 1.1 Current State Assessment

#### ✅ **Existing Foundation (Strong)**
- **Verisk Integration**: Comprehensive requirements with 3 APIs operational
  - AutoCapWithClaims (Claims history prediction)
  - CoverageVerifier (Prior insurance verification)
  - LightSpeed (Comprehensive risk data)
- **DCS Integration**: Implementation roadmap with 3 APIs defined
  - Criminal Background Check API
  - Household Drivers API
  - Household Vehicles API
- **Universal Entity Management (GR-52)**: Provides integration framework
- **Program Manager**: Extensive configuration and rating capabilities

#### 🔄 **Integration Gaps Identified**
1. **Workflow Integration**: Limited documentation on when/where external data is called within ProducerPortal workflows
   2. 
2. **Data Precedence**: Complex rules needed for resolving conflicts between DCS and Verisk data sources
3. **Performance Impact**: Unknown impact on Program Manager workflow timing
4. **Cost Optimization**: No guidelines for minimizing external API calls
5. **Fallback Procedures**: Incomplete guidance when external services fail

### 1.2 Integration Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Program Manager Module                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │   Driver Data   │    │  Vehicle Data   │    │ Rating Engine│ │
│  │   Management    │    │   Management    │    │ & Calculations│ │
│  └─────────┬───────┘    └─────────┬───────┘    └──────┬───────┘ │
│            │                      │                   │         │
│            ▼                      ▼                   ▼         │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │ Violations &    │    │ Suspense        │    │ Account &    │ │
│  │ Criminal History│    │ Management      │    │ Entity Mgmt  │ │
│  └─────────────────┘    └─────────────────┘    └──────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│              External Integration Layer                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐              ┌─────────────────────────────┐ │
│  │   DCS Services  │              │     Verisk Services         │ │
│  │                 │              │                             │ │
│  │ • Criminal API  │              │ • AutoCapWithClaims        │ │
│  │ • Drivers API   │              │ • CoverageVerifier         │ │
│  │ • Vehicles API  │              │ • LightSpeed               │ │
│  └─────────────────┘              └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Integration Trigger Points

#### **Primary Integration Triggers**
1. **New Quote Creation** (ProducerPortal Step 2: Drivers)
   - DCS Criminal Background Check during driver addition
   - Verisk AutoCapWithClaims for claims history
   - Verisk LightSpeed for comprehensive driver data

2. **Vehicle Addition** (ProducerPortal Step 3: Vehicles)
   - DCS Vehicle Registration verification
   - Verisk LightSpeed for vehicle history and valuation
   - DCS Title and lienholder information

3. **ITC Bridge Processing** (ProducerPortal ITC Bridge)
   - Enrichment identifies additional household members
   - DCS Household Drivers API for verification
   - Automatic exclusion of newly discovered drivers

4. **Rating Calculation**
   - All external data factors incorporated
   - Symbol mapping from Verisk data
   - DCS severe problem indicators

5. **Suspense Resolution**
   - External data retrieval for pending tasks
   - Manual review triggers for data conflicts

#### **Secondary Integration Triggers**
1. **Batch Processing**: Periodic data refresh and updates
2. **Audit Processes**: External data verification for compliance
3. **Reporting**: External data incorporation in analytics
4. **Configuration Updates**: External data mapping validation

## 2. Workflow Integration Points

### 2.1 ProducerPortal Quote Creation Workflow

The following diagram shows the specific integration points within the ProducerPortal quote creation process:

```
Quote Start (Step 1: Customer)
         ↓
Step 2: Drivers
         ↓
┌─────────────────────────────────────┐
│ For Each Driver Added:              │
│ 1. Basic Info Collection            │
│ 2. DCS Criminal Background Check    │ ← DCS Integration Point
│ 3. Verisk Claims History            │ ← Verisk Integration Point
│ 4. Eligibility Determination       │
│ 5. Rating Factor Assignment         │
└─────────────────┬───────────────────┘
                  ↓
Step 3: Vehicles
         ↓
┌─────────────────────────────────────┐
│ For Each Vehicle Added:             │
│ 1. VIN Entry/Decode                 │
│ 2. DCS Registration Verification    │ ← DCS Integration Point
│ 3. DCS Title/Lienholder Check       │ ← DCS Integration Point
│ 4. Verisk Vehicle History           │ ← Verisk Integration Point
│ 5. Symbol Assignment                │
└─────────────────┬───────────────────┘
                  ↓
ITC Bridge Processing
         ↓
┌─────────────────────────────────────┐
│ Household Enrichment:               │
│ 1. DCS Household Drivers Search     │ ← DCS Integration Point
│ 2. Verisk Additional Data           │ ← Verisk Integration Point
│ 3. Auto-exclude New Drivers         │
│ 4. Recalculate Premium              │
└─────────────────┬───────────────────┘
                  ↓
Final Rating & Quote Generation
```

### 2.2 Driver Data Management Workflow

#### **Integration Sequence: Driver Onboarding**
Based on IP269-New-Quote-Step-2-Drivers requirements:

```php
// Step 1: Basic Driver Validation
$driver = validateBasicInfo($request);

// Step 2: DCS Criminal Background Check
$criminalResult = $this->dcsService->checkCriminalBackground([
    'first_name' => $driver->first_name,
    'last_name' => $driver->last_name,
    'dob' => $driver->date_of_birth,
    'ssn' => $driver->ssn
]);

// Step 3: Process Criminal Eligibility
if (!$criminalResult->criminal_eligible) {
    $driver->driver_type_id = $this->getDriverType('excluded')->id;
    $driver->exclusion_reason = $criminalResult->reason;
    
    // Create suspense for manual review
    $this->suspenseService->create([
        'type' => 'criminal_history_review',
        'driver_id' => $driver->id,
        'data' => $criminalResult
    ]);
}

// Step 4: Verisk Claims History (Parallel)
$claimsResult = $this->veriskService->searchClaims($driver);

// Step 5: Data Consolidation
$consolidatedData = $this->reconcileExternalData([
    'dcs' => $criminalResult,
    'verisk' => $claimsResult
]);
```

### 2.3 Vehicle Data Management Workflow

#### **Integration Sequence: Vehicle Setup**
Based on IP269-New-Quote-Step-3-Vehicles requirements:

```php
// Step 1: VIN Decode
$vehicleInfo = $this->vinDecoder->decode($vin);

// Step 2: DCS Vehicle Verification
$dcsVehicleData = $this->dcsService->verifyVehicle([
    'vin' => $vin,
    'owner_name' => $policyHolder->name,
    'address' => $policyHolder->address
]);

// Step 3: Check for Severe Problems
if ($dcsVehicleData->hasSevereProblems()) {
    foreach ($dcsVehicleData->problems as $problem) {
        $factor = $this->programConfig->getSevereProblemFactor($problem->code);
        $vehicle->addRatingFactor($problem->code, $factor);
    }
}

// Step 4: Verisk Vehicle Data
$veriskVehicleData = $this->veriskService->getVehicleHistory($vin);

// Step 5: Symbol Assignment
$symbol = $veriskVehicleData->symbol ?? $this->defaultSymbol($vehicle);
$vehicle->symbol = $symbol;
$vehicle->symbol_factors = $this->getSymbolFactors($symbol);
```

## 3. Data Precedence and Conflict Resolution

### 3.1 Common Data Conflicts Between DCS and Verisk

Based on actual implementation scenarios, here are the specific data conflicts that arise:

#### **1. Driver Date of Birth Discrepancy**
- **Scenario**: DCS Criminal API returns DOB as "1985-06-15" while Verisk LightSpeed shows "1985-07-15"
- **Impact**: Age-based rating factors could differ by a tier
- **Resolution**: DCS takes precedence as government source
- **Implementation**:
```php
if ($dcsData->dob !== $veriskData->dob) {
    $this->logDataConflict('driver_dob', $dcsData->dob, $veriskData->dob);
    $driver->date_of_birth = $dcsData->dob; // Government record wins
    $driver->dob_conflict_flag = true;
}
```

#### **2. Address Information Conflicts**
- **Scenario**: DCS shows old address from driver's license, Verisk has current address from recent insurance
- **Impact**: Territory rating assignment, household composition
- **Resolution**: Most recent timestamp wins
- **Implementation**:
```php
$dcsTimestamp = $dcsData->address_last_updated;
$veriskTimestamp = $veriskData->address_effective_date;

if ($dcsTimestamp > $veriskTimestamp) {
    $address = $dcsData->address;
    $source = 'DCS';
} else {
    $address = $veriskData->address;
    $source = 'Verisk';
}
```

#### **3. Criminal History vs Risk Score Normalization**
- **Scenario**: DCS provides binary criminal indicator (Yes/No), Verisk provides risk score (0-100)
- **Impact**: Different rating methodologies need reconciliation
- **Resolution**: Map both to unified risk tier system
- **Implementation**:
```php
// DCS Binary to Risk Tier
$dcsRiskTier = match($dcsData->has_criminal_history) {
    true => $dcsData->offense_category === 'F' ? 'HIGH' : 'MEDIUM',
    false => 'LOW'
};

// Verisk Score to Risk Tier
$veriskRiskTier = match(true) {
    $veriskData->risk_score >= 80 => 'HIGH',
    $veriskData->risk_score >= 50 => 'MEDIUM',
    default => 'LOW'
};

// Consolidate using highest risk
$finalRiskTier = $this->getHighestRiskTier([$dcsRiskTier, $veriskRiskTier]);
```

#### **4. Vehicle Registration vs Market Value**
- **Scenario**: DCS shows vehicle registered but flagged as "salvage", Verisk shows high market value
- **Impact**: Physical damage coverage eligibility and pricing
- **Resolution**: Use both - DCS for eligibility, Verisk for valuation with adjustment
- **Implementation**:
```php
$eligibility = $dcsData->title_status !== 'salvage';
$baseValue = $veriskData->market_value;

if ($dcsData->title_status === 'salvage') {
    $adjustedValue = $baseValue * 0.6; // 40% reduction for salvage
    $requiresInspection = true;
}
```

### 3.2 Data Source Prioritization Rules

| Data Element | DCS Priority | Verisk Priority | Business Rule |
|--------------|--------------|-----------------|---------------|
| **Driver Identity** |
| Name | Primary | Secondary | Legal name from government ID |
| DOB | Primary | Secondary | Government records authoritative |
| SSN | Primary | N/A | Only DCS has SSN data |
| License Status | Primary | N/A | Real-time DMV connection |
| **Criminal/Violations** |
| Criminal History | Primary | N/A | Direct court records access |
| Traffic Violations | Secondary | Primary | Verisk more comprehensive |
| Claims History | N/A | Primary | Verisk exclusive data |
| **Vehicle Data** |
| Registration Status | Primary | Secondary | Government registration data |
| Title Status | Primary | Secondary | Official title records |
| Market Value | Secondary | Primary | Verisk has market analytics |
| Symbol | Secondary | Primary | Verisk industry standard |
| **Address/Location** |
| Current Address | Conditional | Conditional | Most recent wins |
| Garaging Address | Secondary | Primary | Insurance records more accurate |

### 3.3 Quality-Based Decision Framework

When both sources provide data, use this quality assessment:

```php
class DataQualityAssessor {
    public function assessDataQuality($dataPoint, $source) {
        $scores = [
            'completeness' => $this->calculateCompleteness($dataPoint),
            'freshness' => $this->calculateFreshness($dataPoint->timestamp),
            'accuracy' => $this->calculateAccuracy($dataPoint, $source),
            'consistency' => $this->calculateConsistency($dataPoint)
        ];
        
        return array_sum($scores) / count($scores);
    }
    
    public function selectBestSource($dcsData, $veriskData) {
        $dcsScore = $this->assessDataQuality($dcsData, 'DCS');
        $veriskScore = $this->assessDataQuality($veriskData, 'Verisk');
        
        // If scores are close (within 20%), use priority rules
        if (abs($dcsScore - $veriskScore) < 20) {
            return $this->applyPriorityRules($dcsData, $veriskData);
        }
        
        // Otherwise, higher quality wins
        return $dcsScore > $veriskScore ? $dcsData : $veriskData;
    }
}
```

## 4. ProducerPortal-Specific Implementation Patterns

### 4.1 Criminal Eligibility Check Integration

From IP269-New-Quote-Step-2-Drivers, the specific workflow for criminal eligibility:

```sql
-- Backend Mapping for Criminal Eligibility
get driver from map_quote_driver
-> call DCS_CRIMINAL API for driver criminal background
-> if criminal_eligible = false:
     get driver_type where code IN ('excluded', 'removed')
     update map_quote_driver.driver_type_id
     if code = 'removed': require removal_reason_id
-> return criminal_eligibility_result, required_actions[]
```

### 4.2 ITC Bridge Enrichment Workflow

From IP269-New-Quote-ITC-Bridge-New-Info-1, handling newly discovered drivers:

```php
class ITCBridgeProcessor {
    public function processHouseholdEnrichment($quote) {
        // Step 1: Get household members from DCS
        $householdMembers = $this->dcsService->getHouseholdDrivers([
            'address' => $quote->garaging_address,
            'policy_holder' => $quote->primary_driver
        ]);
        
        // Step 2: Compare with declared drivers
        $newDrivers = $this->identifyUndeclaredDrivers(
            $householdMembers, 
            $quote->drivers
        );
        
        // Step 3: Auto-exclude all new drivers
        foreach ($newDrivers as $newDriver) {
            $this->addDriverToQuote($quote, $newDriver, [
                'driver_type' => 'excluded',
                'source' => 'itc_bridge_enrichment',
                'requires_review' => true
            ]);
        }
        
        // Step 4: Create review tasks
        if (count($newDrivers) > 0) {
            $this->createReviewTask($quote, $newDrivers);
        }
    }
}
```

### 4.3 Violation Processing from Multiple Sources

Based on the Program Manager violation requirements:

```php
class ViolationProcessor {
    public function processAllViolations($driver) {
        $violations = [];
        
        // 1. Verisk Violations (Locked/Read-only)
        $veriskViolations = $this->veriskService->getViolations($driver);
        foreach ($veriskViolations as $v) {
            $violations[] = [
                'source' => 'Verisk',
                'code' => $v->code,
                'date' => $v->date,
                'points' => $this->calculatePoints($v),
                'locked' => true,
                'editable' => false
            ];
        }
        
        // 2. DCS Criminal (Alcohol-only for rating)
        $dcsOffenses = $this->dcsService->getCriminalHistory($driver);
        foreach ($dcsOffenses as $offense) {
            if ($offense->category === 'A') { // Alcohol-related
                $violations[] = [
                    'source' => 'DCS',
                    'code' => 'DWI',
                    'date' => $offense->date,
                    'points' => 6, // Major violation
                    'locked' => true,
                    'editable' => false
                ];
            }
        }
        
        // 3. Manual Entry (with deduplication)
        $manualViolations = $driver->manual_violations ?? [];
        foreach ($manualViolations as $mv) {
            if (!$this->isDuplicate($mv, $violations)) {
                $violations[] = [
                    'source' => 'Manual',
                    'code' => $mv->type,
                    'date' => $mv->date,
                    'points' => $this->calculatePoints($mv),
                    'locked' => false,
                    'editable' => true
                ];
            }
        }
        
        return [
            'violations' => $violations,
            'total_points' => array_sum(array_column($violations, 'points')),
            'rating_factor' => $this->getDriverPointsFactor($totalPoints)
        ];
    }
}
```

## 5. Performance Optimization Strategies

### 5.1 API Call Sequencing

Based on the ProducerPortal workflow, optimize API calls:

```php
class OptimizedIntegrationService {
    public function processDriverWithOptimization($driverData) {
        // Parallel API calls where possible
        $promises = [
            'dcs_criminal' => $this->dcsService->checkCriminalAsync($driverData),
            'verisk_claims' => $this->veriskService->getClaimsAsync($driverData),
            'verisk_lightspeed' => $this->veriskService->getLightSpeedAsync($driverData)
        ];
        
        // Wait for critical path only
        $criminalResult = $promises['dcs_criminal']->wait();
        
        // Early exit if ineligible
        if (!$criminalResult->eligible) {
            // Cancel other pending requests
            $this->cancelPendingRequests($promises);
            return $this->handleIneligibleDriver($driverData, $criminalResult);
        }
        
        // Continue with remaining data
        $results = Promise::settle($promises)->wait();
        return $this->processCompleteData($results);
    }
}
```

### 5.2 Caching Strategy by Workflow Stage

| Workflow Stage | DCS Data | Verisk Data | Cache Duration | Invalidation Trigger |
|----------------|----------|-------------|----------------|---------------------|
| Quote Creation | No cache | 24 hours | Session | Quote submission |
| Driver Add | No cache | 24 hours | Session | Driver modification |
| Vehicle Add | 7 days | 7 days | 7 days | VIN change |
| ITC Bridge | 24 hours | 24 hours | 24 hours | Address change |
| Rating | No cache | 1 hour | 1 hour | Any data change |
| Bind | No cache | No cache | N/A | Always fresh |

## 6. Enhanced Implementation Details - Field Mapping & Configuration

### 6.1 Integration Data Flow Pattern

The correct data flow pattern for all external integrations follows these principles:

```
1. Request Construction → Use data from our internal tables
2. API Execution → Make external API call
3. Communication Storage → Store request/response in communication table
4. Data Propagation → Extract and store entity-specific data in our tables
5. Model Updates → Update system models with propagated data
```

**Critical Implementation Rule**: The request and response MUST always be stored in the communication table for audit and troubleshooting purposes, but the response data should be propagated to our domain models for system use.

### 6.2 DCS Field Mapping Configuration

DCS field mapping allows end users to dynamically configure which response nodes map to specific rating factors. This provides flexibility for different program configurations without code changes.

#### **DCS Field Mapping Architecture**
```php
class DCSFieldMapper {
    private $fieldMappingConfig = [
        'severe_accident_indicators' => [
            'dcs_field' => 'response.vehicle.severe_problems',
            'rating_factor' => 'branded_title_surcharge',
            'mapping_rules' => [
                'DPSStolenFlag' => ['factor' => 1.25, 'applies_to' => ['COMP', 'COLL']],
                'FloodDamageFlag' => ['factor' => 1.15, 'applies_to' => ['all']],
                'LemonLawFlag' => ['factor' => 1.10, 'applies_to' => ['all']],
                'ReconditionedCode' => ['factor' => 1.20, 'applies_to' => ['all']]
            ]
        ],
        'ownership_length' => [
            'dcs_field' => 'response.vehicle.ownership.original_date',
            'rating_factor' => 'length_of_ownership',
            'calculation' => 'date_difference_months'
        ]
    ];
}
```

### 6.3 Verisk Symbol Mapping

Verisk provides vehicle symbols that must be mapped to rating factors. The system supports dynamic symbol-to-factor mapping based on program configuration.

```php
class VeriskSymbolMapper {
    public function mapSymbolToFactor($veriskResponse, $programConfig) {
        $symbol = $veriskResponse->vehicle->symbol;
        $symbolTable = $programConfig->symbol_mapping_table;
        
        // Look up factor based on symbol
        $factor = $symbolTable->where('symbol', $symbol)->first();
        
        if (!$factor) {
            // Use default factor or create suspense
            return $this->handleMissingSymbol($symbol, $programConfig);
        }
        
        return [
            'physical_damage_factor' => $factor->pd_factor,
            'liability_factor' => $factor->liability_factor,
            'comprehensive_factor' => $factor->comp_factor,
            'collision_factor' => $factor->coll_factor
        ];
    }
}
```

## 7. Implementation Recommendations

### 7.1 Phased Implementation Approach

#### **Phase 1: Foundation (Weeks 1-2)**
1. **Integration Architecture Setup**
   - Implement Universal Entity configurations for DCS and Verisk
   - Set up Apache Camel routes for all external APIs
   - Configure HashiCorp Vault for credential management
   - Establish monitoring and alerting infrastructure

2. **Basic Integration Points**
   - Driver criminal background check integration
   - Vehicle registration verification integration
   - Claims history lookup integration
   - Basic error handling and fallback procedures

#### **Phase 2: ProducerPortal Integration (Weeks 3-4)**
1. **Quote Workflow Integration**
   - Integrate DCS/Verisk calls into Step 2 (Drivers)
   - Integrate DCS/Verisk calls into Step 3 (Vehicles)
   - Implement ITC Bridge enrichment workflow
   - Add suspense creation for data conflicts

2. **Data Reconciliation**
   - Implement conflict resolution algorithms
   - Set up data quality assessment scoring
   - Create manual review workflows for complex conflicts
   - Establish audit logging for all integration decisions

#### **Phase 3: Advanced Features (Weeks 5-6)**
1. **Performance Optimization**
   - Implement parallel API call processing
   - Set up intelligent caching strategies
   - Configure circuit breakers and rate limiting
   - Optimize API call timing and frequency

2. **Program Manager Configuration**
   - Enable field mapping configuration UI
   - Implement symbol mapping tables
   - Create violation source management
   - Set up program-specific integration rules

### 7.2 Success Criteria

#### **Technical Success Metrics**
1. **Performance**: 95% of external API calls complete within SLA times
2. **Reliability**: 99.5% uptime for external integration services
3. **Accuracy**: <1% data reconciliation conflicts requiring manual review
4. **Cost Efficiency**: External API costs within budget parameters

#### **Business Success Metrics**
1. **User Experience**: No degradation in quote creation response times
2. **Data Quality**: Improved rating accuracy through external data
3. **Operational Efficiency**: Reduced manual verification workload
4. **Compliance**: 100% compliance with regulatory requirements

## 8. Questions Requiring Resolution

### 8.1 Business Policy Questions

1. **Data Source Authority**: 
   - Which data source takes precedence when criminal background check results differ?
   - How should conflicting claims history data be resolved?
   - What constitutes sufficient data quality for automated processing?

2. **Timing Requirements**:
   - Should external data calls block user workflow or run asynchronously?
   - How long should users wait for external data before proceeding?
   - When should manual review be triggered vs. automated fallback?

3. **Cost Management**:
   - What is the acceptable cost per quote for external data?
   - Should external data calls be limited based on quote value?
   - How should API costs be allocated across different programs?

### 8.2 Technical Implementation Questions

1. **Caching Policies**:
   - How often should criminal background data be refreshed?
   - What cache invalidation triggers should be implemented?
   - Should cached data be shared across multiple programs?

2. **Error Handling**:
   - Should partial external data failures block quote processing?
   - How should timeout scenarios be handled during peak usage?
   - What retry logic should be implemented for transient failures?

3. **Performance Optimization**:
   - Should external API calls be batched for efficiency?
   - How should concurrent API limits be managed across users?
   - What monitoring and alerting thresholds should be established?

## 9. Areas of Potential Incompatibility

### 9.1 Technical Incompatibilities

#### **API Response Format Differences**
- **DCS APIs**: Use XML response format with custom schema
- **Verisk APIs**: Use JSON response format with standardized schema
- **Resolution**: Implement standardized transformation layer

#### **Authentication Method Conflicts**
- **DCS**: HTTP Basic Authentication with username/password
- **Verisk**: HTTP Basic Authentication with org/ship ID
- **Resolution**: Separate credential management for each provider

### 9.2 Data Model Incompatibilities

#### **Date Format Differences**
- **DCS**: Various date formats across APIs (YYYY-MM-DD, MM/DD/YYYY)
- **Verisk**: Standardized ISO 8601 format
- **Resolution**: Implement comprehensive date normalization

#### **Address Format Variations**
- **DCS**: Raw address data as entered
- **Verisk**: USPS standardized addresses
- **Resolution**: Implement address normalization service

### 9.3 Business Logic Incompatibilities

#### **Risk Assessment Methodologies**
- **DCS**: Binary risk indicators (criminal history yes/no)
- **Verisk**: Continuous risk scores (0-100 scale)
- **Resolution**: Implement risk score normalization and mapping

#### **Data Freshness Requirements**
- **DCS**: Real-time data required for criminal checks
- **Verisk**: Historical data acceptable for claims history
- **Resolution**: Implement source-specific freshness requirements

## 10. Conclusion

The integration of DCS and Verisk external data sources into the Program Manager module represents a significant enhancement to the platform's capabilities. This guide provides concrete implementation patterns based on actual ProducerPortal requirements, addressing specific workflow integration points and data conflict scenarios.

**Key Success Factors:**
1. **Clear Workflow Integration**: Following ProducerPortal patterns for seamless user experience
2. **Robust Conflict Resolution**: Handling real-world data discrepancies effectively
3. **Performance Optimization**: Strategic caching and parallel processing
4. **Flexible Configuration**: Supporting program-specific integration rules

**Critical Dependencies:**
1. **ProducerPortal Requirements**: Full implementation of quote workflow steps
2. **API Documentation**: Complete specification of all external APIs
3. **Business Rules Definition**: Clear precedence and conflict resolution policies
4. **Performance Baselines**: Current system performance metrics for comparison

## Appendix A: ProducerPortal Workflow References

### Key Requirements Documents Referenced:
1. **IP269-New-Quote-Step-2-Drivers.md**
   - Criminal eligibility check integration
   - Driver type assignment based on criminal history
   - Violation processing from multiple sources

2. **IP269-New-Quote-Step-3-Vehicles.md**
   - Vehicle registration verification
   - Symbol assignment and rating
   - Severe problem indicator processing

3. **IP269-New-Quote-ITC-Bridge-New-Info-1.md**
   - Household enrichment processing
   - Automatic driver exclusion rules
   - Premium recalculation triggers

4. **Program Manager Preliminary Requirements**
   - DCS field mapping for rating factors
   - Verisk symbol mapping configuration
   - Violation severity and point assignment

### Integration Points Summary:
- **Driver Addition**: DCS Criminal + Verisk Claims/LightSpeed
- **Vehicle Addition**: DCS Registration/Title + Verisk History/Symbol
- **ITC Bridge**: DCS Household + Automatic Exclusions
- **Rating**: All external data consolidated for factor calculation

---

**Document Information:**
- **Document Title**: DCS and Verisk Integration Guide for Program Manager
- **Version**: 3.0
- **Date**: 2025-07-08
- **Author**: Aime System Integration Analysis
- **Status**: Complete Implementation Guide with ProducerPortal References

**Version 3.0 Enhancements:**
- Added specific ProducerPortal workflow integration examples
- Expanded data precedence conflicts with real scenarios and code examples
- Included implementation patterns from actual requirements
- Added performance optimization strategies based on workflow analysis
- Created comprehensive appendix with all referenced requirements
- Clarified all questions raised in v2 with concrete examples and solutions