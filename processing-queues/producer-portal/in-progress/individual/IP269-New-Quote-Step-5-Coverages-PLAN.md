# IP269-New-Quote-Step-5-Coverages - Implementation Plan

## Requirement Overview

### Purpose
The Coverage Selection step enables users to:
- Select insurance coverage options tailored to customer needs
- Ensure accurate premium generation
- Maintain compliance with underwriting rules and state mandates
- Provide flexibility in policy customization
- Enable clear comparisons across carrier programs

### Scope
- Policy-wide and per-vehicle coverage selection
- Limit and deductible configuration via dropdowns
- Optional coverage checkboxes
- Additional equipment coverage with type/value
- Real-time premium calculation
- Payment schedule configuration

## Entity Analysis

### New Entities Required

1. **coverage_type**
   - Reference table for coverage types
   - Bodily Injury, Property Damage, Medical Payments, PIP, etc.
   - Policy-level vs vehicle-level indicator

2. **coverage_limit_option**
   - Available limits per coverage type
   - State-specific variations
   - Program-specific options

3. **coverage_deductible_option**
   - Available deductibles per coverage type
   - Minimum requirements by state/program

4. **quote_coverage**
   - Selected coverages per quote
   - Links to coverage type and selected limits/deductibles
   - Premium impact tracking

5. **quote_vehicle_coverage**
   - Vehicle-specific coverage selections
   - Links quote, vehicle, and coverage

6. **additional_equipment**
   - Equipment type and value
   - Associated with vehicles

7. **payment_schedule_type**
   - Full pay, installments, etc.
   - Down payment percentage options

8. **quote_payment_schedule**
   - Selected payment configuration
   - Down payment amount
   - First installment date

### Existing Entities Involved

- **quote**: Parent entity for coverages
- **vehicle**: For vehicle-specific coverages
- **program**: Determines available coverages
- **state**: Coverage requirements
- **premium_calculation**: Real-time updates

## Global Requirements Alignment

### Primary GRs
- **GR-41 (Database Standards)**: Naming conventions and structure
- **GR-33 (Data Services)**: Premium calculation caching
- **GR-20 (Business Logic)**: Coverage validation rules
- **GR-08 (Performance)**: Real-time premium updates
- **GR-38 (Microservices)**: Rating service integration

### Supporting GRs
- **GR-04 (Validation)**: State mandate compliance
- **GR-19 (Relationships)**: Coverage-vehicle associations
- **GR-21 (Integration)**: Rating engine connectivity
- **GR-12 (Security)**: Premium calculation integrity

## Database Schema Planning

### Core Tables

1. **coverage_type**
   ```sql
   - id (PK)
   - code (unique)
   - name
   - description
   - scope (policy, vehicle)
   - display_order
   - is_optional (boolean)
   - status_id (FK)
   - created_at, updated_at
   ```

2. **quote_coverage**
   ```sql
   - id (PK)
   - quote_id (FK)
   - coverage_type_id (FK)
   - coverage_limit_option_id (FK)
   - coverage_deductible_option_id (FK, nullable)
   - is_selected (boolean)
   - premium_impact (decimal)
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

3. **quote_vehicle_coverage**
   ```sql
   - id (PK)
   - quote_id (FK)
   - vehicle_id (FK)
   - coverage_type_id (FK)
   - coverage_limit_option_id (FK)
   - coverage_deductible_option_id (FK, nullable)
   - is_selected (boolean)
   - premium_impact (decimal)
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

4. **additional_equipment**
   ```sql
   - id (PK)
   - vehicle_id (FK)
   - equipment_type
   - equipment_value (decimal)
   - description
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

5. **quote_payment_schedule**
   ```sql
   - id (PK)
   - quote_id (FK)
   - payment_schedule_type_id (FK)
   - down_payment_percentage (decimal)
   - down_payment_amount (decimal)
   - first_installment_date
   - installment_amount (decimal)
   - number_of_installments
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

### Map Tables

1. **map_program_coverage_type**
   - Links programs to available coverages
   - State-specific overrides

2. **map_coverage_limit_state**
   - State-specific limit requirements
   - Minimum coverage mandates

### Indexes
- quote_coverage: quote_id, coverage_type_id
- quote_vehicle_coverage: quote_id, vehicle_id, coverage_type_id
- Coverage options: program_id, state_code

## API Endpoints

### Required Endpoints
```
GET    /api/v1/quotes/{quote_id}/available-coverages
GET    /api/v1/programs/{program_id}/coverage-options
POST   /api/v1/quotes/{quote_id}/coverages
PUT    /api/v1/quotes/{quote_id}/coverages/{id}
POST   /api/v1/quotes/{quote_id}/calculate-premium
GET    /api/v1/quotes/{quote_id}/payment-schedules
POST   /api/v1/quotes/{quote_id}/payment-schedule
```

### Real-time Updates
```javascript
private-quote.{quote_id}.premium-updates
private-quote.{quote_id}.coverage-changes
```

## Integration Points

### Internal Services
1. **RatingService**
   - Real-time premium calculation
   - Coverage impact analysis
   - Discount application

2. **ProgramService**
   - Available coverage options
   - State-specific rules

3. **ValidationService**
   - Minimum coverage requirements
   - State mandate compliance

### External Services
- Rating engines via API (future GR-52 implementation)

## Implementation Considerations

### Key Patterns
1. **Dynamic Coverage Loading**
   - Cache coverage options by program/state
   - Progressive disclosure for optional coverages
   - Smart defaults based on state minimums

2. **Premium Calculation**
   - Debounced API calls on selection changes
   - Optimistic UI updates
   - Background recalculation queue

3. **Payment Schedule**
   - Dynamic installment calculation
   - Business rules for down payment
   - Date validation for first payment

### Technical Decisions
- Use Vue.js reactive components for real-time updates
- Implement CoverageService for business logic
- Redis caching for coverage options
- WebSocket for premium updates
- Database transactions for coverage selection

## Quality Checkpoints

### Pre-Implementation
- [ ] Review state coverage requirements
- [ ] Validate rating service integration
- [ ] Check existing coverage patterns
- [ ] Review GR-33 for caching strategies

### Implementation
- [ ] State mandate validation logic
- [ ] Premium calculation accuracy
- [ ] Performance with multiple vehicles
- [ ] Mobile-responsive dropdowns

### Post-Implementation
- [ ] Integration tests with rating service
- [ ] Load testing for concurrent updates
- [ ] Accuracy of payment calculations
- [ ] Cross-browser compatibility

## Dependencies

### Upstream
- Quote Step 4 (UW Questions) complete
- Vehicle information available
- Program configuration loaded

### Downstream
- Quote Review depends on selections
- Premium affects payment processing
- Policy binding requires coverage data

## Risk Mitigation

1. **Performance**: Aggressive caching of options
2. **Accuracy**: Validation against state rules
3. **User Experience**: Save selections automatically
4. **Compliance**: Audit trail for all changes

## Cross-Domain Considerations

- **Accounting**: Payment schedule affects billing
- **Rating**: Real-time integration required
- **Policy**: Coverage data flows to policy creation

## Next Steps

1. Create coverage type seed data
2. Build database migrations
3. Implement CoverageService
4. Create rating service integration
5. Build Vue.js coverage components
6. Implement payment schedule logic
7. Add comprehensive validation