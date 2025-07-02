# 37.0 Locking Workflow with Centralized Logging and Action Tracking

1. Centralized Locking and Activity Logging
    - Every lock and unlock operation, as well as create, read, update, delete (CRUD) and additional operations (trash, restore, process, etc.), must create a new record in the action table.
    - The action record must capture essential metadata, including:
        - action_type_id – Identifies the type of action performed.
        - description – Provides a summary of the action taken.
        - status_id – Indicates whether the action is active, expired, or released.
        - timestamps – Records when the action occurred.
        - user references – Identifies who performed the action.
    - User references must be recorded for all actions, whether performed by:
        - A real user (user_id).
        - A system process (system_user_id).
        - A scheduler job (scheduler_user_id).
    - Each lock operation must be logged in the lock table to ensure that every locked record has a corresponding action record, which tracks:
        - The type of lock applied (lock_type_id).
        - The entity that was locked (entity_type_id).
        - The user responsible for the lock (created_by, updated_by).
2. Linking Locks and Actions to Records
    - action.record_id must link each action to the specific record it affects.
    - map_lock_action must ensure that every lock is tied to an action, maintaining consistency between the locking mechanism and the audit log.
3. User Accountability and Permissions
    - All locks and actions must store who performed them (created_by, updated_by), ensuring full traceability.
    - System-driven or scheduled operations must use a user reference that points to either a system user or a scheduler user in the user table.
    - Access to locked records must be controlled based on user roles:
        - Administrators or managers may override a lock.
        - Regular users may only view locked records in read-only mode.
4. Lock Types and Status Management
    - Locks can be temporary or system-enforced. The lock_type table defines different lock types, including:
        - User Lock – Applied when a user starts editing a record.
        - System Lock – Applied automatically by a system process (e.g., data synchronization).
    - The status_id field in both lock and action tables determines whether the lock is:
        - Active – The record is currently locked.
        - Expired – The lock has timed out.
        - Released – The lock was manually removed.
5. Detailed Change Description in Action Logs
    - Each action record must store a clear, meaningful description of what changed in the locked entity.
    - Examples:
        - Lock Acquired: "User #5 locked Policy #123 for editing."
        - Lock Released: "System unlocked Claim #45 due to timeout."
        - Field Update: "Updated policy status from ‘Pending’ to ‘Active’."
    - The action table serves as an independent audit log, maintaining a history of lock activity and record changes.

### 37.1 Workflow Requirements

1. Lock Creation/Insert
    1. Check for Existing Lock
        - Before applying a lock, verify if the record is already locked (record_id in lock).
        - If an active lock exists (status_id = Active), prevent other users from editing.
    2. Insert Lock Record
        - Create a new row in lock, specifying:
            - lock_type_id – The type of lock applied.
            - entity_type_id – The entity category being locked.
            - record_id – The specific record being locked.
            - created_by – The user who initiated the lock.
    3. Insert Action Record
        - Create a corresponding action record, with action_type_id referencing lock creation.
    4. Map Lock to Record
        - Insert a row in map_lock_action, linking the lock and action records to the specific record.id.
        - If the lock is system-driven, the created_by field must reference the system user.
2. Read/View a Locked Record
    - Check if the record is locked in lock.
    - If locked, restrict editing and allow only read-only access.
    - Log an action in the action table, indicating that the record was accessed while locked.
3. Update a Locked Record
    1. Verify Lock Ownership
        - If the user attempting to update the record does not own the lock, deny the update.
        - If the user owns the lock, allow the update.
    2. Insert Action Record
        - Log an update action, capturing field changes (old_value, new_value).
    3. Unlock Automatically Upon Save
        - Release the lock by updating status_id in lock.
        - Log an unlock action in the action table and map_lock_action table.
4. Delete/Trash/Process a Locked Record
    1. Verify Lock Status
        - If the record is locked by another user or system process, prevent deletion.
        - If the user owns the lock, allow the delete/trash operation.
    2. Log a Delete or Trash Action
        - Insert a row in action, specifying action_type_id as "delete" or "trash".
    3. Update lock to mark it as inactive
        - Update lock to mark it as inactive.
5. Automatic Lock Expiration & Release
    1. Scheduled Cleanup Job
        - A background process will periodically check lock for expired locks.
        - If created_at is older than 30 minutes, update status_id to "expired".
        - Log an unlock action with the description: "Lock auto-released due to timeout."
    2. User-initiated Unlock
        - Certain users (e.g., administrators) can manually unlock records.
        - Logs an override action in action, specifying who forcefully removed the lock.

### 37.2 Table Relationships & Data Structure

1. Entity Lock Table (lock)
    - Tracks active and expired locks on records.
    - Links to user for accountability.
2. Lock Type Table (lock_type)
    - Defines different lock mechanisms, including:
        - User lock (manual).
        - System lock (automated).
3. Entity Type Table (entity_type)
    - Categorizes entities that can be locked, such as:
        - Policy
        - Claim
        - User
4. Action Table (action)
    - Stores every event in the system, including:
        - Locking and unlocking actions.
        - Record modifications.
        - System-driven updates.
5. Mapping Table (map_lock_action)
    - Links lock records to action records for audit tracking.

### 37.3 Business Logic & Application Layer

1. Eloquent Observers for Automatic Logging
    - Observers track Eloquent events (creating, updating, deleting).
    - When a model is updated, an action is automatically logged.
2. Transactional Integrity
    - Locks, actions, and entity updates must be wrapped in a database transaction to prevent partial writes.
3. Role-Based Lock Overrides
    - Certain user roles (e.g., managers, administrators) can override locks when necessary.