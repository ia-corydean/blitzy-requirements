#!/usr/bin/env python3
"""
Cross-Domain Relationship Analyzer

This engine analyzes and manages relationships between entities, workflows,
and components across different business domains, enabling intelligent
coordination and impact analysis.

Features:
- Entity relationship mapping
- Cross-domain dependency detection
- Impact analysis for changes
- Relationship strength calculation
- Circular dependency detection
"""

import json
import logging
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from collections import defaultdict, deque
import networkx as nx
import matplotlib.pyplot as plt
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RelationshipType(Enum):
    """Types of relationships between components"""
    DEPENDS_ON = "depends_on"
    TRIGGERS = "triggers"
    SHARES_DATA = "shares_data"
    VALIDATES = "validates"
    EXTENDS = "extends"
    IMPLEMENTS = "implements"
    USES = "uses"
    PROVIDES = "provides"
    REQUIRES = "requires"
    CONFLICTS_WITH = "conflicts_with"


class ComponentType(Enum):
    """Types of components in the system"""
    ENTITY = "entity"
    WORKFLOW = "workflow"
    SERVICE = "service"
    INTEGRATION = "integration"
    VALIDATION = "validation"
    GLOBAL_REQUIREMENT = "global_requirement"
    DOMAIN = "domain"


@dataclass
class Relationship:
    """Represents a relationship between components"""
    source: str
    source_type: ComponentType
    target: str
    target_type: ComponentType
    relationship_type: RelationshipType
    strength: float  # 0.0 to 1.0
    domain: Optional[str] = None
    cross_domain: bool = False
    metadata: Dict = field(default_factory=dict)


@dataclass
class Component:
    """Represents a system component"""
    id: str
    name: str
    type: ComponentType
    domain: str
    description: str = ""
    attributes: Dict = field(default_factory=dict)
    relationships: List[Relationship] = field(default_factory=list)


@dataclass
class ImpactAnalysis:
    """Results of impact analysis for a change"""
    component: str
    direct_impacts: List[Dict]
    indirect_impacts: List[Dict]
    affected_domains: Set[str]
    risk_level: str  # 'low', 'medium', 'high', 'critical'
    circular_dependencies: List[List[str]]
    recommendations: List[str]


class CrossDomainRelationshipAnalyzer:
    """
    Analyzes relationships and dependencies across business domains
    """
    
    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.graph = nx.DiGraph()
        self.components: Dict[str, Component] = {}
        self.domain_map: Dict[str, Set[str]] = defaultdict(set)
        self.relationship_index: Dict[str, List[Relationship]] = defaultdict(list)
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load relationship data from knowledge base"""
        try:
            # Load entity catalog
            entity_catalog_path = self.knowledge_base_path / "universal-entity-catalog.json"
            if entity_catalog_path.exists():
                with open(entity_catalog_path, 'r') as f:
                    catalog_data = json.load(f)
                    self._load_entities(catalog_data.get('entities', {}))
            
            # Load cross-domain relationships
            relationships_path = self.knowledge_base_path / "cross-domain-relationships/relationship-map.json"
            if relationships_path.exists():
                with open(relationships_path, 'r') as f:
                    rel_data = json.load(f)
                    self._load_relationships(rel_data.get('relationships', []))
            
            # Load workflow patterns
            self._load_workflow_patterns()
            
            # Build graph
            self._build_relationship_graph()
            
            logger.info(f"Loaded {len(self.components)} components and {self.graph.number_of_edges()} relationships")
            
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
    
    def _load_entities(self, entities: Dict):
        """Load entities as components"""
        for entity_name, entity_data in entities.items():
            component = Component(
                id=f"entity_{entity_name}",
                name=entity_name,
                type=ComponentType.ENTITY,
                domain=entity_data.get('primary_domain', 'shared'),
                description=entity_data.get('description', ''),
                attributes=entity_data
            )
            
            self.components[component.id] = component
            self.domain_map[component.domain].add(component.id)
            
            # Add entity relationships
            for related in entity_data.get('related_entities', []):
                rel = Relationship(
                    source=component.id,
                    source_type=ComponentType.ENTITY,
                    target=f"entity_{related}",
                    target_type=ComponentType.ENTITY,
                    relationship_type=RelationshipType.SHARES_DATA,
                    strength=0.7,
                    domain=component.domain
                )
                component.relationships.append(rel)
    
    def _load_relationships(self, relationships: List[Dict]):
        """Load cross-domain relationships"""
        for rel_data in relationships:
            source_id = f"entity_{rel_data['source_entity']}"
            target_id = f"entity_{rel_data['target_entity']}"
            
            # Determine relationship type
            rel_type_map = {
                'has_many': RelationshipType.DEPENDS_ON,
                'belongs_to': RelationshipType.DEPENDS_ON,
                'triggers': RelationshipType.TRIGGERS,
                'validates': RelationshipType.VALIDATES,
                'uses': RelationshipType.USES
            }
            
            rel_type = rel_type_map.get(
                rel_data.get('relationship_type', 'uses'),
                RelationshipType.USES
            )
            
            # Check if cross-domain
            source_domain = self.components.get(source_id, {}).domain if source_id in self.components else None
            target_domain = self.components.get(target_id, {}).domain if target_id in self.components else None
            cross_domain = source_domain != target_domain if source_domain and target_domain else False
            
            rel = Relationship(
                source=source_id,
                source_type=ComponentType.ENTITY,
                target=target_id,
                target_type=ComponentType.ENTITY,
                relationship_type=rel_type,
                strength=rel_data.get('strength', 0.8),
                cross_domain=cross_domain,
                metadata=rel_data
            )
            
            self.relationship_index[source_id].append(rel)
            
            # Add to component if exists
            if source_id in self.components:
                self.components[source_id].relationships.append(rel)
    
    def _load_workflow_patterns(self):
        """Load workflow patterns and their relationships"""
        workflow_patterns = {
            'quote_creation': {
                'domain': 'producer-portal',
                'entities': ['driver', 'vehicle', 'quote'],
                'triggers': ['rate_calculation'],
                'depends_on': ['driver_collection', 'vehicle_collection']
            },
            'quote_binding': {
                'domain': 'producer-portal',
                'entities': ['quote', 'policy', 'payment'],
                'triggers': ['policy_issuance', 'billing_setup'],
                'depends_on': ['quote_creation', 'payment_collection']
            },
            'billing_setup': {
                'domain': 'accounting',
                'entities': ['policy', 'billing', 'payment'],
                'triggers': ['invoice_generation'],
                'depends_on': ['policy_issuance']
            },
            'driver_verification': {
                'domain': 'entity-integration',
                'entities': ['driver', 'license'],
                'uses': ['DCS'],
                'validates': ['driver']
            }
        }
        
        for workflow_name, workflow_data in workflow_patterns.items():
            # Create workflow component
            workflow = Component(
                id=f"workflow_{workflow_name}",
                name=workflow_name,
                type=ComponentType.WORKFLOW,
                domain=workflow_data['domain'],
                description=f"Workflow: {workflow_name}",
                attributes=workflow_data
            )
            
            self.components[workflow.id] = workflow
            self.domain_map[workflow.domain].add(workflow.id)
            
            # Add entity relationships
            for entity in workflow_data.get('entities', []):
                rel = Relationship(
                    source=workflow.id,
                    source_type=ComponentType.WORKFLOW,
                    target=f"entity_{entity}",
                    target_type=ComponentType.ENTITY,
                    relationship_type=RelationshipType.USES,
                    strength=0.9,
                    domain=workflow.domain
                )
                workflow.relationships.append(rel)
            
            # Add trigger relationships
            for triggered in workflow_data.get('triggers', []):
                rel = Relationship(
                    source=workflow.id,
                    source_type=ComponentType.WORKFLOW,
                    target=f"workflow_{triggered}",
                    target_type=ComponentType.WORKFLOW,
                    relationship_type=RelationshipType.TRIGGERS,
                    strength=0.8,
                    domain=workflow.domain
                )
                workflow.relationships.append(rel)
            
            # Add dependency relationships
            for dependency in workflow_data.get('depends_on', []):
                rel = Relationship(
                    source=workflow.id,
                    source_type=ComponentType.WORKFLOW,
                    target=f"workflow_{dependency}",
                    target_type=ComponentType.WORKFLOW,
                    relationship_type=RelationshipType.DEPENDS_ON,
                    strength=0.9,
                    domain=workflow.domain
                )
                workflow.relationships.append(rel)
    
    def _build_relationship_graph(self):
        """Build NetworkX graph from components and relationships"""
        # Add nodes
        for component_id, component in self.components.items():
            self.graph.add_node(
                component_id,
                name=component.name,
                type=component.type.value,
                domain=component.domain,
                **component.attributes
            )
        
        # Add edges
        for component in self.components.values():
            for rel in component.relationships:
                self.graph.add_edge(
                    rel.source,
                    rel.target,
                    relationship_type=rel.relationship_type.value,
                    strength=rel.strength,
                    cross_domain=rel.cross_domain,
                    **rel.metadata
                )
    
    def analyze_component_relationships(self, component_id: str) -> Dict:
        """
        Analyze all relationships for a specific component
        
        Args:
            component_id: Component identifier
            
        Returns:
            Dictionary with relationship analysis
        """
        if component_id not in self.components:
            return {'error': f'Component {component_id} not found'}
        
        component = self.components[component_id]
        
        # Get direct relationships
        outgoing = list(self.graph.out_edges(component_id, data=True))
        incoming = list(self.graph.in_edges(component_id, data=True))
        
        # Categorize relationships
        relationships_by_type = defaultdict(list)
        
        for source, target, data in outgoing:
            rel_type = data.get('relationship_type', 'unknown')
            relationships_by_type[f'outgoing_{rel_type}'].append({
                'target': target,
                'target_name': self.components.get(target, {}).name if target in self.components else target,
                'strength': data.get('strength', 0.5),
                'cross_domain': data.get('cross_domain', False)
            })
        
        for source, target, data in incoming:
            rel_type = data.get('relationship_type', 'unknown')
            relationships_by_type[f'incoming_{rel_type}'].append({
                'source': source,
                'source_name': self.components.get(source, {}).name if source in self.components else source,
                'strength': data.get('strength', 0.5),
                'cross_domain': data.get('cross_domain', False)
            })
        
        # Calculate metrics
        metrics = {
            'total_relationships': len(outgoing) + len(incoming),
            'outgoing_relationships': len(outgoing),
            'incoming_relationships': len(incoming),
            'cross_domain_relationships': sum(
                1 for _, _, d in outgoing + incoming 
                if d.get('cross_domain', False)
            ),
            'average_strength': sum(
                d.get('strength', 0.5) 
                for _, _, d in outgoing + incoming
            ) / max(len(outgoing) + len(incoming), 1),
            'centrality': nx.degree_centrality(self.graph).get(component_id, 0),
            'betweenness_centrality': nx.betweenness_centrality(self.graph).get(component_id, 0)
        }
        
        # Find strongly connected components
        strong_connections = []
        for target in self.graph.successors(component_id):
            if component_id in self.graph.successors(target):
                strong_connections.append(target)
        
        return {
            'component': {
                'id': component_id,
                'name': component.name,
                'type': component.type.value,
                'domain': component.domain
            },
            'relationships': dict(relationships_by_type),
            'metrics': metrics,
            'strong_connections': strong_connections,
            'analysis': self._generate_relationship_insights(component, relationships_by_type, metrics)
        }
    
    def _generate_relationship_insights(self, component: Component, 
                                      relationships: Dict, metrics: Dict) -> List[str]:
        """Generate insights about component relationships"""
        insights = []
        
        # High connectivity
        if metrics['total_relationships'] > 10:
            insights.append(f"Highly connected component with {metrics['total_relationships']} relationships")
        
        # Cross-domain hub
        if metrics['cross_domain_relationships'] > 3:
            insights.append(f"Cross-domain hub with {metrics['cross_domain_relationships']} inter-domain connections")
        
        # Central component
        if metrics['centrality'] > 0.3:
            insights.append("Central component in the system architecture")
        
        # Bottleneck risk
        if metrics['betweenness_centrality'] > 0.2:
            insights.append("Potential bottleneck - high betweenness centrality")
        
        # Dependency analysis
        deps = relationships.get('outgoing_depends_on', [])
        if len(deps) > 5:
            insights.append(f"High dependency count ({len(deps)}) - consider reducing coupling")
        
        # Trigger chain
        triggers = relationships.get('outgoing_triggers', [])
        if len(triggers) > 3:
            insights.append(f"Triggers {len(triggers)} other components - critical for workflow")
        
        return insights
    
    def find_cross_domain_dependencies(self, domain: str) -> Dict:
        """
        Find all cross-domain dependencies for a specific domain
        
        Args:
            domain: Domain name
            
        Returns:
            Dictionary with cross-domain dependency analysis
        """
        domain_components = self.domain_map.get(domain, set())
        
        if not domain_components:
            return {'error': f'Domain {domain} not found'}
        
        cross_domain_deps = {
            'outgoing': defaultdict(list),
            'incoming': defaultdict(list)
        }
        
        # Analyze each component in the domain
        for component_id in domain_components:
            # Outgoing cross-domain
            for target in self.graph.successors(component_id):
                target_component = self.components.get(target)
                if target_component and target_component.domain != domain:
                    edge_data = self.graph.get_edge_data(component_id, target)
                    cross_domain_deps['outgoing'][target_component.domain].append({
                        'source': component_id,
                        'source_name': self.components[component_id].name,
                        'target': target,
                        'target_name': target_component.name,
                        'relationship': edge_data.get('relationship_type', 'unknown'),
                        'strength': edge_data.get('strength', 0.5)
                    })
            
            # Incoming cross-domain
            for source in self.graph.predecessors(component_id):
                source_component = self.components.get(source)
                if source_component and source_component.domain != domain:
                    edge_data = self.graph.get_edge_data(source, component_id)
                    cross_domain_deps['incoming'][source_component.domain].append({
                        'source': source,
                        'source_name': source_component.name,
                        'target': component_id,
                        'target_name': self.components[component_id].name,
                        'relationship': edge_data.get('relationship_type', 'unknown'),
                        'strength': edge_data.get('strength', 0.5)
                    })
        
        # Calculate summary statistics
        summary = {
            'total_cross_domain_dependencies': sum(
                len(deps) for deps in cross_domain_deps['outgoing'].values()
            ) + sum(
                len(deps) for deps in cross_domain_deps['incoming'].values()
            ),
            'dependent_domains': list(set(
                list(cross_domain_deps['outgoing'].keys()) + 
                list(cross_domain_deps['incoming'].keys())
            )),
            'most_dependent_on': max(
                cross_domain_deps['outgoing'].items(),
                key=lambda x: len(x[1]),
                default=(None, [])
            )[0] if cross_domain_deps['outgoing'] else None,
            'most_depended_by': max(
                cross_domain_deps['incoming'].items(),
                key=lambda x: len(x[1]),
                default=(None, [])
            )[0] if cross_domain_deps['incoming'] else None
        }
        
        return {
            'domain': domain,
            'cross_domain_dependencies': dict(cross_domain_deps),
            'summary': summary,
            'recommendations': self._generate_domain_recommendations(domain, cross_domain_deps, summary)
        }
    
    def _generate_domain_recommendations(self, domain: str, 
                                       dependencies: Dict, summary: Dict) -> List[str]:
        """Generate recommendations for domain dependencies"""
        recommendations = []
        
        total_deps = summary['total_cross_domain_dependencies']
        
        if total_deps > 20:
            recommendations.append(f"High cross-domain coupling ({total_deps} dependencies) - consider domain boundary review")
        
        if summary['most_dependent_on']:
            recommendations.append(f"Strong dependency on {summary['most_dependent_on']} domain - ensure interface stability")
        
        if summary['most_depended_by']:
            recommendations.append(f"Critical provider for {summary['most_depended_by']} domain - maintain backward compatibility")
        
        # Check for circular dependencies
        for other_domain in dependencies['outgoing']:
            if other_domain in dependencies['incoming']:
                recommendations.append(f"Circular dependency with {other_domain} domain - review architecture")
        
        return recommendations
    
    def perform_impact_analysis(self, component_id: str, 
                              change_type: str = 'modify') -> ImpactAnalysis:
        """
        Perform impact analysis for a component change
        
        Args:
            component_id: Component to analyze
            change_type: Type of change ('modify', 'remove', 'add')
            
        Returns:
            ImpactAnalysis with detailed impact assessment
        """
        if component_id not in self.components and change_type != 'add':
            return ImpactAnalysis(
                component=component_id,
                direct_impacts=[],
                indirect_impacts=[],
                affected_domains=set(),
                risk_level='unknown',
                circular_dependencies=[],
                recommendations=['Component not found']
            )
        
        # Find direct impacts
        direct_impacts = []
        affected_domains = set()
        
        if change_type in ['modify', 'remove']:
            # Analyze dependencies
            for target in self.graph.successors(component_id):
                target_comp = self.components.get(target)
                if target_comp:
                    edge_data = self.graph.get_edge_data(component_id, target)
                    impact = {
                        'component': target,
                        'name': target_comp.name,
                        'domain': target_comp.domain,
                        'relationship': edge_data.get('relationship_type', 'unknown'),
                        'severity': self._calculate_impact_severity(edge_data)
                    }
                    direct_impacts.append(impact)
                    affected_domains.add(target_comp.domain)
            
            # Analyze dependents
            for source in self.graph.predecessors(component_id):
                source_comp = self.components.get(source)
                if source_comp:
                    edge_data = self.graph.get_edge_data(source, component_id)
                    impact = {
                        'component': source,
                        'name': source_comp.name,
                        'domain': source_comp.domain,
                        'relationship': edge_data.get('relationship_type', 'unknown'),
                        'severity': self._calculate_impact_severity(edge_data)
                    }
                    direct_impacts.append(impact)
                    affected_domains.add(source_comp.domain)
        
        # Find indirect impacts (2nd degree)
        indirect_impacts = []
        processed = {component_id}
        
        for impact in direct_impacts:
            comp_id = impact['component']
            processed.add(comp_id)
            
            # Check successors
            for target in self.graph.successors(comp_id):
                if target not in processed:
                    target_comp = self.components.get(target)
                    if target_comp:
                        indirect_impacts.append({
                            'component': target,
                            'name': target_comp.name,
                            'domain': target_comp.domain,
                            'via': comp_id,
                            'severity': 'low'  # Indirect impacts are usually lower severity
                        })
                        affected_domains.add(target_comp.domain)
        
        # Detect circular dependencies
        circular_deps = self._detect_circular_dependencies(component_id)
        
        # Calculate risk level
        risk_level = self._calculate_risk_level(
            len(direct_impacts), 
            len(indirect_impacts),
            len(affected_domains),
            circular_deps
        )
        
        # Generate recommendations
        recommendations = self._generate_impact_recommendations(
            component_id, change_type, direct_impacts, affected_domains, risk_level
        )
        
        return ImpactAnalysis(
            component=component_id,
            direct_impacts=direct_impacts,
            indirect_impacts=indirect_impacts,
            affected_domains=affected_domains,
            risk_level=risk_level,
            circular_dependencies=circular_deps,
            recommendations=recommendations
        )
    
    def _calculate_impact_severity(self, edge_data: Dict) -> str:
        """Calculate impact severity based on relationship"""
        rel_type = edge_data.get('relationship_type', '')
        strength = edge_data.get('strength', 0.5)
        
        # Critical relationships
        if rel_type in ['depends_on', 'requires'] and strength > 0.8:
            return 'critical'
        elif rel_type in ['validates', 'triggers'] and strength > 0.7:
            return 'high'
        elif strength > 0.6:
            return 'medium'
        else:
            return 'low'
    
    def _detect_circular_dependencies(self, component_id: str) -> List[List[str]]:
        """Detect circular dependencies involving the component"""
        try:
            # Find all simple cycles in the graph
            cycles = list(nx.simple_cycles(self.graph))
            
            # Filter cycles that include the component
            component_cycles = [
                cycle for cycle in cycles 
                if component_id in cycle
            ]
            
            # Convert to readable format
            readable_cycles = []
            for cycle in component_cycles:
                readable_cycle = []
                for node in cycle:
                    comp = self.components.get(node)
                    readable_cycle.append(
                        comp.name if comp else node
                    )
                readable_cycles.append(readable_cycle)
            
            return readable_cycles
            
        except:
            return []
    
    def _calculate_risk_level(self, direct_count: int, indirect_count: int,
                            domain_count: int, circular_deps: List) -> str:
        """Calculate overall risk level for the change"""
        risk_score = 0
        
        # Direct impact scoring
        if direct_count > 10:
            risk_score += 3
        elif direct_count > 5:
            risk_score += 2
        elif direct_count > 2:
            risk_score += 1
        
        # Indirect impact scoring
        if indirect_count > 20:
            risk_score += 2
        elif indirect_count > 10:
            risk_score += 1
        
        # Cross-domain scoring
        if domain_count > 3:
            risk_score += 2
        elif domain_count > 1:
            risk_score += 1
        
        # Circular dependency scoring
        if circular_deps:
            risk_score += 2
        
        # Map to risk level
        if risk_score >= 7:
            return 'critical'
        elif risk_score >= 5:
            return 'high'
        elif risk_score >= 3:
            return 'medium'
        else:
            return 'low'
    
    def _generate_impact_recommendations(self, component_id: str, change_type: str,
                                       direct_impacts: List[Dict], 
                                       affected_domains: Set[str],
                                       risk_level: str) -> List[str]:
        """Generate recommendations based on impact analysis"""
        recommendations = []
        
        if risk_level in ['critical', 'high']:
            recommendations.append(f"{risk_level.capitalize()} risk change - thorough testing required")
        
        if len(affected_domains) > 2:
            recommendations.append(f"Impacts {len(affected_domains)} domains - coordinate with domain teams")
        
        # Check for critical dependencies
        critical_deps = [
            imp for imp in direct_impacts 
            if imp.get('severity') == 'critical'
        ]
        if critical_deps:
            recommendations.append(f"{len(critical_deps)} critical dependencies - ensure backward compatibility")
        
        # Workflow impacts
        workflow_impacts = [
            imp for imp in direct_impacts
            if imp['component'].startswith('workflow_')
        ]
        if workflow_impacts:
            recommendations.append(f"Affects {len(workflow_impacts)} workflows - update workflow documentation")
        
        # Change-specific recommendations
        if change_type == 'remove':
            recommendations.append("Consider deprecation period before removal")
        elif change_type == 'modify':
            recommendations.append("Maintain interface compatibility where possible")
        
        return recommendations
    
    def find_dependency_path(self, source: str, target: str) -> Optional[List[str]]:
        """
        Find dependency path between two components
        
        Args:
            source: Source component ID
            target: Target component ID
            
        Returns:
            List of component IDs in the path, or None if no path exists
        """
        try:
            path = nx.shortest_path(self.graph, source, target)
            return path
        except nx.NetworkXNoPath:
            return None
    
    def visualize_component_relationships(self, component_id: str, 
                                        depth: int = 2,
                                        output_file: Optional[str] = None):
        """
        Visualize relationships for a component
        
        Args:
            component_id: Component to visualize
            depth: How many levels of relationships to show
            output_file: Optional file to save visualization
        """
        if component_id not in self.components:
            logger.error(f"Component {component_id} not found")
            return
        
        # Create subgraph
        nodes = {component_id}
        
        # Add nodes within depth
        current_level = {component_id}
        for _ in range(depth):
            next_level = set()
            for node in current_level:
                # Add successors and predecessors
                next_level.update(self.graph.successors(node))
                next_level.update(self.graph.predecessors(node))
            nodes.update(next_level)
            current_level = next_level
        
        # Create subgraph
        subgraph = self.graph.subgraph(nodes)
        
        # Set up visualization
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(subgraph, k=2, iterations=50)
        
        # Color nodes by domain
        domain_colors = {
            'producer-portal': 'lightblue',
            'accounting': 'lightgreen',
            'program-manager': 'lightyellow',
            'entity-integration': 'lightcoral',
            'shared': 'lightgray'
        }
        
        node_colors = []
        for node in subgraph.nodes():
            comp = self.components.get(node)
            domain = comp.domain if comp else 'shared'
            node_colors.append(domain_colors.get(domain, 'white'))
        
        # Draw nodes
        nx.draw_networkx_nodes(subgraph, pos, node_color=node_colors, 
                              node_size=1000, alpha=0.9)
        
        # Draw edges with different styles for relationship types
        edge_styles = {
            'depends_on': 'solid',
            'triggers': 'dashed',
            'uses': 'dotted',
            'validates': 'dashdot'
        }
        
        for edge in subgraph.edges(data=True):
            source, target, data = edge
            rel_type = data.get('relationship_type', 'uses')
            style = edge_styles.get(rel_type, 'solid')
            
            nx.draw_networkx_edges(subgraph, pos, [(source, target)],
                                 style=style, alpha=0.6,
                                 width=data.get('strength', 0.5) * 3)
        
        # Draw labels
        labels = {}
        for node in subgraph.nodes():
            comp = self.components.get(node)
            labels[node] = comp.name if comp else node
        
        nx.draw_networkx_labels(subgraph, pos, labels, font_size=8)
        
        # Highlight the central component
        nx.draw_networkx_nodes(subgraph, pos, [component_id],
                             node_color='red', node_size=1200, alpha=0.7)
        
        plt.title(f"Relationships for {self.components[component_id].name}")
        plt.axis('off')
        
        if output_file:
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            logger.info(f"Visualization saved to {output_file}")
        else:
            plt.show()
    
    def export_relationship_analysis(self, output_file: Optional[str] = None) -> Dict:
        """Export comprehensive relationship analysis"""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'total_components': len(self.components),
            'total_relationships': self.graph.number_of_edges(),
            'domains': {
                domain: {
                    'component_count': len(components),
                    'components': list(components)
                }
                for domain, components in self.domain_map.items()
            },
            'cross_domain_analysis': {},
            'critical_components': [],
            'circular_dependencies': [],
            'statistics': {
                'average_degree': sum(dict(self.graph.degree()).values()) / len(self.components) if self.components else 0,
                'density': nx.density(self.graph),
                'connected_components': nx.number_weakly_connected_components(self.graph)
            }
        }
        
        # Analyze each domain
        for domain in self.domain_map:
            analysis['cross_domain_analysis'][domain] = self.find_cross_domain_dependencies(domain)
        
        # Find critical components (high centrality)
        centrality = nx.eigenvector_centrality_numpy(self.graph)
        critical = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        
        for comp_id, score in critical:
            comp = self.components.get(comp_id)
            if comp:
                analysis['critical_components'].append({
                    'id': comp_id,
                    'name': comp.name,
                    'domain': comp.domain,
                    'centrality_score': score
                })
        
        # Find all circular dependencies
        try:
            cycles = list(nx.simple_cycles(self.graph))
            for cycle in cycles[:20]:  # Limit to first 20
                readable_cycle = []
                for node in cycle:
                    comp = self.components.get(node)
                    readable_cycle.append({
                        'id': node,
                        'name': comp.name if comp else node,
                        'domain': comp.domain if comp else 'unknown'
                    })
                analysis['circular_dependencies'].append(readable_cycle)
        except:
            pass
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(analysis, f, indent=2)
            logger.info(f"Analysis exported to {output_file}")
        
        return analysis


# Example usage and testing
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = CrossDomainRelationshipAnalyzer("/app/workspace/requirements/shared-infrastructure/knowledge-base")
    
    # Analyze a specific component
    print("Analyzing driver entity relationships...")
    driver_analysis = analyzer.analyze_component_relationships("entity_driver")
    
    print(f"\nDriver Entity Analysis:")
    print(f"  Total relationships: {driver_analysis['metrics']['total_relationships']}")
    print(f"  Cross-domain relationships: {driver_analysis['metrics']['cross_domain_relationships']}")
    print(f"  Centrality: {driver_analysis['metrics']['centrality']:.3f}")
    
    print("\nInsights:")
    for insight in driver_analysis['analysis']:
        print(f"  - {insight}")
    
    # Find cross-domain dependencies
    print("\n\nAnalyzing Producer Portal domain dependencies...")
    domain_deps = analyzer.find_cross_domain_dependencies("producer-portal")
    
    print(f"\nProducer Portal Cross-Domain Dependencies:")
    print(f"  Total dependencies: {domain_deps['summary']['total_cross_domain_dependencies']}")
    print(f"  Dependent domains: {domain_deps['summary']['dependent_domains']}")
    
    print("\nRecommendations:")
    for rec in domain_deps['recommendations']:
        print(f"  - {rec}")
    
    # Perform impact analysis
    print("\n\nPerforming impact analysis for quote entity modification...")
    impact = analyzer.perform_impact_analysis("entity_quote", "modify")
    
    print(f"\nQuote Entity Impact Analysis:")
    print(f"  Risk level: {impact.risk_level}")
    print(f"  Direct impacts: {len(impact.direct_impacts)}")
    print(f"  Indirect impacts: {len(impact.indirect_impacts)}")
    print(f"  Affected domains: {impact.affected_domains}")
    
    if impact.circular_dependencies:
        print(f"\nCircular dependencies detected:")
        for cycle in impact.circular_dependencies:
            print(f"  - {' -> '.join(cycle)}")
    
    print("\nRecommendations:")
    for rec in impact.recommendations:
        print(f"  - {rec}")
    
    # Find dependency path
    print("\n\nFinding dependency path...")
    path = analyzer.find_dependency_path("workflow_quote_creation", "workflow_billing_setup")
    if path:
        print(f"Path from quote_creation to billing_setup:")
        print(f"  {' -> '.join(path)}")
    
    # Visualize relationships (commented out for non-interactive environments)
    # print("\n\nVisualizing quote entity relationships...")
    # analyzer.visualize_component_relationships("entity_quote", depth=2)