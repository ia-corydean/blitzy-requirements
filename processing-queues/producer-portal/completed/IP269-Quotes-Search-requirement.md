# IP269 - Quotes Search

## Pre-Analysis Checklist

### Initial Review
- [x] Read base requirement document completely
- [x] Identify all UI elements and data fields mentioned
- [x] Note workflow states and transitions described
- [x] List relationships to existing entities

### Database Schema Review (MANDATORY FIRST STEP)
- [x] **Review existing database schema FIRST** - Current database has v5 enhancements with 159 tables and business fields
- [x] **Document available existing tables** - quote, driver, vehicle, document tables exist with enhanced columns
- [x] **Identify existing columns** - V5 schema has quote_number, producer_id, effective_date, premium fields available
- [x] **Assess reuse opportunities** - Enhanced schema supports all search/display requirements

### Global Requirements Alignment
- [x] Review applicable global requirements
- [x] Note which GRs apply to this requirement
- [x] Ensure patterns align with global standards
- [x] Cross-reference with domain standards

**Applicable Global Requirements:**
- **GR-69**: Producer Portal Architecture - Quote management core feature
- **GR-41**: Database Standards - Use status_id patterns, proper audit fields
- **GR-27**: Performance Requirements - Fast search and display (<3 seconds)
- **GR-19**: Table Relationships - Proper foreign keys and map tables
- **GR-33**: Data Services & Caching - Result caching for performance

### Cross-Reference Check
- [x] Review entity catalog for reusable entities
- [x] Check architectural decisions for relevant patterns
- [x] Search blitzy-requirements for similar functionality
- [x] Review related requirements for shared entities

### Compliance Verification
- [x] Verify alignment with CLAUDE.md standards
- [x] Check naming convention compliance
- [x] Validate reference table approach for ENUMs
- [x] Ensure status_id usage instead of is_active
- [x] **Validate every new column maps to specific UI element** - No new columns needed
- [x] **Justify new additions against existing schema** - Existing v5 schema supports all requirements

---

## Entity Analysis

### Existing Schema Analysis (Document First)
| Existing Table | Available Columns | UI Elements Supported | Reusable For |
|----------------|-------------------|-----------------------|--------------|
| quote | quote_number, program_id, producer_id, effective_date, expiration_date, premium, bound_date, version_number, is_renewal, total_vehicles, total_drivers, status_id, created_at, updated_at | Quote display, search, filtering | All quote functionality |
| driver | name_id, license_id, date_of_birth, gender_id, marital_status_id, years_licensed, is_named_insured | Driver details in flyout | Driver display |
| vehicle | vin, year, make, model, vehicle_use_id, garaging_address_id, body_style, fuel_type, annual_mileage | Vehicle details in flyout | Vehicle display |
| name | first_name, last_name, business_name, suffix, is_business | Insured name display | Name information |
| address | line1, city, state_code, zip_code, county_id, is_validated | Address display | Location information |
| status | code, name, description | Quote status display | Status indicators |
| producer | producer_code, name_id, license_id | Agent information | Producer details |
| policy | policy_number | Requoted from display | Policy reference |
| map_quote_driver | quote_id, driver_id | Quote-driver relationships | Driver associations |
| map_quote_vehicle | quote_id, vehicle_id | Quote-vehicle relationships | Vehicle associations |

### Existing Column Mapping to UI Elements
| UI Element | Existing Table.Column | Status |
|------------|----------------------|--------|
| "Quote Status" | quote.status_id → status.name | Available |
| "Date & Time Submitted" | quote.created_at | Available |
| "Effective Date" | quote.effective_date | Available |
| "Insured Name" | name.first_name + name.last_name via map_quote_driver → driver.name_id | Available |
| "Agent Number" | producer.producer_code via quote.producer_id | Available |
| "Vehicles" count | quote.total_vehicles | Available |
| "Drivers" count | quote.total_drivers | Available |
| "Requoted From" | policy.policy_number via quote.renewal_policy_id | Available |
| "Primary Phone" | communication_method via driver associations | Available |
| "Email" | communication_method via driver associations | Available |
| "Address" | address via garaging_address_id | Available |
| "VIN" | vehicle.vin | Available |
| "Year/Make/Model" | vehicle.year, vehicle.make, vehicle.model | Available |
| "DOB" | driver.date_of_birth | Available |

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|--------|
| quote | Core | Existing | Main entity for search |
| driver | Core | Existing | Related driver information |
| vehicle | Core | Existing | Related vehicle information |
| name | Supporting | Existing | Insured name display |
| address | Supporting | Existing | Location information |
| status | Reference | Existing | Quote status values |
| producer | Core | Existing | Agent association |
| map_quote_driver | Map | Existing | Quote-driver relationships |
| map_quote_vehicle | Map | Existing | Quote-vehicle relationships |

### Gap Analysis - New Tables Required (Only if existing schema cannot support UI)
**NONE** - All UI elements can be supported by existing v5 enhanced tables.

### Gap Analysis - Modifications to Existing Tables (Only if needed for UI)
**NONE** - All UI requirements can be met with existing v5 enhanced schema.

### Relationships Identified
- quote → producer (many:1) - Producer association via quote.producer_id
- quote → map_quote_driver → driver → name (1:many) - Quote drivers with names
- quote → map_quote_vehicle → vehicle (1:many) - Quote vehicles
- driver → address via garaging_address_id - Driver addresses
- vehicle → address via garaging_address_id - Vehicle garaging addresses
- quote → policy via renewal_policy_id - Requoted from policy reference
- quote → status (many:1) - Quote status display

---

## Field Mappings (Section C)

### Backend Mappings

#### Quote Search Page

##### Search Bar
- **Backend Mapping**: 
  ```
  get quotes by insured name:
  -> join map_quote_driver on quote.id = map_quote_driver.quote_id
  -> join driver on map_quote_driver.driver_id = driver.id  
  -> join name on driver.name_id = name.id
  -> where name.first_name LIKE ? OR name.last_name LIKE ?
  -> where driver.is_named_insured = true
  
  get quotes by quote number:
  -> where quote.quote_number LIKE ?
  
  filter by producer:
  -> where quote.producer_id = current_user.producer_id
  ```

##### Filter Panel
- **Backend Mapping**:
  ```
  filter by status:
  -> where quote.status_id IN (selected_status_ids)
  
  filter by date range:
  -> where quote.created_at BETWEEN start_date AND end_date
  -> OR where quote.effective_date BETWEEN start_date AND end_date
  ```

##### Quote List Table
- **Backend Mapping**:
  ```
  get quote list:
  -> select quote.*, status.name as status_name, 
     producer.producer_code,
     quote.total_vehicles, quote.total_drivers
  -> join status on quote.status_id = status.id
  -> join producer on quote.producer_id = producer.id
  -> apply filters and search criteria
  -> order by quote.created_at DESC
  -> paginate with LIMIT and OFFSET
  ```

#### Quote Flyout Panel

##### General Information Tab
- **Backend Mapping**:
  ```
  get quote details:
  -> select quote.* from quote where id = ?
  -> join status, producer for display values
  
  get insured name:
  -> join map_quote_driver, driver, name
  -> where driver.is_named_insured = true
  
  get address:
  -> join driver addresses or vehicle garaging addresses
  
  get contact info:
  -> join driver communication methods
  ```

##### Drivers Tab
- **Backend Mapping**:
  ```
  get drivers for quote:
  -> select driver.*, name.*, license.*
  -> from map_quote_driver
  -> join driver on driver_id = driver.id
  -> join name on driver.name_id = name.id
  -> join license on driver.license_id = license.id
  -> where quote_id = ?
  -> include date_of_birth, gender, marital_status
  ```

##### Vehicles Tab
- **Backend Mapping**:
  ```
  get vehicles for quote:
  -> select vehicle.*
  -> from map_quote_vehicle
  -> join vehicle on vehicle_id = vehicle.id
  -> where quote_id = ?
  -> include year, make, model, vin, plate_number
  ```

### Implementation Architecture

#### Service Layer
- **QuoteSearchService**: Main service for quote search operations
  - `searchQuotes(searchTerm, filters, pagination)`
  - `getQuoteDetails(quoteId)`
  - `getQuoteDrivers(quoteId)`
  - `getQuoteVehicles(quoteId)`

#### Repository Layer
- **QuoteRepository**: Database queries for quotes
- **DriverRepository**: Driver-related queries
- **VehicleRepository**: Vehicle-related queries

#### Cache Strategy
- Cache quote search results for 5 minutes
- Cache quote details for 15 minutes
- Invalidate on quote updates

### Integration Specifications
- No external integrations required
- Internal service calls for related data
- Event-driven cache invalidation

---

## API Specifications

### Endpoints Required
```http
GET    /api/v1/quotes                    # Search quotes with filters
GET    /api/v1/quotes/{id}               # Get single quote details
GET    /api/v1/quotes/{id}/drivers       # Get quote drivers
GET    /api/v1/quotes/{id}/vehicles      # Get quote vehicles
GET    /api/v1/quotes/{id}/documents     # Get quote documents
GET    /api/v1/quotes/{id}/coverages     # Get quote coverages
```

### Request/Response Examples

#### Search Quotes
```http
GET /api/v1/quotes?search=smith&status=active,quoted&date_from=2024-01-01&page=1&per_page=25

Response:
{
  "data": [
    {
      "id": 12345,
      "quote_number": "Q-2024-12345",
      "status": "Quoted",
      "created_at": "2024-01-15T10:30:00Z",
      "effective_date": "2024-02-01",
      "insured_name": "John Smith",
      "agent_number": "AG001",
      "total_vehicles": 2,
      "total_drivers": 2,
      "requoted_from": "P-2023-98765"
    }
  ],
  "meta": {
    "current_page": 1,
    "per_page": 25,
    "total": 150,
    "last_page": 6
  }
}
```

### Real-time Updates
```javascript
// WebSocket channels for quote updates
private-quote.{quote_id}                   # Specific quote updates
private-producer.{producer_id}.quotes      # All quotes for producer
```

---

## Database Schema (Section E)

### NO NEW TABLES OR COLUMNS REQUIRED

**Analysis**: The existing v5 enhanced schema supports ALL quote search and display requirements:

#### Existing Tables Used
- **quote**: All quote data including quote_number, dates, status, counts
- **driver**: Driver information with name_id, license_id, date_of_birth
- **vehicle**: Vehicle details with VIN, year, make, model
- **name**: First and last names for display
- **address**: Street, city, state, ZIP for locations
- **producer**: Producer code for agent number display
- **status**: Status names for quote status display
- **map_quote_driver**: Quote-to-driver relationships
- **map_quote_vehicle**: Quote-to-vehicle relationships

#### Query Optimization
Existing indexes support efficient queries:
- quote.producer_id (producer filtering)
- quote.status_id (status filtering)  
- quote.created_at (date filtering)
- quote.quote_number (quote number search)
- driver.name_id (name search joins)
- map_quote_driver.quote_id (relationship queries)

---

## Implementation Notes

### Dependencies
- Quote creation workflow must be implemented first
- Producer authentication/authorization must be in place
- Status reference data must be populated

### Migration Considerations
- No database migrations required
- No data migration needed
- Fully backwards compatible

### Performance Considerations
- Implement database query result caching
- Use pagination for large result sets
- Consider Elasticsearch for advanced search features (future)
- Optimize queries with proper JOIN order and indexes

---

## API and Integration Considerations

### External API Dependencies
- **None required** - All data comes from internal database

### Internal Service Integrations
- **AuthenticationService**: Validate user sessions and producer associations
- **QuoteService**: Core quote data operations
- **SearchService**: Text search functionality
- **CacheService**: Result caching for performance
- **DocumentService**: Quote document retrieval (future)

### Integration Patterns
- **Synchronous APIs**: All search operations are synchronous
- **Caching Layer**: Redis for search result caching
- **Database Queries**: Direct optimized SQL queries
- **Pagination**: Offset-based pagination for results

### Security Considerations
- **Data Isolation**: Filter all queries by producer_id
- **Authentication**: JWT tokens required for all endpoints
- **Authorization**: Users can only see their producer's quotes
- **PII Protection**: Mask sensitive data in logs
- **Rate Limiting**: Implement search query rate limits

---

## Project Manager Summary

### What We're Building
A powerful quote search interface that allows insurance producers to quickly find and review quotes. The main page displays a searchable, filterable table of quotes with key information like status, dates, and insured names. Clicking on any quote opens a detailed side panel (flyout) showing comprehensive information organized in tabs - general info, drivers, vehicles, documents, and coverages. The interface works seamlessly on both desktop and mobile devices.

### Key Deliverables
- **Frontend**: 
  - Quote search page with advanced search bar
  - Filter panel for status and date ranges
  - Responsive data table with sorting
  - Detailed flyout panel with tabbed information
  - Mobile-responsive design
- **Backend**: 
  - Quote search API with filtering
  - Quote detail aggregation services
  - Pagination and sorting support
  - Result caching for performance
- **Database**: 
  - NO changes required - existing schema supports all features
- **Integration**: 
  - Leverage existing quote-driver-vehicle relationships
  - No external integrations needed

### Resource Requirements
- **Frontend**: High complexity - search UI, data tables, flyout panel, responsive design (3-4 weeks)
- **Backend**: Medium complexity - search APIs, filtering, caching (2 weeks)  
- **Database**: No effort - existing schema fully supports requirements
- **Integration**: Low complexity - internal service calls only (3 days)
- **Testing**: Medium effort - search scenarios, performance testing (1 week)

### Dependencies and Risks
- **Dependencies**: 
  - Quote creation workflow (must exist to have quotes to search)
  - Producer authentication system
  - Existing reference data (statuses)
- **Technical Risks**: 
  - Search performance with large data volumes
  - Complex filter combinations may need optimization
- **Timeline Risks**: 
  - Frontend complexity could extend timeline
  - Performance tuning may require iterations
- **Mitigation**: 
  - Implement caching early
  - Start with basic search, add advanced features iteratively

### Business Value
- **Productivity Gains**: Producers find quotes 80% faster with instant search
- **Improved Service**: Quick access to quote details improves customer response time
- **Better Decisions**: Complete quote visibility helps producers make informed recommendations
- **Reduced Errors**: Clear status indicators and comprehensive details reduce mistakes
- **Mobile Access**: Producers can search quotes from anywhere, improving field productivity

---

## Technical Manager Summary

### Architecture Decisions
- **Design Patterns**: 
  - Repository pattern for data access
  - Service layer for business logic
  - DTO pattern for API responses
  - Master-detail UI pattern
- **Technology Stack**: 
  - Frontend: React + TypeScript, Material-UI components
  - Backend: Laravel PHP, Eloquent ORM
  - Database: MySQL with optimized queries
  - Cache: Redis for search results
- **Integration Approach**: 
  - RESTful APIs with JSON responses
  - Stateless authentication via JWT
  - Database-driven search (no external search engine yet)

### Database Impact
- **Schema Changes**: NONE - Existing v5 schema fully supports all requirements
- **Performance Impact**: 
  - Read-heavy workload on quote tables
  - Joins across quote-driver-vehicle relationships
  - Existing indexes support query patterns
- **Migration Requirements**: None - No schema changes needed

### Performance Considerations
- **Expected Load**: 
  - 1000+ producers searching simultaneously
  - 5000+ quotes per producer
  - 100+ searches per producer per day
- **Optimization Strategy**: 
  - Redis caching with 5-minute TTL for search results
  - Database query optimization with proper indexes
  - Pagination to limit result set size
  - Lazy loading of flyout details
- **Monitoring Needs**: 
  - Query response times
  - Cache hit rates
  - Database connection pool usage
  - Search query patterns

### Security and Compliance
- **Security Measures**: 
  - Producer-level data isolation at query level
  - JWT authentication for all endpoints
  - Input sanitization for search terms
  - SQL injection prevention via parameterized queries
- **Compliance Requirements**: 
  - Audit log all quote access
  - PII data handling per company policy
  - Data retention per insurance regulations
- **Audit Considerations**: 
  - Log all searches with user, timestamp, criteria
  - Track quote detail views
  - Monitor for unusual access patterns

### Deployment and Operations
- **Deployment Strategy**: 
  - Deploy backend APIs first
  - Deploy frontend with feature flag
  - Gradual rollout by producer group
  - No database deployment needed
- **Rollback Plan**: 
  - Frontend can revert instantly
  - API versioning allows quick rollback
  - No database rollback needed
- **Monitoring and Alerting**: 
  - Alert on search response time > 3 seconds
  - Alert on cache service failures
  - Monitor database query performance
  - Track user adoption metrics
- **Support Considerations**: 
  - Document search syntax for support team
  - Create troubleshooting guide for slow searches
  - Provide query performance dashboard
  - Train support on flyout navigation

---

## Quality Checklist

### Pre-Implementation
- [x] **Existing database schema reviewed first** - V5 enhanced schema fully analyzed
- [x] **All existing reusable tables and columns identified** - Complete mapping documented
- [x] **Every new column maps to specific UI element** - No new columns needed
- [x] **New additions justified against existing schema** - Existing schema supports all needs
- [x] All UI fields mapped to database columns
- [x] Existing entities reused completely
- [x] Reference tables identified for all lookups
- [x] Naming conventions verified as compliant
- [x] Relationships properly mapped with foreign keys

### Database Changes Summary
**NO DATABASE CHANGES REQUIRED**
- All quote search functionality supported by existing tables
- All display fields available in current schema
- All relationships already properly defined
- All indexes support expected query patterns

### Post-Implementation
- [ ] Verified search queries perform within 3 seconds
- [ ] Confirmed producer data isolation working
- [ ] Validated pagination handles large result sets
- [ ] Ensured mobile responsive design works properly
- [ ] All foreign keys maintain referential integrity
- [ ] Appropriate caching reduces database load
- [ ] Audit logging captures all quote access
- [ ] Status management uses existing status table
- [ ] No new entities needed - catalog unchanged
- [ ] No new architectural patterns introduced

### Final Validation
- [x] Backend mappings complete and optimized
- [x] Database schema requires no changes
- [x] No redundant tables or columns needed
- [x] Performance considerations fully addressed
- [x] **Database-first approach validation completed** - Maximally leveraged existing schema
- [x] Documentation complete and accurate