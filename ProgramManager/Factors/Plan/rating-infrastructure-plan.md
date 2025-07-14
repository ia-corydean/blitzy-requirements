# Rating Infrastructure Master Plan
## Aguila Dorada Texas Personal Auto Program

### Executive Summary
This master plan defines the comprehensive rating infrastructure for the Aguila Dorada Texas Personal Auto insurance program. The system implements a sophisticated multiplicative rating engine that processes 34 distinct rate factors across driver, vehicle, and policy dimensions to calculate accurate premiums based on risk assessment and regulatory requirements.

---

## 1. Rating Methodology Overview

### Core Rating Formula
```
Final Premium = Base Rate × Policy Core Matrix × Driver Class × Driver Points × Vehicle Age × [All Other Factors]
```

### Multiplicative Algorithm Structure
- **Foundation**: Territory-based vehicle base rates by coverage type
- **Risk Assessment**: Multi-dimensional factor application across all rating categories
- **Calculation Sequence**: Ordered factor application with validation at each step
- **Result Validation**: Premium reasonableness checks and regulatory compliance verification

### Rating Factor Categories
1. **Core Components (7 factors)**: Foundation rating elements
2. **Driver Factors (4 factors)**: Demographics, violations, and licensing
3. **Vehicle Factors (14 factors)**: Physical characteristics, usage, and territory
4. **Policy Factors (9 factors)**: Coverage, terms, and operational adjustments

---

## 2. Global Requirements Integration

### Applicable Global Requirements
- **GR-20**: Application Business Logic - Service architecture patterns
- **GR-41**: Table Schema Requirements - Database design standards
- **GR-18**: Workflow Requirements - Rating process integration
- **GR-03**: Models & Relationships - Eloquent model patterns
- **GR-04**: Validation & Data Handling - Input validation standards
- **GR-33**: Data Services Architecture - Caching and performance optimization
- **GR-19**: Table Relationships - Association patterns and audit trails

### Architecture Alignment
The rating infrastructure follows established Laravel service layer patterns from the blitzy-requirements codebase:
- Domain-driven service organization under `app/Domain/Rating/`
- Event-driven architecture with comprehensive audit trails
- Multi-tenant support with tenant-scoped rating configurations
- Integration with existing authentication and authorization systems

---

## 3. Service Architecture Design

### Core Rating Services

#### RatingEngineService
**Purpose**: Central rating calculation engine
**Responsibilities**:
- Orchestrate factor lookup and application
- Execute multiplicative calculation sequence
- Validate calculation results and business rules
- Generate comprehensive audit trails

**Key Methods**:
```php
public function calculatePremium(PolicyRatingRequest $request): PremiumCalculation
public function validateRatingInputs(array $ratingData): ValidationResult
public function getRatingFactorBreakdown(int $policyId): RatingBreakdown
```

#### RatingFactorService
**Purpose**: Rating factor management and lookup
**Responsibilities**:
- Retrieve active rating factors by category and type
- Validate factor effective dates and program applicability
- Cache factor lookups for performance optimization
- Handle factor versioning and historical data

**Key Methods**:
```php
public function getDriverClassFactor(DriverProfile $driver): RatingFactor
public function getVehicleAgeFactor(Vehicle $vehicle): RatingFactor
public function getPolicyCoreMatrixFactor(PolicyData $policy): RatingFactor
```

#### PremiumCalculationService
**Purpose**: Premium computation with detailed breakdown
**Responsibilities**:
- Execute step-by-step premium calculations
- Generate factor application audit trails
- Store calculation results with full traceability
- Support premium recalculation for adjustments

#### RiskAssessmentService
**Purpose**: Risk evaluation and factor validation
**Responsibilities**:
- Validate risk factor combinations
- Apply underwriting guidelines and restrictions
- Generate risk assessment reports
- Support exception handling and manual overrides

### Integration with Existing Services
- **PolicyService**: Rating integration for quote and policy workflows
- **PaymentService**: Premium calculation integration for billing
- **DocumentManager**: Rating documentation and audit report generation
- **WorkflowService**: Rating process integration with policy lifecycle

---

## 4. Database Schema Architecture

### Rating Factor Tables

#### Core Rating Factor Structure
```sql
-- Rating factor categories (driver, vehicle, policy)
CREATE TABLE rating_factor_category (
    id BIGINT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    sort_order INT DEFAULT 0,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (status_id) REFERENCES status(id)
);

-- Rating factor types within categories
CREATE TABLE rating_factor_type (
    id BIGINT PRIMARY KEY,
    category_id BIGINT NOT NULL,
    code VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    calculation_method ENUM('LOOKUP', 'FORMULA', 'MATRIX') NOT NULL,
    applies_to ENUM('POLICY', 'COVERAGE', 'VEHICLE', 'DRIVER') NOT NULL,
    is_required BOOLEAN DEFAULT TRUE,
    sort_order INT DEFAULT 0,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES rating_factor_category(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    UNIQUE KEY unique_factor_type (category_id, code)
);

-- Rating factor values with versioning
CREATE TABLE rating_factor_value (
    id BIGINT PRIMARY KEY,
    factor_type_id BIGINT NOT NULL,
    program_id BIGINT NOT NULL,
    factor_key VARCHAR(255) NOT NULL,
    factor_value DECIMAL(10,6) NOT NULL,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    metadata JSON,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (factor_type_id) REFERENCES rating_factor_type(id),
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_factor_lookup (factor_type_id, program_id, factor_key, effective_date),
    INDEX idx_effective_dates (effective_date, expiration_date)
);
```

#### Premium Calculation Storage
```sql
-- Premium calculation audit and storage
CREATE TABLE premium_calculation (
    id BIGINT PRIMARY KEY,
    policy_id BIGINT,
    quote_id BIGINT,
    calculation_type ENUM('QUOTE', 'POLICY', 'RENEWAL', 'ADJUSTMENT') NOT NULL,
    base_premium DECIMAL(12,2) NOT NULL,
    total_premium DECIMAL(12,2) NOT NULL,
    calculation_date TIMESTAMP NOT NULL,
    effective_date DATE NOT NULL,
    calculation_metadata JSON,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (quote_id) REFERENCES quote(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_policy_calculation (policy_id, calculation_date),
    INDEX idx_quote_calculation (quote_id, calculation_date)
);

-- Applied rating factors per calculation
CREATE TABLE applied_rating_factor (
    id BIGINT PRIMARY KEY,
    calculation_id BIGINT NOT NULL,
    factor_type_id BIGINT NOT NULL,
    factor_key VARCHAR(255) NOT NULL,
    factor_value DECIMAL(10,6) NOT NULL,
    applied_premium DECIMAL(12,2) NOT NULL,
    calculation_step INT NOT NULL,
    metadata JSON,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (calculation_id) REFERENCES premium_calculation(id),
    FOREIGN KEY (factor_type_id) REFERENCES rating_factor_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_calculation_factors (calculation_id, calculation_step)
);
```

### Territory and Geographic Tables
```sql
-- Territory assignment and base rates
CREATE TABLE rating_territory (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    territory_code VARCHAR(10) NOT NULL,
    territory_name VARCHAR(255) NOT NULL,
    state_id BIGINT NOT NULL,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (state_id) REFERENCES state(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    UNIQUE KEY unique_territory (program_id, territory_code, effective_date)
);

-- ZIP code to territory mapping
CREATE TABLE territory_zip_mapping (
    id BIGINT PRIMARY KEY,
    territory_id BIGINT NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (territory_id) REFERENCES rating_territory(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_zip_lookup (zip_code, effective_date),
    INDEX idx_territory_mapping (territory_id, effective_date)
);
```

---

## 5. Rating Factor Implementation Strategy

### Factor Categories and Implementation Approach

#### Core Rating Components (7 factors)
1. **Algorithm** - Central calculation engine with multiplicative logic
2. **Vehicle Base Rates** - Territory-based foundation rates by coverage
3. **Policy Core Matrix** - Three-dimensional discount matrix (insurance history × license years × ownership)
4. **Driver Class** - Age/gender/marital status risk assessment
5. **Driver Points** - Violation and conviction multipliers
6. **Policy Limits** - Coverage limit selection factors
7. **Driver Assignment** - Driver-to-vehicle assignment rules

#### Driver-Related Factors (4 factors)
1. **Driver Points Violations** - Specific violation point assignments
2. **Driver Points Violations V1** - Legacy violation scoring system
3. **Driver License Type** - License classification factors
4. **Policy Criminal History** - Criminal background risk assessment

#### Vehicle-Related Factors (14 factors)
1. **Vehicle Age** - Model year-based depreciation factors
2. **Vehicle Use/Usage** - Primary use classification (pleasure, commute, business)
3. **Vehicle Make/Model** - Manufacturer and model risk factors
4. **Vehicle Territory** - Geographic risk assessment
5. **Vehicle County Modifier** - County-specific adjustments
6. **Vehicle Photo** - Photo inspection requirement factors
7. **Vehicle Deductible** - Deductible selection impact
8. **Vehicle Additional Equipment** - Equipment coverage factors
9. **Vehicle Coverage Type** - Coverage selection factors
10. **Vehicle Length of Owner** - Ownership duration impact
11. **Vehicle Mileage Ratio** - Annual mileage risk assessment
12. **Vehicle Model Year** - Specific model year classifications
13. **Vehicle Severe Problem** - Vehicle condition risk factors
14. **Vehicle VIN Master Physical Damage** - VIN-based physical damage factors

#### Policy-Level Factors (9 factors)
1. **Policy Distribution Channel** - Sales channel impact
2. **Policy Driver to Vehicle** - Assignment relationship factors
3. **Policy Term** - Policy term length factors
4. **Policy Miscellaneous Adjustments** - Various policy-level adjustments
5. **Policy Fees** - Fee structure and assessment
6. **Policy Payment Plan** - Payment plan selection impact
7. **Policy Renewal** - Renewal-specific factors
8. **Region** - Regional classification and factors

---

## 6. Performance Optimization Strategy

### Caching Architecture (Following GR-33)
#### L1 Cache - Application Level
- **Rating Factor Cache**: 1-hour TTL for factor lookups
- **Territory Mapping Cache**: 24-hour TTL for ZIP code mappings
- **Base Rate Cache**: 4-hour TTL for territory base rates

#### L2 Cache - Redis
- **Premium Calculation Cache**: Policy-specific calculation results
- **Factor Combination Cache**: Common factor combination results
- **Validation Rule Cache**: Business rule and validation caching

#### L3 Cache - CDN/Database
- **Static Factor Tables**: Read replicas for factor lookup optimization
- **Historical Rate Data**: Archived calculation results

### Database Performance Optimization
- **Connection Pooling**: Laravel connection pooling for rating queries
- **Read Replicas**: Factor lookups use read replicas
- **Query Optimization**: Optimized joins and indexes for rating calculations
- **Batch Processing**: Bulk rating calculations for renewals

### Calculation Performance Targets
- **Individual Rating**: <2 seconds for complete premium calculation
- **Batch Rating**: <30 seconds per 100 policies for renewal calculations
- **Factor Lookup**: <100ms for individual factor retrieval
- **Cache Hit Ratio**: >90% for factor lookups during normal operations

---

## 7. Integration Points and APIs

### External Integration Requirements
- **DCS APIs (GR-53)**: Driver and vehicle verification data integration
- **Territory Services**: ZIP code and geographic data validation
- **Regulatory Systems**: Rate filing and compliance verification
- **Document Generation**: Rating documentation and disclosure generation

### Internal API Integration
- **Quote Workflow**: Real-time rating during quote generation
- **Policy Binding**: Final premium calculation and validation
- **Policy Renewal**: Renewal premium calculation with factor updates
- **Policy Adjustment**: Mid-term adjustment calculations

### Rating API Endpoints
```php
// Core rating endpoints
POST /api/v1/rating/calculate           // Calculate premium for quote/policy
GET  /api/v1/rating/factors/{type}      // Retrieve rating factors by type
POST /api/v1/rating/validate           // Validate rating inputs
GET  /api/v1/rating/breakdown/{id}      // Get detailed factor breakdown

// Territory and geographic endpoints
GET  /api/v1/rating/territory/{zip}     // Get territory by ZIP code
GET  /api/v1/rating/base-rates/{territory} // Get base rates by territory

// Administrative endpoints
POST /api/v1/admin/rating/factors       // Update rating factors
GET  /api/v1/admin/rating/audit/{id}    // Get calculation audit trail
```

---

## 8. Validation and Business Rules

### Input Validation Patterns (Following GR-04)
#### Multi-Layer Validation
- **Client-Side**: Real-time validation with immediate feedback
- **Server-Side**: Laravel Form Request validation with insurance-specific rules
- **Database**: Constraint validation and referential integrity

#### Custom Validation Rules
```php
// Insurance domain validation rules
ValidDriverAge::class,           // Age between 16-100
ValidVehicleYear::class,         // Model year within acceptable range
ValidCoverageAmount::class,      // Coverage amounts within regulatory limits
ValidTerritoryCode::class,       // Valid territory for state and program
ValidPremiumAmount::class,       // Premium within reasonable bounds
```

### Business Rule Implementation
- **Regulatory Compliance**: Texas insurance regulation adherence
- **Underwriting Guidelines**: Risk assessment and eligibility rules
- **Factor Interaction Rules**: Validation of factor combinations
- **Premium Reasonableness**: Upper and lower bounds validation

---

## 9. Security and Compliance

### Multi-Tenant Security
- **Tenant Isolation**: Rating factors and calculations scoped by tenant
- **Data Access Control**: Role-based access to rating administration
- **Audit Trail Security**: Comprehensive logging with user attribution

### Regulatory Compliance
- **Rate Filing Compliance**: Integration with regulatory rate filing systems
- **Calculation Transparency**: Detailed factor breakdown for regulatory review
- **Historical Data Retention**: 7-year retention for regulatory compliance
- **Actuarial Support**: Statistical justification tracking for all factors

### Data Protection
- **PII Handling**: Secure handling of driver and policy data
- **Calculation Integrity**: Cryptographic validation of calculation results
- **Access Logging**: Comprehensive access logs for rating data

---

## 10. Testing and Quality Assurance

### Testing Strategy
#### Unit Testing
- **Rating Factor Tests**: Individual factor calculation validation
- **Service Layer Tests**: Rating service business logic testing
- **Validation Tests**: Input validation and business rule testing

#### Integration Testing
- **API Integration**: Rating API endpoint testing
- **Database Integration**: Rating calculation storage and retrieval testing
- **Cache Integration**: Cache performance and consistency testing

#### Performance Testing
- **Load Testing**: High-volume rating calculation testing
- **Stress Testing**: System behavior under extreme rating loads
- **Endurance Testing**: Long-running rating operation stability

### Quality Metrics
- **Calculation Accuracy**: 99.9% accuracy for rating calculations
- **Performance Targets**: Sub-2-second individual rating calculations
- **Cache Efficiency**: >90% cache hit ratio for factor lookups
- **Error Rate**: <0.1% calculation errors in production

---

## 11. Deployment and Monitoring

### Deployment Strategy
- **Blue-Green Deployment**: Zero-downtime rating engine updates
- **Feature Flags**: Gradual rollout of rating enhancements
- **Database Migrations**: Safe schema updates with rollback capability

### Monitoring and Alerting
#### Performance Monitoring
- **Calculation Response Times**: Rating calculation performance metrics
- **Cache Performance**: Cache hit ratios and invalidation patterns
- **Database Performance**: Query performance and connection monitoring

#### Business Monitoring
- **Premium Calculation Volume**: Daily rating calculation metrics
- **Error Rates**: Rating calculation error tracking and alerting
- **Factor Usage**: Rating factor utilization and effectiveness metrics

#### Alerting Thresholds
- **Response Time**: >5 seconds for individual calculations
- **Error Rate**: >1% calculation errors
- **Cache Hit Rate**: <80% cache hit ratio

---

## 12. Future Enhancements and Roadmap

### Phase 1: Core Implementation (Current)
- Basic rating engine with all 34 factors
- Standard caching and performance optimization
- Basic audit trails and compliance features

### Phase 2: Advanced Features
- **Machine Learning Integration**: Predictive risk assessment
- **Real-Time Factor Updates**: Dynamic factor adjustment capability
- **Advanced Analytics**: Rating factor effectiveness analysis

### Phase 3: Platform Expansion
- **Multi-Program Support**: Rating engine for additional insurance programs
- **API Platform**: External rating API for partner integration
- **Regulatory Automation**: Automated rate filing and compliance reporting

---

## 13. Global Requirements Recommendations

### New Global Requirements Needed
Based on this rating infrastructure analysis, the following new Global Requirements should be created:

#### GR-65: Rating Engine Architecture
- Core rating calculation patterns and service architecture
- Factor management and versioning standards
- Premium calculation audit requirements
- Performance optimization for rating systems

#### GR-66: Insurance Risk Assessment Framework
- Risk factor validation and business rule patterns
- Underwriting guideline integration standards
- Territory and geographic rating standards
- Regulatory compliance for rating systems

#### GR-67: Rating Factor Management
- Factor table design and relationship patterns
- Factor versioning and effective date management
- Factor administration and approval workflows
- Historical factor data retention requirements

#### GR-68: Premium Calculation Standards
- Calculation methodology documentation requirements
- Audit trail and traceability standards
- Calculation validation and reasonableness checks
- Integration with billing and payment systems

### Integration with Existing Global Requirements
This rating infrastructure leverages and extends:
- **GR-20**: Service architecture patterns for rating services
- **GR-41**: Database schema standards for rating tables
- **GR-18**: Workflow integration for rating processes
- **GR-33**: Caching and performance optimization strategies

---

## Conclusion

This master plan provides a comprehensive foundation for implementing the Aguila Dorada Texas Personal Auto rating infrastructure. The design follows established Global Requirements patterns while providing the flexibility and performance needed for a sophisticated insurance rating system.

The implementation will create 34 individual factor plan files that detail the specific requirements for each rating component, ensuring complete coverage of the rating methodology while maintaining consistency with existing system architecture and Global Requirements standards.

Next steps involve creating detailed plan files for each of the 34 rate factors, defining the specific Global Requirements needed for rating infrastructure, and validating the approach with business stakeholders and technical teams.