# GR-19 Table Relationships Requirements - Requirement Comparison Outline

## Overview
This document outlines the proposed changes to GR-19 (Table Relationships Requirements) to reflect the actual relationship patterns in the claude_db database.

## Current GR-19 Structure vs Proposed Updates

### 1. Current Content Focus
**Current GR-19**:
- Only 3 items focusing on action tracking pattern
- action_type table
- action table  
- map_ENTITY_action pattern
- Limited to audit/action tracking relationships

**Proposed GR-19**:
- Comprehensive coverage of all 22 mapping tables
- Multiple relationship categories (Policy, Quote, Program, etc.)
- Real-world business relationships
- Complete relationship documentation

### 2. Relationship Patterns

#### Current Pattern:
```
1. action_type
2. action (references action_type_id)
3. map_ENTITY_action (generic pattern)
```

#### Proposed Patterns:
```
1. Entity-to-Entity Mappings (map_ prefix standard)
2. Policy Relationships (5 tables)
3. Quote Relationships (3 tables)
4. Program Relationships (6 tables)
5. Producer Relationships (2 tables)
6. Security Relationships (2 tables)
7. Other Relationships (4 tables)
```

### 3. Detailed Relationship Documentation

**Current**: Generic description of action tracking
**Proposed**: Specific documentation for each mapping table including:
- Table name and purpose
- Foreign key relationships
- Additional fields (e.g., is_primary_driver, commission_rate)
- Business rules and constraints

### 4. New Sections to Add

#### Relationship Categories:
1. **Policy Relationships**
   - map_policy_driver
   - map_policy_vehicle
   - map_policy_coverage
   - map_policy_document
   - map_policy_installment

2. **Quote Relationships**
   - map_quote_driver
   - map_quote_vehicle
   - map_quote_coverage

3. **Program Relationships**
   - map_program_producer
   - map_program_coverage
   - map_program_deductible
   - map_program_limit
   - map_program_underwriting_question
   - map_program_news

4. **Producer Relationships**
   - map_producer_policy_commission
   - map_producer_suspense

5. **Security Relationships**
   - map_user_role
   - map_role_permission

6. **Other Relationships**
   - map_driver_violation
   - map_entity_document
   - map_integration_configuration
   - map_resource_group

#### Relationship Rules:
- Referential integrity requirements
- Audit field standards
- Performance indexing guidelines
- Data validation rules

## Comparison Table

| Aspect | Current GR-19 | Proposed GR-19 |
|--------|---------------|----------------|
| Scope | Action tracking only | All business relationships |
| Tables Covered | 3 conceptual | 22 actual tables |
| Pattern Type | Generic template | Specific implementations |
| Business Context | Limited | Comprehensive |
| Examples | Theoretical | Real database tables |

## Key Improvements

1. **Completeness**: Documents all actual relationships vs. theoretical subset
2. **Accuracy**: Based on real database analysis
3. **Practicality**: Developers can reference actual table structures
4. **Business Alignment**: Shows how entities relate in the business domain

## Removed Content

**Action Tracking Pattern**: 
- The action/action_type/map_ENTITY_action pattern doesn't exist in the actual database
- This pattern is replaced with real mapping tables that serve actual business needs

## Implementation Notes

### For Each Mapping Table:
1. Document purpose and business use case
2. List all foreign keys with references
3. Identify any additional fields beyond FKs
4. Note any special constraints or rules
5. Include standard audit fields

### Standard Structure Example:
```markdown
#### map_policy_driver
Links policies to insured drivers
- policy_id → policy.id
- driver_id → driver.id
- is_primary_driver (BOOLEAN)
- created_by, updated_by, created_at, updated_at
```

## Benefits of Updates

1. **Real-World Alignment**: Documents actual database relationships
2. **Developer Reference**: Practical guide for understanding data model
3. **Complete Coverage**: No missing relationships
4. **Business Context**: Clear purpose for each relationship

## Next Steps

1. Review this comparison with stakeholders
2. Upon approval, update GR-19 with actual relationships
3. Consider adding relationship diagrams for complex areas
4. Ensure consistency with other Global Requirements