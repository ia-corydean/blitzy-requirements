# IP271 - Reports - Complete Requirement

---

## **A) WHY – Vision and Purpose**

The Reports feature transforms how insurance professionals access and analyze business data by providing a comprehensive suite of 13 distinct report types covering every aspect of insurance operations. Instead of spending hours manually gathering data from multiple sources, users can generate critical business insights with just a few clicks, export them in their preferred format, and make data-driven decisions that improve profitability and customer retention.

This reporting system addresses the critical need for real-time visibility into business performance, compliance tracking, and operational efficiency. By automating report generation and providing sophisticated filtering capabilities, the system enables producers to identify trends, spot risks early, and take proactive measures to grow their business. The role-based access ensures that sensitive financial information like commission statements remains secure while operational reports are widely available.

---

## **B) WHAT – Core Requirements**

The Reports feature provides a unified reporting platform with 13 specialized report types, each designed to address specific business needs while maintaining consistency in user experience and technical implementation.

### **1. Producer Performance Report**

Provides comprehensive metrics on business performance including:
- **New Business**: Policies issued within selected period with count and dollar value
- **Renewals**: Successfully renewed policies with retention metrics
- **Endorsements**: Modified policies tracking changes and revenue impact
- **Expiring Policies**: Upcoming expirations for proactive renewal management
- **Non-Renewals**: Policies not renewing with reason tracking
- **Non-Pay Cancellations**: Payment-related cancellations for collection focus
- **Cash Payments**: Customer payment tracking by date
- Customizable sections allowing users to include/exclude specific metrics
- Date-based filtering with policy counts and dollar values per date

### **2. Cancellations Report**

Centralized tracking of all policy cancellations with:
- **Advanced Filtering**:
  - Cancellation reasons (non-pay, underwriting, customer request)
  - Date range selection for cancellation or expiration dates
  - Office-specific or company-wide views
- **Detailed Information Display**:
  - Policy number with direct navigation link
  - Policyholder name and contact information
  - Policy status with visual indicators
  - Payment due dates and amounts
  - Cancellation effective dates
- **Interactive Features**:
  - Click-through to detailed policy view in side panel
  - Direct payment processing for recoverable cancellations
  - Contact information for customer retention efforts

### **3. Non-Renewals Report**

Proactive management of policies not renewing:
- **Flexible Date Filtering**: Start/end date ranges for analysis periods
- **Category Selection**: Filter by non-renewal types (printed notices, etc.)
- **Office-Level Control**: View all offices or specific locations
- **Key Data Points**:
  - Policy details with navigation links
  - Insured information for outreach
  - Non-renewal and print dates
  - Detailed messages explaining non-renewal reasons

### **4. Policy Suspenses Report**

Action item tracking for policy-related tasks:
- **Smart Filtering**:
  - Date range for suspense due dates
  - Show/hide processed items toggle
  - Policy number search capability
- **Comprehensive Display**:
  - Policy and insured information
  - Producer assignment and due dates
  - Detailed suspense messages
  - Status tracking (open/processed)
- **Resolution Workflow**:
  - Direct action buttons (Open/Submit)
  - Side panel for suspense details
  - Document upload capabilities
  - Photo upload requirements
  - Digital signature collection
  - Notes and instructions display

### **5. Requotable Policies Report**

Opportunity tracking for policy recovery:
- **Simple Filtering**: Office selection for targeted views
- **Essential Information**:
  - Policy numbers with quick navigation
  - Insured names for recognition
  - Cancellation dates for timing
- **Action-Oriented**: Direct links to begin re-quoting process

### **6. Unsigned E-Signature Endorsements**

Compliance tracking for pending signatures:
- **Automatic Detection**: Identifies all unsigned endorsements
- **Time-Sensitive Display**:
  - Creation and effective dates
  - Age of pending signature
  - Policy and insured details
- **Empty State Handling**: Clear messaging when all signatures collected

### **7. Payment Due Report**

Revenue protection through payment tracking:
- **Date-Based Filtering**: Payment due or cancellation date ranges
- **Comprehensive Details**:
  - Policy status indicators
  - Primary and alternate phone numbers
  - Payment amounts and due dates
  - Cancellation warnings
- **Collection Support**: Contact information readily available

### **8. Claims Report**

Loss management and analysis:
- **Status Filtering**: Open vs closed claims
- **Date Options**: Loss date or report date filtering
- **Financial Tracking**:
  - Loss sequence numbers
  - Loss amounts paid
  - Claim status tracking
  - Policy linkage

### **9. Transmittal Report**

Financial transaction reconciliation:
- **Flexible Filtering**:
  - Date range selection
  - Producer e-check items filter
- **Dual View Modes**:
  - Summary view by transaction type
  - Detailed itemized breakdown
- **Transaction Types**: New business, payments, endorsements, requotes
- **E-Check Tracking**: Numbers, confirmation, acceptance status

### **10. Retention Report**

Customer retention analytics:
- **Ordering Options**:
  - Date/Program view
  - Program/Date view
- **Metrics Display**:
  - Year and month breakdowns
  - Policy counts by program
  - Retention percentages
  - Lapse rate tracking

### **11. Producer Summary Report**

Individual producer performance metrics:
- **Point-in-Time Analysis**: Select specific end date
- **Comprehensive Metrics**:
  - Transaction counts and premiums
  - Cancellation analysis by reason
  - Earned premiums vs incurred losses
  - In-force policy counts
  - Renewal performance

### **12. Commission Statement Report**

Financial compensation tracking (Manager access only):
- **Hierarchical Display**:
  - Global commission statements
  - Office-specific statements
- **Document Access**:
  - PDF viewing in-app
  - CSV download for analysis
- **Security**: Role-based access control

### **13. Sweep Balance Report**

Check transaction reconciliation:
- **Required Date Selection**: Start and end dates
- **Detailed Transaction Info**:
  - Office and policy linkage
  - Payment timestamps
  - E-check processing details
  - Sweep dates and amounts
- **Subtotals**: By date, office, and total amounts

### **3. Business Rules & Validation**

- All date ranges must be valid (start date before end date)
- Export file sizes limited to prevent system overload
- Report generation timeout after 5 minutes with error handling
- Pagination required for reports exceeding 1000 rows
- Role-based access enforced at API level
- Data retention policies apply to generated report files

### **4. Save & Navigation**

- Report parameters saved in user session for quick re-run
- Export history maintained for 30 days
- Direct navigation from report rows to source records
- Breadcrumb navigation back to report list
- Print-friendly layouts for all reports

---

## Entity Analysis

### Entities Involved
| Entity Name | Type | Status | Notes |
|-------------|------|--------|-------|
| template | Core | Existing | Stores report definitions |
| template_type | Reference | Existing | Categorizes templates |
| configuration | Supporting | Existing | Report parameters |
| configuration_type | Reference | Existing | Parameter categories |
| file | Supporting | Existing | Generated report storage |
| policy | Core | Existing | Policy data source |
| quote | Core | Existing | Quote metrics source |
| driver | Core | Existing | Driver information |
| vehicle | Core | Existing | Vehicle data |
| claim | Core | Existing | Claims information |
| payment | Core | Existing | Payment tracking |
| suspense | Core | Existing | Task management |
| producer | Core | Existing | Producer metrics |
| user | Core | Existing | Access control |
| program | Core | Existing | Program filtering |
| commission | Core | Existing | Commission data |
| transaction | Core | Existing | Financial data |

### New Tables Required
None - the reporting system leverages entirely existing infrastructure.

### Modifications to Existing Tables
None - all required fields already exist in the current schema.

### Relationships Identified
- template → template_type (many:1)
- configuration → configuration_type (many:1)
- Reports access data from all core business tables through read-only queries

---

## Field Mappings (Section C)

### Backend Mappings

#### Report Generation

##### Template-Based Report Creation
- **Backend Mapping**: 
  ```
  get template by code where template_type = 'report'
  -> parse template.content for report definition
  -> apply configuration parameters
  -> execute data queries
  -> format results using template
  -> return formatted report
  ```

##### Configuration Parameter Processing
- **Backend Mapping**: 
  ```
  get configuration where key = 'report_{report_code}_filters'
  -> parse metadata JSON for filter definitions
  -> apply user selections to query
  -> store selections in session
  -> return filtered dataset
  ```

#### Report Export

##### PDF Generation
- **Backend Mapping**: 
  ```
  get report data from generation process
  -> apply PDF template from template table
  -> generate PDF using existing service
  -> store in file table with file_type = 'report_pdf'
  -> return file.path for download
  ```

##### CSV Export
- **Backend Mapping**: 
  ```
  get report data from generation process
  -> format as CSV with headers
  -> store in file table with file_type = 'report_csv'
  -> stream file for download
  ```

### Implementation Architecture

The reporting system follows a template-driven architecture that maximizes reusability:

- **Report Service**: Centralized service handling all report generation
- **Template Engine**: Processes report templates with data injection
- **Configuration Manager**: Handles dynamic filters and parameters
- **Export Service**: Manages PDF/CSV generation and delivery
- **Cache Layer**: Stores frequently accessed report data
- **Queue System**: Handles long-running reports asynchronously

### Integration Specifications

- **Data Access**: Read-only queries against production read replicas
- **Caching Strategy**: 15-minute cache for non-financial reports
- **Export Limits**: 50,000 rows for CSV, 500 pages for PDF
- **API Rate Limiting**: 10 report generations per minute per user
- **WebSocket Updates**: Real-time progress for long-running reports

---

## **D) User Experience (UX) & Flows**

### **1. Report Selection Flow**

1. User navigates to Reports section in main navigation
2. Report list displays with categories and descriptions
3. User selects desired report type
4. System loads report-specific filter interface
5. Default filters populate based on user's context

### **2. Report Configuration Flow**

1. User adjusts filters (dates, offices, statuses)
2. Optional: User selects sections to include/exclude
3. User clicks "Generate Report"
4. Loading indicator shows with progress updates
5. Report displays in paginated table format

### **3. Report Interaction Flow**

1. User can sort by clicking column headers
2. Click on any row for detailed side panel view
3. Use pagination controls for large datasets
4. Apply quick filters without regenerating
5. Save filter combination for future use

### **4. Export Flow**

1. User clicks "Export" button
2. Modal appears with format options (PDF/CSV)
3. Optional: Select specific pages or all data
4. Processing indicator during generation
5. File downloads automatically when ready

### **5. Error Handling Flow**

1. If report fails, clear error message displays
2. Option to retry with same parameters
3. Fallback to cached version if available
4. Support contact information provided
5. Error logged for system monitoring

---

## API Specifications

### Endpoints Required
```http
# Report Management
GET    /api/v1/reports                    # List available reports
GET    /api/v1/reports/{code}/filters     # Get filter options
POST   /api/v1/reports/{code}/generate    # Generate report
GET    /api/v1/reports/{code}/status/{id} # Check generation status
GET    /api/v1/reports/{code}/download/{id} # Download generated report

# Report Data Access
GET    /api/v1/reports/{code}/data        # Get paginated report data
POST   /api/v1/reports/{code}/export      # Export to PDF/CSV
GET    /api/v1/reports/history            # User's report history

# Configuration
GET    /api/v1/reports/{code}/config      # Get report configuration
PUT    /api/v1/reports/{code}/config      # Save user preferences
```

### Real-time Updates
```javascript
// WebSocket channels for progress tracking
private-report-generation.{job_id}         // Progress updates
private-report-complete.{job_id}           // Completion notification
```

---

## Database Schema (Section E)

### Existing Infrastructure Usage

The reporting system requires NO new tables. All functionality is achieved through:

#### Template Storage
```sql
-- Report definitions stored as templates
INSERT INTO template (template_type_id, code, name, content, configuration, status_id, created_by)
SELECT 
    (SELECT id FROM template_type WHERE code = 'report'),
    'producer_performance_report',
    'Producer Performance Report',
    '<!-- Report template HTML/JSON -->',
    '{"filters": ["date_range", "office"], "sections": ["new_business", "renewals"]}',
    (SELECT id FROM status WHERE code = 'active'),
    1;
```

#### Configuration Storage
```sql
-- User preferences and saved filters
INSERT INTO configuration (configuration_type_id, key, value, metadata, status_id, created_by)
SELECT
    (SELECT id FROM configuration_type WHERE code = 'report_preferences'),
    'user_123_producer_performance_filters',
    '{"date_start": "2024-01-01", "office_id": 5}',
    '{"last_used": "2024-01-15", "frequency": "weekly"}',
    (SELECT id FROM status WHERE code = 'active'),
    123;
```

#### File Storage for Exports
```sql
-- Generated reports stored as files
INSERT INTO file (file_type_id, name, path, size, mime_type, metadata, status_id, created_by)
SELECT
    (SELECT id FROM file_type WHERE code = 'report_export'),
    'producer_performance_2024Q1.pdf',
    '/storage/reports/2024/01/report_12345.pdf',
    2048576,
    'application/pdf',
    '{"report_type": "producer_performance", "parameters": {...}}',
    (SELECT id FROM status WHERE code = 'active'),
    123;
```

---

## Implementation Notes

### Dependencies
- Template system must support report type templates
- Configuration system must handle JSON metadata
- File storage system must support large files
- Queue system required for asynchronous processing
- Read replica database for report queries

### Migration Considerations
- Seed initial report templates during deployment
- Configure template_type to include 'report' type
- Set up appropriate file_type entries
- Create configuration_type for report preferences
- No data migration required

### Performance Considerations
- Index optimization on frequently queried fields
- Materialized views for complex aggregations
- Partitioning for large transaction tables
- Query result caching for repeated reports
- Connection pooling for read replicas

---

## Quality Checklist

### Pre-Implementation
- [x] All UI fields mapped to database columns
- [x] Existing entities reused where possible
- [x] Reference tables support all report types
- [x] Naming conventions followed consistently
- [x] Relationships properly defined

### Post-Implementation
- [ ] All reports generate successfully
- [ ] Export formats work correctly
- [ ] Performance meets SLA requirements
- [ ] Role-based access properly enforced
- [ ] Error handling covers all scenarios

### Final Validation
- [ ] Backend mappings complete and accurate
- [ ] Database schema requires no changes
- [ ] No redundant functionality created
- [ ] Performance optimizations implemented
- [ ] Documentation updated

### Global Requirements Compliance
- [ ] **GR-41**: Database Standards - All queries follow naming conventions
- [ ] **GR-38**: Microservice Architecture - Report service properly bounded
- [ ] **GR-52**: Universal Entity Management - Leverages existing entities
- [ ] **GR-69**: Producer Portal Architecture - Integrated with portal navigation