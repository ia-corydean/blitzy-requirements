# IP269-New-Quote-Step-6-Quote-Review - Implementation Plan

## Requirement Overview

### Purpose
The Review Quote step consolidates all quote information into a single, editable summary to:
- Allow final review and minor corrections before submission
- Ensure accuracy across personal details, vehicles, drivers, coverage, and premiums
- Provide transparency into premium calculation
- Minimize errors and improve trust for binding success

### Scope
- Display all major data blocks from quote process
- Inline edit functionality for each section
- Premium summary with payment breakdown
- Applied discounts visibility
- Mobile-responsive collapsible sections

## Entity Analysis

### New Entities Required

1. **quote_summary_view** (View/Service Layer)
   - Aggregated quote data for display
   - Not a physical table, but service response

2. **quote_discount**
   - Applied discounts tracking
   - Multi-car, homeowner, etc.
   - Discount amount and type

3. **quote_section_completion**
   - Track completion status of each step
   - Enable/disable edit based on state

### Existing Entities Involved

- **quote**: Core quote data
- **driver**: All drivers with included/excluded status
- **vehicle**: Year, make, model, VIN
- **quote_coverage**: Selected coverages
- **quote_payment_schedule**: Payment breakdown
- **premium_calculation**: Total premium data
- **name**: Primary insured information

## Global Requirements Alignment

### Primary GRs
- **GR-09 (State Management)**: Maintain quote state during edits
- **GR-07 (Reusable Components)**: Summary display components
- **GR-18 (Workflow)**: Navigation between steps
- **GR-08 (Performance)**: Fast summary loading
- **GR-11 (Accessibility)**: Screen reader friendly

### Supporting GRs
- **GR-04 (Validation)**: Pre-submission validation
- **GR-13 (Error Handling)**: Edit navigation errors
- **GR-21 (Integration)**: Real-time premium updates
- **GR-40 (Seeding)**: Test data for all sections

## Database Schema Planning

### New Tables

1. **quote_discount**
   ```sql
   - id (PK)
   - quote_id (FK)
   - discount_type_id (FK)
   - discount_amount (decimal)
   - discount_percentage (decimal, nullable)
   - reason
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

2. **discount_type** (Reference)
   ```sql
   - id (PK)
   - code (unique)
   - name
   - description
   - calculation_type (percentage, fixed)
   - status_id (FK)
   - created_at, updated_at
   ```

3. **quote_section_completion**
   ```sql
   - id (PK)
   - quote_id (FK)
   - section_name
   - is_complete (boolean)
   - last_modified_at
   - status_id (FK)
   - created_by, updated_by, created_at, updated_at
   ```

### Views/Queries
- Aggregated quote summary query
- Driver list with tags
- Vehicle list with details
- Coverage summary by type
- Premium breakdown calculation

## API Endpoints

### Required Endpoints
```
GET    /api/v1/quotes/{quote_id}/summary
GET    /api/v1/quotes/{quote_id}/section-status
POST   /api/v1/quotes/{quote_id}/validate-completeness
GET    /api/v1/quotes/{quote_id}/premium-breakdown
GET    /api/v1/quotes/{quote_id}/applied-discounts
```

### Navigation Endpoints
```
POST   /api/v1/quotes/{quote_id}/navigate-to-section
GET    /api/v1/quotes/{quote_id}/edit-urls
```

### Real-time Updates
```javascript
private-quote.{quote_id}.section-updates
private-quote.{quote_id}.premium-changes
```

## Integration Points

### Internal Services
1. **QuoteSummaryService**
   - Aggregate data from all tables
   - Format for display
   - Calculate completeness

2. **NavigationService**
   - Generate edit URLs
   - Maintain state during navigation
   - Return to review functionality

3. **PremiumService**
   - Breakdown calculation
   - Discount application
   - Payment schedule display

### Cross-Step Dependencies
- All previous steps must persist data
- Edit navigation must preserve state
- Real-time updates on return from edit

## Implementation Considerations

### Key Patterns
1. **Lazy Loading Sections**
   - Load summary data progressively
   - Collapsible sections for performance
   - Cache summary data briefly

2. **Edit Navigation**
   - State preservation service
   - Return URL generation
   - Breadcrumb tracking

3. **Real-time Updates**
   - WebSocket for live changes
   - Optimistic UI updates
   - Change highlighting

### Technical Decisions
- Vue.js components for each section
- Vuex for state management during edits
- Service layer for data aggregation
- Redis for temporary state storage
- Component-based architecture

## Quality Checkpoints

### Pre-Implementation
- [ ] Review all quote step outputs
- [ ] Validate edit navigation patterns
- [ ] Check existing summary patterns
- [ ] Review GR-09 state management

### Implementation
- [ ] All sections display correctly
- [ ] Edit links maintain state
- [ ] Premium calculations accurate
- [ ] Mobile layout responsive

### Post-Implementation
- [ ] End-to-end edit flow testing
- [ ] Performance with full quotes
- [ ] Accessibility compliance
- [ ] Cross-browser testing

## Dependencies

### Upstream
- All quote steps (1-5) must be complete
- Data must be persisted properly
- Premium calculation complete

### Downstream
- Bind process depends on review
- Final validation before binding
- Quote-to-policy conversion

## Risk Mitigation

1. **Data Consistency**: Transaction wrapping
2. **Navigation Issues**: State preservation
3. **Performance**: Section lazy loading
4. **User Confusion**: Clear status indicators

## UI/UX Specifications

### Desktop Layout
- Left sidebar with step indicators
- Main content area with sections
- Sticky continue button

### Mobile Layout
- Stacked sections
- Collapsible accordions
- Sticky CTA at bottom
- Smooth scroll to section

### Visual Elements
- Green checkmarks for completed
- Edit icons for each section
- Premium prominently displayed
- Discount tags inline

## Next Steps

1. Create QuoteSummaryService
2. Build aggregation queries
3. Implement state preservation
4. Create Vue.js summary components
5. Build edit navigation system
6. Implement discount display
7. Add validation before continue