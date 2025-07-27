# IP269-New-Quote-Step-4-UW-Questions - Implementation Approach

## Requirement Understanding
The Underwriting Questions step serves as a critical risk assessment checkpoint that dynamically displays program-specific questions, validates responses, identifies disqualifying answers, and determines quote eligibility. The system must handle hard stops, warnings, conditional questions, and maintain response persistence while providing clear feedback on eligibility issues.

## Domain Classification
- Primary Domain: Producer Portal / Quote Management
- Cross-Domain Impact: Yes - Affects eligibility, rating, program selection
- Complexity Level: Medium

## Pattern Analysis

### Reusable Patterns Identified
- [GR-69]: Producer Portal Architecture - Dynamic form patterns
- [GR-18]: Workflow Requirements - Conditional logic patterns
- [GR-41]: Database Standards - Question/answer storage
- [GR-20]: Business Logic Standards - Rule evaluation
- [GR-38]: Microservice Architecture - Underwriting service

### Domain-Specific Needs
- Dynamic question loading by program
- Yes/No radio button responses
- Disqualifying answer detection
- Hard stop vs warning differentiation
- Conditional question display
- Response persistence
- Eligibility determination

## Proposed Implementation

### Simplification Approach
- Current Complexity: Dynamic questions with complex validation rules
- Simplified Solution: Use existing comprehensive underwriting_question table
- Trade-offs: None - table structure supports all requirements

### Technical Approach
1. **Phase 1**: Question Loading
   - [ ] Query map_program_underwriting_question
   - [ ] Load questions for quote's program
   - [ ] Order by display_order field
   - [ ] Check for existing answers
   - [ ] Build question form dynamically

2. **Phase 2**: Question Display
   - [ ] Render Yes/No radio buttons
   - [ ] Show question_text and help_text
   - [ ] Handle conditional questions
   - [ ] Check parent_question_id logic
   - [ ] Show/hide based on parent_answer

3. **Phase 3**: Response Handling
   - [ ] Capture radio button selections
   - [ ] Save to answer_value field
   - [ ] Update answer_date timestamp
   - [ ] Persist on each change
   - [ ] Maintain quote context

4. **Phase 4**: Validation Logic
   - [ ] Check is_required fields
   - [ ] Parse validation_rules JSON
   - [ ] Identify disqualifying answers
   - [ ] Differentiate hard stops/warnings
   - [ ] Display appropriate messages

5. **Phase 5**: Eligibility Check
   - [ ] Evaluate all responses
   - [ ] Apply program rules
   - [ ] Show warning banners
   - [ ] Block/allow continuation
   - [ ] Track override attempts

6. **Phase 6**: Save & Navigation
   - [ ] Validate all required answered
   - [ ] Check no hard stops active
   - [ ] Save final responses
   - [ ] Enable/disable continue
   - [ ] Navigate to Step 5

## Risk Assessment
- **Risk 1**: Complex validation rules → Mitigation: Robust rule parser
- **Risk 2**: Conditional logic errors → Mitigation: Comprehensive testing
- **Risk 3**: Program rule changes → Mitigation: Database-driven configuration
- **Risk 4**: Performance with many questions → Mitigation: Efficient queries
- **Risk 5**: User confusion → Mitigation: Clear error messaging

## Context Preservation
- Key Decisions: Use existing table structure, implement rule engine
- Dependencies: Program configuration, validation rules, quote context
- Future Impact: Foundation for automated underwriting decisions

## Database Requirements Summary
- **New Tables**: 0 tables need to be created
- **Existing Tables**: 3 tables will be reused as-is
- **Modified Tables**: 0 existing tables need modifications

## Database Schema Analysis

### Core Tables (All Exist)
1. **underwriting_question**: Comprehensive question/answer storage
   - Has all required fields including validation_rules
   - Supports parent/child relationships
   - Stores answers directly in table
   - Perfect for implementation

2. **map_program_underwriting_question**: Program-question mapping
   - Links questions to specific programs
   - Controls which questions appear
   - Supports program-specific rules

3. **program**: Insurance program definitions
   - Contains underwriting rules
   - Links to questions via mapping

### Key Features Already Supported
- Dynamic question loading (program-based)
- Conditional questions (parent_question_id)
- Validation rules (validation_rules JSON)
- Required field tracking (is_required)
- Answer persistence (answer_value)
- Display ordering (display_order)
- Help text (help_text)

### Validation Rules Structure
The validation_rules field can store JSON like:
```json
{
  "disqualifying": {
    "value": "Yes",
    "type": "hard_stop",
    "message": "This risk is not eligible"
  },
  "warning": {
    "value": "Yes", 
    "type": "warning",
    "message": "Additional review required"
  }
}
```

## Business Summary for Stakeholders
### What We're Building
An intelligent underwriting questionnaire that dynamically presents program-specific questions, validates responses in real-time, and determines quote eligibility. The system identifies high-risk factors, provides clear warnings for concerning answers, and ensures only qualified prospects proceed to coverage selection, reducing downstream underwriting issues.

### Why It's Needed
Manual underwriting question collection leads to inconsistent risk assessment and missed disqualifying factors. This automated system ensures all required questions are answered, immediately identifies eligibility issues, and prevents ineligible quotes from proceeding - saving time and reducing errors in the quote-to-bind process.

### Expected Outcomes
- Reduced quote abandonment through clear guidance
- Improved risk selection with consistent questioning
- Faster underwriting decisions via automated rules
- Decreased bind-time rejections by catching issues early
- Better agent experience with intelligent form behavior

## Technical Summary for Developers
### Key Technical Decisions
- **Architecture Pattern**: Use existing underwriting_question table as-is
- **Rule Engine**: JSON-based validation in validation_rules field
- **State Management**: Answer persistence on each change
- **Conditional Logic**: Parent/child question relationships
- **Validation Approach**: Client and server-side rule evaluation

### Implementation Guidelines
- Load questions via program mapping
- Parse validation_rules for each question
- Implement conditional display logic
- Build warning/error UI components
- Create rule evaluation service
- Use debounced auto-save
- Cache program questions
- Handle edge cases gracefully

## Validation Criteria
### Pre-Implementation Checkpoints
- [x] Underwriting question table exists
- [x] Program mapping table ready
- [x] Validation rules field available
- [x] Parent/child support exists
- [x] Answer storage in place
- [x] All required fields present

### Success Metrics
- [ ] Questions load by program
- [ ] Yes/No radios function
- [ ] Conditional questions show/hide
- [ ] Required validation works
- [ ] Disqualifying answers detected
- [ ] Warnings display correctly
- [ ] Hard stops block progression
- [ ] Answers persist on reload

## Approval Section
**Status**: Ready for Review  
**Database Verification**: All tables exist with complete structure  
**Pattern Reuse**: 100% - No modifications needed  
**Risk Level**: Low - Comprehensive table structure supports all needs  
**Next Steps**: Review approach and approve for implementation  
**Reviewer Comments**: [Pending]  
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER