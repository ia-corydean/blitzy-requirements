# IP269-New-Quote-ITC-Bridge-New-Info-2 - Implementation Plan

## Requirement Overview

### Purpose
This enhanced bridge screen emphasizes visibility with bolder alert styling and requires producers to address newly identified drivers before proceeding to bind. It ensures:
- Accuracy and completeness of underwriting data
- Prevention of quote submission with missing/invalid data
- User intervention to verify or exclude discovered entities
- Mandatory resolution before continuing

### Scope
- Warning-style alert cards with urgency indicators
- Bulk "Exclude All" functionality
- Missing info badges on discovered drivers
- Interaction lock until resolution
- Side panel for driver management
- Real-time premium updates

## Entity Analysis

### New Entities Required

1. **bridge_validation_rule**
   - Rules for mandatory resolution
   - Blocking conditions
   - Override permissions

2. **driver_missing_info**
   - Track missing fields per driver
   - Required vs optional fields
   - Completion percentage

3. **bulk_action_log**
   - Track bulk exclusions
   - Audit trail for compliance
   - User and timestamp

### Existing Entities Involved

- **quote**: Parent entity with validation state
- **driver**: Enhanced with completion status
- **bridge_discovered_driver**: Source data
- **quote_bridge_alert**: Enhanced styling
- **driver_type**: Inclusion/exclusion status

## Global Requirements Alignment

### Primary GRs
- **GR-53 (DCS Integration)**: Driver discovery
- **GR-04 (Validation)**: Mandatory field validation
- **GR-37 (Action Tracking)**: Bulk action audit
- **GR-18 (Workflow)**: Progression blocking
- **GR-20 (Business Logic)**: Resolution rules

### Supporting GRs
- **GR-11 (Accessibility)**: Alert visibility
- **GR-13 (Error Handling)**: Clear messaging
- **GR-09 (State Management)**: Lock state
- **GR-07 (UI Components)**: Alert styling

## Database Schema Planning

### Core Tables

1. **driver_missing_info**
   ```sql
   - id (PK)
   - driver_id (FK)
   - field_name
   - field_type (required, optional)
   - is_resolved (boolean)
   - resolved_at
   - status_id (FK)
   - created_at, updated_at
   ```

2. **bridge_validation_rule**
   ```sql
   - id (PK)
   - rule_code (unique)
   - rule_type (block_progress, warning_only)
   - condition_sql (text)
   - error_message
   - can_override (boolean)
   - status_id (FK)
   - created_at, updated_at
   ```

3. **bulk_action_log**
   ```sql
   - id (PK)
   - quote_id (FK)
   - action_type (exclude_all, include_all)
   - affected_count
   - entity_type (drivers, vehicles)
   - performed_by (FK)
   - performed_at
   - status_id (FK)
   ```

### Modified Tables

1. **quote_bridge_alert**
   ```sql
   ADD COLUMN severity_level (warning, error, critical)
   ADD COLUMN requires_resolution (boolean)
   ADD COLUMN resolution_deadline
   ```

2. **quote**
   ```sql
   ADD COLUMN bridge_validation_status
   ADD COLUMN can_proceed_to_bind (boolean)
   ```

## API Endpoints

### Required Endpoints
```
GET    /api/v1/quotes/{quote_id}/missing-info
POST   /api/v1/quotes/{quote_id}/validate-bridge-data
GET    /api/v1/quotes/{quote_id}/can-proceed
POST   /api/v1/quotes/{quote_id}/drivers/bulk-exclude
PUT    /api/v1/quotes/{quote_id}/drivers/{id}/complete-info
GET    /api/v1/quotes/{quote_id}/bridge-validation-status
```

### Validation Endpoints
```
POST   /api/v1/quotes/{quote_id}/override-validation
GET    /api/v1/validation-rules/bridge-requirements
```

### Real-time Updates
```javascript
private-quote.{quote_id}.validation-status
private-quote.{quote_id}.missing-info-updates
```

## Integration Points

### Internal Services
1. **ValidationService**
   - Check mandatory fields
   - Apply blocking rules
   - Calculate completion

2. **BulkActionService**
   - Process bulk exclusions
   - Update multiple drivers
   - Log actions

3. **ProgressionService**
   - Check can-proceed status
   - Apply workflow blocks
   - Handle overrides

4. **NotificationService**
   - Alert styling logic
   - Severity calculation
   - Message formatting

## Implementation Considerations

### Key Patterns
1. **Progressive Validation**
   - Real-time field checking
   - Visual completion indicators
   - Clear error states

2. **Bulk Operations**
   - Transactional bulk updates
   - Undo capability
   - Audit logging

3. **UI Blocking**
   - Disable continue button
   - Show resolution required
   - Guide user actions

4. **Alert Hierarchy**
   - Critical (red) - must resolve
   - Warning (yellow) - should resolve
   - Info (blue) - optional

### Technical Decisions
- Vue.js reactive validation
- Vuex for validation state
- Database transactions for bulk ops
- WebSocket for live updates
- Component-based alerts

## Quality Checkpoints

### Pre-Implementation
- [ ] Review validation patterns
- [ ] Check bulk operation standards
- [ ] Validate blocking logic
- [ ] Review alert styling guides

### Implementation
- [ ] Validation rules working
- [ ] Bulk exclude functioning
- [ ] UI properly blocked
- [ ] Alerts display correctly

### Post-Implementation
- [ ] Test all validation paths
- [ ] Verify bulk operations
- [ ] Check audit trails
- [ ] Validate accessibility

## Dependencies

### Upstream
- Bridge data must be fetched
- Basic quote data complete
- Driver discovery finished

### Downstream
- Binding blocked until resolved
- Premium finalized after resolution
- Compliance reporting affected

## Risk Mitigation

1. **User Frustration**: Clear guidance
2. **Data Loss**: Auto-save progress
3. **Bulk Errors**: Transaction rollback
4. **False Blocks**: Override capability

## UI/UX Specifications

### Alert Card Design
- Yellow/orange background
- Warning icon prominent
- Clear explanation text
- "Exclude All" CTA button
- Border highlighting

### Driver Status Badges
- "Missing Info" - red badge
- "Excluded" - gray badge
- "Included" - green badge
- Info icon for details

### Side Panel
- Required fields highlighted
- Progress indicator
- Save button per field
- Close returns to list

### Blocking Behavior
- Continue button disabled
- Tooltip explains why
- Resolution counter shown
- Success state on completion

## Next Steps

1. Create validation rule engine
2. Implement bulk action service
3. Build enhanced alert components
4. Create driver info side panel
5. Implement progression blocking
6. Add real-time validation
7. Create comprehensive audit logs