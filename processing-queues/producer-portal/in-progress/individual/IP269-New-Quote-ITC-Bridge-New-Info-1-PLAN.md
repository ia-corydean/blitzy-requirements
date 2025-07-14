# IP269-New-Quote-ITC-Bridge-New-Info-1 - Implementation Plan

## Requirement Overview

### Purpose
This enhanced Review Quote screen handles external data enrichment (bridge) that identifies new drivers related to the quote that weren't initially declared. The system must:
- Transparently notify agents about auto-discovered information
- Enable validation and editing of discovered data
- Preserve compliance by ensuring all household members are disclosed
- Automatically set new drivers as excluded with option to include

### Scope
- Bridge data integration for driver discovery
- Automatic exclusion of discovered drivers
- Side panel editing for driver inclusion
- Premium recalculation on driver status changes
- Alert banners for new information

## Entity Analysis

### New Entities Required

1. **bridge_data_source**
   - External data source configuration
   - API endpoint information
   - Source credibility rating

2. **quote_bridge_result**
   - Bridge query results per quote
   - Timestamp and status
   - Raw response data storage

3. **bridge_discovered_driver**
   - Drivers found via bridge
   - Link to quote and source
   - Confidence score

4. **bridge_alert**
   - Alert configurations
   - Message templates
   - Display rules

### Existing Entities Involved

- **quote**: Parent for bridge results
- **driver**: Enhanced with bridge source
- **driver_type**: Excluded/included status
- **entity**: DCS integration (GR-52/GR-53)
- **communication**: API call tracking (GR-44)

## Global Requirements Alignment

### Primary GRs
- **GR-53 (DCS Integration)**: Household driver lookup
- **GR-52 (Universal Entity)**: External API management
- **GR-44 (Communication)**: API call logging
- **GR-48 (External Integrations)**: Apache Camel routing
- **GR-37 (Action Tracking)**: Bridge result audit

### Supporting GRs
- **GR-20 (Business Logic)**: Auto-exclusion rules
- **GR-33 (Data Services)**: Cache bridge results
- **GR-12 (Security)**: PII handling for discovered data
- **GR-04 (Validation)**: Driver data validation

## Database Schema Planning

### Core Tables

1. **quote_bridge_result**
   ```sql
   - id (PK)
   - quote_id (FK)
   - entity_id (FK) -- GR-52 external entity
   - request_correlation_id (UUID)
   - response_data (JSON)
   - discovered_count
   - processing_status
   - processed_at
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

2. **bridge_discovered_driver**
   ```sql
   - id (PK)
   - quote_bridge_result_id (FK)
   - driver_id (FK, nullable) -- if converted to actual driver
   - first_name
   - last_name
   - date_of_birth
   - license_number (encrypted)
   - confidence_score (decimal)
   - action_taken (excluded, included, ignored)
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

3. **quote_bridge_alert**
   ```sql
   - id (PK)
   - quote_id (FK)
   - alert_type (new_drivers, new_vehicles)
   - alert_message
   - is_acknowledged (boolean)
   - acknowledged_by (FK)
   - acknowledged_at
   - status_id (FK)
   - created_at, updated_at
   ```

### Modified Tables

1. **driver**
   ```sql
   ADD COLUMN bridge_source_id (FK to bridge_discovered_driver)
   ADD COLUMN is_bridge_discovered (boolean)
   ```

## API Endpoints

### Required Endpoints
```
POST   /api/v1/quotes/{quote_id}/bridge-lookup
GET    /api/v1/quotes/{quote_id}/bridge-results
GET    /api/v1/quotes/{quote_id}/discovered-drivers
POST   /api/v1/quotes/{quote_id}/discovered-drivers/{id}/convert
PUT    /api/v1/quotes/{quote_id}/drivers/{id}/inclusion-status
POST   /api/v1/quotes/{quote_id}/bridge-alerts/acknowledge
```

### DCS Integration (GR-53)
```
POST   /integrations/dcs/household-drivers
```

### Real-time Updates
```javascript
private-quote.{quote_id}.bridge-updates
private-quote.{quote_id}.driver-changes
```

## Integration Points

### External Services (GR-52/GR-53)
1. **DCS Household API**
   - Entity Type: DCS_HOUSEHOLD_DRIVERS
   - Timeout: 5 seconds
   - Circuit breaker: 5 failures
   - Cache duration: 24 hours

### Internal Services
1. **BridgeService**
   - Orchestrate external lookups
   - Process discovered entities
   - Auto-exclusion logic

2. **DriverService**
   - Convert discovered to actual drivers
   - Handle inclusion/exclusion
   - Trigger premium updates

3. **CommunicationService (GR-44)**
   - Log all DCS API calls
   - Track correlation IDs
   - Mask PII in logs

## Implementation Considerations

### Key Patterns
1. **Async Bridge Processing**
   - Queue bridge lookups
   - Non-blocking UI updates
   - Progressive enhancement

2. **Auto-Exclusion Logic**
   - All discovered drivers start excluded
   - Require explicit inclusion
   - Track decision audit trail

3. **Side Panel Editing**
   - Lazy load driver details
   - Real-time validation
   - Premium impact preview

### Technical Decisions
- Apache Camel for DCS integration
- Redis for bridge result caching
- Vue.js reactive components
- WebSocket for real-time updates
- Encrypted storage for PII

## Quality Checkpoints

### Pre-Implementation
- [ ] Review GR-53 DCS patterns
- [ ] Validate entity management setup
- [ ] Check communication logging
- [ ] Review driver exclusion rules

### Implementation
- [ ] DCS integration working
- [ ] Auto-exclusion functioning
- [ ] Side panel updates premium
- [ ] Alert banners display

### Post-Implementation
- [ ] Load test DCS calls
- [ ] Verify PII encryption
- [ ] Test circuit breakers
- [ ] Validate audit trails

## Dependencies

### Upstream
- Quote review step reached
- Basic driver info available
- DCS credentials configured

### Downstream
- Premium calculation affected
- Policy binding includes all drivers
- Compliance reporting updated

## Risk Mitigation

1. **API Failures**: Circuit breakers and fallbacks
2. **Data Privacy**: Encrypt all PII
3. **Performance**: Async processing and caching
4. **Accuracy**: Confidence scoring and manual review

## UI/UX Specifications

### Alert Banner
- Yellow/orange warning style
- Clear explanation text
- Positioned in driver section
- Dismissible after action

### Driver Cards
- "Discovered" badge
- Excluded by default
- Edit icon for side panel
- Quick exclude all option

### Side Panel
- Driver details form
- Include/exclude toggle
- Additional info fields
- Premium impact display

## Next Steps

1. Configure DCS entity in Universal Entity Management
2. Create bridge service with Apache Camel
3. Implement auto-exclusion logic
4. Build discovered driver UI components
5. Create side panel editing
6. Add WebSocket updates
7. Implement comprehensive logging