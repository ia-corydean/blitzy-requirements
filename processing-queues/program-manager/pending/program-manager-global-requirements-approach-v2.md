# ProgramManager Global Requirements Approach V2

## Executive Summary

The ProgramManager serves as the comprehensive configuration and management system for insurance programs within the Aime platform. Version 2 of this approach enhances the original design with improved audit trails, better separation of configuration types from instances, and granular tracking capabilities. The system provides administrative interfaces and backend services for creating, configuring, and maintaining insurance programs including coverage options, territorial definitions, payment configurations, eligibility rules, and business rule enforcement through a draft/publish workflow.

## Key V2 Enhancements

### Enhanced Audit Trail
- Factor-level logging for complete calculation transparency
- Separate type definitions from instance applications
- Comprehensive tracking of all configuration changes
- Support for regulatory compliance reporting

### Improved Data Architecture
- Clear separation between configuration (types) and execution (instances)
- Better normalization for scale and performance
- Enhanced support for versioning and historical tracking
- Optimized for reporting and analytics

## 1. System Overview

### 1.1 Core Responsibilities

```
┌─────────────────────────────────────────────────────────────┐
│                    ProgramManager V2                         │
├─────────────────────────────────────────────────────────────┤
│ • Program Configuration & Versioning                         │
│ • Territory & Geographic Management                          │
│ • Coverage & Limits Configuration                            │
│ • Business Rules & Eligibility                              │
│ • Discount & Surcharge Management                            │
│ • Payment Plan Configuration                                 │
│ • Integration Management                                     │
│ • Draft/Publish Workflow                                     │
│ • Enhanced Audit Trail & Compliance                          │
│ • Type/Instance Separation                                   │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Key Features

1. **Program Lifecycle Management**
   - Create and configure new insurance programs
   - Version control with draft/publish workflow
   - Effective date management
   - Program activation/deactivation
   - Complete audit trail of all changes

2. **Geographic Configuration**
   - Territory definition and management
   - ZIP code to territory mapping
   - County-based tax configuration
   - Regional surcharge setup
   - Historical territory tracking

3. **Product Configuration**
   - Coverage types and combinations
   - Limit options and constraints
   - Deductible configurations
   - Endorsement management
   - Type-based categorization

4. **Business Rule Engine**
   - Eligibility criteria definition
   - Underwriting rule configuration
   - Validation rule setup
   - Override authority management
   - Rule versioning and history

5. **Financial Configuration**
   - Payment plan types and instances
   - Discount types and applications
   - Surcharge types and triggers
   - Fee structures and applications

## 2. Functional Requirements

### 2.1 Program Setup & Configuration

#### 2.1.1 Basic Program Information
- **Program Identification**
  - Unique program code and name
  - Program type classification (standard, non-standard, preferred)
  - Carrier and MGA associations
  - Line of business designation

- **Program Lifecycle**
  - Draft creation and editing
  - Version management and history
  - Publishing workflow with approvals
  - Effective date controls
  - Program status tracking (draft, pending, active, suspended, terminated)

#### 2.1.2 Version Control System
```typescript
interface ProgramVersion {
  id: string
  programId: string
  version: string // semantic versioning
  status: 'draft' | 'pending_approval' | 'published' | 'archived'
  effectiveDate: Date
  expirationDate?: Date
  configuration: ProgramConfiguration
  createdBy: string
  approvedBy?: string
  publishedAt?: Date
  changeLog: ChangeEntry[]
}
```

### 2.2 Territory Management

#### 2.2.1 Territory Configuration
Based on the rating factors analysis, territories are fundamental to the rating structure:

- **Territory Definition**
  - 12 distinct territories for Texas program
  - Territory codes (01-12) with descriptive names
  - Risk tier assignment per territory
  - Base rate configuration by coverage type

- **Geographic Mapping**
  - ZIP code to territory assignment
  - County to territory relationships
  - Border ZIP handling for multi-state programs
  - Exception handling for unmapped areas

#### 2.2.2 Territory Data Model V2
```sql
-- Territory type definition
CREATE TABLE territory_type (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type_code VARCHAR(50) UNIQUE NOT NULL,
    type_name VARCHAR(100) NOT NULL,
    description TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Territory instances
CREATE TABLE territory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_version_id UUID REFERENCES program_version(id),
    territory_type_id UUID REFERENCES territory_type(id),
    territory_code VARCHAR(10) NOT NULL,
    territory_name VARCHAR(100) NOT NULL,
    description TEXT,
    risk_tier INTEGER NOT NULL CHECK (risk_tier BETWEEN 1 AND 10),
    state_id UUID REFERENCES state(id),
    base_rate_config JSONB, -- Structured base rates by coverage
    is_active BOOLEAN DEFAULT true,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    created_by UUID REFERENCES user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(program_version_id, territory_code, effective_date)
);

-- Territory ZIP mapping with history
CREATE TABLE territory_zip_mapping (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    territory_id UUID REFERENCES territory(id),
    zip_code VARCHAR(10) NOT NULL,
    county_id UUID REFERENCES county(id),
    effective_date DATE NOT NULL,
    expiration_date DATE,
    created_by UUID REFERENCES user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_zip_territory (zip_code, effective_date),
    UNIQUE(territory_id, zip_code, effective_date)
);
```

### 2.3 Coverage Management

#### 2.3.1 Coverage Configuration
- **Coverage Types**
  - Liability (Bodily Injury/Property Damage)
  - Uninsured/Underinsured Motorist
  - Comprehensive
  - Collision
  - Personal Injury Protection (PIP)
  - Medical Payments
  - Roadside Assistance
  - Rental Reimbursement

- **Coverage Rules**
  - Minimum/maximum limits by coverage
  - Required vs optional designations
  - Coverage dependencies and exclusions
  - State-specific requirements

#### 2.3.2 Coverage Data Model V2
```sql
-- Coverage type definition
CREATE TABLE coverage_type (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coverage_code VARCHAR(50) UNIQUE NOT NULL,
    coverage_name VARCHAR(100) NOT NULL,
    coverage_category VARCHAR(50) NOT NULL,
    description TEXT,
    metadata JSONB, -- Display info, help text, etc.
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Program-specific coverage configuration
CREATE TABLE program_coverage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_version_id UUID REFERENCES program_version(id),
    coverage_type_id UUID REFERENCES coverage_type(id),
    is_required BOOLEAN DEFAULT false,
    is_available BOOLEAN DEFAULT true,
    display_order INTEGER,
    configuration JSONB, -- Limits, deductibles, rules
    effective_date DATE NOT NULL,
    expiration_date DATE,
    created_by UUID REFERENCES user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Limit configuration
CREATE TABLE limit (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_coverage_id UUID REFERENCES program_coverage(id),
    limit_code VARCHAR(50) NOT NULL,
    limit_display VARCHAR(100) NOT NULL, -- "30/60/25"
    limit_values JSONB NOT NULL, -- {per_person: 30000, per_accident: 60000, property: 25000}
    is_default BOOLEAN DEFAULT false,
    display_order INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Limit type for categorization
CREATE TABLE limit_type (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type_code VARCHAR(50) UNIQUE NOT NULL,
    type_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 2.4 Payment Configuration V2

#### 2.4.1 Payment Plan Types and Instances
```sql
-- Payment plan type definition
CREATE TABLE payment_plan_type (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_type_code VARCHAR(50) UNIQUE NOT NULL,
    plan_type_name VARCHAR(100) NOT NULL,
    installment_count INTEGER NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Program-specific payment plans
CREATE TABLE payment_plan (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_version_id UUID REFERENCES program_version(id),
    payment_plan_type_id UUID REFERENCES payment_plan_type(id),
    plan_code VARCHAR(20) NOT NULL,
    plan_name VARCHAR(100) NOT NULL,
    down_payment_percent DECIMAL(5,2) NOT NULL,
    installment_fee DECIMAL(10,2),
    grace_period_days INTEGER DEFAULT 10,
    nsf_fee DECIMAL(10,2),
    configuration JSONB, -- Additional settings
    is_active BOOLEAN DEFAULT true,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    created_by UUID REFERENCES user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(program_version_id, plan_code, effective_date)
);
```

### 2.5 Discount Management V2

#### 2.5.1 Discount Types and Applications
```sql
-- Discount type definitions
CREATE TABLE discount_type (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    discount_type_code VARCHAR(50) UNIQUE NOT NULL,
    discount_type_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL, -- driver, vehicle, policy
    calculation_method VARCHAR(20) NOT NULL, -- percentage, fixed_amount
    description TEXT,
    metadata JSONB, -- Help text, requirements, etc.
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Program-specific discount configuration
CREATE TABLE discount (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_version_id UUID REFERENCES program_version(id),
    discount_type_id UUID REFERENCES discount_type(id),
    discount_code VARCHAR(50) NOT NULL,
    discount_name VARCHAR(100) NOT NULL,
    base_value DECIMAL(10,4) NOT NULL,
    min_value DECIMAL(10,4),
    max_value DECIMAL(10,4),
    eligibility_rules JSONB NOT NULL,
    proof_requirements JSONB,
    stackable BOOLEAN DEFAULT true,
    max_stack_count INTEGER,
    applies_to VARCHAR(50) NOT NULL, -- policy, vehicle, coverage, driver
    effective_date DATE NOT NULL,
    expiration_date DATE,
    created_by UUID REFERENCES user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(program_version_id, discount_code, effective_date)
);
```

### 2.6 Surcharge Management V2

#### 2.6.1 Surcharge Types and Applications
```sql
-- Surcharge type definitions
CREATE TABLE surcharge_type (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    surcharge_type_code VARCHAR(50) UNIQUE NOT NULL,
    surcharge_type_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL, -- driver, vehicle, territory, policy
    calculation_method VARCHAR(20) NOT NULL, -- percentage, fixed_amount, factor
    description TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Program-specific surcharge configuration
CREATE TABLE surcharge (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_version_id UUID REFERENCES program_version(id),
    surcharge_type_id UUID REFERENCES surcharge_type(id),
    surcharge_code VARCHAR(50) NOT NULL,
    surcharge_name VARCHAR(100) NOT NULL,
    base_value DECIMAL(10,4) NOT NULL,
    tier_values JSONB, -- For tiered surcharges
    trigger_conditions JSONB NOT NULL,
    duration_months INTEGER, -- How long surcharge applies
    applies_to VARCHAR(50) NOT NULL,
    is_declinable BOOLEAN DEFAULT false,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    created_by UUID REFERENCES user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(program_version_id, surcharge_code, effective_date)
);
```

### 2.7 Business Rules Engine

#### 2.7.1 Eligibility Rules
- **Driver Eligibility**
  - Minimum/maximum age
  - License type requirements
  - Years licensed minimum
  - Maximum violations
  - Maximum accidents
  - Excluded driver types

- **Vehicle Eligibility**
  - Vehicle age limits
  - Vehicle type restrictions
  - Value thresholds
  - Usage restrictions
  - Modified vehicle rules

- **Policy Eligibility**
  - Prior insurance requirements
  - Coverage requirement rules
  - Territory restrictions
  - Payment plan eligibility

#### 2.7.2 Underwriting Rules V2
```typescript
interface UnderwritingRule {
  ruleId: string
  ruleName: string
  category: 'eligibility' | 'referral' | 'decline'
  priority: number
  conditions: RuleCondition[]
  actions: RuleAction[]
  effectiveDateRange: DateRange
  overrideable: boolean
  overrideAuthority?: string[]
}

interface RuleCondition {
  field: string
  operator: 'equals' | 'greater_than' | 'less_than' | 'contains' | 'between'
  value: any
  logicalOperator?: 'AND' | 'OR'
}
```

### 2.8 Fee Management V2

```sql
-- Fee type definitions
CREATE TABLE fee_type (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fee_type_code VARCHAR(50) UNIQUE NOT NULL,
    fee_type_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL, -- policy, installment, service, state
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Program-specific fee configuration
CREATE TABLE fee (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_version_id UUID REFERENCES program_version(id),
    fee_type_id UUID REFERENCES fee_type(id),
    fee_code VARCHAR(50) NOT NULL,
    fee_name VARCHAR(100) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    calculation_method VARCHAR(20) DEFAULT 'fixed', -- fixed, percentage
    percentage_base VARCHAR(50), -- premium, coverage_premium
    trigger_conditions JSONB,
    waivable BOOLEAN DEFAULT false,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    created_by UUID REFERENCES user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(program_version_id, fee_code, effective_date)
);
```

## 3. Technical Architecture

### 3.1 System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Interface                             │
│        (Program Configuration UI - React/TypeScript)         │
├─────────────────────────────────────────────────────────────┤
│                    API Gateway                               │
│              (REST APIs + GraphQL)                           │
├─────────────────────────────────────────────────────────────┤
│                 ProgramManager Core Services                 │
├─────────────────┬─────────────────┬────────────────────────┤
│ Program Service │ Territory Svc   │ Business Rule Service  │
├─────────────────┼─────────────────┼────────────────────────┤
│ Coverage Service│ Payment Service │ Integration Service    │
├─────────────────┼─────────────────┼────────────────────────┤
│ Discount Service│ Surcharge Svc   │ Fee Service            │
├─────────────────┴─────────────────┴────────────────────────┤
│                    Data Access Layer                         │
├─────────────────────────────────────────────────────────────┤
│                    PostgreSQL Database                       │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Service Definitions

```typescript
// Program Management Service
interface IProgramService {
  createProgram(config: ProgramConfig): Promise<Program>
  updateProgram(id: string, updates: Partial<ProgramConfig>): Promise<Program>
  createDraftVersion(programId: string): Promise<ProgramVersion>
  publishVersion(versionId: string, approver: User): Promise<void>
  getActiveVersion(programId: string, date: Date): Promise<ProgramVersion>
  rollbackVersion(programId: string, targetVersion: string): Promise<void>
  getVersionHistory(programId: string): Promise<ProgramVersion[]>
}

// Territory Management Service
interface ITerritoryService {
  createTerritory(programId: string, territory: TerritoryConfig): Promise<Territory>
  mapZipCodes(territoryId: string, zipCodes: string[]): Promise<void>
  getTerritoryByZip(programId: string, zipCode: string, date: Date): Promise<Territory>
  updateTerritoryRates(territoryId: string, rates: BaseRates): Promise<void>
  validateTerritoryConfiguration(programId: string): Promise<ValidationResult>
  getTerritoryHistory(territoryId: string): Promise<TerritoryVersion[]>
}

// Business Rule Service
interface IBusinessRuleService {
  createRule(rule: BusinessRule): Promise<BusinessRule>
  evaluateRules(context: RuleContext): Promise<RuleResult[]>
  getApplicableRules(programId: string, ruleType: string, date: Date): Promise<BusinessRule[]>
  validateRuleSet(programId: string): Promise<ValidationResult>
  processOverride(ruleId: string, override: OverrideRequest): Promise<OverrideResult>
  getRuleExecutionHistory(ruleId: string): Promise<RuleExecution[]>
}

// Discount Management Service
interface IDiscountService {
  configureDiscount(programId: string, discount: DiscountConfig): Promise<Discount>
  getEligibleDiscounts(context: DiscountContext): Promise<Discount[]>
  validateDiscountEligibility(discountId: string, context: any): Promise<boolean>
  calculateDiscountValue(discount: Discount, baseAmount: number): Promise<number>
  getDiscountHistory(programId: string): Promise<DiscountVersion[]>
}

// Surcharge Management Service
interface ISurchargeService {
  configureSurcharge(programId: string, surcharge: SurchargeConfig): Promise<Surcharge>
  getApplicableSurcharges(context: SurchargeContext): Promise<Surcharge[]>
  calculateSurchargeValue(surcharge: Surcharge, baseAmount: number): Promise<number>
  getSurchargeHistory(programId: string): Promise<SurchargeVersion[]>
}
```

### 3.3 Enhanced Database Schema

```sql
-- Program Management Core Tables
CREATE TABLE program (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_code VARCHAR(20) UNIQUE NOT NULL,
    program_name VARCHAR(100) NOT NULL,
    program_type VARCHAR(50) NOT NULL,
    carrier_id UUID REFERENCES entity(id),
    mga_id UUID REFERENCES entity(id),
    line_of_business VARCHAR(50) NOT NULL,
    market_segment VARCHAR(50),
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    created_by UUID REFERENCES user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE program_version (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_id UUID REFERENCES program(id),
    version VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    configuration JSONB NOT NULL,
    change_log JSONB,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    created_by UUID REFERENCES user(id),
    approved_by UUID REFERENCES user(id),
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(program_id, version)
);

-- Audit trail for all configuration changes
CREATE TABLE program_configuration_audit (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_version_id UUID REFERENCES program_version(id),
    entity_type VARCHAR(50) NOT NULL, -- discount, surcharge, territory, etc.
    entity_id UUID NOT NULL,
    action VARCHAR(20) NOT NULL, -- create, update, delete
    previous_value JSONB,
    new_value JSONB,
    changed_by UUID REFERENCES user(id),
    change_reason TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Business Rules with versioning
CREATE TABLE business_rule (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_version_id UUID REFERENCES program_version(id),
    rule_code VARCHAR(50) NOT NULL,
    rule_name VARCHAR(100) NOT NULL,
    rule_category VARCHAR(50) NOT NULL,
    priority INTEGER NOT NULL,
    conditions JSONB NOT NULL,
    actions JSONB NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_overrideable BOOLEAN DEFAULT false,
    override_authority JSONB,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    created_by UUID REFERENCES user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(program_version_id, rule_code, effective_date)
);

-- Enhanced indexes for performance
CREATE INDEX idx_territory_zip_lookup ON territory_zip_mapping(zip_code, effective_date DESC);
CREATE INDEX idx_program_version_active ON program_version(program_id, status, effective_date DESC);
CREATE INDEX idx_discount_eligibility ON discount(program_version_id, applies_to, effective_date DESC);
CREATE INDEX idx_surcharge_triggers ON surcharge(program_version_id, applies_to, effective_date DESC);
CREATE INDEX idx_audit_trail ON program_configuration_audit(program_version_id, entity_type, created_at DESC);
```

## 4. Implementation Strategy

### 4.1 Phase 1: Foundation (Weeks 1-4)
1. **Core Infrastructure**
   - Set up program and program_version tables
   - Implement basic CRUD operations
   - Create draft/publish workflow
   - Build version management system
   - Establish audit trail framework

2. **Type System Setup**
   - Create all _type tables
   - Populate standard type definitions
   - Build type management interfaces
   - Implement type validation

### 4.2 Phase 2: Territory Management (Weeks 5-8)
1. **Territory Configuration**
   - Implement territory and territory_type tables
   - Build ZIP code mapping functionality
   - Create territory visualization
   - Implement historical tracking

2. **Territory Integration**
   - Connect to address validation service
   - Implement ZIP to territory lookup with date awareness
   - Create territory assignment API
   - Build territory change management

### 4.3 Phase 3: Coverage & Limits (Weeks 9-12)
1. **Coverage Configuration**
   - Implement coverage_type and program_coverage
   - Build limit configuration system
   - Create deductible management
   - Implement coverage dependencies

2. **Coverage Validation**
   - State requirement checking
   - Coverage combination validation
   - Limit adequacy verification
   - Required coverage enforcement

### 4.4 Phase 4: Payment & Financial (Weeks 13-16)
1. **Payment Plan Setup**
   - Implement payment_plan_type and payment_plan
   - Build installment calculation
   - Create payment schedule generation
   - Implement grace period logic

2. **Fee Management**
   - Implement fee_type and fee tables
   - Build fee calculation engine
   - Create waiver logic
   - Implement fee stacking rules

### 4.5 Phase 5: Discounts & Surcharges (Weeks 17-20)
1. **Discount Management**
   - Implement discount_type and discount tables
   - Build eligibility evaluation
   - Create proof requirement tracking
   - Implement stacking rules

2. **Surcharge Management**
   - Implement surcharge_type and surcharge tables
   - Build trigger evaluation
   - Create duration tracking
   - Implement tier calculations

### 4.6 Phase 6: Business Rules (Weeks 21-24)
1. **Rule Engine Development**
   - Implement business_rule table
   - Build rule evaluation engine
   - Create override workflow
   - Implement rule versioning

2. **Rule Testing & Validation**
   - Build rule testing sandbox
   - Implement conflict detection
   - Create performance optimization
   - Build rule analytics

## 5. Integration Points

### 5.1 Internal System Integration

1. **ProgramRater Integration**
   - Provide all configuration data with version awareness
   - Supply type definitions for factor categorization
   - Deliver discount/surcharge configurations
   - Share business rule parameters

2. **Producer Portal Integration**
   - Program availability by producer
   - Real-time configuration updates
   - Override request handling
   - Commission configuration

3. **Accounting System Integration**
   - Payment plan details
   - Fee schedules
   - Commission structures
   - Premium allocation rules

### 5.2 External Service Integration

1. **Regulatory Reporting**
   - Enhanced audit trail exports
   - Type-based categorization reports
   - Configuration change tracking
   - Compliance documentation

2. **Data Services**
   - MVR ordering configuration
   - Credit scoring parameters
   - Claims history thresholds
   - Address validation rules

## 6. Security & Compliance

### 6.1 Access Control
- Role-based permissions (Admin, Manager, Analyst, Viewer)
- Program-level access restrictions
- Approval workflow enforcement
- Complete change attribution

### 6.2 Enhanced Audit Requirements
- Configuration change tracking at field level
- User action logging with context
- Version comparison capabilities
- Regulatory compliance documentation
- Type/instance relationship tracking

### 6.3 Data Protection
- Encryption of sensitive configuration
- Secure credential storage
- API key management
- PII handling compliance

## 7. Performance Requirements

### 7.1 Response Time Targets
- Program load: < 1 second
- Configuration save: < 2 seconds
- ZIP lookup: < 100ms
- Rule evaluation: < 500ms
- Version publish: < 5 seconds
- Audit trail query: < 1 second

### 7.2 Scalability Requirements
- Support 100+ active programs
- Handle 1M+ ZIP code mappings
- Process 10K+ business rules
- Maintain complete audit history
- Support 1M+ configuration changes

## 8. User Interface Requirements

### 8.1 Configuration Interfaces
1. **Program Dashboard**
   - Active program overview
   - Version status summary
   - Recent changes with audit trail
   - Pending approvals

2. **Type Management**
   - Type definition interfaces
   - Type usage analytics
   - Type migration tools
   - Type validation reports

3. **Configuration Wizards**
   - Step-by-step program setup
   - Type-based templates
   - Validation at each step
   - Import/export capabilities

### 8.2 Administrative Tools
1. **Enhanced Approval Workflow**
   - Change impact analysis
   - Side-by-side comparisons
   - Bulk approval capabilities
   - Audit trail review

2. **Monitoring & Analytics**
   - Configuration usage metrics
   - Type utilization reports
   - Change frequency analysis
   - Performance dashboards

## 9. Success Metrics

### 9.1 Operational Metrics
- Configuration accuracy: 99.9%
- System availability: 99.95%
- Average configuration time: < 2 hours
- Version deployment time: < 10 minutes
- Audit query performance: < 1 second

### 9.2 Business Metrics
- Programs managed: 50+ in year 1
- Configuration errors: < 0.1%
- Time to market: 50% reduction
- Compliance violations: Zero
- Audit findings: Zero critical

## 10. Risk Mitigation

### 10.1 Technical Risks
1. **Configuration Complexity**
   - Mitigation: Type system simplification
   - Testing: Comprehensive validation
   - Recovery: Version rollback capability

2. **Performance at Scale**
   - Mitigation: Proper indexing strategy
   - Monitoring: Real-time metrics
   - Scaling: Partitioning ready

### 10.2 Business Risks
1. **Regulatory Compliance**
   - Mitigation: Complete audit trails
   - Documentation: Automated reporting
   - Review: Regular compliance audits

2. **Data Integrity**
   - Mitigation: Type validation
   - Testing: Referential integrity
   - Recovery: Point-in-time restore

## 11. Migration Strategy

### 11.1 From V1 to V2
1. **Type System Migration**
   - Extract types from existing data
   - Create type definitions
   - Map instances to types
   - Validate relationships

2. **Audit Trail Enhancement**
   - Backfill historical data where possible
   - Implement forward-looking tracking
   - Create migration reports
   - Validate compliance

## 12. Future Enhancements

### 12.1 Advanced Features
- AI-powered configuration recommendations
- Automated testing suites
- Market analysis integration
- Competitive intelligence tools
- Predictive configuration optimization

### 12.2 Integration Expansion
- Real-time rate filing
- Automated compliance checking
- Market feedback loops
- Performance optimization AI
- Configuration impact analysis

## Appendix A: Type System Examples

### A.1 Discount Type Definition
```json
{
  "discount_type_code": "GOOD_DRIVER",
  "discount_type_name": "Good Driver Discount",
  "category": "driver",
  "calculation_method": "percentage",
  "metadata": {
    "description": "Discount for drivers with clean records",
    "requirements": [
      "No at-fault accidents in 3 years",
      "No moving violations in 3 years",
      "Valid license for 3+ years"
    ],
    "documentation": "MVR required for verification"
  }
}
```

### A.2 Surcharge Type Definition
```json
{
  "surcharge_type_code": "YOUTHFUL_DRIVER",
  "surcharge_type_name": "Youthful Driver Surcharge",
  "category": "driver",
  "calculation_method": "factor",
  "metadata": {
    "description": "Surcharge for drivers under 25",
    "age_bands": [
      {"min": 16, "max": 17, "factor": 1.75},
      {"min": 18, "max": 20, "factor": 1.50},
      {"min": 21, "max": 24, "factor": 1.25}
    ],
    "mitigation": "Good student discount available"
  }
}
```

## Appendix B: Audit Trail Examples

### B.1 Configuration Change Audit
```json
{
  "program_version_id": "uuid-123",
  "entity_type": "discount",
  "entity_id": "uuid-456",
  "action": "update",
  "previous_value": {
    "base_value": 0.10,
    "max_value": 0.15
  },
  "new_value": {
    "base_value": 0.12,
    "max_value": 0.20
  },
  "changed_by": "user-789",
  "change_reason": "Market competitive adjustment",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### B.2 Territory Change Tracking
```json
{
  "program_version_id": "uuid-123",
  "entity_type": "territory_zip_mapping",
  "entity_id": "uuid-789",
  "action": "create",
  "new_value": {
    "territory_id": "territory-01",
    "zip_codes": ["75001", "75002", "75003"],
    "effective_date": "2024-02-01"
  },
  "changed_by": "user-456",
  "change_reason": "Q1 2024 territory realignment",
  "created_at": "2024-01-20T14:15:00Z"
}
```