# IP270-Policies - Complete Requirement

---

## **A) WHY – Vision and Purpose**

The Policies feature provides a comprehensive policy management system that enables producers to efficiently locate, review, and service insurance policies. This centralized platform eliminates the need to navigate between multiple systems, reducing service time and improving customer satisfaction.

The purpose is to:
- Enable rapid policy location through powerful search and filtering capabilities
- Provide complete policy visibility across all aspects (details, payments, documents, claims)
- Streamline policy servicing with integrated payment processing and cancellation workflows
- Maintain comprehensive audit trails for all policy activities
- Support mobile and desktop users with responsive, intuitive interfaces

By consolidating all policy information and actions into a single, well-organized interface with contextual navigation, the system empowers producers to deliver superior customer service while maintaining operational efficiency.

---

## **B) WHAT – Core Requirements**

### **1. Policy Search & Filtering**

The search experience must support rapid policy location through:

- **Keyword Search** supporting multiple identifiers:
  - Policy number (exact or partial match)
  - Insured name (first, last, or full)
  - Phone number (any format)
  - Email address
  - Driver's license number
  - Vehicle Identification Number (VIN)

- **Advanced Filters**:
  - Status (multi-select): In Force, Pending Cancellation, Cancelled, Expired
  - Effective Date: Single date or date range selection
  - Expiration Date: Single date or date range selection
  - Clear visual indicators for active filters

- **Results Display**:
  - Sortable columns: Policy Number, Insured Name, Producer Number, Effective Date, Cancellation Date, Status
  - Color-coded status pills for quick visual scanning
  - Pagination with 10 results per page default
  - Real-time search with partial matching

### **2. Policy Details Tab**

Comprehensive policy overview displaying:

- **Policy Header**:
  - Insured name with policy number
  - Status badge and Do Not Call indicator
  - Action buttons: More Actions dropdown, Cancel Policy

- **Overview Panel** (Right Rail):
  - Billing summary: Amount due, remaining balance, fees
  - Next payment date with installment schedule
  - Important dates: Effective, Expiration, Inception

- **Upcoming Payment Section**:
  - Payment amount and due date
  - Make a Payment quick action button

- **Primary Insured Information**:
  - Personal details: Name, DOB, license, gender, marital status
  - Contact information: Address, phones, email, notification preferences
  - Policy specifics: Term, discounts (Paperless, EFT), prior insurance status
  - Eligible discounts list

- **Coverage Details**:
  - Policy-wide coverages (BI, PD, UM/UIM, PIP)
  - Vehicle-specific coverages grouped by vehicle
  - Premium display per coverage line
  - Total premium calculation

### **3. Drivers & Vehicles Tab**

Complete listing of all policy participants and assets:

- **Drivers Section**:
  - List view: Name, primary indicator, DOB, license, violation points, status
  - Expandable detail panel showing:
    - Driver info: Class, gender, age, marital status, relationship
    - License details: State, country, number, years of experience
    - Employment info: Status, occupation, employer

- **Vehicles Section**:
  - List view: Year/Make/Model, VIN, plate number
  - Expandable detail panel showing:
    - Vehicle image (if available)
    - Limits & deductibles for each coverage
    - Premium breakdown by coverage
    - Total vehicle premium

- **Applied Discounts**:
  - Complete list of policy discounts
  - Discount amounts or percentages

### **4. Payment History Tab**

Financial transaction transparency including:

- **Transaction Table**:
  - Date, type, method, confirmation number, amount, balance, status
  - Color-coded status indicators

- **Filtering Options**:
  - Term: Current or Previous
  - Category: Installment, Billing Fee, Endorsement Fee
  - Status: Paid, Upcoming, Failed, Cancelled

- **Transaction Details** (Expandable):
  - General info: Type, status, date, description
  - Payment info: Method, confirmation, amount, masked account details
  - Additional info: Billing cycle, autopay status, payment actions

### **5. Documents Tab**

Document management capabilities:

- **Document List**:
  - File type icon, name, date added
  - Search by name or date
  - Three-dot menu for actions (delete)
  - On-demand ID card generation

- **Upload Functionality**:
  - Document type selection dropdown
  - Drag-and-drop or file picker
  - File validation and size limits

- **Document Viewer**:
  - Preview capability
  - Metadata panel: Name, policy number, description, assignments
  - Document history log

### **6. Claims Tab**

Claims visibility and management:

- **Claims List**:
  - Loss number, description, date, assigned adjuster
  - Submit Claim action button

- **Claim Details** (Expandable):
  - Loss details: Number, description, date
  - Financial info: Paid out amount, open/closed lines
  - Adjuster assignment

- **Empty State**:
  - Friendly message when no claims exist
  - Clear path to submit new claim

### **7. Endorsements Tab**

Policy modification tracking:

- **Endorsements List**:
  - Endorsement number, type, message, effective date
  - Chronological ordering

- **Submit Endorsement**:
  - Prominent action button
  - Routes to endorsement workflow

### **8. Cancel Policy Workflow**

Guided cancellation process:

- **Cancellation Form**:
  - Effective date selection
  - Reason dropdown with common options
  - Additional notes field
  - Confirmation screen with policy details

- **Post-Cancellation States**:
  - Visual status updates
  - Banner notifications
  - Payment/refund calculations
  - Reinstatement eligibility display

### **9. Make Payment Workflow**

Flexible payment processing:

- **Payment Methods**:
  - Insured E-Check: Routing and account numbers
  - Producer E-Check: No additional info required
  - Credit Card: Full card details and billing address

- **Payment Options**:
  - Pay in full
  - Minimum payment
  - Custom amount

- **Validation & Fees**:
  - Real-time field validation
  - Optional convenience fee for credit cards
  - Clear error messaging

### **10. Right Panel Navigation**

Context-aware quick actions:

- **Sections**:
  - Overview: Billing and dates summary
  - Activity: Chronological policy events log
  - Notes: View and add producer notes
  - Settings: Update contact info and payment methods

- **Functionality**:
  - Persistent across tab navigation
  - Collapsible for full-screen viewing
  - Real-time updates

---

## Entity Analysis

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|-------|
| policy | Core | Existing | Complete policy information |
| policy_type | Reference | Existing | Policy categorization |
| search_history | Supporting | Existing | Search query tracking |
| driver | Core | Existing | All driver information |
| vehicle | Core | Existing | Vehicle details |
| coverage | Core | Existing | Coverage types and limits |
| transaction | Core | Existing | Payment transactions |
| payment_method | Reference | Existing | Payment options |
| document | Core | Existing | Document storage |
| file | Supporting | Existing | Physical file storage |
| loss | Core | Existing | Claims information |
| claimant | Supporting | Existing | Claim participants |
| endorsement | Core | Existing | Policy modifications |
| cancellation | Supporting | Existing | Cancellation tracking |
| cancellation_reason | Reference | Existing | Cancellation codes |
| note | Supporting | Existing | Policy notes |
| activity/audit | Supporting | Existing | Activity logging |
| discount | Supporting | Existing | Applied discounts |
| fee | Supporting | Existing | Fee calculations |
| map_policy_driver | Map | Existing | Policy-driver links |
| map_policy_vehicle | Map | Existing | Policy-vehicle links |
| map_policy_coverage | Map | Existing | Policy-coverage links |
| map_policy_document | Map | Existing | Policy-document links |
| map_policy_installment | Map | Existing | Payment schedules |

### New Tables Required
None - all functionality supported by existing infrastructure

### Modifications to Existing Tables
None - comprehensive existing schema supports all requirements

### Relationships Identified
- policy → has many → drivers (via map_policy_driver)
- policy → has many → vehicles (via map_policy_vehicle)
- policy → has many → coverages (via map_policy_coverage)
- policy → has many → documents (via map_policy_document)
- policy → has many → transactions
- policy → has many → losses (claims)
- policy → has many → endorsements
- policy → has one → cancellation
- driver → has many → violations
- vehicle → has many → coverages
- transaction → belongs to → payment_method

---

## Field Mappings (Section C)

### Backend Mappings

#### Policy Search

##### Multi-field Search
- **Backend Mapping**: 
  ```
  receive search query
  -> search policy.policy_number (indexed)
  -> search driver names via map_policy_driver
  -> search communication_method for phone/email
  -> search license.number for DL matches
  -> search vehicle.vin for VIN matches
  -> apply status filters if selected
  -> apply date range filters if specified
  -> return paginated results with sorting
  -> store query in search_history
  ```

#### Policy Details Tab

##### Load Policy Overview
- **Backend Mapping**: 
  ```
  get policy.id from selection
  -> load complete policy record
  -> get primary insured from map_policy_driver
     where is_primary = true
  -> calculate billing summary from transactions
  -> get next payment from map_policy_installment
  -> get all coverages from map_policy_coverage
  -> calculate total premium with discounts
  -> return consolidated policy view
  ```

#### Drivers & Vehicles Tab

##### Display Drivers and Vehicles
- **Backend Mapping**: 
  ```
  get policy.id
  -> get all drivers from map_policy_driver
  -> for each driver:
     - get name, license, violations
     - get employment information
  -> get all vehicles from map_policy_vehicle
  -> for each vehicle:
     - get coverages and deductibles
     - calculate vehicle premium
  -> get all applied discounts
  -> return organized display data
  ```

#### Payment History Tab

##### Load Transaction History
- **Backend Mapping**: 
  ```
  get policy.id
  -> get all transactions for policy
  -> join with transaction_type
  -> join with payment_method
  -> apply filters (term, category, status)
  -> calculate running balance
  -> return paginated transaction list
  ```

#### Documents Tab

##### Document Management
- **Backend Mapping**: 
  ```
  get policy.id
  -> get documents from map_policy_document
  -> join with document and file tables
  -> for upload:
     - validate file type and size
     - create file record
     - create document record
     - link via map_policy_document
  -> for ID card:
     - generate on demand
     - return as downloadable file
  -> track all actions in audit
  ```

#### Cancel Policy Workflow

##### Process Cancellation
- **Backend Mapping**: 
  ```
  get policy.id
  -> validate policy status allows cancellation
  -> create cancellation record:
     - effective_date
     - cancellation_reason_id
     - notes
  -> update policy.status_id
  -> calculate refund/balance
  -> create transaction records
  -> send notifications
  -> return confirmation
  ```

#### Make Payment

##### Process Payment
- **Backend Mapping**: 
  ```
  get policy.id and payment details
  -> validate payment method
  -> calculate total with fees
  -> create transaction record
  -> update payment_method if new
  -> process through payment gateway
  -> update policy balance
  -> create confirmation
  -> return transaction details
  ```

### Implementation Architecture

The policies system leverages the comprehensive existing infrastructure:

1. **Search Service**: Optimized multi-table queries with caching
2. **Policy Aggregation**: Efficient data loading with relationship management
3. **Transaction Engine**: ACID-compliant payment processing
4. **Document Service**: File management with metadata tracking
5. **Activity Logger**: Real-time audit trail generation
6. **Notification System**: Event-driven updates for policy changes

### Integration Specifications

**Search Optimization**:
- Elasticsearch integration for complex queries
- Redis caching for frequent searches
- Database indexes on all searchable fields

**Payment Gateway**:
- PCI-compliant credit card processing
- ACH integration for e-check payments
- Webhook handling for async confirmations

**Document Generation**:
- PDF generation service for ID cards
- Template engine for document creation
- CDN integration for file serving

**Real-time Updates**:
- WebSocket connections for activity panel
- Event broadcasting for status changes
- Queue workers for background processing

---

## **D) User Experience (UX) & Flows**

### **1. Policy Search Flow**

1. User enters search criteria (policy number, name, etc.)
2. System performs real-time search across multiple fields
3. Results display with sortable columns
4. User applies filters to refine results
5. Clicking a policy navigates to details view

### **2. Policy Navigation Flow**

1. User lands on Policy Details tab
2. Right panel shows billing overview
3. User navigates between tabs without losing context
4. Each tab loads relevant data dynamically
5. Right panel remains accessible throughout

### **3. Payment Processing Flow**

1. User clicks "Make a Payment"
2. Selects payment method (E-Check or Credit Card)
3. Enters payment details with validation
4. Reviews amount (full, minimum, or custom)
5. Submits payment with loading indicator
6. Receives confirmation or error handling

### **4. Cancellation Flow**

1. User clicks "Cancel Policy"
2. Enters effective date
3. Selects cancellation reason
4. Adds optional notes
5. Reviews confirmation screen
6. Policy status updates immediately

### **5. Document Management Flow**

1. User navigates to Documents tab
2. Views existing documents
3. Uploads new documents via drag-drop
4. Downloads or previews documents
5. Deletes with confirmation

### **6. Mobile Experience**

- Responsive design adapts to screen size
- Horizontal scrolling for wide tables
- Collapsible sections for space efficiency
- Touch-optimized interactions
- Maintained functionality across devices

### **7. UI Presentation Guidelines**

- Status pills with consistent color coding
- Card-based layouts for information grouping
- Progressive disclosure for complex data
- Sticky headers and navigation
- Loading states for all async operations
- Clear error messaging with recovery paths
- Accessibility compliance (WCAG 2.1)
- Print-friendly document views

---

## API Specifications

### Endpoints Required
```http
# Search and List
GET    /api/v1/policies/search              # Multi-field policy search
GET    /api/v1/policies/{id}                # Single policy details
GET    /api/v1/policies/{id}/overview       # Policy overview summary

# Tab-specific Data
GET    /api/v1/policies/{id}/drivers        # Drivers and vehicles
GET    /api/v1/policies/{id}/transactions   # Payment history
GET    /api/v1/policies/{id}/documents      # Document list
GET    /api/v1/policies/{id}/claims         # Claims list
GET    /api/v1/policies/{id}/endorsements   # Endorsements list

# Actions
POST   /api/v1/policies/{id}/cancel         # Cancel policy
POST   /api/v1/policies/{id}/payment        # Make payment
POST   /api/v1/policies/{id}/documents      # Upload document
DELETE /api/v1/policies/{id}/documents/{docId} # Delete document
POST   /api/v1/policies/{id}/notes          # Add note
PUT    /api/v1/policies/{id}/settings       # Update settings
```

### Real-time Updates
```javascript
// WebSocket channels for live updates
private-policy.{policy_id}.activity     # Activity log updates
private-policy.{policy_id}.status       # Status changes
private-policy.{policy_id}.payments     # Payment updates
```

---

## Database Schema (Section E)

### Core Tables Used

#### policy
```sql
-- Comprehensive policy table with all required fields
-- Key columns:
-- id, policy_number (unique, indexed)
-- policy_type_id, program_id, producer_id
-- effective_date, expiration_date, inception_date
-- cancellation_date, cancellation_reason_id
-- total_premium, total_fees, total_discount
-- status_id, created_by, updated_by
-- Indexes on all searchable fields
```

#### search_history
```sql
-- Tracks user search queries
-- Key columns:
-- id, user_id, query, search_type
-- results_count, selected_result_id
-- created_at
```

#### transaction
```sql
-- Complete payment tracking
-- Key columns:
-- id, policy_id, transaction_type_id
-- amount, balance, confirmation_number
-- payment_method_id, status_id
-- transaction_date, created_at
```

#### driver
```sql
-- Driver information with violations
-- Key columns:
-- id, name_id, license_id
-- date_of_birth, gender, marital_status_id
-- violation_points, employment_status
```

#### vehicle
```sql
-- Vehicle details and coverage
-- Key columns:
-- id, year, make, model, vin
-- plate_number, usage_type_id
-- garaging_address_id
```

### Relationship Tables

All existing map tables provide flexible associations:
- map_policy_driver (includes is_primary, is_excluded flags)
- map_policy_vehicle (maintains vehicle order)
- map_policy_coverage (separates policy vs vehicle level)
- map_policy_document (document associations)
- map_policy_installment (payment schedules)

### Supporting Tables

Complete supporting infrastructure:
- cancellation (tracks cancellation details)
- cancellation_reason (reason codes)
- note (policy notes with timestamps)
- activity/audit (comprehensive logging)
- discount (applied discounts)
- fee (fee calculations)
- loss (claims data)
- endorsement (policy changes)

---

## Implementation Notes

### Dependencies
- Existing policy management infrastructure
- Payment gateway integration
- Document storage system
- Search indexing service
- Notification system

### Migration Considerations
- No data migration required
- All tables and relationships exist
- Indexes already optimized

### Performance Considerations
- Implement query result caching
- Use pagination for all lists
- Lazy load tab content
- Optimize search with Elasticsearch
- Background jobs for heavy operations
- CDN for document serving
- Database connection pooling
- Index all foreign keys

---

## Quality Checklist

### Pre-Implementation
- [x] All UI fields mapped to existing columns
- [x] 40+ tables identified and verified
- [x] No new tables required
- [x] Search optimization planned
- [x] Mobile responsiveness considered

### Post-Implementation
- [ ] Search returns results in <2 seconds
- [ ] All tabs load completely
- [ ] Payment processing functions
- [ ] Cancellation workflow completes
- [ ] Documents upload successfully
- [ ] Real-time updates working

### Final Validation
- [ ] Multi-field search accurate
- [ ] Status filtering works correctly
- [ ] Payment calculations accurate
- [ ] Activity logging comprehensive
- [ ] Mobile experience optimized

### Global Requirements Compliance
- [x] **GR-69**: Producer Portal Architecture - Complete policy management patterns
- [x] **GR-52**: Universal Entity Management - Leverages all existing entities
- [x] **GR-41**: Database Standards - Uses status_id patterns and audit fields
- [x] **GR-44**: Communication Architecture - Payment and cancellation notifications
- [x] **GR-64**: Policy Reinstatement Process - Cancellation workflow implemented