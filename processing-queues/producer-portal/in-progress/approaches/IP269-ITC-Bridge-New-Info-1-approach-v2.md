# IP269-ITC-Bridge-New-Info-1 - Implementation Approach v2

## Revision Notes
- **v2 Changes**: Updated to use driver.source_entity_id instead of driver.lookup_source
- **Key Updates**: Leverages entity pattern for tracking data source

## Requirement Understanding
The ITC Bridge New Info Option 1 handles scenarios where external data enrichment discovers additional drivers not initially declared in the quote. The system must display alerts about newly discovered drivers, automatically set them as excluded, allow producers to modify their inclusion status, capture required information for included drivers, and update premium calculations accordingly. This ensures compliance with household member disclosure requirements.

## Domain Classification
- Primary Domain: Producer Portal / Quote Management
- Cross-Domain Impact: Yes - Affects underwriting, rating, compliance
- Complexity Level: Medium

## Pattern Analysis

### Reusable Patterns Identified
- [GR-69]: Producer Portal Architecture - Data enrichment patterns
- [GR-53]: DCS Integration Architecture - External data verification
- [GR-52]: Universal Entity Management - Driver entity handling
- [GR-44]: Communication Architecture - Alert notifications
- [GR-20]: Business Logic Standards - Inclusion/exclusion rules

### Domain-Specific Needs
- External data bridge integration
- Automatic driver discovery
- Default exclusion setting
- Inline alert banners
- Side panel editing
- Premium recalculation triggers
- Compliance tracking

## Proposed Implementation

### Simplification Approach
- Current Complexity: External data integration, dynamic driver addition
- Simplified Solution: Use existing driver infrastructure with entity source tracking
- Trade-offs: Need to ensure entity records exist for external sources

### Technical Approach
1. **Phase 1**: Bridge Data Reception
   - [ ] Receive external data response
   - [ ] Parse discovered drivers
   - [ ] Match against existing drivers
   - [ ] Identify new discoveries
   - [ ] Store bridge results

2. **Phase 2**: Source Entity Setup
   - [ ] Create/retrieve ITC entity
   - [ ] Set entity_type as 'integration'
   - [ ] Store bridge metadata
   - [ ] Get entity_id for reference
   - [ ] Link to verification

3. **Phase 3**: Driver Creation
   - [ ] Create driver records for new
   - [ ] Set is_excluded = true default
   - [ ] Set source_entity_id to ITC
   - [ ] Link to quote
   - [ ] Preserve discovery metadata

4. **Phase 4**: Alert Display
   - [ ] Query drivers by source_entity_id
   - [ ] Show inline banner
   - [ ] Highlight bridge discoveries
   - [ ] Count new drivers found
   - [ ] Enable edit actions

5. **Phase 5**: Edit Flow
   - [ ] Open side panel on edit
   - [ ] Allow inclusion toggle
   - [ ] Show required fields
   - [ ] Validate included drivers
   - [ ] Update driver record

6. **Phase 6**: Premium Impact
   - [ ] Detect inclusion changes
   - [ ] Trigger rating recalc
   - [ ] Update premium display
   - [ ] Show price difference
   - [ ] Maintain calculation audit

7. **Phase 7**: Navigation
   - [ ] Allow return to Step 2
   - [ ] Preserve bridge data
   - [ ] Maintain alert state
   - [ ] Handle bulk updates
   - [ ] Return to review

## Risk Assessment
- **Risk 1**: Data quality from bridge → Mitigation: Validation, manual override
- **Risk 2**: Premium calculation errors → Mitigation: Comprehensive testing
- **Risk 3**: Compliance violations → Mitigation: Audit trail, disclosures
- **Risk 4**: User confusion → Mitigation: Clear alerts, help text
- **Risk 5**: Performance impact → Mitigation: Async processing
- **Risk 6**: Entity reference integrity → Mitigation: Ensure entity exists

## Context Preservation
- Key Decisions: Use source_entity_id for tracking, default to excluded
- Dependencies: Entity management, external data service, rating engine
- Future Impact: Foundation for tracking any external data source

## Database Requirements Summary
- **New Tables**: 0 tables need to be created
- **Existing Tables**: 6+ tables will be reused
- **Modified Tables**: 0 tables need modifications (driver already has source_entity_id)

## Database Schema Analysis

### Existing Tables to Use

1. **driver**: Store discovered drivers
   - Use is_excluded flag for default exclusion
   - Use source_entity_id to track ITC source
   - Track all driver information
   - Link to quote via map_quote_driver

2. **entity**: Source tracking
   - Create/use ITC entity record
   - entity_type_id = 'integration'
   - Store integration metadata
   - Provides source_entity_id

3. **entity_type**: Entity categorization
   - Has 'integration' type
   - Defines external sources
   - Controls entity behavior

4. **map_quote_driver**: Quote-driver links
   - Associate new drivers
   - Track inclusion status
   - Maintain relationships

5. **verification**: Bridge results
   - Store external data response
   - Track verification source
   - Link discovered entities
   - Reference entity_id

6. **integration**: External service
   - ITC bridge configuration
   - API credentials
   - Service endpoints
   - Links to entity

7. **quote**: Quote being enriched
   - Update premium
   - Track bridge status
   - Store metadata

### Entity Setup for ITC
```sql
-- Ensure ITC entity exists
INSERT INTO entity (entity_type_id, name, code, status_id, created_by)
SELECT 
  et.id,
  'ITC Bridge Integration',
  'ITC_BRIDGE',
  1,
  1
FROM entity_type et
WHERE et.code = 'integration'
AND NOT EXISTS (
  SELECT 1 FROM entity e 
  WHERE e.code = 'ITC_BRIDGE'
);

-- Get entity_id for driver source tracking
SELECT id FROM entity WHERE code = 'ITC_BRIDGE';
```

### Query Patterns
```sql
-- Find bridge-discovered drivers
SELECT d.*, n.first_name, n.last_name
FROM driver d
JOIN name n ON d.name_id = n.id
JOIN map_quote_driver mqd ON d.id = mqd.driver_id
JOIN entity e ON d.source_entity_id = e.id
WHERE mqd.quote_id = ?
AND e.code = 'ITC_BRIDGE';

-- Count excluded bridge drivers
SELECT COUNT(*) as excluded_count
FROM driver d
JOIN map_quote_driver mqd ON d.id = mqd.driver_id
JOIN entity e ON d.source_entity_id = e.id
WHERE mqd.quote_id = ?
AND e.code = 'ITC_BRIDGE'
AND d.is_excluded = true;
```

### Alert Implementation
- Query drivers with source_entity_id = ITC
- Calculate alert state dynamically
- Show inline banner when found
- Track acknowledgment in session
- Clear after producer action

## Business Summary for Stakeholders
### What We're Building
An intelligent system that automatically discovers additional household drivers through external data sources and tracks their origin using our entity management system. By linking discovered drivers to their source (ITC Bridge), we maintain complete traceability while defaulting to safe exclusion status. Producers can review and include these drivers with full premium recalculation.

### Why It's Needed
Undisclosed household members are a major source of underwriting risk and claim disputes. This automated discovery with source tracking ensures all potential drivers are identified, their origin is documented, and proper risk assessment occurs. The entity-based tracking allows us to handle multiple external sources in the future.

### Expected Outcomes
- Complete source traceability for discovered drivers
- Improved risk assessment with external data
- Flexible framework for multiple data sources
- Reduced claims disputes from undisclosed drivers
- Compliance with disclosure requirements
- Accurate premium calculations

## Technical Summary for Developers
### Key Technical Decisions
- **Architecture Pattern**: Entity-based source tracking
- **Source Tracking**: Use source_entity_id field
- **Entity Management**: ITC as integration entity
- **Default Behavior**: Auto-exclude for safety
- **Alert Strategy**: Dynamic calculation from source

### Implementation Guidelines
- Ensure ITC entity exists in database
- Set source_entity_id on driver creation
- Query by entity relationship
- Build alert component for discoveries
- Implement side panel editing
- Handle inclusion state changes
- Trigger premium recalculation
- Maintain source throughout lifecycle

### Benefits of Entity Approach
1. **Extensibility**: Easy to add new sources
2. **Consistency**: All external sources tracked same way
3. **Queryability**: Simple joins to find source
4. **Auditability**: Complete source history
5. **Flexibility**: Entity metadata for source details

## Validation Criteria
### Pre-Implementation Checkpoints
- [x] Driver table has source_entity_id
- [x] Entity infrastructure exists
- [x] Integration entity type available
- [x] Verification system ready
- [x] Quote modification supported
- [x] Rating recalculation possible

### Success Metrics
- [ ] ITC entity created successfully
- [ ] Drivers link to source entity
- [ ] Queries identify bridge drivers
- [ ] Alerts display for discoveries
- [ ] Edit panel shows source
- [ ] Premium updates on changes
- [ ] Navigation preserves data
- [ ] Source tracking maintained

## Approval Section
**Status**: Ready for Review  
**Database Changes**: None - uses existing source_entity_id field  
**Pattern Reuse**: 100% - Using entity infrastructure  
**Risk Level**: Medium - External data dependency  
**Next Steps**: Review approach and implement with entity tracking  
**Reviewer Comments**: [Updated to use source_entity_id pattern]  
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER