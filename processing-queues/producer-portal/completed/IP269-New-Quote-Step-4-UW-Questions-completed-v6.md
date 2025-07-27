# IP269-New-Quote-Step-4-UW-Questions - Complete Requirement

## **A) WHY – Vision and Purpose**

The Underwriting Questions step serves as a critical risk assessment checkpoint in the quote process. It dynamically presents carrier-specific questions to identify eligibility issues early, preventing unqualified risks from proceeding and reducing downstream underwriting friction.

The purpose is to:
- Identify eligibility for quotes based on carrier-specific guidelines
- Flag high-risk profiles for review or automatic decline
- Gather structured data essential for accurate rating and policy binding
- Capture underwriter notes for special considerations or explanations
- Ensure consistent risk assessment across all quotes
- Reduce quote-to-bind errors by catching disqualifying factors early

By enforcing systematic underwriting question completion with intelligent validation and note capture, the system ensures only qualified prospects proceed, saving time for both agents and underwriters while improving the quality of submitted business.

---

## **B) WHAT – Core Requirements**

### **1. Dynamic Question Rendering**

- Display underwriting questions dynamically based on:
  - Selected insurance program
  - Program-specific question mappings
- Each question displays:
  - Clear question text
  - Required/optional indicator
  - Available answer options (from underwriting_answer table)
- Support conditional questions that appear based on parent question answers
- Maintain display order as configured per program

### **2. Response Validation**

- **Required Field Validation**:
  - Highlight unanswered required questions in red
  - Prevent progression until all required questions answered
- **Disqualifying Answer Detection**:
  - Identify answers that trigger hard stops
  - Differentiate between warnings and declines
  - Display appropriate messaging for each type
- **Real-time Validation**:
  - Validate as user answers each question
  - Update eligibility status dynamically
  - Show/hide conditional questions immediately

### **3. Eligibility Management**

- **Hard Stops** (Risk Declined):
  - Display prominent error banner
  - Disable Continue button
  - Provide specific decline reason
  - No override option available
- **Warnings** (Review Required):
  - Display yellow warning banner
  - Allow progression with acknowledgment
  - Track warning acceptance
  - Flag quote for underwriter review
- **Conditional Logic**:
  - Show/hide questions based on parent answers
  - Update eligibility as answers change
  - Re-evaluate all rules on any change

### **4. Notes Capture**

- **Note Input Field**:
  - Multi-line text area for additional context
  - Optional field available at bottom of questions
  - Character limit of 2000 characters
  - Placeholder text: "Note"
- **Note Persistence**:
  - Save notes with underwriting question responses
  - Associate with quote for future reference
  - Display in underwriter review screens
  - Track note author and timestamp

### **5. Business Rules & Validation**

- All responses must be saved and persist on page reload
- Notes are optional but saved when provided
- Allow editing of answers and notes before final submission
- Support program-specific validation rules
- Enable rule updates without code changes
- Maintain response and note history

### **6. Save & Navigation**

- Save responses and notes on form submit
- Validate all required questions before enabling Continue
- Check for hard stops before allowing progression
- Navigate to Coverage Selection (Step 5) when valid
- Preserve all answers and notes in quote context

---

## Entity Analysis

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|-------|
| underwriting_question | Core | Existing (Modified) | Stores only base questions, no answers |
| underwriting_answer | Core | Existing | Stores answer options for questions |
| map_program_underwriting_question | Map | Existing | Links questions to programs |
| map_quote_underwriting_question | Map | Existing | Links quote-specific answers |
| program | Core | Existing | Defines which questions apply |
| quote | Core | Existing | Parent entity for answers |
| note | Core | Existing | Stores text notes with categorization |
| note_type | Reference | Existing | Categorizes different note types |

### Three-Table Architecture for Questions
The system uses a properly normalized three-table structure:
- `underwriting_question` - Stores question definitions only
- `underwriting_answer` - Stores all possible answer options
- `map_quote_underwriting_question` - Links quotes to selected answers

### Note System Design
Notes use direct entity linkage via entity_type/entity_id:
- No mapping table required since note has direct entity reference
- Supports flexible attachment to any entity type
- Maintains full audit trail

### Relationships Identified
- program → has many → underwriting_questions (via map_program_underwriting_question)
- underwriting_question → has many → underwriting_answers
- underwriting_question → can have → parent_question (self-referential)
- quote → has many → question/answer pairs (via map_quote_underwriting_question)
- quote → has many → notes (via entity_type/entity_id in note table)
- note → belongs to → note_type

---

## Field Mappings (Section C)

### Backend Mappings

#### Question Loading

##### Get Program Questions
- **Backend Mapping**: 
  ```
  get quote.program_id from quote
  -> get questions from map_program_underwriting_question
     where program_id = quote.program_id
  -> join with underwriting_question table
  -> for each question:
     -> get available answers from underwriting_answer
        where underwriting_question_id = underwriting_question.id
  -> get existing answers from map_quote_underwriting_question
     where quote_id = quote.id
  -> order by display_order
  -> return questions with answer options and selected answers
  ```

#### Question Display

##### Render Question Form
- **Backend Mapping**: 
  ```
  for each question:
  -> display question_text
  -> show help_text if present
  -> check is_required flag
  -> get answer options from underwriting_answer:
     - display answer_text for each option
     - use answer_value as radio/checkbox value
  -> if parent_question_id exists:
     -> check parent answer from map_quote_underwriting_question
     -> show/hide based on parent_answer_required
  -> load existing answer_id if present in map_quote_underwriting_question
  ```

#### Answer Handling

##### Save Answer
- **Backend Mapping**: 
  ```
  receive question_id and answer_id
  -> validate answer_id belongs to question_id
  -> check/update map_quote_underwriting_question:
     - quote_id = current_quote
     - underwriting_question_id = question_id
     - underwriting_answer_id = answer_id
     - answered_date = current_timestamp
  -> get validation_rules from underwriting_answer
  -> evaluate rules for eligibility
  -> return validation result
  ```

#### Note Handling

##### Save Underwriting Note
- **Backend Mapping**: 
  ```
  receive note_text from form
  -> if note_text is not empty:
     -> create note record:
        - note_type_id = (SELECT id FROM note_type WHERE code = 'UNDERWRITING')
        - note_text = submitted text
        - entity_type = 'quote'
        - entity_id = quote.id
        - is_internal = true
        - created_by = current_user
     -> return note.id
  ```

##### Link Note to Policy (Post-Bind)
- **Backend Mapping**: 
  ```
  when quote converts to policy:
  -> get notes where entity_type = 'quote' and entity_id = quote.id
  -> update notes:
     - create new note records with entity_type = 'policy' and entity_id = policy.id
     - maintain reference to original quote note
  ```

#### Validation Logic

##### Evaluate Rules
- **Backend Mapping**: 
  ```
  get validation_rules JSON from underwriting_answer
  -> parse rules for answer impact
  -> check disqualifying conditions:
     if hard_stop: return {eligible: false, type: 'decline'}
     if warning: return {eligible: true, type: 'warning'}
  -> check all required questions answered via map_quote_underwriting_question
  -> return overall eligibility status
  ```

### Implementation Architecture

The underwriting questions system uses a properly normalized three-table structure:

1. **Dynamic Question Service**: Loads program-specific questions with available answers
2. **Answer Management**: Tracks selected answers separately from question definitions
3. **Validation Engine**: Evaluates answer-specific rules for eligibility
4. **State Management**: Maintains answer persistence throughout the session
5. **Note Service**: Uses direct entity reference for flexible note attachment
6. **Eligibility Calculator**: Aggregates all responses to determine quote viability
7. **Audit Service**: Tracks all answer changes and notes with timestamps

### Integration Specifications

**Rule Engine Integration**:
- JSON-based rules stored in validation_rules column of underwriting_answer
- Answer-specific validation logic
- Supports complex conditional logic
- Extensible for future rule types

**Program Configuration**:
- Questions linked via map_program_underwriting_question
- Program-specific display order
- State-based overrides supported
- Answer availability can be program-specific

**Answer Tracking**:
- Separate storage of questions and answers
- Clean mapping via map_quote_underwriting_question
- Historical answer tracking with timestamps
- Efficient querying without JSON extraction

**Note Management**:
- Direct entity reference via entity_type/entity_id in note table
- No mapping table required
- Flexible note system for any entity type
- Categorization via note_type
- Full audit trail with timestamps

---

## **D) User Experience (UX) & Flows**

### **1. Entry Flow**

1. User navigates to "Underwriting Questions" after Vehicle/Coverage steps
2. System loads program-specific questions with answer options
3. Questions display in configured order
4. Any previously saved answers pre-populate
5. Required questions marked with asterisk
6. Note field appears at bottom

### **2. Answer Flow**

1. User sees each question with available answer options
2. Answer options displayed as radio buttons or checkboxes
3. User selects from pre-defined answers (no free text)
4. Conditional questions appear/hide based on answers
5. Auto-save triggers after each selection
6. Validation runs immediately:
   - Required field check
   - Disqualifying answer check
7. UI updates based on validation results
8. User can add optional notes

### **3. Warning Flow**

1. User selects answer that triggers warning
2. Yellow banner appears at top of page
3. Specific question highlighted with warning icon
4. Warning message explains concern
5. Continue button remains enabled
6. User can acknowledge and proceed
7. Notes can provide additional context

### **4. Hard Stop Flow**

1. User selects disqualifying answer
2. Red error banner appears prominently
3. Specific decline reason provided
4. Continue button becomes disabled
5. User must change answer or abandon quote
6. No override option available

### **5. Note Entry Flow**

1. User scrolls to bottom of questions
2. Sees optional note field
3. Enters relevant underwriting context
4. Character count shows remaining space
5. Note saves with other responses
6. Can edit note before submission

### **6. Submission Flow**

1. All required questions answered
2. No hard stops active
3. Optional notes captured
4. User clicks Continue
5. Final validation performed
6. Answers and notes saved to quote
7. Navigation to Coverage Selection

### **7. UI Presentation Guidelines**

- Questions in card-based layout
- Answer options clearly labeled with radio buttons
- Error states with red highlighting
- Warning states with yellow highlighting
- Help text in collapsible sections
- Note field with clear label and character count
- Progress indicator showing completion
- Mobile responsive with touch-friendly controls
- Keyboard navigation support
- Screen reader compatible

---

## API Specifications

### Endpoints Required
```http
GET    /api/v1/quotes/{id}/underwriting-questions     # Get questions with answers
PUT    /api/v1/quotes/{id}/underwriting-answers       # Save selected answers
POST   /api/v1/quotes/{id}/validate-underwriting      # Validate all answers
GET    /api/v1/quotes/{id}/eligibility                # Check eligibility status
POST   /api/v1/quotes/{id}/notes                      # Save underwriting note
GET    /api/v1/quotes/{id}/notes                      # Get quote notes
```

### Question Response Format
```json
{
  "questions": [
    {
      "question_id": 1,
      "question_code": "FELONY_CONVICTION",
      "question_text": "Has any driver had a felony conviction in the past 5 years?",
      "help_text": "Include all drivers listed on this policy",
      "is_required": true,
      "display_order": 1,
      "answers": [
        {
          "answer_id": 1,
          "answer_text": "Yes",
          "answer_value": "YES",
          "validation_rules": {"type": "hard_stop", "message": "Felony convictions disqualify this risk"}
        },
        {
          "answer_id": 2,
          "answer_text": "No",
          "answer_value": "NO",
          "validation_rules": null
        }
      ],
      "selected_answer_id": null
    }
  ]
}
```

### Answer Submission Payload
```json
{
  "answers": [
    {
      "question_id": 1,
      "answer_id": 2
    },
    {
      "question_id": 2,
      "answer_id": 4
    }
  ]
}
```

### Real-time Updates
```javascript
// WebSocket channels for live validation
private-quote.{quote_id}.underwriting    # Real-time eligibility updates
```

---

## Database Schema (Section E)

### Core Tables Used

#### underwriting_question
```sql
-- Stores question definitions only (answer columns removed)
-- Key columns:
-- id, question_code, question_text, question_type
-- is_required, display_order, parent_question_id, parent_answer
-- validation_rules, help_text
-- status_id, created_by, updated_by, created_at, updated_at
```

#### underwriting_answer
```sql
-- Stores all possible answer options
-- Key columns:
-- id, underwriting_question_id, answer_text, answer_value
-- validation_rules, display_order, is_default
-- status_id, created_by, updated_by, created_at, updated_at
```

#### map_quote_underwriting_question
```sql
-- Links quotes to selected answers
-- Key columns:
-- id, quote_id, underwriting_question_id, underwriting_answer_id
-- answered_date
-- created_by, updated_by, created_at, updated_at
```

#### note
```sql
-- Stores underwriting notes with direct entity reference
-- Key columns:
-- id, note_type_id, note_text
-- entity_type, entity_id
-- is_internal, priority
-- status_id, created_by, updated_by, created_at, updated_at
```

#### note_type
```sql
-- Categorizes note types
-- Key columns:
-- id, code, name, description
-- is_default
-- status_id, created_by, updated_by, created_at, updated_at
```

### Sample Data

#### Insert Sample Questions
```sql
-- Example underwriting questions
INSERT INTO underwriting_question (
  question_code, question_text, help_text, question_type, 
  is_required, display_order, status_id
) VALUES 
(
  'FELONY_CONVICTION',
  'Has any driver had a felony conviction in the past 5 years?',
  'Include all drivers listed on this policy',
  'single_choice',
  true,
  1,
  1
),
(
  'PRIOR_CLAIMS',
  'Have you had 3 or more claims in the past 3 years?',
  'Include all types of claims',
  'single_choice',
  true,
  2,
  1
);
```

#### Insert Sample Answers
```sql
-- Example answers for questions
INSERT INTO underwriting_answer (
  underwriting_question_id, answer_text, answer_value, 
  validation_rules, display_order, status_id
) VALUES 
-- Answers for FELONY_CONVICTION
(
  (SELECT id FROM underwriting_question WHERE question_code = 'FELONY_CONVICTION'),
  'Yes',
  'YES',
  '{"type":"hard_stop","message":"Felony convictions disqualify this risk","code":"DECLINE_FELONY"}',
  1,
  1
),
(
  (SELECT id FROM underwriting_question WHERE question_code = 'FELONY_CONVICTION'),
  'No',
  'NO',
  NULL,
  2,
  1
),
-- Answers for PRIOR_CLAIMS
(
  (SELECT id FROM underwriting_question WHERE question_code = 'PRIOR_CLAIMS'),
  'Yes',
  'YES',
  '{"type":"warning","message":"Multiple claims may affect pricing","code":"WARN_CLAIMS"}',
  1,
  1
),
(
  (SELECT id FROM underwriting_question WHERE question_code = 'PRIOR_CLAIMS'),
  'No',
  'NO',
  NULL,
  2,
  1
);
```

### Query Examples

#### Get Questions with Answers for a Quote
```sql
SELECT 
    q.id as question_id,
    q.question_code,
    q.question_text,
    q.help_text,
    q.is_required,
    a.id as answer_id,
    a.answer_text,
    a.answer_value,
    a.validation_rules,
    mquq.underwriting_answer_id as selected_answer_id,
    mquq.answered_date
FROM map_program_underwriting_question mpuq
JOIN underwriting_question q ON mpuq.underwriting_question_id = q.id
LEFT JOIN underwriting_answer a ON a.underwriting_question_id = q.id
LEFT JOIN map_quote_underwriting_question mquq ON 
    mquq.quote_id = ? AND 
    mquq.underwriting_question_id = q.id AND
    mquq.underwriting_answer_id = a.id
WHERE mpuq.program_id = ? AND q.status_id = 1 AND a.status_id = 1
ORDER BY mpuq.display_order, q.display_order, a.display_order;
```

#### Get Notes for a Quote
```sql
-- Get all notes for a quote using direct entity reference
SELECT 
    n.*,
    nt.name as note_type_name,
    nt.code as note_type_code,
    u.username as created_by_name
FROM note n
JOIN note_type nt ON n.note_type_id = nt.id
LEFT JOIN user u ON n.created_by = u.id
WHERE n.entity_type = 'quote' 
AND n.entity_id = ?
AND n.status_id = 1
ORDER BY n.created_at DESC;
```

---

## Implementation Notes

### Dependencies
- Program configuration must include question mappings
- Answer validation rules must be properly formatted JSON
- Quote context must be maintained throughout session
- Parent/child question relationships must be configured

### Performance Considerations
- Index on map_quote_underwriting_question for fast lookups
- Efficient joins between three tables
- No JSON extraction needed for queries
- Cache program questions and answers
- Lazy load conditional questions
- Debounce auto-save to prevent excessive updates

### Architecture Benefits
- **Separation of Concerns**: Questions, answers, and selections are properly separated
- **Scalability**: Easy to add new answer options without schema changes
- **Query Performance**: No JSON extraction needed for answer retrieval
- **Data Integrity**: Foreign keys ensure valid question/answer relationships
- **Flexibility**: Programs can share questions but have different available answers
- **Direct Entity Linkage**: Notes use entity_type/entity_id pattern, no mapping table needed

---

## Quality Checklist

### Pre-Implementation
- [x] All UI fields mapped to database columns
- [x] Three-table structure properly designed
- [x] Existing entities leveraged where possible
- [x] Validation rules structure defined
- [x] Parent/child relationships supported
- [x] Answer and note persistence included
- [x] Direct entity linkage for notes (no mapping table)

### Post-Implementation
- [ ] Questions load with available answers
- [ ] Answer selection saves correctly
- [ ] Conditional questions show/hide properly
- [ ] Validation rules evaluate correctly
- [ ] Hard stops prevent progression
- [ ] Warnings display appropriately
- [ ] Notes save and retrieve correctly via entity reference
- [ ] Answers persist across sessions

### Final Validation
- [ ] All required questions enforced
- [ ] Eligibility correctly calculated
- [ ] Three-table structure performs well
- [ ] Notes properly linked to entities
- [ ] Error messages clear and actionable
- [ ] Mobile experience optimized
- [ ] Performance acceptable

### Global Requirements Compliance
- [x] **GR-69**: Producer Portal Architecture - Dynamic form patterns implemented
- [x] **GR-18**: Workflow Requirements - Conditional logic fully supported
- [x] **GR-41**: Database Standards - Proper normalized table structure
- [x] **GR-20**: Business Logic Standards - Rule engine for validation
- [x] **GR-37**: Action Tracking - Answer tracking with audit fields