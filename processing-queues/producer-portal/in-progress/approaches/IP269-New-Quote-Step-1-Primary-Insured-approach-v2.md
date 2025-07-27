# IP269-New-Quote-Step-1-Primary-Insured - Implementation Approach v2

## Revision Notes
- **v2 Changes**: Documents that license table fields will be created in Docker database
- **Key Updates**: References entity catalog update to v5.3 with enhanced license table

## Requirement Understanding
The Primary Insured step initiates new insurance quotes by collecting and verifying the primary insured's identity. The system must support searching existing records, handling different license types (US and international), validating effective dates, and providing a streamlined experience for both desktop and mobile users. This is the critical first step that establishes the foundation for the entire quote.

## Domain Classification
- Primary Domain: Producer Portal / Quote Management
- Cross-Domain Impact: Yes - Establishes data for entire quote workflow
- Complexity Level: Medium

## Pattern Analysis

### Reusable Patterns Identified
- [GR-69]: Producer Portal Architecture - Quote initiation patterns
- [GR-52]: Universal Entity Management - Driver and name entity reuse
- [GR-41]: Database Standards - Consistent naming and relationships
- [GR-53]: DCS Integration Architecture - Driver verification patterns
- [GR-44]: Communication Architecture - Address validation

### Domain-Specific Needs
- Effective date validation (within 30 days)
- Program availability based on effective date
- License type handling (US vs International)
- Existing record search and matching
- Address modification option for matches
- Quote initialization with primary insured

## Proposed Implementation

### Simplification Approach
- Current Complexity: Multiple license types, search functionality, validation rules
- Simplified Solution: Enhanced license table (v5.3), leverage existing entities
- Trade-offs: Database migration required but provides complete functionality

### Technical Approach
1. **Phase 1**: Quote Initialization
   - [ ] Create new quote record
   - [ ] Validate effective date (max 30 days future)
   - [ ] Load available programs for date
   - [ ] Set quote status to "in_progress"

2. **Phase 2**: License Type Handling
   - [ ] Use enhanced license table (v5.3)
   - [ ] Implement US License flow (DL number, state)
   - [ ] Implement International flow (name, address)
   - [ ] Country field logic (disabled for US)

3. **Phase 3**: Search Functionality
   - [ ] Search by license number for US licenses
   - [ ] Search by name/address for international
   - [ ] Query existing driver records
   - [ ] Return matching profiles

4. **Phase 4**: Match Handling
   - [ ] Display match results in modal
   - [ ] Handle "Yes - Information Correct"
   - [ ] Handle "No - Not a Match" 
   - [ ] Handle "No - Address Incorrect"
   - [ ] Prefill or allow manual entry

5. **Phase 5**: Data Creation
   - [ ] Create/update driver record
   - [ ] Create/update license record
   - [ ] Create/update name record
   - [ ] Create/update address record
   - [ ] Link to quote via map_quote_driver

6. **Phase 6**: Navigation
   - [ ] Validate all required fields
   - [ ] Save quote progress
   - [ ] Navigate to Step 2 (Drivers)
   - [ ] Maintain quote context

## Risk Assessment
- **Risk 1**: Database migration timing → Mitigation: Execute v5.3 updates before implementation
- **Risk 2**: Match accuracy issues → Mitigation: Fuzzy matching algorithms
- **Risk 3**: Effective date edge cases → Mitigation: Clear validation messages
- **Risk 4**: Performance with large datasets → Mitigation: Use new indexes
- **Risk 5**: Data consistency → Mitigation: Transactional operations

## Context Preservation
- Key Decisions: Use v5.3 enhanced license table, reuse existing entities
- Dependencies: v5.3 database migration, driver/name/address entities
- Future Impact: Foundation for entire quote process with complete license data

## Database Requirements Summary
- **New Tables**: 0 tables need to be created
- **Existing Tables**: 10+ tables will be reused
- **Modified Tables**: 1 table enhanced in v5.3 (license)

## Database Schema Requirements

### Enhanced License Table (v5.3)
As documented in database-changes-summary-v5.3.md:
```sql
ALTER TABLE license
ADD COLUMN license_number VARCHAR(50) AFTER id,
ADD COLUMN state_id INT(11) AFTER license_number,
ADD COLUMN issue_date DATE AFTER state_id,
ADD COLUMN expiration_date DATE AFTER issue_date,
ADD COLUMN license_class VARCHAR(10) AFTER expiration_date,
ADD COLUMN restrictions TEXT AFTER license_class,
ADD COLUMN is_suspended BOOLEAN DEFAULT FALSE AFTER restrictions,
ADD COLUMN is_revoked BOOLEAN DEFAULT FALSE AFTER is_suspended,
ADD COLUMN suspension_date DATE AFTER is_revoked,
ADD COLUMN reinstatement_date DATE AFTER suspension_date;

ALTER TABLE license
ADD FOREIGN KEY (state_id) REFERENCES state(id);

ALTER TABLE license
ADD INDEX idx_license_number (license_number),
ADD INDEX idx_state (state_id),
ADD INDEX idx_expiration (expiration_date);
```

**Note**: The v5.3 migration includes additional fields beyond the original requirement for comprehensive license tracking and compliance needs.

### Existing Tables to Use

1. **quote**: Store new quote information
   - Has effective_date, program_id, premium fields
   - Ready for quote creation

2. **driver**: Primary insured information
   - Has name_id, license_id, DOB, gender
   - Supports is_named_insured flag
   - Enhanced with employment_id, occupation_id (v5.3)

3. **name**: Personal information
   - Has first_name, last_name, middle_name, suffix (v5.2)
   - Supports both person and business names

4. **address**: Location information
   - Complete address fields
   - Links to driver records

5. **license_type**: License categorization
   - Define US License, International, etc.

6. **program**: Available insurance programs
   - Filter by effective date
   - Contains rating rules

7. **map_quote_driver**: Link quotes to drivers
   - Establishes primary insured relationship

8. **state**: US state reference
   - For license state selection

9. **country**: Country reference
   - For international licenses

10. **gender**: Gender options
    - For driver demographics

### Search Implementation
```sql
-- Search by US license number
SELECT d.*, l.license_number, l.state_id, n.first_name, n.last_name
FROM driver d
JOIN license l ON d.license_id = l.id
JOIN name n ON d.name_id = n.id
WHERE l.license_number = ?
AND l.state_id = ?
AND d.status_id = 1;

-- Search by name for international
SELECT d.*, n.first_name, n.last_name, a.city, a.country_id
FROM driver d
JOIN name n ON d.name_id = n.id
LEFT JOIN address a ON a.entity_id = d.id AND a.entity_type_id = (SELECT id FROM entity_type WHERE code = 'driver')
WHERE n.first_name LIKE ?
AND n.last_name LIKE ?
AND a.country_id = ?;
```

### International License Handling
For international licenses, the license table will use:
- license_number: Passport or international ID
- state_id: NULL for international
- license_type_id: References 'international' type
- Country tracked via address.country_id

## Business Summary for Stakeholders
### What We're Building
A comprehensive primary insured entry system that leverages the enhanced license infrastructure from v5.3. The system supports both US and international licenses with complete data capture, enables searching existing records to prevent duplicates, and establishes the foundation for accurate quote generation.

### Why It's Needed
Accurate primary insured identification is critical for proper rating, underwriting, and compliance. The enhanced license table provides complete tracking of license status, restrictions, and history, enabling better risk assessment and reducing data entry errors through intelligent matching.

### Expected Outcomes
- Complete license data capture with v5.3 enhancements
- Reduced duplicate records through search functionality
- Improved data quality with validation
- Faster quote initiation with prefill capabilities
- Better compliance with comprehensive license tracking
- Foundation for accurate rating calculations

## Technical Summary for Developers
### Key Technical Decisions
- **Architecture Pattern**: Entity-based with enhanced license table
- **Database Version**: Requires v5.3 with license enhancements
- **Search Strategy**: License number for US, name/address for international
- **Data Model**: Reuse existing entities with new license fields
- **Validation Approach**: Frontend and backend validation

### Implementation Guidelines
- Ensure v5.3 database migration is complete
- Use enhanced license fields for complete data
- Implement type-specific validation rules
- Build efficient search queries with indexes
- Handle international licenses via address country
- Create comprehensive matching logic
- Maintain transaction integrity
- Track primary insured via is_named_insured

### Entity Catalog Reference
The universal-entity-catalog-v5.3.json will include:
- Enhanced license entity with all new fields
- Proper relationships documented
- Index specifications for performance
- Validation rules for each field

## Validation Criteria
### Pre-Implementation Checkpoints
- [ ] v5.3 database migration executed
- [ ] License table enhanced with new fields
- [ ] Entity catalog updated to v5.3
- [x] All reference tables exist
- [x] Search indexes created
- [x] Program filtering ready

### Success Metrics
- [ ] License fields save correctly
- [ ] US license search works
- [ ] International search works
- [ ] Match handling functions
- [ ] Quote creates successfully
- [ ] Primary insured links properly
- [ ] Navigation preserves data
- [ ] Validation prevents bad data

## Approval Section
**Status**: Ready for Review  
**Database Changes**: License table enhanced in v5.3 migration  
**Pattern Reuse**: 95% - New license fields, existing patterns  
**Risk Level**: Low - Standard enhancement with v5.3  
**Next Steps**: Execute v5.3 migration, then implement  
**Reviewer Comments**: [Documents v5.3 dependency]  
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER