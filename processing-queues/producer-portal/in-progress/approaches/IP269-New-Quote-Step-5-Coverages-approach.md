# IP269-New-Quote-Step-5-Coverages - Implementation Approach

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
- Additional equipment coverage entry
- State-mandated minimum enforcement
- Real-time premium recalculation
- Payment plan selection
- Down payment percentage configuration

## Proposed Implementation

### Simplification Approach
- Current Complexity: Multiple coverage types, limits, deductibles, validation
- Simplified Solution: Leverage existing coverage infrastructure
- Trade-offs: May need to enhance coverage table for equipment

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

3. **Phase 3**: Additional Equipment
   - [ ] Add equipment fields to coverage
   - [ ] Capture equipment type
   - [ ] Validate equipment value
   - [ ] Include in premium calculation
   - [ ] Store with coverage selection

4. **Phase 4**: Validation Rules
   - [ ] Check state minimums
   - [ ] Enforce required coverages
   - [ ] Validate limit/deductible combinations
   - [ ] Block invalid selections
   - [ ] Show clear error messages

5. **Phase 5**: Premium Calculation
   - [ ] Call rating service on changes
   - [ ] Display premium breakdown
   - [ ] Show fees separately
   - [ ] Update total in real-time
   - [ ] Handle calculation errors

6. **Phase 6**: Payment Configuration
   - [ ] Payment plan selection
   - [ ] Down payment percentage
   - [ ] First installment date
   - [ ] Calculate payment schedule
   - [ ] Display payment summary

7. **Phase 7**: Save & Navigation
   - [ ] Save all selections to map_quote_coverage
   - [ ] Validate all required selected
   - [ ] Enable continue when valid
   - [ ] Navigate to Step 6 Review

## Risk Assessment
- **Risk 1**: Complex rating calculations → Mitigation: Robust rating service
- **Risk 2**: State regulation compliance → Mitigation: Database-driven rules
- **Risk 3**: Performance with many coverages → Mitigation: Optimized queries
- **Risk 4**: Equipment coverage complexity → Mitigation: Simple UI design
- **Risk 5**: Payment calculation errors → Mitigation: Comprehensive testing

## Context Preservation
- Key Decisions: Use existing tables, enhance for equipment, integrate rating
- Dependencies: Coverage definitions, rating service, state rules, payment plans
- Future Impact: Foundation for accurate premiums and policy issuance

## Database Requirements Summary
- **New Tables**: 0 tables need to be created
- **Existing Tables**: 15+ tables will be reused
- **Modified Tables**: 1 table may need enhancement (coverage for equipment)

## Database Schema Requirements

### Potential Enhancement

#### coverage (May Need Equipment Fields)
If not storing equipment in separate table:
```sql
ALTER TABLE coverage
ADD COLUMN has_equipment BOOLEAN DEFAULT FALSE AFTER is_selected,
ADD COLUMN equipment_type VARCHAR(100) AFTER has_equipment,
ADD COLUMN equipment_value DECIMAL(10,2) AFTER equipment_type,
ADD INDEX idx_has_equipment (has_equipment);
```

### Existing Tables to Use

1. **coverage**: Coverage definitions
   - Has type, limit, deductible references
   - Tracks selection and requirements
   - Stores premium amounts

2. **coverage_type**: Coverage categories
   - Bodily Injury, Property Damage, etc.
   - Policy-wide vs vehicle-specific

3. **limit**: Coverage limit options
   - Available limit values
   - Min/max constraints

4. **limit_type**: Limit categories
   - Per person, per accident, etc.

5. **deductible**: Deductible options
   - Available deductible amounts
   - Coverage-specific options

6. **deductible_type**: Deductible categories
   - Comprehensive, collision, etc.

7. **map_quote_coverage**: Quote coverage selections
   - Links selected coverages to quote
   - Tracks user selections

8. **map_program_coverage**: Program coverage rules
   - Available coverages by program
   - Required coverage flags

9. **map_program_limit**: Program limit rules
   - Available limits by program
   - State minimum enforcement

10. **map_program_deductible**: Program deductible rules
    - Available deductibles by program
    - Default selections

11. **payment_plan**: Payment options
    - Full pay, monthly, etc.
    - Down payment requirements

12. **rate**: Premium calculation rules
    - Rating factors and algorithms

13. **fee**: Additional fees
    - Policy fees, installment fees

14. **state**: State regulations
    - Minimum coverage requirements

15. **vehicle**: For vehicle-specific coverages
    - Links coverages to vehicles

## Business Summary for Stakeholders
### What We're Building
A comprehensive coverage selection system that allows producers to customize insurance policies with appropriate limits and deductibles, add optional coverages like equipment protection, configure payment plans, and see real-time premium calculations. The system enforces state requirements and underwriting rules while providing flexibility for customer needs.

### Why It's Needed
Manual coverage selection is error-prone and time-consuming, often resulting in non-compliant quotes or calculation mistakes. This automated system ensures proper coverage selection, accurate premium calculation, and regulatory compliance while providing a smooth user experience that helps producers create competitive, compliant quotes quickly.

### Expected Outcomes
- Reduced quote creation time through intuitive selection interface
- Improved accuracy with automated validation and calculations
- Better compliance with state-mandated minimums
- Increased conversion rates through flexible payment options
- Enhanced customer satisfaction with transparent pricing

## Technical Summary for Developers
### Key Technical Decisions
- **Architecture Pattern**: Leverage existing coverage tables with potential enhancement
- **Calculation Strategy**: Real-time rating service integration
- **Validation Approach**: Database-driven rules with client-side preview
- **State Management**: Quote-scoped coverage selections
- **Payment Integration**: Configurable payment plans with down payment options

### Implementation Guidelines
- Build dynamic coverage loader by program
- Implement limit/deductible cascading dropdowns
- Create equipment coverage component
- Integrate with rating microservice
- Build validation rule engine
- Implement debounced recalculation
- Cache program rules for performance
- Handle async rating responses

## Validation Criteria
### Pre-Implementation Checkpoints
- [x] Coverage tables exist with relationships
- [x] Limit and deductible tables ready
- [x] Program mapping tables available
- [x] Payment plan infrastructure exists
- [x] Rating service defined
- [ ] Equipment fields may need addition

### Success Metrics
- [ ] Coverages display by program
- [ ] Dropdowns populate correctly
- [ ] Equipment coverage captures
- [ ] State minimums enforce
- [ ] Premium recalculates on change
- [ ] Payment options configure
- [ ] Required coverages validate
- [ ] Continue enables when valid

## Approval Section
**Status**: Ready for Review  
**Database Changes**: May need 3 equipment fields in coverage table  
**Pattern Reuse**: 98% - Minor enhancement for equipment coverage  
**Risk Level**: Medium - Complex calculations but proven infrastructure  
**Next Steps**: Review approach, confirm equipment storage strategy, implement  
**Reviewer Comments**: [Pending]  
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER