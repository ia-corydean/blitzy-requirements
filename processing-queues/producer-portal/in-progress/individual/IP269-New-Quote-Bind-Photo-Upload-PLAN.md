# IP269-New-Quote-Bind-Photo-Upload - Implementation Plan

## Requirement Overview

### Purpose
This step ensures proper documentation of each insured vehicle with photographic evidence to:
- Serve as visual condition record at policy issuance
- Support underwriting, claims investigation, and risk verification
- Meet compliance and audit readiness requirements
- Capture six specific photos per vehicle

### Scope
- Six required photos per vehicle (Front, Rear, Driver Side, Passenger Side, Odometer, VIN)
- Multi-vehicle support with scrollable list
- Upload interface with drag-and-drop
- Photo type identification via dropdown
- Suspense creation for missing photos
- Re-rating warning for backward navigation

## Entity Analysis

### New Entities Required

1. **vehicle_photo_requirement**
   - Photo types required per vehicle
   - Display order and grouping
   - Help text and examples

2. **vehicle_photo**
   - Uploaded photos per vehicle
   - Photo type classification
   - Metadata (timestamp, location)

3. **photo_validation_result**
   - Image quality checks
   - Clarity validation
   - Required elements visible

4. **vehicle_photo_set**
   - Groups 6 photos per vehicle
   - Completion status tracking
   - Submission readiness

### Existing Entities Involved

- **vehicle**: Parent for photos
- **quote**: Overall context
- **document**: Photo storage (reuse pattern)
- **suspense**: Missing photo tracking
- **map_vehicle_document**: Vehicle-photo relationship

## Global Requirements Alignment

### Primary GRs
- **GR-46 (S3 Storage)**: Photo storage
- **GR-43 (Document Generation)**: Photo handling
- **GR-04 (Validation)**: Photo requirements
- **GR-37 (Action Tracking)**: Upload audit
- **GR-18 (Workflow)**: Bind workflow

### Supporting GRs
- **GR-08 (Performance)**: Image optimization
- **GR-11 (Accessibility)**: Upload accessibility
- **GR-12 (Security)**: Secure photo handling
- **GR-24 (Data Security)**: Image encryption

## Database Schema Planning

### Core Tables

1. **vehicle_photo_requirement**
   ```sql
   - id (PK)
   - photo_type_code (unique)
   - display_name
   - description
   - example_image_url
   - display_order
   - validation_rules (JSON)
   - status_id (FK)
   - created_at, updated_at
   ```

2. **vehicle_photo**
   ```sql
   - id (PK)
   - vehicle_id (FK)
   - quote_id (FK)
   - photo_type_code
   - document_id (FK)
   - original_filename
   - s3_key
   - file_size
   - mime_type
   - exif_data (JSON)
   - upload_timestamp
   - validation_status
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

3. **vehicle_photo_set**
   ```sql
   - id (PK)
   - vehicle_id (FK)
   - quote_id (FK)
   - front_photo_id (FK)
   - rear_photo_id (FK)
   - driver_side_photo_id (FK)
   - passenger_side_photo_id (FK)
   - odometer_photo_id (FK)
   - vin_photo_id (FK)
   - is_complete (boolean)
   - completed_at
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

4. **photo_upload_session**
   ```sql
   - id (PK)
   - quote_id (FK)
   - total_vehicles
   - total_photos_required
   - total_photos_uploaded
   - session_started_at
   - session_completed_at
   - status_id (FK)
   ```

### Photo Type Reference Data
```sql
INSERT INTO vehicle_photo_requirement (photo_type_code, display_name, display_order) VALUES
('front', 'Front View', 1),
('rear', 'Rear View', 2),
('driver_side', 'Driver Side', 3),
('passenger_side', 'Passenger Side', 4),
('odometer', 'Odometer', 5),
('vin', 'VIN Plate', 6);
```

## API Endpoints

### Required Endpoints
```
GET    /api/v1/quotes/{quote_id}/vehicles/{vehicle_id}/photo-requirements
POST   /api/v1/quotes/{quote_id}/vehicles/{vehicle_id}/photos/upload
GET    /api/v1/quotes/{quote_id}/vehicles/{vehicle_id}/photos
PUT    /api/v1/quotes/{quote_id}/vehicles/{vehicle_id}/photos/{id}/type
DELETE /api/v1/quotes/{quote_id}/vehicles/{vehicle_id}/photos/{id}
GET    /api/v1/quotes/{quote_id}/photo-upload-status
POST   /api/v1/quotes/{quote_id}/create-photo-suspenses
```

### Validation Endpoints
```
POST   /api/v1/photos/validate-quality
POST   /api/v1/photos/detect-type
```

### Real-time Updates
```javascript
private-quote.{quote_id}.photo-uploads
private-vehicle.{vehicle_id}.photo-progress
```

## Integration Points

### Internal Services
1. **PhotoUploadService**
   - Handle image uploads
   - Type classification
   - Quality validation
   - Thumbnail generation

2. **VehiclePhotoService**
   - Track requirements
   - Validate completeness
   - Generate suspenses

3. **ImageProcessingService**
   - Resize for storage
   - Extract EXIF data
   - Generate thumbnails
   - Optimize file size

### External Services
- **AWS S3**: Photo storage
- **AWS Rekognition**: Photo type detection (future)
- **Image optimization API**: Compression

## Implementation Considerations

### Key Patterns
1. **Bulk Upload Support**
   - Multiple files at once
   - Auto-classification attempt
   - Manual type selection
   - Progress tracking

2. **Photo Organization**
   - By vehicle clearly
   - Visual grid layout
   - Completion indicators
   - Easy navigation

3. **Mobile Optimization**
   - Camera integration
   - Touch-friendly UI
   - Reduced image size
   - Offline capability

4. **Validation Logic**
   - File type check
   - Size limits (10MB)
   - Image clarity
   - Required elements

### Technical Decisions
- Vue.js photo grid components
- Dropzone.js for uploads
- Sharp/ImageMagick for processing
- S3 multipart for large images
- IndexedDB for offline storage

## Quality Checkpoints

### Pre-Implementation
- [ ] Review photo requirements
- [ ] Validate S3 configuration
- [ ] Check image processing setup
- [ ] Review mobile camera APIs

### Implementation
- [ ] Upload functionality working
- [ ] Type selection smooth
- [ ] Thumbnails generated
- [ ] Suspenses created correctly

### Post-Implementation
- [ ] Mobile camera testing
- [ ] Large image handling
- [ ] Network interruption recovery
- [ ] Cross-device compatibility

## Dependencies

### Upstream
- Vehicles added to quote
- Moving to bind phase
- Storage configuration ready

### Downstream
- Document upload step
- Suspense resolution
- Policy binding completion

## Risk Mitigation

1. **Image Quality**: Validation and guidance
2. **Storage Costs**: Image optimization
3. **Upload Failures**: Retry mechanism
4. **Type Confusion**: Clear labels and examples

## UI/UX Specifications

### Vehicle List
- Card per vehicle
- Make/model/year display
- Progress indicator (X/6)
- Expand to show photos

### Photo Grid
- 2x3 grid layout
- Photo type labels
- Upload placeholders
- Thumbnail previews

### Upload Interface
- Drag-drop zone
- Browse button
- Multiple selection
- Progress bars

### Photo Management
- Type dropdown
- Remove button
- Replace option
- View full size

### Mobile Specific
- Camera button prominent
- Single column layout
- Swipe between vehicles
- Large touch targets

### Completion States
- Green check for complete
- Yellow warning for partial
- Red alert for missing
- Clear messaging

## Cross-Domain Considerations

- **Claims**: Photo access for claims
- **Underwriting**: Risk assessment
- **Compliance**: Retention policies
- **Fraud**: Detection patterns

## Next Steps

1. Create photo requirement data
2. Build photo upload service
3. Implement image processing
4. Create photo grid UI
5. Add type selection dropdown
6. Implement validation logic
7. Build suspense creation
8. Add mobile camera support