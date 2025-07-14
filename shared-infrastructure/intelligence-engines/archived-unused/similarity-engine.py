#!/usr/bin/env python3
"""
Advanced Similarity Engine for Cross-Domain Pattern Recognition

This engine provides sophisticated pattern matching and similarity scoring
capabilities across all business domains, enabling intelligent requirement
grouping and pattern reuse.

Features:
- Multi-dimensional similarity analysis
- Cross-domain pattern matching
- Confidence-based scoring
- Historical pattern learning
- Performance optimization
"""

import json
import logging
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import re
from collections import defaultdict
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimilarityDimension(Enum):
    """Dimensions for similarity analysis"""
    ENTITY = "entity"
    WORKFLOW = "workflow"
    GLOBAL_REQUIREMENT = "global_requirement"
    DOMAIN = "domain"
    INTEGRATION = "integration"
    VALIDATION = "validation"
    INFRASTRUCTURE = "infrastructure"


@dataclass
class SimilarityScore:
    """Detailed similarity score breakdown"""
    overall_score: float
    dimension_scores: Dict[SimilarityDimension, float]
    confidence: float
    matched_patterns: List[str]
    recommendations: List[str]


@dataclass
class Pattern:
    """Represents a reusable pattern"""
    id: str
    domain: str
    type: str
    content: Dict
    entities: List[str]
    global_requirements: List[str]
    success_rate: float
    usage_count: int
    last_used: datetime
    metadata: Dict = field(default_factory=dict)


class AdvancedSimilarityEngine:
    """
    Advanced engine for multi-dimensional similarity analysis
    and cross-domain pattern recognition
    """
    
    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.patterns: Dict[str, Pattern] = {}
        self.entity_index: Dict[str, Set[str]] = defaultdict(set)
        self.gr_index: Dict[str, Set[str]] = defaultdict(set)
        self.domain_index: Dict[str, Set[str]] = defaultdict(set)
        self.similarity_cache: Dict[str, SimilarityScore] = {}
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load patterns and indices from knowledge base"""
        try:
            # Load universal entity catalog
            entity_catalog_path = self.knowledge_base_path / "universal-entity-catalog.json"
            if entity_catalog_path.exists():
                with open(entity_catalog_path, 'r') as f:
                    self.entity_catalog = json.load(f)
                    logger.info(f"Loaded {len(self.entity_catalog['entities'])} entities")
            
            # Load global requirements index
            gr_index_path = self.knowledge_base_path / "global-requirements-index.json"
            if gr_index_path.exists():
                with open(gr_index_path, 'r') as f:
                    self.gr_mapping = json.load(f)
                    logger.info(f"Loaded {len(self.gr_mapping['global_requirements'])} GRs")
            
            # Load domain patterns
            domain_patterns_path = self.knowledge_base_path / "domain-patterns"
            if domain_patterns_path.exists():
                for domain_dir in domain_patterns_path.iterdir():
                    if domain_dir.is_dir():
                        self._load_domain_patterns(domain_dir)
            
            # Load cross-domain relationships
            relationships_path = self.knowledge_base_path / "cross-domain-relationships/relationship-map.json"
            if relationships_path.exists():
                with open(relationships_path, 'r') as f:
                    self.cross_domain_relationships = json.load(f)
                    logger.info("Loaded cross-domain relationships")
            
            logger.info(f"Loaded {len(self.patterns)} patterns total")
            
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
    
    def _load_domain_patterns(self, domain_dir: Path):
        """Load patterns for a specific domain"""
        domain_name = domain_dir.name
        pattern_files = list(domain_dir.glob("*.json"))
        
        for pattern_file in pattern_files:
            try:
                with open(pattern_file, 'r') as f:
                    pattern_data = json.load(f)
                    
                pattern = Pattern(
                    id=f"{domain_name}_{pattern_file.stem}",
                    domain=domain_name,
                    type=pattern_data.get('type', 'unknown'),
                    content=pattern_data,
                    entities=pattern_data.get('entities', []),
                    global_requirements=pattern_data.get('global_requirements', []),
                    success_rate=pattern_data.get('success_rate', 0.8),
                    usage_count=pattern_data.get('usage_count', 0),
                    last_used=datetime.fromisoformat(pattern_data.get('last_used', datetime.now().isoformat())),
                    metadata=pattern_data.get('metadata', {})
                )
                
                self.patterns[pattern.id] = pattern
                
                # Update indices
                for entity in pattern.entities:
                    self.entity_index[entity].add(pattern.id)
                
                for gr in pattern.global_requirements:
                    self.gr_index[gr].add(pattern.id)
                
                self.domain_index[domain_name].add(pattern.id)
                
            except Exception as e:
                logger.warning(f"Error loading pattern {pattern_file}: {e}")
    
    def calculate_similarity(self, 
                           requirement1: Dict, 
                           requirement2: Dict,
                           dimensions: Optional[List[SimilarityDimension]] = None) -> SimilarityScore:
        """
        Calculate multi-dimensional similarity between two requirements
        
        Args:
            requirement1: First requirement to compare
            requirement2: Second requirement to compare
            dimensions: Specific dimensions to analyze (default: all)
            
        Returns:
            SimilarityScore with detailed breakdown
        """
        if dimensions is None:
            dimensions = list(SimilarityDimension)
        
        dimension_scores = {}
        matched_patterns = []
        recommendations = []
        
        # Calculate similarity for each dimension
        for dimension in dimensions:
            if dimension == SimilarityDimension.ENTITY:
                score, patterns = self._calculate_entity_similarity(requirement1, requirement2)
                dimension_scores[dimension] = score
                matched_patterns.extend(patterns)
                
            elif dimension == SimilarityDimension.WORKFLOW:
                score, patterns = self._calculate_workflow_similarity(requirement1, requirement2)
                dimension_scores[dimension] = score
                matched_patterns.extend(patterns)
                
            elif dimension == SimilarityDimension.GLOBAL_REQUIREMENT:
                score, patterns = self._calculate_gr_similarity(requirement1, requirement2)
                dimension_scores[dimension] = score
                matched_patterns.extend(patterns)
                
            elif dimension == SimilarityDimension.DOMAIN:
                score = self._calculate_domain_similarity(requirement1, requirement2)
                dimension_scores[dimension] = score
                
            elif dimension == SimilarityDimension.INTEGRATION:
                score, patterns = self._calculate_integration_similarity(requirement1, requirement2)
                dimension_scores[dimension] = score
                matched_patterns.extend(patterns)
                
            elif dimension == SimilarityDimension.VALIDATION:
                score = self._calculate_validation_similarity(requirement1, requirement2)
                dimension_scores[dimension] = score
                
            elif dimension == SimilarityDimension.INFRASTRUCTURE:
                score = self._calculate_infrastructure_similarity(requirement1, requirement2)
                dimension_scores[dimension] = score
        
        # Calculate overall score with weighted average
        weights = {
            SimilarityDimension.ENTITY: 0.25,
            SimilarityDimension.WORKFLOW: 0.20,
            SimilarityDimension.GLOBAL_REQUIREMENT: 0.20,
            SimilarityDimension.DOMAIN: 0.10,
            SimilarityDimension.INTEGRATION: 0.10,
            SimilarityDimension.VALIDATION: 0.10,
            SimilarityDimension.INFRASTRUCTURE: 0.05
        }
        
        overall_score = sum(
            dimension_scores.get(dim, 0) * weights.get(dim, 0)
            for dim in dimensions
        ) / sum(weights.get(dim, 0) for dim in dimensions)
        
        # Calculate confidence based on pattern matches and data completeness
        confidence = self._calculate_confidence(
            requirement1, requirement2, matched_patterns, dimension_scores
        )
        
        # Generate recommendations
        if overall_score > 0.7:
            recommendations.append("High similarity - consider batch processing together")
            recommendations.append("Review for pattern consolidation opportunities")
        elif overall_score > 0.5:
            recommendations.append("Moderate similarity - review shared components")
            recommendations.append("Consider coordinated validation")
        
        # Add dimension-specific recommendations
        if dimension_scores.get(SimilarityDimension.ENTITY, 0) > 0.8:
            recommendations.append("Strong entity overlap - ensure consistent definitions")
        
        if dimension_scores.get(SimilarityDimension.GLOBAL_REQUIREMENT, 0) > 0.9:
            recommendations.append("Same GR compliance requirements - use shared validation")
        
        return SimilarityScore(
            overall_score=overall_score,
            dimension_scores=dimension_scores,
            confidence=confidence,
            matched_patterns=list(set(matched_patterns)),
            recommendations=recommendations
        )
    
    def _calculate_entity_similarity(self, req1: Dict, req2: Dict) -> Tuple[float, List[str]]:
        """Calculate similarity based on shared entities"""
        entities1 = set(req1.get('entities', []))
        entities2 = set(req2.get('entities', []))
        
        if not entities1 or not entities2:
            return 0.0, []
        
        # Direct entity overlap
        common_entities = entities1.intersection(entities2)
        direct_similarity = len(common_entities) / max(len(entities1), len(entities2))
        
        # Check for related entities through patterns
        pattern_matches = []
        for entity in common_entities:
            if entity in self.entity_index:
                pattern_matches.extend(self.entity_index[entity])
        
        # Consider entity relationships
        relationship_boost = 0.0
        if hasattr(self, 'cross_domain_relationships'):
            for relationship in self.cross_domain_relationships.get('relationships', []):
                if (relationship['source_entity'] in entities1 and 
                    relationship['target_entity'] in entities2):
                    relationship_boost += 0.1
        
        final_score = min(1.0, direct_similarity + relationship_boost)
        return final_score, pattern_matches[:5]  # Return top 5 pattern matches
    
    def _calculate_workflow_similarity(self, req1: Dict, req2: Dict) -> Tuple[float, List[str]]:
        """Calculate similarity based on workflow patterns"""
        workflow1 = req1.get('workflow', {})
        workflow2 = req2.get('workflow', {})
        
        if not workflow1 or not workflow2:
            return 0.0, []
        
        # Compare workflow steps
        steps1 = set(workflow1.get('steps', []))
        steps2 = set(workflow2.get('steps', []))
        
        if steps1 and steps2:
            step_similarity = len(steps1.intersection(steps2)) / max(len(steps1), len(steps2))
        else:
            step_similarity = 0.0
        
        # Compare workflow type
        type_similarity = 1.0 if workflow1.get('type') == workflow2.get('type') else 0.0
        
        # Check for pattern matches
        pattern_matches = []
        workflow_key = f"{workflow1.get('type', 'unknown')}_{workflow2.get('type', 'unknown')}"
        
        for pattern_id, pattern in self.patterns.items():
            if pattern.type == 'workflow' and workflow_key in str(pattern.content):
                pattern_matches.append(pattern_id)
        
        final_score = (step_similarity * 0.7 + type_similarity * 0.3)
        return final_score, pattern_matches[:3]
    
    def _calculate_gr_similarity(self, req1: Dict, req2: Dict) -> Tuple[float, List[str]]:
        """Calculate similarity based on Global Requirements"""
        grs1 = set(req1.get('global_requirements', []))
        grs2 = set(req2.get('global_requirements', []))
        
        if not grs1 or not grs2:
            return 0.0, []
        
        # Direct GR overlap
        common_grs = grs1.intersection(grs2)
        direct_similarity = len(common_grs) / max(len(grs1), len(grs2))
        
        # Check for pattern matches
        pattern_matches = []
        for gr in common_grs:
            if gr in self.gr_index:
                pattern_matches.extend(self.gr_index[gr])
        
        # Consider GR categories (if available)
        category_boost = 0.0
        if hasattr(self, 'gr_mapping'):
            categories1 = set()
            categories2 = set()
            
            for gr in grs1:
                if gr in self.gr_mapping.get('global_requirements', {}):
                    cat = self.gr_mapping['global_requirements'][gr].get('category')
                    if cat:
                        categories1.add(cat)
            
            for gr in grs2:
                if gr in self.gr_mapping.get('global_requirements', {}):
                    cat = self.gr_mapping['global_requirements'][gr].get('category')
                    if cat:
                        categories2.add(cat)
            
            if categories1 and categories2:
                category_boost = len(categories1.intersection(categories2)) / max(len(categories1), len(categories2)) * 0.2
        
        final_score = min(1.0, direct_similarity + category_boost)
        return final_score, list(set(pattern_matches))[:5]
    
    def _calculate_domain_similarity(self, req1: Dict, req2: Dict) -> float:
        """Calculate similarity based on domain alignment"""
        domain1 = req1.get('domain', '')
        domain2 = req2.get('domain', '')
        
        if not domain1 or not domain2:
            return 0.0
        
        # Direct domain match
        if domain1 == domain2:
            return 1.0
        
        # Check for related domains
        related_domains = {
            'producer-portal': ['accounting', 'entity-integration'],
            'accounting': ['producer-portal', 'reinstatement'],
            'program-manager': ['program-traits'],
            'program-traits': ['program-manager'],
            'entity-integration': ['producer-portal', 'sr22'],
            'reinstatement': ['accounting', 'producer-portal'],
            'sr22': ['entity-integration', 'producer-portal']
        }
        
        if domain2 in related_domains.get(domain1, []):
            return 0.5
        
        return 0.0
    
    def _calculate_integration_similarity(self, req1: Dict, req2: Dict) -> Tuple[float, List[str]]:
        """Calculate similarity based on integration patterns"""
        integrations1 = set(req1.get('integrations', []))
        integrations2 = set(req2.get('integrations', []))
        
        if not integrations1 and not integrations2:
            return 1.0, []  # Both have no integrations
        
        if not integrations1 or not integrations2:
            return 0.0, []
        
        # Direct integration overlap
        common_integrations = integrations1.intersection(integrations2)
        similarity = len(common_integrations) / max(len(integrations1), len(integrations2))
        
        # Check for integration patterns
        pattern_matches = []
        for pattern_id, pattern in self.patterns.items():
            if pattern.type == 'integration':
                pattern_integrations = set(pattern.content.get('integrations', []))
                if pattern_integrations.intersection(common_integrations):
                    pattern_matches.append(pattern_id)
        
        return similarity, pattern_matches[:3]
    
    def _calculate_validation_similarity(self, req1: Dict, req2: Dict) -> float:
        """Calculate similarity based on validation requirements"""
        validations1 = req1.get('validations', {})
        validations2 = req2.get('validations', {})
        
        if not validations1 and not validations2:
            return 1.0
        
        if not validations1 or not validations2:
            return 0.0
        
        # Compare validation types
        types1 = set(validations1.keys())
        types2 = set(validations2.keys())
        
        if types1 and types2:
            type_similarity = len(types1.intersection(types2)) / max(len(types1), len(types2))
        else:
            type_similarity = 0.0
        
        # Compare validation rules
        rule_similarity = 0.0
        common_types = types1.intersection(types2)
        
        if common_types:
            rule_matches = 0
            total_rules = 0
            
            for val_type in common_types:
                rules1 = set(validations1.get(val_type, {}).get('rules', []))
                rules2 = set(validations2.get(val_type, {}).get('rules', []))
                
                if rules1 and rules2:
                    rule_matches += len(rules1.intersection(rules2))
                    total_rules += max(len(rules1), len(rules2))
            
            if total_rules > 0:
                rule_similarity = rule_matches / total_rules
        
        return (type_similarity * 0.6 + rule_similarity * 0.4)
    
    def _calculate_infrastructure_similarity(self, req1: Dict, req2: Dict) -> float:
        """Calculate similarity based on infrastructure requirements"""
        infra1 = req1.get('infrastructure', {})
        infra2 = req2.get('infrastructure', {})
        
        if not infra1 and not infra2:
            return 1.0
        
        if not infra1 or not infra2:
            return 0.0
        
        similarity_score = 0.0
        comparison_count = 0
        
        # Compare database requirements
        if 'database' in infra1 or 'database' in infra2:
            db1 = set(infra1.get('database', {}).get('tables', []))
            db2 = set(infra2.get('database', {}).get('tables', []))
            
            if db1 and db2:
                similarity_score += len(db1.intersection(db2)) / max(len(db1), len(db2))
                comparison_count += 1
        
        # Compare API requirements
        if 'api' in infra1 or 'api' in infra2:
            api1 = set(infra1.get('api', {}).get('endpoints', []))
            api2 = set(infra2.get('api', {}).get('endpoints', []))
            
            if api1 and api2:
                similarity_score += len(api1.intersection(api2)) / max(len(api1), len(api2))
                comparison_count += 1
        
        # Compare service requirements
        if 'services' in infra1 or 'services' in infra2:
            svc1 = set(infra1.get('services', []))
            svc2 = set(infra2.get('services', []))
            
            if svc1 and svc2:
                similarity_score += len(svc1.intersection(svc2)) / max(len(svc1), len(svc2))
                comparison_count += 1
        
        return similarity_score / comparison_count if comparison_count > 0 else 0.0
    
    def _calculate_confidence(self, req1: Dict, req2: Dict, 
                            matched_patterns: List[str], 
                            dimension_scores: Dict[SimilarityDimension, float]) -> float:
        """Calculate confidence score for similarity assessment"""
        confidence = 0.5  # Base confidence
        
        # Boost confidence based on data completeness
        completeness1 = self._calculate_requirement_completeness(req1)
        completeness2 = self._calculate_requirement_completeness(req2)
        confidence += (completeness1 + completeness2) / 2 * 0.2
        
        # Boost confidence based on pattern matches
        if matched_patterns:
            pattern_confidence = min(len(matched_patterns) / 10, 0.2)
            confidence += pattern_confidence
        
        # Boost confidence based on high similarity scores
        high_similarity_dimensions = sum(
            1 for score in dimension_scores.values() if score > 0.8
        )
        confidence += high_similarity_dimensions / len(dimension_scores) * 0.1
        
        return min(confidence, 1.0)
    
    def _calculate_requirement_completeness(self, requirement: Dict) -> float:
        """Calculate how complete a requirement specification is"""
        required_fields = [
            'domain', 'entities', 'global_requirements', 
            'workflow', 'validations', 'infrastructure'
        ]
        
        present_fields = sum(1 for field in required_fields if requirement.get(field))
        return present_fields / len(required_fields)
    
    def find_similar_patterns(self, requirement: Dict, 
                            threshold: float = 0.7,
                            max_results: int = 10) -> List[Tuple[Pattern, SimilarityScore]]:
        """
        Find patterns similar to the given requirement
        
        Args:
            requirement: Requirement to match against
            threshold: Minimum similarity score
            max_results: Maximum number of results to return
            
        Returns:
            List of (Pattern, SimilarityScore) tuples
        """
        similar_patterns = []
        
        # First, filter patterns by domain if specified
        domain = requirement.get('domain')
        candidate_patterns = (
            [self.patterns[pid] for pid in self.domain_index.get(domain, [])]
            if domain else list(self.patterns.values())
        )
        
        # Calculate similarity with each candidate pattern
        for pattern in candidate_patterns:
            # Convert pattern to requirement format for comparison
            pattern_as_req = {
                'domain': pattern.domain,
                'entities': pattern.entities,
                'global_requirements': pattern.global_requirements,
                'workflow': pattern.content.get('workflow', {}),
                'validations': pattern.content.get('validations', {}),
                'infrastructure': pattern.content.get('infrastructure', {}),
                'integrations': pattern.content.get('integrations', [])
            }
            
            similarity = self.calculate_similarity(requirement, pattern_as_req)
            
            if similarity.overall_score >= threshold:
                similar_patterns.append((pattern, similarity))
        
        # Sort by similarity score and return top results
        similar_patterns.sort(key=lambda x: x[1].overall_score, reverse=True)
        return similar_patterns[:max_results]
    
    def group_similar_requirements(self, requirements: List[Dict], 
                                 threshold: float = 0.6) -> List[List[Dict]]:
        """
        Group requirements by similarity for batch processing
        
        Args:
            requirements: List of requirements to group
            threshold: Minimum similarity score for grouping
            
        Returns:
            List of requirement groups
        """
        if len(requirements) <= 1:
            return [requirements]
        
        # Calculate pairwise similarities
        n = len(requirements)
        similarity_matrix = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                similarity = self.calculate_similarity(requirements[i], requirements[j])
                score = similarity.overall_score
                similarity_matrix[i][j] = score
                similarity_matrix[j][i] = score
        
        # Group using hierarchical clustering
        groups = []
        assigned = [False] * n
        
        for i in range(n):
            if assigned[i]:
                continue
            
            # Start new group
            group = [requirements[i]]
            assigned[i] = True
            
            # Add similar requirements to group
            for j in range(i + 1, n):
                if not assigned[j] and similarity_matrix[i][j] >= threshold:
                    # Check if similar to all in group
                    similar_to_all = all(
                        similarity_matrix[requirements.index(req)][j] >= threshold * 0.8
                        for req in group
                    )
                    
                    if similar_to_all:
                        group.append(requirements[j])
                        assigned[j] = True
            
            groups.append(group)
        
        return groups
    
    def update_pattern_success(self, pattern_id: str, success: bool):
        """Update pattern success rate based on usage"""
        if pattern_id in self.patterns:
            pattern = self.patterns[pattern_id]
            
            # Update success rate with exponential moving average
            alpha = 0.1  # Learning rate
            current_success = 1.0 if success else 0.0
            pattern.success_rate = (1 - alpha) * pattern.success_rate + alpha * current_success
            
            # Update usage count and timestamp
            pattern.usage_count += 1
            pattern.last_used = datetime.now()
            
            logger.info(f"Updated pattern {pattern_id}: success_rate={pattern.success_rate:.2f}, usage_count={pattern.usage_count}")
    
    def export_similarity_report(self, requirement1: Dict, requirement2: Dict) -> Dict:
        """Generate detailed similarity analysis report"""
        similarity = self.calculate_similarity(requirement1, requirement2)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_similarity': similarity.overall_score,
            'confidence': similarity.confidence,
            'dimension_breakdown': {
                dim.value: {
                    'score': score,
                    'interpretation': self._interpret_score(score)
                }
                for dim, score in similarity.dimension_scores.items()
            },
            'matched_patterns': [
                {
                    'pattern_id': pattern_id,
                    'pattern': self.patterns[pattern_id].content if pattern_id in self.patterns else None
                }
                for pattern_id in similarity.matched_patterns
            ],
            'recommendations': similarity.recommendations,
            'batch_processing_suitable': similarity.overall_score > 0.7,
            'coordination_required': any(
                score > 0.5 for dim, score in similarity.dimension_scores.items()
                if dim in [SimilarityDimension.ENTITY, SimilarityDimension.INTEGRATION]
            )
        }
        
        return report
    
    def _interpret_score(self, score: float) -> str:
        """Interpret similarity score"""
        if score >= 0.9:
            return "Very High - Nearly identical"
        elif score >= 0.7:
            return "High - Strong similarity"
        elif score >= 0.5:
            return "Moderate - Some commonality"
        elif score >= 0.3:
            return "Low - Limited similarity"
        else:
            return "Very Low - Minimal overlap"


# Example usage and testing
if __name__ == "__main__":
    # Initialize engine
    engine = AdvancedSimilarityEngine("/app/workspace/requirements/shared-infrastructure/knowledge-base")
    
    # Example requirements for testing
    req1 = {
        'domain': 'producer-portal',
        'entities': ['driver', 'vehicle', 'quote'],
        'global_requirements': ['GR-52', 'GR-44', 'GR-41'],
        'workflow': {
            'type': 'quote_creation',
            'steps': ['collect_driver_info', 'add_vehicles', 'calculate_rate', 'generate_quote']
        },
        'validations': {
            'driver': {'rules': ['age_check', 'license_valid']},
            'vehicle': {'rules': ['vin_format', 'year_range']}
        },
        'infrastructure': {
            'database': {'tables': ['drivers', 'vehicles', 'quotes']},
            'api': {'endpoints': ['/api/quotes', '/api/drivers']}
        },
        'integrations': ['DCS', 'rating_engine']
    }
    
    req2 = {
        'domain': 'producer-portal',
        'entities': ['driver', 'vehicle', 'policy'],
        'global_requirements': ['GR-52', 'GR-44', 'GR-38'],
        'workflow': {
            'type': 'policy_binding',
            'steps': ['verify_quote', 'collect_payment', 'bind_policy', 'generate_documents']
        },
        'validations': {
            'driver': {'rules': ['age_check', 'mvr_check']},
            'policy': {'rules': ['coverage_limits', 'payment_valid']}
        },
        'infrastructure': {
            'database': {'tables': ['drivers', 'vehicles', 'policies']},
            'api': {'endpoints': ['/api/policies', '/api/drivers']}
        },
        'integrations': ['DCS', 'payment_gateway']
    }
    
    # Calculate similarity
    similarity = engine.calculate_similarity(req1, req2)
    
    print(f"Overall Similarity: {similarity.overall_score:.2f}")
    print(f"Confidence: {similarity.confidence:.2f}")
    print("\nDimension Scores:")
    for dim, score in similarity.dimension_scores.items():
        print(f"  {dim.value}: {score:.2f}")
    print(f"\nMatched Patterns: {similarity.matched_patterns}")
    print(f"\nRecommendations:")
    for rec in similarity.recommendations:
        print(f"  - {rec}")
    
    # Find similar patterns
    print("\n\nFinding similar patterns...")
    similar = engine.find_similar_patterns(req1, threshold=0.5)
    for pattern, score in similar[:3]:
        print(f"\nPattern: {pattern.id}")
        print(f"  Score: {score.overall_score:.2f}")
        print(f"  Domain: {pattern.domain}")
        print(f"  Success Rate: {pattern.success_rate:.2f}")
    
    # Group requirements
    print("\n\nGrouping requirements...")
    requirements = [req1, req2]
    groups = engine.group_similar_requirements(requirements, threshold=0.6)
    print(f"Formed {len(groups)} groups")
    for i, group in enumerate(groups):
        print(f"  Group {i+1}: {len(group)} requirements")