# GR-41 Database Alignment Approach - V3

## Overview
This document narrows the focus of GR-41 to specifically address table schema requirements and standards, removing overlapping content with other GRs.

## Changes from V2
1. **Removed reinstatement-specific content** - This is covered comprehensively in GR-64
2. **Focused solely on schema standards** - Core naming conventions and structure patterns
3. **Eliminated redundant transaction examples** - These belong in implementation guides
4. **Streamlined to essential schema requirements** - Removed application-level concerns

## Analysis: Should GR-41 Be Removed?

After analyzing other Global Requirements, GR-41 could potentially be merged or removed because:

1. **GR-02 (Database Migrations)** - Covers table structure patterns and standards
2. **GR-19 (Table Relationships)** - Defines relationship patterns and foreign key standards
3. **GR-40 (Database Seeding)** - Covers initial data requirements
4. **Specific GRs** - Each domain GR (64, 70, etc.) defines its own schema needs

However, GR-41 serves as a **central reference** for schema standards that other GRs reference.

## Core Schema Standards (Retained Focus)

### 1. Table Naming Conventions
```sql
-- Core entity tables: singular nouns
CREATE TABLE user (...);
CREATE TABLE policy (...);
CREATE TABLE driver (...);

-- Reference tables: _type suffix
CREATE TABLE user_type (...);
CREATE TABLE document_type (...);

-- Mapping tables: map_ prefix with singular nouns
CREATE TABLE map_user_group (...);
CREATE TABLE map_policy_driver (...);
```

### 2. Standard Column Requirements
Every table MUST include:
```sql
id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
status_id BIGINT UNSIGNED NOT NULL,
created_by BIGINT UNSIGNED NOT NULL,
updated_by BIGINT UNSIGNED NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

### 3. Foreign Key Standards
```sql
-- Consistent naming: fk_[table]_[referenced_table]
CONSTRAINT fk_user_status FOREIGN KEY (status_id) REFERENCES status(id)

-- Cascade rules
ON DELETE RESTRICT  -- Default for data integrity
ON UPDATE CASCADE   -- Allow referenced ID updates
```

### 4. Index Standards
```sql
-- Primary indexes on foreign keys
INDEX idx_[column_name] (column_name)

-- Composite indexes for common queries
INDEX idx_[table]_[col1]_[col2] (column1, column2)
```

### 5. Data Type Standards
- **IDs**: BIGINT UNSIGNED
- **Names**: VARCHAR(255)
- **Codes**: VARCHAR(50)
- **Descriptions**: TEXT
- **Money**: DECIMAL(10,2)
- **Percentages**: DECIMAL(5,4)
- **Dates**: DATE or DATETIME
- **Booleans**: BOOLEAN (not TINYINT)

### 6. Comment Requirements
```sql
-- Table comments explain purpose
COMMENT='Stores user account information'

-- Column comments for non-obvious fields
reinstatement_date DATE COMMENT 'Effective date of reinstatement'
```

## Recommendation

**Keep GR-41** but limit its scope to:
1. Core naming conventions
2. Standard column requirements
3. Data type standards
4. Comment requirements

Remove all domain-specific content (reinstatements, transactions, etc.) as these are covered by their respective GRs.

## Cross-References
- **GR-02**: Database migration patterns
- **GR-19**: Table relationship requirements
- **GR-64**: Reinstatement-specific schemas
- **GR-70**: Accounting-specific schemas

## Conclusion

GR-41 should remain as a focused reference for table schema standards that all other GRs can reference. Domain-specific schema requirements should reside in their respective GRs (64, 70, etc.), while GR-41 maintains the universal standards applicable across all tables.