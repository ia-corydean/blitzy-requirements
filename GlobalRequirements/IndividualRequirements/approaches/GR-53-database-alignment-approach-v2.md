# GR-53 DCS Integration Architecture - Database Alignment Approach V2

## Overview
This approach focuses on using the configuration table with configuration_type pattern for DCS integration settings, as suggested in the feedback. It also addresses storing integration logs with proper entity references (policy_id, quote_id, driver_id) instead of program_id.

## Current Database Reality

### Configuration Tables
1. **configuration** - Very minimal structure
   - id, configuration_type_id, status_id
   - Standard audit fields
   - NO key/value columns visible

2. **configuration_type** - Configuration categories
   - Standard type table pattern

3. **map_integration_configuration** - Links integrations to configurations
   - Maps program_id, integration_type_id to configuration_id

### Integration Tables
1. **integration** - Core integration records
2. **integration_type** - Integration categories

## Key Issues with Current Structure

The configuration table appears to be missing key/value storage columns. This needs to be addressed for any meaningful configuration storage.

## Recommended Approach

### 1. Extend Configuration Table
```sql
-- Add missing columns to configuration table
ALTER TABLE configuration
ADD COLUMN IF NOT EXISTS config_key VARCHAR(100) NOT NULL AFTER configuration_type_id,
ADD COLUMN IF NOT EXISTS config_value TEXT,
ADD COLUMN IF NOT EXISTS config_metadata JSON COMMENT 'Additional configuration metadata',
ADD COLUMN IF NOT EXISTS scope VARCHAR(50) DEFAULT 'SYSTEM' COMMENT 'SYSTEM, PROGRAM, INTEGRATION',
ADD COLUMN IF NOT EXISTS scope_id INT COMMENT 'ID of scoped entity (program_id, integration_id, etc.)',
ADD UNIQUE KEY uk_config_key (scope, scope_id, config_key),
ADD INDEX idx_config_scope (scope, scope_id);
```

### 2. Configuration Types for DCS
```sql
-- DCS-specific configuration types
INSERT INTO configuration_type (code, name, description, is_default, status_id) VALUES
('DCS_CONNECTION', 'DCS Connection Settings', 'API endpoints and authentication', FALSE, 1),
('DCS_CREDENTIALS', 'DCS Credentials', 'Encrypted credentials for DCS API', FALSE, 1),
('DCS_LIMITS', 'DCS Rate Limits', 'API rate limiting configuration', FALSE, 1),
('DCS_MAPPING', 'DCS Field Mapping', 'Map DCS fields to internal fields', FALSE, 1),
('DCS_RETRY', 'DCS Retry Policy', 'Retry and circuit breaker settings', FALSE, 1);
```

### 3. Integration Log with Entity References
```sql
-- Create integration log with proper entity references
CREATE TABLE IF NOT EXISTS integration_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    integration_id INT NOT NULL,
    
    -- Entity references (not program_id)
    policy_id INT COMMENT 'Related policy if applicable',
    quote_id INT COMMENT 'Related quote if applicable',
    driver_id INT COMMENT 'Related driver if applicable',
    vehicle_id INT COMMENT 'Related vehicle if applicable',
    
    -- Request/Response details
    request_type VARCHAR(50) COMMENT 'API method called',
    request_url VARCHAR(500) COMMENT 'Full request URL',
    request_data JSON COMMENT 'Request payload',
    response_data JSON COMMENT 'Response payload',
    response_code INT COMMENT 'HTTP response code',
    response_time_ms INT COMMENT 'Response time in milliseconds',
    
    -- Error handling
    is_success BOOLEAN DEFAULT TRUE,
    error_message TEXT COMMENT 'Error details if failed',
    retry_count INT DEFAULT 0,
    
    -- Tracking
    correlation_id VARCHAR(100) COMMENT 'For tracking related requests',
    external_reference VARCHAR(100) COMMENT 'DCS transaction ID',
    
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_integration_log_integration (integration_id),
    INDEX idx_integration_log_policy (policy_id),
    INDEX idx_integration_log_quote (quote_id),
    INDEX idx_integration_log_driver (driver_id),
    INDEX idx_integration_log_correlation (correlation_id),
    INDEX idx_integration_log_created (created_at),
    
    FOREIGN KEY (integration_id) REFERENCES integration(id),
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (quote_id) REFERENCES quote(id),
    FOREIGN KEY (driver_id) REFERENCES driver(id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(id),
    FOREIGN KEY (created_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Logs all DCS API interactions with entity references';
```

### 4. DCS Configuration Storage Pattern
```sql
-- System-level DCS defaults
INSERT INTO configuration (
    configuration_type_id,
    config_key,
    config_value,
    scope,
    scope_id,
    status_id,
    created_by
) VALUES
-- Connection settings
(
    (SELECT id FROM configuration_type WHERE code = 'DCS_CONNECTION'),
    'base_url',
    'https://ws.dcsinfosys.com:442',
    'SYSTEM',
    NULL,
    1,
    1
),
(
    (SELECT id FROM configuration_type WHERE code = 'DCS_CONNECTION'),
    'timeout_seconds',
    '30',
    'SYSTEM',
    NULL,
    1,
    1
),
-- Rate limits
(
    (SELECT id FROM configuration_type WHERE code = 'DCS_LIMITS'),
    'requests_per_minute',
    '100',
    'SYSTEM',
    NULL,
    1,
    1
),
(
    (SELECT id FROM configuration_type WHERE code = 'DCS_LIMITS'),
    'daily_limit',
    '10000',
    'SYSTEM',
    NULL,
    1,
    1
),
-- Retry policy
(
    (SELECT id FROM configuration_type WHERE code = 'DCS_RETRY'),
    'max_retries',
    '3',
    'SYSTEM',
    NULL,
    1,
    1
),
(
    (SELECT id FROM configuration_type WHERE code = 'DCS_RETRY'),
    'retry_delay_ms',
    '1000',
    'SYSTEM',
    NULL,
    1,
    1
);

-- Program-specific overrides
INSERT INTO configuration (
    configuration_type_id,
    config_key,
    config_value,
    scope,
    scope_id,
    status_id,
    created_by
) VALUES
(
    (SELECT id FROM configuration_type WHERE code = 'DCS_CREDENTIALS'),
    'account_number',
    'PROG1_12345', -- Different per program
    'PROGRAM',
    1, -- program_id
    1,
    1
),
(
    (SELECT id FROM configuration_type WHERE code = 'DCS_CREDENTIALS'),
    'department_id',
    '4',
    'PROGRAM',
    1,
    1,
    1
),
(
    (SELECT id FROM configuration_type WHERE code = 'DCS_LIMITS'),
    'requests_per_minute',
    '50', -- Lower limit for this program
    'PROGRAM',
    1,
    1,
    1
);
```

### 5. Integration Type Setup
```sql
-- DCS integration types
INSERT INTO integration_type (code, name, description, is_default, status_id) VALUES
('DCS_DRIVER_API', 'DCS Driver Verification', 'Driver lookup and verification services', FALSE, 1),
('DCS_VEHICLE_API', 'DCS Vehicle Services', 'Vehicle lookup and VIN decoding', FALSE, 1),
('DCS_CRIMINAL_API', 'DCS Criminal Check', 'Criminal background verification', FALSE, 1);

-- DCS integrations
INSERT INTO integration (
    integration_type_id,
    status_id,
    created_by
) VALUES
(
    (SELECT id FROM integration_type WHERE code = 'DCS_DRIVER_API'),
    1,
    1
),
(
    (SELECT id FROM integration_type WHERE code = 'DCS_VEHICLE_API'),
    1,
    1
),
(
    (SELECT id FROM integration_type WHERE code = 'DCS_CRIMINAL_API'),
    1,
    1
);
```

### 6. Map Configuration to Integration
```sql
-- Link DCS configurations to integrations for a program
INSERT INTO map_integration_configuration (
    program_id,
    integration_type_id,
    configuration_id,
    is_active,
    created_by,
    created_at
)
SELECT 
    1, -- program_id
    it.id,
    c.id,
    TRUE,
    1,
    NOW()
FROM integration_type it
CROSS JOIN configuration c
WHERE it.code LIKE 'DCS_%'
AND c.configuration_type_id IN (
    SELECT id FROM configuration_type 
    WHERE code IN ('DCS_CONNECTION', 'DCS_CREDENTIALS', 'DCS_LIMITS', 'DCS_RETRY')
)
AND (c.scope = 'SYSTEM' OR (c.scope = 'PROGRAM' AND c.scope_id = 1));
```

### 7. Configuration Access Pattern
```sql
-- View to get effective configuration for a program/integration
CREATE VIEW v_effective_dcs_configuration AS
SELECT 
    p.id as program_id,
    it.code as integration_type,
    ct.code as config_type,
    c.config_key,
    -- Program config overrides system config
    COALESCE(
        MAX(CASE WHEN c.scope = 'PROGRAM' THEN c.config_value END),
        MAX(CASE WHEN c.scope = 'SYSTEM' THEN c.config_value END)
    ) as config_value
FROM program p
CROSS JOIN integration_type it
CROSS JOIN configuration_type ct
LEFT JOIN configuration c ON (
    c.configuration_type_id = ct.id
    AND (
        (c.scope = 'SYSTEM' AND c.scope_id IS NULL)
        OR (c.scope = 'PROGRAM' AND c.scope_id = p.id)
    )
)
WHERE it.code LIKE 'DCS_%'
AND ct.code LIKE 'DCS_%'
GROUP BY p.id, it.code, ct.code, c.config_key;

-- Usage: Get all DCS settings for program 1
SELECT * FROM v_effective_dcs_configuration 
WHERE program_id = 1 
AND integration_type = 'DCS_DRIVER_API'
ORDER BY config_type, config_key;
```

### 8. Secure Credential Storage
```sql
-- Store encrypted credentials separately
CREATE TABLE IF NOT EXISTS integration_credential (
    id INT AUTO_INCREMENT PRIMARY KEY,
    integration_id INT NOT NULL,
    environment VARCHAR(20) NOT NULL DEFAULT 'PRODUCTION' COMMENT 'PRODUCTION, STAGING, DEVELOPMENT',
    credential_key VARCHAR(50) NOT NULL COMMENT 'username, password, api_key',
    encrypted_value VARBINARY(500) NOT NULL COMMENT 'AES encrypted value',
    encryption_key_id VARCHAR(100) COMMENT 'Reference to key management system',
    expires_at DATETIME,
    last_rotated_at DATETIME,
    status_id INT NOT NULL,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_integration_cred (integration_id, environment, credential_key),
    INDEX idx_cred_environment (environment),
    INDEX idx_cred_expires (expires_at),
    
    FOREIGN KEY (integration_id) REFERENCES integration(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Encrypted storage for integration credentials';

-- Example: Store DCS credentials
INSERT INTO integration_credential (
    integration_id,
    environment,
    credential_key,
    encrypted_value,
    encryption_key_id,
    status_id,
    created_by
) VALUES
(
    (SELECT i.id FROM integration i 
     JOIN integration_type it ON i.integration_type_id = it.id 
     WHERE it.code = 'DCS_DRIVER_API'),
    'PRODUCTION',
    'username',
    AES_ENCRYPT('prod_user', 'temp_key'), -- Use proper KMS in production
    'kms/dcs/prod/v1',
    1,
    1
),
(
    (SELECT i.id FROM integration i 
     JOIN integration_type it ON i.integration_type_id = it.id 
     WHERE it.code = 'DCS_DRIVER_API'),
    'PRODUCTION',
    'password',
    AES_ENCRYPT('prod_pass', 'temp_key'),
    'kms/dcs/prod/v1',
    1,
    1
);
```

## Key Improvements in V2

1. **Configuration Table Enhancement** - Added key/value storage
2. **Entity-Based Logging** - Uses policy_id, quote_id, driver_id instead of program_id
3. **Configuration Type Pattern** - Leverages existing configuration_type table
4. **Secure Credential Storage** - Separate encrypted credential table
5. **Flexible Scoping** - System vs Program configuration hierarchy
6. **Proper Foreign Keys** - Links to actual entity tables

## Benefits of This Approach

1. **Uses Existing Patterns** - Works with configuration/configuration_type structure
2. **Entity-Centric** - Logs reference actual business entities
3. **Secure** - Credentials stored encrypted and separate
4. **Flexible** - Easy to add new configuration types
5. **Auditable** - Full logging of all API interactions

## Implementation Notes

1. **Configuration Access**
   - System defaults apply to all
   - Program overrides are optional
   - Easy to extend to other scopes

2. **Integration Logging**
   - Every API call logged
   - Links to relevant entities
   - Correlation IDs for workflows

3. **Credential Management**
   - Never store plain text
   - Use proper encryption
   - Support key rotation

4. **Performance**
   - Indexes on all foreign keys
   - Configuration cached in app
   - Logs partitioned by date

## Summary

This V2 approach uses the configuration table with configuration_type pattern as suggested, stores integration logs with proper entity references (not program_id), and provides a secure, flexible way to manage DCS integration settings. The solution works within the existing database structure while adding only the necessary enhancements.