# IP269-New-Quote-Bind-Document-Upload - Implementation Approach

## Requirement Understanding

The Document Upload step enables digital submission of required underwriting documents during the quote binding process. This step must:

- Display dynamically determined document requirements based on policy parameters
- Support drag-and-drop and click-to-browse file upload methods
- Accept PDF, JPEG, and PNG files up to 10MB
- Show upload progress and preview thumbnails
- Allow document removal before submission
- Create suspenses for missing documents if user proceeds without all uploads
- Prevent backward navigation without re-rating warning
- Provide responsive mobile experience

This step streamlines document intake while allowing flexibility to proceed with incomplete documentation.

## Domain Classification
- Primary Domain: ProducerPortal
- Cross-Domain Impact: No
- Complexity Level: Medium

## Pattern Analysis

### Reusable Patterns Identified

**From Infrastructure Codebase:**
- **File Upload Pattern**: react-dropzone implementation in `file-upload-page.tsx`
- **Document Storage**: AWS S3 integration with presigned URLs
- **Suspense System**: Established pattern from IP269-Quotes-Search
- **Document Model**: Existing document management infrastructure

**From Global Requirements:**
- **[GR-46 - AWS S3 Storage]**: Document storage architecture
- **[GR-43 - Document Generation]**: Document handling patterns
- **[GR-07 - Reusable Components]**: Upload component patterns
- **[GR-11 - Accessibility]**: WCAG compliance for file uploads
- **[GR-04 - Validation]**: File type and size validation

**From Approved ProducerPortal Requirements:**
- **[IP269-Quotes-Search]**: Suspense creation and management patterns
- Navigation and state management from previous steps
- Form validation and error handling patterns

### Domain-Specific Needs
- **Dynamic Document Requirements**: List changes based on policy parameters
- **Multiple File Handling**: Support uploading multiple documents
- **Preview Generation**: Show thumbnails for uploaded files
- **Suspense Creation**: Automatic creation for missing documents
- **Progress Tracking**: Visual feedback during upload

## Proposed Implementation

### Simplification Approach
- **Current Complexity**: Multiple file uploads, dynamic requirements, preview generation, suspense workflow
- **Simplified Solution**: 
  - Use react-dropzone for proven upload functionality
  - Leverage existing suspense tables and patterns
  - Simple card-based UI for each document type
  - Direct S3 upload with presigned URLs
  - Basic thumbnail generation for images
- **Trade-offs**: 
  - Gain: Reuse proven patterns, maintainable code, reliable uploads
  - Lose: Advanced preview features (can be added later)

### Technical Approach

#### Phase 1: Backend Services
- [ ] Create `DocumentRequirementService` to determine required documents
- [ ] Implement dynamic requirement logic based on policy parameters
- [ ] Create presigned URL generation for S3 uploads
- [ ] Add document validation logic (type, size)
- [ ] Implement suspense creation for missing documents

#### Phase 2: API Endpoints
- [ ] GET `/api/quotes/{id}/document-requirements` - Get required documents
- [ ] POST `/api/quotes/{id}/documents/upload-url` - Generate presigned URL
- [ ] POST `/api/quotes/{id}/documents` - Record uploaded document
- [ ] DELETE `/api/quotes/{id}/documents/{docId}` - Remove document
- [ ] POST `/api/quotes/{id}/validate-documents` - Check completeness

#### Phase 3: Frontend Components
- [ ] Create `DocumentUploadCard` component for each document type
- [ ] Implement `DocumentUploadSection` container with:
  - Drag-and-drop zone per document
  - File type/size validation
  - Upload progress indicator
  - Thumbnail preview
  - Remove functionality
- [ ] Add `DocumentRequirementsList` to show all required documents
- [ ] Create warning dialog for proceeding without all documents

#### Phase 4: Upload Flow
- [ ] Implement client-side file validation
- [ ] Create S3 upload service using presigned URLs
- [ ] Add progress tracking with visual feedback
- [ ] Generate and display thumbnails for images
- [ ] Handle upload errors gracefully

#### Phase 5: Integration
- [ ] Add backward navigation interceptor
- [ ] Implement suspense creation on continue
- [ ] Ensure mobile-responsive design
- [ ] Add comprehensive error handling

## Risk Assessment

- **Risk 1**: Large file uploads on mobile → Mitigation: Implement chunked uploads, show clear size limits
- **Risk 2**: S3 upload failures → Mitigation: Retry logic, clear error messages
- **Risk 3**: Browser compatibility → Mitigation: Use well-tested react-dropzone library
- **Risk 4**: Missing required documents → Mitigation: Clear visual indicators, suspense tracking

## Context Preservation

- **Key Decisions**: 
  - Use react-dropzone for upload functionality
  - Leverage existing suspense system
  - Direct S3 upload with presigned URLs
  - Simple card-based UI per document type
  - Allow proceeding with suspenses
  
- **Dependencies**: 
  - Requires completed quote review
  - Uses existing suspense infrastructure
  - Builds on S3 storage patterns (GR-46)
  
- **Future Impact**: 
  - Foundation for enhanced document management
  - Supports photo upload requirements
  - Enables document-based underwriting workflows

## Approval Section
**Status**: PENDING APPROVAL
**Reviewer Comments**: [Space for feedback]
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER