# Vehicle Base Rates Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Vehicle Base Rates  
**Category**: Core Rating Component  
**Priority**: Critical - Foundation rates for all premium calculations  
**Implementation Complexity**: Medium  

### Business Requirements Summary
The Vehicle Base Rates factor provides territory-based foundation premium rates that serve as the starting point for all premium calculations. This factor establishes base rates for each coverage type across 12 Texas territories, with rates varying by geographic risk and loss experience.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing and new Global Requirements:

#### Leverages GR-65: Rating Engine Architecture
**Integration**: Base rate lookup within multiplicative calculation engine  
**Dependencies**: RatingEngineService for base rate selection and validation

#### Leverages GR-66: Insurance Risk Assessment Framework
**Integration**: Territory risk assessment and geographic rating validation  
**Dependencies**: Territory assignment and ZIP code validation rules

#### New Requirement: GR-69: Geographic Rating Infrastructure
**Priority**: High  
**Rationale**: Territory management and geographic rating standards needed across programs  

**Core Components**:
- Territory definition and ZIP code mapping standards
- Base rate management and versioning systems
- Geographic risk assessment methodologies
- Multi-state territory expansion patterns

### Integration with Existing Global Requirements
- **GR-41**: Table Schema Requirements - Territory and base rate table structures
- **GR-33**: Data Services Architecture - Territory lookup caching strategies
- **GR-20**: Application Business Logic - Geographic service patterns

---

## 2. Service Architecture Requirements

### Geographic Rating Services

#### TerritoryService
**Purpose**: Territory assignment and management  
**Location**: `app/Domain/Rating/Services/TerritoryService.php`

**Key Methods**:
```php
class TerritoryService
{
    public function getTerritoryByZipCode(string $zipCode, int $programId): Territory
    {
        // 1. Validate ZIP code format
        // 2. Lookup territory mapping with effective date checking
        // 3. Return territory with caching
        // 4. Handle edge cases (new ZIP codes, territory changes)
    }
    
    public function getBaseBratesByTerritory(int $territoryId, array $coverageTypes): array
    {
        // Retrieve base rates for territory and coverage combinations
    }
    
    public function validateTerritoryAssignment(string $zipCode, int $programId): ValidationResult
    {
        // Validate territory assignment rules and eligibility
    }
}
```

#### BaseRateService
**Purpose**: Base rate lookup and management  
**Location**: `app/Domain/Rating/Services/BaseRateService.php`

**Key Methods**:
```php
class BaseRateService
{
    public function getBaseRate(int $territoryId, string $coverageCode, Carbon $effectiveDate): BaseRate
    {
        // Retrieve base rate with version and effective date validation
    }
    
    public function getAllBaseRates(int $programId, Carbon $effectiveDate): Collection
    {
        // Get complete base rate matrix for program
    }
    
    public function validateBaseRateConsistency(int $programId): ValidationResult
    {
        // Validate base rate completeness and consistency
    }
}
```

---

## 3. Database Schema Requirements

### Territory Management Tables

#### rating_territory
```sql
CREATE TABLE rating_territory (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    territory_code VARCHAR(10) NOT NULL,
    territory_name VARCHAR(255) NOT NULL,
    territory_description TEXT,
    state_id BIGINT NOT NULL,
    risk_level ENUM('LOW', 'MODERATE', 'HIGH', 'VERY_HIGH') NOT NULL,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (state_id) REFERENCES state(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_territory_program (program_id, territory_code, effective_date),
    INDEX idx_territory_lookup (territory_code, effective_date),
    INDEX idx_program_territory (program_id, effective_date)
);
```

#### territory_zip_mapping
```sql
CREATE TABLE territory_zip_mapping (
    id BIGINT PRIMARY KEY,
    territory_id BIGINT NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    zip_code_prefix VARCHAR(5) NOT NULL, -- For 5-digit ZIP lookup optimization
    effective_date DATE NOT NULL,
    expiration_date DATE,
    mapping_source VARCHAR(100), -- Manual, Import, API
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (territory_id) REFERENCES rating_territory(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_zip_mapping (zip_code, effective_date),
    INDEX idx_zip_lookup (zip_code, effective_date),
    INDEX idx_zip_prefix (zip_code_prefix, effective_date),
    INDEX idx_territory_mapping (territory_id, effective_date)
);
```

### Base Rate Management Tables

#### base_rate_schedule
```sql
CREATE TABLE base_rate_schedule (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    schedule_name VARCHAR(255) NOT NULL,
    schedule_version VARCHAR(50) NOT NULL,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    filing_number VARCHAR(100),
    approval_date DATE,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_schedule_version (program_id, schedule_version, effective_date),
    INDEX idx_schedule_effective (effective_date, expiration_date),
    INDEX idx_filing_lookup (filing_number)
);
```

#### base_rate
```sql
CREATE TABLE base_rate (
    id BIGINT PRIMARY KEY,
    schedule_id BIGINT NOT NULL,
    territory_id BIGINT NOT NULL,
    coverage_code VARCHAR(50) NOT NULL,
    term_months INT NOT NULL DEFAULT 6,
    base_rate_amount DECIMAL(10,2) NOT NULL,
    rate_per_exposure DECIMAL(8,4), -- For unit-based coverages
    minimum_premium DECIMAL(8,2),
    maximum_premium DECIMAL(10,2),
    rate_metadata JSON,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (schedule_id) REFERENCES base_rate_schedule(id),
    FOREIGN KEY (territory_id) REFERENCES rating_territory(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_territory_coverage_rate (schedule_id, territory_id, coverage_code, term_months),
    INDEX idx_territory_coverage (territory_id, coverage_code),
    INDEX idx_schedule_rates (schedule_id, territory_id),
    INDEX idx_coverage_rates (coverage_code, territory_id)
);
```

#### coverage_type
```sql
CREATE TABLE coverage_type (
    id BIGINT PRIMARY KEY,
    coverage_code VARCHAR(50) UNIQUE NOT NULL,
    coverage_name VARCHAR(255) NOT NULL,
    coverage_description TEXT,
    coverage_category ENUM('LIABILITY', 'PHYSICAL_DAMAGE', 'OTHER') NOT NULL,
    is_required BOOLEAN DEFAULT FALSE,
    has_limits BOOLEAN DEFAULT TRUE,
    has_deductible BOOLEAN DEFAULT FALSE,
    calculation_basis ENUM('FLAT', 'PER_VEHICLE', 'PER_DRIVER', 'COMBINED') NOT NULL,
    sort_order INT DEFAULT 0,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_coverage_category (coverage_category),
    INDEX idx_coverage_active (status_id, sort_order)
);
```

---

## 4. Business Logic Requirements

### Territory Assignment Logic

#### ZIP Code Territory Resolution
```php
class TerritoryService
{
    public function getTerritoryByZipCode(string $zipCode, int $programId): Territory
    {
        // 1. Clean and validate ZIP code format
        $cleanZip = $this->validateAndCleanZipCode($zipCode);
        
        // 2. Check cache for recent lookup
        $cacheKey = "territory_{$programId}_{$cleanZip}";
        if ($cached = Cache::get($cacheKey)) {
            return $cached;
        }
        
        // 3. Query territory mapping with effective date
        $mapping = DB::table('territory_zip_mapping')
            ->join('rating_territory', 'territory_zip_mapping.territory_id', '=', 'rating_territory.id')
            ->where('territory_zip_mapping.zip_code', $cleanZip)
            ->where('rating_territory.program_id', $programId)
            ->where('territory_zip_mapping.effective_date', '<=', now())
            ->where(function($query) {
                $query->whereNull('territory_zip_mapping.expiration_date')
                      ->orWhere('territory_zip_mapping.expiration_date', '>', now());
            })
            ->where('rating_territory.status_id', Status::ACTIVE)
            ->first();
            
        // 4. Handle missing territory mapping
        if (!$mapping) {
            throw new TerritoryNotFoundException("No territory found for ZIP code: {$cleanZip}");
        }
        
        // 5. Cache result and return
        $territory = new Territory($mapping);
        Cache::put($cacheKey, $territory, 3600); // 1-hour cache
        
        return $territory;
    }
}
```

### Base Rate Lookup Logic

#### Coverage Base Rate Retrieval
```php
class BaseRateService
{
    public function getBaseRate(int $territoryId, string $coverageCode, Carbon $effectiveDate): BaseRate
    {
        // 1. Find active rate schedule for effective date
        $schedule = DB::table('base_rate_schedule')
            ->where('effective_date', '<=', $effectiveDate)
            ->where(function($query) use ($effectiveDate) {
                $query->whereNull('expiration_date')
                      ->orWhere('expiration_date', '>', $effectiveDate);
            })
            ->where('status_id', Status::ACTIVE)
            ->orderBy('effective_date', 'DESC')
            ->first();
            
        if (!$schedule) {
            throw new BaseRateNotFoundException("No active rate schedule for date: {$effectiveDate}");
        }
        
        // 2. Retrieve base rate for territory and coverage
        $baseRate = DB::table('base_rate')
            ->where('schedule_id', $schedule->id)
            ->where('territory_id', $territoryId)
            ->where('coverage_code', $coverageCode)
            ->where('status_id', Status::ACTIVE)
            ->first();
            
        if (!$baseRate) {
            throw new BaseRateNotFoundException(
                "No base rate found for territory {$territoryId}, coverage {$coverageCode}"
            );
        }
        
        return new BaseRate($baseRate);
    }
}
```

### Aguila Dorada Territory Structure

#### 12-Territory Texas Framework
```php
// Territory configuration for Aguila Dorada program
const AGUILA_DORADA_TERRITORIES = [
    '01' => ['name' => 'Houston Metropolitan', 'risk_level' => 'VERY_HIGH'],
    '02' => ['name' => 'Dallas-Fort Worth', 'risk_level' => 'VERY_HIGH'],
    '03' => ['name' => 'San Antonio Metropolitan', 'risk_level' => 'HIGH'],
    '04' => ['name' => 'Austin Metropolitan', 'risk_level' => 'HIGH'],
    '05' => ['name' => 'El Paso County', 'risk_level' => 'MODERATE'],
    '06' => ['name' => 'Corpus Christi Coastal', 'risk_level' => 'HIGH'],
    '07' => ['name' => 'East Texas Rural', 'risk_level' => 'MODERATE'],
    '08' => ['name' => 'West Texas Rural', 'risk_level' => 'LOW'],
    '09' => ['name' => 'Central Texas Rural', 'risk_level' => 'MODERATE'],
    '10' => ['name' => 'South Texas Border', 'risk_level' => 'HIGH'],
    '11' => ['name' => 'North Texas Rural', 'risk_level' => 'MODERATE'],
    '12' => ['name' => 'Panhandle Rural', 'risk_level' => 'LOW']
];
```

---

## 5. Caching Strategy

### Territory Lookup Optimization
```php
// Multi-tier territory caching
class TerritoryService
{
    public function getTerritoryByZipCode(string $zipCode, int $programId): Territory
    {
        // L1 Cache - Application memory (5 minutes)
        $l1Key = "territory_l1_{$programId}_{$zipCode}";
        if ($this->appCache->has($l1Key)) {
            return $this->appCache->get($l1Key);
        }
        
        // L2 Cache - Redis (1 hour)
        $l2Key = "territory_l2_{$programId}_{$zipCode}";
        if ($territory = Cache::get($l2Key)) {
            $this->appCache->put($l1Key, $territory, 300);
            return $territory;
        }
        
        // L3 Cache - Database lookup with caching
        $territory = $this->lookupTerritoryFromDatabase($zipCode, $programId);
        
        Cache::put($l2Key, $territory, 3600);
        $this->appCache->put($l1Key, $territory, 300);
        
        return $territory;
    }
}
```

### Base Rate Caching
```php
// Base rate matrix caching
class BaseRateService
{
    public function getAllBaseRates(int $programId, Carbon $effectiveDate): Collection
    {
        $cacheKey = "base_rates_{$programId}_{$effectiveDate->format('Y-m-d')}";
        
        return Cache::remember($cacheKey, 14400, function() use ($programId, $effectiveDate) {
            return $this->loadBaseRateMatrix($programId, $effectiveDate);
        });
    }
}
```

---

## 6. API Integration Requirements

### Territory and Base Rate Endpoints
```php
// Geographic rating API endpoints
GET /api/v1/rating/territory/{zipCode}
// Returns territory assignment for ZIP code

GET /api/v1/rating/base-rates/{territoryId}
// Returns base rates for territory

POST /api/v1/rating/territory/validate
{
    "zip_codes": ["78701", "77001", "75201"],
    "program_id": 1
}
// Bulk territory validation

GET /api/v1/admin/territories/{programId}
// Administrative territory management
```

### Response Formats
```json
// Territory lookup response
{
    "territory_id": 123,
    "territory_code": "01",
    "territory_name": "Houston Metropolitan",
    "risk_level": "VERY_HIGH",
    "effective_date": "2025-07-15",
    "base_rates": {
        "LIABILITY": 450.00,
        "COMPREHENSIVE": 180.00,
        "COLLISION": 275.00,
        "PIP": 85.00
    }
}

// Base rate matrix response
{
    "program_id": 1,
    "schedule_version": "2025.1",
    "effective_date": "2025-07-15",
    "territories": [
        {
            "territory_code": "01",
            "coverage_rates": {
                "LIABILITY": 450.00,
                "COMPREHENSIVE": 180.00,
                "COLLISION": 275.00
            }
        }
    ]
}
```

---

## 7. Validation Requirements

### Territory Assignment Validation
```php
class TerritoryValidator
{
    public function validateZipCode(string $zipCode): ValidationResult
    {
        // 1. Format validation (5 or 9 digit ZIP)
        // 2. USPS ZIP code existence validation
        // 3. Texas state boundary validation
        // 4. Program territory coverage validation
    }
    
    public function validateTerritoryAssignment(int $territoryId, int $programId): ValidationResult
    {
        // 1. Territory exists and is active
        // 2. Territory belongs to program
        // 3. Territory has complete base rate coverage
        // 4. Territory effective date validation
    }
}
```

### Base Rate Validation
```php
class BaseRateValidator
{
    public function validateRateSchedule(int $scheduleId): ValidationResult
    {
        // 1. Complete territory coverage validation
        // 2. Required coverage type validation
        // 3. Rate reasonableness validation
        // 4. Regulatory filing compliance validation
    }
}
```

---

## 8. Performance Requirements

### Lookup Performance Targets
- **Territory Lookup**: <100ms for ZIP code to territory resolution
- **Base Rate Retrieval**: <50ms for individual coverage base rate
- **Bulk Operations**: <500ms for complete territory matrix lookup
- **Cache Hit Ratio**: >95% for territory lookups during normal operations

### Database Optimization
```sql
-- Optimized ZIP code lookup index
CREATE INDEX idx_zip_lookup_optimized 
ON territory_zip_mapping (zip_code, effective_date, territory_id) 
WHERE status_id = 1;

-- Territory base rate lookup optimization
CREATE INDEX idx_territory_coverage_lookup 
ON base_rate (territory_id, coverage_code, schedule_id) 
WHERE status_id = 1;
```

---

## 9. Regulatory Compliance

### Rate Filing Integration
- **Filing Numbers**: All base rate schedules linked to regulatory filings
- **Effective Date Tracking**: Precise effective date management for rate changes
- **Approval Validation**: Base rates only active after regulatory approval
- **Historical Retention**: 7-year retention of all rate schedules and changes

### Actuarial Support
- **Rate Justification**: Statistical basis for territory assignments
- **Loss Experience**: Territory risk levels based on historical loss data
- **Geographic Analysis**: ZIP code assignments based on loss experience
- **Rate Adequacy**: Regular validation of base rate adequacy

---

## 10. Testing Requirements

### Unit Testing
```php
class TerritoryServiceTest extends TestCase
{
    public function test_zip_code_territory_assignment()
    {
        // Test accurate territory assignment for known ZIP codes
    }
    
    public function test_base_rate_lookup_accuracy()
    {
        // Test base rate retrieval for all territory/coverage combinations
    }
    
    public function test_effective_date_handling()
    {
        // Test proper handling of rate schedule effective dates
    }
}
```

### Integration Testing
- **ZIP Code Coverage**: Test all Aguila Dorada territory ZIP codes
- **Rate Schedule Integration**: Test rate schedule transitions
- **Cache Performance**: Test caching effectiveness and invalidation

---

## Implementation Priority: CRITICAL
This factor must be implemented early as it provides the foundation rates for all premium calculations. All other factors multiply against these base rates.

## Dependencies
- **Algorithm Factor**: Requires core rating engine for base rate lookup
- **Required for**: All other rating factors depend on base rate foundation

## Estimated Implementation Effort
- **Database Schema**: 3 days
- **Service Layer**: 4 days
- **Territory Data Import**: 2 days
- **API Integration**: 2 days
- **Testing**: 3 days
- **Total**: 14 days

This plan establishes the geographic foundation for all premium calculations, ensuring accurate territory assignment and regulatory-compliant base rate management.