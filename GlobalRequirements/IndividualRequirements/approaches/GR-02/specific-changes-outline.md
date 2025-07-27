# GR-02 Specific Changes Outline

## Overview
This document outlines the specific changes needed in other Global Requirements files due to the update of GR-02 from multi-tenant to single-tenant architecture. The goal is to keep changes minimal while ensuring consistency.

## Changes Required by File

### 1. GR-03: Models Relationships
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/03-models-relationships.md`

**Changes Needed**:
- Remove any references to `tenant_id` in model relationships
- Remove tenant-based model scoping examples
- Update base model class from `TenantAwareModel` to `BaseModel`
- Remove tenant isolation logic from relationship definitions

**Specific Sections**:
- Base Model Definition: Change parent class
- Relationship Examples: Remove tenant_id from foreign key definitions
- Query Scoping: Remove tenant-based query examples

### 2. GR-19: Table Relationships Requirements
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/19-table-relationships-requirements.md`

**Changes Needed**:
- Remove `tenant_id` from all relationship diagrams
- Remove tenant-based relationship constraints
- Update foreign key examples to exclude tenant_id
- Remove multi-tenant isolation requirements

**Specific Sections**:
- Foreign Key Standards: Remove tenant_id requirements
- Relationship Patterns: Update examples without tenant context
- Data Integrity Rules: Remove tenant isolation rules

### 3. GR-36: Authentication User Groups Permissions
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/36-authentication-user-groups-permissions.md`

**Changes Needed**:
- Remove tenant-based permission scoping
- Remove tenant switching functionality
- Update user authentication to single-tenant model
- Remove tenant_id from user and role tables

**Specific Sections**:
- User Model: Remove tenant_id field
- Permission Model: Remove tenant-based permissions
- Authentication Flow: Remove tenant selection/switching

### 4. GR-40: Database Seeding Requirements
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/40-database-seeding-requirements.md`

**Changes Needed**:
- Remove tenant-specific seeding logic
- Remove tenant creation seeders
- Update seeder base class from `TenantAwareSeeder` to `BaseSeeder`
- Remove multi-tenant test data generation

**Specific Sections**:
- Seeder Classes: Change parent class
- Seeding Strategy: Remove tenant isolation
- Test Data: Remove multi-tenant scenarios

### 5. GR-41: Table Schema Requirements
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/41-table-schema-requirements.md`

**Changes Needed**:
- Remove `tenant_id` from standard table fields
- Remove tenant_id indexing requirements
- Update schema examples without tenant_id
- Remove tenant-based partitioning strategies

**Specific Sections**:
- Required Fields: Remove tenant_id from list
- Index Standards: Remove tenant_id composite indexes
- Schema Examples: Update all examples

### 6. GR-20: Application Business Logic
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/20-application-business-logic.md`

**Changes Needed**:
- Remove tenant context from business logic layer
- Remove tenant-based data isolation logic
- Update service layer examples
- Remove tenant switching logic

**Specific Sections**:
- Service Layer: Remove tenant context injection
- Business Rules: Remove tenant-specific logic
- Data Access: Remove tenant filtering

### 7. GR-01: Identity Access Management
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/01-identity-access-management.md`

**Changes Needed**:
- Remove tenant-based access control
- Update IAM to single-tenant model
- Remove tenant admin roles
- Simplify permission structure

**Specific Sections**:
- Access Control: Remove tenant isolation
- Role Definitions: Remove tenant admin roles
- Permission Matrix: Simplify without tenant context

## Implementation Guidelines

### Priority Order
1. **High Priority**: GR-41, GR-03, GR-19 (core database structure)
2. **Medium Priority**: GR-36, GR-01 (authentication/authorization)
3. **Low Priority**: GR-20, GR-40 (application logic and seeding)

### Minimal Change Principles
1. Only remove tenant-specific code/references
2. Keep all other functionality intact
3. Preserve existing patterns where possible
4. Maintain backward compatibility for non-tenant features

### Search and Replace Patterns
```bash
# Common patterns to find and update:
- "tenant_id" → remove field
- "TenantAwareMigration" → "BaseMigration"
- "TenantAwareModel" → "BaseModel"
- "TenantAwareSeeder" → "BaseSeeder"
- "tenant-based" → "single-database"
- "multi-tenant" → "single-tenant"
```

### Validation Checklist
- [ ] No remaining references to tenant_id
- [ ] All base classes updated
- [ ] Foreign key constraints updated
- [ ] Index definitions updated
- [ ] Permission models simplified
- [ ] Seeding logic simplified
- [ ] Documentation updated

## Risk Mitigation

### Potential Issues
1. **Hidden Dependencies**: Some files may have implicit tenant assumptions
2. **Test Fixtures**: Test data may assume multi-tenant setup
3. **Configuration**: Environment configs may reference tenant settings

### Mitigation Strategies
1. Global search for "tenant" across all requirements
2. Review all database migration examples
3. Update test scenarios to single-tenant
4. Remove tenant-related environment variables

## Summary

The transition from multi-tenant to single-tenant architecture requires careful updates across 7 key Global Requirements files. The changes are primarily focused on:

1. Removing tenant_id fields from all database schemas
2. Updating base classes to non-tenant-aware versions
3. Simplifying authentication and authorization
4. Removing tenant isolation logic

By following this outline and keeping changes minimal, we can successfully update the architecture while maintaining system integrity and avoiding unnecessary modifications.