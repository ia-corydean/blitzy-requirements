# LightSpeed VinMaster Symbols - Program Manager Integration Plan

**Status:** DRAFT - Awaiting Approval  
**Date:** 2025-01-08  
**Version:** 4.0  
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

### Integration Requirements
This plan outlines what's needed to connect LightSpeed VinMaster data to the existing Section 9.3 Physical Damage Symbol Factors:
- **Automated symbol retrieval** during Rate/Quote/Bind process
- **Symbol storage** in vehicle table for rating calculations
- **Factor application** using existing Section 9.3 configuration

---

## Objectives

### Primary Goals
1. **Implement the existing Section 9.3** Physical Damage Symbol Factors with LightSpeed VinMaster integration
2. Enable automated symbol retrieval from LightSpeed comprehensive response during Rate/Quote/Bind
3. Store symbols in vehicle table for rating calculations
4. Apply symbol factors based on model year bands as defined in Section 9.3

### Expected Outcomes
- Fully functional Section 9.3 implementation
- Automated symbol-based physical damage rating
- Zero manual symbol entry
- Improved rating accuracy using actual VinMaster data

---

## Scope and Approach

### In Scope
1. **VinMaster Symbol Integration**:
   - Implement Section 9.1 - Retrieve Vehicle Symbol via LightSpeed
   - Extract symbols from LightSpeed comprehensive response
   - Store symbols in vehicle table

2. **Program Manager Implementation**:
   - Implement Section 9.2 - Model Year Band determination
   - Implement Section 9.3 - Factor lookup by coverage
   - Enable real-time symbol factor application during rating

3. **Data Management**:
   - Symbol storage in vehicle table
   - Symbol source tracking for audit

### Out of Scope
- Direct VinMaster API integration (no separate API documentation available)
- Custom symbol creation (Verisk provides best match for all vehicles)
- Liability symbol integration (future phase)
- Migration of historical symbol data
- Modification of existing Section 9.3 table structure

### Technical Approach
- Extract symbols from LightSpeed comprehensive response during Rate/Quote/Bind
- Store symbols directly in vehicle table
- Use existing model year band logic (2010 & prior vs 2011 & over)
- Apply factors from Section 9.3 configuration

---

## Implementation Requirements

### Program Manager Configuration

#### Section 9.3 Implementation Details

The existing Section 9.3 table structure will be implemented with:
- Automated symbol retrieval from LightSpeed VinMaster
- Model year band calculation based on vehicle year
- Factor application to COMP, COLL, and UMPD coverages

#### Symbol Data Source
**LightSpeed comprehensive response** (during Rate/Quote/Bind):
- Path: `Response.Body.CompleteQuote.Vehicles[].VinMaster`
- Includes all symbol types
- Verisk provides best matching symbol for all vehicles

### Integration Architecture

#### Data Flow
```yaml
rate_quote_bind_process:
  1. vehicle_vin_entered:
     - trigger: VIN validation
     - action: Queue LightSpeed comprehensive request
  
  2. lightspeed_response_processing:
     - extract: VinMaster symbols from response
     - store: Save symbols to vehicle record
     - note: Verisk always returns appropriate symbol
  
  3. rating_calculation:
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
        // Get symbols from vehicle record (populated during LightSpeed processing)
        $symbol = $vehicle->physical_damage_symbol;
        
        if (!$symbol) {
            throw new RatingException('Physical damage symbol not found for vehicle');
        }
        
        // Implement Section 9.2 - Determine Model Year Band
        $modelYearBand = $vehicle->year <= 2010 ? 'PRIOR_2010' : 'POST_2011';
        
        // Implement Section 9.3 - Lookup Factor by Coverage
        $symbolFactors = $this->getSection93Factors(
            $program->id,
            $symbol,
            $modelYearBand
        );
        
        // Apply factors to base rates
        return [
            'comp_factor' => $symbolFactors['comp_factor'] ?? 1.0,
            'coll_factor' => $symbolFactors['coll_factor'] ?? 1.0,
            'umpd_factor' => $symbolFactors['umpd_factor'] ?? 1.0,
            'symbol_used' => $symbol,
            'model_year_band' => $modelYearBand
        ];
    }
}

class LightSpeedResponseProcessor
{
    public function processVehicleData(array $lightspeedVehicle, Vehicle $vehicle): void
    {
        // Extract VinMaster data
        $vinMaster = $lightspeedVehicle['VinMaster'] ?? [];
        
        // Store physical damage symbol (Verisk provides appropriate symbol)
        $vehicle->physical_damage_symbol = $vinMaster['PhysicalDamageSymbol'] ?? null;
        
        // Store additional symbols for reference
        $vehicle->symbol_27_one = $vinMaster['Symbol27One'] ?? null;
        $vehicle->symbol_27_two = $vinMaster['Symbol27Two'] ?? null;
        $vehicle->symbol_75 = $vinMaster['Symbol75'] ?? null;
        
        // Track source
        $vehicle->symbol_source = 'LIGHTSPEED';
        $vehicle->symbol_updated_at = now();
        
        $vehicle->save();
    }
}
```

### Database Schema

#### Updated vehicle table columns
```sql
-- Add symbol storage columns to existing vehicle table
ALTER TABLE vehicle ADD COLUMN physical_damage_symbol VARCHAR(3) NULL COMMENT 'Symbol from Section 9.3';
ALTER TABLE vehicle ADD COLUMN symbol_27_one VARCHAR(3) NULL COMMENT 'VinMaster 27 Symbol (One Position)';
ALTER TABLE vehicle ADD COLUMN symbol_27_two VARCHAR(3) NULL COMMENT 'VinMaster 27 Symbol (Two Positions)';
ALTER TABLE vehicle ADD COLUMN symbol_75 VARCHAR(3) NULL COMMENT 'VinMaster 75 Symbol';
ALTER TABLE vehicle ADD COLUMN symbol_source ENUM('LIGHTSPEED', 'MANUAL') DEFAULT 'LIGHTSPEED';
ALTER TABLE vehicle ADD COLUMN symbol_updated_at TIMESTAMP NULL;

-- Index for symbol lookups
CREATE INDEX idx_vehicle_symbols ON vehicle(physical_damage_symbol, symbol_updated_at);
```

### Configuration Management

#### Program-Level Settings
```yaml
program_configuration:
  section_9_physical_damage_symbols:
    enabled: true
    symbol_retrieval:
      source: "lightspeed_vinmaster"
    manual_override:
      # Per Section 9.3 note: "Manual symbol overrides should be restricted"
      enabled: false
      requires_approval: true
```

---

## Integration Points

### Quote/Bind Workflow
1. VIN entry triggers LightSpeed comprehensive request
2. VinMaster symbols extracted from response and stored
3. Section 9.2 model year band determination
4. Section 9.3 factor lookup and application
5. Rating calculation with symbol factors

### Endorsement Processing
- Re-fetch symbols if VIN changes
- Recalculate physical damage premiums
- Maintain symbol history for auditing

### Reporting Integration
- Symbol distribution by model year band
- Symbol coverage reports

---

## Performance Requirements

### Response Times
- Symbol lookup from vehicle record: < 10ms
- LightSpeed API call: Per existing Rate/Quote/Bind process
- Factor application: < 50ms

### Data Storage Strategy
- Symbols stored directly on vehicle record
- No separate caching required
- Updated during each LightSpeed call

### Scalability
- Support existing quote volume
- Handle batch processing for renewals

---

## Risk Mitigation

### Technical Risks
1. **LightSpeed Response Missing Symbol**
   - Mitigation: Log and alert, use default factor of 1.0
   - Note: Verisk typically provides symbol for all vehicles

2. **Performance Impact**
   - Mitigation: Minimal - symbols extracted during existing LightSpeed call
   - Storage: Direct on vehicle record

### Business Risks
1. **Factor Accuracy**
   - Mitigation: Use existing Section 9.3 factors
   - Validation: Compare with any current manual process

2. **Manual Override Restrictions**
   - Mitigation: Follow Section 9.3 note on restrictions
   - Control: Disabled by default

---

## Next Steps After Approval

### Implementation Phases
1. **Phase 1: Infrastructure** (Week 1)
   - Update vehicle table schema
   - Implement LightSpeed response processor for symbols
   - Connect to existing Section 9.3 configuration

2. **Phase 2: Integration** (Week 2)
   - LightSpeed VinMaster data extraction
   - Section 9.2/9.3 automation
   - Rating engine updates

3. **Phase 3: Testing** (Week 3)
   - Test with various vehicle types
   - Verify model year band logic
   - Validate factor application

4. **Phase 4: Rollout** (Week 4)
   - Pilot program testing
   - Performance monitoring
   - Full deployment

### Success Metrics
- 100% automated symbol retrieval from LightSpeed
- Zero manual symbol entry required
- Accurate factor application per Section 9.3
- No significant performance impact

---

## Approval Required

**This plan requires approval before proceeding with detailed requirements generation.**

Once approved, the multi-agent system will:
1. Generate detailed technical requirements
2. Create LightSpeed integration specifications
3. Define symbol extraction workflows
4. Establish testing scenarios
5. Document operational procedures

### Review Checklist
- [ ] Implementation aligns with existing Section 9.3
- [ ] LightSpeed symbol extraction approach approved
- [ ] Vehicle table schema changes acceptable
- [ ] Timeline achievable

---

**Note**: This plan implements the existing Section 9 - Physical Damage Symbol Factors from Program Manager documentation, automating the integration with LightSpeed VinMaster data that is already available in the comprehensive response during the Rate/Quote/Bind process.