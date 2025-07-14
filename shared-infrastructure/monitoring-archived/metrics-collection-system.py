#!/usr/bin/env python3
"""
Metrics Collection System for Requirements Generation

This system collects, aggregates, and stores metrics from all components
of the requirements generation system for analysis and optimization.

Features:
- Distributed metrics collection
- Time-series data storage
- Metric aggregation and rollups
- Alerting and threshold monitoring
- Export capabilities for analysis
"""

import json
import logging
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, deque
import threading
import time
import sqlite3
from enum import Enum
import gzip
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of metrics collected"""
    COUNTER = "counter"  # Monotonically increasing value
    GAUGE = "gauge"  # Point-in-time value
    HISTOGRAM = "histogram"  # Distribution of values
    SUMMARY = "summary"  # Statistical summary
    RATE = "rate"  # Rate of change


class AggregationMethod(Enum):
    """Methods for aggregating metrics"""
    SUM = "sum"
    AVG = "avg"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    P50 = "p50"
    P95 = "p95"
    P99 = "p99"


@dataclass
class MetricDefinition:
    """Definition of a metric to be collected"""
    name: str
    type: MetricType
    description: str
    unit: str
    tags: List[str] = field(default_factory=list)
    aggregations: List[AggregationMethod] = field(default_factory=list)
    retention_days: int = 30
    alert_thresholds: Dict[str, float] = field(default_factory=dict)


@dataclass
class MetricPoint:
    """Single metric data point"""
    metric_name: str
    value: float
    timestamp: datetime
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricAlert:
    """Alert triggered by metric threshold"""
    metric_name: str
    threshold_name: str
    threshold_value: float
    actual_value: float
    timestamp: datetime
    severity: str  # 'warning', 'critical'
    message: str


@dataclass
class MetricSummary:
    """Summary statistics for a metric"""
    metric_name: str
    time_range: Tuple[datetime, datetime]
    count: int
    sum: float
    min: float
    max: float
    avg: float
    p50: float
    p95: float
    p99: float
    tags: Dict[str, str] = field(default_factory=dict)


class MetricsCollectionSystem:
    """
    Central system for collecting and managing metrics
    """
    
    def __init__(self, storage_path: str):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Metric definitions
        self.metric_definitions: Dict[str, MetricDefinition] = {}
        self._initialize_standard_metrics()
        
        # In-memory buffer for recent metrics
        self.metrics_buffer: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))
        self.buffer_lock = threading.Lock()
        
        # Alert tracking
        self.active_alerts: List[MetricAlert] = []
        self.alert_callbacks: List[Callable[[MetricAlert], None]] = []
        
        # SQLite for time-series storage
        self.db_path = self.storage_path / "metrics.db"
        self._initialize_database()
        
        # Background threads
        self.running = True
        self.aggregation_thread = threading.Thread(target=self._aggregation_loop)
        self.aggregation_thread.daemon = True
        self.aggregation_thread.start()
        
        self.persistence_thread = threading.Thread(target=self._persistence_loop)
        self.persistence_thread.daemon = True
        self.persistence_thread.start()
    
    def _initialize_standard_metrics(self):
        """Initialize standard metric definitions"""
        standard_metrics = [
            MetricDefinition(
                name="requirement.processing_time",
                type=MetricType.HISTOGRAM,
                description="Time to process a requirement",
                unit="seconds",
                tags=["agent_id", "domain", "requirement_type"],
                aggregations=[AggregationMethod.AVG, AggregationMethod.P95, AggregationMethod.P99],
                alert_thresholds={"warning": 300, "critical": 600}
            ),
            MetricDefinition(
                name="requirement.count",
                type=MetricType.COUNTER,
                description="Number of requirements processed",
                unit="requirements",
                tags=["agent_id", "domain", "status"],
                aggregations=[AggregationMethod.SUM, AggregationMethod.RATE]
            ),
            MetricDefinition(
                name="agent.utilization",
                type=MetricType.GAUGE,
                description="Agent utilization percentage",
                unit="percentage",
                tags=["agent_id", "domain"],
                aggregations=[AggregationMethod.AVG, AggregationMethod.MAX],
                alert_thresholds={"warning": 80, "critical": 95}
            ),
            MetricDefinition(
                name="queue.depth",
                type=MetricType.GAUGE,
                description="Number of requirements in queue",
                unit="requirements",
                tags=["queue_type"],
                aggregations=[AggregationMethod.AVG, AggregationMethod.MAX],
                alert_thresholds={"warning": 50, "critical": 100}
            ),
            MetricDefinition(
                name="engine.inference_time",
                type=MetricType.HISTOGRAM,
                description="Time for intelligence engine inference",
                unit="milliseconds",
                tags=["engine_type", "operation"],
                aggregations=[AggregationMethod.AVG, AggregationMethod.P95]
            ),
            MetricDefinition(
                name="gr.compliance_score",
                type=MetricType.GAUGE,
                description="Global requirement compliance score",
                unit="score",
                tags=["gr_id", "domain"],
                aggregations=[AggregationMethod.AVG, AggregationMethod.MIN],
                alert_thresholds={"warning": 0.8, "critical": 0.6}
            ),
            MetricDefinition(
                name="system.memory_usage",
                type=MetricType.GAUGE,
                description="System memory usage",
                unit="megabytes",
                tags=["component"],
                aggregations=[AggregationMethod.AVG, AggregationMethod.MAX],
                alert_thresholds={"warning": 1024, "critical": 1536}
            ),
            MetricDefinition(
                name="database.query_time",
                type=MetricType.HISTOGRAM,
                description="Database query execution time",
                unit="milliseconds",
                tags=["query_type", "table"],
                aggregations=[AggregationMethod.AVG, AggregationMethod.P95],
                alert_thresholds={"warning": 100, "critical": 500}
            ),
            MetricDefinition(
                name="error.count",
                type=MetricType.COUNTER,
                description="Number of errors encountered",
                unit="errors",
                tags=["error_type", "component", "severity"],
                aggregations=[AggregationMethod.SUM, AggregationMethod.RATE],
                alert_thresholds={"warning": 10, "critical": 50}
            ),
            MetricDefinition(
                name="batch.optimization_savings",
                type=MetricType.GAUGE,
                description="Time saved through batch optimization",
                unit="seconds",
                tags=["optimization_type"],
                aggregations=[AggregationMethod.SUM, AggregationMethod.AVG]
            )
        ]
        
        for metric in standard_metrics:
            self.register_metric(metric)
    
    def _initialize_database(self):
        """Initialize SQLite database for metrics storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                value REAL NOT NULL,
                timestamp INTEGER NOT NULL,
                tags TEXT,
                INDEX idx_metric_timestamp (metric_name, timestamp)
            )
        """)
        
        # Create aggregations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aggregations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                aggregation_type TEXT NOT NULL,
                period TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                value REAL NOT NULL,
                count INTEGER,
                tags TEXT,
                INDEX idx_aggregation (metric_name, aggregation_type, period, timestamp)
            )
        """)
        
        # Create alerts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                threshold_name TEXT NOT NULL,
                threshold_value REAL NOT NULL,
                actual_value REAL NOT NULL,
                timestamp INTEGER NOT NULL,
                severity TEXT NOT NULL,
                message TEXT,
                acknowledged INTEGER DEFAULT 0,
                INDEX idx_alerts_timestamp (timestamp)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def register_metric(self, definition: MetricDefinition):
        """Register a new metric definition"""
        self.metric_definitions[definition.name] = definition
        logger.info(f"Registered metric: {definition.name}")
    
    def record(self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Record a metric value"""
        if metric_name not in self.metric_definitions:
            logger.warning(f"Unknown metric: {metric_name}")
            return
        
        point = MetricPoint(
            metric_name=metric_name,
            value=value,
            timestamp=datetime.now(),
            tags=tags or {}
        )
        
        with self.buffer_lock:
            key = self._get_metric_key(metric_name, tags)
            self.metrics_buffer[key].append(point)
        
        # Check thresholds
        self._check_thresholds(point)
    
    def _get_metric_key(self, metric_name: str, tags: Optional[Dict[str, str]]) -> str:
        """Generate a unique key for metric + tags combination"""
        if not tags:
            return metric_name
        
        tag_str = ",".join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{metric_name}:{tag_str}"
    
    def _check_thresholds(self, point: MetricPoint):
        """Check if metric exceeds defined thresholds"""
        definition = self.metric_definitions.get(point.metric_name)
        if not definition or not definition.alert_thresholds:
            return
        
        for threshold_name, threshold_value in definition.alert_thresholds.items():
            # For different metric types, check thresholds differently
            should_alert = False
            
            if definition.type == MetricType.GAUGE:
                should_alert = point.value > threshold_value
            elif definition.type == MetricType.RATE:
                # Calculate rate from recent points
                key = self._get_metric_key(point.metric_name, point.tags)
                recent_points = list(self.metrics_buffer[key])[-10:]
                if len(recent_points) >= 2:
                    time_diff = (recent_points[-1].timestamp - recent_points[0].timestamp).total_seconds()
                    if time_diff > 0:
                        rate = (recent_points[-1].value - recent_points[0].value) / time_diff
                        should_alert = rate > threshold_value
            
            if should_alert:
                severity = "critical" if "critical" in threshold_name else "warning"
                alert = MetricAlert(
                    metric_name=point.metric_name,
                    threshold_name=threshold_name,
                    threshold_value=threshold_value,
                    actual_value=point.value,
                    timestamp=point.timestamp,
                    severity=severity,
                    message=f"{point.metric_name} exceeded {threshold_name} threshold: {point.value} > {threshold_value}"
                )
                
                self._trigger_alert(alert)
    
    def _trigger_alert(self, alert: MetricAlert):
        """Trigger an alert"""
        self.active_alerts.append(alert)
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alerts (metric_name, threshold_name, threshold_value, 
                              actual_value, timestamp, severity, message)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (alert.metric_name, alert.threshold_name, alert.threshold_value,
              alert.actual_value, int(alert.timestamp.timestamp()),
              alert.severity, alert.message))
        conn.commit()
        conn.close()
        
        # Call alert callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"Error in alert callback: {e}")
        
        logger.warning(f"Alert triggered: {alert.message}")
    
    def register_alert_callback(self, callback: Callable[[MetricAlert], None]):
        """Register a callback for alerts"""
        self.alert_callbacks.append(callback)
    
    def _aggregation_loop(self):
        """Background thread for metric aggregation"""
        while self.running:
            try:
                # Run aggregations every minute
                time.sleep(60)
                self._run_aggregations()
            except Exception as e:
                logger.error(f"Error in aggregation loop: {e}")
    
    def _run_aggregations(self):
        """Run metric aggregations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now()
        
        with self.buffer_lock:
            for key, points in self.metrics_buffer.items():
                if not points:
                    continue
                
                metric_name = key.split(':')[0]
                definition = self.metric_definitions.get(metric_name)
                if not definition:
                    continue
                
                # Get points from last minute
                minute_ago = now - timedelta(minutes=1)
                recent_points = [p for p in points if p.timestamp > minute_ago]
                
                if not recent_points:
                    continue
                
                values = [p.value for p in recent_points]
                
                # Calculate aggregations
                aggregations = {
                    AggregationMethod.SUM: sum(values),
                    AggregationMethod.AVG: statistics.mean(values),
                    AggregationMethod.MIN: min(values),
                    AggregationMethod.MAX: max(values),
                    AggregationMethod.COUNT: len(values)
                }
                
                # Calculate percentiles if needed
                if len(values) >= 2:
                    sorted_values = sorted(values)
                    aggregations[AggregationMethod.P50] = sorted_values[len(values) // 2]
                    aggregations[AggregationMethod.P95] = sorted_values[int(len(values) * 0.95)]
                    aggregations[AggregationMethod.P99] = sorted_values[int(len(values) * 0.99)]
                
                # Store aggregations
                for agg_method in definition.aggregations:
                    if agg_method in aggregations:
                        cursor.execute("""
                            INSERT INTO aggregations 
                            (metric_name, aggregation_type, period, timestamp, value, count, tags)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            metric_name,
                            agg_method.value,
                            "1m",
                            int(now.timestamp()),
                            aggregations[agg_method],
                            len(values),
                            json.dumps(recent_points[0].tags) if recent_points[0].tags else None
                        ))
        
        conn.commit()
        conn.close()
    
    def _persistence_loop(self):
        """Background thread for persisting metrics to database"""
        while self.running:
            try:
                # Persist every 10 seconds
                time.sleep(10)
                self._persist_metrics()
            except Exception as e:
                logger.error(f"Error in persistence loop: {e}")
    
    def _persist_metrics(self):
        """Persist buffered metrics to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        persisted_count = 0
        
        with self.buffer_lock:
            for key, points in self.metrics_buffer.items():
                # Persist points older than 30 seconds
                cutoff = datetime.now() - timedelta(seconds=30)
                to_persist = []
                
                while points and points[0].timestamp < cutoff:
                    to_persist.append(points.popleft())
                
                # Batch insert
                if to_persist:
                    cursor.executemany("""
                        INSERT INTO metrics (metric_name, value, timestamp, tags)
                        VALUES (?, ?, ?, ?)
                    """, [
                        (p.metric_name, p.value, int(p.timestamp.timestamp()),
                         json.dumps(p.tags) if p.tags else None)
                        for p in to_persist
                    ])
                    persisted_count += len(to_persist)
        
        conn.commit()
        conn.close()
        
        if persisted_count > 0:
            logger.debug(f"Persisted {persisted_count} metric points")
    
    def query_metrics(self, metric_name: str, start_time: datetime, end_time: datetime,
                     tags: Optional[Dict[str, str]] = None) -> List[MetricPoint]:
        """Query metrics from storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # First check buffer for recent data
        results = []
        
        with self.buffer_lock:
            key = self._get_metric_key(metric_name, tags)
            if key in self.metrics_buffer:
                results.extend([
                    p for p in self.metrics_buffer[key]
                    if start_time <= p.timestamp <= end_time
                ])
        
        # Then query database
        query = """
            SELECT value, timestamp, tags
            FROM metrics
            WHERE metric_name = ?
            AND timestamp >= ?
            AND timestamp <= ?
        """
        
        params = [metric_name, int(start_time.timestamp()), int(end_time.timestamp())]
        
        if tags:
            # Filter by tags in application layer (could be optimized with JSON queries)
            cursor.execute(query, params)
            for row in cursor.fetchall():
                value, timestamp, tags_json = row
                point_tags = json.loads(tags_json) if tags_json else {}
                
                # Check if all required tags match
                if all(point_tags.get(k) == v for k, v in tags.items()):
                    results.append(MetricPoint(
                        metric_name=metric_name,
                        value=value,
                        timestamp=datetime.fromtimestamp(timestamp),
                        tags=point_tags
                    ))
        else:
            cursor.execute(query, params)
            for row in cursor.fetchall():
                value, timestamp, tags_json = row
                results.append(MetricPoint(
                    metric_name=metric_name,
                    value=value,
                    timestamp=datetime.fromtimestamp(timestamp),
                    tags=json.loads(tags_json) if tags_json else {}
                ))
        
        conn.close()
        
        # Sort by timestamp
        results.sort(key=lambda p: p.timestamp)
        
        return results
    
    def get_metric_summary(self, metric_name: str, start_time: datetime, 
                          end_time: datetime, tags: Optional[Dict[str, str]] = None) -> MetricSummary:
        """Get summary statistics for a metric"""
        points = self.query_metrics(metric_name, start_time, end_time, tags)
        
        if not points:
            return MetricSummary(
                metric_name=metric_name,
                time_range=(start_time, end_time),
                count=0,
                sum=0,
                min=0,
                max=0,
                avg=0,
                p50=0,
                p95=0,
                p99=0,
                tags=tags or {}
            )
        
        values = [p.value for p in points]
        sorted_values = sorted(values)
        
        return MetricSummary(
            metric_name=metric_name,
            time_range=(start_time, end_time),
            count=len(values),
            sum=sum(values),
            min=min(values),
            max=max(values),
            avg=statistics.mean(values),
            p50=sorted_values[len(values) // 2],
            p95=sorted_values[int(len(values) * 0.95)],
            p99=sorted_values[int(len(values) * 0.99)],
            tags=tags or {}
        )
    
    def export_metrics(self, start_time: datetime, end_time: datetime,
                      output_file: Optional[str] = None) -> Dict:
        """Export metrics for analysis"""
        export_data = {
            'export_time': datetime.now().isoformat(),
            'time_range': {
                'start': start_time.isoformat(),
                'end': end_time.isoformat()
            },
            'metrics': {},
            'summaries': {},
            'alerts': []
        }
        
        # Export each metric
        for metric_name, definition in self.metric_definitions.items():
            points = self.query_metrics(metric_name, start_time, end_time)
            
            if points:
                export_data['metrics'][metric_name] = {
                    'definition': {
                        'type': definition.type.value,
                        'description': definition.description,
                        'unit': definition.unit
                    },
                    'data_points': [
                        {
                            'value': p.value,
                            'timestamp': p.timestamp.isoformat(),
                            'tags': p.tags
                        }
                        for p in points
                    ]
                }
                
                # Add summary
                summary = self.get_metric_summary(metric_name, start_time, end_time)
                export_data['summaries'][metric_name] = {
                    'count': summary.count,
                    'sum': summary.sum,
                    'min': summary.min,
                    'max': summary.max,
                    'avg': summary.avg,
                    'p50': summary.p50,
                    'p95': summary.p95,
                    'p99': summary.p99
                }
        
        # Export alerts
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT metric_name, threshold_name, threshold_value, actual_value,
                   timestamp, severity, message
            FROM alerts
            WHERE timestamp >= ? AND timestamp <= ?
            ORDER BY timestamp DESC
        """, (int(start_time.timestamp()), int(end_time.timestamp())))
        
        for row in cursor.fetchall():
            export_data['alerts'].append({
                'metric_name': row[0],
                'threshold_name': row[1],
                'threshold_value': row[2],
                'actual_value': row[3],
                'timestamp': datetime.fromtimestamp(row[4]).isoformat(),
                'severity': row[5],
                'message': row[6]
            })
        
        conn.close()
        
        # Save to file if specified
        if output_file:
            # Compress if large
            if len(json.dumps(export_data)) > 1024 * 1024:  # 1MB
                with gzip.open(output_file + '.gz', 'wt') as f:
                    json.dump(export_data, f, indent=2)
            else:
                with open(output_file, 'w') as f:
                    json.dump(export_data, f, indent=2)
        
        return export_data
    
    def cleanup_old_data(self, retention_days: Optional[int] = None):
        """Clean up old metrics data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for metric_name, definition in self.metric_definitions.items():
            days = retention_days or definition.retention_days
            cutoff = datetime.now() - timedelta(days=days)
            cutoff_ts = int(cutoff.timestamp())
            
            # Delete old metrics
            cursor.execute("""
                DELETE FROM metrics
                WHERE metric_name = ? AND timestamp < ?
            """, (metric_name, cutoff_ts))
            
            # Delete old aggregations
            cursor.execute("""
                DELETE FROM aggregations
                WHERE metric_name = ? AND timestamp < ?
            """, (metric_name, cutoff_ts))
        
        # Delete old alerts (keep for 90 days)
        alert_cutoff = datetime.now() - timedelta(days=90)
        cursor.execute("""
            DELETE FROM alerts
            WHERE timestamp < ?
        """, (int(alert_cutoff.timestamp()),))
        
        conn.commit()
        conn.close()
        
        logger.info("Cleaned up old metrics data")
    
    def get_active_alerts(self) -> List[MetricAlert]:
        """Get currently active alerts"""
        # Remove old alerts from memory
        cutoff = datetime.now() - timedelta(hours=1)
        self.active_alerts = [a for a in self.active_alerts if a.timestamp > cutoff]
        
        return self.active_alerts
    
    def shutdown(self):
        """Shutdown the metrics collection system"""
        self.running = False
        
        # Persist remaining metrics
        self._persist_metrics()
        
        # Wait for threads
        self.aggregation_thread.join()
        self.persistence_thread.join()
        
        logger.info("Metrics collection system shutdown complete")


# Helper class for easy metric recording
class MetricsRecorder:
    """Simplified interface for recording metrics"""
    
    def __init__(self, metrics_system: MetricsCollectionSystem):
        self.metrics_system = metrics_system
    
    def record_requirement_processing(self, agent_id: str, domain: str,
                                    requirement_type: str, processing_time: float,
                                    success: bool):
        """Record requirement processing metrics"""
        # Record processing time
        self.metrics_system.record(
            "requirement.processing_time",
            processing_time,
            {
                "agent_id": agent_id,
                "domain": domain,
                "requirement_type": requirement_type
            }
        )
        
        # Record count
        self.metrics_system.record(
            "requirement.count",
            1,
            {
                "agent_id": agent_id,
                "domain": domain,
                "status": "success" if success else "failure"
            }
        )
        
        # Record error if failed
        if not success:
            self.metrics_system.record(
                "error.count",
                1,
                {
                    "error_type": "requirement_processing",
                    "component": agent_id,
                    "severity": "high"
                }
            )
    
    def record_agent_utilization(self, agent_id: str, domain: str, utilization: float):
        """Record agent utilization"""
        self.metrics_system.record(
            "agent.utilization",
            utilization,
            {
                "agent_id": agent_id,
                "domain": domain
            }
        )
    
    def record_queue_depth(self, queue_type: str, depth: int):
        """Record queue depth"""
        self.metrics_system.record(
            "queue.depth",
            depth,
            {"queue_type": queue_type}
        )
    
    def record_engine_inference(self, engine_type: str, operation: str,
                              inference_time: float):
        """Record intelligence engine inference time"""
        self.metrics_system.record(
            "engine.inference_time",
            inference_time,
            {
                "engine_type": engine_type,
                "operation": operation
            }
        )
    
    def record_gr_compliance(self, gr_id: str, domain: str, score: float):
        """Record GR compliance score"""
        self.metrics_system.record(
            "gr.compliance_score",
            score,
            {
                "gr_id": gr_id,
                "domain": domain
            }
        )


# Example usage and testing
if __name__ == "__main__":
    # Initialize metrics system
    metrics_system = MetricsCollectionSystem("/app/workspace/requirements/shared-infrastructure/monitoring/metrics-data")
    recorder = MetricsRecorder(metrics_system)
    
    # Example alert callback
    def alert_handler(alert: MetricAlert):
        print(f"ALERT: {alert.severity.upper()} - {alert.message}")
    
    metrics_system.register_alert_callback(alert_handler)
    
    # Simulate some metrics
    import random
    
    print("Recording sample metrics...")
    
    # Record requirement processing
    for i in range(10):
        processing_time = random.uniform(50, 400)
        success = random.random() > 0.1
        
        recorder.record_requirement_processing(
            agent_id=f"agent_{random.choice(['pp', 'acc', 'ei'])}",
            domain=random.choice(["producer-portal", "accounting", "entity-integration"]),
            requirement_type=random.choice(["create", "update", "validate"]),
            processing_time=processing_time,
            success=success
        )
    
    # Record agent utilization
    for agent in ["agent_pp", "agent_acc", "agent_ei"]:
        recorder.record_agent_utilization(
            agent_id=agent,
            domain="test",
            utilization=random.uniform(30, 95)
        )
    
    # Record queue depth (trigger alert)
    recorder.record_queue_depth("main", 75)  # Should trigger warning
    
    # Wait for persistence
    time.sleep(2)
    
    # Query metrics
    print("\nQuerying recent metrics...")
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=5)
    
    points = metrics_system.query_metrics(
        "requirement.processing_time",
        start_time,
        end_time
    )
    print(f"Found {len(points)} processing time points")
    
    # Get summary
    summary = metrics_system.get_metric_summary(
        "requirement.processing_time",
        start_time,
        end_time
    )
    
    print(f"\nProcessing Time Summary:")
    print(f"  Count: {summary.count}")
    print(f"  Average: {summary.avg:.2f}s")
    print(f"  P95: {summary.p95:.2f}s")
    print(f"  Max: {summary.max:.2f}s")
    
    # Check alerts
    active_alerts = metrics_system.get_active_alerts()
    print(f"\nActive alerts: {len(active_alerts)}")
    
    # Export metrics
    export_data = metrics_system.export_metrics(
        start_time,
        end_time,
        "/app/workspace/requirements/shared-infrastructure/monitoring/metrics-export.json"
    )
    print(f"\nExported {len(export_data['metrics'])} metrics")
    
    # Cleanup
    metrics_system.shutdown()
    print("\nMetrics system shutdown complete")