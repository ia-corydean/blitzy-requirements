# [Requirement ID] - [Requirement Name] - Complete Requirement

---

## **A) WHY – Vision and Purpose**

[Describe the business context and rationale for this requirement. What problem does it solve? What value does it deliver? This should be written in clear business language that stakeholders can understand.]

---

## **B) WHAT – Core Requirements**

[Provide a high-level description of what needs to be built, followed by detailed functional requirements organized by major feature areas.]

### **1. [Major Feature Area]**

- [Specific requirement or capability]
- [User interaction or workflow]
- [Data elements involved]
- [Business rules or constraints]

### **2. [Another Feature Area]**

- [Requirements specific to this area]
- [Integration points]
- [Validation rules]

### **3. Business Rules & Validation**

- [List specific business rules that must be enforced]
- [Validation requirements]
- [Error handling requirements]

### **4. Save & Navigation**

- [Workflow navigation requirements]
- [Save/persistence requirements]
- [Progress tracking needs]

---

## Entity Analysis

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|-------|
| [entity] | Core/Reference/Map/Supporting | New/Existing/Modified | [usage notes] |

### New Tables Required
- **[table_name]**: [purpose and usage description]

### Modifications to Existing Tables
- **[table_name]**: [specific changes needed and why]

### Relationships Identified
- [entity_a] → [relationship type] → [entity_b]

---

## Field Mappings (Section C)

### Backend Mappings

#### [UI Section or Feature Area]

##### [Field or Feature Name]
- **Backend Mapping**: 
  ```
  get [entity].id from [table]
  -> get [related_entity] by [entity].[foreign_key]
  -> return [fields], [transformations]
  ```

### Implementation Architecture

[Describe the technical implementation approach, including patterns, services, and architectural decisions that guide development.]

### Integration Specifications

[Detail any external service integrations, APIs, or third-party systems involved.]

---

## **D) User Experience (UX) & Flows** (if applicable)

### **1. [Primary User Flow]**

1. [Step-by-step user journey]
2. [Key interaction points]
3. [Decision points or branches]

### **2. [Secondary Flow or Modal]**

1. [Alternative paths or edge cases]
2. [Error states and recovery]

### **3. [UI Presentation Guidelines]**

- [Layout considerations]
- [Responsive design requirements]
- [Accessibility requirements]

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

### New Reference Tables

#### [reference_table_name]
```sql
CREATE TABLE [reference_table_name] (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(50) UNIQUE NOT NULL,
  name VARCHAR(100) NOT NULL,
  description TEXT NULL,
  status_id BIGINT UNSIGNED NOT NULL,
  
  -- Audit fields
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Foreign key constraints
  FOREIGN KEY (status_id) REFERENCES status(id),
  
  -- Indexes
  INDEX idx_code (code),
  INDEX idx_status (status_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Modified Tables

#### ALTER TABLE [existing_table]
```sql
-- Add new columns with business justification
ALTER TABLE [existing_table] 
ADD COLUMN [new_column] [TYPE] [constraints] COMMENT '[business reason]';

-- Add foreign key constraints
ALTER TABLE [existing_table]
ADD CONSTRAINT fk_[table]_[reference] 
FOREIGN KEY ([column]_id) REFERENCES [reference_table](id);

-- Add indexes for performance
ALTER TABLE [existing_table]
ADD INDEX idx_[meaningful_name] ([column]);
```

---

## Implementation Notes

### Dependencies
- [List any dependencies on other requirements or systems]
- [Note integration points with existing functionality]
- [Identify prerequisite data or configurations]

### Migration Considerations
- [Data migration requirements]
- [Backwards compatibility concerns]
- [Rollback strategies]

### Performance Considerations
- [Expected data volumes and growth]
- [Query optimization strategies]
- [Caching requirements]
- [Index strategy for common queries]

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

### Global Requirements Compliance
- [ ] **GR-[number]**: [Global requirement name and how it's applied]
- [ ] **GR-[number]**: [Another relevant global requirement]