#!/usr/bin/env python3
"""
Global Requirements Compliance Checker
Complete Requirements Generation System - Multi-Agent Architecture

Automated checking against all 64+ Global Requirements for comprehensive
compliance validation across all business domains.

Created: 2025-01-07
Version: 1.0.0
GR Compliance: GR-02, GR-10, GR-19, GR-41, GR-44, GR-52, GR-64
"""

import json
import yaml
import logging
import asyncio
from typing import Dict, List, Optional, Tuple, Any, Set
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
from dataclasses import dataclass, asdict
from enum import Enum
import re
from collections import defaultdict

# Configuration and Data Classes
@dataclass
class GRComplianceRule:
    """Represents a Global Requirements compliance rule."""
    gr_id: str
    gr_name: str
    description: str
    compliance_criteria: List[str]
    validation_rules: List[Dict]
    applicable_domains: List[str]
    entity_dependencies: List[str]
    priority: str  # critical, high, medium, low
    auto_fixable: bool

@dataclass
class ComplianceViolation:
    """Represents a compliance violation."""
    gr_id: str
    violation_type: str
    severity: str  # critical, major, minor, warning
    description: str
    location: str
    suggested_fix: str
    auto_fixable: bool
    confidence: float

@dataclass
class ComplianceCheckResult:
    """Result of GR compliance checking."""
    requirement_id: str
    total_grs_checked: int
    grs_passed: List[str]
    grs_failed: List[str]
    violations: List[ComplianceViolation]
    overall_compliance_score: float
    compliance_status: str  # compliant, non_compliant, partial_compliant
    recommendations: List[str]
    processing_time: float
    check_metadata: Dict

class ComplianceStatus(Enum):
    """Compliance status levels."""
    COMPLIANT = "compliant"
    PARTIAL_COMPLIANT = "partial_compliant"
    NON_COMPLIANT = "non_compliant"
    ERROR = "error"

class ViolationSeverity(Enum):
    """Severity levels for violations."""
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    WARNING = "warning"

class GRComplianceChecker:
    """
    Automated checker for Global Requirements compliance across all domains.
    Validates requirements against the complete set of 64+ Global Requirements.
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the GR Compliance Checker."""
        self.config_path = config_path or "/app/workspace/requirements/shared-infrastructure/agent-configurations/universal-validator.yaml"
        self.config = self._load_configuration()
        self.logger = self._setup_logging()
        
        # Global Requirements repository
        self.gr_index = {}
        self.gr_rules = {}
        self.compliance_cache = {}
        
        # Validation engines
        self.validation_engines = {}
        self.domain_specific_rules = {}
        
        # Performance tracking
        self.performance_metrics = {}
        
        # Initialize compliance checker
        self._initialize_compliance_checker()
    
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
            "validation": {
                "compliance_threshold": 0.95,
                "critical_gr_threshold": 1.0,
                "auto_fix_enabled": False
            },
            "performance": {
                "cache_enabled": True,
                "cache_ttl_hours": 12,
                "max_cache_size": 500
            }
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the compliance checker."""
        logger = logging.getLogger("GRComplianceChecker")
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def _initialize_compliance_checker(self):
        """Initialize all compliance checking components."""
        self.logger.info("Initializing GR Compliance Checker...")
        
        try:
            # Load Global Requirements index
            self._load_global_requirements_index()
            
            # Initialize compliance rules
            self._initialize_compliance_rules()
            
            # Load domain-specific rules
            self._load_domain_specific_rules()
            
            # Initialize validation engines
            self._initialize_validation_engines()
            
            self.logger.info("GR Compliance Checker initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize compliance checker: {e}")
            raise
    
    def _load_global_requirements_index(self):
        """Load the Global Requirements index."""
        gr_index_path = "/app/workspace/requirements/shared-infrastructure/knowledge-base/global-requirements-index.json"
        
        if not Path(gr_index_path).exists():
            self.logger.warning("Global Requirements index not found")
            self.gr_index = self._create_default_gr_index()
            return
        
        try:
            with open(gr_index_path, 'r') as f:
                self.gr_index = json.load(f)
            
            self.logger.info(f"Loaded {len(self.gr_index.get('global_requirements', []))} Global Requirements")
            
        except Exception as e:
            self.logger.error(f"Error loading Global Requirements index: {e}")
            self.gr_index = self._create_default_gr_index()
    
    def _create_default_gr_index(self) -> Dict:
        """Create a default Global Requirements index."""
        return {
            "global_requirements": [
                {
                    "gr_id": "GR-02",
                    "name": "Database Design Principles",
                    "description": "Core database design standards including audit fields",
                    "domains": ["all"],
                    "priority": "critical"
                },
                {
                    "gr_id": "GR-10", 
                    "name": "SR22/SR26 Financial Responsibility Filing",
                    "description": "Financial responsibility filing requirements",
                    "domains": ["sr22", "producer_portal"],
                    "priority": "high"
                },
                {
                    "gr_id": "GR-19",
                    "name": "Table Relationships",
                    "description": "Standard table relationship patterns",
                    "domains": ["all"],
                    "priority": "critical"
                },
                {
                    "gr_id": "GR-41",
                    "name": "Database Design Standards",
                    "description": "Naming conventions and schema standards",
                    "domains": ["all"],
                    "priority": "critical"
                },
                {
                    "gr_id": "GR-44",
                    "name": "Communication Architecture",
                    "description": "Unified communication patterns",
                    "domains": ["all"],
                    "priority": "high"
                },
                {
                    "gr_id": "GR-52",
                    "name": "Universal Entity Management",
                    "description": "Universal entity patterns for external entities",
                    "domains": ["all"],
                    "priority": "critical"
                },
                {
                    "gr_id": "GR-64",
                    "name": "Policy Reinstatement Process",
                    "description": "Comprehensive reinstatement workflow",
                    "domains": ["reinstatement", "producer_portal"],
                    "priority": "high"
                }
            ]
        }
    
    def _initialize_compliance_rules(self):
        """Initialize compliance rules for each Global Requirement."""
        global_requirements = self.gr_index.get("global_requirements", [])
        
        for gr in global_requirements:
            gr_id = gr["gr_id"]
            
            # Create compliance rule based on GR
            rule = self._create_compliance_rule(gr)
            self.gr_rules[gr_id] = rule
        
        self.logger.info(f"Initialized {len(self.gr_rules)} compliance rules")
    
    def _create_compliance_rule(self, gr_data: Dict) -> GRComplianceRule:
        """Create a compliance rule from GR data."""
        gr_id = gr_data["gr_id"]
        
        # Define compliance criteria based on GR type
        compliance_criteria = self._get_compliance_criteria(gr_id)
        validation_rules = self._get_validation_rules(gr_id)
        
        return GRComplianceRule(
            gr_id=gr_id,
            gr_name=gr_data.get("name", ""),
            description=gr_data.get("description", ""),
            compliance_criteria=compliance_criteria,
            validation_rules=validation_rules,
            applicable_domains=gr_data.get("domains", ["all"]),
            entity_dependencies=self._get_entity_dependencies(gr_id),
            priority=gr_data.get("priority", "medium"),
            auto_fixable=self._is_auto_fixable(gr_id)
        )
    
    def _get_compliance_criteria(self, gr_id: str) -> List[str]:
        """Get compliance criteria for a specific GR."""
        criteria_map = {
            "GR-02": [
                "All tables must include audit fields (created_at, updated_at, created_by, updated_by)",
                "Status fields must follow enum patterns",
                "Soft delete patterns must be implemented"
            ],
            "GR-10": [
                "SR22 filing capabilities must be present",
                "State compliance validation required",
                "Financial responsibility tracking implemented"
            ],
            "GR-19": [
                "Foreign key relationships properly defined",
                "Referential integrity maintained",
                "Relationship naming follows conventions"
            ],
            "GR-41": [
                "Table names follow snake_case convention",
                "Column names are descriptive and consistent",
                "Index naming follows standards"
            ],
            "GR-44": [
                "Communication templates implemented",
                "Multi-channel support present",
                "Message tracking capabilities"
            ],
            "GR-52": [
                "Universal entity patterns used for external entities",
                "Metadata schema compliance",
                "Entity reuse validated"
            ],
            "GR-64": [
                "Reinstatement workflow implemented",
                "Grace period handling present",
                "Policy restoration capabilities"
            ]
        }
        
        return criteria_map.get(gr_id, ["Generic compliance validation required"])
    
    def _get_validation_rules(self, gr_id: str) -> List[Dict]:
        """Get validation rules for a specific GR."""
        rules_map = {
            "GR-02": [
                {
                    "rule_type": "table_structure",
                    "check": "audit_fields_present",
                    "required_fields": ["created_at", "updated_at", "created_by", "updated_by"]
                }
            ],
            "GR-19": [
                {
                    "rule_type": "foreign_keys",
                    "check": "proper_relationships",
                    "naming_pattern": r".*_id$"
                }
            ],
            "GR-41": [
                {
                    "rule_type": "naming_convention",
                    "check": "snake_case_tables",
                    "pattern": r"^[a-z][a-z0-9_]*[a-z0-9]$"
                }
            ],
            "GR-52": [
                {
                    "rule_type": "entity_pattern",
                    "check": "universal_entity_usage",
                    "required_metadata": ["entity_type", "source_system"]
                }
            ]
        }
        
        return rules_map.get(gr_id, [])
    
    def _get_entity_dependencies(self, gr_id: str) -> List[str]:
        """Get entity dependencies for a specific GR."""
        dependencies_map = {
            "GR-02": ["all_entities"],
            "GR-10": ["sr22_filing", "financial_responsibility"],
            "GR-19": ["all_entities"],
            "GR-41": ["all_entities"],
            "GR-44": ["communication", "message", "template"],
            "GR-52": ["external_entities", "universal_entities"],
            "GR-64": ["policy", "reinstatement", "lapse"]
        }
        
        return dependencies_map.get(gr_id, [])
    
    def _is_auto_fixable(self, gr_id: str) -> bool:
        """Determine if violations for this GR can be auto-fixed."""
        auto_fixable_grs = ["GR-41"]  # Naming conventions can often be auto-fixed
        return gr_id in auto_fixable_grs
    
    def _load_domain_specific_rules(self):
        """Load domain-specific compliance rules."""
        domains = ["producer_portal", "accounting", "program_manager", 
                  "program_traits", "entity_integration", "reinstatement", "sr22"]
        
        for domain in domains:
            domain_rules = self._get_domain_rules(domain)
            self.domain_specific_rules[domain] = domain_rules
        
        self.logger.info(f"Loaded domain-specific rules for {len(domains)} domains")
    
    def _get_domain_rules(self, domain: str) -> Dict:
        """Get domain-specific compliance rules."""
        # Simplified domain rules - in practice these would be loaded from files
        return {
            "required_entities": self._get_domain_required_entities(domain),
            "workflow_requirements": self._get_domain_workflow_requirements(domain),
            "integration_requirements": self._get_domain_integration_requirements(domain)
        }
    
    def _get_domain_required_entities(self, domain: str) -> List[str]:
        """Get required entities for a domain."""
        domain_entities = {
            "producer_portal": ["quote", "policy", "driver", "vehicle", "producer"],
            "accounting": ["payment", "billing_account", "commission", "transaction"],
            "program_manager": ["rate_factor", "territory", "program", "coverage"],
            "program_traits": ["trait", "rule", "configuration"],
            "entity_integration": ["external_entity", "integration_point"],
            "reinstatement": ["policy", "lapse", "reinstatement"],
            "sr22": ["sr22_filing", "financial_responsibility"]
        }
        
        return domain_entities.get(domain, [])
    
    def _get_domain_workflow_requirements(self, domain: str) -> List[str]:
        """Get workflow requirements for a domain."""
        return ["standard_workflow", "error_handling", "audit_trail"]
    
    def _get_domain_integration_requirements(self, domain: str) -> List[str]:
        """Get integration requirements for a domain."""
        return ["api_compliance", "event_handling", "data_validation"]
    
    def _initialize_validation_engines(self):
        """Initialize validation engines for different types of checks."""
        self.validation_engines = {
            "table_structure": self._validate_table_structure,
            "naming_convention": self._validate_naming_convention,
            "foreign_keys": self._validate_foreign_keys,
            "entity_pattern": self._validate_entity_pattern,
            "communication": self._validate_communication,
            "workflow": self._validate_workflow
        }
        
        self.logger.info(f"Initialized {len(self.validation_engines)} validation engines")
    
    async def check_gr_compliance(self, 
                                requirement_content: str,
                                domain: str = None,
                                applicable_grs: List[str] = None,
                                context: Dict = None) -> ComplianceCheckResult:
        """
        Check Global Requirements compliance for a requirement.
        
        Args:
            requirement_content: The requirement text to validate
            domain: Target domain for domain-specific checks
            applicable_grs: List of GRs to check (if None, auto-detect)
            context: Additional context information
            
        Returns:
            ComplianceCheckResult with detailed compliance information
        """
        start_time = datetime.now()
        requirement_id = self._generate_requirement_id(requirement_content)
        
        self.logger.info(f"Checking GR compliance for requirement {requirement_id}")
        
        try:
            # Check cache first
            cache_key = self._generate_cache_key(requirement_content, domain, applicable_grs)
            cached_result = self._get_cached_result(cache_key)
            if cached_result:
                self.logger.info(f"Using cached compliance result for {requirement_id}")
                return cached_result
            
            # Determine applicable GRs
            if not applicable_grs:
                applicable_grs = await self._auto_detect_applicable_grs(requirement_content, domain)
            
            # Perform compliance checks
            compliance_results = {}
            violations = []
            
            for gr_id in applicable_grs:
                if gr_id in self.gr_rules:
                    gr_rule = self.gr_rules[gr_id]
                    
                    # Check compliance for this GR
                    gr_result = await self._check_single_gr_compliance(
                        requirement_content, gr_rule, domain, context
                    )
                    
                    compliance_results[gr_id] = gr_result
                    
                    # Collect violations
                    if not gr_result["compliant"]:
                        violations.extend(gr_result["violations"])
            
            # Calculate overall compliance
            overall_score = self._calculate_overall_compliance_score(compliance_results)
            compliance_status = self._determine_compliance_status(overall_score, violations)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(violations, compliance_results)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            result = ComplianceCheckResult(
                requirement_id=requirement_id,
                total_grs_checked=len(applicable_grs),
                grs_passed=[gr_id for gr_id, result in compliance_results.items() if result["compliant"]],
                grs_failed=[gr_id for gr_id, result in compliance_results.items() if not result["compliant"]],
                violations=violations,
                overall_compliance_score=overall_score,
                compliance_status=compliance_status.value,
                recommendations=recommendations,
                processing_time=processing_time,
                check_metadata={
                    "domain": domain,
                    "applicable_grs": applicable_grs,
                    "check_timestamp": datetime.now().isoformat(),
                    "validation_engines_used": list(self.validation_engines.keys())
                }
            )
            
            # Cache the result
            self._cache_result(cache_key, result)
            
            self.logger.info(f"Compliance check completed for {requirement_id} in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            self.logger.error(f"Error checking compliance for requirement {requirement_id}: {e}")
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return ComplianceCheckResult(
                requirement_id=requirement_id,
                total_grs_checked=0,
                grs_passed=[],
                grs_failed=[],
                violations=[],
                overall_compliance_score=0.0,
                compliance_status=ComplianceStatus.ERROR.value,
                recommendations=[],
                processing_time=processing_time,
                check_metadata={"error": str(e)}
            )
    
    async def _auto_detect_applicable_grs(self, requirement_content: str, domain: str = None) -> List[str]:
        """Auto-detect applicable Global Requirements for a requirement."""
        applicable_grs = []
        content_lower = requirement_content.lower()
        
        # Check all GRs for applicability
        for gr_id, gr_rule in self.gr_rules.items():
            # Check domain applicability
            if domain and "all" not in gr_rule.applicable_domains and domain not in gr_rule.applicable_domains:
                continue
            
            # Check content keywords
            gr_keywords = self._get_gr_keywords(gr_id)
            keyword_matches = sum(1 for keyword in gr_keywords if keyword in content_lower)
            
            # Check entity dependencies
            entity_matches = sum(1 for entity in gr_rule.entity_dependencies 
                               if entity in content_lower or entity.replace("_", " ") in content_lower)
            
            # Determine applicability
            total_indicators = len(gr_keywords) + len(gr_rule.entity_dependencies)
            total_matches = keyword_matches + entity_matches
            
            if total_indicators > 0:
                match_ratio = total_matches / total_indicators
                if match_ratio >= 0.3:  # 30% match threshold
                    applicable_grs.append(gr_id)
        
        # Always include critical GRs
        critical_grs = ["GR-02", "GR-19", "GR-41", "GR-52"]
        for gr_id in critical_grs:
            if gr_id not in applicable_grs and gr_id in self.gr_rules:
                applicable_grs.append(gr_id)
        
        self.logger.info(f"Auto-detected applicable GRs: {applicable_grs}")
        return applicable_grs
    
    def _get_gr_keywords(self, gr_id: str) -> List[str]:
        """Get keywords that indicate applicability of a GR."""
        keywords_map = {
            "GR-02": ["database", "table", "audit", "created", "updated"],
            "GR-10": ["sr22", "sr26", "financial responsibility", "filing"],
            "GR-19": ["relationship", "foreign key", "reference", "link"],
            "GR-41": ["naming", "convention", "schema", "table name", "column"],
            "GR-44": ["communication", "email", "sms", "notification", "message"],
            "GR-52": ["entity", "external", "universal", "api", "integration"],
            "GR-64": ["reinstatement", "lapse", "policy", "restore", "grace period"]
        }
        
        return keywords_map.get(gr_id, [])
    
    async def _check_single_gr_compliance(self, 
                                        requirement_content: str,
                                        gr_rule: GRComplianceRule,
                                        domain: str = None,
                                        context: Dict = None) -> Dict:
        """Check compliance for a single Global Requirement."""
        self.logger.debug(f"Checking compliance for {gr_rule.gr_id}")
        
        violations = []
        compliance_score = 1.0
        
        # Run validation rules for this GR
        for validation_rule in gr_rule.validation_rules:
            rule_type = validation_rule.get("rule_type")
            
            if rule_type in self.validation_engines:
                try:
                    validation_engine = self.validation_engines[rule_type]
                    rule_result = await validation_engine(
                        requirement_content, validation_rule, gr_rule, domain, context
                    )
                    
                    if not rule_result["passed"]:
                        violations.extend(rule_result["violations"])
                        compliance_score *= rule_result.get("score", 0.0)
                    
                except Exception as e:
                    self.logger.error(f"Error in validation engine {rule_type}: {e}")
                    violations.append(ComplianceViolation(
                        gr_id=gr_rule.gr_id,
                        violation_type="validation_error",
                        severity=ViolationSeverity.MAJOR.value,
                        description=f"Validation engine error: {e}",
                        location="validation_engine",
                        suggested_fix="Check validation engine configuration",
                        auto_fixable=False,
                        confidence=0.9
                    ))
                    compliance_score *= 0.5
        
        # Additional heuristic checks
        heuristic_result = await self._perform_heuristic_checks(
            requirement_content, gr_rule, domain
        )
        
        if not heuristic_result["passed"]:
            violations.extend(heuristic_result["violations"])
            compliance_score *= heuristic_result.get("score", 0.8)
        
        return {
            "gr_id": gr_rule.gr_id,
            "compliant": len(violations) == 0,
            "compliance_score": compliance_score,
            "violations": violations,
            "checks_performed": len(gr_rule.validation_rules) + 1  # +1 for heuristic
        }
    
    async def _validate_table_structure(self, 
                                      requirement_content: str,
                                      validation_rule: Dict,
                                      gr_rule: GRComplianceRule,
                                      domain: str = None,
                                      context: Dict = None) -> Dict:
        """Validate table structure compliance."""
        violations = []
        
        # Check for table definitions in requirement
        table_mentions = re.findall(r'\btable[s]?\s+(\w+)', requirement_content.lower())
        
        if table_mentions and validation_rule.get("check") == "audit_fields_present":
            required_fields = validation_rule.get("required_fields", [])
            
            for field in required_fields:
                if field not in requirement_content.lower():
                    violations.append(ComplianceViolation(
                        gr_id=gr_rule.gr_id,
                        violation_type="missing_audit_field",
                        severity=ViolationSeverity.MAJOR.value,
                        description=f"Required audit field '{field}' not mentioned in table definition",
                        location="table_structure",
                        suggested_fix=f"Add '{field}' field to table definition with appropriate type",
                        auto_fixable=True,
                        confidence=0.8
                    ))
        
        return {
            "passed": len(violations) == 0,
            "violations": violations,
            "score": 1.0 if len(violations) == 0 else 0.6
        }
    
    async def _validate_naming_convention(self, 
                                        requirement_content: str,
                                        validation_rule: Dict,
                                        gr_rule: GRComplianceRule,
                                        domain: str = None,
                                        context: Dict = None) -> Dict:
        """Validate naming convention compliance."""
        violations = []
        
        # Extract table names from requirement
        table_names = re.findall(r'\btable[s]?\s+[`"]?(\w+)[`"]?', requirement_content.lower())
        
        if validation_rule.get("check") == "snake_case_tables":
            pattern = validation_rule.get("pattern")
            if pattern:
                for table_name in table_names:
                    if not re.match(pattern, table_name):
                        violations.append(ComplianceViolation(
                            gr_id=gr_rule.gr_id,
                            violation_type="naming_convention_violation",
                            severity=ViolationSeverity.MINOR.value,
                            description=f"Table name '{table_name}' does not follow snake_case convention",
                            location="table_name",
                            suggested_fix=f"Change table name to snake_case format",
                            auto_fixable=True,
                            confidence=0.9
                        ))
        
        return {
            "passed": len(violations) == 0,
            "violations": violations,
            "score": 1.0 if len(violations) == 0 else 0.8
        }
    
    async def _validate_foreign_keys(self, 
                                   requirement_content: str,
                                   validation_rule: Dict,
                                   gr_rule: GRComplianceRule,
                                   domain: str = None,
                                   context: Dict = None) -> Dict:
        """Validate foreign key compliance."""
        violations = []
        
        # Look for foreign key mentions
        fk_mentions = re.findall(r'(\w+_id)\b', requirement_content.lower())
        
        if validation_rule.get("check") == "proper_relationships":
            pattern = validation_rule.get("naming_pattern")
            
            # Check if foreign keys follow naming convention
            for fk in fk_mentions:
                if pattern and not re.match(pattern, fk):
                    violations.append(ComplianceViolation(
                        gr_id=gr_rule.gr_id,
                        violation_type="foreign_key_naming",
                        severity=ViolationSeverity.MINOR.value,
                        description=f"Foreign key '{fk}' may not follow proper naming convention",
                        location="foreign_key",
                        suggested_fix="Ensure foreign keys end with '_id'",
                        auto_fixable=False,
                        confidence=0.7
                    ))
        
        return {
            "passed": len(violations) == 0,
            "violations": violations,
            "score": 1.0 if len(violations) == 0 else 0.8
        }
    
    async def _validate_entity_pattern(self, 
                                     requirement_content: str,
                                     validation_rule: Dict,
                                     gr_rule: GRComplianceRule,
                                     domain: str = None,
                                     context: Dict = None) -> Dict:
        """Validate universal entity pattern compliance."""
        violations = []
        
        # Check for universal entity usage
        universal_entities = ["address", "phone", "email", "payment"]
        external_keywords = ["external", "api", "third party", "vendor", "service"]
        
        has_external_mentions = any(keyword in requirement_content.lower() for keyword in external_keywords)
        
        if has_external_mentions:
            # Should use universal entity patterns
            has_universal_entity = any(entity in requirement_content.lower() for entity in universal_entities)
            
            if not has_universal_entity:
                violations.append(ComplianceViolation(
                    gr_id=gr_rule.gr_id,
                    violation_type="missing_universal_entity",
                    severity=ViolationSeverity.MAJOR.value,
                    description="External integration should use universal entity patterns",
                    location="entity_integration",
                    suggested_fix="Use universal entity patterns for external data (address, phone, email, payment)",
                    auto_fixable=False,
                    confidence=0.8
                ))
        
        return {
            "passed": len(violations) == 0,
            "violations": violations,
            "score": 1.0 if len(violations) == 0 else 0.7
        }
    
    async def _validate_communication(self, 
                                    requirement_content: str,
                                    validation_rule: Dict,
                                    gr_rule: GRComplianceRule,
                                    domain: str = None,
                                    context: Dict = None) -> Dict:
        """Validate communication pattern compliance."""
        violations = []
        
        # Check for communication mentions
        comm_keywords = ["email", "sms", "notification", "message", "alert", "communication"]
        has_communication = any(keyword in requirement_content.lower() for keyword in comm_keywords)
        
        if has_communication:
            # Should mention templates or tracking
            template_keywords = ["template", "format", "tracking", "correlation"]
            has_templates = any(keyword in requirement_content.lower() for keyword in template_keywords)
            
            if not has_templates:
                violations.append(ComplianceViolation(
                    gr_id=gr_rule.gr_id,
                    violation_type="missing_communication_patterns",
                    severity=ViolationSeverity.MINOR.value,
                    description="Communication features should use templates and tracking",
                    location="communication",
                    suggested_fix="Include communication templates and correlation ID tracking",
                    auto_fixable=False,
                    confidence=0.6
                ))
        
        return {
            "passed": len(violations) == 0,
            "violations": violations,
            "score": 1.0 if len(violations) == 0 else 0.8
        }
    
    async def _validate_workflow(self, 
                               requirement_content: str,
                               validation_rule: Dict,
                               gr_rule: GRComplianceRule,
                               domain: str = None,
                               context: Dict = None) -> Dict:
        """Validate workflow compliance."""
        violations = []
        
        # Check for workflow mentions
        workflow_keywords = ["workflow", "process", "step", "trigger", "automation"]
        has_workflow = any(keyword in requirement_content.lower() for keyword in workflow_keywords)
        
        if has_workflow:
            # Should include error handling
            error_keywords = ["error", "exception", "failure", "retry", "rollback"]
            has_error_handling = any(keyword in requirement_content.lower() for keyword in error_keywords)
            
            if not has_error_handling:
                violations.append(ComplianceViolation(
                    gr_id=gr_rule.gr_id,
                    violation_type="missing_error_handling",
                    severity=ViolationSeverity.MINOR.value,
                    description="Workflow should include error handling",
                    location="workflow",
                    suggested_fix="Add error handling and retry mechanisms to workflow",
                    auto_fixable=False,
                    confidence=0.6
                ))
        
        return {
            "passed": len(violations) == 0,
            "violations": violations,
            "score": 1.0 if len(violations) == 0 else 0.9
        }
    
    async def _perform_heuristic_checks(self, 
                                      requirement_content: str,
                                      gr_rule: GRComplianceRule,
                                      domain: str = None) -> Dict:
        """Perform heuristic checks based on GR criteria."""
        violations = []
        
        # Check compliance criteria heuristically
        for criteria in gr_rule.compliance_criteria:
            criteria_lower = criteria.lower()
            content_lower = requirement_content.lower()
            
            # Simple keyword-based heuristic
            criteria_keywords = criteria_lower.split()
            keyword_matches = sum(1 for keyword in criteria_keywords if keyword in content_lower)
            
            if len(criteria_keywords) > 2 and keyword_matches == 0:
                violations.append(ComplianceViolation(
                    gr_id=gr_rule.gr_id,
                    violation_type="criteria_not_addressed",
                    severity=ViolationSeverity.WARNING.value,
                    description=f"Compliance criteria may not be addressed: {criteria}",
                    location="requirement_content",
                    suggested_fix=f"Consider addressing: {criteria}",
                    auto_fixable=False,
                    confidence=0.4
                ))
        
        return {
            "passed": len(violations) == 0,
            "violations": violations,
            "score": 1.0 if len(violations) == 0 else 0.9
        }
    
    def _calculate_overall_compliance_score(self, compliance_results: Dict) -> float:
        """Calculate overall compliance score."""
        if not compliance_results:
            return 0.0
        
        total_score = 0.0
        total_weight = 0.0
        
        for gr_id, result in compliance_results.items():
            gr_rule = self.gr_rules.get(gr_id)
            if gr_rule:
                # Weight by priority
                weight = {"critical": 1.0, "high": 0.8, "medium": 0.6, "low": 0.4}.get(gr_rule.priority, 0.6)
                total_score += result["compliance_score"] * weight
                total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def _determine_compliance_status(self, overall_score: float, violations: List[ComplianceViolation]) -> ComplianceStatus:
        """Determine overall compliance status."""
        critical_violations = [v for v in violations if v.severity == ViolationSeverity.CRITICAL.value]
        major_violations = [v for v in violations if v.severity == ViolationSeverity.MAJOR.value]
        
        if critical_violations:
            return ComplianceStatus.NON_COMPLIANT
        elif overall_score >= 0.95 and not major_violations:
            return ComplianceStatus.COMPLIANT
        elif overall_score >= 0.80:
            return ComplianceStatus.PARTIAL_COMPLIANT
        else:
            return ComplianceStatus.NON_COMPLIANT
    
    def _generate_recommendations(self, violations: List[ComplianceViolation], compliance_results: Dict) -> List[str]:
        """Generate recommendations based on compliance results."""
        recommendations = []
        
        # Group violations by type
        violation_groups = defaultdict(list)
        for violation in violations:
            violation_groups[violation.violation_type].append(violation)
        
        # Generate specific recommendations
        for violation_type, violations_list in violation_groups.items():
            if violation_type == "missing_audit_field":
                recommendations.append("Add required audit fields (created_at, updated_at, created_by, updated_by) to all table definitions")
            elif violation_type == "naming_convention_violation":
                recommendations.append("Update table and column names to follow snake_case convention")
            elif violation_type == "missing_universal_entity":
                recommendations.append("Use universal entity patterns for external integrations (address, phone, email, payment)")
            elif violation_type == "missing_communication_patterns":
                recommendations.append("Implement communication templates and correlation ID tracking")
            elif violation_type == "missing_error_handling":
                recommendations.append("Add comprehensive error handling and retry mechanisms")
            else:
                recommendations.append(f"Address {violation_type} violations")
        
        # Add general recommendations
        failed_grs = [gr_id for gr_id, result in compliance_results.items() if not result["compliant"]]
        if failed_grs:
            recommendations.append(f"Review Global Requirements: {', '.join(failed_grs)}")
        
        return recommendations
    
    def _generate_requirement_id(self, content: str) -> str:
        """Generate unique ID for a requirement."""
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:12]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"comp_{timestamp}_{content_hash}"
    
    def _generate_cache_key(self, requirement_content: str, domain: str = None, applicable_grs: List[str] = None) -> str:
        """Generate cache key for compliance check."""
        content_hash = hashlib.sha256(requirement_content.encode()).hexdigest()[:16]
        domain_suffix = f"_{domain}" if domain else ""
        grs_suffix = f"_{'_'.join(sorted(applicable_grs))}" if applicable_grs else ""
        return f"compliance_{content_hash}{domain_suffix}{grs_suffix}"
    
    def _get_cached_result(self, cache_key: str) -> Optional[ComplianceCheckResult]:
        """Get cached compliance result if available."""
        if not self.config.get("performance", {}).get("cache_enabled", True):
            return None
        
        if cache_key not in self.compliance_cache:
            return None
        
        cached_entry = self.compliance_cache[cache_key]
        cache_ttl_hours = self.config.get("performance", {}).get("cache_ttl_hours", 12)
        
        if datetime.now() - cached_entry["timestamp"] > timedelta(hours=cache_ttl_hours):
            del self.compliance_cache[cache_key]
            return None
        
        return cached_entry["result"]
    
    def _cache_result(self, cache_key: str, result: ComplianceCheckResult):
        """Cache compliance result."""
        if not self.config.get("performance", {}).get("cache_enabled", True):
            return
        
        max_cache_size = self.config.get("performance", {}).get("max_cache_size", 500)
        
        # Clean up old entries if cache is full
        if len(self.compliance_cache) >= max_cache_size:
            oldest_key = min(self.compliance_cache.keys(), 
                           key=lambda k: self.compliance_cache[k]["timestamp"])
            del self.compliance_cache[oldest_key]
        
        self.compliance_cache[cache_key] = {
            "result": result,
            "timestamp": datetime.now()
        }
    
    def get_compliance_statistics(self) -> Dict:
        """Get statistics about compliance checking."""
        return {
            "total_grs": len(self.gr_rules),
            "gr_rules_loaded": list(self.gr_rules.keys()),
            "validation_engines": list(self.validation_engines.keys()),
            "domain_rules": list(self.domain_specific_rules.keys()),
            "cache_size": len(self.compliance_cache),
            "performance_metrics": self.performance_metrics
        }

# Main execution and testing
if __name__ == "__main__":
    async def test_compliance_checker():
        """Test the GR Compliance Checker."""
        print("Testing GR Compliance Checker...")
        
        # Initialize compliance checker
        checker = GRComplianceChecker()
        
        # Test compliance statistics
        stats = checker.get_compliance_statistics()
        print(f"Compliance Statistics: {json.dumps(stats, indent=2)}")
        
        # Test compliance checking
        test_requirement = """
        Create a new driver management feature that allows producers to add drivers to quotes.
        The system should store driver information in a drivers table with the following fields:
        - driver_id (primary key)
        - license_number
        - first_name
        - last_name
        - date_of_birth
        - created_at
        - updated_at
        
        The system should validate driver license information through DCS integration
        and support email notifications for driver updates.
        """
        
        result = await checker.check_gr_compliance(
            requirement_content=test_requirement,
            domain="producer_portal",
            applicable_grs=["GR-02", "GR-19", "GR-41", "GR-44", "GR-52"]
        )
        
        print(f"Compliance Check Result: {json.dumps(asdict(result), indent=2, default=str)}")
        
        return checker
    
    # Run test if executed directly
    import asyncio
    asyncio.run(test_compliance_checker())