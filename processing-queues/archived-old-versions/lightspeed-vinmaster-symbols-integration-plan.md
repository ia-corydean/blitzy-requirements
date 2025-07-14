# LightSpeed VinMaster Symbols - Program Manager Integration Plan

**Status:** DRAFT - Awaiting Approval  
**Date:** 2025-01-08  
**Version:** 1.0  
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
   - Global rounding controls for precision
   - Term-specific configurations (6-month, 12-month)

### Global Requirements Alignment
This initiative aligns with key Global Requirements:
- **GR-52**: Universal Entity Management - For managing LightSpeed as external entity
- **GR-48**: External Integrations Catalog - Apache Camel integration
- **GR-44**: Communication Architecture - API call tracking
- **GR-38**: Microservice Architecture - Service boundary compliance
- **GR-41**: Database Standards - Symbol mapping table design
- **GR-33**: Data Services & Caching - Symbol data caching strategy

### Integration Gap Analysis
- Program Manager currently lacks vehicle symbol-based rating factors
- No existing integration with external symbol providers
- Physical damage rating uses static factors without vehicle-specific adjustments
- Missing symbol-to-factor mapping configuration

---

## Objectives

### Primary Goals
1. Integrate VinMaster physical damage symbols into Program Manager rating engine
2. Create configurable symbol-to-factor mapping tables
3. Enable real-time symbol lookup during quote/bind process
4. Implement caching strategy for symbol data (7-day TTL)
5. Provide program-specific symbol factor overrides

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

2. **Program Manager Enhancements**:
   - New Vehicle Symbol factor category
   - Symbol-to-factor mapping configuration
   - Factor grouping modifications
   - Real-time integration during rating
     - see 9 — Physical Damage Symbol Factors in Aime/workspace/requirements/ProgramManager/Documentation/PrelimRequirements/[III] Rating — Program Attributes 20ed4a7f4d16808d9e0cf88e41e8cc4c.md

3. **Data Management**:
   - Symbol caching with 7-day TTL
     - There should be no caching. The symbol will be in the communication response or a field on the vehicle table that represents the symbol.
   - Program-specific override capability
     - see 9 — Physical Damage Symbol Factors in Aime/workspace/requirements/ProgramManager/Documentation/PrelimRequirements/[III] Rating — Program Attributes 20ed4a7f4d16808d9e0cf88e41e8cc4c.md
   - Fallback handling for missing symbols
     - Does verisk have a solution for this within their process?

### Out of Scope
- Liability symbol integration (future phase)
- Historical symbol migration
  - What do you mean?
- Custom symbol creation
  - We may need to do this if Verisk does not provide a good way to handle scenarios where symbols are not available.
- Direct VinMaster API integration (using LightSpeed aggregation)
  - Why would we not do this?

### Technical Approach
- Leverage existing LightSpeed integration for VinMaster data
- Extend Program Manager factor tables for symbol-based rating
- Implement Universal Entity pattern for configuration
- Use Apache Camel for request routing

---

## Implementation Requirements

### Program Manager Configuration

#### New Factor Category: Vehicle Symbols
```
Factor Type: Vehicle Symbol Classification
Applies To: COMP, COLL
Configuration Level: Program-specific with system defaults
```

#### Symbol Factor Tables
1. **27 Symbol Table Factors**:
   ```
   | Symbol | Symbol Description | Round By | COMP Factor | COLL Factor | Terms | Supported |
   |--------|-------------------|----------|-------------|-------------|-------|-----------|
   | 01     | Compact Car       | 2        | 0.85        | 0.90        | 6,12  | On        |
   | 02     | Mid-Size Car      | 2        | 0.95        | 0.95        | 6,12  | On        |
   | ...    | ...               | ...      | ...         | ...         | ...   | ...       |
   ```

2. **75 Symbol Table Factors**:
   ```
   | Symbol | Symbol Description | Round By | COMP Factor | COLL Factor | Terms | Supported |
   |--------|-------------------|----------|-------------|-------------|-------|-----------|
   | 001    | Subcompact        | 2        | 0.80        | 0.85        | 6,12  | On        |
   | 002    | Compact           | 2        | 0.85        | 0.90        | 6,12  | On        |
   | ...    | ...               | ...      | ...         | ...         | ...   | ...       |
   ```

3. **Physical Damage Symbol Factors**:
   ```
   | Symbol Type | Symbol | Round By | Factor | Terms | Supported |
   |-------------|--------|----------|--------|-------|-----------|
   | VSR_One     | A      | 2        | 0.95   | 6,12  | On        |
   | VSR_Two     | AA     | 2        | 0.90   | 6,12  | On        |
   | COMP        | 1      | 2        | 0.85   | 6,12  | On        |
   | COLL        | 1      | 2        | 0.88   | 6,12  | On        |
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
     - cache: Store symbols with 7-day TTL
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
        // Get cached symbols from LightSpeed response
        $symbols = $this->getVehicleSymbols($vehicle->vin);
        
        // Lookup program-specific symbol factors
        $symbolFactors = $this->programManager->getSymbolFactors(
            $program->id,
            $symbols
        );
        
        // Apply factors to base rates
        return [
            'comp_adjustment' => $symbolFactors['comp_factor'] ?? 1.0,
            'coll_adjustment' => $symbolFactors['coll_factor'] ?? 1.0,
            'applied_symbols' => $symbols
        ];
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
    UNIQUE KEY unique_program_symbol (program_id, symbol_table, symbol_code),
    INDEX idx_symbol_lookup (symbol_table, symbol_code),
    
    -- Foreign keys
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```

##### vehicle_symbol_cache
```sql
CREATE TABLE vehicle_symbol_cache (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    vin VARCHAR(25) NOT NULL,
    symbol_27_one VARCHAR(3) NULL,
    symbol_27_two VARCHAR(3) NULL,
    symbol_75 VARCHAR(3) NULL,
    vsr_symbol_one VARCHAR(3) NULL,
    vsr_symbol_two VARCHAR(3) NULL,
    comp_symbol VARCHAR(3) NULL,
    coll_symbol VARCHAR(3) NULL,
    raw_vinmaster_data JSON NULL,
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    
    -- Indexes
    UNIQUE KEY unique_vin (vin),
    INDEX idx_expires (expires_at)
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
    cache_ttl_days: 7
```

---

## Integration Points

### Quote/Bind Workflow
1. VIN entry triggers LightSpeed lookup (if not cached)
2. Symbol extraction from VinMaster response
3. Symbol factor lookup in Program Manager
4. Factor application during rating calculation
5. Symbol data displayed in quote summary

### Endorsement Processing
- Re-fetch symbols if VIN changes
- Recalculate physical damage premiums
- Maintain symbol history for auditing

### Reporting Integration
- Symbol distribution reports by program
- Factor effectiveness analysis
- Cache hit rate monitoring

---

## Performance Requirements

### Response Times
- Symbol lookup from cache: < 50ms
- LightSpeed API call (when needed): < 10 seconds
- Factor application: < 100ms additional overhead

### Caching Strategy
- 7-day TTL for VinMaster symbols (vehicle specs stable)
- Warm cache during off-peak hours
- Program-specific cache invalidation

### Scalability
- Support 100+ concurrent symbol lookups
- Handle 50+ unique programs with custom factors
- Process 10,000+ quotes daily with symbol rating

---

## Risk Mitigation

### Technical Risks
1. **LightSpeed API Unavailability**
   - Mitigation: Use cached data or default factors
   - Fallback: Manual symbol entry option

2. **Symbol Mapping Gaps**
   - Mitigation: Default factor for unknown symbols
   - Monitoring: Alert on unmapped symbols

3. **Performance Impact**
   - Mitigation: Aggressive caching strategy
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
   - Create database tables
   - Implement caching service
   - Basic Program Manager UI

2. **Phase 2: Integration** (Week 2)
   - LightSpeed data extraction
   - Symbol factor engine
   - Rating calculation updates

3. **Phase 3: Configuration** (Week 3)
   - Program-specific setup
   - Testing and validation
   - Performance optimization

4. **Phase 4: Rollout** (Week 4)
   - Pilot program activation
   - Monitoring and adjustments
   - Full deployment

### Success Metrics
- 95% symbol match rate
- < 3% rating calculation time increase
- 80% cache hit rate
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
- [ ] Symbol tables align with business needs
- [ ] Factor ranges acceptable for rating
- [ ] Performance requirements achievable
- [ ] Integration approach approved
- [ ] Rollout timeline acceptable

---

**Note**: This plan focuses on VinMaster physical damage symbols. Liability symbols and other rating factors will be addressed in separate initiatives.