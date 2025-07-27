# IP286-Re-Quoting - Implementation Approach

## Requirement Understanding
The Re-Quoting feature enables users to generate new quotes by leveraging data from existing policies. This streamlines the quoting process by reusing validated data while allowing updates for changed circumstances. The system must handle flagging of new/changed information, support editing of all quote components, and seamlessly integrate with the existing quote and bind workflows. This is particularly valuable for renewals, post-cancellation re-engagement, or life change scenarios.

## Domain Classification
- Primary Domain: Producer Portal / Quote Management
- Cross-Domain Impact: Yes - Integrates with Policy, Quote, Bind workflows
- Complexity Level: Medium

## Pattern Analysis

### Reusable Patterns Identified
- [GR-69]: Producer Portal Architecture - Quote generation patterns
- [GR-52]: Universal Entity Management - Reuse driver, vehicle, coverage entities
- [GR-41]: Database Standards - Audit fields and status management
- [GR-64]: Policy Reinstatement Process - Re-engagement patterns
- [GR-18]: Workflow Requirements - Multi-step quote process

### Domain-Specific Needs
- Policy data extraction and cloning
- Change detection and flagging
- Address verification integration
- Driver discovery handling
- Effective date management
- Visual change indicators
- Seamless transition to bind workflow

## Proposed Implementation

### Simplification Approach
- Current Complexity: Need to clone policy data and detect changes
- Simplified Solution: Use existing quote table with policy_id link, leverage quote workflows
- Trade-offs: None - infrastructure already supports requoting

### Technical Approach
1. **Phase 1**: Requote Initiation
   - [ ] Create requote dialog component
   - [ ] Set effective date (default today)
   - [ ] Create new quote linked to policy_id
   - [ ] Copy policy data to quote tables

2. **Phase 2**: Data Cloning
   - [ ] Clone drivers from map_policy_driver to map_quote_driver
   - [ ] Clone vehicles from map_policy_vehicle to map_quote_vehicle
   - [ ] Clone coverages from map_policy_coverage to map_quote_coverage
   - [ ] Preserve original data for comparison

3. **Phase 3**: Change Detection
   - [ ] Run address verification for primary insured
   - [ ] Check for household driver changes
   - [ ] Flag any data discrepancies
   - [ ] Store change indicators in quote metadata

4. **Phase 4**: Review Quote Screen
   - [ ] Reuse IP269 Step 6 Review Quote
   - [ ] Add change notification components
   - [ ] Implement address selection modal
   - [ ] Add driver inclusion/exclusion handling
   - [ ] Visual highlighting for changes

5. **Phase 5**: Edit Capabilities
   - [ ] Enable navigation to quote steps
   - [ ] Pass requote context through workflows
   - [ ] Maintain change tracking
   - [ ] Update premium calculations

6. **Phase 6**: Bind Integration
   - [ ] Seamless transition to bind workflow
   - [ ] Pass requote context for proper handling
   - [ ] Complete standard bind steps
   - [ ] Create new policy from requote

## Risk Assessment
- **Risk 1**: Data synchronization issues → Mitigation: Transactional cloning process
- **Risk 2**: Change detection accuracy → Mitigation: Comprehensive verification rules
- **Risk 3**: User confusion with changes → Mitigation: Clear visual indicators, explanations
- **Risk 4**: Performance with large policies → Mitigation: Optimize cloning queries
- **Risk 5**: Regulatory compliance → Mitigation: Maintain complete audit trail

## Context Preservation
- Key Decisions: Use policy_id link, clone all data, leverage existing workflows
- Dependencies: Policy system, quote workflows, bind process, verification services
- Future Impact: Foundation for renewals, policy comparisons, bulk requoting

## Database Requirements Summary
- **New Tables**: 0 tables need to be created
- **Existing Tables**: 20+ tables will be reused as-is
- **Modified Tables**: 0 existing tables need modifications

## Database Schema Analysis

### Core Tables (All Exist)
1. **quote**: Already has policy_id field for source linking
   - Fields support renewal tracking (is_renewal, renewal_policy_id)
   - Version number for quote iterations
   - Ready for requote implementation

2. **policy**: Source data for requoting
   - Complete policy information available
   - All relationships intact for cloning

3. **quote_type**: Can define "Requote" type
   - Distinguishes from new business quotes

### Cloning Process Tables (All Exist)
1. **map_policy_driver** → **map_quote_driver**
2. **map_policy_vehicle** → **map_quote_vehicle**
3. **map_policy_coverage** → **map_quote_coverage**
4. **driver**: Shared driver records
5. **vehicle**: Shared vehicle records
6. **coverage**: Coverage definitions

### Supporting Tables (All Exist)
1. **address**: Address verification results
2. **verification**: External verification tracking
3. **discount**: Available discounts
4. **rate**: Premium calculations
5. **program**: Rating rules

### Change Tracking
- Use quote.external_reference for change flags
- Store change details in transaction metadata
- Leverage audit tables for history

## Business Summary for Stakeholders
### What We're Building
A requoting system that creates new insurance quotes using existing policy data as a starting point. The system automatically detects changes like new addresses or household members, allows editing of all quote components, and seamlessly guides users through the binding process to create a new policy.

### Why It's Needed
Creating quotes from scratch is time-consuming and error-prone, especially for existing customers. Requoting enables fast, accurate quote generation for renewals, policy updates after life changes, or win-back scenarios after cancellation. This improves efficiency and customer retention.

### Expected Outcomes
- Quote creation time reduced by 75% for existing customers
- Improved data accuracy through reuse of validated information
- Better customer retention through easy renewal process
- Increased conversion rates for cancelled policies
- Streamlined workflow for producers handling policy changes

## Technical Summary for Developers
### Key Technical Decisions
- **Architecture Pattern**: Clone policy data to quote tables with source tracking
- **Change Detection**: Real-time verification with visual flagging
- **Workflow Integration**: Reuse existing quote/bind workflows with context
- **Data Strategy**: Full cloning ensures independence from source policy
- **State Management**: Quote-based state with policy reference

### Implementation Guidelines
- Create requote service for data cloning
- Implement change detection algorithms
- Build visual components for change indicators
- Extend quote workflows with requote context
- Use database transactions for cloning
- Add verification service integration
- Implement proper error handling
- Cache frequently accessed policy data

## Validation Criteria
### Pre-Implementation Checkpoints
- [x] Quote table has policy_id field
- [x] All mapping tables exist for cloning
- [x] Quote workflows ready for reuse
- [x] Bind process supports quotes
- [x] Verification services available
- [x] Change tracking infrastructure exists

### Success Metrics
- [ ] Requote dialog launches correctly
- [ ] Policy data clones completely
- [ ] Changes detected and flagged
- [ ] Address verification works
- [ ] Driver discovery functions
- [ ] All sections editable
- [ ] Premium recalculates accurately
- [ ] Bind process completes successfully

## Approval Section
**Status**: Ready for Review  
**Database Verification**: All required tables exist with proper structure  
**Pattern Reuse**: 100% - No new tables needed  
**Risk Level**: Medium - Complex data flow but proven infrastructure  
**Next Steps**: Review approach and approve for implementation  
**Reviewer Comments**: [Pending]  
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER