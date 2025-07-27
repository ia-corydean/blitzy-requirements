# IP285 - Producer Portal Global Navigation - Complete Requirement

---

## **A) WHY – Vision and Purpose**

The Producer Portal Global Navigation transforms how producers interact with the platform by providing a persistent, intelligent navigation system that adapts to their workflow needs. Instead of getting lost in complex menu hierarchies or struggling to find specific policies, producers have immediate access to a powerful global search, smart alerts system, and intuitive navigation that follows them throughout their journey.

This comprehensive navigation solution addresses three critical pain points: producers spending valuable time hunting for policies across multiple screens, missing important deadlines due to overlooked notifications, and losing context when switching between different areas of the platform. By implementing a unified navigation experience with integrated search and proactive alerts, we enable producers to work more efficiently, reduce errors from missed deadlines, and maintain focus on serving their clients rather than navigating software.

---

## **B) WHAT – Core Requirements**

### **1. Global Search Experience**

The global search provides instant access to any policy, quote, or client record from anywhere in the platform:

- **Persistent Search Bar**: Always visible in the global header, accessible with keyboard shortcut (Ctrl+K or Cmd+K)
- **Smart Search Modal**: Opens as overlay with auto-focus on input field
- **Multi-Field Search Support**:
  - Policy numbers (exact or partial match)
  - Insured names (fuzzy matching for misspellings)
  - Email addresses
  - Phone numbers
  - Driver license numbers
  - Vehicle Identification Numbers (VIN)
- **Real-Time Results**: Display after 3 characters with 300-500ms debounce
- **Result Preview**: Each result shows insured name, policy/quote indicator, policy number, and effective date
- **Smart Highlighting**: Query terms highlighted in green within results

### **2. Search Results Page**

When users need to explore multiple search results:

- **Full Results View**: Accessed via "View All Results" from search modal
- **Advanced Filtering**:
  - Policy vs Quote status
  - Effective date ranges
  - Inception date ranges
- **Column Sorting**: Click any column header to sort
- **Fuzzy Match Support**: "Did you mean?" suggestions for misspellings
- **Side Panel Preview**: Click any result to view detailed summary without leaving search
  - Policy details, contact info, vehicles, drivers, coverage information
  - Direct link to full policy view

### **3. Persistent Global Navigation**

The navigation sidebar provides consistent access throughout the platform:

- **Expandable/Collapsible Design**: 
  - Full width shows icons and labels
  - Collapsed shows icons only
  - User preference persisted across sessions
- **Primary Navigation Items**:
  - Alerts (with badge for active count)
  - Home (Dashboard)
  - Quotes
  - Policies
  - Reports
  - Resources
  - Account Management (via username dropdown)
- **Account Management Submenu**:
  - Contact Info
  - Profile
  - Digital Signatures
  - Roles
  - Producers
  - Documents
  - Log Out

### **4. Proactive Alerts System**

The alerts system ensures producers never miss critical tasks:

- **Dashboard Integration**:
  - Single alert: Shows specific message with direct action button
  - Multiple alerts: Summary banner with count and "Review Now" link
- **Dedicated Alerts Center**:
  - Comprehensive list of all active alerts
  - Sort by timestamp (newest first)
  - Each alert includes title, description, status, and "Resolve" action
  - Direct navigation to resolution page
- **Alert Categories**:
  - License expirations
  - Missing documents
  - Pending approvals
  - Policy renewals
  - Payment issues
- **Resolution Tracking**: System tracks when alerts are viewed and resolved

### **3. Business Rules & Validation**

- Search requires minimum 3 characters to prevent excessive queries
- Search results limited to records user has permission to access
- Alerts automatically clear when underlying issue is resolved
- Navigation state (expanded/collapsed) persists per user
- All external links open in new tabs with security headers

### **4. Save & Navigation**

- Search history tracked for analytics and performance optimization
- User navigation preferences saved to profile
- Alert acknowledgment tracked for audit purposes
- Recent searches available for quick access

---

## Entity Analysis

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|-------|
| user | Core | Existing | Minimal schema, needs preference storage |
| alert | Core | Existing | Needs enhancement with business fields |
| alert_type | Reference | Existing | Needs category and routing fields |
| search_history | Supporting | New | Analytics and performance tracking |
| status | Reference | Existing | Used for alert states |

### New Tables Required
- **search_history**: Tracks all search queries for analytics, performance monitoring, and user experience optimization

### Modifications to Existing Tables
- **alert_type**: Add category, priority, resolution_route fields for proper alert routing
- **alert**: Add alert_type_id, user_id, title, message fields for alert content

### Relationships Identified
- user → (1:many) → alert
- user → (1:many) → search_history
- alert → (many:1) → alert_type
- alert → (many:1) → status

---

## Field Mappings (Section C)

### Backend Mappings

#### Global Search

##### Search Query Processing
- **Backend Mapping**: 
  ```
  get search_query from request
  -> validate minimum 3 characters
  -> check user permissions
  -> search across policy, quote, driver, vehicle tables
  -> return matched records with highlighting
  ```

##### Search History Tracking
- **Backend Mapping**: 
  ```
  get user.id from session
  -> insert into search_history (user_id, search_query, search_type, result_count)
  -> track selected_result if user clicks
  -> calculate search_duration_ms for performance monitoring
  ```

#### Alerts System

##### Alert Display
- **Backend Mapping**: 
  ```
  get user.id from session
  -> get alerts where user_id = user.id and status.code = 'new'
  -> join alert_type for category, priority, resolution_route
  -> order by created_at DESC
  -> return alert list with counts
  ```

##### Alert Resolution
- **Backend Mapping**: 
  ```
  get alert.id from request
  -> update alert set status_id = (select id from status where code = 'resolved')
  -> log resolution timestamp
  -> trigger any dependent workflows
  ```

### Implementation Architecture

The global navigation system follows a component-based architecture with clear separation of concerns:

- **Navigation Container**: Manages state for expand/collapse and user preferences
- **Search Service**: Handles query processing, debouncing, and result formatting
- **Alert Service**: Manages alert lifecycle, notifications, and resolution tracking
- **Analytics Service**: Tracks search patterns and navigation usage

### Integration Specifications

- **Search API**: RESTful endpoints with pagination and field projection
- **WebSocket Channels**: Real-time alert notifications on `private-alerts.{user_id}`
- **External Links**: Configured with CSP headers and tracking parameters

---

## **D) User Experience (UX) & Flows**

### **1. Global Search Flow**

1. User presses Ctrl+K anywhere in application
2. Search modal opens with focus on input field
3. User types "Smith" (minimum 3 characters)
4. After 300ms debounce, results appear below
5. Green highlighting shows "Smith" in matching records
6. User arrows down to select result
7. Press Enter navigates directly to policy detail page

### **2. Advanced Search Results Flow**

1. User searches for common name like "Johnson"
2. Multiple results appear in modal
3. User clicks "View All Results"
4. Full search page opens with all matches
5. User applies "Policy" filter to exclude quotes
6. Sorts by effective date to find recent policies
7. Clicks result to open side panel preview
8. Reviews details and clicks policy number to navigate

### **3. Alerts Management Flow**

1. Producer logs in, sees banner "2 tasks need your attention"
2. Clicks "Review Now" to open Alerts Center
3. Sees license expiration alert at top
4. Clicks "Resolve" button
5. Navigated to license update page
6. Completes update, alert automatically clears
7. Returns to see remaining alert

### **4. Navigation Preference Flow**

1. User finds navigation too wide on laptop
2. Clicks border to collapse navigation
3. Navigation shows icons only
4. Preference saved to user profile
5. Next login shows collapsed state
6. Mobile automatically uses collapsed view

---

## API Specifications

### Endpoints Required
```http
# Search endpoints
GET    /api/v1/search/global              # Global search with query parameter
GET    /api/v1/search/history             # User's search history
POST   /api/v1/search/history             # Log search interaction

# Alert endpoints  
GET    /api/v1/alerts                     # List user's alerts
GET    /api/v1/alerts/{id}                # Get specific alert
PUT    /api/v1/alerts/{id}/resolve        # Mark alert resolved
GET    /api/v1/alerts/count               # Get unresolved count

# Navigation preferences
GET    /api/v1/users/preferences          # Get navigation settings
PUT    /api/v1/users/preferences          # Update navigation settings
```

### Real-time Updates
```javascript
// WebSocket channels for live updates
private-alerts.{user_id}                   // New alerts for user
private-tenant.{tenant_id}.alerts          // All alerts for tenant monitoring
```

---

## Database Schema (Section E)

### New Core Tables

#### search_history
```sql
CREATE TABLE search_history (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  
  -- Business columns
  user_id BIGINT UNSIGNED NOT NULL COMMENT 'User who performed search',
  search_query VARCHAR(255) NOT NULL COMMENT 'Search query text',
  search_type VARCHAR(50) COMMENT 'Type of search: global, policy, quote',
  result_count INT DEFAULT 0 COMMENT 'Number of results returned',
  selected_result_type VARCHAR(50) COMMENT 'Type of result selected',
  selected_result_id BIGINT UNSIGNED COMMENT 'ID of selected result',
  search_duration_ms INT COMMENT 'Search duration in milliseconds',
  
  -- Audit fields
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  -- Foreign key constraints
  FOREIGN KEY (user_id) REFERENCES user(id) ON UPDATE CASCADE,
  
  -- Indexes
  INDEX idx_user_created (user_id, created_at),
  INDEX idx_query (search_query),
  INDEX idx_search_type (search_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Modified Tables

#### ALTER TABLE alert_type
```sql
-- Add business fields for alert categorization and routing
ALTER TABLE alert_type 
ADD COLUMN category VARCHAR(50) COMMENT 'Alert category: license, document, payment, task',
ADD COLUMN priority INT DEFAULT 0 COMMENT 'Higher number = higher priority',
ADD COLUMN auto_resolve BOOLEAN DEFAULT FALSE COMMENT 'Can alert auto-resolve',
ADD COLUMN resolution_route VARCHAR(255) COMMENT 'Route to resolve the alert',
ADD COLUMN display_order INT DEFAULT 0 COMMENT 'Display ordering',
ADD COLUMN is_default BOOLEAN DEFAULT FALSE COMMENT 'Default alert type';

-- Add index for category lookups
ALTER TABLE alert_type
ADD INDEX idx_category (category);
```

#### ALTER TABLE alert
```sql
-- Add fields to support alert content and relationships
ALTER TABLE alert
ADD COLUMN alert_type_id BIGINT UNSIGNED NOT NULL COMMENT 'Reference to alert_type',
ADD COLUMN user_id BIGINT UNSIGNED NOT NULL COMMENT 'User who receives alert',
ADD COLUMN title VARCHAR(255) NOT NULL COMMENT 'Alert title',
ADD COLUMN message TEXT COMMENT 'Alert message body';

-- Add foreign key constraints
ALTER TABLE alert
ADD CONSTRAINT fk_alert_type 
FOREIGN KEY (alert_type_id) REFERENCES alert_type(id) ON UPDATE CASCADE,
ADD CONSTRAINT fk_alert_user 
FOREIGN KEY (user_id) REFERENCES user(id) ON UPDATE CASCADE;

-- Add indexes for performance
ALTER TABLE alert
ADD INDEX idx_user_status (user_id, status_id),
ADD INDEX idx_created (created_at),
ADD INDEX idx_alert_type (alert_type_id);
```

---

## Implementation Notes

### Dependencies
- Requires user table to exist with authentication system
- Depends on policy, quote, driver, vehicle tables having searchable fields
- Status table must have appropriate alert status codes
- Frontend framework must support WebSocket connections

### Migration Considerations
- Search history can be preserved when transitioning from logs to database
- Alert types should be seeded with initial categories
- Existing alerts (if any) need migration to new schema
- User preferences initially in localStorage, migrate to database later

### Performance Considerations
- Search queries use full-text indexes where applicable
- Result sets paginated to prevent memory issues
- Search history table partitioned by month after 1M records
- Alert queries optimized with composite indexes
- WebSocket connections use connection pooling

---

## Quality Checklist

### Pre-Implementation
- [x] All UI fields mapped to database columns
- [x] Existing entities reused where possible
- [x] Reference tables enhanced for ENUMs
- [x] Naming conventions followed consistently
- [x] Relationships properly defined with foreign keys

### Post-Implementation
- [ ] All foreign keys have proper constraints
- [ ] Appropriate indexes for expected query patterns
- [ ] Audit fields included on all tables
- [ ] Status management consistent across tables
- [ ] Entity catalog updated with new entities
- [ ] Architectural decisions documented if new patterns

### Final Validation
- [ ] Backend mappings complete and accurate
- [ ] Database schema follows all standards
- [ ] No redundant tables or columns created
- [ ] Performance considerations addressed
- [ ] Documentation updated

### Global Requirements Compliance
- [ ] **GR-41**: Database Standards - All tables follow naming conventions, audit fields, status management
- [ ] **GR-38**: Microservice Architecture - Search and alerts as separate service boundaries
- [ ] **GR-52**: Universal Entity Management - Reusing existing user, status entities
- [ ] **GR-69**: Producer Portal Architecture - Aligns with portal navigation patterns