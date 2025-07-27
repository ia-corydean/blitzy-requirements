# ProgramManager Global Requirements Approach

## Executive Summary

The ProgramManager serves as the comprehensive configuration and management system for insurance programs within the Aime platform. It provides the administrative interface and backend systems for creating, configuring, and maintaining insurance programs including coverage options, territorial definitions, payment configurations, eligibility rules, and business rule enforcement. The system implements a draft/publish workflow to ensure changes are properly tested before deployment.

## 1. System Overview

### 1.1 Core Responsibilities

```
┌─────────────────────────────────────────────────────────────┐
│                    ProgramManager                            │
├─────────────────────────────────────────────────────────────┤
│ • Program Configuration & Versioning                         │
│ • Territory & Geographic Management                          │
│ • Coverage & Limits Configuration                            │
│ • Business Rules & Eligibility                              │
│ • Discount & Surcharge Management                            │
│ • Payment Plan Configuration                                 │
│ • Integration Management                                     │
│ • Draft/Publish Workflow                                     │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Key Features

1. **Program Lifecycle Management**
   - Create and configure new insurance programs
   - Version control with draft/publish workflow
   - Effective date management
   - Program activation/deactivation

2. **Geographic Configuration**
   - Territory definition and management
   - ZIP code to territory mapping
   - County-based tax configuration
   - Regional surcharge setup

3. **Product Configuration**
   - Coverage types and combinations
   - Limit options and constraints
   - Deductible configurations
   - Endorsement management

4. **Business Rule Engine**
   - Eligibility criteria definition
   - Underwriting rule configuration
   - Validation rule setup
   - Override authority management

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

#### 2.2.2 Territory Data Model
```sql
CREATE TABLE territory (
    id UUID PRIMARY KEY,
    program_id UUID REFERENCES program(id),
    territory_code VARCHAR(10) NOT NULL,
    territory_name VARCHAR(100) NOT NULL,
    description TEXT,
    risk_tier INTEGER NOT NULL CHECK (risk_tier BETWEEN 1 AND 10),
    state_id UUID REFERENCES state(id),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(program_id, territory_code)
);

CREATE TABLE territory_zip_mapping (
    id UUID PRIMARY KEY,
    territory_id UUID REFERENCES territory(id),
    zip_code VARCHAR(10) NOT NULL,
    county_id UUID REFERENCES county(id),
    effective_date DATE NOT NULL,
    expiration_date DATE,
    created_at TIMESTAMP DEFAULT NOW(),
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

#### 2.3.2 Limit Configuration
```typescript
interface CoverageLimitConfig {
  coverageType: string
  availableLimits: LimitOption[]
  defaultLimit: string
  minimumRequired?: string
  stateRequirements: StateRequirement[]
  combinedSingleLimit: boolean
  deductibleOptions?: DeductibleOption[]
}

interface LimitOption {
  limitCode: string
  limitDisplay: string // e.g., "30/60/25"
  limitValues: {
    perPerson?: number
    perAccident?: number
    propertyDamage?: number
    combinedLimit?: number
  }
  restrictionRules: string[]
}
```

### 2.4 Payment Configuration

#### 2.4.1 Payment Plans
- **Plan Types**
  - Full pay
  - Two-pay (50% down)
  - Four-pay quarterly
  - Six-pay bi-monthly
  - Monthly (10 or 12 payments)

- **Plan Configuration**
  - Down payment percentages
  - Installment fee schedules
  - Grace period settings
  - NSF fee configuration
  - Reinstatement rules

#### 2.4.2 Payment Methods
- **Accepted Methods**
  - Credit/Debit cards
  - ACH/Electronic funds transfer
  - Check/Money order
  - Cash (agent office only)
  - Premium finance

- **Method Rules**
  - Processing fees by method
  - Recurring payment setup
  - Payment method restrictions by program

### 2.5 Discount Management

#### 2.5.1 Available Discounts
Based on the rating factors, the following discounts must be configurable:

1. **Driver Discounts**
   - Good driver discount
   - Defensive driving course
   - Scholastic discount
   - Mature driver discount

2. **Vehicle Discounts**
   - Multi-car discount
   - Anti-theft device
   - Passive restraint
   - Vehicle safety features

3. **Policy Discounts**
   - Multi-policy discount
   - Electronic funds transfer
   - Paperless delivery
   - Paid-in-full discount

#### 2.5.2 Discount Configuration
```typescript
interface DiscountConfig {
  discountCode: string
  discountName: string
  discountType: 'percentage' | 'fixed_amount'
  value: number
  applicableTo: 'policy' | 'vehicle' | 'coverage' | 'driver'
  eligibilityRules: EligibilityRule[]
  stackable: boolean
  maxStackedValue?: number
  effectiveDateRange: DateRange
  requiredProof?: ProofRequirement[]
}
```

### 2.6 Surcharge Management

#### 2.6.1 Surcharge Types
1. **Driver Surcharges**
   - Inexperienced driver
   - Youthful driver
   - Violations (speeding, DUI, etc.)
   - At-fault accidents
   - License type restrictions

2. **Geographic Surcharges**
   - High-risk territory
   - Urban zone surcharge
   - Regional adjustments

3. **Policy Surcharges**
   - Lapse in coverage
   - SR-22 filing
   - High-risk classification

#### 2.6.2 Surcharge Rules
```typescript
interface SurchargeConfig {
  surchargeCode: string
  surchargeName: string
  surchargeType: 'percentage' | 'fixed_amount' | 'factor'
  baseValue: number
  tieredValues?: TieredValue[]
  applicableTo: string
  triggerConditions: TriggerCondition[]
  duration?: number // months
  declineOption: boolean
}
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

#### 2.7.2 Underwriting Rules
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

### 2.8 Integration Configuration

#### 2.8.1 External Service Integration
Based on program requirements, configure connections to:

1. **Data Services**
   - MVR providers (driver records)
   - CLUE database (claims history)
   - Credit bureaus (where permitted)
   - VIN decoders
   - Address validation services

2. **Regulatory Services**
   - DMV connections
   - SR-22 filing systems
   - State reporting interfaces

3. **Financial Services**
   - Payment gateways
   - Premium finance companies
   - ACH processors

#### 2.8.2 Integration Settings
```typescript
interface IntegrationConfig {
  serviceType: string
  provider: string
  credentials: EncryptedCredentials
  endpoints: EndpointConfig[]
  retryPolicy: RetryConfig
  timeoutMs: number
  cacheTTL?: number
  fallbackBehavior: 'fail' | 'default' | 'manual'
  costPerTransaction?: number
  usageTracking: boolean
}
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
}

// Territory Management Service
interface ITerritoryService {
  createTerritory(programId: string, territory: TerritoryConfig): Promise<Territory>
  mapZipCodes(territoryId: string, zipCodes: string[]): Promise<void>
  getTerritoryByZip(programId: string, zipCode: string): Promise<Territory>
  updateTerritoryRates(territoryId: string, rates: BaseRates): Promise<void>
  validateTerritoryConfiguration(programId: string): Promise<ValidationResult>
}

// Business Rule Service
interface IBusinessRuleService {
  createRule(rule: BusinessRule): Promise<BusinessRule>
  evaluateRules(context: RuleContext): Promise<RuleResult[]>
  getApplicableRules(programId: string, ruleType: string): Promise<BusinessRule[]>
  validateRuleSet(programId: string): Promise<ValidationResult>
  processOverride(ruleId: string, override: OverrideRequest): Promise<OverrideResult>
}
```

### 3.3 Database Schema

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

-- Coverage Configuration
CREATE TABLE program_coverage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_version_id UUID REFERENCES program_version(id),
    coverage_type_id UUID REFERENCES coverage_type(id),
    is_required BOOLEAN DEFAULT false,
    is_available BOOLEAN DEFAULT true,
    limit_options JSONB NOT NULL,
    deductible_options JSONB,
    configuration JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Discount Configuration
CREATE TABLE program_discount (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_version_id UUID REFERENCES program_version(id),
    discount_code VARCHAR(50) NOT NULL,
    discount_name VARCHAR(100) NOT NULL,
    discount_type VARCHAR(20) NOT NULL,
    base_value DECIMAL(10,4) NOT NULL,
    configuration JSONB NOT NULL,
    eligibility_rules JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(program_version_id, discount_code)
);

-- Surcharge Configuration
CREATE TABLE program_surcharge (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_version_id UUID REFERENCES program_version(id),
    surcharge_code VARCHAR(50) NOT NULL,
    surcharge_name VARCHAR(100) NOT NULL,
    surcharge_type VARCHAR(20) NOT NULL,
    base_value DECIMAL(10,4) NOT NULL,
    configuration JSONB NOT NULL,
    trigger_conditions JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(program_version_id, surcharge_code)
);

-- Business Rules
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
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(program_version_id, rule_code)
);

-- Payment Plans
CREATE TABLE program_payment_plan (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_version_id UUID REFERENCES program_version(id),
    plan_code VARCHAR(20) NOT NULL,
    plan_name VARCHAR(100) NOT NULL,
    installments INTEGER NOT NULL,
    down_payment_percent DECIMAL(5,2) NOT NULL,
    installment_fee DECIMAL(10,2),
    configuration JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(program_version_id, plan_code)
);
```

## 4. Implementation Strategy

### 4.1 Phase 1: Foundation (Weeks 1-4)
1. **Core Infrastructure**
   - Set up program and program_version tables
   - Implement basic CRUD operations
   - Create draft/publish workflow
   - Build version management system

2. **User Interface Foundation**
   - Program list and search interface
   - Basic program creation wizard
   - Version comparison tools
   - Audit trail viewer

### 4.2 Phase 2: Territory Management (Weeks 5-8)
1. **Territory Configuration**
   - Territory definition interface
   - ZIP code mapping tools
   - Bulk ZIP upload functionality
   - Territory visualization maps

2. **Territory Integration**
   - Connect to address validation service
   - Implement ZIP to territory lookup
   - Create territory assignment API
   - Build territory change management

### 4.3 Phase 3: Coverage & Limits (Weeks 9-12)
1. **Coverage Configuration**
   - Coverage type management
   - Limit option configuration
   - Deductible setup
   - Coverage dependency rules

2. **Coverage Validation**
   - State requirement checking
   - Coverage combination validation
   - Limit adequacy verification
   - Required coverage enforcement

### 4.4 Phase 4: Payment & Financial (Weeks 13-16)
1. **Payment Plan Setup**
   - Payment plan configuration
   - Down payment rules
   - Installment fee management
   - Grace period configuration

2. **Payment Integration**
   - Payment gateway setup
   - Recurring payment configuration
   - NSF handling rules
   - Reinstatement procedures

### 4.5 Phase 5: Discounts & Surcharges (Weeks 17-20)
1. **Discount Management**
   - Discount configuration interface
   - Eligibility rule builder
   - Proof requirement setup
   - Stacking rule configuration

2. **Surcharge Management**
   - Surcharge definition tools
   - Trigger condition builder
   - Duration management
   - Tier configuration

### 4.6 Phase 6: Business Rules (Weeks 21-24)
1. **Rule Engine Development**
   - Rule builder interface
   - Condition configuration
   - Action definition
   - Priority management

2. **Rule Testing & Validation**
   - Rule testing sandbox
   - Conflict detection
   - Override workflow
   - Rule performance optimization

## 5. Integration Points

### 5.1 Internal System Integration

1. **ProgramRater Integration**
   - Provide rating configuration data
   - Territory and base rate information
   - Discount/surcharge definitions
   - Business rule parameters

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
   - Rate filing extracts
   - Program change notifications
   - Compliance reporting
   - Audit trail exports

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
- Change tracking and attribution

### 6.2 Audit Requirements
- Complete configuration change history
- User action logging
- Version comparison capabilities
- Regulatory compliance documentation

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

### 7.2 Scalability Requirements
- Support 100+ active programs
- Handle 1M+ ZIP code mappings
- Process 10K+ business rules
- Maintain 5-year version history

## 8. User Interface Requirements

### 8.1 Configuration Interfaces
1. **Program Dashboard**
   - Active program overview
   - Version status summary
   - Recent changes
   - Pending approvals

2. **Configuration Wizards**
   - Step-by-step program setup
   - Validation at each step
   - Configuration templates
   - Import/export capabilities

3. **Testing Tools**
   - Configuration sandbox
   - Test quote generation
   - Rule testing interface
   - Version comparison

### 8.2 Administrative Tools
1. **Approval Workflow**
   - Change review interface
   - Approval queues
   - Comment and feedback
   - Rollback capabilities

2. **Monitoring & Analytics**
   - Configuration usage metrics
   - Rule hit rates
   - Override frequency
   - Error tracking

## 9. Success Metrics

### 9.1 Operational Metrics
- Configuration accuracy: 99.9%
- System availability: 99.95%
- Average configuration time: < 2 hours
- Version deployment time: < 10 minutes

### 9.2 Business Metrics
- Programs managed: 50+ in year 1
- Configuration errors: < 0.1%
- Time to market: 50% reduction
- Compliance violations: Zero

## 10. Risk Mitigation

### 10.1 Technical Risks
1. **Configuration Errors**
   - Mitigation: Comprehensive validation
   - Testing: Sandbox environment
   - Recovery: Version rollback capability

2. **Performance Issues**
   - Mitigation: Caching strategies
   - Monitoring: Real-time metrics
   - Scaling: Horizontal scaling ready

### 10.2 Business Risks
1. **Regulatory Compliance**
   - Mitigation: Built-in compliance checks
   - Documentation: Complete audit trails
   - Review: Regular compliance audits

2. **User Adoption**
   - Mitigation: Intuitive interface design
   - Training: Comprehensive documentation
   - Support: Dedicated help resources

## 11. Future Enhancements

### 11.1 Advanced Features
- AI-powered configuration recommendations
- Automated testing suites
- Market analysis integration
- Competitive intelligence tools

### 11.2 Integration Expansion
- Real-time rate filing
- Automated compliance checking
- Market feedback loops
- Performance optimization AI

## Appendix A: Configuration Templates

### A.1 Standard Auto Program Template
```json
{
  "programType": "personal_auto",
  "territories": 12,
  "coverages": ["liability", "um_uim", "comprehensive", "collision", "pip"],
  "paymentPlans": ["full", "two_pay", "four_pay", "monthly"],
  "standardDiscounts": ["multi_car", "good_driver", "defensive_driving"],
  "eligibilityRules": {
    "minDriverAge": 18,
    "maxVehicleAge": 20,
    "maxViolations": 3,
    "requiresPriorInsurance": true
  }
}
```

### A.2 Territory Configuration Template
```json
{
  "territoryCode": "01",
  "territoryName": "North Texas Metro",
  "riskTier": 3,
  "baseRates": {
    "liability": 279,
    "um_uim": 45,
    "comprehensive": 96,
    "collision": 251,
    "pip": 25
  },
  "zipCodes": ["75001", "75002", "75003"]
}
```

## Appendix B: Business Rule Examples

### B.1 Eligibility Rule
```json
{
  "ruleCode": "ELIG_001",
  "ruleName": "Minimum Driver Age",
  "category": "eligibility",
  "conditions": [{
    "field": "driver.age",
    "operator": "less_than",
    "value": 18
  }],
  "actions": [{
    "type": "decline",
    "message": "Driver must be at least 18 years old"
  }]
}
```

### B.2 Underwriting Rule
```json
{
  "ruleCode": "UW_001",
  "ruleName": "High Risk Driver Referral",
  "category": "referral",
  "conditions": [{
    "field": "driver.violations.dui",
    "operator": "greater_than",
    "value": 0
  }],
  "actions": [{
    "type": "refer_underwriting",
    "reason": "DUI violation requires underwriter review"
  }],
  "overrideable": true,
  "overrideAuthority": ["underwriter", "manager"]
}
```