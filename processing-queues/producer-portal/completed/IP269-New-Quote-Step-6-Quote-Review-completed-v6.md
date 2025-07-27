# IP269-New-Quote-Step-6-Quote-Review - Complete Requirement

## **A) WHY – Vision and Purpose**

The Quote Review step serves as a critical final verification checkpoint before policy binding, consolidating all quote information into a comprehensive, editable summary. This transparency builds trust by showing exactly what coverage is being purchased, at what cost, and with what discounts applied.

The purpose is to:
- Ensure accuracy across all quote components before submission
- Provide transparent premium calculations with discount visibility
- Allow quick corrections without losing entered data
- Minimize binding errors through comprehensive review
- Build user confidence with clear price breakdowns

By presenting all quote details in an organized, reviewable format with easy edit access, the system reduces costly post-bind corrections and improves the overall quote-to-bind conversion rate.

---

## **B) WHAT – Core Requirements**

### **1. Summary Sections Display**

All major data blocks from the quote process must be displayed clearly:

- **Primary Insured Information**:
  - Full name and contact details
  - Mailing and garaging addresses
  - Email and phone numbers
  - License information
  - Date of birth

- **Drivers Section**:
  - All drivers with included/excluded status tags
  - Key details: name, age, license status
  - Relationship to primary insured
  - Driver count summary

- **Vehicles Section**:
  - Year, Make, Model, VIN display
  - Usage type and annual mileage
  - Garaging address
  - Vehicle count summary

- **Coverage Details**:
  - Policy-wide coverages (BI/PD limits)
  - Per-vehicle coverages (Comprehensive/Collision)
  - Deductibles and limits clearly shown
  - Premium for each coverage line

- **Applied Discounts**:
  - List of all applicable discounts
  - Discount amounts or percentages
  - Multi-car, homeowner, good driver, etc.
  - Total discount amount

- **Premium Summary**:
  - Base premium breakdown
  - Total fees itemized
  - Discount total
  - Final premium amount
  - Payment schedule options

### **2. Edit Functionality**

Each major section must have inline "Edit" links that:
- Navigate directly to the specific quote step
- Preserve all existing quote data
- Return to review page after edits
- Maintain quote state throughout navigation
- Show visual indicators for edited sections

### **3. Premium Calculation Display**

Clear presentation of pricing including:
- **Total Premium** (Full term - 6 or 12 months)
- **Policy Fees** (separated from premium)
- **Installment Fees** (if applicable)
- **Down Payment Amount**
- **Monthly Payment** (for installment plans)

### **4. Business Rules & Validation**

- All required sections must be complete before binding
- Premium calculations must match rating engine
- Discount eligibility verified in real-time
- Edit navigation preserves all data
- Warning for any pending underwriting issues
- Validation of all coverage minimums

### **5. Save & Navigation**

- Auto-save any review page interactions
- Enable "Continue to Bind" when valid
- Back navigation returns to Coverage step
- Session timeout warnings displayed
- Progress indicator shows review as final step

---

## Entity Analysis

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|-------|
| quote | Core | Existing | Base quote with premium totals |
| driver | Core | Existing | All drivers including primary insured |
| vehicle | Core | Existing | All vehicles with details |
| coverage | Core | Existing | Selected coverages and limits |
| discount | Core | Existing | Applied discounts with amounts |
| fee | Supporting | Existing | Policy and installment fees |
| payment_plan | Reference | Existing | Payment schedule options |
| name | Supporting | Existing | Driver name details |
| address | Supporting | Existing | Mailing and garaging addresses |
| license | Supporting | Existing | Driver license information |
| map_quote_driver | Map | Existing | Links drivers to quote |
| map_quote_vehicle | Map | Existing | Links vehicles to quote |
| map_quote_coverage | Map | Existing | Links coverages to quote |
| map_vehicle_coverage | Map | Existing | Links coverages to vehicles |

### Coverage Mapping Architecture
The system uses consistent mapping patterns:
- **map_quote_coverage** links coverages to quotes (policy-level)
- **map_policy_coverage** links coverages to policies
- **map_vehicle_coverage** links coverages to vehicles
- This creates uniform relationships across all entities

### Relationships Identified
- quote → has many → drivers (via map_quote_driver)
- quote → has many → vehicles (via map_quote_vehicle)
- quote → has many → coverages (via map_quote_coverage)
- vehicle → has many → coverages (via map_vehicle_coverage)
- quote → has many → discounts
- driver → has one → name
- driver → has one → license
- quote → has many → addresses
- coverage → belongs to → coverage_type
- discount → belongs to → discount_type

---

## Field Mappings (Section C)

### Backend Mappings

#### Primary Insured Section

##### Display Primary Insured
- **Backend Mapping**: 
  ```
  get quote.id from quote
  -> get primary driver from map_quote_driver 
     where is_primary_insured = true
  -> get name from driver.name_id
  -> get license from driver.license_id
  -> get addresses from quote addresses
  -> return consolidated primary insured data
  ```

#### Drivers Section

##### List All Drivers
- **Backend Mapping**: 
  ```
  get quote.id from quote
  -> get all drivers from map_quote_driver
  -> for each driver:
     - get name details
     - get license status
     - check is_included flag
     - calculate age from DOB
  -> return driver list with status tags
  ```

#### Vehicles Section

##### Display Vehicles
- **Backend Mapping**: 
  ```
  get quote.id from quote
  -> get all vehicles from map_quote_vehicle
  -> for each vehicle:
     - format year/make/model
     - get VIN details
     - get usage type
     - get garaging address
  -> return vehicle summary list
  ```

#### Coverage Section

##### Show All Coverages
- **Backend Mapping**: 
  ```
  get quote.id from quote
  -> get policy-level coverages from map_quote_coverage
     where coverage has no vehicle association
  -> get vehicle-specific coverages:
     - from map_vehicle_coverage
     - join with vehicle details
  -> join all coverages with coverage_type
  -> get limit and deductible values
  -> group vehicle coverages by vehicle
  -> return organized coverage display
  ```

##### Policy-Level Coverage Query
```sql
-- Get policy-level coverages
SELECT c.*, ct.name, l.name as limit_name
FROM map_quote_coverage mqc
JOIN coverage c ON mqc.coverage_id = c.id
JOIN coverage_type ct ON c.coverage_type_id = ct.id
LEFT JOIN limit l ON c.limit_id = l.id
WHERE mqc.quote_id = ? 
AND c.id NOT IN (
    SELECT coverage_id FROM map_vehicle_coverage
);
```

##### Vehicle-Specific Coverage Query
```sql
-- Get vehicle-specific coverages using map table
SELECT 
    c.*, 
    ct.name as coverage_type_name,
    v.year, v.make, v.model,
    d.amount as deductible_amount
FROM map_vehicle_coverage mvc
JOIN coverage c ON mvc.coverage_id = c.id
JOIN vehicle v ON mvc.vehicle_id = v.id
JOIN map_quote_vehicle mqv ON mqv.vehicle_id = v.id
JOIN coverage_type ct ON c.coverage_type_id = ct.id
LEFT JOIN deductible d ON c.deductible_id = d.id
WHERE mqv.quote_id = ?
ORDER BY v.id, ct.display_order;
```

#### Discounts & Premium

##### Calculate Premium Summary
- **Backend Mapping**: 
  ```
  get quote.total_premium from quote
  -> get all discounts for quote
  -> sum discount amounts
  -> get fees from fee table
  -> get payment_plan details
  -> calculate:
     - down payment
     - installment amounts
     - payment schedule
  -> return complete premium breakdown
  ```

### Implementation Architecture

The quote review system leverages existing data relationships to build a comprehensive view:

1. **Aggregation Service**: Loads all quote-related data efficiently
2. **Navigation Manager**: Handles edit links with state preservation
3. **Display Components**: Organized sections for each data type
4. **Coverage Organizer**: Uses consistent mapping for all coverage types
5. **Premium Calculator**: Ensures consistency with rating engine
6. **Responsive Framework**: Mobile-optimized collapsible sections

### Integration Specifications

**Quote State Management**:
- Session-based state preservation
- Navigation context maintained
- Edit return handling

**Coverage Display**:
- Policy-level coverages shown first
- Vehicle-specific coverages grouped by vehicle
- Consistent data retrieval via map tables
- Clear visual separation between coverage types

**Premium Verification**:
- Real-time discount validation
- Fee calculation consistency
- Payment plan integration

**Mobile Optimization**:
- Progressive enhancement
- Touch-friendly edit buttons
- Collapsible section management

---

## **D) User Experience (UX) & Flows**

### **1. Entry Flow**

1. User completes Coverage Selection (Step 5)
2. System loads all quote data
3. Review page displays with all sections
4. Green checkmarks show completed steps
5. Premium calculation shown at bottom

### **2. Review Flow**

1. User reviews each section sequentially
2. Sections can be expanded/collapsed
3. Edit links visible for each section
4. Hovering shows what step to edit
5. Coverage section shows clear separation of policy vs vehicle coverages
6. Premium updates reflect any changes

### **3. Edit Navigation Flow**

1. User clicks Edit on a section
2. System preserves current state
3. Navigation to specific step
4. User makes changes
5. Return to review with updates
6. Premium recalculates if needed

### **4. Mobile Experience**

1. Sections stack vertically
2. Tap to expand section details
3. Edit buttons remain accessible
4. Premium summary sticky at bottom
5. Continue button always visible

### **5. Submission Flow**

1. User reviews all information
2. Clicks "Continue to Bind"
3. Final validation performed
4. Any issues highlighted
5. Navigation to binding process

### **6. UI Presentation Guidelines**

- Card-based layout for each section
- Clear section headers with edit links
- Included/excluded tags for drivers
- Coverage limits in readable format
- Vehicle coverages clearly associated with vehicles
- Discount chips showing savings
- Premium in large, clear font
- Mobile breakpoints at 768px
- Accessibility with ARIA labels
- Keyboard navigation support
- Print-friendly view option

---

## API Specifications

### Endpoints Required
```http
GET    /api/v1/quotes/{id}/review           # Complete quote summary
GET    /api/v1/quotes/{id}/premium-summary  # Detailed premium breakdown
POST   /api/v1/quotes/{id}/validate-review  # Pre-bind validation
GET    /api/v1/quotes/{id}/discounts        # Applied discount details
GET    /api/v1/quotes/{id}/coverages        # All coverages with consistent mapping
```

### Coverage Response Format
```json
{
  "policy_coverages": [
    {
      "coverage_id": 1,
      "coverage_type": "BI",
      "limit": "100/300",
      "premium": 450.00
    },
    {
      "coverage_id": 2,
      "coverage_type": "PD",
      "limit": "50000",
      "premium": 200.00
    }
  ],
  "vehicle_coverages": [
    {
      "vehicle_id": 123,
      "vehicle": "2020 Honda Accord",
      "coverages": [
        {
          "coverage_id": 3,
          "coverage_type": "COMP",
          "deductible": 500,
          "premium": 150.00
        },
        {
          "coverage_id": 4,
          "coverage_type": "COLL",
          "deductible": 500,
          "premium": 300.00
        }
      ]
    }
  ]
}
```

### Real-time Updates
```javascript
// WebSocket channels for live updates
private-quote.{quote_id}.review    # Premium updates during edits
```

---

## Database Schema (Section E)

### Core Tables Used

#### quote
```sql
-- Existing comprehensive quote table
-- Key columns for review:
-- id, quote_number, effective_date, expiration_date
-- total_premium, total_fees, total_discount
-- down_payment, payment_plan_id
-- program_id, status_id
-- created_at, updated_at
```

#### driver
```sql
-- All driver information including primary insured
-- Key columns:
-- id, name_id, license_id
-- date_of_birth, gender
-- marital_status_id, relationship_id
-- is_excluded, is_primary_insured
```

#### vehicle
```sql
-- Vehicle details for display
-- Key columns:
-- id, year, make, model, vin
-- usage_type_id, annual_mileage
-- garaging_address_id
```

#### coverage
```sql
-- Selected coverage details
-- Key columns:
-- id, coverage_type_id
-- limit_id, deductible_id
-- premium_amount
-- is_rejected, rejection_reason
```

#### discount
```sql
-- Applied discounts with calculations
-- Key columns:
-- id, discount_type_id, quote_id
-- discount_amount, discount_percentage
-- eligibility_status, applied_date
```

### Relationship Tables

#### map_quote_driver
```sql
-- Links drivers to quotes
-- Includes is_included flag for display
```

#### map_quote_vehicle  
```sql
-- Links vehicles to quotes
-- Maintains vehicle order
```

#### map_quote_coverage
```sql
-- Links coverages to quotes
-- Used for policy-level coverages
```

#### map_vehicle_coverage
```sql
-- Links coverages to vehicles
-- Used for vehicle-specific coverages
```

### Reference Tables

All existing reference tables provide lookup values:
- coverage_type (BI, PD, COMP, COLL, etc.)
- limit (coverage limit options)
- deductible (deductible amounts)
- discount_type (Multi-car, Homeowner, etc.)
- payment_plan (Full pay, Monthly, etc.)
- vehicle_use (Commute, Pleasure, Business)

### Query Examples

#### Get All Coverages with Consistent Mapping
```sql
-- Combined query for all coverages using map tables
WITH policy_coverages AS (
    SELECT 
        c.id,
        c.coverage_type_id,
        c.limit_id,
        c.deductible_id,
        c.premium_amount,
        ct.name as coverage_type_name,
        ct.code as coverage_type_code,
        l.name as limit_name,
        NULL as vehicle_id,
        'Policy-Level' as coverage_scope
    FROM map_quote_coverage mqc
    JOIN coverage c ON mqc.coverage_id = c.id
    JOIN coverage_type ct ON c.coverage_type_id = ct.id
    LEFT JOIN limit l ON c.limit_id = l.id
    WHERE mqc.quote_id = ?
    AND c.id NOT IN (SELECT coverage_id FROM map_vehicle_coverage)
),
vehicle_coverages AS (
    SELECT 
        c.id,
        c.coverage_type_id,
        c.limit_id,
        c.deductible_id,
        c.premium_amount,
        ct.name as coverage_type_name,
        ct.code as coverage_type_code,
        d.amount as deductible_amount,
        v.id as vehicle_id,
        CONCAT(v.year, ' ', v.make, ' ', v.model) as coverage_scope
    FROM map_vehicle_coverage mvc
    JOIN coverage c ON mvc.coverage_id = c.id
    JOIN vehicle v ON mvc.vehicle_id = v.id
    JOIN map_quote_vehicle mqv ON mqv.vehicle_id = v.id
    JOIN coverage_type ct ON c.coverage_type_id = ct.id
    LEFT JOIN deductible d ON c.deductible_id = d.id
    WHERE mqv.quote_id = ?
)
SELECT * FROM policy_coverages
UNION ALL
SELECT * FROM vehicle_coverages
ORDER BY vehicle_id NULLS FIRST, coverage_type_code;
```

---

## Implementation Notes

### Dependencies
- All previous quote steps must be complete
- Premium calculation engine must be current
- Discount eligibility rules must be defined
- Payment plan configuration required

### Performance Considerations
- Eager load all relationships for display
- Cache quote data during review session
- Optimize coverage queries with proper joins
- Index on map tables for fast lookups
- Consider pagination for many vehicles/drivers
- Preload reference data for dropdowns

### Architecture Benefits
- **Consistency**: All entity-coverage relationships use map tables
- **Flexibility**: Easier to manage vehicle-coverage relationships
- **Scalability**: Better performance with proper indexing
- **Maintainability**: Cleaner separation of concerns
- **Future-Proof**: Easier to add new mapping requirements

---

## Quality Checklist

### Pre-Implementation
- [x] All UI fields mapped to existing columns
- [x] Coverage mapping approach standardized
- [x] Map table pattern consistently applied
- [x] All entities reused from existing system
- [x] Relationships support all display needs
- [x] Navigation patterns established

### Post-Implementation
- [ ] All sections load correctly
- [ ] Edit navigation preserves state
- [ ] Premium calculations accurate
- [ ] Discounts display properly
- [ ] Coverages properly mapped via tables
- [ ] Vehicle coverages grouped correctly
- [ ] Mobile layout responsive
- [ ] Performance acceptable

### Final Validation
- [ ] Complete quote data displayed
- [ ] All edit links functional
- [ ] Premium breakdown clear
- [ ] Coverage organization consistent
- [ ] Continue to bind enabled appropriately
- [ ] No data loss during edits

### Global Requirements Compliance
- [x] **GR-69**: Producer Portal Architecture - Review patterns implemented
- [x] **GR-52**: Universal Entity Management - Entity aggregation patterns
- [x] **GR-41**: Database Standards - Proper table relationships with consistency
- [x] **GR-20**: Business Logic Standards - Validation rules enforced
- [x] **GR-44**: Communication Architecture - Ready for quote submission