# IP286-Re-Quoting - Complete Requirement

---

## **A) WHY – Vision and Purpose**

The Re-Quoting feature revolutionizes the quote generation process by enabling producers to create new quotes using existing policy data as a foundation. This significantly reduces quote creation time while ensuring accuracy through automated change detection and verification.

The purpose is to:
- Accelerate quote generation by reusing validated policy data
- Automatically detect and flag changes in customer information
- Streamline renewals, policy updates, and win-back scenarios
- Reduce data entry errors through intelligent data cloning
- Provide seamless transitions from cancelled policies to new quotes

By leveraging existing policy information and intelligently detecting changes, the system empowers producers to generate accurate quotes in minutes rather than starting from scratch, improving both efficiency and customer satisfaction.

---

## **B) WHAT – Core Requirements**

### **1. Requote Entry Points**

The requote process must be accessible from:
- **Policy Detail Pages**: Prominent "Requote" button
- **Policy Search Results**: Quick action option
- **Cancelled Policy Views**: Re-engagement opportunity

### **2. Requote Kickoff Dialog**

Initial configuration includes:
- **Effective Date Selection**:
  - Defaults to today's date
  - User-editable with calendar picker
  - Validation against policy terms
- **Action Options**:
  - "Start Requote" primary action
  - "Cancel" to abort process
- **Context Information**:
  - Source policy number display
  - Current policy status indicator

### **3. Requote Review Screen**

Enhanced version of standard Quote Review with:

- **Change Notifications**:
  - **Address Changes**:
    - Modal displays old vs new address
    - User selects which to use
    - Yellow highlighting for changes
    - Revert option available
  - **Driver Discovery**:
    - New household members detected
    - Include/exclude selection required
    - Side panel for driver details
    - Additional information collection

- **Standard Review Sections**:
  - Primary Insured Information
  - Drivers (with change indicators)
  - Vehicles (with coverage details)
  - Coverages (policy and vehicle level)
  - Discounts (recalculated)
  - Premium Summary (updated)

### **4. Editable Sections**

Full editing capabilities for:
- **Drivers**: Add, edit, remove, include/exclude
- **Vehicles**: Update details, change usage, modify VIN
- **Coverages**: Adjust limits, deductibles, add/remove
- **Discounts**: Verify eligibility, apply new
- **Premium**: Real-time recalculation

### **5. Business Rules & Validation**

- **Data Cloning Rules**:
  - All policy data copied to quote tables
  - Original policy remains unchanged
  - Audit trail maintained
  - Version tracking enabled

- **Change Detection**:
  - Address verification runs automatically
  - Driver discovery checks household
  - Coverage availability verified
  - Discount eligibility rechecked

- **Visual Indicators**:
  - Yellow highlight for changes
  - Information icons for details
  - Clear change explanations

### **6. Save & Navigation**

- **Quote Persistence**:
  - Auto-save during editing
  - Draft status maintained
  - Resume capability

- **Navigation Options**:
  - Edit any section directly
  - Return to policy view
  - Continue to binding

---

## Entity Analysis

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|-------|
| quote | Core | Existing | Has policy_id for source tracking |
| quote_type | Reference | Existing | Can define "Requote" type |
| policy | Core | Existing | Source data for cloning |
| driver | Core | Existing | Shared between policy and quote |
| vehicle | Core | Existing | Shared vehicle records |
| coverage | Core | Existing | Coverage definitions |
| address | Supporting | Existing | Verification results |
| verification | Supporting | Existing | External verification tracking |
| discount | Supporting | Existing | Discount calculations |
| map_policy_driver | Map | Existing | Source for driver cloning |
| map_policy_vehicle | Map | Existing | Source for vehicle cloning |
| map_policy_coverage | Map | Existing | Source for coverage cloning |
| map_quote_driver | Map | Existing | Destination for cloned drivers |
| map_quote_vehicle | Map | Existing | Destination for cloned vehicles |
| map_quote_coverage | Map | Existing | Destination for cloned coverages |

### New Tables Required
None - existing infrastructure fully supports requoting

### Modifications to Existing Tables
None - quote table already has policy_id and renewal fields

### Relationships Identified
- quote → references → policy (via policy_id)
- policy → has many → drivers/vehicles/coverages (for cloning)
- quote → has many → drivers/vehicles/coverages (cloned data)
- quote → uses → quote_type (to identify as requote)
- address → belongs to → verification (for change detection)

---

## Field Mappings (Section C)

### Backend Mappings

#### Requote Initiation

##### Create Requote from Policy
- **Backend Mapping**: 
  ```
  get policy.id from selection
  -> validate policy status allows requoting
  -> create new quote record:
     - policy_id = source policy
     - quote_type_id = 'REQUOTE'
     - effective_date = user selection
     - is_renewal = true/false based on context
     - version_number = increment
  -> clone all policy data to quote:
     - drivers via map tables
     - vehicles via map tables
     - coverages via map tables
  -> return new quote.id
  ```

#### Data Cloning Process

##### Clone Policy Components
- **Backend Mapping**: 
  ```
  get source policy.id
  -> for each driver in map_policy_driver:
     - create map_quote_driver record
     - link to same driver entity
     - preserve all attributes
  -> for each vehicle in map_policy_vehicle:
     - create map_quote_vehicle record
     - link to same vehicle entity
     - copy all coverage details
  -> for each coverage in map_policy_coverage:
     - create map_quote_coverage record
     - maintain limits and deductibles
  -> calculate initial premium
  ```

#### Change Detection

##### Verify and Flag Changes
- **Backend Mapping**: 
  ```
  get quote with cloned data
  -> run address verification:
     - call external service
     - compare to stored address
     - flag if different
  -> check driver discovery:
     - query household members
     - identify new drivers
     - flag for inclusion decision
  -> verify coverage availability:
     - check program rules
     - validate against new date
  -> store flags in quote metadata
  ```

#### Review Screen Display

##### Build Enhanced Review
- **Backend Mapping**: 
  ```
  get quote with all relationships
  -> check for change flags
  -> if address changed:
     - prepare comparison modal
     - highlight affected sections
  -> if new drivers found:
     - prepare driver list
     - show inclusion options
  -> load standard review data:
     - all drivers, vehicles, coverages
     - calculate discounts
     - determine premium
  -> return enhanced review data
  ```

#### Edit Navigation

##### Handle Section Edits
- **Backend Mapping**: 
  ```
  receive edit request for section
  -> pass quote context with:
     - requote indicator
     - source policy reference
     - change flags
  -> navigate to appropriate step
  -> maintain all quote data
  -> recalculate on return
  -> update change indicators
  ```

### Implementation Architecture

The requoting system leverages existing infrastructure with enhancements:

1. **Cloning Service**: Transactional data copying from policy to quote
2. **Verification Engine**: External service integration for changes
3. **Change Detection**: Algorithm-based comparison and flagging
4. **Visual Components**: UI indicators for changed data
5. **Context Manager**: Maintains requote state through workflows
6. **Premium Calculator**: Real-time recalculation with new data

### Integration Specifications

**Address Verification**:
- External API for address validation
- Standardization and comparison logic
- Change flagging and storage

**Driver Discovery**:
- Household composition service
- Inclusion/exclusion workflow

**Quote Workflows**:
- Context passing for requote indicator
- Change preservation through edits
- Seamless bind transition

**Audit Trail**:
- Complete cloning history
- Change decision tracking
- User action logging

---

## **D) User Experience (UX) & Flows**

### **1. Requote Initiation Flow**

1. User views policy details
2. Clicks "Requote" button
3. Dialog appears with effective date
4. User adjusts date if needed
5. Clicks "Start Requote"
6. System clones data in background
7. Redirects to enhanced review screen

### **2. Change Notification Flow**

1. Review screen loads with notifications
2. **Address Change**:
   - Modal shows old vs new address
   - User selects preferred address
   - System updates and highlights
3. **New Drivers**:
   - List shows discovered drivers
   - User clicks to view details
   - Selects include/exclude
   - Enters required information

### **3. Review and Edit Flow**

1. User reviews all sections
2. Changed items highlighted yellow
3. Clicks edit on any section
4. Navigates to appropriate step
5. Makes necessary changes
6. Returns to review
7. Premium updates automatically

### **4. Binding Transition Flow**

1. User completes review
2. Clicks "Start Binding"
3. System passes requote context
4. Standard bind workflow begins:
   - Vehicle photo upload
   - Document upload
   - Signature collection
   - Payment processing
5. New policy created

### **5. Mobile Experience**

- Responsive design for all screens
- Touch-optimized dialogs
- Swipeable change notifications
- Collapsible sections for space
- Maintained functionality

### **6. UI Presentation Guidelines**

- Yellow highlighting for all changes
- Information icons with explanations
- Modal dialogs for decisions
- Side panels for details
- Progress indicators during cloning
- Clear action buttons
- Consistent navigation
- Loading states for async operations

---

## API Specifications

### Endpoints Required
```http
# Requote Operations
POST   /api/v1/policies/{id}/requote         # Initiate requote
GET    /api/v1/quotes/{id}/changes           # Get detected changes
POST   /api/v1/quotes/{id}/address-selection # Select address option
POST   /api/v1/quotes/{id}/driver-decision   # Include/exclude driver

# Verification Services
POST   /api/v1/verification/address          # Verify address
POST   /api/v1/verification/drivers          # Discover household drivers

# Standard Quote APIs (reused)
GET    /api/v1/quotes/{id}/review            # Enhanced review data
PUT    /api/v1/quotes/{id}                   # Update quote
POST   /api/v1/quotes/{id}/calculate         # Recalculate premium
```

### Real-time Updates
```javascript
// WebSocket channels for requote process
private-quote.{quote_id}.cloning      # Cloning progress
private-quote.{quote_id}.verification # Verification results
private-quote.{quote_id}.changes      # Change notifications
```

---

## Database Schema (Section E)

### Core Tables Used

#### quote
```sql
-- Existing quote table with requote support
-- Key columns for requoting:
-- id, quote_number
-- policy_id                    # Links to source policy
-- quote_type_id                # Identifies as requote
-- is_renewal                   # Renewal indicator
-- renewal_policy_id            # For renewal tracking
-- version_number               # Quote iterations
-- external_reference           # Store change flags
-- effective_date, expiration_date
-- All standard quote fields...
```

#### quote_type
```sql
-- Add requote type if not exists:
INSERT IGNORE INTO quote_type (code, name, description, status_id) VALUES
('REQUOTE', 'Requote', 'Quote created from existing policy', 1),
('RENEWAL', 'Renewal', 'Renewal quote from expiring policy', 1);
```

### Cloning Map Tables

All existing map tables used for data cloning:
```sql
-- Source tables (read from):
-- map_policy_driver → map_quote_driver
-- map_policy_vehicle → map_quote_vehicle  
-- map_policy_coverage → map_quote_coverage

-- Cloning preserves all relationships and attributes
-- Original policy data remains unchanged
```

### Supporting Tables

#### verification
```sql
-- External verification tracking
-- Stores address verification results
-- Tracks driver discovery outcomes
-- Links to quote for change tracking
```

#### address
```sql
-- Verified address storage
-- Original vs verified comparison
-- Standardization results
```

### Change Tracking

```sql
-- Example change flag storage in quote.external_reference:
{
  "changes": {
    "address_changed": true,
    "new_drivers_found": ["driver_id_1", "driver_id_2"],
    "original_address_id": 12345,
    "verified_address_id": 67890,
    "change_timestamp": "2024-01-15T10:30:00Z"
  }
}
```

---

## Implementation Notes

### Dependencies
- Existing quote workflow system
- Address verification service
- Driver discovery service
- Policy data access
- Bind workflow integration

### Migration Considerations
- No data migration required
- Quote table already supports policy linking
- All map tables ready for cloning

### Performance Considerations
- Optimize cloning queries with batch inserts
- Cache policy data during cloning
- Async verification service calls
- Lazy load change notifications
- Index foreign keys for joins

---

## Quality Checklist

### Pre-Implementation
- [x] Quote table has policy_id field
- [x] All cloning tables identified
- [x] Quote workflows ready for reuse
- [x] Verification services available
- [x] Change tracking method defined

### Post-Implementation
- [ ] Requote creates successfully
- [ ] All data clones correctly
- [ ] Changes detected accurately
- [ ] Address verification works
- [ ] Driver discovery functions
- [ ] Visual indicators display
- [ ] Premium recalculates
- [ ] Bind process completes

### Final Validation
- [ ] Complete data preservation
- [ ] Change detection accuracy
- [ ] UI responsiveness
- [ ] Performance acceptable
- [ ] Audit trail complete

### Global Requirements Compliance
- [x] **GR-69**: Producer Portal Architecture - Quote generation patterns
- [x] **GR-52**: Universal Entity Management - Entity reuse for efficiency
- [x] **GR-41**: Database Standards - Audit fields and status management
- [x] **GR-64**: Policy Reinstatement Process - Re-engagement workflow
- [x] **GR-18**: Workflow Requirements - Multi-step process integration