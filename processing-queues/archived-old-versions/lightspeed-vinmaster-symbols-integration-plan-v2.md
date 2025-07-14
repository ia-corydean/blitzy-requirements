# LightSpeed VinMaster Symbols - Program Manager Integration Plan

**Status:** DRAFT - Awaiting Approval  
**Date:** 2025-01-08  
**Version:** 2.0  
**Domain:** EntityIntegration + ProgramManager  
**Processing Agent:** EntityIntegration Specialist + ProgramManager Specialist  

---

## Pre-Analysis Summary

### Existing Documentation Review
Based on analysis of LightSpeed V4 and Program Manager documentation:

1. **LightSpeed VinMaster Capabilities**:
   - VinMaster vehicle specifications within LightSpeed response
   - 27 Symbol Table (One and Two Position variants)
   - 75 Symbol Table for detailed classification
   - Physical Damage symbols (Combined VSR, Comprehensive, Collision)
   - Located at: `Response.Body.CompleteQuote.Vehicles[].VinMaster`

2. **Program Manager Rating Architecture**:
   - Base rates defined for Comprehensive and Collision coverage
   - Factor grouping system for rating calculations
   - Section 9 - Physical Damage Symbol Factors with model year bands
   - Term-specific configurations (6-month, 12-month)

### Global Requirements Alignment
This initiative aligns with key Global Requirements:
- **GR-52**: Universal Entity Management - For managing LightSpeed as external entity
- **GR-48**: External Integrations Catalog - Apache Camel integration
- **GR-44**: Communication Architecture - API call tracking
- **GR-38**: Microservice Architecture - Service boundary compliance
- **GR-41**: Database Standards - Symbol mapping table design
- **GR-33**: Data Services & Caching - Symbol data storage strategy

### Integration Gap Analysis
- Program Manager currently lacks vehicle symbol-based rating factors
  - How do you get to this conclusion with section 9.3 defined?
  - ProgramManager/Documentation/PrelimRequirements/[III] Rating — Program Attributes 20ed4a7f4d16808d9e0cf88e41e8cc4c.md
- No existing integration with external symbol providers
  - Verisk LightSpeed VINMASTER is the external symbol proivder
- Physical damage rating uses static factors without vehicle-specific adjustments
  - Any and every vehicle will have a symbol returned from LightSpeed.
  - That symbol will then reference section 9.3 to determine the factor.
  - ProgramManager/Documentation/PrelimRequirements/[III] Rating — Program Attributes 20ed4a7f4d16808d9e0cf88e41e8cc4c.md
- Missing symbol-to-factor mapping configuration
  - How do you get to this conclusion with section 9.3 defined?
  - ProgramManager/Documentation/PrelimRequirements/[III] Rating — Program Attributes 20ed4a7f4d16808d9e0cf88e41e8cc4c.md

---

## Objectives

### Primary Goals
1. Integrate VinMaster physical damage symbols into Program Manager rating engine
2. Create configurable symbol-to-factor mapping tables aligned with Section 9 requirements
3. Enable real-time symbol lookup during quote/bind process
4. Store symbols in communication response or vehicle table
5. Provide program-specific symbol factor overrides with model year bands

### Expected Outcomes
- Enhanced physical damage rating accuracy using vehicle-specific symbols
- Reduced manual underwriting for symbol classification
- Automated symbol-based factor application
- Improved competitive positioning through precise vehicle rating
- Compliance with industry-standard symbol tables

---

## Scope and Approach

### In Scope
1. **VinMaster Symbol Integration**:
   - 27 Symbol Table (One Position)
   - 27 Symbol Table (Two Positions)
   - 75 Symbol Table
   - Physical Damage symbols (VSR, Comprehensive, Collision)
   - Direct VinMaster API integration for enhanced symbol lookup

2. **Program Manager Enhancements**:
   - Enhanced Section 9 - Physical Damage Symbol Factors
   - Symbol-to-factor mapping configuration with model year bands
   - Factor grouping modifications
   - Real-time integration during rating

3. **Data Management**:
   - Symbol storage in communication response or vehicle table field
   - Program-specific override capability per Section 9 - Physical Damage Symbol Factors
   - Missing symbol handling via Verisk default values or custom symbol creation
   - Custom symbol creation for missing/new vehicle models

### Out of Scope
- Liability symbol integration (future phase)
- Migration of historical symbol data from legacy systems

### Technical Approach
- Leverage existing LightSpeed integration for VinMaster data
- Implement direct VinMaster API integration as fallback
- Extend Program Manager factor tables for symbol-based rating
- Implement Universal Entity pattern for configuration
- Use Apache Camel for request routing

---

## Implementation Requirements

### Program Manager Configuration

#### Enhanced Section 9: Physical Damage Symbol Factors
```
Factor Type: Physical Damage Symbol Classification
Applies To: COMP, COLL
Configuration Level: Program-specific with model year bands
Model Year Bands: 2010 & prior, 2011 & over
```

#### Symbol Factor Tables
1. **27 Symbol Table Factors**:
   ```
   | Symbol | Symbol Description | Model Year Band | Round By | COMP Factor | COLL Factor | Terms | Supported |
   |--------|-------------------|-----------------|----------|-------------|-------------|-------|-----------|
   | 01     | Compact Car       | 2010 & prior    | 2        | 0.85        | 0.90        | 6,12  | On        |
   | 01     | Compact Car       | 2011 & over     | 2        | 0.82        | 0.87        | 6,12  | On        |
   | 02     | Mid-Size Car      | 2010 & prior    | 2        | 0.95        | 0.95        | 6,12  | On        |
   | 02     | Mid-Size Car      | 2011 & over     | 2        | 0.92        | 0.92        | 6,12  | On        |
   | ...    | ...               | ...             | ...      | ...         | ...         | ...   | ...       |
   ```

2. **75 Symbol Table Factors**:
   ```
   | Symbol | Symbol Description | Model Year Band | Round By | COMP Factor | COLL Factor | Terms | Supported |
   |--------|-------------------|-----------------|----------|-------------|-------------|-------|-----------|
   | 001    | Subcompact        | 2010 & prior    | 2        | 0.80        | 0.85        | 6,12  | On        |
   | 001    | Subcompact        | 2011 & over     | 2        | 0.78        | 0.83        | 6,12  | On        |
   | 002    | Compact           | 2010 & prior    | 2        | 0.85        | 0.90        | 6,12  | On        |
   | 002    | Compact           | 2011 & over     | 2        | 0.83        | 0.88        | 6,12  | On        |
   | ...    | ...               | ...             | ...      | ...         | ...         | ...   | ...       |
   ```

3. **Physical Damage Symbol Factors**:
   ```
   | Symbol Type | Symbol | Model Year Band | Round By | Factor | Terms | Supported |
   |-------------|--------|-----------------|----------|--------|-------|-----------|
   | VSR_One     | A      | 2010 & prior    | 2        | 0.95   | 6,12  | On        |
   | VSR_One     | A      | 2011 & over     | 2        | 0.93   | 6,12  | On        |
   | VSR_Two     | AA     | 2010 & prior    | 2        | 0.90   | 6,12  | On        |
   | VSR_Two     | AA     | 2011 & over     | 2        | 0.88   | 6,12  | On        |
   | COMP        | 1      | All Years       | 2        | 0.85   | 6,12  | On        |
   | COLL        | 1      | All Years       | 2        | 0.88   | 6,12  | On        |
   ```

### Integration Architecture

#### Data Flow
```yaml
quote_creation:
  1. vehicle_vin_entered:
     - trigger: VIN validation
     - action: Queue LightSpeed comprehensive request
  
  2. lightspeed_response:
     - extract: VinMaster symbols from response
     - store: Save symbols to vehicle record or communication response
     - proceed: Continue to rating
  
  3. rating_calculation:
     - lookup: Symbol factors from Program Manager config
     - apply: Multiply base rates by symbol factors
     - round: Apply program-specific rounding rules
```

#### Service Implementation
```php
class VehicleSymbolRatingService
{
    public function applySymbolFactors(Vehicle $vehicle, Program $program): array
    {
        // Get symbols from vehicle record or communication response
        $symbols = $vehicle->getPhysicalDamageSymbols() 
            ?? $this->getCommunicationSymbols($vehicle->vin);
        
        // Determine model year band
        $modelYearBand = $vehicle->year <= 2010 ? 'PRIOR_2010' : 'POST_2011';
        
        // Lookup program-specific symbol factors with model year band
        $symbolFactors = $this->programManager->getSymbolFactors(
            $program->id,
            $symbols,
            $modelYearBand
        );
        
        // Handle missing symbols
        if (empty($symbolFactors)) {
            $symbolFactors = $this->handleMissingSymbol($vehicle, $program);
        }
        
        // Apply factors to base rates
        return [
            'comp_adjustment' => $symbolFactors['comp_factor'] ?? 1.0,
            'coll_adjustment' => $symbolFactors['coll_factor'] ?? 1.0,
            'applied_symbols' => $symbols,
            'model_year_band' => $modelYearBand
        ];
    }
    
    private function handleMissingSymbol(Vehicle $vehicle, Program $program): array
    {
        // Check Verisk defaults
        $veriskDefaults = $this->getVeriskDefaultSymbols($vehicle);
        
        if ($veriskDefaults) {
            return $veriskDefaults;
        }
        
        // Create custom symbol if enabled
        if ($program->customSymbolCreationEnabled()) {
            return $this->createCustomSymbol($vehicle, $program);
        }
        
        // Return program defaults
        return $program->getDefaultSymbolFactors();
    }
}
```

### Database Schema

#### New Tables

##### vehicle_symbol_factors
```sql
CREATE TABLE vehicle_symbol_factors (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    program_id BIGINT UNSIGNED NOT NULL,
    symbol_table ENUM('27_ONE', '27_TWO', '75', 'VSR', 'COMP', 'COLL') NOT NULL,
    symbol_code VARCHAR(10) NOT NULL,
    symbol_description VARCHAR(255) NULL,
    model_year_band ENUM('PRIOR_2010', 'POST_2011', 'ALL') DEFAULT 'ALL',
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
    UNIQUE KEY unique_program_symbol (program_id, symbol_table, symbol_code, model_year_band),
    INDEX idx_symbol_lookup (symbol_table, symbol_code, model_year_band),
    
    -- Foreign keys
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```

##### Updated vehicle table columns
```sql
ALTER TABLE vehicle ADD COLUMN symbol_27_one VARCHAR(3) NULL;
ALTER TABLE vehicle ADD COLUMN symbol_27_two VARCHAR(3) NULL;
ALTER TABLE vehicle ADD COLUMN symbol_75 VARCHAR(3) NULL;
ALTER TABLE vehicle ADD COLUMN vsr_symbol_one VARCHAR(3) NULL;
ALTER TABLE vehicle ADD COLUMN vsr_symbol_two VARCHAR(3) NULL;
ALTER TABLE vehicle ADD COLUMN comp_symbol VARCHAR(3) NULL;
ALTER TABLE vehicle ADD COLUMN coll_symbol VARCHAR(3) NULL;
ALTER TABLE vehicle ADD COLUMN symbol_source ENUM('LIGHTSPEED', 'VINMASTER_DIRECT', 'CUSTOM') NULL;
ALTER TABLE vehicle ADD COLUMN symbol_updated_at TIMESTAMP NULL;

-- Index for symbol lookups
CREATE INDEX idx_vehicle_symbols ON vehicle(symbol_27_one, symbol_27_two, symbol_75);
```

##### custom_vehicle_symbols
```sql
CREATE TABLE custom_vehicle_symbols (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    program_id BIGINT UNSIGNED NOT NULL,
    year YEAR NOT NULL,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    symbol_27_one VARCHAR(3) NULL,
    symbol_27_two VARCHAR(3) NULL,
    symbol_75 VARCHAR(3) NULL,
    comp_symbol VARCHAR(3) NULL,
    coll_symbol VARCHAR(3) NULL,
    approval_status ENUM('PENDING', 'APPROVED', 'REJECTED') DEFAULT 'PENDING',
    approved_by BIGINT UNSIGNED NULL,
    approved_at TIMESTAMP NULL,
    
    -- Audit fields
    created_by BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_vehicle_lookup (year, make, model),
    INDEX idx_approval_status (approval_status),
    
    -- Foreign keys
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (approved_by) REFERENCES user(id)
);
```

### Configuration Management

#### Program-Level Settings
```yaml
program_configuration:
  vehicle_symbols:
    enabled: true
    symbol_tables:
      - type: "27_ONE"
        enabled: true
        default_factor: 1.00
      - type: "27_TWO"  
        enabled: true
        default_factor: 1.00
      - type: "75"
        enabled: false
        default_factor: 1.00
    fallback_behavior: "use_default_factor"
    custom_symbol_creation:
      enabled: true
      approval_required: true
    model_year_bands:
      - band: "PRIOR_2010"
        max_year: 2010
      - band: "POST_2011"
        min_year: 2011
    vinmaster_direct_api:
      enabled: true
      use_when: "lightspeed_unavailable"
```

---

## Integration Points

### Quote/Bind Workflow
1. VIN entry triggers LightSpeed lookup
2. Symbol extraction from VinMaster response
3. Store symbols in vehicle record
4. Symbol factor lookup in Program Manager with model year band
5. Factor application during rating calculation
6. Symbol data displayed in quote summary

### Endorsement Processing
- Re-fetch symbols if VIN changes
- Recalculate physical damage premiums
- Maintain symbol history for auditing

### Reporting Integration
- Symbol distribution reports by program
- Factor effectiveness analysis by model year band
- Custom symbol usage tracking

---

## Performance Requirements

### Response Times
- Symbol lookup from vehicle record: < 10ms
- LightSpeed API call (when needed): < 10 seconds
- Direct VinMaster API fallback: < 5 seconds
- Factor application: < 100ms additional overhead

### Data Storage Strategy
- Symbols stored directly on vehicle record
- Communication response includes symbol data
- No separate caching layer required
- Real-time updates when VIN changes

### Scalability
- Support 100+ concurrent symbol lookups
- Handle 50+ unique programs with custom factors
- Process 10,000+ quotes daily with symbol rating

---

## Risk Mitigation

### Technical Risks
1. **LightSpeed API Unavailability**
   - Mitigation: Direct VinMaster API fallback
   - Secondary: Use stored symbols or default factors

2. **Symbol Mapping Gaps**
   - Mitigation: Custom symbol creation workflow
   - Fallback: Verisk default values or program defaults
   - Monitoring: Alert on unmapped symbols for review

3. **Performance Impact**
   - Mitigation: Store symbols on vehicle record
   - Optimization: Batch symbol lookups

### Business Risks
1. **Factor Accuracy**
   - Mitigation: Phased rollout with A/B testing
   - Validation: Compare with current rating

2. **Program Adoption**
   - Mitigation: Optional per program
   - Training: Symbol factor configuration guide

---

## Next Steps After Approval

### Implementation Phases
1. **Phase 1: Infrastructure** (Week 1)
   - Update vehicle table schema
   - Implement direct VinMaster integration
   - Enhance Section 9 Program Manager UI

2. **Phase 2: Integration** (Week 2)
   - LightSpeed data extraction
   - Symbol factor engine with model year bands
   - Rating calculation updates

3. **Phase 3: Configuration** (Week 3)
   - Program-specific setup
   - Custom symbol workflow
   - Testing and validation

4. **Phase 4: Rollout** (Week 4)
   - Pilot program activation
   - Monitoring and adjustments
   - Full deployment

### Success Metrics
- 95% symbol match rate
- < 3% rating calculation time increase
- 100% symbol availability (via custom creation)
- Zero rating errors due to symbols

---

## Approval Required

**This plan requires approval before proceeding with detailed requirements generation.**

Once approved, the multi-agent system will:
1. Generate detailed technical requirements
2. Create API integration specifications
3. Define Program Manager UI enhancements
4. Establish testing scenarios
5. Document operational procedures

### Review Checklist
- [ ] Symbol tables align with Section 9 requirements
- [ ] Model year band approach approved
- [ ] Custom symbol creation process acceptable
- [ ] Direct API integration approach approved
- [ ] Rollout timeline acceptable

---

**Note**: This plan focuses on VinMaster physical damage symbols with enhancements for model year bands and custom symbol handling. Liability symbols and other rating factors will be addressed in separate initiatives.