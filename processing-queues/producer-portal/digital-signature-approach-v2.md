# Digital Signature System - Database and Technology Approach v2
- instead of audit, use action table, right?
## Executive Summary

This document outlines a comprehensive database and technology approach for implementing digital signatures in the Producer Portal. The solution leverages existing database infrastructure, supports both in-person and remote signing scenarios, provides full legal compliance, and offers significant cost savings compared to third-party solutions like DocuSign.

## 1. Database Schema Design

### 1.1 Existing Tables to Leverage

#### signature (Existing - Enhance)
Current structure already includes:
- `id` - Primary key
- `user_id` - User who created signature
- `signature_data` - Base64 signature image
- `initials_data` - Base64 initials image
- `signature_adopted_name` - Name for adoption
- `signature_adopted_at` - Adoption timestamp
- `status_id` - Status reference
- Standard audit fields (created_by, created_at, updated_by, updated_at)

**Required Enhancements:**
```sql
ALTER TABLE signature
ADD COLUMN signature_type_id INT(11) AFTER user_id,
ADD COLUMN driver_id INT(11) AFTER signature_type_id,
ADD COLUMN signing_method VARCHAR(20) DEFAULT 'in_person' AFTER signature_adopted_at,
ADD COLUMN signing_session_id INT(11) AFTER signing_method,
ADD COLUMN signing_ip VARCHAR(45) AFTER signing_session_id,
ADD COLUMN signing_user_agent TEXT AFTER signing_ip,
ADD COLUMN remote_sent_at TIMESTAMP NULL AFTER signing_user_agent,
ADD COLUMN remote_signed_at TIMESTAMP NULL AFTER remote_sent_at,
ADD COLUMN auth_method VARCHAR(50) AFTER remote_signed_at,
ADD COLUMN auth_attempts INT DEFAULT 0 AFTER auth_method,
ADD FOREIGN KEY (signature_type_id) REFERENCES signature_type(id),
ADD FOREIGN KEY (driver_id) REFERENCES driver(id),
ADD FOREIGN KEY (signing_session_id) REFERENCES session(id),
ADD INDEX idx_signing_method (signing_method),
ADD INDEX idx_driver (driver_id);
```

#### document (Existing - Use as-is)
Already includes:
- `id` - Primary key
- `document_type_id` - Type of document
- `file_id` - Link to file storage
- `is_signed` - Signing status
- `signed_at` - When signed
- `status_id` - Document status
- Standard audit fields

#### file (Existing - Use as-is)
Already includes:
- `id` - Primary key
- `file_type_id` - Type of file
- `name` - File name
- `path` - Storage path
- `hash` - File hash for integrity
- `metadata` - JSON metadata
- Standard audit fields

Perfect for storing:
- Generated PDF documents
- Signature image files (if needed separately)

#### session (Existing - Use as-is)
Already includes:
- `id` - Primary key
- `session_type_id` - Type of session
- Standard audit fields

**Enhancement for remote signing:**
```sql
-- Add session columns if not present
ALTER TABLE session
ADD COLUMN IF NOT EXISTS session_token VARCHAR(255) UNIQUE AFTER session_type_id,
ADD COLUMN IF NOT EXISTS user_id INT(11) AFTER session_token,
ADD COLUMN IF NOT EXISTS quote_id INT(11) AFTER user_id,
ADD COLUMN IF NOT EXISTS policy_id INT(11) AFTER quote_id,
ADD COLUMN IF NOT EXISTS data JSON AFTER policy_id,
ADD COLUMN IF NOT EXISTS ip_address VARCHAR(45) AFTER data,
ADD COLUMN IF NOT EXISTS user_agent TEXT AFTER ip_address,
ADD COLUMN IF NOT EXISTS expires_at TIMESTAMP NULL AFTER user_agent,
ADD COLUMN IF NOT EXISTS last_activity_at TIMESTAMP NULL AFTER expires_at,
ADD COLUMN IF NOT EXISTS terminated_at TIMESTAMP NULL AFTER last_activity_at;
```

#### audit (Existing - Use as-is)
Already includes:
- `id` - Primary key
- `audit_type_id` - Type of audit event
- Standard audit fields

Will be used for signature audit trail with new audit types.
- instead of audit use action table right? actual audit information can be found in the signature record itself

#### template (Existing - Use as-is)
Already includes:
- `id` - Primary key
- `template_type_id` - Type of template
- Standard audit fields

Can be extended with signature template data in metadata.

### 1.2 New Tables Required

#### signature_type
```sql
CREATE TABLE IF NOT EXISTS signature_type (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    status_id INT(11) NOT NULL,
    created_by INT(11) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INT(11),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_code (code),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default types
INSERT INTO signature_type (code, name, description, is_default, status_id, created_by) VALUES
('full_name', 'Full Name Signature', 'Complete legal signature', 1, 1, 1),
('initials', 'Initials Only', 'First and last initials', 0, 1, 1),
('electronic', 'Electronic Signature', 'Typed or generated signature', 0, 1, 1),
('drawn', 'Hand Drawn', 'Canvas/touch drawn signature', 0, 1, 1);
```

#### map_document_signature
```sql
CREATE TABLE IF NOT EXISTS map_document_signature (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    document_id INT(11) NOT NULL,
    signature_id INT(11) NOT NULL,
    
    -- Signature placement
    page_number INT NOT NULL DEFAULT 1,
    x_position DECIMAL(5,2),               -- Percentage from left
    y_position DECIMAL(5,2),               -- Percentage from top
    width DECIMAL(5,2),                    -- Percentage width
    height DECIMAL(5,2),                   -- Percentage height
    
    -- Signature type on this location
    signature_type VARCHAR(20) DEFAULT 'signature', -- 'signature' or 'initials'
    
    -- Tracking
    applied_at TIMESTAMP NULL,
    applied_by INT(11),
    
    -- Standard fields
    status_id INT(11) NOT NULL DEFAULT 1,
    created_by INT(11) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INT(11),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes and constraints
    UNIQUE KEY idx_document_signature (document_id, signature_id, page_number, signature_type),
    INDEX idx_signature (signature_id),
    FOREIGN KEY (document_id) REFERENCES document(id) ON DELETE CASCADE,
    FOREIGN KEY (signature_id) REFERENCES signature(id) ON DELETE CASCADE,
    FOREIGN KEY (applied_by) REFERENCES user(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### map_document_template
```sql
-- This likely already exists, but if not:
CREATE TABLE IF NOT EXISTS map_document_template (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    document_id INT(11) NOT NULL,
    template_id INT(11) NOT NULL,
    
    -- Template data
    data JSON,                             -- Template-specific data including signature fields
    
    -- Standard fields
    status_id INT(11) NOT NULL DEFAULT 1,
    created_by INT(11) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INT(11),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes and constraints
    UNIQUE KEY idx_document_template (document_id, template_id),
    INDEX idx_template (template_id),
    FOREIGN KEY (document_id) REFERENCES document(id) ON DELETE CASCADE,
    FOREIGN KEY (template_id) REFERENCES template(id) ON DELETE CASCADE,
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 1.3 Audit Integration

Use existing `audit` table with new audit types:
```sql
INSERT INTO audit_type (code, name, description, status_id, created_by) VALUES
('signature_created', 'Signature Created', 'New signature record created', 1, 1),
('signature_adopted', 'Signature Adopted', 'User adopted signature', 1, 1),
('signature_sent', 'Signature Request Sent', 'Remote signature request sent', 1, 1),
('signature_viewed', 'Signature Request Viewed', 'Remote signature link accessed', 1, 1),
('signature_authenticated', 'Signature Authentication', 'User authenticated for signing', 1, 1),
('signature_applied', 'Signature Applied', 'Signature applied to document', 1, 1),
('signature_rejected', 'Signature Rejected', 'Signature request rejected', 1, 1);
```

Audit records will store detailed JSON data:
```json
{
  "signature_id": 123,
  "document_id": 456,
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "auth_method": "dob",
  "location": "City, State"
}
```

### 1.4 Session Type for Remote Signing

```sql
INSERT INTO session_type (code, name, description, is_default, status_id, created_by) VALUES
('remote_signing', 'Remote Signing Session', 'Customer remote signature collection', 0, 1, 1);
```

Session data structure for remote signing:
```json
{
  "quote_id": 123,
  "driver_id": 456,
  "documents": ["doc1", "doc2"],
  "progress": {
    "authenticated": true,
    "signature_created": true,
    "documents_signed": ["doc1"],
    "payment_completed": false
  },
  "auth": {
    "method": "dob",
    "attempts": 1,
    "verified_at": "2023-10-15 14:30:00"
  }
}
```

## 2. Technology Implementation

### 2.1 Signature Storage Strategy

1. **For Font-Styled Signatures (Generated)**:
   - Store as TEXT in `signature.signature_data`
   - Generate PDF on-demand using chosen font
   - No separate file storage needed

2. **For Hand-Drawn Signatures**:
   - Store base64 in `signature.signature_data`
   - Optionally create file record for permanent storage
   - Link via `file` table if needed

3. **For Documents**:
   - Use existing `document` and `file` tables
   - Set `document.is_signed = true` when signed
   - Store signed PDF in `file` table
   - Link signatures via `map_document_signature`

### 2.2 Template Integration

Leverage existing template system:
```json
// Template metadata for signature fields
{
  "signature_fields": [
    {
      "field_name": "insured_signature",
      "page": 1,
      "x": 10.5,
      "y": 85.2,
      "width": 25,
      "height": 5,
      "type": "signature",
      "required": true
    },
    {
      "field_name": "insured_initials",
      "page": 3,
      "x": 70,
      "y": 90,
      "width": 10,
      "height": 3,
      "type": "initials",
      "required": false
    }
  ]
}
```

### 2.3 Implementation Architecture

```
Laravel Application
├── Services
│   ├── SignatureService
│   │   ├── create() - Create signature record
│   │   ├── adopt() - Adoption process
│   │   ├── generateFromName() - Font-based generation
│   │   └── applyToDocument() - Apply to PDF
│   │
│   ├── SignatureSessionService
│   │   ├── createRemoteSession() - Uses session table
│   │   ├── validateToken() - Token verification
│   │   ├── trackProgress() - Update session data
│   │   └── terminate() - Close session
│   │
│   └── SignatureAuditService
│       ├── logEvent() - Write to audit table
│       ├── getTrail() - Retrieve audit history
│       └── generateReport() - Compliance reports
│
├── Controllers
│   ├── SignatureController - In-person signing
│   ├── RemoteSignatureController - Remote portal
│   └── SignatureMonitorController - Producer dashboard
│
└── PDF Generation
    ├── Blade Templates - UI rendering
    ├── Laravel-Snappy - PDF generation
    └── Signature Overlay - Apply signatures to PDFs
```

## 3. Cost-Benefit Analysis

### 3.1 Custom Implementation Advantages

1. **Zero Per-Transaction Costs**
   - DocuSign: $0.50-1.00 per envelope
   - Custom: $0 per signature
   - At 2000 signatures/month: Save $1,000-2,000/month

2. **Full Integration Control**
   - Direct database integration
   - Custom workflows for insurance
   - No external API dependencies

3. **Leverages Existing Infrastructure**
   - Uses existing tables (80% reuse)
   - Minimal new table creation
   - Existing audit system
   - Current session management

### 3.2 Implementation Timeline

**Phase 1: Foundation (2 weeks)**
- Enhance signature table
- Create signature_type table
- Create map_document_signature table
- Basic signature capture UI

**Phase 2: In-Person Signing (2 weeks)**
- Signature generation service
- PDF integration
- Adoption workflow
- Audit logging

**Phase 3: Remote Signing (3 weeks)**
- Session integration
- Portal development
- Authentication flow
- Progress tracking

**Phase 4: Testing & Deployment (1 week)**
- Security testing
- Performance validation
- Production deployment

**Total: 8 weeks** (vs 16-18 weeks in v1)

## 4. Security & Compliance

### 4.1 Audit Trail Using Existing Infrastructure

Each signature event creates audit record:
1. Signature created (audit_type: signature_created)
2. Authentication performed (audit_type: signature_authenticated)
3. Signature adopted (audit_type: signature_adopted)
4. Applied to document (audit_type: signature_applied)

### 4.2 Session Security

- Use existing session table with tokens
- Automatic expiration via expires_at
- IP and user agent validation
- One-time use enforcement

### 4.3 Data Protection

- Signatures in database (encrypted at rest)
- Documents in file system via file table
- Hash verification for integrity
- HTTPS-only transmission

## 5. Summary of Changes

### 5.1 Database Modifications

**New Tables (3)**:
1. `signature_type` - Categorize signatures
2. `map_document_signature` - Link signatures to documents
3. `map_document_template` - Template associations (if not exists)

**Enhanced Tables (2)**:
1. `signature` - Add remote signing fields
2. `session` - Add columns if missing

**New Audit Types (7)**:
- Various signature-related audit events

### 5.2 Key Design Decisions

1. **Reuse Existing Infrastructure**:
   - audit table for audit trail (no new audit log table)
   - session/session_type for remote access
   - file/document for storage
   - template for signature templates

2. **Follow Naming Conventions**:
   - map_* for relationship tables
   - *_type for lookup tables
   - Standard audit fields

3. **Minimize Custom Code**:
   - Leverage Laravel's existing features
   - Use established patterns
   - Standard JSON storage in existing columns

This approach provides a robust, cost-effective digital signature solution that integrates seamlessly with the existing database structure while maintaining full legal compliance and security standards.

---

**Document Version**: 2.0  
**Date**: 2025-07-23  
**Status**: Ready for Review  
**Key Changes from v1**: 
- Aligned with existing database structure
- Reduced new tables from 4 to 3
- Leverages existing audit and session infrastructure
- Uses established naming conventions