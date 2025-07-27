# Accounting Chart of Accounts - Implementation Approach

## Overview

The Chart of Accounts (COA) provides the structural foundation for organizing financial data in the insurance management system. It defines the hierarchical account structure used to categorize all financial transactions, enabling accurate financial reporting, regulatory compliance, and management analysis.

## Core Principles

### 1. Hierarchical Structure
- Parent-child relationships for account groupings
- Flexible depth to support various reporting needs
- Control accounts with mandatory sub-accounts
- Inheritance of account properties from parents

### 2. Account Categorization
- Clear separation by financial statement (Balance Sheet vs Income Statement)
- Standard account types following GAAP principles
- Insurance-specific account classifications
- Support for multi-company consolidation

### 3. Flexibility and Control
- Configuration-driven account properties
- Role-based access to sensitive accounts
- Validation rules to prevent misuse
- Support for account aliases and mappings

## Table Schemas

### 1. Account Table

**Purpose**: Define all general ledger accounts in the system

```sql
CREATE TABLE account (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    account_name VARCHAR(100) NOT NULL,
    account_type_id BIGINT UNSIGNED NOT NULL,
    parent_account_id BIGINT UNSIGNED,
    
    -- Properties moved from account_type per feedback
    normal_balance ENUM('DEBIT', 'CREDIT') NOT NULL,
    financial_statement VARCHAR(50), -- BALANCE_SHEET, INCOME_STATEMENT
    sort_order INT DEFAULT 0,
    
    -- Account configuration
    is_control_account BOOLEAN DEFAULT FALSE,
    requires_sub_account BOOLEAN DEFAULT FALSE,
    allow_manual_entry BOOLEAN DEFAULT TRUE,
    is_cash_account BOOLEAN DEFAULT FALSE,
    
    -- Insurance-specific properties
    is_trust_account BOOLEAN DEFAULT FALSE,
    is_premium_account BOOLEAN DEFAULT FALSE,
    is_claim_account BOOLEAN DEFAULT FALSE,
    
    -- Additional structured settings
    metadata JSON, -- For account-specific configurations
    
    -- Standard audit fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (account_type_id) REFERENCES account_type(id),
    FOREIGN KEY (parent_account_id) REFERENCES account(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    INDEX idx_account_type (account_type_id),
    INDEX idx_parent (parent_account_id),
    INDEX idx_account_number (account_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - no direct existing equivalent

### 2. Account Type Table

**Purpose**: Define the five fundamental account categories

```sql
CREATE TABLE account_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL, -- ASSET, LIABILITY, REVENUE, EXPENSE, EQUITY
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Type properties
    debit_increases BOOLEAN NOT NULL, -- TRUE for Assets/Expenses, FALSE for Liabilities/Revenue/Equity
    
    -- Standard fields
    status_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**This is a NEW table** - defines fundamental accounting categories

## Standard Account Structure

### 1. Asset Accounts (1000-1999)

```
1000 - Assets
├── 1100 - Current Assets
│   ├── 1110 - Cash and Cash Equivalents
│   │   ├── 1111 - Operating Cash
│   │   ├── 1112 - Premium Trust Account
│   │   └── 1113 - Claims Trust Account
│   ├── 1200 - Receivables
│   │   ├── 1210 - Premium Receivables
│   │   ├── 1220 - Commission Receivables
│   │   └── 1230 - Other Receivables
│   └── 1300 - Prepaid Expenses
│       ├── 1310 - Prepaid Insurance
│       └── 1320 - Prepaid Commissions
└── 1500 - Non-Current Assets
    ├── 1510 - Property and Equipment
    └── 1520 - Intangible Assets
```

### 2. Liability Accounts (2000-2999)

```
2000 - Liabilities
├── 2100 - Current Liabilities
│   ├── 2110 - Accounts Payable
│   ├── 2120 - Unearned Premium
│   ├── 2130 - Commission Payable
│   ├── 2140 - Claims Payable
│   └── 2150 - Tax Payable
└── 2500 - Non-Current Liabilities
    └── 2510 - Long-term Debt
```

### 3. Equity Accounts (3000-3999)

```
3000 - Equity
├── 3100 - Capital Stock
├── 3200 - Retained Earnings
└── 3300 - Current Year Earnings
```

### 4. Revenue Accounts (4000-4999)

```
4000 - Revenue
├── 4100 - Premium Revenue
│   ├── 4110 - Written Premium
│   ├── 4120 - Earned Premium
│   └── 4130 - Unearned Premium Change
├── 4200 - Fee Revenue
│   ├── 4210 - Policy Fees
│   ├── 4220 - Installment Fees
│   └── 4230 - Other Fees
└── 4300 - Investment Income
```

### 5. Expense Accounts (5000-5999)

```
5000 - Expenses
├── 5100 - Commission Expense
│   ├── 5110 - Direct Commission
│   └── 5120 - Override Commission
├── 5200 - Operating Expenses
│   ├── 5210 - Salaries and Benefits
│   ├── 5220 - Technology Costs
│   └── 5230 - Professional Fees
├── 5300 - Claims Expense
│   ├── 5310 - Paid Claims
│   └── 5320 - Claims Adjustment Expense
└── 5400 - Tax Expense
```

## Business Rules

### 1. Account Number Assignment
- 4-digit main account numbers
- Hierarchical structure reflected in numbering
- Sub-accounts inherit first digits from parent
- No gaps in critical account ranges

### 2. Control Account Management
- Control accounts cannot have direct transactions
- All entries must go to sub-accounts
- Automatic rollup to control account totals
- Validation of sub-account requirements

### 3. Trust Account Handling
- Segregated premium and claim trust accounts
- Special reconciliation requirements
- Restricted access controls
- Regulatory compliance tracking

### 4. Account Status Management
- Active accounts only for new transactions
- Inactive accounts retained for history
- Archive process for obsolete accounts
- Reactivation workflow when needed

## Integration Points

### 1. With Double-Entry System
- Every transaction line references an account
- Account type determines debit/credit rules
- Normal balance validation
- Control account restrictions enforced

### 2. With Financial Reporting
- Account hierarchy drives report structure
- Financial statement mapping
- Multi-level consolidation support
- Custom grouping capabilities

### 3. With Configuration System
- Program-specific account mappings
- Revenue recognition rules
- Default account assignments
- Closing process configuration

### 4. With Security System
- Role-based account access
- Sensitive account restrictions
- Audit trail requirements
- Approval workflows for changes

## Implementation Considerations

### 1. Initial Setup
- Load standard chart of accounts
- Configure insurance-specific accounts
- Set up trust account requirements
- Define program-specific mappings

### 2. Migration Requirements
- Map existing GL accounts to new structure
- Validate historical transaction mappings
- Preserve audit trail continuity
- Test financial report accuracy

### 3. Maintenance Processes
- Annual account review process
- New account request workflow
- Account modification controls
- Periodic cleanup procedures

## Account Configuration Examples

### 1. Premium Trust Account
```json
{
  "account_number": "1112",
  "metadata": {
    "reconciliation_required": true,
    "reconciliation_frequency": "daily",
    "segregation_type": "premium_trust",
    "regulatory_jurisdiction": "state",
    "restricted_access": true,
    "allowed_transaction_types": ["PREMIUM_RECEIPT", "PREMIUM_DISBURSEMENT"]
  }
}
```

### 2. Commission Expense Account
```json
{
  "account_number": "5110",
  "metadata": {
    "expense_category": "variable",
    "allocation_basis": "premium_written",
    "budget_tracking": true,
    "cost_center_required": false,
    "commission_types": ["NEW_BUSINESS", "RENEWAL"]
  }
}
```

## Cross-References

- **GR-41**: Table schema requirements and naming conventions
- **GR-52**: Entity management for account ownership
- Transaction table for journal entry posting
- Configuration table for account settings

## Validation Rules

### 1. Account Creation
- Unique account number required
- Valid parent account if specified
- Account type must be active
- Normal balance must match type

### 2. Account Hierarchy
- Maximum depth of 5 levels
- Parent must be same account type
- No circular references
- Control accounts at level 2 or 3

### 3. Transaction Posting
- Account must be active
- Not a control account
- Matches transaction requirements
- Passes security checks

## Reporting Capabilities

### 1. Trial Balance
- All accounts with balances
- Grouped by account type
- Control account summaries
- Period comparisons

### 2. Financial Statements
- Automated statement generation
- Multi-level detail options
- Comparative periods
- Consolidation support

### 3. Account Analysis
- Transaction detail by account
- Period-over-period changes
- Budget vs actual (when configured)
- Audit trail reports