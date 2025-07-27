# ProgramRater Global Requirements Approach V2

## Executive Summary

The ProgramRater serves as the core rating engine for the Aime insurance platform, responsible for calculating accurate premiums based on a comprehensive set of rating factors. Version 2 of this approach significantly enhances the original design with granular factor-level audit trails, complete calculation transparency, and improved data architecture that supports regulatory compliance and debugging. The system processes all 36 identified rating factors while maintaining detailed records of every calculation step.

## Key V2 Enhancements

### Complete Calculation Transparency
- Every factor application logged individually
- Step-by-step calculation storage
- Line-level premium breakdowns
- Full audit trail for regulatory compliance

### Improved Data Architecture
- Separation of rate configuration from execution
- Normalized storage of all calculations
- Support for historical rate reconstruction
- Optimized for both performance and auditability

## 1. System Overview

### 1.1 Core Responsibilities

```
┌─────────────────────────────────────────────────────────────┐
│                      ProgramRater V2                         │
├─────────────────────────────────────────────────────────────┤
│ • Premium Calculation Engine                                 │
│ • Rating Factor Processing                                   │
│ • Factor Stacking & Precedence                              │
│ • Rate Validation & Constraints                             │
│ • Granular Calculation Audit Trail                          │
│ • Factor-Level Logging                                      │
│ • Line-Level Premium Tracking                               │
│ • Calculation Reconstruction                                │
│ • Performance Optimization                                   │
│ • Rate Book Management                                       │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Rating Factor Categories

Based on analysis of the 36 interpretation files, the rating factors are organized into:

1. **Vehicle Factors** (11 factors) - Applied to individual vehicles
2. **Driver Factors** (12 factors) - Applied based on driver characteristics
3. **Policy Factors** (9 factors) - Applied at the policy level
4. **Territory/Region Factors** (4 factors) - Geographic-based adjustments

## 2. Enhanced Data Model for Complete Auditability

### 2.1 Core Rating Tables

```sql
-- Rate type definitions
CREATE TABLE rate_type (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rate_type_code VARCHAR(50) UNIQUE NOT NULL,
    rate_type_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Main rate calculation record
CREATE TABLE rate (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    quote_id UUID REFERENCES quote(id),
    policy_id UUID REFERENCES policy(id),
    rate_type_id UUID REFERENCES rate_type(id),
    program_version_id UUID REFERENCES program_version(id),
    calculation_date TIMESTAMP NOT NULL,
    effective_date DATE NOT NULL,
    term_months INTEGER NOT NULL,
    
    -- Summary amounts
    total_premium DECIMAL(10,2) NOT NULL,
    total_base_premium DECIMAL(10,2) NOT NULL,
    total_discounts DECIMAL(10,2) NOT NULL,
    total_surcharges DECIMAL(10,2) NOT NULL,
    total_fees DECIMAL(10,2) NOT NULL,
    total_taxes DECIMAL(10,2) NOT NULL,
    
    -- Metadata
    calculation_version VARCHAR(20) NOT NULL,
    calculation_status VARCHAR(20) NOT NULL, -- completed, failed, partial
    calculation_duration_ms INTEGER,
    created_by UUID REFERENCES user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_quote_rate (quote_id, created_at),
    INDEX idx_policy_rate (policy_id, effective_date)
);

-- Line-level premium breakdown
CREATE TABLE rate_line (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rate_id UUID REFERENCES rate(id),
    line_type VARCHAR(50) NOT NULL, -- vehicle, coverage, policy
    line_number INTEGER NOT NULL,
    
    -- Line identifiers
    vehicle_id UUID REFERENCES vehicle(id),
    coverage_type_id UUID REFERENCES coverage_type(id),
    driver_id UUID REFERENCES driver(id),
    
    -- Premium components
    base_premium DECIMAL(10,2) NOT NULL,
    adjusted_premium DECIMAL(10,2) NOT NULL,
    final_premium DECIMAL(10,2) NOT NULL,
    
    -- Factors applied
    total_factor DECIMAL(10,6) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    surcharge_amount DECIMAL(10,2) DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_rate_lines (rate_id, line_type, line_number)
);
```

### 2.2 Factor Tracking Tables

```sql
-- Rate factor type definitions
CREATE TABLE rate_factor_type (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    factor_type_code VARCHAR(50) UNIQUE NOT NULL,
    factor_type_name VARCHAR(100) NOT NULL,
    factor_category VARCHAR(30) NOT NULL, -- vehicle, driver, policy, territory
    calculation_method VARCHAR(20) NOT NULL, -- multiply, add, subtract
    apply_to VARCHAR(30) NOT NULL, -- base, adjusted, final
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Factor grouping for organization
CREATE TABLE rate_factor_group (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_code VARCHAR(50) UNIQUE NOT NULL,
    group_name VARCHAR(100) NOT NULL,
    group_category VARCHAR(30) NOT NULL,
    display_order INTEGER NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Individual factor applications
CREATE TABLE rate_factor (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rate_id UUID REFERENCES rate(id),
    rate_line_id UUID REFERENCES rate_line(id),
    rate_factor_type_id UUID REFERENCES rate_factor_type(id),
    rate_factor_group_id UUID REFERENCES rate_factor_group(id),
    
    -- Factor details
    factor_code VARCHAR(50) NOT NULL,
    factor_name VARCHAR(100) NOT NULL,
    sequence_number INTEGER NOT NULL,
    
    -- Values
    input_value DECIMAL(20,6), -- Value being evaluated
    factor_value DECIMAL(10,6) NOT NULL, -- Factor applied
    impact_amount DECIMAL(10,2) NOT NULL, -- Dollar impact
    
    -- Context
    lookup_key VARCHAR(255), -- What was looked up
    lookup_table VARCHAR(100), -- Which table/rate sheet
    calculation_details JSONB, -- Detailed calc info
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_rate_factors (rate_id, sequence_number),
    INDEX idx_line_factors (rate_line_id, sequence_number)
);
```

### 2.3 Calculation Storage Tables

```sql
-- Calculation type definitions
CREATE TABLE calculation_type (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    calc_type_code VARCHAR(50) UNIQUE NOT NULL,
    calc_type_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Detailed calculation storage
CREATE TABLE calculation (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rate_id UUID REFERENCES rate(id),
    rate_line_id UUID REFERENCES rate_line(id),
    rate_factor_id UUID REFERENCES rate_factor(id),
    calculation_type_id UUID REFERENCES calculation_type(id),
    
    -- Calculation details
    step_number INTEGER NOT NULL,
    operation VARCHAR(50) NOT NULL, -- multiply, add, lookup, etc.
    formula TEXT NOT NULL,
    
    -- Values
    input_values JSONB NOT NULL,
    output_value DECIMAL(20,6) NOT NULL,
    running_total DECIMAL(10,2),
    
    -- Debugging info
    execution_time_ms INTEGER,
    cache_hit BOOLEAN DEFAULT false,
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_calc_rate (rate_id, step_number),
    INDEX idx_calc_factor (rate_factor_id)
);
```

### 2.4 Rate Configuration Tables

```sql
-- Rate tables for lookups
CREATE TABLE rate_table (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_version_id UUID REFERENCES program_version(id),
    table_code VARCHAR(50) NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    table_type VARCHAR(20) NOT NULL, -- lookup, range, interpolation
    rate_factor_type_id UUID REFERENCES rate_factor_type(id),
    
    -- Table data
    table_structure JSONB NOT NULL, -- Column definitions
    table_data JSONB NOT NULL, -- Actual rates
    
    -- Validity
    effective_date DATE NOT NULL,
    expiration_date DATE,
    
    created_by UUID REFERENCES user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(program_version_id, table_code, effective_date)
);

-- Factor configuration
CREATE TABLE rate_factor_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_version_id UUID REFERENCES program_version(id),
    rate_factor_type_id UUID REFERENCES rate_factor_type(id),
    rate_factor_group_id UUID REFERENCES rate_factor_group(id),
    
    -- Configuration
    factor_code VARCHAR(50) NOT NULL,
    factor_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_required BOOLEAN DEFAULT true,
    calculation_order INTEGER NOT NULL,
    
    -- Rules
    rate_table_id UUID REFERENCES rate_table(id),
    calculation_formula TEXT,
    validation_rules JSONB,
    
    -- Constraints
    min_factor DECIMAL(10,6),
    max_factor DECIMAL(10,6),
    default_factor DECIMAL(10,6) DEFAULT 1.0,
    
    effective_date DATE NOT NULL,
    expiration_date DATE,
    
    created_by UUID REFERENCES user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(program_version_id, factor_code, effective_date)
);
```

## 3. Rating Calculation Engine V2

### 3.1 Enhanced Calculation Pipeline

```typescript
interface RatingPipelineV2 {
  // Initialize rating record
  initializeRate(quote: Quote): Promise<Rate>
  
  // Stage 1: Base Rate Selection with logging
  selectBaseRates(
    rate: Rate, 
    territory: Territory, 
    coverages: Coverage[]
  ): Promise<RateLine[]>
  
  // Stage 2: Vehicle Factor Application with audit
  applyVehicleFactors(
    rate: Rate,
    rateLines: RateLine[], 
    vehicles: Vehicle[]
  ): Promise<RateFactor[]>
  
  // Stage 3: Driver Factor Application with tracking
  applyDriverFactors(
    rate: Rate,
    rateLines: RateLine[], 
    drivers: Driver[]
  ): Promise<RateFactor[]>
  
  // Stage 4: Policy Factor Application with logging
  applyPolicyFactors(
    rate: Rate,
    rateLines: RateLine[], 
    policy: Policy
  ): Promise<RateFactor[]>
  
  // Stage 5: Geographic Adjustments with audit
  applyGeographicFactors(
    rate: Rate,
    rateLines: RateLine[], 
    location: Location
  ): Promise<RateFactor[]>
  
  // Stage 6: Fees and Taxes with tracking
  applyFeesAndTaxes(
    rate: Rate,
    rateLines: RateLine[], 
    fees: Fee[]
  ): Promise<RateFactor[]>
  
  // Stage 7: Finalize and validate
  finalizeRate(rate: Rate): Promise<RatingResult>
}
```

### 3.2 Factor Application with Audit Trail

```typescript
class AuditedRatingEngine implements RatingEngine {
  async applyFactor(
    context: FactorContext,
    factorConfig: RateFactorConfig
  ): Promise<RateFactor> {
    const startTime = Date.now()
    
    // Create factor record
    const rateFactor = await this.db.rateFactor.create({
      rate_id: context.rateId,
      rate_line_id: context.rateLineId,
      rate_factor_type_id: factorConfig.rate_factor_type_id,
      rate_factor_group_id: factorConfig.rate_factor_group_id,
      factor_code: factorConfig.factor_code,
      factor_name: factorConfig.factor_name,
      sequence_number: context.sequenceNumber
    })
    
    // Perform calculation
    const calculation = await this.calculateFactor(context, factorConfig)
    
    // Store calculation details
    await this.db.calculation.create({
      rate_id: context.rateId,
      rate_line_id: context.rateLineId,
      rate_factor_id: rateFactor.id,
      calculation_type_id: calculation.typeId,
      step_number: calculation.stepNumber,
      operation: calculation.operation,
      formula: calculation.formula,
      input_values: calculation.inputs,
      output_value: calculation.output,
      running_total: calculation.runningTotal,
      execution_time_ms: Date.now() - startTime
    })
    
    // Update factor with results
    await this.db.rateFactor.update(rateFactor.id, {
      input_value: calculation.inputValue,
      factor_value: calculation.factorValue,
      impact_amount: calculation.impactAmount,
      lookup_key: calculation.lookupKey,
      lookup_table: calculation.lookupTable,
      calculation_details: calculation.details
    })
    
    return rateFactor
  }
}
```

### 3.3 Territory Base Rate Implementation V2

```typescript
class TerritoryBaseRatesFactorV2 implements RatingFactor {
  async calculate(context: RatingContext): Promise<FactorResult> {
    // Initialize rate record
    const rate = await this.createRateRecord(context)
    
    // Get territory
    const territory = await this.territoryService.getByZip(
      context.garagingZipCode,
      context.effectiveDate
    )
    
    // Lookup base rates
    const baseRates = await this.rateTableService.lookup(
      'territory-base-rates',
      territory.code,
      context.effectiveDate
    )
    
    // Create rate lines for each coverage
    const rateLines: RateLine[] = []
    
    for (const coverage of context.coverages) {
      const baseRate = baseRates[coverage.type]
      
      // Create rate line
      const rateLine = await this.db.rateLine.create({
        rate_id: rate.id,
        line_type: 'coverage',
        line_number: rateLines.length + 1,
        coverage_type_id: coverage.coverage_type_id,
        base_premium: baseRate,
        adjusted_premium: baseRate,
        final_premium: baseRate,
        total_factor: 1.0
      })
      
      // Create base rate factor record
      await this.db.rateFactor.create({
        rate_id: rate.id,
        rate_line_id: rateLine.id,
        rate_factor_type_id: this.factorTypeId,
        factor_code: 'territory-base-rate',
        factor_name: `Territory ${territory.code} Base Rate`,
        sequence_number: 1,
        input_value: null,
        factor_value: 1.0,
        impact_amount: baseRate,
        lookup_key: territory.code,
        lookup_table: 'territory-base-rates',
        calculation_details: {
          territory_code: territory.code,
          territory_name: territory.name,
          coverage_type: coverage.type,
          term_months: context.termMonths,
          base_rate_6_month: baseRate
        }
      })
      
      // Log calculation
      await this.db.calculation.create({
        rate_id: rate.id,
        rate_line_id: rateLine.id,
        rate_factor_id: rateFactor.id,
        step_number: 1,
        operation: 'lookup',
        formula: `BaseRate = LookupTerritoryRate(${territory.code}, ${coverage.type})`,
        input_values: {
          territory_code: territory.code,
          coverage_type: coverage.type
        },
        output_value: baseRate,
        running_total: baseRate
      })
      
      rateLines.push(rateLine)
    }
    
    return { rate, rateLines }
  }
}
```

### 3.4 Driver Assignment Implementation V2

```typescript
class DriverAssignmentFactorV2 implements RatingFactor {
  async calculate(context: PolicyRatingContext): Promise<FactorResult> {
    const assignments = await this.createOptimalAssignments(
      context.drivers,
      context.vehicles
    )
    
    for (const assignment of assignments) {
      const vehicleRateLine = await this.getVehicleRateLine(
        context.rateId,
        assignment.vehicle.id
      )
      
      // Calculate driver factor
      const driverFactor = await this.calculateDriverFactor(
        assignment.driver,
        assignment.vehicle,
        assignment.percentage
      )
      
      // Create factor record
      const rateFactor = await this.db.rateFactor.create({
        rate_id: context.rateId,
        rate_line_id: vehicleRateLine.id,
        rate_factor_type_id: this.factorTypeId,
        factor_code: 'driver-assignment',
        factor_name: 'Driver Assignment Factor',
        sequence_number: context.getNextSequence(),
        input_value: assignment.percentage,
        factor_value: driverFactor,
        impact_amount: vehicleRateLine.adjusted_premium * (driverFactor - 1),
        lookup_key: `${assignment.driver.id}-${assignment.vehicle.id}`,
        lookup_table: 'driver-assignment-matrix',
        calculation_details: {
          driver_id: assignment.driver.id,
          driver_age: assignment.driver.age,
          vehicle_id: assignment.vehicle.id,
          assignment_type: assignment.type,
          percentage: assignment.percentage
        }
      })
      
      // Log calculation steps
      await this.logCalculationSteps(rateFactor.id, {
        driverRiskScore: assignment.driver.riskScore,
        vehicleRiskScore: assignment.vehicle.riskScore,
        assignmentOptimization: assignment.optimizationDetails,
        factorCalculation: driverFactor
      })
      
      // Update rate line
      await this.updateRateLine(vehicleRateLine.id, driverFactor)
    }
  }
  
  private async logCalculationSteps(
    rateFactorId: string,
    details: any
  ): Promise<void> {
    const steps = [
      {
        operation: 'risk_assessment',
        formula: 'DriverRisk = CalculateDriverRiskScore(age, violations, experience)',
        input_values: details.driverRiskInputs,
        output_value: details.driverRiskScore
      },
      {
        operation: 'assignment_optimization',
        formula: 'Assignment = OptimizeDriverVehicleMatch(drivers, vehicles)',
        input_values: details.assignmentInputs,
        output_value: details.assignmentResult
      },
      {
        operation: 'factor_calculation',
        formula: 'Factor = BaseDriverFactor * ExperienceMod * ViolationMod',
        input_values: details.factorInputs,
        output_value: details.factorCalculation
      }
    ]
    
    for (const [index, step] of steps.entries()) {
      await this.db.calculation.create({
        rate_factor_id: rateFactorId,
        step_number: index + 1,
        ...step
      })
    }
  }
}
```

## 4. Implementation Architecture V2

### 4.1 System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Rating API Layer                          │
│              (REST/GraphQL Endpoints)                        │
├─────────────────────────────────────────────────────────────┤
│                 Rating Engine Core V2                        │
├─────────────────┬─────────────────┬────────────────────────┤
│ Factor Processor│ Calc Engine     │ Validation Engine      │
├─────────────────┼─────────────────┼────────────────────────┤
│ Rate Tables     │ Cache Layer     │ Audit Logger           │
├─────────────────┼─────────────────┼────────────────────────┤
│ Line Processor  │ Factor Groups   │ Calc Storage           │
├─────────────────┴─────────────────┴────────────────────────┤
│                    Data Access Layer                         │
├─────────────────────────────────────────────────────────────┤
│              PostgreSQL + Redis Cache                        │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Enhanced Service Architecture

```typescript
// Main Rating Service V2
interface IRatingServiceV2 {
  // Calculate with full audit trail
  calculateQuote(context: RatingContext): Promise<RatingResultV2>
  
  // Recalculate with change tracking
  recalculatePolicy(
    policyId: string, 
    changes: PolicyChange
  ): Promise<RatingResultV2>
  
  // Validate with detailed results
  validateRates(result: RatingResultV2): Promise<ValidationResult>
  
  // Explain any calculation
  explainCalculation(rateId: string): Promise<CalculationExplanation>
  
  // Reconstruct historical calculation
  reconstructCalculation(
    rateId: string, 
    asOfDate: Date
  ): Promise<RatingResultV2>
}

// Factor Processing Service V2
interface IFactorServiceV2 {
  // Load factors with configuration
  loadFactors(
    programId: string, 
    version: string, 
    date: Date
  ): Promise<FactorSet>
  
  // Apply factor with logging
  applyFactor(
    factor: Factor, 
    context: FactorContext
  ): Promise<FactorResultV2>
  
  // Calculate factor stack with audit
  calculateFactorStack(
    factors: Factor[], 
    method: StackMethod
  ): Promise<StackResult>
  
  // Get factor history
  getFactorHistory(
    factorCode: string, 
    dateRange: DateRange
  ): Promise<FactorHistory[]>
}

// Rate Line Service
interface IRateLineService {
  // Create rate lines
  createRateLines(
    rate: Rate, 
    context: RatingContext
  ): Promise<RateLine[]>
  
  // Update line premiums
  updateLinePremiums(
    rateLineId: string, 
    factor: number
  ): Promise<RateLine>
  
  // Get line breakdown
  getLineBreakdown(rateId: string): Promise<LineBreakdown[]>
}

// Calculation Storage Service
interface ICalculationService {
  // Store calculation step
  storeCalculation(calc: CalculationStep): Promise<void>
  
  // Retrieve calculation chain
  getCalculationChain(rateId: string): Promise<CalculationChain>
  
  // Generate calculation report
  generateReport(
    rateId: string, 
    format: ReportFormat
  ): Promise<CalculationReport>
}
```

### 4.3 Performance Optimizations

```typescript
class OptimizedRatingEngineV2 {
  private batchProcessor: BatchProcessor
  private cache: RatingCache
  
  async calculateBatch(quotes: Quote[]): Promise<RatingResultV2[]> {
    // Group by program and territory for efficiency
    const groups = this.groupQuotesByProgramTerritory(quotes)
    
    // Preload all rate tables for the batch
    await this.preloadRateTables(groups)
    
    // Process groups in parallel with rate limiting
    const results = await this.batchProcessor.process(
      groups,
      async (group) => {
        // Process all quotes in group
        return await Promise.all(
          group.quotes.map(q => this.calculateSingle(q))
        )
      },
      { concurrency: 10 }
    )
    
    return results.flat()
  }
  
  private async calculateSingle(quote: Quote): Promise<RatingResultV2> {
    // Create rate record
    const rate = await this.db.rate.create({
      quote_id: quote.id,
      rate_type_id: this.getRateType('new_business'),
      program_version_id: quote.program_version_id,
      calculation_date: new Date(),
      effective_date: quote.effective_date,
      term_months: quote.term_months,
      calculation_version: this.ENGINE_VERSION,
      calculation_status: 'in_progress'
    })
    
    try {
      // Calculate with full logging
      const result = await this.pipeline.execute(rate, quote)
      
      // Update rate with results
      await this.db.rate.update(rate.id, {
        total_premium: result.totalPremium,
        total_base_premium: result.basePremium,
        total_discounts: result.discounts,
        total_surcharges: result.surcharges,
        total_fees: result.fees,
        total_taxes: result.taxes,
        calculation_status: 'completed',
        calculation_duration_ms: result.duration
      })
      
      return result
    } catch (error) {
      // Log error and update status
      await this.handleCalculationError(rate.id, error)
      throw error
    }
  }
}
```

## 5. Audit and Compliance Features

### 5.1 Calculation Reconstruction

```typescript
class CalculationReconstructor {
  async reconstructCalculation(
    rateId: string,
    asOfDate?: Date
  ): Promise<ReconstructedCalculation> {
    // Get rate record
    const rate = await this.db.rate.findById(rateId)
    
    // Get all rate lines
    const rateLines = await this.db.rateLine.findByRateId(rateId)
    
    // Get all factors applied
    const factors = await this.db.rateFactor.findByRateId(rateId)
    
    // Get all calculations
    const calculations = await this.db.calculation.findByRateId(rateId)
    
    // Reconstruct step by step
    const reconstruction = {
      rate,
      lines: [],
      timeline: []
    }
    
    for (const line of rateLines) {
      const lineFactors = factors.filter(f => f.rate_line_id === line.id)
      const lineCalcs = calculations.filter(c => c.rate_line_id === line.id)
      
      reconstruction.lines.push({
        line,
        factors: lineFactors,
        calculations: lineCalcs,
        progression: this.buildProgression(lineCalcs)
      })
    }
    
    return reconstruction
  }
  
  private buildProgression(calculations: Calculation[]): PremiumProgression {
    const sorted = calculations.sort((a, b) => a.step_number - b.step_number)
    const progression = []
    
    for (const calc of sorted) {
      progression.push({
        step: calc.step_number,
        operation: calc.operation,
        formula: calc.formula,
        inputs: calc.input_values,
        output: calc.output_value,
        runningTotal: calc.running_total
      })
    }
    
    return progression
  }
}
```

### 5.2 Regulatory Reporting

```typescript
class RegulatoryReportGenerator {
  async generateFilingReport(
    programId: string,
    dateRange: DateRange
  ): Promise<FilingReport> {
    // Get all rates for period
    const rates = await this.db.rate.findByProgramAndDateRange(
      programId,
      dateRange
    )
    
    // Aggregate by factor type
    const factorAnalysis = await this.analyzeFactorUsage(rates)
    
    // Generate statistical summaries
    const statistics = await this.calculateStatistics(rates)
    
    // Create filing-ready report
    return {
      programId,
      period: dateRange,
      totalQuotes: rates.length,
      averagePremium: statistics.avgPremium,
      factorUtilization: factorAnalysis,
      territoryDistribution: statistics.territoryDist,
      complianceMetrics: await this.getComplianceMetrics(rates)
    }
  }
  
  private async analyzeFactorUsage(
    rates: Rate[]
  ): Promise<FactorAnalysis> {
    const analysis = {}
    
    for (const rate of rates) {
      const factors = await this.db.rateFactor.findByRateId(rate.id)
      
      for (const factor of factors) {
        if (!analysis[factor.factor_code]) {
          analysis[factor.factor_code] = {
            count: 0,
            avgFactor: 0,
            minFactor: Infinity,
            maxFactor: -Infinity,
            totalImpact: 0
          }
        }
        
        const stats = analysis[factor.factor_code]
        stats.count++
        stats.avgFactor += factor.factor_value
        stats.minFactor = Math.min(stats.minFactor, factor.factor_value)
        stats.maxFactor = Math.max(stats.maxFactor, factor.factor_value)
        stats.totalImpact += factor.impact_amount
      }
    }
    
    // Calculate averages
    for (const factorCode in analysis) {
      analysis[factorCode].avgFactor /= analysis[factorCode].count
    }
    
    return analysis
  }
}
```

## 6. Query Examples and Performance

### 6.1 Common Queries

```sql
-- Get complete calculation for a quote
WITH rate_details AS (
  SELECT r.*, rt.rate_type_name
  FROM rate r
  JOIN rate_type rt ON r.rate_type_id = rt.id
  WHERE r.quote_id = $1
  ORDER BY r.created_at DESC
  LIMIT 1
),
line_details AS (
  SELECT rl.*, ct.coverage_name
  FROM rate_line rl
  LEFT JOIN coverage_type ct ON rl.coverage_type_id = ct.id
  WHERE rl.rate_id = (SELECT id FROM rate_details)
),
factor_details AS (
  SELECT 
    rf.*,
    rft.factor_type_name,
    rfg.group_name
  FROM rate_factor rf
  JOIN rate_factor_type rft ON rf.rate_factor_type_id = rft.id
  LEFT JOIN rate_factor_group rfg ON rf.rate_factor_group_id = rfg.id
  WHERE rf.rate_id = (SELECT id FROM rate_details)
  ORDER BY rf.sequence_number
)
SELECT 
  json_build_object(
    'rate', row_to_json(rate_details),
    'lines', json_agg(DISTINCT line_details),
    'factors', json_agg(DISTINCT factor_details)
  ) as calculation_detail
FROM rate_details, line_details, factor_details;

-- Analyze factor impact by territory
SELECT 
  t.territory_code,
  t.territory_name,
  rft.factor_type_name,
  COUNT(*) as usage_count,
  AVG(rf.factor_value) as avg_factor,
  SUM(rf.impact_amount) as total_impact
FROM rate r
JOIN quote q ON r.quote_id = q.id
JOIN territory t ON q.territory_id = t.id
JOIN rate_factor rf ON rf.rate_id = r.id
JOIN rate_factor_type rft ON rf.rate_factor_type_id = rft.id
WHERE r.calculation_date >= $1
  AND r.calculation_date < $2
GROUP BY t.territory_code, t.territory_name, rft.factor_type_name
ORDER BY t.territory_code, total_impact DESC;
```

### 6.2 Performance Considerations

```sql
-- Key indexes for performance
CREATE INDEX idx_rate_quote_lookup ON rate(quote_id, created_at DESC);
CREATE INDEX idx_rate_line_coverage ON rate_line(rate_id, coverage_type_id);
CREATE INDEX idx_factor_sequence ON rate_factor(rate_id, sequence_number);
CREATE INDEX idx_factor_type ON rate_factor(rate_factor_type_id, created_at);
CREATE INDEX idx_calc_lookup ON calculation(rate_id, step_number);

-- Partitioning for scale
CREATE TABLE rate_2024 PARTITION OF rate
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
  
CREATE TABLE rate_factor_2024 PARTITION OF rate_factor
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

## 7. Testing Strategy V2

### 7.1 Factor-Level Testing

```typescript
describe('RatingFactors V2', () => {
  describe('Audit Trail', () => {
    it('should create complete factor records', async () => {
      const context = createMockContext()
      const result = await vehicleAgeFactor.calculate(context)
      
      // Verify rate factor record
      const factor = await db.rateFactor.findById(result.factorId)
      expect(factor).toMatchObject({
        factor_code: 'vehicle-age',
        factor_value: 0.95,
        impact_amount: -15.00,
        lookup_key: '2019',
        lookup_table: 'vehicle-age-factors'
      })
      
      // Verify calculation record
      const calcs = await db.calculation.findByFactorId(result.factorId)
      expect(calcs).toHaveLength(3) // lookup, calculate, apply
      expect(calcs[0].formula).toContain('LookupVehicleAgeFactor')
    })
  })
  
  describe('Calculation Reconstruction', () => {
    it('should perfectly reconstruct calculations', async () => {
      const originalQuote = createTestQuote()
      const originalResult = await ratingEngine.calculate(originalQuote)
      
      // Reconstruct from stored data
      const reconstructed = await reconstructor.reconstruct(
        originalResult.rateId
      )
      
      expect(reconstructed.totalPremium).toBe(originalResult.totalPremium)
      expect(reconstructed.factorSequence).toEqual(
        originalResult.factorsApplied
      )
    })
  })
})
```

### 7.2 Performance Testing V2

```typescript
describe('Performance with Audit Logging', () => {
  it('should maintain SLA with full logging', async () => {
    const quotes = generateTestQuotes(100)
    
    const start = Date.now()
    const results = await ratingEngine.calculateBatch(quotes)
    const duration = Date.now() - start
    
    expect(results).toHaveLength(100)
    expect(duration / 100).toBeLessThan(500) // 500ms per quote
    
    // Verify audit completeness
    for (const result of results) {
      const factors = await db.rateFactor.findByRateId(result.rateId)
      expect(factors.length).toBeGreaterThan(20) // All factors logged
    }
  })
})
```

## 8. Migration from V1 to V2

### 8.1 Migration Strategy

```sql
-- Migration script outline
BEGIN;

-- Create new V2 tables
CREATE TABLE rate_type (...);
CREATE TABLE rate (...);
CREATE TABLE rate_line (...);
CREATE TABLE rate_factor_type (...);
CREATE TABLE rate_factor_group (...);
CREATE TABLE rate_factor (...);
CREATE TABLE calculation_type (...);
CREATE TABLE calculation (...);

-- Migrate existing calculations
INSERT INTO rate (quote_id, policy_id, total_premium, ...)
SELECT 
  quote_id,
  policy_id,
  total_premium,
  ...
FROM calculation_audit;

-- Create rate lines from existing data
INSERT INTO rate_line (rate_id, line_type, base_premium, ...)
SELECT 
  r.id,
  'coverage',
  ca.coverage_premiums->>'base',
  ...
FROM rate r
JOIN calculation_audit ca ON ca.quote_id = r.quote_id;

-- Backfill factor records where possible
INSERT INTO rate_factor (rate_id, factor_code, factor_value, ...)
SELECT 
  r.id,
  factor->>'code',
  (factor->>'value')::decimal,
  ...
FROM rate r
JOIN calculation_audit ca ON ca.quote_id = r.quote_id
CROSS JOIN LATERAL jsonb_array_elements(ca.factors_applied) factor;

COMMIT;
```

### 8.2 Dual-Write Period

```typescript
class DualWriteRatingEngine {
  async calculate(quote: Quote): Promise<RatingResult> {
    // Calculate using V1 engine
    const v1Result = await this.v1Engine.calculate(quote)
    
    // Calculate using V2 engine
    const v2Result = await this.v2Engine.calculate(quote)
    
    // Compare results
    if (!this.resultsMatch(v1Result, v2Result)) {
      await this.logDiscrepancy(quote.id, v1Result, v2Result)
    }
    
    // Return V1 result during transition
    return v1Result
  }
}
```

## 9. Success Metrics V2

### 9.1 Operational Metrics
- Calculation accuracy: 99.99%
- Audit trail completeness: 100%
- Factor logging rate: 100%
- Reconstruction accuracy: 100%
- Query performance: < 100ms for detail retrieval

### 9.2 Compliance Metrics
- Regulatory report generation: < 5 minutes
- Historical calculation access: < 1 second
- Audit trail retention: 7+ years
- Factor change tracking: 100% coverage

## 10. Appendix: Complete Calculation Example

### 10.1 Sample Rate Calculation Audit Trail

```json
{
  "rate": {
    "id": "rate-123",
    "quote_id": "quote-456",
    "rate_type": "new_business",
    "total_premium": 834.07,
    "total_base_premium": 765.00,
    "total_discounts": -68.85,
    "total_surcharges": 75.50,
    "total_fees": 5.00,
    "total_taxes": 57.42
  },
  "lines": [
    {
      "id": "line-1",
      "line_type": "coverage",
      "coverage_type": "liability",
      "base_premium": 326.00,
      "adjusted_premium": 358.60,
      "final_premium": 358.60,
      "total_factor": 1.10
    }
  ],
  "factors": [
    {
      "id": "factor-1",
      "factor_code": "territory-base-rate",
      "factor_name": "Territory 06 Base Rate",
      "sequence_number": 1,
      "factor_value": 1.0,
      "impact_amount": 326.00,
      "lookup_key": "06",
      "lookup_table": "territory-base-rates"
    },
    {
      "id": "factor-2",
      "factor_code": "vehicle-age",
      "factor_name": "Vehicle Age Factor",
      "sequence_number": 2,
      "factor_value": 0.95,
      "impact_amount": -16.30,
      "lookup_key": "2019",
      "lookup_table": "vehicle-age-factors"
    },
    {
      "id": "factor-3",
      "factor_code": "driver-class",
      "factor_name": "Driver Class Factor",
      "sequence_number": 3,
      "factor_value": 1.15,
      "impact_amount": 48.90,
      "lookup_key": "standard",
      "lookup_table": "driver-class-factors"
    }
  ],
  "calculations": [
    {
      "step_number": 1,
      "operation": "lookup",
      "formula": "BaseRate = TerritoryLookup(06, liability)",
      "input_values": {"territory": "06", "coverage": "liability"},
      "output_value": 326.00,
      "running_total": 326.00
    },
    {
      "step_number": 2,
      "operation": "multiply",
      "formula": "AdjustedRate = BaseRate * VehicleAgeFactor",
      "input_values": {"base": 326.00, "factor": 0.95},
      "output_value": 309.70,
      "running_total": 309.70
    },
    {
      "step_number": 3,
      "operation": "multiply",
      "formula": "FinalRate = AdjustedRate * DriverClassFactor",
      "input_values": {"adjusted": 309.70, "factor": 1.15},
      "output_value": 358.60,
      "running_total": 358.60
    }
  ]
}
```

This V2 approach provides complete transparency and auditability while maintaining high performance through careful schema design and optimization strategies.