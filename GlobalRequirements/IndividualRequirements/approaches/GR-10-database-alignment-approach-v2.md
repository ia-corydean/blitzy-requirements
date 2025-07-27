# GR-10 SR22/SR26 Financial Responsibility Filing - Database Alignment Approach V2

## Overview
This approach document outlines how to update GR-10 (SR22/SR26 Financial Responsibility Filing) to include database schema sections that align with the current database structure in the Docker container (claude_db).

**V2 Updates**: Removed state submission tracking since SR22/SR26 documents are only generated for the insured, not submitted to state authorities.

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
```

## New Tables Needed

Based on the business requirements in GR-10, the following enhancements are needed:

1. **Add fields to sr22 table**:
   - policy_id, driver_id (foreign keys)
   - case_number, filing_state, effective_date, expiration_date
   - filing_date, document_id, fee_amount
   - is_non_owner

2. **Add fields to sr26 table**:
   - sr22_id (foreign key to original filing)
   - cancellation_date, filing_date, document_id

**Note**: No state submission tracking table needed since documents are generated for the insured, not submitted to state authorities.

## Migration Path

1. Add the new Section E to GR-10
2. Create migration scripts to add missing fields to existing tables
3. Populate type tables with standard type codes (owner, operator, etc.)

## Benefits of This Approach

1. **Complete Documentation**: GR-10 will have full database schema documentation
2. **Business Alignment**: Database structure will support all business requirements
3. **Audit Trail**: Enhanced tables include proper tracking and audit fields
4. **Document Generation**: Support for generating SR22/SR26 documents for insureds

## Risks and Mitigation

1. **Risk**: Existing data in minimal tables
   **Mitigation**: Create careful migration scripts to preserve existing data

2. **Risk**: Missing required fields for document generation
   **Mitigation**: Ensure all fields needed for form population are included

## Next Steps

1. Review this approach with stakeholders
2. Upon approval, update GR-10 with Section E
3. Create migration scripts for table enhancements
4. Update related Global Requirements if needed