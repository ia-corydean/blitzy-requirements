#!/usr/bin/env python3
"""
Batch Optimization Engine

This engine optimizes the processing of multiple requirements by intelligently
grouping them, determining optimal processing order, and allocating resources
for maximum efficiency.

Features:
- Intelligent requirement grouping
- Processing order optimization
- Resource allocation strategies
- Parallel processing recommendations
- Performance prediction
"""

import json
import logging
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, deque
import numpy as np
from scipy.optimize import linprog
import networkx as nx
from enum import Enum
import heapq

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProcessingStrategy(Enum):
    """Processing strategies for batch optimization"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HYBRID = "hybrid"
    PRIORITY_BASED = "priority_based"
    RESOURCE_AWARE = "resource_aware"


class ResourceType(Enum):
    """Types of resources in the system"""
    AGENT = "agent"
    DATABASE = "database"
    API = "api"
    VALIDATION = "validation"
    MEMORY = "memory"
    COMPUTE = "compute"


@dataclass
class ProcessingTask:
    """Represents a requirement processing task"""
    requirement_id: str
    domain: str
    priority: int  # 1-10, higher is more important
    estimated_time: float  # minutes
    required_resources: Dict[ResourceType, float]
    dependencies: List[str] = field(default_factory=list)
    deadline: Optional[datetime] = None
    metadata: Dict = field(default_factory=dict)


@dataclass
class BatchPlan:
    """Optimized batch processing plan"""
    batch_id: str
    strategy: ProcessingStrategy
    task_groups: List[List[ProcessingTask]]
    processing_order: List[str]
    resource_allocation: Dict[str, Dict[ResourceType, float]]
    estimated_total_time: float
    estimated_savings: float
    parallelization_factor: float
    critical_path: List[str]
    recommendations: List[str] = field(default_factory=list)


@dataclass
class ResourceConstraints:
    """System resource constraints"""
    max_agents: int = 7  # 7 domain specialists
    max_parallel_db_connections: int = 10
    max_api_calls_per_minute: int = 100
    max_memory_gb: float = 16.0
    max_compute_units: float = 8.0


class BatchOptimizationEngine:
    """
    Optimizes batch processing of requirements for maximum efficiency
    """
    
    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.resource_constraints = ResourceConstraints()
        self.processing_history: Dict[str, List[float]] = defaultdict(list)
        self.resource_profiles: Dict[str, Dict] = {}
        self.optimization_cache: Dict[str, BatchPlan] = {}
        self.load_optimization_data()
    
    def load_optimization_data(self):
        """Load historical processing data and resource profiles"""
        try:
            # Load processing history
            history_path = self.knowledge_base_path / "performance-metrics/processing-history.json"
            if history_path.exists():
                with open(history_path, 'r') as f:
                    history_data = json.load(f)
                    self.processing_history = defaultdict(list, history_data)
            
            # Load resource profiles
            profiles_path = self.knowledge_base_path / "performance-metrics/resource-profiles.json"
            if profiles_path.exists():
                with open(profiles_path, 'r') as f:
                    self.resource_profiles = json.load(f)
            
            logger.info("Optimization data loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading optimization data: {e}")
    
    def create_optimization_plan(self, requirements: List[Dict],
                               constraints: Optional[ResourceConstraints] = None,
                               strategy: Optional[ProcessingStrategy] = None) -> BatchPlan:
        """
        Create optimized batch processing plan
        
        Args:
            requirements: List of requirements to process
            constraints: Resource constraints (uses defaults if None)
            strategy: Processing strategy (auto-selected if None)
            
        Returns:
            Optimized BatchPlan
        """
        if not requirements:
            return self._create_empty_plan()
        
        # Use provided constraints or defaults
        if constraints:
            self.resource_constraints = constraints
        
        # Convert requirements to tasks
        tasks = self._convert_to_tasks(requirements)
        
        # Auto-select strategy if not provided
        if not strategy:
            strategy = self._select_optimal_strategy(tasks)
        
        # Create optimization plan based on strategy
        if strategy == ProcessingStrategy.SEQUENTIAL:
            return self._optimize_sequential(tasks)
        elif strategy == ProcessingStrategy.PARALLEL:
            return self._optimize_parallel(tasks)
        elif strategy == ProcessingStrategy.HYBRID:
            return self._optimize_hybrid(tasks)
        elif strategy == ProcessingStrategy.PRIORITY_BASED:
            return self._optimize_priority_based(tasks)
        else:  # RESOURCE_AWARE
            return self._optimize_resource_aware(tasks)
    
    def _convert_to_tasks(self, requirements: List[Dict]) -> List[ProcessingTask]:
        """Convert requirements to processing tasks"""
        tasks = []
        
        for req in requirements:
            # Estimate processing time
            estimated_time = self._estimate_processing_time(req)
            
            # Estimate resource requirements
            resources = self._estimate_resource_requirements(req)
            
            # Extract dependencies
            dependencies = self._extract_dependencies(req)
            
            # Determine priority
            priority = self._calculate_priority(req)
            
            task = ProcessingTask(
                requirement_id=req.get('id', f"req_{id(req)}"),
                domain=req.get('domain', 'unknown'),
                priority=priority,
                estimated_time=estimated_time,
                required_resources=resources,
                dependencies=dependencies,
                deadline=req.get('deadline'),
                metadata={
                    'entities': req.get('entities', []),
                    'integrations': req.get('integrations', []),
                    'complexity': req.get('complexity', 'medium')
                }
            )
            
            tasks.append(task)
        
        return tasks
    
    def _estimate_processing_time(self, requirement: Dict) -> float:
        """Estimate processing time for a requirement"""
        base_time = 10.0  # Base 10 minutes
        
        # Adjust based on complexity
        complexity_factors = {
            'simple': 0.5,
            'medium': 1.0,
            'complex': 2.0,
            'very_complex': 3.0
        }
        complexity = requirement.get('complexity', 'medium')
        base_time *= complexity_factors.get(complexity, 1.0)
        
        # Adjust based on entities
        entity_count = len(requirement.get('entities', []))
        base_time += entity_count * 1.5
        
        # Adjust based on integrations
        integration_count = len(requirement.get('integrations', []))
        base_time += integration_count * 3.0
        
        # Adjust based on validations
        validation_count = len(requirement.get('validations', {}))
        base_time += validation_count * 2.0
        
        # Check historical data
        domain = requirement.get('domain', '')
        if domain in self.processing_history:
            historical_times = self.processing_history[domain]
            if historical_times:
                # Use exponential moving average
                historical_avg = np.mean(historical_times[-10:])  # Last 10 entries
                base_time = 0.7 * base_time + 0.3 * historical_avg
        
        return max(base_time, 5.0)  # Minimum 5 minutes
    
    def _estimate_resource_requirements(self, requirement: Dict) -> Dict[ResourceType, float]:
        """Estimate resource requirements for a requirement"""
        resources = {
            ResourceType.AGENT: 1.0,  # Always needs at least one agent
            ResourceType.DATABASE: 0.0,
            ResourceType.API: 0.0,
            ResourceType.VALIDATION: 0.0,
            ResourceType.MEMORY: 0.1,  # Base 0.1 GB
            ResourceType.COMPUTE: 0.1  # Base 0.1 compute units
        }
        
        # Database resources based on entities
        entity_count = len(requirement.get('entities', []))
        resources[ResourceType.DATABASE] = min(entity_count * 0.5, 3.0)
        
        # API resources based on integrations
        integrations = requirement.get('integrations', [])
        resources[ResourceType.API] = len(integrations) * 10  # 10 calls per integration
        
        # Validation resources
        if requirement.get('validations'):
            resources[ResourceType.VALIDATION] = 1.0
        
        # Memory based on complexity
        complexity_memory = {
            'simple': 0.1,
            'medium': 0.2,
            'complex': 0.5,
            'very_complex': 1.0
        }
        complexity = requirement.get('complexity', 'medium')
        resources[ResourceType.MEMORY] = complexity_memory.get(complexity, 0.2)
        
        # Compute based on workflow
        if requirement.get('workflow', {}).get('steps', []):
            step_count = len(requirement['workflow']['steps'])
            resources[ResourceType.COMPUTE] = min(step_count * 0.1, 2.0)
        
        return resources
    
    def _extract_dependencies(self, requirement: Dict) -> List[str]:
        """Extract dependencies from requirement"""
        dependencies = []
        
        # Explicit dependencies
        if 'dependencies' in requirement:
            dependencies.extend(requirement['dependencies'])
        
        # Workflow dependencies
        workflow = requirement.get('workflow', {})
        if 'depends_on' in workflow:
            dependencies.extend(workflow['depends_on'])
        
        # Previous workflow in sequence
        if 'previous_workflow' in workflow:
            dependencies.append(workflow['previous_workflow'])
        
        return list(set(dependencies))  # Remove duplicates
    
    def _calculate_priority(self, requirement: Dict) -> int:
        """Calculate priority score for a requirement"""
        base_priority = 5  # Default medium priority
        
        # Explicit priority
        if 'priority' in requirement:
            priority_map = {
                'critical': 10,
                'high': 8,
                'medium': 5,
                'low': 3
            }
            base_priority = priority_map.get(requirement['priority'], 5)
        
        # Boost for time-sensitive workflows
        time_sensitive = ['quote_creation', 'payment_processing', 'reinstatement']
        if requirement.get('workflow', {}).get('type') in time_sensitive:
            base_priority = min(base_priority + 2, 10)
        
        # Boost for customer-facing requirements
        if requirement.get('domain') == 'producer-portal':
            base_priority = min(base_priority + 1, 10)
        
        return base_priority
    
    def _select_optimal_strategy(self, tasks: List[ProcessingTask]) -> ProcessingStrategy:
        """Auto-select optimal processing strategy"""
        task_count = len(tasks)
        
        # Check for dependencies
        has_dependencies = any(task.dependencies for task in tasks)
        
        # Check resource constraints
        total_agents_needed = sum(task.required_resources[ResourceType.AGENT] for task in tasks)
        
        # Check priority distribution
        high_priority_count = sum(1 for task in tasks if task.priority >= 8)
        
        # Decision logic
        if task_count <= 3:
            return ProcessingStrategy.SEQUENTIAL
        elif not has_dependencies and total_agents_needed <= self.resource_constraints.max_agents:
            return ProcessingStrategy.PARALLEL
        elif high_priority_count > task_count * 0.3:
            return ProcessingStrategy.PRIORITY_BASED
        elif has_dependencies:
            return ProcessingStrategy.RESOURCE_AWARE
        else:
            return ProcessingStrategy.HYBRID
    
    def _optimize_sequential(self, tasks: List[ProcessingTask]) -> BatchPlan:
        """Optimize for sequential processing"""
        # Sort by priority and dependencies
        sorted_tasks = self._topological_sort_with_priority(tasks)
        
        # Create single group
        task_groups = [[task] for task in sorted_tasks]
        
        # Calculate total time
        total_time = sum(task.estimated_time for task in sorted_tasks)
        
        # No parallelization
        parallelization_factor = 1.0
        
        # Resource allocation (one at a time)
        resource_allocation = {}
        for task in sorted_tasks:
            resource_allocation[task.requirement_id] = task.required_resources
        
        return BatchPlan(
            batch_id=f"batch_seq_{datetime.now().timestamp()}",
            strategy=ProcessingStrategy.SEQUENTIAL,
            task_groups=task_groups,
            processing_order=[task.requirement_id for task in sorted_tasks],
            resource_allocation=resource_allocation,
            estimated_total_time=total_time,
            estimated_savings=0.0,  # No savings in sequential
            parallelization_factor=parallelization_factor,
            critical_path=[task.requirement_id for task in sorted_tasks],
            recommendations=["Consider parallel processing for independent tasks"]
        )
    
    def _optimize_parallel(self, tasks: List[ProcessingTask]) -> BatchPlan:
        """Optimize for parallel processing"""
        # Group by resource compatibility
        groups = self._group_by_resource_compatibility(tasks)
        
        # Balance groups
        balanced_groups = self._balance_task_groups(groups)
        
        # Calculate time (max of group times)
        group_times = [sum(task.estimated_time for task in group) for group in balanced_groups]
        total_time = max(group_times) if group_times else 0
        
        # Calculate savings
        sequential_time = sum(task.estimated_time for task in tasks)
        savings = (sequential_time - total_time) / sequential_time if sequential_time > 0 else 0
        
        # Parallelization factor
        parallelization_factor = len(balanced_groups)
        
        # Resource allocation
        resource_allocation = self._allocate_resources_parallel(balanced_groups)
        
        # Processing order (all groups in parallel)
        processing_order = []
        for group in balanced_groups:
            processing_order.extend([task.requirement_id for task in group])
        
        # Find critical path
        critical_group_idx = group_times.index(max(group_times)) if group_times else 0
        critical_path = [task.requirement_id for task in balanced_groups[critical_group_idx]] if balanced_groups else []
        
        return BatchPlan(
            batch_id=f"batch_par_{datetime.now().timestamp()}",
            strategy=ProcessingStrategy.PARALLEL,
            task_groups=balanced_groups,
            processing_order=processing_order,
            resource_allocation=resource_allocation,
            estimated_total_time=total_time,
            estimated_savings=savings,
            parallelization_factor=parallelization_factor,
            critical_path=critical_path,
            recommendations=self._generate_parallel_recommendations(balanced_groups)
        )
    
    def _optimize_hybrid(self, tasks: List[ProcessingTask]) -> BatchPlan:
        """Optimize using hybrid approach"""
        # Separate independent and dependent tasks
        independent_tasks = [t for t in tasks if not t.dependencies]
        dependent_tasks = [t for t in tasks if t.dependencies]
        
        # Process independent tasks in parallel
        if independent_tasks:
            parallel_groups = self._group_by_resource_compatibility(independent_tasks)
        else:
            parallel_groups = []
        
        # Process dependent tasks sequentially
        if dependent_tasks:
            sequential_order = self._topological_sort_with_priority(dependent_tasks)
            sequential_groups = [[task] for task in sequential_order]
        else:
            sequential_groups = []
        
        # Combine groups
        all_groups = parallel_groups + sequential_groups
        
        # Calculate timing
        parallel_time = max([sum(t.estimated_time for t in g) for g in parallel_groups], default=0)
        sequential_time = sum(t.estimated_time for t in dependent_tasks)
        total_time = parallel_time + sequential_time
        
        # Calculate savings
        all_sequential_time = sum(task.estimated_time for task in tasks)
        savings = (all_sequential_time - total_time) / all_sequential_time if all_sequential_time > 0 else 0
        
        # Resource allocation
        resource_allocation = self._allocate_resources_hybrid(parallel_groups, sequential_groups)
        
        # Processing order
        processing_order = []
        for group in parallel_groups:
            processing_order.extend([t.requirement_id for t in group])
        for group in sequential_groups:
            processing_order.extend([t.requirement_id for t in group])
        
        return BatchPlan(
            batch_id=f"batch_hyb_{datetime.now().timestamp()}",
            strategy=ProcessingStrategy.HYBRID,
            task_groups=all_groups,
            processing_order=processing_order,
            resource_allocation=resource_allocation,
            estimated_total_time=total_time,
            estimated_savings=savings,
            parallelization_factor=len(parallel_groups) if parallel_groups else 1,
            critical_path=processing_order[-len(dependent_tasks):] if dependent_tasks else [],
            recommendations=["Hybrid approach balances parallelism with dependencies"]
        )
    
    def _optimize_priority_based(self, tasks: List[ProcessingTask]) -> BatchPlan:
        """Optimize based on priority"""
        # Sort by priority (descending) and deadline
        sorted_tasks = sorted(
            tasks,
            key=lambda t: (
                -t.priority,
                t.deadline.timestamp() if t.deadline else float('inf')
            )
        )
        
        # Create priority groups
        priority_groups = defaultdict(list)
        for task in sorted_tasks:
            priority_groups[task.priority].append(task)
        
        # Process high priority in parallel, others sequentially
        task_groups = []
        for priority in sorted(priority_groups.keys(), reverse=True):
            group_tasks = priority_groups[priority]
            if priority >= 8 and len(group_tasks) > 1:
                # High priority - try to parallelize
                sub_groups = self._group_by_resource_compatibility(group_tasks)
                task_groups.extend(sub_groups)
            else:
                # Lower priority - sequential within priority
                task_groups.extend([[task] for task in group_tasks])
        
        # Calculate timing with priority consideration
        total_time = 0
        current_time = 0
        high_priority_time = 0
        
        for group in task_groups:
            group_time = max(task.estimated_time for task in group)
            if any(task.priority >= 8 for task in group):
                high_priority_time = max(high_priority_time, group_time)
            else:
                current_time += group_time
        
        total_time = max(high_priority_time, current_time)
        
        # Resource allocation with priority
        resource_allocation = self._allocate_resources_priority(task_groups)
        
        # Processing order
        processing_order = [task.requirement_id for group in task_groups for task in group]
        
        return BatchPlan(
            batch_id=f"batch_pri_{datetime.now().timestamp()}",
            strategy=ProcessingStrategy.PRIORITY_BASED,
            task_groups=task_groups,
            processing_order=processing_order,
            resource_allocation=resource_allocation,
            estimated_total_time=total_time,
            estimated_savings=(sum(t.estimated_time for t in tasks) - total_time) / sum(t.estimated_time for t in tasks),
            parallelization_factor=len([g for g in task_groups if len(g) > 1]),
            critical_path=[t.requirement_id for t in sorted_tasks if t.priority >= 8],
            recommendations=["High priority tasks scheduled first with parallel processing"]
        )
    
    def _optimize_resource_aware(self, tasks: List[ProcessingTask]) -> BatchPlan:
        """Optimize with resource awareness"""
        # Build dependency graph
        dep_graph = self._build_dependency_graph(tasks)
        
        # Find critical path
        critical_path_tasks = self._find_critical_path(dep_graph, tasks)
        
        # Schedule tasks considering resources
        schedule = self._resource_constrained_scheduling(tasks, dep_graph)
        
        # Create groups from schedule
        task_groups = self._schedule_to_groups(schedule)
        
        # Calculate metrics
        total_time = max(end_time for _, end_time in schedule.values())
        sequential_time = sum(task.estimated_time for task in tasks)
        savings = (sequential_time - total_time) / sequential_time if sequential_time > 0 else 0
        
        # Resource allocation
        resource_allocation = {}
        for task_id, (start_time, end_time) in schedule.items():
            task = next(t for t in tasks if t.requirement_id == task_id)
            resource_allocation[task_id] = task.required_resources
        
        return BatchPlan(
            batch_id=f"batch_res_{datetime.now().timestamp()}",
            strategy=ProcessingStrategy.RESOURCE_AWARE,
            task_groups=task_groups,
            processing_order=list(schedule.keys()),
            resource_allocation=resource_allocation,
            estimated_total_time=total_time,
            estimated_savings=savings,
            parallelization_factor=self._calculate_parallelization_factor(schedule),
            critical_path=[t.requirement_id for t in critical_path_tasks],
            recommendations=self._generate_resource_recommendations(schedule, tasks)
        )
    
    def _group_by_resource_compatibility(self, tasks: List[ProcessingTask]) -> List[List[ProcessingTask]]:
        """Group tasks by resource compatibility"""
        groups = []
        remaining = tasks.copy()
        
        while remaining:
            group = [remaining.pop(0)]
            group_resources = group[0].required_resources.copy()
            
            # Try to add compatible tasks
            i = 0
            while i < len(remaining):
                task = remaining[i]
                if self._can_combine_resources(group_resources, task.required_resources):
                    group.append(remaining.pop(i))
                    # Update group resources
                    for res_type, amount in task.required_resources.items():
                        group_resources[res_type] = group_resources.get(res_type, 0) + amount
                else:
                    i += 1
            
            groups.append(group)
        
        return groups
    
    def _can_combine_resources(self, current: Dict[ResourceType, float], 
                             additional: Dict[ResourceType, float]) -> bool:
        """Check if resources can be combined within constraints"""
        combined = current.copy()
        
        for res_type, amount in additional.items():
            combined[res_type] = combined.get(res_type, 0) + amount
        
        # Check constraints
        if combined.get(ResourceType.AGENT, 0) > self.resource_constraints.max_agents:
            return False
        
        if combined.get(ResourceType.DATABASE, 0) > self.resource_constraints.max_parallel_db_connections:
            return False
        
        if combined.get(ResourceType.API, 0) > self.resource_constraints.max_api_calls_per_minute:
            return False
        
        if combined.get(ResourceType.MEMORY, 0) > self.resource_constraints.max_memory_gb:
            return False
        
        if combined.get(ResourceType.COMPUTE, 0) > self.resource_constraints.max_compute_units:
            return False
        
        return True
    
    def _balance_task_groups(self, groups: List[List[ProcessingTask]]) -> List[List[ProcessingTask]]:
        """Balance task groups for even processing time"""
        if len(groups) <= 1:
            return groups
        
        # Calculate group times
        group_times = [sum(task.estimated_time for task in group) for group in groups]
        
        # Rebalance if needed
        avg_time = sum(group_times) / len(groups)
        threshold = avg_time * 0.2  # 20% deviation allowed
        
        balanced_groups = [g.copy() for g in groups]
        
        # Move tasks from heavy groups to light groups
        for _ in range(10):  # Max 10 iterations
            group_times = [sum(task.estimated_time for task in group) for group in balanced_groups]
            
            # Find heaviest and lightest groups
            max_idx = group_times.index(max(group_times))
            min_idx = group_times.index(min(group_times))
            
            if group_times[max_idx] - group_times[min_idx] <= threshold:
                break
            
            # Try to move a task
            if len(balanced_groups[max_idx]) > 1:
                # Find best task to move
                best_task = None
                best_diff = float('inf')
                
                for task in balanced_groups[max_idx]:
                    # Check if can move
                    temp_resources = defaultdict(float)
                    for t in balanced_groups[min_idx]:
                        for res, amt in t.required_resources.items():
                            temp_resources[res] += amt
                    
                    if self._can_combine_resources(dict(temp_resources), task.required_resources):
                        # Calculate improvement
                        new_max = group_times[max_idx] - task.estimated_time
                        new_min = group_times[min_idx] + task.estimated_time
                        new_diff = abs(new_max - new_min)
                        
                        if new_diff < best_diff:
                            best_diff = new_diff
                            best_task = task
                
                if best_task:
                    balanced_groups[max_idx].remove(best_task)
                    balanced_groups[min_idx].append(best_task)
        
        return balanced_groups
    
    def _topological_sort_with_priority(self, tasks: List[ProcessingTask]) -> List[ProcessingTask]:
        """Topological sort considering dependencies and priority"""
        # Build dependency graph
        graph = defaultdict(list)
        in_degree = defaultdict(int)
        task_map = {task.requirement_id: task for task in tasks}
        
        for task in tasks:
            in_degree[task.requirement_id] = 0
        
        for task in tasks:
            for dep in task.dependencies:
                if dep in task_map:
                    graph[dep].append(task.requirement_id)
                    in_degree[task.requirement_id] += 1
        
        # Priority queue for processing (negative priority for max heap)
        queue = []
        for task_id, degree in in_degree.items():
            if degree == 0:
                task = task_map[task_id]
                heapq.heappush(queue, (-task.priority, task.requirement_id))
        
        sorted_tasks = []
        
        while queue:
            _, task_id = heapq.heappop(queue)
            sorted_tasks.append(task_map[task_id])
            
            # Update dependencies
            for neighbor in graph[task_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    task = task_map[neighbor]
                    heapq.heappush(queue, (-task.priority, neighbor))
        
        # Add any remaining tasks (cycles or missing dependencies)
        for task in tasks:
            if task not in sorted_tasks:
                sorted_tasks.append(task)
        
        return sorted_tasks
    
    def _build_dependency_graph(self, tasks: List[ProcessingTask]) -> nx.DiGraph:
        """Build dependency graph from tasks"""
        graph = nx.DiGraph()
        
        # Add nodes
        for task in tasks:
            graph.add_node(task.requirement_id, task=task)
        
        # Add edges
        task_ids = {task.requirement_id for task in tasks}
        for task in tasks:
            for dep in task.dependencies:
                if dep in task_ids:
                    graph.add_edge(dep, task.requirement_id)
        
        return graph
    
    def _find_critical_path(self, graph: nx.DiGraph, tasks: List[ProcessingTask]) -> List[ProcessingTask]:
        """Find critical path in dependency graph"""
        if not graph.nodes():
            return []
        
        # Add dummy start and end nodes
        graph.add_node('START')
        graph.add_node('END')
        
        # Connect start to nodes with no predecessors
        for node in list(graph.nodes()):
            if node not in ['START', 'END'] and graph.in_degree(node) == 0:
                graph.add_edge('START', node, weight=0)
        
        # Connect nodes with no successors to end
        for node in list(graph.nodes()):
            if node not in ['START', 'END'] and graph.out_degree(node) == 0:
                task = next((t for t in tasks if t.requirement_id == node), None)
                weight = task.estimated_time if task else 0
                graph.add_edge(node, 'END', weight=weight)
        
        # Add weights to edges
        for edge in graph.edges():
            if edge[0] != 'START' and edge[1] != 'END' and 'weight' not in graph[edge[0]][edge[1]]:
                task = next((t for t in tasks if t.requirement_id == edge[0]), None)
                graph[edge[0]][edge[1]]['weight'] = task.estimated_time if task else 0
        
        try:
            # Find longest path (critical path)
            path = nx.dag_longest_path(graph, weight='weight')
            
            # Remove dummy nodes and get tasks
            critical_task_ids = [n for n in path if n not in ['START', 'END']]
            critical_tasks = [t for t in tasks if t.requirement_id in critical_task_ids]
            
            return critical_tasks
        except:
            return []
    
    def _resource_constrained_scheduling(self, tasks: List[ProcessingTask], 
                                       dep_graph: nx.DiGraph) -> Dict[str, Tuple[float, float]]:
        """Schedule tasks with resource constraints"""
        schedule = {}  # task_id -> (start_time, end_time)
        resource_usage = defaultdict(lambda: defaultdict(float))  # time -> resource -> usage
        
        # Get tasks in topological order
        try:
            topo_order = list(nx.topological_sort(dep_graph))
            ordered_tasks = [t for tid in topo_order for t in tasks if t.requirement_id == tid]
        except:
            ordered_tasks = sorted(tasks, key=lambda t: (-t.priority, t.requirement_id))
        
        for task in ordered_tasks:
            # Find earliest start time considering dependencies
            earliest_start = 0
            
            for dep in task.dependencies:
                if dep in schedule:
                    earliest_start = max(earliest_start, schedule[dep][1])
            
            # Find time slot with available resources
            start_time = earliest_start
            while True:
                # Check resource availability
                can_schedule = True
                
                for t in range(int(start_time), int(start_time + task.estimated_time)):
                    for res_type, amount in task.required_resources.items():
                        current_usage = resource_usage[t][res_type]
                        
                        if res_type == ResourceType.AGENT:
                            if current_usage + amount > self.resource_constraints.max_agents:
                                can_schedule = False
                                break
                        elif res_type == ResourceType.DATABASE:
                            if current_usage + amount > self.resource_constraints.max_parallel_db_connections:
                                can_schedule = False
                                break
                        # Check other resources...
                    
                    if not can_schedule:
                        break
                
                if can_schedule:
                    # Schedule task
                    end_time = start_time + task.estimated_time
                    schedule[task.requirement_id] = (start_time, end_time)
                    
                    # Update resource usage
                    for t in range(int(start_time), int(end_time)):
                        for res_type, amount in task.required_resources.items():
                            resource_usage[t][res_type] += amount
                    
                    break
                else:
                    # Try next time slot
                    start_time += 1
        
        return schedule
    
    def _schedule_to_groups(self, schedule: Dict[str, Tuple[float, float]]) -> List[List[ProcessingTask]]:
        """Convert schedule to task groups"""
        # Group tasks that run concurrently
        time_groups = defaultdict(list)
        
        for task_id, (start, end) in schedule.items():
            time_groups[start].append(task_id)
        
        # Convert to task groups
        groups = []
        for start_time in sorted(time_groups.keys()):
            group_ids = time_groups[start_time]
            # Note: This is simplified - actual implementation would need the task objects
            groups.append(group_ids)
        
        return groups
    
    def _calculate_parallelization_factor(self, schedule: Dict[str, Tuple[float, float]]) -> float:
        """Calculate effective parallelization factor"""
        if not schedule:
            return 1.0
        
        # Find time periods with concurrent tasks
        time_points = []
        for task_id, (start, end) in schedule.items():
            time_points.append((start, 1))  # Task starts
            time_points.append((end, -1))   # Task ends
        
        time_points.sort()
        
        max_concurrent = 0
        current_concurrent = 0
        
        for time, delta in time_points:
            current_concurrent += delta
            max_concurrent = max(max_concurrent, current_concurrent)
        
        return float(max_concurrent)
    
    def _allocate_resources_parallel(self, groups: List[List[ProcessingTask]]) -> Dict[str, Dict[ResourceType, float]]:
        """Allocate resources for parallel processing"""
        allocation = {}
        
        for group in groups:
            for task in group:
                allocation[task.requirement_id] = task.required_resources
        
        return allocation
    
    def _allocate_resources_hybrid(self, parallel_groups: List[List[ProcessingTask]], 
                                  sequential_groups: List[List[ProcessingTask]]) -> Dict[str, Dict[ResourceType, float]]:
        """Allocate resources for hybrid processing"""
        allocation = {}
        
        # Parallel phase
        for group in parallel_groups:
            for task in group:
                allocation[task.requirement_id] = task.required_resources
        
        # Sequential phase
        for group in sequential_groups:
            for task in group:
                allocation[task.requirement_id] = task.required_resources
        
        return allocation
    
    def _allocate_resources_priority(self, groups: List[List[ProcessingTask]]) -> Dict[str, Dict[ResourceType, float]]:
        """Allocate resources with priority consideration"""
        allocation = {}
        
        # Allocate more resources to high priority tasks
        for group in groups:
            for task in group:
                resources = task.required_resources.copy()
                
                # Boost resources for high priority
                if task.priority >= 8:
                    for res_type in [ResourceType.COMPUTE, ResourceType.MEMORY]:
                        if res_type in resources:
                            resources[res_type] *= 1.5  # 50% boost
                
                allocation[task.requirement_id] = resources
        
        return allocation
    
    def _generate_parallel_recommendations(self, groups: List[List[ProcessingTask]]) -> List[str]:
        """Generate recommendations for parallel processing"""
        recommendations = []
        
        # Check group balance
        group_times = [sum(task.estimated_time for task in group) for group in groups]
        if group_times:
            max_time = max(group_times)
            min_time = min(group_times)
            
            if max_time > min_time * 1.5:
                recommendations.append("Consider rebalancing groups for better time distribution")
        
        # Check resource utilization
        total_agents = sum(
            max(task.required_resources.get(ResourceType.AGENT, 0) for task in group)
            for group in groups
        )
        
        if total_agents < self.resource_constraints.max_agents * 0.7:
            recommendations.append("Resource underutilization - consider increasing parallelization")
        
        return recommendations
    
    def _generate_resource_recommendations(self, schedule: Dict[str, Tuple[float, float]], 
                                         tasks: List[ProcessingTask]) -> List[str]:
        """Generate recommendations for resource-aware processing"""
        recommendations = []
        
        # Check for resource bottlenecks
        resource_peaks = defaultdict(float)
        
        for task in tasks:
            for res_type, amount in task.required_resources.items():
                resource_peaks[res_type] = max(resource_peaks[res_type], amount)
        
        # Agent bottleneck
        if resource_peaks[ResourceType.AGENT] > self.resource_constraints.max_agents * 0.8:
            recommendations.append("Agent capacity near limit - consider scaling or optimizing agent usage")
        
        # Database bottleneck
        if resource_peaks[ResourceType.DATABASE] > self.resource_constraints.max_parallel_db_connections * 0.8:
            recommendations.append("Database connections near limit - consider connection pooling optimization")
        
        # API rate limiting
        if resource_peaks[ResourceType.API] > self.resource_constraints.max_api_calls_per_minute * 0.8:
            recommendations.append("API rate limit risk - implement request queuing or caching")
        
        return recommendations
    
    def _create_empty_plan(self) -> BatchPlan:
        """Create empty batch plan"""
        return BatchPlan(
            batch_id=f"batch_empty_{datetime.now().timestamp()}",
            strategy=ProcessingStrategy.SEQUENTIAL,
            task_groups=[],
            processing_order=[],
            resource_allocation={},
            estimated_total_time=0,
            estimated_savings=0,
            parallelization_factor=1,
            critical_path=[],
            recommendations=["No requirements to process"]
        )
    
    def simulate_execution(self, plan: BatchPlan) -> Dict:
        """Simulate execution of batch plan"""
        simulation = {
            'batch_id': plan.batch_id,
            'start_time': datetime.now().isoformat(),
            'events': [],
            'resource_timeline': defaultdict(list),
            'completion_times': {}
        }
        
        current_time = 0
        
        # Simulate based on strategy
        if plan.strategy == ProcessingStrategy.SEQUENTIAL:
            for group in plan.task_groups:
                for task in group:
                    simulation['events'].append({
                        'time': current_time,
                        'event': 'start',
                        'task': task.requirement_id,
                        'resources': task.required_resources
                    })
                    
                    current_time += task.estimated_time
                    
                    simulation['events'].append({
                        'time': current_time,
                        'event': 'complete',
                        'task': task.requirement_id
                    })
                    
                    simulation['completion_times'][task.requirement_id] = current_time
        
        elif plan.strategy == ProcessingStrategy.PARALLEL:
            # Simulate parallel execution
            group_end_times = []
            
            for group_idx, group in enumerate(plan.task_groups):
                group_start = 0
                group_end = 0
                
                for task in group:
                    simulation['events'].append({
                        'time': group_start,
                        'event': 'start',
                        'task': task.requirement_id,
                        'group': group_idx,
                        'resources': task.required_resources
                    })
                    
                    task_end = group_start + task.estimated_time
                    group_end = max(group_end, task_end)
                    
                    simulation['completion_times'][task.requirement_id] = task_end
                
                group_end_times.append(group_end)
            
            # Add completion events
            for group_idx, group in enumerate(plan.task_groups):
                for task in group:
                    simulation['events'].append({
                        'time': simulation['completion_times'][task.requirement_id],
                        'event': 'complete',
                        'task': task.requirement_id,
                        'group': group_idx
                    })
        
        simulation['end_time'] = (datetime.now() + timedelta(minutes=plan.estimated_total_time)).isoformat()
        simulation['total_duration_minutes'] = plan.estimated_total_time
        
        return simulation
    
    def export_optimization_report(self, requirements: List[Dict], plan: BatchPlan) -> Dict:
        """Export comprehensive optimization report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_requirements': len(requirements),
                'optimization_strategy': plan.strategy.value,
                'estimated_time': f"{plan.estimated_total_time:.1f} minutes",
                'time_savings': f"{plan.estimated_savings * 100:.1f}%",
                'parallelization_factor': plan.parallelization_factor,
                'number_of_groups': len(plan.task_groups)
            },
            'resource_analysis': {
                'peak_agent_usage': 0,
                'peak_database_connections': 0,
                'total_api_calls': 0,
                'peak_memory_gb': 0,
                'peak_compute_units': 0
            },
            'group_details': [],
            'critical_path': plan.critical_path,
            'recommendations': plan.recommendations,
            'execution_timeline': []
        }
        
        # Analyze resource usage
        for group in plan.task_groups:
            group_resources = defaultdict(float)
            group_time = 0
            
            for task in group:
                for res_type, amount in task.required_resources.items():
                    group_resources[res_type] += amount
                group_time = max(group_time, task.estimated_time)
            
            report['resource_analysis']['peak_agent_usage'] = max(
                report['resource_analysis']['peak_agent_usage'],
                group_resources.get(ResourceType.AGENT, 0)
            )
            
            report['resource_analysis']['peak_database_connections'] = max(
                report['resource_analysis']['peak_database_connections'],
                group_resources.get(ResourceType.DATABASE, 0)
            )
            
            report['resource_analysis']['total_api_calls'] += group_resources.get(ResourceType.API, 0)
            
            report['resource_analysis']['peak_memory_gb'] = max(
                report['resource_analysis']['peak_memory_gb'],
                group_resources.get(ResourceType.MEMORY, 0)
            )
            
            report['resource_analysis']['peak_compute_units'] = max(
                report['resource_analysis']['peak_compute_units'],
                group_resources.get(ResourceType.COMPUTE, 0)
            )
            
            # Group details
            report['group_details'].append({
                'group_size': len(group),
                'estimated_time': group_time,
                'task_ids': [task.requirement_id for task in group],
                'domains': list(set(task.domain for task in group)),
                'total_priority': sum(task.priority for task in group)
            })
        
        # Add execution timeline
        if plan.strategy == ProcessingStrategy.SEQUENTIAL:
            time = 0
            for group in plan.task_groups:
                for task in group:
                    report['execution_timeline'].append({
                        'start': time,
                        'end': time + task.estimated_time,
                        'task': task.requirement_id,
                        'duration': task.estimated_time
                    })
                    time += task.estimated_time
        else:
            # Simplified parallel timeline
            for idx, group in enumerate(plan.task_groups):
                start_time = 0 if idx == 0 else report['execution_timeline'][-1]['end'] if plan.strategy != ProcessingStrategy.PARALLEL else 0
                
                for task in group:
                    report['execution_timeline'].append({
                        'start': start_time,
                        'end': start_time + task.estimated_time,
                        'task': task.requirement_id,
                        'duration': task.estimated_time,
                        'parallel_group': idx
                    })
        
        return report


# Example usage and testing
if __name__ == "__main__":
    # Initialize optimizer
    optimizer = BatchOptimizationEngine("/app/workspace/requirements/shared-infrastructure/knowledge-base")
    
    # Example requirements
    requirements = [
        {
            'id': 'req_001',
            'domain': 'producer-portal',
            'priority': 'high',
            'entities': ['driver', 'vehicle', 'quote'],
            'integrations': ['DCS'],
            'complexity': 'medium',
            'workflow': {
                'type': 'quote_creation',
                'steps': ['collect_driver', 'add_vehicles', 'calculate_rate']
            }
        },
        {
            'id': 'req_002',
            'domain': 'producer-portal',
            'priority': 'critical',
            'entities': ['quote', 'policy'],
            'integrations': ['payment_gateway'],
            'complexity': 'complex',
            'workflow': {
                'type': 'quote_binding',
                'depends_on': ['req_001']
            }
        },
        {
            'id': 'req_003',
            'domain': 'accounting',
            'priority': 'medium',
            'entities': ['payment', 'billing'],
            'integrations': ['payment_gateway'],
            'complexity': 'medium',
            'workflow': {
                'type': 'billing_setup',
                'depends_on': ['req_002']
            }
        },
        {
            'id': 'req_004',
            'domain': 'entity-integration',
            'priority': 'high',
            'entities': ['driver', 'license'],
            'integrations': ['DCS'],
            'complexity': 'simple',
            'workflow': {
                'type': 'driver_verification'
            }
        },
        {
            'id': 'req_005',
            'domain': 'producer-portal',
            'priority': 'medium',
            'entities': ['vehicle'],
            'integrations': [],
            'complexity': 'simple',
            'workflow': {
                'type': 'vehicle_update'
            }
        }
    ]
    
    # Create optimization plan
    print("Creating optimization plan...")
    plan = optimizer.create_optimization_plan(requirements)
    
    print(f"\nOptimization Strategy: {plan.strategy.value}")
    print(f"Estimated Total Time: {plan.estimated_total_time:.1f} minutes")
    print(f"Time Savings: {plan.estimated_savings * 100:.1f}%")
    print(f"Parallelization Factor: {plan.parallelization_factor}")
    
    print(f"\nTask Groups ({len(plan.task_groups)}):")
    for i, group in enumerate(plan.task_groups):
        print(f"\n  Group {i+1} ({len(group)} tasks):")
        for task in group:
            print(f"    - {task.requirement_id} ({task.domain}) - Priority: {task.priority}")
    
    print(f"\nCritical Path: {' -> '.join(plan.critical_path)}")
    
    print("\nRecommendations:")
    for rec in plan.recommendations:
        print(f"  - {rec}")
    
    # Test different strategies
    print("\n\nTesting different strategies...")
    for strategy in ProcessingStrategy:
        test_plan = optimizer.create_optimization_plan(requirements, strategy=strategy)
        print(f"\n{strategy.value}:")
        print(f"  Time: {test_plan.estimated_total_time:.1f} min")
        print(f"  Savings: {test_plan.estimated_savings * 100:.1f}%")
        print(f"  Groups: {len(test_plan.task_groups)}")
    
    # Simulate execution
    print("\n\nSimulating execution...")
    simulation = optimizer.simulate_execution(plan)
    print(f"Simulation events: {len(simulation['events'])}")
    print(f"Total duration: {simulation['total_duration_minutes']:.1f} minutes")
    
    # Generate report
    print("\n\nGenerating optimization report...")
    report = optimizer.export_optimization_report(requirements, plan)
    print(f"Report generated with {len(report['group_details'])} groups")
    print(f"Peak agent usage: {report['resource_analysis']['peak_agent_usage']}")
    print(f"Total API calls: {report['resource_analysis']['total_api_calls']}")