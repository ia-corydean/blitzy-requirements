# GR-64 Database Alignment Approach: Policy Reinstatement with Lapse Process
- lets discuss reinstatements just being a transaction_type for the policy.
    - would this ne a simpler apporach and how would we acoomplish using transaction and transaction_line and transaction_type table

## Current State Analysis

### Tables Found in Database

1. **policy** - EXISTS
   - Has reinstatement_date field ✓
   - Has cancellation_date and cancellation_reason_id fields ✓
   - Has premium and payment-related fields ✓
   - **MISSING**: reinstatement_eligibility fields

2. **reinstatement** - EXISTS (basic structure)
   - Current: id, reinstatement_type_id, status_id, created_by, updated_by, created_at, updated_at
   - **NOT MATCHING** the reinstatement_calculation table specified in GR-64

3. **cancellation_reason** - EXISTS
   - Good structure with code, name, category
   - Can be used to determine reinstatement eligibility

4. **status** - EXISTS
   - Need to add reinstatement-specific statuses

### Missing Tables/Features

1. **reinstatement_calculation** - Required detailed calculation table doesn't exist
2. **reinstatement_eligibility** - No dedicated eligibility tracking
3. **payment_schedule** - May need restructuring capabilities

## Key Differences from GR-64 Requirements

### 1. Policy Table
**Current State:**
- Has reinstatement_date field
- Basic cancellation tracking

**GR-64 Requirements:**
- Need eligibility tracking fields
- Need reinstatement window expiration date
- Need eligibility status field

### 2. Reinstatement Calculation
**Current State:**
- Basic reinstatement table with minimal fields

**GR-64 Requirements:**
- Detailed calculation table with:
  - Lapse period tracking
  - Premium breakdown
  - Daily rate calculations
  - Fee tracking
  - Payment requirements

### 3. Status Management
**Current State:**
- Basic status table exists

**GR-64 Requirements:**
- Need specific reinstatement statuses:
  - ELIGIBLE_FOR_REINSTATEMENT
  - REINSTATED
  - EXPIRED_REINSTATEMENT

### 4. Action Tracking
**Current State:**
- Action table exists but lacks specific fields

**GR-64 Requirements:**
- Need reinstatement-specific action types
- Detailed audit trail for reinstatement process

## Proposed Updates

### 1. Update Policy Table
```sql
ALTER TABLE policy
ADD COLUMN reinstatement_eligible BOOLEAN DEFAULT FALSE,
ADD COLUMN reinstatement_window_expires DATE,
ADD COLUMN reinstatement_calculation_id INT,
    - see the updates provided in [GR-41-database-alignment-approach.md](../approaches/GR-41-database-alignment-approach.md)
ADD INDEX idx_reinstatement_eligible (reinstatement_eligible),
ADD INDEX idx_reinstatement_expires (reinstatement_window_expires);
```

### 2. Create Reinstatement Calculation Table
```sql
-- Drop and recreate with proper structure
DROP TABLE IF EXISTS reinstatement;

CREATE TABLE reinstatement_calculation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    policy_id INT NOT NULL,
    
    -- Calculation details
    cancellation_date DATE NOT NULL,
    reinstatement_date DATE NOT NULL,
    lapse_days INT NOT NULL,
    
    -- Premium breakdown
    original_premium DECIMAL(10,2) NOT NULL,
    daily_premium_rate DECIMAL(8,4) NOT NULL,
    lapsed_premium DECIMAL(10,2) NOT NULL,
    adjusted_premium DECIMAL(10,2) NOT NULL,
    unpaid_premium DECIMAL(10,2) DEFAULT 0,
    reinstatement_fees DECIMAL(10,2) DEFAULT 0,
    total_due DECIMAL(10,2) NOT NULL,
    
    -- SR22 specific fields
    includes_sr22 BOOLEAN DEFAULT FALSE,
    sr22_fee DECIMAL(10,2) DEFAULT 0,
    
    -- Status and audit
    status_id INT NOT NULL,
    created_by INT NOT NULL,
    updated_by INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id),
    
    -- Indexes
    INDEX idx_policy (policy_id),
    INDEX idx_reinstatement_date (reinstatement_date),
    INDEX idx_status (status_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 3. Add Reinstatement Status Values
```sql
-- Check if status_type table has POLICY type
INSERT INTO status_type (code, name, description) VALUES 
('POLICY', 'Policy Status', 'Status values for policy lifecycle')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- Add reinstatement-specific statuses
INSERT INTO status (status_type_id, code, name, description) VALUES
((SELECT id FROM status_type WHERE code = 'POLICY'), 'ELIGIBLE_FOR_REINSTATEMENT', 'Eligible for Reinstatement', 'Policy cancelled but within reinstatement window'),
((SELECT id FROM status_type WHERE code = 'POLICY'), 'REINSTATED', 'Reinstated', 'Policy successfully reinstated after cancellation'),
((SELECT id FROM status_type WHERE code = 'POLICY'), 'EXPIRED_REINSTATEMENT', 'Reinstatement Expired', 'Policy reinstatement window has expired');
```

### 4. Add Reinstatement Action Types
```sql
-- Add to action_type table
INSERT INTO action_type (code, name, description) VALUES
('POLICY_REINSTATEMENT_ELIGIBILITY_EVALUATED', 'Reinstatement Eligibility Evaluated', 'System evaluated policy reinstatement eligibility'),
('POLICY_REINSTATEMENT_CALCULATION_PERFORMED', 'Reinstatement Calculation Performed', 'System calculated reinstatement premium and fees'),
('POLICY_REINSTATEMENT_PAYMENT_RECEIVED', 'Reinstatement Payment Received', 'Payment received for policy reinstatement'),
('POLICY_REINSTATEMENT_COMPLETED', 'Reinstatement Completed', 'Policy successfully reinstated'),
('POLICY_REINSTATEMENT_FAILED', 'Reinstatement Failed', 'Policy reinstatement process failed'),
('POLICY_REINSTATEMENT_ELIGIBILITY_EXPIRED', 'Reinstatement Eligibility Expired', 'Reinstatement window has expired');
```

### 5. Create Reinstatement Configuration Table
```sql
CREATE TABLE reinstatement_config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    program_id INT NOT NULL,
    eligible_cancellation_reasons JSON COMMENT 'Array of cancellation reason codes',
    reinstatement_window_days INT NOT NULL DEFAULT 30,
    reinstatement_fee DECIMAL(10,2) DEFAULT 0,
    allow_backdating BOOLEAN DEFAULT FALSE,
    require_full_payment BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES program(id),
    UNIQUE KEY uk_program (program_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 6. Payment Schedule Restructuring Support
```sql
-- Add fields to track payment restructuring
ALTER TABLE payment_plan
ADD COLUMN supports_restructuring BOOLEAN DEFAULT TRUE,
ADD COLUMN min_payments_remaining INT DEFAULT 1;

-- Create payment schedule adjustment table
CREATE TABLE payment_schedule_adjustment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    policy_id INT NOT NULL,
    adjustment_type VARCHAR(50) NOT NULL, -- 'REINSTATEMENT', 'ENDORSEMENT', etc.
    adjustment_date DATE NOT NULL,
    original_schedule JSON,
    new_schedule JSON,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (policy_id) REFERENCES policy(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    INDEX idx_policy (policy_id),
    INDEX idx_adjustment_date (adjustment_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## Implementation Considerations

### 1. SR22 Integration
- Ensure SR22 status is maintained during reinstatement
- Include SR22 fees in reinstatement calculations
- No new SR22 filing required for reinstatement

### 2. Workflow Integration
- Implement state transitions in workflow engine
- Add time-based triggers for eligibility expiration
- Create automated status update jobs

### 3. Business Logic Services
- Create ReinstatementService implementing interface from GR-64
- Implement daily rate calculation methodology
- Add payment schedule restructuring logic

### 4. Performance Optimization
- Index reinstatement eligibility fields for quick queries
- Optimize calculation queries
- Consider caching for frequently accessed configs

## Data Migration Strategy

### 1. Existing Reinstatement Data
- Preserve existing reinstatement table data
- Map to new reinstatement_calculation structure
- Maintain data integrity during transition

### 2. Policy Status Updates
- Identify cancelled policies within reinstatement window
- Update reinstatement_eligible flag
- Calculate and set reinstatement_window_expires

### 3. Configuration Setup
- Create default reinstatement configurations per program
- Set Aguila Dorada specific settings (30 days, nonpayment only)
- Configure reinstatement fees

## Testing Requirements

### 1. Unit Tests
- Daily rate calculations
- Eligibility determination logic
- Payment schedule restructuring

### 2. Integration Tests
- Full reinstatement workflow
- Payment processing integration
- Status transition handling

### 3. Performance Tests
- Eligibility queries under load
- Calculation performance
- Concurrent reinstatement processing

## Next Steps
1. Review and approve schema changes
2. Create database migrations in order
3. Implement ReinstatementService
4. Add reinstatement API endpoints
5. Create frontend components for reinstatement flow
6. Configure program-specific rules
7. Implement automated eligibility expiration job
8. Add comprehensive testing suite