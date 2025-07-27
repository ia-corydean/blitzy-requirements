# 02.0 Database Migrations - Updated

## Database Migration Strategy

### Database Architecture Overview
- **Primary Database**: MariaDB for transactional data
- **Single Database**: For containing all application tables
- **Type-Based Architecture**: Each entity has corresponding _type tables
- **Standard Audit Fields**: All tables include audit tracking

### Technology Stack Integration
- **Laravel Migration Framework**: Standard Laravel migrations
- **Database Driver**: Laravel's native MariaDB driver with connection pooling
- **Migration Engine**: Laravel's schema builder

## Core Migration Framework

### Base Migration Class
```php
// BaseMigration.php - Base class for standard migrations
abstract class BaseMigration extends Migration
{
    /**
     * Add standard audit fields to any table
     */
    protected function addAuditFields(Blueprint $table): void
    {
        $table->integer('created_by')->nullable();
        $table->integer('updated_by')->nullable();
        $table->timestamp('created_at')->nullable()->default(DB::raw('CURRENT_TIMESTAMP'));
        $table->timestamp('updated_at')->nullable()->default(DB::raw('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'));
        
        // Add indexes
        $table->index('created_at');
    }
    
    /**
     * Add status field with foreign key
     */
    protected function addStatusField(Blueprint $table): void
    {
        $table->integer('status_id')->nullable();
        $table->foreign('status_id')->references('id')->on('status');
        $table->index('status_id');
    }
    
    /**
     * Add type reference pattern
     */
    protected function addTypeReference(Blueprint $table, string $typeName): void
    {
        $typeField = $typeName . '_type_id';
        $table->integer($typeField);
        $table->foreign($typeField)->references('id')->on($typeName . '_type');
        $table->index($typeField);
    }
}
```

### Database Patterns

#### Type Table Pattern
Every major entity has a corresponding type table:
```php
// Example: Create Entity Type Table
class CreateEntityTypeTable extends Migration
{
    public function up()
    {
        Schema::create('entity_type', function (Blueprint $table) {
            $table->integer('id', true);
            $table->string('code', 50)->unique();
            $table->string('name', 100);
            $table->text('description')->nullable();
            $table->boolean('is_default')->default(false);
            $table->integer('status_id')->nullable();
            $table->integer('created_by')->nullable();
            $table->integer('updated_by')->nullable();
            $table->timestamp('created_at')->nullable()->default(DB::raw('CURRENT_TIMESTAMP'));
            $table->timestamp('updated_at')->nullable()->default(DB::raw('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'));
            
            // Indexes
            $table->index('code');
            $table->index('status_id');
            
            // Foreign keys
            $table->foreign('status_id')->references('id')->on('status');
        });
    }
    
    public function down()
    {
        Schema::dropIfExists('entity_type');
    }
}
```

#### Main Entity Table Pattern
```php
// Example: Create Entity Table
class CreateEntityTable extends BaseMigration
{
    public function up()
    {
        Schema::create('entity', function (Blueprint $table) {
            $table->integer('id', true);
            
            // Type reference
            $this->addTypeReference($table, 'entity');
            
            // Standard fields
            $this->addStatusField($table);
            $this->addAuditFields($table);
            
            // Additional indexes
            $table->index('created_at');
        });
    }
    
    public function down()
    {
        Schema::dropIfExists('entity');
    }
}
```

#### Map Table Pattern
For many-to-many relationships:
```php
// Example: Create Map Table
class CreateMapPolicyDriverTable extends Migration
{
    public function up()
    {
        Schema::create('map_policy_driver', function (Blueprint $table) {
            $table->integer('id', true);
            $table->integer('policy_id');
            $table->integer('driver_id');
            $table->boolean('is_primary_driver')->default(false);
            $table->integer('created_by')->nullable();
            $table->integer('updated_by')->nullable();
            $table->timestamp('created_at')->nullable()->default(DB::raw('CURRENT_TIMESTAMP'));
            $table->timestamp('updated_at')->nullable()->default(DB::raw('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'));
            
            // Indexes
            $table->index('policy_id');
            $table->index('driver_id');
            $table->unique(['policy_id', 'driver_id']);
            
            // Foreign keys
            $table->foreign('policy_id')->references('id')->on('policy');
            $table->foreign('driver_id')->references('id')->on('driver');
        });
    }
    
    public function down()
    {
        Schema::dropIfExists('map_policy_driver');
    }
}
```

### Core Insurance Domain Migrations

#### User Management Migration
```php
// Create Users Table
class CreateUserTable extends BaseMigration
{
    public function up()
    {
        Schema::create('user', function (Blueprint $table) {
            $table->integer('id', true);
            
            // Type reference
            $this->addTypeReference($table, 'user');
            
            // User fields
            $table->integer('name_id')->nullable();
            $table->integer('role_id')->nullable();
            $table->string('email', 255)->unique()->nullable();
            $table->string('username', 100)->unique()->nullable();
            $table->string('password', 255)->nullable();
            $table->string('phone', 20)->nullable();
            $table->boolean('mfa_enabled')->default(false);
            $table->string('mfa_secret', 255)->nullable();
            $table->boolean('email_verified')->default(false);
            $table->boolean('phone_verified')->default(false);
            $table->timestamp('last_login_at')->nullable();
            $table->integer('failed_login_attempts')->default(0);
            $table->timestamp('locked_until')->nullable();
            $table->timestamp('password_changed_at')->nullable();
            $table->integer('signature_id')->nullable();
            $table->integer('language_preference_id')->nullable();
            $table->string('password_reset_token', 255)->nullable();
            $table->timestamp('password_reset_expires')->nullable();
            
            // Standard fields
            $this->addStatusField($table);
            $this->addAuditFields($table);
            
            // Indexes
            $table->index('email');
            $table->index('role_id');
            $table->index('name_id');
            
            // Foreign keys
            $table->foreign('name_id')->references('id')->on('name');
            $table->foreign('role_id')->references('id')->on('role');
            $table->foreign('signature_id')->references('id')->on('signature');
            $table->foreign('language_preference_id')->references('id')->on('language');
        });
    }
    
    public function down()
    {
        Schema::dropIfExists('user');
    }
}
```

#### Policy Management Migration
```php
// Create Policy Table
class CreatePolicyTable extends BaseMigration
{
    public function up()
    {
        Schema::create('policy', function (Blueprint $table) {
            $table->integer('id', true);
            
            // Type reference
            $this->addTypeReference($table, 'policy');
            
            // Policy fields
            $table->string('policy_number', 50)->unique()->nullable();
            $table->integer('program_id')->nullable();
            $table->integer('quote_id')->nullable();
            $table->integer('producer_id')->nullable();
            $table->date('effective_date')->nullable();
            $table->date('expiration_date')->nullable();
            $table->decimal('premium', 10, 2)->nullable();
            $table->timestamp('bound_date')->nullable();
            $table->date('cancellation_date')->nullable();
            $table->integer('cancellation_reason_id')->nullable();
            $table->date('reinstatement_date')->nullable();
            $table->date('non_renewal_date')->nullable();
            $table->integer('non_renewal_reason_id')->nullable();
            $table->integer('total_vehicles')->default(0);
            $table->integer('total_drivers')->default(0);
            $table->integer('payment_plan_id')->nullable();
            $table->decimal('down_payment', 10, 2)->nullable();
            $table->date('paid_to_date')->nullable();
            $table->decimal('total_paid', 10, 2)->default(0.00);
            $table->decimal('balance_due', 10, 2)->default(0.00);
            
            // Standard fields
            $this->addStatusField($table);
            $this->addAuditFields($table);
            
            // Indexes
            $table->index('policy_number');
            $table->index('program_id');
            $table->index('quote_id');
            $table->index('producer_id');
            $table->index('effective_date');
            $table->index('cancellation_date');
            $table->index('paid_to_date');
            
            // Foreign keys
            $table->foreign('program_id')->references('id')->on('program');
            $table->foreign('quote_id')->references('id')->on('quote');
            $table->foreign('producer_id')->references('id')->on('producer');
            $table->foreign('cancellation_reason_id')->references('id')->on('cancellation_reason');
            $table->foreign('non_renewal_reason_id')->references('id')->on('non_renewal_type');
            $table->foreign('payment_plan_id')->references('id')->on('payment_plan');
        });
    }
    
    public function down()
    {
        Schema::dropIfExists('policy');
    }
}
```

## Migration Testing and Validation

### Migration Testing Framework
```php
// MigrationTestCase.php - Base test class for migration testing
abstract class MigrationTestCase extends TestCase
{
    use RefreshDatabase;
    
    /**
     * Test migration up and down
     */
    public function test_migration_up_and_down(): void
    {
        // Test migration up
        $this->artisan('migrate', ['--path' => $this->getMigrationPath()])
             ->assertExitCode(0);
        
        // Verify table structure
        $this->assertDatabaseHasTable($this->getTableName());
        $this->assertTableStructure();
        
        // Test migration rollback
        $this->artisan('migrate:rollback', ['--path' => $this->getMigrationPath()])
             ->assertExitCode(0);
        
        // Verify table is dropped
        $this->assertDatabaseMissingTable($this->getTableName());
    }
    
    /**
     * Test standard fields exist
     */
    public function test_standard_fields_exist(): void
    {
        $this->artisan('migrate', ['--path' => $this->getMigrationPath()])
             ->assertExitCode(0);
        
        $columns = Schema::getColumnListing($this->getTableName());
        
        // Verify audit fields
        $this->assertContains('created_by', $columns);
        $this->assertContains('updated_by', $columns);
        $this->assertContains('created_at', $columns);
        $this->assertContains('updated_at', $columns);
        
        // Verify status field if applicable
        if ($this->hasStatusField()) {
            $this->assertContains('status_id', $columns);
        }
    }
    
    abstract protected function getMigrationPath(): string;
    abstract protected function getTableName(): string;
    abstract protected function assertTableStructure(): void;
    abstract protected function hasStatusField(): bool;
}
```

## Environment-Specific Migration Strategies

### Development Environment
```bash
# Run all migrations
php artisan migrate

# Run specific migration
php artisan migrate --path=database/migrations/2024_01_01_000001_create_status_table.php

# Rollback migrations
php artisan migrate:rollback --step=1

# Fresh migration (drop all tables and re-run)
php artisan migrate:fresh
```

### Production Migration Safety
```php
// ProductionMigrationCommand.php - Safe production migrations
class ProductionMigrationCommand extends Command
{
    protected $signature = 'migrate:production {--dry-run} {--backup}';
    
    public function handle(): void
    {
        if ($this->option('backup')) {
            $this->createBackup();
        }
        
        if ($this->option('dry-run')) {
            $this->performDryRun();
            return;
        }
        
        // Check maintenance mode
        if (!$this->laravel->isDownForMaintenance()) {
            $this->error('Production migrations require maintenance mode');
            return;
        }
        
        // Execute migrations with monitoring
        $this->executeWithMonitoring();
    }
    
    private function createBackup(): void
    {
        $this->info('Creating database backup...');
        $filename = 'backup_' . date('Y_m_d_His') . '.sql';
        
        $this->call('db:backup', [
            '--filename' => $filename,
            '--compress' => true
        ]);
    }
    
    private function executeWithMonitoring(): void
    {
        $startTime = microtime(true);
        
        try {
            $this->call('migrate', ['--force' => true]);
            
            $duration = microtime(true) - $startTime;
            $this->logMigrationSuccess($duration);
            
        } catch (Exception $e) {
            $this->logMigrationFailure($e);
            
            if ($this->option('backup')) {
                $this->restoreBackup();
            }
            
            throw $e;
        }
    }
}
```

## Migration Documentation and Standards

### Migration Naming Conventions
- **Format**: `YYYY_MM_DD_HHMMSS_descriptive_migration_name.php`
- **Table Creation**: `create_[table_name]_table.php`
- **Table Modification**: `add_[field]_to_[table]_table.php`
- **Indexes**: Include purpose in index name (e.g., `idx_policy_effective_date`)
- **Foreign Keys**: Include referenced table in constraint name

### Migration Best Practices
1. **Atomic Operations**: Each migration should be atomic and reversible
2. **Performance**: Consider impact on large datasets
3. **Testing**: Comprehensive test coverage for all migration scenarios
4. **Documentation**: Clear comments explaining complex migration logic
5. **Backward Compatibility**: Ensure migrations don't break existing functionality
6. **Index Strategy**: Add indexes for foreign keys and commonly queried fields

### Standard Table Requirements
All tables must include:
1. Primary key field (`id`)
2. Audit fields (created_by, updated_by, created_at, updated_at)
3. Status field where applicable
4. Appropriate indexes for performance
5. Foreign key constraints with proper naming

This database migration framework provides comprehensive single-database migration strategies with security, performance, and maintainability considerations for the insurance management system.