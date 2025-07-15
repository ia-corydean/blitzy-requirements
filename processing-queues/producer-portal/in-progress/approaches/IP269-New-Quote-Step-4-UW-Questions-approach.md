# IP269-New-Quote-Step-4-UW-Questions - Implementation Approach

## Requirement Understanding

The Underwriting Questions (UWQ) step is a critical risk assessment checkpoint in the quote flow. It dynamically presents program-specific underwriting questions to identify eligibility and flag high-risk profiles. The system must:

- Render questions dynamically based on the insurance program
- Provide Yes/No radio options for each question
- Validate all required questions are answered
- Identify disqualifying answers that may result in hard stops or warnings
- Save responses with the quote for downstream processing
- Support mobile-responsive design with error handling

This requirement focuses on gathering structured risk assessment data while enforcing carrier-specific underwriting guidelines before quote continuation.

## Domain Classification
- Primary Domain: ProducerPortal
- Cross-Domain Impact: No
- Complexity Level: Medium

## Pattern Analysis

### Reusable Patterns Identified

**From Global Requirements:**
- **[GR-04 - Validation & Data Handling]**: Multi-layer validation architecture with real-time feedback, custom validation rules, and Zod schema integration
- **[GR-18 - Workflow Requirements]**: Underwriting workflow states with conditional transitions based on eligibility conditions
- **[GR-20 - Application Business Logic]**: Business rule engine pattern for eligibility validation
- **[GR-07 - Reusable Components]**: Form component patterns with consistent styling and validation
- **[GR-11 - Accessibility]**: WCAG 2.1 AA compliance for form interactions

**From Approved ProducerPortal Requirements:**
- **[IP269-New-Quote-Step-2-Drivers]**: Pattern for handling eligibility flags and validation errors
- **[IP269-Quotes-Search]**: Reference table approach for classification types

**From Infrastructure Patterns:**
- React Hook Form with Zod validation (seen in payment forms)
- Conditional schema validation using discriminated unions
- Real-time eligibility checking patterns (`usePaymentEligibility.ts`)
- Laravel Form Request validation framework

### Domain-Specific Needs
- **Program-specific question sets**: Questions vary by carrier/program
- **Disqualification logic**: Hard stops vs warnings based on answers
- **Risk assessment tracking**: Audit trail for underwriting decisions
- **Dynamic question ordering**: Questions may appear/hide based on previous answers

## Proposed Implementation

### Simplification Approach
- **Current Complexity**: Dynamic questionnaires with conditional logic, multiple validation layers, and complex eligibility rules
- **Simplified Solution**: 
  - Use a single `underwriting_question` table with JSON metadata for flexibility
  - Implement a simple Yes/No radio pattern (no complex question types initially)
  - Use reference tables for question types and disqualification rules
  - Leverage existing validation patterns from approved requirements
- **Trade-offs**: 
  - Gain: Faster implementation, reusable patterns, maintainable code
  - Lose: Advanced question types (text input, multi-select) - can be added later if needed

### Technical Approach

#### Phase 1: Database Schema Design
- [ ] Create `underwriting_question` table with program-specific questions
- [ ] Create `underwriting_question_type` reference table
- [ ] Create `map_quote_underwriting_response` for storing answers
- [ ] Create `underwriting_disqualification_rule` for eligibility logic
- [ ] Add necessary indexes for performance

#### Phase 2: Backend Implementation
- [ ] Create `UnderwritingQuestionService` for business logic
- [ ] Implement `UnderwritingQuestionRequest` validation class
- [ ] Create API endpoints for fetching questions and saving responses
- [ ] Implement eligibility checking logic with hard stop/warning differentiation
- [ ] Add audit logging for all underwriting decisions

#### Phase 3: Frontend Implementation
- [ ] Create `UnderwritingQuestionsForm` component using React Hook Form
- [ ] Implement Zod schema for dynamic validation
- [ ] Create `useUnderwritingEligibility` hook for real-time validation
- [ ] Add mobile-responsive layout with error handling
- [ ] Implement warning/error banner components

#### Phase 4: Integration & Testing
- [ ] Integrate with existing quote flow navigation
- [ ] Add comprehensive test coverage
- [ ] Validate mobile responsiveness
- [ ] Ensure accessibility compliance

## Risk Assessment

- **Risk 1**: Complex conditional question logic → Mitigation: Start with simple Yes/No pattern, add complexity incrementally
- **Risk 2**: Performance with many questions → Mitigation: Use proper indexing and lazy loading if needed
- **Risk 3**: Carrier-specific variations → Mitigation: Use flexible JSON metadata structure
- **Risk 4**: Regulatory compliance → Mitigation: Implement comprehensive audit logging

## Context Preservation

- **Key Decisions**: 
  - Use reference tables instead of ENUMs for flexibility
  - Implement simple Yes/No pattern initially
  - Leverage existing validation patterns from payment forms
  - Store responses in map table for consistency
  
- **Dependencies**: 
  - Builds on existing quote flow (Steps 1-3)
  - Uses established validation patterns from GR-04
  - Follows workflow patterns from GR-18
  
- **Future Impact**: 
  - Enables Step 5 (Coverages) which depends on underwriting eligibility
  - Foundation for more complex question types if needed
  - Reusable pattern for other questionnaires in the system

## Approval Section
**Status**: PENDING APPROVAL
**Reviewer Comments**: [Space for feedback]
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER