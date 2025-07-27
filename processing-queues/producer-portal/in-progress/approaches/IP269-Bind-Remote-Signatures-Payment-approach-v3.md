# IP269-Bind-Remote-Signatures-Payment - Implementation Approach v3
- we have a lnguage selection radio buttons
- a phone number field to send link via sms for signing documents
  - a preview link that opens up what the sms will look like and say
- send by email with email address
  - a preview link that opens up what the email will look like and say
- the previes should pull from our template table

## Revision Notes
- **v3 Changes**: Aligned with digital-signature-approach-v3.md database design
- **Key Updates**: Uses action table for workflow tracking, map_document_signature for associations, comprehensive audit in signature table

## Requirement Understanding
The Remote Signatures & Payment flow enables insureds to complete policy binding independently through a secure web portal accessed via email/SMS link. The system must authenticate users via date of birth, capture electronic signatures, present documents for signing, collect payment (E-Check or Credit Card), handle convenience fees, and track the entire process for producer visibility. This creates a fully digital, self-serve binding experience.

## Domain Classification
- Primary Domain: Producer Portal / Quote Binding
- Cross-Domain Impact: Yes - Customer portal, communications, payments, policy issuance
- Complexity Level: High

## Pattern Analysis

### Reusable Patterns Identified
- [GR-69]: Producer Portal Architecture - Remote binding patterns
- [GR-44]: Communication Architecture - Email/SMS delivery
- [GR-01]: Identity & Access Management - DOB authentication
- [GR-52]: Universal Entity Management - Document and payment entities
- [GR-20]: Business Logic Standards - Remote signing rules

### Domain-Specific Needs
- Secure portal access via unique links
- Date of birth authentication
- Remote signature generation and adoption
- Web-based document viewer
- Mobile-optimized signing experience
- Producer monitoring dashboard
- Payment collection with fee handling
- Suspense visibility for missing items

## Proposed Implementation

### Simplification Approach
- Current Complexity: Remote portal, authentication, signing, payment, monitoring
- Simplified Solution: Web portal using session infrastructure with v3 architecture
- Trade-offs: Leverages existing tables, minimal new additions

### Technical Approach
1. **Phase 1**: Communication Delivery
   - [ ] Generate secure signing token
   - [ ] Create session record with type 'remote_signing'
   - [ ] Create email/SMS templates
   - [ ] Include branded content
   - [ ] Send via communication system
   - [ ] Track delivery status
   - [ ] Create action for signature_sent

2. **Phase 2**: Portal Authentication
   - [ ] Build web portal interface
   - [ ] Validate session token
   - [ ] Implement DOB verification
   - [ ] Update session authentication data
   - [ ] Handle invalid access
   - [ ] Track attempts in session.data
   - [ ] Create action for signature_viewed

3. **Phase 3**: Remote Signature Setup
   - [ ] Load insured name from driver
   - [ ] Generate signature/initials
   - [ ] Display for review
   - [ ] Require adoption
   - [ ] Store in signature table with full audit
   - [ ] Set signature_type_id
   - [ ] Link to session via signing_session_id
   - [ ] Create action for signature_created

4. **Phase 4**: Document Signing
   - [ ] Load required documents
   - [ ] Embed PDF viewer
   - [ ] Show signature locations from template
   - [ ] Track signing progress
   - [ ] Create map_document_signature records
   - [ ] Update document.is_signed
   - [ ] Store document hash in signature
   - [ ] Create action for signature_applied

5. **Phase 5**: Payment Collection
   - [ ] Display payment summary
   - [ ] Offer E-Check/Credit Card
   - [ ] Handle convenience fees
   - [ ] Process payment via transaction
   - [ ] Show confirmation
   - [ ] Update session.data with payment info
   - [ ] Create action for payment_processed

6. **Phase 6**: Producer Monitoring
   - [ ] Show communication status
   - [ ] Display signing progress from session
   - [ ] Track payment status
   - [ ] List open suspenses
   - [ ] Enable link resending
   - [ ] Query session and action data
   - [ ] Show audit trail from signature table

7. **Phase 7**: Policy Activation
   - [ ] Validate all requirements
   - [ ] Generate final documents
   - [ ] Store in file table
   - [ ] Create policy record
   - [ ] Send confirmations
   - [ ] Close quote
   - [ ] Terminate session
   - [ ] Create action for policy_bound

## Risk Assessment
- **Risk 1**: Security vulnerabilities → Mitigation: Token expiration in session, HTTPS only
- **Risk 2**: Authentication bypass → Mitigation: DOB + token validation, audit in signature
- **Risk 3**: Mobile signing issues → Mitigation: Responsive design, testing
- **Risk 4**: Payment failures → Mitigation: Clear error handling, retry
- **Risk 5**: Communication delivery → Mitigation: Multiple channels, tracking
- **Risk 6**: Session hijacking → Mitigation: IP validation in signature table, user agent checks

## Context Preservation
- Key Decisions: Use session infrastructure with v3 enhancements, audit trail in signature table
- Dependencies: Session tables, communication system, payment gateway, action tracking
- Future Impact: Foundation for all remote customer interactions with full compliance

## Database Requirements Summary
- **New Tables**: 3 tables (signature_type, map_document_signature, map_document_template)
- **Existing Tables**: 17+ tables will be reused
- **Modified Tables**: 2 tables (signature, session)

## Database Schema Requirements

### Using Enhanced Session Infrastructure

#### session_type (Add new type)
```sql
INSERT INTO session_type (code, name, description, is_default, status_id, created_by) VALUES
('remote_signing', 'Remote Signing Session', 'Customer remote signature collection', 0, 1, 1);
```

#### session (Enhanced if needed)
```sql
-- Add columns if not present:
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

### Session Data Structure
Store in session.data JSON:
```json
{
  "authentication": {
    "dob_verified": true,
    "verified_at": "2023-10-15 14:30:00",
    "attempts": 1
  },
  "signing": {
    "driver_id": 123,
    "signature_id": 456,
    "documents_signed": ["doc1", "doc2"],
    "completed_at": "2023-10-15 14:45:00"
  },
  "payment": {
    "transaction_id": 789,
    "method": "credit_card",
    "amount": 150.00,
    "completed_at": "2023-10-15 14:50:00"
  },
  "progress": {
    "current_step": "payment",
    "steps_completed": ["auth", "signature", "documents"],
    "suspenses": []
  }
}
```

### New Tables (from v3 approach)

1. **signature_type**: Categorize signature types
2. **map_document_signature**: Link signatures to documents with placement
3. **map_document_template**: Template associations if needed

### Existing Tables to Use

1. **session**: Remote access tracking
   - Track all portal sessions
   - Store progress in JSON data
   - Monitor expiration
   - Link to quote/policy

2. **session_type**: Session categories
   - Define remote signing type
   - Control session behavior
   - Set expiration rules

3. **communication**: Track sent messages
   - Store email/SMS records
   - Include signing links with token
   - Track open rates
   - Monitor click-through

4. **signature**: Remote signatures with full audit
   - Store generated signatures
   - Track adoption remotely
   - Complete audit trail (WHO, WHAT, WHEN, WHERE, HOW)
   - Link to session via signing_session_id
   - All compliance data in one place

5. **document**: Signed documents
   - Track signing status
   - Store completed PDFs
   - Link signatures via map_document_signature

6. **file**: PDF storage
   - Store signed documents
   - Hash verification
   - Secure access

7. **map_document_signature**: Signature associations
   - Link signatures to documents
   - Track placement coordinates
   - Record application timestamp

8. **transaction**: Payment records
   - Process remote payments
   - Track payment method
   - Store fee information

9. **payment_method**: Payment options
   - E-Check configuration
   - Credit Card processing
   - Fee structures

10. **suspense**: Missing items
    - Track incomplete items
    - Display to producer
    - Monitor resolution

11. **quote**: Source quote
    - Premium information
    - Coverage details
    - Customer data

12. **driver**: Customer info
    - Date of birth for auth
    - Contact information
    - Name for signatures

13. **policy**: Final policy
    - Create upon completion
    - Activate coverage
    - Link all components

14. **fee**: Convenience fees
    - Credit card fees
    - Dynamic configuration
    - Clear disclosure

15. **template**: Communication templates
    - Email/SMS templates
    - Multi-language support
    - Dynamic token insertion

16. **action**: Workflow tracking
    - Track all events
    - No detailed data (in signature)
    - Monitor progress

17. **action_type**: Event types
    - signature_sent
    - signature_viewed
    - signature_authenticated
    - signature_created
    - signature_applied
    - payment_processed
    - policy_bound

### Security Enhancements
- Cryptographically secure token in session.session_token
- Automatic expiration via expires_at
- IP address validation stored in signature table
- User agent consistency checks in signature table
- Rate limiting on authentication attempts
- Session termination on completion
- Complete audit trail in signature table
- Document hash verification

### Query Examples
```sql
-- Get active remote signing sessions with progress
SELECT 
    s.id,
    s.session_token,
    s.quote_id,
    st.name as session_type,
    s.data->>'$.progress.current_step' as current_step,
    s.last_activity_at,
    s.expires_at
FROM session s
JOIN session_type st ON s.session_type_id = st.id
WHERE st.code = 'remote_signing'
AND s.expires_at > NOW()
AND s.terminated_at IS NULL;

-- Get signature audit trail for compliance
SELECT 
    s.id,
    s.signature_adopted_at,
    s.signing_method,
    s.signing_ip,
    s.geographic_location,
    s.auth_method,
    s.document_hash,
    d.name as signer_name
FROM signature s
JOIN driver d ON s.driver_id = d.id
WHERE s.signing_session_id = ?;
```

## Business Summary for Stakeholders
### What We're Building
A secure self-service portal that allows customers to complete insurance policy binding remotely using the v3 architecture. The solution leverages enhanced session management for secure access and stores comprehensive audit trails directly in the signature table for compliance. Customers authenticate via date of birth, sign documents electronically, and complete payment in one seamless flow.

### Why It's Needed
Many customers prefer to complete insurance purchases on their own time without visiting an office. By using the v3 architecture with complete audit trails in the signature table, we ensure legal compliance, security, and full visibility while reducing development complexity through maximum reuse of existing infrastructure.

### Expected Outcomes
- Secure remote signing with session tokens
- Complete audit trail in signature table
- Enhanced security with full tracking
- Consistent workflow via action table
- Producer visibility into progress
- Reduced office visits
- Faster policy issuance
- Improved customer satisfaction

## Technical Summary for Developers
### Key Technical Decisions
- **Architecture Pattern**: Session-based remote access with v3 design
- **Session Management**: Enhanced session table with JSON progress
- **Audit Storage**: Complete trail in signature table
- **Document Association**: map_document_signature for linking
- **Security Model**: Token-based with automatic expiration
- **Progress Tracking**: Step-based progress in session data
- **Workflow Visibility**: Action table for event tracking

### Implementation Guidelines
- Use session service for all operations
- Store progress milestones in JSON data
- Implement secure token generation
- Build DOB verification against driver
- Track all audit data in signature table
- Create map_document_signature records
- Use session expiration for security
- Query actions for workflow monitoring
- Terminate session on completion
- Handle session recovery scenarios

### Session Lifecycle
```
1. Create session (type: remote_signing)
2. Generate secure token
3. Send communication with token
4. Customer authenticates (DOB)
5. Create signature with full audit
6. Apply signatures via map_document_signature
7. Process payment
8. Create policy
9. Terminate session
10. Archive for compliance
```

## Validation Criteria
### Pre-Implementation Checkpoints
- [x] Session tables available
- [x] Communication system ready
- [x] Signature infrastructure exists
- [x] Payment processing available
- [x] Document system ready
- [x] Fee configuration supported
- [x] Action table exists
- [ ] New tables need creation (3)

### Success Metrics
- [ ] Sessions create with tokens
- [ ] Links include session tokens
- [ ] DOB authentication works
- [ ] Progress tracks in JSON
- [ ] Signatures store full audit trail
- [ ] Documents link via map_document_signature
- [ ] Payments update sessions
- [ ] Producer queries show progress
- [ ] Sessions expire properly
- [ ] Actions track all events
- [ ] Complete compliance trail

## Approval Section
**Status**: Ready for Review  
**Database Changes**: 3 new tables, 2 enhanced tables  
**Pattern Reuse**: 85% - Maximum reuse with v3 architecture  
**Risk Level**: High - Security and payment considerations  
**Next Steps**: Review v3 approach, implement with enhanced audit  
**Reviewer Comments**: [Updated to align with v3 database design]  
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER