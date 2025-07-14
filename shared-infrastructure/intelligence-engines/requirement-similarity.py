#!/usr/bin/env python3
"""
Requirement Similarity Calculator

This engine calculates similarity between requirements to enable intelligent
grouping, batch processing, and pattern reuse across the system.

Features:
- Multi-requirement comparison
- Similarity matrix generation
- Clustering for batch groups
- Cross-domain similarity detection
- Processing optimization recommendations
"""

import json
import logging
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import numpy as np
from collections import defaultdict
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class RequirementSimilarity:
    """Similarity between two requirements"""
    req1_id: str
    req2_id: str
    overall_similarity: float
    text_similarity: float
    entity_similarity: float
    gr_similarity: float
    workflow_similarity: float
    domain_compatibility: float
    batch_compatible: bool
    processing_order: Optional[int] = None
    shared_resources: List[str] = field(default_factory=list)


@dataclass
class BatchGroup:
    """Group of requirements for batch processing"""
    group_id: str
    requirements: List[Dict]
    similarity_threshold: float
    group_type: str  # 'high_similarity', 'same_domain', 'shared_entities', 'workflow_sequence'
    processing_priority: int
    estimated_time_savings: float
    shared_context: Dict = field(default_factory=dict)


class RequirementSimilarityCalculator:
    """
    Calculate and analyze similarity between requirements
    for optimal batch processing and pattern reuse
    """
    
    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.entity_catalog = {}
        self.gr_index = {}
        self.domain_relationships = {}
        self.workflow_patterns = {}
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load knowledge base for similarity calculations"""
        try:
            # Load entity catalog
            entity_catalog_path = self.knowledge_base_path / "universal-entity-catalog.json"
            if entity_catalog_path.exists():
                with open(entity_catalog_path, 'r') as f:
                    catalog_data = json.load(f)
                    self.entity_catalog = catalog_data.get('entities', {})
            
            # Load GR index
            gr_index_path = self.knowledge_base_path / "global-requirements-index.json"
            if gr_index_path.exists():
                with open(gr_index_path, 'r') as f:
                    gr_data = json.load(f)
                    self.gr_index = gr_data.get('global_requirements', {})
            
            # Load cross-domain relationships
            relationships_path = self.knowledge_base_path / "cross-domain-relationships/relationship-map.json"
            if relationships_path.exists():
                with open(relationships_path, 'r') as f:
                    rel_data = json.load(f)
                    self.domain_relationships = rel_data
            
            logger.info("Knowledge base loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
    
    def calculate_pairwise_similarity(self, req1: Dict, req2: Dict) -> RequirementSimilarity:
        """
        Calculate comprehensive similarity between two requirements
        
        Args:
            req1: First requirement
            req2: Second requirement
            
        Returns:
            RequirementSimilarity object with detailed scores
        """
        # Extract requirement IDs
        req1_id = req1.get('id', f"req_{id(req1)}")
        req2_id = req2.get('id', f"req_{id(req2)}")
        
        # Calculate different similarity dimensions
        text_sim = self._calculate_text_similarity(req1, req2)
        entity_sim = self._calculate_entity_similarity(req1, req2)
        gr_sim = self._calculate_gr_similarity(req1, req2)
        workflow_sim = self._calculate_workflow_similarity(req1, req2)
        domain_compat = self._calculate_domain_compatibility(req1, req2)
        
        # Calculate overall similarity with weights
        weights = {
            'text': 0.15,
            'entity': 0.30,
            'gr': 0.25,
            'workflow': 0.20,
            'domain': 0.10
        }
        
        overall_sim = (
            text_sim * weights['text'] +
            entity_sim * weights['entity'] +
            gr_sim * weights['gr'] +
            workflow_sim * weights['workflow'] +
            domain_compat * weights['domain']
        )
        
        # Determine batch compatibility
        batch_compatible = self._check_batch_compatibility(
            req1, req2, overall_sim, entity_sim, domain_compat
        )
        
        # Identify shared resources
        shared_resources = self._identify_shared_resources(req1, req2)
        
        return RequirementSimilarity(
            req1_id=req1_id,
            req2_id=req2_id,
            overall_similarity=overall_sim,
            text_similarity=text_sim,
            entity_similarity=entity_sim,
            gr_similarity=gr_sim,
            workflow_similarity=workflow_sim,
            domain_compatibility=domain_compat,
            batch_compatible=batch_compatible,
            shared_resources=shared_resources
        )
    
    def _calculate_text_similarity(self, req1: Dict, req2: Dict) -> float:
        """Calculate text-based similarity using TF-IDF"""
        # Combine all text fields
        text1 = self._extract_text(req1)
        text2 = self._extract_text(req2)
        
        if not text1 or not text2:
            return 0.0
        
        try:
            # Vectorize and calculate cosine similarity
            vectors = self.vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            return float(similarity)
        except:
            # Fallback to simple word overlap
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            if not words1 or not words2:
                return 0.0
            
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            return len(intersection) / len(union)
    
    def _extract_text(self, requirement: Dict) -> str:
        """Extract all text content from requirement"""
        text_parts = []
        
        # Add description
        if 'description' in requirement:
            text_parts.append(str(requirement['description']))
        
        # Add requirement details
        if 'requirement' in requirement:
            text_parts.append(str(requirement['requirement']))
        
        # Add entity names
        if 'entities' in requirement:
            text_parts.extend(requirement['entities'])
        
        # Add workflow descriptions
        if 'workflow' in requirement:
            workflow = requirement['workflow']
            if isinstance(workflow, dict):
                if 'description' in workflow:
                    text_parts.append(workflow['description'])
                if 'steps' in workflow:
                    text_parts.extend(str(s) for s in workflow['steps'])
        
        # Add validation descriptions
        if 'validations' in requirement:
            for val_type, val_data in requirement['validations'].items():
                if isinstance(val_data, dict) and 'description' in val_data:
                    text_parts.append(val_data['description'])
        
        return ' '.join(text_parts)
    
    def _calculate_entity_similarity(self, req1: Dict, req2: Dict) -> float:
        """Calculate similarity based on shared entities"""
        entities1 = set(req1.get('entities', []))
        entities2 = set(req2.get('entities', []))
        
        if not entities1 and not entities2:
            return 1.0  # Both have no entities
        
        if not entities1 or not entities2:
            return 0.0
        
        # Direct overlap
        common = entities1.intersection(entities2)
        total = entities1.union(entities2)
        
        direct_similarity = len(common) / len(total)
        
        # Consider entity relationships
        relationship_boost = 0.0
        for e1 in entities1:
            for e2 in entities2:
                if self._are_entities_related(e1, e2):
                    relationship_boost += 0.1
        
        return min(direct_similarity + relationship_boost, 1.0)
    
    def _are_entities_related(self, entity1: str, entity2: str) -> bool:
        """Check if two entities are related"""
        if entity1 == entity2:
            return True
        
        # Check catalog relationships
        if entity1 in self.entity_catalog:
            related = self.entity_catalog[entity1].get('related_entities', [])
            if entity2 in related:
                return True
        
        # Check cross-domain relationships
        for rel in self.domain_relationships.get('relationships', []):
            if (rel['source_entity'] == entity1 and rel['target_entity'] == entity2) or \
               (rel['source_entity'] == entity2 and rel['target_entity'] == entity1):
                return True
        
        return False
    
    def _calculate_gr_similarity(self, req1: Dict, req2: Dict) -> float:
        """Calculate similarity based on Global Requirements"""
        grs1 = set(req1.get('global_requirements', []))
        grs2 = set(req2.get('global_requirements', []))
        
        if not grs1 and not grs2:
            return 1.0  # Both have no GRs
        
        if not grs1 or not grs2:
            return 0.0
        
        # Direct overlap
        common = grs1.intersection(grs2)
        total = grs1.union(grs2)
        
        direct_similarity = len(common) / len(total)
        
        # Consider GR categories
        category_boost = 0.0
        categories1 = {self.gr_index.get(gr, {}).get('category') for gr in grs1}
        categories2 = {self.gr_index.get(gr, {}).get('category') for gr in grs2}
        
        categories1.discard(None)
        categories2.discard(None)
        
        if categories1 and categories2:
            common_categories = categories1.intersection(categories2)
            if common_categories:
                category_boost = len(common_categories) / max(len(categories1), len(categories2)) * 0.2
        
        return min(direct_similarity + category_boost, 1.0)
    
    def _calculate_workflow_similarity(self, req1: Dict, req2: Dict) -> float:
        """Calculate similarity based on workflow patterns"""
        workflow1 = req1.get('workflow', {})
        workflow2 = req2.get('workflow', {})
        
        if not workflow1 and not workflow2:
            return 1.0
        
        if not workflow1 or not workflow2:
            return 0.0
        
        similarity_score = 0.0
        comparisons = 0
        
        # Compare workflow type
        if 'type' in workflow1 and 'type' in workflow2:
            if workflow1['type'] == workflow2['type']:
                similarity_score += 1.0
            comparisons += 1
        
        # Compare workflow steps
        if 'steps' in workflow1 and 'steps' in workflow2:
            steps1 = workflow1['steps'] if isinstance(workflow1['steps'], list) else []
            steps2 = workflow2['steps'] if isinstance(workflow2['steps'], list) else []
            
            if steps1 and steps2:
                # Check for common steps
                common_steps = set(steps1).intersection(set(steps2))
                step_similarity = len(common_steps) / max(len(steps1), len(steps2))
                
                # Check for sequence similarity
                sequence_similarity = self._calculate_sequence_similarity(steps1, steps2)
                
                similarity_score += (step_similarity + sequence_similarity) / 2
                comparisons += 1
        
        # Compare triggers
        if 'trigger' in workflow1 and 'trigger' in workflow2:
            if workflow1['trigger'] == workflow2['trigger']:
                similarity_score += 1.0
            comparisons += 1
        
        return similarity_score / comparisons if comparisons > 0 else 0.0
    
    def _calculate_sequence_similarity(self, seq1: List, seq2: List) -> float:
        """Calculate similarity between two sequences"""
        if not seq1 or not seq2:
            return 0.0
        
        # Use longest common subsequence
        m, n = len(seq1), len(seq2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i-1] == seq2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        lcs_length = dp[m][n]
        return lcs_length / max(m, n)
    
    def _calculate_domain_compatibility(self, req1: Dict, req2: Dict) -> float:
        """Calculate domain compatibility for batch processing"""
        domain1 = req1.get('domain', '')
        domain2 = req2.get('domain', '')
        
        if not domain1 or not domain2:
            return 0.5  # Unknown compatibility
        
        if domain1 == domain2:
            return 1.0
        
        # Check domain relationships
        domain_compatibility = {
            ('producer-portal', 'accounting'): 0.8,
            ('producer-portal', 'entity-integration'): 0.7,
            ('accounting', 'reinstatement'): 0.8,
            ('program-manager', 'program-traits'): 0.9,
            ('entity-integration', 'sr22'): 0.6,
            ('producer-portal', 'reinstatement'): 0.6
        }
        
        # Check both directions
        compat = domain_compatibility.get((domain1, domain2), 
                 domain_compatibility.get((domain2, domain1), 0.3))
        
        return compat
    
    def _check_batch_compatibility(self, req1: Dict, req2: Dict, 
                                  overall_sim: float, entity_sim: float, 
                                  domain_compat: float) -> bool:
        """Determine if requirements can be batch processed together"""
        # High similarity requirements
        if overall_sim >= 0.7:
            return True
        
        # Same domain with good entity overlap
        if domain_compat >= 1.0 and entity_sim >= 0.5:
            return True
        
        # Shared critical entities
        critical_entities = ['quote', 'policy', 'driver', 'vehicle']
        entities1 = set(req1.get('entities', []))
        entities2 = set(req2.get('entities', []))
        
        critical_overlap = entities1.intersection(entities2).intersection(critical_entities)
        if len(critical_overlap) >= 2:
            return True
        
        # Sequential workflow steps
        if self._are_sequential_workflows(req1, req2):
            return True
        
        return False
    
    def _are_sequential_workflows(self, req1: Dict, req2: Dict) -> bool:
        """Check if requirements have sequential workflows"""
        workflow1 = req1.get('workflow', {})
        workflow2 = req2.get('workflow', {})
        
        if not workflow1 or not workflow2:
            return False
        
        # Check for explicit sequencing
        if workflow1.get('next_workflow') == workflow2.get('type'):
            return True
        
        if workflow2.get('previous_workflow') == workflow1.get('type'):
            return True
        
        # Check for common patterns
        sequential_patterns = [
            ('quote_creation', 'quote_binding'),
            ('quote_binding', 'policy_issuance'),
            ('policy_issuance', 'billing_setup'),
            ('driver_collection', 'vehicle_collection'),
            ('rate_calculation', 'quote_generation')
        ]
        
        type1 = workflow1.get('type', '')
        type2 = workflow2.get('type', '')
        
        return (type1, type2) in sequential_patterns
    
    def _identify_shared_resources(self, req1: Dict, req2: Dict) -> List[str]:
        """Identify resources shared between requirements"""
        shared = []
        
        # Shared entities
        entities1 = set(req1.get('entities', []))
        entities2 = set(req2.get('entities', []))
        shared_entities = entities1.intersection(entities2)
        shared.extend(f"entity:{e}" for e in shared_entities)
        
        # Shared integrations
        integrations1 = set(req1.get('integrations', []))
        integrations2 = set(req2.get('integrations', []))
        shared_integrations = integrations1.intersection(integrations2)
        shared.extend(f"integration:{i}" for i in shared_integrations)
        
        # Shared infrastructure
        infra1 = req1.get('infrastructure', {})
        infra2 = req2.get('infrastructure', {})
        
        # Database tables
        tables1 = set(infra1.get('database', {}).get('tables', []))
        tables2 = set(infra2.get('database', {}).get('tables', []))
        shared_tables = tables1.intersection(tables2)
        shared.extend(f"table:{t}" for t in shared_tables)
        
        # API endpoints
        apis1 = set(infra1.get('api', {}).get('endpoints', []))
        apis2 = set(infra2.get('api', {}).get('endpoints', []))
        shared_apis = apis1.intersection(apis2)
        shared.extend(f"api:{a}" for a in shared_apis)
        
        return shared
    
    def create_similarity_matrix(self, requirements: List[Dict]) -> np.ndarray:
        """
        Create similarity matrix for multiple requirements
        
        Args:
            requirements: List of requirements
            
        Returns:
            NxN similarity matrix
        """
        n = len(requirements)
        matrix = np.zeros((n, n))
        
        for i in range(n):
            matrix[i][i] = 1.0  # Self-similarity
            
            for j in range(i + 1, n):
                similarity = self.calculate_pairwise_similarity(
                    requirements[i], requirements[j]
                )
                matrix[i][j] = similarity.overall_similarity
                matrix[j][i] = similarity.overall_similarity
        
        return matrix
    
    def create_batch_groups(self, requirements: List[Dict], 
                          similarity_threshold: float = 0.6,
                          max_group_size: int = 10) -> List[BatchGroup]:
        """
        Create optimal batch groups from requirements
        
        Args:
            requirements: List of requirements to group
            similarity_threshold: Minimum similarity for grouping
            max_group_size: Maximum requirements per group
            
        Returns:
            List of batch groups
        """
        if len(requirements) <= 1:
            return [BatchGroup(
                group_id="batch_single",
                requirements=requirements,
                similarity_threshold=1.0,
                group_type='single',
                processing_priority=1,
                estimated_time_savings=0.0
            )]
        
        # Create similarity graph
        G = nx.Graph()
        
        # Add nodes
        for i, req in enumerate(requirements):
            G.add_node(i, requirement=req)
        
        # Add edges for similar requirements
        for i in range(len(requirements)):
            for j in range(i + 1, len(requirements)):
                similarity = self.calculate_pairwise_similarity(
                    requirements[i], requirements[j]
                )
                
                if similarity.overall_similarity >= similarity_threshold and similarity.batch_compatible:
                    G.add_edge(i, j, weight=similarity.overall_similarity)
        
        # Find connected components (natural groups)
        components = list(nx.connected_components(G))
        
        batch_groups = []
        
        for comp_idx, component in enumerate(components):
            # Split large components if needed
            component_list = list(component)
            
            if len(component_list) > max_group_size:
                # Use spectral clustering for large groups
                subgroups = self._split_large_group(
                    [requirements[i] for i in component_list],
                    max_group_size
                )
                
                for subgroup_idx, subgroup in enumerate(subgroups):
                    batch_groups.append(self._create_batch_group(
                        subgroup,
                        f"batch_{comp_idx}_{subgroup_idx}",
                        similarity_threshold
                    ))
            else:
                group_requirements = [requirements[i] for i in component_list]
                batch_groups.append(self._create_batch_group(
                    group_requirements,
                    f"batch_{comp_idx}",
                    similarity_threshold
                ))
        
        # Sort by priority
        batch_groups.sort(key=lambda g: g.processing_priority, reverse=True)
        
        return batch_groups
    
    def _split_large_group(self, requirements: List[Dict], 
                          max_size: int) -> List[List[Dict]]:
        """Split large group into smaller subgroups"""
        if len(requirements) <= max_size:
            return [requirements]
        
        # Create similarity matrix for the group
        matrix = self.create_similarity_matrix(requirements)
        
        # Simple greedy clustering
        subgroups = []
        unassigned = set(range(len(requirements)))
        
        while unassigned:
            # Start new subgroup with random unassigned requirement
            current_group = [unassigned.pop()]
            
            # Add most similar requirements until size limit
            while len(current_group) < max_size and unassigned:
                # Find most similar unassigned requirement
                best_idx = None
                best_sim = 0
                
                for idx in unassigned:
                    # Average similarity to current group
                    avg_sim = np.mean([matrix[idx][g_idx] for g_idx in current_group])
                    if avg_sim > best_sim:
                        best_sim = avg_sim
                        best_idx = idx
                
                if best_idx is not None and best_sim >= 0.5:
                    current_group.append(best_idx)
                    unassigned.remove(best_idx)
                else:
                    break
            
            subgroups.append([requirements[i] for i in current_group])
        
        return subgroups
    
    def _create_batch_group(self, requirements: List[Dict], 
                           group_id: str,
                           similarity_threshold: float) -> BatchGroup:
        """Create a batch group with metadata"""
        if not requirements:
            raise ValueError("Cannot create empty batch group")
        
        # Determine group type
        group_type = self._determine_group_type(requirements)
        
        # Calculate priority based on group characteristics
        priority = self._calculate_group_priority(requirements, group_type)
        
        # Estimate time savings
        time_savings = self._estimate_time_savings(requirements, group_type)
        
        # Extract shared context
        shared_context = self._extract_shared_context(requirements)
        
        return BatchGroup(
            group_id=group_id,
            requirements=requirements,
            similarity_threshold=similarity_threshold,
            group_type=group_type,
            processing_priority=priority,
            estimated_time_savings=time_savings,
            shared_context=shared_context
        )
    
    def _determine_group_type(self, requirements: List[Dict]) -> str:
        """Determine the type of batch group"""
        if len(requirements) == 1:
            return 'single'
        
        # Check if all same domain
        domains = {req.get('domain') for req in requirements}
        if len(domains) == 1:
            return 'same_domain'
        
        # Check for high entity overlap
        all_entities = [set(req.get('entities', [])) for req in requirements]
        if all_entities:
            common_entities = set.intersection(*all_entities)
            if len(common_entities) >= 2:
                return 'shared_entities'
        
        # Check for workflow sequence
        workflow_types = [req.get('workflow', {}).get('type') for req in requirements]
        if self._is_workflow_sequence(workflow_types):
            return 'workflow_sequence'
        
        return 'high_similarity'
    
    def _is_workflow_sequence(self, workflow_types: List[str]) -> bool:
        """Check if workflows form a sequence"""
        if not all(workflow_types):
            return False
        
        # Known sequences
        known_sequences = [
            ['quote_creation', 'quote_binding', 'policy_issuance'],
            ['driver_collection', 'vehicle_collection', 'rate_calculation'],
            ['policy_update', 'endorsement_creation', 'billing_adjustment']
        ]
        
        for sequence in known_sequences:
            if all(wf in sequence for wf in workflow_types):
                # Check if in order
                indices = [sequence.index(wf) for wf in workflow_types]
                if indices == sorted(indices):
                    return True
        
        return False
    
    def _calculate_group_priority(self, requirements: List[Dict], 
                                 group_type: str) -> int:
        """Calculate processing priority for a group"""
        base_priority = {
            'workflow_sequence': 100,
            'shared_entities': 80,
            'same_domain': 60,
            'high_similarity': 40,
            'single': 20
        }.get(group_type, 0)
        
        # Boost for critical requirements
        critical_boost = sum(
            10 for req in requirements 
            if req.get('priority') == 'critical'
        )
        
        # Boost for time-sensitive workflows
        time_sensitive = ['quote_creation', 'payment_processing', 'reinstatement']
        time_boost = sum(
            5 for req in requirements
            if req.get('workflow', {}).get('type') in time_sensitive
        )
        
        return base_priority + critical_boost + time_boost
    
    def _estimate_time_savings(self, requirements: List[Dict], 
                              group_type: str) -> float:
        """Estimate time savings from batch processing"""
        if len(requirements) <= 1:
            return 0.0
        
        # Base savings by group type
        base_savings = {
            'workflow_sequence': 0.4,  # 40% savings
            'shared_entities': 0.35,
            'same_domain': 0.25,
            'high_similarity': 0.20,
            'single': 0.0
        }.get(group_type, 0.1)
        
        # Scale by group size (diminishing returns)
        size_factor = min(len(requirements) / 10, 1.0)
        
        # Factor in shared resources
        shared_resources = set()
        for req in requirements:
            shared_resources.update(req.get('entities', []))
            shared_resources.update(req.get('integrations', []))
        
        resource_factor = min(len(shared_resources) / 20, 0.2)
        
        return base_savings * (1 + size_factor * 0.5) + resource_factor
    
    def _extract_shared_context(self, requirements: List[Dict]) -> Dict:
        """Extract context shared by all requirements in group"""
        shared_context = {}
        
        # Shared domain
        domains = {req.get('domain') for req in requirements}
        if len(domains) == 1:
            shared_context['domain'] = domains.pop()
        
        # Shared entities
        all_entities = [set(req.get('entities', [])) for req in requirements]
        if all_entities:
            common_entities = list(set.intersection(*all_entities))
            if common_entities:
                shared_context['shared_entities'] = common_entities
        
        # Shared GRs
        all_grs = [set(req.get('global_requirements', [])) for req in requirements]
        if all_grs:
            common_grs = list(set.intersection(*all_grs))
            if common_grs:
                shared_context['shared_global_requirements'] = common_grs
        
        # Shared integrations
        all_integrations = [set(req.get('integrations', [])) for req in requirements]
        if all_integrations:
            common_integrations = list(set.intersection(*all_integrations))
            if common_integrations:
                shared_context['shared_integrations'] = common_integrations
        
        # Workflow information
        workflow_types = [req.get('workflow', {}).get('type') for req in requirements]
        if workflow_types:
            shared_context['workflow_types'] = list(set(workflow_types))
        
        return shared_context
    
    def recommend_processing_order(self, batch_groups: List[BatchGroup]) -> List[BatchGroup]:
        """
        Recommend optimal processing order for batch groups
        
        Args:
            batch_groups: List of batch groups
            
        Returns:
            Ordered list of batch groups
        """
        # Already sorted by priority in create_batch_groups
        # Additional ordering considerations
        
        ordered_groups = []
        remaining_groups = batch_groups.copy()
        
        # Process workflow sequences first
        workflow_sequences = [g for g in remaining_groups if g.group_type == 'workflow_sequence']
        for seq in sorted(workflow_sequences, key=lambda g: g.processing_priority, reverse=True):
            ordered_groups.append(seq)
            remaining_groups.remove(seq)
        
        # Then shared entity groups
        shared_entity_groups = [g for g in remaining_groups if g.group_type == 'shared_entities']
        for group in sorted(shared_entity_groups, key=lambda g: len(g.requirements), reverse=True):
            ordered_groups.append(group)
            remaining_groups.remove(group)
        
        # Add remaining groups by priority
        ordered_groups.extend(sorted(remaining_groups, key=lambda g: g.processing_priority, reverse=True))
        
        # Set processing order
        for idx, group in enumerate(ordered_groups):
            for req in group.requirements:
                if 'processing_order' not in req:
                    req['processing_order'] = idx
        
        return ordered_groups
    
    def export_similarity_analysis(self, requirements: List[Dict]) -> Dict:
        """Generate comprehensive similarity analysis report"""
        analysis_start = datetime.now()
        
        # Create similarity matrix
        similarity_matrix = self.create_similarity_matrix(requirements)
        
        # Create batch groups
        batch_groups = self.create_batch_groups(requirements)
        
        # Order groups
        ordered_groups = self.recommend_processing_order(batch_groups)
        
        # Calculate statistics
        total_requirements = len(requirements)
        total_groups = len(batch_groups)
        avg_group_size = sum(len(g.requirements) for g in batch_groups) / total_groups if total_groups > 0 else 0
        
        # Calculate total estimated savings
        total_savings = sum(g.estimated_time_savings for g in batch_groups) / total_groups if total_groups > 0 else 0
        
        analysis_time = (datetime.now() - analysis_start).total_seconds()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'analysis_time_seconds': analysis_time,
            'total_requirements': total_requirements,
            'total_batch_groups': total_groups,
            'average_group_size': avg_group_size,
            'estimated_time_savings': f"{total_savings * 100:.1f}%",
            'similarity_statistics': {
                'mean_similarity': float(np.mean(similarity_matrix)),
                'max_similarity': float(np.max(similarity_matrix[similarity_matrix < 1.0])) if total_requirements > 1 else 0,
                'min_similarity': float(np.min(similarity_matrix))
            },
            'group_distribution': {
                group_type: sum(1 for g in batch_groups if g.group_type == group_type)
                for group_type in ['single', 'same_domain', 'shared_entities', 'workflow_sequence', 'high_similarity']
            },
            'batch_groups': [
                {
                    'group_id': g.group_id,
                    'size': len(g.requirements),
                    'type': g.group_type,
                    'priority': g.processing_priority,
                    'estimated_savings': f"{g.estimated_time_savings * 100:.1f}%",
                    'shared_context': g.shared_context,
                    'requirement_ids': [r.get('id', f"req_{i}") for i, r in enumerate(g.requirements)]
                }
                for g in ordered_groups
            ],
            'processing_recommendations': [
                f"Process {total_groups} batch groups in recommended order",
                f"Expected time savings: {total_savings * 100:.1f}% overall",
                f"Largest group has {max(len(g.requirements) for g in batch_groups)} requirements" if batch_groups else "No groups formed",
                f"Consider parallel processing for {sum(1 for g in batch_groups if g.group_type == 'same_domain')} same-domain groups"
            ]
        }
        
        return report


# Example usage and testing
if __name__ == "__main__":
    # Initialize calculator
    calculator = RequirementSimilarityCalculator("/app/workspace/requirements/shared-infrastructure/knowledge-base")
    
    # Example requirements
    requirements = [
        {
            'id': 'req_001',
            'domain': 'producer-portal',
            'entities': ['driver', 'vehicle', 'quote'],
            'global_requirements': ['GR-52', 'GR-44'],
            'workflow': {
                'type': 'quote_creation',
                'steps': ['collect_driver', 'add_vehicles', 'calculate_rate']
            },
            'integrations': ['DCS', 'rating_engine'],
            'description': 'Create new quote with driver and vehicle information'
        },
        {
            'id': 'req_002',
            'domain': 'producer-portal',
            'entities': ['driver', 'vehicle', 'quote', 'policy'],
            'global_requirements': ['GR-52', 'GR-44', 'GR-38'],
            'workflow': {
                'type': 'quote_binding',
                'steps': ['verify_quote', 'collect_payment', 'bind_policy']
            },
            'integrations': ['payment_gateway', 'policy_system'],
            'description': 'Bind quote to create policy with payment'
        },
        {
            'id': 'req_003',
            'domain': 'accounting',
            'entities': ['payment', 'billing', 'policy'],
            'global_requirements': ['GR-44', 'GR-41'],
            'workflow': {
                'type': 'billing_setup',
                'steps': ['create_billing_cycle', 'schedule_payments', 'send_invoice']
            },
            'integrations': ['payment_gateway', 'email_service'],
            'description': 'Set up billing for new policy'
        },
        {
            'id': 'req_004',
            'domain': 'producer-portal',
            'entities': ['driver', 'license'],
            'global_requirements': ['GR-52', 'GR-53'],
            'workflow': {
                'type': 'driver_verification',
                'steps': ['collect_license', 'verify_with_dcs', 'update_driver']
            },
            'integrations': ['DCS'],
            'description': 'Verify driver license through DCS'
        }
    ]
    
    # Test pairwise similarity
    print("Testing pairwise similarity...")
    similarity = calculator.calculate_pairwise_similarity(requirements[0], requirements[1])
    print(f"\nSimilarity between req_001 and req_002:")
    print(f"  Overall: {similarity.overall_similarity:.2f}")
    print(f"  Text: {similarity.text_similarity:.2f}")
    print(f"  Entity: {similarity.entity_similarity:.2f}")
    print(f"  GR: {similarity.gr_similarity:.2f}")
    print(f"  Workflow: {similarity.workflow_similarity:.2f}")
    print(f"  Batch Compatible: {similarity.batch_compatible}")
    print(f"  Shared Resources: {similarity.shared_resources}")
    
    # Test batch grouping
    print("\n\nTesting batch grouping...")
    batch_groups = calculator.create_batch_groups(requirements)
    
    print(f"\nCreated {len(batch_groups)} batch groups:")
    for group in batch_groups:
        print(f"\n{group.group_id}:")
        print(f"  Type: {group.group_type}")
        print(f"  Size: {len(group.requirements)}")
        print(f"  Priority: {group.processing_priority}")
        print(f"  Time Savings: {group.estimated_time_savings * 100:.1f}%")
        print(f"  Requirements: {[r['id'] for r in group.requirements]}")
        print(f"  Shared Context: {group.shared_context}")
    
    # Generate report
    print("\n\nGenerating similarity analysis report...")
    report = calculator.export_similarity_analysis(requirements)
    
    print(f"\nAnalysis completed in {report['analysis_time_seconds']:.2f} seconds")
    print(f"Total requirements: {report['total_requirements']}")
    print(f"Batch groups formed: {report['total_batch_groups']}")
    print(f"Estimated time savings: {report['estimated_time_savings']}")
    print("\nRecommendations:")
    for rec in report['processing_recommendations']:
        print(f"  - {rec}")