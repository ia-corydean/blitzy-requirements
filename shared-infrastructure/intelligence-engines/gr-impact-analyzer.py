#!/usr/bin/env python3
"""
Global Requirements Impact Analyzer

This engine analyzes the impact of changes to Global Requirements across
the entire system, helping teams understand ripple effects and plan updates.

Features:
- GR change impact assessment
- Affected component identification
- Risk analysis for GR modifications
- Dependency chain visualization
- Update coordination recommendations
"""

import json
import logging
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from collections import defaultdict, deque
import networkx as nx
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChangeType(Enum):
    """Types of changes to Global Requirements"""
    ADD_CONSTRAINT = "add_constraint"
    REMOVE_CONSTRAINT = "remove_constraint"
    MODIFY_VALIDATION = "modify_validation"
    UPDATE_THRESHOLD = "update_threshold"
    CHANGE_SCOPE = "change_scope"
    DEPRECATE = "deprecate"
    ENHANCE = "enhance"


class ImpactLevel(Enum):
    """Levels of impact from GR changes"""
    CRITICAL = "critical"  # Breaking changes
    HIGH = "high"  # Significant changes requiring updates
    MEDIUM = "medium"  # Moderate changes with workarounds
    LOW = "low"  # Minor changes with minimal impact
    NONE = "none"  # No impact


@dataclass
class AffectedComponent:
    """Component affected by GR change"""
    component_id: str
    component_type: str  # 'requirement', 'entity', 'workflow', 'validation'
    domain: str
    impact_level: ImpactLevel
    required_changes: List[str]
    estimated_effort: str  # 'hours', 'days', 'weeks'
    risk_factors: List[str]
    dependencies: List[str] = field(default_factory=list)


@dataclass
class GRChange:
    """Represents a change to a Global Requirement"""
    gr_id: str
    gr_name: str
    change_type: ChangeType
    description: str
    old_value: Any
    new_value: Any
    rationale: str
    effective_date: Optional[datetime] = None


@dataclass
class ImpactAnalysisResult:
    """Complete impact analysis for a GR change"""
    gr_change: GRChange
    total_affected_components: int
    affected_by_domain: Dict[str, int]
    affected_by_type: Dict[str, int]
    critical_impacts: List[AffectedComponent]
    dependency_chains: List[List[str]]
    estimated_total_effort: str
    risk_assessment: Dict[str, Any]
    recommendations: List[str]
    rollback_plan: List[str]


class GRImpactAnalyzer:
    """
    Analyzes the impact of Global Requirement changes across the system
    """
    
    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.gr_index = {}
        self.gr_usage_map = defaultdict(list)  # GR -> components using it
        self.component_gr_map = defaultdict(list)  # component -> GRs
        self.dependency_graph = nx.DiGraph()
        self.validation_rules = {}
        self.load_gr_knowledge()
    
    def load_gr_knowledge(self):
        """Load GR knowledge and usage patterns"""
        try:
            # Load GR index
            gr_index_path = self.knowledge_base_path / "global-requirements-index.json"
            if gr_index_path.exists():
                with open(gr_index_path, 'r') as f:
                    gr_data = json.load(f)
                    self.gr_index = gr_data.get('global_requirements', {})
            
            # Load validation rules
            self._load_validation_rules()
            
            # Build usage maps
            self._build_usage_maps()
            
            # Build dependency graph
            self._build_dependency_graph()
            
            logger.info(f"Loaded {len(self.gr_index)} Global Requirements")
            
        except Exception as e:
            logger.error(f"Error loading GR knowledge: {e}")
    
    def _load_validation_rules(self):
        """Load validation rules for each GR"""
        self.validation_rules = {
            'GR-52': {
                'type': 'field_validation',
                'rules': ['required_fields', 'field_types', 'field_lengths'],
                'dependencies': ['entity_structure', 'data_types']
            },
            'GR-44': {
                'type': 'data_flow',
                'rules': ['field_mapping', 'transformation_rules', 'validation_order'],
                'dependencies': ['workflow_sequence', 'entity_relationships']
            },
            'GR-41': {
                'type': 'validation_sequence',
                'rules': ['validation_order', 'error_handling', 'retry_logic'],
                'dependencies': ['workflow_state', 'error_codes']
            },
            'GR-38': {
                'type': 'security',
                'rules': ['access_control', 'data_encryption', 'audit_logging'],
                'dependencies': ['user_roles', 'security_policies']
            },
            'GR-53': {
                'type': 'performance',
                'rules': ['response_time', 'throughput', 'resource_limits'],
                'dependencies': ['system_capacity', 'load_patterns']
            }
        }
    
    def _build_usage_maps(self):
        """Build maps of GR usage across components"""
        # Simulated usage patterns - in production, this would be extracted from actual requirements
        usage_patterns = {
            'GR-52': [
                {'id': 'req_001', 'type': 'requirement', 'domain': 'producer-portal'},
                {'id': 'entity_driver', 'type': 'entity', 'domain': 'shared'},
                {'id': 'entity_vehicle', 'type': 'entity', 'domain': 'shared'},
                {'id': 'workflow_quote_creation', 'type': 'workflow', 'domain': 'producer-portal'}
            ],
            'GR-44': [
                {'id': 'req_002', 'type': 'requirement', 'domain': 'accounting'},
                {'id': 'workflow_billing_setup', 'type': 'workflow', 'domain': 'accounting'},
                {'id': 'entity_payment', 'type': 'entity', 'domain': 'accounting'},
                {'id': 'integration_payment_gateway', 'type': 'integration', 'domain': 'accounting'}
            ],
            'GR-41': [
                {'id': 'validation_driver_license', 'type': 'validation', 'domain': 'entity-integration'},
                {'id': 'validation_vehicle_vin', 'type': 'validation', 'domain': 'entity-integration'},
                {'id': 'workflow_quote_validation', 'type': 'workflow', 'domain': 'producer-portal'}
            ],
            'GR-38': [
                {'id': 'entity_user', 'type': 'entity', 'domain': 'shared'},
                {'id': 'workflow_authentication', 'type': 'workflow', 'domain': 'shared'},
                {'id': 'integration_auth_service', 'type': 'integration', 'domain': 'shared'}
            ],
            'GR-53': [
                {'id': 'workflow_rate_calculation', 'type': 'workflow', 'domain': 'producer-portal'},
                {'id': 'service_quote_engine', 'type': 'service', 'domain': 'producer-portal'},
                {'id': 'cache_rate_tables', 'type': 'cache', 'domain': 'shared'}
            ]
        }
        
        # Build bidirectional maps
        for gr_id, components in usage_patterns.items():
            for component in components:
                self.gr_usage_map[gr_id].append(component)
                self.component_gr_map[component['id']].append(gr_id)
    
    def _build_dependency_graph(self):
        """Build dependency graph for impact analysis"""
        # Add nodes for GRs
        for gr_id, gr_info in self.gr_index.items():
            self.dependency_graph.add_node(
                gr_id,
                type='global_requirement',
                name=gr_info.get('name', ''),
                category=gr_info.get('category', '')
            )
        
        # Add nodes for components
        for gr_id, components in self.gr_usage_map.items():
            for component in components:
                self.dependency_graph.add_node(
                    component['id'],
                    type=component['type'],
                    domain=component['domain']
                )
                
                # Add edge from component to GR (component depends on GR)
                self.dependency_graph.add_edge(
                    component['id'],
                    gr_id,
                    relationship='implements'
                )
        
        # Add component dependencies
        component_deps = {
            'workflow_quote_creation': ['entity_driver', 'entity_vehicle', 'validation_driver_license'],
            'workflow_billing_setup': ['entity_payment', 'integration_payment_gateway'],
            'workflow_quote_validation': ['validation_driver_license', 'validation_vehicle_vin'],
            'service_quote_engine': ['workflow_rate_calculation', 'cache_rate_tables']
        }
        
        for source, targets in component_deps.items():
            for target in targets:
                if self.dependency_graph.has_node(source) and self.dependency_graph.has_node(target):
                    self.dependency_graph.add_edge(source, target, relationship='depends_on')
    
    def analyze_gr_change_impact(self, gr_change: GRChange) -> ImpactAnalysisResult:
        """
        Analyze the impact of a change to a Global Requirement
        
        Args:
            gr_change: The proposed GR change
            
        Returns:
            Complete impact analysis
        """
        if gr_change.gr_id not in self.gr_index:
            logger.error(f"GR {gr_change.gr_id} not found")
            return self._empty_result(gr_change)
        
        # Find all affected components
        affected_components = self._find_affected_components(gr_change)
        
        # Analyze impact for each component
        analyzed_components = []
        for component in affected_components:
            impact = self._analyze_component_impact(component, gr_change)
            analyzed_components.append(impact)
        
        # Find dependency chains
        dependency_chains = self._find_dependency_chains(gr_change.gr_id)
        
        # Aggregate results
        result = self._aggregate_impact_analysis(
            gr_change, analyzed_components, dependency_chains
        )
        
        return result
    
    def _find_affected_components(self, gr_change: GRChange) -> List[Dict]:
        """Find all components affected by the GR change"""
        affected = []
        
        # Direct usage
        direct_components = self.gr_usage_map.get(gr_change.gr_id, [])
        for component in direct_components:
            affected.append({
                **component,
                'impact_type': 'direct',
                'distance': 0
            })
        
        # Find indirect impacts through dependency graph
        if gr_change.gr_id in self.dependency_graph:
            # Use BFS to find components within 2 hops
            visited = set()
            queue = deque([(gr_change.gr_id, 0)])
            
            while queue:
                node, distance = queue.popleft()
                if node in visited or distance > 2:
                    continue
                
                visited.add(node)
                
                # Check predecessors (components that depend on this node)
                for pred in self.dependency_graph.predecessors(node):
                    if pred not in visited and distance > 0:
                        node_data = self.dependency_graph.nodes[pred]
                        affected.append({
                            'id': pred,
                            'type': node_data.get('type', 'unknown'),
                            'domain': node_data.get('domain', 'unknown'),
                            'impact_type': 'indirect',
                            'distance': distance
                        })
                        queue.append((pred, distance + 1))
        
        return affected
    
    def _analyze_component_impact(self, component: Dict, gr_change: GRChange) -> AffectedComponent:
        """Analyze impact on a specific component"""
        # Determine impact level based on change type and component type
        impact_level = self._calculate_impact_level(component, gr_change)
        
        # Determine required changes
        required_changes = self._determine_required_changes(component, gr_change)
        
        # Estimate effort
        effort = self._estimate_effort(impact_level, len(required_changes))
        
        # Identify risk factors
        risk_factors = self._identify_risk_factors(component, gr_change)
        
        # Find dependencies
        dependencies = []
        if component['id'] in self.dependency_graph:
            dependencies = list(self.dependency_graph.successors(component['id']))
        
        return AffectedComponent(
            component_id=component['id'],
            component_type=component['type'],
            domain=component['domain'],
            impact_level=impact_level,
            required_changes=required_changes,
            estimated_effort=effort,
            risk_factors=risk_factors,
            dependencies=dependencies
        )
    
    def _calculate_impact_level(self, component: Dict, gr_change: GRChange) -> ImpactLevel:
        """Calculate the impact level for a component"""
        # Critical changes
        if gr_change.change_type in [ChangeType.REMOVE_CONSTRAINT, ChangeType.DEPRECATE]:
            if component['impact_type'] == 'direct':
                return ImpactLevel.CRITICAL
            else:
                return ImpactLevel.HIGH
        
        # High impact changes
        if gr_change.change_type in [ChangeType.MODIFY_VALIDATION, ChangeType.CHANGE_SCOPE]:
            if component['impact_type'] == 'direct':
                return ImpactLevel.HIGH
            else:
                return ImpactLevel.MEDIUM
        
        # Medium impact changes
        if gr_change.change_type == ChangeType.UPDATE_THRESHOLD:
            if component['type'] in ['workflow', 'service']:
                return ImpactLevel.MEDIUM
            else:
                return ImpactLevel.LOW
        
        # Low impact changes
        if gr_change.change_type in [ChangeType.ADD_CONSTRAINT, ChangeType.ENHANCE]:
            if component['impact_type'] == 'direct':
                return ImpactLevel.MEDIUM
            else:
                return ImpactLevel.LOW
        
        return ImpactLevel.LOW
    
    def _determine_required_changes(self, component: Dict, gr_change: GRChange) -> List[str]:
        """Determine what changes are required for the component"""
        changes = []
        
        if gr_change.change_type == ChangeType.ADD_CONSTRAINT:
            changes.append(f"Add validation for new constraint: {gr_change.new_value}")
            if component['type'] == 'entity':
                changes.append("Update entity schema documentation")
            if component['type'] == 'workflow':
                changes.append("Add constraint check to workflow validation")
        
        elif gr_change.change_type == ChangeType.REMOVE_CONSTRAINT:
            changes.append(f"Remove validation for constraint: {gr_change.old_value}")
            changes.append("Update related error handling")
            if component['type'] == 'validation':
                changes.append("Remove or refactor validation logic")
        
        elif gr_change.change_type == ChangeType.MODIFY_VALIDATION:
            changes.append(f"Update validation logic from {gr_change.old_value} to {gr_change.new_value}")
            changes.append("Update test cases for new validation")
            if component['type'] == 'workflow':
                changes.append("Review workflow error paths")
        
        elif gr_change.change_type == ChangeType.UPDATE_THRESHOLD:
            changes.append(f"Update threshold from {gr_change.old_value} to {gr_change.new_value}")
            if component['type'] in ['service', 'cache']:
                changes.append("Update configuration values")
                changes.append("Test performance with new threshold")
        
        elif gr_change.change_type == ChangeType.CHANGE_SCOPE:
            changes.append("Review component for scope compliance")
            changes.append("Update implementation to match new scope")
            if component['impact_type'] == 'direct':
                changes.append("Major refactoring may be required")
        
        elif gr_change.change_type == ChangeType.DEPRECATE:
            changes.append("Plan migration away from deprecated GR")
            changes.append("Implement alternative approach")
            changes.append("Update documentation")
        
        elif gr_change.change_type == ChangeType.ENHANCE:
            changes.append("Review enhancement for implementation")
            changes.append("Optional: Implement enhanced features")
        
        return changes
    
    def _estimate_effort(self, impact_level: ImpactLevel, change_count: int) -> str:
        """Estimate effort required for changes"""
        if impact_level == ImpactLevel.CRITICAL:
            return "weeks"
        elif impact_level == ImpactLevel.HIGH:
            if change_count > 3:
                return "weeks"
            else:
                return "days"
        elif impact_level == ImpactLevel.MEDIUM:
            if change_count > 5:
                return "days"
            else:
                return "hours"
        else:
            return "hours"
    
    def _identify_risk_factors(self, component: Dict, gr_change: GRChange) -> List[str]:
        """Identify risk factors for the component change"""
        risks = []
        
        # Type-specific risks
        if component['type'] == 'entity' and gr_change.change_type in [ChangeType.REMOVE_CONSTRAINT, ChangeType.MODIFY_VALIDATION]:
            risks.append("Data integrity risk - existing data may not comply")
        
        if component['type'] == 'workflow' and component['impact_type'] == 'direct':
            risks.append("Business process disruption risk")
        
        if component['type'] == 'integration':
            risks.append("External system compatibility risk")
        
        if component['type'] == 'validation' and gr_change.change_type == ChangeType.DEPRECATE:
            risks.append("Security risk - validation gap during migration")
        
        # Domain-specific risks
        if component['domain'] == 'accounting':
            risks.append("Financial data accuracy risk")
        
        if component['domain'] == 'producer-portal' and impact_level in [ImpactLevel.CRITICAL, ImpactLevel.HIGH]:
            risks.append("User experience disruption risk")
        
        # General risks
        if component.get('distance', 0) > 1:
            risks.append("Cascade effect risk - indirect impact")
        
        if len(component.get('dependencies', [])) > 3:
            risks.append("High dependency risk - multiple components affected")
        
        return risks
    
    def _find_dependency_chains(self, gr_id: str) -> List[List[str]]:
        """Find dependency chains affected by the GR"""
        chains = []
        
        if gr_id not in self.dependency_graph:
            return chains
        
        # Find all paths from GR to leaf nodes
        try:
            # Get all components that depend on this GR
            dependent_components = list(self.dependency_graph.predecessors(gr_id))
            
            for component in dependent_components:
                # Find paths from component to other components
                for target in self.dependency_graph.nodes():
                    if target != component and target != gr_id:
                        try:
                            paths = list(nx.all_simple_paths(
                                self.dependency_graph, 
                                component, 
                                target, 
                                cutoff=4
                            ))
                            for path in paths:
                                if gr_id not in path:
                                    full_path = [gr_id] + path
                                    if len(full_path) > 2:  # Only include meaningful chains
                                        chains.append(full_path)
                        except nx.NetworkXNoPath:
                            continue
            
            # Limit to most significant chains
            chains = sorted(chains, key=len, reverse=True)[:10]
            
        except Exception as e:
            logger.error(f"Error finding dependency chains: {e}")
        
        return chains
    
    def _aggregate_impact_analysis(self, gr_change: GRChange, 
                                  affected_components: List[AffectedComponent],
                                  dependency_chains: List[List[str]]) -> ImpactAnalysisResult:
        """Aggregate impact analysis results"""
        # Count by domain
        affected_by_domain = defaultdict(int)
        for component in affected_components:
            affected_by_domain[component.domain] += 1
        
        # Count by type
        affected_by_type = defaultdict(int)
        for component in affected_components:
            affected_by_type[component.component_type] += 1
        
        # Find critical impacts
        critical_impacts = [
            c for c in affected_components 
            if c.impact_level in [ImpactLevel.CRITICAL, ImpactLevel.HIGH]
        ]
        
        # Estimate total effort
        effort_weights = {
            'hours': 1,
            'days': 8,
            'weeks': 40
        }
        total_hours = sum(
            effort_weights.get(c.estimated_effort, 1) 
            for c in affected_components
        )
        
        if total_hours > 160:
            total_effort = "months"
        elif total_hours > 40:
            total_effort = "weeks"
        elif total_hours > 8:
            total_effort = "days"
        else:
            total_effort = "hours"
        
        # Risk assessment
        risk_assessment = self._assess_overall_risk(
            affected_components, critical_impacts, dependency_chains
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            gr_change, affected_components, critical_impacts, risk_assessment
        )
        
        # Generate rollback plan
        rollback_plan = self._generate_rollback_plan(gr_change, critical_impacts)
        
        return ImpactAnalysisResult(
            gr_change=gr_change,
            total_affected_components=len(affected_components),
            affected_by_domain=dict(affected_by_domain),
            affected_by_type=dict(affected_by_type),
            critical_impacts=critical_impacts,
            dependency_chains=dependency_chains,
            estimated_total_effort=total_effort,
            risk_assessment=risk_assessment,
            recommendations=recommendations,
            rollback_plan=rollback_plan
        )
    
    def _assess_overall_risk(self, all_components: List[AffectedComponent],
                           critical_components: List[AffectedComponent],
                           dependency_chains: List[List[str]]) -> Dict[str, Any]:
        """Assess overall risk of the GR change"""
        risk_score = 0
        risk_factors = []
        
        # Critical component factor
        critical_ratio = len(critical_components) / max(len(all_components), 1)
        if critical_ratio > 0.5:
            risk_score += 3
            risk_factors.append("High ratio of critical impacts")
        elif critical_ratio > 0.2:
            risk_score += 2
            risk_factors.append("Significant critical impacts")
        elif critical_components:
            risk_score += 1
            risk_factors.append("Some critical impacts")
        
        # Cross-domain factor
        domains_affected = len(set(c.domain for c in all_components))
        if domains_affected > 3:
            risk_score += 2
            risk_factors.append(f"Cross-domain impact ({domains_affected} domains)")
        elif domains_affected > 1:
            risk_score += 1
            risk_factors.append("Multi-domain impact")
        
        # Dependency chain factor
        long_chains = [c for c in dependency_chains if len(c) > 3]
        if long_chains:
            risk_score += 2
            risk_factors.append(f"Long dependency chains ({len(long_chains)})")
        
        # Integration risk
        integration_impacts = [
            c for c in all_components 
            if c.component_type == 'integration'
        ]
        if integration_impacts:
            risk_score += 2
            risk_factors.append("External integration impacts")
        
        # Calculate risk level
        if risk_score >= 7:
            risk_level = "critical"
        elif risk_score >= 5:
            risk_level = "high"
        elif risk_score >= 3:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'mitigation_priority': 'immediate' if risk_level == 'critical' else 'standard'
        }
    
    def _generate_recommendations(self, gr_change: GRChange,
                                affected_components: List[AffectedComponent],
                                critical_impacts: List[AffectedComponent],
                                risk_assessment: Dict) -> List[str]:
        """Generate recommendations for the GR change"""
        recommendations = []
        
        # Risk-based recommendations
        if risk_assessment['risk_level'] == 'critical':
            recommendations.append("Consider phased rollout with careful monitoring")
            recommendations.append("Implement comprehensive rollback plan")
            recommendations.append("Schedule change during low-traffic period")
        elif risk_assessment['risk_level'] == 'high':
            recommendations.append("Implement feature flags for gradual rollout")
            recommendations.append("Increase monitoring during deployment")
        
        # Change type recommendations
        if gr_change.change_type == ChangeType.DEPRECATE:
            recommendations.append("Provide migration guide for affected teams")
            recommendations.append("Set deprecation timeline with clear milestones")
            recommendations.append("Maintain backward compatibility during transition")
        
        elif gr_change.change_type == ChangeType.REMOVE_CONSTRAINT:
            recommendations.append("Audit existing data for constraint violations")
            recommendations.append("Update documentation to reflect removed constraints")
        
        elif gr_change.change_type == ChangeType.MODIFY_VALIDATION:
            recommendations.append("Create comprehensive test suite for new validation")
            recommendations.append("Document validation changes clearly")
        
        # Domain-specific recommendations
        domains = set(c.domain for c in affected_components)
        if 'accounting' in domains:
            recommendations.append("Coordinate with finance team for validation")
            recommendations.append("Ensure audit trail integrity")
        
        if 'producer-portal' in domains and critical_impacts:
            recommendations.append("Prepare user communication about changes")
            recommendations.append("Update user documentation and help content")
        
        # Testing recommendations
        if len(affected_components) > 10:
            recommendations.append("Implement automated regression testing")
            recommendations.append("Consider load testing for performance impact")
        
        if any(c.component_type == 'integration' for c in affected_components):
            recommendations.append("Coordinate with external system owners")
            recommendations.append("Test integration points thoroughly")
        
        # Coordination recommendations
        if len(domains) > 2:
            recommendations.append("Establish cross-domain coordination team")
            recommendations.append("Create unified testing strategy")
        
        return recommendations
    
    def _generate_rollback_plan(self, gr_change: GRChange,
                               critical_impacts: List[AffectedComponent]) -> List[str]:
        """Generate rollback plan for the GR change"""
        rollback_steps = []
        
        # General rollback steps
        rollback_steps.append(f"Revert GR {gr_change.gr_id} to previous value: {gr_change.old_value}")
        rollback_steps.append("Notify all affected teams immediately")
        
        # Component-specific rollback
        if critical_impacts:
            rollback_steps.append("Priority rollback for critical components:")
            for component in critical_impacts[:5]:  # Top 5 critical
                rollback_steps.append(f"  - Rollback {component.component_id} ({component.component_type})")
        
        # Type-specific rollback
        if gr_change.change_type == ChangeType.MODIFY_VALIDATION:
            rollback_steps.append("Restore original validation rules")
            rollback_steps.append("Clear validation cache if applicable")
        
        elif gr_change.change_type == ChangeType.UPDATE_THRESHOLD:
            rollback_steps.append("Reset thresholds to original values")
            rollback_steps.append("Restart affected services if needed")
        
        elif gr_change.change_type == ChangeType.REMOVE_CONSTRAINT:
            rollback_steps.append("Re-enable constraint validation")
            rollback_steps.append("Validate data integrity post-rollback")
        
        # Verification steps
        rollback_steps.append("Verification steps:")
        rollback_steps.append("  - Run automated tests for affected components")
        rollback_steps.append("  - Monitor system metrics for 30 minutes")
        rollback_steps.append("  - Verify no data corruption occurred")
        rollback_steps.append("  - Confirm all integrations are functional")
        
        return rollback_steps
    
    def _empty_result(self, gr_change: GRChange) -> ImpactAnalysisResult:
        """Return empty result for invalid GR"""
        return ImpactAnalysisResult(
            gr_change=gr_change,
            total_affected_components=0,
            affected_by_domain={},
            affected_by_type={},
            critical_impacts=[],
            dependency_chains=[],
            estimated_total_effort="none",
            risk_assessment={'risk_level': 'unknown', 'risk_score': 0, 'risk_factors': []},
            recommendations=["Invalid GR ID provided"],
            rollback_plan=[]
        )
    
    def find_safe_gr_changes(self) -> List[Dict]:
        """Find GRs that can be safely modified with minimal impact"""
        safe_changes = []
        
        for gr_id, gr_info in self.gr_index.items():
            # Count direct usage
            direct_usage = len(self.gr_usage_map.get(gr_id, []))
            
            # Check for critical components
            critical_components = [
                c for c in self.gr_usage_map.get(gr_id, [])
                if c['type'] in ['integration', 'validation']
            ]
            
            # Calculate safety score
            safety_score = 10
            safety_score -= direct_usage * 0.5
            safety_score -= len(critical_components) * 2
            
            if safety_score > 7:
                safe_changes.append({
                    'gr_id': gr_id,
                    'gr_name': gr_info.get('name', ''),
                    'direct_usage': direct_usage,
                    'safety_score': safety_score,
                    'safe_change_types': self._get_safe_change_types(gr_id, direct_usage)
                })
        
        return sorted(safe_changes, key=lambda x: x['safety_score'], reverse=True)
    
    def _get_safe_change_types(self, gr_id: str, usage_count: int) -> List[str]:
        """Determine safe change types for a GR"""
        safe_types = []
        
        if usage_count == 0:
            safe_types.extend(['deprecate', 'remove_constraint'])
        
        if usage_count < 3:
            safe_types.extend(['enhance', 'add_constraint'])
        
        safe_types.append('update_threshold')  # Generally safe with proper testing
        
        return safe_types
    
    def generate_change_report(self, gr_changes: List[GRChange]) -> Dict:
        """Generate comprehensive report for multiple GR changes"""
        report = {
            'analysis_date': datetime.now().isoformat(),
            'total_changes': len(gr_changes),
            'changes': [],
            'overall_impact': {
                'total_affected_components': 0,
                'affected_domains': set(),
                'critical_changes': 0,
                'estimated_total_effort': 0
            },
            'recommendations': []
        }
        
        effort_to_hours = {
            'hours': 8,
            'days': 40,
            'weeks': 200,
            'months': 800
        }
        
        for gr_change in gr_changes:
            analysis = self.analyze_gr_change_impact(gr_change)
            
            report['changes'].append({
                'gr_id': gr_change.gr_id,
                'change_type': gr_change.change_type.value,
                'impact_summary': {
                    'affected_components': analysis.total_affected_components,
                    'risk_level': analysis.risk_assessment['risk_level'],
                    'effort': analysis.estimated_total_effort
                }
            })
            
            # Update overall impact
            report['overall_impact']['total_affected_components'] += analysis.total_affected_components
            report['overall_impact']['affected_domains'].update(analysis.affected_by_domain.keys())
            
            if analysis.risk_assessment['risk_level'] in ['critical', 'high']:
                report['overall_impact']['critical_changes'] += 1
            
            report['overall_impact']['estimated_total_effort'] += effort_to_hours.get(
                analysis.estimated_total_effort, 8
            )
        
        # Convert set to list for JSON serialization
        report['overall_impact']['affected_domains'] = list(
            report['overall_impact']['affected_domains']
        )
        
        # Overall recommendations
        if report['overall_impact']['critical_changes'] > 0:
            report['recommendations'].append("Multiple critical changes detected - consider staggered deployment")
        
        if len(report['overall_impact']['affected_domains']) > 3:
            report['recommendations'].append("Wide system impact - establish change coordination committee")
        
        total_effort_weeks = report['overall_impact']['estimated_total_effort'] / 40
        if total_effort_weeks > 4:
            report['recommendations'].append(f"Significant effort required (~{total_effort_weeks:.1f} weeks) - plan resources accordingly")
        
        return report


# Example usage and testing
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = GRImpactAnalyzer("/app/workspace/requirements/shared-infrastructure/knowledge-base")
    
    # Example 1: Analyze validation change
    print("Analyzing GR-52 validation modification...")
    gr_change = GRChange(
        gr_id="GR-52",
        gr_name="Field Validation Standards",
        change_type=ChangeType.MODIFY_VALIDATION,
        description="Update email validation to support international domains",
        old_value="standard_email_regex",
        new_value="international_email_regex",
        rationale="Support global customer base"
    )
    
    impact = analyzer.analyze_gr_change_impact(gr_change)
    
    print(f"\nImpact Analysis for {gr_change.gr_name}:")
    print(f"  Total affected components: {impact.total_affected_components}")
    print(f"  Risk level: {impact.risk_assessment['risk_level']}")
    print(f"  Estimated effort: {impact.estimated_total_effort}")
    
    print("\nAffected domains:")
    for domain, count in impact.affected_by_domain.items():
        print(f"  - {domain}: {count} components")
    
    print("\nCritical impacts:")
    for component in impact.critical_impacts[:3]:
        print(f"  - {component.component_id} ({component.component_type})")
        print(f"    Required changes: {len(component.required_changes)}")
    
    print("\nRecommendations:")
    for rec in impact.recommendations[:5]:
        print(f"  - {rec}")
    
    # Example 2: Find safe changes
    print("\n\nFinding safe GR changes...")
    safe_changes = analyzer.find_safe_gr_changes()
    
    print("\nSafest GRs to modify:")
    for safe_gr in safe_changes[:3]:
        print(f"  - {safe_gr['gr_id']}: {safe_gr['gr_name']}")
        print(f"    Safety score: {safe_gr['safety_score']:.1f}")
        print(f"    Safe changes: {', '.join(safe_gr['safe_change_types'])}")
    
    # Example 3: Multiple change report
    print("\n\nGenerating change report for multiple GRs...")
    changes = [
        GRChange(
            gr_id="GR-44",
            gr_name="Data Transformation Rules",
            change_type=ChangeType.ADD_CONSTRAINT,
            description="Add currency field validation",
            old_value=None,
            new_value="currency_format_validation",
            rationale="Ensure consistent currency handling"
        ),
        GRChange(
            gr_id="GR-53",
            gr_name="Performance Requirements",
            change_type=ChangeType.UPDATE_THRESHOLD,
            description="Reduce response time threshold",
            old_value="3000ms",
            new_value="2000ms",
            rationale="Improve user experience"
        )
    ]
    
    report = analyzer.generate_change_report(changes)
    
    print("\nChange Report Summary:")
    print(f"  Total changes: {report['total_changes']}")
    print(f"  Total affected components: {report['overall_impact']['total_affected_components']}")
    print(f"  Critical changes: {report['overall_impact']['critical_changes']}")
    print(f"  Estimated total effort: {report['overall_impact']['estimated_total_effort']} hours")