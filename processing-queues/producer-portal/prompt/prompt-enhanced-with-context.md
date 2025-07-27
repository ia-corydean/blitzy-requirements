# Producer Portal Requirements Generation - Enhanced Context

## Overview
This prompt provides comprehensive context for generating requirements for the 23 producer portal features currently in the pending queue. The requirements generation process should leverage the pattern analysis and implementation guidance provided below. The process is defined in README.md

## Files to Process
All files in `/app/workspace/requirements/processing-queues/producer-portal/pending/`

## Critical Context for Requirements Generation

### 1. System Architecture Context
- **Greenfield Implementation**: Building new, not migrating existing
- **Personal Auto Only**: No commercial lines, no CDL support
- **Pre-Production System**: No legacy data constraints
- **Technology Stack**: React 18+, Laravel 10+, React Hook Form, Zod validation

### 2. Pattern Source Analysis

For each requirement, reference this pattern availability matrix:

#### Pattern Sources Legend
- **BR (Blitzy-Requirements)**: Proven UI/UX patterns from reference implementation
- **PE (Processing Environment)**: Business rules and GR requirements
- **MS (My Suggestions)**: Gap-filling patterns for missing pieces

#### Dashboard & Navigation Patterns
| Feature | BR Patterns | PE Rules | MS Patterns | Implementation Notes |
|---------|-------------|----------|-------------|---------------------|
| Dashboard Widgets | ✓ Widget framework | - | - | Use card-based layout |
| Quick Actions | ✓ Menu patterns | - | - | Dropdown with icons |
| Global Navigation | ✓ Nav structure | - | - | Responsive sidebar |
| Breadcrumbs | ✓ Standard pattern | - | - | Path-based tracking |

#### Quote Workflow Patterns
| Feature | BR Patterns | PE Rules | MS Patterns | Implementation Notes |
|---------|-------------|----------|-------------|---------------------|
| Named Insured Form | ✓ Form patterns | - | - | React Hook Form |
| Address Validation | ✓ Validation | - | - | Real-time validation |
| SSN Encryption | ✓ Encryption | ✓ Security GR | - | Field-level PCI compliant |
| Driver Validation | - | ✓ GR-53 | ✓ Age/State | Min age 16, state codes |
| VIN Decode | ✓ Integration | ✓ GR-53 | - | DCS API integration |
| UW Questions | - | ✓ Program rules | - | Dynamic per program |
| Coverage Selection | ✓ UI patterns | ✓ Business rules | - | Real-time premium |

#### Integration Patterns
| Feature | BR Patterns | PE Rules | MS Patterns | Implementation Notes |
|---------|-------------|----------|-------------|---------------------|
| ITC Bridge | - | ✓ External GR | ✓ Mapping | API field mapping |
| E-Signatures | ✓ DocuSign-style | - | - | Document workflow |
| Payment Gateway | ✓ Payment UI | ✓ Accounting | - | PCI compliant |
| File Upload | ✓ Upload patterns | - | - | Drag-drop support |

### 3. Simplification Requirements

**CRITICAL**: For every requirement, enforce these simplification principles:

1. **Form Simplification**
   - Use React Hook Form for ALL forms (no custom form management)
   - Use Zod for ALL validation (no custom validation logic)
   - Reuse form field components across all features

2. **State Management Simplification**
   - React Query for server state (no Redux for API calls)
   - Context API for local state only
   - No complex state machines unless absolutely necessary

3. **Pattern Reuse Target**
   - 85%+ of UI components should reuse existing patterns
   - New patterns only when no existing pattern fits
   - Document why if creating new patterns

4. **Integration Simplification**
   - Use standard REST patterns for all APIs
   - Consistent error handling across all integrations
   - Single integration pattern for external services

### 4. PCI Compliance Built-In

**IMPORTANT**: Do not schedule PCI audits as separate tasks. Instead, build PCI compliance into every requirement:

1. **Payment Handling Requirements**
   - Never store credit card numbers
   - Use tokenization for all payment methods
   - Implement field-level encryption for sensitive data
   - Log all payment-related actions for audit

2. **PII Protection Requirements**
   - SSN: Field-level encryption required
   - Driver License: Field-level encryption required
   - Bank Account: Tokenization required
   - All PII access must be logged

3. **Security Patterns**
   - API rate limiting on all endpoints
   - JWT tokens with 1-hour expiration
   - Refresh token rotation
   - HTTPS only, no HTTP fallback

### 5. Specific Guidance by Feature Type

#### Dashboard Features (IP268, IP285)
- Focus on performance (< 2s load time)
- Use lazy loading for widgets
- Implement caching for metrics
- Mobile-responsive required

#### Quote Workflow Features (IP269)
- Step-by-step navigation with progress indicator
- Auto-save every field change
- Validation on blur, not on submit
- Allow backwards navigation without data loss

#### Policy Management Features (IP270, IP279)
- Read-heavy optimization (caching)
- Bulk operations support
- Document generation async
- Version history for all changes

#### Reporting Features (IP271)
- Server-side report generation
- Streaming for large exports
- Scheduled reports via queue
- Template-based configuration

#### Support Features (IP272, IP273)
- Static content caching
- Search indexing for help
- Role-based access control
- Audit trail for admin actions

### 6. Implementation Priorities

Process requirements in this order:
1. **High Priority**: Quote workflow (foundation for everything else)
2. **High Priority**: Dashboard & Navigation (user entry points)
3. **Medium Priority**: Policy Management (post-quote operations)
4. **Medium Priority**: Reporting (analytics and insights)
5. **Low Priority**: Support Features (help and resources)

### 7. Quality Standards

Every requirement must include:
1. **Validation Rules**: Comprehensive Zod schemas
2. **Error Handling**: User-friendly error messages
3. **Loading States**: Skeleton screens or spinners
4. **Empty States**: Helpful messages when no data
5. **Accessibility**: WCAG 2.1 AA compliance
6. **Testing**: Unit tests for logic, integration tests for APIs

### 8. Architecture Decisions

- **Microservice Boundaries**: Align with domain boundaries (quote service, policy service, etc.)
- **Event-Driven**: Use events for cross-service communication
- **API Gateway**: All external APIs go through gateway
- **Caching Strategy**: Redis for session, CDN for static
- **Database**: PostgreSQL with proper indexing

## Execution Instructions

1. Process each pending requirement file
2. Generate approach files that:
   - Reference specific patterns from the matrix above
   - Include PCI compliance measures where applicable
   - Emphasize simplification over sophistication
   - Provide clear implementation steps
3. Stop for approval after generating approach files
4. Do not modify existing code until approval received

## Expected Outcomes

- 23 approach files covering all producer portal features
- Each approach file should reference pattern sources (BR/PE/MS)
- Security and PCI compliance built into each requirement
- Clear simplification choices documented
- Implementation ready after approval