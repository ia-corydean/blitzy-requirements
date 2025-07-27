# GR-37 Locking Workflow with Centralized Logging - Requirement Comparison Outline

## Overview
This document outlines the proposed updates to GR-37 based on the database alignment findings and v2 approach feedback, particularly the simplification of user tracking.

## Current GR-37 Structure

### Existing Content:
1. **Centralized Locking and Activity Logging**
   - Action tracking for all operations
   - Multiple user ID types (user_id, system_user_id, scheduler_user_id)
   - Lock and action table requirements

2. **Linking Locks and Actions**
   - action.record_id linkage
   - map_lock_action relationship table

3. **User Accountability and Permissions**
   - User tracking requirements
   - Role-based access control

4. **Lock Types and Status Management**
   - Different lock types
   - Status tracking

5. **Detailed Change Description**
   - Action log descriptions
   - Audit trail requirements

### Section 37.1: Workflow Requirements
- Lock creation/insert procedures
- Lock checking logic
- Lock release procedures

## Proposed Updates Based on V2 Approach

### 1. Simplify User Tracking

**Current Approach**:
```
- user_id (for real users)
- system_user_id (for system processes)  
- scheduler_user_id (for scheduled jobs)
```

**Proposed Approach**:
```
- user_id only (references user table)
- User type determined by user_type table:
  - USER (manual users)
  - SYSTEM (system processes)
  - SCHEDULER (scheduled jobs)
  - API (external integrations)
```

### 2. Database Schema Updates

**Add Missing Fields to Action Table**:
- description (TEXT)
- record_id (INT)
- user_id (INT) - single field for all user types
- metadata (JSON)

**Add Missing Fields to Lock Table**:
- entity_type_id (INT)
- record_id (INT)
- expires_at (TIMESTAMP)
- user_id (INT)

**Create map_lock_action Table**:
- New table to link locks and actions
- Simple structure with lock_id, action_id

### 3. Content Structure Changes

#### Section to Update: "Centralized Locking and Activity Logging"
**Remove**: References to multiple user ID fields
**Add**: Explanation of user_type pattern
**Update**: Examples to use single user_id approach

#### Section to Update: "User Accountability"
**Remove**: Complex user reference logic
**Add**: Clear explanation of user types
**Provide**: Examples of system/scheduler user setup

#### New Section: "Database Schema"
**Add**: Complete schema definitions for:
- action table (with enhancements)
- lock table (with enhancements)
- map_lock_action table
- User type examples

## Comparison Table

| Aspect | Current GR-37 | Proposed GR-37 |
|--------|---------------|----------------|
| User Tracking | 3 separate ID fields | 1 user_id field with types |
| Database Schema | Not included | Full schema section |
| Action Table | Basic structure implied | Enhanced with all fields |
| Lock Table | Basic structure implied | Enhanced with entity tracking |
| Examples | Generic descriptions | Specific SQL examples |

## Benefits of Updates

1. **Simplification**: Single user tracking pattern
2. **Clarity**: Explicit database schema
3. **Consistency**: Aligns with existing database patterns
4. **Flexibility**: User types can be extended
5. **Implementation Ready**: Clear schemas for developers

## Implementation Examples to Add

### User Type Setup Example:
```sql
-- System users for different processes
INSERT INTO user (email, user_type_id, name_id) VALUES
('system@insurance.com', (SELECT id FROM user_type WHERE code = 'SYSTEM'), ...),
('scheduler@insurance.com', (SELECT id FROM user_type WHERE code = 'SCHEDULER'), ...);
```

### Action Logging Example:
```sql
-- Log a system action
INSERT INTO action (action_type_id, user_id, record_id, description)
SELECT 
    at.id,
    u.id,
    123,
    'Policy eligibility check completed'
FROM action_type at, user u
WHERE at.code = 'POLICY_CHECK'
AND u.email = 'system@insurance.com';
```

## Sections Requiring Minor Updates

1. **Workflow Requirements (37.1)**
   - Update to use single user_id
   - Add lock expiration handling
   - Include entity_type checking

2. **Examples Throughout**
   - Replace multi-user references
   - Use consistent user_type pattern
   - Show real SQL examples

## Summary

The updates to GR-37 will:
- Simplify the user tracking mechanism
- Add complete database schema documentation
- Provide clear implementation examples
- Maintain all business requirements
- Align with existing database patterns