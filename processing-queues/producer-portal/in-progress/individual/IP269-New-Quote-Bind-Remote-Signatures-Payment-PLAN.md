# IP269-New-Quote-Bind-Remote-Signatures-Payment - Implementation Plan

## Requirement Overview

### Purpose
This experience facilitates a fully digital and seamless close-out of the quoting process by enabling insureds to:
- Electronically sign documents remotely via email/SMS link
- Make payments through a self-service portal
- Complete purchase without agent or in-person interaction
- Support modern, self-serve insurance model

### Scope
- Email/SMS notification system with signing links
- Web-based signing portal with authentication
- Multi-language support
- Remote signature capture and adoption
- Self-service payment collection
- Producer monitoring dashboard

## Entity Analysis

### New Entities Required

1. **remote_signing_session**
   - Unique session tokens
   - Expiration tracking
   - Authentication status
   - Language preference

2. **signing_notification**
   - Email/SMS delivery tracking
   - Language selection
   - Template used
   - Delivery status

3. **remote_signature_auth**
   - Date of birth verification
   - Session validation
   - Failed attempt tracking
   - IP/device logging

4. **signing_portal_config**
   - Branding per program
   - Language options
   - Portal customization
   - Legal disclaimers

### Existing Entities Involved

- **quote**: Source data for signing
- **communication**: Notification tracking (GR-44)
- **signature**: Remote signature storage
- **document**: Documents to sign
- **payment_method**: Payment collection
- **policy**: Created after completion

## Global Requirements Alignment

### Primary GRs
- **GR-44 (Communication)**: Email/SMS delivery
- **GR-52 (Universal Entity)**: SendGrid/Twilio
- **GR-46 (S3 Storage)**: Document storage
- **GR-36 (Authentication)**: DOB verification
- **GR-43 (Document Generation)**: Dynamic PDFs

### Supporting GRs
- **GR-11 (Accessibility)**: Portal accessibility
- **GR-12 (Security)**: Secure authentication
- **GR-24 (Data Security)**: PCI compliance
- **GR-51 (Compliance)**: Legal signatures

## Database Schema Planning

### Core Tables

1. **remote_signing_session**
   ```sql
   - id (PK)
   - quote_id (FK)
   - session_token (unique, UUID)
   - expires_at
   - language_code
   - is_authenticated (boolean)
   - authenticated_at
   - completion_status
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

2. **signing_notification**
   ```sql
   - id (PK)
   - remote_signing_session_id (FK)
   - communication_id (FK) -- GR-44
   - notification_type (email, sms)
   - recipient_address
   - language_code
   - template_name
   - sent_at
   - opened_at
   - clicked_at
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

3. **remote_signature_auth**
   ```sql
   - id (PK)
   - remote_signing_session_id (FK)
   - provided_dob
   - is_valid (boolean)
   - attempt_number
   - ip_address
   - user_agent
   - created_at
   ```

4. **signing_portal_activity**
   ```sql
   - id (PK)
   - remote_signing_session_id (FK)
   - activity_type (view, sign, payment, complete)
   - activity_data (JSON)
   - occurred_at
   - status_id (FK)
   ```

## API Endpoints

### Portal Endpoints
```
POST   /api/v1/signing-portal/sessions
POST   /api/v1/signing-portal/authenticate
GET    /api/v1/signing-portal/sessions/{token}/documents
POST   /api/v1/signing-portal/sessions/{token}/signatures/adopt
POST   /api/v1/signing-portal/sessions/{token}/documents/{id}/sign
GET    /api/v1/signing-portal/sessions/{token}/payment-info
POST   /api/v1/signing-portal/sessions/{token}/payment
POST   /api/v1/signing-portal/sessions/{token}/complete
```

### Producer Endpoints
```
POST   /api/v1/quotes/{quote_id}/send-signing-link
GET    /api/v1/quotes/{quote_id}/signing-status
POST   /api/v1/quotes/{quote_id}/resend-notification
GET    /api/v1/quotes/{quote_id}/signing-activity
```

### Real-time Updates
```javascript
private-quote.{quote_id}.remote-signing-updates
private-producer.{producer_id}.signing-notifications
```

## Integration Points

### External Services (GR-52/GR-44)
1. **SendGrid Email**
   - Template management
   - Multi-language support
   - Click tracking
   - Delivery webhooks

2. **Twilio SMS**
   - SMS delivery
   - Short link generation
   - Delivery confirmation
   - Language support

### Internal Services
1. **NotificationService**
   - Template selection
   - Language routing
   - Retry logic
   - Status tracking

2. **AuthenticationService**
   - DOB verification
   - Session management
   - Security logging
   - Attempt limiting

3. **PortalService**
   - Session creation
   - Document preparation
   - Progress tracking
   - Completion handling

## Implementation Considerations

### Key Patterns
1. **Secure Session Management**
   - Time-limited tokens
   - One-time use links
   - Session invalidation
   - Activity logging

2. **Multi-Language Support**
   - Template per language
   - Dynamic content loading
   - RTL support consideration
   - Cultural formatting

3. **Progressive Enhancement**
   - Mobile-first design
   - Touch-friendly signing
   - Offline capability
   - Resume functionality

4. **Producer Visibility**
   - Real-time status
   - Activity timeline
   - Resend capability
   - Completion alerts

### Technical Decisions
- JWT for session tokens
- Vue.js SPA for portal
- i18n for translations
- Redis for session storage
- WebSocket for live updates

## Quality Checkpoints

### Pre-Implementation
- [ ] Review authentication patterns
- [ ] Validate multi-language setup
- [ ] Check notification templates
- [ ] Review security requirements

### Implementation
- [ ] DOB auth working
- [ ] Notifications delivered
- [ ] Signatures captured
- [ ] Payments processed

### Post-Implementation
- [ ] Security penetration test
- [ ] Multi-language testing
- [ ] Mobile device testing
- [ ] Load testing portal

## Dependencies

### Upstream
- Quote ready for binding
- Documents generated
- Premium calculated
- Contact info available

### Downstream
- Policy activation
- Coverage effective
- Payment processing
- Commission calculation

## Risk Mitigation

1. **Security**: Time-limited sessions
2. **Delivery**: Multiple channels (email/SMS)
3. **Authentication**: Rate limiting on DOB
4. **Completion**: Save progress capability

## UI/UX Specifications

### Email/SMS Templates
- Clear CTA buttons
- Branding consistent
- Mobile responsive
- Language appropriate

### Portal Landing
- Welcome message
- Insurer branding
- DOB entry form
- Security messaging

### Signature Flow
- Name/initials display
- Signature generation
- Touch-friendly drawing
- Clear progression

### Document Review
- PDF viewer embedded
- Sign indicators
- Progress tracking
- Error handling

### Payment Collection
- Method selection
- Form simplicity
- Fee transparency
- Security badges

### Producer Dashboard
- Send status display
- Activity timeline
- Resend button
- Completion indicators

## Cross-Domain Considerations

- **Communication**: Notification delivery
- **Policy**: Remote activation
- **Accounting**: Payment collection
- **Compliance**: Legal signatures

## Next Steps

1. Create session management system
2. Build notification templates
3. Implement DOB authentication
4. Create signing portal SPA
5. Add multi-language support
6. Integrate payment processing
7. Build producer dashboard
8. Implement activity tracking