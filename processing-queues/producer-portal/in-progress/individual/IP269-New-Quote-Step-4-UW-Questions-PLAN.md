# IP269-New-Quote-Step-4-UW-Questions - Implementation Plan

## Requirement Overview

### Purpose
The Underwriting Questions (UWQs) step serves as a risk assessment checkpoint to:
- Identify eligibility for quotes based on carrier-specific guidelines
- Flag high-risk profiles for review or blocking
- Gather structured data for downstream policy binding and rating

### Scope
- Dynamic rendering of program-specific underwriting questions
- Yes/No radio button responses
- Validation and error handling for unanswered questions
- Eligibility flags for hard stops and warnings
- Data persistence and mobile compatibility

## Entity Analysis

### New Entities Required

1. **underwriting_question**
   - Core table for question definitions
   - Program-specific configuration
   - Question text and metadata

2. **underwriting_question_type** (Reference)
   - Types: eligibility, risk_assessment, disclosure
   - Categorization for question handling

3. **underwriting_eligibility_rule**
   - Defines disqualifying conditions
   - Links questions to hard stops/warnings
   - Program-specific rules

4. **quote_underwriting_response**
   - Stores user responses per quote
   - Links to underwriting questions
   - Audit trail for compliance

5. **map_program_underwriting_question**
   - Associates questions with programs
   - Order and requirement flags
   - State-specific variations

### Existing Entities Involved

- **quote**: Parent entity for responses
- **program**: Determines question set
- **status**: For response and rule states
- **user**: Audit trail tracking

## Global Requirements Alignment

### Primary GRs
- **GR-41 (Database Standards)**: Table naming, audit fields, indexes
- **GR-20 (Business Logic)**: Service layer for eligibility evaluation
- **GR-04 (Validation)**: Question response validation
- **GR-18 (Workflow)**: Integration with quote workflow
- **GR-37 (Action Tracking)**: Audit trail for responses

### Supporting GRs
- **GR-52 (Universal Entity)**: If external UW services needed
- **GR-11 (Accessibility)**: Screen reader support for questions
- **GR-12 (Security)**: PII handling in responses
- **GR-27 (Performance)**: Fast question loading

## Database Schema Planning

### Core Tables

1. **underwriting_question**
   ```sql
   - id (PK)
   - code (unique)
   - question_text
   - underwriting_question_type_id (FK)
   - help_text
   - display_order
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

2. **quote_underwriting_response**
   ```sql
   - id (PK)
   - quote_id (FK)
   - underwriting_question_id (FK)
   - response (boolean)
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

3. **underwriting_eligibility_rule**
   ```sql
   - id (PK)
   - underwriting_question_id (FK)
   - disqualifying_response (boolean)
   - rule_type (hard_stop, warning)
   - message_text
   - override_allowed (boolean)
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

### Indexes
- quote_underwriting_response: quote_id, underwriting_question_id
- underwriting_eligibility_rule: underwriting_question_id
- map_program_underwriting_question: program_id, state_code

## API Endpoints

### Required Endpoints
```
GET    /api/v1/quotes/{quote_id}/underwriting-questions
POST   /api/v1/quotes/{quote_id}/underwriting-responses
PUT    /api/v1/quotes/{quote_id}/underwriting-responses/{id}
GET    /api/v1/programs/{program_id}/underwriting-questions
POST   /api/v1/quotes/{quote_id}/validate-underwriting
```

### Real-time Updates
```javascript
private-quote.{quote_id}.underwriting-updates
```

## Integration Points

### Internal Services
1. **QuoteService**
   - Update quote eligibility status
   - Trigger premium recalculation

2. **ProgramService**
   - Fetch program-specific questions
   - Apply state variations

3. **ValidationService**
   - Response completeness check
   - Eligibility rule evaluation

### External Services
- Future: External underwriting APIs via GR-52 Universal Entity pattern

## Implementation Considerations

### Key Patterns
1. **Dynamic Question Loading**
   - Cache program questions in Redis
   - Load based on quote program/state
   - Support for question versioning

2. **Eligibility Evaluation**
   - Real-time validation on response
   - Service layer business logic
   - Override workflow for warnings

3. **Mobile Optimization**
   - Progressive enhancement
   - Touch-friendly radio buttons
   - Scroll-to-error behavior

### Technical Decisions
- Use Laravel Form Requests for validation
- Implement UnderwritingService for business logic
- Cache question sets per program in Redis
- Use database transactions for response saving

## Quality Checkpoints

### Pre-Implementation
- [ ] Review GR-41 for database standards
- [ ] Check existing quote workflow patterns
- [ ] Validate against approved requirements
- [ ] Review program configuration patterns

### Implementation
- [ ] All tables include proper audit fields
- [ ] Service layer handles business logic
- [ ] Proper indexes for performance
- [ ] Mobile-responsive UI components

### Post-Implementation
- [ ] Integration tests for eligibility rules
- [ ] Performance testing with multiple questions
- [ ] Accessibility compliance verification
- [ ] Security review for PII handling

## Dependencies

### Upstream
- Quote Step 3 (Vehicles) must be complete
- Program configuration must exist

### Downstream
- Step 5 (Coverages) depends on eligibility
- Premium calculation affected by responses
- Policy binding requires all responses

## Risk Mitigation

1. **Performance**: Cache question sets aggressively
2. **Data Loss**: Save responses on blur/change
3. **User Experience**: Clear error messaging
4. **Compliance**: Audit trail for all responses

## Next Steps

1. Create database migrations for new tables
2. Implement UnderwritingService class
3. Build API endpoints with proper validation
4. Create Vue.js components for question display
5. Implement eligibility rule engine
6. Add comprehensive test coverage