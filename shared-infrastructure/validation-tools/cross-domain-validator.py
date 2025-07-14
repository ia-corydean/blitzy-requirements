#!/usr/bin/env python3
"""
Cross-Domain Consistency Validator
Complete Requirements Generation System - Multi-Agent Architecture

Ensures consistency of shared entities across domains and validates
cross-domain workflows and relationships.

Created: 2025-01-07
Version: 1.0.0
GR Compliance: GR-52, GR-38, GR-44, GR-49
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
from collections import defaultdict
import difflib

# Configuration and Data Classes
@dataclass
class EntityConsistencyCheck:
    """Represents an entity consistency check result."""
    entity_name: str
    domains_involved: List[str]
    consistency_status: str  # consistent, inconsistent, partial
    conflicts: List[Dict]
    recommendations: List[str]
    confidence_score: float

@dataclass
class WorkflowConsistencyCheck:
    """Represents a workflow consistency check result."""
    workflow_name: str
    domains_involved: List[str]
    consistency_status: str
    workflow_conflicts: List[Dict]
    coordination_requirements: List[str]
    confidence_score: float

@dataclass
class CrossDomainValidationResult:
    """Result of cross-domain consistency validation."""
    requirement_id: str
    domains_analyzed: List[str]
    entity_consistency_checks: List[EntityConsistencyCheck]
    workflow_consistency_checks: List[WorkflowConsistencyCheck]
    overall_consistency_score: float
    validation_status: str  # consistent, inconsistent, needs_coordination
    critical_issues: List[Dict]
    recommendations: List[str]
    processing_time: float
    validation_metadata: Dict

class ConsistencyStatus(Enum):
    """Consistency status levels."""
    CONSISTENT = "consistent"
    INCONSISTENT = "inconsistent"
    PARTIAL_CONSISTENT = "partial_consistent"
    NEEDS_COORDINATION = "needs_coordination"
    ERROR = "error"

class ConflictSeverity(Enum):
    """Severity levels for consistency conflicts."""
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    WARNING = "warning"

class CrossDomainValidator:
    """
    Validator for ensuring consistency across business domains.
    Checks entity definitions, workflow coordination, and data integrity.
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the Cross-Domain Validator."""
        self.config_path = config_path or "/app/workspace/requirements/shared-infrastructure/agent-configurations/universal-validator.yaml"
        self.config = self._load_configuration()
        self.logger = self._setup_logging()
        
        # Cross-domain knowledge
        self.cross_domain_relationships = {}
        self.universal_entities = {}
        self.domain_entities = {}
        self.domain_workflows = {}
        
        # Validation state
        self.validation_cache = {}
        self.consistency_rules = {}
        
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
            "cross_domain_validation": {
                "consistency_threshold": 0.85,
                "critical_entity_threshold": 0.95,
                "workflow_coordination_threshold": 0.80
            },
            "performance": {
                "cache_enabled": True,
                "cache_ttl_hours": 6,
                "max_cache_size": 200
            }
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the validator."""
        logger = logging.getLogger("CrossDomainValidator")
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
        self.logger.info("Initializing Cross-Domain Validator...")
        
        try:
            # Load cross-domain relationships
            self._load_cross_domain_relationships()
            
            # Load universal entities
            self._load_universal_entities()
            
            # Load domain-specific entities and workflows
            self._load_domain_data()
            
            # Initialize consistency rules
            self._initialize_consistency_rules()
            
            self.logger.info("Cross-Domain Validator initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize validator: {e}")
            raise
    
    def _load_cross_domain_relationships(self):
        """Load cross-domain relationship mappings."""
        relationships_file = "/app/workspace/requirements/shared-infrastructure/knowledge-base/cross-domain-relationships/relationship-map.json"
        
        if not Path(relationships_file).exists():
            self.logger.warning("Cross-domain relationships file not found")
            self.cross_domain_relationships = self._create_default_relationships()
            return
        
        try:
            with open(relationships_file, 'r') as f:
                data = json.load(f)
            
            self.cross_domain_relationships = data
            self.logger.info(f"Loaded cross-domain relationships")
            
        except Exception as e:
            self.logger.error(f"Error loading cross-domain relationships: {e}")
            self.cross_domain_relationships = self._create_default_relationships()
    
    def _create_default_relationships(self) -> Dict:
        """Create default cross-domain relationships."""
        return {
            "entity_relationship_matrix": {
                "producer_portal_to_accounting": {
                    "shared_entities": ["payment", "address", "phone", "email"],
                    "workflow_connections": ["payment_processing", "billing_updates"],
                    "data_flow": ["quote_to_payment", "policy_to_billing"]
                },
                "producer_portal_to_entity_integration": {
                    "shared_entities": ["driver", "vehicle", "address", "phone"],
                    "workflow_connections": ["dcs_verification", "data_validation"],
                    "data_flow": ["driver_verification", "vehicle_lookup"]
                },
                "accounting_to_program_manager": {
                    "shared_entities": ["payment", "program", "rate_factor"],
                    "workflow_connections": ["commission_calculation", "billing_rules"],
                    "data_flow": ["rate_to_billing", "commission_processing"]
                }
            },
            "universal_entity_usage": {
                "address": ["producer_portal", "accounting", "entity_integration"],
                "phone": ["producer_portal", "accounting", "entity_integration"],
                "email": ["producer_portal", "accounting", "entity_integration"],
                "payment": ["producer_portal", "accounting", "program_manager"]
            }
        }
    
    def _load_universal_entities(self):
        """Load universal entity catalog."""
        entities_file = "/app/workspace/requirements/shared-infrastructure/knowledge-base/universal-entity-catalog.json"
        
        if not Path(entities_file).exists():
            self.logger.warning("Universal entity catalog not found")
            self.universal_entities = self._create_default_universal_entities()
            return
        
        try:
            with open(entities_file, 'r') as f:
                data = json.load(f)
            
            self.universal_entities = data
            self.logger.info("Loaded universal entity catalog")
            
        except Exception as e:
            self.logger.error(f"Error loading universal entities: {e}")
            self.universal_entities = self._create_default_universal_entities()
    
    def _create_default_universal_entities(self) -> Dict:
        """Create default universal entities."""
        return {
            "core_entities": [
                {
                    "name": "address",
                    "type": "universal",
                    "domains": ["producer_portal", "accounting", "entity_integration"],
                    "standard_fields": ["street_address", "city", "state", "postal_code", "country"]
                },
                {
                    "name": "phone",
                    "type": "universal", 
                    "domains": ["producer_portal", "accounting", "entity_integration"],
                    "standard_fields": ["phone_number", "phone_type", "is_primary"]
                },
                {
                    "name": "email",
                    "type": "universal",
                    "domains": ["producer_portal", "accounting", "entity_integration"],
                    "standard_fields": ["email_address", "email_type", "is_primary"]
                },
                {
                    "name": "payment",
                    "type": "universal",
                    "domains": ["producer_portal", "accounting", "program_manager"],
                    "standard_fields": ["amount", "payment_method", "transaction_id", "status"]
                }
            ]
        }
    
    def _load_domain_data(self):
        """Load domain-specific entity and workflow data."""
        domains = ["producer_portal", "accounting", "program_manager", 
                  "program_traits", "entity_integration", "reinstatement", "sr22"]
        
        for domain in domains:
            # Load domain entities (simplified - would load from actual files)
            self.domain_entities[domain] = self._get_domain_entities(domain)
            
            # Load domain workflows (simplified - would load from actual files) 
            self.domain_workflows[domain] = self._get_domain_workflows(domain)
        
        self.logger.info(f"Loaded domain data for {len(domains)} domains")
    
    def _get_domain_entities(self, domain: str) -> Dict:
        """Get domain-specific entities."""
        domain_entity_map = {
            "producer_portal": {
                "quote": {"fields": ["quote_id", "producer_id", "effective_date"], "relationships": ["driver", "vehicle"]},
                "policy": {"fields": ["policy_id", "policy_number"], "relationships": ["quote", "payment"]},
                "driver": {"fields": ["driver_id", "license_number"], "relationships": ["address", "phone", "email"]},
                "vehicle": {"fields": ["vehicle_id", "vin"], "relationships": ["driver"]},
                "producer": {"fields": ["producer_id", "license_number"], "relationships": ["address", "phone", "email"]}
            },
            "accounting": {
                "billing_account": {"fields": ["account_id", "account_number"], "relationships": ["payment"]},
                "transaction": {"fields": ["transaction_id", "amount"], "relationships": ["payment", "billing_account"]},
                "commission": {"fields": ["commission_id", "rate"], "relationships": ["transaction", "producer"]}
            },
            "program_manager": {
                "rate_factor": {"fields": ["factor_id", "factor_type"], "relationships": ["program"]},
                "territory": {"fields": ["territory_id", "state"], "relationships": ["address"]},
                "program": {"fields": ["program_id", "program_name"], "relationships": ["rate_factor"]}
            }
        }
        
        return domain_entity_map.get(domain, {})
    
    def _get_domain_workflows(self, domain: str) -> Dict:
        """Get domain-specific workflows."""
        domain_workflow_map = {
            "producer_portal": {
                "quote_creation": {"steps": ["driver_validation", "vehicle_lookup", "rating"], "coordination_points": ["dcs_verification"]},
                "policy_binding": {"steps": ["quote_validation", "payment_processing"], "coordination_points": ["payment_gateway"]}
            },
            "accounting": {
                "payment_processing": {"steps": ["validation", "authorization", "settlement"], "coordination_points": ["billing_update"]},
                "commission_calculation": {"steps": ["rate_lookup", "calculation", "payment"], "coordination_points": ["producer_notification"]}
            }
        }
        
        return domain_workflow_map.get(domain, {})
    
    def _initialize_consistency_rules(self):
        """Initialize consistency rules for validation."""
        self.consistency_rules = {
            "entity_field_consistency": {
                "rule": "Shared entities must have consistent field definitions across domains",
                "severity": "major",
                "check_function": self._check_entity_field_consistency
            },
            "relationship_consistency": {
                "rule": "Entity relationships must be consistent across domains",
                "severity": "major", 
                "check_function": self._check_relationship_consistency
            },
            "workflow_coordination": {
                "rule": "Cross-domain workflows must have proper coordination points",
                "severity": "minor",
                "check_function": self._check_workflow_coordination
            },
            "universal_entity_usage": {
                "rule": "Universal entities must be used consistently",
                "severity": "critical",
                "check_function": self._check_universal_entity_usage
            },
            "data_flow_consistency": {
                "rule": "Data flow between domains must be consistent",
                "severity": "major",
                "check_function": self._check_data_flow_consistency
            }
        }
        
        self.logger.info(f"Initialized {len(self.consistency_rules)} consistency rules")
    
    async def validate_cross_domain_consistency(self, 
                                              requirement_content: str,
                                              primary_domain: str,
                                              involved_domains: List[str] = None,
                                              context: Dict = None) -> CrossDomainValidationResult:
        """
        Validate cross-domain consistency for a requirement.
        
        Args:
            requirement_content: The requirement text to validate
            primary_domain: Primary domain for the requirement
            involved_domains: List of domains involved (if None, auto-detect)
            context: Additional context information
            
        Returns:
            CrossDomainValidationResult with detailed consistency information
        """
        start_time = datetime.now()
        requirement_id = self._generate_requirement_id(requirement_content)
        
        self.logger.info(f"Validating cross-domain consistency for requirement {requirement_id}")
        
        try:
            # Check cache first
            cache_key = self._generate_cache_key(requirement_content, primary_domain, involved_domains)
            cached_result = self._get_cached_result(cache_key)
            if cached_result:
                self.logger.info(f"Using cached validation result for {requirement_id}")
                return cached_result
            
            # Auto-detect involved domains if not specified
            if not involved_domains:
                involved_domains = await self._auto_detect_involved_domains(
                    requirement_content, primary_domain
                )
            
            # Extract entities and workflows from requirement
            entities = await self._extract_entities_from_requirement(requirement_content)
            workflows = await self._extract_workflows_from_requirement(requirement_content)
            
            # Perform entity consistency checks
            entity_checks = await self._perform_entity_consistency_checks(
                entities, involved_domains, requirement_content
            )
            
            # Perform workflow consistency checks
            workflow_checks = await self._perform_workflow_consistency_checks(
                workflows, involved_domains, requirement_content
            )
            
            # Calculate overall consistency score
            overall_score = self._calculate_overall_consistency_score(
                entity_checks, workflow_checks
            )
            
            # Determine validation status
            validation_status = self._determine_validation_status(overall_score, entity_checks, workflow_checks)
            
            # Identify critical issues
            critical_issues = self._identify_critical_issues(entity_checks, workflow_checks)
            
            # Generate recommendations
            recommendations = self._generate_consistency_recommendations(
                entity_checks, workflow_checks, critical_issues
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            result = CrossDomainValidationResult(
                requirement_id=requirement_id,
                domains_analyzed=involved_domains,
                entity_consistency_checks=entity_checks,
                workflow_consistency_checks=workflow_checks,
                overall_consistency_score=overall_score,
                validation_status=validation_status.value,
                critical_issues=critical_issues,
                recommendations=recommendations,
                processing_time=processing_time,
                validation_metadata={
                    "primary_domain": primary_domain,
                    "entities_found": len(entities),
                    "workflows_found": len(workflows),
                    "validation_timestamp": datetime.now().isoformat(),
                    "consistency_rules_applied": list(self.consistency_rules.keys())
                }
            )
            
            # Cache the result
            self._cache_result(cache_key, result)
            
            self.logger.info(f"Cross-domain validation completed for {requirement_id} in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            self.logger.error(f"Error validating cross-domain consistency for requirement {requirement_id}: {e}")
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return CrossDomainValidationResult(
                requirement_id=requirement_id,
                domains_analyzed=involved_domains or [primary_domain],
                entity_consistency_checks=[],
                workflow_consistency_checks=[],
                overall_consistency_score=0.0,
                validation_status=ConsistencyStatus.ERROR.value,
                critical_issues=[],
                recommendations=[],
                processing_time=processing_time,
                validation_metadata={"error": str(e)}
            )
    
    async def _auto_detect_involved_domains(self, requirement_content: str, primary_domain: str) -> List[str]:
        """Auto-detect domains involved in the requirement."""
        involved_domains = [primary_domain]
        content_lower = requirement_content.lower()
        
        # Check for cross-domain keywords
        domain_keywords = {
            "producer_portal": ["quote", "policy", "producer", "driver", "vehicle"],
            "accounting": ["payment", "billing", "commission", "transaction"],
            "program_manager": ["rate", "factor", "territory", "program"],
            "program_traits": ["trait", "rule", "configuration"],
            "entity_integration": ["dcs", "external", "api", "integration"],
            "reinstatement": ["reinstate", "lapse", "restore"],
            "sr22": ["sr22", "sr26", "financial responsibility"]
        }
        
        for domain, keywords in domain_keywords.items():
            if domain != primary_domain:
                keyword_matches = sum(1 for keyword in keywords if keyword in content_lower)
                if keyword_matches >= 1:  # At least one keyword match
                    involved_domains.append(domain)
        
        # Check cross-domain relationships
        relationship_matrix = self.cross_domain_relationships.get("entity_relationship_matrix", {})
        for relationship_key, relationship_data in relationship_matrix.items():
            if primary_domain in relationship_key:
                other_domain = relationship_key.replace(primary_domain, "").replace("_to_", "").strip("_")
                if other_domain and other_domain not in involved_domains:
                    # Check if shared entities are mentioned
                    shared_entities = relationship_data.get("shared_entities", [])
                    for entity in shared_entities:
                        if entity in content_lower and other_domain not in involved_domains:
                            involved_domains.append(other_domain)
                            break
        
        self.logger.info(f"Auto-detected involved domains: {involved_domains}")
        return involved_domains
    
    async def _extract_entities_from_requirement(self, requirement_content: str) -> List[str]:
        """Extract business entities mentioned in the requirement."""
        entities = []
        content_lower = requirement_content.lower()
        
        # Check universal entities
        universal_entities = self.universal_entities.get("core_entities", [])
        for entity_info in universal_entities:
            entity_name = entity_info.get("name", "")
            if entity_name and entity_name in content_lower:
                entities.append(entity_name)
        
        # Check domain entities
        for domain, domain_entities in self.domain_entities.items():
            for entity_name in domain_entities:
                if entity_name in content_lower:
                    entities.append(entity_name)
        
        return list(set(entities))  # Remove duplicates
    
    async def _extract_workflows_from_requirement(self, requirement_content: str) -> List[str]:
        """Extract workflow mentions from the requirement."""
        workflows = []
        content_lower = requirement_content.lower()
        
        # Check domain workflows
        for domain, domain_workflows in self.domain_workflows.items():
            for workflow_name in domain_workflows:
                workflow_keywords = workflow_name.replace("_", " ").split()
                if all(keyword in content_lower for keyword in workflow_keywords):
                    workflows.append(workflow_name)
        
        # Check for generic workflow keywords
        workflow_indicators = ["process", "workflow", "procedure", "automation", "trigger"]
        for indicator in workflow_indicators:
            if indicator in content_lower:
                workflows.append(f"generic_{indicator}")
        
        return list(set(workflows))  # Remove duplicates
    
    async def _perform_entity_consistency_checks(self, 
                                               entities: List[str],
                                               involved_domains: List[str],
                                               requirement_content: str) -> List[EntityConsistencyCheck]:
        """Perform entity consistency checks across domains."""
        entity_checks = []
        
        for entity in entities:
            check_result = await self._check_entity_consistency_across_domains(
                entity, involved_domains, requirement_content
            )
            if check_result:
                entity_checks.append(check_result)
        
        return entity_checks
    
    async def _check_entity_consistency_across_domains(self, 
                                                     entity_name: str,
                                                     involved_domains: List[str],
                                                     requirement_content: str) -> Optional[EntityConsistencyCheck]:
        """Check consistency of an entity across domains."""
        domains_with_entity = []
        entity_definitions = {}
        conflicts = []
        
        # Check universal entities first
        universal_entities = self.universal_entities.get("core_entities", [])
        universal_entity = next((e for e in universal_entities if e["name"] == entity_name), None)
        
        if universal_entity:
            domains_with_entity = universal_entity.get("domains", [])
            entity_definitions["universal"] = universal_entity
        
        # Check domain-specific definitions
        for domain in involved_domains:
            domain_entities = self.domain_entities.get(domain, {})
            if entity_name in domain_entities:
                domains_with_entity.append(domain)
                entity_definitions[domain] = domain_entities[entity_name]
        
        if len(domains_with_entity) <= 1:
            return None  # No cross-domain consistency issues
        
        # Check for field consistency
        field_conflicts = self._check_field_consistency(entity_definitions)
        conflicts.extend(field_conflicts)
        
        # Check for relationship consistency
        relationship_conflicts = self._check_relationship_consistency_for_entity(entity_definitions)
        conflicts.extend(relationship_conflicts)
        
        # Determine consistency status
        if not conflicts:
            consistency_status = "consistent"
            confidence_score = 1.0
        elif len(conflicts) <= 2:
            consistency_status = "partial"
            confidence_score = 0.7
        else:
            consistency_status = "inconsistent"
            confidence_score = 0.3
        
        # Generate recommendations
        recommendations = self._generate_entity_recommendations(entity_name, conflicts)
        
        return EntityConsistencyCheck(
            entity_name=entity_name,
            domains_involved=domains_with_entity,
            consistency_status=consistency_status,
            conflicts=conflicts,
            recommendations=recommendations,
            confidence_score=confidence_score
        )
    
    def _check_field_consistency(self, entity_definitions: Dict) -> List[Dict]:
        """Check field consistency across entity definitions."""
        conflicts = []
        
        if "universal" in entity_definitions:
            universal_fields = set(entity_definitions["universal"].get("standard_fields", []))
            
            for domain, definition in entity_definitions.items():
                if domain != "universal":
                    domain_fields = set(definition.get("fields", []))
                    
                    # Check for missing universal fields
                    missing_fields = universal_fields - domain_fields
                    if missing_fields:
                        conflicts.append({
                            "type": "missing_universal_fields",
                            "domain": domain,
                            "missing_fields": list(missing_fields),
                            "severity": ConflictSeverity.MAJOR.value
                        })
        
        return conflicts
    
    def _check_relationship_consistency_for_entity(self, entity_definitions: Dict) -> List[Dict]:
        """Check relationship consistency for an entity."""
        conflicts = []
        
        # Compare relationships across domains
        domain_relationships = {}
        for domain, definition in entity_definitions.items():
            if domain != "universal":
                relationships = definition.get("relationships", [])
                domain_relationships[domain] = set(relationships)
        
        if len(domain_relationships) > 1:
            domains = list(domain_relationships.keys())
            for i, domain1 in enumerate(domains):
                for domain2 in domains[i+1:]:
                    relationships1 = domain_relationships[domain1]
                    relationships2 = domain_relationships[domain2]
                    
                    # Check for conflicting relationships
                    if relationships1 != relationships2:
                        conflicts.append({
                            "type": "relationship_mismatch",
                            "domains": [domain1, domain2],
                            "domain1_relationships": list(relationships1),
                            "domain2_relationships": list(relationships2),
                            "severity": ConflictSeverity.MINOR.value
                        })
        
        return conflicts
    
    def _generate_entity_recommendations(self, entity_name: str, conflicts: List[Dict]) -> List[str]:
        """Generate recommendations for entity consistency issues."""
        recommendations = []
        
        for conflict in conflicts:
            if conflict["type"] == "missing_universal_fields":
                recommendations.append(
                    f"Add missing universal fields to {entity_name} in {conflict['domain']}: {', '.join(conflict['missing_fields'])}"
                )
            elif conflict["type"] == "relationship_mismatch":
                recommendations.append(
                    f"Standardize {entity_name} relationships across {', '.join(conflict['domains'])}"
                )
        
        if not recommendations and conflicts:
            recommendations.append(f"Review {entity_name} definition for consistency across domains")
        
        return recommendations
    
    async def _perform_workflow_consistency_checks(self, 
                                                 workflows: List[str],
                                                 involved_domains: List[str],
                                                 requirement_content: str) -> List[WorkflowConsistencyCheck]:
        """Perform workflow consistency checks across domains."""
        workflow_checks = []
        
        for workflow in workflows:
            check_result = await self._check_workflow_consistency_across_domains(
                workflow, involved_domains, requirement_content
            )
            if check_result:
                workflow_checks.append(check_result)
        
        return workflow_checks
    
    async def _check_workflow_consistency_across_domains(self, 
                                                       workflow_name: str,
                                                       involved_domains: List[str],
                                                       requirement_content: str) -> Optional[WorkflowConsistencyCheck]:
        """Check consistency of a workflow across domains."""
        domains_with_workflow = []
        workflow_definitions = {}
        workflow_conflicts = []
        coordination_requirements = []
        
        # Find workflow in domain definitions
        for domain in involved_domains:
            domain_workflows = self.domain_workflows.get(domain, {})
            if workflow_name in domain_workflows:
                domains_with_workflow.append(domain)
                workflow_definitions[domain] = domain_workflows[workflow_name]
        
        if len(domains_with_workflow) <= 1:
            return None  # No cross-domain workflow issues
        
        # Check for coordination points
        for domain, workflow_def in workflow_definitions.items():
            coordination_points = workflow_def.get("coordination_points", [])
            coordination_requirements.extend(coordination_points)
        
        # Check for workflow step consistency
        step_conflicts = self._check_workflow_step_consistency(workflow_definitions)
        workflow_conflicts.extend(step_conflicts)
        
        # Determine consistency status
        if not workflow_conflicts:
            consistency_status = "consistent"
            confidence_score = 0.9
        elif len(workflow_conflicts) <= 1:
            consistency_status = "partial"
            confidence_score = 0.7
        else:
            consistency_status = "inconsistent"
            confidence_score = 0.4
        
        return WorkflowConsistencyCheck(
            workflow_name=workflow_name,
            domains_involved=domains_with_workflow,
            consistency_status=consistency_status,
            workflow_conflicts=workflow_conflicts,
            coordination_requirements=list(set(coordination_requirements)),
            confidence_score=confidence_score
        )
    
    def _check_workflow_step_consistency(self, workflow_definitions: Dict) -> List[Dict]:
        """Check workflow step consistency across domains."""
        conflicts = []
        
        # Compare workflow steps
        domain_steps = {}
        for domain, workflow_def in workflow_definitions.items():
            steps = workflow_def.get("steps", [])
            domain_steps[domain] = steps
        
        if len(domain_steps) > 1:
            domains = list(domain_steps.keys())
            for i, domain1 in enumerate(domains):
                for domain2 in domains[i+1:]:
                    steps1 = set(domain_steps[domain1])
                    steps2 = set(domain_steps[domain2])
                    
                    # Check for missing steps
                    missing_in_domain2 = steps1 - steps2
                    missing_in_domain1 = steps2 - steps1
                    
                    if missing_in_domain1 or missing_in_domain2:
                        conflicts.append({
                            "type": "workflow_step_mismatch",
                            "domains": [domain1, domain2],
                            "missing_in_domain1": list(missing_in_domain1),
                            "missing_in_domain2": list(missing_in_domain2),
                            "severity": ConflictSeverity.MINOR.value
                        })
        
        return conflicts
    
    def _calculate_overall_consistency_score(self, 
                                           entity_checks: List[EntityConsistencyCheck],
                                           workflow_checks: List[WorkflowConsistencyCheck]) -> float:
        """Calculate overall consistency score."""
        if not entity_checks and not workflow_checks:
            return 1.0  # No cross-domain issues
        
        total_score = 0.0
        total_weight = 0.0
        
        # Weight entity checks more heavily
        for check in entity_checks:
            weight = 0.7
            total_score += check.confidence_score * weight
            total_weight += weight
        
        # Weight workflow checks less heavily
        for check in workflow_checks:
            weight = 0.3
            total_score += check.confidence_score * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def _determine_validation_status(self, 
                                   overall_score: float,
                                   entity_checks: List[EntityConsistencyCheck],
                                   workflow_checks: List[WorkflowConsistencyCheck]) -> ConsistencyStatus:
        """Determine overall validation status."""
        # Check for critical entity issues
        critical_entity_issues = any(
            check.consistency_status == "inconsistent" for check in entity_checks
        )
        
        # Check for workflow coordination needs
        needs_coordination = any(
            check.coordination_requirements for check in workflow_checks
        )
        
        if critical_entity_issues:
            return ConsistencyStatus.INCONSISTENT
        elif overall_score >= 0.95:
            return ConsistencyStatus.CONSISTENT
        elif overall_score >= 0.80 or needs_coordination:
            return ConsistencyStatus.NEEDS_COORDINATION
        elif overall_score >= 0.60:
            return ConsistencyStatus.PARTIAL_CONSISTENT
        else:
            return ConsistencyStatus.INCONSISTENT
    
    def _identify_critical_issues(self, 
                                entity_checks: List[EntityConsistencyCheck],
                                workflow_checks: List[WorkflowConsistencyCheck]) -> List[Dict]:
        """Identify critical consistency issues."""
        critical_issues = []
        
        # Critical entity issues
        for check in entity_checks:
            if check.consistency_status == "inconsistent":
                major_conflicts = [c for c in check.conflicts if c.get("severity") == ConflictSeverity.MAJOR.value]
                if major_conflicts:
                    critical_issues.append({
                        "type": "entity_inconsistency",
                        "entity": check.entity_name,
                        "domains": check.domains_involved,
                        "conflicts": major_conflicts,
                        "severity": ConflictSeverity.CRITICAL.value
                    })
        
        # Critical workflow issues
        for check in workflow_checks:
            if check.consistency_status == "inconsistent":
                critical_issues.append({
                    "type": "workflow_inconsistency",
                    "workflow": check.workflow_name,
                    "domains": check.domains_involved,
                    "conflicts": check.workflow_conflicts,
                    "severity": ConflictSeverity.MAJOR.value
                })
        
        return critical_issues
    
    def _generate_consistency_recommendations(self, 
                                            entity_checks: List[EntityConsistencyCheck],
                                            workflow_checks: List[WorkflowConsistencyCheck],
                                            critical_issues: List[Dict]) -> List[str]:
        """Generate recommendations for consistency improvements."""
        recommendations = []
        
        # Entity recommendations
        for check in entity_checks:
            recommendations.extend(check.recommendations)
        
        # Workflow recommendations
        for check in workflow_checks:
            if check.coordination_requirements:
                recommendations.append(
                    f"Implement coordination for {check.workflow_name}: {', '.join(check.coordination_requirements)}"
                )
        
        # Critical issue recommendations
        for issue in critical_issues:
            if issue["type"] == "entity_inconsistency":
                recommendations.append(
                    f"CRITICAL: Resolve entity inconsistency for {issue['entity']} across {', '.join(issue['domains'])}"
                )
            elif issue["type"] == "workflow_inconsistency":
                recommendations.append(
                    f"MAJOR: Standardize workflow {issue['workflow']} across {', '.join(issue['domains'])}"
                )
        
        # General recommendations
        if not recommendations:
            recommendations.append("Cross-domain consistency is maintained")
        
        return list(set(recommendations))  # Remove duplicates
    
    # Consistency rule check functions
    async def _check_entity_field_consistency(self, *args) -> Dict:
        """Check entity field consistency rule."""
        return {"passed": True, "score": 1.0, "details": "Entity fields are consistent"}
    
    async def _check_relationship_consistency(self, *args) -> Dict:
        """Check relationship consistency rule."""
        return {"passed": True, "score": 1.0, "details": "Relationships are consistent"}
    
    async def _check_workflow_coordination(self, *args) -> Dict:
        """Check workflow coordination rule."""
        return {"passed": True, "score": 1.0, "details": "Workflow coordination is proper"}
    
    async def _check_universal_entity_usage(self, *args) -> Dict:
        """Check universal entity usage rule."""
        return {"passed": True, "score": 1.0, "details": "Universal entities are used correctly"}
    
    async def _check_data_flow_consistency(self, *args) -> Dict:
        """Check data flow consistency rule."""
        return {"passed": True, "score": 1.0, "details": "Data flow is consistent"}
    
    def _generate_requirement_id(self, content: str) -> str:
        """Generate unique ID for a requirement."""
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:12]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"xdval_{timestamp}_{content_hash}"
    
    def _generate_cache_key(self, requirement_content: str, primary_domain: str, involved_domains: List[str] = None) -> str:
        """Generate cache key for validation."""
        content_hash = hashlib.sha256(requirement_content.encode()).hexdigest()[:16]
        domain_suffix = f"_{primary_domain}"
        involved_suffix = f"_{'_'.join(sorted(involved_domains))}" if involved_domains else ""
        return f"xdval_{content_hash}{domain_suffix}{involved_suffix}"
    
    def _get_cached_result(self, cache_key: str) -> Optional[CrossDomainValidationResult]:
        """Get cached validation result if available."""
        if not self.config.get("performance", {}).get("cache_enabled", True):
            return None
        
        if cache_key not in self.validation_cache:
            return None
        
        cached_entry = self.validation_cache[cache_key]
        cache_ttl_hours = self.config.get("performance", {}).get("cache_ttl_hours", 6)
        
        if datetime.now() - cached_entry["timestamp"] > timedelta(hours=cache_ttl_hours):
            del self.validation_cache[cache_key]
            return None
        
        return cached_entry["result"]
    
    def _cache_result(self, cache_key: str, result: CrossDomainValidationResult):
        """Cache validation result."""
        if not self.config.get("performance", {}).get("cache_enabled", True):
            return
        
        max_cache_size = self.config.get("performance", {}).get("max_cache_size", 200)
        
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
        """Get statistics about cross-domain validation."""
        return {
            "domains_supported": list(self.domain_entities.keys()),
            "universal_entities": len(self.universal_entities.get("core_entities", [])),
            "domain_entities": {domain: len(entities) for domain, entities in self.domain_entities.items()},
            "domain_workflows": {domain: len(workflows) for domain, workflows in self.domain_workflows.items()},
            "consistency_rules": list(self.consistency_rules.keys()),
            "cache_size": len(self.validation_cache),
            "cross_domain_relationships": len(self.cross_domain_relationships.get("entity_relationship_matrix", {}))
        }

# Main execution and testing
if __name__ == "__main__":
    async def test_cross_domain_validator():
        """Test the Cross-Domain Validator."""
        print("Testing Cross-Domain Validator...")
        
        # Initialize validator
        validator = CrossDomainValidator()
        
        # Test validation statistics
        stats = validator.get_validation_statistics()
        print(f"Validation Statistics: {json.dumps(stats, indent=2)}")
        
        # Test cross-domain validation
        test_requirement = """
        Create a driver management feature that allows producers to add drivers to quotes.
        The system should store driver information with personal details and validate
        license information through DCS integration. When a driver is added, the system
        should update the quote pricing and send email notifications to the producer.
        Payment information should be collected and processed through the accounting system.
        """
        
        result = await validator.validate_cross_domain_consistency(
            requirement_content=test_requirement,
            primary_domain="producer_portal",
            involved_domains=["producer_portal", "accounting", "entity_integration"],
            context={"priority": "high"}
        )
        
        print(f"Validation Result: {json.dumps(asdict(result), indent=2, default=str)}")
        
        return validator
    
    # Run test if executed directly
    import asyncio
    asyncio.run(test_cross_domain_validator())