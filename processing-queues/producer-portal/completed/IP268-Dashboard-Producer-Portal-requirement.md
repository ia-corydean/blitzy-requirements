# IP268 - Dashboard Producer Portal - Complete Requirement

---

## **A) WHY – Vision and Purpose**

The Producer Portal Dashboard serves as the critical command center for insurance producers, providing immediate visibility into their business operations and actionable items. Currently, producers must navigate through multiple screens and reports to understand their business status, leading to:

- Missed opportunities due to lack of visibility into requotable policies
- Delayed responses to unsigned endorsements and suspense items
- Inability to quickly assess business performance and trends
- Time wasted searching for relevant news and updates

This dashboard consolidates all essential information into a single, at-a-glance view that enables producers to:
- Prioritize their daily activities through the My Tasks widget
- Monitor business performance with visual trend analysis
- Stay informed with program-specific news
- Track key metrics and KPIs in real-time

The goal is to empower producers with data-driven insights that improve operational efficiency, reduce administrative overhead, and ultimately drive business growth through better decision-making.

---

## **B) WHAT – Core Requirements**

The Producer Portal Dashboard provides a comprehensive view of the producer's business through four primary widgets, each serving a specific business function.

### **1. My Tasks Widget**

Displays actionable items requiring immediate attention:
- **Suspense Items**: Count of active suspense items assigned to the producer
- **Unsigned Endorsements**: Endorsements with documents requiring signatures
- **Non-Pay Cancellations**: Recent cancellations due to non-payment (last 30 days)
- **Requotable Policies**: Cancelled policies eligible for re-quoting (older than 30 days)

Each metric should be clickable, navigating to the appropriate detail screen for action.

### **2. Business Trends Widget**

Provides visual representation of business performance over the last 12 months:
- **Policies Sold**: Monthly count of bound policies displayed as a line chart
- **Losses Reported**: Monthly count of reported losses displayed as a line chart
- **Cancellations**: Monthly count of policy cancellations displayed as a line chart
- **Inforce Summary**: Current total policy count and total premium amount

Charts should be interactive with hover details and support both desktop and mobile viewing.

### **3. News Widget**

Displays company and program-specific announcements:
- Latest 5 news items relevant to the producer's programs
- Each item shows:
  - Headline/Title
  - Publication date
  - Brief content preview (first 100 characters)
- Click-through capability to read full article
- Program-based filtering to ensure relevance

### **4. Statistics Widget**

Shows key performance metrics for the last 31 days:
- **New Applications**: Count of new policies with recent effective dates
- **New Endorsements**: Count of endorsements created
- **Cancellations**: Count of policies cancelled
- **Reinstatements**: Count of policies reinstated
- **Renewals**: Count of policies renewed
- **Premium**: Total premium from all above activities
- **Loss Ratio**: Calculated as (Losses / Premium) × 100
  - Note: Loss ratio hidden for CSR role users

### **5. Dashboard Features & Requirements**

- **Auto-refresh**: Dashboard data refreshes every 15 minutes
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Role-Based Display**: CSR users cannot see loss ratio metric
- **Performance**: Initial load time under 3 seconds
- **Error Handling**: Individual widget failures don't affect other widgets
- **Caching**: Implement caching strategy with widget-specific TTLs:
  - My Tasks: 5 minutes
  - Business Trends: 15 minutes
  - News: 60 minutes
  - Statistics: 5 minutes

---

## Entity Analysis

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|-------|
| policy | Core | Existing | Primary source for most metrics |
| producer | Core | Existing | User association and filtering |
| map_producer_suspense | Map | Existing | Tracks suspense items |
| endorsement | Core | Existing | Endorsement counts and signatures |
| cancellation | Core | Existing | Cancellation tracking and reasons |
| loss | Core | Existing | Loss amounts and reporting |
| news | Supporting | Existing | Company announcements |
| map_program_news | Map | Existing | Program-specific news filtering |
| renewal | Core | Existing | Renewal tracking |
| document | Supporting | Existing | Document signature requirements |
| map_endorsement_document | Map | Existing | Links endorsements to documents |
| map_document_signature | Map | Existing | Tracks document signatures |
| status | Reference | Existing | Status values for all entities |

### New Tables Required
- None - All dashboard functionality is supported by existing v5 enhanced schema

### Modifications to Existing Tables
- None - All requirements can be met with existing table structures

### Relationships Identified
- producer → policy (1:many) - Producer's policies via policy.producer_id
- producer → map_producer_suspense (1:many) - Suspense items
- policy → endorsement (1:many) - Policy endorsements
- policy → cancellation (1:many) - Policy cancellations
- policy → loss (1:many) - Policy losses
- policy → renewal (1:many) - Policy renewals
- endorsement → document (many:many) - Via map_endorsement_document
- document → signature (1:many) - Via map_document_signature
- program → news (many:many) - Via map_program_news

---

## Field Mappings (Section C)

### Backend Mappings

#### My Tasks Widget Data

##### Suspense Items Count
- **Backend Mapping**: 
  ```
  get map_producer_suspense by producer_id
  -> filter by status.code = 'active'
  -> return COUNT(*)
  ```

##### Unsigned Endorsements Count
- **Backend Mapping**:
  ```
  get policy by producer_id
  -> join endorsement on policy.id
  -> join map_endorsement_document on endorsement.id
  -> join document where signature_required = true
  -> exclude where map_document_signature exists
  -> return COUNT(DISTINCT endorsement.id)
  ```

##### Non-Pay Cancellations Count
- **Backend Mapping**:
  ```
  get policy by producer_id
  -> join cancellation where cancellation_type = 'non_pay'
  -> filter by date >= 30 days ago
  -> return COUNT(*)
  ```

##### Requotable Policies Count
- **Backend Mapping**:
  ```
  get policy by producer_id
  -> join cancellation where date < 30 days ago
  -> exclude where new policy exists with similar policy_number
  -> return COUNT(*)
  ```

#### Business Trends Widget Data

##### Monthly Policies Sold
- **Backend Mapping**:
  ```
  get policy by producer_id
  -> filter by bound_date in last 12 months
  -> group by MONTH(bound_date)
  -> return month, COUNT(*) for chart data
  ```

##### Monthly Losses Reported
- **Backend Mapping**:
  ```
  get policy by producer_id
  -> join loss on policy.id
  -> filter by created_at in last 12 months
  -> group by MONTH(created_at)
  -> return month, COUNT(*) for chart data
  ```

##### Monthly Cancellations
- **Backend Mapping**:
  ```
  get policy by producer_id
  -> join cancellation on policy.id
  -> filter by date in last 12 months
  -> group by MONTH(date)
  -> return month, COUNT(*) for chart data
  ```

##### Inforce Totals
- **Backend Mapping**:
  ```
  get policy by producer_id
  -> filter by status NOT IN ('cancelled', 'expired', 'non_renewed')
  -> filter by cancellation_date is null OR > today
  -> return COUNT(*) as total_policies, SUM(premium) as total_premium
  ```

#### News Widget Data

##### Program-Specific News
- **Backend Mapping**:
  ```
  get producer's programs via policy.program_id
  -> join map_program_news on program_id
  -> join news on news_id
  -> filter by publication_date <= today
  -> order by publication_date DESC
  -> limit 5
  -> return title, content, publication_date
  ```

#### Statistics Widget Data

##### Last 31 Days Metrics
- **Backend Mapping**:
  ```
  calculate for each metric where date >= 31 days ago:
  -> new_applications: COUNT(policy) where effective_date in range
  -> new_endorsements: COUNT(endorsement) where created_at in range
  -> cancellations: COUNT(cancellation) where date in range
  -> reinstatements: COUNT(policy) where reinstatement_date in range
  -> renewals: COUNT(renewal) where effective_date in range
  -> premium: SUM(premium) from all above
  -> loss_ratio: (SUM(loss.amount) / SUM(policy.premium)) × 100
  ```

### Implementation Architecture

**Service Layer Design**: Implement a DashboardService that orchestrates data retrieval from multiple repositories, handles caching, and formats responses for the frontend.

**Caching Strategy**: Use Redis with widget-specific TTLs to reduce database load. Implement cache warming on service startup and smart invalidation based on data changes.

**Query Optimization**: All queries use existing indexes on producer_id, dates, and status fields. Consider read replicas for dashboard queries to avoid impacting transactional systems.

**Error Isolation**: Each widget loads independently with its own error handling, ensuring one widget failure doesn't break the entire dashboard.

### Integration Specifications

**Internal Services Only**: Dashboard relies entirely on internal data sources with no external API dependencies, ensuring reliability and fast response times.

**Future WebSocket Support**: Architecture supports real-time updates via WebSocket channels for live dashboard updates when implemented.

---

## API Specifications

### Endpoints Required
```http
GET /api/v1/dashboard                    # Complete dashboard data
GET /api/v1/dashboard/my-tasks           # My Tasks widget only
GET /api/v1/dashboard/business-trends    # Business Trends widget only
GET /api/v1/dashboard/news               # News widget only
GET /api/v1/dashboard/statistics         # Statistics widget only
```

### Response Structure Example
```json
{
  "data": {
    "my_tasks": {
      "suspense_items": 5,
      "unsigned_endorsements": 3,
      "non_pay_cancellations": 2,
      "requotable_policies": 8
    },
    "business_trends": {
      "policies_sold": [
        {"month": "Jan", "count": 45},
        {"month": "Feb", "count": 52}
      ],
      "losses_reported": [...],
      "cancellations": [...],
      "inforce": {
        "total": 1250,
        "premium": 2500000
      }
    },
    "news": [
      {
        "title": "New Product Launch",
        "date": "2024-01-15",
        "content": "We are excited to announce..."
      }
    ],
    "statistics": {
      "new_applications": 23,
      "new_endorsements": 45,
      "cancellations": 12,
      "reinstatements": 3,
      "renewals": 89,
      "premium": 125000,
      "loss_ratio": 68.5
    }
  },
  "meta": {
    "generated_at": "2024-01-20T10:30:00Z",
    "cache_ttl": 300
  }
}
```

### Real-time Updates (Future Enhancement)
```javascript
// WebSocket channels for live updates
private-producer.{producer_id}.dashboard    # Full dashboard updates
private-producer.{producer_id}.tasks        # Task count changes
```

---

## Database Schema (Section E)

### No Database Changes Required

The existing v5 enhanced schema fully supports all dashboard requirements without any modifications:

#### Tables Used
- **policy**: Contains policy_number, producer_id, effective_date, bound_date, premium, status_id
- **producer**: Producer identification and authentication
- **map_producer_suspense**: Suspense item tracking with producer association
- **endorsement**: Endorsement records with creation timestamps
- **cancellation**: Cancellation records with types and dates
- **loss**: Loss amounts and dates for ratio calculations
- **news**: News content with publication dates
- **map_program_news**: Program-specific news associations
- **renewal**: Renewal tracking with effective dates
- **document**: Document signature requirements
- **map_endorsement_document**: Links endorsements to documents
- **map_document_signature**: Signature completion tracking

#### Performance Considerations
Existing indexes support efficient dashboard queries:
- `policy.producer_id` - Producer filtering
- `policy.bound_date` - Date range queries
- `endorsement.created_at` - Time-based filtering
- `cancellation.date` - Cancellation queries
- `news.publication_date` - News ordering

---

## Implementation Notes

### Dependencies
- Producer authentication system must be operational
- Policy management system must contain data
- Status reference data must be populated
- Program associations must exist for news filtering

### Migration Considerations
- No database migrations required
- No data transformation needed
- Fully backward compatible

### Performance Considerations
- Implement Redis caching from day one
- Use database read replicas for dashboard queries
- Consider materialized views for complex aggregations in future
- Monitor query execution times and optimize as needed

---

## Quality Checklist

### Pre-Implementation
- [x] All UI elements mapped to database columns
- [x] Existing entities maximally reused
- [x] No new tables or columns required
- [x] Performance strategy defined with caching
- [x] Role-based access requirements identified

### Post-Implementation
- [ ] Dashboard loads within 3-second target
- [ ] Producer data isolation verified
- [ ] Cache hit rates meet 80%+ target
- [ ] Mobile responsive design validated
- [ ] Error handling tested for widget failures
- [ ] Role-based visibility working correctly

### Final Validation
- [x] Backend mappings optimized for performance
- [x] No database changes required
- [x] Caching strategy documented
- [x] Security considerations addressed
- [x] Documentation complete

### Global Requirements Compliance
- [x] **GR-69**: Producer Portal Architecture - Dashboard as primary entry point
- [x] **GR-41**: Database Standards - Uses existing schema with proper patterns
- [x] **GR-27**: Performance Requirements - 3-second load time with caching
- [x] **GR-33**: Data Services & Caching - Redis caching for all widgets
- [x] **GR-36**: Authentication & Permissions - JWT auth with role-based display