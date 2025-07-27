# Requirements Generation Standards

## Complete Architecture Integration

### Repository Structure
- **Global Requirements**: `/app/workspace/requirements/GlobalRequirements/IndividualRequirements/`
- **Domain-Specific Standards**: `/app/workspace/requirements/[Domain]/CLAUDE.md`
- **Approved Requirements**: `/app/workspace/requirements/[Domain]/approved-requirements/`
- **Infrastructure Codebase**: `/app/workspace/blitzy-requirements/` (staging branch)

### Cross-Reference Standards
Every requirement must verify against:
1. Applicable Global Requirements
2. Domain-specific approved requirements  
3. Existing infrastructure patterns
4. Current codebase implementations

### Infrastructure Integration

#### Repository Access Procedures
Before processing any requirement:
```bash
cd /app/workspace/blitzy-requirements
git checkout staging
git pull origin staging
```

**GitHub Repository**: https://github.com/blitzy-public-samples/insure-pilot-new/tree/staging

#### Infrastructure Reference Guidelines
1. **Read-Only Access**: NEVER modify any files in blitzy-requirements
2. **Pattern Discovery**: Search for existing implementations before creating new patterns
3. **Validation**: Cross-reference all new requirements against existing code
4. **Documentation**: Note which parts of blitzy-requirements implement similar features

⚠️ **CRITICAL**: The blitzy-requirements directory contains active development code. Any modifications could break the production system. This directory is for REFERENCE ONLY.

#### Pattern Selection Principles for Greenfield Implementation
1. **Greenfield Context**: We are building a new pre-production system without existing data
2. **BR as Reference Library**: Blitzy-requirements provides proven patterns that inform our choices
3. **PE as Requirements**: Global Requirements define what must be built
4. **Pattern Freedom**: BR patterns inform but do not constrain our implementation choices
5. **Future Standards**: Selected patterns become templates for ongoing requirements generation
6. **Reconciliation Focus**: We align patterns and approaches, not migrate data

#### Cross-Reference Standards
Every requirement must validate against existing infrastructure:

**Database Schema Validation:**
- Check `src/backend/database/migrations/` for existing table patterns
- Review `src/backend/app/Models/` for entity relationships
- Validate naming conventions against established patterns

**API Pattern Validation:**
- Review `src/backend/routes/api.php` and `src/backend/routes/portal_api.php`
- Check `src/backend/app/Http/Controllers/` for endpoint patterns
- Validate RESTful conventions and response formats

**Service Layer Validation:**
- Review `src/backend/app/Services/` for business logic patterns
- Check integration with external services
- Validate authentication and authorization patterns

#### Performance Benchmarks
From actual infrastructure analysis:
- Entity queries: <500ms target
- API response times: <200ms for standard operations
- Database connections: Connection pooling via Laravel

### Quality Assurance Integration
Enhanced quality gates include:
- [ ] Global Requirements compliance verified
- [ ] Approved requirements consistency confirmed
- [ ] Infrastructure patterns aligned
- [ ] Git repository currency validated

## Overview
This document serves as a high-level guide and reference aggregator, pointing to specific global requirements for detailed implementation. All detailed specifications are maintained in the GlobalRequirements/IndividualRequirements directory.

## Core Principles
- GlobalRequirements/IndividualRequirements serve as the single source of truth
- Context files translate and aggregate references for practical use
- Consistent patterns across all requirements and domains
- Each global requirement focuses on exactly one topic for clarity

## Quick Reference Guide

### ⚠️ PRIORITY REQUIREMENTS
- **Pattern Reuse Guidelines** → See GR-68 (MUST REVIEW FIRST)
- **Producer Portal Architecture** → See GR-69

### Database & Data Management
- **Database Design Principles** → See GR-02, GR-41
- **Table Relationships** → See GR-03, GR-19
- **Data Services & Caching** → See GR-33
- **Data Security** → See GR-24

### Entity & Architecture Patterns
- **Universal Entity Management** → See GR-52
- **External Integrations Catalog** → See GR-48
- **DCS Integration Architecture** → See GR-53
- **Microservice Architecture** → See GR-38

### Communication & Messaging
- **Communication Architecture** → See GR-44
- **Event-Driven Messaging** → See GR-49
- **Real-time Updates** → See GR-21

### Security & Authentication
- **Identity & Access Management** → See GR-01
- **Authentication & Permissions** → See GR-36
- **Security Considerations** → See GR-12
- **Component-Based Security** → See GR-52

### Workflow & Business Logic
- **Policy Reinstatement Process** → See GR-64
- **Workflow Requirements** → See GR-18
- **Business Logic Standards** → See GR-20
- **Locking & Action Tracking** → See GR-37

### Testing & Quality
- **Testing Requirements** → See GR-05, GR-10
- **Performance Requirements** → See GR-08, GR-27
- **Validation & Data Handling** → See GR-04

### Infrastructure & Deployment
- **Technology Standards** → See GR-00
- **Docker Requirements** → See GR-28, GR-29, GR-30
- **Deployment & Orchestration** → See GR-32
- **Disaster Recovery** → See GR-50

### Compliance & Documentation
- **Compliance & Audit** → See GR-51
- **Documentation Standards** → See GR-14
- **API Gateway Architecture** → See GR-47
- **SR22/SR26 Financial Responsibility Filing** → See GR-10

## Section C Requirements (Backend Mappings)

### Format Standards
Backend mappings should use clear arrow notation for query paths:
```
get [entity].id from [table]
-> get [related_entity] by [entity].[foreign_key]
-> return [fields], [transformations]
```

### Integration Specifications
When applicable, Section C should include:
- API Integration Points
- Configuration Management patterns
- Security Implementation details
- Performance & Monitoring approach
- Error Handling strategies

For detailed integration patterns → See GR-48, GR-53

## Section E Requirements (Database Schema)

### Table Organization
Group tables by type in this order:
1. Core Tables - Main business entities
2. Reference Tables - Lookup/type tables
3. Relationship Tables - map_* tables
4. Supporting Tables - Reusable entities

### Standards References
- Naming conventions → See GR-41
- Audit fields → See GR-02
- Status management → See GR-19
- Index patterns → See GR-33

## Quality Checklist

### Pre-Implementation
- [ ] **⚠️ PRIORITY: Review GR-68 Pattern Reuse Guidelines FIRST** - Must achieve 85% pattern reuse
- [ ] **⚠️ MANDATORY: Review existing database schema FIRST** - Check universal-entity-catalog-v5.json for actual available columns before proposing any new ones
- [ ] **Document available existing tables** - List existing tables from v5 catalog that could be reused for the requirement
- [ ] **Identify existing columns** - Map existing v5 enhanced columns to UI requirements before adding new ones
- [ ] **Map EVERY UI field to database column** - Do not add any column that doesn't have a corresponding UI element in the requirements
- [ ] **Validate column necessity** - Each proposed column must serve a specific UI function described in requirements
- [ ] **No speculative columns** - Don't add "nice to have" or "future enhancement" columns
- [ ] **Review applicable global requirements** (GR-52, GR-48, GR-44, GR-41, GR-19, GR-64)
- [ ] **Check GR-64 for reinstatement patterns** if policy lifecycle involved
- [ ] **Check GR-69 for producer portal features** if building producer functionality
- [ ] **Check SR22/SR26 filing requirements** if financial responsibility filing needed (GR-10)
- [ ] **Check domain-specific approved requirements** for reusable patterns
- [ ] **Review infrastructure codebase** for existing implementations
- [ ] **Check if entity is external** - Use universal entity pattern if so (GR-52)
- [ ] **Verify patterns align with standards** and Global Requirements
- [ ] **Check entity catalog for reuse** - Avoid creating duplicate entities
- [ ] **Confirm naming conventions** following GR-41 standards
- [ ] **Validate communication patterns** align with GR-44 if applicable
- [ ] **Review DCS integration requirements** if driver/vehicle data involved (GR-53)
- [ ] **Validate against existing API patterns** using infrastructure codebase
- [ ] **Assess database schema consistency** with current codebase

### Implementation
- [ ] **Follow template structure** → See requirement-template.md
- [ ] **Include integration specs in Section C** with Global Requirements references
- [ ] **Reference global requirements appropriately** (GR-XX format)
- [ ] **Maintain consistency with existing patterns**
- [ ] **Use universal entity management** for all external entities (APIs, attorneys, body shops, vendors)
- [ ] **Implement JSON metadata schemas** for entity types requiring UI generation
- [ ] **Apply three-level configuration hierarchy** (entity → program → system) if configuration needed
- [ ] **Use polymorphic communication tracking** with correlation IDs for external communications

### Post-Implementation
- [ ] **Verify existing database schema was reviewed** - Confirm universal-entity-catalog-v5.json was consulted and database-first approach was followed
- [ ] **Validate all reusable existing columns were identified and used** - Confirm v5 enhanced schema was maximally leveraged
- [ ] **Confirm new columns are justified against existing schema** - Each new column has documented justification for why existing v5 enhanced schema couldn't support the UI requirement
- [ ] **Ensure no duplicate functionality created** - No new columns that replicate existing column functionality
- [ ] **Every database column has corresponding UI element** - No orphaned columns without UI mapping
- [ ] **No speculative or convenience columns added** - All columns serve documented UI requirements
- [ ] **Update entity catalog** if new entities discovered during implementation
- [ ] **Document architectural decisions** if new patterns emerge
- [ ] **Ensure all Global Requirements references are accurate** (GR-XX format)
- [ ] **Validate against approved requirements patterns** for consistency
- [ ] **Test against infrastructure codebase** (API consistency, schema alignment)
- [ ] **Validate against performance standards** (GR-52: <500ms entity queries, <200ms communication queries)
- [ ] **Confirm compliance requirements** met (7-year retention, audit logging, PII masking)
- [ ] **Test universal entity patterns** work correctly with metadata schemas
- [ ] **Verify communication templates** function with insurance-specific helpers
- [ ] **Document infrastructure integration points** if new patterns established
- [ ] **Update approved requirements library** if new reusable patterns created

## Template Usage

### Two-Template System
The requirements generation system uses two distinct templates for different stages:

1. **Approach Template** (`/shared-infrastructure/templates/approach-template.md`)
   - Used for initial technical analysis and approach documentation
   - Technical focus with detailed entity analysis
   - Pre-analysis checklist and compliance verification
   - Database-first design with schema analysis
   - Used for files in `/in-progress/approaches/`

2. **Completed Requirement Template** (`/shared-infrastructure/templates/completed-requirement-template.md`)
   - Used for final approved requirements ready for implementation
   - Business-focused narrative starting with WHY and WHAT
   - Professional format for stakeholder communication
   - Comprehensive implementation guide
   - Used for files in `/completed/`

### Template Selection Guide
- **Creating an approach file** → Use approach-template.md
- **Converting approved approach to final requirement** → Use completed-requirement-template.md
- **Approach files** focus on technical analysis and validation
- **Completed files** focus on business value and implementation clarity

All requirements follow a progression from technical approach to business-ready requirement:
- Pre-Analysis Checklist with Global Requirements alignment
- Entity Analysis with reuse validation
- Complete Field Mappings (Section C) with implementation architecture
- Integration Specifications for external services
- Database Schema (Section E) with performance optimization
- Quality validation and compliance verification

## Approach File Standards

### Required Sections for Validation
Every approach file must include these sections for comprehensive validation:

1. **Business Summary for Stakeholders**
   - Written in plain English without technical jargon
   - Explains what is being built and why it matters
   - Describes expected business outcomes
   - Identifies value delivered to users

2. **Technical Summary for Developers**
   - Key architectural decisions and patterns
   - Technology choices with justifications
   - Integration approach and dependencies
   - Performance and security considerations

3. **Suggested Tables and Schemas**
   - Expected database tables with purpose
   - Key fields and data types
   - Relationships between tables
   - Important indexes for performance

4. **Validation Criteria**
   - Pre-implementation checkpoints
   - Specific measurable success metrics
   - Quality thresholds that must be met
   - Testing requirements

### Quality Standards for New Sections
- Business summaries must be understandable by non-technical stakeholders
- Technical summaries must provide clear implementation guidance
- Database schemas must follow naming conventions from GR-41
- Validation criteria must be specific, measurable, and testable

## Database Design Principles

### Core Principle: Start Normalized, Add JSON Later
**Remember**: It's much easier to add JSON fields later than to extract structured data from JSON fields after you've accumulated millions of records.

### Scale Dimensions Checklist
When designing database schemas, always consider these growth dimensions:

1. **Entity Growth**: 5 → 50+ (e.g., programs, locations, products)
2. **Records per Entity**: 20 → 100+ (e.g., questions, rules, configurations)
3. **Complexity Evolution**: Simple → Conditional logic
4. **Query Volume**: 1000s/day → Millions/day
5. **Reporting Needs**: Basic counts → Complex analytics
6. **Audit Requirements**: Simple logs → Comprehensive compliance trails

### JSON Usage Guidelines

#### When to Use JSON
- Truly dynamic, unstructured data
- UI preferences or display hints
- Temporary data that won't be queried
- Configuration that changes as a unit
- Metadata that's read but not searched

#### When NOT to Use JSON
- Data that needs frequent querying
- Fields used in JOINs or WHERE clauses
- Data requiring database-level validation
- Information needed for reporting
- Anything with foreign key relationships

#### JSON Migration Costs to Consider
- Extracting structured data from JSON requires full table scans
- Cannot add retrospective foreign key constraints
- Index creation becomes impossible
- Data inconsistencies multiply over time

### Performance Impact Examples

```sql
-- JSON Query (Poor Performance at Scale)
-- 500ms-2s on 1M records
SELECT * FROM table 
WHERE JSON_EXTRACT(data, '$.rule.action') = 'hard_stop';

-- Normalized Query (Optimized)
-- 2-10ms on 1M records with proper indexes
SELECT t.* FROM table t
JOIN rules r ON r.table_id = t.id
WHERE r.action = 'hard_stop';
```

### Data Integrity Considerations

| Aspect | Normalized Tables | JSON Fields |
|--------|------------------|-------------|
| Foreign Keys | ✓ Enforced by DB | ✗ No validation |
| Type Safety | ✓ Column types | ✗ String interpretation |
| Typo Protection | ✓ Schema enforced | ✗ Silent failures |
| Query Optimization | ✓ Index usage | ✗ Full scans |
| Reporting | ✓ Standard SQL | ✗ Complex extracts |

### Design Decision Framework

Before choosing JSON storage, answer:
1. Will this data need to be queried? If yes → Normalize
2. Will this data need validation? If yes → Normalize
3. Will this data grow to millions of records? If yes → Normalize
4. Will this data need to be reported on? If yes → Normalize
5. Is this truly unstructured? If no → Normalize

### Migration Path Strategy

**Phase 1**: Start Simple but Structured
- Basic normalized tables
- Clear foreign keys
- Proper indexes

**Phase 2**: Add Complexity Carefully
- Additional tables as needed
- JSON only for true metadata
- Maintain query performance

**Phase 3**: Optimize for Scale
- Denormalize for performance
- Add caching layers
- Partition large tables

## Active Infrastructure Components
The shared-infrastructure directory contains actively used components:

### Templates (`/shared-infrastructure/templates/`)
- `approach-template.md`: Template for approach files with validation sections
- `requirement-template.md`: Template for final requirements

### Context Store (`/shared-infrastructure/context-store/`)
- `domain-contexts/`: Domain-specific processing knowledge
- `pattern-applications.json`: Tracks pattern usage
- `simplification-decisions.json`: Records simplification choices
- `approval-history.json`: Maintains approval decisions

### Agent Configurations (`/shared-infrastructure/agent-configurations/`)
- 5 YAML configuration files for the current agent system
- Note: `/archived-11-agent-system/` contains historical configs

### Knowledge Base (`/shared-infrastructure/knowledge-base/`)
- Entity catalogs for reuse
- Pattern libraries
- Relationship mappings
- Architecture decisions
- Database design principles (JSON vs normalized guidance)

## Domain-Specific Standards
For ProducerPortal-specific patterns → See `/app/workspace/requirements/ProducerPortal/CLAUDE.md`