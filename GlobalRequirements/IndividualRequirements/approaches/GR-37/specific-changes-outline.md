# GR-37 Specific Changes Outline

## Overview
This document outlines the specific changes needed in other Global Requirements files due to the update of GR-37 to use the unified user/user_type pattern instead of multiple user fields (created_by_user_id, locked_by_user_id, etc.).

## Key Change Summary
- Replace multiple user ID fields with single `user_id` field
- Use `user_type` table to differentiate user roles/contexts
- Maintain audit trail through action tables
- Simplify foreign key relationships

## Changes Required by File

### 1. GR-02: Database Migrations
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/02-database-migrations-updated.md`

**Changes Needed**:
- Update `BaseMigration` class to use single `created_by` and `updated_by` fields (already done)
- Remove examples showing multiple user fields
- Update migration examples to show user_type pattern

**Specific Sections**:
- Base Migration Class: Already uses correct pattern
- Migration Examples: Ensure consistency

### 2. GR-03: Models Relationships
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/03-models-relationships.md`

**Changes Needed**:
- Update model relationships to use single user relation
- Add user_type relationship pattern
- Remove multiple user field relationships

**Specific Sections**:
- User Relationships: Change from multiple relations to single user relation with type
- Audit Trail Pattern: Update to use action tables with user_id

### 3. GR-19: Table Relationships Requirements
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/19-table-relationships-requirements.md`

**Changes Needed**:
- Update relationship diagrams to show user → user_type pattern
- Remove multiple user foreign keys
- Show action table relationships for tracking different user actions

**Specific Sections**:
- Foreign Key Standards: Single user_id with user_type context
- Audit Relationships: Through action tables

### 4. GR-20: Application Business Logic
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/20-application-business-logic.md`

**Changes Needed**:
- Update business logic to check user_type for permissions
- Remove logic for multiple user fields
- Use action tables for tracking who did what

**Specific Sections**:
- User Context: Get from user + user_type
- Action Tracking: Use action tables instead of multiple fields

### 5. GR-36: Authentication User Groups Permissions
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/36-authentication-user-groups-permissions.md`

**Changes Needed**:
- Align permission checks with user_type pattern
- Update examples to show user_type-based authorization
- Remove references to role-specific user fields

**Specific Sections**:
- Permission Model: Base on user_type
- Authorization Examples: Use user_type for context

### 6. GR-40: Database Seeding Requirements
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/40-database-seeding-requirements.md`

**Changes Needed**:
- Update seeders to create users with appropriate user_types
- Remove seeding of multiple user fields
- Add user_type seeding examples

**Specific Sections**:
- User Seeding: Include user_type assignment
- Test Data: Show variety of user_types

### 7. GR-41: Table Schema Requirements
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/41-table-schema-requirements.md`

**Changes Needed**:
- Update standard audit fields to single user pattern
- Remove multiple user field requirements
- Add user_type relationship requirement

**Specific Sections**:
- Audit Fields: created_by, updated_by only
- User Tracking: Through action tables
- Foreign Keys: Single user_id pattern

### 8. GR-18: Workflow Requirements
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/18-workflow-requirements.md`

**Changes Needed**:
- Update workflow tracking to use action tables
- Remove workflow-specific user fields
- Show user_type context in workflows

**Specific Sections**:
- Workflow State: Track via actions
- User Assignment: Single user_id with type context

### 9. GR-13: Error Handling Logging
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/13-error-handling-logging.md`

**Changes Needed**:
- Update logging to capture user_id and user_type
- Remove references to multiple user fields
- Show action-based logging pattern

**Specific Sections**:
- Log Context: Include user_type
- Audit Logging: Via action tables

### 10. GR-51: Compliance Audit Architecture
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/51-compliance-audit-architecture.md`

**Changes Needed**:
- Update audit trail to use action tables
- Remove multiple user field auditing
- Show user_type in audit context

**Specific Sections**:
- Audit Trail: Action-based tracking
- User Context: user_id + user_type

## Implementation Guidelines

### Priority Order
1. **High Priority**: GR-41, GR-19 (schema standards)
2. **Medium Priority**: GR-03, GR-36 (models and permissions)
3. **Low Priority**: Other files (logging, workflows, etc.)

### Minimal Change Principles
1. Only update user field references
2. Preserve all other functionality
3. Maintain existing patterns where possible
4. Keep action tracking comprehensive

### Database Pattern
```sql
-- Instead of:
locked_by_user_id INT,
approved_by_user_id INT,
reviewed_by_user_id INT,

-- Use:
user_id INT,
-- with user_type determining context
-- and action tables for tracking
```

### Action Table Pattern
```sql
-- Track different user actions
CREATE TABLE entity_action (
    id INT PRIMARY KEY,
    entity_id INT,
    action_type_id INT,
    user_id INT,
    action_data JSON,
    created_at TIMESTAMP
);
```

### Validation Checklist
- [ ] No multiple user fields remain
- [ ] User_type pattern implemented
- [ ] Action tables referenced for tracking
- [ ] Foreign keys simplified
- [ ] Audit trail maintained
- [ ] Documentation updated

## Risk Mitigation

### Potential Issues
1. **Loss of Context**: Need to ensure user_type provides enough context
2. **Action Tracking**: Must implement comprehensive action tables
3. **Migration Complexity**: Existing data with multiple user fields

### Mitigation Strategies
1. Comprehensive user_type definitions
2. Rich action_type taxonomy
3. Clear migration path for existing data
4. Thorough testing of audit trails

## Benefits of This Approach

1. **Simplified Schema**: One user field instead of many
2. **Flexible Tracking**: Action tables can capture any user action
3. **Better Normalization**: Follows database best practices
4. **Easier Maintenance**: Consistent pattern across all entities
5. **Scalable**: Can add new action types without schema changes

## Summary

The transition to a unified user/user_type pattern requires updates across 10 Global Requirements files. The changes focus on:

1. Removing multiple user ID fields
2. Implementing user_type for role context
3. Using action tables for comprehensive tracking
4. Simplifying foreign key relationships

This approach provides a cleaner, more maintainable solution while preserving all necessary audit and tracking capabilities.