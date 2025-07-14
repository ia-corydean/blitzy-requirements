# Accounting Global Requirements Generation - Initial Requirement (Version 3)

## Pre-Analysis Checklist
- [x] **Reviewed applicable Global Requirements**: GR-37 (Action Tracking), GR-41 (Table Schema), GR-44 (Communication Architecture), GR-52 (Universal Entity Management), GR-64 (Policy Reinstatement), GR-10 (SR22/SR26 Filing)
- [x] **Analyzed previous Accounting domain iterations**: Reviewed all output files (plan.md through plan4.md, accounting-infrastructure-support.md and updated version)
- [x] **Confirmed infrastructure compatibility**: Analyzed existing blitzy-requirements codebase patterns and service architecture
- [x] **Identified cross-domain dependencies**: ProducerPortal (policies, producers), ProgramManager (rate factors), EntityIntegration (external API patterns), Reinstatement (premium calculations), Sr22 (fee processing)
- [x] **Reviewed architectural decisions**: Double-entry accounting, program-centric configuration, database consolidation strategy, outage handling requirements
- [x] **Corrected service capability understanding**: DCS provides driver/vehicle/criminal data verification, NOT payment verification
- [x] **Analyzed ProgramManager requirements**: Comprehensive program configuration including payment plans, commission structures, and fee management

## Requirement Description

Generate comprehensive Global Requirements for complete accounting functionality across the insurance management platform, covering 9 new Global Requirements (GR-54 through GR-62) that integrate seamlessly with existing infrastructure while delivering:

### Core Accounting Capabilities
- **Complete double-entry accounting system** using enhanced transaction/transaction_line architecture
- **Premium and fee management** with reinstatement processing (GR-64) and SR22 fee integration (GR-10)
- **Payment gateway integration** with Paysafe including enhanced outage handling and manual payment entry
- **Billing and invoicing architecture** with automated communication workflows
- **Payment plan management** synchronized with ProgramManager configurations
- **Check printing and Positive Pay** (limited scope: Sunflower Bank integration only)
- **Financial reporting and analytics** with real-time KPI integration
- **Comprehensive compliance and audit** framework with complete action tracking
- **Commission processing** aligned with ProgramManager's commission structures

### Integration Requirements
- **Extend existing Transaction/Payment infrastructure** rather than creating parallel systems
- **Universal entity management integration** for all external services (Paysafe, Sunflower Bank)
- **Cross-domain entity consistency** with ProducerPortal policies, ProgramManager configurations
- **Enhanced communication architecture** leveraging existing EmailService patterns
- **Complete action tracking integration** for audit compliance and regulatory requirements
- **Bidirectional synchronization** with ProgramManager for payment plans, fees, and commissions

## Entity Analysis

### Primary Accounting Entities (New/Enhanced)
- **Transaction** (Extended) - Enhanced with accounting-specific fields and transaction types
- **TransactionLine** (New) - Double-entry accounting detail lines with account classifications
- **PaymentPlan** (Enhanced) - Synchronized with ProgramManager payment configurations
- **Installment** (Enhanced) - Individual installment tracking with program-specific fee calculations
- **Commission** (Enhanced) - Producer commission calculations using ProgramManager structures
- **CheckRegister** (New) - Check printing and MICR encoding management
- **PositivePayExport** (New) - Daily Positive Pay file generation for Sunflower Bank
- **ManualPayment** (New) - Manual payment entry during gateway outages
- **FeeSchedule** (New) - Local representation of ProgramManager fee configurations
- **CommissionSchedule** (New) - Local representation of ProgramManager commission structures

### Cross-Domain Entity Dependencies
- **Policy** (ProducerPortal) - Core entity for all billing and premium calculations
- **Producer** (ProducerPortal) - Commission processing and payment relationships
- **Program** (ProgramManager) - Master source for rate factors, payment plans, fees, and commissions
- **ProgramPaymentPlan** (ProgramManager) - Payment plan configurations including installment structures
- **ProgramCommissionStructure** (ProgramManager) - Commission rates and calculation rules
- **ProgramFeeConfiguration** (ProgramManager) - All fee types and calculation formulas
- **ReinstatementCalculation** (Reinstatement) - Premium recalculation and payment restructuring
- **SR22Filing** (Sr22) - Fee processing and billing integration
- **PaymentMethod** (Existing) - Payment processing and verification workflows

### External Integration Entities (Universal Entity Management)
- **PaysafeGateway** - Payment processing with outage detection and graceful degradation
- **SunflowerBank** - Positive Pay integration with NACHA file transmission
- **CheckPrintingService** - Check printing configuration and signature management
- **PaymentVerificationService** - Payment method verification and fraud prevention

## Implementation Requirements

### Architecture Foundation (Based on Previous Decisions + ProgramManager Integration)
1. **Database Schema Extensions**
   - Extend existing `transaction` table with accounting-specific fields
   - Create `transaction_line` table for double-entry accounting details
   - Add accounting transaction types (REINSTATEMENT, SR22_FEE, COMMISSION, INSTALLMENT_FEE, NSF_FEE, etc.)
   - Implement reinstatement_calculation table following GR-64 requirements
   - Create payment plan and installment management tables with program_id references
   - Add fee_schedule and commission_schedule tables for local caching of ProgramManager data
   - Create synchronization tracking tables for ProgramManager updates

2. **Service Layer Architecture**
   - **AccountingService** - Core accounting operations extending existing PaymentService
   - **TransactionService** - Double-entry transaction processing and validation
   - **PaymentPlanService** - Payment plan management synchronized with ProgramManager
   - **InstallmentFeeService** - Calculate installment fees using ProgramManager formulas
   - **ReinstatementService** - Integration with GR-64 premium calculation requirements
   - **CommissionService** - Producer commission calculation using ProgramManager structures
   - **CheckPrintingService** - Check generation with signature and MICR management
   - **PositivePayService** - Limited scope Sunflower Bank integration
   - **ManualPaymentService** - Outage handling and manual payment entry
   - **PaymentVerificationService** - Payment method verification and fraud prevention
   - **ProgramSyncService** - Synchronize payment plans, fees, and commissions from ProgramManager

3. **API Endpoints (RESTful Extensions)**
   - Extend existing route patterns in `routes/api.php` and `routes/portal_api.php`
   - Comprehensive accounting endpoint groups following established conventions
   - Integration with existing authentication and authorization patterns
   - New endpoints for ProgramManager synchronization status and configuration viewing

### Business Rules and Constraints (Enhanced with ProgramManager Analysis)
1. **Commission Processing**
   - **No commission clawbacks** - Commissions not recovered on mid-term cancellations
   - **Single producer per policy** - No multi-level commission splits
   - **Program-specific rates** - Use ProgramManager's commission structures
   - **Calculation basis** - Support Collected, Earned, or Written basis per program
   - **New Business vs Renewal** - Different rates configured in ProgramManager
   - **Term-specific rates** - Support different rates for 6-month vs 12-month policies

2. **Payment Processing**
   - **Graceful degradation** during Paysafe outages with manual payment entry
   - **Customer communication** - Configurable per-program outage notifications
   - **Batch processing** - Manual payments validated and processed when service restored
   - **Payment verification** - Handled by Paysafe verification APIs, NOT DCS
   - **Payment plan synchronization** - Use ProgramManager's payment plan configurations
   - **Down payment calculation** - Apply ProgramManager's down payment percentages
   - **EFT discounts** - Apply ProgramManager's EFT enhancement factors

3. **Fee Management (Synchronized with ProgramManager)**
   - **Installment fees** - Use ProgramManager's threshold/increment formula
   - **NSF fees** - Apply ProgramManager's fixed NSF fee amounts
   - **Late payment fees** - Apply ProgramManager's late fee configuration
   - **SR-22 fees** - Use ProgramManager's SR-22 fee amounts
   - **MGA fees** - Per-policy fees from ProgramManager
   - **MVCPA fees** - Per-vehicle fees from ProgramManager
   - **Convenience fees** - Transaction-type specific fees

4. **Check Processing**
   - **Limited scope** - Positive Pay integration with Sunflower Bank only
   - **Manual signatures** - Signature image storage for check printing
   - **NACHA compliance** - Daily file transmission with ACH processing

5. **Financial Periods**
   - **Month-end close** - 3 business days for premium reconciliation
   - **Year-end close** - 7 business days for annual reporting
   - **Audit lock** - Prevent changes to closed periods without special permissions

## Cross-Domain Dependencies (Enhanced)

### ProgramManager Integration (Critical)
- **Payment Plan Configuration**
  - Retrieve installment structures from ProgramManager
  - Apply down payment percentages and installment counts
  - Calculate installment fees using ProgramManager formulas
  - Support multiple payment plan options per program
  
- **Commission Structure Integration**
  - Synchronize commission rates for new business and renewals
  - Apply term-specific commission rates
  - Support different calculation bases (Collected/Earned/Written)
  - Handle default rate selection logic

- **Fee Configuration Integration**
  - Cache all fee types and amounts from ProgramManager
  - Apply fee calculation formulas (e.g., installment fee formula)
  - Support program-specific fee variations
  - Track fee version changes for audit purposes

- **Integration Patterns**
  - Event-driven synchronization when programs are published
  - Periodic reconciliation to ensure data consistency
  - Fallback to cached values if ProgramManager unavailable
  - Version tracking for configuration changes

### ProducerPortal Integration
- **Policy Entity** - Core billing entity with premium calculations and payment plans
- **Producer Entity** - Commission processing and producer hierarchy management
- **Quote to Billing Workflow** - Automatic billing setup upon quote binding
- **Entity Relationship Management** - Consistent entity definitions across domains

### EntityIntegration Dependencies
- **Payment Method Verification** - Customer identity validation and fraud prevention through payment gateways
- **External API Management** - Universal entity management patterns for all external integrations
- **Verification Workflows** - Payment method verification using Paysafe APIs
- **Bank Account Validation** - ACH payment verification through banking APIs

Note: DCS integration (driver/vehicle/criminal data) is NOT used for payment verification - that capability is provided by payment gateway APIs and banking integrations.

### Reinstatement Domain Integration (GR-64)
- **Premium Recalculation** - Daily rate methodology for lapse period adjustments
- **Payment Plan Restructuring** - Redistribution of remaining balance across payment periods
- **Reinstatement Fees** - State-specific fee calculations and billing integration

### Sr22 Domain Integration (GR-10)
- **Fee Management** - SR22 filing fees and cancellation processing fees
- **Billing Integration** - SR22 fees included in policy premium calculations
- **Compliance Tracking** - State-specific requirements and documentation

## Areas Requiring Additional Context

### 1. Configuration Source of Truth
- **Question**: When ProgramManager and local accounting configurations conflict, which takes precedence?
- **Consideration**: Need clear rules for override scenarios and emergency configurations
- **Impact**: Affects system design for configuration management and synchronization
  - The accoutning infrastructure should support all transactions based off of the results the policy / quote / ensdorsement was rated against.

### 2. Real-time vs Batch Synchronization
- **Question**: Should ProgramManager changes reflect immediately in accounting or through batch processes?
- **Consideration**: Real-time provides consistency but may impact performance
- **Impact**: Affects integration architecture and user experience
  - The accounting infrastructure should support the financial aspect of all program manager changes.
  - The accounting infrastructure is a foundation for the program manager to lay on top of.
  - Our accounting infradtrucutre should be flexible enough to support changes in program manager and reflect those changes when policies and quotes are rated against it.

### 3. Historical Rate Preservation
- **Question**: How should accounting handle rate/fee changes for existing policies?
- **Consideration**: Policies may need to maintain original rates despite program updates
- **Impact**: Affects data model for storing point-in-time configurations
  - Rate changes are scheduled for future polciies and renewals and existing policies are locked into the terms that were agreed upon when binding.

### 4. Commission Override Authority
- **Question**: Can individual producer agreements override ProgramManager commission structures?
- **Consideration**: Business may require producer-specific commission deals
- **Impact**: Affects commission calculation hierarchy and data model
  - Possible. TBD.

### 5. Fee Waiver Management
- **Question**: How should the system handle fee waivers or adjustments?
- **Consideration**: Customer service may need to waive NSF or late fees
- **Impact**: Affects transaction types and approval workflows
  - This will be handled the Underwriting Part of the system.
  - More info to come. TBD.

### 6. Multi-Program Accounting
- **Question**: How should accounting handle producers selling multiple programs?
- **Consideration**: Different programs may have conflicting fee structures
- **Impact**: Affects account segregation and reporting structures
  - The program dtermines the rating characterisics and how we formulate the premium owed.
  - Accounting stores the results of those in an organized way so regardless of the program, the accounting infrasctructer is consistent.

## Quality Validation Criteria (Enhanced)

### Infrastructure Compatibility
- [x] **Existing Model Extensions** - Build on Transaction, Payment, PaymentMethod infrastructure
- [x] **Service Pattern Adherence** - Follow established service layer patterns and dependency injection
- [x] **API Convention Compliance** - RESTful endpoints following existing route organization
- [x] **Database Standards** - Schema extensions following GR-41 naming conventions and patterns
- [x] **ProgramManager Integration** - Proper synchronization patterns and event handling

### Global Requirements Compliance
- [x] **GR-52 Integration** - Universal entity management for all external integrations
- [x] **GR-44 Integration** - Communication architecture for billing and outage notifications  
- [x] **GR-41 Compliance** - Database schema standards and audit field requirements
- [x] **GR-37 Integration** - Complete action tracking for all financial operations
- [x] **GR-64 Integration** - Reinstatement premium calculation and workflow requirements
- [x] **GR-10 Integration** - SR22 fee processing and compliance requirements

### Cross-Domain Validation
- [x] **Entity Consistency** - Shared entity definitions across ProducerPortal, ProgramManager domains
- [x] **Workflow Integration** - Seamless integration with existing policy and producer workflows
- [x] **Performance Standards** - Meet established performance targets for financial operations
- [x] **Security Compliance** - Integration with existing authentication and authorization patterns
- [x] **Configuration Synchronization** - Reliable sync with ProgramManager configurations

## Expected Processing Outcomes

### Multi-Agent Coordination Expected
1. **System Orchestrator** - Analyze cross-domain dependencies and coordinate multi-domain processing
2. **Accounting Domain Specialist** - Apply comprehensive accounting expertise and business rules
3. **ProducerPortal Domain Specialist** - Ensure policy and producer entity integration consistency
4. **ProgramManager Domain Specialist** - Validate configuration synchronization and usage patterns
5. **Universal Validator** - Comprehensive validation against all applicable Global Requirements

### Deliverable Expectations
- **9 Complete Global Requirements** (GR-54 through GR-62) with comprehensive technical specifications
- **Database Schema Documentation** - Complete migration scripts and table definitions
- **Service Architecture Documentation** - Service interfaces and integration patterns
- **API Specification** - Complete REST endpoint documentation with examples
- **Cross-Domain Integration Guide** - Entity mapping and workflow coordination documentation
- **Business Rules Documentation** - Complete business logic and constraint specifications
- **ProgramManager Sync Guide** - Configuration synchronization patterns and processes
- **Implementation Plan** - Phased rollout strategy with testing and validation requirements

## Success Criteria

### Technical Success Criteria
- [ ] All accounting services extend existing infrastructure without duplication
- [ ] Database schema follows GR-41 standards with proper foreign key relationships
- [ ] API endpoints follow existing RESTful conventions and authentication patterns
- [ ] Service layer integrates with existing dependency injection and service patterns
- [ ] Universal entity management used for all external service integrations
- [ ] ProgramManager synchronization maintains data consistency and version tracking

### Functional Success Criteria  
- [ ] Double-entry accounting maintains balanced transactions with complete audit trail
- [ ] Reinstatement processing integrates seamlessly with GR-64 requirements
- [ ] SR22 fee processing integrates seamlessly with GR-10 requirements
- [ ] Payment processing includes enhanced outage handling and manual entry capabilities
- [ ] Commission processing uses ProgramManager structures with proper calculations
- [ ] Check printing and Positive Pay meet Sunflower Bank integration requirements
- [ ] Payment verification correctly uses Paysafe APIs, not DCS services
- [ ] Fee calculations match ProgramManager configurations exactly
- [ ] Payment plans generate correct installment schedules from ProgramManager data

### Quality Assurance Criteria
- [ ] Complete action tracking integration provides regulatory compliance audit trail
- [ ] Cross-domain entity consistency maintained across all business domains
- [ ] Performance targets met for all financial operations and reporting
- [ ] Security and access control aligned with existing patterns and requirements
- [ ] Integration testing validates end-to-end workflows across all domains
- [ ] External service capabilities correctly understood and documented
- [ ] ProgramManager configuration changes properly reflected in accounting

## Revision Notes

### Version 3 Changes
- **Added ProgramManager Integration Analysis**: Comprehensive review of payment plans, commission structures, and fee configurations
- **Enhanced Entity Model**: Added FeeSchedule and CommissionSchedule entities for local caching
- **Expanded Business Rules**: Incorporated ProgramManager's specific calculation formulas and structures
- **Added Synchronization Requirements**: Defined patterns for keeping accounting aligned with ProgramManager
- **Identified Integration Complexities**: Listed specific areas needing clarification for proper implementation
- **Enhanced Cross-Domain Dependencies**: Detailed the bidirectional relationship with ProgramManager
- **Added Configuration Management**: Addressed the need for version tracking and point-in-time configurations

### Key Integration Insights from ProgramManager
1. **Payment Plan Complexity**: ProgramManager defines detailed installment structures that accounting must honor
2. **Fee Calculation Formulas**: Specific formulas for installment fees that must be implemented consistently
3. **Commission Flexibility**: Support for multiple calculation bases and term-specific rates
4. **Configuration Versioning**: Need to track configuration changes for audit and historical accuracy
5. **Program-Centric Design**: All accounting configurations flow from program definitions

This comprehensive requirement leverages all previous architectural decisions and analysis while incorporating deep integration with ProgramManager's configuration capabilities to produce high-quality, compliant, and integrated accounting global requirements with corrected understanding of external service capabilities and enhanced program-driven configuration management.