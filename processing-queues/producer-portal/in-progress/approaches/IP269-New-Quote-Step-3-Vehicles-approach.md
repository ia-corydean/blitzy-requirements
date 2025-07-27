# IP269-New-Quote-Step-3-Vehicles - Implementation Approach

## Requirement Understanding
The Vehicles step enables users to add and manage vehicles for the insurance quote through automatic lookup based on the primary insured's address, manual VIN entry, or year/make/model search. The system must handle vehicle verification, usage type assignment, garaging address management, and ensure vehicle owners are included in the policy. This step is critical for accurate premium calculation and risk assessment.

## Domain Classification
- Primary Domain: Producer Portal / Quote Management
- Cross-Domain Impact: Yes - Affects coverage selection, premium calculation
- Complexity Level: High

## Pattern Analysis

### Reusable Patterns Identified
- [GR-69]: Producer Portal Architecture - Vehicle management patterns
- [GR-52]: Universal Entity Management - Vehicle entity reuse
- [GR-53]: DCS Integration - Vehicle verification services
- [GR-41]: Database Standards - Consistent field naming
- [GR-44]: Communication Architecture - Third-party data integration

### Domain-Specific Needs
- Vehicle lookup by address association
- VIN decoding and verification
- Year/Make/Model search functionality
- License plate capture
- Vehicle owner validation
- Usage type classification
- Garaging address management
- Manual entry fallback options

## Proposed Implementation

### Simplification Approach
- Current Complexity: Multiple lookup methods, owner validation, missing plate fields
- Simplified Solution: Enhance vehicle table, leverage verification services
- Trade-offs: Need to add license plate fields to vehicle table

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
   - [ ] Add license plate fields to vehicle
   - [ ] Call VIN decode service
   - [ ] Populate vehicle details
   - [ ] Handle decode failures

4. **Phase 4**: Year/Make/Model Search
   - [ ] Build Y/M/M search interface
   - [ ] Query vehicle database
   - [ ] Display matching options
   - [ ] Capture plate information
   - [ ] Save selected vehicle

5. **Phase 5**: Owner Validation
   - [ ] Check vehicle ownership
   - [ ] Prompt to add missing owners
   - [ ] Route to driver addition
   - [ ] Validate owner on policy
   - [ ] Block if owner not added

6. **Phase 6**: Data Management
   - [ ] Track garaging addresses
   - [ ] Manage vehicle use types
   - [ ] Store verification status
   - [ ] Link to quote properly

## Risk Assessment
- **Risk 1**: Incomplete vehicle data → Mitigation: Add license plate fields
- **Risk 2**: Third-party service failures → Mitigation: Manual entry fallback
- **Risk 3**: VIN decode accuracy → Mitigation: Allow manual override
- **Risk 4**: Owner validation complexity → Mitigation: Clear workflow guidance
- **Risk 5**: Performance with lookups → Mitigation: Async processing, caching

## Context Preservation
- Key Decisions: Enhance vehicle table, use external verification, enforce ownership
- Dependencies: Vehicle verification services, driver management, address system
- Future Impact: Foundation for coverage selection, premium calculation

## Database Requirements Summary
- **New Tables**: 0 tables need to be created
- **Existing Tables**: 10+ tables will be reused
- **Modified Tables**: 1 existing table needs modifications (vehicle)

## Database Schema Requirements

### Tables to Enhance

#### vehicle (Need License Plate Fields)
Add plate information:
```sql
ALTER TABLE vehicle
ADD COLUMN license_plate_number VARCHAR(20) AFTER vin_verified,
ADD COLUMN license_plate_state_id INT(11) AFTER license_plate_number,
ADD COLUMN registered_owner_driver_id INT(11) AFTER license_plate_state_id,
ADD COLUMN lookup_source VARCHAR(50) AFTER registered_owner_driver_id,
ADD CONSTRAINT fk_vehicle_plate_state FOREIGN KEY (license_plate_state_id) REFERENCES state(id),
ADD CONSTRAINT fk_vehicle_owner FOREIGN KEY (registered_owner_driver_id) REFERENCES driver(id),
ADD INDEX idx_license_plate (license_plate_number),
ADD INDEX idx_plate_state (license_plate_state_id);
```

### Existing Tables to Use

1. **vehicle**: Core vehicle information
   - Has VIN, Y/M/M, usage, garaging
   - Ready for enhancement

2. **map_quote_vehicle**: Links vehicles to quotes
   - Tracks vehicles per quote

3. **vehicle_type**: Vehicle categorization
   - Car, truck, motorcycle, etc.

4. **vehicle_use**: Usage types
   - Personal, business, farm, etc.

5. **vehicle_use_type**: Usage categories
   - Commute, pleasure, etc.

6. **vehicle_ownership_type**: Ownership status
   - Owned, leased, financed

7. **address**: Garaging addresses
   - Links to vehicle locations

8. **state**: License plate states
   - For plate registration

9. **driver**: Vehicle owners
   - Links registered owners

10. **verification**: External lookups
    - Track verification sources

### Lookup Integration
- Store lookup_source (address, VIN, manual)
- Track verification status in vin_verified
- Link owners via registered_owner_driver_id

## Business Summary for Stakeholders
### What We're Building
A comprehensive vehicle management system that automatically discovers vehicles associated with the insured's address, enables manual vehicle addition through VIN or year/make/model search, validates vehicle ownership, and captures all necessary information for accurate insurance quotes. The system ensures all vehicles and their owners are properly documented.

### Why It's Needed
Accurate vehicle information is essential for proper premium calculation and coverage determination. Missing or incorrect vehicle data leads to pricing errors and potential coverage gaps. This system streamlines vehicle data collection while ensuring completeness through multiple entry methods and ownership validation.

### Expected Outcomes
- Reduced vehicle data entry time by 70% through automatic lookup
- Improved accuracy with VIN verification
- Complete vehicle owner capture preventing coverage issues
- Flexible entry options accommodating various scenarios
- Better risk assessment through proper vehicle classification

## Technical Summary for Developers
### Key Technical Decisions
- **Architecture Pattern**: Enhance vehicle table with plate/owner fields
- **Lookup Strategy**: Address-based with VIN/YMM fallbacks
- **Verification Approach**: External service with local caching
- **Owner Validation**: Required driver record before vehicle addition
- **State Management**: Quote-scoped vehicle collection

### Implementation Guidelines
- Extend vehicle model with new fields
- Build vehicle lookup service integration
- Implement VIN decoder service
- Create YMM search functionality
- Build owner validation workflow
- Use database transactions
- Cache lookup results
- Handle service failures gracefully

## Validation Criteria
### Pre-Implementation Checkpoints
- [x] Vehicle table exists with core fields
- [x] Vehicle use types defined
- [x] Address system ready
- [x] State reference table exists
- [ ] Vehicle table needs plate fields
- [x] External services identified

### Success Metrics
- [ ] Address lookup returns vehicles
- [ ] VIN decode populates details
- [ ] YMM search finds matches
- [ ] License plate captures correctly
- [ ] Owner validation enforces rules
- [ ] Usage types save properly
- [ ] Garaging addresses link
- [ ] Continue enables when valid

## Approval Section
**Status**: Ready for Review  
**Database Changes**: Add 4 fields to vehicle table (plate, owner, source)  
**Pattern Reuse**: 95% - Leveraging existing vehicle infrastructure  
**Risk Level**: Medium - External service dependencies but fallbacks exist  
**Next Steps**: Review approach, approve vehicle table changes, implement  
**Reviewer Comments**: [Pending]  
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER