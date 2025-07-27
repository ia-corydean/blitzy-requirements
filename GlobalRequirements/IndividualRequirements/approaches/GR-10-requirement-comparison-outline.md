# GR-10 SR22/SR26 Financial Responsibility Filing - Requirement Comparison Outline

## Overview
This document outlines the proposed changes to GR-10 to include database schema documentation based on the current database structure and feedback from the v2 approach.

## Current GR-10 Structure

### Existing Sections:
1. Overview
2. SR22 Filing Requirements
3. SR22 Form Specifications
4. SR26 Cancellation Process
5. System Integration Requirements
6. Business Rules Framework
7. Fee and Payment Processing
8. Regulatory Compliance Framework
9. Workflow and Process Management

### Missing Section:
- **Section E: Database Schema** - Not present in current GR-10

## Proposed Additions

### New Section E: Database Schema

#### Location: After Section 9, before any appendices

#### Content to Add:

1. **SR22 Filing Tables**
   - sr22_type table (with standard fields)
   - sr22_reason table (existing, document structure)
   - sr22 table (enhanced with business fields)

2. **SR26 Cancellation Tables**
   - sr26_type table (with standard fields)
   - sr26_reason table (existing, document structure)
   - sr26 table (enhanced with business fields)

3. **Key Enhancements to Existing Tables**:
   - Add policy_id, driver_id, document_id relationships
   - Add business fields: case_number, filing_state, dates
   - Add fee tracking fields
   - Remove state submission tracking (per v2 feedback)

## Comparison of Database Elements

### Current State (No Section E)
- No database documentation
- Business requirements without technical implementation details
- No schema definitions

### Proposed State (With Section E)
```markdown
## Section E: Database Schema

### SR22 Filing Tables
[Detailed schema definitions as outlined in v2 approach]

### SR26 Cancellation Tables  
[Detailed schema definitions as outlined in v2 approach]

### Data Relationships
- SR22 → Policy (many-to-one)
- SR22 → Driver (many-to-one)
- SR22 → Document (one-to-one)
- SR26 → SR22 (one-to-one)
```

## Key Differences from V1 Approach

1. **No State Submission Tracking**
   - V1 included sr22_state_submission table
   - V2 removes this since documents are only generated for insureds

2. **Simplified Fee Structure**
   - Fee amount tracked directly in sr22 table
   - No separate fee tracking tables

3. **Document Generation Focus**
   - Emphasis on document_id relationships
   - Support for PDF generation requirements

## Integration with Existing Sections

### Updates to Other Sections:

1. **Section 4 (System Integration)**
   - Add reference to database tables
   - Link document generation to document table

2. **Section 6 (Business Rules)**  
   - Reference database constraints
   - Link to type and reason tables

3. **Section 7 (Fee Processing)**
   - Reference fee_amount field in sr22 table
   - Link to transaction tables for payments

## Benefits of Adding Section E

1. **Complete Specification**: Business + Technical requirements in one document
2. **Implementation Clarity**: Developers have clear schema to implement
3. **Consistency**: Aligns with other GRs that include database sections
4. **Traceability**: Clear mapping from business rules to database fields

## Migration Notes

- Existing sr22/sr26 tables need field additions
- Type tables may need standard seed data
- No breaking changes to existing data

## Summary

The addition of Section E provides:
- Complete database schema documentation
- Clear implementation guidelines
- Support for all business requirements
- Focus on document generation (not state submission)
- Integration with existing insurance system tables