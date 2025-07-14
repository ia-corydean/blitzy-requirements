# IP269-New-Quote-Bind-Document-Upload - Implementation Plan

## Requirement Overview

### Purpose
The document upload experience enables users to:
- Submit required documentation digitally for underwriting review
- Reduce delays and friction in quote processing
- Provide clear visual confirmation and status indicators
- Support various document types (driver's license, proof of insurance, etc.)

### Scope
- Dynamic document requirement list based on policy parameters
- Drag-and-drop and click-to-browse upload
- File format validation (PDF, JPEG, PNG)
- Suspense creation for missing documents
- Re-rating warning for backward navigation
- Progress tracking and visual feedback

## Entity Analysis

### New Entities Required

1. **document_requirement**
   - Required document types per program/state
   - Conditional requirements based on policy
   - Display order and grouping

2. **document_requirement_rule**
   - Business rules for document requirements
   - Conditional logic (e.g., SR22 requires filing)
   - Dynamic requirement evaluation

3. **quote_document_upload**
   - Uploaded documents per quote
   - Links to document requirements
   - Upload status and metadata

4. **upload_validation_result**
   - File validation outcomes
   - Error messages and codes
   - Retry information

### Existing Entities Involved

- **quote**: Parent for document uploads
- **document**: Base document entity
- **document_type**: Types of documents
- **suspense**: Created for missing docs
- **map_quote_document**: Quote-document relationship

## Global Requirements Alignment

### Primary GRs
- **GR-46 (S3 Storage)**: Document storage architecture
- **GR-43 (Document Generation)**: Document handling
- **GR-04 (Validation)**: File validation rules
- **GR-37 (Action Tracking)**: Upload audit trail
- **GR-18 (Workflow)**: Bind workflow integration

### Supporting GRs
- **GR-12 (Security)**: Secure file handling
- **GR-24 (Data Security)**: Encryption at rest
- **GR-11 (Accessibility)**: Upload accessibility
- **GR-08 (Performance)**: Large file handling

## Database Schema Planning

### Core Tables

1. **document_requirement**
   ```sql
   - id (PK)
   - program_id (FK)
   - state_code
   - document_type_id (FK)
   - requirement_code (unique)
   - display_name
   - help_text
   - is_always_required (boolean)
   - display_order
   - status_id (FK)
   - created_at, updated_at
   ```

2. **document_requirement_rule**
   ```sql
   - id (PK)
   - document_requirement_id (FK)
   - rule_type (conditional, always)
   - condition_field
   - condition_operator
   - condition_value
   - applies_to (quote, driver, vehicle)
   - status_id (FK)
   - created_at, updated_at
   ```

3. **quote_document_upload**
   ```sql
   - id (PK)
   - quote_id (FK)
   - document_requirement_id (FK)
   - document_id (FK)
   - original_filename
   - file_size
   - mime_type
   - s3_key
   - upload_status (pending, completed, failed)
   - error_message
   - uploaded_at
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

4. **document_upload_session**
   ```sql
   - id (PK)
   - quote_id (FK)
   - session_token
   - total_required
   - total_uploaded
   - started_at
   - completed_at
   - status_id (FK)
   ```

### Modified Tables

1. **suspense**
   ```sql
   -- Link to document requirements
   ADD COLUMN document_requirement_id (FK)
   ```

## API Endpoints

### Required Endpoints
```
GET    /api/v1/quotes/{quote_id}/document-requirements
POST   /api/v1/quotes/{quote_id}/documents/upload
GET    /api/v1/quotes/{quote_id}/uploaded-documents
DELETE /api/v1/quotes/{quote_id}/documents/{id}
POST   /api/v1/quotes/{quote_id}/documents/validate
GET    /api/v1/quotes/{quote_id}/document-upload-status
POST   /api/v1/quotes/{quote_id}/create-document-suspenses
```

### S3 Integration
```
POST   /api/v1/documents/presigned-upload-url
GET    /api/v1/documents/presigned-download-url
```

### Real-time Updates
```javascript
private-quote.{quote_id}.document-uploads
private-quote.{quote_id}.upload-progress
```

## Integration Points

### Internal Services
1. **DocumentRequirementService**
   - Evaluate dynamic requirements
   - Apply business rules
   - Generate requirement list

2. **FileUploadService**
   - Handle file uploads to S3
   - Validate file types/sizes
   - Generate thumbnails

3. **SuspenseService**
   - Create suspenses for missing
   - Track resolution status
   - Link to requirements

### External Services
- **AWS S3**: Document storage (GR-46)
- **Virus Scanner**: File safety check
- **Image Processing**: Thumbnail generation

## Implementation Considerations

### Key Patterns
1. **Progressive Upload**
   - Chunked uploads for large files
   - Resume capability
   - Progress indicators

2. **Dynamic Requirements**
   - Real-time evaluation
   - Policy parameter based
   - State-specific rules

3. **Visual Feedback**
   - Upload progress bars
   - Success animations
   - Error state clarity

4. **Suspense Management**
   - Automatic creation
   - Clear messaging
   - Resolution tracking

### Technical Decisions
- Vue.js file upload components
- S3 multipart uploads
- Dropzone.js for drag-drop
- Redis for upload sessions
- Background job for processing

## Quality Checkpoints

### Pre-Implementation
- [ ] Review S3 integration patterns
- [ ] Validate file size limits
- [ ] Check virus scanning setup
- [ ] Review suspense patterns

### Implementation
- [ ] File uploads working
- [ ] Progress tracking accurate
- [ ] Requirements dynamic
- [ ] Suspenses created

### Post-Implementation
- [ ] Large file testing
- [ ] Network interruption handling
- [ ] Cross-browser compatibility
- [ ] Mobile upload testing

## Dependencies

### Upstream
- Quote data complete
- Moving to bind phase
- Policy parameters set

### Downstream
- Document signing step
- Suspense resolution
- Policy binding completion

## Risk Mitigation

1. **File Security**: Virus scanning and type validation
2. **Large Files**: Chunked uploads and limits
3. **Network Issues**: Resume capability
4. **User Errors**: Clear validation messages

## UI/UX Specifications

### Upload Cards
- Document type header
- Description/help text
- Upload area prominent
- Remove option visible

### Drag & Drop
- Dashed border area
- Hover state change
- Drop feedback
- Multiple file support

### Progress Indicators
- Upload percentage
- Time remaining
- Cancel option
- Error recovery

### File Preview
- Thumbnail display
- File name/size
- Upload timestamp
- Remove button

### Mobile Experience
- Touch-friendly targets
- Camera integration
- Simplified layout
- Clear CTAs

## Cross-Domain Considerations

- **Compliance**: Document retention policies
- **Underwriting**: Review requirements
- **Claims**: Access to documents
- **Audit**: Upload history tracking

## Next Steps

1. Create document requirement rules engine
2. Implement S3 multipart upload
3. Build file validation service
4. Create upload UI components
5. Implement progress tracking
6. Add virus scanning integration
7. Build suspense creation logic
8. Add comprehensive error handling