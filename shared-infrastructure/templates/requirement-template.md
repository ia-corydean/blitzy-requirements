# [Requirement ID] - [Requirement Name]

## Pre-Analysis Checklist

### Initial Review
- [ ] Read base requirement document completely
- [ ] Identify all UI elements and data fields mentioned
- [ ] Note workflow states and transitions described
- [ ] List relationships to existing entities

### Database Schema Review (MANDATORY FIRST STEP)
- [ ] **Review existing database schema FIRST** - Check what tables/columns already exist
- [ ] **Document available existing tables** - List existing tables that could be reused
- [ ] **Identify existing columns** - Map existing columns to UI requirements before adding new ones
- [ ] **Assess reuse opportunities** - Identify which existing structures can support new UI elements

### Global Requirements Alignment
- [ ] Review applicable global requirements
- [ ] Note which GRs apply to this requirement
- [ ] Ensure patterns align with global standards
- [ ] Cross-reference with domain standards

### Cross-Reference Check
- [ ] Review entity catalog for reusable entities
- [ ] Check architectural decisions for relevant patterns
- [ ] Search blitzy-requirements for similar functionality
- [ ] Review related requirements for shared entities

### Compliance Verification
- [ ] Verify alignment with CLAUDE.md standards
- [ ] Check naming convention compliance
- [ ] Validate reference table approach for ENUMs
- [ ] Ensure status_id usage instead of is_active
- [ ] **Validate every new column maps to specific UI element** - No speculative columns
- [ ] **Justify new additions against existing schema** - Document why existing schema can't support the UI

---

## Entity Analysis

### Existing Schema Analysis (Document First)
| Existing Table | Available Columns | UI Elements Supported | Reusable For |
|----------------|-------------------|-----------------------|--------------|
| [table_name] | [list existing columns] | [which UI elements these support] | [how they can be reused] |

### Existing Column Mapping to UI Elements
| UI Element | Existing Table.Column | Status |
|------------|----------------------|--------|
| [UI field name] | [table.column] | Available/Needs Enhancement |

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|--------|
| [entity] | Core/Reference/Map/Supporting | New/Existing/Modified | [usage notes] |

### Gap Analysis - New Tables Required (Only if existing schema cannot support UI)
- **[table_name]**: [purpose and usage] - **Justification**: [why existing tables cannot support this UI requirement]

### Gap Analysis - Modifications to Existing Tables (Only if needed for UI)
- **[table_name]**: [specific changes needed] - **UI Justification**: [which UI elements require these specific columns]

### Relationships Identified
- [entity_a] → [relationship] → [entity_b]

---

## Field Mappings (Section C)

### Backend Mappings

#### [UI Section Name]

##### [Field Name]
- **Backend Mapping**: 
  ```
  get [entity].id from [table]
  -> get [related_entity] by [entity].[foreign_key]
  -> return [fields], [transformations]
  ```

### Implementation Architecture
[Details about how the requirement is implemented, including patterns, services, and architectural decisions]

### Integration Specifications (if applicable)
[External service integrations, communication patterns, etc.]

---

## API Specifications

### Endpoints Required
```http
GET    /api/v1/[resource]              # List with pagination
GET    /api/v1/[resource]/{id}         # Single record
POST   /api/v1/[resource]              # Create
PUT    /api/v1/[resource]/{id}         # Update
DELETE /api/v1/[resource]/{id}         # Delete
```

### Real-time Updates
```javascript
// WebSocket channels
private-[entity].{id}                  # Specific entity updates
private-tenant.{tenant_id}.[entities]  # All entities for tenant
```

---

## Database Schema (Section E)

### New Core Tables

#### [table_name]
```sql
CREATE TABLE [table_name] (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  
  -- Business columns
  [column_name] [TYPE] [constraints],
  
  -- Foreign keys
  [related_table]_id BIGINT UNSIGNED NOT NULL,
  status_id BIGINT UNSIGNED NOT NULL,
  
  -- Audit fields
  created_by BIGINT UNSIGNED NOT NULL,
  updated_by BIGINT UNSIGNED NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Foreign key constraints
  FOREIGN KEY ([related_table]_id) REFERENCES [related_table](id),
  FOREIGN KEY (status_id) REFERENCES status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  
  -- Indexes
  INDEX idx_[related_table] ([related_table]_id),
  INDEX idx_status (status_id),
  INDEX idx_[business_field] ([business_field])
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## Implementation Notes

### Dependencies
- [List any dependencies on other requirements]
- [Note integration points with existing systems]

### Migration Considerations
- [Data migration needs]
- [Backwards compatibility concerns]

### Performance Considerations
- [Query optimization notes]
- [Caching strategy]
- [Index strategy]

---

## API and Integration Considerations

### External API Dependencies
- [List any third-party APIs required]
- [Authentication/authorization requirements]
- [Rate limiting and error handling]

### Internal Service Integrations
- [Services that need to be called]
- [Data synchronization requirements]
- [Circuit breaker/retry patterns needed]

### Integration Patterns
- [Real-time vs batch processing]
- [Event-driven vs direct API calls]
- [Data consistency requirements]

### Security Considerations
- [API authentication methods]
- [Data encryption requirements]
- [PII handling and masking]

---

## Project Manager Summary

### What We're Building
[Plain English description of the deliverable - what the user will see and be able to do]

### Key Deliverables
- [Frontend component/pages to be built]
- [Backend services/APIs to be developed]
- [Database changes required]
- [Integration work needed]

### Resource Requirements
- **Frontend**: [Estimated effort and complexity]
- **Backend**: [Estimated effort and complexity]
- **Database**: [Schema changes and migration effort]
- **Integration**: [External service setup and testing]

### Dependencies and Risks
- **Dependencies**: [Other teams, systems, or requirements needed first]
- **Technical Risks**: [Complexity, unknowns, or integration challenges]
- **Timeline Risks**: [External dependencies, resource availability]

### Business Value
- [Primary business outcomes delivered]
- [User experience improvements]
- [Operational efficiency gains]

---

## Technical Manager Summary

### Architecture Decisions
- **Design Patterns**: [Architectural patterns being used]
- **Technology Stack**: [Key technologies and frameworks]
- **Integration Approach**: [How components communicate]

### Database Impact
- **Schema Changes**: [New tables, columns, relationships]
- **Performance Impact**: [Query complexity, indexing needs]
- **Migration Requirements**: [Data migration, downtime considerations]

### Performance Considerations
- **Expected Load**: [User volume, data volume, query frequency]
- **Optimization Strategy**: [Caching, indexing, query optimization]
- **Monitoring Needs**: [Performance metrics to track]

### Security and Compliance
- **Security Measures**: [Authentication, authorization, data protection]
- **Compliance Requirements**: [Regulatory or policy requirements]
- **Audit Considerations**: [Logging, tracking, data retention]

### Deployment and Operations
- **Deployment Strategy**: [How changes will be rolled out]
- **Rollback Plan**: [How to revert if issues arise]
- **Monitoring and Alerting**: [What metrics to watch]
- **Support Considerations**: [Documentation, training, maintenance]

---

## Quality Checklist

### Pre-Implementation
- [ ] **Existing database schema reviewed first** - Database-first approach followed
- [ ] **All existing reusable tables and columns identified** - Documented in Existing Schema Analysis
- [ ] **Every new column maps to specific UI element** - No orphaned or speculative columns
- [ ] **New additions justified against existing schema** - Documented why existing cannot support UI
- [ ] All UI fields mapped to database columns
- [ ] Existing entities reused where possible
- [ ] Reference tables created for all ENUMs
- [ ] Naming conventions followed consistently
- [ ] Relationships properly defined with foreign keys

### Post-Implementation
- [ ] **Verified existing schema was maximally reused** - No duplicate functionality created
- [ ] **Confirmed all new columns serve documented UI requirements** - No convenience additions
- [ ] **Validated no speculative columns were added** - All columns trace to UI elements
- [ ] All foreign keys have proper constraints
- [ ] Appropriate indexes for expected query patterns
- [ ] Audit fields included on all tables
- [ ] Status management consistent across tables
- [ ] Entity catalog updated with new entities
- [ ] Architectural decisions documented if new patterns

### Final Validation
- [ ] Backend mappings complete and accurate
- [ ] Database schema follows all standards
- [ ] No redundant tables or columns created
- [ ] Performance considerations addressed
- [ ] **Database-first approach validation completed** - Existing schema maximally reused
- [ ] Documentation updated