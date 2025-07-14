# [Requirement ID] - [Requirement Name]

## Pre-Analysis Checklist

### Initial Review
- [ ] Read base requirement document completely
- [ ] Identify all UI elements and data fields mentioned
- [ ] Note workflow states and transitions described
- [ ] List relationships to existing entities

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

---

## Entity Analysis

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|--------|
| [entity] | Core/Reference/Map/Supporting | New/Existing/Modified | [usage notes] |

### New Tables Required
- **[table_name]**: [purpose and usage]
- **[reference_table]**: [lookup/type data]

### Modifications to Existing Tables
- **[table_name]**: [changes needed and impact]

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

## Quality Checklist

### Pre-Implementation
- [ ] All UI fields mapped to database columns
- [ ] Existing entities reused where possible
- [ ] Reference tables created for all ENUMs
- [ ] Naming conventions followed consistently
- [ ] Relationships properly defined with foreign keys

### Post-Implementation
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
- [ ] Documentation updated