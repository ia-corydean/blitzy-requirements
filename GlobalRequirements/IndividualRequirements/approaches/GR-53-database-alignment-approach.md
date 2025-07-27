# GR-53 DCS Integration Architecture - Database Alignment Approach
- requery the database to see what needs to be added here.
  - I feel like 

## Overview
This approach document outlines how the current database structure can support GR-53 (DCS Integration Architecture) requirements using existing integration tables.

## Current State Analysis

### Existing Integration Tables in Database
Based on Docker container analysis:

1. **integration** - Core integration records
   - id, integration_type_id, status_id
   - Standard audit fields (created_by, updated_by, created_at, updated_at)
   - **MISSING**: Fields for API endpoints, authentication, metadata

2. **integration_type** - Integration categories
   - id, code, name, description, is_default, status_id
   - Standard type table pattern
   - Can store DCS integration types

3. **map_integration_configuration** - Links integrations to configurations
   - id, program_id, integration_type_id, configuration_id, is_active
   - Supports program-specific configurations
   - Already has the right relationship structure

4. **configuration** - Exists (need to verify structure)
   - Likely stores configuration key-value pairs
   - Should support API credentials and settings

## Key Requirements from GR-53

### DCS API Types Needed:
1. DCS_HOUSEHOLD_DRIVERS (v2.7)
2. DCS_HOUSEHOLD_VEHICLES (v2.3)
3. DCS_CRIMINAL (v1.0)

### Configuration Requirements:
- API endpoints (environment-specific)
- Authentication credentials (account/user/password)
- Program-specific settings
- Request/response formats (XML)

### Security Requirements:
- Vault-based credential storage
- Component-based permissions
- Audit logging

## Proposed Database Updates

### 1. Enhance Integration Table
```sql
ALTER TABLE integration
ADD COLUMN code VARCHAR(50) UNIQUE COMMENT 'Unique integration identifier',
ADD COLUMN name VARCHAR(100) COMMENT 'Display name',
ADD COLUMN endpoint_url VARCHAR(500) COMMENT 'API endpoint URL',
ADD COLUMN auth_type VARCHAR(50) DEFAULT 'BASIC' COMMENT 'Authentication type',
ADD COLUMN request_format VARCHAR(20) DEFAULT 'XML' COMMENT 'Request format',
ADD COLUMN response_format VARCHAR(20) DEFAULT 'XML' COMMENT 'Response format',
ADD COLUMN version VARCHAR(20) COMMENT 'API version',
ADD COLUMN metadata JSON COMMENT 'Additional integration metadata',
ADD INDEX idx_code (code),
ADD INDEX idx_integration_type (integration_type_id);
```

### 2. Create Integration Log Table
```sql
CREATE TABLE integration_log (
    id INT PRIMARY KEY AUTO_INCREMENT,
    integration_id INT NOT NULL,
    program_id INT,
    request_type VARCHAR(50) COMMENT 'API method called',
    request_data JSON COMMENT 'Request payload',
    response_data JSON COMMENT 'Response payload',
    response_code INT COMMENT 'HTTP response code',
    response_time_ms INT COMMENT 'Response time in milliseconds',
    error_message TEXT COMMENT 'Error details if failed',
    correlation_id VARCHAR(100) COMMENT 'For tracking related requests',
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_integration (integration_id),
    INDEX idx_program (program_id),
    INDEX idx_correlation (correlation_id),
    INDEX idx_created (created_at),
    
    FOREIGN KEY (integration_id) REFERENCES integration(id),
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (created_by) REFERENCES user(id)
);
```
- we should add policy_id, quote_id, driver_id and remove program_id.

### 3. Create Integration Credential Table
```sql
CREATE TABLE integration_credential (
    id INT PRIMARY KEY AUTO_INCREMENT,
    integration_id INT NOT NULL,
    program_id INT COMMENT 'Null for system-wide credentials',
    environment VARCHAR(20) NOT NULL COMMENT 'DEV, UAT, PROD',
    credential_type VARCHAR(50) NOT NULL COMMENT 'account, user, password, api_key',
    credential_value VARCHAR(500) COMMENT 'Encrypted value',
    vault_path VARCHAR(200) COMMENT 'HashiCorp Vault path',
    expires_at TIMESTAMP NULL,
    status_id INT,
    created_by INT,
    updated_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_credential (integration_id, program_id, environment, credential_type),
    INDEX idx_program (program_id),
    INDEX idx_environment (environment),
    
    FOREIGN KEY (integration_id) REFERENCES integration(id),
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```
- could these not be sotred in the configuration table with configuration_type?
- map_entity_configuration

### 4. Update Configuration Table (if needed)
```sql
-- Verify existing structure first
-- If missing key fields, add:
ALTER TABLE configuration
ADD COLUMN scope VARCHAR(50) DEFAULT 'SYSTEM' COMMENT 'SYSTEM, PROGRAM, ENTITY',
ADD COLUMN scope_id INT COMMENT 'ID of scoped entity',
ADD COLUMN config_key VARCHAR(100) NOT NULL,
ADD COLUMN config_value TEXT,
ADD COLUMN config_type VARCHAR(50) DEFAULT 'STRING' COMMENT 'STRING, JSON, BOOLEAN, INTEGER',
ADD UNIQUE KEY uk_config (scope, scope_id, config_key);
```

### 5. Standard Integration Type Data
```sql
-- Insert DCS integration types
INSERT INTO integration_type (code, name, description, status_id) VALUES
('DCS_HOUSEHOLD_DRIVERS', 'DCS Household Drivers API', 'Driver verification and household discovery', 1),
('DCS_HOUSEHOLD_VEHICLES', 'DCS Household Vehicles API', 'Vehicle verification and VIN decoding', 1),
('DCS_CRIMINAL', 'DCS Criminal Background API', 'Criminal history and background checks', 1);

-- Insert DCS integrations
INSERT INTO integration (integration_type_id, code, name, endpoint_url, version, status_id)
SELECT it.id, 'DCS_DRIVERS_V27', 'DCS Drivers API v2.7', 
       'https://ws.dcsinfosys.com:442/apidevV2.7/DcsSearchApi/HouseholdDrivers', 'v2.7', 1
FROM integration_type it WHERE it.code = 'DCS_HOUSEHOLD_DRIVERS';

INSERT INTO integration (integration_type_id, code, name, endpoint_url, version, status_id)
SELECT it.id, 'DCS_VEHICLES_V23', 'DCS Vehicles API v2.3',
       'https://ws.dcsinfosys.com:442/apidevV2.3/DcsSearchApi/HouseholdVehicles', 'v2.3', 1
FROM integration_type it WHERE it.code = 'DCS_HOUSEHOLD_VEHICLES';

INSERT INTO integration (integration_type_id, code, name, endpoint_url, version, status_id)
SELECT it.id, 'DCS_CRIMINAL_V10', 'DCS Criminal API v1.0',
       'https://ws.dcsinfosys.com:442/apidevV2.8/DcsSearchApi/Criminal', 'v1.0', 1
FROM integration_type it WHERE it.code = 'DCS_CRIMINAL';
```

## How This Supports DCS Integration

### 1. API Configuration
- `integration` table stores endpoint URLs and API metadata
- `integration_credential` manages environment-specific credentials
- `configuration` table handles additional settings

### 2. Program-Specific Setup
- `map_integration_configuration` links programs to their integrations
- Credentials can be program-specific or system-wide
- Configuration hierarchy supported through scope fields

### 3. Security & Audit
- Credentials reference Vault paths for secure storage
- `integration_log` provides complete audit trail
- User permissions checked through existing role system

### 4. Extensibility
- JSON metadata fields for API-specific data
- Configuration table supports any key-value pairs
- Easy to add new integration types

## Benefits of This Approach

1. **Reuses Existing Tables**: Minimal new tables needed
2. **Flexible Configuration**: Supports all DCS requirements
3. **Secure**: Credentials in Vault, audit logging
4. **Scalable**: Can support other integrations beyond DCS
5. **Program-Aware**: Multi-program support built-in

## Implementation Notes

1. **Credential Encryption**: credential_value should be encrypted at rest
2. **Vault Integration**: vault_path points to HashiCorp Vault secrets
3. **XML Handling**: request_data and response_data in JSON fields can store XML as strings
4. **Performance**: Indexes on frequently queried fields

## Next Steps

1. Review and approve approach
2. Create database migrations
3. Implement credential management service
4. Build DCS integration service layer
5. Add integration logging middleware