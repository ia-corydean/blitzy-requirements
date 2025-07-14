# Database Table Naming Conventions (GR-41)

## Overview
This document defines the standardized table naming conventions that must be followed across all business domains to ensure consistency, maintainability, and automated tooling compatibility.

## Core Naming Principles

### 1. Singular Table Names
- **Rule**: All table names must be singular
- **Examples**: 
  - ✅ `driver`, `vehicle`, `policy`
  - ❌ `drivers`, `vehicles`, `policies`
- **Rationale**: Singular names represent the entity being stored, not a collection

### 2. Lowercase with Underscore Separation
- **Rule**: Use lowercase letters with underscores for multi-word names
- **Examples**:
  - ✅ `driver_license`, `vehicle_type`, `payment_method`
  - ❌ `DriverLicense`, `vehicleType`, `PaymentMethod`
- **Rationale**: Database portability and consistency across platforms

### 3. Relationship Table Prefix
- **Rule**: Many-to-many relationship tables use `map_` prefix
- **Format**: `map_{entity1}_{entity2}`
- **Examples**:
  - ✅ `map_quote_driver`, `map_driver_vehicle`, `map_policy_address`
  - ❌ `quote_drivers`, `driver_vehicles`, `policy_addresses`
- **Rationale**: Clear identification of relationship tables

### 4. Reference Table Suffix
- **Rule**: Lookup/reference tables use `_type` suffix
- **Examples**:
  - ✅ `driver_type`, `vehicle_type`, `payment_type`, `address_type`
  - ❌ `driver_types`, `vehicle_category`, `payment_kinds`
- **Rationale**: Consistent identification of reference data

### 5. Foreign Key Naming
- **Rule**: Foreign keys use `{table}_id` format
- **Examples**:
  - ✅ `driver_id`, `vehicle_id`, `policy_id`, `quote_id`
  - ❌ `driverId`, `vehicle_key`, `policy_ref`
- **Rationale**: Clear identification of relationships

## Table Categories and Examples

### Core Business Entity Tables
```sql
-- Primary business entities
driver
vehicle  
policy
quote
producer
payment
address
phone
email

-- External entities (GR-52 compliance)
external_entity
api_endpoint
attorney
body_shop
vendor
```

### Reference Tables (`_type` suffix)
```sql
-- Classification tables
driver_type          -- (primary, secondary, excluded, etc.)
vehicle_type         -- (auto, motorcycle, commercial, etc.)  
policy_type          -- (personal_auto, commercial, etc.)
quote_type           -- (new_business, renewal, amendment)
payment_type         -- (premium, fee, refund, commission)
address_type         -- (residential, mailing, business, garaging)
phone_type           -- (mobile, home, work, fax)
email_type           -- (personal, work, billing)
status_type          -- (active, inactive, pending, cancelled)
```

### Relationship Tables (`map_` prefix)
```sql
-- Many-to-many relationships
map_quote_driver          -- Drivers on a quote
map_quote_vehicle         -- Vehicles on a quote  
map_driver_vehicle        -- Which drivers can operate which vehicles
map_policy_address        -- Addresses associated with policy
map_driver_phone          -- Phone numbers for a driver
map_producer_email        -- Email addresses for a producer
map_external_entity_address -- Addresses for external entities
```

### Supporting Tables
```sql
-- Universal tables
status                -- Universal status reference (GR-19)
name                  -- Universal name entity
territory             -- Rating territories
coverage              -- Insurance coverages
rate_factor           -- Rating factors

-- Audit and logging
audit_log             -- Change tracking
communication_log     -- Communication attempts
error_log             -- System errors
```

## Field Naming Conventions

### Primary Keys
- **Format**: `id` (always singular)
- **Type**: `bigint PRIMARY KEY AUTO_INCREMENT`
- **Example**: Every table has an `id` field

### Foreign Keys
- **Format**: `{referenced_table}_id`
- **Examples**: `driver_id`, `vehicle_id`, `quote_id`
- **Type**: `bigint` with appropriate foreign key constraints

### Boolean Fields
- **Format**: `is_{condition}` or `has_{attribute}`
- **Examples**: `is_primary`, `is_verified`, `has_sr22_requirement`
- **Type**: `boolean` with appropriate defaults

### Date/Time Fields
- **Specific dates**: `{purpose}_date`
  - Examples: `effective_date`, `expiration_date`, `birth_date`
- **Timestamps**: `{purpose}_at`
  - Examples: `created_at`, `updated_at`, `verified_at`

### Audit Fields (Required on all tables)
```sql
created_by    bigint NOT NULL           -- User who created record
updated_by    bigint NOT NULL           -- User who last updated record  
created_at    timestamp DEFAULT CURRENT_TIMESTAMP
updated_at    timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

## Index Naming Conventions

### Primary Index
- **Format**: Automatically named by database
- **Example**: Table `driver` has primary key automatically indexed

### Foreign Key Indexes
- **Format**: `idx_{table}_{foreign_key_field}`
- **Examples**: 
  - `idx_driver_status_id`
  - `idx_quote_producer_id`

### Composite Indexes
- **Format**: `idx_{table}_{field1}_{field2}_{etc}`
- **Examples**:
  - `idx_payment_policy_status_date`
  - `idx_driver_status_primary`

### Unique Constraints
- **Format**: `unique_{table}_{field}` or `unique_{table}_{field1}_{field2}`
- **Examples**:
  - `unique_driver_license_number`
  - `unique_quote_producer_number`

## Constraint Naming Conventions

### Foreign Key Constraints
- **Format**: `fk_{table}_{referenced_table}`
- **Examples**:
  - `fk_driver_status` 
  - `fk_quote_producer`

### Check Constraints
- **Format**: `chk_{table}_{field}_{validation}`
- **Examples**:
  - `chk_driver_age_range`
  - `chk_payment_amount_positive`

### Unique Constraints
- **Format**: `uk_{table}_{field}`
- **Examples**:
  - `uk_driver_license_number`
  - `uk_vehicle_vin`

## Domain-Specific Patterns

### Producer Portal
```sql
-- Core entities follow standard naming
quote
driver  
vehicle
coverage

-- Relationship tables
map_quote_driver
map_quote_vehicle
map_driver_vehicle

-- Reference tables
quote_type
driver_type
vehicle_type
coverage_type
```

### Accounting
```sql
-- Financial entities
payment
billing_cycle
commission
invoice

-- Relationship tables  
map_payment_billing_cycle
map_producer_commission

-- Reference tables
payment_type
billing_type
commission_type
```

### Universal Entities (GR-52)
```sql
-- External entity management
external_entity
external_entity_type
external_entity_metadata

-- Polymorphic relationships
map_external_entity_address
map_external_entity_phone  
map_external_entity_email
```

## Validation Rules

### Automated Checks
1. **Singular verification**: No table names ending in 's'
2. **Prefix validation**: Relationship tables must start with `map_`
3. **Suffix validation**: Reference tables must end with `_type`
4. **Foreign key format**: Must follow `{table}_id` pattern
5. **Audit field presence**: All tables must have audit fields

### Manual Review Requirements
1. **Business logic naming**: Field names accurately reflect business purpose
2. **Consistency check**: Similar concepts use similar naming patterns
3. **Future scalability**: Names support anticipated business growth

## Migration Guidelines

### From Legacy Systems
1. **Identify current naming patterns**: Document existing conventions
2. **Create mapping table**: Map legacy names to new standards
3. **Gradual migration**: Migrate in phases to minimize disruption
4. **Alias support**: Create views with legacy names during transition

### Implementation Steps
1. **Review existing schema**: Audit current naming compliance
2. **Generate migration scripts**: Automated renaming where possible
3. **Update application code**: Modify queries to use new names
4. **Validate functionality**: Comprehensive testing post-migration

## Compliance Monitoring

### Automated Monitoring
- **Schema validation**: Automated checking of naming conventions
- **CI/CD integration**: Prevent non-compliant changes from deployment
- **Documentation generation**: Auto-generate schema documentation

### Regular Reviews
- **Monthly audits**: Review new tables and fields for compliance
- **Quarterly assessments**: Evaluate naming convention effectiveness
- **Annual reviews**: Consider updates to conventions based on business needs

## Examples of Complete Table Definitions

### Core Entity Example
```sql
CREATE TABLE driver (
    id bigint PRIMARY KEY AUTO_INCREMENT,
    name_id bigint NOT NULL,
    date_of_birth date NOT NULL,
    driver_type_id bigint NOT NULL,
    is_named_insured boolean DEFAULT false,
    driver_license_number varchar(50),
    driver_license_state char(2),
    status_id bigint NOT NULL,
    created_by bigint NOT NULL,
    updated_by bigint NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (name_id) REFERENCES name(id),
    FOREIGN KEY (driver_type_id) REFERENCES driver_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_driver_status (status_id),
    INDEX idx_driver_named_insured (is_named_insured),
    UNIQUE KEY uk_driver_license (driver_license_number, driver_license_state)
);
```

### Relationship Table Example
```sql
CREATE TABLE map_quote_driver (
    id bigint PRIMARY KEY AUTO_INCREMENT,
    quote_id bigint NOT NULL,
    driver_id bigint NOT NULL,
    created_by bigint NOT NULL,
    updated_by bigint NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (quote_id) REFERENCES quote(id),
    FOREIGN KEY (driver_id) REFERENCES driver(id),
    
    INDEX idx_map_quote_driver_quote (quote_id),
    INDEX idx_map_quote_driver_driver (driver_id),
    UNIQUE KEY uk_map_quote_driver (quote_id, driver_id)
);
```

### Reference Table Example  
```sql
CREATE TABLE driver_type (
    id bigint PRIMARY KEY AUTO_INCREMENT,
    name varchar(50) NOT NULL,
    description text,
    sort_order int DEFAULT 0,
    is_active boolean DEFAULT true,
    created_by bigint NOT NULL,
    updated_by bigint NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_driver_type_name (name)
);
```

## Integration with Global Requirements

### GR-52 Universal Entity Management
- External entities follow same naming conventions
- Metadata-driven entity types use standard `_type` suffix
- Polymorphic relationships use `map_external_entity_*` pattern

### GR-19 Table Relationships  
- All foreign keys follow `{table}_id` naming
- Status management uses universal `status` table
- Relationship tables clearly identified with `map_` prefix

### GR-02 Database Migrations
- All naming changes tracked in migration scripts
- Audit fields consistently named across all tables
- Migration rollback supported through naming consistency

This comprehensive naming convention ensures database consistency, maintainability, and automated tooling compatibility across all business domains.