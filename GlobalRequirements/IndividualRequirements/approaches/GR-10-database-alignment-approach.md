# GR-10 SR22/SR26 Financial Responsibility Filing - Database Alignment Approach

## Overview
This approach document outlines how to update GR-10 (SR22/SR26 Financial Responsibility Filing) to include database schema sections that align with the current database structure in the Docker container (claude_db).

## Current State Analysis

### GR-10 Current State
- Comprehensive SR22/SR26 business requirements
- No Section E (Database Schema) present
- Covers filing processes, form specifications, and regulatory compliance
- References reason categories and documentation requirements

### Actual Database State (claude_db)
Based on the Docker container analysis:
- **SR22 tables exist**: sr22, sr22_type, sr22_reason
- **SR26 tables exist**: sr26, sr26_type, sr26_reason
- **Minimal structure**: Tables only contain basic fields with type relationships
- **Standard pattern**: Follows the entity/entity_type pattern consistent with other tables

## Key Additions Needed

### 1. Add Section E (Database Schema)
The current GR-10 lacks a database schema section. We need to add this section based on the actual tables.

### 2. Enhance Table Structures
The current tables are minimal and need additional fields to support the business requirements outlined in GR-10.

## Proposed Updates

### Add New Section: "Section E: Database Schema"

```markdown
## Section E: Database Schema

### SR22 Filing Tables

#### sr22_type Table
Stores types of SR22 filings (owner policy, operator policy, etc.)
```sql
CREATE TABLE sr22_type (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    status_id INT,
    created_by INT,
    updated_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_sr22_type_code (code),
    INDEX idx_sr22_type_status (status_id),
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```

#### sr22_reason Table
Stores standard reasons for SR22 requirements (already exists)
```sql
CREATE TABLE sr22_reason (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_sr22_reason_code (code)
);
```

Standard reason codes:
- DWI_DUI: DWI or DUI Conviction
- NO_INSURANCE: Driving Without Insurance
- MULTIPLE_OFFENSES: Multiple Traffic Offenses
- AT_FAULT_UNINSURED: At-Fault Accident Without Insurance
- LICENSE_SUSPENSION: License Suspension or Revocation
- COURT_ORDER: Court Order or Suspended License

#### sr22 Table (Enhanced)
Main SR22 filing records - needs additional fields to support requirements
```sql
CREATE TABLE sr22 (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sr22_type_id INT NOT NULL,
    status_id INT,
    policy_id INT NOT NULL,
    driver_id INT NOT NULL,
    sr22_reason_id INT NOT NULL,
    case_number VARCHAR(50),  -- Typically driver's license number
    filing_state VARCHAR(2) NOT NULL,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    filing_date DATE NOT NULL,
    document_id INT,  -- Reference to generated SR22 document
    fee_amount DECIMAL(10,2),
    is_non_owner BOOLEAN DEFAULT FALSE,
    state_confirmation_number VARCHAR(100),
    created_by INT,
    updated_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_sr22_policy (policy_id),
    INDEX idx_sr22_driver (driver_id),
    INDEX idx_sr22_status (status_id),
    INDEX idx_sr22_effective_date (effective_date),
    INDEX idx_sr22_filing_state (filing_state),
    
    FOREIGN KEY (sr22_type_id) REFERENCES sr22_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (driver_id) REFERENCES driver(id),
    FOREIGN KEY (sr22_reason_id) REFERENCES sr22_reason(id),
    FOREIGN KEY (document_id) REFERENCES document(id)
);
```

### SR26 Cancellation Tables

#### sr26_type Table
Stores types of SR26 cancellations
```sql
CREATE TABLE sr26_type (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    status_id INT,
    created_by INT,
    updated_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_sr26_type_code (code),
    INDEX idx_sr26_type_status (status_id),
    FOREIGN KEY (status_id) REFERENCES status(id)
);
```

#### sr26_reason Table
Stores reasons for SR26 cancellations (already exists)
```sql
CREATE TABLE sr26_reason (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_sr26_reason_code (code)
);
```

Standard reason codes:
- NO_LONGER_REQUIRED: Driver no longer requires SR22
- POLICY_CANCELLED: Policy cancellation
- COURT_ORDER: Court order removing requirement
- PROGRAM_CHANGE: Program change eliminating requirement

#### sr26 Table (Enhanced)
Main SR26 cancellation records - needs additional fields
```sql
CREATE TABLE sr26 (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sr26_type_id INT NOT NULL,
    status_id INT,
    sr22_id INT NOT NULL,  -- Reference to original SR22 filing
    sr26_reason_id INT NOT NULL,
    cancellation_date DATE NOT NULL,
    filing_date DATE NOT NULL,
    document_id INT,  -- Reference to generated SR26 document
    state_confirmation_number VARCHAR(100),
    created_by INT,
    updated_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_sr26_sr22 (sr22_id),
    INDEX idx_sr26_status (status_id),
    INDEX idx_sr26_cancellation_date (cancellation_date),
    
    FOREIGN KEY (sr26_type_id) REFERENCES sr26_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (sr22_id) REFERENCES sr22(id),
    FOREIGN KEY (sr26_reason_id) REFERENCES sr26_reason(id),
    FOREIGN KEY (document_id) REFERENCES document(id)
);
```

### Supporting Tables

#### sr22_state_submission Table
Tracks SR22/SR26 submissions to state authorities
- we are not submitting them. we are only generating the documents to give to the insured.
```sql
CREATE TABLE sr22_state_submission (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sr22_id INT,
    sr26_id INT,
    submission_type ENUM('SR22', 'SR26') NOT NULL,
    state VARCHAR(2) NOT NULL,
    submission_date DATETIME NOT NULL,
    submission_method VARCHAR(50),
    submission_status VARCHAR(50),
    confirmation_number VARCHAR(100),
    error_message TEXT,
    retry_count INT DEFAULT 0,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_submission_sr22 (sr22_id),
    INDEX idx_submission_sr26 (sr26_id),
    INDEX idx_submission_date (submission_date),
    INDEX idx_submission_status (submission_status),
    
    FOREIGN KEY (sr22_id) REFERENCES sr22(id),
    FOREIGN KEY (sr26_id) REFERENCES sr26(id),
    
    CHECK ((sr22_id IS NOT NULL AND sr26_id IS NULL) OR 
           (sr22_id IS NULL AND sr26_id IS NOT NULL))
);
```
```

## New Tables Needed

Based on the business requirements in GR-10, the following enhancements are needed:

1. **Add fields to sr22 table**:
   - policy_id, driver_id (foreign keys)
   - case_number, filing_state, effective_date, expiration_date
   - filing_date, document_id, fee_amount
   - is_non_owner, state_confirmation_number

2. **Add fields to sr26 table**:
   - sr22_id (foreign key to original filing)
   - cancellation_date, filing_date, document_id
   - state_confirmation_number

3. **Create new table**: sr22_state_submission
   - Track submissions to state authorities
   - Handle both SR22 and SR26 submissions
   - Store confirmation and error information

## Migration Path

1. Add the new Section E to GR-10
2. Create migration scripts to add missing fields to existing tables
3. Create the sr22_state_submission table
4. Populate reason tables with standard codes
- do not do this.
5. Update application code to use enhanced schema
- No need for application code.

## Benefits of This Approach

1. **Complete Documentation**: GR-10 will have full database schema documentation
2. **Business Alignment**: Database structure will support all business requirements
3. **Audit Trail**: Enhanced tables include proper tracking and audit fields
4. **State Integration**: New submission tracking table supports regulatory requirements

## Risks and Mitigation

1. **Risk**: Existing data in minimal tables
   **Mitigation**: Create careful migration scripts to preserve existing data

2. **Risk**: Application code dependencies
   **Mitigation**: Phase the changes to allow code updates

## Next Steps

1. Review this approach with stakeholders
2. Upon approval, update GR-10 with Section E
3. Create migration scripts for table enhancements
4. Update related Global Requirements if needed