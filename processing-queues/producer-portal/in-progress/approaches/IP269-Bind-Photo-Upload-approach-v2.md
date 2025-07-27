# IP269-Bind-Photo-Upload - Implementation Approach v2

## Revision Notes
- **v2 Changes**: Added dedicated photo management tables as requested
- **Key Updates**: New photo and photo_type tables, map_vehicle_photo junction table

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
- Simplified Solution: Dedicated photo management infrastructure
- Trade-offs: Additional tables but better organization and querying

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
   - [ ] Store file in file table
   - [ ] Create photo record

3. **Phase 3**: Photo Type Selection
   - [ ] Add dropdown for photo type
   - [ ] Load types from photo_type
   - [ ] Enforce six types per vehicle
   - [ ] Prevent duplicate types
   - [ ] Update photo record

4. **Phase 4**: File Management
   - [ ] Store files in file table
   - [ ] Create photo records
   - [ ] Link via map_vehicle_photo
   - [ ] Track upload timestamp
   - [ ] Enable replace functionality
   - [ ] Handle photo deletion

5. **Phase 5**: Validation Logic
   - [ ] Check all six types present
   - [ ] Query map_vehicle_photo
   - [ ] Show warnings for missing
   - [ ] Allow proceed with warnings
   - [ ] Create suspense records

6. **Phase 6**: Navigation Control
   - [ ] Implement backward warning
   - [ ] Handle data preservation
   - [ ] Confirm dialog for back
   - [ ] Clear bind progress if back
   - [ ] Continue to document upload

## Risk Assessment
- **Risk 1**: Large file uploads → Mitigation: Size limits, compression
- **Risk 2**: Photo type confusion → Mitigation: Clear labels, examples
- **Risk 3**: Performance with multiple vehicles → Mitigation: Indexed queries
- **Risk 4**: Storage scalability → Mitigation: CDN integration planning
- **Risk 5**: Network interruptions → Mitigation: Resumable uploads

## Context Preservation
- Key Decisions: Dedicated photo tables for better organization
- Dependencies: File storage system, vehicle data, suspense management
- Future Impact: Foundation for claims documentation, underwriting review

## Database Requirements Summary
- **New Tables**: 3 tables need to be created (photo, photo_type, map_vehicle_photo)
- **Existing Tables**: 4+ tables will be reused
- **Modified Tables**: 0 tables need modifications

## Database Schema Requirements

### New Tables (As specified in database-changes-summary-v5.3.md)

#### photo_type
```sql
CREATE TABLE photo_type (
  id INT(11) AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(50) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  is_default BOOLEAN DEFAULT FALSE,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  INDEX idx_code (code),
  INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### photo
```sql
CREATE TABLE photo (
  id INT(11) AUTO_INCREMENT PRIMARY KEY,
  photo_type_id INT(11) NOT NULL,
  file_id INT(11) NOT NULL,
  caption VARCHAR(255),
  taken_at TIMESTAMP NULL,
  metadata JSON,
  status_id INT(11) NOT NULL,
  created_by BIGINT UNSIGNED NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by BIGINT UNSIGNED,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (photo_type_id) REFERENCES photo_type(id),
  FOREIGN KEY (file_id) REFERENCES file(id),
  FOREIGN KEY (status_id) REFERENCES status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  
  INDEX idx_photo_type (photo_type_id),
  INDEX idx_file (file_id),
  INDEX idx_status (status_id),
  INDEX idx_taken_at (taken_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### map_vehicle_photo
```sql
CREATE TABLE map_vehicle_photo (
  id INT(11) AUTO_INCREMENT PRIMARY KEY,
  vehicle_id INT(11) NOT NULL,
  photo_id INT(11) NOT NULL,
  is_primary BOOLEAN DEFAULT FALSE,
  display_order INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (vehicle_id) REFERENCES vehicle(id),
  FOREIGN KEY (photo_id) REFERENCES photo(id),
  
  UNIQUE KEY uk_vehicle_photo (vehicle_id, photo_id),
  INDEX idx_vehicle (vehicle_id),
  INDEX idx_photo (photo_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Reference Data
```sql
-- Insert vehicle photo types
INSERT INTO photo_type (code, name, description) VALUES
('vehicle_front', 'Vehicle Front', 'Front view of vehicle'),
('vehicle_rear', 'Vehicle Rear', 'Rear view of vehicle'),
('vehicle_side_left', 'Vehicle Left Side', 'Left side view of vehicle'),
('vehicle_side_right', 'Vehicle Right Side', 'Right side view of vehicle'),
('vehicle_damage', 'Vehicle Damage', 'Photo of vehicle damage'),
('vehicle_vin', 'Vehicle VIN', 'Photo of vehicle VIN plate'),
('vehicle_odometer', 'Vehicle Odometer', 'Photo of vehicle odometer');
```

### Existing Tables to Use

1. **file**: Store uploaded photo files
   - Has name, path, size, mime_type
   - Links to photo records
   - Handles actual file storage

2. **file_type**: Photo file types
   - Define allowed image formats
   - Set size limits
   - Control file validation

3. **vehicle**: Vehicles requiring photos
   - Links to photos via mapping
   - Has all vehicle details

4. **suspense**: Track missing photos
   - Create for incomplete uploads
   - Monitor compliance
   - Track resolution

### Photo Metadata Structure
Store in photo.metadata JSON:
```json
{
  "exif_data": {
    "make": "Apple",
    "model": "iPhone 12",
    "datetime": "2023-10-15 14:30:00",
    "gps_latitude": 34.0522,
    "gps_longitude": -118.2437
  },
  "upload_context": {
    "quote_id": 456,
    "step": "bind_photos",
    "user_agent": "Mozilla/5.0..."
  },
  "processing": {
    "thumbnail_generated": true,
    "compression_applied": false,
    "original_size": 3456789
  }
}
```

### Query Examples
```sql
-- Get all photos for a vehicle
SELECT p.*, pt.name as photo_type_name, f.path
FROM photo p
JOIN photo_type pt ON p.photo_type_id = pt.id
JOIN file f ON p.file_id = f.id
JOIN map_vehicle_photo mvp ON p.id = mvp.photo_id
WHERE mvp.vehicle_id = ?
ORDER BY mvp.display_order;

-- Check missing photo types for a vehicle
SELECT pt.code, pt.name
FROM photo_type pt
WHERE pt.code LIKE 'vehicle_%'
AND pt.code NOT IN (
  SELECT pt2.code
  FROM map_vehicle_photo mvp
  JOIN photo p ON mvp.photo_id = p.id
  JOIN photo_type pt2 ON p.photo_type_id = pt2.id
  WHERE mvp.vehicle_id = ?
);
```

## Business Summary for Stakeholders
### What We're Building
A comprehensive vehicle photo documentation system with dedicated database infrastructure for managing photos. The system captures six specific views of each insured vehicle, stores them in organized photo tables, enables easy retrieval and management, and creates compliance tracking for missing photos while allowing the bind process to continue.

### Why It's Needed
Visual documentation of vehicle condition at policy inception is critical for underwriting accuracy, claims investigation, and fraud prevention. The dedicated photo infrastructure ensures efficient storage, quick retrieval for claims, proper categorization, and scalable photo management across thousands of vehicles.

### Expected Outcomes
- Organized photo storage with proper categorization
- Fast retrieval for claims investigation
- Complete audit trail of vehicle documentation
- Scalable infrastructure for growth
- Enhanced fraud detection capabilities
- Improved underwriting decisions
- Reduced claims disputes

## Technical Summary for Developers
### Key Technical Decisions
- **Architecture Pattern**: Dedicated photo tables with junction mapping
- **Storage Strategy**: File table for storage, photo table for metadata
- **Validation Approach**: Database-enforced uniqueness per vehicle/type
- **Query Optimization**: Indexed foreign keys for performance
- **Metadata Storage**: JSON field for extensible photo data

### Implementation Guidelines
- Build photo upload service
- Implement file-to-photo creation flow
- Create vehicle-photo mapping logic
- Build validation for required types
- Implement thumbnail generation
- Handle photo replacement workflow
- Create suspense integration
- Build photo retrieval APIs
- Implement bulk upload support

### API Endpoints
```
POST /api/vehicles/{id}/photos
GET  /api/vehicles/{id}/photos
PUT  /api/photos/{id}
DELETE /api/photos/{id}
GET  /api/vehicles/{id}/missing-photos
```

## Validation Criteria
### Pre-Implementation Checkpoints
- [x] File storage infrastructure exists
- [ ] Photo tables need creation
- [ ] Photo type reference needs population
- [x] Vehicle data accessible
- [x] Suspense system ready
- [x] Status management available

### Success Metrics
- [ ] All vehicles display correctly
- [ ] Photos upload and link properly
- [ ] Type selection enforces uniqueness
- [ ] Previews generate from files
- [ ] Replace updates mappings
- [ ] Validation queries work
- [ ] Suspense creates for missing
- [ ] Photo retrieval performs well

## Approval Section
**Status**: Ready for Review  
**Database Changes**: 3 new tables (photo, photo_type, map_vehicle_photo)  
**Pattern Reuse**: 85% - New photo infrastructure, existing file system  
**Risk Level**: Medium - New table structure, migration needed  
**Next Steps**: Review approach, approve database changes, implement  
**Reviewer Comments**: [Updated with dedicated photo tables]  
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER