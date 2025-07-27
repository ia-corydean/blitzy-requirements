# IP269-Bind-Photo-Upload - Implementation Approach

## Requirement Understanding
The Vehicle Photo Upload step ensures proper documentation of each insured vehicle through six required photos (Front, Rear, Driver Side, Passenger Side, Odometer, VIN). The system must support multi-vehicle uploads with clear guidance, thumbnail previews, photo type selection, and validation. Users can proceed with warnings if photos are missing, creating a suspense for later completion.

## Domain Classification
- Primary Domain: Producer Portal / Quote Binding
- Cross-Domain Impact: Yes - Affects underwriting, claims, compliance
- Complexity Level: Medium

## Pattern Analysis

### Reusable Patterns Identified
- [GR-69]: Producer Portal Architecture - Multi-step bind workflow
- [GR-52]: Universal Entity Management - Document/file management
- [GR-41]: Database Standards - File storage patterns
- [GR-44]: Communication Architecture - File upload handling
- [GR-20]: Business Logic Standards - Validation rules

### Domain-Specific Needs
- Six specific photo types per vehicle
- Multi-vehicle photo management
- Photo type dropdown selection
- Thumbnail preview generation
- Replace/remove functionality
- Suspense creation for missing photos
- Backward navigation warning

## Proposed Implementation

### Simplification Approach
- Current Complexity: Multiple photos per vehicle, type identification
- Simplified Solution: Leverage existing file/document infrastructure
- Trade-offs: May need to enhance file table for photo types

### Technical Approach
1. **Phase 1**: Vehicle List Display
   - [ ] Load all vehicles from quote
   - [ ] Create upload section per vehicle
   - [ ] Show six photo slots each
   - [ ] Display vehicle identification
   - [ ] Track completion status

2. **Phase 2**: Photo Upload Interface
   - [ ] Implement drag-and-drop zones
   - [ ] Add file browser option
   - [ ] Support image formats only
   - [ ] Generate thumbnail previews
   - [ ] Store in file table

3. **Phase 3**: Photo Type Selection
   - [ ] Add dropdown for photo type
   - [ ] Enforce six types per vehicle
   - [ ] Prevent duplicate types
   - [ ] Update on selection change
   - [ ] Show type in preview

4. **Phase 4**: File Management
   - [ ] Store files with metadata
   - [ ] Link to vehicle via mapping
   - [ ] Track upload timestamp
   - [ ] Enable replace functionality
   - [ ] Handle file deletion

5. **Phase 5**: Validation Logic
   - [ ] Check all six types present
   - [ ] Show warnings for missing
   - [ ] Allow proceed with warnings
   - [ ] Create suspense records
   - [ ] Track completion status

6. **Phase 6**: Navigation Control
   - [ ] Implement backward warning
   - [ ] Handle data preservation
   - [ ] Confirm dialog for back
   - [ ] Clear bind progress if back
   - [ ] Continue to document upload

## Risk Assessment
- **Risk 1**: Large file uploads → Mitigation: Size limits, compression
- **Risk 2**: Photo type confusion → Mitigation: Clear labels, examples
- **Risk 3**: Performance with multiple vehicles → Mitigation: Lazy loading
- **Risk 4**: Storage scalability → Mitigation: CDN integration planning
- **Risk 5**: Network interruptions → Mitigation: Resumable uploads

## Context Preservation
- Key Decisions: Use file table with photo metadata, create suspense for missing
- Dependencies: File storage system, vehicle data, suspense management
- Future Impact: Foundation for claims documentation, underwriting review

## Database Requirements Summary
- **New Tables**: 1 table may be needed (vehicle_photo_type)
- **Existing Tables**: 5+ tables will be reused
- **Modified Tables**: 0-1 tables may need enhancement

## Database Schema Requirements

### Potential New Table

#### vehicle_photo_type (Reference Table)
```sql
CREATE TABLE vehicle_photo_type (
  id INT(11) AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(50) UNIQUE NOT NULL,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  display_order INT DEFAULT 0,
  status_id INT(11) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (status_id) REFERENCES status(id),
  INDEX idx_code (code),
  INDEX idx_status (status_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert standard photo types
INSERT INTO vehicle_photo_type (code, name, display_order, status_id) VALUES
('FRONT', 'Front View', 1, 1),
('REAR', 'Rear View', 2, 1),
('DRIVER_SIDE', 'Driver Side', 3, 1),
('PASSENGER_SIDE', 'Passenger Side', 4, 1),
('ODOMETER', 'Odometer', 5, 1),
('VIN', 'VIN', 6, 1);
```

### Existing Tables to Use

1. **file**: Store uploaded photos
   - Has name, path, size, mime_type
   - Use metadata for photo type
   - Ready for photo storage

2. **file_type**: Photo file types
   - Define allowed image formats
   - Set size limits

3. **document**: Link files to entities
   - Can store vehicle photos
   - Has file_id reference

4. **vehicle**: Vehicles requiring photos
   - Links to uploaded photos
   - Has all vehicle details

5. **suspense**: Track missing photos
   - Create for incomplete uploads
   - Monitor compliance

### Metadata Structure
Store in file.metadata JSON:
```json
{
  "photo_type": "FRONT",
  "vehicle_id": 123,
  "quote_id": 456,
  "upload_step": "bind_photos"
}
```

## Business Summary for Stakeholders
### What We're Building
A vehicle photo documentation system that captures six specific views of each insured vehicle during the policy binding process. The system guides users through uploading required photos, allows photo type selection, provides preview capabilities, and creates compliance tracking for missing photos while allowing the bind process to continue.

### Why It's Needed
Visual documentation of vehicle condition at policy inception is critical for underwriting accuracy, claims investigation, and fraud prevention. This systematic photo collection ensures consistent documentation across all policies, reduces disputes during claims, and provides auditable evidence of vehicle condition.

### Expected Outcomes
- Complete visual documentation for all insured vehicles
- Reduced claims disputes with inception photos
- Improved underwriting accuracy with visual verification
- Compliance tracking for photo requirements
- Streamlined user experience with clear guidance

## Technical Summary for Developers
### Key Technical Decisions
- **Architecture Pattern**: Use file table with metadata, potential photo type table
- **Storage Strategy**: File system with CDN migration path
- **Validation Approach**: Soft validation with suspense creation
- **Preview Generation**: Client-side thumbnails, server validation
- **State Management**: Quote-scoped photo collection

### Implementation Guidelines
- Build multi-vehicle upload component
- Implement drag-drop with fallback
- Generate thumbnails client-side
- Store metadata in JSON field
- Create suspense service integration
- Handle large file uploads
- Implement progress indicators
- Cache vehicle data for display

## Validation Criteria
### Pre-Implementation Checkpoints
- [x] File storage infrastructure exists
- [x] Document linking available
- [x] Vehicle data accessible
- [x] Suspense system ready
- [ ] Photo type reference may be needed
- [x] Metadata storage supported

### Success Metrics
- [ ] All vehicles display correctly
- [ ] Photo uploads work reliably
- [ ] Type selection functions
- [ ] Previews generate properly
- [ ] Replace/remove works
- [ ] Validation shows warnings
- [ ] Suspense creates for missing
- [ ] Navigation warnings display

## Approval Section
**Status**: Ready for Review  
**Database Changes**: May need vehicle_photo_type reference table  
**Pattern Reuse**: 95% - Leveraging file infrastructure  
**Risk Level**: Medium - File handling complexity  
**Next Steps**: Review approach, confirm photo type strategy, implement  
**Reviewer Comments**: [Pending]  
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER