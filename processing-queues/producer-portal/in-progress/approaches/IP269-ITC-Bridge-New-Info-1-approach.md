# IP269-ITC-Bridge-New-Info-1 - Implementation Approach

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
- Simplified Solution: Use existing driver infrastructure with bridge flags
- Trade-offs: Need to track data source for discovered drivers

### Technical Approach
1. **Phase 1**: Bridge Data Reception
   - [ ] Receive external data response
   - [ ] Parse discovered drivers
   - [ ] Match against existing drivers
   - [ ] Identify new discoveries
   - [ ] Store bridge results

2. **Phase 2**: Driver Creation
   - [ ] Create driver records for new
   - [ ] Set is_excluded = true default
   - [ ] Mark source as "bridge"
   - [ ] Link to quote
   - [ ] Preserve discovery metadata

3. **Phase 3**: Alert Display
   - [ ] Show inline banner in drivers
   - [ ] Highlight new discoveries
   - [ ] Count new drivers found
   - [ ] Indicate excluded status
   - [ ] Enable edit actions

4. **Phase 4**: Edit Flow
   - [ ] Open side panel on edit
   - [ ] Allow inclusion toggle
   - [ ] Show required fields
   - [ ] Validate included drivers
   - [ ] Update driver record

5. **Phase 5**: Premium Impact
   - [ ] Detect inclusion changes
   - [ ] Trigger rating recalc
   - [ ] Update premium display
   - [ ] Show price difference
   - [ ] Maintain calculation audit

6. **Phase 6**: Navigation
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

## Context Preservation
- Key Decisions: Default to excluded, track source, allow modifications
- Dependencies: External data service, driver management, rating engine
- Future Impact: Foundation for automated household discovery

## Database Requirements Summary
- **New Tables**: 0 tables need to be created
- **Existing Tables**: 5+ tables will be reused
- **Modified Tables**: 0-1 tables may need enhancement

## Database Schema Analysis

### Existing Tables to Use

1. **driver**: Store discovered drivers
   - Use is_excluded flag
   - Track all driver info
   - Link to quote

2. **map_quote_driver**: Quote-driver links
   - Associate new drivers
   - Track inclusion status

3. **verification**: Bridge results
   - Store external data response
   - Track verification source
   - Link discovered entities

4. **integration**: External service
   - ITC bridge configuration
   - API credentials
   - Service endpoints

5. **quote**: Quote being enriched
   - Update premium
   - Track bridge status
   - Store metadata

### Tracking Bridge Source
Options for tracking discovered drivers:
1. Use driver.lookup_source field
2. Add metadata to map_quote_driver
3. Use verification table references

Recommended: Set driver.lookup_source = 'ITC_BRIDGE'

### Alert Implementation
- Store alert state in session/frontend
- Calculate dynamically from driver source
- Show only for current session
- Clear after acknowledgment

## Business Summary for Stakeholders
### What We're Building
An intelligent system that automatically discovers additional household drivers through external data sources and presents them for review during the quote process. The system defaults discovered drivers to excluded status for safety, allows producers to include them with proper information collection, and automatically recalculates premiums based on changes.

### Why It's Needed
Undisclosed household members are a major source of underwriting risk and claim disputes. This automated discovery ensures all potential drivers are identified and properly documented, reducing risk while maintaining a smooth user experience. It helps maintain compliance with carrier requirements for household member disclosure.

### Expected Outcomes
- Improved risk assessment through complete household discovery
- Reduced claims disputes from undisclosed drivers
- Compliance with carrier disclosure requirements
- Transparent process for producers and customers
- Accurate premium calculation with all drivers considered

## Technical Summary for Developers
### Key Technical Decisions
- **Architecture Pattern**: Async bridge processing with UI notifications
- **Default Behavior**: Auto-exclude for safety, manual include
- **Data Storage**: Use existing driver tables with source tracking
- **Alert Strategy**: Session-based alerts, not persistent
- **Premium Updates**: Real-time recalculation on changes

### Implementation Guidelines
- Build bridge data parser service
- Create driver discovery logic
- Implement alert banner component
- Extend side panel for editing
- Add source tracking to drivers
- Integrate with rating service
- Handle async bridge responses
- Maintain user context

## Validation Criteria
### Pre-Implementation Checkpoints
- [x] Driver infrastructure exists
- [x] Verification system ready
- [x] Integration framework available
- [x] Quote modification supported
- [x] Rating recalculation possible
- [x] All tables present

### Success Metrics
- [ ] Bridge data processes correctly
- [ ] New drivers appear as excluded
- [ ] Alerts display prominently
- [ ] Edit panel functions properly
- [ ] Required fields enforce
- [ ] Premium updates on changes
- [ ] Navigation preserves state
- [ ] Source tracking works

## Approval Section
**Status**: Ready for Review  
**Database Verification**: All required tables exist  
**Pattern Reuse**: 100% - Using existing infrastructure  
**Risk Level**: Medium - External data dependency  
**Next Steps**: Review approach and approve for implementation  
**Reviewer Comments**: [Pending]  
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER