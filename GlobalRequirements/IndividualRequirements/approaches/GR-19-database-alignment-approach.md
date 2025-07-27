# GR-19 Table Relationships Requirements - Database Alignment Approach

## Overview
This approach document outlines how to update GR-19 (Table Relationships Requirements) to align with the current database structure in the Docker container (claude_db).

## Current State Analysis

### GR-19 Current State
- Focuses on action tracking pattern (action_type, action, map_ENTITY_action)
- Limited to specific relationship patterns
- Does not reflect the full scope of relationships in the actual database

### Actual Database State (claude_db)
Based on the Docker container analysis:
- **22 mapping tables** exist (all prefixed with `map_`)
- **Diverse relationship types**: policy-driver, policy-vehicle, quote-coverage, etc.
- **Standard pattern**: Most map tables use simple foreign key relationships
- **No action tracking tables**: The action/action_type pattern described doesn't exist

## Key Differences to Address

### 1. Expand Relationship Coverage
**Current GR-19**: Only covers action tracking relationships
**Actual Database**: Has 22 different types of entity relationships
**Action**: Document all actual relationship patterns

### 2. Remove Non-Existent Patterns
**Current GR-19**: Describes action/action_type tables that don't exist
**Actual Database**: Uses different patterns for tracking
**Action**: Focus on actual relationship patterns

### 3. Add Real Mapping Tables
**Current GR-19**: Generic map_ENTITY_action pattern
**Actual Database**: Specific mapping tables for business relationships
**Action**: Document all 22 mapping tables and their purposes

## Proposed Updates

### 1. Replace Content with Actual Relationships

```markdown
# 19.0 Table Relationships & Requirements

## Overview
This document defines the relationship patterns and requirements for database tables in the insurance management system. The system uses mapping tables (prefixed with `map_`) to establish many-to-many relationships between entities.

## Core Relationship Patterns

### 1. Entity-to-Entity Mappings
The system uses `map_` prefixed tables to establish many-to-many relationships:
- **Naming Convention**: `map_{entity1}_{entity2}`
- **Structure**: Typically contains foreign keys to both entities plus audit fields
- **Purpose**: Allows flexible associations without modifying core entity tables

### 2. Policy Relationships

#### map_policy_driver
Links policies to insured drivers
- policy_id → policy.id
- driver_id → driver.id
- is_primary_driver (BOOLEAN)
- created_by, updated_by, created_at, updated_at

#### map_policy_vehicle
Links policies to covered vehicles
- policy_id → policy.id
- vehicle_id → vehicle.id
- created_by, updated_by, created_at, updated_at

#### map_policy_coverage
Links policies to selected coverages
- policy_id → policy.id
- coverage_id → coverage.id
- premium_amount (DECIMAL)
- created_by, updated_by, created_at, updated_at

#### map_policy_document
Links policies to related documents
- policy_id → policy.id
- document_id → document.id
- document_purpose (VARCHAR)
- created_by, updated_by, created_at, updated_at

#### map_policy_installment
Links policies to payment installments
- policy_id → policy.id
- installment_number (INT)
- due_date (DATE)
- amount (DECIMAL)
- status_id → status.id
- created_by, updated_by, created_at, updated_at

### 3. Quote Relationships

#### map_quote_driver
Links quotes to potential drivers
- quote_id → quote.id
- driver_id → driver.id
- created_by, updated_by, created_at, updated_at

#### map_quote_vehicle
Links quotes to potential vehicles
- quote_id → quote.id
- vehicle_id → vehicle.id
- created_by, updated_by, created_at, updated_at

#### map_quote_coverage
Links quotes to selected coverages
- quote_id → quote.id
- coverage_id → coverage.id
- premium_amount (DECIMAL)
- created_by, updated_by, created_at, updated_at

### 4. Program Relationships

#### map_program_producer
Links insurance programs to authorized producers
- program_id → program.id
- producer_id → producer.id
- commission_rate (DECIMAL)
- effective_date (DATE)
- expiration_date (DATE)
- created_by, updated_by, created_at, updated_at

#### map_program_coverage
Links programs to available coverages
- program_id → program.id
- coverage_id → coverage.id
- is_required (BOOLEAN)
- is_available (BOOLEAN)
- created_by, updated_by, created_at, updated_at

#### map_program_deductible
Links programs to available deductibles
- program_id → program.id
- deductible_id → deductible.id
- created_by, updated_by, created_at, updated_at

#### map_program_limit
Links programs to coverage limits
- program_id → program.id
- limit_id → limit.id
- created_by, updated_by, created_at, updated_at

#### map_program_underwriting_question
Links programs to underwriting questions
- program_id → program.id
- underwriting_question_id → underwriting_question.id
- is_required (BOOLEAN)
- display_order (INT)
- created_by, updated_by, created_at, updated_at

#### map_program_news
Links programs to news/announcements
- program_id → program.id
- news_id → news.id
- created_by, updated_by, created_at, updated_at

### 5. Producer Relationships

#### map_producer_policy_commission
Tracks commission relationships between producers and policies
- producer_id → producer.id
- policy_id → policy.id
- commission_id → commission.id
- amount (DECIMAL)
- status_id → status.id
- created_by, updated_by, created_at, updated_at

#### map_producer_suspense
Links producers to suspense accounts
- producer_id → producer.id
- suspense_id → suspense.id
- amount (DECIMAL)
- created_by, updated_by, created_at, updated_at

### 6. Security Relationships

#### map_user_role
Links users to their assigned roles
- user_id → user.id
- role_id → role.id
- assigned_date (DATE)
- expiration_date (DATE)
- created_by, updated_by, created_at, updated_at

#### map_role_permission
Links roles to their permissions
- role_id → role.id
- permission_id → permission.id
- created_by, updated_by, created_at, updated_at

### 7. Other Relationships

#### map_driver_violation
Links drivers to traffic violations
- driver_id → driver.id
- violation_id → violation.id
- violation_date (DATE)
- created_by, updated_by, created_at, updated_at

#### map_entity_document
Generic entity-to-document mapping
- entity_id → entity.id
- document_id → document.id
- created_by, updated_by, created_at, updated_at

#### map_integration_configuration
Links integrations to their configurations
- integration_id → integration.id
- configuration_id → configuration.id
- created_by, updated_by, created_at, updated_at

#### map_resource_group
Groups resources together
- resource_id → resource.id
- resource_group_id → resource_group.id
- created_by, updated_by, created_at, updated_at

## Relationship Rules and Constraints

### 1. Referential Integrity
- All foreign keys must have corresponding constraints
- Use CASCADE or SET NULL based on business requirements
- Orphaned records in mapping tables should be prevented

### 2. Audit Requirements
- All mapping tables include standard audit fields
- Track who created and modified relationships
- Maintain timestamp history

### 3. Performance Considerations
- Index all foreign key columns
- Consider composite indexes for common query patterns
- Monitor table growth for high-volume relationships

### 4. Data Validation
- Prevent duplicate relationships where appropriate
- Validate business rules (e.g., one primary driver per policy)
- Ensure date ranges are valid (effective/expiration dates)
```

## Benefits of This Approach

1. **Accuracy**: Documents actual database relationships
2. **Completeness**: Covers all 22 mapping tables
3. **Practical**: Provides real patterns developers can reference
4. **Maintainable**: Clear structure for adding new relationships

## Next Steps

1. Review this approach with stakeholders
2. Upon approval, update GR-19 with actual relationships
3. Consider adding diagrams for complex relationships
4. Update related Global Requirements that reference GR-19