# IP269-New-Quote-Step-5-Coverages - Implementation Approach v2

## Revision Notes
- **v2 Changes**: Adds dedicated special equipment tables
- **Key Updates**: 
  - Creates special_equipment and special_equipment_type tables
  - Provides proper normalization for equipment tracking
  - Better structure than adding fields to coverage table

## Requirement Understanding
The Coverage Selection step enables users to customize insurance coverage options including policy-wide and per-vehicle coverages, select limits and deductibles, handle state-mandated minimums, and see real-time premium calculations. The system must support additional equipment coverage, payment options configuration, and ensure all required coverages are selected before proceeding.

## Domain Classification
- Primary Domain: Producer Portal / Quote Management
- Cross-Domain Impact: Yes - Directly affects premium calculation and policy generation
- Complexity Level: High

## Pattern Analysis

### Reusable Patterns Identified
- [GR-69]: Producer Portal Architecture - Coverage selection patterns
- [GR-52]: Universal Entity Management - Coverage entity reuse
- [GR-41]: Database Standards - Consistent relationships
- [GR-38]: Microservice Architecture - Rating service integration
- [GR-20]: Business Logic Standards - Coverage validation rules

### Domain-Specific Needs
- Policy-wide vs per-vehicle coverage distinction
- Limit and deductible dropdown selections
- Special equipment coverage tracking
- State-mandated minimum enforcement
- Real-time premium recalculation
- Payment plan selection
- Down payment percentage configuration

## Proposed Implementation

### Simplification Approach
- Current Complexity: Multiple coverage types, limits, deductibles, equipment
- Simplified Solution: Leverage existing coverage infrastructure with new equipment tables
- Trade-offs: Additional tables but better data organization

### Technical Approach
1. **Phase 1**: Coverage Display
   - [ ] Load available coverages by program
   - [ ] Separate policy-wide from vehicle-specific
   - [ ] Query map_program_coverage for options
   - [ ] Display current selections
   - [ ] Show required coverage indicators

2. **Phase 2**: Limit/Deductible Selection
   - [ ] Load available limits from limit table
   - [ ] Load deductibles from deductible table
   - [ ] Filter by program rules
   - [ ] Populate dropdowns dynamically
   - [ ] Handle selection changes

3. **Phase 3**: Special Equipment
   - [ ] Create special_equipment records
   - [ ] Link to vehicles
   - [ ] Select equipment types
   - [ ] Capture equipment details
   - [ ] Include in coverage calculations

4. **Phase 4**: Equipment Coverage
   - [ ] Calculate equipment premium
   - [ ] Add to vehicle coverage
   - [ ] Show in premium breakdown
   - [ ] Track coverage limits
   - [ ] Validate equipment values

5. **Phase 5**: Validation Rules
   - [ ] Check state minimums
   - [ ] Enforce required coverages
   - [ ] Validate limit/deductible combinations
   - [ ] Block invalid selections
   - [ ] Show clear error messages

6. **Phase 6**: Premium Calculation
   - [ ] Call rating service on changes
   - [ ] Include equipment premiums
   - [ ] Display premium breakdown
   - [ ] Show fees separately
   - [ ] Update total in real-time

7. **Phase 7**: Payment Configuration
   - [ ] Payment plan selection
   - [ ] Down payment percentage
   - [ ] First installment date
   - [ ] Calculate payment schedule
   - [ ] Display payment summary

8. **Phase 8**: Save & Navigation
   - [ ] Save all selections to map_quote_coverage
   - [ ] Save equipment to special_equipment
   - [ ] Validate all required selected
   - [ ] Enable continue when valid
   - [ ] Navigate to Step 6 Review

## Risk Assessment
- **Risk 1**: Complex rating with equipment → Mitigation: Clear equipment premium calculation
- **Risk 2**: State regulation compliance → Mitigation: Database-driven rules
- **Risk 3**: Performance with equipment queries → Mitigation: Proper indexes
- **Risk 4**: Equipment valuation accuracy → Mitigation: Validation rules
- **Risk 5**: Payment calculation errors → Mitigation: Comprehensive testing

## Context Preservation
- Key Decisions: New equipment tables, integrate with coverage system
- Dependencies: Coverage definitions, rating service, equipment types
- Future Impact: Foundation for comprehensive equipment tracking

## Database Requirements Summary
- **New Tables**: 2 tables from v5.3 (special_equipment, special_equipment_type)
- **Existing Tables**: 15+ tables will be reused
- **Modified Tables**: 0 tables need modifications

## Database Schema Requirements

### New Tables (From v5.3)

#### special_equipment_type
```sql
CREATE TABLE special_equipment_type (
  id INT(11) AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(50) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  is_default BOOLEAN DEFAULT FALSE,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  INDEX idx_code (code),
  INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert equipment types
INSERT INTO special_equipment_type (code, name, description) VALUES
('audio_video', 'Audio/Video', 'Audio and video equipment'),
('custom_parts', 'Custom Parts', 'Custom or aftermarket parts'),
('business_equipment', 'Business Equipment', 'Business use equipment'),
('disability_equipment', 'Disability Equipment', 'Disability assistance equipment'),
('towing_equipment', 'Towing Equipment', 'Towing related equipment'),
('other', 'Other', 'Other special equipment');
```

#### special_equipment
```sql
CREATE TABLE special_equipment (
  id INT(11) AUTO_INCREMENT PRIMARY KEY,
  special_equipment_type_id INT(11) NOT NULL,
  vehicle_id INT(11) NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  value DECIMAL(10,2),
  manufacturer VARCHAR(100),
  model VARCHAR(100),
  serial_number VARCHAR(100),
  installation_date DATE,
  status_id INT(11) NOT NULL,
  created_by BIGINT UNSIGNED NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by BIGINT UNSIGNED,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (special_equipment_type_id) REFERENCES special_equipment_type(id),
  FOREIGN KEY (vehicle_id) REFERENCES vehicle(id),
  FOREIGN KEY (status_id) REFERENCES status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  
  INDEX idx_type (special_equipment_type_id),
  INDEX idx_vehicle (vehicle_id),
  INDEX idx_value (value),
  INDEX idx_status (status_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Existing Tables to Use

1. **coverage**: Coverage definitions
   - Has type, limit, deductible references
   - Tracks selection and requirements
   - Stores premium amounts

2. **coverage_type**: Coverage categories
   - Bodily Injury, Property Damage, etc.
   - Policy-wide vs vehicle-specific
   - Equipment coverage type

3. **limit**: Coverage limit options
   - Available limit values
   - Min/max constraints
   - Equipment coverage limits

4. **limit_type**: Limit categories
   - Per person, per accident, etc.
   - Equipment value limits

5. **deductible**: Deductible options
   - Available deductible amounts
   - Coverage-specific options

6. **deductible_type**: Deductible categories
   - Comprehensive, collision, etc.

7. **map_quote_coverage**: Quote coverage selections
   - Links selected coverages to quote
   - Tracks user selections
   - Includes equipment coverage

8. **map_program_coverage**: Program coverage rules
   - Available coverages by program
   - Required coverage flags

9. **map_program_limit**: Program limit rules
   - Available limits by program

10. **payment_plan**: Payment options
    - Monthly, quarterly, annual
    - Down payment requirements

11. **payment_plan_type**: Plan categories
    - Standard, low down, paid in full

12. **fee**: Additional charges
    - Installment fees
    - Processing fees

13. **vehicle**: Vehicle information
    - Links to special equipment

14. **quote**: Quote being configured
    - Premium totals
    - Selected payment plan

### Equipment Integration
```sql
-- Get equipment for a vehicle
SELECT se.*, set.name as equipment_type
FROM special_equipment se
JOIN special_equipment_type set ON se.special_equipment_type_id = set.id
WHERE se.vehicle_id = ?
AND se.status_id = 1;

-- Calculate total equipment value
SELECT SUM(value) as total_equipment_value
FROM special_equipment
WHERE vehicle_id = ?
AND status_id = 1;

-- Link equipment coverage
INSERT INTO map_quote_coverage (quote_id, coverage_id, vehicle_id, limit_amount)
SELECT 
  ?,
  (SELECT id FROM coverage WHERE coverage_type_id = 
    (SELECT id FROM coverage_type WHERE code = 'equipment_coverage')),
  se.vehicle_id,
  SUM(se.value)
FROM special_equipment se
WHERE se.vehicle_id = ?
AND se.status_id = 1
GROUP BY se.vehicle_id;
```

### Premium Calculation Flow
1. Calculate base coverages
2. Add vehicle-specific coverages
3. Calculate equipment premiums
4. Apply discounts
5. Add fees
6. Calculate payment schedule

## Business Summary for Stakeholders
### What We're Building
A comprehensive coverage selection system with dedicated special equipment tracking. The system uses normalized tables to track equipment separately from standard coverages, enabling accurate valuation, proper premium calculation, and detailed reporting. Users can add multiple equipment items per vehicle with full details and valuation.

### Why It's Needed
Special equipment like custom parts, audio systems, and business equipment represents significant additional value that standard policies don't cover. By tracking equipment in dedicated tables, we can properly underwrite these items, calculate appropriate premiums, and ensure adequate coverage limits. This prevents coverage gaps and claim disputes.

### Expected Outcomes
- Accurate equipment valuation and coverage
- Proper premium calculation for added risk
- Detailed equipment inventory for claims
- Better underwriting with equipment details
- Reduced coverage disputes
- Enhanced customer satisfaction
- Compliance with equipment disclosure

## Technical Summary for Developers
### Key Technical Decisions
- **Architecture Pattern**: Normalized equipment tables
- **Data Model**: Separate equipment from coverage
- **Integration**: Link equipment to vehicles
- **Calculation**: Include in premium calculation
- **Validation**: Value limits and type restrictions

### Implementation Guidelines
- Create equipment during coverage selection
- Link each equipment to specific vehicle
- Calculate total equipment value per vehicle
- Create equipment coverage based on value
- Include equipment premium in total
- Validate against program limits
- Store complete equipment details
- Enable equipment management UI

### UI Flow
```
Coverage Selection
├── Standard Coverages
│   ├── Policy-wide
│   └── Per-vehicle
├── Special Equipment
│   ├── Add Equipment
│   │   ├── Select Type
│   │   ├── Enter Details
│   │   └── Set Value
│   └── Equipment List
│       ├── Edit
│       └── Remove
└── Payment Options
    ├── Payment Plan
    └── Down Payment
```

## Validation Criteria
### Pre-Implementation Checkpoints
- [ ] v5.3 equipment tables created
- [ ] Equipment types populated
- [x] Coverage infrastructure exists
- [x] Vehicle relationships ready
- [x] Premium calculation service
- [x] Payment plan tables exist

### Success Metrics
- [ ] Equipment adds to vehicles
- [ ] Types categorize properly
- [ ] Values validate correctly
- [ ] Premium includes equipment
- [ ] Coverage limits apply
- [ ] Payment plans calculate
- [ ] Navigation preserves data
- [ ] Equipment reports generate

## Approval Section
**Status**: Ready for Review  
**Database Changes**: 2 new tables from v5.3  
**Pattern Reuse**: 98% - New equipment tables, existing patterns  
**Risk Level**: Low - Standard normalized approach  
**Next Steps**: Create v5.3 tables, implement equipment UI  
**Reviewer Comments**: [Proper normalization for equipment]  
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER