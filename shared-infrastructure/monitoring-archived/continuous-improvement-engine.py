#!/usr/bin/env python3
"""
Continuous Improvement Engine for Requirements Generation System

This engine analyzes system performance, identifies optimization opportunities,
and automatically implements improvements to enhance efficiency and quality.

Features:
- Pattern analysis for optimization opportunities
- Automated tuning of system parameters
- Learning from historical performance
- Recommendation generation
- A/B testing framework for improvements
"""

import json
import logging
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
import pickle
from enum import Enum
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImprovementType(Enum):
    """Types of improvements that can be made"""
    PARAMETER_TUNING = "parameter_tuning"
    WORKFLOW_OPTIMIZATION = "workflow_optimization"
    RESOURCE_ALLOCATION = "resource_allocation"
    PATTERN_REUSE = "pattern_reuse"
    BATCH_STRATEGY = "batch_strategy"
    CACHE_OPTIMIZATION = "cache_optimization"
    ERROR_REDUCTION = "error_reduction"


class ExperimentStatus(Enum):
    """Status of improvement experiments"""
    PROPOSED = "proposed"
    RUNNING = "running"
    COMPLETED = "completed"
    ADOPTED = "adopted"
    REJECTED = "rejected"


@dataclass
class PerformanceMetric:
    """Performance metric for analysis"""
    name: str
    current_value: float
    target_value: float
    historical_values: List[float]
    trend: str  # 'improving', 'stable', 'degrading'
    importance: float  # 0-1 scale


@dataclass
class ImprovementOpportunity:
    """Identified opportunity for improvement"""
    id: str
    type: ImprovementType
    description: str
    expected_benefit: float  # Percentage improvement
    confidence: float  # 0-1 scale
    effort: str  # 'low', 'medium', 'high'
    risk: str  # 'low', 'medium', 'high'
    parameters: Dict[str, Any]
    affected_components: List[str]


@dataclass
class Experiment:
    """A/B test experiment for improvements"""
    id: str
    opportunity_id: str
    start_time: datetime
    end_time: Optional[datetime]
    status: ExperimentStatus
    control_group: Dict[str, Any]
    treatment_group: Dict[str, Any]
    metrics_before: Dict[str, float]
    metrics_after: Optional[Dict[str, float]]
    statistical_significance: Optional[float]
    adopted: bool = False


@dataclass
class LearningRecord:
    """Record of what the system has learned"""
    timestamp: datetime
    learning_type: str
    description: str
    impact: float
    context: Dict[str, Any]


class ContinuousImprovementEngine:
    """
    Engine for continuous system improvement through analysis and learning
    """
    
    def __init__(self, knowledge_base_path: str, metrics_path: str):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.metrics_path = Path(metrics_path)
        self.improvements_path = self.metrics_path / "improvements"
        self.improvements_path.mkdir(parents=True, exist_ok=True)
        
        # System parameters that can be tuned
        self.tunable_parameters = {
            'batch_size': {'min': 5, 'max': 50, 'current': 20},
            'parallel_agents': {'min': 1, 'max': 7, 'current': 3},
            'cache_ttl': {'min': 300, 'max': 3600, 'current': 900},
            'similarity_threshold': {'min': 0.5, 'max': 0.95, 'current': 0.7},
            'confidence_threshold': {'min': 0.6, 'max': 0.9, 'current': 0.75},
            'queue_poll_interval': {'min': 1, 'max': 30, 'current': 5},
            'retry_attempts': {'min': 1, 'max': 5, 'current': 3},
            'timeout_seconds': {'min': 60, 'max': 600, 'current': 300}
        }
        
        # Performance targets
        self.performance_targets = {
            'avg_processing_time': 180,  # seconds
            'success_rate': 0.95,
            'throughput_per_hour': 50,
            'resource_utilization': 0.75,
            'error_rate': 0.05,
            'queue_depth': 20
        }
        
        # Historical performance data
        self.performance_history: Dict[str, List[PerformanceMetric]] = defaultdict(list)
        
        # Active experiments
        self.experiments: Dict[str, Experiment] = {}
        
        # Learning records
        self.learning_records: List[LearningRecord] = []
        
        # ML models for prediction
        self.performance_predictor = None
        self.pattern_classifier = None
        
        # Load historical data
        self._load_historical_data()
    
    def _load_historical_data(self):
        """Load historical performance and learning data"""
        try:
            # Load performance history
            history_file = self.improvements_path / "performance_history.json"
            if history_file.exists():
                with open(history_file, 'r') as f:
                    data = json.load(f)
                    # Convert to proper format
                    for metric_name, values in data.items():
                        self.performance_history[metric_name] = [
                            PerformanceMetric(**v) for v in values
                        ]
            
            # Load learning records
            learning_file = self.improvements_path / "learning_records.json"
            if learning_file.exists():
                with open(learning_file, 'r') as f:
                    records = json.load(f)
                    self.learning_records = [
                        LearningRecord(
                            timestamp=datetime.fromisoformat(r['timestamp']),
                            learning_type=r['learning_type'],
                            description=r['description'],
                            impact=r['impact'],
                            context=r['context']
                        )
                        for r in records
                    ]
            
            # Load ML models
            self._load_ml_models()
            
        except Exception as e:
            logger.error(f"Error loading historical data: {e}")
    
    def _load_ml_models(self):
        """Load or initialize ML models"""
        try:
            # Performance predictor
            predictor_file = self.improvements_path / "performance_predictor.pkl"
            if predictor_file.exists():
                with open(predictor_file, 'rb') as f:
                    self.performance_predictor = pickle.load(f)
            else:
                self.performance_predictor = RandomForestRegressor(n_estimators=100)
            
            # Pattern classifier
            classifier_file = self.improvements_path / "pattern_classifier.pkl"
            if classifier_file.exists():
                with open(classifier_file, 'rb') as f:
                    self.pattern_classifier = pickle.load(f)
            else:
                self.pattern_classifier = KMeans(n_clusters=5)
            
        except Exception as e:
            logger.error(f"Error loading ML models: {e}")
            self.performance_predictor = RandomForestRegressor(n_estimators=100)
            self.pattern_classifier = KMeans(n_clusters=5)
    
    def analyze_performance(self, current_metrics: Dict[str, float]) -> List[ImprovementOpportunity]:
        """
        Analyze current performance and identify improvement opportunities
        
        Args:
            current_metrics: Current system metrics
            
        Returns:
            List of improvement opportunities
        """
        opportunities = []
        
        # Update performance history
        self._update_performance_history(current_metrics)
        
        # Check each metric against targets
        for metric_name, current_value in current_metrics.items():
            if metric_name in self.performance_targets:
                target_value = self.performance_targets[metric_name]
                
                # Calculate performance gap
                if metric_name in ['error_rate', 'avg_processing_time', 'queue_depth']:
                    # Lower is better
                    gap = (current_value - target_value) / target_value
                else:
                    # Higher is better
                    gap = (target_value - current_value) / target_value
                
                if gap > 0.1:  # More than 10% off target
                    # Identify improvement opportunities
                    metric_opportunities = self._identify_metric_improvements(
                        metric_name, current_value, target_value, gap
                    )
                    opportunities.extend(metric_opportunities)
        
        # Analyze patterns for optimization
        pattern_opportunities = self._analyze_patterns()
        opportunities.extend(pattern_opportunities)
        
        # Analyze resource utilization
        resource_opportunities = self._analyze_resource_utilization(current_metrics)
        opportunities.extend(resource_opportunities)
        
        # Rank opportunities by expected benefit
        opportunities.sort(key=lambda x: x.expected_benefit * x.confidence, reverse=True)
        
        return opportunities
    
    def _update_performance_history(self, current_metrics: Dict[str, float]):
        """Update performance history with current metrics"""
        for metric_name, value in current_metrics.items():
            history = self.performance_history[metric_name]
            
            # Calculate trend
            if len(history) >= 5:
                recent_values = [m.current_value for m in history[-5:]]
                trend = self._calculate_trend(recent_values + [value])
            else:
                trend = 'stable'
            
            # Create metric record
            metric = PerformanceMetric(
                name=metric_name,
                current_value=value,
                target_value=self.performance_targets.get(metric_name, value),
                historical_values=[m.current_value for m in history[-20:]],
                trend=trend,
                importance=self._calculate_metric_importance(metric_name)
            )
            
            history.append(metric)
            
            # Keep only recent history
            if len(history) > 100:
                self.performance_history[metric_name] = history[-100:]
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend from values"""
        if len(values) < 2:
            return 'stable'
        
        # Simple linear regression
        x = list(range(len(values)))
        slope = np.polyfit(x, values, 1)[0]
        
        # Normalize by mean
        mean_value = statistics.mean(values)
        normalized_slope = slope / mean_value if mean_value != 0 else 0
        
        if abs(normalized_slope) < 0.01:
            return 'stable'
        elif normalized_slope > 0:
            return 'degrading'  # Assuming lower is better for most metrics
        else:
            return 'improving'
    
    def _calculate_metric_importance(self, metric_name: str) -> float:
        """Calculate importance of a metric"""
        # Define importance weights
        importance_weights = {
            'success_rate': 1.0,
            'avg_processing_time': 0.9,
            'throughput_per_hour': 0.8,
            'error_rate': 0.9,
            'resource_utilization': 0.7,
            'queue_depth': 0.6
        }
        
        return importance_weights.get(metric_name, 0.5)
    
    def _identify_metric_improvements(self, metric_name: str, current_value: float,
                                    target_value: float, gap: float) -> List[ImprovementOpportunity]:
        """Identify improvements for a specific metric"""
        opportunities = []
        
        if metric_name == 'avg_processing_time' and gap > 0.2:
            # Processing time is too high
            opportunities.append(ImprovementOpportunity(
                id=f"opt_batch_size_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                type=ImprovementType.PARAMETER_TUNING,
                description="Increase batch size to amortize processing overhead",
                expected_benefit=min(gap * 0.3, 0.2),  # Up to 20% improvement
                confidence=0.8,
                effort='low',
                risk='low',
                parameters={
                    'parameter': 'batch_size',
                    'current': self.tunable_parameters['batch_size']['current'],
                    'proposed': min(
                        self.tunable_parameters['batch_size']['current'] * 1.5,
                        self.tunable_parameters['batch_size']['max']
                    )
                },
                affected_components=['batch_processor']
            ))
            
            opportunities.append(ImprovementOpportunity(
                id=f"opt_parallel_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                type=ImprovementType.RESOURCE_ALLOCATION,
                description="Increase parallel agent count for faster processing",
                expected_benefit=min(gap * 0.4, 0.3),
                confidence=0.7,
                effort='medium',
                risk='medium',
                parameters={
                    'parameter': 'parallel_agents',
                    'current': self.tunable_parameters['parallel_agents']['current'],
                    'proposed': min(
                        self.tunable_parameters['parallel_agents']['current'] + 1,
                        self.tunable_parameters['parallel_agents']['max']
                    )
                },
                affected_components=['agent_manager', 'resource_allocator']
            ))
        
        elif metric_name == 'success_rate' and current_value < target_value:
            # Success rate is too low
            opportunities.append(ImprovementOpportunity(
                id=f"opt_retry_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                type=ImprovementType.ERROR_REDUCTION,
                description="Increase retry attempts for transient failures",
                expected_benefit=(target_value - current_value) * 0.5,
                confidence=0.6,
                effort='low',
                risk='low',
                parameters={
                    'parameter': 'retry_attempts',
                    'current': self.tunable_parameters['retry_attempts']['current'],
                    'proposed': min(
                        self.tunable_parameters['retry_attempts']['current'] + 1,
                        self.tunable_parameters['retry_attempts']['max']
                    )
                },
                affected_components=['error_handler']
            ))
            
            opportunities.append(ImprovementOpportunity(
                id=f"opt_timeout_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                type=ImprovementType.PARAMETER_TUNING,
                description="Increase timeout to reduce timeout failures",
                expected_benefit=(target_value - current_value) * 0.3,
                confidence=0.5,
                effort='low',
                risk='medium',
                parameters={
                    'parameter': 'timeout_seconds',
                    'current': self.tunable_parameters['timeout_seconds']['current'],
                    'proposed': min(
                        self.tunable_parameters['timeout_seconds']['current'] * 1.2,
                        self.tunable_parameters['timeout_seconds']['max']
                    )
                },
                affected_components=['request_handler']
            ))
        
        elif metric_name == 'throughput_per_hour' and current_value < target_value:
            # Throughput is too low
            opportunities.append(ImprovementOpportunity(
                id=f"opt_cache_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                type=ImprovementType.CACHE_OPTIMIZATION,
                description="Increase cache TTL to reduce redundant processing",
                expected_benefit=(target_value - current_value) / target_value * 0.4,
                confidence=0.7,
                effort='low',
                risk='low',
                parameters={
                    'parameter': 'cache_ttl',
                    'current': self.tunable_parameters['cache_ttl']['current'],
                    'proposed': min(
                        self.tunable_parameters['cache_ttl']['current'] * 1.5,
                        self.tunable_parameters['cache_ttl']['max']
                    )
                },
                affected_components=['cache_manager']
            ))
        
        return opportunities
    
    def _analyze_patterns(self) -> List[ImprovementOpportunity]:
        """Analyze patterns in system behavior for optimization"""
        opportunities = []
        
        # Analyze error patterns
        if 'error_rate' in self.performance_history:
            error_history = self.performance_history['error_rate']
            if len(error_history) > 10:
                # Check for recurring error spikes
                error_values = [m.current_value for m in error_history[-20:]]
                if max(error_values) > statistics.mean(error_values) * 2:
                    opportunities.append(ImprovementOpportunity(
                        id=f"opt_error_pattern_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        type=ImprovementType.ERROR_REDUCTION,
                        description="Implement pattern-based error prediction and prevention",
                        expected_benefit=0.15,
                        confidence=0.6,
                        effort='high',
                        risk='medium',
                        parameters={
                            'strategy': 'predictive_error_handling',
                            'pattern_window': 10
                        },
                        affected_components=['error_predictor', 'request_validator']
                    ))
        
        # Analyze processing time patterns
        if 'avg_processing_time' in self.performance_history:
            time_history = self.performance_history['avg_processing_time']
            if len(time_history) > 20:
                # Check for time-based patterns (e.g., peak hours)
                recent_times = [m.current_value for m in time_history[-24:]]
                if max(recent_times) > statistics.mean(recent_times) * 1.5:
                    opportunities.append(ImprovementOpportunity(
                        id=f"opt_schedule_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        type=ImprovementType.WORKFLOW_OPTIMIZATION,
                        description="Implement time-based resource scaling",
                        expected_benefit=0.2,
                        confidence=0.7,
                        effort='medium',
                        risk='low',
                        parameters={
                            'strategy': 'dynamic_scaling',
                            'scale_factor': 1.5,
                            'prediction_window': 60  # minutes
                        },
                        affected_components=['resource_scheduler', 'load_balancer']
                    ))
        
        return opportunities
    
    def _analyze_resource_utilization(self, current_metrics: Dict[str, float]) -> List[ImprovementOpportunity]:
        """Analyze resource utilization for optimization"""
        opportunities = []
        
        utilization = current_metrics.get('resource_utilization', 0)
        
        if utilization < 0.5:
            # Under-utilized
            opportunities.append(ImprovementOpportunity(
                id=f"opt_consolidate_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                type=ImprovementType.RESOURCE_ALLOCATION,
                description="Consolidate resources to improve efficiency",
                expected_benefit=0.1,
                confidence=0.8,
                effort='medium',
                risk='low',
                parameters={
                    'strategy': 'resource_consolidation',
                    'target_utilization': 0.75
                },
                affected_components=['resource_manager']
            ))
        elif utilization > 0.9:
            # Over-utilized
            opportunities.append(ImprovementOpportunity(
                id=f"opt_scale_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                type=ImprovementType.RESOURCE_ALLOCATION,
                description="Scale resources to prevent bottlenecks",
                expected_benefit=0.25,
                confidence=0.9,
                effort='medium',
                risk='medium',
                parameters={
                    'strategy': 'resource_scaling',
                    'scale_factor': 1.3
                },
                affected_components=['resource_manager', 'load_balancer']
            ))
        
        return opportunities
    
    def create_experiment(self, opportunity: ImprovementOpportunity) -> Experiment:
        """Create an A/B test experiment for an improvement opportunity"""
        experiment = Experiment(
            id=f"exp_{opportunity.id}",
            opportunity_id=opportunity.id,
            start_time=datetime.now(),
            end_time=None,
            status=ExperimentStatus.PROPOSED,
            control_group={
                'size': 0.5,
                'parameters': {
                    param: self.tunable_parameters[param]['current']
                    for param in self.tunable_parameters
                }
            },
            treatment_group={
                'size': 0.5,
                'parameters': {
                    **{param: self.tunable_parameters[param]['current']
                       for param in self.tunable_parameters},
                    **opportunity.parameters
                }
            },
            metrics_before=self._get_current_metrics(),
            metrics_after=None,
            statistical_significance=None
        )
        
        self.experiments[experiment.id] = experiment
        return experiment
    
    def _get_current_metrics(self) -> Dict[str, float]:
        """Get current system metrics"""
        # In production, this would fetch from the metrics system
        current_metrics = {}
        
        for metric_name in self.performance_targets:
            if metric_name in self.performance_history:
                history = self.performance_history[metric_name]
                if history:
                    current_metrics[metric_name] = history[-1].current_value
                else:
                    current_metrics[metric_name] = self.performance_targets[metric_name]
            else:
                current_metrics[metric_name] = self.performance_targets[metric_name]
        
        return current_metrics
    
    def run_experiment(self, experiment_id: str, duration_hours: int = 24):
        """Run an experiment for a specified duration"""
        if experiment_id not in self.experiments:
            logger.error(f"Experiment {experiment_id} not found")
            return
        
        experiment = self.experiments[experiment_id]
        experiment.status = ExperimentStatus.RUNNING
        experiment.end_time = datetime.now() + timedelta(hours=duration_hours)
        
        logger.info(f"Started experiment {experiment_id} for {duration_hours} hours")
        
        # In production, this would actually configure the system for A/B testing
        # For now, we'll simulate the results
        self._simulate_experiment_results(experiment)
    
    def _simulate_experiment_results(self, experiment: Experiment):
        """Simulate experiment results (for testing)"""
        # Simulate some improvement
        metrics_after = {}
        
        for metric_name, before_value in experiment.metrics_before.items():
            # Simulate improvement based on opportunity type
            improvement = np.random.normal(0.1, 0.05)  # 10% ± 5% improvement
            
            if metric_name in ['error_rate', 'avg_processing_time']:
                # Lower is better
                metrics_after[metric_name] = before_value * (1 - improvement)
            else:
                # Higher is better
                metrics_after[metric_name] = before_value * (1 + improvement)
        
        experiment.metrics_after = metrics_after
        experiment.statistical_significance = np.random.uniform(0.9, 0.99)
        experiment.status = ExperimentStatus.COMPLETED
    
    def evaluate_experiment(self, experiment_id: str) -> Dict[str, Any]:
        """Evaluate experiment results"""
        if experiment_id not in self.experiments:
            return {'error': 'Experiment not found'}
        
        experiment = self.experiments[experiment_id]
        
        if experiment.status != ExperimentStatus.COMPLETED:
            return {'error': 'Experiment not completed'}
        
        # Calculate improvements
        improvements = {}
        for metric_name in experiment.metrics_before:
            before = experiment.metrics_before[metric_name]
            after = experiment.metrics_after[metric_name]
            
            if metric_name in ['error_rate', 'avg_processing_time', 'queue_depth']:
                # Lower is better
                improvement = (before - after) / before if before > 0 else 0
            else:
                # Higher is better
                improvement = (after - before) / before if before > 0 else 0
            
            improvements[metric_name] = improvement
        
        # Decision criteria
        overall_improvement = statistics.mean(improvements.values())
        significant = experiment.statistical_significance > 0.95
        positive_impact = overall_improvement > 0.05  # 5% improvement threshold
        
        recommendation = 'adopt' if significant and positive_impact else 'reject'
        
        return {
            'experiment_id': experiment_id,
            'improvements': improvements,
            'overall_improvement': overall_improvement,
            'statistical_significance': experiment.statistical_significance,
            'recommendation': recommendation,
            'significant': significant,
            'positive_impact': positive_impact
        }
    
    def adopt_improvement(self, experiment_id: str):
        """Adopt improvements from a successful experiment"""
        if experiment_id not in self.experiments:
            logger.error(f"Experiment {experiment_id} not found")
            return
        
        experiment = self.experiments[experiment_id]
        
        if experiment.status != ExperimentStatus.COMPLETED:
            logger.error(f"Experiment {experiment_id} not completed")
            return
        
        # Update tunable parameters
        for param_name, param_value in experiment.treatment_group['parameters'].items():
            if param_name in self.tunable_parameters:
                old_value = self.tunable_parameters[param_name]['current']
                self.tunable_parameters[param_name]['current'] = param_value
                
                # Record learning
                self.learning_records.append(LearningRecord(
                    timestamp=datetime.now(),
                    learning_type='parameter_tuning',
                    description=f"Updated {param_name} from {old_value} to {param_value}",
                    impact=self._calculate_experiment_impact(experiment),
                    context={
                        'experiment_id': experiment_id,
                        'metrics_improvement': {
                            k: (experiment.metrics_after[k] - experiment.metrics_before[k]) / experiment.metrics_before[k]
                            for k in experiment.metrics_before
                        }
                    }
                ))
        
        experiment.status = ExperimentStatus.ADOPTED
        experiment.adopted = True
        
        logger.info(f"Adopted improvements from experiment {experiment_id}")
        
        # Save updated parameters
        self._save_parameters()
    
    def _calculate_experiment_impact(self, experiment: Experiment) -> float:
        """Calculate overall impact of an experiment"""
        if not experiment.metrics_after:
            return 0.0
        
        impacts = []
        for metric_name in experiment.metrics_before:
            before = experiment.metrics_before[metric_name]
            after = experiment.metrics_after[metric_name]
            importance = self._calculate_metric_importance(metric_name)
            
            if metric_name in ['error_rate', 'avg_processing_time', 'queue_depth']:
                # Lower is better
                impact = (before - after) / before if before > 0 else 0
            else:
                # Higher is better
                impact = (after - before) / before if before > 0 else 0
            
            impacts.append(impact * importance)
        
        return statistics.mean(impacts) if impacts else 0.0
    
    def get_recommendations(self) -> List[Dict[str, Any]]:
        """Get current recommendations based on analysis"""
        recommendations = []
        
        # Get current metrics
        current_metrics = self._get_current_metrics()
        
        # Analyze performance
        opportunities = self.analyze_performance(current_metrics)
        
        # Convert top opportunities to recommendations
        for opp in opportunities[:5]:  # Top 5 opportunities
            recommendations.append({
                'id': opp.id,
                'type': opp.type.value,
                'description': opp.description,
                'expected_benefit': f"{opp.expected_benefit * 100:.1f}%",
                'confidence': f"{opp.confidence * 100:.0f}%",
                'effort': opp.effort,
                'risk': opp.risk,
                'action': 'Create experiment to test this improvement'
            })
        
        # Add learning-based recommendations
        if len(self.learning_records) > 10:
            # Analyze successful patterns
            successful_learnings = [
                lr for lr in self.learning_records
                if lr.impact > 0.1
            ]
            
            if successful_learnings:
                pattern_types = defaultdict(list)
                for lr in successful_learnings:
                    pattern_types[lr.learning_type].append(lr.impact)
                
                best_pattern = max(pattern_types.items(), 
                                 key=lambda x: statistics.mean(x[1]))
                
                recommendations.append({
                    'id': 'learning_based_001',
                    'type': 'pattern_reuse',
                    'description': f"Focus on {best_pattern[0]} improvements - historically successful",
                    'expected_benefit': f"{statistics.mean(best_pattern[1]) * 100:.1f}%",
                    'confidence': "85%",
                    'effort': 'low',
                    'risk': 'low',
                    'action': 'Apply similar improvements to other components'
                })
        
        return recommendations
    
    def generate_improvement_report(self) -> Dict[str, Any]:
        """Generate comprehensive improvement report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'current_parameters': self.tunable_parameters,
            'performance_summary': {},
            'active_experiments': [],
            'completed_experiments': [],
            'adopted_improvements': [],
            'learning_summary': {},
            'recommendations': self.get_recommendations()
        }
        
        # Performance summary
        current_metrics = self._get_current_metrics()
        for metric_name, value in current_metrics.items():
            target = self.performance_targets.get(metric_name, value)
            achievement = (value / target) * 100 if target > 0 else 100
            
            if metric_name in ['error_rate', 'avg_processing_time', 'queue_depth']:
                # Lower is better - invert achievement
                achievement = (target / value) * 100 if value > 0 else 100
            
            report['performance_summary'][metric_name] = {
                'current': value,
                'target': target,
                'achievement': f"{achievement:.1f}%",
                'trend': self.performance_history[metric_name][-1].trend if metric_name in self.performance_history and self.performance_history[metric_name] else 'unknown'
            }
        
        # Experiments summary
        for exp_id, experiment in self.experiments.items():
            exp_summary = {
                'id': exp_id,
                'status': experiment.status.value,
                'start_time': experiment.start_time.isoformat(),
                'end_time': experiment.end_time.isoformat() if experiment.end_time else None
            }
            
            if experiment.status == ExperimentStatus.RUNNING:
                report['active_experiments'].append(exp_summary)
            elif experiment.status == ExperimentStatus.COMPLETED:
                evaluation = self.evaluate_experiment(exp_id)
                exp_summary['overall_improvement'] = f"{evaluation['overall_improvement'] * 100:.1f}%"
                exp_summary['recommendation'] = evaluation['recommendation']
                report['completed_experiments'].append(exp_summary)
            elif experiment.adopted:
                report['adopted_improvements'].append(exp_summary)
        
        # Learning summary
        if self.learning_records:
            by_type = defaultdict(list)
            for lr in self.learning_records:
                by_type[lr.learning_type].append(lr.impact)
            
            report['learning_summary'] = {
                learning_type: {
                    'count': len(impacts),
                    'average_impact': f"{statistics.mean(impacts) * 100:.1f}%",
                    'total_impact': f"{sum(impacts) * 100:.1f}%"
                }
                for learning_type, impacts in by_type.items()
            }
        
        return report
    
    def _save_parameters(self):
        """Save current parameters to disk"""
        params_file = self.improvements_path / "tunable_parameters.json"
        with open(params_file, 'w') as f:
            json.dump(self.tunable_parameters, f, indent=2)
    
    def save_state(self):
        """Save engine state to disk"""
        try:
            # Save performance history
            history_data = {}
            for metric_name, metrics in self.performance_history.items():
                history_data[metric_name] = [
                    {
                        'name': m.name,
                        'current_value': m.current_value,
                        'target_value': m.target_value,
                        'historical_values': m.historical_values,
                        'trend': m.trend,
                        'importance': m.importance
                    }
                    for m in metrics[-100:]  # Keep last 100
                ]
            
            with open(self.improvements_path / "performance_history.json", 'w') as f:
                json.dump(history_data, f, indent=2)
            
            # Save learning records
            learning_data = [
                {
                    'timestamp': lr.timestamp.isoformat(),
                    'learning_type': lr.learning_type,
                    'description': lr.description,
                    'impact': lr.impact,
                    'context': lr.context
                }
                for lr in self.learning_records[-500:]  # Keep last 500
            ]
            
            with open(self.improvements_path / "learning_records.json", 'w') as f:
                json.dump(learning_data, f, indent=2)
            
            # Save ML models
            if self.performance_predictor:
                with open(self.improvements_path / "performance_predictor.pkl", 'wb') as f:
                    pickle.dump(self.performance_predictor, f)
            
            if self.pattern_classifier:
                with open(self.improvements_path / "pattern_classifier.pkl", 'wb') as f:
                    pickle.dump(self.pattern_classifier, f)
            
            logger.info("Improvement engine state saved")
            
        except Exception as e:
            logger.error(f"Error saving state: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Initialize engine
    engine = ContinuousImprovementEngine(
        "/app/workspace/requirements/shared-infrastructure/knowledge-base",
        "/app/workspace/requirements/shared-infrastructure/monitoring"
    )
    
    # Simulate current metrics
    current_metrics = {
        'avg_processing_time': 250,  # Above target of 180
        'success_rate': 0.92,  # Below target of 0.95
        'throughput_per_hour': 45,  # Below target of 50
        'resource_utilization': 0.65,
        'error_rate': 0.08,  # Above target of 0.05
        'queue_depth': 25  # Above target of 20
    }
    
    print("=== Continuous Improvement Engine ===")
    print("\nAnalyzing current performance...")
    
    # Analyze performance
    opportunities = engine.analyze_performance(current_metrics)
    
    print(f"\nIdentified {len(opportunities)} improvement opportunities:")
    for opp in opportunities[:3]:
        print(f"\n- {opp.description}")
        print(f"  Type: {opp.type.value}")
        print(f"  Expected benefit: {opp.expected_benefit * 100:.1f}%")
        print(f"  Confidence: {opp.confidence * 100:.0f}%")
        print(f"  Effort: {opp.effort}, Risk: {opp.risk}")
    
    # Create and run experiment
    if opportunities:
        print("\n\nCreating experiment for top opportunity...")
        experiment = engine.create_experiment(opportunities[0])
        print(f"Created experiment: {experiment.id}")
        
        # Simulate running the experiment
        engine.run_experiment(experiment.id, duration_hours=1)
        
        # Evaluate results
        print("\nEvaluating experiment results...")
        evaluation = engine.evaluate_experiment(experiment.id)
        
        print(f"\nExperiment Results:")
        print(f"  Overall improvement: {evaluation['overall_improvement'] * 100:.1f}%")
        print(f"  Statistical significance: {evaluation['statistical_significance']:.2f}")
        print(f"  Recommendation: {evaluation['recommendation']}")
        
        if evaluation['recommendation'] == 'adopt':
            print("\nAdopting improvement...")
            engine.adopt_improvement(experiment.id)
            print("Improvement adopted successfully!")
    
    # Generate report
    print("\n\nGenerating improvement report...")
    report = engine.generate_improvement_report()
    
    print("\nPerformance Summary:")
    for metric, data in report['performance_summary'].items():
        print(f"  {metric}: {data['current']} (target: {data['target']}) - {data['achievement']} - Trend: {data['trend']}")
    
    print(f"\nActive experiments: {len(report['active_experiments'])}")
    print(f"Completed experiments: {len(report['completed_experiments'])}")
    print(f"Adopted improvements: {len(report['adopted_improvements'])}")
    
    print("\nTop Recommendations:")
    for rec in report['recommendations'][:3]:
        print(f"  - {rec['description']}")
        print(f"    Expected benefit: {rec['expected_benefit']}, Confidence: {rec['confidence']}")
    
    # Save state
    engine.save_state()
    print("\nEngine state saved.")