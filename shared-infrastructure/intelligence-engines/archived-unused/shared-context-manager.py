#!/usr/bin/env python3
"""
Shared Context Manager
Complete Requirements Generation System - Multi-Agent Architecture

Manages shared context and real-time coordination between all agents
in the multi-agent requirements processing system.

Created: 2025-01-07
Version: 1.0.0
GR Compliance: GR-38, GR-49, GR-52
"""

import json
import yaml
import logging
import asyncio
import threading
from typing import Dict, List, Optional, Tuple, Any, Set, Callable
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import defaultdict
import time
import weakref

# Configuration and Data Classes
@dataclass
class ContextEntry:
    """Represents a single context entry."""
    entry_id: str
    context_type: str
    agent_id: str
    timestamp: datetime
    content: Dict
    ttl_seconds: Optional[int] = None
    tags: List[str] = field(default_factory=list)
    priority: str = "medium"  # high, medium, low

@dataclass
class AgentRegistration:
    """Represents an agent registration in the shared context."""
    agent_id: str
    agent_type: str
    domain: str
    capabilities: List[str]
    registration_time: datetime
    last_ping: datetime
    status: str = "active"  # active, inactive, error
    subscriptions: List[str] = field(default_factory=list)

@dataclass
class ContextUpdate:
    """Represents a context update event."""
    update_id: str
    update_type: str  # create, update, delete, sync
    context_type: str
    affected_entries: List[str]
    timestamp: datetime
    agent_id: str
    metadata: Dict = field(default_factory=dict)

class ContextType(Enum):
    """Types of context data."""
    ENTITY = "entity"
    PATTERN = "pattern"
    WORKFLOW = "workflow"
    VALIDATION = "validation"
    INTELLIGENCE = "intelligence"
    PERFORMANCE = "performance"
    ERROR = "error"
    COORDINATION = "coordination"

class UpdateType(Enum):
    """Types of context updates."""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    SYNC = "sync"
    BROADCAST = "broadcast"

class Priority(Enum):
    """Priority levels for context entries."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    CRITICAL = "critical"

class SharedContextManager:
    """
    Central manager for shared context between all agents.
    Provides real-time synchronization, conflict resolution, and persistence.
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the Shared Context Manager."""
        self.config_path = config_path or "/app/workspace/requirements/shared-infrastructure/agent-configurations/system-orchestrator.yaml"
        self.config = self._load_configuration()
        self.logger = self._setup_logging()
        
        # Context storage
        self.context_data: Dict[str, Dict[str, ContextEntry]] = defaultdict(dict)
        self.context_lock = threading.RLock()
        
        # Agent management
        self.registered_agents: Dict[str, AgentRegistration] = {}
        self.agent_callbacks: Dict[str, List[Callable]] = defaultdict(list)
        
        # Update tracking
        self.update_history: List[ContextUpdate] = []
        self.pending_updates: Dict[str, List[ContextUpdate]] = defaultdict(list)
        
        # Synchronization
        self.sync_enabled = True
        self.sync_interval = 5  # seconds
        self.sync_task = None
        
        # Performance tracking
        self.performance_metrics = {
            "total_entries": 0,
            "updates_per_second": 0,
            "memory_usage_mb": 0,
            "active_agents": 0
        }
        
        # Initialize manager
        self._initialize_manager()
    
    def _load_configuration(self) -> Dict:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config.get("shared_context", {})
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Return default configuration."""
        return {
            "real_time_sync": True,
            "sync_interval": "5 seconds",
            "conflict_resolution": "orchestrator_authority",
            "context_persistence": True,
            "context_retention": "30 days",
            "max_context_size": "100MB",
            "compression_enabled": True,
            "delta_sync_enabled": True
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the context manager."""
        logger = logging.getLogger("SharedContextManager")
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def _initialize_manager(self):
        """Initialize the context manager."""
        self.logger.info("Initializing Shared Context Manager...")
        
        try:
            # Load persisted context if available
            self._load_persisted_context()
            
            # Start synchronization if enabled
            if self.config.get("real_time_sync", True):
                self._start_sync_task()
            
            # Start cleanup task
            self._start_cleanup_task()
            
            self.logger.info("Shared Context Manager initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize context manager: {e}")
            raise
    
    def _start_sync_task(self):
        """Start the background synchronization task."""
        if self.sync_task:
            return  # Already running
        
        async def sync_loop():
            while self.sync_enabled:
                try:
                    await self._perform_sync()
                    await asyncio.sleep(self.sync_interval)
                except Exception as e:
                    self.logger.error(f"Error in sync loop: {e}")
                    await asyncio.sleep(self.sync_interval)
        
        self.sync_task = asyncio.create_task(sync_loop())
        self.logger.info("Synchronization task started")
    
    def _start_cleanup_task(self):
        """Start the background cleanup task."""
        async def cleanup_loop():
            while True:
                try:
                    await self._cleanup_expired_entries()
                    await asyncio.sleep(300)  # Run every 5 minutes
                except Exception as e:
                    self.logger.error(f"Error in cleanup loop: {e}")
                    await asyncio.sleep(300)
        
        asyncio.create_task(cleanup_loop())
        self.logger.info("Cleanup task started")
    
    async def register_agent(self, 
                           agent_id: str,
                           agent_type: str,
                           domain: str,
                           capabilities: List[str],
                           subscriptions: List[str] = None) -> bool:
        """
        Register an agent with the shared context.
        
        Args:
            agent_id: Unique identifier for the agent
            agent_type: Type of agent (orchestrator, domain_specialist, validator)
            domain: Domain the agent specializes in
            capabilities: List of agent capabilities
            subscriptions: Context types the agent wants to be notified about
            
        Returns:
            bool: True if registration successful
        """
        try:
            with self.context_lock:
                registration = AgentRegistration(
                    agent_id=agent_id,
                    agent_type=agent_type,
                    domain=domain,
                    capabilities=capabilities,
                    registration_time=datetime.now(),
                    last_ping=datetime.now(),
                    status="active",
                    subscriptions=subscriptions or []
                )
                
                self.registered_agents[agent_id] = registration
                
                # Log registration
                self.logger.info(f"Agent registered: {agent_id} ({agent_type}) for domain {domain}")
                
                # Notify other agents of new registration
                await self._broadcast_update(
                    update_type=UpdateType.CREATE,
                    context_type="agent_registration",
                    content={"agent_id": agent_id, "domain": domain, "capabilities": capabilities},
                    agent_id="system"
                )
                
                return True
                
        except Exception as e:
            self.logger.error(f"Error registering agent {agent_id}: {e}")
            return False
    
    async def unregister_agent(self, agent_id: str) -> bool:
        """
        Unregister an agent from the shared context.
        
        Args:
            agent_id: Unique identifier for the agent
            
        Returns:
            bool: True if unregistration successful
        """
        try:
            with self.context_lock:
                if agent_id in self.registered_agents:
                    del self.registered_agents[agent_id]
                    
                    # Remove agent callbacks
                    if agent_id in self.agent_callbacks:
                        del self.agent_callbacks[agent_id]
                    
                    self.logger.info(f"Agent unregistered: {agent_id}")
                    
                    # Notify other agents
                    await self._broadcast_update(
                        update_type=UpdateType.DELETE,
                        context_type="agent_registration",
                        content={"agent_id": agent_id},
                        agent_id="system"
                    )
                    
                    return True
                else:
                    self.logger.warning(f"Attempted to unregister unknown agent: {agent_id}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error unregistering agent {agent_id}: {e}")
            return False
    
    async def ping_agent(self, agent_id: str) -> bool:
        """
        Update agent last ping time.
        
        Args:
            agent_id: Unique identifier for the agent
            
        Returns:
            bool: True if ping successful
        """
        try:
            with self.context_lock:
                if agent_id in self.registered_agents:
                    self.registered_agents[agent_id].last_ping = datetime.now()
                    self.registered_agents[agent_id].status = "active"
                    return True
                else:
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error pinging agent {agent_id}: {e}")
            return False
    
    async def add_context(self, 
                         context_type: str,
                         content: Dict,
                         agent_id: str,
                         entry_id: str = None,
                         ttl_seconds: int = None,
                         tags: List[str] = None,
                         priority: str = "medium") -> str:
        """
        Add a new context entry.
        
        Args:
            context_type: Type of context (entity, pattern, workflow, etc.)
            content: Context data
            agent_id: ID of the agent adding the context
            entry_id: Optional custom entry ID
            ttl_seconds: Time to live in seconds
            tags: Optional tags for categorization
            priority: Priority level (high, medium, low, critical)
            
        Returns:
            str: Entry ID of the added context
        """
        try:
            if not entry_id:
                entry_id = self._generate_entry_id(context_type, agent_id)
            
            with self.context_lock:
                entry = ContextEntry(
                    entry_id=entry_id,
                    context_type=context_type,
                    agent_id=agent_id,
                    timestamp=datetime.now(),
                    content=content,
                    ttl_seconds=ttl_seconds,
                    tags=tags or [],
                    priority=priority
                )
                
                self.context_data[context_type][entry_id] = entry
                
                # Update metrics
                self.performance_metrics["total_entries"] = sum(
                    len(entries) for entries in self.context_data.values()
                )
                
                self.logger.debug(f"Context added: {context_type}/{entry_id} by {agent_id}")
                
                # Notify subscribers
                await self._notify_subscribers(
                    update_type=UpdateType.CREATE,
                    context_type=context_type,
                    entry_id=entry_id,
                    content=content,
                    agent_id=agent_id
                )
                
                return entry_id
                
        except Exception as e:
            self.logger.error(f"Error adding context: {e}")
            raise
    
    async def update_context(self, 
                           context_type: str,
                           entry_id: str,
                           content: Dict,
                           agent_id: str,
                           merge: bool = True) -> bool:
        """
        Update an existing context entry.
        
        Args:
            context_type: Type of context
            entry_id: ID of the entry to update
            content: New content
            agent_id: ID of the agent updating the context
            merge: Whether to merge with existing content or replace
            
        Returns:
            bool: True if update successful
        """
        try:
            with self.context_lock:
                if context_type in self.context_data and entry_id in self.context_data[context_type]:
                    entry = self.context_data[context_type][entry_id]
                    
                    # Check if agent has permission to update
                    if not self._can_agent_update(agent_id, entry):
                        self.logger.warning(f"Agent {agent_id} not authorized to update {context_type}/{entry_id}")
                        return False
                    
                    # Update content
                    if merge:
                        entry.content.update(content)
                    else:
                        entry.content = content
                    
                    entry.timestamp = datetime.now()
                    
                    self.logger.debug(f"Context updated: {context_type}/{entry_id} by {agent_id}")
                    
                    # Notify subscribers
                    await self._notify_subscribers(
                        update_type=UpdateType.UPDATE,
                        context_type=context_type,
                        entry_id=entry_id,
                        content=entry.content,
                        agent_id=agent_id
                    )
                    
                    return True
                else:
                    self.logger.warning(f"Context entry not found: {context_type}/{entry_id}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error updating context: {e}")
            return False
    
    async def get_context(self, 
                         context_type: str,
                         entry_id: str = None,
                         agent_id: str = None,
                         tags: List[str] = None) -> Optional[Dict]:
        """
        Retrieve context data.
        
        Args:
            context_type: Type of context
            entry_id: Specific entry ID (if None, returns all entries of type)
            agent_id: Filter by agent ID
            tags: Filter by tags
            
        Returns:
            Dict or List of context entries
        """
        try:
            with self.context_lock:
                if context_type not in self.context_data:
                    return {} if entry_id else []
                
                if entry_id:
                    # Return specific entry
                    if entry_id in self.context_data[context_type]:
                        entry = self.context_data[context_type][entry_id]
                        return {
                            "entry_id": entry.entry_id,
                            "context_type": entry.context_type,
                            "agent_id": entry.agent_id,
                            "timestamp": entry.timestamp.isoformat(),
                            "content": entry.content,
                            "tags": entry.tags,
                            "priority": entry.priority
                        }
                    else:
                        return None
                else:
                    # Return all entries with optional filtering
                    entries = []
                    for entry in self.context_data[context_type].values():
                        # Apply filters
                        if agent_id and entry.agent_id != agent_id:
                            continue
                        if tags and not any(tag in entry.tags for tag in tags):
                            continue
                        
                        entries.append({
                            "entry_id": entry.entry_id,
                            "context_type": entry.context_type,
                            "agent_id": entry.agent_id,
                            "timestamp": entry.timestamp.isoformat(),
                            "content": entry.content,
                            "tags": entry.tags,
                            "priority": entry.priority
                        })
                    
                    return entries
                    
        except Exception as e:
            self.logger.error(f"Error getting context: {e}")
            return None
    
    async def delete_context(self, 
                           context_type: str,
                           entry_id: str,
                           agent_id: str) -> bool:
        """
        Delete a context entry.
        
        Args:
            context_type: Type of context
            entry_id: ID of the entry to delete
            agent_id: ID of the agent deleting the context
            
        Returns:
            bool: True if deletion successful
        """
        try:
            with self.context_lock:
                if context_type in self.context_data and entry_id in self.context_data[context_type]:
                    entry = self.context_data[context_type][entry_id]
                    
                    # Check if agent has permission to delete
                    if not self._can_agent_delete(agent_id, entry):
                        self.logger.warning(f"Agent {agent_id} not authorized to delete {context_type}/{entry_id}")
                        return False
                    
                    # Delete entry
                    del self.context_data[context_type][entry_id]
                    
                    # Update metrics
                    self.performance_metrics["total_entries"] = sum(
                        len(entries) for entries in self.context_data.values()
                    )
                    
                    self.logger.debug(f"Context deleted: {context_type}/{entry_id} by {agent_id}")
                    
                    # Notify subscribers
                    await self._notify_subscribers(
                        update_type=UpdateType.DELETE,
                        context_type=context_type,
                        entry_id=entry_id,
                        content={"deleted": True},
                        agent_id=agent_id
                    )
                    
                    return True
                else:
                    self.logger.warning(f"Context entry not found for deletion: {context_type}/{entry_id}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error deleting context: {e}")
            return False
    
    async def subscribe_to_updates(self, 
                                 agent_id: str,
                                 context_types: List[str],
                                 callback: Callable) -> bool:
        """
        Subscribe an agent to context update notifications.
        
        Args:
            agent_id: ID of the subscribing agent
            context_types: List of context types to subscribe to
            callback: Function to call when updates occur
            
        Returns:
            bool: True if subscription successful
        """
        try:
            # Store callback with weak reference to prevent memory leaks
            callback_ref = weakref.ref(callback)
            
            for context_type in context_types:
                subscription_key = f"{agent_id}:{context_type}"
                self.agent_callbacks[subscription_key].append(callback_ref)
            
            # Update agent subscriptions
            if agent_id in self.registered_agents:
                self.registered_agents[agent_id].subscriptions.extend(context_types)
                self.registered_agents[agent_id].subscriptions = list(set(self.registered_agents[agent_id].subscriptions))
            
            self.logger.info(f"Agent {agent_id} subscribed to {context_types}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error subscribing agent {agent_id}: {e}")
            return False
    
    async def unsubscribe_from_updates(self, 
                                     agent_id: str,
                                     context_types: List[str] = None) -> bool:
        """
        Unsubscribe an agent from context update notifications.
        
        Args:
            agent_id: ID of the subscribing agent
            context_types: List of context types to unsubscribe from (if None, unsubscribe from all)
            
        Returns:
            bool: True if unsubscription successful
        """
        try:
            if context_types is None:
                # Unsubscribe from all
                keys_to_remove = [key for key in self.agent_callbacks.keys() if key.startswith(f"{agent_id}:")]
                for key in keys_to_remove:
                    del self.agent_callbacks[key]
                
                if agent_id in self.registered_agents:
                    self.registered_agents[agent_id].subscriptions = []
            else:
                # Unsubscribe from specific types
                for context_type in context_types:
                    subscription_key = f"{agent_id}:{context_type}"
                    if subscription_key in self.agent_callbacks:
                        del self.agent_callbacks[subscription_key]
                
                if agent_id in self.registered_agents:
                    current_subs = self.registered_agents[agent_id].subscriptions
                    self.registered_agents[agent_id].subscriptions = [
                        sub for sub in current_subs if sub not in context_types
                    ]
            
            self.logger.info(f"Agent {agent_id} unsubscribed from {context_types or 'all'}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error unsubscribing agent {agent_id}: {e}")
            return False
    
    async def _notify_subscribers(self, 
                                update_type: UpdateType,
                                context_type: str,
                                entry_id: str,
                                content: Dict,
                                agent_id: str):
        """Notify subscribers of context updates."""
        try:
            update = ContextUpdate(
                update_id=self._generate_update_id(),
                update_type=update_type.value,
                context_type=context_type,
                affected_entries=[entry_id],
                timestamp=datetime.now(),
                agent_id=agent_id
            )
            
            # Add to update history
            self.update_history.append(update)
            
            # Limit history size
            if len(self.update_history) > 1000:
                self.update_history = self.update_history[-1000:]
            
            # Notify subscribers
            subscription_key = f"*:{context_type}"  # Wildcard subscription
            specific_keys = [key for key in self.agent_callbacks.keys() if key.endswith(f":{context_type}")]
            
            for key in specific_keys:
                callbacks = self.agent_callbacks[key]
                for callback_ref in callbacks[:]:  # Copy list to avoid modification during iteration
                    callback = callback_ref()
                    if callback is None:
                        # Callback was garbage collected, remove reference
                        callbacks.remove(callback_ref)
                    else:
                        try:
                            # Call the callback asynchronously
                            if asyncio.iscoroutinefunction(callback):
                                asyncio.create_task(callback(update))
                            else:
                                callback(update)
                        except Exception as e:
                            self.logger.error(f"Error calling callback for {key}: {e}")
            
        except Exception as e:
            self.logger.error(f"Error notifying subscribers: {e}")
    
    async def _broadcast_update(self, 
                              update_type: UpdateType,
                              context_type: str,
                              content: Dict,
                              agent_id: str):
        """Broadcast an update to all interested agents."""
        try:
            update = ContextUpdate(
                update_id=self._generate_update_id(),
                update_type=update_type.value,
                context_type=context_type,
                affected_entries=[],
                timestamp=datetime.now(),
                agent_id=agent_id,
                metadata=content
            )
            
            # Notify all registered agents
            for registered_agent in self.registered_agents.values():
                if context_type in registered_agent.subscriptions or "all" in registered_agent.subscriptions:
                    subscription_key = f"{registered_agent.agent_id}:{context_type}"
                    if subscription_key in self.agent_callbacks:
                        callbacks = self.agent_callbacks[subscription_key]
                        for callback_ref in callbacks[:]:
                            callback = callback_ref()
                            if callback:
                                try:
                                    if asyncio.iscoroutinefunction(callback):
                                        asyncio.create_task(callback(update))
                                    else:
                                        callback(update)
                                except Exception as e:
                                    self.logger.error(f"Error broadcasting to {registered_agent.agent_id}: {e}")
            
        except Exception as e:
            self.logger.error(f"Error broadcasting update: {e}")
    
    async def _perform_sync(self):
        """Perform periodic synchronization tasks."""
        try:
            # Check agent health
            await self._check_agent_health()
            
            # Process pending updates
            await self._process_pending_updates()
            
            # Update performance metrics
            self._update_performance_metrics()
            
            # Persist context if enabled
            if self.config.get("context_persistence", True):
                await self._persist_context()
            
        except Exception as e:
            self.logger.error(f"Error in synchronization: {e}")
    
    async def _check_agent_health(self):
        """Check health of registered agents."""
        current_time = datetime.now()
        inactive_threshold = timedelta(seconds=60)  # 1 minute
        
        for agent_id, registration in list(self.registered_agents.items()):
            time_since_ping = current_time - registration.last_ping
            
            if time_since_ping > inactive_threshold:
                if registration.status == "active":
                    registration.status = "inactive"
                    self.logger.warning(f"Agent {agent_id} marked as inactive (no ping for {time_since_ping})")
                
                # Remove agents that have been inactive for too long
                if time_since_ping > timedelta(minutes=10):
                    await self.unregister_agent(agent_id)
    
    async def _process_pending_updates(self):
        """Process any pending updates."""
        # Implementation for handling delayed updates, conflict resolution, etc.
        pass
    
    def _update_performance_metrics(self):
        """Update performance metrics."""
        self.performance_metrics.update({
            "total_entries": sum(len(entries) for entries in self.context_data.values()),
            "active_agents": sum(1 for agent in self.registered_agents.values() if agent.status == "active"),
            "memory_usage_mb": self._estimate_memory_usage(),
            "last_updated": datetime.now().isoformat()
        })
    
    def _estimate_memory_usage(self) -> float:
        """Estimate memory usage in MB."""
        try:
            import sys
            total_size = 0
            
            # Estimate context data size
            total_size += sys.getsizeof(self.context_data)
            for context_type, entries in self.context_data.items():
                total_size += sys.getsizeof(entries)
                for entry in entries.values():
                    total_size += sys.getsizeof(entry)
                    total_size += sys.getsizeof(entry.content)
            
            # Estimate other data structures
            total_size += sys.getsizeof(self.registered_agents)
            total_size += sys.getsizeof(self.update_history)
            
            return total_size / (1024 * 1024)  # Convert to MB
        except:
            return 0.0
    
    async def _cleanup_expired_entries(self):
        """Clean up expired context entries."""
        current_time = datetime.now()
        
        with self.context_lock:
            for context_type, entries in list(self.context_data.items()):
                for entry_id, entry in list(entries.items()):
                    # Check TTL
                    if entry.ttl_seconds:
                        expiry_time = entry.timestamp + timedelta(seconds=entry.ttl_seconds)
                        if current_time > expiry_time:
                            del entries[entry_id]
                            self.logger.debug(f"Expired context entry removed: {context_type}/{entry_id}")
                
                # Remove empty context types
                if not entries:
                    del self.context_data[context_type]
    
    async def _persist_context(self):
        """Persist context to storage."""
        # Implementation for context persistence
        pass
    
    def _load_persisted_context(self):
        """Load persisted context from storage."""
        # Implementation for loading persisted context
        pass
    
    def _can_agent_update(self, agent_id: str, entry: ContextEntry) -> bool:
        """Check if an agent can update a context entry."""
        # Allow the original creator to update
        if entry.agent_id == agent_id:
            return True
        
        # Allow orchestrator to update anything
        if agent_id == "system-orchestrator":
            return True
        
        # Check agent permissions based on type
        if agent_id in self.registered_agents:
            agent = self.registered_agents[agent_id]
            if agent.agent_type == "orchestrator":
                return True
        
        return False
    
    def _can_agent_delete(self, agent_id: str, entry: ContextEntry) -> bool:
        """Check if an agent can delete a context entry."""
        # Same rules as update for now
        return self._can_agent_update(agent_id, entry)
    
    def _generate_entry_id(self, context_type: str, agent_id: str) -> str:
        """Generate a unique entry ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        content_hash = hashlib.sha256(f"{context_type}_{agent_id}_{timestamp}".encode()).hexdigest()[:8]
        return f"{context_type}_{agent_id}_{timestamp}_{content_hash}"
    
    def _generate_update_id(self) -> str:
        """Generate a unique update ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"update_{timestamp}"
    
    def get_context_statistics(self) -> Dict:
        """Get statistics about the shared context."""
        with self.context_lock:
            context_stats = {}
            for context_type, entries in self.context_data.items():
                context_stats[context_type] = {
                    "entry_count": len(entries),
                    "agents": list(set(entry.agent_id for entry in entries.values())),
                    "latest_update": max((entry.timestamp for entry in entries.values()), default=None)
                }
            
            return {
                "context_types": context_stats,
                "registered_agents": len(self.registered_agents),
                "active_agents": sum(1 for agent in self.registered_agents.values() if agent.status == "active"),
                "total_entries": sum(len(entries) for entries in self.context_data.values()),
                "update_history_size": len(self.update_history),
                "performance_metrics": self.performance_metrics,
                "subscriptions": sum(len(agent.subscriptions) for agent in self.registered_agents.values())
            }
    
    def get_agent_status(self, agent_id: str = None) -> Dict:
        """Get status of specific agent or all agents."""
        with self.context_lock:
            if agent_id:
                if agent_id in self.registered_agents:
                    agent = self.registered_agents[agent_id]
                    return {
                        "agent_id": agent.agent_id,
                        "agent_type": agent.agent_type,
                        "domain": agent.domain,
                        "status": agent.status,
                        "last_ping": agent.last_ping.isoformat(),
                        "subscriptions": agent.subscriptions,
                        "capabilities": agent.capabilities
                    }
                else:
                    return {}
            else:
                return {
                    agent_id: {
                        "agent_type": agent.agent_type,
                        "domain": agent.domain,
                        "status": agent.status,
                        "last_ping": agent.last_ping.isoformat(),
                        "subscriptions": agent.subscriptions
                    }
                    for agent_id, agent in self.registered_agents.items()
                }
    
    async def shutdown(self):
        """Shutdown the shared context manager."""
        self.logger.info("Shutting down Shared Context Manager...")
        
        # Stop synchronization
        self.sync_enabled = False
        if self.sync_task:
            self.sync_task.cancel()
            try:
                await self.sync_task
            except asyncio.CancelledError:
                pass
        
        # Persist final context
        if self.config.get("context_persistence", True):
            await self._persist_context()
        
        # Clear all data
        with self.context_lock:
            self.context_data.clear()
            self.registered_agents.clear()
            self.agent_callbacks.clear()
        
        self.logger.info("Shared Context Manager shutdown complete")

# Main execution and testing
if __name__ == "__main__":
    async def test_shared_context_manager():
        """Test the Shared Context Manager."""
        print("Testing Shared Context Manager...")
        
        # Initialize context manager
        manager = SharedContextManager()
        
        # Test agent registration
        await manager.register_agent(
            agent_id="test-orchestrator",
            agent_type="orchestrator",
            domain="system",
            capabilities=["coordination", "pattern_recognition"],
            subscriptions=["entity", "workflow"]
        )
        
        await manager.register_agent(
            agent_id="test-domain-specialist",
            agent_type="domain_specialist",
            domain="producer_portal",
            capabilities=["quote_processing", "entity_management"],
            subscriptions=["entity", "validation"]
        )
        
        # Test context operations
        entity_id = await manager.add_context(
            context_type="entity",
            content={
                "entity_name": "driver",
                "fields": ["driver_id", "license_number", "first_name"],
                "domain": "producer_portal"
            },
            agent_id="test-domain-specialist",
            tags=["driver", "entity_definition"]
        )
        
        # Test context retrieval
        entity_data = await manager.get_context("entity", entity_id)
        print(f"Retrieved entity: {json.dumps(entity_data, indent=2)}")
        
        # Test context update
        await manager.update_context(
            context_type="entity",
            entry_id=entity_id,
            content={"validation_rules": ["required", "unique"]},
            agent_id="test-domain-specialist"
        )
        
        # Test statistics
        stats = manager.get_context_statistics()
        print(f"Context Statistics: {json.dumps(stats, indent=2, default=str)}")
        
        # Test agent status
        agent_status = manager.get_agent_status()
        print(f"Agent Status: {json.dumps(agent_status, indent=2, default=str)}")
        
        # Wait a bit to see synchronization
        await asyncio.sleep(2)
        
        # Shutdown
        await manager.shutdown()
        
        return manager
    
    # Run test if executed directly
    import asyncio
    asyncio.run(test_shared_context_manager())