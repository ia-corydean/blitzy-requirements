# IP269-ITC-Bridge-New-Info-2 - Implementation Approach v2

## Revision Notes
- **v2 Changes**: Incorporates all feedback from prompt15.md
- **Key Updates**: 
  - Uses driver.source_entity_id for tracking
  - Leverages session infrastructure
  - Aligns with photo and employment changes
  - Consistent with v2 updates across all approaches

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
- Entity-based source tracking

## Proposed Implementation

### Simplification Approach
- Current Complexity: Mandatory validation, progression blocking
- Simplified Solution: Use existing driver table with entity source tracking
- Trade-offs: Need to track review status for blocking logic

### Technical Approach
1. **Phase 1**: Bridge Data Reception
   - [ ] Receive external data response
   - [ ] Parse discovered drivers
   - [ ] Create/retrieve ITC entity
   - [ ] Store verification results
   - [ ] Link to entity source

2. **Phase 2**: Driver Creation
   - [ ] Create driver records
   - [ ] Set source_entity_id to ITC
   - [ ] Set is_excluded = true
   - [ ] Link employment_id if found
   - [ ] Link to quote

3. **Phase 3**: Alert Display
   - [ ] Show warning alert card
   - [ ] Yellow/orange background
   - [ ] List discovered drivers
   - [ ] Add "Missing Info" badges
   - [ ] Include "Exclude All" CTA
   - [ ] Query by source_entity_id

4. **Phase 4**: Progression Blocking
   - [ ] Disable Continue button
   - [ ] Check review status
   - [ ] Query unreviewed drivers
   - [ ] Show blocking reason
   - [ ] Update dynamically

5. **Phase 5**: Driver Review
   - [ ] Open side panel on click
   - [ ] Show required fields
   - [ ] Allow inclusion toggle
   - [ ] Capture employment_id
   - [ ] Capture occupation_id
   - [ ] Update driver record

6. **Phase 6**: Bulk Actions
   - [ ] Implement "Exclude All"
   - [ ] Update all discovered
   - [ ] Clear blocking status
   - [ ] Recalculate premium
   - [ ] Remove alert banner

7. **Phase 7**: Premium Updates
   - [ ] Detect inclusion changes
   - [ ] Trigger rating engine
   - [ ] Update display real-time
   - [ ] Show price differences
   - [ ] Maintain calculation log

## Risk Assessment
- **Risk 1**: User frustration from blocking → Mitigation: Clear messaging, bulk actions
- **Risk 2**: Incomplete data submission → Mitigation: Field validation, required indicators
- **Risk 3**: Performance with many drivers → Mitigation: Indexed queries, caching
- **Risk 4**: Lost work on navigation → Mitigation: Session storage, confirmation
- **Risk 5**: Incorrect exclusions → Mitigation: Review summary, undo capability
- **Risk 6**: Entity reference issues → Mitigation: Ensure ITC entity exists

## Context Preservation
- Key Decisions: Mandatory review, entity-based tracking, session storage
- Dependencies: Entity infrastructure, session management, rating engine
- Future Impact: Pattern for all mandatory validation flows

## Database Requirements Summary
- **New Tables**: 0 tables need to be created
- **Existing Tables**: 8+ tables will be reused
- **Modified Tables**: 0 tables need modifications

## Database Schema Analysis

### Existing Tables to Use

1. **driver**: Discovered driver storage
   - Store all driver info
   - Use source_entity_id for ITC
   - Track is_excluded status
   - Link employment_id
   - Link occupation_id

2. **entity**: Source tracking
   - ITC entity record
   - entity_type = 'integration'
   - Provides consistent source

3. **map_quote_driver**: Quote associations
   - Link discovered drivers
   - Could track reviewed_at
   - Maintain relationships

4. **verification**: Bridge results
   - Store discovery data
   - Track validation status
   - Link to entity source

5. **integration**: External service
   - ITC bridge config
   - Service endpoints
   - Error handling

6. **quote**: Quote being validated
   - Track blocking status
   - Update premium
   - Store review state

7. **status**: Driver statuses
   - Missing Info status
   - Reviewed status
   - Excluded status

8. **session**: Review state
   - Track progress in JSON
   - Store blocking reasons
   - Maintain UI state

### Blocking Implementation

Using session.data for tracking:
```json
{
  "bridge_review": {
    "discovered_drivers": [123, 124, 125],
    "reviewed_drivers": [123],
    "unreviewed_count": 2,
    "blocking": true,
    "last_action": "2023-10-15 14:30:00"
  }
}
```

### Query Patterns
```sql
-- Find unreviewed bridge drivers
SELECT d.*, n.first_name, n.last_name,
  CASE 
    WHEN d.employment_id IS NULL THEN 'Missing Info'
    WHEN d.occupation_id IS NULL THEN 'Missing Info'
    ELSE 'Complete'
  END as info_status
FROM driver d
JOIN name n ON d.name_id = n.id
JOIN map_quote_driver mqd ON d.id = mqd.driver_id
JOIN entity e ON d.source_entity_id = e.id
WHERE mqd.quote_id = ?
AND e.code = 'ITC_BRIDGE'
AND (d.employment_id IS NULL OR d.occupation_id IS NULL);

-- Check if blocking needed
SELECT COUNT(*) > 0 as should_block
FROM driver d
JOIN map_quote_driver mqd ON d.id = mqd.driver_id
JOIN entity e ON d.source_entity_id = e.id
WHERE mqd.quote_id = ?
AND e.code = 'ITC_BRIDGE'
AND d.is_excluded = false
AND (d.employment_id IS NULL OR d.occupation_id IS NULL);
```

### Status Badge Logic
- Check driver.source_entity_id = ITC entity
- Check employment_id IS NULL
- Check occupation_id IS NULL
- Display "Missing Info" if incomplete
- Clear badge after update

## Business Summary for Stakeholders
### What We're Building
A mandatory validation system that ensures all household members discovered through external data sources are properly reviewed before allowing quote progression. Using entity-based source tracking and session management, the system displays prominent warnings, requires producers to make explicit decisions about each discovered driver, and blocks advancement until all drivers are addressed with complete employment and occupation information.

### Why It's Needed
Undisclosed drivers are a leading cause of claim denials and premium disputes. This mandatory review process with comprehensive data collection ensures no discovered driver is overlooked, all required information is captured (including employment and occupation), and proper risk assessment occurs. The entity-based tracking provides full audit trails of data sources.

### Expected Outcomes
- Zero quotes with unreviewed discovered drivers
- Complete employment/occupation data capture
- Full source traceability via entities
- Clear audit trail of all decisions
- Improved premium accuracy
- Reduced downstream corrections
- Enhanced compliance tracking

## Technical Summary for Developers
### Key Technical Decisions
- **Architecture Pattern**: Entity-based source tracking with session state
- **Source Tracking**: driver.source_entity_id references ITC entity
- **Review State**: Session.data JSON for UI state
- **Blocking Logic**: Query-based validation
- **Data Requirements**: employment_id and occupation_id mandatory
- **Alert Strategy**: Warning banners with badge indicators

### Implementation Guidelines
- Ensure ITC entity exists
- Set source_entity_id on creation
- Store UI state in session
- Build blocking validation service
- Create warning alert component
- Implement badge status logic
- Check employment/occupation
- Build bulk exclusion action
- Integrate side panel editing
- Handle real-time updates

### Integration Points
```
1. Entity Management
   - Create/retrieve ITC entity
   - Set integration type
   - Use for source tracking

2. Session Management  
   - Store review progress
   - Track blocking state
   - Maintain UI preferences

3. Employment/Occupation
   - Reference new tables (v5.3)
   - Validate data presence
   - Show in side panel
```

## Validation Criteria
### Pre-Implementation Checkpoints
- [x] Driver has source_entity_id
- [x] Entity infrastructure ready
- [x] Session management available
- [x] Employment tables exist (v5.3)
- [x] Occupation tables exist (v5.3)
- [x] Status management ready
- [x] Quote blocking possible

### Success Metrics
- [ ] ITC entity references work
- [ ] Warning alerts display
- [ ] Continue button blocks
- [ ] Badges show correctly
- [ ] Side panel collects data
- [ ] Employment/occupation save
- [ ] Bulk exclude functions
- [ ] Premium updates real-time
- [ ] Session tracks progress
- [ ] Unblocking works properly

## Approval Section
**Status**: Ready for Review  
**Database Changes**: None - uses existing v5.3 infrastructure  
**Pattern Reuse**: 100% - Entity and session patterns  
**Risk Level**: High - Blocks critical user flow  
**Next Steps**: Review approach and implement with v5.3 schema  
**Reviewer Comments**: [Updated with all v2 feedback incorporated]  
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER