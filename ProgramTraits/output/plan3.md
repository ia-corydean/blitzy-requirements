# Program Traits Global Requirements Plan (Simplified Documentation Approach)

## Executive Summary
Based on the feedback, I will create a single comprehensive Global Requirement document that serves as a factual reference for the Aguila Dorada Texas Personal Auto insurance program. This document will be structured for two primary audiences: Claude (for validation) and stakeholders (for fact verification).

## Key Changes from Previous Plan:
1. **Single Global Requirement**: Instead of 7 separate files (63-69), create one comprehensive document
2. **Facts-focused**: Document program details as facts, not technical architecture
3. **No database tables**: Remove technical implementation details
4. **Dual-purpose structure**: Serve both Claude validation and stakeholder verification

## Feedback Integration:
- **Conflicting Eligibility Rules**: Confirmed that drivers would be deemed ineligible (restrictive rules take precedence)

## Updated Approach

### Single Document Structure: 63-aguila-dorada-program-traits.md

**Purpose**: Comprehensive factual documentation of the Aguila Dorada Texas Personal Auto insurance program

### Document Sections:

#### 1. Program Identification
- Program name, underwriter, MGA details
- Geographic scope and effective dates
- Contact information and business hours
- Policy terms and target market

#### 2. Coverage Specifications
- All 9 coverage types with exact limits
- Coverage dependencies and requirements
- Deductible options and restrictions
- State-mandated minimums and rejection requirements

#### 3. Driver Eligibility Criteria
- Age restrictions and license requirements
- Residency requirements
- Conviction history limitations
- Documentation requirements by license type
- Special cases (military, SR-22, etc.)

#### 4. Vehicle Eligibility Criteria
- Acceptable vehicle types and restrictions
- Age, weight, and value limitations
- Photo requirements (6 photos for specific coverages)
- Prohibited vehicle types and uses
- Special restrictions and exceptions

#### 5. Rating Factors and Discounts
- All 10 discount types with qualification rules
- Proof requirements for each discount
- Discount interaction rules
- Premium calculation factors
- Prior insurance requirements

#### 6. Fees and Financial Structure
- All 6 fee types with exact amounts
- Assessment triggers and timing
- Payment plan options
- Down payment structures
- Late fee and penalty rules

#### 7. Endorsements and Modifications
- Available endorsements with codes
- Eligibility criteria for each endorsement
- Fee structures for endorsements
- Effective date and application rules

#### 8. Business Rules and Constraints
- Underwriting guidelines
- Policy issuance requirements
- Renewal criteria
- Cancellation rules
- Exception handling (confirmed: ineligible drivers remain ineligible)

#### 9. State-Specific Texas Requirements
- Minimum liability limits
- UM/UIM and PIP rejection requirements
- SR-22 filing capabilities
- New resident license requirements
- Military personnel exemptions

### Structure for Dual Purpose:

#### For Claude Validation:
- **Machine-readable format** with clear hierarchies
- **Specific numerical values** for all limits, fees, and percentages
- **Boolean logic** for eligibility rules (if X then Y)
- **Complete rule coverage** with no ambiguities
- **Cross-references** between related rules

#### For Stakeholder Verification:
- **Clear section headers** and logical organization
- **Plain language explanations** alongside technical specifications
- **Complete fact coverage** for all program aspects
- **Easy reference format** for quick fact-checking
- **Comprehensive index** of all program traits

### Key Benefits of This Approach:
1. **Single source of truth** for all Aguila Dorada program facts
2. **Easy maintenance** - one document to update
3. **Clear validation reference** for Claude when generating requirements
4. **Stakeholder-friendly** format for fact verification
5. **Complete coverage** of all program aspects in one place

### Document Format Standards:
- **Structured headings** for easy navigation
- **Bullet points** for clear fact presentation
- **Numerical specifications** for all quantifiable aspects
- **Boolean conditions** for eligibility rules
- **Cross-references** for related requirements
- **Plain language summaries** for stakeholder understanding

### Quality Assurance:
- **Complete fact coverage** from source documentation
- **No technical implementation details** (tables, APIs, etc.)
- **Consistent formatting** throughout document
- **Clear distinction** between requirements and examples
- **Validation-ready structure** for Claude consumption

### Todo List for Implementation:
- [COMPLETED] Create comprehensive plan for Program Traits Global Requirements
- [COMPLETED] Review ProgramManager documentation in detail  
- [COMPLETED] Create plan document in ProgramTraits/output
- [COMPLETED] Create plan2.md with updated feedback
- [IN_PROGRESS] Create plan3.md with simplified approach
- [PENDING] Create single comprehensive 63-aguila-dorada-program-traits.md

This simplified approach will provide a comprehensive, factual reference document that serves both technical validation and business verification needs without unnecessary technical complexity.