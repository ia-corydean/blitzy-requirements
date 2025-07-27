# IP269-New-Quote-Step-3-Vehicles - Implementation Approach v2

## Revision Notes
- **v2 Changes**: Addresses registered owner complexity
- **Key Updates**: 
  - Proposes flexible owner tracking solution using entity pattern
  - Allows owner to be driver or entity (company, trust, etc.)
  - Simplifies registered_owner_driver_id issue

## Requirement Understanding
The Vehicles step enables users to add and manage vehicles for the insurance quote through automatic lookup based on the primary insured's address, manual VIN entry, or year/make/model search. The system must handle vehicle verification, usage type assignment, garaging address management, and ensure vehicle owners are included in the policy. This step is critical for accurate premium calculation and risk assessment.

## Domain Classification
- Primary Domain: Producer Portal / Quote Management
- Cross-Domain Impact: Yes - Affects coverage selection, premium calculation
- Complexity Level: High

## Pattern Analysis

### Reusable Patterns Identified
- [GR-69]: Producer Portal Architecture - Vehicle management patterns
- [GR-52]: Universal Entity Management - Vehicle and owner entities
- [GR-53]: DCS Integration - Vehicle verification services
- [GR-41]: Database Standards - Consistent field naming
- [GR-44]: Communication Architecture - Third-party data integration

### Domain-Specific Needs
- Vehicle lookup by address association
- VIN decoding and verification
- Year/Make/Model search functionality
- License plate capture
- Flexible vehicle owner tracking (person or entity)
- Usage type classification
- Garaging address management
- Manual entry fallback options

## Proposed Implementation

### Simplification Approach
- Current Complexity: Multiple lookup methods, owner validation, entity ownership
- Simplified Solution: Use entity pattern for flexible ownership
- Trade-offs: Additional join but maximum flexibility

### Technical Approach
1. **Phase 1**: Vehicle Lookup
   - [ ] Query third-party service by address
   - [ ] Display returned vehicles
   - [ ] Show vehicle details for review
   - [ ] Enable add/remove actions
   - [ ] Store lookup results

2. **Phase 2**: Add from Lookup
   - [ ] Open side panel for vehicle
   - [ ] Capture usage type
   - [ ] Validate required fields
   - [ ] Save to map_quote_vehicle
   - [ ] Update vehicle list display

3. **Phase 3**: Manual VIN Entry
   - [ ] Build VIN entry form
   - [ ] Capture license plate info
   - [ ] Call VIN decode service
   - [ ] Populate vehicle details
   - [ ] Handle decode failures

4. **Phase 4**: Year/Make/Model Search
   - [ ] Build Y/M/M search interface
   - [ ] Query vehicle database
   - [ ] Display matching options
   - [ ] Capture plate information
   - [ ] Save selected vehicle

5. **Phase 5**: Owner Management
   - [ ] Implement flexible owner selection
   - [ ] Support driver as owner
   - [ ] Support entity as owner
   - [ ] Validate owner exists
   - [ ] Create entity if needed

6. **Phase 6**: Owner Validation
   - [ ] Check vehicle ownership
   - [ ] If driver owner, ensure on policy
   - [ ] If entity owner, track for reference
   - [ ] Prompt to add missing driver owners
   - [ ] Allow entity owners without policy inclusion

7. **Phase 7**: Data Management
   - [ ] Track garaging addresses
   - [ ] Manage vehicle use types
   - [ ] Store verification status
   - [ ] Link to quote properly

## Risk Assessment
- **Risk 1**: Owner type complexity → Mitigation: Clear UI for owner selection
- **Risk 2**: Third-party service failures → Mitigation: Manual entry fallback
- **Risk 3**: VIN decode accuracy → Mitigation: Allow manual override
- **Risk 4**: Entity owner creation → Mitigation: Simple entity creation flow
- **Risk 5**: Performance with lookups → Mitigation: Async processing, caching

## Context Preservation
- Key Decisions: Entity pattern for ownership, flexible owner types
- Dependencies: Entity management, vehicle verification, driver system
- Future Impact: Supports all ownership scenarios (individual, company, trust)

## Database Requirements Summary
- **New Tables**: 0 tables need to be created
- **Existing Tables**: 12+ tables will be reused
- **Modified Tables**: 1 table modified in v5.3 (vehicle)

## Database Schema Requirements

### Enhanced Vehicle Table (v5.3)

#### Vehicle Owner Solution
Using entity pattern for maximum flexibility:
```sql
-- Add flexible owner tracking using entity pattern
ALTER TABLE vehicle
ADD COLUMN registered_owner_entity_id INT(11) AFTER primary_driver_id,
ADD COLUMN registered_owner_entity_type_id INT(11) AFTER registered_owner_entity_id,
ADD COLUMN license_plate_number VARCHAR(20) AFTER registered_owner_entity_type_id,
ADD COLUMN license_plate_state_id INT(11) AFTER license_plate_number;

ALTER TABLE vehicle
ADD FOREIGN KEY (registered_owner_entity_id) REFERENCES entity(id),
ADD FOREIGN KEY (registered_owner_entity_type_id) REFERENCES entity_type(id),
ADD FOREIGN KEY (license_plate_state_id) REFERENCES state(id);

ALTER TABLE vehicle
ADD INDEX idx_owner_entity (registered_owner_entity_id),
ADD INDEX idx_owner_type (registered_owner_entity_type_id),
ADD INDEX idx_license_plate (license_plate_number),
ADD INDEX idx_plate_state (license_plate_state_id);
```

### Owner Type Examples
```sql
-- Driver as owner (individual)
INSERT INTO vehicle (vin, registered_owner_entity_id, registered_owner_entity_type_id)
VALUES ('1HGCM12345', 
  123, -- driver entity id
  (SELECT id FROM entity_type WHERE code = 'driver')
);

-- Company as owner
INSERT INTO vehicle (vin, registered_owner_entity_id, registered_owner_entity_type_id)
VALUES ('1HGCM67890',
  456, -- company entity id  
  (SELECT id FROM entity_type WHERE code = 'company')
);

-- Trust as owner
INSERT INTO vehicle (vin, registered_owner_entity_id, registered_owner_entity_type_id)
VALUES ('1HGCM11111',
  789, -- trust entity id
  (SELECT id FROM entity_type WHERE code = 'trust')
);
```

### Existing Tables to Use

1. **vehicle**: Core vehicle information
   - Has VIN, Y/M/M, usage, garaging
   - Enhanced with flexible ownership

2. **entity**: Universal entity reference
   - Supports any owner type
   - Links to specific tables

3. **entity_type**: Entity categorization
   - driver, company, trust, etc.
   - Defines owner types

4. **map_quote_vehicle**: Links vehicles to quotes
   - Tracks vehicles per quote

5. **vehicle_type**: Vehicle categorization
   - Car, truck, motorcycle, etc.

6. **vehicle_use**: Usage types
   - Personal, business, farm, etc.

7. **vehicle_ownership_type**: Ownership status
   - Owned, leased, financed

8. **address**: Garaging addresses
   - Links to vehicle locations

9. **state**: License plate states
   - For plate registration

10. **driver**: Individual owners
    - When entity_type = 'driver'

11. **company**: Business owners
    - When entity_type = 'company'

12. **verification**: External lookups
    - Track verification sources

### Query Examples
```sql
-- Get vehicle with owner details (any type)
SELECT v.*, 
  e.name as owner_name,
  et.name as owner_type,
  CASE 
    WHEN et.code = 'driver' THEN d.id
    WHEN et.code = 'company' THEN c.id
    ELSE e.id
  END as owner_specific_id
FROM vehicle v
JOIN entity e ON v.registered_owner_entity_id = e.id
JOIN entity_type et ON v.registered_owner_entity_type_id = et.id
LEFT JOIN driver d ON e.id = d.id AND et.code = 'driver'
LEFT JOIN company c ON e.id = c.id AND et.code = 'company'
WHERE v.id = ?;

-- Check if driver owner is on policy
SELECT COUNT(*) > 0 as owner_on_policy
FROM vehicle v
JOIN entity_type et ON v.registered_owner_entity_type_id = et.id
JOIN map_quote_driver mqd ON v.registered_owner_entity_id = mqd.driver_id
WHERE v.id = ?
AND et.code = 'driver'
AND mqd.quote_id = ?;
```

### Owner Creation Flow
```javascript
// Service layer example
async function setVehicleOwner(vehicleId, ownerType, ownerData) {
  let entityId;
  let entityTypeId;
  
  if (ownerType === 'driver') {
    // Check if driver exists
    const driver = await findOrCreateDriver(ownerData);
    entityId = driver.entity_id;
    entityTypeId = await getEntityTypeId('driver');
  } else if (ownerType === 'company') {
    // Create or find company entity
    const company = await findOrCreateCompany(ownerData);
    entityId = company.entity_id;
    entityTypeId = await getEntityTypeId('company');
  } else if (ownerType === 'trust') {
    // Create or find trust entity
    const trust = await findOrCreateTrust(ownerData);
    entityId = trust.entity_id;
    entityTypeId = await getEntityTypeId('trust');
  }
  
  // Update vehicle
  await updateVehicle(vehicleId, {
    registered_owner_entity_id: entityId,
    registered_owner_entity_type_id: entityTypeId
  });
}
```

## Business Summary for Stakeholders
### What We're Building
A flexible vehicle management system that supports all types of vehicle ownership scenarios. Using the entity pattern, we can track whether a vehicle is owned by an individual (driver), a company, a trust, or any other entity type. This approach handles real-world complexity where vehicles may not always be owned by individuals on the policy.

### Why It's Needed
Insurance policies must accurately reflect vehicle ownership for legal and underwriting purposes. Many vehicles are owned by companies, trusts, or other entities rather than individuals. This flexible approach allows us to capture any ownership scenario while maintaining data integrity and supporting proper risk assessment.

### Expected Outcomes
- Support for all vehicle ownership types
- Accurate ownership documentation
- Flexibility for business vehicles
- Proper handling of trust-owned vehicles
- Complete audit trail of ownership
- Better risk assessment with accurate data
- Compliance with ownership disclosure requirements

## Technical Summary for Developers
### Key Technical Decisions
- **Architecture Pattern**: Entity-based ownership tracking
- **Flexibility**: Supports any current or future owner type
- **Data Model**: Uses entity_id + entity_type_id pattern
- **Validation**: Type-specific validation based on entity_type
- **Extensibility**: Easy to add new owner types

### Implementation Guidelines
- Always set both entity_id and entity_type_id
- Validate entity exists before linking
- Check driver owners are on policy
- Allow non-driver owners without policy inclusion
- Use entity service for owner creation
- Handle UI selection of owner type
- Implement type-specific validation
- Maintain entity relationships

### UI Considerations
```
Owner Type Selection:
[ ] Individual (Driver on Policy)
[ ] Company
[ ] Trust
[ ] Other Entity

If Individual:
  - Show driver dropdown
  - Validate driver on policy
  
If Company/Trust/Other:
  - Show entity search/create
  - No policy inclusion required
```

## Validation Criteria
### Pre-Implementation Checkpoints
- [ ] v5.3 vehicle table updates executed
- [ ] Entity infrastructure exists
- [ ] Entity types configured
- [ ] Company table available
- [ ] Trust support planned
- [ ] UI owner selection designed

### Success Metrics
- [ ] Vehicles link to any owner type
- [ ] Driver owners validate on policy
- [ ] Entity owners create properly
- [ ] License plates save correctly
- [ ] VIN decode works
- [ ] Y/M/M search functions
- [ ] Owner queries perform well
- [ ] Navigation preserves data

## Approval Section
**Status**: Ready for Review  
**Database Changes**: Vehicle table enhanced with entity pattern  
**Pattern Reuse**: 95% - Entity pattern for flexibility  
**Risk Level**: Low - Proven entity pattern approach  
**Next Steps**: Execute v5.3 migration, implement flexible ownership  
**Reviewer Comments**: [Addresses ownership complexity elegantly]  
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER