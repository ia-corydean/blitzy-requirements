# CMS Reporting Requirements - Implementation Approach

## Requirement Understanding

### Overview
The Centers for Medicare & Medicaid Services (CMS) requires mandatory reporting under Section 111 of the Medicare, Medicaid, and SCHIP Extension Act (MMSEA) for all entities that pay or are responsible for paying medical claims. For Texas personal auto insurance, this means reporting liability insurance claims where the claimant may be a Medicare beneficiary.

### Key Requirements from API Documentation
1. **Mandatory Reporting**: All liability insurers must report claims to determine if Medicare has primary or secondary payer responsibility
2. **Data Collection**: 70+ data fields required per claim including injured party details, policy information, and settlement data
3. **Query Capability**: Must query CMS to identify Medicare beneficiaries and their enrollment status
4. **Ongoing Updates**: Claims must be updated as they progress through their lifecycle
5. **Compliance Tracking**: Must track reporting status and handle CMS response codes

### Texas Personal Auto Insurance Context
- Applies to all auto liability claims in Texas
- Must integrate with existing policy and claims management systems
- Requires secure handling of PII and PHI data
- Subject to CMS penalties for non-compliance or late reporting

## Domain Classification
- **Primary Domain**: Entity Integration (External API)
- **Secondary Domain**: Regulatory Compliance
- **Cross-Domain Impact**: 
  - Claims Management (claim data source)
  - Policy Management (policy details)
  - Financial/Accounting (settlement amounts)
  - Document Management (reporting archives)
- **Complexity Level**: High (due to regulatory requirements and data volume)

## Pattern Analysis

### Reusable Patterns Identified
- **GR-52 (Universal Entity Management)**: 
  - Use entity framework for CMS API configuration
  - Store API endpoints, credentials, and metadata
  - Leverage communication tracking for API calls
  
- **GR-44 (Communication Architecture)**:
  - Track all CMS API communications
  - Log requests/responses for audit trail
  - Handle retries and failures
  
- **GR-10 (SR22/SR26 Filing)**:
  - Similar regulatory reporting pattern
  - Document generation and submission workflow
  - Status tracking and updates

### Domain-Specific Needs
- **SOAP/WS-Security**: Unlike REST APIs, requires SOAP envelope with security headers
- **Large Data Payload**: 70+ fields per claim vs simpler filing requirements
- **Bidirectional Queries**: Not just submission but also status queries and beneficiary lookups
- **Complex Response Handling**: Multiple response types with detailed error codes

## Proposed Implementation

### Simplification Approach
- **Current Complexity**: Direct SOAP integration with complex security headers and large payloads
- **Simplified Solution**: 
  - Abstract SOAP complexity behind service layer
  - Use database queuing for reliable submission
  - Implement robust error handling and retry logic
- **Trade-offs**: 
  - Gain: Reliability, maintainability, audit trail
  - Lose: Real-time submission (acceptable for batch reporting)

### Technical Approach

#### Phase 1: Database Schema and Entity Setup
- [ ] Create CMS entity type in universal entity management
- [ ] Design normalized database schema for claims data
- [ ] Implement data validation rules
- [ ] Set up audit trail tables

#### Phase 2: API Integration Layer
- [ ] Implement SOAP client with WS-Security
- [ ] Create service wrapper for CMS operations
- [ ] Build request/response transformers
- [ ] Implement communication tracking

#### Phase 3: Claim Processing Workflow
- [ ] Create claim submission queue
- [ ] Implement batch processing jobs
- [ ] Build status query mechanisms
- [ ] Handle response processing

#### Phase 4: Monitoring and Compliance
- [ ] Create compliance dashboard
- [ ] Implement alerting for failures
- [ ] Build reporting for audit
- [ ] Set up data retention policies

## Risk Assessment
- **Risk 1**: Non-compliance penalties → Mitigation: Automated validation and timely submission
- **Risk 2**: Data security breach → Mitigation: Encryption, secure credentials, audit logging
- **Risk 3**: API downtime → Mitigation: Queue-based processing with retry logic
- **Risk 4**: Data quality issues → Mitigation: Comprehensive validation before submission

## Context Preservation
- **Key Decisions**: 
  - Use normalized tables for claim data (not JSON) for queryability
  - Implement asynchronous processing for reliability
  - Maintain complete audit trail for compliance
- **Dependencies**: 
  - Claims system must provide required data
  - Policy system must expose policy details
  - Communication system for notifications
- **Future Impact**: 
  - Enables other regulatory reporting
  - Provides audit framework
  - Scalable for volume growth

## Suggested Tables and Schemas

### Core Tables Following GR-41 Standards

```sql
-- Main claim record table
CREATE TABLE cms_claim (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  claim_id BIGINT UNSIGNED NOT NULL, -- FK to main claims table
  icn VARCHAR(30) NOT NULL UNIQUE, -- Internal Control Number
  rreid VARCHAR(9) NOT NULL, -- RRE ID
  
  -- Injured Party Information (normalized, not JSON)
  injured_party_hicn VARCHAR(12),
  injured_party_ssn VARCHAR(9),
  injured_party_last_name VARCHAR(40),
  injured_party_first_name VARCHAR(30),
  injured_party_middle_initial VARCHAR(1),
  injured_party_gender ENUM('M', 'F', 'U'),
  injured_party_dob DATE,
  
  -- Address (normalized for querying)
  injured_party_street1 VARCHAR(75),
  injured_party_street2 VARCHAR(75),
  injured_party_city VARCHAR(75),
  injured_party_state VARCHAR(2),
  injured_party_zip VARCHAR(5),
  
  -- Claim Details
  cms_date_of_incident DATE,
  industry_date_of_incident DATE,
  cause_code VARCHAR(7),
  state_of_venue VARCHAR(2),
  
  -- Policy Information
  policy_number VARCHAR(30),
  plan_type CHAR(1), -- D, E, L
  self_insured CHAR(1), -- Y, N
  
  -- Financial Information
  tpoc_amount DECIMAL(12,2),
  tpoc_date DATE,
  orm_indicator ENUM('Y', 'N', 'U'),
  
  -- Status Tracking
  cms_status ENUM('PENDING', 'SUBMITTED', 'ACCEPTED', 'REJECTED', 'ERROR'),
  last_submission_date DATETIME,
  last_response_date DATETIME,
  reportable BOOLEAN DEFAULT FALSE,
  beneficiary_status VARCHAR(7),
  
  -- Audit fields
  status_id BIGINT UNSIGNED NOT NULL,
  created_by BIGINT UNSIGNED NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by BIGINT UNSIGNED,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (claim_id) REFERENCES claim(id),
  FOREIGN KEY (status_id) REFERENCES status(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  FOREIGN KEY (updated_by) REFERENCES user(id),
  
  INDEX idx_icn (icn),
  INDEX idx_claim (claim_id),
  INDEX idx_submission_date (last_submission_date),
  INDEX idx_cms_status (cms_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Diagnosis codes (normalized, not in JSON)
CREATE TABLE cms_claim_diagnosis (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  cms_claim_id BIGINT UNSIGNED NOT NULL,
  diagnosis_code VARCHAR(7) NOT NULL,
  diagnosis_order INT NOT NULL, -- 1-19
  icd_version CHAR(1), -- 9 or 0 (ICD-9 or ICD-10)
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (cms_claim_id) REFERENCES cms_claim(id) ON DELETE CASCADE,
  UNIQUE KEY uk_claim_order (cms_claim_id, diagnosis_order),
  INDEX idx_diagnosis_code (diagnosis_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- API submission tracking
CREATE TABLE cms_submission (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  cms_claim_id BIGINT UNSIGNED NOT NULL,
  submission_type ENUM('ADD', 'UPDATE', 'DELETE', 'QUERY'),
  submission_date DATETIME NOT NULL,
  
  -- Request/Response tracking
  communication_id BIGINT UNSIGNED, -- Link to communication table
  request_payload TEXT, -- Encrypted
  response_payload TEXT, -- Encrypted
  
  -- Status
  submission_status ENUM('PENDING', 'SENT', 'SUCCESS', 'ERROR', 'TIMEOUT'),
  cms_disposition_code VARCHAR(2),
  error_count INT DEFAULT 0,
  
  -- Timing
  sent_at DATETIME,
  response_at DATETIME,
  processing_time_ms INT,
  
  -- Audit fields
  created_by BIGINT UNSIGNED NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (cms_claim_id) REFERENCES cms_claim(id),
  FOREIGN KEY (communication_id) REFERENCES communication(id),
  FOREIGN KEY (created_by) REFERENCES user(id),
  
  INDEX idx_claim_submission (cms_claim_id, submission_date),
  INDEX idx_status (submission_status),
  INDEX idx_submission_date (submission_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- CMS response codes and errors
CREATE TABLE cms_response_code (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  cms_submission_id BIGINT UNSIGNED NOT NULL,
  cms_code VARCHAR(5) NOT NULL,
  code_type CHAR(1), -- E for error, C for compliance
  description VARCHAR(100),
  origin VARCHAR(20), -- CMS or MIRX
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (cms_submission_id) REFERENCES cms_submission(id),
  INDEX idx_submission (cms_submission_id),
  INDEX idx_code (cms_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Scalability Considerations

#### Expected Data Volume
- **Year 1**: 50,000-100,000 claims (Texas market entry)
- **Year 3**: 500,000-1,000,000 claims (growth projection)
- **Year 5**: 2,000,000+ claims (mature market)

#### Query Patterns
- **High-frequency queries**: 
  - Claims pending submission (every 15 minutes)
  - Status checks by ICN
  - Error queue monitoring
- **Reporting queries**: 
  - Compliance reports (daily/weekly)
  - Submission success rates
  - Beneficiary match rates
- **Real-time requirements**: 
  - None - batch processing acceptable
  - 24-hour SLA for initial submission

#### JSON vs Normalized Analysis
- **Fields using JSON**: 
  - Representative info (optional, rarely queried)
  - TPOC details beyond first (rare multiple TPOCs)
  - Additional metadata (future extensibility)
- **Why not normalized**: 
  - 70+ fields already normalized for querying
  - JSON only for truly optional/rare data
  - Maintains query performance
- **Migration plan if needed**: 
  - Monitor JSON field usage
  - Extract to tables if query needs emerge

## Maintenance Scenarios

### Adding New CMS Requirements
- Add columns to cms_claim table
- Update validation rules
- Modify submission transformer
- No code changes to core workflow

### Handling API Version Changes
- Update entity configuration
- Modify request/response transformers
- Maintain backward compatibility
- Phased migration approach

### Managing Compliance Updates
- Update validation rules in database
- Modify error code mappings
- Adjust submission timing
- Update compliance reports

## Business Summary for Stakeholders

### What We're Building
We're creating an automated system to report auto insurance claims to Medicare (CMS) as required by federal law. When someone with Medicare is injured in an auto accident, we must report the claim details to CMS so they can coordinate benefits properly.

### Why It's Needed
- **Legal Requirement**: Federal law mandates this reporting with significant penalties for non-compliance
- **Cost Recovery**: Helps Medicare recover costs when our insurance should pay first
- **Compliance**: Avoids fines of $1,000 per day per claim for late reporting
- **Efficiency**: Automates a complex manual process

### Expected Outcomes
- 100% compliance with CMS reporting requirements
- Automated claim submission within required timeframes
- Complete audit trail for regulatory reviews
- Reduced manual effort and error rates
- Protection from compliance penalties

## Technical Summary for Developers

### Key Technical Decisions
- **Architecture Pattern**: Service-oriented with queue-based processing
- **Technology Choices**: 
  - Laravel SOAP client for API integration
  - MySQL for data storage (normalized schema)
  - Redis queues for reliable processing
  - Vault for credential management
- **Integration Approach**: 
  - Asynchronous batch processing
  - Database-driven workflow
  - Comprehensive error handling

### Implementation Guidelines
- Use dependency injection for SOAP client
- Implement circuit breaker for API calls
- Encrypt all PII/PHI data at rest
- Log all API interactions for audit
- Use database transactions for consistency
- Implement idempotent operations

## Validation Criteria

### Pre-Implementation Checkpoints
- [x] Business requirements clearly understood
- [x] Technical approach aligns with architecture standards
- [x] Database schema follows naming conventions
- [x] Pattern reuse maximized (85%+ target)
- [x] Security considerations addressed
- [x] Performance impact assessed
- [x] Analyzed expected data growth (2M+ records in 5 years)
- [x] Identified high-frequency query patterns
- [x] Considered reporting requirements
- [x] Evaluated JSON vs normalized (minimal JSON use)
- [x] Planned for future migration paths
- [x] Reviewed scalability at 5 dimensions

### Success Metrics
- [ ] 100% of eligible claims reported within 1 business day
- [ ] Zero compliance penalties due to late/missing reports
- [ ] < 1% error rate on submissions
- [ ] < 5 minute processing time per 1000 claims
- [ ] Complete audit trail for 100% of submissions

## Key Questions for Discussion

1. **Integration Points**
   - How does the current claims system store injury/diagnosis data?
     - How do we need to?
   - What is the policy system's data model for coverage details?
     - reference our entity list and other documentation to try and figure this out.
   - Are there existing integrations we can leverage?
     - For what?

2. **Data Quality**
   - What percentage of claims currently have complete data for CMS?
     - None. this is a greenfield system.
   - How do we handle missing SSN/HICN data?
     - How should we?
   - What validation should occur at claim entry vs CMS submission?
     - Whats your suggestion?

3. **Operational Considerations**
   - What is the expected daily claim volume?
     - whatever the average would be for a $30m book of business.
   - When should batch submissions run?
     - Whats the best practice?
   - Who needs alerts for submission failures?
     - Suggestions?
   - What reports do compliance teams need?
     - What's best practice?

4. **Business Rules**
   - Which claims are exempt from reporting?
     - Try and find this answer out yourself from the appropriate sources.
   - How do we handle claim amendments/corrections?
     - What's the suggestion?
   - What is the retention policy for CMS data?
     - What's best practice?
   - How do we manage claim lifecycle updates?
     - What do you mean? In reference to what?

5. **Performance Requirements**
   - Acceptable processing time for batch submissions?
     - Whats the best practice?
   - Query response time expectations?
     - Best practice
   - Disaster recovery requirements?
     - best practice
   - Uptime/availability targets?
     - best practice.

## Approval Section
**Status**: PENDING APPROVAL
**Reviewer Comments**: [Space for feedback]
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER