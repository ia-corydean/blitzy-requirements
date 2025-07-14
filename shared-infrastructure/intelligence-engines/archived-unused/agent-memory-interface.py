#!/usr/bin/env python3
"""
Agent Memory Interface
Complete Requirements Generation System - Multi-Agent Architecture

Provides a clean, standardized interface for agents to interact with
the shared context and memory management system.

Created: 2025-01-07
Version: 1.0.0
GR Compliance: GR-38, GR-49, GR-52
"""

import json
import logging
import asyncio
from typing import Dict, List, Optional, Tuple, Any, Callable
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict

# Import the shared context manager
try:
    from .shared_context_manager import SharedContextManager, ContextUpdate, ContextType
except ImportError:
    # For standalone testing
    import sys
    sys.path.append(str(Path(__file__).parent))
    from shared_context_manager import SharedContextManager, ContextUpdate, ContextType

# Configuration and Data Classes
@dataclass
class MemoryQuery:
    """Represents a memory query."""
    query_id: str
    agent_id: str
    query_type: str
    context_types: List[str]
    filters: Dict
    timestamp: datetime

@dataclass
class MemoryResult:
    """Represents a memory query result."""
    query_id: str
    success: bool
    data: List[Dict]
    metadata: Dict
    processing_time: float
    error_message: Optional[str] = None

class QueryType(Enum):
    """Types of memory queries."""
    GET_ENTITIES = "get_entities"
    GET_PATTERNS = "get_patterns" 
    GET_WORKFLOWS = "get_workflows"
    GET_VALIDATIONS = "get_validations"
    GET_INTELLIGENCE = "get_intelligence"
    SEARCH = "search"
    GET_RECENT = "get_recent"
    GET_BY_AGENT = "get_by_agent"
    GET_BY_TAGS = "get_by_tags"

class AgentMemoryInterface:
    """
    Interface for agents to interact with shared memory and context.
    Provides high-level methods for memory operations, caching, and notifications.
    """
    
    def __init__(self, 
                 agent_id: str,
                 agent_type: str,
                 domain: str,
                 capabilities: List[str],
                 shared_context_manager: SharedContextManager = None):
        """
        Initialize the Agent Memory Interface.
        
        Args:
            agent_id: Unique identifier for the agent
            agent_type: Type of agent (orchestrator, domain_specialist, validator)
            domain: Domain the agent specializes in
            capabilities: List of agent capabilities
            shared_context_manager: Instance of SharedContextManager (if None, creates new one)
        """
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.domain = domain
        self.capabilities = capabilities
        
        # Initialize logger
        self.logger = self._setup_logging()
        
        # Shared context manager
        self.context_manager = shared_context_manager or SharedContextManager()
        
        # Local cache
        self.local_cache = {}
        self.cache_ttl = timedelta(minutes=30)
        self.cache_hits = 0
        self.cache_misses = 0
        
        # Query tracking
        self.query_history = []
        self.active_subscriptions = []
        
        # Performance metrics
        self.performance_metrics = {
            "queries_executed": 0,
            "memory_operations": 0,
            "cache_hit_rate": 0.0,
            "average_query_time": 0.0
        }
        
        # Initialize interface
        self._initialize_interface()
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the memory interface."""
        logger = logging.getLogger(f"AgentMemoryInterface_{self.agent_id}")
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def _initialize_interface(self):
        """Initialize the memory interface."""
        self.logger.info(f"Initializing Agent Memory Interface for {self.agent_id}")
        
        try:
            # This will be called after context manager is available
            pass
        except Exception as e:
            self.logger.error(f"Error initializing memory interface: {e}")
    
    async def connect(self, subscriptions: List[str] = None) -> bool:
        """
        Connect the agent to the shared context system.
        
        Args:
            subscriptions: List of context types to subscribe to for notifications
            
        Returns:
            bool: True if connection successful
        """
        try:
            # Register with context manager
            success = await self.context_manager.register_agent(
                agent_id=self.agent_id,
                agent_type=self.agent_type,
                domain=self.domain,
                capabilities=self.capabilities,
                subscriptions=subscriptions or []
            )
            
            if success:
                # Set up subscriptions
                if subscriptions:
                    await self.subscribe_to_updates(subscriptions)
                
                self.logger.info(f"Agent {self.agent_id} connected to shared context")
                return True
            else:
                self.logger.error(f"Failed to register agent {self.agent_id}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error connecting agent {self.agent_id}: {e}")
            return False
    
    async def disconnect(self) -> bool:
        """
        Disconnect the agent from the shared context system.
        
        Returns:
            bool: True if disconnection successful
        """
        try:
            # Unregister from context manager
            success = await self.context_manager.unregister_agent(self.agent_id)
            
            if success:
                self.logger.info(f"Agent {self.agent_id} disconnected from shared context")
                return True
            else:
                self.logger.error(f"Failed to unregister agent {self.agent_id}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error disconnecting agent {self.agent_id}: {e}")
            return False
    
    async def ping(self) -> bool:
        """
        Send a ping to maintain connection with shared context.
        
        Returns:
            bool: True if ping successful
        """
        try:
            return await self.context_manager.ping_agent(self.agent_id)
        except Exception as e:
            self.logger.error(f"Error pinging from agent {self.agent_id}: {e}")
            return False
    
    # Memory Storage Operations
    
    async def store_entity(self, 
                          entity_name: str,
                          entity_data: Dict,
                          tags: List[str] = None,
                          ttl_seconds: int = None) -> str:
        """
        Store entity information in shared memory.
        
        Args:
            entity_name: Name of the entity
            entity_data: Entity data to store
            tags: Optional tags for categorization
            ttl_seconds: Time to live in seconds
            
        Returns:
            str: Entry ID of the stored entity
        """
        try:
            content = {
                "entity_name": entity_name,
                "entity_data": entity_data,
                "stored_by": self.agent_id,
                "domain": self.domain
            }
            
            entry_id = await self.context_manager.add_context(
                context_type=ContextType.ENTITY.value,
                content=content,
                agent_id=self.agent_id,
                ttl_seconds=ttl_seconds,
                tags=tags or [entity_name, "entity"]
            )
            
            # Update local cache
            self._cache_entry(ContextType.ENTITY.value, entry_id, content)
            
            self.performance_metrics["memory_operations"] += 1
            self.logger.debug(f"Entity stored: {entity_name} -> {entry_id}")
            
            return entry_id
            
        except Exception as e:
            self.logger.error(f"Error storing entity {entity_name}: {e}")
            raise
    
    async def store_pattern(self, 
                           pattern_name: str,
                           pattern_data: Dict,
                           tags: List[str] = None,
                           ttl_seconds: int = None) -> str:
        """
        Store pattern information in shared memory.
        
        Args:
            pattern_name: Name of the pattern
            pattern_data: Pattern data to store
            tags: Optional tags for categorization
            ttl_seconds: Time to live in seconds
            
        Returns:
            str: Entry ID of the stored pattern
        """
        try:
            content = {
                "pattern_name": pattern_name,
                "pattern_data": pattern_data,
                "stored_by": self.agent_id,
                "domain": self.domain
            }
            
            entry_id = await self.context_manager.add_context(
                context_type=ContextType.PATTERN.value,
                content=content,
                agent_id=self.agent_id,
                ttl_seconds=ttl_seconds,
                tags=tags or [pattern_name, "pattern"]
            )
            
            # Update local cache
            self._cache_entry(ContextType.PATTERN.value, entry_id, content)
            
            self.performance_metrics["memory_operations"] += 1
            self.logger.debug(f"Pattern stored: {pattern_name} -> {entry_id}")
            
            return entry_id
            
        except Exception as e:
            self.logger.error(f"Error storing pattern {pattern_name}: {e}")
            raise
    
    async def store_workflow(self, 
                            workflow_name: str,
                            workflow_data: Dict,
                            tags: List[str] = None,
                            ttl_seconds: int = None) -> str:
        """
        Store workflow information in shared memory.
        
        Args:
            workflow_name: Name of the workflow
            workflow_data: Workflow data to store
            tags: Optional tags for categorization
            ttl_seconds: Time to live in seconds
            
        Returns:
            str: Entry ID of the stored workflow
        """
        try:
            content = {
                "workflow_name": workflow_name,
                "workflow_data": workflow_data,
                "stored_by": self.agent_id,
                "domain": self.domain
            }
            
            entry_id = await self.context_manager.add_context(
                context_type=ContextType.WORKFLOW.value,
                content=content,
                agent_id=self.agent_id,
                ttl_seconds=ttl_seconds,
                tags=tags or [workflow_name, "workflow"]
            )
            
            # Update local cache
            self._cache_entry(ContextType.WORKFLOW.value, entry_id, content)
            
            self.performance_metrics["memory_operations"] += 1
            self.logger.debug(f"Workflow stored: {workflow_name} -> {entry_id}")
            
            return entry_id
            
        except Exception as e:
            self.logger.error(f"Error storing workflow {workflow_name}: {e}")
            raise
    
    async def store_intelligence(self, 
                               intelligence_type: str,
                               intelligence_data: Dict,
                               tags: List[str] = None,
                               ttl_seconds: int = None) -> str:
        """
        Store intelligence information in shared memory.
        
        Args:
            intelligence_type: Type of intelligence
            intelligence_data: Intelligence data to store
            tags: Optional tags for categorization
            ttl_seconds: Time to live in seconds
            
        Returns:
            str: Entry ID of the stored intelligence
        """
        try:
            content = {
                "intelligence_type": intelligence_type,
                "intelligence_data": intelligence_data,
                "stored_by": self.agent_id,
                "domain": self.domain
            }
            
            entry_id = await self.context_manager.add_context(
                context_type=ContextType.INTELLIGENCE.value,
                content=content,
                agent_id=self.agent_id,
                ttl_seconds=ttl_seconds,
                tags=tags or [intelligence_type, "intelligence"]
            )
            
            # Update local cache
            self._cache_entry(ContextType.INTELLIGENCE.value, entry_id, content)
            
            self.performance_metrics["memory_operations"] += 1
            self.logger.debug(f"Intelligence stored: {intelligence_type} -> {entry_id}")
            
            return entry_id
            
        except Exception as e:
            self.logger.error(f"Error storing intelligence {intelligence_type}: {e}")
            raise
    
    # Memory Retrieval Operations
    
    async def get_entities(self, 
                          entity_name: str = None,
                          tags: List[str] = None,
                          agent_id: str = None) -> List[Dict]:
        """
        Retrieve entity information from shared memory.
        
        Args:
            entity_name: Specific entity name to filter by
            tags: Tags to filter by
            agent_id: Agent ID to filter by
            
        Returns:
            List[Dict]: List of entity entries
        """
        try:
            start_time = datetime.now()
            
            # Check local cache first
            cache_key = f"entities_{entity_name}_{tags}_{agent_id}"
            cached_result = self._get_from_cache(cache_key)
            if cached_result:
                self.cache_hits += 1
                return cached_result
            
            self.cache_misses += 1
            
            # Get from shared context
            entities = await self.context_manager.get_context(
                context_type=ContextType.ENTITY.value,
                agent_id=agent_id,
                tags=tags
            )
            
            # Filter by entity name if specified
            if entity_name and entities:
                entities = [
                    entity for entity in entities
                    if entity.get("content", {}).get("entity_name") == entity_name
                ]
            
            # Cache the result
            self._cache_result(cache_key, entities)
            
            # Update performance metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            self._update_query_metrics(processing_time)
            
            self.logger.debug(f"Retrieved {len(entities or [])} entities")
            return entities or []
            
        except Exception as e:
            self.logger.error(f"Error getting entities: {e}")
            return []
    
    async def get_patterns(self, 
                          pattern_name: str = None,
                          tags: List[str] = None,
                          agent_id: str = None) -> List[Dict]:
        """
        Retrieve pattern information from shared memory.
        
        Args:
            pattern_name: Specific pattern name to filter by
            tags: Tags to filter by
            agent_id: Agent ID to filter by
            
        Returns:
            List[Dict]: List of pattern entries
        """
        try:
            start_time = datetime.now()
            
            # Check local cache first
            cache_key = f"patterns_{pattern_name}_{tags}_{agent_id}"
            cached_result = self._get_from_cache(cache_key)
            if cached_result:
                self.cache_hits += 1
                return cached_result
            
            self.cache_misses += 1
            
            # Get from shared context
            patterns = await self.context_manager.get_context(
                context_type=ContextType.PATTERN.value,
                agent_id=agent_id,
                tags=tags
            )
            
            # Filter by pattern name if specified
            if pattern_name and patterns:
                patterns = [
                    pattern for pattern in patterns
                    if pattern.get("content", {}).get("pattern_name") == pattern_name
                ]
            
            # Cache the result
            self._cache_result(cache_key, patterns)
            
            # Update performance metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            self._update_query_metrics(processing_time)
            
            self.logger.debug(f"Retrieved {len(patterns or [])} patterns")
            return patterns or []
            
        except Exception as e:
            self.logger.error(f"Error getting patterns: {e}")
            return []
    
    async def get_workflows(self, 
                           workflow_name: str = None,
                           tags: List[str] = None,
                           agent_id: str = None) -> List[Dict]:
        """
        Retrieve workflow information from shared memory.
        
        Args:
            workflow_name: Specific workflow name to filter by
            tags: Tags to filter by
            agent_id: Agent ID to filter by
            
        Returns:
            List[Dict]: List of workflow entries
        """
        try:
            start_time = datetime.now()
            
            # Check local cache first
            cache_key = f"workflows_{workflow_name}_{tags}_{agent_id}"
            cached_result = self._get_from_cache(cache_key)
            if cached_result:
                self.cache_hits += 1
                return cached_result
            
            self.cache_misses += 1
            
            # Get from shared context
            workflows = await self.context_manager.get_context(
                context_type=ContextType.WORKFLOW.value,
                agent_id=agent_id,
                tags=tags
            )
            
            # Filter by workflow name if specified
            if workflow_name and workflows:
                workflows = [
                    workflow for workflow in workflows
                    if workflow.get("content", {}).get("workflow_name") == workflow_name
                ]
            
            # Cache the result
            self._cache_result(cache_key, workflows)
            
            # Update performance metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            self._update_query_metrics(processing_time)
            
            self.logger.debug(f"Retrieved {len(workflows or [])} workflows")
            return workflows or []
            
        except Exception as e:
            self.logger.error(f"Error getting workflows: {e}")
            return []
    
    async def get_intelligence(self, 
                              intelligence_type: str = None,
                              tags: List[str] = None,
                              agent_id: str = None) -> List[Dict]:
        """
        Retrieve intelligence information from shared memory.
        
        Args:
            intelligence_type: Specific intelligence type to filter by
            tags: Tags to filter by
            agent_id: Agent ID to filter by
            
        Returns:
            List[Dict]: List of intelligence entries
        """
        try:
            start_time = datetime.now()
            
            # Check local cache first
            cache_key = f"intelligence_{intelligence_type}_{tags}_{agent_id}"
            cached_result = self._get_from_cache(cache_key)
            if cached_result:
                self.cache_hits += 1
                return cached_result
            
            self.cache_misses += 1
            
            # Get from shared context
            intelligence = await self.context_manager.get_context(
                context_type=ContextType.INTELLIGENCE.value,
                agent_id=agent_id,
                tags=tags
            )
            
            # Filter by intelligence type if specified
            if intelligence_type and intelligence:
                intelligence = [
                    intel for intel in intelligence
                    if intel.get("content", {}).get("intelligence_type") == intelligence_type
                ]
            
            # Cache the result
            self._cache_result(cache_key, intelligence)
            
            # Update performance metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            self._update_query_metrics(processing_time)
            
            self.logger.debug(f"Retrieved {len(intelligence or [])} intelligence entries")
            return intelligence or []
            
        except Exception as e:
            self.logger.error(f"Error getting intelligence: {e}")
            return []
    
    # Search and Query Operations
    
    async def search_memory(self, 
                           search_terms: List[str],
                           context_types: List[str] = None,
                           tags: List[str] = None) -> MemoryResult:
        """
        Search across all memory types for specific terms.
        
        Args:
            search_terms: Terms to search for
            context_types: Context types to search in (if None, search all)
            tags: Tags to filter by
            
        Returns:
            MemoryResult: Search results
        """
        start_time = datetime.now()
        query_id = self._generate_query_id()
        
        try:
            search_results = []
            
            # Default context types if not specified
            if not context_types:
                context_types = [ct.value for ct in ContextType]
            
            # Search each context type
            for context_type in context_types:
                entries = await self.context_manager.get_context(
                    context_type=context_type,
                    tags=tags
                )
                
                if entries:
                    # Filter entries that contain search terms
                    for entry in entries:
                        content_str = json.dumps(entry.get("content", {})).lower()
                        if any(term.lower() in content_str for term in search_terms):
                            search_results.append(entry)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            result = MemoryResult(
                query_id=query_id,
                success=True,
                data=search_results,
                metadata={
                    "search_terms": search_terms,
                    "context_types_searched": context_types,
                    "total_results": len(search_results)
                },
                processing_time=processing_time
            )
            
            # Track query
            self._track_query(query_id, QueryType.SEARCH, context_types, {"search_terms": search_terms})
            self._update_query_metrics(processing_time)
            
            self.logger.debug(f"Search completed: {len(search_results)} results for terms {search_terms}")
            return result
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Error searching memory: {e}")
            
            return MemoryResult(
                query_id=query_id,
                success=False,
                data=[],
                metadata={"search_terms": search_terms},
                processing_time=processing_time,
                error_message=str(e)
            )
    
    async def get_recent_entries(self, 
                                context_type: str = None,
                                limit: int = 10,
                                hours: int = 24) -> List[Dict]:
        """
        Get recent entries from memory.
        
        Args:
            context_type: Specific context type (if None, get from all types)
            limit: Maximum number of entries to return
            hours: Number of hours to look back
            
        Returns:
            List[Dict]: Recent entries sorted by timestamp
        """
        try:
            start_time = datetime.now()
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            all_entries = []
            
            # Determine context types to check
            context_types = [context_type] if context_type else [ct.value for ct in ContextType]
            
            # Get entries from each context type
            for ct in context_types:
                entries = await self.context_manager.get_context(context_type=ct)
                if entries:
                    all_entries.extend(entries)
            
            # Filter by recency and sort
            recent_entries = []
            for entry in all_entries:
                try:
                    entry_time = datetime.fromisoformat(entry["timestamp"])
                    if entry_time >= cutoff_time:
                        recent_entries.append(entry)
                except (KeyError, ValueError):
                    continue
            
            # Sort by timestamp (most recent first) and limit
            recent_entries.sort(key=lambda x: x["timestamp"], reverse=True)
            recent_entries = recent_entries[:limit]
            
            # Update performance metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            self._update_query_metrics(processing_time)
            
            self.logger.debug(f"Retrieved {len(recent_entries)} recent entries")
            return recent_entries
            
        except Exception as e:
            self.logger.error(f"Error getting recent entries: {e}")
            return []
    
    # Update Operations
    
    async def update_entry(self, 
                          context_type: str,
                          entry_id: str,
                          updates: Dict,
                          merge: bool = True) -> bool:
        """
        Update an existing memory entry.
        
        Args:
            context_type: Type of context
            entry_id: ID of the entry to update
            updates: Update data
            merge: Whether to merge with existing content or replace
            
        Returns:
            bool: True if update successful
        """
        try:
            success = await self.context_manager.update_context(
                context_type=context_type,
                entry_id=entry_id,
                content=updates,
                agent_id=self.agent_id,
                merge=merge
            )
            
            if success:
                # Invalidate local cache for this entry
                self._invalidate_cache_entry(context_type, entry_id)
                self.performance_metrics["memory_operations"] += 1
                self.logger.debug(f"Entry updated: {context_type}/{entry_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error updating entry {context_type}/{entry_id}: {e}")
            return False
    
    async def delete_entry(self, 
                          context_type: str,
                          entry_id: str) -> bool:
        """
        Delete a memory entry.
        
        Args:
            context_type: Type of context
            entry_id: ID of the entry to delete
            
        Returns:
            bool: True if deletion successful
        """
        try:
            success = await self.context_manager.delete_context(
                context_type=context_type,
                entry_id=entry_id,
                agent_id=self.agent_id
            )
            
            if success:
                # Invalidate local cache for this entry
                self._invalidate_cache_entry(context_type, entry_id)
                self.performance_metrics["memory_operations"] += 1
                self.logger.debug(f"Entry deleted: {context_type}/{entry_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error deleting entry {context_type}/{entry_id}: {e}")
            return False
    
    # Subscription and Notification Operations
    
    async def subscribe_to_updates(self, 
                                  context_types: List[str],
                                  callback: Callable = None) -> bool:
        """
        Subscribe to updates for specific context types.
        
        Args:
            context_types: List of context types to subscribe to
            callback: Optional callback function for updates
            
        Returns:
            bool: True if subscription successful
        """
        try:
            # Use default callback if none provided
            if not callback:
                callback = self._default_update_callback
            
            success = await self.context_manager.subscribe_to_updates(
                agent_id=self.agent_id,
                context_types=context_types,
                callback=callback
            )
            
            if success:
                self.active_subscriptions.extend(context_types)
                self.active_subscriptions = list(set(self.active_subscriptions))  # Remove duplicates
                self.logger.info(f"Subscribed to updates for: {context_types}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error subscribing to updates: {e}")
            return False
    
    async def unsubscribe_from_updates(self, 
                                     context_types: List[str] = None) -> bool:
        """
        Unsubscribe from updates.
        
        Args:
            context_types: List of context types to unsubscribe from (if None, unsubscribe from all)
            
        Returns:
            bool: True if unsubscription successful
        """
        try:
            success = await self.context_manager.unsubscribe_from_updates(
                agent_id=self.agent_id,
                context_types=context_types
            )
            
            if success:
                if context_types:
                    self.active_subscriptions = [
                        sub for sub in self.active_subscriptions if sub not in context_types
                    ]
                else:
                    self.active_subscriptions = []
                self.logger.info(f"Unsubscribed from updates for: {context_types or 'all'}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error unsubscribing from updates: {e}")
            return False
    
    async def _default_update_callback(self, update: ContextUpdate):
        """Default callback for context updates."""
        try:
            self.logger.info(f"Received update: {update.update_type} for {update.context_type} by {update.agent_id}")
            
            # Invalidate relevant cache entries
            self._invalidate_cache_for_context_type(update.context_type)
            
        except Exception as e:
            self.logger.error(f"Error in update callback: {e}")
    
    # Cache Management
    
    def _get_from_cache(self, cache_key: str) -> Optional[Any]:
        """Get entry from local cache."""
        if cache_key in self.local_cache:
            entry = self.local_cache[cache_key]
            # Check if cache entry is still valid
            if datetime.now() - entry["timestamp"] < self.cache_ttl:
                return entry["data"]
            else:
                # Remove expired entry
                del self.local_cache[cache_key]
        
        return None
    
    def _cache_result(self, cache_key: str, data: Any):
        """Cache a result."""
        self.local_cache[cache_key] = {
            "data": data,
            "timestamp": datetime.now()
        }
        
        # Limit cache size
        if len(self.local_cache) > 1000:
            # Remove oldest entries
            oldest_keys = sorted(
                self.local_cache.keys(),
                key=lambda k: self.local_cache[k]["timestamp"]
            )[:100]
            
            for key in oldest_keys:
                del self.local_cache[key]
    
    def _cache_entry(self, context_type: str, entry_id: str, content: Dict):
        """Cache a specific entry."""
        cache_key = f"entry_{context_type}_{entry_id}"
        self._cache_result(cache_key, content)
    
    def _invalidate_cache_entry(self, context_type: str, entry_id: str):
        """Invalidate cache for a specific entry."""
        cache_key = f"entry_{context_type}_{entry_id}"
        if cache_key in self.local_cache:
            del self.local_cache[cache_key]
    
    def _invalidate_cache_for_context_type(self, context_type: str):
        """Invalidate all cache entries for a context type."""
        keys_to_remove = [
            key for key in self.local_cache.keys()
            if context_type in key
        ]
        
        for key in keys_to_remove:
            del self.local_cache[key]
    
    def clear_cache(self):
        """Clear all cached data."""
        self.local_cache.clear()
        self.logger.debug("Local cache cleared")
    
    # Performance and Metrics
    
    def _track_query(self, 
                    query_id: str,
                    query_type: QueryType,
                    context_types: List[str],
                    filters: Dict):
        """Track a query for analytics."""
        query = MemoryQuery(
            query_id=query_id,
            agent_id=self.agent_id,
            query_type=query_type.value,
            context_types=context_types,
            filters=filters,
            timestamp=datetime.now()
        )
        
        self.query_history.append(query)
        
        # Limit history size
        if len(self.query_history) > 1000:
            self.query_history = self.query_history[-1000:]
    
    def _update_query_metrics(self, processing_time: float):
        """Update query performance metrics."""
        self.performance_metrics["queries_executed"] += 1
        
        # Update average query time
        current_avg = self.performance_metrics["average_query_time"]
        query_count = self.performance_metrics["queries_executed"]
        
        new_avg = ((current_avg * (query_count - 1)) + processing_time) / query_count
        self.performance_metrics["average_query_time"] = new_avg
        
        # Update cache hit rate
        total_cache_attempts = self.cache_hits + self.cache_misses
        if total_cache_attempts > 0:
            self.performance_metrics["cache_hit_rate"] = self.cache_hits / total_cache_attempts
    
    def _generate_query_id(self) -> str:
        """Generate a unique query ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"query_{self.agent_id}_{timestamp}"
    
    # Status and Information
    
    def get_memory_statistics(self) -> Dict:
        """Get memory interface statistics."""
        context_stats = self.context_manager.get_context_statistics()
        
        return {
            "agent_info": {
                "agent_id": self.agent_id,
                "agent_type": self.agent_type,
                "domain": self.domain,
                "capabilities": self.capabilities
            },
            "performance_metrics": self.performance_metrics,
            "cache_statistics": {
                "cache_size": len(self.local_cache),
                "cache_hits": self.cache_hits,
                "cache_misses": self.cache_misses,
                "cache_hit_rate": self.performance_metrics["cache_hit_rate"]
            },
            "subscriptions": {
                "active_subscriptions": self.active_subscriptions,
                "subscription_count": len(self.active_subscriptions)
            },
            "query_history": {
                "total_queries": len(self.query_history),
                "recent_queries": len([q for q in self.query_history if datetime.now() - q.timestamp < timedelta(hours=1)])
            },
            "shared_context": context_stats
        }
    
    def get_agent_status(self) -> Dict:
        """Get current agent status."""
        return self.context_manager.get_agent_status(self.agent_id)

# Main execution and testing
if __name__ == "__main__":
    async def test_agent_memory_interface():
        """Test the Agent Memory Interface."""
        print("Testing Agent Memory Interface...")
        
        # Initialize memory interface
        interface = AgentMemoryInterface(
            agent_id="test-agent",
            agent_type="domain_specialist",
            domain="producer_portal",
            capabilities=["entity_management", "pattern_recognition"]
        )
        
        # Connect to shared context
        await interface.connect(subscriptions=["entity", "pattern", "workflow"])
        
        # Test entity storage
        entity_id = await interface.store_entity(
            entity_name="driver",
            entity_data={
                "fields": ["driver_id", "license_number", "first_name", "last_name"],
                "relationships": ["address", "phone", "email"],
                "validation_rules": ["required", "unique"]
            },
            tags=["driver", "entity_definition"]
        )
        print(f"Stored entity: {entity_id}")
        
        # Test pattern storage
        pattern_id = await interface.store_pattern(
            pattern_name="driver_validation",
            pattern_data={
                "validation_steps": ["license_check", "age_validation", "mvr_check"],
                "external_services": ["dcs_integration"],
                "error_handling": ["retry", "fallback"]
            },
            tags=["driver", "validation", "pattern"]
        )
        print(f"Stored pattern: {pattern_id}")
        
        # Test retrieval
        entities = await interface.get_entities(entity_name="driver")
        print(f"Retrieved {len(entities)} driver entities")
        
        patterns = await interface.get_patterns(pattern_name="driver_validation")
        print(f"Retrieved {len(patterns)} driver validation patterns")
        
        # Test search
        search_result = await interface.search_memory(
            search_terms=["driver", "validation"],
            context_types=["entity", "pattern"]
        )
        print(f"Search results: {search_result.metadata}")
        
        # Test recent entries
        recent = await interface.get_recent_entries(limit=5, hours=1)
        print(f"Retrieved {len(recent)} recent entries")
        
        # Test statistics
        stats = interface.get_memory_statistics()
        print(f"Memory Statistics: {json.dumps(stats, indent=2, default=str)}")
        
        # Disconnect
        await interface.disconnect()
        
        return interface
    
    # Run test if executed directly
    import asyncio
    asyncio.run(test_agent_memory_interface())