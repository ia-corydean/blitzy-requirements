#!/usr/bin/env python3
"""
Real-Time Monitoring Interface for Requirements Generation System

This interface provides real-time visibility into system operations,
performance metrics, and alerts through a web-based dashboard.

Features:
- WebSocket-based real-time updates
- Interactive dashboard with charts
- Alert notifications
- System health visualization
- Agent activity monitoring
"""

import json
import logging
import asyncio
import websockets
from typing import Dict, List, Set, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path
import threading
from dataclasses import dataclass, asdict
from collections import deque, defaultdict
import time
from aiohttp import web
import aiohttp_cors

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SystemStatus:
    """Current system status"""
    timestamp: str
    health: str  # 'healthy', 'warning', 'critical'
    active_requirements: int
    queue_depth: int
    active_agents: int
    throughput_per_minute: float
    average_processing_time: float
    error_rate: float


@dataclass
class AgentStatus:
    """Status of an individual agent"""
    agent_id: str
    domain: str
    status: str  # 'idle', 'processing', 'error', 'offline'
    current_requirement: Optional[str]
    requirements_processed: int
    success_rate: float
    average_time: float
    last_update: str


@dataclass
class Alert:
    """System alert"""
    id: str
    timestamp: str
    severity: str  # 'info', 'warning', 'critical'
    component: str
    message: str
    details: Dict[str, Any]
    acknowledged: bool = False


@dataclass
class MetricUpdate:
    """Real-time metric update"""
    metric_name: str
    value: float
    timestamp: str
    tags: Dict[str, str]


class RealTimeMonitoringInterface:
    """
    Real-time monitoring interface with WebSocket support
    """
    
    def __init__(self, port: int = 8080):
        self.port = port
        self.websocket_clients: Set[websockets.WebSocketServerProtocol] = set()
        
        # Data stores
        self.system_status = SystemStatus(
            timestamp=datetime.now().isoformat(),
            health='healthy',
            active_requirements=0,
            queue_depth=0,
            active_agents=0,
            throughput_per_minute=0.0,
            average_processing_time=0.0,
            error_rate=0.0
        )
        
        self.agent_statuses: Dict[str, AgentStatus] = {}
        self.active_alerts: List[Alert] = []
        self.metric_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        
        # Update intervals
        self.update_interval = 1  # seconds
        self.running = True
        
        # Start update thread
        self.update_thread = threading.Thread(target=self._update_loop)
        self.update_thread.daemon = True
        self.update_thread.start()
    
    async def websocket_handler(self, websocket, path):
        """Handle WebSocket connections"""
        # Register client
        self.websocket_clients.add(websocket)
        logger.info(f"Client connected. Total clients: {len(self.websocket_clients)}")
        
        try:
            # Send initial state
            await self._send_initial_state(websocket)
            
            # Keep connection alive and handle messages
            async for message in websocket:
                await self._handle_client_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            # Unregister client
            self.websocket_clients.remove(websocket)
            logger.info(f"Client disconnected. Total clients: {len(self.websocket_clients)}")
    
    async def _send_initial_state(self, websocket):
        """Send initial system state to new client"""
        initial_data = {
            'type': 'initial_state',
            'data': {
                'system_status': asdict(self.system_status),
                'agent_statuses': {
                    agent_id: asdict(status) 
                    for agent_id, status in self.agent_statuses.items()
                },
                'active_alerts': [asdict(alert) for alert in self.active_alerts[-10:]],
                'metric_history': self._get_metric_history_summary()
            }
        }
        
        await websocket.send(json.dumps(initial_data))
    
    async def _handle_client_message(self, websocket, message):
        """Handle messages from clients"""
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            if message_type == 'acknowledge_alert':
                alert_id = data.get('alert_id')
                self._acknowledge_alert(alert_id)
                
            elif message_type == 'request_metrics':
                metric_name = data.get('metric_name')
                time_range = data.get('time_range', '1h')
                await self._send_metric_details(websocket, metric_name, time_range)
                
            elif message_type == 'ping':
                await websocket.send(json.dumps({'type': 'pong'}))
                
        except Exception as e:
            logger.error(f"Error handling client message: {e}")
    
    def _acknowledge_alert(self, alert_id: str):
        """Acknowledge an alert"""
        for alert in self.active_alerts:
            if alert.id == alert_id:
                alert.acknowledged = True
                self._broadcast_update({
                    'type': 'alert_acknowledged',
                    'data': {'alert_id': alert_id}
                })
                break
    
    async def _send_metric_details(self, websocket, metric_name: str, time_range: str):
        """Send detailed metric history to client"""
        if metric_name in self.metric_history:
            history = list(self.metric_history[metric_name])
            
            # Filter by time range
            if time_range == '5m':
                cutoff = datetime.now() - timedelta(minutes=5)
            elif time_range == '1h':
                cutoff = datetime.now() - timedelta(hours=1)
            else:
                cutoff = datetime.now() - timedelta(days=1)
            
            filtered_history = [
                h for h in history 
                if datetime.fromisoformat(h['timestamp']) > cutoff
            ]
            
            response = {
                'type': 'metric_details',
                'data': {
                    'metric_name': metric_name,
                    'time_range': time_range,
                    'history': filtered_history
                }
            }
            
            await websocket.send(json.dumps(response))
    
    def _get_metric_history_summary(self) -> Dict[str, List[Dict]]:
        """Get summary of recent metrics for initial state"""
        summary = {}
        
        for metric_name, history in self.metric_history.items():
            # Get last 20 points
            recent = list(history)[-20:]
            summary[metric_name] = recent
        
        return summary
    
    def update_system_status(self, **kwargs):
        """Update system status"""
        for key, value in kwargs.items():
            if hasattr(self.system_status, key):
                setattr(self.system_status, key, value)
        
        self.system_status.timestamp = datetime.now().isoformat()
        
        # Determine health based on metrics
        if self.system_status.error_rate > 0.1 or self.system_status.average_processing_time > 600:
            self.system_status.health = 'critical'
        elif self.system_status.error_rate > 0.05 or self.system_status.average_processing_time > 300:
            self.system_status.health = 'warning'
        else:
            self.system_status.health = 'healthy'
        
        # Broadcast update
        self._broadcast_update({
            'type': 'system_status_update',
            'data': asdict(self.system_status)
        })
    
    def update_agent_status(self, agent_id: str, **kwargs):
        """Update agent status"""
        if agent_id not in self.agent_statuses:
            self.agent_statuses[agent_id] = AgentStatus(
                agent_id=agent_id,
                domain=kwargs.get('domain', 'unknown'),
                status='idle',
                current_requirement=None,
                requirements_processed=0,
                success_rate=1.0,
                average_time=0.0,
                last_update=datetime.now().isoformat()
            )
        
        agent = self.agent_statuses[agent_id]
        for key, value in kwargs.items():
            if hasattr(agent, key):
                setattr(agent, key, value)
        
        agent.last_update = datetime.now().isoformat()
        
        # Broadcast update
        self._broadcast_update({
            'type': 'agent_status_update',
            'data': {
                'agent_id': agent_id,
                'status': asdict(agent)
            }
        })
    
    def add_alert(self, severity: str, component: str, message: str, 
                  details: Optional[Dict[str, Any]] = None):
        """Add a new alert"""
        alert = Alert(
            id=f"alert_{len(self.active_alerts)}_{int(time.time())}",
            timestamp=datetime.now().isoformat(),
            severity=severity,
            component=component,
            message=message,
            details=details or {}
        )
        
        self.active_alerts.append(alert)
        
        # Keep only recent alerts
        if len(self.active_alerts) > 100:
            self.active_alerts = self.active_alerts[-100:]
        
        # Broadcast alert
        self._broadcast_update({
            'type': 'new_alert',
            'data': asdict(alert)
        })
        
        return alert
    
    def record_metric(self, metric_name: str, value: float, 
                     tags: Optional[Dict[str, str]] = None):
        """Record a metric value"""
        metric_update = {
            'metric_name': metric_name,
            'value': value,
            'timestamp': datetime.now().isoformat(),
            'tags': tags or {}
        }
        
        # Store in history
        self.metric_history[metric_name].append(metric_update)
        
        # Broadcast update
        self._broadcast_update({
            'type': 'metric_update',
            'data': metric_update
        })
    
    def _broadcast_update(self, message: Dict):
        """Broadcast update to all connected clients"""
        if not self.websocket_clients:
            return
        
        message_json = json.dumps(message)
        
        # Send to all clients
        disconnected_clients = set()
        
        for client in self.websocket_clients:
            try:
                asyncio.create_task(client.send(message_json))
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected_clients.add(client)
        
        # Remove disconnected clients
        self.websocket_clients -= disconnected_clients
    
    def _update_loop(self):
        """Background thread for periodic updates"""
        while self.running:
            try:
                # Simulate system metrics update
                self._simulate_metrics()
                
                # Clean old alerts
                self._clean_old_alerts()
                
                time.sleep(self.update_interval)
                
            except Exception as e:
                logger.error(f"Error in update loop: {e}")
    
    def _simulate_metrics(self):
        """Simulate metric updates (for demo/testing)"""
        import random
        
        # Update system metrics
        self.record_metric('cpu_usage', random.uniform(30, 80))
        self.record_metric('memory_usage', random.uniform(40, 70))
        self.record_metric('queue_depth', random.randint(0, 50))
        
        # Random events
        if random.random() < 0.1:  # 10% chance
            self.add_alert(
                severity=random.choice(['info', 'warning', 'critical']),
                component=random.choice(['agent_1', 'queue', 'database']),
                message=random.choice([
                    'High CPU usage detected',
                    'Queue depth increasing',
                    'Processing time above threshold'
                ]),
                details={'value': random.uniform(70, 95)}
            )
    
    def _clean_old_alerts(self):
        """Remove old acknowledged alerts"""
        cutoff = datetime.now() - timedelta(hours=1)
        
        self.active_alerts = [
            alert for alert in self.active_alerts
            if not alert.acknowledged or 
            datetime.fromisoformat(alert.timestamp) > cutoff
        ]
    
    async def start_http_server(self):
        """Start HTTP server for static files"""
        app = web.Application()
        
        # Configure CORS
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods="*"
            )
        })
        
        # Serve dashboard HTML
        async def serve_dashboard(request):
            html_content = self._generate_dashboard_html()
            return web.Response(text=html_content, content_type='text/html')
        
        # API endpoints
        async def get_status(request):
            return web.json_response({
                'system_status': asdict(self.system_status),
                'agent_count': len(self.agent_statuses),
                'alert_count': len([a for a in self.active_alerts if not a.acknowledged])
            })
        
        # Add routes
        app.router.add_get('/', serve_dashboard)
        app.router.add_get('/api/status', get_status)
        
        # Configure CORS for routes
        for route in list(app.router.routes()):
            cors.add(route)
        
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', self.port)
        await site.start()
        
        logger.info(f"HTTP server started on http://localhost:{self.port}")
    
    def _generate_dashboard_html(self) -> str:
        """Generate dashboard HTML"""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Requirements System - Real-Time Monitor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        .header {
            background: #2c3e50;
            color: white;
            padding: 20px;
            margin: -20px -20px 20px -20px;
        }
        .container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .metric {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
        }
        .metric-value {
            font-weight: bold;
        }
        .status-healthy { color: #27ae60; }
        .status-warning { color: #f39c12; }
        .status-critical { color: #e74c3c; }
        .alert {
            padding: 10px;
            margin: 10px 0;
            border-radius: 4px;
        }
        .alert-info { background: #3498db22; border-left: 3px solid #3498db; }
        .alert-warning { background: #f39c1222; border-left: 3px solid #f39c12; }
        .alert-critical { background: #e74c3c22; border-left: 3px solid #e74c3c; }
        .agent {
            display: flex;
            justify-content: space-between;
            padding: 10px;
            margin: 5px 0;
            background: #ecf0f1;
            border-radius: 4px;
        }
        .agent-idle { border-left: 3px solid #95a5a6; }
        .agent-processing { border-left: 3px solid #3498db; }
        .agent-error { border-left: 3px solid #e74c3c; }
        #connection-status {
            position: fixed;
            top: 10px;
            right: 10px;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
        }
        .connected { background: #27ae60; color: white; }
        .disconnected { background: #e74c3c; color: white; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Requirements Generation System - Real-Time Monitor</h1>
        <div id="connection-status" class="disconnected">Disconnected</div>
    </div>
    
    <div class="container">
        <div class="card">
            <h2>System Status</h2>
            <div id="system-status">
                <div class="metric">
                    <span>Health:</span>
                    <span class="metric-value" id="health">-</span>
                </div>
                <div class="metric">
                    <span>Active Requirements:</span>
                    <span class="metric-value" id="active-requirements">-</span>
                </div>
                <div class="metric">
                    <span>Queue Depth:</span>
                    <span class="metric-value" id="queue-depth">-</span>
                </div>
                <div class="metric">
                    <span>Throughput/min:</span>
                    <span class="metric-value" id="throughput">-</span>
                </div>
                <div class="metric">
                    <span>Avg Processing Time:</span>
                    <span class="metric-value" id="avg-time">-</span>
                </div>
                <div class="metric">
                    <span>Error Rate:</span>
                    <span class="metric-value" id="error-rate">-</span>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>Active Agents</h2>
            <div id="agents-list"></div>
        </div>
        
        <div class="card">
            <h2>Recent Alerts</h2>
            <div id="alerts-list"></div>
        </div>
        
        <div class="card">
            <h2>Performance Metrics</h2>
            <canvas id="metrics-chart" width="400" height="200"></canvas>
        </div>
    </div>
    
    <script>
        let ws = null;
        let metricsData = {};
        
        function connect() {
            ws = new WebSocket('ws://localhost:8081');
            
            ws.onopen = () => {
                console.log('Connected to monitoring server');
                document.getElementById('connection-status').className = 'connected';
                document.getElementById('connection-status').textContent = 'Connected';
            };
            
            ws.onclose = () => {
                console.log('Disconnected from monitoring server');
                document.getElementById('connection-status').className = 'disconnected';
                document.getElementById('connection-status').textContent = 'Disconnected';
                setTimeout(connect, 5000); // Reconnect after 5 seconds
            };
            
            ws.onmessage = (event) => {
                const message = JSON.parse(event.data);
                handleMessage(message);
            };
            
            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        }
        
        function handleMessage(message) {
            switch (message.type) {
                case 'initial_state':
                    updateInitialState(message.data);
                    break;
                case 'system_status_update':
                    updateSystemStatus(message.data);
                    break;
                case 'agent_status_update':
                    updateAgentStatus(message.data);
                    break;
                case 'new_alert':
                    addAlert(message.data);
                    break;
                case 'metric_update':
                    updateMetric(message.data);
                    break;
            }
        }
        
        function updateInitialState(data) {
            updateSystemStatus(data.system_status);
            
            // Update agents
            document.getElementById('agents-list').innerHTML = '';
            for (const [agentId, status] of Object.entries(data.agent_statuses)) {
                updateAgentStatus({ agent_id: agentId, status });
            }
            
            // Update alerts
            document.getElementById('alerts-list').innerHTML = '';
            data.active_alerts.forEach(alert => addAlert(alert));
            
            // Initialize metrics
            metricsData = data.metric_history;
        }
        
        function updateSystemStatus(status) {
            document.getElementById('health').textContent = status.health;
            document.getElementById('health').className = 'metric-value status-' + status.health;
            document.getElementById('active-requirements').textContent = status.active_requirements;
            document.getElementById('queue-depth').textContent = status.queue_depth;
            document.getElementById('throughput').textContent = status.throughput_per_minute.toFixed(1);
            document.getElementById('avg-time').textContent = status.average_processing_time.toFixed(1) + 's';
            document.getElementById('error-rate').textContent = (status.error_rate * 100).toFixed(1) + '%';
        }
        
        function updateAgentStatus(data) {
            const agentId = data.agent_id;
            const status = data.status;
            
            let agentDiv = document.getElementById('agent-' + agentId);
            if (!agentDiv) {
                agentDiv = document.createElement('div');
                agentDiv.id = 'agent-' + agentId;
                document.getElementById('agents-list').appendChild(agentDiv);
            }
            
            agentDiv.className = 'agent agent-' + status.status;
            agentDiv.innerHTML = `
                <span>${agentId} (${status.domain})</span>
                <span>${status.status} - ${status.requirements_processed} processed</span>
            `;
        }
        
        function addAlert(alert) {
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-' + alert.severity;
            alertDiv.innerHTML = `
                <strong>${alert.component}:</strong> ${alert.message}
                <br><small>${new Date(alert.timestamp).toLocaleTimeString()}</small>
            `;
            
            const alertsList = document.getElementById('alerts-list');
            alertsList.insertBefore(alertDiv, alertsList.firstChild);
            
            // Keep only last 5 alerts
            while (alertsList.children.length > 5) {
                alertsList.removeChild(alertsList.lastChild);
            }
        }
        
        function updateMetric(data) {
            if (!metricsData[data.metric_name]) {
                metricsData[data.metric_name] = [];
            }
            metricsData[data.metric_name].push(data);
            
            // Keep only last 50 points
            if (metricsData[data.metric_name].length > 50) {
                metricsData[data.metric_name].shift();
            }
        }
        
        // Connect on load
        connect();
        
        // Send ping every 30 seconds to keep connection alive
        setInterval(() => {
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ type: 'ping' }));
            }
        }, 30000);
    </script>
</body>
</html>
"""
    
    async def start(self):
        """Start the monitoring interface"""
        # Start HTTP server
        await self.start_http_server()
        
        # Start WebSocket server
        ws_server = await websockets.serve(
            self.websocket_handler, 
            'localhost', 
            self.port + 1
        )
        
        logger.info(f"WebSocket server started on ws://localhost:{self.port + 1}")
        
        # Keep server running
        await asyncio.Future()  # Run forever
    
    def stop(self):
        """Stop the monitoring interface"""
        self.running = False
        logger.info("Monitoring interface stopped")


# Simulator for testing
class SystemSimulator:
    """Simulate system activity for testing"""
    
    def __init__(self, monitor: RealTimeMonitoringInterface):
        self.monitor = monitor
        self.agents = [
            ('agent_pp_1', 'producer-portal'),
            ('agent_pp_2', 'producer-portal'),
            ('agent_acc_1', 'accounting'),
            ('agent_ei_1', 'entity-integration')
        ]
        self.running = True
    
    async def simulate(self):
        """Simulate system activity"""
        import random
        
        while self.running:
            try:
                # Update system status
                self.monitor.update_system_status(
                    active_requirements=random.randint(5, 20),
                    queue_depth=random.randint(10, 40),
                    active_agents=random.randint(1, len(self.agents)),
                    throughput_per_minute=random.uniform(10, 30),
                    average_processing_time=random.uniform(50, 300),
                    error_rate=random.uniform(0.01, 0.1)
                )
                
                # Update agent statuses
                for agent_id, domain in self.agents:
                    status = random.choice(['idle', 'processing', 'processing', 'processing'])
                    self.monitor.update_agent_status(
                        agent_id,
                        domain=domain,
                        status=status,
                        current_requirement=f"REQ_{random.randint(1000, 9999)}" if status == 'processing' else None,
                        requirements_processed=random.randint(50, 200),
                        success_rate=random.uniform(0.85, 0.99),
                        average_time=random.uniform(30, 180)
                    )
                
                # Record metrics
                self.monitor.record_metric('cpu_usage', random.uniform(30, 80))
                self.monitor.record_metric('memory_usage', random.uniform(40, 70))
                self.monitor.record_metric('db_connections', random.randint(5, 20))
                
                # Occasionally add alerts
                if random.random() < 0.1:  # 10% chance
                    severity = random.choice(['info', 'warning', 'critical'])
                    components = ['queue', 'agent', 'database', 'api']
                    messages = [
                        'High load detected',
                        'Processing time above threshold',
                        'Error rate increasing',
                        'Resource limit approaching'
                    ]
                    
                    self.monitor.add_alert(
                        severity=severity,
                        component=random.choice(components),
                        message=random.choice(messages),
                        details={'metric': random.uniform(70, 95)}
                    )
                
                await asyncio.sleep(2)  # Update every 2 seconds
                
            except Exception as e:
                logger.error(f"Simulation error: {e}")
                await asyncio.sleep(5)


# Main execution
async def main():
    """Main function to run the monitoring interface"""
    # Create monitoring interface
    monitor = RealTimeMonitoringInterface(port=8080)
    
    # Create simulator for testing
    simulator = SystemSimulator(monitor)
    
    # Start monitoring and simulation
    await asyncio.gather(
        monitor.start(),
        simulator.simulate()
    )


if __name__ == "__main__":
    print("=== Real-Time Monitoring Interface ===")
    print("Starting monitoring server...")
    print("Dashboard: http://localhost:8080")
    print("WebSocket: ws://localhost:8081")
    print("\nPress Ctrl+C to stop\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down monitoring interface...")