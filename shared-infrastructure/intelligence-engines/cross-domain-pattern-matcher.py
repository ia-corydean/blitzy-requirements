#!/usr/bin/env python3
"""
Cross-Domain Pattern Matcher Intelligence Engine
Complete Requirements Generation System - Multi-Agent Architecture

Identifies reusable patterns across business domains and enables intelligent
pattern matching for cross-domain requirements processing.

Created: 2025-01-07
Version: 1.0.0
GR Compliance: GR-38, GR-44, GR-52, GR-49
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
import difflib
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configuration and Data Classes
@dataclass
class PatternMatch:
    """Represents a pattern match result."""
    pattern_id: str
    pattern_name: str
    confidence_score: float
    match_type: str  # exact, partial, similar
    domain_source: str
    pattern_data: Dict
    similarity_details: Dict
    recommended_usage: str

@dataclass
class CrossDomainRelationship:
    """Represents a relationship between domains."""
    relationship_id: str
    source_domain: str
    target_domain: str
    entity_connections: List[str]
    workflow_dependencies: List[str]
    shared_patterns: List[str]
    coordination_required: bool

@dataclass
class PatternAnalysisResult:
    """Result of pattern analysis."""
    requirement_id: str
    identified_patterns: List[PatternMatch]
    cross_domain_opportunities: List[CrossDomainRelationship]
    reuse_recommendations: List[Dict]
    confidence_score: float
    processing_time: float
    analysis_metadata: Dict

class PatternType(Enum):
    """Types of patterns that can be matched."""
    ENTITY_PATTERN = "entity_pattern"
    WORKFLOW_PATTERN = "workflow_pattern"
    COMMUNICATION_PATTERN = "communication_pattern"
    INTEGRATION_PATTERN = "integration_pattern"
    VALIDATION_PATTERN = "validation_pattern"
    UI_PATTERN = "ui_pattern"

class MatchQuality(Enum):
    """Quality levels for pattern matches."""
    EXACT = "exact"           # 95-100% match
    HIGH = "high"             # 85-94% match
    MEDIUM = "medium"         # 70-84% match
    LOW = "low"               # 50-69% match
    POOR = "poor"             # <50% match

class CrossDomainPatternMatcher:
    """
    Advanced pattern matching engine for identifying reusable patterns
    across business domains and enabling intelligent cross-domain processing.
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the Cross-Domain Pattern Matcher."""
        self.config_path = config_path or "/app/workspace/requirements/shared-infrastructure/agent-configurations/system-orchestrator.yaml"
        self.config = self._load_configuration()
        self.logger = self._setup_logging()
        
        # Pattern libraries
        self.universal_patterns = {}
        self.domain_patterns = {}
        self.cross_domain_relationships = {}
        
        # Analysis engines
        self.text_vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=1000,
            ngram_range=(1, 3)
        )
        self.pattern_vectors = {}
        self.pattern_index = {}
        
        # Performance tracking
        self.analysis_cache = {}
        self.performance_metrics = {}
        
        # Initialize pattern matcher
        self._initialize_pattern_matcher()
    
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
            "pattern_matching": {
                "similarity_threshold": 0.7,
                "max_patterns_per_analysis": 10,
                "cross_domain_threshold": 0.8
            },
            "performance": {
                "cache_enabled": True,
                "cache_ttl_hours": 24,
                "max_cache_size": 1000
            }
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the pattern matcher."""
        logger = logging.getLogger("CrossDomainPatternMatcher")
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def _initialize_pattern_matcher(self):
        """Initialize all pattern matching components."""
        self.logger.info("Initializing Cross-Domain Pattern Matcher...")
        
        try:
            # Load pattern libraries
            self._load_universal_patterns()
            self._load_domain_patterns()
            self._load_cross_domain_relationships()
            
            # Build pattern indexes
            self._build_pattern_indexes()
            
            # Initialize vectorization
            self._initialize_text_analysis()
            
            self.logger.info("Cross-Domain Pattern Matcher initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize pattern matcher: {e}")
            raise
    
    def _load_universal_patterns(self):
        """Load universal patterns from the knowledge base."""
        kb_config = self.config.get("knowledge_base", {})
        
        # Load universal entity patterns
        entities_dir = kb_config.get("universal_entities", "")
        if entities_dir and Path(entities_dir).exists():
            for pattern_file in Path(entities_dir).glob("*.json"):
                pattern_name = pattern_file.stem
                try:
                    with open(pattern_file, 'r') as f:
                        pattern_data = json.load(f)
                    self.universal_patterns[pattern_name] = {
                        "type": PatternType.ENTITY_PATTERN,
                        "data": pattern_data,
                        "source_file": str(pattern_file)
                    }
                except Exception as e:
                    self.logger.error(f"Error loading universal pattern {pattern_file}: {e}")
        
        # Load communication templates
        comm_dir = kb_config.get("communication_templates", "")
        if comm_dir and Path(comm_dir).exists():
            for template_file in Path(comm_dir).glob("*.json"):
                template_name = template_file.stem
                try:
                    with open(template_file, 'r') as f:
                        template_data = json.load(f)
                    self.universal_patterns[f"comm_{template_name}"] = {
                        "type": PatternType.COMMUNICATION_PATTERN,
                        "data": template_data,
                        "source_file": str(template_file)
                    }
                except Exception as e:
                    self.logger.error(f"Error loading communication template {template_file}: {e}")
        
        # Load service integration patterns
        service_dir = kb_config.get("service_integrations", "")
        if service_dir and Path(service_dir).exists():
            for service_file in Path(service_dir).glob("*.json"):
                service_name = service_file.stem
                try:
                    with open(service_file, 'r') as f:
                        service_data = json.load(f)
                    self.universal_patterns[f"service_{service_name}"] = {
                        "type": PatternType.INTEGRATION_PATTERN,
                        "data": service_data,
                        "source_file": str(service_file)
                    }
                except Exception as e:
                    self.logger.error(f"Error loading service integration {service_file}: {e}")
        
        self.logger.info(f"Loaded {len(self.universal_patterns)} universal patterns")
    
    def _load_domain_patterns(self):
        """Load domain-specific patterns."""
        kb_config = self.config.get("knowledge_base", {})
        domain_patterns_dir = kb_config.get("domain_patterns", "")
        
        if not domain_patterns_dir or not Path(domain_patterns_dir).exists():
            self.logger.warning("Domain patterns directory not found")
            return
        
        domains = ["producer-portal", "accounting", "program-manager", 
                  "program-traits", "entity-integration", "reinstatement", "sr22"]
        
        for domain in domains:
            domain_dir = Path(domain_patterns_dir) / domain
            if domain_dir.exists():
                self.domain_patterns[domain] = {}
                
                for pattern_file in domain_dir.glob("*.json"):
                    pattern_name = pattern_file.stem
                    try:
                        with open(pattern_file, 'r') as f:
                            pattern_data = json.load(f)
                        self.domain_patterns[domain][pattern_name] = {
                            "data": pattern_data,
                            "source_file": str(pattern_file)
                        }
                    except Exception as e:
                        self.logger.error(f"Error loading domain pattern {pattern_file}: {e}")
        
        total_domain_patterns = sum(len(patterns) for patterns in self.domain_patterns.values())
        self.logger.info(f"Loaded {total_domain_patterns} domain-specific patterns")
    
    def _load_cross_domain_relationships(self):
        """Load cross-domain relationship mappings."""
        kb_config = self.config.get("knowledge_base", {})
        relationships_file = kb_config.get("cross_domain_relationships", "")
        
        if not relationships_file or not Path(relationships_file).exists():
            self.logger.warning("Cross-domain relationships file not found")
            return
        
        try:
            with open(relationships_file, 'r') as f:
                relationships_data = json.load(f)
            
            # Process relationship matrix
            relationship_matrix = relationships_data.get("entity_relationship_matrix", {})
            for domain_pair, relationships in relationship_matrix.items():
                self.cross_domain_relationships[domain_pair] = relationships
            
            self.logger.info(f"Loaded {len(self.cross_domain_relationships)} cross-domain relationships")
            
        except Exception as e:
            self.logger.error(f"Error loading cross-domain relationships: {e}")
    
    def _build_pattern_indexes(self):
        """Build searchable indexes for all patterns."""
        pattern_id = 0
        
        # Index universal patterns
        for pattern_name, pattern_info in self.universal_patterns.items():
            pattern_text = self._extract_searchable_text(pattern_info["data"])
            self.pattern_index[pattern_id] = {
                "id": pattern_id,
                "name": pattern_name,
                "type": pattern_info["type"],
                "domain": "universal",
                "text": pattern_text,
                "data": pattern_info["data"],
                "source": pattern_info["source_file"]
            }
            pattern_id += 1
        
        # Index domain patterns
        for domain, domain_patterns in self.domain_patterns.items():
            for pattern_name, pattern_info in domain_patterns.items():
                pattern_text = self._extract_searchable_text(pattern_info["data"])
                self.pattern_index[pattern_id] = {
                    "id": pattern_id,
                    "name": pattern_name,
                    "type": PatternType.WORKFLOW_PATTERN,  # Assume workflow for domain patterns
                    "domain": domain,
                    "text": pattern_text,
                    "data": pattern_info["data"],
                    "source": pattern_info["source_file"]
                }
                pattern_id += 1
        
        self.logger.info(f"Built pattern index with {len(self.pattern_index)} patterns")
    
    def _extract_searchable_text(self, pattern_data: Dict) -> str:
        """Extract searchable text from pattern data."""
        text_parts = []
        
        def extract_text_recursive(obj, prefix=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, str):
                        text_parts.append(f"{prefix}{key}: {value}")
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, str):
                                text_parts.append(f"{prefix}{key}: {item}")
                            elif isinstance(item, dict):
                                extract_text_recursive(item, f"{prefix}{key}.")
                    elif isinstance(value, dict):
                        extract_text_recursive(value, f"{prefix}{key}.")
            elif isinstance(obj, str):
                text_parts.append(obj)
        
        extract_text_recursive(pattern_data)
        return " ".join(text_parts)
    
    def _initialize_text_analysis(self):
        """Initialize text analysis components."""
        if not self.pattern_index:
            self.logger.warning("No patterns available for text analysis")
            return
        
        # Prepare text corpus
        pattern_texts = [pattern["text"] for pattern in self.pattern_index.values()]
        
        # Fit vectorizer
        try:
            self.text_vectorizer.fit(pattern_texts)
            
            # Create pattern vectors
            for pattern_id, pattern in self.pattern_index.items():
                vector = self.text_vectorizer.transform([pattern["text"]])
                self.pattern_vectors[pattern_id] = vector
            
            self.logger.info("Text analysis components initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing text analysis: {e}")
    
    async def analyze_requirement_patterns(self, 
                                         requirement_content: str,
                                         domain: str = None,
                                         context: Dict = None) -> PatternAnalysisResult:
        """
        Analyze a requirement to identify applicable patterns across domains.
        
        Args:
            requirement_content: The requirement text to analyze
            domain: Target domain (if known)
            context: Additional context information
            
        Returns:
            PatternAnalysisResult with identified patterns and recommendations
        """
        start_time = datetime.now()
        requirement_id = self._generate_requirement_id(requirement_content)
        
        self.logger.info(f"Analyzing patterns for requirement {requirement_id}")
        
        try:
            # Check cache first
            cache_key = self._generate_cache_key(requirement_content, domain)
            cached_result = self._get_cached_result(cache_key)
            if cached_result:
                self.logger.info(f"Using cached analysis for {requirement_id}")
                return cached_result
            
            # Extract entities and keywords
            entities = await self._extract_entities(requirement_content)
            keywords = await self._extract_keywords(requirement_content)
            
            # Find pattern matches
            pattern_matches = await self._find_pattern_matches(
                requirement_content, entities, keywords, domain
            )
            
            # Identify cross-domain opportunities
            cross_domain_opportunities = await self._identify_cross_domain_opportunities(
                entities, pattern_matches, domain
            )
            
            # Generate reuse recommendations
            reuse_recommendations = await self._generate_reuse_recommendations(
                pattern_matches, cross_domain_opportunities
            )
            
            # Calculate overall confidence
            confidence_score = self._calculate_confidence_score(
                pattern_matches, cross_domain_opportunities
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            result = PatternAnalysisResult(
                requirement_id=requirement_id,
                identified_patterns=pattern_matches,
                cross_domain_opportunities=cross_domain_opportunities,
                reuse_recommendations=reuse_recommendations,
                confidence_score=confidence_score,
                processing_time=processing_time,
                analysis_metadata={
                    "entities_found": len(entities),
                    "keywords_found": len(keywords),
                    "patterns_analyzed": len(self.pattern_index),
                    "domain": domain,
                    "analysis_timestamp": datetime.now().isoformat()
                }
            )
            
            # Cache the result
            self._cache_result(cache_key, result)
            
            self.logger.info(f"Pattern analysis completed for {requirement_id} in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            self.logger.error(f"Error analyzing patterns for requirement {requirement_id}: {e}")
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return PatternAnalysisResult(
                requirement_id=requirement_id,
                identified_patterns=[],
                cross_domain_opportunities=[],
                reuse_recommendations=[],
                confidence_score=0.0,
                processing_time=processing_time,
                analysis_metadata={"error": str(e)}
            )
    
    async def _extract_entities(self, requirement_content: str) -> List[str]:
        """Extract business entities from requirement content."""
        entities = []
        content_lower = requirement_content.lower()
        
        # Check against universal entity patterns
        for pattern_name, pattern_info in self.universal_patterns.items():
            if pattern_info["type"] == PatternType.ENTITY_PATTERN:
                entity_data = pattern_info["data"]
                
                # Check entity name
                entity_name = entity_data.get("entity_metadata", {}).get("entity_name", "")
                if entity_name and entity_name.lower() in content_lower:
                    entities.append(entity_name)
                
                # Check keywords
                keywords = entity_data.get("entity_metadata", {}).get("keywords", [])
                for keyword in keywords:
                    if keyword.lower() in content_lower:
                        entities.append(entity_name)
                        break
                
                # Check table name
                table_structure = entity_data.get("table_structure", {})
                table_name = table_structure.get("table_name", "")
                if table_name and table_name.lower() in content_lower:
                    entities.append(entity_name)
        
        return list(set(entities))  # Remove duplicates
    
    async def _extract_keywords(self, requirement_content: str) -> List[str]:
        """Extract relevant keywords from requirement content."""
        # Simple keyword extraction (could be enhanced with NLP)
        content_lower = requirement_content.lower()
        
        # Domain-specific keywords
        domain_keywords = {
            "quote": ["quote", "quotation", "estimate", "pricing", "rating"],
            "policy": ["policy", "bind", "issue", "coverage", "effective"],
            "payment": ["payment", "billing", "premium", "installment", "due"],
            "driver": ["driver", "operator", "licensed", "violation", "mvr"],
            "vehicle": ["vehicle", "car", "auto", "vin", "make", "model"],
            "communication": ["email", "sms", "notification", "message", "alert"],
            "workflow": ["process", "workflow", "automation", "trigger", "step"],
            "integration": ["api", "service", "external", "integration", "endpoint"]
        }
        
        found_keywords = []
        for category, keywords in domain_keywords.items():
            for keyword in keywords:
                if keyword in content_lower:
                    found_keywords.append(keyword)
        
        return found_keywords
    
    async def _find_pattern_matches(self, 
                                  requirement_content: str,
                                  entities: List[str],
                                  keywords: List[str],
                                  domain: str = None) -> List[PatternMatch]:
        """Find matching patterns for the requirement."""
        matches = []
        
        # Vectorize the requirement content
        requirement_vector = self.text_vectorizer.transform([requirement_content])
        
        similarity_threshold = self.config.get("pattern_matching", {}).get("similarity_threshold", 0.7)
        max_patterns = self.config.get("pattern_matching", {}).get("max_patterns_per_analysis", 10)
        
        pattern_similarities = []
        
        # Calculate similarities with all patterns
        for pattern_id, pattern_vector in self.pattern_vectors.items():
            similarity = cosine_similarity(requirement_vector, pattern_vector)[0, 0]
            
            if similarity >= similarity_threshold:
                pattern_info = self.pattern_index[pattern_id]
                pattern_similarities.append((similarity, pattern_id, pattern_info))
        
        # Sort by similarity and take top matches
        pattern_similarities.sort(reverse=True, key=lambda x: x[0])
        top_patterns = pattern_similarities[:max_patterns]
        
        # Create PatternMatch objects
        for similarity, pattern_id, pattern_info in top_patterns:
            match_quality = self._determine_match_quality(similarity)
            
            # Additional scoring based on entities and keywords
            entity_score = self._calculate_entity_match_score(entities, pattern_info)
            keyword_score = self._calculate_keyword_match_score(keywords, pattern_info)
            
            # Combined confidence score
            confidence_score = (similarity * 0.6) + (entity_score * 0.3) + (keyword_score * 0.1)
            
            match = PatternMatch(
                pattern_id=f"pattern_{pattern_id}",
                pattern_name=pattern_info["name"],
                confidence_score=confidence_score,
                match_type=match_quality.value,
                domain_source=pattern_info["domain"],
                pattern_data=pattern_info["data"],
                similarity_details={
                    "text_similarity": similarity,
                    "entity_match_score": entity_score,
                    "keyword_match_score": keyword_score,
                    "entities_matched": self._get_matching_entities(entities, pattern_info),
                    "keywords_matched": self._get_matching_keywords(keywords, pattern_info)
                },
                recommended_usage=self._generate_usage_recommendation(pattern_info, confidence_score)
            )
            
            matches.append(match)
        
        return matches
    
    def _determine_match_quality(self, similarity: float) -> MatchQuality:
        """Determine match quality based on similarity score."""
        if similarity >= 0.95:
            return MatchQuality.EXACT
        elif similarity >= 0.85:
            return MatchQuality.HIGH
        elif similarity >= 0.70:
            return MatchQuality.MEDIUM
        elif similarity >= 0.50:
            return MatchQuality.LOW
        else:
            return MatchQuality.POOR
    
    def _calculate_entity_match_score(self, entities: List[str], pattern_info: Dict) -> float:
        """Calculate entity match score for a pattern."""
        if not entities:
            return 0.0
        
        pattern_text = pattern_info["text"].lower()
        matched_entities = sum(1 for entity in entities if entity.lower() in pattern_text)
        
        return matched_entities / len(entities)
    
    def _calculate_keyword_match_score(self, keywords: List[str], pattern_info: Dict) -> float:
        """Calculate keyword match score for a pattern."""
        if not keywords:
            return 0.0
        
        pattern_text = pattern_info["text"].lower()
        matched_keywords = sum(1 for keyword in keywords if keyword in pattern_text)
        
        return matched_keywords / len(keywords)
    
    def _get_matching_entities(self, entities: List[str], pattern_info: Dict) -> List[str]:
        """Get list of entities that match the pattern."""
        pattern_text = pattern_info["text"].lower()
        return [entity for entity in entities if entity.lower() in pattern_text]
    
    def _get_matching_keywords(self, keywords: List[str], pattern_info: Dict) -> List[str]:
        """Get list of keywords that match the pattern."""
        pattern_text = pattern_info["text"].lower()
        return [keyword for keyword in keywords if keyword in pattern_text]
    
    def _generate_usage_recommendation(self, pattern_info: Dict, confidence_score: float) -> str:
        """Generate usage recommendation for a pattern match."""
        pattern_type = pattern_info.get("type", PatternType.WORKFLOW_PATTERN)
        domain = pattern_info["domain"]
        
        if confidence_score >= 0.9:
            return f"Highly recommended: Direct reuse of {pattern_type.value} from {domain}"
        elif confidence_score >= 0.8:
            return f"Recommended: Adapt {pattern_type.value} from {domain} with minor modifications"
        elif confidence_score >= 0.7:
            return f"Consider: Use {pattern_type.value} from {domain} as reference for implementation"
        else:
            return f"Reference only: Review {pattern_type.value} from {domain} for inspiration"
    
    async def _identify_cross_domain_opportunities(self, 
                                                 entities: List[str],
                                                 pattern_matches: List[PatternMatch],
                                                 target_domain: str = None) -> List[CrossDomainRelationship]:
        """Identify opportunities for cross-domain coordination."""
        opportunities = []
        
        if not target_domain:
            return opportunities
        
        # Find patterns from other domains
        other_domain_patterns = [match for match in pattern_matches 
                               if match.domain_source != target_domain and match.domain_source != "universal"]
        
        for pattern_match in other_domain_patterns:
            source_domain = pattern_match.domain_source
            
            # Check if there's a known relationship
            relationship_key = f"{target_domain}_to_{source_domain}"
            reverse_key = f"{source_domain}_to_{target_domain}"
            
            if relationship_key in self.cross_domain_relationships or reverse_key in self.cross_domain_relationships:
                relationship_data = self.cross_domain_relationships.get(
                    relationship_key, self.cross_domain_relationships.get(reverse_key, {})
                )
                
                opportunity = CrossDomainRelationship(
                    relationship_id=f"rel_{target_domain}_{source_domain}",
                    source_domain=target_domain,
                    target_domain=source_domain,
                    entity_connections=self._find_entity_connections(entities, relationship_data),
                    workflow_dependencies=self._find_workflow_dependencies(pattern_match, relationship_data),
                    shared_patterns=[pattern_match.pattern_id],
                    coordination_required=pattern_match.confidence_score >= 0.8
                )
                
                opportunities.append(opportunity)
        
        return opportunities
    
    def _find_entity_connections(self, entities: List[str], relationship_data: Dict) -> List[str]:
        """Find entity connections in cross-domain relationships."""
        connections = []
        
        for entity in entities:
            if entity in relationship_data:
                connections.append(entity)
        
        return connections
    
    def _find_workflow_dependencies(self, pattern_match: PatternMatch, relationship_data: Dict) -> List[str]:
        """Find workflow dependencies from pattern match."""
        dependencies = []
        
        # Check if pattern involves workflow coordination
        pattern_text = str(pattern_match.pattern_data).lower()
        workflow_keywords = ["workflow", "process", "step", "trigger", "event", "notification"]
        
        for keyword in workflow_keywords:
            if keyword in pattern_text:
                dependencies.append(f"{pattern_match.domain_source}_{keyword}")
        
        return dependencies
    
    async def _generate_reuse_recommendations(self, 
                                            pattern_matches: List[PatternMatch],
                                            cross_domain_opportunities: List[CrossDomainRelationship]) -> List[Dict]:
        """Generate specific reuse recommendations."""
        recommendations = []
        
        # High-confidence pattern reuse recommendations
        high_confidence_patterns = [match for match in pattern_matches if match.confidence_score >= 0.8]
        
        for pattern in high_confidence_patterns:
            recommendation = {
                "type": "pattern_reuse",
                "pattern_id": pattern.pattern_id,
                "pattern_name": pattern.pattern_name,
                "confidence": pattern.confidence_score,
                "source_domain": pattern.domain_source,
                "recommendation": pattern.recommended_usage,
                "implementation_effort": self._estimate_implementation_effort(pattern),
                "benefits": self._estimate_benefits(pattern),
                "risks": self._identify_risks(pattern)
            }
            recommendations.append(recommendation)
        
        # Cross-domain coordination recommendations
        for opportunity in cross_domain_opportunities:
            if opportunity.coordination_required:
                recommendation = {
                    "type": "cross_domain_coordination",
                    "relationship_id": opportunity.relationship_id,
                    "source_domain": opportunity.source_domain,
                    "target_domain": opportunity.target_domain,
                    "coordination_points": opportunity.entity_connections + opportunity.workflow_dependencies,
                    "implementation_effort": "medium",
                    "benefits": ["Improved consistency", "Reduced duplication", "Better user experience"],
                    "risks": ["Increased complexity", "Coordination overhead"]
                }
                recommendations.append(recommendation)
        
        return recommendations
    
    def _estimate_implementation_effort(self, pattern: PatternMatch) -> str:
        """Estimate implementation effort for a pattern."""
        if pattern.match_type == MatchQuality.EXACT.value:
            return "low"
        elif pattern.match_type == MatchQuality.HIGH.value:
            return "low_to_medium"
        elif pattern.match_type == MatchQuality.MEDIUM.value:
            return "medium"
        else:
            return "high"
    
    def _estimate_benefits(self, pattern: PatternMatch) -> List[str]:
        """Estimate benefits of using a pattern."""
        benefits = ["Faster development", "Proven implementation"]
        
        if pattern.domain_source == "universal":
            benefits.extend(["Consistent user experience", "Reduced testing overhead"])
        
        if pattern.confidence_score >= 0.9:
            benefits.append("Minimal customization required")
        
        return benefits
    
    def _identify_risks(self, pattern: PatternMatch) -> List[str]:
        """Identify risks of using a pattern."""
        risks = []
        
        if pattern.domain_source != "universal":
            risks.append("Domain-specific assumptions may not apply")
        
        if pattern.confidence_score < 0.8:
            risks.append("Significant adaptation may be required")
        
        if "integration" in pattern.pattern_name.lower():
            risks.append("External dependencies may affect reliability")
        
        return risks
    
    def _calculate_confidence_score(self, 
                                  pattern_matches: List[PatternMatch],
                                  cross_domain_opportunities: List[CrossDomainRelationship]) -> float:
        """Calculate overall confidence score for the analysis."""
        if not pattern_matches:
            return 0.0
        
        # Average confidence of top 3 patterns
        top_patterns = sorted(pattern_matches, key=lambda x: x.confidence_score, reverse=True)[:3]
        pattern_confidence = sum(p.confidence_score for p in top_patterns) / len(top_patterns)
        
        # Boost confidence if cross-domain opportunities exist
        cross_domain_boost = min(0.1, len(cross_domain_opportunities) * 0.05)
        
        return min(1.0, pattern_confidence + cross_domain_boost)
    
    def _generate_requirement_id(self, content: str) -> str:
        """Generate unique ID for a requirement."""
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:12]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"req_{timestamp}_{content_hash}"
    
    def _generate_cache_key(self, requirement_content: str, domain: str = None) -> str:
        """Generate cache key for requirement analysis."""
        content_hash = hashlib.sha256(requirement_content.encode()).hexdigest()[:16]
        domain_suffix = f"_{domain}" if domain else ""
        return f"analysis_{content_hash}{domain_suffix}"
    
    def _get_cached_result(self, cache_key: str) -> Optional[PatternAnalysisResult]:
        """Get cached analysis result if available."""
        if not self.config.get("performance", {}).get("cache_enabled", True):
            return None
        
        if cache_key not in self.analysis_cache:
            return None
        
        cached_entry = self.analysis_cache[cache_key]
        cache_ttl_hours = self.config.get("performance", {}).get("cache_ttl_hours", 24)
        
        if datetime.now() - cached_entry["timestamp"] > timedelta(hours=cache_ttl_hours):
            del self.analysis_cache[cache_key]
            return None
        
        return cached_entry["result"]
    
    def _cache_result(self, cache_key: str, result: PatternAnalysisResult):
        """Cache analysis result."""
        if not self.config.get("performance", {}).get("cache_enabled", True):
            return
        
        max_cache_size = self.config.get("performance", {}).get("max_cache_size", 1000)
        
        # Clean up old entries if cache is full
        if len(self.analysis_cache) >= max_cache_size:
            oldest_key = min(self.analysis_cache.keys(), 
                           key=lambda k: self.analysis_cache[k]["timestamp"])
            del self.analysis_cache[oldest_key]
        
        self.analysis_cache[cache_key] = {
            "result": result,
            "timestamp": datetime.now()
        }
    
    def get_pattern_statistics(self) -> Dict:
        """Get statistics about loaded patterns."""
        universal_count = len(self.universal_patterns)
        domain_counts = {domain: len(patterns) for domain, patterns in self.domain_patterns.items()}
        total_patterns = universal_count + sum(domain_counts.values())
        
        pattern_types = defaultdict(int)
        for pattern_info in self.universal_patterns.values():
            pattern_types[pattern_info["type"].value] += 1
        
        return {
            "total_patterns": total_patterns,
            "universal_patterns": universal_count,
            "domain_patterns": domain_counts,
            "pattern_types": dict(pattern_types),
            "cross_domain_relationships": len(self.cross_domain_relationships),
            "cache_size": len(self.analysis_cache),
            "analysis_performance": self.performance_metrics
        }

# Main execution and testing
if __name__ == "__main__":
    async def test_pattern_matcher():
        """Test the Cross-Domain Pattern Matcher."""
        print("Testing Cross-Domain Pattern Matcher...")
        
        # Initialize pattern matcher
        matcher = CrossDomainPatternMatcher()
        
        # Test pattern statistics
        stats = matcher.get_pattern_statistics()
        print(f"Pattern Statistics: {json.dumps(stats, indent=2)}")
        
        # Test requirement analysis
        test_requirement = """
        Create a new driver management feature that allows producers to add drivers to quotes.
        The system should validate driver license information through DCS integration,
        store driver information in the database following GR-52 standards,
        and support communication preferences for each driver including email and SMS notifications.
        The driver data should be accessible across different policy workflows and integrate
        with the payment processing system for billing purposes.
        """
        
        result = await matcher.analyze_requirement_patterns(
            requirement_content=test_requirement,
            domain="producer_portal",
            context={"priority": "high", "user": "test_user"}
        )
        
        print(f"Analysis Result: {json.dumps(asdict(result), indent=2, default=str)}")
        
        return matcher
    
    # Run test if executed directly
    import asyncio
    asyncio.run(test_pattern_matcher())