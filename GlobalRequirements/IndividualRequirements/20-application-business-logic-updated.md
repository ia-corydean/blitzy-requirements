# 20.0 Application Business Logic - Updated

## Laravel Framework Architecture

### Laravel 11.x Foundation
- **Purpose**: Primary framework for business logic, API development, and service orchestration
- **Architecture**: Mono-repo approach initially, with planned microservice separation
- **Philosophy**: Convention over configuration with enterprise flexibility
- **Performance**: Optimized with OPcache, route caching, and query optimization

### Core Framework Features
- **Service Container**: Powerful IoC container for dependency injection
- **Service Providers**: Modular service bootstrapping and registration
- **Facades**: Convenient static interfaces to services
- **Contracts**: Interface-based programming for flexibility
- **Middleware Pipeline**: Request/response filtering and modification

## Business Domain Structure

### Domain-Driven Design Implementation
```
app/
├── Domain/
│   ├── Policy/
│   │   ├── Models/
│   │   ├── Services/
│   │   ├── Repositories/
│   │   ├── Events/
│   │   └── Actions/
│   ├── Claims/
│   ├── Accounting/
│   ├── Producer/
│   └── Communication/
├── Application/
│   ├── Http/
│   ├── Console/
│   └── Jobs/
└── Infrastructure/
    ├── Database/
    ├── External/
    └── Cache/
```

### Business Logic Layers

#### Domain Layer
- **Entities**: Core business objects (Policy, Claim, Payment)
- **Value Objects**: Immutable domain concepts (Money, PolicyNumber)
- **Domain Services**: Complex business operations
- **Domain Events**: Business-significant occurrences
- **Specifications**: Business rule encapsulation

#### Application Layer
- **Use Cases**: Application-specific business flows
- **DTOs**: Data transfer objects for API communication
- **Commands/Queries**: CQRS pattern implementation
- **Application Services**: Orchestration of domain services
- **Validation**: Request validation and business rule enforcement

## Core Business Modules

### Policy Management
```php
namespace App\Domain\Policy\Services;

class PolicyService
{
    public function createPolicy(PolicyData $data): Policy
    {
        // Validate business rules
        $this->validator->validatePolicyData($data);
        
        // Calculate premium
        $premium = $this->ratingEngine->calculatePremium($data);
        
        // Create policy entity
        $policy = Policy::create([
            'number' => $this->generatePolicyNumber(),
            'effective_date' => $data->effectiveDate,
            'premium' => $premium,
            'status' => PolicyStatus::QUOTED,
        ]);
        
        // Dispatch domain events
        event(new PolicyCreated($policy));
        
        return $policy;
    }
    
    public function bindPolicy(Policy $policy): Policy
    {
        // Business rule validation
        if (!$policy->canBeBound()) {
            throw new PolicyCannotBeBoundException();
        }
        
        // Payment verification
        $this->paymentService->verifyInitialPayment($policy);
        
        // Update status
        $policy->bind();
        
        // Generate documents
        $this->documentService->generatePolicyDocuments($policy);
        
        // Dispatch events
        event(new PolicyBound($policy));
        
        return $policy;
    }
}
```

### Claims Processing
```php
namespace App\Domain\Claims\Services;

class ClaimsService
{
    public function reportClaim(ClaimData $data): Claim
    {
        // Verify policy is active
        $policy = $this->policyRepository->findOrFail($data->policyId);
        $this->validator->validateClaimEligibility($policy);
        
        // Create claim
        $claim = Claim::create([
            'claim_number' => $this->generateClaimNumber(),
            'policy_id' => $policy->id,
            'loss_date' => $data->lossDate,
            'reported_date' => now(),
            'status' => ClaimStatus::REPORTED,
        ]);
        
        // Auto-assignment logic
        $adjuster = $this->assignmentService->assignAdjuster($claim);
        $claim->assignTo($adjuster);
        
        // Fraud detection
        $this->fraudService->analyzeClaimForFraud($claim);
        
        event(new ClaimReported($claim));
        
        return $claim;
    }
}
```

### Payment Processing
```php
namespace App\Domain\Accounting\Services;

class PaymentService
{
    public function processPayment(PaymentRequest $request): Payment
    {
        DB::transaction(function () use ($request) {
            // Create payment record
            $payment = Payment::create([
                'amount' => $request->amount,
                'method' => $request->method,
                'status' => PaymentStatus::PENDING,
            ]);
            
            // Process with payment gateway
            $response = $this->paymentGateway->charge($request);
            
            if ($response->isSuccessful()) {
                $payment->markAsSuccessful($response->transactionId);
                
                // Apply payment to policy
                $this->applyPaymentToPolicy($payment, $request->policyId);
                
                // Calculate commission
                $this->commissionService->calculateCommission($payment);
                
                event(new PaymentProcessed($payment));
            } else {
                $payment->markAsFailed($response->errorMessage);
                event(new PaymentFailed($payment));
            }
            
            return $payment;
        });
    }
}
```

## Business Rules Engine

### Rule Definition
```php
namespace App\Domain\Shared\Rules;

interface BusinessRule
{
    public function isSatisfiedBy($entity): bool;
    public function getErrorMessage(): string;
}

class PolicyBindingRule implements BusinessRule
{
    public function isSatisfiedBy($policy): bool
    {
        return $policy->status === PolicyStatus::QUOTED
            && $policy->hasValidPayment()
            && $policy->effective_date >= now()
            && $policy->isUnderwritingApproved();
    }
    
    public function getErrorMessage(): string
    {
        return 'Policy does not meet binding requirements';
    }
}
```

### Rule Execution
```php
class RuleEngine
{
    public function validate($entity, array $rules): ValidationResult
    {
        $errors = [];
        
        foreach ($rules as $rule) {
            if (!$rule->isSatisfiedBy($entity)) {
                $errors[] = $rule->getErrorMessage();
            }
        }
        
        return new ValidationResult($errors);
    }
}
```

## Event-Driven Architecture

### Domain Events
```php
namespace App\Domain\Policy\Events;

class PolicyBound extends DomainEvent
{
    public function __construct(
        public Policy $policy,
        public Carbon $occurredAt = null
    ) {
        $this->occurredAt = $occurredAt ?? now();
    }
    
    public function broadcastOn()
    {
        return new Channel("tenant.{$this->policy->tenant_id}.policies");
    }
    
    public function toArray()
    {
        return [
            'policy_id' => $this->policy->id,
            'policy_number' => $this->policy->number,
            'effective_date' => $this->policy->effective_date,
            'premium' => $this->policy->premium,
            'occurred_at' => $this->occurredAt,
        ];
    }
}
```

### Event Listeners
```php
namespace App\Application\Listeners;

class PolicyEventSubscriber
{
    public function handlePolicyBound(PolicyBound $event): void
    {
        // Send confirmation email
        dispatch(new SendPolicyConfirmation($event->policy));
        
        // Generate documents
        dispatch(new GeneratePolicyDocuments($event->policy));
        
        // Update producer commission
        dispatch(new CalculateProducerCommission($event->policy));
        
        // Regulatory reporting
        dispatch(new SubmitRegulatoryFiling($event->policy));
    }
    
    public function subscribe($events)
    {
        return [
            PolicyBound::class => 'handlePolicyBound',
            PolicyRenewed::class => 'handlePolicyRenewed',
            PolicyCancelled::class => 'handlePolicyCancelled',
        ];
    }
}
```

## API Layer

### RESTful API Design
```php
namespace App\Application\Http\Controllers\Api;

class PolicyController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $policies = QueryBuilder::for(Policy::class)
            ->allowedFilters(['status', 'effective_date', 'producer_id'])
            ->allowedSorts(['created_at', 'premium', 'effective_date'])
            ->allowedIncludes(['insured', 'coverages', 'documents'])
            ->paginate($request->get('per_page', 15));
            
        return PolicyResource::collection($policies);
    }
    
    public function store(CreatePolicyRequest $request): JsonResponse
    {
        $policy = $this->policyService->createPolicy(
            PolicyData::fromRequest($request)
        );
        
        return new PolicyResource($policy);
    }
}
```

### API Resources
```php
namespace App\Application\Http\Resources;

class PolicyResource extends JsonResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'policy_number' => $this->number,
            'status' => $this->status,
            'effective_date' => $this->effective_date->toISOString(),
            'expiration_date' => $this->expiration_date->toISOString(),
            'premium' => $this->premium->toArray(),
            'insured' => new InsuredResource($this->whenLoaded('insured')),
            'coverages' => CoverageResource::collection($this->whenLoaded('coverages')),
            'documents' => DocumentResource::collection($this->whenLoaded('documents')),
            'created_at' => $this->created_at->toISOString(),
            'updated_at' => $this->updated_at->toISOString(),
        ];
    }
}
```

## Background Jobs and Queues

### Job Processing
```php
namespace App\Application\Jobs;

class GeneratePolicyDocuments implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;
    
    public function __construct(
        private Policy $policy
    ) {}
    
    public function handle(
        DocumentService $documentService,
        StorageService $storageService
    ): void {
        // Generate PDF documents
        $documents = $documentService->generatePolicyPacket($this->policy);
        
        foreach ($documents as $document) {
            // Store in S3
            $path = $storageService->store($document, "policies/{$this->policy->id}");
            
            // Save reference in database
            $this->policy->documents()->create([
                'type' => $document->type,
                'path' => $path,
                'generated_at' => now(),
            ]);
        }
        
        // Notify insured
        event(new PolicyDocumentsGenerated($this->policy));
    }
    
    public function failed(Throwable $exception): void
    {
        // Log failure and notify administrators
        Log::error('Document generation failed', [
            'policy_id' => $this->policy->id,
            'error' => $exception->getMessage(),
        ]);
        
        // Retry logic or manual intervention
    }
}
```

## Caching Strategy

### Cache Implementation
```php
namespace App\Infrastructure\Cache;

class PolicyCache
{
    private const TTL = 3600; // 1 hour
    
    public function remember(string $policyId, Closure $callback): Policy
    {
        return Cache::tags(['policies', "tenant:{$this->tenantId}"])
            ->remember(
                "policy:{$policyId}",
                self::TTL,
                $callback
            );
    }
    
    public function forget(string $policyId): void
    {
        Cache::tags(['policies', "tenant:{$this->tenantId}"])
            ->forget("policy:{$policyId}");
    }
    
    public function flush(): void
    {
        Cache::tags(['policies', "tenant:{$this->tenantId}"])->flush();
    }
}
```

## Integration Patterns

### External Service Integration
```php
namespace App\Infrastructure\External;

class RatingEngineService
{
    public function calculatePremium(PolicyData $data): Premium
    {
        $response = Http::withToken($this->apiToken)
            ->retry(3, 100)
            ->timeout(10)
            ->post($this->endpoint . '/rate', [
                'effective_date' => $data->effectiveDate,
                'coverages' => $data->coverages,
                'risk_factors' => $data->riskFactors,
            ]);
            
        if ($response->failed()) {
            // Fallback to local rating
            return $this->localRatingEngine->calculate($data);
        }
        
        return Premium::fromArray($response->json());
    }
}
```

## Testing Business Logic

### Unit Testing
```php
namespace Tests\Unit\Domain\Policy;

class PolicyServiceTest extends TestCase
{
    public function test_policy_can_be_bound_with_valid_payment()
    {
        // Arrange
        $policy = Policy::factory()->quoted()->create();
        $payment = Payment::factory()->successful()->create([
            'policy_id' => $policy->id,
        ]);
        
        // Act
        $boundPolicy = $this->policyService->bindPolicy($policy);
        
        // Assert
        $this->assertEquals(PolicyStatus::BOUND, $boundPolicy->status);
        $this->assertNotNull($boundPolicy->bound_at);
        
        // Verify events dispatched
        Event::assertDispatched(PolicyBound::class);
    }
}
```

### Integration Testing
```php
namespace Tests\Feature;

class PolicyApiTest extends TestCase
{
    public function test_create_policy_with_valid_data()
    {
        $response = $this->postJson('/api/policies', [
            'effective_date' => now()->addDays(30),
            'coverages' => [
                ['type' => 'liability', 'limit' => 1000000],
                ['type' => 'collision', 'deductible' => 500],
            ],
            'insured' => [
                'name' => 'John Doe',
                'address' => '123 Main St',
            ],
        ]);
        
        $response->assertCreated()
            ->assertJsonStructure([
                'data' => [
                    'id',
                    'policy_number',
                    'premium',
                    'status',
                ],
            ]);
    }
}
```