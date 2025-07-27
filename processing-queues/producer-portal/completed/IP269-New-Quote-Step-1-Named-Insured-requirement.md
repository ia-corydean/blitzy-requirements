# IP269-New-Quote-Step-1-Named-Insured - Complete Requirement

---

## **A) WHY – Vision and Purpose**

This is the foundational step in the quote creation process where producers capture and verify the primary insured's information. This step establishes the policyholder's identity and contact details, which are critical for:

- Accurate risk assessment and pricing
- Regulatory compliance and underwriting requirements
- Establishing the primary point of contact for all policy communications
- Enabling household driver verification through DCS integration

The goal is to create an intuitive, efficient data collection process that minimizes manual entry through smart integrations while ensuring data accuracy and completeness.

---

## **B) WHAT – Core Requirements**

The Named Insured step collects essential information about the primary policyholder, integrates with DCS for household driver verification, and establishes the foundation for the quote.

### **1. Personal Information Collection**

- Fields to capture:
  - First Name (required)
  - Middle Name (optional)
  - Last Name (required)
  - Suffix (optional)
  - Date of Birth (required)
  - Gender (required dropdown)
  - Marital Status (required dropdown)

### **2. License Information**

- Driver's License Number (required)
- State of License Issuance (required dropdown)
- License Type (auto-populated based on state)

### **3. Contact Information**

- Residential Address:
  - Street Address (required)
  - City (required)
  - State (required dropdown)
  - ZIP Code (required)
- Primary Phone Number (required)
- Email Address (required)
- Notification Preference (required dropdown: Email/SMS/Phone)

### **4. Business Rules & Validation**

- Date of Birth must indicate driver is at least 16 years old
- License number format validated based on issuing state rules
- Email format validation
- Phone number format validation (10 digits)
- Address validation readiness (implementation in next requirement)

### **5. Save & Navigation**

- Auto-save functionality on field blur with 500ms debounce
- Continue button enabled only when all required fields are completed
- Progress automatically saved to allow resuming incomplete quotes
- Navigation to Step 2 (Drivers) upon successful completion

### **6. DCS Integration**

- Automatic household driver search triggered after form completion
- Uses named insured's address and personal information
- Results populate Step 2 driver selection
- Integration tracking for audit and troubleshooting

---

## Entity Analysis

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|-------|
| driver | Core | Existing | Primary driver entity with is_named_insured flag |
| name | Core | Existing | Stores name components |
| address | Core | Existing | Residential address storage |
| license | Core | Existing | License information |
| communication_method | Supporting | Existing | Phone/email storage |
| quote | Core | Existing | Quote association |
| gender | Reference | Existing | Gender reference lookup |
| marital_status | Reference | Existing | Marital status lookup |
| integration | Core | Existing | DCS integration tracking |
| integration_type | Reference | Existing | Integration type definitions |
| entity | Core | Existing | External DCS data storage |
| entity_type | Reference | Existing | Entity type definitions |

### New Tables Required
None - all functionality supported by existing v5 enhanced schema

### Modifications to Existing Tables
- **name**: Add middle_name column for middle name capture
- **driver**: Add communication_method_id for notification preference

### Relationships Identified
- quote → map_quote_driver → driver (quote to driver association)
- driver → name (driver name information)
- driver → license (license details)
- driver → address (via existing relationships)
- driver → communication_method (notification preference)
- driver → gender (gender reference)
- driver → marital_status (marital status reference)
- driver → integration (DCS verification tracking)

---

## Field Mappings (Section C)

### Backend Mappings

#### Personal Information Fields

##### Name Components
- **Backend Mapping**: 
  ```
  get driver.name_id from driver
  -> get name.* by driver.name_id
  -> return first_name, middle_name, last_name, suffix
  -> validate required fields populated
  ```

##### Date of Birth and Demographics
- **Backend Mapping**:
  ```
  get driver.date_of_birth from driver
  -> validate age >= 16 years
  -> get gender.name via driver.gender_id
  -> get marital_status.name via driver.marital_status_id
  -> return formatted demographics
  ```

#### License Information

##### License Details
- **Backend Mapping**:
  ```
  get driver.license_id from driver
  -> get license.* by driver.license_id
  -> validate license_number format by state rules
  -> return license_number, state_code, license_type
  ```

#### Contact Information

##### Address Data
- **Backend Mapping**:
  ```
  get driver address association
  -> get address.* by relationship
  -> return line1, city, state_code, zip_code
  -> set is_validated flag for future validation
  ```

##### Communication Methods
- **Backend Mapping**:
  ```
  get map_driver_communication_method entries
  -> filter by communication_method_type (phone/email)
  -> get primary phone and email values
  -> get notification preference via driver.communication_method_id
  ```

#### DCS Integration

##### Household Driver Search
- **Backend Mapping**:
  ```
  create integration record:
  -> integration_type_id = 'HOUSEHOLD_SEARCH'
  -> entity_type_id = 'THIRD_PARTY_INTEGRATION'
  -> entity_id = driver.id
  -> status_id = 'PENDING'
  
  execute DCS API call:
  -> log request/response in integration_log
  -> store DCS results in entity table
  -> update integration status
  -> return household drivers for Step 2
  ```

### Implementation Architecture

**Form-First Design**: Multi-section form with progressive disclosure, client-side validation, and auto-save functionality to ensure data persistence across user sessions.

**Existing Schema Leverage**: Maximizes use of v5 enhanced database schema, requiring only 2 new columns while supporting all form functionality through existing tables and relationships.

**DCS Integration Pattern**: Implements universal entity management (GR-52) for external DCS data, using integration tracking tables for audit trail and entity storage for returned driver information.

**Performance Optimization**: Field-level auto-save with debouncing, efficient relationship queries using existing indexes, and asynchronous DCS API calls to prevent blocking.

### Integration Specifications

#### DCS Household Driver Verification

**Entity Type**: THIRD_PARTY_INTEGRATION  
**Integration Type**: HOUSEHOLD_SEARCH  
**Provider**: Data Collection Services (DCS)  
**Pattern**: Universal Entity Management (GR-52)

**Integration Flow**:
1. Form completion triggers integration record creation
2. API call with named insured data
3. Response logged in integration_log
4. Household drivers stored in entity table
5. Results available for Step 2 driver selection

---

## API Specifications

### Endpoints Required
```http
POST   /api/v1/quotes                      # Initialize quote with named insured
GET    /api/v1/quotes/{id}/named-insured   # Retrieve named insured data
PUT    /api/v1/quotes/{id}/named-insured   # Update named insured information
POST   /api/v1/quotes/{id}/auto-save       # Auto-save form progress
POST   /api/v1/quotes/{id}/validate        # Validate form completion
POST   /api/v1/quotes/{id}/dcs-search      # Trigger DCS household search
GET    /api/v1/reference/genders           # Gender options
GET    /api/v1/reference/marital-statuses  # Marital status options
GET    /api/v1/reference/states            # State codes for dropdowns
GET    /api/v1/reference/notification-preferences # Communication preferences
```

### Real-time Updates
```javascript
// WebSocket channels
private-quote.{id}.named-insured           # Named insured data updates
private-quote.{id}.validation              # Form validation updates
private-quote.{id}.dcs-integration         # DCS search status
```

---

## Database Schema (Section E)

### Modified Tables Only

#### ALTER TABLE name
```sql
-- Add middle name support for form field
ALTER TABLE name
ADD COLUMN middle_name VARCHAR(50) NULL COMMENT 'Middle name - optional form field'
AFTER first_name;

-- Add index for name searches
ALTER TABLE name
ADD INDEX idx_full_name (last_name, first_name, middle_name);
```

#### ALTER TABLE driver
```sql
-- Add notification preference
ALTER TABLE driver
ADD COLUMN communication_method_id BIGINT UNSIGNED NULL 
  COMMENT 'Preferred notification method - Email/SMS/Phone',
ADD CONSTRAINT fk_driver_communication_method 
  FOREIGN KEY (communication_method_id) REFERENCES communication_method(id);

-- Add index for preference lookups
ALTER TABLE driver
ADD INDEX idx_communication_method (communication_method_id);
```

### Existing Schema Utilization

The v5 enhanced schema already provides:
- **name table**: first_name, last_name, suffix fields
- **driver table**: name_id, license_id, date_of_birth, gender_id, marital_status_id, is_named_insured
- **license table**: license_number, state_code, license_type_id
- **address table**: line1, city, state_code, zip_code, is_validated
- **communication_method table**: value, communication_method_type_id
- **gender & marital_status tables**: Reference data with code/name/description
- **integration tables**: Complete framework for DCS integration tracking
- **entity tables**: Storage for external DCS driver data

---

## Implementation Notes

### Dependencies
- Quote creation workflow must be initiated first
- Reference data (gender, marital status, states) must be populated
- DCS API credentials configured in configuration table
- Communication method types established

### Migration Considerations
- Simple ALTER TABLE statements for 2 new columns
- No data migration required
- Backward compatible changes

### Performance Considerations
- Form validation performs client-side first, server-side on submit
- Auto-save uses debouncing to minimize API calls
- DCS integration runs asynchronously
- Existing indexes support all query patterns

---

## Quality Checklist

### Pre-Implementation
- [x] All UI fields mapped to database columns
- [x] Existing entities reused where possible (leveraged v5 schema)
- [x] Reference tables created for all ENUMs (using existing)
- [x] Naming conventions followed consistently
- [x] Relationships properly defined with foreign keys

### Post-Implementation
- [x] All foreign keys have proper constraints
- [x] Appropriate indexes for expected query patterns
- [x] Audit fields included on all tables (existing)
- [x] Status management consistent across tables
- [x] Entity catalog updated with new entities (none needed)
- [x] Architectural decisions documented (DCS pattern)

### Final Validation
- [x] Backend mappings complete and accurate
- [x] Database schema follows all standards
- [x] No redundant tables or columns created
- [x] Performance considerations addressed
- [x] Documentation updated

### Global Requirements Compliance
- [x] **GR-52**: Universal Entity Management for DCS integration
- [x] **GR-53**: DCS Integration Architecture patterns followed
- [x] **GR-41**: Database Standards - minimal changes, proper constraints
- [x] **GR-69**: Producer Portal Architecture - quote creation workflow
- [x] **GR-44**: Communication Architecture - notification preferences
- [x] **GR-33**: Data Services patterns for auto-save functionality