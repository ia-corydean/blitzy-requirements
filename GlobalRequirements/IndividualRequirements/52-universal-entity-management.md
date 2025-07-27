# 52.0 Universal Entity Management Architecture

## Overview
Unified system for managing all external entities (APIs, attorneys, body shops, vendors) through a consistent pattern that requires zero code changes for new entity types.

## Core Components

### Entity Management System
- **entity_category**: Categorizes entity types (INTEGRATION, PARTNER, VENDOR, SYSTEM)
- **entity_type**: Defines schemas and validation rules with JSON metadata
- **entity**: Stores all external entity instances with flexible metadata

### Benefits
- 90% faster development for new external entity types
- Zero code changes to add new entity types
- Consistent CRUD operations across all entities
- Automatic UI support through metadata schemas

## DCS API Integration Examples

### DCS Entity Types Configuration
```sql
-- Driver verification and household lookup
INSERT INTO entity_type (code, name, category_id, metadata_schema) VALUES 
('DCS_HOUSEHOLD_DRIVERS', 'DCS Household Drivers API', 1, 
'{
  "type": "object",
  "properties": {
    "provider": {"type": "string", "const": "Data Capture Solutions"},
    "base_url": {"type": "string", "const": "https://ws.dcsinfosys.com:442"},
    "api_version": {"type": "string", "const": "v2.7"},
    "endpoint": {"type": "string", "const": "/apidevV2.7/DcsSearchApi/HouseholdDrivers"},
    "auth_type": {"type": "string", "const": "basic"},
    "capabilities": {
      "type": "array",
      "items": {"type": "string"},
      "const": ["driver_verification", "household_lookup", "criminal_history", "alias_search"]
    },
    "data_retention_days": {"type": "number", "const": 2555}
  },
  "required": ["provider", "base_url", "api_version", "endpoint", "auth_type"]
}');

-- Vehicle data and VIN decoding
INSERT INTO entity_type (code, name, category_id, metadata_schema) VALUES 
('DCS_HOUSEHOLD_VEHICLES', 'DCS Household Vehicles API', 1, 
'{
  "type": "object",
  "properties": {
    "provider": {"type": "string", "const": "Data Capture Solutions"},
    "base_url": {"type": "string", "const": "https://ws.dcsinfosys.com:442"},
    "api_version": {"type": "string", "const": "v2.3"},
    "endpoint": {"type": "string", "const": "/apidevV2.3/DcsSearchApi/HouseholdVehicles"},
    "auth_type": {"type": "string", "const": "basic"},
    "capabilities": {
      "type": "array",
      "items": {"type": "string"},
      "const": ["vehicle_lookup", "vin_decoding", "registration_data", "household_vehicles"]
    },
    "data_retention_days": {"type": "number", "const": 2555}
  },
  "required": ["provider", "base_url", "api_version", "endpoint", "auth_type"]
}');

-- Criminal background checks
INSERT INTO entity_type (code, name, category_id, metadata_schema) VALUES 
('DCS_CRIMINAL', 'DCS Criminal Background API', 1, 
'{
  "type": "object",
  "properties": {
    "provider": {"type": "string", "const": "Data Capture Solutions"},
    "base_url": {"type": "string", "const": "https://ws.dcsinfosys.com:442"},
    "api_version": {"type": "string", "const": "v1.0"},
    "endpoint": {"type": "string", "const": "/apidevV2.8/DcsSearchApi/Criminal"},
    "auth_type": {"type": "string", "const": "basic"},
    "capabilities": {
      "type": "array",
      "items": {"type": "string"},
      "const": ["criminal_history", "background_check", "offense_details", "court_records"]
    },
    "data_retention_days": {"type": "number", "const": 2555}
  },
  "required": ["provider", "base_url", "api_version", "endpoint", "auth_type"]
}');
```

## DCS Communication Tracking System

### Polymorphic Communication for DCS APIs
- **source_type/source_id**: Can be system, user, or entity
- **target_type/target_id**: Always 'entity' for DCS API calls
- **correlation_id**: Links related DCS API calls in workflows
- **Ultra-simple design**: Only essential fields included

### DCS Communication Flow Examples
```sql
-- Driver verification communication
INSERT INTO communication (
    communication_type_id, source_type, source_id, 
    target_type, target_id, channel_id, direction,
    request_data, correlation_id, status_id
) VALUES (
    1, 'system', 1, 'entity', 5, 1, 'outbound',
    '{"license_number": "TX12345678", "state": "TX", "dob": "1975-02-25"}',
    'quote-123-driver-verification', 1
);

-- Vehicle lookup communication (same correlation ID)
INSERT INTO communication (
    communication_type_id, source_type, source_id, 
    target_type, target_id, channel_id, direction,
    request_data, correlation_id, status_id
) VALUES (
    2, 'system', 1, 'entity', 6, 1, 'outbound',
    '{"address": "123 Main St", "city": "Dallas", "state": "TX", "zip": "75001"}',
    'quote-123-driver-verification', 1
);

-- Criminal check communication (same correlation ID)
INSERT INTO communication (
    communication_type_id, source_type, source_id, 
    target_type, target_id, channel_id, direction,
    request_data, correlation_id, status_id
) VALUES (
    3, 'system', 1, 'entity', 7, 1, 'outbound',
    '{"first_name": "John", "last_name": "Smith", "dob": "1975-02-25", "state": "TX"}',
    'quote-123-driver-verification', 1
);
```

### DCS Reference Tables
```sql
-- Communication types for DCS APIs
INSERT INTO communication_type (code, name, description) VALUES
('DCS_DRIVER_LOOKUP', 'DCS Driver Lookup', 'Driver verification and household search'),
('DCS_VEHICLE_LOOKUP', 'DCS Vehicle Lookup', 'Vehicle data and VIN validation'),
('DCS_CRIMINAL_CHECK', 'DCS Criminal Check', 'Criminal background verification'),
('DCS_ALIAS_SEARCH', 'DCS Alias Search', 'Criminal search using alias names');

-- Communication channels
INSERT INTO communication_channel (code, name, description) VALUES
('DCS_API', 'DCS REST API', 'HTTPS POST requests to DCS endpoints'),
('DCS_BATCH', 'DCS Batch File', 'Bulk processing via file transfer'),
('DCS_WEBHOOK', 'DCS Webhook', 'Asynchronous notifications from DCS');

-- Communication statuses
INSERT INTO communication_status (code, name, description) VALUES
('DCS_PENDING', 'Pending', 'Request sent, awaiting response'),
('DCS_SUCCESS', 'Success', 'Request completed successfully'),
('DCS_FAILED', 'Failed', 'Request failed with error'),
('DCS_TIMEOUT', 'Timeout', 'Request timed out'),
('DCS_RETRY', 'Retrying', 'Request being retried after failure');
```

## DCS Configuration Management

### Three-Level Hierarchy for DCS APIs
1. **System Level**: Default DCS configuration for all programs
2. **Program Level**: Program-specific DCS overrides (different environments)
3. **Entity Level**: Entity-specific DCS settings (failover endpoints)

### DCS Configuration Resolution Order
Entity → Program → System (most specific wins)

### DCS Configuration Types
```sql
-- System-level DCS configuration
INSERT INTO configuration (scope, scope_id, type, key, value) VALUES
('system', 1, 'DCS_SETTINGS', 'default_timeout_ms', '30000'),
('system', 1, 'DCS_SETTINGS', 'default_retry_attempts', '3'),
('system', 1, 'DCS_SETTINGS', 'circuit_breaker_threshold', '5'),
('system', 1, 'DCS_SETTINGS', 'circuit_breaker_timeout_ms', '60000'),
('system', 1, 'DCS_SETTINGS', 'base_url', 'https://ws.dcsinfosys.com:442'),
('system', 1, 'DCS_SETTINGS', 'rate_limit_per_minute', '100');

-- Program-level DCS configuration (Production)
INSERT INTO configuration (scope, scope_id, type, key, value) VALUES
('program', 1, 'DCS_SETTINGS', 'account_number', 'PROD12345'),
('program', 1, 'DCS_SETTINGS', 'department_id', '4'),
('program', 1, 'DCS_SETTINGS', 'user_id', 'PROD_USER'),
('program', 1, 'DCS_SETTINGS', 'user_name', 'Production Portal'),
('program', 1, 'DCS_SETTINGS', 'environment', 'production');

-- Program-level DCS configuration (Staging)
INSERT INTO configuration (scope, scope_id, type, key, value) VALUES
('program', 2, 'DCS_SETTINGS', 'account_number', 'TEST12345'),
('program', 2, 'DCS_SETTINGS', 'department_id', '999'),
('program', 2, 'DCS_SETTINGS', 'user_id', 'TEST_USER'),
('program', 2, 'DCS_SETTINGS', 'user_name', 'Staging Portal'),
('program', 2, 'DCS_SETTINGS', 'environment', 'staging'),
('program', 2, 'DCS_SETTINGS', 'rate_limit_per_minute', '50');

-- Entity-level DCS configuration (specific API optimizations)
INSERT INTO configuration (scope, scope_id, type, key, value) VALUES
('entity', 5, 'DCS_SETTINGS', 'timeout_ms', '45000'),  -- Criminal API needs more time
('entity', 5, 'DCS_SETTINGS', 'retry_attempts', '2'),  -- Criminal API fewer retries
('entity', 6, 'DCS_SETTINGS', 'cache_ttl_seconds', '3600'),  -- Vehicle data caches longer
('entity', 7, 'DCS_SETTINGS', 'priority', 'high');  -- Driver API highest priority
```

### DCS Security Configuration
```sql
-- Encrypted credential storage
INSERT INTO configuration (scope, scope_id, type, key, value) VALUES
('program', 1, 'DCS_AUTH', 'credentials_vault_path', 'secret/dcs/production'),
('program', 1, 'DCS_AUTH', 'credential_rotation_days', '90'),
('program', 1, 'DCS_AUTH', 'audit_retention_days', '2555'),  -- 7 years
('program', 2, 'DCS_AUTH', 'credentials_vault_path', 'secret/dcs/staging');
```

## Component-Based Security for DCS Universal Entities

### DCS System Components
```sql
-- Backend components for DCS APIs
INSERT INTO system_component (namespace, api_prefix, description) VALUES
('App\\Services\\Dcs\\Driver', '/api/v1/dcs/drivers', 'DCS driver verification services'),
('App\\Services\\Dcs\\Vehicle', '/api/v1/dcs/vehicles', 'DCS vehicle lookup services'),
('App\\Services\\Dcs\\Criminal', '/api/v1/dcs/criminal', 'DCS criminal background services'),
('App\\Services\\Dcs\\Workflow', '/api/v1/dcs/workflows', 'DCS multi-API workflow management');

-- Frontend components for DCS integrations
INSERT INTO system_component (namespace, api_prefix, description) VALUES
('dcs-driver-verification', null, 'DCS driver verification UI components'),
('dcs-vehicle-lookup', null, 'DCS vehicle search UI components'),
('dcs-criminal-check', null, 'DCS background check UI components'),
('dcs-workflow-manager', null, 'DCS workflow orchestration UI');
```

### DCS Permission Model
```sql
-- DCS-specific permission codes
INSERT INTO permission_code (code, description, component_namespace) VALUES
('dcs_driver_read', 'View DCS driver verification results', 'App\\Services\\Dcs\\Driver'),
('dcs_driver_request', 'Request DCS driver verification', 'App\\Services\\Dcs\\Driver'),
('dcs_vehicle_read', 'View DCS vehicle lookup results', 'App\\Services\\Dcs\\Vehicle'),
('dcs_vehicle_request', 'Request DCS vehicle lookup', 'App\\Services\\Dcs\\Vehicle'),
('dcs_criminal_read', 'View DCS criminal check results', 'App\\Services\\Dcs\\Criminal'),
('dcs_criminal_request', 'Request DCS criminal background check', 'App\\Services\\Dcs\\Criminal'),
('dcs_workflow_manage', 'Manage DCS multi-API workflows', 'App\\Services\\Dcs\\Workflow'),
('dcs_config_admin', 'Administer DCS API configurations', 'App\\Services\\Dcs\\Config');

-- Security groups for DCS access
INSERT INTO security_group (code, name, description) VALUES
('dcs_basic_users', 'DCS Basic Users', 'Basic access to DCS driver and vehicle lookups'),
('dcs_premium_users', 'DCS Premium Users', 'Full access including criminal background checks'),
('dcs_administrators', 'DCS Administrators', 'Full DCS access including configuration management');
```

## Integration with Other Global Requirements
- **GR 48 (External Integrations)**: All DCS API entities managed through universal system
- **GR 44 (Communication)**: Universal communication tracking for all DCS APIs
- **GR 36 (Authentication)**: Component-based security for DCS operations
- **GR 33 (Data Services)**: Optimized DCS queries with proper indexing and caching

## Implementation Standards
1. All external entities MUST use entity/entity_type pattern
2. Entity types MUST define JSON schemas for metadata validation
3. UI components MUST auto-generate from entity type definitions
4. Communication with entities MUST use polymorphic patterns
5. DCS integrations MUST follow insurance compliance requirements

## Performance Requirements
- Entity queries: < 500ms for 10,000+ entities
- Communication queries: < 200ms with correlation ID indexing
- Configuration resolution: < 100ms across hierarchy
- Metadata validation: < 50ms per entity type
- DCS API calls: Driver < 5s, Vehicle < 3s, Criminal < 10s
- Circuit breaker: 5 failures trigger protection, 60s timeout

## Compliance Requirements
- Data retention: 7 years for insurance regulatory compliance
- Audit logging: All DCS API interactions with PII masking
- Encryption: All credentials and sensitive data at rest
- Access control: Component-based permissions with role separation
- Privacy: Support for consumer data rights and deletion requests

## V4 Shared Entity Model

### Core Shared Entities
The system implements a shared entity model where driver, vehicle, and insured entities are used across both quotes and policies, eliminating the need for separate quote_driver/policy_driver tables.

### Shared Entity Tables
```sql
-- Shared driver entity (replaces quote_driver and policy_driver)
CREATE TABLE driver (
    driver_id INT AUTO_INCREMENT PRIMARY KEY,
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
);

-- Shared vehicle entity (replaces quote_vehicle and policy_vehicle)
CREATE TABLE vehicle (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    vin VARCHAR(17) NOT NULL,
    year INT NOT NULL,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    trim VARCHAR(50),
    vehicle_type VARCHAR(30),
    usage_type VARCHAR(30),
    annual_mileage INT,
    ownership_type VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    metadata JSON,
    UNIQUE KEY uk_vin (vin),
    INDEX idx_year_make_model (year, make, model)
);

-- Shared insured entity (V4: renamed from 'customer')
CREATE TABLE insured (
    insured_id INT AUTO_INCREMENT PRIMARY KEY,
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
);
```

### Map Table Relationships
```sql
-- Quote to driver mapping
CREATE TABLE quote_driver_map (
    quote_id INT NOT NULL,
    driver_id INT NOT NULL,
    is_primary_driver BOOLEAN DEFAULT FALSE,
    driver_type VARCHAR(20), -- PRIMARY, ADDITIONAL, EXCLUDED
    assigned_vehicle_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (quote_id, driver_id),
    FOREIGN KEY (quote_id) REFERENCES quote(quote_id),
    FOREIGN KEY (driver_id) REFERENCES driver(driver_id),
    FOREIGN KEY (assigned_vehicle_id) REFERENCES vehicle(vehicle_id),
    INDEX idx_driver (driver_id)
);

-- Quote to vehicle mapping
CREATE TABLE quote_vehicle_map (
    quote_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    coverage_type VARCHAR(30),
    deductible_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (quote_id, vehicle_id),
    FOREIGN KEY (quote_id) REFERENCES quote(quote_id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id),
    INDEX idx_vehicle (vehicle_id)
);

-- Policy to driver mapping (shares same driver records)
CREATE TABLE policy_driver_map (
    policy_id INT NOT NULL,
    driver_id INT NOT NULL,
    is_primary_driver BOOLEAN DEFAULT FALSE,
    driver_type VARCHAR(20),
    assigned_vehicle_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (policy_id, driver_id),
    FOREIGN KEY (policy_id) REFERENCES policy(policy_id),
    FOREIGN KEY (driver_id) REFERENCES driver(driver_id),
    FOREIGN KEY (assigned_vehicle_id) REFERENCES vehicle(vehicle_id),
    INDEX idx_driver (driver_id)
);

-- Policy to vehicle mapping (shares same vehicle records)
CREATE TABLE policy_vehicle_map (
    policy_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    coverage_type VARCHAR(30),
    deductible_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (policy_id, vehicle_id),
    FOREIGN KEY (policy_id) REFERENCES policy(policy_id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id),
    INDEX idx_vehicle (vehicle_id)
);
```

### Entity Service Implementation
```php
namespace App\Services\Entity;

class SharedEntityService
{
    /**
     * Create or update a driver entity
     */
    public function upsertDriver(array $driverData): Driver
    {
        // Check if driver already exists
        $existingDriver = Driver::where('license_number', $driverData['license_number'])
            ->where('license_state', $driverData['license_state'])
            ->first();
            
        if ($existingDriver) {
            // Update existing driver
            $existingDriver->update($driverData);
            return $existingDriver;
        }
        
        // Create new driver
        return Driver::create($driverData);
    }
    
    /**
     * Attach driver to quote
     */
    public function attachDriverToQuote(int $quoteId, int $driverId, array $mappingData): void
    {
        QuoteDriverMap::updateOrCreate(
            [
                'quote_id' => $quoteId,
                'driver_id' => $driverId,
            ],
            $mappingData
        );
    }
    
    /**
     * Copy quote entities to policy
     */
    public function copyQuoteEntitiesToPolicy(Quote $quote, Policy $policy): void
    {
        // Copy driver mappings
        foreach ($quote->drivers as $driver) {
            PolicyDriverMap::create([
                'policy_id' => $policy->id,
                'driver_id' => $driver->id,
                'is_primary_driver' => $driver->pivot->is_primary_driver,
                'driver_type' => $driver->pivot->driver_type,
                'assigned_vehicle_id' => $driver->pivot->assigned_vehicle_id,
            ]);
        }
        
        // Copy vehicle mappings
        foreach ($quote->vehicles as $vehicle) {
            PolicyVehicleMap::create([
                'policy_id' => $policy->id,
                'vehicle_id' => $vehicle->id,
                'coverage_type' => $vehicle->pivot->coverage_type,
                'deductible_amount' => $vehicle->pivot->deductible_amount,
            ]);
        }
    }
}
```

## V4 Transaction Consolidation

### Single Transaction Table
All financial operations use the consolidated transaction/transaction_line structure defined in GR-70, eliminating the need for separate tables for different transaction types.

```php
// Example: Using unified transaction table for all operations
class TransactionService
{
    public function createTransaction(string $type, array $data): Transaction
    {
        return DB::transaction(function () use ($type, $data) {
            // All transaction types use same table
            $transaction = Transaction::create([
                'transaction_type' => $type, // QUOTE, BIND, PAYMENT, etc.
                'reference_type' => $data['reference_type'],
                'reference_id' => $data['reference_id'],
                'total_amount' => $data['amount'],
                'status_id' => Status::PENDING,
                'created_by' => auth()->id(),
                'metadata' => $data['metadata'] ?? [],
            ]);
            
            // Create transaction lines
            foreach ($data['lines'] as $line) {
                TransactionLine::create([
                    'transaction_id' => $transaction->id,
                    'line_number' => $line['line_number'],
                    'account_type' => $line['account_type'],
                    'account_code' => $line['account_code'],
                    'component_type' => $line['component_type'],
                    'debit_amount' => $line['debit_amount'] ?? 0,
                    'credit_amount' => $line['credit_amount'] ?? 0,
                    'description' => $line['description'],
                ]);
            }
            
            return $transaction;
        });
    }
}
```

## V4 Simplified Versioning

### Action Table Only Versioning
The system uses only the action table for all versioning needs, eliminating separate version tables for each entity type.

```sql
-- Universal action table for all versioning
CREATE TABLE action (
    action_id INT AUTO_INCREMENT PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL, -- driver, vehicle, policy, quote, etc.
    entity_id INT NOT NULL,
    action_type VARCHAR(50) NOT NULL, -- CREATE, UPDATE, DELETE, STATUS_CHANGE
    field_name VARCHAR(100), -- Specific field changed
    old_value TEXT, -- Previous value (JSON for complex types)
    new_value TEXT, -- New value (JSON for complex types)
    reason VARCHAR(255), -- Reason for change
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSON, -- Additional context
    INDEX idx_entity (entity_type, entity_id),
    INDEX idx_user (user_id),
    INDEX idx_created (created_at)
);
```

### Versioning Service
```php
namespace App\Services\Versioning;

class ActionVersioningService
{
    /**
     * Record any entity change in action table
     */
    public function recordChange(
        string $entityType,
        int $entityId,
        string $actionType,
        array $changes,
        ?string $reason = null
    ): void {
        foreach ($changes as $field => $values) {
            Action::create([
                'entity_type' => $entityType,
                'entity_id' => $entityId,
                'action_type' => $actionType,
                'field_name' => $field,
                'old_value' => $this->serializeValue($values['old']),
                'new_value' => $this->serializeValue($values['new']),
                'reason' => $reason,
                'user_id' => auth()->id(),
                'metadata' => [
                    'ip_address' => request()->ip(),
                    'user_agent' => request()->userAgent(),
                ],
            ]);
        }
    }
    
    /**
     * Get entity history from action table
     */
    public function getEntityHistory(string $entityType, int $entityId): Collection
    {
        return Action::where('entity_type', $entityType)
            ->where('entity_id', $entityId)
            ->orderBy('created_at', 'desc')
            ->get();
    }
    
    /**
     * Reconstruct entity state at specific point in time
     */
    public function getEntityStateAt(
        string $entityType,
        int $entityId,
        Carbon $timestamp
    ): array {
        // Get all actions up to timestamp
        $actions = Action::where('entity_type', $entityType)
            ->where('entity_id', $entityId)
            ->where('created_at', '<=', $timestamp)
            ->orderBy('created_at')
            ->get();
            
        // Reconstruct state by applying changes
        $state = [];
        foreach ($actions as $action) {
            if ($action->action_type === 'DELETE') {
                return ['deleted' => true, 'deleted_at' => $action->created_at];
            }
            
            if ($action->field_name) {
                $state[$action->field_name] = $this->deserializeValue($action->new_value);
            }
        }
        
        return $state;
    }
    
    private function serializeValue($value): string
    {
        return is_array($value) || is_object($value) 
            ? json_encode($value) 
            : (string) $value;
    }
    
    private function deserializeValue(string $value)
    {
        $decoded = json_decode($value, true);
        return json_last_error() === JSON_ERROR_NONE ? $decoded : $value;
    }
}
```

### Model Integration
```php
// Trait for automatic versioning
trait TracksChanges
{
    protected static function bootTracksChanges()
    {
        static::updating(function ($model) {
            $changes = [];
            foreach ($model->getDirty() as $field => $newValue) {
                $changes[$field] = [
                    'old' => $model->getOriginal($field),
                    'new' => $newValue,
                ];
            }
            
            if (!empty($changes)) {
                app(ActionVersioningService::class)->recordChange(
                    $model->getTable(),
                    $model->getKey(),
                    'UPDATE',
                    $changes
                );
            }
        });
        
        static::created(function ($model) {
            app(ActionVersioningService::class)->recordChange(
                $model->getTable(),
                $model->getKey(),
                'CREATE',
                ['created' => ['old' => null, 'new' => $model->toArray()]]
            );
        });
        
        static::deleted(function ($model) {
            app(ActionVersioningService::class)->recordChange(
                $model->getTable(),
                $model->getKey(),
                'DELETE',
                ['deleted' => ['old' => $model->toArray(), 'new' => null]]
            );
        });
    }
}

// Usage in models
class Driver extends Model
{
    use TracksChanges;
    // Model implementation
}
```

## Benefits of V4 Architecture

### Shared Entity Model Benefits
1. **Data Consistency**: Single source of truth for driver/vehicle data
2. **Reduced Duplication**: No copying data between quote and policy tables
3. **Simpler Relationships**: Clear mapping through dedicated junction tables
4. **Better Performance**: Less data to manage and sync
5. **Easier Updates**: Update driver once, reflected everywhere

### Simplified Versioning Benefits
1. **Single Versioning System**: One action table for all entities
2. **Consistent History**: Same pattern for tracking all changes
3. **Flexible Reconstruction**: Can rebuild any entity state
4. **Reduced Complexity**: No entity-specific version tables
5. **Better Auditing**: Complete audit trail in one location

### Transaction Consolidation Benefits
1. **Unified Financial Model**: All transactions in one structure
2. **Consistent Processing**: Same flow for all transaction types
3. **Simplified Reporting**: Single source for financial data
4. **Better Integration**: Easier to connect with GL systems
5. **Cleaner Architecture**: Follows GR-70 standards