# Vehicle Make Model Plan
## Aguila Dorada Texas Personal Auto Program

### Factor Overview
**Factor Name**: Vehicle Make Model  
**Category**: Vehicle Factor  
**Priority**: High - Vehicle-specific risk assessment  
**Implementation Complexity**: High  

### Business Requirements Summary
The Vehicle Make Model factor implements risk-based pricing adjustments based on the specific make, model, and potentially trim level of insured vehicles. This factor reflects the statistical correlation between specific vehicle makes/models and claim frequency, severity, theft rates, safety ratings, repair costs, and overall risk characteristics that vary significantly between different vehicle manufacturers and models.

---

## 1. Global Requirements Analysis

### Required Global Requirements
This factor integrates with existing and new Global Requirements:

#### Leverages GR-65: Rating Engine Architecture
**Integration**: Vehicle make/model factor calculation within multiplicative rating engine  
**Dependencies**: RatingEngineService for make/model-specific factor lookup and validation

#### Leverages GR-53: DCS Integration Architecture
**Integration**: Vehicle make/model verification through VIN decoding and vehicle data services  
**Dependencies**: VIN decoding for accurate make/model/year determination

#### New Requirement: GR-84: Vehicle Make Model Classification Standards
**Priority**: High  
**Rationale**: Vehicle make/model classification and risk assessment methodology  

**Core Components**:
- Vehicle make/model standardization and normalization standards
- VIN decoding integration and make/model verification
- Risk classification methodology based on vehicle characteristics
- Safety rating integration and impact on factors
- Theft risk assessment and anti-theft device recognition
- Repair cost correlation and parts availability assessment
- Make/model factor versioning and historical tracking

### Integration with Existing Global Requirements
- **GR-41**: Table Schema Requirements - Vehicle make/model classification tables
- **GR-20**: Application Business Logic - Make/model classification service patterns
- **GR-33**: Data Services Architecture - VIN decoding and vehicle data caching

---

## 2. Service Architecture Requirements

### Vehicle Make Model Services

#### VehicleMakeModelService
**Purpose**: Vehicle make/model classification and factor determination  
**Location**: `app/Domain/Rating/Services/VehicleMakeModelService.php`

**Key Methods**:
```php
class VehicleMakeModelService
{
    public function calculateMakeModelFactor(VehicleMakeModelData $vehicleData): MakeModelFactor
    {
        // 1. Standardize and verify make/model information
        // 2. Classify vehicle into risk category based on make/model
        // 3. Assess safety ratings, theft risk, and repair costs
        // 4. Lookup make/model-specific factors by coverage type
        // 5. Apply anti-theft device discounts if applicable
        // 6. Return factor with detailed risk breakdown
    }
    
    public function classifyVehicleRisk(VehicleMakeModelData $vehicleData): VehicleRiskClassification
    {
        // Classify vehicle into risk categories based on make/model characteristics
    }
    
    public function standardizeMakeModel(string $make, string $model): StandardizedVehicle
    {
        // Standardize make/model names using industry standards
    }
    
    public function getVehicleCharacteristics(string $vin): VehicleCharacteristics
    {
        // Get comprehensive vehicle characteristics from VIN
    }
}
```

#### VINDecodingService
**Purpose**: VIN decoding and vehicle data verification  
**Location**: `app/Domain/Rating/Services/VINDecodingService.php`

**Key Methods**:
```php
class VINDecodingService
{
    public function decodeVIN(string $vin): VINDecodingResult
    {
        // Decode VIN to extract make, model, year, and other characteristics
    }
    
    public function verifyVehicleData(VehicleData $vehicleData): VehicleVerificationResult
    {
        // Verify vehicle data consistency against VIN decoding
    }
    
    public function getVehicleSpecs(string $vin): VehicleSpecifications
    {
        // Get detailed vehicle specifications and equipment
    }
}
```

#### VehicleRiskAssessmentService
**Purpose**: Comprehensive vehicle risk assessment  
**Location**: `app/Domain/Rating/Services/VehicleRiskAssessmentService.php`

**Key Methods**:
```php
class VehicleRiskAssessmentService
{
    public function assessTheftRisk(VehicleMakeModelData $vehicleData): TheftRiskAssessment
    {
        // Assess theft risk based on make/model theft statistics
    }
    
    public function assessSafetyRisk(VehicleMakeModelData $vehicleData): SafetyRiskAssessment
    {
        // Assess safety risk based on IIHS/NHTSA ratings
    }
    
    public function assessRepairCostRisk(VehicleMakeModelData $vehicleData): RepairCostAssessment
    {
        // Assess repair cost risk based on parts availability and labor complexity
    }
}
```

---

## 3. Database Schema Requirements

### Vehicle Make Model Management Tables

#### vehicle_make
```sql
CREATE TABLE vehicle_make (
    id BIGINT PRIMARY KEY,
    make_code VARCHAR(50) UNIQUE NOT NULL,
    make_name VARCHAR(255) NOT NULL,
    make_name_standardized VARCHAR(255) NOT NULL,
    manufacturer_group VARCHAR(255), -- Parent company (e.g., General Motors, Volkswagen Group)
    country_of_origin VARCHAR(100),
    luxury_brand BOOLEAN DEFAULT FALSE,
    risk_level ENUM('LOW', 'MODERATE', 'HIGH', 'VERY_HIGH') NOT NULL DEFAULT 'MODERATE',
    theft_susceptibility ENUM('LOW', 'MODERATE', 'HIGH', 'VERY_HIGH') NOT NULL DEFAULT 'MODERATE',
    repair_cost_factor DECIMAL(6,4) DEFAULT 1.0000,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_make_standardized (make_name_standardized),
    INDEX idx_manufacturer_group (manufacturer_group),
    INDEX idx_risk_level (risk_level, status_id),
    INDEX idx_theft_susceptibility (theft_susceptibility),
    INDEX idx_luxury_brand (luxury_brand, status_id)
);

-- Sample vehicle makes
INSERT INTO vehicle_make (make_code, make_name, make_name_standardized, manufacturer_group, country_of_origin, luxury_brand, risk_level, theft_susceptibility, repair_cost_factor) VALUES
('HONDA', 'Honda', 'HONDA', 'Honda Motor Co.', 'Japan', FALSE, 'LOW', 'MODERATE', 0.9500),
('TOYOTA', 'Toyota', 'TOYOTA', 'Toyota Motor Corp.', 'Japan', FALSE, 'LOW', 'LOW', 0.9000),
('FORD', 'Ford', 'FORD', 'Ford Motor Company', 'USA', FALSE, 'MODERATE', 'MODERATE', 1.0000),
('CHEVROLET', 'Chevrolet', 'CHEVROLET', 'General Motors', 'USA', FALSE, 'MODERATE', 'MODERATE', 1.0000),
('BMW', 'BMW', 'BMW', 'BMW Group', 'Germany', TRUE, 'HIGH', 'VERY_HIGH', 1.4000),
('MERCEDES', 'Mercedes-Benz', 'MERCEDES-BENZ', 'Mercedes-Benz Group', 'Germany', TRUE, 'HIGH', 'VERY_HIGH', 1.5000),
('DODGE', 'Dodge', 'DODGE', 'Stellantis', 'USA', FALSE, 'HIGH', 'HIGH', 1.2000),
('JEEP', 'Jeep', 'JEEP', 'Stellantis', 'USA', FALSE, 'MODERATE', 'HIGH', 1.1000);
```

#### vehicle_model
```sql
CREATE TABLE vehicle_model (
    id BIGINT PRIMARY KEY,
    make_id BIGINT NOT NULL,
    model_code VARCHAR(50) NOT NULL,
    model_name VARCHAR(255) NOT NULL,
    model_name_standardized VARCHAR(255) NOT NULL,
    body_style ENUM('SEDAN', 'COUPE', 'HATCHBACK', 'SUV', 'TRUCK', 'CONVERTIBLE', 'WAGON', 'VAN', 'OTHER') NOT NULL,
    vehicle_segment ENUM('SUBCOMPACT', 'COMPACT', 'MIDSIZE', 'FULLSIZE', 'LUXURY', 'SPORTS', 'TRUCK', 'SUV') NOT NULL,
    performance_category ENUM('ECONOMY', 'STANDARD', 'SPORT', 'HIGH_PERFORMANCE', 'EXOTIC') NOT NULL DEFAULT 'STANDARD',
    safety_rating_iihs VARCHAR(20), -- IIHS Top Safety Pick, etc.
    safety_rating_nhtsa DECIMAL(2,1), -- NHTSA 5-star rating
    anti_theft_features JSON, -- Array of standard anti-theft features
    repair_complexity ENUM('LOW', 'MODERATE', 'HIGH', 'VERY_HIGH') NOT NULL DEFAULT 'MODERATE',
    parts_availability ENUM('EXCELLENT', 'GOOD', 'FAIR', 'POOR') NOT NULL DEFAULT 'GOOD',
    theft_target_rating ENUM('LOW', 'MODERATE', 'HIGH', 'VERY_HIGH') NOT NULL DEFAULT 'MODERATE',
    base_factor DECIMAL(6,4) NOT NULL DEFAULT 1.0000,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (make_id) REFERENCES vehicle_make(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_make_model (make_id, model_code),
    INDEX idx_model_standardized (model_name_standardized),
    INDEX idx_body_style (body_style, vehicle_segment),
    INDEX idx_performance_category (performance_category),
    INDEX idx_safety_ratings (safety_rating_nhtsa, safety_rating_iihs),
    INDEX idx_theft_rating (theft_target_rating),
    INDEX idx_repair_complexity (repair_complexity, parts_availability)
);
```

#### vehicle_make_model_factor
```sql
CREATE TABLE vehicle_make_model_factor (
    id BIGINT PRIMARY KEY,
    program_id BIGINT NOT NULL,
    make_id BIGINT,
    model_id BIGINT,
    coverage_type_id BIGINT, -- NULL for all coverages
    model_year_min INT, -- Minimum model year for this factor
    model_year_max INT, -- Maximum model year for this factor
    factor_value DECIMAL(6,4) NOT NULL,
    factor_type ENUM('MAKE_ONLY', 'MODEL_SPECIFIC', 'YEAR_RANGE') NOT NULL,
    risk_justification TEXT,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    actuarial_support_data JSON,
    status_id BIGINT NOT NULL,
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (program_id) REFERENCES program(id),
    FOREIGN KEY (make_id) REFERENCES vehicle_make(id),
    FOREIGN KEY (model_id) REFERENCES vehicle_model(id),
    FOREIGN KEY (coverage_type_id) REFERENCES coverage_type(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    UNIQUE KEY unique_make_model_factor (
        program_id, 
        make_id, 
        model_id, 
        coverage_type_id, 
        model_year_min,
        model_year_max,
        effective_date
    ),
    INDEX idx_program_make_factors (program_id, make_id),
    INDEX idx_program_model_factors (program_id, model_id),
    INDEX idx_coverage_factors (coverage_type_id, factor_value),
    INDEX idx_model_year_range (model_year_min, model_year_max),
    INDEX idx_effective_dates (effective_date, expiration_date)
);
```

#### vehicle_anti_theft_device
```sql
CREATE TABLE vehicle_anti_theft_device (
    id BIGINT PRIMARY KEY,
    device_code VARCHAR(50) UNIQUE NOT NULL,
    device_name VARCHAR(255) NOT NULL,
    device_description TEXT,
    device_type ENUM('PASSIVE', 'ACTIVE', 'RECOVERY', 'IMMOBILIZER', 'ALARM') NOT NULL,
    effectiveness_rating ENUM('LOW', 'MODERATE', 'HIGH', 'VERY_HIGH') NOT NULL,
    discount_factor DECIMAL(6,4) NOT NULL DEFAULT 1.0000,
    verification_required BOOLEAN DEFAULT FALSE,
    applicable_coverage_types JSON, -- Array of coverage types this applies to
    manufacturer_standard BOOLEAN DEFAULT FALSE, -- True if standard equipment
    aftermarket_available BOOLEAN DEFAULT TRUE,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_device_type (device_type, effectiveness_rating),
    INDEX idx_discount_factor (discount_factor),
    INDEX idx_verification_required (verification_required, status_id)
);

-- Sample anti-theft devices
INSERT INTO vehicle_anti_theft_device (device_code, device_name, device_type, effectiveness_rating, discount_factor, verification_required, applicable_coverage_types, manufacturer_standard) VALUES
('FACTORY_ALARM', 'Factory Alarm System', 'ACTIVE', 'MODERATE', 0.9500, FALSE, '["COMPREHENSIVE", "COLLISION"]', TRUE),
('AFTERMARKET_ALARM', 'Aftermarket Alarm System', 'ACTIVE', 'MODERATE', 0.9500, TRUE, '["COMPREHENSIVE", "COLLISION"]', FALSE),
('LOJACK', 'LoJack Recovery System', 'RECOVERY', 'VERY_HIGH', 0.8500, TRUE, '["COMPREHENSIVE"]', FALSE),
('IMMOBILIZER', 'Engine Immobilizer', 'IMMOBILIZER', 'HIGH', 0.9000, FALSE, '["COMPREHENSIVE"]', TRUE),
('GPS_TRACKING', 'GPS Tracking System', 'RECOVERY', 'HIGH', 0.9000, TRUE, '["COMPREHENSIVE"]', FALSE),
('PASSIVE_DISABLE', 'Passive Disabling Device', 'PASSIVE', 'MODERATE', 0.9500, FALSE, '["COMPREHENSIVE"]', TRUE);
```

#### vehicle_vin_decode_cache
```sql
CREATE TABLE vehicle_vin_decode_cache (
    id BIGINT PRIMARY KEY,
    vin VARCHAR(17) UNIQUE NOT NULL,
    make_id BIGINT,
    model_id BIGINT,
    model_year INT NOT NULL,
    body_style VARCHAR(100),
    engine_size VARCHAR(50),
    fuel_type VARCHAR(50),
    transmission_type VARCHAR(50),
    drive_type VARCHAR(50),
    trim_level VARCHAR(100),
    standard_equipment JSON,
    decode_source VARCHAR(100) NOT NULL,
    decode_date DATE NOT NULL,
    decode_confidence ENUM('HIGH', 'MEDIUM', 'LOW') NOT NULL,
    raw_decode_data JSON,
    status_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (make_id) REFERENCES vehicle_make(id),
    FOREIGN KEY (model_id) REFERENCES vehicle_model(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    
    INDEX idx_vin_lookup (vin),
    INDEX idx_make_model_year (make_id, model_id, model_year),
    INDEX idx_decode_date (decode_date, decode_confidence),
    INDEX idx_decode_source (decode_source, decode_confidence)
);
```

---

## 4. Business Logic Requirements

### Make Model Factor Calculation
```php
class VehicleMakeModelService
{
    public function calculateMakeModelFactor(VehicleMakeModelData $vehicleData): MakeModelFactor
    {
        // 1. Standardize make/model data
        $standardizedVehicle = $this->standardizeMakeModel(
            $vehicleData->make, 
            $vehicleData->model
        );
        
        // 2. Get base make/model factors
        $baseFactors = $this->getBaseMakeModelFactors(
            $standardizedVehicle, 
            $vehicleData->model_year,
            $vehicleData->coverage_types
        );
        
        // 3. Apply anti-theft device discounts
        $antiTheftAdjustments = $this->calculateAntiTheftDiscounts(
            $vehicleData->anti_theft_devices,
            $vehicleData->coverage_types
        );
        
        // 4. Apply safety rating adjustments
        $safetyAdjustments = $this->calculateSafetyAdjustments($standardizedVehicle);
        
        // 5. Calculate final factors
        $finalFactors = [];
        foreach ($baseFactors as $coverage => $baseFactor) {
            $antiTheftFactor = $antiTheftAdjustments[$coverage] ?? 1.0000;
            $safetyFactor = $safetyAdjustments[$coverage] ?? 1.0000;
            
            $finalFactors[$coverage] = $baseFactor * $antiTheftFactor * $safetyFactor;
        }
        
        return new MakeModelFactor([
            'vehicle_id' => $vehicleData->vehicle_id,
            'standardized_make' => $standardizedVehicle->make,
            'standardized_model' => $standardizedVehicle->model,
            'base_factors' => $baseFactors,
            'anti_theft_adjustments' => $antiTheftAdjustments,
            'safety_adjustments' => $safetyAdjustments,
            'final_factors' => $finalFactors,
            'risk_classification' => $this->classifyVehicleRisk($vehicleData),
            'vehicle_characteristics' => $this->getVehicleCharacteristics($vehicleData->vin)
        ]);
    }
    
    private function getBaseMakeModelFactors(
        StandardizedVehicle $vehicle, 
        int $modelYear, 
        array $coverageTypes
    ): array {
        $factors = [];
        
        foreach ($coverageTypes as $coverageType) {
            // Try model-specific factor first
            $factor = $this->getModelSpecificFactor($vehicle, $modelYear, $coverageType);
            
            // Fall back to make-only factor
            if (!$factor) {
                $factor = $this->getMakeOnlyFactor($vehicle, $coverageType);
            }
            
            // Fall back to default factor
            $factors[$coverageType] = $factor ?? 1.0000;
        }
        
        return $factors;
    }
    
    private function getModelSpecificFactor(
        StandardizedVehicle $vehicle, 
        int $modelYear, 
        string $coverageType
    ): ?float {
        return DB::table('vehicle_make_model_factor')
            ->join('vehicle_make', 'vehicle_make_model_factor.make_id', '=', 'vehicle_make.id')
            ->join('vehicle_model', 'vehicle_make_model_factor.model_id', '=', 'vehicle_model.id')
            ->join('coverage_type', 'vehicle_make_model_factor.coverage_type_id', '=', 'coverage_type.id')
            ->where('vehicle_make.make_code', $vehicle->make_code)
            ->where('vehicle_model.model_code', $vehicle->model_code)
            ->where('coverage_type.coverage_code', $coverageType)
            ->where('vehicle_make_model_factor.model_year_min', '<=', $modelYear)
            ->where(function($query) use ($modelYear) {
                $query->whereNull('vehicle_make_model_factor.model_year_max')
                      ->orWhere('vehicle_make_model_factor.model_year_max', '>=', $modelYear);
            })
            ->where('vehicle_make_model_factor.program_id', $this->programId)
            ->where('vehicle_make_model_factor.effective_date', '<=', now())
            ->where(function($query) {
                $query->whereNull('vehicle_make_model_factor.expiration_date')
                      ->orWhere('vehicle_make_model_factor.expiration_date', '>', now());
            })
            ->where('vehicle_make_model_factor.status_id', Status::ACTIVE)
            ->orderBy('vehicle_make_model_factor.factor_type') // Prefer MODEL_SPECIFIC over MAKE_ONLY
            ->value('vehicle_make_model_factor.factor_value');
    }
    
    public function standardizeMakeModel(string $make, string $model): StandardizedVehicle
    {
        // Standardize make name
        $standardizedMake = $this->standardizeMakeName($make);
        
        // Get make record
        $makeRecord = DB::table('vehicle_make')
            ->where('make_name_standardized', $standardizedMake)
            ->where('status_id', Status::ACTIVE)
            ->first();
            
        if (!$makeRecord) {
            throw new UnknownVehicleMakeException("Unknown vehicle make: {$make}");
        }
        
        // Standardize model name
        $standardizedModel = $this->standardizeModelName($model, $makeRecord->id);
        
        // Get model record
        $modelRecord = DB::table('vehicle_model')
            ->where('make_id', $makeRecord->id)
            ->where('model_name_standardized', $standardizedModel)
            ->where('status_id', Status::ACTIVE)
            ->first();
            
        if (!$modelRecord) {
            // Create new model record if not found
            $modelRecord = $this->createNewModelRecord($makeRecord->id, $model, $standardizedModel);
        }
        
        return new StandardizedVehicle([
            'make_id' => $makeRecord->id,
            'make_code' => $makeRecord->make_code,
            'make_name' => $makeRecord->make_name,
            'model_id' => $modelRecord->id,
            'model_code' => $modelRecord->model_code,
            'model_name' => $modelRecord->model_name,
            'body_style' => $modelRecord->body_style,
            'vehicle_segment' => $modelRecord->vehicle_segment,
            'performance_category' => $modelRecord->performance_category
        ]);
    }
}
```

### VIN Decoding Integration
```php
class VINDecodingService
{
    public function decodeVIN(string $vin): VINDecodingResult
    {
        // Check cache first
        $cachedDecode = DB::table('vehicle_vin_decode_cache')
            ->where('vin', $vin)
            ->where('decode_date', '>=', now()->subDays(30)) // 30-day cache
            ->where('status_id', Status::ACTIVE)
            ->first();
            
        if ($cachedDecode && $cachedDecode->decode_confidence !== 'LOW') {
            return $this->createVINResultFromCache($cachedDecode);
        }
        
        // Decode VIN through external service
        $decodeResult = $this->performVINDecode($vin);
        
        // Cache the result
        $this->cacheVINDecode($vin, $decodeResult);
        
        return $decodeResult;
    }
    
    private function performVINDecode(string $vin): VINDecodingResult
    {
        // Integration with VIN decoding service (NHTSA, Edmunds, etc.)
        $response = $this->httpClient->get("https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/{$vin}", [
            'query' => ['format' => 'json', 'modelyear' => date('Y')]
        ]);
        
        $data = json_decode($response->getBody(), true);
        
        return new VINDecodingResult([
            'vin' => $vin,
            'make' => $data['Results'][6]['Value'] ?? null, // Make
            'model' => $data['Results'][8]['Value'] ?? null, // Model
            'model_year' => (int)($data['Results'][9]['Value'] ?? 0), // Model Year
            'body_style' => $data['Results'][21]['Value'] ?? null, // Body Class
            'engine_size' => $data['Results'][12]['Value'] ?? null, // Engine Size
            'fuel_type' => $data['Results'][23]['Value'] ?? null, // Fuel Type
            'confidence' => $this->assessDecodeConfidence($data),
            'raw_data' => $data
        ]);
    }
}
```

### Anti-Theft Device Discounts
```php
class AntiTheftDiscountService
{
    public function calculateAntiTheftDiscounts(array $devices, array $coverageTypes): array
    {
        $discounts = [];
        
        foreach ($coverageTypes as $coverageType) {
            $coverageDiscount = 1.0000;
            
            foreach ($devices as $deviceCode) {
                $device = DB::table('vehicle_anti_theft_device')
                    ->where('device_code', $deviceCode)
                    ->where('status_id', Status::ACTIVE)
                    ->first();
                    
                if ($device) {
                    $applicableCoverages = json_decode($device->applicable_coverage_types, true) ?? [];
                    
                    if (in_array($coverageType, $applicableCoverages)) {
                        // Apply cumulative discount but cap at maximum
                        $deviceDiscount = $device->discount_factor;
                        $coverageDiscount *= $deviceDiscount;
                    }
                }
            }
            
            // Cap maximum discount at 25%
            $discounts[$coverageType] = max(0.7500, $coverageDiscount);
        }
        
        return $discounts;
    }
}
```

---

## 5. Aguila Dorada Make Model Factors

### Sample Make/Model Factor Matrix
```sql
-- Make-only factors (apply when no model-specific factor exists)
INSERT INTO vehicle_make_model_factor (program_id, make_id, model_id, coverage_type_id, factor_value, factor_type, effective_date) VALUES
-- Reliable makes (favorable factors)
(1, (SELECT id FROM vehicle_make WHERE make_code = 'HONDA'), NULL, NULL, 0.9500, 'MAKE_ONLY', '2025-07-15'),
(1, (SELECT id FROM vehicle_make WHERE make_code = 'TOYOTA'), NULL, NULL, 0.9000, 'MAKE_ONLY', '2025-07-15'),

-- Standard makes (neutral factors)
(1, (SELECT id FROM vehicle_make WHERE make_code = 'FORD'), NULL, NULL, 1.0000, 'MAKE_ONLY', '2025-07-15'),
(1, (SELECT id FROM vehicle_make WHERE make_code = 'CHEVROLET'), NULL, NULL, 1.0000, 'MAKE_ONLY', '2025-07-15'),

-- Luxury makes (higher factors, especially for physical damage)
(1, (SELECT id FROM vehicle_make WHERE make_code = 'BMW'), NULL, (SELECT id FROM coverage_type WHERE coverage_code = 'COMPREHENSIVE'), 1.4000, 'MAKE_ONLY', '2025-07-15'),
(1, (SELECT id FROM vehicle_make WHERE make_code = 'BMW'), NULL, (SELECT id FROM coverage_type WHERE coverage_code = 'COLLISION'), 1.3000, 'MAKE_ONLY', '2025-07-15'),
(1, (SELECT id FROM vehicle_make WHERE make_code = 'BMW'), NULL, (SELECT id FROM coverage_type WHERE coverage_code = 'LIABILITY'), 1.1000, 'MAKE_ONLY', '2025-07-15'),

(1, (SELECT id FROM vehicle_make WHERE make_code = 'MERCEDES'), NULL, (SELECT id FROM coverage_type WHERE coverage_code = 'COMPREHENSIVE'), 1.5000, 'MAKE_ONLY', '2025-07-15'),
(1, (SELECT id FROM vehicle_make WHERE make_code = 'MERCEDES'), NULL, (SELECT id FROM coverage_type WHERE coverage_code = 'COLLISION'), 1.4000, 'MAKE_ONLY', '2025-07-15'),
(1, (SELECT id FROM vehicle_make WHERE make_code = 'MERCEDES'), NULL, (SELECT id FROM coverage_type WHERE coverage_code = 'LIABILITY'), 1.1500, 'MAKE_ONLY', '2025-07-15'),

-- High-risk makes
(1, (SELECT id FROM vehicle_make WHERE make_code = 'DODGE'), NULL, NULL, 1.2000, 'MAKE_ONLY', '2025-07-15');

-- Model-specific factors for high-theft or high-performance models
-- (Would require specific model IDs to be inserted first)
```

---

## 6. API Integration Requirements

### Vehicle Make Model Endpoints
```php
// Vehicle make/model API endpoints
POST /api/v1/rating/make-model/calculate
{
    "vehicle_data": {
        "vehicle_id": 12345,
        "vin": "1HGCM82633A123456",
        "make": "Honda",
        "model": "Civic",
        "model_year": 2020,
        "anti_theft_devices": ["FACTORY_ALARM", "IMMOBILIZER"],
        "coverage_types": ["LIABILITY", "COMPREHENSIVE", "COLLISION"]
    }
}

POST /api/v1/rating/make-model/decode-vin
{
    "vin": "1HGCM82633A123456"
}
// Decode VIN to get make/model/year and characteristics

GET /api/v1/rating/make-model/standardize
{
    "make": "HONDA",
    "model": "CIVIC SEDAN"
}
// Standardize make/model names

GET /api/v1/rating/make-model/anti-theft-devices
// Returns available anti-theft devices and discounts
```

### Response Format
```json
{
    "vehicle_id": 12345,
    "standardized_vehicle": {
        "make_code": "HONDA",
        "make_name": "Honda",
        "model_code": "CIVIC",
        "model_name": "Civic",
        "body_style": "SEDAN",
        "vehicle_segment": "COMPACT",
        "performance_category": "STANDARD"
    },
    "make_model_factors": {
        "LIABILITY": 0.9500,
        "COMPREHENSIVE": 0.8550,
        "COLLISION": 0.9025
    },
    "factor_breakdown": {
        "base_factors": {
            "LIABILITY": 0.9500,
            "COMPREHENSIVE": 0.9500,
            "COLLISION": 0.9500
        },
        "anti_theft_adjustments": {
            "COMPREHENSIVE": 0.9000,
            "COLLISION": 0.9500
        },
        "safety_adjustments": {
            "LIABILITY": 1.0000,
            "COMPREHENSIVE": 1.0000,
            "COLLISION": 1.0000
        }
    },
    "risk_assessment": {
        "theft_risk": "MODERATE",
        "safety_rating": "GOOD",
        "repair_cost_risk": "LOW",
        "overall_risk": "LOW"
    },
    "vehicle_characteristics": {
        "safety_rating_iihs": "TOP_SAFETY_PICK",
        "safety_rating_nhtsa": 5.0,
        "standard_anti_theft": ["IMMOBILIZER", "FACTORY_ALARM"],
        "parts_availability": "EXCELLENT",
        "repair_complexity": "LOW"
    },
    "vin_verification": {
        "vin_decoded": true,
        "data_verified": true,
        "confidence": "HIGH",
        "decode_source": "NHTSA_VPIC"
    }
}
```

---

## 7. Performance Requirements

### Make Model Factor Caching
```php
class VehicleMakeModelService
{
    public function calculateMakeModelFactor(VehicleMakeModelData $vehicleData): MakeModelFactor
    {
        // Cache make/model factors by standardized make/model/year
        $cacheKey = "make_model_factor_{$this->programId}_{$vehicleData->standardized_make}_{$vehicleData->standardized_model}_{$vehicleData->model_year}";
        
        return Cache::remember($cacheKey, 3600, function() use ($vehicleData) {
            return $this->performMakeModelFactorCalculation($vehicleData);
        });
    }
}
```

### Database Performance
```sql
-- Make/model factor lookup optimization
CREATE INDEX idx_make_model_factor_lookup 
ON vehicle_make_model_factor (
    program_id, 
    make_id, 
    model_id, 
    coverage_type_id,
    model_year_min,
    model_year_max,
    effective_date
) WHERE status_id = 1;

-- VIN decoding cache lookup optimization
CREATE INDEX idx_vin_decode_lookup 
ON vehicle_vin_decode_cache (
    vin, 
    decode_date, 
    decode_confidence
) WHERE status_id = 1;

-- Make/model standardization lookup
CREATE INDEX idx_make_standardized_lookup 
ON vehicle_make (make_name_standardized, status_id);

CREATE INDEX idx_model_standardized_lookup 
ON vehicle_model (make_id, model_name_standardized, status_id);
```

---

## 8. Testing Requirements

### Make Model Factor Testing
```php
class VehicleMakeModelServiceTest extends TestCase
{
    public function test_honda_civic_favorable_factor()
    {
        $vehicleData = new VehicleMakeModelData([
            'make' => 'Honda',
            'model' => 'Civic',
            'model_year' => 2020,
            'coverage_types' => ['LIABILITY', 'COMPREHENSIVE'],
            'anti_theft_devices' => ['IMMOBILIZER']
        ]);
        
        $factor = $this->makeModelService->calculateMakeModelFactor($vehicleData);
        
        $this->assertEquals('HONDA', $factor->standardized_vehicle->make_code);
        $this->assertLessThan(1.0, $factor->final_factors['LIABILITY']); // Honda discount
        $this->assertLessThan(1.0, $factor->final_factors['COMPREHENSIVE']); // Honda + anti-theft discount
    }
    
    public function test_luxury_vehicle_surcharge()
    {
        $vehicleData = new VehicleMakeModelData([
            'make' => 'BMW',
            'model' => '3 Series',
            'model_year' => 2022,
            'coverage_types' => ['COMPREHENSIVE', 'COLLISION'],
            'anti_theft_devices' => []
        ]);
        
        $factor = $this->makeModelService->calculateMakeModelFactor($vehicleData);
        
        $this->assertEquals('BMW', $factor->standardized_vehicle->make_code);
        $this->assertGreaterThan(1.0, $factor->final_factors['COMPREHENSIVE']); // Luxury surcharge
        $this->assertGreaterThan(1.0, $factor->final_factors['COLLISION']); // Luxury surcharge
    }
    
    public function test_vin_decoding_accuracy()
    {
        $vin = '1HGCM82633A123456'; // Honda Civic VIN
        
        $decodeResult = $this->vinDecodingService->decodeVIN($vin);
        
        $this->assertEquals('HONDA', strtoupper($decodeResult->make));
        $this->assertEquals('CIVIC', strtoupper($decodeResult->model));
        $this->assertEquals('HIGH', $decodeResult->confidence);
    }
    
    public function test_anti_theft_discount_stacking()
    {
        $devices = ['FACTORY_ALARM', 'GPS_TRACKING', 'IMMOBILIZER'];
        $coverageTypes = ['COMPREHENSIVE'];
        
        $discounts = $this->antiTheftService->calculateAntiTheftDiscounts($devices, $coverageTypes);
        
        $this->assertLessThan(1.0, $discounts['COMPREHENSIVE']); // Should have discount
        $this->assertGreaterThanOrEqual(0.75, $discounts['COMPREHENSIVE']); // Should not exceed 25% discount cap
    }
}
```

---

## Implementation Priority: HIGH
This factor is essential for accurate vehicle-specific risk assessment and should be implemented early in vehicle factor development.

## Dependencies
- **VIN Decoding Service**: External VIN decoding integration
- **Vehicle Age Factor**: Make/model factors may vary by age ranges

## Estimated Implementation Effort
- **Database Schema**: 4 days
- **Service Layer**: 6 days
- **VIN Integration**: 4 days
- **Make/Model Standardization**: 3 days
- **Anti-Theft Logic**: 2 days
- **API Integration**: 3 days
- **Testing**: 4 days
- **Total**: 26 days

This plan implements comprehensive vehicle make/model risk assessment while maintaining proper VIN verification, standardization, and detailed risk classification that reflects the varied risk characteristics across different vehicle manufacturers and models.