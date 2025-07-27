# IP269-ITC-Bridge-New-Info-2 - Implementation Approach

## Requirement Understanding
The ITC Bridge New Info Option 2 provides a more stringent approach to handling discovered drivers from external data enrichment. Unlike Option 1 which allows flexible handling, this version blocks quote advancement until all discovered drivers are explicitly reviewed and assigned a status (included or excluded). The system displays warning-style alerts, requires individual or bulk action on each discovered driver, and recalculates premiums in real-time based on inclusion decisions.

## Domain Classification
- Primary Domain: Producer Portal / Quote Management
- Cross-Domain Impact: Yes - Blocks quote progression, affects underwriting
- Complexity Level: High

## Pattern Analysis

### Reusable Patterns Identified
- [GR-69]: Producer Portal Architecture - Quote blocking patterns
- [GR-53]: DCS Integration Architecture - External data validation
- [GR-52]: Universal Entity Management - Driver entity management
- [GR-44]: Communication Architecture - Warning notifications
- [GR-20]: Business Logic Standards - Inclusion validation rules

### Domain-Specific Needs
- Blocking mechanism for quote progression
- Warning-style alert banners
- Mandatory driver status assignment
- Individual and bulk exclusion options
- Real-time premium recalculation
- Missing info badge indicators
- Side panel driver editing

## Proposed Implementation

### Simplification Approach
- Current Complexity: Mandatory validation, progression blocking
- Simplified Solution: Use existing driver table with validation flags
- Trade-offs: Need to track review status for blocking logic

### Technical Approach
1. **Phase 1**: Bridge Data Display
   - [ ] Show warning alert card
   - [ ] Yellow/orange background style
   - [ ] List discovered drivers
   - [ ] Add "Missing Info" badges
   - [ ] Include "Exclude All" CTA

2. **Phase 2**: Progression Blocking
   - [ ] Disable Continue button
   - [ ] Track review status
   - [ ] Require all drivers addressed
   - [ ] Show blocking reason
   - [ ] Update dynamically

3. **Phase 3**: Driver Review
   - [ ] Open side panel on click
   - [ ] Show required fields
   - [ ] Allow inclusion toggle
   - [ ] Capture missing data
   - [ ] Update driver record

4. **Phase 4**: Bulk Actions
   - [ ] Implement "Exclude All"
   - [ ] Update all discovered
   - [ ] Clear blocking status
   - [ ] Recalculate premium
   - [ ] Remove alert banner

5. **Phase 5**: Individual Actions
   - [ ] Update single driver
   - [ ] Validate required fields
   - [ ] Update badge status
   - [ ] Check all reviewed
   - [ ] Enable progression

6. **Phase 6**: Premium Updates
   - [ ] Detect inclusion changes
   - [ ] Trigger rating engine
   - [ ] Update display real-time
   - [ ] Show price differences
   - [ ] Maintain calculation log

## Risk Assessment
- **Risk 1**: User frustration from blocking → Mitigation: Clear messaging, bulk actions
- **Risk 2**: Incomplete data submission → Mitigation: Field validation, required indicators
- **Risk 3**: Performance with many drivers → Mitigation: Batch updates, caching
- **Risk 4**: Lost work on navigation → Mitigation: Auto-save, confirmation prompts
- **Risk 5**: Incorrect exclusions → Mitigation: Review summary, undo capability

## Context Preservation
- Key Decisions: Mandatory review, progression blocking, warning styling
- Dependencies: Bridge data service, driver management, rating engine
- Future Impact: Sets precedent for mandatory data validation flows

## Database Requirements Summary
- **New Tables**: 0 tables need to be created
- **Existing Tables**: 6+ tables will be reused
- **Modified Tables**: 0-1 tables may need enhancement

## Database Schema Analysis

### Existing Tables to Use

1. **driver**: Discovered driver storage
   - Store all driver info
   - Track inclusion status
   - Use is_excluded flag
   - Link to quote

2. **map_quote_driver**: Quote associations
   - Link discovered drivers
   - Track review status
   - Could add reviewed_at field

3. **verification**: Bridge results
   - Store discovery data
   - Track validation status
   - Link to drivers found

4. **integration**: External service
   - ITC bridge config
   - Service endpoints
   - Error handling

5. **quote**: Quote being validated
   - Track blocking status
   - Update premium
   - Store review state

6. **status**: Driver statuses
   - Missing Info status
   - Reviewed status
   - Excluded status

### Blocking Implementation Options

Option 1: Add to map_quote_driver
```sql
ALTER TABLE map_quote_driver
ADD COLUMN reviewed_at TIMESTAMP NULL,
ADD COLUMN review_required BOOLEAN DEFAULT FALSE;
```

Option 2: Use verification table
- Track review status in verification
- Calculate blocking from driver states

Option 3: Session/frontend state
- Track review status in UI
- Block based on driver attributes

Recommended: Option 2 - Use existing tables

### Status Badge Logic
- Check driver.lookup_source = 'ITC_BRIDGE'
- Check for required fields empty
- Display "Missing Info" badge
- Clear badge after update

## Business Summary for Stakeholders
### What We're Building
A mandatory validation system that ensures all household members discovered through external data sources are properly reviewed before allowing quote progression. The system displays prominent warnings, requires producers to make explicit decisions about each discovered driver, and blocks advancement until all drivers are addressed. This creates a more controlled and compliant quote process.

### Why It's Needed
Undisclosed drivers are a leading cause of claim denials and premium disputes. This mandatory review process ensures no discovered driver is overlooked, reducing underwriting risk and improving quote accuracy. The blocking mechanism prevents accidental submission of incomplete information while the warning styling draws immediate attention to critical data that needs review.

### Expected Outcomes
- Zero quotes submitted with unreviewed discovered drivers
- Reduced underwriting errors from missed household members  
- Clear audit trail of inclusion/exclusion decisions
- Improved premium accuracy through complete driver lists
- Enhanced compliance with carrier requirements
- Reduced downstream policy corrections

## Technical Summary for Developers
### Key Technical Decisions
- **Architecture Pattern**: State-based progression blocking
- **Review Tracking**: Calculate from driver attributes
- **Alert Strategy**: Warning-style persistent banner
- **Validation Approach**: Frontend blocking with backend verification
- **Premium Updates**: Real-time recalculation on changes

### Implementation Guidelines
- Create warning alert component
- Build progression blocking logic
- Implement review state tracking
- Add bulk exclusion action
- Create side panel integration
- Build validation framework
- Handle real-time updates
- Maintain review audit trail

## Validation Criteria
### Pre-Implementation Checkpoints
- [x] Driver infrastructure exists
- [x] Verification system ready
- [x] Status management available
- [x] Quote blocking possible
- [x] Side panel framework exists
- [x] Premium recalculation ready

### Success Metrics
- [ ] Warning alerts display prominently
- [ ] Continue button blocks properly
- [ ] Individual review works
- [ ] Bulk exclude functions
- [ ] Required fields enforce
- [ ] Premium updates real-time
- [ ] Badges update correctly
- [ ] Unblocking works properly

## Approval Section
**Status**: Ready for Review  
**Database Verification**: All required tables exist  
**Pattern Reuse**: 100% - Using existing infrastructure  
**Risk Level**: High - Blocks critical user flow  
**Next Steps**: Review approach and approve for implementation  
**Reviewer Comments**: [Pending]  
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER