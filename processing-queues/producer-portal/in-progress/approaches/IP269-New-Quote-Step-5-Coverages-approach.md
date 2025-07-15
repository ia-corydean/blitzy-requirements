# IP269-New-Quote-Step-5-Coverages - Implementation Approach

## Requirement Understanding

The Coverage Selection step enables agents/producers to customize insurance coverage options for quotes. This step must:

- Display available coverages organized by type (policy-wide vs. vehicle-specific)
- Provide dropdowns for selecting limits and deductibles per coverage type
- Support optional coverages with checkboxes (like additional equipment)
- Automatically recalculate premiums based on selection changes
- Handle installment payment options with down payment percentage
- Enforce state/underwriting minimum requirements
- Ensure all required coverages are selected before proceeding

This is a critical step that balances coverage adequacy with affordability while ensuring compliance with underwriting rules.

## Domain Classification
- Primary Domain: ProducerPortal
- Cross-Domain Impact: No
- Complexity Level: Medium

## Pattern Analysis

### Reusable Patterns Identified

**From Infrastructure Codebase:**
- **Existing Coverage Model**: Complete coverage implementation with limits, deductibles, and premium tracking
- **CoverageResource**: Sophisticated formatting for different coverage types and limit formats
- **PolicySummaryService**: Coverage retrieval and transformation patterns
- **Coverage Types**: Comprehensive list of standard coverages (BI, PD, COMP, COLL, PIP, MED, etc.)

**From Global Requirements:**
- **[GR-04 - Validation & Data Handling]**: Multi-layer validation for coverage minimums
- **[GR-07 - Reusable Components]**: Component patterns for forms and selections
- **[GR-20 - Application Business Logic]**: Service layer patterns for premium calculation
- **[GR-33 - Data Services & Caching]**: Caching strategies for coverage options
- **[GR-11 - Accessibility]**: WCAG compliance for dropdowns and selections

**From Approved ProducerPortal Requirements:**
- **[IP269-New-Quote-Step-2-Drivers]**: Pattern for dynamic form updates and validation
- **[IP269-New-Quote-Step-3-Vehicles]**: Vehicle-specific data association patterns

### Domain-Specific Needs
- **Premium Recalculation**: Real-time premium updates on coverage changes
- **Installment Options**: Down payment percentage and payment scheduling
- **Additional Equipment**: Dynamic fields for equipment type and value
- **State-Specific Minimums**: Coverage requirements vary by state
- **Coverage Bundling**: Some coverages may be bundled or have dependencies

## Proposed Implementation

### Simplification Approach
- **Current Complexity**: Multiple coverage types, dynamic pricing, state-specific rules, installment calculations
- **Simplified Solution**: 
  - Leverage existing Coverage model and CoverageResource patterns
  - Use the established coverage type categories (liability, medical, physical_damage, etc.)
  - Implement simple dropdown selection with predefined limit/deductible options
  - Store installment preferences separately from coverage selection
  - Use existing premium field rather than complex real-time calculation initially
- **Trade-offs**: 
  - Gain: Faster implementation using proven patterns, maintainable code
  - Lose: Real-time dynamic pricing (can be added later with rating engine integration)

### Technical Approach

#### Phase 1: Database Schema Enhancement
- [ ] Create `quote_coverage` table mirroring the existing coverage structure
- [ ] Create `coverage_limit_option` table for available limits per coverage type
- [ ] Create `coverage_deductible_option` table for available deductibles
- [ ] Create `map_quote_installment` table for payment preferences
- [ ] Add `additional_equipment` JSON field for equipment details

#### Phase 2: Backend Implementation
- [ ] Create `QuoteCoverageService` extending patterns from PolicySummaryService
- [ ] Implement coverage options retrieval with state-specific filtering
- [ ] Create API endpoints for:
  - GET available coverages by state/program
  - POST/PUT coverage selections
  - GET premium recalculation
- [ ] Implement validation for required coverages and minimums
- [ ] Add installment calculation logic

#### Phase 3: Frontend Implementation
- [ ] Create `CoverageSelectionForm` component with:
  - Policy-wide coverage section
  - Vehicle-specific coverage section
  - Additional equipment section
- [ ] Implement coverage dropdowns using existing select patterns
- [ ] Create `InstallmentOptions` component for payment preferences
- [ ] Add real-time premium display updates
- [ ] Implement mobile-responsive accordion layout

#### Phase 4: Integration & Validation
- [ ] Integrate with quote flow navigation
- [ ] Validate state-specific requirements
- [ ] Ensure accessibility compliance
- [ ] Add comprehensive test coverage

## Risk Assessment

- **Risk 1**: Complex state-specific requirements → Mitigation: Start with common requirements, add state variations incrementally
- **Risk 2**: Premium calculation accuracy → Mitigation: Use pre-calculated premiums initially, integrate rating engine later
- **Risk 3**: Coverage dependencies → Mitigation: Implement simple validation rules, enhance as needed
- **Risk 4**: Performance with many coverages → Mitigation: Use efficient queries and caching

## Context Preservation

- **Key Decisions**: 
  - Reuse existing Coverage model patterns
  - Separate installment preferences from coverage selection
  - Use predefined limit/deductible options
  - Leverage CoverageResource formatting logic
  
- **Dependencies**: 
  - Builds on quote flow (Steps 1-4)
  - Uses existing Coverage infrastructure
  - Requires underwriting eligibility from Step 4
  
- **Future Impact**: 
  - Enables Step 6 (Quote Review) with complete coverage details
  - Foundation for policy binding with selected coverages
  - Supports future rating engine integration

## Approval Section
**Status**: PENDING APPROVAL
**Reviewer Comments**: [Space for feedback]
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER