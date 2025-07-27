# GR-37 Database Alignment Approach V2: Locking Workflow with Centralized Logging

## Overview
This approach aligns GR-37's locking and action tracking requirements with the current database structure, using the existing user/user_type pattern instead of multiple user ID fields.

**V2 Updates**: 
- Use single user_id field with user_type to distinguish between manual users, system processes, and scheduler jobs
- Simplified approach leveraging existing database patterns

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

5. **user** & **user_type** - EXISTS
   - Can distinguish between manual users, system processes, and scheduler jobs
   - User types can include: USER, SYSTEM, SCHEDULER, API, etc.

### Missing Tables/Features
1. **map_lock_action** - DOES NOT EXIST
   - Critical for linking locks to actions as required by GR-37

## Key Differences from GR-37 Requirements

### 1. Action Table
- **Missing Fields**:
  - `description` (TEXT/VARCHAR) - Required for storing meaningful action descriptions
  - `record_id` (INT) - Required for linking actions to specific records
  - `metadata` (JSON) - For storing additional action details

### 2. Lock Table
- **Missing Fields**:
  - `entity_type_id` (INT) - Required to identify what type of entity is locked
  - `record_id` (INT) - Required to identify the specific record being locked
  - `expires_at` (TIMESTAMP) - For automatic lock expiration

### 3. Map Lock Action Table
- **Completely Missing** - Need to create this table

## Proposed Updates

### 1. Update Action Table
```sql
ALTER TABLE action 
ADD COLUMN description TEXT,
ADD COLUMN record_id INT,
ADD COLUMN user_id INT COMMENT 'References user table - type determined by user_type',
ADD COLUMN metadata JSON,
ADD INDEX idx_record_id (record_id),
ADD INDEX idx_user_id (user_id),
ADD FOREIGN KEY (user_id) REFERENCES user(id);
```

**Note**: The user_id field references the user table, where the user_type determines if it's a manual user, system process, or scheduler job.

### 2. Update Lock Table
```sql
ALTER TABLE `lock`
ADD COLUMN entity_type_id INT NOT NULL,
ADD COLUMN record_id INT NOT NULL,
ADD COLUMN expires_at TIMESTAMP NULL,
ADD COLUMN user_id INT COMMENT 'User who created the lock',
ADD INDEX idx_entity_type_id (entity_type_id),
ADD INDEX idx_record_id (record_id),
ADD INDEX idx_expires_at (expires_at),
ADD INDEX idx_user_id (user_id),
ADD FOREIGN KEY (entity_type_id) REFERENCES entity_type(id),
ADD FOREIGN KEY (user_id) REFERENCES user(id);
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

### 4. Ensure User Types Exist
Verify user_type table contains appropriate types:
```sql
-- Example user types needed
INSERT INTO user_type (code, name, description) VALUES
('USER', 'Manual User', 'Human user performing manual actions'),
('SYSTEM', 'System Process', 'Automated system processes'),
('SCHEDULER', 'Scheduler Job', 'Scheduled job or cron task'),
('API', 'API Client', 'External API client'),
('IMPORT', 'Import Process', 'Data import processes');
```

### 5. Add Action Types for Reinstatement
Ensure action_type table contains reinstatement-related types:
```sql
-- Example action types for reinstatement workflow
INSERT INTO action_type (code, name, description) VALUES
('POLICY_REINSTATEMENT_ELIGIBILITY_EVALUATED', 'Reinstatement Eligibility Evaluated', 'System evaluated policy reinstatement eligibility'),
('POLICY_REINSTATEMENT_CALCULATION_PERFORMED', 'Reinstatement Calculation Performed', 'System calculated reinstatement premium'),
('POLICY_REINSTATEMENT_PAYMENT_RECEIVED', 'Reinstatement Payment Received', 'Payment received for policy reinstatement'),
('POLICY_REINSTATEMENT_COMPLETED', 'Reinstatement Completed', 'Policy successfully reinstated'),
('POLICY_REINSTATEMENT_FAILED', 'Reinstatement Failed', 'Policy reinstatement attempt failed'),
('POLICY_REINSTATEMENT_ELIGIBILITY_EXPIRED', 'Reinstatement Eligibility Expired', 'Reinstatement window expired');
```

## Benefits of This Approach

1. **Simplicity**: Uses existing user/user_type pattern instead of multiple user ID fields
2. **Consistency**: Aligns with current database patterns
3. **Flexibility**: User types can be extended without schema changes
4. **Audit Trail**: Complete tracking of who (user) and what (action) occurred

## Implementation Considerations

### 1. User Type Usage
- System processes should have dedicated user records with appropriate user_type
- Scheduler jobs should have their own user records
- This allows full audit trail while maintaining simplicity

### 2. Action Logging Pattern
```sql
-- Example: Logging a system action
INSERT INTO action (action_type_id, user_id, record_id, description, metadata)
SELECT 
    at.id,
    u.id,
    123, -- record being acted upon
    'Policy eligibility check completed',
    '{"result": "eligible", "days_lapsed": 15}'
FROM action_type at
CROSS JOIN user u
WHERE at.code = 'POLICY_REINSTATEMENT_ELIGIBILITY_EVALUATED'
AND u.email = 'system@insurance.com'
AND u.user_type_id = (SELECT id FROM user_type WHERE code = 'SYSTEM');
```

### 3. Lock Management
- Locks should reference the user who created them
- Lock expiration can be handled by scheduled jobs
- Override permissions managed through role-based access

## Next Steps

1. Review and approve simplified approach
2. Create database migrations
3. Set up system and scheduler user records
4. Implement action logging service
5. Create lock management service
6. Add integration tests