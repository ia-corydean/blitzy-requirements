# GR-52 Database Alignment Approach - V3

## Overview
This document aligns the driver entity management approach with the patterns established in the Producer Portal completed requirements, specifically referencing how drivers are handled in the New Quote workflow.

## Changes from V2
1. **Added reference table requirements** - Based on IP269-New-Quote-Step-2-Drivers.md
2. **Enhanced map table relationships** - Incorporated relationship_to_insured pattern
3. **Added violation tracking** - New driver_violation table as per Producer Portal
4. **Aligned with completed requirements** - Following established patterns from completed work

## Current State Analysis

From the Producer Portal completed requirements (IP269-New-Quote-Step-2-Drivers.md), we have established patterns for:
- Driver entity with extended attributes
- Relationship tracking via map tables
- Violation management
- SR-22 requirement handling
- Employment and occupation tracking

## Approach: Align with Producer Portal Patterns

### 1. Extend Driver Table per Producer Portal Requirements
```sql
-- Align with fields identified in IP269-New-Quote-Step-2-Drivers
ALTER TABLE driver 
ADD COLUMN IF NOT EXISTS suffix VARCHAR(10) COMMENT 'Name suffix (Jr, Sr, III)',
ADD COLUMN IF NOT EXISTS middle_name VARCHAR(50) COMMENT 'Driver middle name',
ADD COLUMN IF NOT EXISTS gender CHAR(1) COMMENT 'M/F/X',
ADD COLUMN IF NOT EXISTS marital_status VARCHAR(20) COMMENT 'Single/Married/Divorced/Widowed',
ADD COLUMN IF NOT EXISTS employment_status_id INT COMMENT 'Employment status reference',
ADD COLUMN IF NOT EXISTS occupation VARCHAR(100) COMMENT 'Occupation/Source of income',
ADD COLUMN IF NOT EXISTS employer_name VARCHAR(100) COMMENT 'Current employer',
ADD COLUMN IF NOT EXISTS sr22_required BOOLEAN DEFAULT FALSE COMMENT 'SR-22 requirement flag',
ADD COLUMN IF NOT EXISTS sr22_reason_id INT COMMENT 'Reason for SR-22 requirement',
ADD COLUMN IF NOT EXISTS country_licensed VARCHAR(2) DEFAULT 'US' COMMENT 'Country of license',
ADD COLUMN IF NOT EXISTS driver_license_type VARCHAR(50) COMMENT 'Type of license',
-- Keep existing fields from v2
ADD COLUMN IF NOT EXISTS license_number VARCHAR(50) COMMENT 'Driver license number',
ADD COLUMN IF NOT EXISTS license_state VARCHAR(2) COMMENT 'License issuing state',
ADD COLUMN IF NOT EXISTS license_expiry_date DATE COMMENT 'License expiration date',
ADD COLUMN IF NOT EXISTS date_of_birth DATE COMMENT 'Driver date of birth',
ADD COLUMN IF NOT EXISTS first_licensed_date DATE COMMENT 'Date first licensed',
ADD COLUMN IF NOT EXISTS is_excluded BOOLEAN DEFAULT FALSE COMMENT 'Excluded driver flag',
ADD COLUMN IF NOT EXISTS mvr_ordered_date DATE COMMENT 'MVR order date',
ADD COLUMN IF NOT EXISTS mvr_status VARCHAR(50) COMMENT 'MVR status',
ADD INDEX idx_driver_license (license_number, license_state),
ADD INDEX idx_driver_dob (date_of_birth),
ADD INDEX idx_driver_sr22 (sr22_required),
ADD CONSTRAINT fk_driver_employment_status 
    FOREIGN KEY (employment_status_id) 
    REFERENCES employment_status(id),
ADD CONSTRAINT fk_driver_sr22_reason 
    FOREIGN KEY (sr22_reason_id) 
    REFERENCES sr22_reason(id);
```

### 2. Create Reference Tables per Producer Portal
```sql
-- Employment Status (new per IP269)
CREATE TABLE IF NOT EXISTS employment_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    status_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_employment_status_code (code),
    CONSTRAINT fk_employment_status_status 
        FOREIGN KEY (status_id) 
        REFERENCES status(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Employment status reference lookup';

-- Relationship to Insured (new per IP269)
CREATE TABLE IF NOT EXISTS relationship_to_insured (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    status_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_relationship_code (code),
    CONSTRAINT fk_relationship_status 
        FOREIGN KEY (status_id) 
        REFERENCES status(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Driver relationship types to primary insured';

-- SR-22 Reason (new per IP269)
CREATE TABLE IF NOT EXISTS sr22_reason (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    status_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_sr22_reason_code (code),
    CONSTRAINT fk_sr22_reason_status 
        FOREIGN KEY (status_id) 
        REFERENCES status(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='SR-22 requirement reasons';

-- Violation Type (new per IP269)
CREATE TABLE IF NOT EXISTS violation_type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    severity VARCHAR(20) COMMENT 'MINOR/MAJOR/SEVERE',
    points INT DEFAULT 0 COMMENT 'DMV points assigned',
    is_default BOOLEAN DEFAULT FALSE,
    status_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_violation_type_code (code),
    INDEX idx_violation_type_severity (severity),
    CONSTRAINT fk_violation_type_status 
        FOREIGN KEY (status_id) 
        REFERENCES status(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Violation type classification';
```

### 3. Enhance Map Tables per Producer Portal Patterns
```sql
-- Update map_quote_driver to match IP269 requirements
ALTER TABLE map_quote_driver
ADD COLUMN IF NOT EXISTS relationship_to_insured_id INT COMMENT 'Relationship type',
ADD COLUMN IF NOT EXISTS include_status VARCHAR(20) DEFAULT 'included' COMMENT 'included/excluded/removed',
ADD COLUMN IF NOT EXISTS is_primary BOOLEAN DEFAULT FALSE COMMENT 'Primary driver for quote',
ADD COLUMN IF NOT EXISTS driver_type VARCHAR(50) COMMENT 'Type of driver for this quote',
ADD COLUMN IF NOT EXISTS assigned_vehicle_id INT COMMENT 'Primary vehicle assignment',
ADD COLUMN IF NOT EXISTS effective_date DATE COMMENT 'When driver added to quote',
ADD INDEX idx_quote_driver_primary (quote_id, is_primary),
ADD INDEX idx_quote_driver_status (include_status),
ADD CONSTRAINT fk_map_quote_driver_relationship 
    FOREIGN KEY (relationship_to_insured_id) 
    REFERENCES relationship_to_insured(id),
ADD CONSTRAINT fk_map_quote_driver_vehicle 
    FOREIGN KEY (assigned_vehicle_id) 
    REFERENCES vehicle(id) 
    ON UPDATE CASCADE;

-- Update map_policy_driver similarly
ALTER TABLE map_policy_driver
ADD COLUMN IF NOT EXISTS relationship_to_insured_id INT COMMENT 'Relationship type',
ADD COLUMN IF NOT EXISTS include_status VARCHAR(20) DEFAULT 'included' COMMENT 'included/excluded/removed',
ADD COLUMN IF NOT EXISTS is_primary BOOLEAN DEFAULT FALSE COMMENT 'Primary driver for policy',
ADD COLUMN IF NOT EXISTS driver_type VARCHAR(50) COMMENT 'Type of driver for this policy',
ADD COLUMN IF NOT EXISTS assigned_vehicle_id INT COMMENT 'Primary vehicle assignment',
ADD COLUMN IF NOT EXISTS effective_date DATE COMMENT 'When driver added to policy',
ADD COLUMN IF NOT EXISTS end_date DATE COMMENT 'When driver removed from policy',
ADD INDEX idx_policy_driver_primary (policy_id, is_primary),
ADD INDEX idx_policy_driver_dates (effective_date, end_date),
ADD INDEX idx_policy_driver_status (include_status),
ADD CONSTRAINT fk_map_policy_driver_relationship 
    FOREIGN KEY (relationship_to_insured_id) 
    REFERENCES relationship_to_insured(id),
ADD CONSTRAINT fk_map_policy_driver_vehicle 
    FOREIGN KEY (assigned_vehicle_id) 
    REFERENCES vehicle(id) 
    ON UPDATE CASCADE;
```

### 4. Create Driver Violation Tracking per IP269
```sql
-- Driver Violation table (new per IP269)
CREATE TABLE IF NOT EXISTS driver_violation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    driver_id INT NOT NULL,
    violation_type_id INT NOT NULL,
    violation_date DATE NOT NULL,
    conviction_date DATE,
    description TEXT,
    location VARCHAR(100) COMMENT 'City/State of violation',
    points INT DEFAULT 0 COMMENT 'Points assigned',
    is_accident BOOLEAN DEFAULT FALSE,
    is_at_fault BOOLEAN DEFAULT FALSE,
    status_id INT NOT NULL,
    created_by INT NOT NULL,
    updated_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_driver_violation_driver (driver_id),
    INDEX idx_driver_violation_date (violation_date),
    INDEX idx_driver_violation_type (violation_type_id),
    CONSTRAINT fk_driver_violation_driver 
        FOREIGN KEY (driver_id) 
        REFERENCES driver(id),
    CONSTRAINT fk_driver_violation_type 
        FOREIGN KEY (violation_type_id) 
        REFERENCES violation_type(id),
    CONSTRAINT fk_driver_violation_status 
        FOREIGN KEY (status_id) 
        REFERENCES status(id),
    CONSTRAINT fk_driver_violation_created 
        FOREIGN KEY (created_by) 
        REFERENCES user(id),
    CONSTRAINT fk_driver_violation_updated 
        FOREIGN KEY (updated_by) 
        REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Individual violation tracking per driver';
```

### 5. Reference Data Population
```sql
-- Employment Status values
INSERT INTO employment_status (code, name, status_id) VALUES
('EMPLOYED', 'Employed', 1),
('SELF_EMPLOYED', 'Self Employed', 1),
('UNEMPLOYED', 'Unemployed', 1),
('RETIRED', 'Retired', 1),
('STUDENT', 'Student', 1),
('MILITARY', 'Military', 1),
('HOMEMAKER', 'Homemaker', 1),
('DISABLED', 'Disabled', 1);

-- Relationship to Insured values
INSERT INTO relationship_to_insured (code, name, status_id) VALUES
('SELF', 'Self', 1),
('SPOUSE', 'Spouse', 1),
('CHILD', 'Child', 1),
('PARENT', 'Parent', 1),
('SIBLING', 'Sibling', 1),
('OTHER_RELATIVE', 'Other Relative', 1),
('ROOMMATE', 'Roommate', 1),
('OTHER', 'Other', 1);

-- SR-22 Reason values
INSERT INTO sr22_reason (code, name, status_id) VALUES
('DUI', 'DUI/DWI Conviction', 1),
('RECKLESS', 'Reckless Driving', 1),
('NO_INSURANCE', 'Driving Without Insurance', 1),
('ACCIDENT_UNINSURED', 'At-Fault Accident While Uninsured', 1),
('LICENSE_SUSPENDED', 'License Suspension/Revocation', 1),
('COURT_ORDER', 'Court Ordered', 1),
('OTHER', 'Other Reason', 1);

-- Violation Type values
INSERT INTO violation_type (code, name, severity, points, status_id) VALUES
('SPEEDING_MINOR', 'Speeding 1-15 mph over', 'MINOR', 2, 1),
('SPEEDING_MAJOR', 'Speeding 16+ mph over', 'MAJOR', 4, 1),
('DUI', 'DUI/DWI', 'SEVERE', 8, 1),
('RECKLESS', 'Reckless Driving', 'SEVERE', 6, 1),
('AT_FAULT_ACCIDENT', 'At Fault Accident', 'MAJOR', 4, 1),
('NOT_AT_FAULT_ACCIDENT', 'Not At Fault Accident', 'MINOR', 0, 1),
('FAILURE_TO_STOP', 'Failure to Stop', 'MAJOR', 3, 1),
('IMPROPER_TURN', 'Improper Turn', 'MINOR', 2, 1),
('FOLLOWING_TOO_CLOSE', 'Following Too Closely', 'MINOR', 2, 1);
```

### 6. Business Rule Implementation Support
```sql
-- View to support marital status validation rule
CREATE VIEW v_quote_married_drivers AS
SELECT 
    q.id as quote_id,
    q.quote_number,
    COUNT(DISTINCT CASE 
        WHEN d.marital_status = 'Married' AND mqd.include_status != 'removed' 
        THEN d.id 
    END) as married_driver_count
FROM quote q
LEFT JOIN map_quote_driver mqd ON q.id = mqd.quote_id
LEFT JOIN driver d ON mqd.driver_id = d.id
GROUP BY q.id
HAVING married_driver_count = 1;

-- View for criminal eligibility check integration
CREATE VIEW v_driver_criminal_check AS
SELECT 
    d.id as driver_id,
    d.license_number,
    d.license_state,
    d.date_of_birth,
    mqd.quote_id,
    mqd.include_status,
    -- Placeholder for DCS_CRIMINAL integration results
    NULL as criminal_check_status,
    NULL as criminal_check_date
FROM driver d
JOIN map_quote_driver mqd ON d.id = mqd.driver_id
WHERE mqd.include_status = 'included';
```

## Benefits of This Approach

1. **Consistency with Completed Work**: Aligns with patterns already implemented in Producer Portal
2. **Comprehensive Driver Management**: Supports all requirements from IP269
3. **Flexible Relationship Tracking**: Handles complex driver-insured relationships
4. **Violation History**: Complete tracking of driver violations and points
5. **SR-22 Support**: Built-in support for financial responsibility requirements
6. **Business Rule Ready**: Structure supports validation rules like marital status checks

## Migration Path

1. **Phase 1**: Extend existing driver and map tables
2. **Phase 2**: Create new reference tables (employment_status, relationship_to_insured, etc.)
3. **Phase 3**: Create driver_violation table
4. **Phase 4**: Populate reference data
5. **Phase 5**: Create supporting views
6. **Phase 6**: Update application code to use new fields

## Conclusion

This v3 approach fully aligns with the patterns established in the Producer Portal completed requirements, ensuring consistency across the system while meeting all GR-52 universal entity management requirements for drivers.