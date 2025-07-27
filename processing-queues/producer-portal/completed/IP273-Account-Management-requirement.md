# IP273 - Account Management - Complete Requirement

---

## **A) WHY – Vision and Purpose**

The Account Management system provides a centralized, secure platform for managing user profiles, permissions, and documentation within InsurePilot. This comprehensive solution addresses the critical need for unified user administration, replacing fragmented manual processes with an efficient, role-based system. 

By implementing this feature, InsurePilot will enable managers to control user access, maintain compliance documentation, support digital signatures for paperless workflows, and provide multi-language support for diverse user bases. The system ensures proper access control while maintaining a complete audit trail for regulatory compliance and operational transparency.

---

## **B) WHAT – Core Requirements**

The Account Management feature provides a complete user and producer management system accessible exclusively to users with Manager permissions. The feature is accessed through the username dropdown in the main navigation and includes eight major functional areas organized in a tabbed interface.

### **1. Authentication Management**

- **Sign In**: Username/password authentication with error handling and responsive design
- **Password Reset**: Email-based password recovery with secure token generation
- **Sign Out**: Clean session termination with confirmation screen
- **Password Requirements**: Minimum 10 characters, at least 1 letter, at least 1 number or special character
- **Session Management**: Secure session handling with automatic timeout

### **2. Contact Information**

- **Contact Details**: Website, email, phone number, and fax management
- **Address Management**: Separate mailing and physical addresses
- **Same Address Option**: Checkbox to copy mailing address to physical address
- **Validation**: Required field validation before saving
- **Save/Cancel**: Explicit save and cancel functionality

### **3. Profile Management**

- **Email Display**: Show user's registered email address
- **Language Preference**: Dropdown selection for preferred language
- **Password Change**: Modal dialog with current password verification
- **Password Visibility**: Toggle for showing/hiding password characters
- **Confirmation Dialog**: Warning about external system password updates

### **4. Digital Signatures**

- **Signature Creation**: Generate digital signature from Licensed Agent of Record Name
- **Signature Display**: Show generated signature and initials
- **Adoption Agreement**: Checkbox confirmation for legal adoption
- **Change Signature**: Ability to update existing signature
- **Timestamp Tracking**: Record when signature was adopted

### **5. Roles & Permissions**

- **Role Display**: List of available roles (Manager, Customer Support, etc.)
- **Member Count**: Number of users assigned to each role
- **Permission List**: Detailed permissions for each role
- **Master Permissions**: Special notification banner for users with master access
- **Permission Categories**: Organized by functional area

### **6. All Producers**

- **Producer List**: Comprehensive table with search and export functionality
- **Data Columns**: Login, Email, Producer ID, Access Level, User Level
- **Role Details**: Click role to view assigned permissions
- **Producer Details**: Click producer for detailed view
- **Export Options**: Download list as PDF or CSV

### **7. Document Management**

- **Document Upload**: Support for License Documents and E&O certificates
- **Required Metadata**: 
  - License Documents: License Number and expiration date
  - E&O Documents: Policy Coverage Limit ($1M, $2M, $5M) and expiration date
- **Document Actions**: View info, view history, delete with confirmation
- **Retention Policy**: Deleted documents kept in "Recently Deleted" for 90 days
- **Search Functionality**: Exact match document search

### **8. Navigation & UI**

- **Tab Navigation**: Seamless switching between all feature areas
- **Responsive Design**: Full functionality on desktop and mobile devices
- **Error Handling**: Clear error messages with actionable guidance
- **Success Notifications**: Confirmation messages for successful actions
- **Help & Support**: Customer support contact information available

### **Business Rules & Validation**

- Manager-only access restriction enforced at all levels
- Password complexity validation on all password fields
- Email format validation for all email inputs
- Required field validation before form submission
- Expiration date validation for future dates only
- File size limits enforced on document uploads
- Session timeout after period of inactivity
- Audit logging for all data modifications

### **Save & Navigation**

- Explicit save required for all changes
- Unsaved changes warning on navigation
- Cancel functionality reverts all pending changes
- Tab state preservation during session
- Auto-save drafts for complex forms
- Progress indicators for multi-step processes

---

## Entity Analysis

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|-------|
| user | Core | Modified | Added signature_id, language_preference_id, username, password fields |
| signature | Core | New | Stores digital signature data |
| language | Reference | New | Available language options |
| language_type | Reference | New | Language categorization |
| file | Supporting | New | Physical file storage |
| file_type | Reference | New | File type definitions |
| permission | Core | Modified | Added code, name, description, category fields |
| role | Core | Modified | Added code, name, description fields |
| name | Core | Modified | Added first_name, last_name, middle_name fields |
| document | Core | Existing | Ready for document management |
| document_type | Reference | Existing | Document categorization |
| address | Core | Existing | Contact addresses |
| communication_method | Core | Existing | Contact methods |
| producer | Core | Existing | Producer records |
| map_user_role | Map | Existing | User-role assignments |
| map_role_permission | Map | Existing | Role-permission mapping |
| session | Supporting | Existing | Session management |

### New Tables Required
- **signature**: Digital signature storage with adoption tracking
- **language**: Language options with native names and defaults
- **language_type**: Language classification (UI, Content, Regional)
- **file**: Physical file storage with metadata and security
- **file_type**: File type definitions with validation rules

### Modifications to Existing Tables
- **user**: Added authentication fields (username, password), reference fields (signature_id, language_preference_id), MFA support
- **permission**: Enhanced with code, name, description, category for better organization
- **role**: Enhanced with code, name, description for clearer definitions
- **name**: Added individual name components for proper name handling

### Relationships Identified
- user → one-to-one → signature (digital signature)
- user → many-to-one → language (preference)
- language → many-to-one → language_type
- file → many-to-one → file_type
- document → many-to-one → file
- user → many-to-many → role (via map_user_role)
- role → many-to-many → permission (via map_role_permission)

---

## Field Mappings (Section C)

### Backend Mappings

#### Sign In Screen

##### Username Field
- **Backend Mapping**: 
  ```
  get user.username from user table
  -> validate against authentication service
  -> return user record if valid
  ```

##### Password Field
- **Backend Mapping**: 
  ```
  get user.password (hashed) from user table
  -> verify using bcrypt/argon2
  -> create session on success
  ```

#### Contact Information Tab

##### Contact Details
- **Backend Mapping**: 
  ```
  get user.id from session
  -> get communication_method by user_id and type
  -> return phone, email, fax, website values
  ```

##### Address Information
- **Backend Mapping**: 
  ```
  get user.id from session
  -> get address by user_id and address_type
  -> return mailing and physical addresses
  ```

#### Profile Tab

##### Language Preference
- **Backend Mapping**: 
  ```
  get user.language_preference_id
  -> get language by id
  -> get all active languages for dropdown
  -> return selected and available languages
  ```

##### Password Change
- **Backend Mapping**: 
  ```
  verify user.password matches current_password input
  -> hash new_password using bcrypt/argon2
  -> update user.password
  -> update user.updated_at, updated_by
  ```

#### Digital Signatures Tab

##### Signature Display
- **Backend Mapping**: 
  ```
  get user.signature_id
  -> get signature by id if exists
  -> return signature_data, initials_data, adopted_name, adopted_at
  ```

##### Signature Creation
- **Backend Mapping**: 
  ```
  create signature record with user_id
  -> generate signature_data from name input
  -> generate initials_data from name
  -> set signature_adopted_at to current timestamp
  -> update user.signature_id
  ```

#### Roles & Permissions Tab

##### User Roles
- **Backend Mapping**: 
  ```
  get user.id
  -> get map_user_role by user_id
  -> get role details for each role_id
  -> return role code, name, description
  ```

##### Role Permissions
- **Backend Mapping**: 
  ```
  get role.id for selected role
  -> get map_role_permission by role_id
  -> get permission details for each permission_id
  -> return permission code, name, category, description
  ```

#### All Producers Tab

##### Producer List
- **Backend Mapping**: 
  ```
  get all producer records with status = active
  -> join user on producer.user_id
  -> join map_user_role on user.id
  -> join role on role_id
  -> return login, email, producer_code, access_level, role names
  ```

#### Documents Tab

##### Document List
- **Backend Mapping**: 
  ```
  get user.id from session
  -> get document by user_id
  -> join document_type for type details
  -> join file for file details
  -> return document list with metadata
  ```

##### Document Upload
- **Backend Mapping**: 
  ```
  create file record with upload data
  -> create document record with file_id
  -> set document_type_id based on selection
  -> store license_number or coverage_limit in metadata
  -> set expiration_date
  ```

### Implementation Architecture

The Account Management system follows a clean, service-oriented architecture:

1. **Authentication Service**: Handles sign-in, sign-out, password reset with JWT tokens
2. **User Service**: Manages user profiles, preferences, and contact information
3. **Permission Service**: Controls role-based access with cached permission checks
4. **Document Service**: Handles file uploads, storage, and metadata management
5. **Signature Service**: Generates and stores digital signatures with legal compliance

All services use repository pattern for data access, with comprehensive audit logging through middleware. The system implements database transactions for critical operations and uses queues for file processing.

### Integration Specifications

- **Authentication**: Laravel's built-in auth with custom username field
- **File Storage**: Local filesystem with CDN-ready architecture
- **Session Management**: Redis-backed sessions with configurable timeout
- **Email Service**: Password reset emails via configured SMTP
- **Export Service**: PDF/CSV generation for producer reports
- **Caching**: Redis caching for permission checks and frequent queries

---

## **D) User Experience (UX) & Flows**

### **1. Sign In Flow**

1. User navigates to sign-in page
2. Enters username and password
3. System validates credentials
4. On success: Redirect to Producer Portal dashboard
5. On failure: Display "Incorrect Username or Password" error
6. User can click "Forgot Password?" to initiate reset

### **2. Password Reset Flow**

1. User clicks "Forgot Password?" on sign-in page
2. Enters registered email or username
3. System sends password reset email
4. User clicks secure link in email
5. Enters new password and confirmation
6. System validates password requirements
7. On success: Shows confirmation and "Return to Sign-In" button

### **3. Account Management Navigation**

1. User (Manager only) clicks username in navigation
2. Dropdown shows "Account Management" option
3. Clicking opens tabbed interface
4. User can navigate between tabs without losing changes
5. Each tab loads relevant data dynamically

### **4. Digital Signature Creation**

1. User navigates to Digital Signatures tab
2. If no signature exists, sees "Create a Signature" button
3. Clicks button to open creation dialog
4. Enters Licensed Agent of Record Name
5. Checks adoption agreement checkbox
6. System generates signature and initials
7. Displays created signature with timestamp

### **5. Document Upload Flow**

1. User clicks "Upload Document" button
2. Selects document type (License or E&O)
3. Uploads file from device
4. For License: Enters license number and expiration
5. For E&O: Selects coverage limit and expiration
6. System validates and stores document
7. Document appears in list with actions menu

### **UI Presentation Guidelines**

- **Desktop View**: Fixed left navigation, tabbed content area, action buttons top-right
- **Mobile View**: Collapsible navigation, stacked tabs, full-width forms
- **Color Scheme**: Error messages in red, success in green, warnings in amber
- **Loading States**: Spinner for data fetching, progress bar for uploads
- **Accessibility**: ARIA labels, keyboard navigation, screen reader support

---

## API Specifications

### Endpoints Required
```http
# Authentication
POST   /api/v1/auth/login                    # Sign in with username/password
POST   /api/v1/auth/logout                   # Sign out current user
POST   /api/v1/auth/forgot-password          # Request password reset
POST   /api/v1/auth/reset-password           # Reset password with token

# User Management
GET    /api/v1/users/profile                # Get current user profile
PUT    /api/v1/users/profile                # Update profile/preferences
PUT    /api/v1/users/password               # Change password
GET    /api/v1/users/{id}/permissions       # Get user permissions

# Contact Information
GET    /api/v1/users/{id}/contact           # Get contact details
PUT    /api/v1/users/{id}/contact           # Update contact info
GET    /api/v1/users/{id}/addresses         # Get addresses
PUT    /api/v1/users/{id}/addresses         # Update addresses

# Digital Signatures
GET    /api/v1/signatures/{user_id}         # Get user signature
POST   /api/v1/signatures                   # Create signature
PUT    /api/v1/signatures/{id}              # Update signature

# Roles & Permissions
GET    /api/v1/roles                        # List all roles
GET    /api/v1/roles/{id}/permissions       # Get role permissions
GET    /api/v1/users/{id}/roles             # Get user roles

# Producer Management
GET    /api/v1/producers                    # List all producers
GET    /api/v1/producers/{id}               # Get producer details
GET    /api/v1/producers/export             # Export producer list

# Document Management
GET    /api/v1/documents                    # List user documents
POST   /api/v1/documents/upload             # Upload document
GET    /api/v1/documents/{id}               # Get document details
DELETE /api/v1/documents/{id}               # Delete document
GET    /api/v1/documents/{id}/history       # Get document history

# Reference Data
GET    /api/v1/languages                    # List available languages
GET    /api/v1/document-types               # List document types
```

### Real-time Updates
```javascript
// WebSocket channels
private-user.{user_id}                      # User profile updates
private-permissions.{user_id}               # Permission changes
private-documents.{user_id}                 # Document notifications
private-tenant.{tenant_id}.users            # All users for tenant
```

---

## Database Schema (Section E)

### New Core Tables

#### signature
```sql
CREATE TABLE signature (
  id INT(11) AUTO_INCREMENT PRIMARY KEY,
  
  -- Business columns
  user_id INT(11) NOT NULL UNIQUE,
  signature_data TEXT NOT NULL,
  initials_data TEXT,
  signature_adopted_name VARCHAR(255) NOT NULL,
  signature_adopted_at TIMESTAMP NOT NULL,
  
  -- Standard fields
  status_id INT(11) NOT NULL,
  created_by INT(11) NOT NULL,
  updated_by INT(11) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Foreign key constraints
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (status_id) REFERENCES status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  
  -- Indexes
  INDEX idx_user (user_id),
  INDEX idx_status (status_id),
  INDEX idx_adopted_at (signature_adopted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### file
```sql
CREATE TABLE file (
  id INT(11) AUTO_INCREMENT PRIMARY KEY,
  
  -- Business columns
  file_type_id INT(11) NOT NULL,
  name VARCHAR(255) NOT NULL,
  path VARCHAR(500) NOT NULL,
  size BIGINT NOT NULL,
  mime_type VARCHAR(100) NOT NULL,
  hash VARCHAR(64),
  metadata JSON,
  
  -- Standard fields
  status_id INT(11) NOT NULL,
  created_by INT(11) NOT NULL,
  updated_by INT(11) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Foreign key constraints
  FOREIGN KEY (file_type_id) REFERENCES file_type(id),
  FOREIGN KEY (status_id) REFERENCES status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  
  -- Indexes
  INDEX idx_file_type (file_type_id),
  INDEX idx_name (name),
  INDEX idx_hash (hash),
  INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### New Reference Tables

#### language
```sql
CREATE TABLE language (
  id INT(11) AUTO_INCREMENT PRIMARY KEY,
  
  -- Business columns
  language_type_id INT(11) NOT NULL,
  code VARCHAR(10) UNIQUE NOT NULL,
  name VARCHAR(100) NOT NULL,
  native_name VARCHAR(100),
  is_default BOOLEAN DEFAULT FALSE,
  
  -- Standard fields
  status_id INT(11) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Foreign key constraints
  FOREIGN KEY (language_type_id) REFERENCES language_type(id),
  FOREIGN KEY (status_id) REFERENCES status(id),
  
  -- Indexes
  INDEX idx_code (code),
  INDEX idx_status (status_id),
  INDEX idx_default (is_default)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### language_type
```sql
CREATE TABLE language_type (
  id INT(11) AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(50) UNIQUE NOT NULL,
  name VARCHAR(100) NOT NULL,
  description TEXT NULL,
  status_id INT(11) NOT NULL,
  
  -- Audit fields
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Foreign key constraints
  FOREIGN KEY (status_id) REFERENCES status(id),
  
  -- Indexes
  INDEX idx_code (code),
  INDEX idx_status (status_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### file_type
```sql
CREATE TABLE file_type (
  id INT(11) AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(50) UNIQUE NOT NULL,
  name VARCHAR(100) NOT NULL,
  description TEXT NULL,
  allowed_extensions JSON,
  max_size_mb INT DEFAULT 10,
  status_id INT(11) NOT NULL,
  
  -- Audit fields
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Foreign key constraints
  FOREIGN KEY (status_id) REFERENCES status(id),
  
  -- Indexes
  INDEX idx_code (code),
  INDEX idx_status (status_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Modified Tables

#### ALTER TABLE user
```sql
-- Add authentication and preference fields
ALTER TABLE user 
ADD COLUMN username VARCHAR(50) UNIQUE AFTER id,
ADD COLUMN password VARCHAR(255) AFTER username,
ADD COLUMN signature_id INT(11) NULL,
ADD COLUMN language_preference_id INT(11) NULL;

-- Add foreign key constraints
ALTER TABLE user
ADD CONSTRAINT fk_user_signature 
FOREIGN KEY (signature_id) REFERENCES signature(id),
ADD CONSTRAINT fk_user_language 
FOREIGN KEY (language_preference_id) REFERENCES language(id);

-- Add indexes
ALTER TABLE user
ADD INDEX idx_username (username),
ADD INDEX idx_signature (signature_id),
ADD INDEX idx_language_pref (language_preference_id);
```

#### ALTER TABLE permission
```sql
-- Add descriptive fields
ALTER TABLE permission 
ADD COLUMN code VARCHAR(50) UNIQUE NOT NULL AFTER id,
ADD COLUMN name VARCHAR(100) NOT NULL AFTER code,
ADD COLUMN description TEXT AFTER name,
ADD COLUMN category VARCHAR(50) AFTER description;

-- Add indexes
ALTER TABLE permission
ADD INDEX idx_code (code),
ADD INDEX idx_category (category);
```

#### ALTER TABLE role
```sql
-- Add descriptive fields
ALTER TABLE role 
ADD COLUMN code VARCHAR(50) UNIQUE NOT NULL AFTER id,
ADD COLUMN name VARCHAR(100) NOT NULL AFTER code,
ADD COLUMN description TEXT AFTER name;

-- Add indexes
ALTER TABLE role
ADD INDEX idx_code (code);
```

#### ALTER TABLE name
```sql
-- Add individual name components
ALTER TABLE name 
ADD COLUMN first_name VARCHAR(100) AFTER id,
ADD COLUMN last_name VARCHAR(100) AFTER first_name,
ADD COLUMN middle_name VARCHAR(100) AFTER last_name;

-- Add index for name searches
ALTER TABLE name
ADD INDEX idx_full_name (last_name, first_name);
```

---

## Implementation Notes

### Dependencies
- Laravel Authentication system for secure login/logout
- Redis for session management and permission caching
- Email service (SMTP) for password reset functionality
- File storage system (local with S3/CDN migration path)
- PDF generation library for producer exports
- Frontend framework (React) for responsive UI

### Migration Considerations
- Existing users will need username assignment
- Default language preferences to be set for all users
- Existing documents to be migrated to new file storage
- Role and permission data to be seeded from business requirements
- Password hashes to be verified for compatibility

### Performance Considerations
- **Expected Volumes**: 10,000 users, 500,000 documents within 5 years
- **Query Optimization**: Indexes on all foreign keys and frequently searched fields
- **Caching Strategy**: Redis caching for permissions, roles, and user sessions
- **File Storage**: CDN integration for document delivery at scale
- **Database Growth**: Partitioning strategy for document and file tables

---

## Quality Checklist

### Pre-Implementation
- [x] All UI fields mapped to database columns
- [x] Existing entities reused where possible
- [x] Reference tables created for all ENUMs
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
- [x] **GR-01**: Identity & Access Management patterns applied
- [x] **GR-36**: Authentication & Permissions framework implemented
- [x] **GR-41**: Database standards followed (status_id, audit fields, naming)
- [x] **GR-52**: Universal Entity Management leveraged for existing entities
- [x] **GR-69**: Producer Portal Architecture navigation integration