#!/usr/bin/env python3
"""
System Orchestrator Intelligence Engine
Complete Requirements Generation System - Multi-Agent Architecture

Handles cross-domain coordination, pattern recognition, and Global Requirements mastery.
This is the core intelligence engine that orchestrates all domain specialists and
manages the overall requirements processing workflow.

Created: 2025-01-07
Version: 1.0.0
GR Compliance: GR-38, GR-44, GR-52, GR-49
"""

import json
import yaml
import logging
import asyncio
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
from dataclasses import dataclass, asdict
from enum import Enum
import concurrent.futures
import time

# Configuration and Data Classes
@dataclass
class RequirementContext:
    """Context information for a requirement being processed."""
    requirement_id: str
    domain: str
    priority: str
    content: str
    entities_identified: List[str]
    global_requirements: List[str]
    cross_domain_relationships: List[str]
    confidence_score: float
    processing_start_time: datetime
    assigned_agents: List[str]

@dataclass
class ProcessingResult:
    """Result of requirement processing."""
    requirement_id: str
    success: bool
    processing_time: float
    pattern_matches: List[Dict]
    gr_compliance: Dict[str, bool]
    cross_domain_validations: List[Dict]
    generated_artifacts: List[str]
    confidence_score: float
    error_messages: List[str]

class ProcessingMode(Enum):
    """Available processing modes."""
    INDIVIDUAL = "individual_requirement"
    BATCH = "batch_processing"
    CROSS_DOMAIN = "cross_domain_workflow"
    EMERGENCY = "emergency_processing"

class SystemOrchestratorEngine:
    """
    Core intelligence engine for multi-agent requirements processing orchestration.
    
    This engine coordinates all domain specialists, manages shared context,
    handles pattern recognition, and ensures Global Requirements compliance
    across all business domains.
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the System Orchestrator Engine."""
        self.config_path = config_path or "/app/workspace/requirements/shared-infrastructure/agent-configurations/system-orchestrator.yaml"
        self.config = self._load_configuration()
        self.logger = self._setup_logging()
        
        # Core components
        self.knowledge_base = None
        self.domain_specialists = {}
        self.universal_validator = None
        self.intelligence_engines = {}
        self.shared_context = None
        
        # Processing state
        self.active_workflows = {}
        self.processing_queues = {}
        self.performance_metrics = {}
        
        # Initialize system
        self._initialize_system()
    
    def _load_configuration(self) -> Dict:
        """Load orchestrator configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Return default configuration if config file is not available."""
        return {
            "agent_config": {
                "agent_id": "system-orchestrator",
                "capabilities": {
                    "multi_domain_processing": True,
                    "pattern_recognition": True,
                    "global_requirements_validation": True
                }
            },
            "performance": {
                "max_concurrent_domains": 7,
                "processing_timeout": "30 minutes",
                "coordination_overhead_target": "< 5%"
            }
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the orchestrator engine."""
        logger = logging.getLogger("SystemOrchestrator")
        logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def _initialize_system(self):
        """Initialize all system components."""
        self.logger.info("Initializing System Orchestrator Engine...")
        
        try:
            # Load knowledge base
            self._load_knowledge_base()
            
            # Initialize domain specialists
            self._initialize_domain_specialists()
            
            # Initialize intelligence engines
            self._initialize_intelligence_engines()
            
            # Initialize shared context
            self._initialize_shared_context()
            
            # Initialize processing queues
            self._initialize_processing_queues()
            
            self.logger.info("System Orchestrator Engine initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize system: {e}")
            raise
    
    def _load_knowledge_base(self):
        """Load the complete knowledge base."""
        kb_config = self.config.get("knowledge_base", {})
        
        self.knowledge_base = {
            "universal_entities": self._load_json_file(
                kb_config.get("universal_entity_catalog")
            ),
            "global_requirements": self._load_json_file(
                kb_config.get("global_requirements_index")
            ),
            "cross_domain_relationships": self._load_json_file(
                kb_config.get("cross_domain_relationships")
            ),
            "architectural_decisions": self._load_json_file(
                kb_config.get("architectural_decisions")
            )
        }
        
        self.logger.info("Knowledge base loaded successfully")
    
    def _load_json_file(self, file_path: str) -> Dict:
        """Load and parse a JSON file."""
        if not file_path or not Path(file_path).exists():
            self.logger.warning(f"File not found: {file_path}")
            return {}
        
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading {file_path}: {e}")
            return {}
    
    def _initialize_domain_specialists(self):
        """Initialize connections to all domain specialist agents."""
        specialists_config = self.config.get("domain_specialists", {})
        
        for domain, config in specialists_config.items():
            self.domain_specialists[domain] = {
                "agent_id": config.get("agent_id"),
                "config_file": config.get("config_file"),
                "priority": config.get("priority", "medium"),
                "specializations": config.get("specializations", []),
                "status": "initialized",
                "last_ping": datetime.now()
            }
        
        self.logger.info(f"Initialized {len(self.domain_specialists)} domain specialists")
    
    def _initialize_intelligence_engines(self):
        """Initialize all intelligence engines."""
        engines_config = self.config.get("intelligence_engines", {})
        
        for engine_name, config in engines_config.items():
            self.intelligence_engines[engine_name] = {
                "engine_file": config.get("engine_file"),
                "enabled": config.get("enabled", True),
                "confidence_threshold": config.get("confidence_threshold", 0.8),
                "status": "initialized"
            }
        
        self.logger.info(f"Initialized {len(self.intelligence_engines)} intelligence engines")
    
    def _initialize_shared_context(self):
        """Initialize shared context management system."""
        context_config = self.config.get("shared_context", {})
        
        self.shared_context = {
            "entities": {},
            "relationships": {},
            "patterns": {},
            "workflows": {},
            "performance_data": {},
            "sync_enabled": context_config.get("real_time_sync", True),
            "last_sync": datetime.now()
        }
        
        self.logger.info("Shared context initialized")
    
    def _initialize_processing_queues(self):
        """Initialize processing queue management."""
        queue_config = self.config.get("queue_configuration", {})
        
        # Multi-domain queue
        multi_domain_path = queue_config.get("multi_domain_queue")
        if multi_domain_path:
            self.processing_queues["multi_domain"] = {
                "path": multi_domain_path,
                "current_size": 0,
                "max_size": queue_config.get("max_queue_size", 100)
            }
        
        # Individual domain queues
        domain_queues = queue_config.get("domain_queues", {})
        for domain, path in domain_queues.items():
            self.processing_queues[domain] = {
                "path": path,
                "current_size": 0,
                "max_size": queue_config.get("max_queue_size", 100)
            }
        
        self.logger.info(f"Initialized {len(self.processing_queues)} processing queues")
    
    async def process_requirement(self, 
                                requirement_content: str,
                                domain: str = None,
                                priority: str = "medium",
                                processing_mode: ProcessingMode = ProcessingMode.INDIVIDUAL) -> ProcessingResult:
        """
        Process a single requirement through the complete workflow.
        
        Args:
            requirement_content: The requirement text to process
            domain: Target domain (if known), otherwise auto-detected
            priority: Processing priority (low, medium, high, critical)
            processing_mode: How to process the requirement
            
        Returns:
            ProcessingResult with all processing outcomes
        """
        start_time = time.time()
        requirement_id = self._generate_requirement_id(requirement_content)
        
        self.logger.info(f"Processing requirement {requirement_id} in {processing_mode.value} mode")
        
        try:
            # Phase 1: Pre-processing and Analysis
            context = await self._preprocess_requirement(
                requirement_id, requirement_content, domain, priority
            )
            
            # Phase 2: Domain Coordination
            await self._coordinate_domain_processing(context)
            
            # Phase 3: Pattern Recognition and Intelligence
            await self._apply_intelligence_engines(context)
            
            # Phase 4: Cross-Domain Processing
            processing_results = await self._execute_cross_domain_processing(context)
            
            # Phase 5: Validation and Quality Assurance
            validation_results = await self._validate_results(context, processing_results)
            
            # Phase 6: Finalization and Documentation
            final_result = await self._finalize_processing(
                context, processing_results, validation_results
            )
            
            processing_time = time.time() - start_time
            self._record_performance_metrics(requirement_id, processing_time, final_result)
            
            self.logger.info(f"Completed processing {requirement_id} in {processing_time:.2f}s")
            return final_result
            
        except Exception as e:
            self.logger.error(f"Error processing requirement {requirement_id}: {e}")
            return ProcessingResult(
                requirement_id=requirement_id,
                success=False,
                processing_time=time.time() - start_time,
                pattern_matches=[],
                gr_compliance={},
                cross_domain_validations=[],
                generated_artifacts=[],
                confidence_score=0.0,
                error_messages=[str(e)]
            )
    
    async def _preprocess_requirement(self, 
                                    requirement_id: str,
                                    content: str,
                                    domain: str,
                                    priority: str) -> RequirementContext:
        """Pre-process requirement to extract entities and assign Global Requirements."""
        self.logger.info(f"Pre-processing requirement {requirement_id}")
        
        # Entity extraction
        entities = await self._extract_entities(content)
        
        # Auto-assign Global Requirements
        global_requirements = await self._auto_assign_global_requirements(content, entities)
        
        # Identify cross-domain relationships
        cross_domain_rels = await self._identify_cross_domain_relationships(entities)
        
        # Auto-detect domain if not specified
        if not domain:
            domain = await self._auto_detect_domain(content, entities)
        
        # Calculate initial confidence score
        confidence = await self._calculate_initial_confidence(content, entities, global_requirements)
        
        context = RequirementContext(
            requirement_id=requirement_id,
            domain=domain,
            priority=priority,
            content=content,
            entities_identified=entities,
            global_requirements=global_requirements,
            cross_domain_relationships=cross_domain_rels,
            confidence_score=confidence,
            processing_start_time=datetime.now(),
            assigned_agents=[]
        )
        
        # Update shared context
        await self._update_shared_context("preprocessing", context)
        
        return context
    
    async def _extract_entities(self, content: str) -> List[str]:
        """Extract business entities from requirement content."""
        entities = []
        
        # Use universal entity catalog for entity recognition
        entity_catalog = self.knowledge_base.get("universal_entities", {})
        core_entities = entity_catalog.get("core_entities", [])
        
        content_lower = content.lower()
        
        for entity_info in core_entities:
            entity_name = entity_info.get("name", "")
            keywords = entity_info.get("keywords", [])
            
            # Check for entity name
            if entity_name.lower() in content_lower:
                entities.append(entity_name)
                continue
            
            # Check for entity keywords
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    entities.append(entity_name)
                    break
        
        self.logger.info(f"Extracted entities: {entities}")
        return list(set(entities))  # Remove duplicates
    
    async def _auto_assign_global_requirements(self, content: str, entities: List[str]) -> List[str]:
        """Automatically assign applicable Global Requirements."""
        assigned_grs = []
        
        gr_index = self.knowledge_base.get("global_requirements", {})
        gr_assignments = gr_index.get("auto_assignment_rules", [])
        
        content_lower = content.lower()
        
        for gr_rule in gr_assignments:
            gr_id = gr_rule.get("gr_id")
            keywords = gr_rule.get("keywords", [])
            entity_triggers = gr_rule.get("entity_triggers", [])
            confidence = gr_rule.get("confidence", 0.0)
            
            # Check keyword triggers
            keyword_matches = sum(1 for keyword in keywords if keyword.lower() in content_lower)
            
            # Check entity triggers
            entity_matches = sum(1 for entity in entity_triggers if entity in entities)
            
            # Calculate assignment confidence
            total_triggers = len(keywords) + len(entity_triggers)
            total_matches = keyword_matches + entity_matches
            
            if total_triggers > 0:
                match_confidence = total_matches / total_triggers
                final_confidence = confidence * match_confidence
                
                # Assign if confidence threshold is met
                if final_confidence >= 0.7:  # Configurable threshold
                    assigned_grs.append(gr_id)
        
        self.logger.info(f"Auto-assigned Global Requirements: {assigned_grs}")
        return assigned_grs
    
    async def _identify_cross_domain_relationships(self, entities: List[str]) -> List[str]:
        """Identify relationships that cross domain boundaries."""
        relationships = []
        
        relationship_map = self.knowledge_base.get("cross_domain_relationships", {})
        entity_relationships = relationship_map.get("entity_relationship_matrix", {})
        
        # Look for entities that appear in cross-domain workflows
        for domain_pair, domain_relationships in entity_relationships.items():
            for entity in entities:
                if entity in domain_relationships:
                    relationships.append(f"{domain_pair}:{entity}")
        
        self.logger.info(f"Identified cross-domain relationships: {relationships}")
        return relationships
    
    async def _auto_detect_domain(self, content: str, entities: List[str]) -> str:
        """Auto-detect the primary domain for the requirement."""
        domain_scores = {}
        
        # Score based on domain specialist specializations
        for domain, specialist_config in self.domain_specialists.items():
            score = 0
            specializations = specialist_config.get("specializations", [])
            
            content_lower = content.lower()
            
            # Score based on specialization keywords
            for specialization in specializations:
                if specialization.replace("_", " ") in content_lower:
                    score += 2
                if specialization in content_lower:
                    score += 1
            
            # Score based on entities
            for entity in entities:
                if entity in specializations:
                    score += 3
            
            domain_scores[domain] = score
        
        # Return domain with highest score
        if domain_scores:
            detected_domain = max(domain_scores, key=domain_scores.get)
            self.logger.info(f"Auto-detected domain: {detected_domain} (score: {domain_scores[detected_domain]})")
            return detected_domain
        
        return "producer_portal"  # Default domain
    
    async def _calculate_initial_confidence(self, 
                                          content: str, 
                                          entities: List[str], 
                                          global_requirements: List[str]) -> float:
        """Calculate initial confidence score for the requirement."""
        confidence_factors = []
        
        # Content clarity (based on length and structure)
        content_length = len(content.split())
        if 10 <= content_length <= 200:
            confidence_factors.append(0.8)
        elif content_length > 200:
            confidence_factors.append(0.6)
        else:
            confidence_factors.append(0.4)
        
        # Entity identification confidence
        if len(entities) >= 2:
            confidence_factors.append(0.9)
        elif len(entities) == 1:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.3)
        
        # Global Requirements coverage
        if len(global_requirements) >= 3:
            confidence_factors.append(0.9)
        elif len(global_requirements) >= 1:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.4)
        
        # Calculate weighted average
        if confidence_factors:
            return sum(confidence_factors) / len(confidence_factors)
        
        return 0.5  # Default moderate confidence
    
    async def _coordinate_domain_processing(self, context: RequirementContext):
        """Coordinate processing across relevant domain specialists."""
        self.logger.info(f"Coordinating domain processing for {context.requirement_id}")
        
        # Determine which domain specialists to involve
        primary_domain = context.domain
        secondary_domains = self._get_secondary_domains(context)
        
        assigned_agents = [primary_domain]
        assigned_agents.extend(secondary_domains)
        
        context.assigned_agents = assigned_agents
        
        # Update shared context with coordination plan
        await self._update_shared_context("coordination", {
            "requirement_id": context.requirement_id,
            "primary_domain": primary_domain,
            "secondary_domains": secondary_domains,
            "processing_plan": "parallel_with_orchestrator_coordination"
        })
        
        self.logger.info(f"Assigned agents: {assigned_agents}")
    
    def _get_secondary_domains(self, context: RequirementContext) -> List[str]:
        """Determine secondary domains that should be involved in processing."""
        secondary_domains = []
        
        # Based on cross-domain relationships
        for relationship in context.cross_domain_relationships:
            if ":" in relationship:
                domain_pair = relationship.split(":")[0]
                if "_to_" in domain_pair:
                    domains = domain_pair.replace("_to_", ",").split(",")
                    for domain in domains:
                        domain = domain.replace("-", "_")
                        if domain != context.domain and domain in self.domain_specialists:
                            secondary_domains.append(domain)
        
        # Based on entities that commonly span domains
        universal_entities = ["address", "phone", "email", "payment"]
        for entity in context.entities_identified:
            if entity in universal_entities:
                # These entities often require cross-domain coordination
                if "payment" in entity and "accounting" not in secondary_domains:
                    secondary_domains.append("accounting")
                if entity in ["address", "phone", "email"] and "entity_integration" not in secondary_domains:
                    secondary_domains.append("entity_integration")
        
        return list(set(secondary_domains))  # Remove duplicates
    
    async def _apply_intelligence_engines(self, context: RequirementContext):
        """Apply all intelligence engines to enhance processing."""
        self.logger.info(f"Applying intelligence engines for {context.requirement_id}")
        
        intelligence_results = {}
        
        # Apply each enabled intelligence engine
        for engine_name, engine_config in self.intelligence_engines.items():
            if not engine_config.get("enabled", True):
                continue
            
            try:
                # Simulate intelligence engine processing
                # In a real implementation, these would be separate modules
                result = await self._simulate_intelligence_engine(engine_name, context)
                intelligence_results[engine_name] = result
                
            except Exception as e:
                self.logger.error(f"Error in intelligence engine {engine_name}: {e}")
                intelligence_results[engine_name] = {"error": str(e)}
        
        # Update shared context with intelligence results
        await self._update_shared_context("intelligence", {
            "requirement_id": context.requirement_id,
            "intelligence_results": intelligence_results
        })
    
    async def _simulate_intelligence_engine(self, engine_name: str, context: RequirementContext) -> Dict:
        """Simulate intelligence engine processing (placeholder for actual engines)."""
        if engine_name == "pattern_matcher":
            return {
                "patterns_found": [
                    {"pattern_id": "entity_crud", "confidence": 0.85},
                    {"pattern_id": "workflow_automation", "confidence": 0.72}
                ],
                "confidence": 0.80
            }
        elif engine_name == "similarity_engine":
            return {
                "similar_requirements": [
                    {"requirement_id": "req_001", "similarity": 0.82},
                    {"requirement_id": "req_045", "similarity": 0.76}
                ],
                "confidence": 0.75
            }
        elif engine_name == "gr_auto_assignment":
            return {
                "additional_grs": ["GR-19", "GR-41"],
                "confidence_scores": {"GR-19": 0.92, "GR-41": 0.87}
            }
        elif engine_name == "batch_optimizer":
            return {
                "batch_recommendations": {
                    "can_batch_with": ["req_123", "req_124"],
                    "estimated_efficiency": "45% time savings"
                }
            }
        
        return {"status": "processed", "confidence": 0.5}
    
    async def _execute_cross_domain_processing(self, context: RequirementContext) -> Dict:
        """Execute processing across all assigned domain specialists."""
        self.logger.info(f"Executing cross-domain processing for {context.requirement_id}")
        
        processing_results = {}
        
        # Process with each assigned agent in parallel
        tasks = []
        for agent_domain in context.assigned_agents:
            task = self._process_with_domain_specialist(context, agent_domain)
            tasks.append(task)
        
        # Wait for all processing to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Compile results
        for i, result in enumerate(results):
            agent_domain = context.assigned_agents[i]
            if isinstance(result, Exception):
                processing_results[agent_domain] = {"error": str(result)}
            else:
                processing_results[agent_domain] = result
        
        return processing_results
    
    async def _process_with_domain_specialist(self, context: RequirementContext, domain: str) -> Dict:
        """Process requirement with a specific domain specialist."""
        self.logger.info(f"Processing with {domain} specialist")
        
        specialist_config = self.domain_specialists.get(domain, {})
        
        # Simulate domain specialist processing
        # In a real implementation, this would communicate with actual agent
        await asyncio.sleep(0.1)  # Simulate processing time
        
        return {
            "domain": domain,
            "specializations_applied": specialist_config.get("specializations", []),
            "processing_time": 0.1,
            "artifacts_generated": [f"{domain}_section_c.md", f"{domain}_section_e.sql"],
            "confidence": 0.85,
            "status": "completed"
        }
    
    async def _validate_results(self, context: RequirementContext, processing_results: Dict) -> Dict:
        """Validate all processing results through the Universal Validator."""
        self.logger.info(f"Validating results for {context.requirement_id}")
        
        validation_results = {
            "global_requirements_compliance": await self._validate_gr_compliance(context),
            "cross_domain_consistency": await self._validate_cross_domain_consistency(processing_results),
            "infrastructure_alignment": await self._validate_infrastructure_alignment(processing_results),
            "pattern_compliance": await self._validate_pattern_compliance(context)
        }
        
        # Calculate overall validation score
        validation_scores = [v.get("score", 0.0) for v in validation_results.values()]
        overall_score = sum(validation_scores) / len(validation_scores) if validation_scores else 0.0
        
        validation_results["overall_score"] = overall_score
        validation_results["passed"] = overall_score >= 0.8  # Configurable threshold
        
        return validation_results
    
    async def _validate_gr_compliance(self, context: RequirementContext) -> Dict:
        """Validate Global Requirements compliance."""
        # Simulate GR compliance validation
        return {
            "checked_grs": context.global_requirements,
            "compliance_status": {gr: True for gr in context.global_requirements},
            "score": 0.95,
            "issues": []
        }
    
    async def _validate_cross_domain_consistency(self, processing_results: Dict) -> Dict:
        """Validate consistency across domain processing results."""
        # Simulate cross-domain consistency validation
        return {
            "domains_checked": list(processing_results.keys()),
            "consistency_score": 0.88,
            "conflicts_found": [],
            "score": 0.88
        }
    
    async def _validate_infrastructure_alignment(self, processing_results: Dict) -> Dict:
        """Validate alignment with existing infrastructure."""
        # Simulate infrastructure alignment validation
        return {
            "infrastructure_checks": ["database_schema", "api_patterns", "service_boundaries"],
            "alignment_score": 0.92,
            "conflicts": [],
            "score": 0.92
        }
    
    async def _validate_pattern_compliance(self, context: RequirementContext) -> Dict:
        """Validate compliance with established patterns."""
        # Simulate pattern compliance validation
        return {
            "patterns_checked": ["universal_entities", "communication_templates"],
            "compliance_score": 0.87,
            "violations": [],
            "score": 0.87
        }
    
    async def _finalize_processing(self, 
                                 context: RequirementContext,
                                 processing_results: Dict,
                                 validation_results: Dict) -> ProcessingResult:
        """Finalize processing and prepare final result."""
        self.logger.info(f"Finalizing processing for {context.requirement_id}")
        
        # Determine overall success
        success = validation_results.get("passed", False) and all(
            not result.get("error") for result in processing_results.values()
        )
        
        # Compile pattern matches
        pattern_matches = []
        for domain_result in processing_results.values():
            if "patterns_applied" in domain_result:
                pattern_matches.extend(domain_result["patterns_applied"])
        
        # Compile GR compliance
        gr_compliance = validation_results.get("global_requirements_compliance", {}).get("compliance_status", {})
        
        # Compile cross-domain validations
        cross_domain_validations = [validation_results.get("cross_domain_consistency", {})]
        
        # Compile generated artifacts
        generated_artifacts = []
        for domain_result in processing_results.values():
            if "artifacts_generated" in domain_result:
                generated_artifacts.extend(domain_result["artifacts_generated"])
        
        # Calculate final confidence score
        confidence_scores = [context.confidence_score]
        for domain_result in processing_results.values():
            if "confidence" in domain_result:
                confidence_scores.append(domain_result["confidence"])
        confidence_scores.append(validation_results.get("overall_score", 0.0))
        
        final_confidence = sum(confidence_scores) / len(confidence_scores)
        
        # Compile error messages
        error_messages = []
        for domain_result in processing_results.values():
            if "error" in domain_result:
                error_messages.append(domain_result["error"])
        
        return ProcessingResult(
            requirement_id=context.requirement_id,
            success=success,
            processing_time=(datetime.now() - context.processing_start_time).total_seconds(),
            pattern_matches=pattern_matches,
            gr_compliance=gr_compliance,
            cross_domain_validations=cross_domain_validations,
            generated_artifacts=generated_artifacts,
            confidence_score=final_confidence,
            error_messages=error_messages
        )
    
    async def _update_shared_context(self, context_type: str, data: Any):
        """Update the shared context with new information."""
        if not self.shared_context.get("sync_enabled", True):
            return
        
        timestamp = datetime.now().isoformat()
        
        if context_type not in self.shared_context:
            self.shared_context[context_type] = {}
        
        self.shared_context[context_type][timestamp] = data
        self.shared_context["last_sync"] = datetime.now()
    
    def _generate_requirement_id(self, content: str) -> str:
        """Generate a unique ID for a requirement."""
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:12]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"req_{timestamp}_{content_hash}"
    
    def _record_performance_metrics(self, requirement_id: str, processing_time: float, result: ProcessingResult):
        """Record performance metrics for monitoring."""
        metrics = {
            "requirement_id": requirement_id,
            "processing_time": processing_time,
            "success": result.success,
            "confidence_score": result.confidence_score,
            "pattern_matches_count": len(result.pattern_matches),
            "gr_compliance_rate": sum(result.gr_compliance.values()) / len(result.gr_compliance) if result.gr_compliance else 0,
            "timestamp": datetime.now().isoformat()
        }
        
        if "performance_data" not in self.shared_context:
            self.shared_context["performance_data"] = []
        
        self.shared_context["performance_data"].append(metrics)
        
        # Keep only recent metrics (last 1000 entries)
        if len(self.shared_context["performance_data"]) > 1000:
            self.shared_context["performance_data"] = self.shared_context["performance_data"][-1000:]
    
    def get_system_status(self) -> Dict:
        """Get current system status and health information."""
        return {
            "agent_id": self.config["agent_config"]["agent_id"],
            "status": "operational",
            "last_sync": self.shared_context.get("last_sync", "never").isoformat() if isinstance(self.shared_context.get("last_sync"), datetime) else "never",
            "domain_specialists": {
                domain: specialist["status"] 
                for domain, specialist in self.domain_specialists.items()
            },
            "intelligence_engines": {
                engine: config["status"] 
                for engine, config in self.intelligence_engines.items()
            },
            "processing_queues": {
                queue: {"size": config["current_size"], "max": config["max_size"]}
                for queue, config in self.processing_queues.items()
            },
            "performance_summary": self._get_performance_summary()
        }
    
    def _get_performance_summary(self) -> Dict:
        """Get summary of recent performance metrics."""
        performance_data = self.shared_context.get("performance_data", [])
        
        if not performance_data:
            return {"status": "no_data"}
        
        recent_data = performance_data[-100:]  # Last 100 requirements
        
        avg_processing_time = sum(m["processing_time"] for m in recent_data) / len(recent_data)
        success_rate = sum(1 for m in recent_data if m["success"]) / len(recent_data)
        avg_confidence = sum(m["confidence_score"] for m in recent_data) / len(recent_data)
        
        return {
            "requirements_processed": len(recent_data),
            "average_processing_time": round(avg_processing_time, 2),
            "success_rate": round(success_rate, 3),
            "average_confidence": round(avg_confidence, 3),
            "last_updated": datetime.now().isoformat()
        }

# Main execution and testing
if __name__ == "__main__":
    async def test_orchestrator():
        """Test the System Orchestrator Engine."""
        print("Testing System Orchestrator Engine...")
        
        # Initialize orchestrator
        orchestrator = SystemOrchestratorEngine()
        
        # Test system status
        status = orchestrator.get_system_status()
        print(f"System Status: {json.dumps(status, indent=2)}")
        
        # Test requirement processing
        test_requirement = """
        Create a new driver management feature that allows producers to add drivers to quotes.
        The system should validate driver license information through DCS integration,
        store driver information in the database following GR-52 standards,
        and support communication preferences for each driver.
        """
        
        result = await orchestrator.process_requirement(
            requirement_content=test_requirement,
            domain="producer_portal",
            priority="high"
        )
        
        print(f"Processing Result: {json.dumps(asdict(result), indent=2, default=str)}")
        
        return orchestrator
    
    # Run test if executed directly
    import asyncio
    asyncio.run(test_orchestrator())