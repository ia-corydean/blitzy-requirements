# GR-52 Database Alignment Approach - V2

## Overview
This document outlines the approach for working with existing driver tables and map tables, leveraging the current database structure rather than creating new tables.

## Current Table Analysis

### Existing Tables
1. **driver** - Core driver entity table (already exists)
2. **driver_type** - Driver categorization table (already exists)
3. **map_quote_driver** - Links drivers to quotes (already exists)
4. **map_policy_driver** - Links drivers to policies (already exists)
5. **configuration** - General configuration table (already exists)
6. **configuration_type** - Configuration categorization (already exists)

## Approach: Extending Existing Tables

### 1. Extend Driver Table for Additional GR-52 Requirements
```sql
-- Add GR-52 specific fields to existing driver table
ALTER TABLE driver 
ADD COLUMN IF NOT EXISTS license_number VARCHAR(50) COMMENT 'Driver license number',
ADD COLUMN IF NOT EXISTS license_state VARCHAR(2) COMMENT 'License issuing state',
ADD COLUMN IF NOT EXISTS license_expiry_date DATE COMMENT 'License expiration date',
ADD COLUMN IF NOT EXISTS date_of_birth DATE COMMENT 'Driver date of birth',
ADD COLUMN IF NOT EXISTS first_licensed_date DATE COMMENT 'Date first licensed',
ADD COLUMN IF NOT EXISTS is_primary_driver BOOLEAN DEFAULT FALSE COMMENT 'Primary driver flag',
ADD COLUMN IF NOT EXISTS is_excluded BOOLEAN DEFAULT FALSE COMMENT 'Excluded driver flag',
ADD COLUMN IF NOT EXISTS mvr_ordered_date DATE COMMENT 'MVR order date',
ADD COLUMN IF NOT EXISTS mvr_status VARCHAR(50) COMMENT 'MVR status',
ADD INDEX idx_driver_license (license_number, license_state),
ADD INDEX idx_driver_dob (date_of_birth);
```

### 2. Use Configuration Tables for Driver Settings
```sql
-- Add driver-related configuration types
INSERT INTO configuration_type (code, name, description, is_default, status_id) VALUES
('DRIVER_MVR_SETTINGS', 'Driver MVR Settings', 'Motor Vehicle Record ordering configuration', FALSE, 1),
('DRIVER_VALIDATION_RULES', 'Driver Validation Rules', 'Driver data validation rules', FALSE, 1),
('DRIVER_RATING_FACTORS', 'Driver Rating Factors', 'Driver-based rating configuration', FALSE, 1),
('DRIVER_EXCLUSION_RULES', 'Driver Exclusion Rules', 'Rules for driver exclusions', FALSE, 1);

-- Example configuration entries
INSERT INTO configuration (configuration_type_id, status_id) 
SELECT id, 1 FROM configuration_type WHERE code = 'DRIVER_MVR_SETTINGS';
```

### 3. Enhance Map Tables for Better Driver Relationships
```sql
-- Extend map_quote_driver for additional relationship data
ALTER TABLE map_quote_driver
ADD COLUMN IF NOT EXISTS is_primary BOOLEAN DEFAULT FALSE COMMENT 'Primary driver for quote',
ADD COLUMN IF NOT EXISTS driver_type VARCHAR(50) COMMENT 'Type of driver for this quote',
ADD COLUMN IF NOT EXISTS assigned_vehicle_id INT COMMENT 'Primary vehicle assignment',
ADD COLUMN IF NOT EXISTS effective_date DATE COMMENT 'When driver added to quote',
ADD INDEX idx_quote_driver_primary (quote_id, is_primary),
ADD CONSTRAINT fk_map_quote_driver_vehicle 
    FOREIGN KEY (assigned_vehicle_id) 
    REFERENCES vehicle(id) 
    ON UPDATE CASCADE;

-- Extend map_policy_driver for policy-specific data
ALTER TABLE map_policy_driver
ADD COLUMN IF NOT EXISTS is_primary BOOLEAN DEFAULT FALSE COMMENT 'Primary driver for policy',
ADD COLUMN IF NOT EXISTS driver_type VARCHAR(50) COMMENT 'Type of driver for this policy',
ADD COLUMN IF NOT EXISTS assigned_vehicle_id INT COMMENT 'Primary vehicle assignment',
ADD COLUMN IF NOT EXISTS effective_date DATE COMMENT 'When driver added to policy',
ADD COLUMN IF NOT EXISTS end_date DATE COMMENT 'When driver removed from policy',
ADD INDEX idx_policy_driver_primary (policy_id, is_primary),
ADD INDEX idx_policy_driver_dates (effective_date, end_date),
ADD CONSTRAINT fk_map_policy_driver_vehicle 
    FOREIGN KEY (assigned_vehicle_id) 
    REFERENCES vehicle(id) 
    ON UPDATE CASCADE;
```

### 4. Create Supporting Views
```sql
-- View for active drivers on policies
CREATE VIEW v_active_policy_drivers AS
SELECT 
    p.id as policy_id,
    p.policy_number,
    d.id as driver_id,
    d.license_number,
    d.license_state,
    d.date_of_birth,
    TIMESTAMPDIFF(YEAR, d.date_of_birth, CURDATE()) as age,
    mpd.is_primary,
    mpd.driver_type,
    mpd.effective_date,
    v.vin as assigned_vehicle_vin,
    dt.name as driver_type_name,
    s.name as driver_status
FROM map_policy_driver mpd
JOIN policy p ON mpd.policy_id = p.id
JOIN driver d ON mpd.driver_id = d.id
JOIN driver_type dt ON d.driver_type_id = dt.id
LEFT JOIN vehicle v ON mpd.assigned_vehicle_id = v.id
LEFT JOIN status s ON d.status_id = s.id
WHERE mpd.status_id = 1
AND (mpd.end_date IS NULL OR mpd.end_date > CURDATE());

-- View for driver history
CREATE VIEW v_driver_history AS
SELECT 
    d.id as driver_id,
    d.license_number,
    COUNT(DISTINCT mpd.policy_id) as total_policies,
    COUNT(DISTINCT mqd.quote_id) as total_quotes,
    MIN(mpd.effective_date) as first_policy_date,
    MAX(mpd.effective_date) as last_policy_date,
    SUM(CASE WHEN mpd.is_primary THEN 1 ELSE 0 END) as times_primary_driver
FROM driver d
LEFT JOIN map_policy_driver mpd ON d.id = mpd.driver_id
LEFT JOIN map_quote_driver mqd ON d.id = mqd.driver_id
GROUP BY d.id;
```

### 5. Driver Configuration Management
```sql
-- Create a flexible key-value store for driver configurations
CREATE TABLE IF NOT EXISTS configuration_value (
    id INT AUTO_INCREMENT PRIMARY KEY,
    configuration_id INT NOT NULL COMMENT 'Reference to configuration',
    key_name VARCHAR(100) NOT NULL COMMENT 'Configuration key',
    value_text TEXT COMMENT 'Text value',
    value_number DECIMAL(10,2) COMMENT 'Numeric value',
    value_date DATE COMMENT 'Date value',
    value_json JSON COMMENT 'JSON value for complex data',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_config_key (configuration_id, key_name),
    CONSTRAINT fk_configuration_value_config 
        FOREIGN KEY (configuration_id) 
        REFERENCES configuration(id) 
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Flexible configuration value storage';

-- Example driver configuration values
INSERT INTO configuration_value (configuration_id, key_name, value_text, value_number) VALUES
((SELECT c.id FROM configuration c JOIN configuration_type ct ON c.configuration_type_id = ct.id WHERE ct.code = 'DRIVER_MVR_SETTINGS'), 
 'mvr_order_threshold_days', 'Days before MVR expires', 30),
((SELECT c.id FROM configuration c JOIN configuration_type ct ON c.configuration_type_id = ct.id WHERE ct.code = 'DRIVER_MVR_SETTINGS'), 
 'mvr_auto_order', 'true', NULL),
((SELECT c.id FROM configuration c JOIN configuration_type ct ON c.configuration_type_id = ct.id WHERE ct.code = 'DRIVER_VALIDATION_RULES'), 
 'min_driver_age', NULL, 16),
((SELECT c.id FROM configuration c JOIN configuration_type ct ON c.configuration_type_id = ct.id WHERE ct.code = 'DRIVER_VALIDATION_RULES'), 
 'max_driver_age', NULL, 99);
```

## Why Not Create driver_v52?

The existing `driver` table is sufficient because:
1. It already follows the standard entity pattern with type table
2. Adding columns to existing table maintains data integrity
3. Existing relationships (map tables) remain intact
4. No need to migrate data or update foreign keys
5. Application code changes are minimal

## Benefits of This Approach

1. **No Redundancy**: Uses existing tables, avoiding duplication
2. **Maintains Relationships**: All existing foreign keys remain valid
3. **Configuration Flexibility**: Uses configuration_type pattern for extensibility
4. **Backward Compatible**: Existing queries continue to work
5. **Scalable**: Can add new configuration types without schema changes

## Example Usage

### Adding a Driver to Quote
```sql
-- Add driver with extended information
INSERT INTO driver (driver_type_id, license_number, license_state, date_of_birth, first_licensed_date, status_id)
VALUES (
    (SELECT id FROM driver_type WHERE code = 'PRIMARY'),
    'D123456789',
    'CA',
    '1985-03-15',
    '2001-03-15',
    1
);

-- Link to quote with additional details
INSERT INTO map_quote_driver (quote_id, driver_id, is_primary, driver_type, effective_date, status_id)
VALUES (
    123, -- quote_id
    LAST_INSERT_ID(),
    TRUE,
    'PRIMARY_OPERATOR',
    CURDATE(),
    1
);
```

### Configuring Driver Rules
```sql
-- Set up MVR ordering rules for a program
INSERT INTO configuration_value (configuration_id, key_name, value_json)
SELECT 
    c.id,
    'mvr_order_rules',
    JSON_OBJECT(
        'auto_order_on_quote', true,
        'order_threshold_days', 30,
        'required_states', JSON_ARRAY('CA', 'TX', 'FL'),
        'excluded_license_types', JSON_ARRAY('PERMIT', 'EXPIRED')
    )
FROM configuration c
JOIN configuration_type ct ON c.configuration_type_id = ct.id
WHERE ct.code = 'DRIVER_MVR_SETTINGS';
```

## Migration Path

1. **Phase 1**: Extend existing tables with new columns
2. **Phase 2**: Insert configuration types and values
3. **Phase 3**: Create views for reporting
4. **Phase 4**: Update application to use extended fields

## Conclusion

This approach maximizes the use of existing database structures while meeting all GR-52 requirements. By extending rather than replacing tables, we maintain system integrity and minimize migration complexity.