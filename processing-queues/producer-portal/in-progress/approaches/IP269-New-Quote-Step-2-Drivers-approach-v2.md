# IP269-New-Quote-Step-2-Drivers - Implementation Approach v2

## Revision Notes
- **v2 Changes**: Major restructuring based on feedback
- **Key Updates**: 
  - Create employment and employment_type tables (reference employment_id)
  - Create occupation and occupation_type tables (reference occupation_id)
  - Remove income_source field
  - Use driver_type to account for excluded/included
  - Remove removal_reason field

## Requirement Understanding
The Drivers step manages all driver information for the insurance quote, including adding, editing, including/excluding drivers, handling violations, and enforcing underwriting rules. The system must display drivers associated with the primary insured's address, support driver search functionality, manage driver statuses (included/excluded), and validate business rules like marital status consistency and criminal eligibility.

## Domain Classification
- Primary Domain: Producer Portal / Quote Management
- Cross-Domain Impact: Yes - Affects rating, underwriting, policy generation
- Complexity Level: High

## Pattern Analysis

### Reusable Patterns Identified
- [GR-69]: Producer Portal Architecture - Multi-step quote workflow
- [GR-52]: Universal Entity Management - Driver entity reuse
- [GR-41]: Database Standards - Status management, audit fields
- [GR-10]: SR22/SR26 Requirements - Financial responsibility filing
- [GR-53]: DCS Integration - Driver verification patterns

### Domain-Specific Needs
- Household driver discovery
- Include/exclude status management via driver_type
- Violation tracking and management
- SR-22 requirement handling
- Employment and occupation tracking
- Marital status validation rules
- Criminal eligibility checking
- Real-time household search updates

## Proposed Implementation

### Simplification Approach
- Current Complexity: Multiple driver statuses, violations, SR-22, validations
- Simplified Solution: Use v5.3 employment/occupation tables, driver_type for status
- Trade-offs: More normalized structure, better data integrity

### Technical Approach
1. **Phase 1**: Driver List Display
   - [ ] Load drivers for quote household
   - [ ] Group by driver_type (included/excluded)
   - [ ] Display primary driver indicator
   - [ ] Show license and identification info
   - [ ] Implement search functionality
   - [ ] Add pagination for large lists

2. **Phase 2**: Add Driver Modal
   - [ ] Build comprehensive driver form
   - [ ] Implement license type handling
   - [ ] Link to employment table
   - [ ] Link to occupation table
   - [ ] Handle SR-22 requirements
   - [ ] Support violation entry
   - [ ] Save to map_quote_driver

3. **Phase 3**: Employment/Occupation
   - [ ] Create employment record
   - [ ] Select employment_type
   - [ ] Create occupation record
   - [ ] Select occupation_type
   - [ ] Link to driver

4. **Phase 4**: Status Management
   - [ ] Use driver_type for included/excluded
   - [ ] Update driver_type_id on changes
   - [ ] No removal_reason needed
   - [ ] Maintain audit trail

5. **Phase 5**: Household Search
   - [ ] Re-run search on driver addition
   - [ ] Flag new drivers with "New" tag
   - [ ] Merge results with existing list
   - [ ] Prevent duplicates

6. **Phase 6**: Violation Management
   - [ ] Create violations in violation table
   - [ ] Link via map_driver_violation
   - [ ] Support multiple violations
   - [ ] Track violation dates

7. **Phase 7**: Business Rule Validation
   - [ ] Validate married driver pairs
   - [ ] Check criminal eligibility
   - [ ] Enforce inclusion requirements
   - [ ] Block progression if invalid

8. **Phase 8**: Save & Navigation
   - [ ] Auto-save on field changes
   - [ ] Validate all required fields
   - [ ] Enable continue when valid
   - [ ] Navigate to Step 3 (Vehicles)

## Risk Assessment
- **Risk 1**: Complex table relationships → Mitigation: Clear service layer abstraction
- **Risk 2**: Data migration from old structure → Mitigation: Migration scripts
- **Risk 3**: Household search accuracy → Mitigation: Robust matching algorithms
- **Risk 4**: Performance with joins → Mitigation: Proper indexes, eager loading
- **Risk 5**: SR-22 compliance → Mitigation: Follow GR-10 requirements

## Context Preservation
- Key Decisions: Normalized employment/occupation, driver_type for status
- Dependencies: v5.3 new tables, existing violation structure
- Future Impact: Better data quality, easier reporting, cleaner architecture

## Database Requirements Summary
- **New Tables**: 4 tables from v5.3 (employment, employment_type, occupation, occupation_type)
- **Existing Tables**: 15+ tables will be reused
- **Modified Tables**: 1 table modified in v5.3 (driver)

## Database Schema Requirements

### New Tables (From v5.3)

#### employment_type
```sql
CREATE TABLE employment_type (
  id INT(11) AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(50) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  is_default BOOLEAN DEFAULT FALSE,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### employment
```sql
CREATE TABLE employment (
  id INT(11) AUTO_INCREMENT PRIMARY KEY,
  employment_type_id INT(11) NOT NULL,
  employer_name VARCHAR(255),
  employer_address_id INT(11),
  start_date DATE,
  end_date DATE,
  is_current BOOLEAN DEFAULT TRUE,
  status_id INT(11) NOT NULL,
  created_by BIGINT UNSIGNED NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by BIGINT UNSIGNED,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (employment_type_id) REFERENCES employment_type(id),
  FOREIGN KEY (employer_address_id) REFERENCES address(id),
  FOREIGN KEY (status_id) REFERENCES status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id)
);
```

#### occupation_type
```sql
CREATE TABLE occupation_type (
  id INT(11) AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(50) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  is_default BOOLEAN DEFAULT FALSE,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### occupation
```sql
CREATE TABLE occupation (
  id INT(11) AUTO_INCREMENT PRIMARY KEY,
  occupation_type_id INT(11) NOT NULL,
  title VARCHAR(255) NOT NULL,
  industry VARCHAR(255),
  description TEXT,
  status_id INT(11) NOT NULL,
  created_by BIGINT UNSIGNED NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by BIGINT UNSIGNED,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (occupation_type_id) REFERENCES occupation_type(id),
  FOREIGN KEY (status_id) REFERENCES status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id)
);
```

### Modified Driver Table (v5.3)
```sql
-- Add new columns
ALTER TABLE driver
ADD COLUMN employment_id INT(11) AFTER accidents_count,
ADD COLUMN occupation_id INT(11) AFTER employment_id,
ADD COLUMN source_entity_id INT(11) AFTER occupation_id,
ADD COLUMN is_excluded BOOLEAN DEFAULT FALSE AFTER source_entity_id;

-- Add foreign keys
ALTER TABLE driver
ADD FOREIGN KEY (employment_id) REFERENCES employment(id),
ADD FOREIGN KEY (occupation_id) REFERENCES occupation(id),
ADD FOREIGN KEY (source_entity_id) REFERENCES entity(id);

-- Remove deprecated columns (if they exist)
ALTER TABLE driver
DROP COLUMN IF EXISTS income_source,
DROP COLUMN IF EXISTS removal_reason;
```

### Driver Type Values
```sql
-- Ensure driver_type has included/excluded values
INSERT INTO driver_type (code, name, description, is_active) VALUES
('included', 'Included Driver', 'Driver is included in policy coverage', TRUE),
('excluded', 'Excluded Driver', 'Driver is excluded from policy coverage', TRUE),
('primary', 'Primary Driver', 'Primary driver on policy', TRUE),
('secondary', 'Secondary Driver', 'Additional driver on policy', TRUE);
```

### Existing Tables to Use

1. **driver**: Core driver information
   - Has name_id, license_id, demographics
   - Links to employment_id, occupation_id
   - Uses is_excluded for quick filtering

2. **driver_type**: Status management
   - Included vs excluded drivers
   - Primary vs secondary

3. **map_quote_driver**: Links drivers to quotes
   - Establishes driver relationships
   - Tracks association to quote

4. **violation**: Traffic violations
   - Has type, date, description
   - Links to drivers

5. **violation_type**: Violation categories
   - Moving violations, DUI, etc.

6. **map_driver_violation**: Driver-violation links
   - Multiple violations per driver

7. **sr22**: SR-22 requirements
   - Financial responsibility tracking

8. **sr22_type**: SR-22 categories
   - Different requirement types

9. **sr22_reason**: Why SR-22 required
   - DUI, uninsured accident, etc.

10. **marital_status**: Marital status reference
    - Single, married, divorced, etc.

11. **relationship_to_insured**: Relationship types
    - Self, spouse, child, etc.

### Query Examples
```sql
-- Get all included drivers for a quote
SELECT d.*, dt.name as driver_type_name, e.employer_name, o.title as occupation
FROM driver d
JOIN driver_type dt ON d.driver_type_id = dt.id
JOIN map_quote_driver mqd ON d.id = mqd.driver_id
LEFT JOIN employment e ON d.employment_id = e.id
LEFT JOIN occupation o ON d.occupation_id = o.id
WHERE mqd.quote_id = ?
AND dt.code = 'included';

-- Check for violations
SELECT v.*, vt.name as violation_type_name
FROM violation v
JOIN violation_type vt ON v.violation_type_id = vt.id
JOIN map_driver_violation mdv ON v.id = mdv.violation_id
WHERE mdv.driver_id = ?;
```

## Business Summary for Stakeholders
### What We're Building
A comprehensive driver management system using normalized employment and occupation data structures. The system properly categorizes drivers as included or excluded using driver types, captures complete employment information in dedicated tables, and maintains full audit trails. This approach provides better data quality and easier reporting.

### Why It's Needed
Accurate driver information is critical for proper rating and underwriting. By normalizing employment and occupation data into dedicated tables, we enable better risk assessment, cleaner data management, and more flexible reporting. Using driver_type for status management provides clear categorization without complex boolean flags.

### Expected Outcomes
- Cleaner data architecture with normalized tables
- Better employment/occupation tracking
- Clear driver status management
- Improved data quality and consistency
- Easier reporting and analytics
- Reduced data redundancy
- Enhanced audit capabilities

## Technical Summary for Developers
### Key Technical Decisions
- **Architecture Pattern**: Normalized relational model
- **Status Management**: driver_type instead of booleans
- **Employment Model**: Separate employment and occupation entities
- **Removal Strategy**: No soft deletes, use status/type
- **Audit Pattern**: Standard created_by/updated_by fields

### Implementation Guidelines
- Create employment before linking to driver
- Create occupation before linking to driver
- Use driver_type for included/excluded logic
- Don't use removal_reason, just change status
- Maintain referential integrity
- Use eager loading for performance
- Build service layer for complex operations
- Handle null employment/occupation gracefully

### Service Layer Example
```javascript
class DriverService {
  async addDriver(quoteId, driverData) {
    // Create employment if provided
    if (driverData.employment) {
      const employment = await Employment.create(driverData.employment);
      driverData.employment_id = employment.id;
    }
    
    // Create occupation if provided
    if (driverData.occupation) {
      const occupation = await Occupation.create(driverData.occupation);
      driverData.occupation_id = occupation.id;
    }
    
    // Set driver type
    driverData.driver_type_id = driverData.isExcluded 
      ? await DriverType.findByCode('excluded')
      : await DriverType.findByCode('included');
    
    // Create driver
    const driver = await Driver.create(driverData);
    
    // Link to quote
    await MapQuoteDriver.create({
      quote_id: quoteId,
      driver_id: driver.id
    });
    
    return driver;
  }
}
```

## Validation Criteria
### Pre-Implementation Checkpoints
- [ ] v5.3 database migration executed
- [ ] Employment tables created
- [ ] Occupation tables created
- [ ] Driver table modified
- [ ] Driver type values populated
- [ ] Indexes created

### Success Metrics
- [ ] Drivers create with employment
- [ ] Occupation links properly
- [ ] Driver types work correctly
- [ ] Include/exclude toggles work
- [ ] Violations link properly
- [ ] SR-22 tracks correctly
- [ ] Household search functions
- [ ] Navigation preserves data

## Approval Section
**Status**: Ready for Review  
**Database Changes**: 4 new tables, driver modifications per v5.3  
**Pattern Reuse**: 90% - New normalized structure, existing patterns  
**Risk Level**: Medium - Structural changes to driver management  
**Next Steps**: Execute v5.3 migration, implement normalized approach  
**Reviewer Comments**: [Major restructuring for better architecture]  
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER