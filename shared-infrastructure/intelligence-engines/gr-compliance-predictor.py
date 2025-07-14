#!/usr/bin/env python3
"""
Global Requirements Compliance Predictor

This engine predicts potential compliance issues with Global Requirements
before implementation, enabling proactive remediation and reducing rework.

Features:
- Early compliance issue detection
- Risk assessment for GR violations
- Remediation suggestions
- Compliance confidence scoring
- Historical learning from past violations
"""

import json
import logging
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
import pickle

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ComplianceIssue:
    """Represents a predicted compliance issue"""
    gr_id: str
    gr_name: str
    issue_type: str  # 'missing', 'incomplete', 'incorrect', 'conflict'
    severity: str  # 'critical', 'high', 'medium', 'low'
    confidence: float
    description: str
    affected_areas: List[str]
    remediation_steps: List[str]
    estimated_effort: str  # 'hours', 'days', 'weeks'


@dataclass
class CompliancePrediction:
    """Complete compliance prediction for a requirement"""
    requirement_id: str
    overall_compliance_score: float  # 0-1, higher is better
    risk_level: str  # 'low', 'medium', 'high', 'critical'
    predicted_issues: List[ComplianceIssue]
    compliance_by_gr: Dict[str, float]  # GR ID -> compliance score
    recommendations: List[str]
    estimated_remediation_time: str
    confidence_level: float


class GRCompliancePredictor:
    """
    Predicts compliance issues with Global Requirements
    """
    
    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.gr_index = {}
        self.compliance_patterns = {}
        self.violation_history = defaultdict(list)
        self.ml_models = {}
        self.feature_extractors = {}
        self.load_compliance_knowledge()
    
    def load_compliance_knowledge(self):
        """Load compliance patterns and historical data"""
        try:
            # Load GR index
            gr_index_path = self.knowledge_base_path / "global-requirements-index.json"
            if gr_index_path.exists():
                with open(gr_index_path, 'r') as f:
                    gr_data = json.load(f)
                    self.gr_index = gr_data.get('global_requirements', {})
            
            # Load compliance patterns
            self._load_compliance_patterns()
            
            # Load violation history
            self._load_violation_history()
            
            # Initialize ML models
            self._initialize_ml_models()
            
            logger.info("Compliance knowledge loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading compliance knowledge: {e}")
    
    def _load_compliance_patterns(self):
        """Load patterns for compliance checking"""
        self.compliance_patterns = {
            'GR-52': {  # Universal Entity Management
                'required_elements': ['entity_type', 'metadata_schema', 'configuration_hierarchy'],
                'common_violations': [
                    'missing_metadata_schema',
                    'incorrect_entity_type',
                    'no_universal_pattern'
                ],
                'validation_rules': [
                    'external_entities_must_use_universal_pattern',
                    'metadata_schema_required_for_ui',
                    'three_level_configuration_hierarchy'
                ]
            },
            'GR-44': {  # Communication Architecture
                'required_elements': ['template_id', 'tracking', 'delivery_method'],
                'common_violations': [
                    'missing_template',
                    'no_tracking_mechanism',
                    'hardcoded_messages'
                ],
                'validation_rules': [
                    'use_templated_communications',
                    'implement_delivery_tracking',
                    'support_multiple_channels'
                ]
            },
            'GR-41': {  # Database Standards
                'required_elements': ['naming_convention', 'audit_fields', 'indexes'],
                'common_violations': [
                    'incorrect_naming',
                    'missing_audit_fields',
                    'no_foreign_keys'
                ],
                'validation_rules': [
                    'snake_case_table_names',
                    'include_created_updated_by',
                    'define_all_relationships'
                ]
            },
            'GR-38': {  # Microservice Architecture
                'required_elements': ['service_boundary', 'api_contract', 'event_handling'],
                'common_violations': [
                    'unclear_boundaries',
                    'missing_api_documentation',
                    'synchronous_everything'
                ],
                'validation_rules': [
                    'clear_service_boundaries',
                    'documented_api_contracts',
                    'event_driven_communication'
                ]
            },
            'GR-53': {  # DCS Integration
                'required_elements': ['error_handling', 'retry_logic', 'data_mapping'],
                'common_violations': [
                    'no_error_handling',
                    'missing_retry_logic',
                    'incorrect_field_mapping'
                ],
                'validation_rules': [
                    'comprehensive_error_handling',
                    'exponential_backoff_retry',
                    'validated_data_mapping'
                ]
            }
        }
    
    def _load_violation_history(self):
        """Load historical violation data"""
        history_path = self.knowledge_base_path / "performance-metrics/violation-history.json"
        if history_path.exists():
            try:
                with open(history_path, 'r') as f:
                    history_data = json.load(f)
                    
                    for gr_id, violations in history_data.items():
                        self.violation_history[gr_id] = violations
                
                logger.info(f"Loaded violation history for {len(self.violation_history)} GRs")
            except Exception as e:
                logger.warning(f"Could not load violation history: {e}")
    
    def _initialize_ml_models(self):
        """Initialize machine learning models for prediction"""
        # Initialize feature extractors
        self.feature_extractors = {
            'text': CountVectorizer(max_features=100, ngram_range=(1, 2)),
            'entities': CountVectorizer(tokenizer=lambda x: x, lowercase=False),
            'keywords': CountVectorizer(vocabulary=self._get_compliance_keywords())
        }
        
        # Try to load pre-trained models
        models_path = self.knowledge_base_path / "ml-models"
        if models_path.exists():
            for gr_id in ['GR-52', 'GR-44', 'GR-41', 'GR-38']:
                model_file = models_path / f"compliance_model_{gr_id}.pkl"
                if model_file.exists():
                    try:
                        with open(model_file, 'rb') as f:
                            self.ml_models[gr_id] = pickle.load(f)
                    except:
                        self.ml_models[gr_id] = self._create_default_model()
                else:
                    self.ml_models[gr_id] = self._create_default_model()
        else:
            # Create default models
            for gr_id in self.compliance_patterns:
                self.ml_models[gr_id] = self._create_default_model()
    
    def _create_default_model(self):
        """Create a default compliance prediction model"""
        return RandomForestClassifier(
            n_estimators=50,
            max_depth=10,
            random_state=42
        )
    
    def _get_compliance_keywords(self):
        """Get keywords relevant to compliance"""
        return [
            'audit', 'tracking', 'validation', 'error', 'retry',
            'template', 'naming', 'convention', 'security', 'performance',
            'integration', 'api', 'database', 'service', 'boundary',
            'configuration', 'metadata', 'schema', 'universal', 'pattern'
        ]
    
    def predict_compliance(self, requirement: Dict, assigned_grs: List[str]) -> CompliancePrediction:
        """
        Predict compliance issues for a requirement
        
        Args:
            requirement: Requirement dictionary
            assigned_grs: List of assigned Global Requirement IDs
            
        Returns:
            CompliancePrediction with detailed analysis
        """
        requirement_id = requirement.get('id', f"req_{id(requirement)}")
        predicted_issues = []
        compliance_by_gr = {}
        
        # Analyze compliance for each assigned GR
        for gr_id in assigned_grs:
            if gr_id in self.compliance_patterns:
                gr_compliance, gr_issues = self._analyze_gr_compliance(requirement, gr_id)
                compliance_by_gr[gr_id] = gr_compliance
                predicted_issues.extend(gr_issues)
        
        # Check for cross-GR conflicts
        conflict_issues = self._check_gr_conflicts(requirement, assigned_grs)
        predicted_issues.extend(conflict_issues)
        
        # Calculate overall compliance score
        if compliance_by_gr:
            overall_compliance = sum(compliance_by_gr.values()) / len(compliance_by_gr)
        else:
            overall_compliance = 1.0  # No GRs to check
        
        # Determine risk level
        risk_level = self._calculate_risk_level(overall_compliance, predicted_issues)
        
        # Generate recommendations
        recommendations = self._generate_compliance_recommendations(
            requirement, predicted_issues, compliance_by_gr
        )
        
        # Estimate remediation time
        remediation_time = self._estimate_remediation_time(predicted_issues)
        
        # Calculate confidence level
        confidence = self._calculate_prediction_confidence(requirement, assigned_grs)
        
        return CompliancePrediction(
            requirement_id=requirement_id,
            overall_compliance_score=overall_compliance,
            risk_level=risk_level,
            predicted_issues=predicted_issues,
            compliance_by_gr=compliance_by_gr,
            recommendations=recommendations,
            estimated_remediation_time=remediation_time,
            confidence_level=confidence
        )
    
    def _analyze_gr_compliance(self, requirement: Dict, gr_id: str) -> Tuple[float, List[ComplianceIssue]]:
        """Analyze compliance for a specific GR"""
        issues = []
        compliance_score = 1.0
        
        if gr_id not in self.compliance_patterns:
            return compliance_score, issues
        
        pattern = self.compliance_patterns[gr_id]
        gr_name = self.gr_index.get(gr_id, {}).get('name', gr_id)
        
        # Check required elements
        missing_elements = self._check_required_elements(requirement, gr_id, pattern)
        for element, confidence in missing_elements:
            issues.append(ComplianceIssue(
                gr_id=gr_id,
                gr_name=gr_name,
                issue_type='missing',
                severity='high' if confidence > 0.8 else 'medium',
                confidence=confidence,
                description=f"Missing required element: {element}",
                affected_areas=[element],
                remediation_steps=self._get_remediation_steps(gr_id, 'missing', element),
                estimated_effort='hours'
            ))
            compliance_score -= 0.2
        
        # Check common violations using ML if available
        if gr_id in self.ml_models:
            violation_predictions = self._predict_violations_ml(requirement, gr_id)
            for violation, confidence in violation_predictions:
                if confidence > 0.6:
                    issues.append(ComplianceIssue(
                        gr_id=gr_id,
                        gr_name=gr_name,
                        issue_type='incorrect',
                        severity=self._determine_violation_severity(violation),
                        confidence=confidence,
                        description=f"Potential violation: {violation}",
                        affected_areas=self._get_affected_areas(requirement, violation),
                        remediation_steps=self._get_remediation_steps(gr_id, 'violation', violation),
                        estimated_effort='days'
                    ))
                    compliance_score -= 0.15
        
        # Check validation rules
        rule_violations = self._check_validation_rules(requirement, gr_id, pattern)
        for rule, confidence in rule_violations:
            issues.append(ComplianceIssue(
                gr_id=gr_id,
                gr_name=gr_name,
                issue_type='incomplete',
                severity='medium',
                confidence=confidence,
                description=f"Validation rule not satisfied: {rule}",
                affected_areas=self._get_rule_affected_areas(rule),
                remediation_steps=self._get_remediation_steps(gr_id, 'rule', rule),
                estimated_effort='hours'
            ))
            compliance_score -= 0.1
        
        # Ensure score stays in valid range
        compliance_score = max(0.0, min(1.0, compliance_score))
        
        return compliance_score, issues
    
    def _check_required_elements(self, requirement: Dict, gr_id: str, 
                                pattern: Dict) -> List[Tuple[str, float]]:
        """Check for missing required elements"""
        missing = []
        required_elements = pattern.get('required_elements', [])
        
        # Extract requirement content
        req_text = self._extract_requirement_content(requirement)
        
        for element in required_elements:
            confidence = 0.0
            
            # Check based on GR-specific rules
            if gr_id == 'GR-52' and element == 'metadata_schema':
                if 'metadata' not in req_text and 'schema' not in req_text:
                    confidence = 0.9
            
            elif gr_id == 'GR-44' and element == 'template_id':
                if 'template' not in req_text and not requirement.get('communication_template'):
                    confidence = 0.85
            
            elif gr_id == 'GR-41' and element == 'audit_fields':
                tables = requirement.get('infrastructure', {}).get('database', {}).get('tables', [])
                if tables and 'created_by' not in req_text and 'updated_by' not in req_text:
                    confidence = 0.95
            
            elif gr_id == 'GR-38' and element == 'service_boundary':
                if 'service' not in req_text or 'boundary' not in req_text:
                    confidence = 0.8
            
            elif gr_id == 'GR-53' and element == 'error_handling':
                if 'error' not in req_text and 'exception' not in req_text:
                    confidence = 0.9
            
            if confidence > 0.6:
                missing.append((element, confidence))
        
        return missing
    
    def _predict_violations_ml(self, requirement: Dict, gr_id: str) -> List[Tuple[str, float]]:
        """Use ML model to predict violations"""
        violations = []
        
        if gr_id not in self.ml_models:
            return violations
        
        try:
            # Extract features
            features = self._extract_ml_features(requirement)
            
            # Get model and predict
            model = self.ml_models[gr_id]
            
            # For now, use rule-based prediction as fallback
            # In production, this would use the trained model
            common_violations = self.compliance_patterns[gr_id].get('common_violations', [])
            
            req_text = self._extract_requirement_content(requirement).lower()
            
            for violation in common_violations:
                confidence = 0.0
                
                if violation == 'missing_metadata_schema' and 'metadata' not in req_text:
                    confidence = 0.8
                elif violation == 'no_tracking_mechanism' and 'tracking' not in req_text:
                    confidence = 0.75
                elif violation == 'incorrect_naming' and not self._check_naming_convention(requirement):
                    confidence = 0.85
                elif violation == 'no_error_handling' and 'error' not in req_text:
                    confidence = 0.7
                
                if confidence > 0.0:
                    violations.append((violation, confidence))
        
        except Exception as e:
            logger.warning(f"ML prediction failed for {gr_id}: {e}")
        
        return violations
    
    def _check_validation_rules(self, requirement: Dict, gr_id: str, 
                              pattern: Dict) -> List[Tuple[str, float]]:
        """Check validation rules for compliance"""
        violations = []
        rules = pattern.get('validation_rules', [])
        
        for rule in rules:
            confidence = self._evaluate_validation_rule(requirement, gr_id, rule)
            if confidence > 0.6:
                violations.append((rule, confidence))
        
        return violations
    
    def _evaluate_validation_rule(self, requirement: Dict, gr_id: str, rule: str) -> float:
        """Evaluate a specific validation rule"""
        req_text = self._extract_requirement_content(requirement).lower()
        
        # GR-52 rules
        if rule == 'external_entities_must_use_universal_pattern':
            entities = requirement.get('entities', [])
            external_keywords = ['external', 'api', 'third party', 'vendor']
            
            for entity in entities:
                if any(keyword in req_text for keyword in external_keywords):
                    if 'universal' not in req_text and 'pattern' not in req_text:
                        return 0.9
        
        # GR-44 rules
        elif rule == 'use_templated_communications':
            if any(term in req_text for term in ['email', 'sms', 'notification']):
                if 'template' not in req_text:
                    return 0.85
        
        # GR-41 rules
        elif rule == 'snake_case_table_names':
            tables = requirement.get('infrastructure', {}).get('database', {}).get('tables', [])
            for table in tables:
                if not self._is_snake_case(table):
                    return 0.95
        
        # GR-38 rules
        elif rule == 'clear_service_boundaries':
            if 'microservice' in req_text or 'service' in req_text:
                if 'boundary' not in req_text and 'interface' not in req_text:
                    return 0.8
        
        # GR-53 rules
        elif rule == 'exponential_backoff_retry':
            if 'dcs' in req_text or 'external' in req_text:
                if 'retry' not in req_text and 'backoff' not in req_text:
                    return 0.85
        
        return 0.0
    
    def _check_gr_conflicts(self, requirement: Dict, assigned_grs: List[str]) -> List[ComplianceIssue]:
        """Check for conflicts between assigned GRs"""
        conflicts = []
        
        # Check for known conflicting GR combinations
        conflicting_pairs = [
            ('GR-38', 'monolithic'),  # Microservices vs monolithic
            ('GR-49', 'synchronous'),  # Event-driven vs synchronous
            ('GR-52', 'internal_only')  # Universal entities vs internal-only
        ]
        
        req_text = self._extract_requirement_content(requirement).lower()
        
        for gr_id, conflict_term in conflicting_pairs:
            if gr_id in assigned_grs and conflict_term in req_text:
                gr_name = self.gr_index.get(gr_id, {}).get('name', gr_id)
                conflicts.append(ComplianceIssue(
                    gr_id=gr_id,
                    gr_name=gr_name,
                    issue_type='conflict',
                    severity='high',
                    confidence=0.8,
                    description=f"Potential conflict: {gr_name} with {conflict_term} approach",
                    affected_areas=['architecture'],
                    remediation_steps=[
                        f"Resolve conflict between {gr_name} and {conflict_term} approach",
                        f"Choose either {gr_name} pattern or adjust requirement"
                    ],
                    estimated_effort='days'
                ))
        
        return conflicts
    
    def _extract_requirement_content(self, requirement: Dict) -> str:
        """Extract all text content from requirement"""
        parts = []
        
        # Add text fields
        for field in ['description', 'requirement', 'details', 'summary']:
            if field in requirement:
                parts.append(str(requirement[field]))
        
        # Add workflow info
        if 'workflow' in requirement:
            workflow = requirement['workflow']
            if isinstance(workflow, dict):
                parts.append(workflow.get('type', ''))
                parts.append(workflow.get('description', ''))
                if 'steps' in workflow:
                    parts.extend(str(s) for s in workflow['steps'])
        
        # Add infrastructure info
        if 'infrastructure' in requirement:
            infra = requirement['infrastructure']
            if isinstance(infra, dict):
                if 'database' in infra:
                    parts.append(str(infra['database']))
                if 'api' in infra:
                    parts.append(str(infra['api']))
        
        return ' '.join(filter(None, parts))
    
    def _extract_ml_features(self, requirement: Dict) -> np.ndarray:
        """Extract features for ML prediction"""
        # This is a simplified version - in production would use proper feature engineering
        features = []
        
        # Text features
        req_text = self._extract_requirement_content(requirement)
        text_vec = self.feature_extractors['text'].fit_transform([req_text])
        features.extend(text_vec.toarray()[0])
        
        # Entity features
        entities = requirement.get('entities', [])
        entity_vec = self.feature_extractors['entities'].fit_transform([entities])
        features.extend(entity_vec.toarray()[0])
        
        # Numeric features
        features.append(len(requirement.get('entities', [])))
        features.append(len(requirement.get('integrations', [])))
        features.append(len(requirement.get('validations', {})))
        features.append(1 if 'workflow' in requirement else 0)
        
        return np.array(features)
    
    def _check_naming_convention(self, requirement: Dict) -> bool:
        """Check if naming conventions are followed"""
        tables = requirement.get('infrastructure', {}).get('database', {}).get('tables', [])
        
        for table in tables:
            if not self._is_snake_case(table):
                return False
        
        return True
    
    def _is_snake_case(self, name: str) -> bool:
        """Check if name follows snake_case convention"""
        import re
        return bool(re.match(r'^[a-z]+(_[a-z]+)*$', name))
    
    def _determine_violation_severity(self, violation: str) -> str:
        """Determine severity of a violation"""
        critical_violations = ['no_error_handling', 'missing_security', 'no_audit_trail']
        high_violations = ['incorrect_naming', 'missing_metadata_schema', 'no_tracking_mechanism']
        
        if violation in critical_violations:
            return 'critical'
        elif violation in high_violations:
            return 'high'
        else:
            return 'medium'
    
    def _get_affected_areas(self, requirement: Dict, violation: str) -> List[str]:
        """Get areas affected by a violation"""
        areas = []
        
        if 'naming' in violation:
            areas.append('database')
        if 'tracking' in violation or 'communication' in violation:
            areas.append('communication')
        if 'error' in violation or 'retry' in violation:
            areas.append('integration')
        if 'metadata' in violation or 'schema' in violation:
            areas.append('entity_management')
        if 'service' in violation or 'boundary' in violation:
            areas.append('architecture')
        
        return areas if areas else ['general']
    
    def _get_rule_affected_areas(self, rule: str) -> List[str]:
        """Get areas affected by a rule violation"""
        rule_area_map = {
            'external_entities_must_use_universal_pattern': ['entity_management'],
            'use_templated_communications': ['communication'],
            'snake_case_table_names': ['database'],
            'clear_service_boundaries': ['architecture'],
            'exponential_backoff_retry': ['integration']
        }
        
        return rule_area_map.get(rule, ['general'])
    
    def _get_remediation_steps(self, gr_id: str, issue_type: str, detail: str) -> List[str]:
        """Get remediation steps for an issue"""
        steps = []
        
        if issue_type == 'missing':
            if detail == 'metadata_schema':
                steps.extend([
                    "Define metadata schema for the entity",
                    "Include all required fields for UI generation",
                    "Follow the universal entity pattern structure"
                ])
            elif detail == 'template_id':
                steps.extend([
                    "Create communication template",
                    "Register template in the system",
                    "Update requirement to reference template ID"
                ])
            elif detail == 'audit_fields':
                steps.extend([
                    "Add created_by and updated_by fields to tables",
                    "Add created_at and updated_at timestamps",
                    "Ensure fields are populated on insert/update"
                ])
        
        elif issue_type == 'violation':
            if detail == 'incorrect_naming':
                steps.extend([
                    "Update table/column names to snake_case",
                    "Create migration script for renaming",
                    "Update all references in code"
                ])
            elif detail == 'no_error_handling':
                steps.extend([
                    "Implement comprehensive error handling",
                    "Add try-catch blocks for external calls",
                    "Define error response formats"
                ])
        
        elif issue_type == 'rule':
            if 'template' in detail:
                steps.extend([
                    "Replace hardcoded messages with templates",
                    "Implement template variable substitution",
                    "Test all communication scenarios"
                ])
            elif 'service' in detail:
                steps.extend([
                    "Define clear service boundaries",
                    "Document service interfaces",
                    "Implement API contracts"
                ])
        
        return steps if steps else ["Review and update to comply with " + gr_id]
    
    def _calculate_risk_level(self, compliance_score: float, 
                            issues: List[ComplianceIssue]) -> str:
        """Calculate overall risk level"""
        critical_issues = sum(1 for i in issues if i.severity == 'critical')
        high_issues = sum(1 for i in issues if i.severity == 'high')
        
        if critical_issues > 0 or compliance_score < 0.5:
            return 'critical'
        elif high_issues > 2 or compliance_score < 0.7:
            return 'high'
        elif high_issues > 0 or compliance_score < 0.85:
            return 'medium'
        else:
            return 'low'
    
    def _generate_compliance_recommendations(self, requirement: Dict,
                                           issues: List[ComplianceIssue],
                                           compliance_by_gr: Dict[str, float]) -> List[str]:
        """Generate recommendations for improving compliance"""
        recommendations = []
        
        # General recommendations based on compliance scores
        low_compliance_grs = [gr for gr, score in compliance_by_gr.items() if score < 0.7]
        if low_compliance_grs:
            recommendations.append(f"Focus on improving compliance for: {', '.join(low_compliance_grs)}")
        
        # Issue-specific recommendations
        critical_issues = [i for i in issues if i.severity == 'critical']
        if critical_issues:
            recommendations.append("Address critical issues immediately before implementation")
        
        # Pattern-based recommendations
        issue_types = {i.issue_type for i in issues}
        if 'missing' in issue_types:
            recommendations.append("Review GR requirements and add missing elements")
        
        if 'conflict' in issue_types:
            recommendations.append("Resolve architectural conflicts before proceeding")
        
        # Domain-specific recommendations
        domain = requirement.get('domain', '')
        if domain == 'entity-integration' and any(i.gr_id == 'GR-53' for i in issues):
            recommendations.append("Ensure DCS integration follows established patterns")
        
        if domain == 'producer-portal' and any(i.gr_id == 'GR-52' for i in issues):
            recommendations.append("Apply universal entity patterns for all external entities")
        
        return recommendations
    
    def _estimate_remediation_time(self, issues: List[ComplianceIssue]) -> str:
        """Estimate time to remediate all issues"""
        total_hours = 0
        
        for issue in issues:
            if issue.estimated_effort == 'hours':
                if issue.severity == 'critical':
                    total_hours += 8
                elif issue.severity == 'high':
                    total_hours += 4
                else:
                    total_hours += 2
            elif issue.estimated_effort == 'days':
                if issue.severity == 'critical':
                    total_hours += 24
                elif issue.severity == 'high':
                    total_hours += 16
                else:
                    total_hours += 8
            elif issue.estimated_effort == 'weeks':
                total_hours += 40
        
        if total_hours == 0:
            return "None required"
        elif total_hours <= 8:
            return f"{total_hours} hours"
        elif total_hours <= 40:
            return f"{total_hours / 8:.1f} days"
        else:
            return f"{total_hours / 40:.1f} weeks"
    
    def _calculate_prediction_confidence(self, requirement: Dict, 
                                       assigned_grs: List[str]) -> float:
        """Calculate confidence in the prediction"""
        confidence_factors = []
        
        # Factor 1: Completeness of requirement
        req_completeness = self._calculate_requirement_completeness(requirement)
        confidence_factors.append(req_completeness)
        
        # Factor 2: Coverage of assigned GRs
        covered_grs = [gr for gr in assigned_grs if gr in self.compliance_patterns]
        gr_coverage = len(covered_grs) / len(assigned_grs) if assigned_grs else 0
        confidence_factors.append(gr_coverage)
        
        # Factor 3: Historical data availability
        historical_coverage = sum(
            1 for gr in assigned_grs 
            if gr in self.violation_history and len(self.violation_history[gr]) > 10
        ) / len(assigned_grs) if assigned_grs else 0
        confidence_factors.append(historical_coverage * 0.5 + 0.5)  # Weighted
        
        return sum(confidence_factors) / len(confidence_factors)
    
    def _calculate_requirement_completeness(self, requirement: Dict) -> float:
        """Calculate how complete the requirement specification is"""
        fields = ['description', 'entities', 'workflow', 'validations', 'infrastructure']
        present = sum(1 for f in fields if f in requirement and requirement[f])
        return present / len(fields)
    
    def learn_from_violation(self, requirement_id: str, gr_id: str, 
                           actual_violation: str, was_predicted: bool):
        """Learn from actual violations to improve predictions"""
        violation_record = {
            'requirement_id': requirement_id,
            'timestamp': datetime.now().isoformat(),
            'violation': actual_violation,
            'was_predicted': was_predicted
        }
        
        self.violation_history[gr_id].append(violation_record)
        
        # In production, would retrain ML models periodically
        logger.info(f"Recorded violation for {gr_id}: {actual_violation} (predicted: {was_predicted})")
    
    def export_compliance_report(self, requirement: Dict, prediction: CompliancePrediction) -> Dict:
        """Export detailed compliance prediction report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'requirement_id': prediction.requirement_id,
            'summary': {
                'overall_compliance_score': prediction.overall_compliance_score,
                'risk_level': prediction.risk_level,
                'total_issues': len(prediction.predicted_issues),
                'critical_issues': len([i for i in prediction.predicted_issues if i.severity == 'critical']),
                'estimated_remediation_time': prediction.estimated_remediation_time,
                'confidence_level': prediction.confidence_level
            },
            'gr_compliance': {
                gr_id: {
                    'score': score,
                    'status': 'compliant' if score >= 0.8 else 'non-compliant',
                    'issues': [
                        {
                            'type': i.issue_type,
                            'severity': i.severity,
                            'description': i.description,
                            'confidence': i.confidence
                        }
                        for i in prediction.predicted_issues if i.gr_id == gr_id
                    ]
                }
                for gr_id, score in prediction.compliance_by_gr.items()
            },
            'detailed_issues': [
                {
                    'gr_id': issue.gr_id,
                    'gr_name': issue.gr_name,
                    'issue_type': issue.issue_type,
                    'severity': issue.severity,
                    'confidence': issue.confidence,
                    'description': issue.description,
                    'affected_areas': issue.affected_areas,
                    'remediation_steps': issue.remediation_steps,
                    'estimated_effort': issue.estimated_effort
                }
                for issue in sorted(prediction.predicted_issues, 
                                  key=lambda x: ('critical', 'high', 'medium', 'low').index(x.severity))
            ],
            'recommendations': prediction.recommendations,
            'remediation_plan': self._generate_remediation_plan(prediction.predicted_issues)
        }
        
        return report
    
    def _generate_remediation_plan(self, issues: List[ComplianceIssue]) -> List[Dict]:
        """Generate a prioritized remediation plan"""
        plan = []
        
        # Group by severity
        severity_groups = defaultdict(list)
        for issue in issues:
            severity_groups[issue.severity].append(issue)
        
        # Create plan entries
        priority = 1
        for severity in ['critical', 'high', 'medium', 'low']:
            for issue in severity_groups[severity]:
                plan.append({
                    'priority': priority,
                    'gr_id': issue.gr_id,
                    'issue': issue.description,
                    'severity': issue.severity,
                    'estimated_effort': issue.estimated_effort,
                    'steps': issue.remediation_steps
                })
                priority += 1
        
        return plan


# Example usage and testing
if __name__ == "__main__":
    # Initialize predictor
    predictor = GRCompliancePredictor("/app/workspace/requirements/shared-infrastructure/knowledge-base")
    
    # Example requirement
    requirement = {
        'id': 'req_001',
        'domain': 'producer-portal',
        'description': 'Create external vendor management system for body shops',
        'entities': ['vendor', 'body_shop', 'claim'],
        'workflow': {
            'type': 'vendor_management',
            'steps': ['register_vendor', 'validate_credentials', 'assign_claims']
        },
        'integrations': ['external_api'],
        'infrastructure': {
            'database': {
                'tables': ['Vendors', 'BodyShops', 'VendorClaims']  # Wrong naming!
            },
            'api': ['/api/vendors']
        }
    }
    
    # Assigned GRs
    assigned_grs = ['GR-52', 'GR-41', 'GR-44', 'GR-38']
    
    # Predict compliance
    print("Predicting compliance issues...")
    prediction = predictor.predict_compliance(requirement, assigned_grs)
    
    print(f"\nRequirement: {prediction.requirement_id}")
    print(f"Overall Compliance Score: {prediction.overall_compliance_score:.2f}")
    print(f"Risk Level: {prediction.risk_level}")
    print(f"Confidence: {prediction.confidence_level:.2f}")
    
    print(f"\nCompliance by GR:")
    for gr_id, score in prediction.compliance_by_gr.items():
        status = "✓" if score >= 0.8 else "✗"
        print(f"  {status} {gr_id}: {score:.2f}")
    
    print(f"\nPredicted Issues ({len(prediction.predicted_issues)}):")
    for issue in prediction.predicted_issues:
        print(f"\n  [{issue.severity.upper()}] {issue.gr_id} - {issue.description}")
        print(f"    Confidence: {issue.confidence:.2f}")
        print(f"    Affected: {', '.join(issue.affected_areas)}")
        print(f"    Remediation steps:")
        for step in issue.remediation_steps:
            print(f"      - {step}")
    
    print(f"\nEstimated Remediation Time: {prediction.estimated_remediation_time}")
    
    print(f"\nRecommendations:")
    for rec in prediction.recommendations:
        print(f"  - {rec}")
    
    # Generate report
    print("\n\nGenerating compliance report...")
    report = predictor.export_compliance_report(requirement, prediction)
    
    print(f"\nRemediation Plan:")
    for item in report['remediation_plan'][:5]:  # First 5 items
        print(f"  {item['priority']}. [{item['severity']}] {item['issue']}")
        print(f"     Effort: {item['estimated_effort']}")
    
    # Test learning from violation
    print("\n\nRecording actual violation...")
    predictor.learn_from_violation('req_001', 'GR-41', 'incorrect_table_naming', was_predicted=True)