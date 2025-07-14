#!/usr/bin/env python3
"""
Infrastructure Alignment Validator
Complete Requirements Generation System - Multi-Agent Architecture

Validates requirements against existing infrastructure codebase patterns,
ensuring new requirements align with established architecture and implementations.

Created: 2025-01-07
Version: 1.0.0
GR Compliance: GR-38, GR-41, GR-00, GR-28
"""

import json
import yaml
import logging
import asyncio
import os
import subprocess
from typing import Dict, List, Optional, Tuple, Any, Set
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
import re

# Configuration and Data Classes
@dataclass
class InfrastructurePattern:
    """Represents an infrastructure pattern found in the codebase."""
    pattern_type: str
    pattern_name: str
    file_path: str
    line_number: int
    pattern_content: str
    confidence: float
    usage_frequency: int

@dataclass
class AlignmentCheck:
    """Represents an alignment check result."""
    check_type: str
    check_name: str
    alignment_status: str  # aligned, misaligned, unknown
    existing_patterns: List[InfrastructurePattern]
    recommendations: List[str]
    confidence_score: float
    severity: str  # critical, major, minor, info

@dataclass
class InfrastructureValidationResult:
    """Result of infrastructure alignment validation."""
    requirement_id: str
    repository_path: str
    repository_branch: str
    alignment_checks: List[AlignmentCheck]
    overall_alignment_score: float
    validation_status: str  # aligned, needs_updates, misaligned
    critical_misalignments: List[Dict]
    recommendations: List[str]
    processing_time: float
    validation_metadata: Dict

class AlignmentStatus(Enum):
    """Alignment status levels."""
    ALIGNED = "aligned"
    NEEDS_UPDATES = "needs_updates"
    MISALIGNED = "misaligned"
    UNKNOWN = "unknown"
    ERROR = "error"

class PatternType(Enum):
    """Types of infrastructure patterns."""
    DATABASE_SCHEMA = "database_schema"
    API_ENDPOINT = "api_endpoint"
    SERVICE_CLASS = "service_class"
    MODEL_CLASS = "model_class"
    CONTROLLER_CLASS = "controller_class"
    MIGRATION = "migration"
    CONFIG_PATTERN = "config_pattern"
    VALIDATION_RULE = "validation_rule"

class InfrastructureValidator:
    """
    Validator for ensuring requirements align with existing infrastructure.
    Analyzes the blitzy-requirements repository for patterns and conventions.
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the Infrastructure Validator."""
        self.config_path = config_path or "/app/workspace/requirements/shared-infrastructure/agent-configurations/universal-validator.yaml"
        self.config = self._load_configuration()
        self.logger = self._setup_logging()
        
        # Infrastructure repository configuration
        self.repository_path = "/app/workspace/blitzy-requirements"
        self.target_branch = "staging"
        
        # Pattern analysis
        self.discovered_patterns = {}
        self.infrastructure_index = {}
        self.validation_cache = {}
        
        # Analysis engines
        self.pattern_analyzers = {}
        
        # Initialize validator
        self._initialize_validator()
    
    def _load_configuration(self) -> Dict:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Return default configuration."""
        return {
            "infrastructure_validation": {
                "alignment_threshold": 0.80,
                "critical_pattern_threshold": 0.95,
                "repository_analysis_enabled": True
            },
            "performance": {
                "cache_enabled": True,
                "cache_ttl_hours": 24,
                "max_cache_size": 100
            }
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the validator."""
        logger = logging.getLogger("InfrastructureValidator")
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def _initialize_validator(self):
        """Initialize all validator components."""
        self.logger.info("Initializing Infrastructure Validator...")
        
        try:
            # Initialize pattern analyzers
            self._initialize_pattern_analyzers()
            
            # Check repository access
            self._check_repository_access()
            
            # Analyze infrastructure patterns
            self._analyze_infrastructure_patterns()
            
            self.logger.info("Infrastructure Validator initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize validator: {e}")
            # Don't raise - validator can work in limited mode
    
    def _initialize_pattern_analyzers(self):
        """Initialize pattern analyzers for different infrastructure components."""
        self.pattern_analyzers = {
            PatternType.DATABASE_SCHEMA: self._analyze_database_patterns,
            PatternType.API_ENDPOINT: self._analyze_api_patterns,
            PatternType.SERVICE_CLASS: self._analyze_service_patterns,
            PatternType.MODEL_CLASS: self._analyze_model_patterns,
            PatternType.CONTROLLER_CLASS: self._analyze_controller_patterns,
            PatternType.MIGRATION: self._analyze_migration_patterns,
            PatternType.CONFIG_PATTERN: self._analyze_config_patterns,
            PatternType.VALIDATION_RULE: self._analyze_validation_patterns
        }
        
        self.logger.info(f"Initialized {len(self.pattern_analyzers)} pattern analyzers")
    
    def _check_repository_access(self):
        """Check if the infrastructure repository is accessible."""
        if not Path(self.repository_path).exists():
            self.logger.warning(f"Infrastructure repository not found at {self.repository_path}")
            return False
        
        try:
            # Check git repository
            result = subprocess.run(
                ["git", "status"],
                cwd=self.repository_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                self.logger.warning("Infrastructure repository is not a valid git repository")
                return False
            
            # Switch to target branch
            subprocess.run(
                ["git", "checkout", self.target_branch],
                cwd=self.repository_path,
                capture_output=True,
                timeout=10
            )
            
            # Pull latest changes
            subprocess.run(
                ["git", "pull", "origin", self.target_branch],
                cwd=self.repository_path,
                capture_output=True,
                timeout=30
            )
            
            self.logger.info(f"Infrastructure repository ready at {self.repository_path} on {self.target_branch}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error accessing infrastructure repository: {e}")
            return False
    
    def _analyze_infrastructure_patterns(self):
        """Analyze existing infrastructure patterns."""
        if not Path(self.repository_path).exists():
            self.logger.warning("Skipping infrastructure pattern analysis - repository not available")
            self.discovered_patterns = self._create_default_patterns()
            return
        
        self.logger.info("Analyzing infrastructure patterns...")
        
        for pattern_type, analyzer in self.pattern_analyzers.items():
            try:
                patterns = analyzer()
                self.discovered_patterns[pattern_type] = patterns
                self.logger.info(f"Found {len(patterns)} {pattern_type.value} patterns")
            except Exception as e:
                self.logger.error(f"Error analyzing {pattern_type.value} patterns: {e}")
                self.discovered_patterns[pattern_type] = []
        
        # Build infrastructure index
        self._build_infrastructure_index()
    
    def _create_default_patterns(self) -> Dict:
        """Create default patterns when repository is not available."""
        return {
            PatternType.DATABASE_SCHEMA: self._create_default_database_patterns(),
            PatternType.API_ENDPOINT: self._create_default_api_patterns(),
            PatternType.SERVICE_CLASS: self._create_default_service_patterns(),
            PatternType.MODEL_CLASS: self._create_default_model_patterns(),
            PatternType.CONTROLLER_CLASS: self._create_default_controller_patterns(),
            PatternType.MIGRATION: [],
            PatternType.CONFIG_PATTERN: [],
            PatternType.VALIDATION_RULE: []
        }
    
    def _create_default_database_patterns(self) -> List[InfrastructurePattern]:
        """Create default database patterns."""
        return [
            InfrastructurePattern(
                pattern_type="database_schema",
                pattern_name="audit_fields",
                file_path="database/migrations/create_base_tables.php",
                line_number=1,
                pattern_content="created_at, updated_at, created_by, updated_by",
                confidence=0.9,
                usage_frequency=50
            ),
            InfrastructurePattern(
                pattern_type="database_schema",
                pattern_name="snake_case_naming",
                file_path="database/migrations",
                line_number=1,
                pattern_content="table names use snake_case convention",
                confidence=0.95,
                usage_frequency=100
            )
        ]
    
    def _create_default_api_patterns(self) -> List[InfrastructurePattern]:
        """Create default API patterns."""
        return [
            InfrastructurePattern(
                pattern_type="api_endpoint",
                pattern_name="restful_endpoints",
                file_path="routes/api.php",
                line_number=1,
                pattern_content="RESTful API endpoint patterns",
                confidence=0.9,
                usage_frequency=30
            )
        ]
    
    def _create_default_service_patterns(self) -> List[InfrastructurePattern]:
        """Create default service patterns."""
        return [
            InfrastructurePattern(
                pattern_type="service_class",
                pattern_name="service_layer",
                file_path="app/Services",
                line_number=1,
                pattern_content="Service layer pattern implementation",
                confidence=0.85,
                usage_frequency=20
            )
        ]
    
    def _create_default_model_patterns(self) -> List[InfrastructurePattern]:
        """Create default model patterns."""
        return [
            InfrastructurePattern(
                pattern_type="model_class",
                pattern_name="eloquent_models",
                file_path="app/Models",
                line_number=1,
                pattern_content="Laravel Eloquent model patterns",
                confidence=0.9,
                usage_frequency=40
            )
        ]
    
    def _create_default_controller_patterns(self) -> List[InfrastructurePattern]:
        """Create default controller patterns."""
        return [
            InfrastructurePattern(
                pattern_type="controller_class",
                pattern_name="api_controllers",
                file_path="app/Http/Controllers",
                line_number=1,
                pattern_content="API controller patterns",
                confidence=0.85,
                usage_frequency=25
            )
        ]
    
    def _analyze_database_patterns(self) -> List[InfrastructurePattern]:
        """Analyze database schema patterns from migrations."""
        patterns = []
        migrations_path = Path(self.repository_path) / "src" / "backend" / "database" / "migrations"
        
        if not migrations_path.exists():
            return patterns
        
        migration_files = list(migrations_path.glob("*.php"))
        
        for migration_file in migration_files:
            try:
                with open(migration_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Look for common database patterns
                patterns.extend(self._extract_database_patterns(content, str(migration_file)))
                
            except Exception as e:
                self.logger.error(f"Error analyzing migration {migration_file}: {e}")
        
        return patterns
    
    def _extract_database_patterns(self, content: str, file_path: str) -> List[InfrastructurePattern]:
        """Extract database patterns from migration content."""
        patterns = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Check for audit fields
            if 'timestamps()' in line or ('created_at' in line_lower and 'updated_at' in line_lower):
                patterns.append(InfrastructurePattern(
                    pattern_type="database_schema",
                    pattern_name="audit_fields",
                    file_path=file_path,
                    line_number=i + 1,
                    pattern_content=line.strip(),
                    confidence=0.9,
                    usage_frequency=1
                ))
            
            # Check for table naming
            table_match = re.search(r'create\s*\(\s*[\'"]([^\'\"]+)[\'"]', line_lower)
            if table_match:
                table_name = table_match.group(1)
                if '_' in table_name and table_name.islower():
                    patterns.append(InfrastructurePattern(
                        pattern_type="database_schema",
                        pattern_name="snake_case_table_naming",
                        file_path=file_path,
                        line_number=i + 1,
                        pattern_content=f"Table: {table_name}",
                        confidence=0.95,
                        usage_frequency=1
                    ))
            
            # Check for foreign keys
            if 'foreign(' in line_lower or 'references(' in line_lower:
                patterns.append(InfrastructurePattern(
                    pattern_type="database_schema",
                    pattern_name="foreign_key_constraints",
                    file_path=file_path,
                    line_number=i + 1,
                    pattern_content=line.strip(),
                    confidence=0.85,
                    usage_frequency=1
                ))
        
        return patterns
    
    def _analyze_api_patterns(self) -> List[InfrastructurePattern]:
        """Analyze API endpoint patterns from route files."""
        patterns = []
        
        # Check main API routes
        api_routes_path = Path(self.repository_path) / "src" / "backend" / "routes" / "api.php"
        if api_routes_path.exists():
            patterns.extend(self._extract_api_patterns(api_routes_path))
        
        # Check portal API routes
        portal_api_path = Path(self.repository_path) / "src" / "backend" / "routes" / "portal_api.php"
        if portal_api_path.exists():
            patterns.extend(self._extract_api_patterns(portal_api_path))
        
        return patterns
    
    def _extract_api_patterns(self, file_path: Path) -> List[InfrastructurePattern]:
        """Extract API patterns from route file."""
        patterns = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                line_stripped = line.strip()
                
                # Check for RESTful routes
                if any(method in line_stripped for method in ['Route::get', 'Route::post', 'Route::put', 'Route::delete']):
                    patterns.append(InfrastructurePattern(
                        pattern_type="api_endpoint",
                        pattern_name="restful_routes",
                        file_path=str(file_path),
                        line_number=i + 1,
                        pattern_content=line_stripped,
                        confidence=0.9,
                        usage_frequency=1
                    ))
                
                # Check for API versioning
                if '/api/v' in line_stripped:
                    patterns.append(InfrastructurePattern(
                        pattern_type="api_endpoint",
                        pattern_name="api_versioning",
                        file_path=str(file_path),
                        line_number=i + 1,
                        pattern_content=line_stripped,
                        confidence=0.85,
                        usage_frequency=1
                    ))
                
                # Check for middleware usage
                if 'middleware(' in line_stripped:
                    patterns.append(InfrastructurePattern(
                        pattern_type="api_endpoint",
                        pattern_name="middleware_usage",
                        file_path=str(file_path),
                        line_number=i + 1,
                        pattern_content=line_stripped,
                        confidence=0.8,
                        usage_frequency=1
                    ))
        
        except Exception as e:
            self.logger.error(f"Error extracting API patterns from {file_path}: {e}")
        
        return patterns
    
    def _analyze_service_patterns(self) -> List[InfrastructurePattern]:
        """Analyze service layer patterns."""
        patterns = []
        services_path = Path(self.repository_path) / "src" / "backend" / "app" / "Services"
        
        if not services_path.exists():
            return patterns
        
        service_files = list(services_path.rglob("*.php"))
        
        for service_file in service_files:
            try:
                with open(service_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                patterns.extend(self._extract_service_patterns(content, str(service_file)))
                
            except Exception as e:
                self.logger.error(f"Error analyzing service {service_file}: {e}")
        
        return patterns
    
    def _extract_service_patterns(self, content: str, file_path: str) -> List[InfrastructurePattern]:
        """Extract service patterns from service class content."""
        patterns = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Check for service class definition
            if 'class ' in line_stripped and 'Service' in line_stripped:
                patterns.append(InfrastructurePattern(
                    pattern_type="service_class",
                    pattern_name="service_class_naming",
                    file_path=file_path,
                    line_number=i + 1,
                    pattern_content=line_stripped,
                    confidence=0.9,
                    usage_frequency=1
                ))
            
            # Check for dependency injection
            if '__construct(' in line_stripped and ('Repository' in line_stripped or 'Service' in line_stripped):
                patterns.append(InfrastructurePattern(
                    pattern_type="service_class",
                    pattern_name="dependency_injection",
                    file_path=file_path,
                    line_number=i + 1,
                    pattern_content=line_stripped,
                    confidence=0.85,
                    usage_frequency=1
                ))
            
            # Check for transaction usage
            if 'DB::transaction(' in line_stripped or 'transaction(' in line_stripped:
                patterns.append(InfrastructurePattern(
                    pattern_type="service_class",
                    pattern_name="database_transactions",
                    file_path=file_path,
                    line_number=i + 1,
                    pattern_content=line_stripped,
                    confidence=0.8,
                    usage_frequency=1
                ))
        
        return patterns
    
    def _analyze_model_patterns(self) -> List[InfrastructurePattern]:
        """Analyze model class patterns."""
        patterns = []
        models_path = Path(self.repository_path) / "src" / "backend" / "app" / "Models"
        
        if not models_path.exists():
            return patterns
        
        model_files = list(models_path.glob("*.php"))
        
        for model_file in model_files:
            try:
                with open(model_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                patterns.extend(self._extract_model_patterns(content, str(model_file)))
                
            except Exception as e:
                self.logger.error(f"Error analyzing model {model_file}: {e}")
        
        return patterns
    
    def _extract_model_patterns(self, content: str, file_path: str) -> List[InfrastructurePattern]:
        """Extract model patterns from model class content."""
        patterns = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Check for Eloquent model
            if 'extends Model' in line_stripped:
                patterns.append(InfrastructurePattern(
                    pattern_type="model_class",
                    pattern_name="eloquent_model",
                    file_path=file_path,
                    line_number=i + 1,
                    pattern_content=line_stripped,
                    confidence=0.95,
                    usage_frequency=1
                ))
            
            # Check for fillable fields
            if '$fillable' in line_stripped:
                patterns.append(InfrastructurePattern(
                    pattern_type="model_class",
                    pattern_name="fillable_fields",
                    file_path=file_path,
                    line_number=i + 1,
                    pattern_content=line_stripped,
                    confidence=0.9,
                    usage_frequency=1
                ))
            
            # Check for relationships
            if any(rel in line_stripped for rel in ['belongsTo(', 'hasMany(', 'hasOne(', 'belongsToMany(']):
                patterns.append(InfrastructurePattern(
                    pattern_type="model_class",
                    pattern_name="eloquent_relationships",
                    file_path=file_path,
                    line_number=i + 1,
                    pattern_content=line_stripped,
                    confidence=0.85,
                    usage_frequency=1
                ))
        
        return patterns
    
    def _analyze_controller_patterns(self) -> List[InfrastructurePattern]:
        """Analyze controller class patterns."""
        patterns = []
        controllers_path = Path(self.repository_path) / "src" / "backend" / "app" / "Http" / "Controllers"
        
        if not controllers_path.exists():
            return patterns
        
        controller_files = list(controllers_path.rglob("*.php"))
        
        for controller_file in controller_files:
            try:
                with open(controller_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                patterns.extend(self._extract_controller_patterns(content, str(controller_file)))
                
            except Exception as e:
                self.logger.error(f"Error analyzing controller {controller_file}: {e}")
        
        return patterns
    
    def _extract_controller_patterns(self, content: str, file_path: str) -> List[InfrastructurePattern]:
        """Extract controller patterns from controller class content."""
        patterns = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Check for controller class
            if 'class ' in line_stripped and 'Controller' in line_stripped:
                patterns.append(InfrastructurePattern(
                    pattern_type="controller_class",
                    pattern_name="controller_class_naming",
                    file_path=file_path,
                    line_number=i + 1,
                    pattern_content=line_stripped,
                    confidence=0.9,
                    usage_frequency=1
                ))
            
            # Check for request validation
            if 'validate(' in line_stripped or 'Validator::' in line_stripped:
                patterns.append(InfrastructurePattern(
                    pattern_type="controller_class",
                    pattern_name="request_validation",
                    file_path=file_path,
                    line_number=i + 1,
                    pattern_content=line_stripped,
                    confidence=0.85,
                    usage_frequency=1
                ))
            
            # Check for JSON responses
            if 'response()->json(' in line_stripped or 'return response(' in line_stripped:
                patterns.append(InfrastructurePattern(
                    pattern_type="controller_class",
                    pattern_name="json_responses",
                    file_path=file_path,
                    line_number=i + 1,
                    pattern_content=line_stripped,
                    confidence=0.8,
                    usage_frequency=1
                ))
        
        return patterns
    
    def _analyze_migration_patterns(self) -> List[InfrastructurePattern]:
        """Analyze migration patterns (already covered in database patterns)."""
        return []  # Covered in _analyze_database_patterns
    
    def _analyze_config_patterns(self) -> List[InfrastructurePattern]:
        """Analyze configuration patterns."""
        patterns = []
        config_path = Path(self.repository_path) / "src" / "backend" / "config"
        
        if not config_path.exists():
            return patterns
        
        config_files = list(config_path.glob("*.php"))
        
        for config_file in config_files:
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                patterns.extend(self._extract_config_patterns(content, str(config_file)))
                
            except Exception as e:
                self.logger.error(f"Error analyzing config {config_file}: {e}")
        
        return patterns
    
    def _extract_config_patterns(self, content: str, file_path: str) -> List[InfrastructurePattern]:
        """Extract configuration patterns."""
        patterns = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Check for environment variables
            if 'env(' in line_stripped:
                patterns.append(InfrastructurePattern(
                    pattern_type="config_pattern",
                    pattern_name="environment_variables",
                    file_path=file_path,
                    line_number=i + 1,
                    pattern_content=line_stripped,
                    confidence=0.9,
                    usage_frequency=1
                ))
        
        return patterns
    
    def _analyze_validation_patterns(self) -> List[InfrastructurePattern]:
        """Analyze validation rule patterns."""
        patterns = []
        
        # Look for custom validation rules
        validation_path = Path(self.repository_path) / "src" / "backend" / "app" / "Rules"
        if validation_path.exists():
            rule_files = list(validation_path.glob("*.php"))
            
            for rule_file in rule_files:
                try:
                    with open(rule_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    patterns.extend(self._extract_validation_patterns(content, str(rule_file)))
                    
                except Exception as e:
                    self.logger.error(f"Error analyzing validation rule {rule_file}: {e}")
        
        return patterns
    
    def _extract_validation_patterns(self, content: str, file_path: str) -> List[InfrastructurePattern]:
        """Extract validation patterns."""
        patterns = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Check for validation rule class
            if 'implements Rule' in line_stripped:
                patterns.append(InfrastructurePattern(
                    pattern_type="validation_rule",
                    pattern_name="custom_validation_rule",
                    file_path=file_path,
                    line_number=i + 1,
                    pattern_content=line_stripped,
                    confidence=0.9,
                    usage_frequency=1
                ))
        
        return patterns
    
    def _build_infrastructure_index(self):
        """Build searchable index of infrastructure patterns."""
        self.infrastructure_index = {}
        
        for pattern_type, patterns in self.discovered_patterns.items():
            for pattern in patterns:
                pattern_key = f"{pattern_type.value}_{pattern.pattern_name}"
                if pattern_key not in self.infrastructure_index:
                    self.infrastructure_index[pattern_key] = []
                
                self.infrastructure_index[pattern_key].append(pattern)
        
        self.logger.info(f"Built infrastructure index with {len(self.infrastructure_index)} pattern types")
    
    async def validate_infrastructure_alignment(self, 
                                              requirement_content: str,
                                              domain: str = None,
                                              context: Dict = None) -> InfrastructureValidationResult:
        """
        Validate infrastructure alignment for a requirement.
        
        Args:
            requirement_content: The requirement text to validate
            domain: Target domain for the requirement
            context: Additional context information
            
        Returns:
            InfrastructureValidationResult with detailed alignment information
        """
        start_time = datetime.now()
        requirement_id = self._generate_requirement_id(requirement_content)
        
        self.logger.info(f"Validating infrastructure alignment for requirement {requirement_id}")
        
        try:
            # Check cache first
            cache_key = self._generate_cache_key(requirement_content, domain)
            cached_result = self._get_cached_result(cache_key)
            if cached_result:
                self.logger.info(f"Using cached validation result for {requirement_id}")
                return cached_result
            
            # Perform alignment checks
            alignment_checks = await self._perform_alignment_checks(
                requirement_content, domain, context
            )
            
            # Calculate overall alignment score
            overall_score = self._calculate_overall_alignment_score(alignment_checks)
            
            # Determine validation status
            validation_status = self._determine_validation_status(overall_score, alignment_checks)
            
            # Identify critical misalignments
            critical_misalignments = self._identify_critical_misalignments(alignment_checks)
            
            # Generate recommendations
            recommendations = self._generate_alignment_recommendations(
                alignment_checks, critical_misalignments
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            result = InfrastructureValidationResult(
                requirement_id=requirement_id,
                repository_path=self.repository_path,
                repository_branch=self.target_branch,
                alignment_checks=alignment_checks,
                overall_alignment_score=overall_score,
                validation_status=validation_status.value,
                critical_misalignments=critical_misalignments,
                recommendations=recommendations,
                processing_time=processing_time,
                validation_metadata={
                    "domain": domain,
                    "patterns_analyzed": len(self.infrastructure_index),
                    "validation_timestamp": datetime.now().isoformat(),
                    "repository_available": Path(self.repository_path).exists()
                }
            )
            
            # Cache the result
            self._cache_result(cache_key, result)
            
            self.logger.info(f"Infrastructure validation completed for {requirement_id} in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            self.logger.error(f"Error validating infrastructure alignment for requirement {requirement_id}: {e}")
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return InfrastructureValidationResult(
                requirement_id=requirement_id,
                repository_path=self.repository_path,
                repository_branch=self.target_branch,
                alignment_checks=[],
                overall_alignment_score=0.0,
                validation_status=AlignmentStatus.ERROR.value,
                critical_misalignments=[],
                recommendations=[],
                processing_time=processing_time,
                validation_metadata={"error": str(e)}
            )
    
    async def _perform_alignment_checks(self, 
                                      requirement_content: str,
                                      domain: str = None,
                                      context: Dict = None) -> List[AlignmentCheck]:
        """Perform various alignment checks against infrastructure patterns."""
        alignment_checks = []
        
        # Database alignment check
        db_check = await self._check_database_alignment(requirement_content)
        if db_check:
            alignment_checks.append(db_check)
        
        # API alignment check
        api_check = await self._check_api_alignment(requirement_content)
        if api_check:
            alignment_checks.append(api_check)
        
        # Service layer alignment check
        service_check = await self._check_service_alignment(requirement_content)
        if service_check:
            alignment_checks.append(service_check)
        
        # Model alignment check
        model_check = await self._check_model_alignment(requirement_content)
        if model_check:
            alignment_checks.append(model_check)
        
        # Controller alignment check
        controller_check = await self._check_controller_alignment(requirement_content)
        if controller_check:
            alignment_checks.append(controller_check)
        
        return alignment_checks
    
    async def _check_database_alignment(self, requirement_content: str) -> Optional[AlignmentCheck]:
        """Check database schema alignment."""
        if not any(keyword in requirement_content.lower() for keyword in ['table', 'database', 'schema', 'migration']):
            return None
        
        relevant_patterns = self.discovered_patterns.get(PatternType.DATABASE_SCHEMA, [])
        recommendations = []
        alignment_status = "aligned"
        confidence_score = 0.8
        
        # Check for audit fields mention
        has_audit_fields = any(field in requirement_content.lower() 
                             for field in ['created_at', 'updated_at', 'timestamps'])
        
        if not has_audit_fields:
            recommendations.append("Consider adding audit fields (created_at, updated_at, created_by, updated_by)")
            alignment_status = "needs_updates"
            confidence_score = 0.6
        
        # Check for naming conventions
        table_mentions = re.findall(r'\btable[s]?\s+[`"]?(\w+)[`"]?', requirement_content.lower())
        for table_name in table_mentions:
            if not re.match(r'^[a-z][a-z0-9_]*[a-z0-9]$', table_name):
                recommendations.append(f"Table name '{table_name}' should follow snake_case convention")
                alignment_status = "misaligned"
                confidence_score = 0.4
        
        return AlignmentCheck(
            check_type="database_schema",
            check_name="Database Schema Alignment",
            alignment_status=alignment_status,
            existing_patterns=relevant_patterns,
            recommendations=recommendations,
            confidence_score=confidence_score,
            severity="major" if alignment_status == "misaligned" else "minor"
        )
    
    async def _check_api_alignment(self, requirement_content: str) -> Optional[AlignmentCheck]:
        """Check API endpoint alignment."""
        if not any(keyword in requirement_content.lower() for keyword in ['api', 'endpoint', 'route', 'rest']):
            return None
        
        relevant_patterns = self.discovered_patterns.get(PatternType.API_ENDPOINT, [])
        recommendations = []
        alignment_status = "aligned"
        confidence_score = 0.8
        
        # Check for RESTful patterns
        has_restful_mention = any(method in requirement_content.lower() 
                                for method in ['get', 'post', 'put', 'delete', 'patch'])
        
        if not has_restful_mention:
            recommendations.append("Consider using RESTful HTTP methods (GET, POST, PUT, DELETE)")
            alignment_status = "needs_updates"
            confidence_score = 0.6
        
        # Check for versioning
        if '/api/' in requirement_content.lower() and '/v' not in requirement_content.lower():
            recommendations.append("Consider API versioning (e.g., /api/v1/)")
            confidence_score = min(confidence_score, 0.7)
        
        return AlignmentCheck(
            check_type="api_endpoint",
            check_name="API Endpoint Alignment",
            alignment_status=alignment_status,
            existing_patterns=relevant_patterns,
            recommendations=recommendations,
            confidence_score=confidence_score,
            severity="minor"
        )
    
    async def _check_service_alignment(self, requirement_content: str) -> Optional[AlignmentCheck]:
        """Check service layer alignment."""
        if not any(keyword in requirement_content.lower() for keyword in ['service', 'business logic', 'transaction']):
            return None
        
        relevant_patterns = self.discovered_patterns.get(PatternType.SERVICE_CLASS, [])
        recommendations = []
        alignment_status = "aligned"
        confidence_score = 0.7
        
        # Check for transaction mentions
        if any(keyword in requirement_content.lower() for keyword in ['create', 'update', 'delete', 'process']):
            if 'transaction' not in requirement_content.lower():
                recommendations.append("Consider using database transactions for data integrity")
                confidence_score = min(confidence_score, 0.6)
        
        return AlignmentCheck(
            check_type="service_layer",
            check_name="Service Layer Alignment",
            alignment_status=alignment_status,
            existing_patterns=relevant_patterns,
            recommendations=recommendations,
            confidence_score=confidence_score,
            severity="minor"
        )
    
    async def _check_model_alignment(self, requirement_content: str) -> Optional[AlignmentCheck]:
        """Check model class alignment."""
        if not any(keyword in requirement_content.lower() for keyword in ['model', 'entity', 'eloquent']):
            return None
        
        relevant_patterns = self.discovered_patterns.get(PatternType.MODEL_CLASS, [])
        recommendations = []
        alignment_status = "aligned"
        confidence_score = 0.8
        
        # Check for relationship mentions
        relationship_keywords = ['belongs to', 'has many', 'has one', 'many to many']
        has_relationships = any(keyword in requirement_content.lower() for keyword in relationship_keywords)
        
        if has_relationships:
            recommendations.append("Ensure Eloquent relationships are properly defined")
        
        return AlignmentCheck(
            check_type="model_class",
            check_name="Model Class Alignment",
            alignment_status=alignment_status,
            existing_patterns=relevant_patterns,
            recommendations=recommendations,
            confidence_score=confidence_score,
            severity="minor"
        )
    
    async def _check_controller_alignment(self, requirement_content: str) -> Optional[AlignmentCheck]:
        """Check controller class alignment."""
        if not any(keyword in requirement_content.lower() for keyword in ['controller', 'request', 'response']):
            return None
        
        relevant_patterns = self.discovered_patterns.get(PatternType.CONTROLLER_CLASS, [])
        recommendations = []
        alignment_status = "aligned"
        confidence_score = 0.8
        
        # Check for validation mentions
        if any(keyword in requirement_content.lower() for keyword in ['validate', 'validation', 'input']):
            recommendations.append("Implement proper request validation")
        
        # Check for response format
        if 'json' not in requirement_content.lower() and 'api' in requirement_content.lower():
            recommendations.append("Use consistent JSON response format")
            confidence_score = min(confidence_score, 0.7)
        
        return AlignmentCheck(
            check_type="controller_class",
            check_name="Controller Class Alignment",
            alignment_status=alignment_status,
            existing_patterns=relevant_patterns,
            recommendations=recommendations,
            confidence_score=confidence_score,
            severity="minor"
        )
    
    def _calculate_overall_alignment_score(self, alignment_checks: List[AlignmentCheck]) -> float:
        """Calculate overall alignment score."""
        if not alignment_checks:
            return 1.0  # No checks means perfect alignment
        
        total_score = 0.0
        total_weight = 0.0
        
        for check in alignment_checks:
            # Weight by severity
            weight = {"critical": 1.0, "major": 0.8, "minor": 0.6, "info": 0.4}.get(check.severity, 0.6)
            total_score += check.confidence_score * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def _determine_validation_status(self, overall_score: float, alignment_checks: List[AlignmentCheck]) -> AlignmentStatus:
        """Determine overall validation status."""
        misaligned_checks = [check for check in alignment_checks if check.alignment_status == "misaligned"]
        needs_updates_checks = [check for check in alignment_checks if check.alignment_status == "needs_updates"]
        
        if misaligned_checks:
            return AlignmentStatus.MISALIGNED
        elif overall_score >= 0.90:
            return AlignmentStatus.ALIGNED
        elif overall_score >= 0.70 or needs_updates_checks:
            return AlignmentStatus.NEEDS_UPDATES
        else:
            return AlignmentStatus.MISALIGNED
    
    def _identify_critical_misalignments(self, alignment_checks: List[AlignmentCheck]) -> List[Dict]:
        """Identify critical misalignments."""
        critical_issues = []
        
        for check in alignment_checks:
            if check.alignment_status == "misaligned" and check.severity in ["critical", "major"]:
                critical_issues.append({
                    "check_type": check.check_type,
                    "check_name": check.check_name,
                    "severity": check.severity,
                    "confidence": check.confidence_score,
                    "recommendations": check.recommendations
                })
        
        return critical_issues
    
    def _generate_alignment_recommendations(self, 
                                          alignment_checks: List[AlignmentCheck],
                                          critical_misalignments: List[Dict]) -> List[str]:
        """Generate recommendations for alignment improvements."""
        recommendations = []
        
        # Collect all recommendations from checks
        for check in alignment_checks:
            recommendations.extend(check.recommendations)
        
        # Add general recommendations
        if critical_misalignments:
            recommendations.insert(0, "CRITICAL: Address critical misalignments before proceeding")
        
        # Add infrastructure-specific recommendations
        recommendations.append("Follow existing Laravel/PHP coding standards")
        recommendations.append("Ensure proper error handling and logging")
        recommendations.append("Consider performance implications of database changes")
        
        return list(set(recommendations))  # Remove duplicates
    
    def _generate_requirement_id(self, content: str) -> str:
        """Generate unique ID for a requirement."""
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:12]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"infra_{timestamp}_{content_hash}"
    
    def _generate_cache_key(self, requirement_content: str, domain: str = None) -> str:
        """Generate cache key for validation."""
        content_hash = hashlib.sha256(requirement_content.encode()).hexdigest()[:16]
        domain_suffix = f"_{domain}" if domain else ""
        return f"infra_{content_hash}{domain_suffix}"
    
    def _get_cached_result(self, cache_key: str) -> Optional[InfrastructureValidationResult]:
        """Get cached validation result if available."""
        if not self.config.get("performance", {}).get("cache_enabled", True):
            return None
        
        if cache_key not in self.validation_cache:
            return None
        
        cached_entry = self.validation_cache[cache_key]
        cache_ttl_hours = self.config.get("performance", {}).get("cache_ttl_hours", 24)
        
        if datetime.now() - cached_entry["timestamp"] > timedelta(hours=cache_ttl_hours):
            del self.validation_cache[cache_key]
            return None
        
        return cached_entry["result"]
    
    def _cache_result(self, cache_key: str, result: InfrastructureValidationResult):
        """Cache validation result."""
        if not self.config.get("performance", {}).get("cache_enabled", True):
            return
        
        max_cache_size = self.config.get("performance", {}).get("max_cache_size", 100)
        
        # Clean up old entries if cache is full
        if len(self.validation_cache) >= max_cache_size:
            oldest_key = min(self.validation_cache.keys(), 
                           key=lambda k: self.validation_cache[k]["timestamp"])
            del self.validation_cache[oldest_key]
        
        self.validation_cache[cache_key] = {
            "result": result,
            "timestamp": datetime.now()
        }
    
    def get_validation_statistics(self) -> Dict:
        """Get statistics about infrastructure validation."""
        pattern_counts = {}
        for pattern_type, patterns in self.discovered_patterns.items():
            pattern_counts[pattern_type.value] = len(patterns)
        
        return {
            "repository_path": self.repository_path,
            "repository_available": Path(self.repository_path).exists(),
            "target_branch": self.target_branch,
            "discovered_patterns": pattern_counts,
            "infrastructure_index_size": len(self.infrastructure_index),
            "cache_size": len(self.validation_cache),
            "pattern_analyzers": list(self.pattern_analyzers.keys())
        }

# Main execution and testing
if __name__ == "__main__":
    async def test_infrastructure_validator():
        """Test the Infrastructure Validator."""
        print("Testing Infrastructure Validator...")
        
        # Initialize validator
        validator = InfrastructureValidator()
        
        # Test validation statistics
        stats = validator.get_validation_statistics()
        print(f"Validation Statistics: {json.dumps(stats, indent=2, default=str)}")
        
        # Test infrastructure validation
        test_requirement = """
        Create a new quotes table in the database with the following fields:
        - quote_id (primary key)
        - producer_id (foreign key)
        - driver_id (foreign key)
        - effective_date
        - premium_amount
        - status
        
        Create a REST API endpoint GET /api/v1/quotes to retrieve quotes.
        Implement a QuoteService class to handle business logic and a Quote model
        with Eloquent relationships to Producer and Driver models.
        """
        
        result = await validator.validate_infrastructure_alignment(
            requirement_content=test_requirement,
            domain="producer_portal",
            context={"priority": "high"}
        )
        
        print(f"Validation Result: {json.dumps(asdict(result), indent=2, default=str)}")
        
        return validator
    
    # Run test if executed directly
    import asyncio
    asyncio.run(test_infrastructure_validator())