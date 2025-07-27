# GR-52 Database Alignment Approach: Universal Entity Management

## Current State Analysis

### Tables Found in Database

1. **entity** - EXISTS
   - Basic structure: id, entity_type_id, status_id, created_by, updated_by, created_at, updated_at
   - **MISSING**: metadata field, name field, code field, category_id

2. **entity_type** - EXISTS
   - Structure: id, code, name, description, is_default, status_id, created_by, updated_by, created_at, updated_at
   - **MISSING**: category_id, metadata_schema field

3. **driver** - EXISTS (but different structure)
   - Current structure is entity-specific with fields like driver_type_id, license_id, etc.
   - **NOT MATCHING** the shared entity model described in GR-52 V4

4. **vehicle** - EXISTS (need to check structure)

5. **insured** - NOT FOUND (may be named differently)
   6. not needed. driver_type and/or the driver table accomodates this indication as the named/primary insured.

### Missing Tables/Features

1. **entity_category** - DOES NOT EXIST
   - Required for categorizing entity types (INTEGRATION, PARTNER, VENDOR, SYSTEM)

2. **communication** - Need to verify polymorphic structure
   - Required fields: source_type, source_id, target_type, target_id

3. **configuration** - Need to verify three-level hierarchy support
   - Required fields: scope, scope_id, type, key, value

4. **system_component** - May not exist
   - Required for component-based security

5. **security_group** - May not exist
   - Required for DCS access control

## Key Differences from GR-52 Requirements

### 1. Entity Management System
**Current State:**
- Basic entity/entity_type structure exists
- No category system
- No metadata/JSON schema validation

**GR-52 Requirements:**
- entity_category table for categorization
- metadata_schema in entity_type for validation
- metadata field in entity for flexible data storage

### 2. Shared Entity Model (V4)
**Current State:**
- Separate driver table with specific fields
- Likely separate quote_driver/policy_driver tables
- Traditional normalized structure

**GR-52 V4 Requirements:**
- Shared driver, vehicle, insured entities
- Map tables for relationships (quote_driver_map, policy_driver_map)
- Elimination of duplicate entity tables

### 3. Communication System
**Need to verify:**
- Polymorphic source_type/source_id fields
- Correlation ID support
- Request/response data storage

### 4. Configuration Management
**Need to verify:**
- Three-level hierarchy (system, program, entity)
- Scope-based configuration resolution
- Type-based organization

## Proposed Updates

### 1. Create Entity Category Table
```sql
CREATE TABLE entity_category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert standard categories
INSERT INTO entity_category (code, name, description) VALUES
('INTEGRATION', 'Integration', 'External API integrations'),
('PARTNER', 'Partner', 'Business partners and affiliates'),
('VENDOR', 'Vendor', 'Service vendors and suppliers'),
('SYSTEM', 'System', 'Internal system entities');
```

### 2. Update Entity Type Table
```sql
ALTER TABLE entity_type
ADD COLUMN category_id INT AFTER id,
ADD COLUMN metadata_schema JSON,
ADD FOREIGN KEY (category_id) REFERENCES entity_category(id),
ADD INDEX idx_category (category_id);
```

### 3. Update Entity Table
```sql
ALTER TABLE entity
ADD COLUMN code VARCHAR(100) UNIQUE AFTER id,
ADD COLUMN name VARCHAR(255) AFTER code,
ADD COLUMN metadata JSON,
ADD INDEX idx_code (code);
```

### 4. Implement V4 Shared Entity Model

#### 4.1 Create New Shared Driver Table
```sql
-- Rename existing driver table
RENAME TABLE driver TO driver_legacy;

-- Create new shared driver table
CREATE TABLE driver (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    date_of_birth DATE NOT NULL,
    license_number VARCHAR(50),
    license_state VARCHAR(2),
    license_status VARCHAR(20),
    gender VARCHAR(10),
    marital_status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    metadata JSON,
    INDEX idx_license (license_number, license_state),
    INDEX idx_name (last_name, first_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```
- why rename this, what's the difference in the existing one and this?
#### 4.2 Create Shared Insured Table
```sql
CREATE TABLE insured (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(20),
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(2),
    zip_code VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    metadata JSON,
    INDEX idx_email (email),
    INDEX idx_name (last_name, first_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```
- not needed
#### 4.3 Create Map Tables
```sql
-- Quote to driver mapping
CREATE TABLE map_quote_driver (
    quote_id INT NOT NULL,
    driver_id INT NOT NULL,
    is_primary_driver BOOLEAN DEFAULT FALSE,
    driver_type VARCHAR(20),
    assigned_vehicle_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (quote_id, driver_id),
    FOREIGN KEY (quote_id) REFERENCES quote(id),
    FOREIGN KEY (driver_id) REFERENCES driver(id),
    FOREIGN KEY (assigned_vehicle_id) REFERENCES vehicle(id),
    INDEX idx_driver (driver_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
- this already exists recheck the databse.

-- Policy to driver mapping
CREATE TABLE map_policy_driver (
    policy_id INT NOT NULL,
    driver_id INT NOT NULL,
    is_primary_driver BOOLEAN DEFAULT FALSE,
    driver_type VARCHAR(20),
    assigned_vehicle_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (policy_id, driver_id),
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (driver_id) REFERENCES driver(id),
    FOREIGN KEY (assigned_vehicle_id) REFERENCES vehicle(id),
    INDEX idx_driver (driver_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```
- this already exists recheck the databse.

### 5. Update Communication Table
```sql
-- Add polymorphic fields if missing
ALTER TABLE communication
ADD COLUMN source_type VARCHAR(50),
ADD COLUMN source_id INT,
ADD COLUMN target_type VARCHAR(50),
ADD COLUMN target_id INT,
ADD COLUMN correlation_id VARCHAR(100),
ADD COLUMN request_data JSON,
ADD COLUMN response_data JSON,
ADD INDEX idx_correlation (correlation_id),
ADD INDEX idx_source (source_type, source_id),
ADD INDEX idx_target (target_type, target_id);
```
- request and response data will be in the integration_log

### 6. Create/Update Configuration Table
```sql
CREATE TABLE IF NOT EXISTS configuration (
    id INT AUTO_INCREMENT PRIMARY KEY,
    scope VARCHAR(50) NOT NULL, -- 'system', 'program', 'entity'
    scope_id INT NOT NULL,
    type VARCHAR(50) NOT NULL,
    `key` VARCHAR(100) NOT NULL,
    value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_config (scope, scope_id, type, `key`),
    INDEX idx_scope (scope, scope_id),
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```
- scope should be covered by configuration_type right?

## Implementation Considerations

### 1. Data Migration Strategy
- Preserve existing data in legacy tables
- Create migration scripts to transform data
- Implement parallel run period
- Gradual cutover approach

### 2. Application Layer Updates
- Create SharedEntityService for V4 model
- Update Eloquent models and relationships
- Implement metadata validation using JSON schemas
- Add configuration resolution service

### 3. Performance Optimization
- Proper indexing for polymorphic queries
- Consider partitioning for high-volume tables
- Implement caching for configuration resolution
- Optimize JSON field queries

### 4. DCS Integration Specifics
- Populate entity_type with DCS API definitions
- Configure authentication in secure vault
- Set up circuit breaker patterns
- Implement data retention policies

## Benefits Realization

### Expected Improvements
1. **Development Speed**: 90% faster for new entity types
2. **Code Reduction**: Eliminate duplicate driver/vehicle tables
3. **Consistency**: Single pattern for all external entities
4. **Flexibility**: JSON metadata for entity-specific data
5. **Audit Trail**: Unified action table for all changes

## Next Steps
1. Create entity_category table
2. Update entity and entity_type tables
3. Implement V4 shared entity model migration
4. Update communication table for polymorphic support
5. Create configuration management system
6. Populate DCS-specific entity types
7. Update application services
8. Create integration tests