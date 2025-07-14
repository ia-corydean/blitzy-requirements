#!/usr/bin/env python3
"""
Global Requirements Auto-Assignment Engine

This engine automatically identifies and assigns applicable Global Requirements
to new requirements based on content analysis, entity detection, and domain context.

Features:
- Automatic GR detection from requirement content
- Multi-GR assignment with confidence scores
- Domain-specific GR recommendations
- Compliance requirement identification
- GR relationship mapping
"""

import json
import logging
import re
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class GRAssignment:
    """Represents a Global Requirement assignment"""
    gr_id: str
    gr_name: str
    confidence: float
    reason: str
    category: str
    mandatory: bool
    related_grs: List[str] = field(default_factory=list)
    implementation_notes: str = ""


@dataclass
class GRAssignmentResult:
    """Complete GR assignment result for a requirement"""
    requirement_id: str
    assigned_grs: List[GRAssignment]
    coverage_score: float  # How well GRs cover the requirement
    compliance_level: str  # 'full', 'partial', 'minimal'
    missing_coverage: List[str]  # Areas not covered by assigned GRs
    recommendations: List[str]


class GRAutoAssignmentEngine:
    """
    Automatically assigns Global Requirements based on requirement analysis
    """
    
    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.gr_index = {}
        self.gr_patterns = {}
        self.domain_gr_mapping = {}
        self.entity_gr_mapping = {}
        self.keyword_gr_mapping = {}
        self.gr_relationships = {}
        self.vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 3))
        self.gr_vectors = None
        self.load_gr_knowledge()
    
    def load_gr_knowledge(self):
        """Load Global Requirements knowledge base"""
        try:
            # Load GR index
            gr_index_path = self.knowledge_base_path / "global-requirements-index.json"
            if gr_index_path.exists():
                with open(gr_index_path, 'r') as f:
                    gr_data = json.load(f)
                    self.gr_index = gr_data.get('global_requirements', {})
                    self._build_gr_mappings(gr_data)
                    logger.info(f"Loaded {len(self.gr_index)} Global Requirements")
            
            # Load GR patterns
            self._load_gr_patterns()
            
            # Build text vectors for similarity matching
            self._build_gr_vectors()
            
        except Exception as e:
            logger.error(f"Error loading GR knowledge: {e}")
    
    def _build_gr_mappings(self, gr_data: Dict):
        """Build various GR mapping indices"""
        # Domain to GR mapping
        self.domain_gr_mapping = gr_data.get('domain_mapping', {
            'producer-portal': ['GR-52', 'GR-44', 'GR-41', 'GR-38', 'GR-53'],
            'accounting': ['GR-44', 'GR-41', 'GR-33', 'GR-36', 'GR-51'],
            'program-manager': ['GR-38', 'GR-41', 'GR-20', 'GR-27'],
            'program-traits': ['GR-38', 'GR-20', 'GR-52'],
            'entity-integration': ['GR-53', 'GR-52', 'GR-48', 'GR-47'],
            'reinstatement': ['GR-64', 'GR-44', 'GR-41', 'GR-51'],
            'sr22': ['GR-10', 'GR-44', 'GR-51', 'GR-24']
        })
        
        # Entity to GR mapping
        self.entity_gr_mapping = {
            'driver': ['GR-52', 'GR-53', 'GR-41'],
            'vehicle': ['GR-52', 'GR-53', 'GR-41'],
            'quote': ['GR-52', 'GR-44', 'GR-41', 'GR-38'],
            'policy': ['GR-52', 'GR-64', 'GR-44', 'GR-41'],
            'payment': ['GR-44', 'GR-33', 'GR-24', 'GR-51'],
            'billing': ['GR-44', 'GR-33', 'GR-41', 'GR-51'],
            'commission': ['GR-33', 'GR-51', 'GR-41'],
            'sr22': ['GR-10', 'GR-24', 'GR-51'],
            'reinstatement': ['GR-64', 'GR-44', 'GR-51']
        }
        
        # Keyword to GR mapping
        self.keyword_gr_mapping = {
            'database': ['GR-41', 'GR-02', 'GR-03'],
            'api': ['GR-47', 'GR-38', 'GR-53'],
            'security': ['GR-24', 'GR-36', 'GR-01'],
            'authentication': ['GR-01', 'GR-36'],
            'communication': ['GR-44', 'GR-49'],
            'external': ['GR-52', 'GR-53', 'GR-48'],
            'dcs': ['GR-53'],
            'microservice': ['GR-38'],
            'event': ['GR-49', 'GR-21'],
            'validation': ['GR-04', 'GR-05'],
            'testing': ['GR-05', 'GR-10'],
            'performance': ['GR-08', 'GR-27'],
            'compliance': ['GR-51', 'GR-10', 'GR-64'],
            'workflow': ['GR-18', 'GR-20'],
            'docker': ['GR-28', 'GR-29', 'GR-30'],
            'cache': ['GR-33'],
            'audit': ['GR-51', 'GR-02'],
            'disaster': ['GR-50'],
            'locking': ['GR-37']
        }
        
        # GR relationships
        self.gr_relationships = {
            'GR-52': ['GR-41', 'GR-44', 'GR-53'],  # Universal Entity Management
            'GR-44': ['GR-49', 'GR-21', 'GR-52'],  # Communication Architecture
            'GR-41': ['GR-02', 'GR-03', 'GR-52'],  # Database Standards
            'GR-38': ['GR-47', 'GR-52', 'GR-20'],  # Microservice Architecture
            'GR-53': ['GR-52', 'GR-48', 'GR-47'],  # DCS Integration
            'GR-64': ['GR-44', 'GR-51', 'GR-41'],  # Policy Reinstatement
            'GR-10': ['GR-51', 'GR-24', 'GR-44']   # SR22/SR26 Filing
        }
    
    def _load_gr_patterns(self):
        """Load pattern matching rules for GRs"""
        self.gr_patterns = {
            'GR-52': {
                'patterns': [
                    r'external\s+(entity|api|service)',
                    r'universal\s+entity',
                    r'third[- ]party',
                    r'vendor\s+management',
                    r'attorney|body\s+shop|glass\s+vendor'
                ],
                'required_contexts': ['external', 'integration', 'api']
            },
            'GR-44': {
                'patterns': [
                    r'(email|sms|notification)',
                    r'communication\s+(template|workflow)',
                    r'message\s+delivery',
                    r'customer\s+notification'
                ],
                'required_contexts': ['communication', 'notification', 'message']
            },
            'GR-41': {
                'patterns': [
                    r'database\s+(table|schema|design)',
                    r'(table|column)\s+naming',
                    r'foreign\s+key',
                    r'index|indices',
                    r'database\s+standard'
                ],
                'required_contexts': ['database', 'schema', 'table']
            },
            'GR-38': {
                'patterns': [
                    r'microservice',
                    r'service\s+boundary',
                    r'api\s+endpoint',
                    r'service\s+interface'
                ],
                'required_contexts': ['service', 'api', 'microservice']
            },
            'GR-53': {
                'patterns': [
                    r'dcs\s+(integration|api)',
                    r'driver\s+verification',
                    r'household\s+api',
                    r'criminal\s+background'
                ],
                'required_contexts': ['dcs', 'verification', 'external']
            },
            'GR-64': {
                'patterns': [
                    r'(policy\s+)?reinstatement',
                    r'lapse\s+(processing|management)',
                    r'policy\s+lifecycle',
                    r'reinstatement\s+workflow'
                ],
                'required_contexts': ['reinstatement', 'lapse', 'policy']
            },
            'GR-10': {
                'patterns': [
                    r'sr22|sr26',
                    r'financial\s+responsibility',
                    r'filing\s+requirement',
                    r'state\s+filing'
                ],
                'required_contexts': ['sr22', 'filing', 'compliance']
            }
        }
    
    def _build_gr_vectors(self):
        """Build TF-IDF vectors for GR descriptions"""
        if not self.gr_index:
            return
        
        # Collect GR descriptions
        gr_texts = []
        gr_ids = []
        
        for gr_id, gr_data in self.gr_index.items():
            # Combine name, description, and key concepts
            text_parts = [
                gr_data.get('name', ''),
                gr_data.get('description', ''),
                ' '.join(gr_data.get('key_concepts', [])),
                ' '.join(gr_data.get('applies_to', []))
            ]
            
            combined_text = ' '.join(filter(None, text_parts))
            gr_texts.append(combined_text)
            gr_ids.append(gr_id)
        
        # Build vectors
        if gr_texts:
            self.gr_vectors = self.vectorizer.fit_transform(gr_texts)
            self.gr_id_list = gr_ids
    
    def assign_global_requirements(self, requirement: Dict) -> GRAssignmentResult:
        """
        Automatically assign Global Requirements to a requirement
        
        Args:
            requirement: Requirement dictionary
            
        Returns:
            GRAssignmentResult with assigned GRs and analysis
        """
        requirement_id = requirement.get('id', f"req_{id(requirement)}")
        assigned_grs = []
        
        # 1. Domain-based assignment
        domain_grs = self._assign_by_domain(requirement)
        assigned_grs.extend(domain_grs)
        
        # 2. Entity-based assignment
        entity_grs = self._assign_by_entities(requirement)
        assigned_grs.extend(entity_grs)
        
        # 3. Keyword-based assignment
        keyword_grs = self._assign_by_keywords(requirement)
        assigned_grs.extend(keyword_grs)
        
        # 4. Pattern-based assignment
        pattern_grs = self._assign_by_patterns(requirement)
        assigned_grs.extend(pattern_grs)
        
        # 5. Similarity-based assignment
        similarity_grs = self._assign_by_similarity(requirement)
        assigned_grs.extend(similarity_grs)
        
        # 6. Integration-based assignment
        integration_grs = self._assign_by_integrations(requirement)
        assigned_grs.extend(integration_grs)
        
        # Consolidate and deduplicate
        consolidated_grs = self._consolidate_assignments(assigned_grs)
        
        # Add related GRs
        final_grs = self._add_related_grs(consolidated_grs)
        
        # Calculate coverage and compliance
        coverage_score = self._calculate_coverage_score(requirement, final_grs)
        compliance_level = self._determine_compliance_level(coverage_score, final_grs)
        missing_coverage = self._identify_missing_coverage(requirement, final_grs)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(requirement, final_grs, missing_coverage)
        
        return GRAssignmentResult(
            requirement_id=requirement_id,
            assigned_grs=final_grs,
            coverage_score=coverage_score,
            compliance_level=compliance_level,
            missing_coverage=missing_coverage,
            recommendations=recommendations
        )
    
    def _assign_by_domain(self, requirement: Dict) -> List[GRAssignment]:
        """Assign GRs based on domain"""
        assignments = []
        domain = requirement.get('domain', '')
        
        if domain in self.domain_gr_mapping:
            for gr_id in self.domain_gr_mapping[domain]:
                if gr_id in self.gr_index:
                    gr_data = self.gr_index[gr_id]
                    assignment = GRAssignment(
                        gr_id=gr_id,
                        gr_name=gr_data.get('name', ''),
                        confidence=0.8,  # High confidence for domain match
                        reason=f"Standard for {domain} domain",
                        category=gr_data.get('category', 'general'),
                        mandatory=gr_data.get('mandatory', True)
                    )
                    assignments.append(assignment)
        
        return assignments
    
    def _assign_by_entities(self, requirement: Dict) -> List[GRAssignment]:
        """Assign GRs based on entities"""
        assignments = []
        entities = requirement.get('entities', [])
        
        for entity in entities:
            if entity.lower() in self.entity_gr_mapping:
                for gr_id in self.entity_gr_mapping[entity.lower()]:
                    if gr_id in self.gr_index:
                        gr_data = self.gr_index[gr_id]
                        assignment = GRAssignment(
                            gr_id=gr_id,
                            gr_name=gr_data.get('name', ''),
                            confidence=0.85,  # High confidence for entity match
                            reason=f"Required for {entity} entity",
                            category=gr_data.get('category', 'general'),
                            mandatory=True
                        )
                        assignments.append(assignment)
        
        return assignments
    
    def _assign_by_keywords(self, requirement: Dict) -> List[GRAssignment]:
        """Assign GRs based on keywords"""
        assignments = []
        
        # Extract text from requirement
        text = self._extract_requirement_text(requirement).lower()
        
        # Check each keyword
        for keyword, gr_ids in self.keyword_gr_mapping.items():
            if keyword in text:
                for gr_id in gr_ids:
                    if gr_id in self.gr_index:
                        gr_data = self.gr_index[gr_id]
                        
                        # Calculate confidence based on keyword prominence
                        confidence = 0.6
                        if re.search(rf'\b{keyword}\b', text):
                            confidence = 0.7
                        if text.count(keyword) > 2:
                            confidence = 0.8
                        
                        assignment = GRAssignment(
                            gr_id=gr_id,
                            gr_name=gr_data.get('name', ''),
                            confidence=confidence,
                            reason=f"Keyword '{keyword}' detected",
                            category=gr_data.get('category', 'general'),
                            mandatory=False
                        )
                        assignments.append(assignment)
        
        return assignments
    
    def _assign_by_patterns(self, requirement: Dict) -> List[GRAssignment]:
        """Assign GRs based on pattern matching"""
        assignments = []
        text = self._extract_requirement_text(requirement).lower()
        
        for gr_id, pattern_data in self.gr_patterns.items():
            if gr_id not in self.gr_index:
                continue
            
            # Check patterns
            pattern_matches = 0
            total_patterns = len(pattern_data['patterns'])
            
            for pattern in pattern_data['patterns']:
                if re.search(pattern, text, re.IGNORECASE):
                    pattern_matches += 1
            
            # Check required contexts
            context_matches = 0
            required_contexts = pattern_data.get('required_contexts', [])
            
            for context in required_contexts:
                if context in text:
                    context_matches += 1
            
            # Calculate confidence
            if pattern_matches > 0:
                pattern_confidence = pattern_matches / total_patterns
                context_confidence = context_matches / len(required_contexts) if required_contexts else 1.0
                overall_confidence = (pattern_confidence * 0.7 + context_confidence * 0.3)
                
                if overall_confidence > 0.5:
                    gr_data = self.gr_index[gr_id]
                    assignment = GRAssignment(
                        gr_id=gr_id,
                        gr_name=gr_data.get('name', ''),
                        confidence=overall_confidence,
                        reason=f"Pattern match ({pattern_matches}/{total_patterns} patterns)",
                        category=gr_data.get('category', 'general'),
                        mandatory=overall_confidence > 0.8
                    )
                    assignments.append(assignment)
        
        return assignments
    
    def _assign_by_similarity(self, requirement: Dict) -> List[GRAssignment]:
        """Assign GRs based on text similarity"""
        if self.gr_vectors is None:
            return []
        
        assignments = []
        
        # Vectorize requirement text
        req_text = self._extract_requirement_text(requirement)
        if not req_text:
            return []
        
        try:
            req_vector = self.vectorizer.transform([req_text])
            
            # Calculate similarities
            similarities = cosine_similarity(req_vector, self.gr_vectors)[0]
            
            # Get top matches
            top_indices = np.argsort(similarities)[-5:][::-1]  # Top 5
            
            for idx in top_indices:
                if similarities[idx] > 0.3:  # Minimum similarity threshold
                    gr_id = self.gr_id_list[idx]
                    if gr_id in self.gr_index:
                        gr_data = self.gr_index[gr_id]
                        assignment = GRAssignment(
                            gr_id=gr_id,
                            gr_name=gr_data.get('name', ''),
                            confidence=float(similarities[idx]),
                            reason=f"Content similarity ({similarities[idx]:.2f})",
                            category=gr_data.get('category', 'general'),
                            mandatory=False
                        )
                        assignments.append(assignment)
        
        except Exception as e:
            logger.warning(f"Error in similarity matching: {e}")
        
        return assignments
    
    def _assign_by_integrations(self, requirement: Dict) -> List[GRAssignment]:
        """Assign GRs based on integrations"""
        assignments = []
        integrations = requirement.get('integrations', [])
        
        for integration in integrations:
            integration_lower = integration.lower()
            
            # DCS integration
            if 'dcs' in integration_lower:
                if 'GR-53' in self.gr_index:
                    gr_data = self.gr_index['GR-53']
                    assignment = GRAssignment(
                        gr_id='GR-53',
                        gr_name=gr_data.get('name', ''),
                        confidence=0.95,
                        reason="DCS integration detected",
                        category='integration',
                        mandatory=True,
                        implementation_notes="Follow DCS API standards"
                    )
                    assignments.append(assignment)
            
            # External API integration
            if any(term in integration_lower for term in ['api', 'external', 'third']):
                if 'GR-52' in self.gr_index:
                    gr_data = self.gr_index['GR-52']
                    assignment = GRAssignment(
                        gr_id='GR-52',
                        gr_name=gr_data.get('name', ''),
                        confidence=0.9,
                        reason="External integration detected",
                        category='integration',
                        mandatory=True
                    )
                    assignments.append(assignment)
            
            # Payment integration
            if any(term in integration_lower for term in ['payment', 'gateway', 'ach']):
                if 'GR-44' in self.gr_index:
                    gr_data = self.gr_index['GR-44']
                    assignment = GRAssignment(
                        gr_id='GR-44',
                        gr_name=gr_data.get('name', ''),
                        confidence=0.85,
                        reason="Payment communication required",
                        category='communication',
                        mandatory=True
                    )
                    assignments.append(assignment)
        
        return assignments
    
    def _extract_requirement_text(self, requirement: Dict) -> str:
        """Extract all text from requirement"""
        text_parts = []
        
        # Add description and requirement text
        for field in ['description', 'requirement', 'summary', 'details']:
            if field in requirement:
                text_parts.append(str(requirement[field]))
        
        # Add entity names
        if 'entities' in requirement:
            text_parts.extend(requirement['entities'])
        
        # Add workflow information
        if 'workflow' in requirement:
            workflow = requirement['workflow']
            if isinstance(workflow, dict):
                text_parts.append(workflow.get('type', ''))
                text_parts.append(workflow.get('description', ''))
                if 'steps' in workflow:
                    text_parts.extend(str(s) for s in workflow['steps'])
        
        # Add validation information
        if 'validations' in requirement:
            for val_type, val_data in requirement['validations'].items():
                text_parts.append(val_type)
                if isinstance(val_data, dict):
                    text_parts.append(val_data.get('description', ''))
        
        # Add integration names
        if 'integrations' in requirement:
            text_parts.extend(requirement['integrations'])
        
        return ' '.join(filter(None, text_parts))
    
    def _consolidate_assignments(self, assignments: List[GRAssignment]) -> List[GRAssignment]:
        """Consolidate duplicate assignments, keeping highest confidence"""
        consolidated = {}
        
        for assignment in assignments:
            gr_id = assignment.gr_id
            
            if gr_id not in consolidated:
                consolidated[gr_id] = assignment
            else:
                # Keep assignment with higher confidence
                if assignment.confidence > consolidated[gr_id].confidence:
                    # Merge reasons
                    existing_reason = consolidated[gr_id].reason
                    assignment.reason = f"{assignment.reason}; {existing_reason}"
                    consolidated[gr_id] = assignment
                else:
                    # Still merge reasons
                    consolidated[gr_id].reason += f"; {assignment.reason}"
                
                # Update mandatory flag (OR operation)
                consolidated[gr_id].mandatory = consolidated[gr_id].mandatory or assignment.mandatory
        
        return list(consolidated.values())
    
    def _add_related_grs(self, assignments: List[GRAssignment]) -> List[GRAssignment]:
        """Add related GRs based on relationships"""
        final_assignments = assignments.copy()
        assigned_ids = {a.gr_id for a in assignments}
        
        for assignment in assignments:
            if assignment.gr_id in self.gr_relationships:
                related_grs = self.gr_relationships[assignment.gr_id]
                assignment.related_grs = related_grs
                
                # Add highly related GRs if confidence is high
                if assignment.confidence > 0.8:
                    for related_gr in related_grs:
                        if related_gr not in assigned_ids and related_gr in self.gr_index:
                            gr_data = self.gr_index[related_gr]
                            related_assignment = GRAssignment(
                                gr_id=related_gr,
                                gr_name=gr_data.get('name', ''),
                                confidence=assignment.confidence * 0.7,  # Lower confidence for related
                                reason=f"Related to {assignment.gr_id}",
                                category=gr_data.get('category', 'general'),
                                mandatory=False
                            )
                            final_assignments.append(related_assignment)
                            assigned_ids.add(related_gr)
        
        return final_assignments
    
    def _calculate_coverage_score(self, requirement: Dict, assignments: List[GRAssignment]) -> float:
        """Calculate how well GRs cover the requirement"""
        if not assignments:
            return 0.0
        
        # Coverage factors
        coverage_factors = {
            'database': False,
            'api': False,
            'security': False,
            'communication': False,
            'workflow': False,
            'validation': False,
            'compliance': False,
            'integration': False
        }
        
        # Check what's needed
        req_text = self._extract_requirement_text(requirement).lower()
        
        needs_database = any(term in req_text for term in ['database', 'table', 'schema'])
        needs_api = any(term in req_text for term in ['api', 'endpoint', 'service'])
        needs_security = any(term in req_text for term in ['security', 'authentication', 'authorization'])
        needs_communication = any(term in req_text for term in ['email', 'sms', 'notification'])
        needs_workflow = 'workflow' in requirement
        needs_validation = 'validations' in requirement
        needs_compliance = any(term in req_text for term in ['compliance', 'audit', 'filing'])
        needs_integration = 'integrations' in requirement
        
        # Check coverage
        gr_categories = {a.category for a in assignments}
        gr_ids = {a.gr_id for a in assignments}
        
        if needs_database and any(gr in gr_ids for gr in ['GR-41', 'GR-02', 'GR-03']):
            coverage_factors['database'] = True
        
        if needs_api and any(gr in gr_ids for gr in ['GR-38', 'GR-47', 'GR-52']):
            coverage_factors['api'] = True
        
        if needs_security and any(gr in gr_ids for gr in ['GR-24', 'GR-36', 'GR-01']):
            coverage_factors['security'] = True
        
        if needs_communication and any(gr in gr_ids for gr in ['GR-44', 'GR-49']):
            coverage_factors['communication'] = True
        
        if needs_workflow and any(gr in gr_ids for gr in ['GR-18', 'GR-20']):
            coverage_factors['workflow'] = True
        
        if needs_validation and any(gr in gr_ids for gr in ['GR-04', 'GR-05']):
            coverage_factors['validation'] = True
        
        if needs_compliance and any(gr in gr_ids for gr in ['GR-51', 'GR-10', 'GR-64']):
            coverage_factors['compliance'] = True
        
        if needs_integration and any(gr in gr_ids for gr in ['GR-52', 'GR-53', 'GR-48']):
            coverage_factors['integration'] = True
        
        # Calculate score
        needed_factors = sum([
            needs_database, needs_api, needs_security, needs_communication,
            needs_workflow, needs_validation, needs_compliance, needs_integration
        ])
        
        if needed_factors == 0:
            # If no specific needs identified, base on assignment confidence
            return min(sum(a.confidence for a in assignments) / len(assignments), 1.0)
        
        covered_factors = sum(coverage_factors.values())
        return covered_factors / needed_factors
    
    def _determine_compliance_level(self, coverage_score: float, 
                                  assignments: List[GRAssignment]) -> str:
        """Determine overall compliance level"""
        mandatory_grs = [a for a in assignments if a.mandatory]
        high_confidence_grs = [a for a in assignments if a.confidence > 0.8]
        
        if coverage_score >= 0.9 and len(mandatory_grs) >= 3:
            return 'full'
        elif coverage_score >= 0.7 and len(high_confidence_grs) >= 2:
            return 'partial'
        else:
            return 'minimal'
    
    def _identify_missing_coverage(self, requirement: Dict, 
                                 assignments: List[GRAssignment]) -> List[str]:
        """Identify areas not covered by assigned GRs"""
        missing = []
        
        req_text = self._extract_requirement_text(requirement).lower()
        assigned_grs = {a.gr_id for a in assignments}
        
        # Check for missing coverage
        if 'database' in req_text and 'GR-41' not in assigned_grs:
            missing.append("Database standards (GR-41)")
        
        if any(term in req_text for term in ['security', 'authentication']) and 'GR-36' not in assigned_grs:
            missing.append("Security standards (GR-36)")
        
        if 'performance' in req_text and 'GR-27' not in assigned_grs:
            missing.append("Performance requirements (GR-27)")
        
        if 'test' in req_text and 'GR-05' not in assigned_grs:
            missing.append("Testing requirements (GR-05)")
        
        if 'docker' in req_text and not any(gr in assigned_grs for gr in ['GR-28', 'GR-29', 'GR-30']):
            missing.append("Docker requirements (GR-28/29/30)")
        
        if 'disaster' in req_text and 'GR-50' not in assigned_grs:
            missing.append("Disaster recovery (GR-50)")
        
        return missing
    
    def _generate_recommendations(self, requirement: Dict, assignments: List[GRAssignment],
                                missing_coverage: List[str]) -> List[str]:
        """Generate recommendations for GR compliance"""
        recommendations = []
        
        # Check for missing mandatory GRs
        if missing_coverage:
            recommendations.append(f"Consider adding: {', '.join(missing_coverage)}")
        
        # Check for low confidence assignments
        low_confidence = [a for a in assignments if a.confidence < 0.6]
        if low_confidence:
            recommendations.append(f"Review low confidence assignments: {', '.join(a.gr_id for a in low_confidence)}")
        
        # Check for conflicting GRs
        if 'GR-38' in {a.gr_id for a in assignments} and 'monolithic' in self._extract_requirement_text(requirement).lower():
            recommendations.append("Potential conflict: GR-38 (Microservices) with monolithic approach")
        
        # Domain-specific recommendations
        domain = requirement.get('domain', '')
        if domain == 'producer-portal' and 'GR-52' not in {a.gr_id for a in assignments}:
            recommendations.append("Producer Portal should follow GR-52 for external entities")
        
        if domain == 'accounting' and 'GR-51' not in {a.gr_id for a in assignments}:
            recommendations.append("Accounting domain should include GR-51 for compliance")
        
        # Integration recommendations
        if requirement.get('integrations') and 'GR-48' not in {a.gr_id for a in assignments}:
            recommendations.append("External integrations should reference GR-48")
        
        return recommendations
    
    def get_gr_details(self, gr_id: str) -> Optional[Dict]:
        """Get detailed information about a Global Requirement"""
        if gr_id in self.gr_index:
            return self.gr_index[gr_id]
        return None
    
    def export_assignment_report(self, requirement: Dict, result: GRAssignmentResult) -> Dict:
        """Export detailed GR assignment report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'requirement_id': result.requirement_id,
            'requirement_summary': {
                'domain': requirement.get('domain', 'unknown'),
                'entities': requirement.get('entities', []),
                'integrations': requirement.get('integrations', []),
                'has_workflow': 'workflow' in requirement,
                'has_validations': 'validations' in requirement
            },
            'assignment_summary': {
                'total_grs_assigned': len(result.assigned_grs),
                'mandatory_grs': len([a for a in result.assigned_grs if a.mandatory]),
                'coverage_score': result.coverage_score,
                'compliance_level': result.compliance_level
            },
            'assigned_grs': [
                {
                    'gr_id': a.gr_id,
                    'gr_name': a.gr_name,
                    'confidence': a.confidence,
                    'reason': a.reason,
                    'category': a.category,
                    'mandatory': a.mandatory,
                    'related_grs': a.related_grs,
                    'implementation_notes': a.implementation_notes
                }
                for a in sorted(result.assigned_grs, key=lambda x: x.confidence, reverse=True)
            ],
            'coverage_analysis': {
                'areas_covered': [
                    a.category for a in result.assigned_grs
                ],
                'missing_coverage': result.missing_coverage,
                'coverage_percentage': f"{result.coverage_score * 100:.1f}%"
            },
            'recommendations': result.recommendations,
            'implementation_guidance': self._generate_implementation_guidance(result.assigned_grs)
        }
        
        return report
    
    def _generate_implementation_guidance(self, assignments: List[GRAssignment]) -> List[str]:
        """Generate implementation guidance based on assigned GRs"""
        guidance = []
        gr_ids = {a.gr_id for a in assignments}
        
        if 'GR-52' in gr_ids:
            guidance.append("Implement universal entity patterns for all external entities")
        
        if 'GR-44' in gr_ids:
            guidance.append("Use standardized communication templates and tracking")
        
        if 'GR-41' in gr_ids:
            guidance.append("Follow database naming conventions and include audit fields")
        
        if 'GR-38' in gr_ids:
            guidance.append("Design with microservice boundaries and API contracts")
        
        if 'GR-53' in gr_ids:
            guidance.append("Follow DCS integration patterns and error handling")
        
        if 'GR-64' in gr_ids:
            guidance.append("Implement complete reinstatement workflow with validation")
        
        if 'GR-10' in gr_ids:
            guidance.append("Include SR22/SR26 filing requirements and state compliance")
        
        return guidance


# Example usage and testing
if __name__ == "__main__":
    # Initialize engine
    engine = GRAutoAssignmentEngine("/app/workspace/requirements/shared-infrastructure/knowledge-base")
    
    # Example requirement
    requirement = {
        'id': 'req_001',
        'domain': 'producer-portal',
        'description': 'Implement driver information update workflow with DCS verification',
        'entities': ['driver', 'vehicle', 'quote'],
        'workflow': {
            'type': 'driver_update',
            'steps': ['collect_info', 'verify_dcs', 'update_database', 'notify_customer']
        },
        'integrations': ['DCS', 'email_service'],
        'validations': {
            'driver': {'rules': ['age_check', 'license_valid']},
            'dcs': {'rules': ['api_response', 'data_match']}
        },
        'infrastructure': {
            'database': ['drivers', 'vehicles'],
            'api': ['/api/drivers', '/api/dcs/verify']
        }
    }
    
    # Assign Global Requirements
    print("Assigning Global Requirements...")
    result = engine.assign_global_requirements(requirement)
    
    print(f"\nRequirement: {result.requirement_id}")
    print(f"Coverage Score: {result.coverage_score:.2f}")
    print(f"Compliance Level: {result.compliance_level}")
    
    print(f"\nAssigned GRs ({len(result.assigned_grs)}):")
    for assignment in sorted(result.assigned_grs, key=lambda x: x.confidence, reverse=True):
        mandatory = "MANDATORY" if assignment.mandatory else "Optional"
        print(f"  - {assignment.gr_id}: {assignment.gr_name}")
        print(f"    Confidence: {assignment.confidence:.2f} ({mandatory})")
        print(f"    Reason: {assignment.reason}")
        if assignment.related_grs:
            print(f"    Related: {', '.join(assignment.related_grs)}")
    
    if result.missing_coverage:
        print(f"\nMissing Coverage:")
        for missing in result.missing_coverage:
            print(f"  - {missing}")
    
    print(f"\nRecommendations:")
    for rec in result.recommendations:
        print(f"  - {rec}")
    
    # Generate report
    print("\n\nGenerating assignment report...")
    report = engine.export_assignment_report(requirement, result)
    
    print(f"\nImplementation Guidance:")
    for guide in report['implementation_guidance']:
        print(f"  - {guide}")
    
    # Test another requirement
    print("\n\n" + "="*50)
    print("Testing SR22 filing requirement...")
    
    sr22_requirement = {
        'id': 'req_002',
        'domain': 'sr22',
        'description': 'Implement SR22 filing workflow with state compliance tracking',
        'entities': ['driver', 'policy', 'sr22'],
        'workflow': {
            'type': 'sr22_filing',
            'steps': ['validate_requirement', 'prepare_filing', 'submit_state', 'track_status']
        },
        'integrations': ['state_filing_api'],
        'validations': {
            'compliance': {'rules': ['state_requirements', 'filing_deadlines']}
        }
    }
    
    sr22_result = engine.assign_global_requirements(sr22_requirement)
    print(f"\nSR22 Requirement GRs: {', '.join(a.gr_id for a in sr22_result.assigned_grs)}")
    print(f"Compliance Level: {sr22_result.compliance_level}")