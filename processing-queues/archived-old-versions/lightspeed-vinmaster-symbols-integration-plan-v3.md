# LightSpeed VinMaster Symbols - Program Manager Integration Plan

**Status:** DRAFT - Awaiting Approval  
**Date:** 2025-01-08  
**Version:** 3.0  
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
   - **Section 9 - Physical Damage Symbol Factors already exists** with:
     - Model year bands (2010 & prior vs 2011 & over)
     - Symbol-to-factor mapping table
     - Support for COMP, COLL, and UMPD factors
     - Verisk VINMASTER integration mentioned
   - Factor grouping system for rating calculations
   - Term-specific configurations (6-month, 12-month)

### Global Requirements Alignment
This initiative aligns with key Global Requirements:
- **GR-52**: Universal Entity Management - For managing LightSpeed as external entity
- **GR-48**: External Integrations Catalog - Apache Camel integration
- **GR-44**: Communication Architecture - API call tracking
- **GR-38**: Microservice Architecture - Service boundary compliance
- **GR-41**: Database Standards - Symbol storage design
- **GR-33**: Data Services & Caching - Symbol data storage strategy

### Integration Gap Analysis
- **Section 9.3 Physical Damage Symbol Factors exists** but lacks implementation details
- No actual integration with LightSpeed VinMaster data
  - This is the purpose of these requirements.
  - To outline what's needed for integration.
- Symbol retrieval process not automated
  - This will happen when LightSpeed is ran in Rate Quote Bind
- Missing direct VinMaster API fallback option
  - Do we have this documentaion?
- No custom symbol handling for unmapped vehicles
  - Does the LightSpeed / Verisk services account for this and proivde the best matching symbol, regardless?

---

## Objectives

### Primary Goals
1. **Implement the existing Section 9.3** Physical Damage Symbol Factors with LightSpeed VinMaster integration
2. Enable automated symbol retrieval from LightSpeed comprehensive response
3. Store symbols in vehicle table for rating calculations
4. Provide direct VinMaster API integration as fallback
5. Handle missing symbols through Verisk defaults or custom creation

### Expected Outcomes
- Fully functional Section 9.3 implementation
- Automated symbol-based physical damage rating
- Reduced manual symbol entry
- Improved rating accuracy using actual VinMaster data
- Complete symbol coverage including edge cases

---

## Scope and Approach

### In Scope
1. **VinMaster Symbol Integration**:
   - Implement Section 9.1 - Retrieve Vehicle Symbol via LightSpeed
   - Support all symbol tables mentioned in documentation
   - Direct VinMaster API integration for enhanced symbol lookup
   - Automated symbol extraction and storage

2. **Program Manager Implementation**:
   - Implement Section 9.2 - Model Year Band determination
   - Implement Section 9.3 - Factor lookup by coverage
   - Enable real-time symbol factor application
   - Support manual symbol overrides (restricted per documentation)

3. **Data Management**:
   - Symbol storage in vehicle table
   - Missing symbol handling via Verisk defaults
   - Custom symbol creation for unmapped vehicles
   - Symbol source tracking

### Out of Scope
- Liability symbol integration (future phase)
- Migration of historical symbol data from legacy systems
- Modification of existing Section 9.3 table structure

### Technical Approach
- Implement Section 9.3 using LightSpeed VinMaster data
- Store symbols directly in vehicle table
- Use existing model year band logic (2010 & prior vs 2011 & over)
- Implement direct VinMaster API as fallback

---

## Implementation Requirements

### Program Manager Configuration

#### Section 9.3 Implementation Details

The existing Section 9.3 table structure will be implemented with:
- Automated symbol retrieval from LightSpeed VinMaster
- Model year band calculation based on vehicle year
- Factor application to COMP, COLL, and UMPD coverages

#### Symbol Data Sources
1. **Primary**: LightSpeed comprehensive response
   - Path: `Response.Body.CompleteQuote.Vehicles[].VinMaster`
   - Includes all symbol types

2. **Fallback**: Direct VinMaster API
   - Used when LightSpeed unavailable
   - Provides same symbol data

3. **Default**: Verisk default symbols
   - For unmapped vehicles
   - Based on make/model/year

### Integration Architecture

#### Data Flow
```yaml
quote_creation:
  1. vehicle_vin_entered:
     - trigger: VIN validation
     - action: Queue LightSpeed comprehensive request
  
  2. lightspeed_response:
     - extract: VinMaster symbols from response
     - store: Save symbols to vehicle record
     - proceed: Continue to rating
  
  3. symbol_retrieval_fallback:
     - condition: LightSpeed unavailable or missing symbols
     - action: Direct VinMaster API call
     - store: Save symbols to vehicle record
  
  4. rating_calculation:
     - determine: Model year band (2010 & prior vs 2011 & over)
     - lookup: Symbol factors from Section 9.3 table
     - apply: Multiply base rates by COMP, COLL, UMPD factors
     - round: Apply program-specific rounding rules
```

#### Service Implementation
```php
class VehicleSymbolRatingService
{
    public function applySymbolFactors(Vehicle $vehicle, Program $program): array
    {
        // Get symbols from vehicle record
        $symbols = $this->getVehicleSymbols($vehicle);
        
        // If symbols not available, retrieve them
        if (!$symbols) {
            $symbols = $this->retrieveSymbols($vehicle);
        }
        
        // Implement Section 9.2 - Determine Model Year Band
        $modelYearBand = $vehicle->year <= 2010 ? 'PRIOR_2010' : 'POST_2011';
        
        // Implement Section 9.3 - Lookup Factor by Coverage
        $symbolFactors = $this->getSection93Factors(
            $program->id,
            $symbols->physicalDamageSymbol,
            $modelYearBand
        );
        
        // Handle missing symbols per Section 9.1
        if (!$symbolFactors) {
            $symbolFactors = $this->handleMissingSymbol($vehicle, $program);
        }
        
        // Apply factors to base rates
        return [
            'comp_factor' => $symbolFactors['comp_factor'] ?? 1.0,
            'coll_factor' => $symbolFactors['coll_factor'] ?? 1.0,
            'umpd_factor' => $symbolFactors['umpd_factor'] ?? 1.0,
            'symbol_used' => $symbols->physicalDamageSymbol,
            'model_year_band' => $modelYearBand,
            'source' => $symbols->source
        ];
    }
    
    private function retrieveSymbols(Vehicle $vehicle): ?VehicleSymbols
    {
        // Try LightSpeed first
        $lightspeedSymbols = $this->lightSpeedService->getVinMasterData($vehicle->vin);
        
        if ($lightspeedSymbols) {
            $this->storeSymbolsOnVehicle($vehicle, $lightspeedSymbols, 'LIGHTSPEED');
            return $lightspeedSymbols;
        }
        
        // Fallback to direct VinMaster API
        $vinmasterSymbols = $this->vinMasterService->getSymbols($vehicle->vin);
        
        if ($vinmasterSymbols) {
            $this->storeSymbolsOnVehicle($vehicle, $vinmasterSymbols, 'VINMASTER_DIRECT');
            return $vinmasterSymbols;
        }
        
        return null;
    }
}
```

### Database Schema

#### Updated vehicle table columns
```sql
-- Add symbol storage columns to existing vehicle table
ALTER TABLE vehicle ADD COLUMN physical_damage_symbol VARCHAR(3) NULL COMMENT 'Symbol from Section 9.3';
ALTER TABLE vehicle ADD COLUMN symbol_27_one VARCHAR(3) NULL;
ALTER TABLE vehicle ADD COLUMN symbol_27_two VARCHAR(3) NULL;
ALTER TABLE vehicle ADD COLUMN symbol_75 VARCHAR(3) NULL;
ALTER TABLE vehicle ADD COLUMN vsr_symbol_one VARCHAR(3) NULL;
ALTER TABLE vehicle ADD COLUMN vsr_symbol_two VARCHAR(3) NULL;
ALTER TABLE vehicle ADD COLUMN comp_symbol VARCHAR(3) NULL;
ALTER TABLE vehicle ADD COLUMN coll_symbol VARCHAR(3) NULL;
ALTER TABLE vehicle ADD COLUMN symbol_source ENUM('LIGHTSPEED', 'VINMASTER_DIRECT', 'CUSTOM', 'DEFAULT') NULL;
ALTER TABLE vehicle ADD COLUMN symbol_updated_at TIMESTAMP NULL;

-- Index for symbol lookups
CREATE INDEX idx_vehicle_symbols ON vehicle(physical_damage_symbol, symbol_updated_at);
```

#### Custom symbol handling table
```sql
-- For vehicles not found in VinMaster
CREATE TABLE custom_vehicle_symbols (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    program_id BIGINT UNSIGNED NOT NULL,
    year YEAR NOT NULL,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    physical_damage_symbol VARCHAR(3) NOT NULL,
    approval_status ENUM('PENDING', 'APPROVED', 'REJECTED') DEFAULT 'PENDING',
    approved_by BIGINT UNSIGNED NULL,
    approved_at TIMESTAMP NULL,
    notes TEXT NULL,
    
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
  section_9_physical_damage_symbols:
    enabled: true
    symbol_retrieval:
      primary_source: "lightspeed"
      enable_vinmaster_direct: true
      enable_custom_symbols: true
    manual_override:
      # Per Section 9.3 note: "Manual symbol overrides should be restricted"
      enabled: false
      requires_approval: true
    missing_symbol_handling:
      use_verisk_defaults: true
      allow_custom_creation: true
      default_factor: 1.00
```

---

## Integration Points

### Quote/Bind Workflow
1. VIN entry triggers LightSpeed lookup
2. VinMaster symbols extracted and stored
3. Section 9.2 model year band determination
4. Section 9.3 factor lookup and application
5. Rating calculation with symbol factors

### Endorsement Processing
- Re-fetch symbols if VIN changes
- Recalculate physical damage premiums
- Maintain symbol history for auditing

### Reporting Integration
- Symbol distribution by model year band
- Missing symbol reports
- Custom symbol usage tracking

---

## Performance Requirements

### Response Times
- Symbol lookup from vehicle record: < 10ms
- LightSpeed API call: Per existing SLA
- Direct VinMaster API: < 5 seconds
- Factor application: < 50ms

### Data Storage Strategy
- Symbols stored directly on vehicle record
- No separate caching required
- Real-time updates when VIN changes

### Scalability
- Support existing quote volume
- Handle batch symbol updates
- Process concurrent API calls

---

## Risk Mitigation

### Technical Risks
1. **LightSpeed API Unavailability**
   - Mitigation: Direct VinMaster API fallback
   - Secondary: Use stored symbols or Verisk defaults

2. **Symbol Mapping Gaps**
   - Mitigation: Verisk default values
   - Fallback: Custom symbol creation workflow
   - Monitoring: Alert on unmapped symbols

3. **Performance Impact**
   - Mitigation: Store symbols on vehicle record
   - Optimization: Batch processing for renewals

### Business Risks
1. **Factor Accuracy**
   - Mitigation: Use existing Section 9.3 factors
   - Validation: Compare with current manual process

2. **Manual Override Restrictions**
   - Mitigation: Follow Section 9.3 note on restrictions
   - Control: Approval workflow if enabled

---

## Next Steps After Approval

### Implementation Phases
1. **Phase 1: Infrastructure** (Week 1)
   - Update vehicle table schema
   - Implement symbol retrieval services
   - Connect to existing Section 9.3 configuration

2. **Phase 2: Integration** (Week 2)
   - LightSpeed VinMaster data extraction
   - Direct VinMaster API implementation
   - Section 9.2/9.3 automation

3. **Phase 3: Configuration** (Week 3)
   - Program-specific settings
   - Missing symbol workflows
   - Testing with Section 9.3 factors

4. **Phase 4: Rollout** (Week 4)
   - Pilot program testing
   - Performance monitoring
   - Full deployment

### Success Metrics
- 100% automated symbol retrieval
- Zero manual symbol entry required
- < 3% rating calculation time increase
- Complete symbol coverage (including custom)

---

## Approval Required

**This plan requires approval before proceeding with detailed requirements generation.**

Once approved, the multi-agent system will:
1. Generate detailed technical requirements
2. Create API integration specifications
3. Define symbol retrieval workflows
4. Establish testing scenarios
5. Document operational procedures

### Review Checklist
- [ ] Implementation aligns with existing Section 9.3
- [ ] Symbol retrieval approach approved
- [ ] Missing symbol handling acceptable
- [ ] Direct API integration approved
- [ ] Timeline achievable

---

**Note**: This plan implements the existing Section 9 - Physical Damage Symbol Factors from Program Manager documentation, adding the automated integration with LightSpeed VinMaster that was missing from the current implementation.