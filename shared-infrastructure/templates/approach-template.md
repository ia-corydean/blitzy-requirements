# [Requirement ID] - Implementation Approach

## Requirement Understanding
[Comprehensive analysis of the requirement]

## Domain Classification
- Primary Domain: [domain]
- Cross-Domain Impact: [Yes/No - specify domains]
- Complexity Level: [Low/Medium/High]

## Pattern Analysis

### Reusable Patterns Identified
- [GR-XX]: [How it applies]
- [Pattern from blitzy-requirements]: [Implementation reference]

### Domain-Specific Needs
- [Specific need 1]: [Why it's unique to this domain]
- [Specific need 2]: [How it differs from global patterns]

## Proposed Implementation

### Simplification Approach
- Current Complexity: [Description]
- Simplified Solution: [Description]
- Trade-offs: [What we gain/lose]

### Technical Approach
1. [Phase 1]: [Description]
   - [ ] Task 1
   - [ ] Task 2

2. [Phase 2]: [Description]
   - [ ] Task 3
   - [ ] Task 4

## Risk Assessment
- **Risk 1**: [Description] → Mitigation: [Strategy]
- **Risk 2**: [Description] → Mitigation: [Strategy]

## Context Preservation
- Key Decisions: [List important choices]
- Dependencies: [What this builds on]
- Future Impact: [What this enables]

## Database Requirements Summary
- **New Tables**: [count] tables need to be created
- **Existing Tables**: [count] tables will be reused as-is
- **Modified Tables**: [count] existing tables need modifications

## Database Schema Requirements

### New Tables Required
[List each new table with purpose and structure]

1. **[table_name]**: [Purpose description]
   - Key fields: [list main fields]
   - Relationships: [foreign keys and references]

### Existing Tables to Reuse
[List existing tables that will be used without modification]

1. **[table_name]**: [How it will be used]
   - Relevant fields: [fields being used]
   - No modifications needed

### Existing Tables to Modify
[List existing tables that need alterations]

1. **[table_name]**: [What modifications are needed]
   - New fields to add: [list fields]
   - Constraints to add: [list constraints]

### Table Standards
**Note**: All tables must follow these standards:
- Use `status_id` instead of `is_active` (references `status` table)
- Include audit fields: `created_by`, `created_at`, `updated_by`, `updated_at`
- Use singular nouns for table names
- Use `map_` prefix for junction/mapping tables

### Example Structure for New Tables
```sql
CREATE TABLE [table_name] (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  -- domain fields
  status_id BIGINT UNSIGNED NOT NULL,
  created_by BIGINT UNSIGNED NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by BIGINT UNSIGNED,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (status_id) REFERENCES status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  -- indexes
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Scalability Considerations
[Analyze how this schema will perform at scale]

#### Expected Data Volume
- Year 1: [estimated records]
- Year 3: [projected growth]
- Year 5: [scale projections]

#### Query Patterns
- High-frequency queries: [list common queries]
- Reporting queries: [analytical needs]
- Real-time requirements: [performance SLAs]

#### JSON vs Normalized Analysis
- Fields using JSON: [justify each]
- Why not normalized: [specific reasons]
- Migration plan if needed: [future path]

## Maintenance Scenarios
[Examples of common maintenance tasks and their implementation]

### Adding New Elements
- How to add new [entities/features]
- Required database changes
- Configuration updates needed

### Modifying Existing Elements
- How to update [entities/features]
- Impact on existing data
- Migration considerations

### Removing/Retiring Elements
- Safe removal process
- Data archival approach
- Backward compatibility handling

### Schema Evolution
- Migrating from JSON to normalized structure
- Adding indexes for performance optimization
- Handling breaking changes
- Zero-downtime migration strategies

## Business Summary for Stakeholders
### What We're Building
[Plain English explanation that a non-technical person can understand]

### Why It's Needed
[Business value and problem being solved]

### Expected Outcomes
[What success looks like from business perspective]

## Technical Summary for Developers
### Key Technical Decisions
- **Architecture Pattern**: [e.g., microservice, API-driven, event-based]
- **Technology Choices**: [frameworks, libraries, services]
- **Integration Approach**: [APIs, events, direct DB, etc.]

### Implementation Guidelines
- Critical code patterns to follow
- Performance considerations
- Security requirements
- Error handling approach

## Validation Criteria
### Pre-Implementation Checkpoints
- [ ] Business requirements clearly understood
- [ ] Technical approach aligns with architecture standards
- [ ] Database schema follows naming conventions
- [ ] Pattern reuse maximized (85%+ target)
- [ ] Security considerations addressed
- [ ] Performance impact assessed
- [ ] Analyzed expected data growth (records/year)
- [ ] Identified high-frequency query patterns
- [ ] Considered reporting requirements
- [ ] Evaluated JSON vs normalized for each entity
- [ ] Planned for future migration paths
- [ ] Reviewed scalability at 5 dimensions (entity count, records per entity, complexity, query volume, reporting needs)

### Database Verification Checklist
- [ ] Verified which tables already exist in database
- [ ] Confirmed existing table structures match requirements
- [ ] Identified tables that need modification vs creation
- [ ] Checked for naming conflicts with existing tables
- [ ] Validated foreign key references to existing tables
- [ ] Ensured no duplicate functionality being created

### Success Metrics
- [ ] [Specific measurable outcome 1]
- [ ] [Specific measurable outcome 2]
- [ ] [Performance target if applicable]
- [ ] [Quality threshold if applicable]

## Approval Section
**Status**: PENDING APPROVAL
**Reviewer Comments**: [Space for feedback]
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER