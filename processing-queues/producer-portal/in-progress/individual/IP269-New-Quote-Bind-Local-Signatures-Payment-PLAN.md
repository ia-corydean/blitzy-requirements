# IP269-New-Quote-Bind-Local-Signatures-Payment - Implementation Plan

## Requirement Overview

### Purpose
This experience supports the final steps of insurance policy activation by streamlining document signing and payment in a single cohesive flow. It aims to:
- Enable seamless signing of all required legal documents in person
- Provide flexible payment methods (Producer E-Check, Insured E-Check, Credit Card)
- Ensure compliant submission with real-time confirmation
- Support both desktop and mobile signers

### Scope
- In-person signature capture and adoption
- Document viewer with e-sign capability
- Multiple payment method support
- Re-rating warning for backward navigation
- Document package email delivery
- Policy activation upon completion

## Entity Analysis

### New Entities Required

1. **signature**
   - Signature image/data storage
   - Type (full signature, initials)
   - Associated person

2. **document_signature_location**
   - X/Y coordinates for signatures
   - Page number and document
   - Signature or initial type

3. **signed_document**
   - Completed document storage
   - Signature timestamps
   - Legal compliance data

4. **payment_method**
   - E-Check routing/account
   - Credit card details (tokenized)
   - Producer vs insured indicator

5. **bind_payment**
   - Payment transaction record
   - Amount, fees, method
   - Gateway response

6. **convenience_fee_config**
   - Credit card fee settings
   - Program-specific rates
   - Fee calculation rules

### Existing Entities Involved

- **quote**: Being converted to policy
- **document**: Templates for signing
- **policy**: Created upon binding
- **user**: Producer/agent info
- **suspense**: For missing items

## Global Requirements Alignment

### Primary GRs
- **GR-43 (Document Generation)**: Policy documents
- **GR-44 (Communication)**: Email delivery
- **GR-46 (S3 Storage)**: Document storage
- **GR-20 (Business Logic)**: Payment processing
- **GR-37 (Action Tracking)**: Signature audit

### Supporting GRs
- **GR-12 (Security)**: Payment data protection
- **GR-24 (Data Security)**: PCI compliance
- **GR-36 (Authentication)**: User verification
- **GR-51 (Compliance)**: Legal signatures

## Database Schema Planning

### Core Tables

1. **signature**
   ```sql
   - id (PK)
   - user_id (FK)
   - signature_data (text/base64)
   - signature_type (full, initials)
   - ip_address
   - user_agent
   - created_at
   - status_id (FK)
   ```

2. **document_signature_location**
   ```sql
   - id (PK)
   - document_type_id (FK)
   - page_number
   - x_coordinate
   - y_coordinate
   - width
   - height
   - signature_type (signature, initial)
   - is_required (boolean)
   - status_id (FK)
   ```

3. **signed_document**
   ```sql
   - id (PK)
   - quote_id (FK)
   - document_id (FK)
   - s3_path
   - signature_id (FK)
   - signed_at
   - legal_timestamp
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

4. **bind_payment**
   ```sql
   - id (PK)
   - quote_id (FK)
   - payment_method_type (producer_echeck, insured_echeck, credit_card)
   - amount
   - convenience_fee
   - total_amount
   - gateway_transaction_id
   - gateway_response (JSON)
   - processed_at
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

5. **payment_method**
   ```sql
   - id (PK)
   - quote_id (FK)
   - method_type
   - account_holder_name
   - account_last_four
   - routing_number_encrypted
   - account_number_encrypted
   - card_token
   - billing_address_id (FK)
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

## API Endpoints

### Required Endpoints
```
POST   /api/v1/quotes/{quote_id}/signatures/adopt
GET    /api/v1/quotes/{quote_id}/documents-to-sign
POST   /api/v1/quotes/{quote_id}/documents/{id}/sign
GET    /api/v1/quotes/{quote_id}/signature-status
POST   /api/v1/quotes/{quote_id}/validate-signatures
POST   /api/v1/quotes/{quote_id}/payment-methods
POST   /api/v1/quotes/{quote_id}/process-payment
POST   /api/v1/quotes/{quote_id}/bind-policy
GET    /api/v1/programs/{id}/convenience-fee-config
```

### Document Endpoints
```
GET    /api/v1/documents/{id}/signature-locations
POST   /api/v1/documents/{id}/generate-signed-pdf
```

### Real-time Updates
```javascript
private-quote.{quote_id}.signature-progress
private-quote.{quote_id}.payment-status
```

## Integration Points

### Internal Services
1. **DocumentService**
   - Generate signing documents
   - Apply signatures to PDFs
   - Store in S3

2. **PaymentService**
   - Process payments
   - Handle gateway communication
   - Calculate fees

3. **PolicyService**
   - Convert quote to policy
   - Activate coverage
   - Generate policy number

4. **EmailService (GR-44)**
   - Send document package
   - Confirmation emails
   - Receipt delivery

### External Services
- Payment gateway (via Universal Entity)
- S3 for document storage
- Email service (SendGrid)

## Implementation Considerations

### Key Patterns
1. **Signature Workflow**
   - Generate default signature
   - Allow adoption/redraw
   - Apply to all locations
   - Track legally

2. **Payment Processing**
   - PCI-compliant tokenization
   - Gateway abstraction
   - Fee calculation
   - Receipt generation

3. **Document Management**
   - PDF generation with signatures
   - S3 storage with encryption
   - Email delivery queue
   - Audit trail

4. **Re-rating Protection**
   - Warn on backward navigation
   - Clear bind progress
   - Force re-calculation

### Technical Decisions
- PDF.js for document viewing
- Canvas for signature capture
- Stripe/payment gateway SDK
- S3 presigned URLs
- Database encryption for sensitive data

## Quality Checkpoints

### Pre-Implementation
- [ ] Review PCI compliance requirements
- [ ] Validate signature legal requirements
- [ ] Check payment gateway setup
- [ ] Review document generation patterns

### Implementation
- [ ] Signature capture working
- [ ] Payment processing secure
- [ ] Documents generated correctly
- [ ] Email delivery functional

### Post-Implementation
- [ ] PCI compliance scan
- [ ] Legal signature validation
- [ ] Payment reconciliation
- [ ] Document audit trail

## Dependencies

### Upstream
- Quote review completed
- All required data collected
- Premium calculated

### Downstream
- Policy creation
- Billing activation
- Coverage effective date
- Commission calculation

## Risk Mitigation

1. **Payment Security**: Tokenization and encryption
2. **Legal Compliance**: Audit trail and timestamps
3. **Data Loss**: Transaction management
4. **User Experience**: Progress indicators

## UI/UX Specifications

### Signature Adoption
- Name and initials display
- Generated signature preview
- "Adopt" button prominent
- Redraw option available

### Document Viewer
- Embedded PDF display
- Signature indicators clear
- Progress tracking
- Zoom and navigation

### Payment Section
- Method selection tabs
- Form fields per method
- Fee disclosure clear
- Total amount prominent

### Confirmation
- Success checkmark
- Policy number display
- Next steps clear
- Download options

## Cross-Domain Considerations

- **Accounting**: Payment flows to billing
- **Policy**: Quote converts to policy
- **Commission**: Producer payment tracking
- **Compliance**: Document retention

## Next Steps

1. Implement signature capture component
2. Create PDF signature application
3. Build payment processing service
4. Integrate payment gateway
5. Create document generation workflow
6. Implement S3 storage
7. Build email delivery system
8. Add comprehensive audit logging