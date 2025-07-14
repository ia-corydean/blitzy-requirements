#!/usr/bin/env python3
"""
Performance Dashboard for Requirements Generation System

This dashboard provides real-time visibility into system performance,
requirement processing metrics, and agent utilization.

Features:
- Real-time performance metrics
- Agent utilization tracking
- Requirement processing statistics
- System health monitoring
- Historical trend analysis
"""

import json
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, deque
import time
import threading
from enum import Enum
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of metrics tracked"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    RATE = "rate"


class HealthStatus(Enum):
    """System health status levels"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


@dataclass
class Metric:
    """Individual metric data point"""
    name: str
    value: float
    timestamp: datetime
    type: MetricType
    tags: Dict[str, str] = field(default_factory=dict)
    unit: str = ""


@dataclass
class AgentMetrics:
    """Metrics for a specific agent"""
    agent_id: str
    domain: str
    requirements_processed: int
    average_processing_time: float
    success_rate: float
    current_load: int
    status: str  # 'idle', 'processing', 'overloaded'
    last_active: datetime
    error_count: int


@dataclass
class SystemMetrics:
    """Overall system metrics"""
    total_requirements: int
    completed_requirements: int
    failed_requirements: int
    average_completion_time: float
    throughput_per_hour: float
    queue_depth: int
    active_agents: int
    system_health: HealthStatus
    resource_utilization: Dict[str, float]


@dataclass
class PerformanceTrend:
    """Performance trend analysis"""
    metric_name: str
    time_period: str  # '1h', '24h', '7d'
    trend_direction: str  # 'improving', 'stable', 'degrading'
    change_percentage: float
    data_points: List[Tuple[datetime, float]]
    forecast: Optional[float] = None


class PerformanceDashboard:
    """
    Real-time performance monitoring dashboard
    """
    
    def __init__(self, metrics_store_path: str):
        self.metrics_store_path = Path(metrics_store_path)
        self.metrics_store_path.mkdir(parents=True, exist_ok=True)
        
        # In-memory metrics storage
        self.metrics_buffer: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))
        self.agent_metrics: Dict[str, AgentMetrics] = {}
        self.system_metrics = SystemMetrics(
            total_requirements=0,
            completed_requirements=0,
            failed_requirements=0,
            average_completion_time=0.0,
            throughput_per_hour=0.0,
            queue_depth=0,
            active_agents=0,
            system_health=HealthStatus.HEALTHY,
            resource_utilization={}
        )
        
        # Performance thresholds
        self.thresholds = {
            'processing_time_warning': 300,  # 5 minutes
            'processing_time_critical': 600,  # 10 minutes
            'queue_depth_warning': 50,
            'queue_depth_critical': 100,
            'error_rate_warning': 0.05,  # 5%
            'error_rate_critical': 0.10,  # 10%
            'agent_load_warning': 5,
            'agent_load_critical': 10
        }
        
        # Start background metrics aggregation
        self.running = True
        self.aggregation_thread = threading.Thread(target=self._aggregate_metrics_loop)
        self.aggregation_thread.daemon = True
        self.aggregation_thread.start()
    
    def record_metric(self, metric: Metric):
        """Record a new metric"""
        key = f"{metric.name}:{','.join(f'{k}={v}' for k, v in sorted(metric.tags.items()))}"
        self.metrics_buffer[key].append(metric)
    
    def record_requirement_start(self, requirement_id: str, agent_id: str, domain: str):
        """Record start of requirement processing"""
        self.record_metric(Metric(
            name="requirement.started",
            value=1,
            timestamp=datetime.now(),
            type=MetricType.COUNTER,
            tags={
                'requirement_id': requirement_id,
                'agent_id': agent_id,
                'domain': domain
            }
        ))
        
        # Update agent metrics
        if agent_id not in self.agent_metrics:
            self.agent_metrics[agent_id] = AgentMetrics(
                agent_id=agent_id,
                domain=domain,
                requirements_processed=0,
                average_processing_time=0.0,
                success_rate=1.0,
                current_load=0,
                status='idle',
                last_active=datetime.now(),
                error_count=0
            )
        
        self.agent_metrics[agent_id].current_load += 1
        self.agent_metrics[agent_id].status = 'processing'
        self.agent_metrics[agent_id].last_active = datetime.now()
    
    def record_requirement_complete(self, requirement_id: str, agent_id: str, 
                                  processing_time: float, success: bool):
        """Record completion of requirement processing"""
        self.record_metric(Metric(
            name="requirement.completed",
            value=1,
            timestamp=datetime.now(),
            type=MetricType.COUNTER,
            tags={
                'requirement_id': requirement_id,
                'agent_id': agent_id,
                'success': str(success)
            }
        ))
        
        self.record_metric(Metric(
            name="requirement.processing_time",
            value=processing_time,
            timestamp=datetime.now(),
            type=MetricType.HISTOGRAM,
            tags={'agent_id': agent_id},
            unit="seconds"
        ))
        
        # Update agent metrics
        if agent_id in self.agent_metrics:
            agent = self.agent_metrics[agent_id]
            agent.requirements_processed += 1
            agent.current_load = max(0, agent.current_load - 1)
            
            # Update average processing time
            agent.average_processing_time = (
                (agent.average_processing_time * (agent.requirements_processed - 1) + processing_time) 
                / agent.requirements_processed
            )
            
            # Update success rate
            if not success:
                agent.error_count += 1
            agent.success_rate = 1 - (agent.error_count / agent.requirements_processed)
            
            # Update status
            if agent.current_load == 0:
                agent.status = 'idle'
            elif agent.current_load > self.thresholds['agent_load_critical']:
                agent.status = 'overloaded'
        
        # Update system metrics
        self.system_metrics.total_requirements += 1
        if success:
            self.system_metrics.completed_requirements += 1
        else:
            self.system_metrics.failed_requirements += 1
    
    def record_queue_depth(self, depth: int):
        """Record current queue depth"""
        self.record_metric(Metric(
            name="queue.depth",
            value=depth,
            timestamp=datetime.now(),
            type=MetricType.GAUGE,
            unit="requirements"
        ))
        self.system_metrics.queue_depth = depth
    
    def record_resource_utilization(self, resource: str, utilization: float):
        """Record resource utilization"""
        self.record_metric(Metric(
            name=f"resource.{resource}.utilization",
            value=utilization,
            timestamp=datetime.now(),
            type=MetricType.GAUGE,
            tags={'resource': resource},
            unit="percentage"
        ))
        self.system_metrics.resource_utilization[resource] = utilization
    
    def get_current_dashboard(self) -> Dict[str, Any]:
        """Get current dashboard data"""
        # Calculate system metrics
        self._update_system_metrics()
        
        # Get agent summary
        agent_summary = self._get_agent_summary()
        
        # Get recent trends
        trends = self._analyze_trends()
        
        # Get health status
        health_status = self._assess_system_health()
        
        # Get top issues
        top_issues = self._identify_top_issues()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'system_metrics': {
                'total_requirements': self.system_metrics.total_requirements,
                'completed_requirements': self.system_metrics.completed_requirements,
                'failed_requirements': self.system_metrics.failed_requirements,
                'success_rate': self._calculate_success_rate(),
                'average_completion_time': self.system_metrics.average_completion_time,
                'throughput_per_hour': self.system_metrics.throughput_per_hour,
                'queue_depth': self.system_metrics.queue_depth,
                'active_agents': self.system_metrics.active_agents
            },
            'agent_summary': agent_summary,
            'resource_utilization': self.system_metrics.resource_utilization,
            'health_status': {
                'overall': health_status.value,
                'components': self._get_component_health()
            },
            'trends': trends,
            'top_issues': top_issues,
            'recommendations': self._generate_recommendations()
        }
    
    def _update_system_metrics(self):
        """Update calculated system metrics"""
        # Calculate average completion time
        completion_times = []
        for key, metrics in self.metrics_buffer.items():
            if 'requirement.processing_time' in key:
                recent_metrics = [m for m in metrics if m.timestamp > datetime.now() - timedelta(hours=1)]
                completion_times.extend([m.value for m in recent_metrics])
        
        if completion_times:
            self.system_metrics.average_completion_time = statistics.mean(completion_times)
        
        # Calculate throughput
        hour_ago = datetime.now() - timedelta(hours=1)
        recent_completions = sum(
            1 for key, metrics in self.metrics_buffer.items()
            if 'requirement.completed' in key
            for m in metrics if m.timestamp > hour_ago
        )
        self.system_metrics.throughput_per_hour = recent_completions
        
        # Count active agents
        self.system_metrics.active_agents = sum(
            1 for agent in self.agent_metrics.values()
            if agent.status != 'idle'
        )
    
    def _calculate_success_rate(self) -> float:
        """Calculate overall success rate"""
        total = self.system_metrics.total_requirements
        if total == 0:
            return 1.0
        return self.system_metrics.completed_requirements / total
    
    def _get_agent_summary(self) -> List[Dict]:
        """Get summary of agent performance"""
        summary = []
        for agent_id, metrics in self.agent_metrics.items():
            summary.append({
                'agent_id': agent_id,
                'domain': metrics.domain,
                'status': metrics.status,
                'current_load': metrics.current_load,
                'requirements_processed': metrics.requirements_processed,
                'average_processing_time': round(metrics.average_processing_time, 2),
                'success_rate': round(metrics.success_rate, 3),
                'last_active': metrics.last_active.isoformat()
            })
        
        # Sort by current load (busiest first)
        return sorted(summary, key=lambda x: x['current_load'], reverse=True)
    
    def _analyze_trends(self) -> List[Dict]:
        """Analyze performance trends"""
        trends = []
        
        # Analyze processing time trend
        processing_times = []
        for key, metrics in self.metrics_buffer.items():
            if 'requirement.processing_time' in key:
                # Get last 24 hours
                day_ago = datetime.now() - timedelta(days=1)
                recent = [(m.timestamp, m.value) for m in metrics if m.timestamp > day_ago]
                processing_times.extend(recent)
        
        if len(processing_times) > 10:
            processing_times.sort(key=lambda x: x[0])
            
            # Compare first half vs second half
            mid = len(processing_times) // 2
            first_half_avg = statistics.mean([x[1] for x in processing_times[:mid]])
            second_half_avg = statistics.mean([x[1] for x in processing_times[mid:]])
            
            change_pct = ((second_half_avg - first_half_avg) / first_half_avg) * 100
            
            if abs(change_pct) < 5:
                direction = 'stable'
            elif change_pct < 0:
                direction = 'improving'
            else:
                direction = 'degrading'
            
            trends.append({
                'metric': 'processing_time',
                'period': '24h',
                'direction': direction,
                'change_percentage': round(change_pct, 1),
                'current_value': round(second_half_avg, 2)
            })
        
        # Analyze throughput trend
        hour_counts = defaultdict(int)
        for key, metrics in self.metrics_buffer.items():
            if 'requirement.completed' in key:
                for m in metrics:
                    hour = m.timestamp.replace(minute=0, second=0, microsecond=0)
                    hour_counts[hour] += 1
        
        if len(hour_counts) > 2:
            sorted_hours = sorted(hour_counts.items())
            recent_throughput = statistics.mean([x[1] for x in sorted_hours[-3:]])
            older_throughput = statistics.mean([x[1] for x in sorted_hours[:-3]])
            
            if older_throughput > 0:
                change_pct = ((recent_throughput - older_throughput) / older_throughput) * 100
                
                if abs(change_pct) < 5:
                    direction = 'stable'
                elif change_pct > 0:
                    direction = 'improving'
                else:
                    direction = 'degrading'
                
                trends.append({
                    'metric': 'throughput',
                    'period': 'recent_hours',
                    'direction': direction,
                    'change_percentage': round(change_pct, 1),
                    'current_value': round(recent_throughput, 1)
                })
        
        return trends
    
    def _assess_system_health(self) -> HealthStatus:
        """Assess overall system health"""
        issues = []
        
        # Check processing time
        if self.system_metrics.average_completion_time > self.thresholds['processing_time_critical']:
            issues.append('critical')
        elif self.system_metrics.average_completion_time > self.thresholds['processing_time_warning']:
            issues.append('warning')
        
        # Check queue depth
        if self.system_metrics.queue_depth > self.thresholds['queue_depth_critical']:
            issues.append('critical')
        elif self.system_metrics.queue_depth > self.thresholds['queue_depth_warning']:
            issues.append('warning')
        
        # Check error rate
        error_rate = 1 - self._calculate_success_rate()
        if error_rate > self.thresholds['error_rate_critical']:
            issues.append('critical')
        elif error_rate > self.thresholds['error_rate_warning']:
            issues.append('warning')
        
        # Check agent overload
        overloaded_agents = sum(
            1 for agent in self.agent_metrics.values()
            if agent.status == 'overloaded'
        )
        if overloaded_agents > len(self.agent_metrics) * 0.5:
            issues.append('critical')
        elif overloaded_agents > len(self.agent_metrics) * 0.25:
            issues.append('warning')
        
        # Determine overall health
        if 'critical' in issues:
            return HealthStatus.CRITICAL
        elif 'warning' in issues:
            return HealthStatus.WARNING
        else:
            return HealthStatus.HEALTHY
    
    def _get_component_health(self) -> Dict[str, str]:
        """Get health status of individual components"""
        components = {}
        
        # Agent health
        for agent_id, metrics in self.agent_metrics.items():
            if metrics.status == 'overloaded':
                components[f'agent_{agent_id}'] = 'critical'
            elif metrics.current_load > self.thresholds['agent_load_warning']:
                components[f'agent_{agent_id}'] = 'warning'
            else:
                components[f'agent_{agent_id}'] = 'healthy'
        
        # Queue health
        if self.system_metrics.queue_depth > self.thresholds['queue_depth_critical']:
            components['queue'] = 'critical'
        elif self.system_metrics.queue_depth > self.thresholds['queue_depth_warning']:
            components['queue'] = 'warning'
        else:
            components['queue'] = 'healthy'
        
        # Processing health
        if self.system_metrics.average_completion_time > self.thresholds['processing_time_critical']:
            components['processing'] = 'critical'
        elif self.system_metrics.average_completion_time > self.thresholds['processing_time_warning']:
            components['processing'] = 'warning'
        else:
            components['processing'] = 'healthy'
        
        return components
    
    def _identify_top_issues(self) -> List[Dict]:
        """Identify top performance issues"""
        issues = []
        
        # Slow processing
        if self.system_metrics.average_completion_time > self.thresholds['processing_time_warning']:
            issues.append({
                'type': 'slow_processing',
                'severity': 'high' if self.system_metrics.average_completion_time > self.thresholds['processing_time_critical'] else 'medium',
                'description': f'Average processing time ({self.system_metrics.average_completion_time:.1f}s) exceeds threshold',
                'impact': 'Reduced throughput and increased queue depth'
            })
        
        # High queue depth
        if self.system_metrics.queue_depth > self.thresholds['queue_depth_warning']:
            issues.append({
                'type': 'high_queue_depth',
                'severity': 'high' if self.system_metrics.queue_depth > self.thresholds['queue_depth_critical'] else 'medium',
                'description': f'Queue depth ({self.system_metrics.queue_depth}) exceeds threshold',
                'impact': 'Increased latency for new requirements'
            })
        
        # Agent overload
        overloaded = [a for a in self.agent_metrics.values() if a.status == 'overloaded']
        if overloaded:
            issues.append({
                'type': 'agent_overload',
                'severity': 'high',
                'description': f'{len(overloaded)} agents are overloaded',
                'impact': 'Reduced processing capacity',
                'affected_agents': [a.agent_id for a in overloaded]
            })
        
        # High error rate
        error_rate = 1 - self._calculate_success_rate()
        if error_rate > self.thresholds['error_rate_warning']:
            issues.append({
                'type': 'high_error_rate',
                'severity': 'high' if error_rate > self.thresholds['error_rate_critical'] else 'medium',
                'description': f'Error rate ({error_rate:.1%}) exceeds threshold',
                'impact': 'Reduced reliability and rework required'
            })
        
        # Sort by severity
        severity_order = {'high': 0, 'medium': 1, 'low': 2}
        return sorted(issues, key=lambda x: severity_order.get(x['severity'], 999))
    
    def _generate_recommendations(self) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        # Based on system health
        health = self._assess_system_health()
        
        if health == HealthStatus.CRITICAL:
            recommendations.append("URGENT: System is in critical state - immediate action required")
        
        # Processing time recommendations
        if self.system_metrics.average_completion_time > self.thresholds['processing_time_warning']:
            recommendations.append("Consider optimizing requirement processing logic or adding caching")
            recommendations.append("Review complex requirements for simplification opportunities")
        
        # Queue recommendations
        if self.system_metrics.queue_depth > self.thresholds['queue_depth_warning']:
            recommendations.append("Scale up processing capacity or optimize throughput")
            recommendations.append("Consider batch processing for similar requirements")
        
        # Agent recommendations
        overloaded_count = sum(1 for a in self.agent_metrics.values() if a.status == 'overloaded')
        if overloaded_count > 0:
            recommendations.append(f"Redistribute load from {overloaded_count} overloaded agents")
            recommendations.append("Consider adding more agents or optimizing agent allocation")
        
        # Error rate recommendations
        error_rate = 1 - self._calculate_success_rate()
        if error_rate > self.thresholds['error_rate_warning']:
            # Find agents with high error rates
            problem_agents = [
                a for a in self.agent_metrics.values()
                if a.success_rate < 0.9
            ]
            if problem_agents:
                recommendations.append(f"Review error patterns for {len(problem_agents)} agents with high error rates")
            recommendations.append("Implement better error handling and retry mechanisms")
        
        # Trend-based recommendations
        trends = self._analyze_trends()
        for trend in trends:
            if trend['direction'] == 'degrading' and trend['change_percentage'] > 10:
                recommendations.append(f"{trend['metric']} is degrading - investigate root cause")
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _aggregate_metrics_loop(self):
        """Background thread for metrics aggregation"""
        while self.running:
            try:
                # Aggregate metrics every minute
                time.sleep(60)
                self._persist_metrics()
                self._cleanup_old_metrics()
            except Exception as e:
                logger.error(f"Error in metrics aggregation: {e}")
    
    def _persist_metrics(self):
        """Persist metrics to disk"""
        try:
            # Get current dashboard state
            dashboard_data = self.get_current_dashboard()
            
            # Save to file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.metrics_store_path / f"dashboard_{timestamp}.json"
            
            with open(output_file, 'w') as f:
                json.dump(dashboard_data, f, indent=2)
            
            # Also save as latest
            latest_file = self.metrics_store_path / "dashboard_latest.json"
            with open(latest_file, 'w') as f:
                json.dump(dashboard_data, f, indent=2)
            
        except Exception as e:
            logger.error(f"Error persisting metrics: {e}")
    
    def _cleanup_old_metrics(self):
        """Clean up old metrics from memory and disk"""
        # Clean up in-memory metrics older than 24 hours
        cutoff = datetime.now() - timedelta(days=1)
        
        for key in list(self.metrics_buffer.keys()):
            metrics = self.metrics_buffer[key]
            # Remove old metrics
            while metrics and metrics[0].timestamp < cutoff:
                metrics.popleft()
            
            # Remove empty metric keys
            if not metrics:
                del self.metrics_buffer[key]
        
        # Clean up old dashboard files (keep last 7 days)
        try:
            for file in self.metrics_store_path.glob("dashboard_*.json"):
                if file.name == "dashboard_latest.json":
                    continue
                
                # Parse timestamp from filename
                timestamp_str = file.stem.replace("dashboard_", "")
                try:
                    file_time = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                    if file_time < datetime.now() - timedelta(days=7):
                        file.unlink()
                except:
                    pass
        except Exception as e:
            logger.error(f"Error cleaning up old files: {e}")
    
    def export_metrics_report(self, time_period: str = "24h") -> Dict:
        """Export comprehensive metrics report"""
        # Determine time range
        if time_period == "1h":
            start_time = datetime.now() - timedelta(hours=1)
        elif time_period == "24h":
            start_time = datetime.now() - timedelta(days=1)
        elif time_period == "7d":
            start_time = datetime.now() - timedelta(days=7)
        else:
            start_time = datetime.now() - timedelta(days=1)
        
        report = {
            'report_period': time_period,
            'start_time': start_time.isoformat(),
            'end_time': datetime.now().isoformat(),
            'summary': {},
            'agent_performance': [],
            'hourly_metrics': [],
            'issues_encountered': [],
            'recommendations': []
        }
        
        # Calculate summary metrics
        total_processed = 0
        total_failed = 0
        processing_times = []
        
        for key, metrics in self.metrics_buffer.items():
            if 'requirement.completed' in key:
                recent = [m for m in metrics if m.timestamp > start_time]
                for m in recent:
                    total_processed += 1
                    if 'success=False' in key:
                        total_failed += 1
            
            elif 'requirement.processing_time' in key:
                recent = [m for m in metrics if m.timestamp > start_time]
                processing_times.extend([m.value for m in recent])
        
        report['summary'] = {
            'total_requirements_processed': total_processed,
            'success_rate': (total_processed - total_failed) / max(total_processed, 1),
            'average_processing_time': statistics.mean(processing_times) if processing_times else 0,
            'min_processing_time': min(processing_times) if processing_times else 0,
            'max_processing_time': max(processing_times) if processing_times else 0,
            'p95_processing_time': sorted(processing_times)[int(len(processing_times) * 0.95)] if processing_times else 0
        }
        
        # Agent performance
        for agent_id, metrics in self.agent_metrics.items():
            report['agent_performance'].append({
                'agent_id': agent_id,
                'domain': metrics.domain,
                'requirements_processed': metrics.requirements_processed,
                'average_processing_time': metrics.average_processing_time,
                'success_rate': metrics.success_rate,
                'utilization': metrics.current_load / self.thresholds['agent_load_warning']
            })
        
        # Generate recommendations based on report data
        if report['summary']['success_rate'] < 0.95:
            report['recommendations'].append("Investigate high failure rate - review error logs")
        
        if report['summary']['p95_processing_time'] > self.thresholds['processing_time_warning']:
            report['recommendations'].append("P95 processing time is high - optimize slow requirements")
        
        return report
    
    def shutdown(self):
        """Shutdown the dashboard"""
        self.running = False
        self.aggregation_thread.join()
        self._persist_metrics()


# Example usage and testing
if __name__ == "__main__":
    # Initialize dashboard
    dashboard = PerformanceDashboard("/app/workspace/requirements/shared-infrastructure/monitoring/metrics")
    
    # Simulate some metrics
    import random
    
    agents = [
        ("agent_producer_portal", "producer-portal"),
        ("agent_accounting", "accounting"),
        ("agent_entity_int", "entity-integration")
    ]
    
    # Simulate requirement processing
    for i in range(20):
        agent_id, domain = random.choice(agents)
        req_id = f"REQ_{i:04d}"
        
        # Start processing
        dashboard.record_requirement_start(req_id, agent_id, domain)
        
        # Simulate processing time
        processing_time = random.uniform(10, 300)
        success = random.random() > 0.1  # 90% success rate
        
        # Complete processing
        dashboard.record_requirement_complete(req_id, agent_id, processing_time, success)
    
    # Record queue depth
    dashboard.record_queue_depth(random.randint(5, 50))
    
    # Record resource utilization
    dashboard.record_resource_utilization("cpu", random.uniform(0.3, 0.8))
    dashboard.record_resource_utilization("memory", random.uniform(0.4, 0.7))
    dashboard.record_resource_utilization("database_connections", random.uniform(0.2, 0.5))
    
    # Get current dashboard
    current_dashboard = dashboard.get_current_dashboard()
    
    print("=== Performance Dashboard ===")
    print(f"\nSystem Metrics:")
    for key, value in current_dashboard['system_metrics'].items():
        print(f"  {key}: {value}")
    
    print(f"\nHealth Status: {current_dashboard['health_status']['overall']}")
    
    print(f"\nTop Issues:")
    for issue in current_dashboard['top_issues']:
        print(f"  - [{issue['severity']}] {issue['description']}")
    
    print(f"\nRecommendations:")
    for rec in current_dashboard['recommendations']:
        print(f"  - {rec}")
    
    print(f"\nAgent Summary:")
    for agent in current_dashboard['agent_summary'][:3]:
        print(f"  - {agent['agent_id']}: {agent['status']} (load: {agent['current_load']})")
    
    # Export report
    report = dashboard.export_metrics_report("24h")
    print(f"\n24-Hour Report Summary:")
    print(f"  Total processed: {report['summary']['total_requirements_processed']}")
    print(f"  Success rate: {report['summary']['success_rate']:.1%}")
    print(f"  Avg processing time: {report['summary']['average_processing_time']:.1f}s")
    
    # Cleanup
    dashboard.shutdown()