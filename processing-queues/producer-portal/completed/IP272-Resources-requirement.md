# IP272 - Resources - Complete Requirement

---

## **A) WHY – Vision and Purpose**

The Resources feature transforms how insurance professionals access critical tools and information by providing a centralized, well-organized library of essential links and documents. Instead of wasting valuable time searching through bookmarks, emails, or multiple websites for forms, government resources, and insurance tools, users have instant access to everything they need in one intuitive location.

This feature addresses the daily frustration of producers and support staff who need quick access to external resources while serving clients. By organizing resources into logical categories with clear visual hierarchy and responsive design, the system ensures that whether users are in the office on desktop or in the field on mobile devices, they can find what they need within seconds. The prioritized ranking system ensures the most frequently used resources are always easy to find, while the visual design with external link indicators prevents confusion about where links will take them.

---

## **B) WHAT – Core Requirements**

### **1. Resource List Layout & Categorization**

The Resources page provides an organized, scannable interface for accessing external and internal links:

- **Visual Category Sections**: Each resource category displays as a distinct section with clear header
- **Category Headers**: Bold, prominent category names that create visual hierarchy
- **Resource Lists**: Links displayed beneath each category header in a clean list format
- **Priority Ordering**: Categories arranged by importance/frequency of use
- **Visual Dividers**: Clear separation between categories for improved scanning
- **Flexible Structure**: Support for varying numbers of resources per category

### **2. Resource Items**

Each individual resource link includes specific features for usability:

- **Clickable Link Names**: Resource name serves as the active link text
- **External Link Indicators**: Visual icon showing when links open in new tab/window
- **Internal Link Behavior**: No icon for links that stay within the Producer Portal
- **Hover States**: Visual feedback when hovering over links
- **Priority Sorting**: Resources within each category ordered by usage frequency
- **Responsive Behavior**: Links adapt to screen size while maintaining functionality
- **Accessibility Support**: Proper ARIA labels and keyboard navigation

### **3. Responsiveness**

The layout adapts seamlessly across all device types:

- **Desktop View**:
  - Two-column layout for efficient use of screen space
  - Categories balanced across columns
  - Consistent alignment and spacing
  - Maximum readability with appropriate line lengths

- **Mobile View**:
  - Single-column layout for mobile screens
  - Categories stack vertically
  - First column content takes priority
  - Touch-friendly link spacing
  - Maintained readability on small screens

### **4. User Roles and Permissions**

Simple, inclusive access model:

- All authenticated users can access Resources section
- No role-based restrictions or filtering
- Same resource list for all user types
- Consistent experience across the platform

### **3. Business Rules & Validation**

- All external links must use HTTPS protocol
- Links validated periodically for availability
- Broken links flagged for administrative review
- Maximum 50 resources per category for performance
- Resource names limited to 100 characters
- URLs must be properly formatted and accessible

### **4. Save & Navigation**

- No user-specific saving required (static content)
- Direct navigation from main menu
- Browser back button properly supported
- Links open in new tabs preserve user context
- Page state maintained when returning from internal links

---

## Entity Analysis

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|-------|
| resource | Core | Existing | Stores individual resource links |
| resource_type | Reference | Existing | Categorizes as External/Internal |
| resource_group | Core | New | Categories for organizing resources |
| map_resource_group | Map | New | Links resources to groups with ordering |
| status | Reference | Existing | Active/inactive status management |
| user | Core | Existing | For audit fields only |

### New Tables Required
- **resource_group**: Categories for organizing related resources
- **map_resource_group**: Many-to-many relationship with display ordering

### Modifications to Existing Tables
None - all existing tables used as-is.

### Relationships Identified
- resource → resource_type (many:1)
- resource → map_resource_group (1:many)
- resource_group → map_resource_group (1:many)
- All tables → status (many:1)

---

## Field Mappings (Section C)

### Backend Mappings

#### Resource Display

##### Resource Group Loading
- **Backend Mapping**: 
  ```
  get resource_group where status.code = 'active'
  -> order by display_order ASC
  -> for each group:
     -> get map_resource_group where resource_group_id = group.id
     -> join resource on map_resource_group.resource_id
     -> join resource_type for external/internal flag
     -> order by map_resource_group.display_order
  -> return grouped resources
  ```

##### External Link Detection
- **Backend Mapping**: 
  ```
  get resource.resource_type_id
  -> join resource_type
  -> if resource_type.code = 'EXTERNAL'
     -> add external_link_indicator = true
  -> else
     -> external_link_indicator = false
  -> return with link metadata
  ```

### Implementation Architecture

The Resources feature follows a simple, maintainable architecture:

- **Resources Controller**: Handles page requests and data retrieval
- **Resource Service**: Business logic for organizing and filtering resources
- **Cache Layer**: Caches resource list for performance (invalidate on changes)
- **Admin Interface**: CRUD operations for resource management

### Integration Specifications

- **Navigation Integration**: Added to main navigation menu
- **Link Security**: All external links validated for HTTPS
- **Performance**: Page load target under 500ms
- **Caching**: 1-hour cache for resource list
- **Monitoring**: Track broken links and usage patterns

---

## **D) User Experience (UX) & Flows**

### **1. Viewing Resources Flow**

1. User clicks "Resources" in main navigation
2. Resources page loads with all categories visible
3. User scans categories to find needed resource type
4. Visual dividers help separate distinct categories
5. User locates specific resource within category

### **2. Interacting with Resource Links**

1. User hovers over resource link
2. Visual hover state provides feedback
3. User clicks on resource link
4. For external links:
   - New tab/window opens
   - External icon provided visual warning
   - Original page remains open
5. For internal links:
   - Navigation occurs in same window
   - User can use back button to return

### **3. Mobile Navigation Flow**

1. User accesses Resources on mobile device
2. Categories display in single column
3. User scrolls vertically through categories
4. Touch targets properly sized for mobile
5. External links still open in new tabs

### **4. Desktop Two-Column Flow**

1. Categories distribute across two columns
2. Left column loads first (priority content)
3. Right column balances the layout
4. User can scan both columns efficiently
5. Visual hierarchy maintained across columns

---

## API Specifications

### Endpoints Required
```http
# Resource Management
GET    /api/v1/resources                  # Get all resources grouped by category
GET    /api/v1/resources/groups           # Get resource groups only
GET    /api/v1/resources/groups/{id}      # Get specific group with resources

# Admin Endpoints (future)
POST   /api/v1/admin/resources            # Create new resource
PUT    /api/v1/admin/resources/{id}      # Update resource
DELETE /api/v1/admin/resources/{id}      # Delete resource
POST   /api/v1/admin/resource-groups      # Create new group
PUT    /api/v1/admin/resource-groups/{id} # Update group
```

### Real-time Updates
Not required - static content updated through admin interface.

---

## Database Schema (Section E)

### New Core Tables

#### resource_group
```sql
CREATE TABLE resource_group (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  
  -- Business columns
  code VARCHAR(50) UNIQUE NOT NULL COMMENT 'Unique identifier code',
  name VARCHAR(100) NOT NULL COMMENT 'Display name for category',
  description TEXT COMMENT 'Optional description',
  display_order INT DEFAULT 0 COMMENT 'Sort order for display',
  
  -- Standard columns
  status_id BIGINT UNSIGNED NOT NULL,
  created_by BIGINT UNSIGNED NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by BIGINT UNSIGNED,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Foreign key constraints
  FOREIGN KEY (status_id) REFERENCES status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  
  -- Indexes
  INDEX idx_display_order (display_order),
  INDEX idx_status (status_id),
  INDEX idx_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### map_resource_group
```sql
CREATE TABLE map_resource_group (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  
  -- Relationship columns
  resource_id BIGINT UNSIGNED NOT NULL COMMENT 'Reference to resource',
  resource_group_id BIGINT UNSIGNED NOT NULL COMMENT 'Reference to resource_group',
  display_order INT DEFAULT 0 COMMENT 'Sort order within group',
  
  -- Standard columns
  status_id BIGINT UNSIGNED NOT NULL,
  created_by BIGINT UNSIGNED NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by BIGINT UNSIGNED,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Unique constraint
  UNIQUE KEY unique_resource_group (resource_id, resource_group_id),
  
  -- Foreign key constraints
  FOREIGN KEY (resource_id) REFERENCES resource(id) ON DELETE CASCADE,
  FOREIGN KEY (resource_group_id) REFERENCES resource_group(id) ON DELETE CASCADE,
  FOREIGN KEY (status_id) REFERENCES status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  
  -- Indexes
  INDEX idx_group_order (resource_group_id, display_order),
  INDEX idx_resource (resource_id),
  INDEX idx_status (status_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Data Seeding Examples

```sql
-- Insert resource types if not exist
INSERT IGNORE INTO resource_type (code, name, status_id, created_by) VALUES
('EXTERNAL', 'External Link', 1, 1),
('INTERNAL', 'Internal Link', 1, 1);

-- Insert sample resource groups
INSERT INTO resource_group (code, name, description, display_order, status_id, created_by) VALUES
('FORMS', 'Forms & Applications', 'Common insurance forms', 1, 1, 1),
('GOVT', 'Government Resources', 'State and federal resources', 2, 1, 1),
('TOOLS', 'Insurance Tools', 'Calculators and utilities', 3, 1, 1),
('TRAINING', 'Training Materials', 'Educational resources', 4, 1, 1);

-- Insert sample resources
INSERT INTO resource (code, name, url, resource_type_id, status_id, created_by) VALUES
('DMV_CA', 'California DMV', 'https://www.dmv.ca.gov', 
  (SELECT id FROM resource_type WHERE code = 'EXTERNAL'), 1, 1),
('RATE_CALC', 'Rate Calculator', '/tools/rate-calculator', 
  (SELECT id FROM resource_type WHERE code = 'INTERNAL'), 1, 1);
```

---

## Implementation Notes

### Dependencies
- Existing resource and resource_type tables must be available
- Status management system must be configured
- Main navigation must support Resources menu item
- Frontend responsive framework required

### Migration Considerations
- Existing resources (if any) need to be mapped to groups
- Create initial resource groups based on business requirements
- Seed commonly used resources during deployment
- No data migration required for new installations

### Performance Considerations
- Cache resource list for 1 hour
- Invalidate cache on any resource/group changes
- Limit resources per group to maintain performance
- Use database indexes for sorting operations
- Consider CDN for external resource icons

---

## Quality Checklist

### Pre-Implementation
- [x] All UI fields mapped to database columns
- [x] Existing entities reused where possible
- [x] Reference tables identified correctly
- [x] Naming conventions followed consistently
- [x] Relationships properly defined with foreign keys

### Post-Implementation
- [ ] All resource links validated and functional
- [ ] Responsive design works on all devices
- [ ] External link indicators display correctly
- [ ] Page loads within 500ms target
- [ ] Accessibility standards met (WCAG)

### Final Validation
- [ ] Backend mappings complete and accurate
- [ ] Database schema follows all standards
- [ ] No redundant tables or columns created
- [ ] Performance considerations addressed
- [ ] Documentation updated

### Global Requirements Compliance
- [ ] **GR-41**: Database Standards - All tables follow naming conventions and audit fields
- [ ] **GR-52**: Universal Entity Management - Reuses existing resource infrastructure
- [ ] **GR-69**: Producer Portal Architecture - Properly integrated with portal navigation