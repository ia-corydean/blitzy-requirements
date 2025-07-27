# GR-37 Database Alignment Approach: Locking Workflow with Centralized Logging

## Current State Analysis

### Tables Found in Database
1. **action** - EXISTS
   - Structure matches basic requirements
   - Fields: id, action_type_id, status_id, created_by, updated_by, created_at, updated_at
   - **MISSING**: description field, record_id field

2. **action_type** - EXISTS
   - Assumed to contain action type definitions

3. **lock** - EXISTS  
   - Structure matches basic requirements
   - Fields: id, lock_type_id, status_id, created_by, updated_by, created_at, updated_at
   - **MISSING**: entity_type_id, record_id fields

4. **lock_type** - EXISTS
   - Contains lock type definitions with proper structure
   - Fields: id, code, name, description, is_default, status_id, created_by, updated_by, created_at, updated_at

5. **entity_type** - EXISTS
   - Assumed to contain entity type definitions

### Missing Tables/Features
1. **map_lock_action** - DOES NOT EXIST
   - Critical for linking locks to actions as required by GR-37

## Key Differences from GR-37 Requirements

### 1. Action Table
- **Missing Fields**:
  - `description` (TEXT/VARCHAR) - Required for storing meaningful action descriptions
  - `record_id` (INT) - Required for linking actions to specific records
  - `user_id` (INT) - For real user references
  - `system_user_id` (INT) - For system process references  
  - `scheduler_user_id` (INT) - For scheduler job references
  - `metadata` (JSON) - For storing additional action details

### 2. Lock Table
- **Missing Fields**:
  - `entity_type_id` (INT) - Required to identify what type of entity is locked
  - `record_id` (INT) - Required to identify the specific record being locked
  - `expires_at` (TIMESTAMP) - For automatic lock expiration

### 3. Map Lock Action Table
- **Completely Missing** - Need to create this table
- Required structure:
  - `id` (INT PRIMARY KEY)
  - `lock_id` (INT) - Foreign key to lock table
  - `action_id` (INT) - Foreign key to action table
  - `created_at` (TIMESTAMP)

## Proposed Updates

### 1. Update Action Table
```sql
ALTER TABLE action 
ADD COLUMN description TEXT,
ADD COLUMN record_id INT,
ADD COLUMN user_id INT,
ADD COLUMN system_user_id INT,
ADD COLUMN scheduler_user_id INT,
    - all of these users should be accounted for with user and user_type
ADD COLUMN metadata JSON,
ADD INDEX idx_record_id (record_id),
ADD INDEX idx_user_id (user_id),
ADD INDEX idx_system_user_id (system_user_id),
ADD INDEX idx_scheduler_user_id (scheduler_user_id);
```

### 2. Update Lock Table
```sql
ALTER TABLE `lock`
ADD COLUMN entity_type_id INT NOT NULL,
ADD COLUMN record_id INT NOT NULL,
ADD COLUMN expires_at TIMESTAMP NULL,
ADD INDEX idx_entity_type_id (entity_type_id),
ADD INDEX idx_record_id (record_id),
ADD INDEX idx_expires_at (expires_at),
ADD FOREIGN KEY (entity_type_id) REFERENCES entity_type(id);
```

### 3. Create Map Lock Action Table
```sql
CREATE TABLE map_lock_action (
    id INT PRIMARY KEY AUTO_INCREMENT,
    lock_id INT NOT NULL,
    action_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lock_id) REFERENCES `lock`(id) ON DELETE CASCADE,
    FOREIGN KEY (action_id) REFERENCES action(id) ON DELETE CASCADE,
    INDEX idx_lock_id (lock_id),
    INDEX idx_action_id (action_id)
);
```

### 4. Add Reinstatement Action Types
Need to ensure action_type table contains the following types:
- POLICY_REINSTATEMENT_ELIGIBILITY_EVALUATED
- POLICY_REINSTATEMENT_CALCULATION_PERFORMED
- POLICY_REINSTATEMENT_PAYMENT_RECEIVED
- POLICY_REINSTATEMENT_COMPLETED
- POLICY_REINSTATEMENT_FAILED
- POLICY_REINSTATEMENT_ELIGIBILITY_EXPIRED

## Implementation Considerations

### 1. Migration Strategy
- Create migrations in proper order to avoid foreign key conflicts
- Populate default values for new required fields
- Consider data migration for existing records

### 2. Application Layer Updates
- Update Eloquent models to include new relationships
- Create observers for automatic action logging
- Implement lock expiration logic (cron job or scheduled task)

### 3. Performance Considerations
- Add appropriate indexes for query performance
- Consider partitioning action table by date if high volume expected
- Implement archival strategy for old action records

### 4. Integration Points
- Ensure all CRUD operations trigger action logging
- Implement transactional integrity for lock/action/record updates
- Add role-based permissions for lock overrides

## Next Steps
1. Review and approve proposed schema changes
2. Create database migrations
3. Update Eloquent models and relationships
4. Implement action logging service
5. Create lock management service with expiration handling
6. Add integration tests for locking workflow