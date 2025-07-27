# IP269-Bind-Document-Upload - Complete Requirement

## **A) WHY – Vision and Purpose**

The Document Upload feature enables users to submit required documentation digitally during the insurance policy binding process. This streamlines the document intake process by eliminating manual paperwork, reducing delays in quote processing, and providing clear visual confirmation of upload status.

The purpose is to:
- Enable digital submission of required documents (proof of prior insurance, driver's licenses, vehicle registrations)
- Reduce friction and delays in the binding process through intuitive upload interfaces
- Provide transparency with visual confirmations and status indicators
- Ensure compliance tracking while allowing flexible progression through suspense creation

This digital transformation of document collection accelerates policy issuance, improves user experience, and maintains comprehensive audit trails for regulatory compliance.

---

## **B) WHAT – Core Requirements**

### **1. Document Requirements Display**

- Display dynamically determined list of required documents based on:
  - Policy parameters and coverage selections
  - Program level definitions
- Each document requirement shows:
  - Document type name and description
  - Upload button with drag-and-drop zone

### **2. Upload Functionality**

- **Upload Methods**:
  - Drag and drop files directly onto upload zones
  - Click to browse and select files
  - Support for multiple file selection where appropriate
- **File Validation**:
  - Client-side format checking for immediate feedback (validates PDF, JPEG, PNG)
  - Server-side validation for security
  - File size enforcement with clear error messages (10MB limit)
  - Duplicate detection to prevent re-uploads
- **Progress Indicators**:
  - Real-time upload progress bars
  - Success confirmation with thumbnail preview
  - Error states with actionable messages

### **3. Document Management**

- **Post-Upload Actions**:
  - View uploaded document thumbnails
  - Remove documents with 'X' button
  - Replace existing documents
  - Download uploaded documents
- **Status Tracking**:
  - Visual indicators for upload completion
  - Running count of uploaded vs required documents
  - Clear identification of missing documents

### **4. Business Rules & Validation**

- **Navigation Rules**:
  - Backward navigation shows warning dialog
  - Warns that policy will need re-rating
  - Confirms that bind progress (uploads, signatures) will be purged
- **Continuation Rules**:
  - Allow progression without all documents
  - Create suspense items for missing required documents
  - Display warning about suspense creation
  - Track incomplete items for follow-up
- **Document Requirements**:
  - Proof of Prior Insurance (if applicable)
  - Driver's License (for each driver)
  - Vehicle Registration (for each vehicle)
  - Additional documents as determined by underwriting rules

### **5. Save & Navigation**

- Auto-save uploaded documents immediately
- Preserve upload state during session
- Enable "Continue" button regardless of completion
- Show suspense warning if documents missing
- Clear navigation to next binding step

---

## Entity Analysis

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|-------|
| document | Core | Existing | Stores document metadata and relationships |
| document_type | Reference | Existing | Defines document categories |
| file | Core | Existing | Physical file storage records with storage_location |
| file_type | Reference | Existing | Allowed file formats and limits |
| suspense | Supporting | Existing | Tracks missing items with entity linking |
| map_entity_document | Map | Existing | Universal document linking table |
| entity | Core | Existing | Universal entity reference |
| entity_type | Reference | Existing | Defines entity categories |
| quote | Core | Existing | Parent entity for bind documents |
| policy | Core | Existing | Alternative parent for documents |
| driver | Core | Existing | Driver entities for license documents |
| vehicle | Core | Existing | Vehicle entities for registration documents |
| program | Core | Existing | Defines document requirements |

### Document Mapping Approach
The system uses `map_entity_document` for all document associations:
- **Universal Pattern**: One mapping table for all entity types
- **Flexible Assignment**: Documents can be linked to quotes, policies, vehicles, or drivers
- **Entity Identification**: Uses entity_id with entity_type context
- **No Redundancy**: Avoids creating multiple mapping tables

### Relationships Identified
- entity → has many → documents (via map_entity_document)
- document → belongs to → document_type
- document → has one → file
- file → belongs to → file_type
- quote/policy/vehicle/driver → are types of → entity
- quote → has many → suspenses (via entity_type/entity_id)
- program → defines → document requirements

---

## Field Mappings (Section C)

### Backend Mappings

#### Document Requirements List

##### Required Documents Display
- **Backend Mapping**: 
  ```
  get quote.id, quote.program_id from quote
  -> get program rules for document requirements
  -> evaluate based on:
     - quote.state_id
     - drivers count and ages
     - vehicles types
     - prior_insurance_indicator
  -> return document_type list with requirements
  ```

#### Upload Section

##### File Upload Handler
- **Backend Mapping**: 
  ```
  receive file upload with context (entity_type, entity_id)
  -> validate file_type (PDF, JPEG, PNG)
  -> check file size <= 10MB
  -> create file record with:
     - name, path, size, mime_type
     - hash for deduplication
     - metadata JSON
     - storage_location (local/s3/etc)
  -> create document record with:
     - document_type_id
     - file_id
     - status_id = active
  -> create map_entity_document with:
     - entity_id = context entity_id (quote.id, driver.id, vehicle.id, etc.)
     - document_id
  -> return success with thumbnail URL
  ```

##### Document Assignment Examples
- **Quote-Level Documents**:
  ```
  map_entity_document:
  - entity_id = quote.id
  - document_id = proof_of_prior_insurance.id
  ```

- **Driver-Specific Documents**:
  ```
  map_entity_document:
  - entity_id = driver.id
  - document_id = driver_license.id
  ```

- **Vehicle-Specific Documents**:
  ```
  map_entity_document:
  - entity_id = vehicle.id
  - document_id = vehicle_registration.id
  ```

##### Document Removal
- **Backend Mapping**: 
  ```
  get document.id
  -> soft delete via status_id = deleted
  -> maintain file record for audit
  -> remove from UI display
  ```

#### Suspense Creation

##### Missing Documents Check
- **Backend Mapping**: 
  ```
  get required document_types for quote
  -> get uploaded documents for quote via map_entity_document
  -> check driver documents via driver entity_ids
  -> check vehicle documents via vehicle entity_ids
  -> compare lists
  -> for each missing required:
     - create suspense record:
       - suspense_type_id = 'missing_document'
       - description = document name and entity context
       - entity_type = 'quote'
       - entity_id = quote.id
       - due_date = effective_date or configurable days
  -> return suspense count
  ```

### Implementation Architecture

The document upload system leverages the existing file and document infrastructure with a service layer that handles:

1. **Dynamic Requirements Engine**: Evaluates policy parameters to determine required documents
2. **File Processing Service**: Handles uploads, validation, and storage with location tracking
3. **Thumbnail Generation**: Creates preview images for visual confirmation
4. **Entity-Aware Assignment**: Links documents to appropriate entities (quote, driver, vehicle)
5. **Suspense Management**: Tracks and creates items for missing documents with full entity context
6. **Progress Tracking**: Maintains upload state throughout the session

### Integration Specifications

**File Storage Integration**:
- Files stored in designated upload directory or cloud storage
- Paths tracked in file.path column
- Storage location tracked for CDN/cloud integration
- Supports multiple storage backends (local, S3, etc.)

**Validation Services**:
- MIME type checking against file_type table
- File size enforcement at application level
- Error messages only on validation failure
- Virus scanning integration point (future)

**Document Requirements API**:
- Program-based rules engine
- State-specific requirement overrides
- Dynamic evaluation based on quote data
- Entity-specific requirements (per driver, per vehicle)

**Entity Mapping Service**:
- Universal document assignment via map_entity_document
- Context-aware linking based on document type
- Support for multiple entity types without schema changes

**Suspense Tracking**:
- Entity-aware suspense creation using entity_type/entity_id
- Descriptive suspense items with due dates
- Integration with follow-up workflows
- Clear entity context for resolution

---

## **D) User Experience (UX) & Flows**

### **1. Normal Upload Flow**

1. User lands on "Upload Documents" step in binding process
2. System displays required documents based on policy parameters
3. Each document shown in card with upload zone
4. Driver/Vehicle specific documents clearly labeled
5. User drags files or clicks to browse
6. Files upload with progress indicator
7. Success shown with thumbnail preview
8. System automatically assigns to correct entity
9. User can remove/replace as needed
10. Continue button always enabled
11. Warning shown if documents missing
12. Suspense created for missing items

### **2. Return/Edit Flow**

1. User returns to in-progress bind
2. Previously uploaded documents shown with thumbnails
3. Documents grouped by entity (quote-level, per driver, per vehicle)
4. User can:
   - Add missing documents
   - Replace existing documents
   - Remove incorrect uploads
5. Changes save automatically
6. Progress preserved from previous session

### **3. Backward Navigation Flow**

1. User clicks back to quote steps
2. Warning dialog appears:
   - "Returning will require re-rating"
   - "All bind progress will be lost"
3. User confirms or cancels
4. If confirmed, bind progress cleared

### **4. UI Presentation Guidelines**

- Card-based layout for each document type
- Entity context shown (e.g., "Driver: John Smith - License")
- Drag-drop zones with clear visual indicators
- Thumbnail previews at 120x120px
- Progress bars during upload
- Success checkmarks on completion
- Error messages inline with upload zones (only on failure)
- Mobile-responsive with stacked cards
- Accessibility compliant with ARIA labels

---

## API Specifications

### Endpoints Required
```http
GET    /api/v1/quotes/{id}/document-requirements    # Get required documents
GET    /api/v1/quotes/{id}/documents                # List all uploaded documents
POST   /api/v1/documents/upload                      # Upload new document
DELETE /api/v1/documents/{id}                       # Remove document
GET    /api/v1/documents/{id}/download              # Download document
POST   /api/v1/quotes/{id}/check-documents          # Validate and create suspenses
GET    /api/v1/entities/{type}/{id}/documents       # Get entity-specific documents
```

### Document Requirements Response
```json
{
  "documents": [
    {
      "document_type_id": 123,
      "document_type_name": "Driver License",
      "entity_context": "Driver: John Smith"
    }
  ]
}
```

### Upload Payload
```json
{
  "file": "multipart/form-data",
  "document_type_id": 123,
  "entity_type": "driver|vehicle|quote|policy",
  "entity_id": 456,
  "metadata": {
    "description": "Front of license",
    "tags": ["primary", "verified"]
  }
}
```

### Real-time Updates
```javascript
// WebSocket channels for upload progress
private-quote.{quote_id}.documents    # Document upload status updates
```

---

## Database Schema (Section E)

### Core Tables Used

#### document
```sql
-- Stores document metadata and relationships
-- Key columns:
-- id, document_type_id, file_id
-- is_signed, signed_at, expiration_date
-- status_id, created_by, updated_by, created_at, updated_at
```

#### file
```sql
-- Physical file storage records
-- Key columns:
-- id, file_type_id, name, path, size, mime_type
-- hash, metadata (JSON), storage_location
-- status_id, created_by, updated_by, created_at, updated_at
```

#### map_entity_document
```sql
-- Universal document mapping table
-- Key columns:
-- id, entity_id, document_id
-- status_id, created_by, updated_by
-- created_at, updated_at
```

#### entity
```sql
-- Universal entity reference
-- Key columns:
-- id, entity_type_id
-- status_id, created_by, updated_by, created_at, updated_at
```

#### suspense
```sql
-- Suspense tracking with entity linking support
-- Key columns:
-- id, suspense_type_id, route_path
-- description, entity_type, entity_id, due_date
-- status_id, created_by, updated_by, created_at, updated_at
```

### Query Examples

#### Get All Documents for a Quote
```sql
-- Includes documents at all levels (quote, drivers, vehicles)
SELECT 
    d.*,
    dt.name as document_type_name,
    med.entity_id,
    f.storage_location,
    CASE 
        WHEN med.entity_id = q.id THEN 'Quote'
        WHEN med.entity_id IN (SELECT id FROM driver WHERE quote_id = q.id) THEN 'Driver'
        WHEN med.entity_id IN (SELECT id FROM vehicle WHERE quote_id = q.id) THEN 'Vehicle'
    END as entity_context
FROM quote q
JOIN map_entity_document med ON (
    med.entity_id = q.id 
    OR med.entity_id IN (SELECT id FROM driver WHERE quote_id = q.id)
    OR med.entity_id IN (SELECT id FROM vehicle WHERE quote_id = q.id)
)
JOIN document d ON med.document_id = d.id
JOIN document_type dt ON d.document_type_id = dt.id
JOIN file f ON d.file_id = f.id
WHERE q.id = ? AND d.status_id = 1;
```

#### Get Suspenses for a Quote
```sql
-- Get all suspense items for a quote with full context
SELECT 
    s.*,
    st.name as suspense_type_name,
    st.code as suspense_type_code,
    s.description,
    s.due_date,
    DATEDIFF(s.due_date, CURDATE()) as days_until_due
FROM suspense s
JOIN suspense_type st ON s.suspense_type_id = st.id
WHERE s.entity_type = 'quote' 
AND s.entity_id = ?
AND s.status_id = 1
ORDER BY s.due_date ASC;
```

---

## Implementation Notes

### Dependencies
- Existing file upload infrastructure must be configured
- Document storage directory must have write permissions
- Thumbnail generation library required (frontend)
- Program rules for document requirements must be defined
- Entity records must exist before document assignment

### Performance Considerations
- Chunked uploads for large files
- Asynchronous thumbnail generation
- CDN integration for document serving based on storage_location
- Index on map_entity_document.entity_id for fast lookups
- Index on suspense.entity_type/entity_id for efficient queries
- Consider composite index on (entity_id, document_id)
- Caching of document requirements per program

---

## Quality Checklist

### Pre-Implementation
- [x] All UI fields mapped to database columns
- [x] Existing entities reused completely
- [x] Universal mapping approach validated
- [x] Database has all required fields
- [x] Naming conventions followed consistently
- [x] Relationships properly defined with foreign keys

### Post-Implementation
- [ ] File upload validates format and size
- [ ] Thumbnails generate correctly
- [ ] Documents link to correct entities
- [ ] Suspenses create with proper entity linking
- [ ] Navigation warnings function properly
- [ ] Entity context displays properly
- [ ] Progress preserves across sessions
- [ ] Storage location properly tracked

### Final Validation
- [ ] Backend mappings complete and accurate
- [ ] Database schema fully utilized
- [ ] No redundant tables or columns created
- [ ] Universal pattern implemented correctly
- [ ] Performance acceptable for large files
- [ ] Documentation complete

### Global Requirements Compliance
- [x] **GR-69**: Producer Portal Architecture - Document management patterns applied
- [x] **GR-52**: Universal Entity Management - Entity pattern correctly used
- [x] **GR-41**: Database Standards - Proper status management and audit fields
- [x] **GR-44**: Communication Architecture - File upload handling standards
- [x] **GR-20**: Business Logic Standards - Document requirement rules implemented