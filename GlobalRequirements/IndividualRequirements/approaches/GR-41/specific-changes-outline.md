# GR-41 Specific Changes Outline

## Overview
This document outlines the specific changes needed in other Global Requirements files due to the update of GR-41 to use INT instead of BIGINT and proper data type standards based on the actual database schema.

## Key Change Summary
- Change all ID fields from BIGINT to INT
- Standardize VARCHAR lengths: VARCHAR(50) for codes, VARCHAR(100) for names
- Update audit field definitions to use INT for user references
- Align with actual database schema patterns

## Changes Required by File

### 1. GR-02: Database Migrations
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/02-database-migrations-updated.md`

**Changes Needed**:
- Update migration examples to use INT for ID fields
- Change foreign key definitions from BIGINT to INT
- Update VARCHAR lengths in examples

**Specific Sections**:
- Migration examples: Change `$table->bigInteger('id')` to `$table->integer('id')`
- Foreign key examples: Use INT for all _id fields
- Example schemas: Update data types

### 2. GR-03: Models Relationships
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/03-models-relationships.md`

**Changes Needed**:
- Update model property types from bigint to int
- Change relationship definitions to expect INT keys
- Update model casting arrays

**Specific Sections**:
- Model Properties: Change ID type hints
- Relationship Methods: Update foreign key types
- Type Casting: Ensure IDs cast to integer

### 3. GR-19: Table Relationships Requirements
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/19-table-relationships-requirements.md`

**Changes Needed**:
- Update all relationship diagrams to show INT for keys
- Change foreign key data type references
- Update index definitions

**Specific Sections**:
- ERD Examples: Change BIGINT to INT
- Foreign Key Definitions: Use INT
- Index Specifications: Match INT type

### 4. GR-40: Database Seeding Requirements
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/40-database-seeding-requirements.md`

**Changes Needed**:
- Update seeder examples to use appropriate data types
- Change ID generation to use INT range
- Update VARCHAR lengths in test data

**Specific Sections**:
- Seeder Classes: Use correct data types
- Factory Definitions: INT for IDs
- Test Data: Proper VARCHAR lengths

### 5. GR-37: Locking Workflow
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/37-locking-workflow-with-centralized-logging-and-action-tracking.md`

**Changes Needed**:
- Ensure lock table uses INT for IDs
- Update action table to use INT
- Verify user_id fields are INT

**Specific Sections**:
- Table Definitions: Already updated
- Foreign Keys: Verify INT usage

### 6. GR-64: Policy Reinstatement
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/64-policy-reinstatement-with-lapse-process.md`

**Changes Needed**:
- Update reinstatement_calculation table definition
- Change all ID fields to INT
- Update decimal field names to match pattern

**Specific Sections**:
- Database Schema: Use INT for IDs
- Field Names: Match actual database patterns

### 7. GR-70: Accounting Architecture
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/70-accounting-architecture.md`

**Changes Needed**:
- Update transaction tables to use INT
- Change decimal precisions to match standards
- Update VARCHAR lengths

**Specific Sections**:
- Transaction Tables: INT for IDs
- GL Tables: Proper data types
- Audit Fields: INT for user references

### 8. GR-52: Universal Entity Management
**Location**: `/workspace/requirements/GlobalRequirements/IndividualRequirements/52-universal-entity-management.md`

**Changes Needed**:
- Update entity tables to use INT
- Standardize VARCHAR lengths
- Ensure JSON fields use TEXT type

**Specific Sections**:
- Entity Table: INT primary key
- Metadata Fields: TEXT for JSON
- Configuration: Proper VARCHAR lengths

## Implementation Guidelines

### Priority Order
1. **High Priority**: Core table definitions (GR-02, GR-19)
2. **Medium Priority**: Related schemas (GR-64, GR-70, GR-52)
3. **Low Priority**: Seeders and examples (GR-40)

### Data Type Quick Reference
```sql
-- IDs
id INT AUTO_INCREMENT PRIMARY KEY
foreign_key_id INT

-- Strings
code VARCHAR(50)
name VARCHAR(100)
email VARCHAR(255)
url VARCHAR(500)
description TEXT

-- Numbers
amount DECIMAL(10,2)
percentage DECIMAL(5,2)
count INT
flag BOOLEAN

-- Dates
date_field DATE
timestamp_field TIMESTAMP
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

-- Audit
created_by INT NULL
updated_by INT NULL
```

### Validation Checklist
- [ ] All ID fields use INT
- [ ] VARCHAR lengths match standards
- [ ] Decimal fields use (10,2) for money
- [ ] Timestamps use proper defaults
- [ ] Foreign keys match primary key types
- [ ] Audit fields use INT for users

## Risk Mitigation

### Potential Issues
1. **Migration Scripts**: May have hardcoded BIGINT
2. **Model Casts**: May expect bigint type
3. **API Responses**: May format IDs as strings

### Mitigation Strategies
1. Global search for "BIGINT" in all files
2. Review model $casts arrays
3. Test API responses for ID formatting
4. Ensure foreign key constraints match

## Benefits of Standardization

1. **Consistency**: All tables use same data types
2. **Performance**: INT uses less storage than BIGINT
3. **Compatibility**: Matches existing database
4. **Maintenance**: Easier to remember standards
5. **Integration**: Works with current codebase

## Summary

The data type standardization requires updates across 8 Global Requirements files. The changes focus on:

1. Using INT instead of BIGINT for all IDs
2. Standardizing VARCHAR lengths by purpose
3. Using consistent decimal precision
4. Matching the actual database schema

This ensures all new development follows the established patterns in the existing database.