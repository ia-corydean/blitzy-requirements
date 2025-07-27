# GR-02 Database Migrations - Requirement Comparison Outline

## Overview
This document outlines the proposed changes to GR-02 (Database Migrations) to align with the current single-tenant database structure in claude_db.

## Current GR-02 Structure vs Proposed Updates

### 1. Multi-Tenant Migration Strategy Section
**Current**: 
- Extensive multi-tenant architecture with namespace isolation
- Tenant management migrations
- Row-level security policies
- TenantAwareMigration base class

**Proposed**:
- Remove entire multi-tenant strategy section
- Replace with single-database migration approach
- Focus on standard Laravel migrations without tenant context

### 2. Technology Stack Section
**Current**:
- Laravel 12.x+ with modern migration features
- PHP 8.4+ for enhanced database connectivity
- Multi-tenant specific features

**Proposed**:
- Generic Laravel migration approach (version agnostic)
- Standard PHP requirements
- MariaDB-specific optimizations

### 3. Core Migration Framework
**Current**:
```php
abstract class TenantAwareMigration extends Migration {
    // Complex tenant-aware logic
}
```

**Proposed**:
```php
abstract class BaseMigration extends Migration {
    protected function addAuditFields(Blueprint $table): void
    protected function addStatusField(Blueprint $table): void
}
```

### 4. Example Migrations

#### Current Examples:
- CreateTenantsTable
- CreateUsersTable (with tenant_id)
- CreatePoliciesTable (with tenant isolation)
- CreateClaimsTable (with tenant constraints)

#### Proposed Examples:
- CreateEntityTypeTable
- CreateEntityTable
- CreatePolicyTable (without tenant_id)
- CreateDriverTable
- Standard single-database patterns

### 5. Advanced Features

**Remove**:
- Data Encryption Migration (EncryptedFieldsMigration)
- Multi-Environment Migration Management
- TenantMigrationManager
- Production migration with tenant considerations

**Keep/Modify**:
- Audit Trail Migration (simplified)
- Migration Testing Framework (without tenant testing)
- Environment-specific strategies (simplified)
- Migration documentation standards

### 6. New Sections to Add

**Database Patterns**:
- Type table pattern (entity_type, driver_type, etc.)
- Map table pattern for relationships
- Standard audit field implementation
- Status management pattern

**Migration Best Practices**:
- Single database considerations
- Performance optimizations for MariaDB
- Index strategies
- Foreign key management

## Key Benefits of Updates

1. **Accuracy**: Reflects actual single-tenant database
2. **Simplicity**: Removes unnecessary complexity
3. **Practical Examples**: Uses real table structures from claude_db
4. **Maintainability**: Easier to understand and implement

## Migration Impact

### Code Changes Required:
- Update migration base classes
- Remove tenant-specific logic
- Simplify migration commands
- Update testing frameworks

### Documentation Updates:
- Remove multi-tenant references
- Update examples to match actual tables
- Simplify architecture diagrams
- Update best practices

## Comparison Summary

| Aspect | Current GR-02 | Proposed GR-02 |
|--------|---------------|----------------|
| Architecture | Multi-tenant | Single-tenant |
| Complexity | High | Low |
| Base Classes | TenantAwareMigration | BaseMigration |
| Examples | Tenant-aware tables | Standard tables |
| Security | Row-level tenant isolation | Standard access control |
| Testing | Complex tenant testing | Simple migration testing |

## Next Steps

1. Review this comparison with stakeholders
2. Upon approval, create updated GR-02 document
3. Ensure consistency with other Global Requirements
4. Update any dependent documentation