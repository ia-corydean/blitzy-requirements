# GR-02 Database Migrations - Database Alignment Approach

## Overview
This approach document outlines how to update GR-02 (Database Migrations) to align with the current database structure in the Docker container (claude_db).

## Current State Analysis

### GR-02 Current Focus
- Multi-tenant architecture with tenant isolation
- Laravel 12.x migration framework
- Row-level security policies
- Encrypted fields for sensitive data
- Audit trail capabilities

### Actual Database State (claude_db)
Based on the Docker container analysis:
- **No multi-tenant structure**: No `tenant` table exists
- **Single-tenant database**: All tables are in a single database without tenant isolation
- **Simplified user table**: Basic user management without multi-tenant fields
- **Core tables present**: 167 tables including entity, policy, quote, producer, driver, vehicle, etc.
- **Type-based architecture**: Each main entity has corresponding `_type` tables
- **Standard audit fields**: All tables include created_by, updated_by, created_at, updated_at

## Key Differences to Address

### 1. Remove Multi-Tenant Architecture
**Current GR-02**: Focuses heavily on multi-tenant isolation
**Actual Database**: Single-tenant architecture
**Action**: Remove all multi-tenant references and update to single-tenant approach

### 2. Update Technology Stack
**Current GR-02**: Laravel 12.x, PHP 8.4+
**Actual Database**: MariaDB with standard structure
**Action**: Focus on database-agnostic migration principles

### 3. Simplify Migration Base Classes
**Current GR-02**: Complex TenantAwareMigration base class
**Actual Database**: Standard migrations without tenant context
**Action**: Provide simplified migration base class

### 4. Align Table Structures
**Current GR-02**: Different table structures with tenant_id
**Actual Database**: Tables use status_id and type_id patterns
**Action**: Update example migrations to match actual schema

## Proposed Updates

### 1. Migration Framework Section
Replace multi-tenant framework with:
```
## Core Migration Framework

### Database Structure Overview
- **Primary Database**: MariaDB for transactional data
- **Single Database**: claude_db containing all application tables
- **Type-Based Architecture**: Each entity has corresponding _type tables
- **Standard Audit Fields**: All tables include audit tracking

### Base Migration Class
```php
abstract class BaseMigration extends Migration
{
    /**
     * Add standard audit fields to any table
     */
    protected function addAuditFields(Blueprint $table): void
    {
        $table->integer('created_by')->nullable();
        $table->integer('updated_by')->nullable();
        $table->timestamp('created_at')->nullable()->default(DB::raw('CURRENT_TIMESTAMP'));
        $table->timestamp('updated_at')->nullable()->default(DB::raw('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'));
        
        // Add indexes
        $table->index('created_at');
    }
    
    /**
     * Add status field with foreign key
     */
    protected function addStatusField(Blueprint $table): void
    {
        $table->integer('status_id')->nullable();
        $table->foreign('status_id')->references('id')->on('status');
        $table->index('status_id');
    }
}
```

### 2. Update Example Migrations
Replace existing examples with actual database patterns:

```php
// Create Entity Type Table
class CreateEntityTypeTable extends Migration
{
    public function up()
    {
        Schema::create('entity_type', function (Blueprint $table) {
            $table->integer('id', true);
            $table->string('code', 50)->unique();
            $table->string('name', 100);
            $table->text('description')->nullable();
            $table->boolean('is_default')->default(false);
            $table->integer('status_id')->nullable();
            $table->integer('created_by')->nullable();
            $table->integer('updated_by')->nullable();
            $table->timestamp('created_at')->nullable()->default(DB::raw('CURRENT_TIMESTAMP'));
            $table->timestamp('updated_at')->nullable()->default(DB::raw('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'));
            
            // Indexes
            $table->index('code');
            $table->index('status_id');
            
            // Foreign keys
            $table->foreign('status_id')->references('id')->on('status');
        });
    }
}

// Create Entity Table
class CreateEntityTable extends Migration
{
    public function up()
    {
        Schema::create('entity', function (Blueprint $table) {
            $table->integer('id', true);
            $table->integer('entity_type_id');
            $table->integer('status_id')->nullable();
            $table->integer('created_by')->nullable();
            $table->integer('updated_by')->nullable();
            $table->timestamp('created_at')->nullable()->default(DB::raw('CURRENT_TIMESTAMP'));
            $table->timestamp('updated_at')->nullable()->default(DB::raw('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'));
            
            // Indexes
            $table->index('entity_type_id');
            $table->index('status_id');
            $table->index('created_at');
            
            // Foreign keys
            $table->foreign('entity_type_id')->references('id')->on('entity_type');
            $table->foreign('status_id')->references('id')->on('status');
        });
    }
}
```

### 3. Remove Tenant-Specific Sections
Remove or replace:
- Multi-Tenant Migration Strategy section
- TenantAwareMigration base class
- Row-level security policies for tenant isolation
- Tenant management migrations
- TenantMigrationManager class

### 4. Add Current Database Patterns
Add new sections for:
- Type table pattern (every entity has _type table)
- Map table pattern for many-to-many relationships
- Standard status management pattern
- Relationship patterns using foreign keys

## New Tables Needed

Based on the current GR-02, no new tables are needed. The actual database already contains all necessary tables for the application.

## Migration Path

1. Update the technology stack section to reflect current setup
2. Replace multi-tenant examples with single-database examples
3. Add migration examples that match actual table structures
4. Update best practices to align with current patterns
5. Remove complex features not present in actual database

## Benefits of This Approach

1. **Accuracy**: GR-02 will reflect the actual database structure
2. **Simplicity**: Removes unnecessary multi-tenant complexity
3. **Consistency**: Aligns with existing table patterns
4. **Practicality**: Provides real examples developers can use

## Risks and Mitigation

1. **Risk**: Removing multi-tenant might limit future scalability
   **Mitigation**: Document the single-tenant approach clearly and note it can be extended later

2. **Risk**: Existing code might reference old migration patterns
   **Mitigation**: Keep a note about the change from multi-tenant to single-tenant

## Next Steps

1. Review this approach with stakeholders
2. Upon approval, create updated GR-02 document
3. Update any dependent Global Requirements
4. Document the change in version history