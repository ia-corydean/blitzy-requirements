# Accounting Global Requirements Generation - Initial Requirement

## Pre-Analysis Checklist
- [x] **Reviewed applicable Global Requirements**: GR-37 (Action Tracking), GR-41 (Table Schema), GR-44 (Communication Architecture), GR-52 (Universal Entity Management), GR-64 (Policy Reinstatement), GR-10 (SR22/SR26 Filing)
- [x] **Analyzed previous Accounting domain iterations**: Reviewed all output files (plan.md through plan4.md, accounting-infrastructure-support.md and updated version)
- [x] **Confirmed infrastructure compatibility**: Analyzed existing blitzy-requirements codebase patterns and service architecture
- [x] **Identified cross-domain dependencies**: ProducerPortal (policies, producers), ProgramManager (rate factors), EntityIntegration (DCS verification), Reinstatement (premium calculations), Sr22 (fee processing)
- [x] **Reviewed architectural decisions**: Double-entry accounting, program-centric configuration, database consolidation strategy, outage handling requirements

## Requirement Description

Generate comprehensive Global Requirements for complete accounting functionality across the insurance management platform, covering 9 new Global Requirements (GR-54 through GR-62) that integrate seamlessly with existing infrastructure while delivering:

### Core Accounting Capabilities
- **Complete double-entry accounting system** using enhanced transaction/transaction_line architecture
- **Premium and fee management** with reinstatement processing (GR-64) and SR22 fee integration (GR-10)
- **Payment gateway integration** with Paysafe including enhanced outage handling and manual payment entry
- **Billing and invoicing architecture** with automated communication workflows
- **Payment plan management** with installment processing and restructuring capabilities
- **Check printing and Positive Pay** (limited scope: Sunflower Bank integration only)
- **Financial reporting and analytics** with real-time KPI integration
- **Comprehensive compliance and audit** framework with complete action tracking

### Integration Requirements
- **Extend existing Transaction/Payment infrastructure** rather than creating parallel systems
- **Universal entity management integration** for all external services (Paysafe, Sunflower Bank)
- **Cross-domain entity consistency** with ProducerPortal policies, ProgramManager rate factors
- **Enhanced communication architecture** leveraging existing EmailService patterns
- **Complete action tracking integration** for audit compliance and regulatory requirements

## Entity Analysis

### Primary Accounting Entities (New)
- **Transaction** (Extended) - Enhanced with accounting-specific fields and transaction types
- **TransactionLine** (New) - Double-entry accounting detail lines with account classifications
- **PaymentPlan** (New) - Payment plan management with installment generation
- **Installment** (New) - Individual installment tracking with payment allocation
- **Commission** (New) - Producer commission calculations and payment processing
- **CheckRegister** (New) - Check printing and MICR encoding management
- **PositivePayExport** (New) - Daily Positive Pay file generation for Sunflower Bank
- **ManualPayment** (New) - Manual payment entry during gateway outages

### Cross-Domain Entity Dependencies
- **Policy** (ProducerPortal) - Core entity for all billing and premium calculations
- **Producer** (ProducerPortal) - Commission processing and payment relationships
- **Program** (ProgramManager) - Rate factor integration and program-specific rules
- **ReinstatementCalculation** (Reinstatement) - Premium recalculation and payment restructuring
- **SR22Filing** (Sr22) - Fee processing and billing integration
- **PaymentMethod** (Existing) - Payment processing and verification workflows

### External Integration Entities (Universal Entity Management)
- **PaysafeGateway** - Payment processing with outage detection and graceful degradation
- **SunflowerBank** - Positive Pay integration with NACHA file transmission
- **CheckPrintingService** - Check printing configuration and signature management

## Implementation Requirements

### Architecture Foundation (Based on Previous Decisions)
1. **Database Schema Extensions**
   - Extend existing `transaction` table with accounting-specific fields
   - Create `transaction_line` table for double-entry accounting details
   - Add accounting transaction types (REINSTATEMENT, SR22_FEE, COMMISSION, etc.)
   - Implement reinstatement_calculation table following GR-64 requirements
   - Create payment plan and installment management tables

2. **Service Layer Architecture**
   - **AccountingService** - Core accounting operations extending existing PaymentService
   - **TransactionService** - Double-entry transaction processing and validation
   - **PaymentPlanService** - Payment plan generation and installment management
   - **ReinstatementService** - Integration with GR-64 premium calculation requirements
   - **CommissionService** - Producer commission calculation and payment processing
   - **CheckPrintingService** - Check generation with signature and MICR management
   - **PositivePayService** - Limited scope Sunflower Bank integration
   - **ManualPaymentService** - Outage handling and manual payment entry

3. **API Endpoints (RESTful Extensions)**
   - Extend existing route patterns in `routes/api.php` and `routes/portal_api.php`
   - Comprehensive accounting endpoint groups following established conventions
   - Integration with existing authentication and authorization patterns

### Business Rules and Constraints (From Previous Analysis)
1. **Commission Processing**
   - **No commission clawbacks** - Commissions not recovered on mid-term cancellations
   - **Single producer per policy** - No multi-level commission splits
   - **Program-specific rates** - Default program rates with producer-specific overrides

2. **Payment Processing**
   - **Graceful degradation** during Paysafe outages with manual payment entry
   - **Customer communication** - Configurable per-program outage notifications
   - **Batch processing** - Manual payments validated and processed when service restored

3. **Check Processing**
   - **Limited scope** - Positive Pay integration with Sunflower Bank only
   - **Manual signatures** - Signature image storage for check printing
   - **NACHA compliance** - Daily file transmission with ACH processing

4. **Financial Periods**
   - **Month-end close** - 3 business days for premium reconciliation
   - **Year-end close** - 7 business days for annual reporting
   - **Audit lock** - Prevent changes to closed periods without special permissions

## Cross-Domain Dependencies

### ProducerPortal Integration
- **Policy Entity** - Core billing entity with premium calculations and payment plans
- **Producer Entity** - Commission processing and producer hierarchy management
- **Quote to Billing Workflow** - Automatic billing setup upon quote binding
- **Entity Relationship Management** - Consistent entity definitions across domains

### ProgramManager Integration
- **Rate Factor Integration** - Program-specific rate calculations for premium billing
- **Underwriting Rules** - Integration with rate calculation and commission structures
- **Program Configuration** - Program-centric business rule configuration

### EntityIntegration Dependencies
- **DCS Integration** - Payment verification and customer data validation
- **External API Management** - Universal entity management for payment gateways
- **Verification Workflows** - Payment method verification and fraud prevention

### Reinstatement Domain Integration (GR-64)
- **Premium Recalculation** - Daily rate methodology for lapse period adjustments
- **Payment Plan Restructuring** - Redistribution of remaining balance across payment periods
- **Reinstatement Fees** - State-specific fee calculations and billing integration

### Sr22 Domain Integration (GR-10)
- **Fee Management** - SR22 filing fees and cancellation processing fees
- **Billing Integration** - SR22 fees included in policy premium calculations
- **Compliance Tracking** - State-specific requirements and documentation

## Quality Validation Criteria

### Infrastructure Compatibility
- [x] **Existing Model Extensions** - Build on Transaction, Payment, PaymentMethod infrastructure
- [x] **Service Pattern Adherence** - Follow established service layer patterns and dependency injection
- [x] **API Convention Compliance** - RESTful endpoints following existing route organization
- [x] **Database Standards** - Schema extensions following GR-41 naming conventions and patterns

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

## Expected Processing Outcomes

### Multi-Agent Coordination Expected
1. **System Orchestrator** - Analyze cross-domain dependencies and coordinate multi-domain processing
2. **Accounting Domain Specialist** - Apply comprehensive accounting expertise and business rules
3. **ProducerPortal Domain Specialist** - Ensure policy and producer entity integration consistency
4. **ProgramManager Domain Specialist** - Validate rate factor and program configuration integration
5. **Universal Validator** - Comprehensive validation against all applicable Global Requirements

### Deliverable Expectations
- **9 Complete Global Requirements** (GR-54 through GR-62) with comprehensive technical specifications
- **Database Schema Documentation** - Complete migration scripts and table definitions
- **Service Architecture Documentation** - Service interfaces and integration patterns
- **API Specification** - Complete REST endpoint documentation with examples
- **Cross-Domain Integration Guide** - Entity mapping and workflow coordination documentation
- **Business Rules Documentation** - Complete business logic and constraint specifications
- **Implementation Plan** - Phased rollout strategy with testing and validation requirements

## Success Criteria

### Technical Success Criteria
- [ ] All accounting services extend existing infrastructure without duplication
- [ ] Database schema follows GR-41 standards with proper foreign key relationships
- [ ] API endpoints follow existing RESTful conventions and authentication patterns
- [ ] Service layer integrates with existing dependency injection and service patterns
- [ ] Universal entity management used for all external service integrations

### Functional Success Criteria  
- [ ] Double-entry accounting maintains balanced transactions with complete audit trail
- [ ] Reinstatement processing integrates seamlessly with GR-64 requirements
- [ ] SR22 fee processing integrates seamlessly with GR-10 requirements
- [ ] Payment processing includes enhanced outage handling and manual entry capabilities
- [ ] Commission processing follows established business rules (no clawbacks, single producer)
- [ ] Check printing and Positive Pay meet Sunflower Bank integration requirements

### Quality Assurance Criteria
- [ ] Complete action tracking integration provides regulatory compliance audit trail
- [ ] Cross-domain entity consistency maintained across all business domains
- [ ] Performance targets met for all financial operations and reporting
- [ ] Security and access control aligned with existing patterns and requirements
- [ ] Integration testing validates end-to-end workflows across all domains

This comprehensive requirement leverages all previous architectural decisions and analysis while utilizing the new multi-agent requirements generation system to produce high-quality, compliant, and integrated accounting global requirements.