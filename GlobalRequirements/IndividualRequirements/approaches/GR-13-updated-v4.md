# GR-13: Error Handling & Logging - Updated V4

## Table of Contents
1. [Overview](#overview)
2. [V8 Configuration Integration](#v8-configuration-integration)
3. [Comprehensive Logging Strategy](#comprehensive-logging-strategy)
4. [Error Handling Architecture](#error-handling-architecture)
5. [Circuit Breaker Implementation](#circuit-breaker-implementation)
6. [Database Schema Design](#database-schema-design)
7. [Map Table Relationships](#map-table-relationships)
8. [Monitoring & Alerting](#monitoring--alerting)
9. [Performance Optimization](#performance-optimization)
10. [Security Considerations](#security-considerations)
11. [Implementation Guidelines](#implementation-guidelines)

## 1. Overview

### Purpose
This document defines the comprehensive error handling and logging framework that provides structured monitoring, alerting, and debugging capabilities across the entire insurance system.

**V4 Updates**: This version incorporates V8 architectural decisions including configuration pattern usage for alerts and circuit breakers, proper entity/communication integration, and comprehensive map table rationale for all logging relationships.

### Scope
The error handling and logging system manages:
- **Structured Logging**: JSON-formatted logs with consistent schema
- **Multi-Level Logging**: Debug, info, warning, error, critical levels
- **Centralized Collection**: Integration with modern observability stacks
- **Real-Time Monitoring**: Instant alerting for critical errors
- **Compliance Logging**: Audit trails for regulatory requirements
- **Circuit Breaker Integration**: Service reliability patterns
- **External Integration Errors**: API and webhook failure handling

### Key Benefits
- **Comprehensive Audit Trail**: Every error tracked with full context
- **V8 Configuration Integration**: Alerts and circuit breakers via configuration system
- **Real-Time Monitoring**: Instant notification of critical system errors
- **Map Table Optimization**: Superior reporting and BI tool compatibility
- **Compliance Ready**: Built-in retention policies and audit trails

### Global Requirements Compliance
- **GR-41**: Database design standards with proper normalization
- **GR-19**: Table relationships using map tables for complex associations
- **GR-52**: Universal Entity Management for external observability tools
- **GR-44**: Communication architecture for error notifications

## 2. V8 Configuration Integration

### 2.1 Alert Configuration via Configuration System

**V8 Change**: Alert configurations are managed through the universal configuration system instead of separate alert tables.

```sql
-- Configuration types for alerting
INSERT INTO configuration_type (code, name, data_type, category, is_encrypted, description, status_id, created_by) VALUES
('LOG_ALERT_THRESHOLD', 'Log Alert Threshold', 'integer', 'monitoring', FALSE, 'Number of log entries to trigger alert', 1, 1),
('LOG_ALERT_WINDOW', 'Log Alert Window', 'integer', 'monitoring', FALSE, 'Time window in minutes for alert threshold', 1, 1),
('LOG_ALERT_CHANNELS', 'Log Alert Channels', 'json', 'monitoring', FALSE, 'Notification channels for log alerts', 1, 1),
('LOG_ALERT_RECIPIENTS', 'Log Alert Recipients', 'json', 'monitoring', FALSE, 'Alert recipient list', 1, 1),
('LOG_RETENTION_DAYS', 'Log Retention Days', 'integer', 'monitoring', FALSE, 'Days to retain logs', 1, 1);
```

### 2.2 Circuit Breaker Configuration Integration

**V8 Change**: Circuit breaker settings for logging integrations use configuration system.

```sql
-- Logging-specific circuit breaker settings
INSERT INTO configuration_type (code, name, data_type, category, description, status_id, created_by) VALUES
('LOG_CB_FAILURE_THRESHOLD', 'Log Circuit Breaker Failure Threshold', 'integer', 'monitoring', 'Number of logging failures before opening circuit', 1, 1),
('LOG_CB_SUCCESS_THRESHOLD', 'Log Circuit Breaker Success Threshold', 'integer', 'monitoring', 'Number of successes to close circuit', 1, 1),
('LOG_CB_TIMEOUT', 'Log Circuit Breaker Timeout', 'integer', 'monitoring', 'Timeout in seconds before retry', 1, 1);
```

### 2.3 Entity/Logging Separation

**V8 Change**: Clean separation between entity management and logging tracking.

```sql
-- Entity for logging services (V8)
CREATE TABLE entity (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    entity_type_id BIGINT UNSIGNED NOT NULL,
    name_id BIGINT UNSIGNED NOT NULL,     -- V8: Reference to clean name service
    code VARCHAR(50) UNIQUE,
    metadata JSON,                        -- Service-specific metadata
    status_id BIGINT UNSIGNED NOT NULL,
    -- audit fields
);

-- Logging tracking (separate from entity)
CREATE TABLE log (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    log_type_id BIGINT UNSIGNED NOT NULL,
    level_id BIGINT UNSIGNED NOT NULL,
    
    -- Entity context (what generated the log)
    entity_type_id BIGINT UNSIGNED,
    entity_id BIGINT UNSIGNED,
    
    -- Log content
    message TEXT NOT NULL,
    context JSON,
    stack_trace TEXT,
    
    -- Request tracking
    request_id VARCHAR(36),
    correlation_id VARCHAR(36),
    
    -- User context
    user_id BIGINT UNSIGNED,
    session_id BIGINT UNSIGNED,
    ip_address VARCHAR(45),
    user_agent TEXT,
    
    -- Timing
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- audit fields
);
```

## 3. Comprehensive Logging Strategy

### 3.1 Structured Logging Requirements

**Multi-Level Logging Framework**:
- **Debug**: Development debugging information
- **Info**: General operational information
- **Warning**: Potential issues that don't break functionality
- **Error**: Errors that affect specific operations
- **Critical**: System-wide failures requiring immediate attention

### 3.2 Log Schema Standards

```json
{
  "timestamp": "2025-01-17T10:30:00Z",
  "level": "error",
  "message": "Policy binding failed for policy P-123456",
  "context": {
    "policy_id": 12345,
    "user_id": 67890,
    "session_id": "sess_abc123",
    "request_id": "req_xyz789",
    "correlation_id": "corr_456def",
    "service": "policy-service",
    "endpoint": "/api/policies/12345/bind",
    "method": "POST",
    "error_code": "BINDING_VALIDATION_FAILED",
    "error_details": {
      "validation_errors": [
        "Driver license expired",
        "Missing required coverage"
      ]
    }
  },
  "stack_trace": "Exception stack trace...",
  "metadata": {
    "environment": "production",
    "version": "1.2.3",
    "instance_id": "app-server-01"
  }
}
```

### 3.3 Observability Stack Integration

**Requirements for Log Collection**:
- **Structured Format**: Consistent JSON schema for all log entries
- **Metadata Enrichment**: Automatic context addition
- **Real-time Processing**: Stream processing for immediate alerting
- **Long-term Storage**: Compressed storage with retention policies
- **Compliance**: Audit trail preservation

## 4. Error Handling Architecture

### 4.1 Exception Categories

**Business Logic Exceptions**:
- Policy validation failures
- Underwriting rule violations
- Payment processing errors
- Coverage limit exceeded

**Integration Exceptions**:
- External API failures
- Database connection errors
- Message queue failures
- File system errors

**Security Exceptions**:
- Authentication failures
- Authorization violations
- Session expiration
- Invalid tokens

**Validation Exceptions**:
- Input validation errors
- Data format violations
- Required field missing
- Business rule violations

### 4.2 Error Response Standards

```json
{
  "error": {
    "code": "POLICY_VALIDATION_FAILED",
    "message": "Policy cannot be bound due to validation errors",
    "details": "Driver license has expired",
    "request_id": "req_xyz789",
    "timestamp": "2025-01-17T10:30:00Z",
    "validation_errors": {
      "driver_license": ["License expired on 2024-12-31"],
      "coverage": ["Minimum liability coverage required"]
    }
  }
}
```

### 4.3 Error Code Standards

**Format**: `DOMAIN_ERROR_TYPE`
- **POLICY_NOT_FOUND**: Policy does not exist
- **PAYMENT_INSUFFICIENT_FUNDS**: Payment declined
- **DRIVER_LICENSE_EXPIRED**: Driver license has expired
- **COVERAGE_LIMIT_EXCEEDED**: Coverage limit exceeded

## 5. Circuit Breaker Implementation

### 5.1 Circuit Breaker Requirements

**V8 Architecture**: Circuit breaker configuration stored in configuration system, runtime state in cache.

```sql
-- Circuit breaker configuration for logging services
INSERT INTO configuration_type (code, name, data_type, category, description, status_id, created_by) VALUES
('LOG_CB_FAILURE_THRESHOLD', 'Log Circuit Breaker Failure Threshold', 'integer', 'monitoring', 'Number of failures before opening circuit', 1, 1),
('LOG_CB_SUCCESS_THRESHOLD', 'Log Circuit Breaker Success Threshold', 'integer', 'monitoring', 'Number of successes to close circuit', 1, 1),
('LOG_CB_TIMEOUT_SECONDS', 'Log Circuit Breaker Timeout', 'integer', 'monitoring', 'Timeout in seconds before retry', 1, 1);

-- Apply to logging service entities
INSERT INTO map_entity_configuration (entity_id, configuration_type_id, configuration_id, environment, effective_date, status_id, created_by)
VALUES (
    (SELECT id FROM entity WHERE code = 'loki_logging'),
    (SELECT id FROM configuration_type WHERE code = 'LOG_CB_FAILURE_THRESHOLD'),
    (SELECT id FROM configuration WHERE value = '5'),
    'production',
    NOW(),
    1,
    1
);
```

### 5.2 Circuit Breaker States

**Closed**: Normal operation, requests pass through
**Open**: Service unavailable, requests fail immediately
**Half-Open**: Testing recovery with limited requests

### 5.3 Runtime State Management

```php
// Circuit breaker service with V8 configuration integration
class LoggingCircuitBreaker {
    private $cache;
    private $configService;
    
    public function canExecute(string $serviceName): bool {
        $state = $this->cache->get("circuit_breaker:{$serviceName}:state", 'closed');
        
        if ($state === 'open') {
            $openedAt = $this->cache->get("circuit_breaker:{$serviceName}:opened_at");
            $timeout = $this->configService->getEntityConfig($serviceName, 'LOG_CB_TIMEOUT_SECONDS');
            
            if (time() - $openedAt > $timeout) {
                $this->cache->set("circuit_breaker:{$serviceName}:state", 'half_open');
                return true;
            }
            return false;
        }
        
        return true;
    }
}
```

## 6. Database Schema Design

### 6.1 Level Table (Normalized)

```sql
CREATE TABLE level (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL,
    severity INT NOT NULL, -- 0=debug, 1=info, 2=warning, 3=error, 4=critical
    color VARCHAR(7), -- Hex color code for UI
    icon VARCHAR(50), -- Icon for UI display
    status_id BIGINT UNSIGNED NOT NULL,
    
    -- Audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by BIGINT UNSIGNED,
    
    -- Indexes
    INDEX idx_code (code),
    INDEX idx_severity (severity),
    INDEX idx_status (status_id),
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
);

-- Standard log levels
INSERT INTO level (code, name, severity, color, icon, status_id, created_by) VALUES
('debug', 'Debug', 0, '#9CA3AF', 'bug', 1, 1),
('info', 'Information', 1, '#3B82F6', 'info', 1, 1),
('warning', 'Warning', 2, '#F59E0B', 'warning', 1, 1),
('error', 'Error', 3, '#EF4444', 'error', 1, 1),
('critical', 'Critical', 4, '#DC2626', 'alert', 1, 1);
```

### 6.2 Log Type Table

```sql
CREATE TABLE log_type (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL, -- 'application', 'security', 'performance', 'integration'
    
    -- Retention settings
    retention_days INT DEFAULT 90,
    archive_after_days INT DEFAULT 30,
    
    -- Alert settings
    alert_threshold INT DEFAULT 10,
    alert_window_minutes INT DEFAULT 5,
    
    -- Status
    status_id BIGINT UNSIGNED NOT NULL,
    
    -- Audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by BIGINT UNSIGNED,
    
    -- Indexes
    INDEX idx_code (code),
    INDEX idx_category (category),
    INDEX idx_status (status_id),
    
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
);

-- Standard log types
INSERT INTO log_type (code, name, description, category, status_id, created_by) VALUES
('application_error', 'Application Error', 'General application errors', 'application', 1, 1),
('authentication_failure', 'Authentication Failure', 'Failed login attempts', 'security', 1, 1),
('api_request', 'API Request', 'External API requests', 'integration', 1, 1),
('database_query', 'Database Query', 'Database query performance', 'performance', 1, 1),
('policy_binding', 'Policy Binding', 'Policy binding operations', 'application', 1, 1),
('payment_processing', 'Payment Processing', 'Payment processing events', 'application', 1, 1),
('health_check', 'Health Check', 'System health checks', 'monitoring', 1, 1);
```

### 6.3 Enhanced Log Table

```sql
CREATE TABLE log (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    log_type_id BIGINT UNSIGNED NOT NULL,
    level_id BIGINT UNSIGNED NOT NULL,
    
    -- Entity context (what generated the log)
    entity_type_id BIGINT UNSIGNED,
    entity_id BIGINT UNSIGNED,
    
    -- Log content
    message TEXT NOT NULL,
    context JSON,
    stack_trace TEXT,
    
    -- Request tracking
    request_id VARCHAR(36),
    correlation_id VARCHAR(36),
    
    -- User context
    user_id BIGINT UNSIGNED,
    session_id BIGINT UNSIGNED,
    ip_address VARCHAR(45),
    user_agent TEXT,
    
    -- Performance metrics
    duration_ms INT UNSIGNED,
    memory_usage_mb DECIMAL(10,2),
    
    -- Timing
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by BIGINT UNSIGNED NOT NULL,
    
    -- Indexes
    INDEX idx_log_type (log_type_id),
    INDEX idx_level (level_id),
    INDEX idx_level_time (level_id, logged_at),
    INDEX idx_entity (entity_type_id, entity_id),
    INDEX idx_request (request_id),
    INDEX idx_correlation (correlation_id),
    INDEX idx_user (user_id),
    INDEX idx_session (session_id),
    INDEX idx_logged_at (logged_at),
    
    -- Performance optimization indexes
    INDEX idx_error_logs (level_id, logged_at) WHERE level_id >= 3,
    INDEX idx_user_errors (user_id, level_id, logged_at),
    INDEX idx_entity_errors (entity_type_id, entity_id, level_id, logged_at),
    
    -- Foreign keys
    FOREIGN KEY (log_type_id) REFERENCES log_type(id),
    FOREIGN KEY (level_id) REFERENCES level(id),
    FOREIGN KEY (entity_type_id) REFERENCES entity_type(id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (session_id) REFERENCES session(id),
    FOREIGN KEY (created_by) REFERENCES user(id)
);
```

## 7. Map Table Relationships

### 7.1 Why Map Tables for Logging Relationships

**Business Need**: Logging systems have complex many-to-many relationships that require tracking over time.

#### Decision Matrix for Logging Relationships

| Relationship Type | Map Table | Direct FK | Rationale |
|-------------------|-----------|-----------|-----------|
| Log ↔ Communications | ✓ | ✗ | Logs can trigger multiple communications |
| Log ↔ Configurations | ✓ | ✗ | Logs can be related to multiple configurations |
| Log ↔ Entities | ✗ | ✓ | Each log entry relates to one entity context |
| Entity ↔ Log Configurations | ✓ | ✗ | Entities have multiple logging configurations |

### 7.2 Map Table Implementations

#### map_log_communication

```sql
CREATE TABLE map_log_communication (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    log_id BIGINT UNSIGNED NOT NULL,
    communication_id BIGINT UNSIGNED NOT NULL,
    
    -- Communication context
    communication_type VARCHAR(50) NOT NULL, -- 'alert', 'notification', 'escalation'
    trigger_reason VARCHAR(100),
    is_automatic BOOLEAN DEFAULT TRUE,
    
    -- Delivery tracking
    sent_at TIMESTAMP NULL,
    delivered_at TIMESTAMP NULL,
    acknowledged_at TIMESTAMP NULL,
    
    -- Status
    status_id BIGINT UNSIGNED NOT NULL,
    
    -- Audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by BIGINT UNSIGNED,
    
    -- Constraints
    UNIQUE KEY uk_log_communication (log_id, communication_id),
    INDEX idx_log (log_id),
    INDEX idx_communication (communication_id),
    INDEX idx_type (communication_type),
    INDEX idx_sent (sent_at),
    INDEX idx_delivered (delivered_at),
    INDEX idx_status (status_id),
    
    FOREIGN KEY (log_id) REFERENCES log(id),
    FOREIGN KEY (communication_id) REFERENCES communication(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
);
```

#### map_entity_log_configuration

```sql
CREATE TABLE map_entity_log_configuration (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    entity_id BIGINT UNSIGNED NOT NULL,
    log_type_id BIGINT UNSIGNED NOT NULL,
    configuration_type_id BIGINT UNSIGNED NOT NULL,
    configuration_id BIGINT UNSIGNED NOT NULL,
    
    -- Configuration context
    environment VARCHAR(20) DEFAULT 'production',
    log_level_minimum INT DEFAULT 1, -- Minimum level to log
    is_enabled BOOLEAN DEFAULT TRUE,
    
    -- Retention settings
    retention_days INT,
    archive_after_days INT,
    
    -- Alert settings
    alert_threshold INT,
    alert_window_minutes INT,
    
    -- Effective period
    effective_date TIMESTAMP NOT NULL,
    expiration_date TIMESTAMP,
    status_id BIGINT UNSIGNED NOT NULL,
    
    -- Audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by BIGINT UNSIGNED NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by BIGINT UNSIGNED,
    
    -- Constraints
    UNIQUE KEY uk_entity_log_config (entity_id, log_type_id, configuration_type_id, environment, effective_date),
    INDEX idx_entity (entity_id),
    INDEX idx_log_type (log_type_id),
    INDEX idx_config_type (configuration_type_id),
    INDEX idx_config (configuration_id),
    INDEX idx_environment (environment),
    INDEX idx_effective (effective_date, expiration_date),
    INDEX idx_status (status_id),
    
    FOREIGN KEY (entity_id) REFERENCES entity(id),
    FOREIGN KEY (log_type_id) REFERENCES log_type(id),
    FOREIGN KEY (configuration_type_id) REFERENCES configuration_type(id),
    FOREIGN KEY (configuration_id) REFERENCES configuration(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    FOREIGN KEY (updated_by) REFERENCES user(id)
);
```

### 7.3 Map Table Benefits for Logging

#### Reporting Excellence

```sql
-- Comprehensive logging analysis
SELECT 
    l.message,
    lt.name as log_type,
    lv.name as level,
    COUNT(DISTINCT mlc.communication_id) as alerts_sent,
    COUNT(DISTINCT melc.configuration_id) as configurations_applied,
    AVG(l.duration_ms) as avg_duration_ms
FROM log l
JOIN log_type lt ON l.log_type_id = lt.id
JOIN level lv ON l.level_id = lv.id
LEFT JOIN map_log_communication mlc ON l.id = mlc.log_id
LEFT JOIN map_entity_log_configuration melc ON l.entity_id = melc.entity_id AND l.log_type_id = melc.log_type_id
WHERE l.logged_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
GROUP BY l.id, l.message, lt.name, lv.name
ORDER BY avg_duration_ms DESC;
```

#### BI Tool Integration

- **Grafana**: Direct visualization of log metrics and alert patterns
- **Tableau**: Native join support for log analysis dashboards
- **Custom Reports**: Standard SQL without complex polymorphic logic

## 8. Monitoring & Alerting

### 8.1 Real-Time Monitoring Requirements

**Error Rate Monitoring**:
- Track errors per minute/hour by service
- Alert on threshold breaches
- Identify error patterns and trends

**Performance Monitoring**:
- Response time tracking
- Resource utilization monitoring
- Database query performance analysis

**Business Process Monitoring**:
- Quote conversion failures
- Payment processing errors
- Policy binding failures

### 8.2 Alert Configuration (V8)

```sql
-- Alert configuration using V8 configuration system
INSERT INTO configuration_type (code, name, data_type, category, description, status_id, created_by) VALUES
('ERROR_ALERT_CONFIG', 'Error Alert Configuration', 'json', 'monitoring', 'Configuration for error alerting', 1, 1);

-- Example alert configuration
INSERT INTO configuration (configuration_type_id, value, environment, effective_date, status_id, created_by) VALUES
((SELECT id FROM configuration_type WHERE code = 'ERROR_ALERT_CONFIG'),
 JSON_OBJECT(
     'name', 'Critical Error Alert',
     'description', 'Alert on critical system errors',
     'criteria', JSON_OBJECT(
         'level_ids', JSON_ARRAY(4, 5),
         'log_type_codes', JSON_ARRAY('application_error', 'security_error'),
         'threshold_count', 1,
         'threshold_window_minutes', 5
     ),
     'actions', JSON_OBJECT(
         'notification_channels', JSON_ARRAY('email', 'sms', 'slack'),
         'recipient_list', JSON_ARRAY('admin@company.com', 'oncall@company.com'),
         'escalation_minutes', 15
     )
 ),
 'production',
 NOW(),
 1,
 1);
```

### 8.3 Alert Priority Levels

- **P1 (Critical)**: System down, data loss risk
- **P2 (High)**: Major feature unavailable
- **P3 (Medium)**: Performance degradation
- **P4 (Low)**: Minor issues, cosmetic errors

## 9. Performance Optimization

### 9.1 Query Optimization

```sql
-- Efficient error log lookup
SELECT l.*, lt.name as log_type_name, lv.name as level_name
FROM log l
JOIN log_type lt ON l.log_type_id = lt.id
JOIN level lv ON l.level_id = lv.id
WHERE l.level_id >= 3 -- errors and critical
  AND l.logged_at >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
  AND l.entity_type_id = ?
ORDER BY l.logged_at DESC
LIMIT 100;

-- Optimized alert query
SELECT l.id, l.message, l.logged_at, COUNT(*) as occurrence_count
FROM log l
WHERE l.level_id = 4 -- critical
  AND l.logged_at >= DATE_SUB(NOW(), INTERVAL 5 MINUTE)
  AND l.log_type_id IN (1, 2, 3)
GROUP BY l.message
HAVING COUNT(*) >= 1
ORDER BY occurrence_count DESC;
```

### 9.2 Index Strategy

```sql
-- Performance indexes for logging
CREATE INDEX idx_log_error_recent ON log(level_id, logged_at) WHERE level_id >= 3;
CREATE INDEX idx_log_user_session ON log(user_id, session_id, logged_at);
CREATE INDEX idx_log_entity_type ON log(entity_type_id, entity_id, logged_at);
CREATE INDEX idx_log_request_correlation ON log(request_id, correlation_id);

-- Covering indexes for common queries
CREATE INDEX idx_log_summary ON log(log_type_id, level_id, logged_at) 
INCLUDE (message, duration_ms, user_id);
```

### 9.3 Storage Optimization

```sql
-- Appropriate data types for logging
BIGINT UNSIGNED     -- For log IDs and foreign keys
INT UNSIGNED        -- For duration and counts
VARCHAR(36)         -- For UUIDs (request_id, correlation_id)
TEXT                -- For message and stack trace
JSON                -- For context data
TIMESTAMP           -- For precise datetime tracking
DECIMAL(10,2)       -- For memory usage
```

## 10. Security Considerations

### 10.1 Sensitive Data Handling

**PII Masking**: Automatic masking of sensitive data in logs
**Encryption**: Encrypt logs containing sensitive information
**Access Control**: Role-based access to log data
**Audit Trail**: Track all log access and queries

### 10.2 Security Event Logging

```sql
-- Security-specific log types
INSERT INTO log_type (code, name, description, category, retention_days, status_id, created_by) VALUES
('authentication_attempt', 'Authentication Attempt', 'User authentication attempts', 'security', 365, 1, 1),
('authorization_failure', 'Authorization Failure', 'Access denied events', 'security', 365, 1, 1),
('session_management', 'Session Management', 'Session creation/destruction', 'security', 180, 1, 1),
('password_change', 'Password Change', 'Password change events', 'security', 730, 1, 1),
('administrative_action', 'Administrative Action', 'Admin user actions', 'security', 2555, 1, 1); -- 7 years
```

### 10.3 Compliance Requirements

**Log Retention Policies**:
- **Error Logs**: 90 days online, 7 years archived
- **Security Logs**: 1 year online, 10 years archived
- **Audit Logs**: 7 years online
- **Performance Logs**: 30 days online

## 11. Implementation Guidelines

### 11.1 Development Standards

```php
// Structured logging example
class LoggingService {
    private $logger;
    
    public function logError(string $message, array $context = [], ?Throwable $exception = null): void {
        $logData = [
            'message' => $message,
            'context' => $context,
            'request_id' => $this->getRequestId(),
            'correlation_id' => $this->getCorrelationId(),
            'user_id' => $this->getCurrentUserId(),
            'session_id' => $this->getSessionId(),
            'stack_trace' => $exception ? $exception->getTraceAsString() : null,
            'timestamp' => now()->toISOString(),
        ];
        
        $this->logger->error($message, $logData);
    }
}
```

### 11.2 Integration Patterns

```php
// Circuit breaker integration with logging
class IntegrationService {
    private $circuitBreaker;
    private $logger;
    
    public function callExternalApi(string $endpoint, array $data): mixed {
        if (!$this->circuitBreaker->canExecute('external_api')) {
            $this->logger->warning('Circuit breaker open for external API', [
                'endpoint' => $endpoint,
                'circuit_state' => 'open'
            ]);
            throw new ServiceUnavailableException('External API circuit breaker is open');
        }
        
        try {
            $response = $this->makeApiCall($endpoint, $data);
            $this->circuitBreaker->recordSuccess('external_api');
            return $response;
        } catch (Exception $e) {
            $this->circuitBreaker->recordFailure('external_api');
            $this->logger->error('External API call failed', [
                'endpoint' => $endpoint,
                'error' => $e->getMessage(),
                'circuit_state' => $this->circuitBreaker->getState('external_api')
            ]);
            throw $e;
        }
    }
}
```

### 11.3 Operational Procedures

**Daily Operations**:
- Review critical errors from previous 24 hours
- Analyze alert patterns and false positives
- Monitor circuit breaker states
- Check log retention compliance

**Weekly Operations**:
- Trend analysis of error patterns
- Performance metric review
- Alert threshold optimization
- Circuit breaker configuration tuning

### 11.4 Database Normalization Benefits

**V4 Implementation Features**:
- Log levels in separate normalized table with foreign key reference
- Entity type references use proper foreign keys instead of VARCHAR
- Alert configurations use standard configuration system
- All status tracking uses foreign keys to status table
- Map tables for complex logging relationships

**Performance Impact**:
- Efficient queries using proper indexes
- Reduced storage through normalization
- Faster aggregation queries
- Better constraint enforcement

---

**Document Version**: V4.0
**Effective Date**: 2025-01-17
**Next Review**: 2025-07-17
**Global Requirements Compliance**: GR-13, GR-19, GR-41, GR-44, GR-52