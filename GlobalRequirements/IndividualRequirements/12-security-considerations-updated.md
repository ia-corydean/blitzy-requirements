# 12.0 Security Considerations - Updated

## Security Framework Overview

### Defense in Depth Strategy
- **Multi-Layer Security**: Application, network, infrastructure, and data protection
- **Zero Trust Architecture**: Never trust, always verify approach
- **Insurance Industry Compliance**: SOX, HIPAA, PCI DSS, GDPR, CCPA requirements
- **Threat Modeling**: Systematic identification and mitigation of security threats
- **Security by Design**: Security integrated throughout development lifecycle

## Authentication & Authorization

### OAuth2/JWT Implementation
```php
// Laravel Passport OAuth2 configuration
class AuthController extends Controller
{
    public function login(LoginRequest $request)
    {
        $credentials = $request->validated();
        
        if (!Auth::attempt($credentials)) {
            throw new AuthenticationException('Invalid credentials');
        }
        
        $user = Auth::user();
        $scopes = $this->getUserScopes($user);
        
        $token = $user->createToken('insurance-app', $scopes)->accessToken;
        
        // Log successful authentication
        AuditLog::create([
            'user_id' => $user->id,
            'action' => 'user_login',
            'ip_address' => $request->ip(),
            'user_agent' => $request->userAgent(),
            'metadata' => ['tenant_id' => $user->tenant_id]
        ]);
        
        return response()->json([
            'access_token' => $token,
            'token_type' => 'Bearer',
            'expires_at' => now()->addHour() // V4 Update: 1-hour expiration
        ]);
    }
    
    private function getUserScopes(User $user): array
    {
        return $user->roles->flatMap->permissions
            ->pluck('name')
            ->unique()
            ->toArray();
    }
}
```

### Portal-Specific MFA Requirements (V4 Update)
```php
// MFAConfiguration.php - Different requirements per portal
class MFAConfiguration
{
    const PORTAL_MFA_REQUIREMENTS = [
        'producer' => [
            'required' => false,  // V4: No MFA for producer portal
            'methods' => ['optional'],
        ],
        'policy' => [
            'required' => true,   // V4: MFA mandatory
            'methods' => ['totp', 'sms', 'biometric'],
        ],
        'claims' => [
            'required' => true,   // V4: MFA mandatory
            'methods' => ['totp', 'sms', 'biometric'],
        ],
        'insured' => [
            'required' => true,   // V4: MFA mandatory
            'methods' => ['totp', 'sms', 'email'],
        ],
    ];
}
```

### Multi-Factor Authentication (MFA) Implementation
- **TOTP Implementation**: Time-based One-Time Password using Google Authenticator
- **SMS/Email Backup**: Secondary authentication methods
- **Biometric Support**: Touch ID, Face ID for mobile applications
- **Hardware Tokens**: Support for FIDO2/WebAuthn security keys
- **Portal-Specific**: MFA enforced based on portal type (V4)

### Role-Based Access Control (RBAC)
```php
// Permission-based authorization
class PolicyController extends Controller
{
    public function store(StorePolicyRequest $request)
    {
        $this->authorize('create-policy', [
            'tenant_id' => auth()->user()->tenant_id,
            'program_id' => $request->program_id
        ]);
        
        // Tenant isolation middleware ensures data separation
        $policy = Policy::create([
            'tenant_id' => auth()->user()->tenant_id,
            'created_by' => auth()->id(),
            ...$request->validated()
        ]);
        
        return new PolicyResource($policy);
    }
}

// Custom authorization policy
class PolicyPolicy
{
    public function create(User $user, array $context): bool
    {
        // Verify tenant access
        if ($user->tenant_id !== $context['tenant_id']) {
            return false;
        }
        
        // Check specific permissions
        return $user->hasPermissionTo('create-policy') &&
               $user->hasAccessToProgram($context['program_id']);
    }
}
```

## PCI DSS Compliance Architecture (V4 Update)

### Built-in PCI Compliance
```php
// PCIComplianceService.php - Security by design for payment handling
class PCIComplianceService
{
    /**
     * V4: Dual compliance approach - continuous + periodic validation
     */
    const COMPLIANCE_STRATEGY = [
        'continuous' => [
            'automated_scanning' => 'daily',
            'configuration_validation' => 'real-time',
            'vulnerability_detection' => 'continuous',
            'compliance_dashboard' => 'always available',
        ],
        'periodic' => [
            'quarterly_assessment' => 'SAQ-D',
            'annual_audit' => 'third-party',
            'penetration_testing' => 'semi-annual',
            'security_review' => 'monthly',
        ],
    ];

    /**
     * Six PCI DSS Requirements Implementation
     */
    public function validatePCICompliance(): ComplianceReport
    {
        $results = [];
        
        // 1. Build and Maintain Secure Network
        $results['network'] = $this->validateNetworkSecurity();
        
        // 2. Protect Cardholder Data (We don't store any)
        $results['data_protection'] = $this->validateNoCardStorage();
        
        // 3. Maintain Vulnerability Management Program
        $results['vulnerability'] = $this->validateVulnerabilityManagement();
        
        // 4. Implement Strong Access Control
        $results['access_control'] = $this->validateAccessControls();
        
        // 5. Monitor and Test Networks
        $results['monitoring'] = $this->validateMonitoring();
        
        // 6. Maintain Information Security Policy
        $results['policy'] = $this->validateSecurityPolicy();
        
        return new ComplianceReport($results);
    }
    
    private function validateNoCardStorage(): array
    {
        // Scan all database tables for card patterns
        $violations = DB::select("
            SELECT table_name, column_name 
            FROM information_schema.columns 
            WHERE column_name LIKE '%card%' 
               OR column_name LIKE '%cc%'
               OR column_name LIKE '%credit%'
        ");
        
        foreach ($violations as $column) {
            // Check for actual card data patterns
            $hasCardData = $this->scanForCardPatterns(
                $column->table_name, 
                $column->column_name
            );
            
            if ($hasCardData) {
                throw new PCIViolationException(
                    "Card data found in {$column->table_name}.{$column->column_name}"
                );
            }
        }
        
        return ['status' => 'compliant', 'message' => 'No card data storage detected'];
    }
}
```

### Payment Tokenization Only
```php
// TokenizationService.php - Never touch actual card data
class TokenizationService
{
    private PaymentGateway $gateway;
    
    public function tokenizePaymentMethod(array $paymentData): string
    {
        // Card data goes directly to payment gateway
        // We only receive and store tokens
        $token = $this->gateway->tokenize($paymentData);
        
        // Store only token reference
        PaymentMethod::create([
            'user_id' => auth()->id(),
            'token' => $token->id,
            'last_four' => $token->last_four,
            'brand' => $token->brand,
            'exp_month' => $token->exp_month,
            'exp_year' => $token->exp_year,
        ]);
        
        // Log tokenization for audit
        SecurityAudit::log('payment_tokenization', [
            'user_id' => auth()->id(),
            'token_created' => true,
            'gateway' => $this->gateway->name,
        ]);
        
        return $token->id;
    }
}
```

## Data Protection & Encryption (V4 Update)

### Field-Level Encryption with Viewing Capability
```php
// V4: Updated encryption for viewable PII fields
class EncryptedModel extends Model
{
    protected $casts = [
        'ssn' => 'encrypted:reversible',
        'driver_license' => 'encrypted:reversible', // V4: Viewable
        'date_of_birth' => 'encrypted:reversible', // V4: Viewable
        'bank_account' => 'encrypted:masked',
        'medical_records' => 'encrypted:json'
    ];
    
    protected $encrypted = [
        'ssn', 'bank_account', 'medical_records'
    ];
    
    public function getEncryptedAttributes(): array
    {
        return $this->encrypted;
    }
}

// Custom encryption cast
class EncryptedCast implements CastsAttributes
{
    public function get($model, string $key, $value, array $attributes)
    {
        return $value ? decrypt($value) : null;
    }
    
    public function set($model, string $key, $value, array $attributes)
    {
        return $value ? encrypt($value) : null;
    }
}
```

### Encryption in Transit
- **TLS 1.3**: Minimum encryption standard for all communications
- **Certificate Management**: Automated SSL certificate provisioning via Let's Encrypt
- **API Security**: HTTPS-only APIs with HSTS headers
- **Database Connections**: Encrypted connections to AWS RDS

### AWS KMS Integration
```yaml
# AWS KMS key management
Resources:
  InsuranceDataKey:
    Type: AWS::KMS::Key
    Properties:
      Description: "Insurance application data encryption key"
      KeyPolicy:
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub "arn:aws:iam::${AWS::AccountId}:root"
            Action: "kms:*"
            Resource: "*"
          - Effect: Allow
            Principal:
              AWS: !GetAtt EKSServiceRole.Arn
            Action:
              - kms:Decrypt
              - kms:DescribeKey
            Resource: "*"
```

## Multi-Tenant Security

### Tenant Isolation
```php
// Tenant-aware middleware
class TenantIsolationMiddleware
{
    public function handle(Request $request, Closure $next)
    {
        $user = auth()->user();
        
        if (!$user || !$user->tenant_id) {
            throw new UnauthorizedException('Invalid tenant access');
        }
        
        // Set tenant context for queries
        TenantScope::setTenantId($user->tenant_id);
        
        // Validate API access to tenant resources
        if ($request->has('tenant_id') && 
            $request->tenant_id !== $user->tenant_id) {
            throw new ForbiddenException('Cross-tenant access denied');
        }
        
        return $next($request);
    }
}

// Global scope for tenant isolation
class TenantScope implements Scope
{
    public function apply(Builder $builder, Model $model)
    {
        if ($tenantId = static::getTenantId()) {
            $builder->where('tenant_id', $tenantId);
        }
    }
    
    public static function setTenantId(int $tenantId): void
    {
        app()->instance('tenant.id', $tenantId);
    }
    
    public static function getTenantId(): ?int
    {
        return app('tenant.id');
    }
}
```

### Database-Level Security
```sql
-- Row-level security for PostgreSQL
CREATE POLICY tenant_isolation_policy ON policies
    FOR ALL
    TO insurance_app_role
    USING (tenant_id = current_setting('app.current_tenant_id')::INTEGER);

-- Secure stored procedures for sensitive operations
CREATE OR REPLACE FUNCTION calculate_premium(
    policy_data JSONB,
    tenant_id_param INTEGER
) RETURNS DECIMAL
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    -- Verify tenant access
    IF tenant_id_param != current_setting('app.current_tenant_id')::INTEGER THEN
        RAISE EXCEPTION 'Unauthorized tenant access';
    END IF;
    
    -- Premium calculation logic
    RETURN calculate_premium_internal(policy_data);
END;
$$ LANGUAGE plpgsql;
```

## API Security

### Kong API Gateway Security
```yaml
# Kong security plugins configuration
services:
  - name: insurance-api
    url: http://laravel-app:8000
    plugins:
      - name: jwt
        config:
          secret_is_base64: false
          key_claim_name: iss
          algorithm: RS256
      - name: rate-limiting
        config:
          minute: 1000
          hour: 10000
          policy: redis
      - name: request-size-limiting
        config:
          allowed_payload_size: 10
      - name: cors
        config:
          origins: ["https://app.insurance.com"]
          methods: ["GET", "POST", "PUT", "DELETE"]
          headers: ["Authorization", "Content-Type"]
          credentials: true
```

### Request Validation & Sanitization
```php
// Comprehensive input validation
class StorePolicyRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create-policy');
    }
    
    public function rules(): array
    {
        return [
            'insured_name' => ['required', 'string', 'max:255', 'regex:/^[a-zA-Z\s\-\'\.]+$/'],
            'policy_number' => ['required', 'string', 'regex:/^POL-[0-9]{6}$/', 'unique:policies'],
            'effective_date' => ['required', 'date', 'after:today'],
            'premium' => ['required', 'decimal:2', 'min:0', 'max:999999.99'],
            'coverage_limits' => ['required', 'array'],
            'coverage_limits.*.type' => ['required', 'string', 'in:liability,collision,comprehensive'],
            'coverage_limits.*.limit' => ['required', 'integer', 'min:0']
        ];
    }
    
    protected function prepareForValidation(): void
    {
        $this->merge([
            'insured_name' => strip_tags(trim($this->insured_name)),
            'policy_number' => strtoupper(trim($this->policy_number))
        ]);
    }
}
```

### SQL Injection Prevention
```php
// Parameterized queries and ORM usage
class PolicyRepository
{
    public function findByComplexCriteria(array $criteria): Collection
    {
        $query = Policy::query();
        
        // Safe dynamic query building
        if (isset($criteria['status'])) {
            $query->whereIn('status', $criteria['status']);
        }
        
        if (isset($criteria['date_range'])) {
            $query->whereBetween('effective_date', [
                Carbon::parse($criteria['date_range']['start']),
                Carbon::parse($criteria['date_range']['end'])
            ]);
        }
        
        // Always use parameter binding for raw queries
        if (isset($criteria['custom_sql'])) {
            $query->whereRaw('premium > ? AND tenant_id = ?', [
                $criteria['minimum_premium'],
                auth()->user()->tenant_id
            ]);
        }
        
        return $query->get();
    }
}
```

## Frontend Security (React)

### XSS Prevention
```typescript
// Secure component implementation
import DOMPurify from 'dompurify';

interface SafeHtmlProps {
  content: string;
  allowedTags?: string[];
}

const SafeHtml: React.FC<SafeHtmlProps> = ({ content, allowedTags = [] }) => {
  const sanitizedContent = DOMPurify.sanitize(content, {
    ALLOWED_TAGS: allowedTags,
    ALLOWED_ATTR: ['class', 'id', 'href', 'target'],
    FORBID_SCRIPT: true
  });
  
  return (
    <div 
      dangerouslySetInnerHTML={{ __html: sanitizedContent }}
      role="region"
      aria-label="User generated content"
    />
  );
};

// Secure form handling
const PolicyForm: React.FC = () => {
  const [formData, setFormData] = useState<PolicyFormData>({});
  
  const handleInputChange = (field: string, value: string) => {
    // Input sanitization
    const sanitizedValue = DOMPurify.sanitize(value, { ALLOWED_TAGS: [] });
    
    setFormData(prev => ({
      ...prev,
      [field]: sanitizedValue
    }));
  };
  
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    
    // Client-side validation
    const validatedData = PolicyFormSchema.parse(formData);
    
    try {
      await apiClient.post('/api/policies', validatedData);
    } catch (error) {
      // Secure error handling - don't expose internal details
      if (error.response?.status === 422) {
        setErrors(error.response.data.errors);
      } else {
        setErrors({ general: 'An unexpected error occurred' });
      }
    }
  };
};
```

### Content Security Policy (CSP)
```typescript
// CSP configuration
const cspConfig = {
  'default-src': ["'self'"],
  'script-src': [
    "'self'",
    "'unsafe-inline'", // For inline React scripts
    "https://apis.google.com"
  ],
  'style-src': [
    "'self'",
    "'unsafe-inline'",
    "https://fonts.googleapis.com"
  ],
  'font-src': [
    "'self'",
    "https://fonts.gstatic.com"
  ],
  'img-src': [
    "'self'",
    "data:",
    "https://secure.gravatar.com"
  ],
  'connect-src': [
    "'self'",
    "https://api.insurance.com",
    "wss://api.insurance.com"
  ],
  'frame-ancestors': ["'none'"],
  'base-uri': ["'self'"],
  'object-src': ["'none'"]
};
```

## Infrastructure Security

### AWS Security Configuration
```yaml
# EKS cluster security configuration
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: insurance-cluster
  region: us-west-2

vpc:
  enableDnsHostnames: true
  enableDnsSupport: true
  cidr: "10.0.0.0/16"

privateCluster:
  enabled: true
  additionalEndpointServices:
    - s3
    - cloudformation

secretsEncryption:
  keyARN: arn:aws:kms:us-west-2:123456789012:key/12345678-1234-1234-1234-123456789012

nodeGroups:
  - name: worker-nodes
    instanceType: t3.medium
    minSize: 2
    maxSize: 10
    volumeSize: 100
    volumeEncrypted: true
    securityGroups:
      attachIDs: ["sg-12345678"]
    ssh:
      enableSsm: true
```

### Network Security
```yaml
# Istio security policies
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: insurance-app
spec:
  mtls:
    mode: STRICT
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: insurance-api-access
  namespace: insurance-app
spec:
  selector:
    matchLabels:
      app: insurance-api
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/insurance-app/sa/frontend"]
  - to:
    - operation:
        methods: ["GET", "POST", "PUT", "DELETE"]
  - when:
    - key: request.headers[authorization]
      values: ["Bearer *"]
```

## Security Monitoring & Incident Response

### Security Event Logging
```php
// Comprehensive security logging
class SecurityLogger
{
    public static function logSecurityEvent(
        string $event,
        array $context = [],
        string $severity = 'info'
    ): void {
        $logData = [
            'event' => $event,
            'severity' => $severity,
            'user_id' => auth()->id(),
            'tenant_id' => auth()->user()?->tenant_id,
            'ip_address' => request()->ip(),
            'user_agent' => request()->userAgent(),
            'timestamp' => now()->toISOString(),
            'session_id' => session()->getId(),
            'context' => $context
        ];
        
        // Send to multiple logging destinations
        Log::channel('security')->info($event, $logData);
        
        // Critical events to SIEM
        if (in_array($severity, ['critical', 'high'])) {
            SiemLogger::dispatch($logData);
        }
        
        // Real-time alerting for immediate threats
        if ($severity === 'critical') {
            SecurityAlert::dispatch($logData);
        }
    }
}

// Usage in authentication
class LoginAttemptListener
{
    public function handle(LoginFailed $event): void
    {
        SecurityLogger::logSecurityEvent('login_failed', [
            'email' => $event->credentials['email'],
            'reason' => 'invalid_credentials'
        ], 'warning');
        
        // Rate limiting
        RateLimiter::hit('login_attempts:' . request()->ip(), 300);
        
        if (RateLimiter::tooManyAttempts('login_attempts:' . request()->ip(), 5)) {
            SecurityLogger::logSecurityEvent('login_rate_limit_exceeded', [
                'ip_address' => request()->ip()
            ], 'high');
        }
    }
}
```

### Vulnerability Management
```php
// Automated security scanning integration
class SecurityScanCommand extends Command
{
    protected $signature = 'security:scan';
    
    public function handle(): void
    {
        // Dependency vulnerability scanning
        $this->runComposerAudit();
        $this->runNpmAudit();
        
        // Code security analysis
        $this->runPhpStanSecurity();
        $this->runEslintSecurity();
        
        // Infrastructure scanning
        $this->runTerraformScan();
        $this->runDockerScan();
        
        $this->info('Security scan completed');
    }
    
    private function runComposerAudit(): void
    {
        $result = Process::run('composer audit --format=json');
        
        if (!$result->successful()) {
            $vulnerabilities = json_decode($result->output(), true);
            
            foreach ($vulnerabilities['advisories'] as $advisory) {
                SecurityVulnerability::create([
                    'type' => 'dependency',
                    'package' => $advisory['packageName'],
                    'severity' => $advisory['severity'],
                    'cve' => $advisory['cve'] ?? null,
                    'description' => $advisory['title'],
                    'fixed_version' => $advisory['sources'][0]['remoteId'] ?? null
                ]);
            }
        }
    }
}
```

## Comprehensive Audit Logging Requirements (V4 Update)

### PII Access Audit Logging
```php
// PIIAuditService.php - V4 comprehensive PII access logging
class PIIAuditService
{
    /**
     * Log every PII field access with context
     */
    public function logPIIAccess(string $field, string $operation, array $context): void
    {
        PIIAccessLog::create([
            'user_id' => auth()->id(),
            'field_accessed' => $field,
            'operation_type' => $operation, // view, update, delete, unmask
            'display_type' => $this->getDisplayType($field), // V4: direct, masked, unmasked
            'entity_type' => $context['entity_type'],
            'entity_id' => $context['entity_id'],
            'session_type' => auth()->user()->account_type, // shared or individual
            'portal_type' => $this->detectPortal(),
            'ip_address' => request()->ip(),
            'user_agent' => request()->userAgent(),
            'timestamp' => now(),
            'timezone' => config('app.timezone'),
            'success' => $context['success'] ?? true,
            'metadata' => $context,
        ]);
    }
    
    private function getDisplayType(string $field): string
    {
        // V4: DL and DOB are directly viewable
        if (in_array($field, ['driver_license', 'date_of_birth'])) {
            return 'direct';
        }
        
        // SSN is masked by default
        if ($field === 'ssn') {
            return request()->input('unmask') ? 'unmasked' : 'masked';
        }
        
        return 'encrypted';
    }
}
```

### Payment Operation Logging
```php
// PaymentAuditService.php - Comprehensive payment audit trail
class PaymentAuditService
{
    public function logPaymentOperation(string $operation, array $details): void
    {
        PaymentAuditLog::create([
            'transaction_reference' => $details['transaction_id'],
            'operation_type' => $operation,
            'amount' => $details['amount'] ?? 0,
            'currency' => $details['currency'] ?? 'USD',
            'payment_method_type' => $details['method_type'], // card, ach, check
            'gateway_used' => $details['gateway'],
            'user_id' => auth()->id(),
            'portal_type' => $this->detectPortal(),
            'result' => $details['success'] ? 'success' : 'failure',
            'error_code' => $details['error_code'] ?? null,
            'integration_response' => $details['gateway_response'] ?? null,
            'ip_address' => request()->ip(),
            'session_id' => session()->getId(),
            'timestamp' => now(),
        ]);
        
        // Additional NSF tracking if payment failed
        if (!$details['success'] && $details['nsf_indicator']) {
            $this->logNSFOccurrence($details);
        }
    }
}
```

### Retention Requirements
```php
class AuditRetentionPolicy
{
    const RETENTION_PERIODS = [
        'security_logs' => '1 year',
        'pii_access_logs' => '7 years',
        'payment_logs' => '7 years',
        'failed_authentication' => '90 days',
        'compliance_assessments' => '7 years',
        'penetration_test_results' => '3 years',
    ];
}
```

## Compliance Validation Approach (V4 Update)

### Dual Validation Strategy
```php
// ComplianceValidationService.php - Continuous + Periodic validation
class ComplianceValidationService
{
    /**
     * V4: Both continuous and periodic assessments required
     */
    public function runComplianceValidation(): ComplianceStatus
    {
        $results = [];
        
        // Continuous validation (automated daily)
        $results['continuous'] = [
            'security_monitoring' => $this->runSecurityMonitoring(),
            'configuration_validation' => $this->validateConfigurations(),
            'vulnerability_scanning' => $this->runVulnerabilityScans(),
            'compliance_dashboard' => $this->updateComplianceDashboard(),
        ];
        
        // Periodic assessments (scheduled)
        $results['periodic'] = [
            'quarterly_saq' => $this->getLastSAQStatus(),
            'semi_annual_pentest' => $this->getLastPentestResults(),
            'annual_pci_audit' => $this->getLastPCIAuditStatus(),
            'monthly_vulnerability' => $this->getMonthlyVulnResults(),
        ];
        
        return new ComplianceStatus($results);
    }
    
    private function runSecurityMonitoring(): array
    {
        return [
            'real_time_threat_detection' => $this->threatDetectionStatus(),
            'anomaly_detection' => $this->anomalyDetectionStatus(),
            'failed_auth_tracking' => $this->failedAuthAnalysis(),
            'automated_remediation' => $this->remediationStatus(),
        ];
    }
}
```

## Portal-Specific Security Requirements (V4 Update)

### Security Configuration by Portal
```php
// PortalSecurityService.php - Different security per portal type
class PortalSecurityService
{
    public function enforcePortalSecurity(string $portal, User $user): void
    {
        switch ($portal) {
            case 'producer':
                $this->enforceProducerSecurity($user);
                break;
            case 'policy':
            case 'claims':
            case 'insured':
                $this->enforceStrictSecurity($user);
                break;
        }
    }
    
    private function enforceProducerSecurity(User $user): void
    {
        // Producer portal specific
        if ($user->account_type === 'shared') {
            SharedAccountMonitor::trackActivity($user);
        }
        
        // IP-based security mandatory
        if (!$this->validateIPAccess($user)) {
            throw new IPSecurityException('IP not authorized');
        }
        
        // No MFA required for producer portal
        // Enhanced activity logging instead
        ActivityLogger::logProducerActivity($user);
    }
    
    private function enforceStrictSecurity(User $user): void
    {
        // Other portals require MFA
        if (!$user->mfa_verified) {
            throw new MFARequiredException();
        }
        
        // No shared accounts allowed
        if ($user->account_type === 'shared') {
            throw new SharedAccountException('Individual accounts only');
        }
        
        // Single session enforcement
        if ($this->hasOtherActiveSessions($user)) {
            throw new ConcurrentSessionException();
        }
    }
}
```

## Security Testing Standards (V4 Update)

### Automated Security Testing in CI/CD
```yaml
# security-pipeline.yml - Security tests in every build
name: Security Pipeline
on: [push, pull_request]

jobs:
  static-analysis:
    runs-on: ubuntu-latest
    steps:
      - name: Static Security Analysis
        run: |
          # PHP security analysis
          vendor/bin/psalm --taint-analysis
          vendor/bin/phpstan analyse --level=max
          
          # JavaScript security analysis
          npm audit
          npm run eslint:security
          
      - name: Dependency Scanning
        run: |
          # Check for known vulnerabilities
          composer audit
          npm audit --production
          
      - name: Secret Scanning
        uses: trufflesecurity/trufflehog@v3
        with:
          path: ./
          base: main
          
  dynamic-analysis:
    runs-on: ubuntu-latest
    steps:
      - name: OWASP ZAP Scan
        uses: zaproxy/action-baseline@v0.7.0
        with:
          target: ${{ env.TEST_URL }}
          
      - name: PCI Compliance Check
        run: |
          # Run automated PCI compliance validation
          ./scripts/pci-compliance-check.sh
```

### Manual Security Testing Requirements
```php
class SecurityTestingSchedule
{
    const TESTING_SCHEDULE = [
        'penetration_testing' => 'quarterly',
        'code_security_review' => 'with_each_feature',
        'architecture_review' => 'new_components',
        'incident_response_drill' => 'quarterly',
        'pci_dss_assessment' => 'annually',
        'vulnerability_assessment' => 'monthly',
    ];
}
```

## Compliance & Regulatory Security

### Data Retention & Privacy
```php
// GDPR/CCPA compliance implementation
class DataRetentionService
{
    public function processDataSubjectRequest(DataSubjectRequest $request): void
    {
        match ($request->type) {
            'access' => $this->exportPersonalData($request->user),
            'deletion' => $this->deletePersonalData($request->user),
            'portability' => $this->portPersonalData($request->user),
            'rectification' => $this->updatePersonalData($request->user, $request->data)
        };
        
        // Audit compliance actions
        ComplianceAuditLog::create([
            'request_type' => $request->type,
            'user_id' => $request->user->id,
            'processed_by' => auth()->id(),
            'processed_at' => now(),
            'metadata' => $request->metadata
        ]);
    }
    
    private function deletePersonalData(User $user): void
    {
        DB::transaction(function () use ($user) {
            // Anonymize rather than delete for audit trail
            $user->update([
                'first_name' => 'REDACTED',
                'last_name' => 'REDACTED',
                'email' => "deleted-{$user->id}@privacy.local",
                'ssn' => null,
                'phone' => null,
                'deleted_at' => now()
            ]);
            
            // Remove from search indexes
            $user->searchable();
            
            SecurityLogger::logSecurityEvent('personal_data_deleted', [
                'user_id' => $user->id,
                'reason' => 'data_subject_request'
            ], 'info');
        });
    }
}
```

### Audit Trail Requirements
```php
// Immutable audit logging
class AuditTrail extends Model
{
    protected $fillable = [
        'table_name',
        'record_id',
        'action',
        'old_values',
        'new_values',
        'user_id',
        'tenant_id',
        'ip_address',
        'user_agent',
        'created_at'
    ];
    
    protected $casts = [
        'old_values' => 'encrypted:json',
        'new_values' => 'encrypted:json',
        'created_at' => 'immutable_datetime'
    ];
    
    // Prevent updates and deletes
    public function update(array $attributes = [], array $options = [])
    {
        throw new Exception('Audit records cannot be modified');
    }
    
    public function delete()
    {
        throw new Exception('Audit records cannot be deleted');
    }
}

// Automatic audit logging trait
trait Auditable
{
    protected static function bootAuditable(): void
    {
        static::created(function ($model) {
            AuditTrail::create([
                'table_name' => $model->getTable(),
                'record_id' => $model->getKey(),
                'action' => 'created',
                'new_values' => $model->getAttributes(),
                'user_id' => auth()->id(),
                'tenant_id' => auth()->user()?->tenant_id,
                'ip_address' => request()->ip(),
                'user_agent' => request()->userAgent()
            ]);
        });
        
        static::updated(function ($model) {
            AuditTrail::create([
                'table_name' => $model->getTable(),
                'record_id' => $model->getKey(),
                'action' => 'updated',
                'old_values' => $model->getOriginal(),
                'new_values' => $model->getAttributes(),
                'user_id' => auth()->id(),
                'tenant_id' => auth()->user()?->tenant_id,
                'ip_address' => request()->ip(),
                'user_agent' => request()->userAgent()
            ]);
        });
    }
}
```

## Security Incident Response (V4 Update)

### Payment Data Breach Response
```php
// PaymentBreachResponse.php - PCI-compliant incident response
class PaymentBreachResponse
{
    public function handlePaymentBreach(SecurityIncident $incident): void
    {
        // 1. Immediate containment (within 15 minutes)
        $this->disableAffectedServices($incident);
        $this->notifySecurityTeam($incident);
        
        // 2. Evidence preservation
        $this->preserveEvidence($incident);
        $this->startForensicCapture($incident);
        
        // 3. Notification (within 1 hour)
        $this->notifyPaymentProcessor($incident);
        $this->notifyManagement($incident);
        
        // 4. Investigation
        $this->beginInvestigation($incident);
        
        // 5. PCI DSS requirements
        $this->followPCIDSSProcedures($incident);
    }
}
```

### PII Exposure Response
```php
class PIIExposureResponse
{
    public function handlePIIExposure(array $affectedData): void
    {
        // 1. Identify scope
        $scope = $this->identifyExposureScope($affectedData);
        
        // 2. Re-encrypt affected data
        $this->reencryptData($scope);
        
        // 3. Audit access logs
        $accessLogs = $this->auditDataAccess($scope);
        
        // 4. Notify affected users per regulations
        $this->notifyAffectedUsers($scope, $accessLogs);
        
        // 5. Strengthen controls
        $this->reviewAndStrengthenControls($scope);
    }
}
```

## Security Testing & Validation

### Automated Security Testing
```php
// PHPUnit security tests
class SecurityTest extends TestCase
{
    public function test_prevents_sql_injection()
    {
        $user = User::factory()->create();
        $this->actingAs($user);
        
        // Attempt SQL injection
        $response = $this->postJson('/api/policies/search', [
            'query' => "'; DROP TABLE policies; --"
        ]);
        
        $response->assertStatus(422);
        $this->assertDatabaseHas('policies', []); // Table still exists
    }
    
    public function test_enforces_tenant_isolation()
    {
        $tenantA = Tenant::factory()->create();
        $tenantB = Tenant::factory()->create();
        
        $userA = User::factory()->for($tenantA)->create();
        $policyB = Policy::factory()->for($tenantB)->create();
        
        $this->actingAs($userA);
        
        $response = $this->getJson("/api/policies/{$policyB->id}");
        $response->assertForbidden();
    }
    
    public function test_requires_mfa_for_admin_actions()
    {
        $admin = User::factory()->admin()->create();
        $this->actingAs($admin);
        
        // Admin action without MFA should fail
        $response = $this->postJson('/api/admin/users', [
            'email' => 'test@example.com'
        ]);
        
        $response->assertStatus(428); // Precondition Required (MFA)
    }
}
```

### Penetration Testing Integration
```yaml
# OWASP ZAP automated security scanning
name: Security Scan
on:
  push:
    branches: [main, develop]
  schedule:
    - cron: '0 2 * * 1' # Weekly scan

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Start application
        run: |
          docker-compose up -d
          sleep 30
          
      - name: OWASP ZAP Full Scan
        uses: zaproxy/action-full-scan@v0.4.0
        with:
          target: 'http://localhost:8000'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a -d -T 60'
          
      - name: Upload ZAP results
        uses: actions/upload-artifact@v3
        with:
          name: zap-report
          path: report_html.html
```

## Business Continuity & Disaster Recovery

### Backup Security
```php
// Encrypted backup implementation
class SecureBackupService
{
    public function createSecureBackup(): void
    {
        $backupFile = "backup-" . now()->format('Y-m-d-H-i-s') . ".sql.gpg";
        
        // Create encrypted database dump
        Process::run([
            'mysqldump',
            '--single-transaction',
            '--routines',
            '--triggers',
            config('database.connections.mysql.database')
        ])->pipe([
            'gpg',
            '--trust-model', 'always',
            '--encrypt',
            '--recipient', config('backup.gpg_recipient'),
            '--output', storage_path("backups/{$backupFile}")
        ]);
        
        // Upload to secure S3 bucket
        Storage::disk('s3-backup')->put(
            "database/{$backupFile}",
            file_get_contents(storage_path("backups/{$backupFile}"))
        );
        
        // Log backup creation
        SecurityLogger::logSecurityEvent('secure_backup_created', [
            'backup_file' => $backupFile,
            'size' => filesize(storage_path("backups/{$backupFile}"))
        ]);
        
        // Clean up local file
        unlink(storage_path("backups/{$backupFile}"));
    }
}
```

## Security Metrics & KPIs

### Security Dashboard
```php
// Security metrics collection
class SecurityMetrics
{
    public function getSecurityDashboard(): array
    {
        return [
            'authentication' => [
                'successful_logins' => $this->getLoginMetrics('success'),
                'failed_logins' => $this->getLoginMetrics('failed'),
                'mfa_adoption_rate' => $this->getMfaAdoptionRate(),
                'password_policy_compliance' => $this->getPasswordCompliance()
            ],
            'vulnerabilities' => [
                'open_vulnerabilities' => SecurityVulnerability::open()->count(),
                'critical_vulnerabilities' => SecurityVulnerability::critical()->count(),
                'time_to_remediation' => $this->getRemediationTime(),
                'vulnerability_trends' => $this->getVulnerabilityTrends()
            ],
            'incidents' => [
                'security_incidents' => SecurityIncident::thisMonth()->count(),
                'incident_response_time' => $this->getIncidentResponseTime(),
                'false_positive_rate' => $this->getFalsePositiveRate()
            ],
            'compliance' => [
                'audit_coverage' => $this->getAuditCoverage(),
                'data_retention_compliance' => $this->getRetentionCompliance(),
                'access_review_status' => $this->getAccessReviewStatus()
            ]
        ];
    }
}
```