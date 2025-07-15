# IP269-New-Quote-Bind-Photo-Upload - Implementation Approach

## Requirement Understanding

The Vehicle Photo Upload step captures visual documentation of each insured vehicle for underwriting and claims purposes. This step must:

- Collect six specific photos per vehicle: Front, Rear, Driver Side, Passenger Side, Odometer, VIN
- Support multiple vehicles with clear organization
- Allow photo upload via drag-drop, click-to-browse, or camera
- Display thumbnails with user-selectable photo type descriptions
- Limit uploads to exactly six photos per vehicle
- Enable photo removal and replacement
- Create suspenses for missing photos if user proceeds incomplete
- Provide mobile-friendly interface for field use
- Prevent backward navigation without re-rating warning

This creates a comprehensive visual record of vehicle condition at policy inception.

## Domain Classification
- Primary Domain: ProducerPortal
- Cross-Domain Impact: No
- Complexity Level: Medium

## Pattern Analysis

### Reusable Patterns Identified

**From Infrastructure Codebase:**
- **File Upload Pattern**: react-dropzone from document upload
- **Image Preview**: Thumbnail generation patterns
- **S3 Storage**: Image storage with presigned URLs
- **Suspense System**: Missing photo tracking

**From Global Requirements:**
- **[GR-46 - AWS S3 Storage]**: Image storage architecture
- **[GR-07 - Reusable Components]**: Upload component patterns
- **[GR-11 - Accessibility]**: WCAG compliance for image uploads
- **[GR-04 - Validation]**: File validation patterns

**From Approved ProducerPortal Requirements:**
- **[IP269-New-Quote-Bind-Document-Upload]**: Upload UI patterns
- **[IP269-Quotes-Search]**: Suspense creation patterns
- Vehicle data from Step 3

### Domain-Specific Needs
- **Six Photo Requirement**: Specific views needed per vehicle
- **Photo Type Selection**: User must identify each photo
- **Multi-Vehicle Management**: Organize photos by vehicle
- **Mobile Camera Integration**: Support direct camera capture
- **Visual Progress Tracking**: Clear indication of completion

## Proposed Implementation

### Simplification Approach
- **Current Complexity**: Multiple vehicles, six photos each, type selection, mobile camera
- **Simplified Solution**: 
  - Fixed grid of six photo slots per vehicle
  - Dropdown for photo type selection after upload
  - Vehicle accordion/tab organization
  - Reuse document upload patterns
  - Simple completion tracking per vehicle
- **Trade-offs**: 
  - Gain: Clear requirements, intuitive interface, proven patterns
  - Lose: Advanced photo validation (can add AI validation later)

### Technical Approach

#### Phase 1: Data Model & Backend
- [ ] Create `vehicle_photo` table with vehicle_id, photo_type, s3_key
- [ ] Create `vehicle_photo_type` reference table (front, rear, etc.)
- [ ] Implement photo requirement service
- [ ] Add S3 presigned URL generation for photos
- [ ] Create suspense logic for missing photos

#### Phase 2: Vehicle Photo Grid Component
- [ ] Create `VehiclePhotoGrid` with six fixed slots:
  - Front view
  - Rear view  
  - Driver side
  - Passenger side
  - Odometer
  - VIN
- [ ] Add upload button per slot
- [ ] Implement thumbnail preview
- [ ] Add photo type dropdown

#### Phase 3: Upload Functionality
- [ ] Integrate react-dropzone per photo slot
- [ ] Add camera capture option for mobile
- [ ] Implement image validation (type, size)
- [ ] Create S3 upload service
- [ ] Add progress indicators

#### Phase 4: Multi-Vehicle Support
- [ ] Create `VehiclePhotoManager` container
- [ ] Implement vehicle tabs/accordion
- [ ] Add completion status per vehicle
- [ ] Show overall progress summary
- [ ] Enable navigation between vehicles

#### Phase 5: Validation & Submission
- [ ] Implement photo completeness check
- [ ] Create warning dialog for missing photos
- [ ] Add suspense creation for incomplete vehicles
- [ ] Implement backward navigation warning
- [ ] Add final review screen

## Risk Assessment

- **Risk 1**: Large image files on mobile → Mitigation: Client-side compression, size limits
- **Risk 2**: Poor photo quality → Mitigation: Clear instructions, retake option
- **Risk 3**: Wrong photo types → Mitigation: Visual guides, type selection validation
- **Risk 4**: Upload failures → Mitigation: Retry logic, save progress locally

## Context Preservation

- **Key Decisions**: 
  - Fixed six-photo grid for clarity
  - Photo type selection via dropdown
  - Per-vehicle organization
  - Allow proceeding with suspenses
  - Reuse upload patterns from documents
  
- **Dependencies**: 
  - Requires vehicle data from Step 3
  - Uses S3 storage infrastructure
  - Builds on document upload patterns
  - Integrates with suspense system
  
- **Future Impact**: 
  - Foundation for AI photo validation
  - Enables automated damage detection
  - Supports claims photo comparison
  - Template for other photo requirements

## Approval Section
**Status**: PENDING APPROVAL
**Reviewer Comments**: [Space for feedback]
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER