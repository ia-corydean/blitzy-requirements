#!/usr/bin/env python3
"""
Entity Extraction Engine for Automatic Entity Discovery

This engine automatically identifies and extracts business entities from
requirement specifications, classifying them according to the universal
entity catalog and discovering new entity patterns.

Features:
- Natural language entity extraction
- Entity type classification
- Relationship detection
- Cross-domain entity mapping
- New entity discovery
"""

import json
import logging
import re
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EntityType(Enum):
    """Types of entities in the system"""
    CORE_BUSINESS = "core_business"  # driver, vehicle, quote, policy
    REFERENCE = "reference"  # driver_type, vehicle_type
    RELATIONSHIP = "relationship"  # map_driver_vehicle
    EXTERNAL = "external"  # DCS entities, external APIs
    SUPPORTING = "supporting"  # address, phone, email
    TRANSACTIONAL = "transactional"  # payment, commission
    COMPLIANCE = "compliance"  # SR22, reinstatement
    CONFIGURATION = "configuration"  # rate_factor, program_trait


@dataclass
class ExtractedEntity:
    """Represents an extracted entity"""
    name: str
    type: EntityType
    confidence: float
    context: str
    attributes: List[str] = field(default_factory=list)
    relationships: List[Dict[str, str]] = field(default_factory=list)
    domain_specific: bool = False
    global_requirement: Optional[str] = None
    source_text: str = ""
    metadata: Dict = field(default_factory=dict)


@dataclass
class EntityRelationship:
    """Represents a relationship between entities"""
    source_entity: str
    target_entity: str
    relationship_type: str
    cardinality: str
    confidence: float
    context: str


class EntityExtractionEngine:
    """
    Engine for automatic entity extraction and classification
    from requirement specifications
    """
    
    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.entity_catalog = {}
        self.entity_patterns = {}
        self.relationship_patterns = {}
        self.domain_mappings = {}
        self.extraction_rules = {}
        self.load_knowledge_base()
        self._initialize_extraction_patterns()
    
    def load_knowledge_base(self):
        """Load entity catalog and patterns from knowledge base"""
        try:
            # Load universal entity catalog
            entity_catalog_path = self.knowledge_base_path / "universal-entity-catalog.json"
            if entity_catalog_path.exists():
                with open(entity_catalog_path, 'r') as f:
                    catalog_data = json.load(f)
                    self.entity_catalog = catalog_data.get('entities', {})
                    logger.info(f"Loaded {len(self.entity_catalog)} entities from catalog")
            
            # Load entity patterns
            patterns_dir = self.knowledge_base_path / "global-patterns/universal-entities"
            if patterns_dir.exists():
                for pattern_file in patterns_dir.glob("*.json"):
                    with open(pattern_file, 'r') as f:
                        pattern = json.load(f)
                        entity_name = pattern_file.stem
                        self.entity_patterns[entity_name] = pattern
                logger.info(f"Loaded {len(self.entity_patterns)} entity patterns")
            
            # Load relationship map
            relationships_path = self.knowledge_base_path / "cross-domain-relationships/relationship-map.json"
            if relationships_path.exists():
                with open(relationships_path, 'r') as f:
                    relationship_data = json.load(f)
                    self.relationship_patterns = relationship_data.get('relationships', [])
                    logger.info(f"Loaded {len(self.relationship_patterns)} relationship patterns")
            
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
    
    def _initialize_extraction_patterns(self):
        """Initialize regex patterns for entity extraction"""
        
        # Entity name patterns
        self.entity_name_patterns = [
            # Table references
            (r'\btable[s]?\s+[`"]?(\w+)[`"]?', 1.0),
            (r'\bfrom\s+[`"]?(\w+)[`"]?', 0.9),
            (r'\bjoin\s+[`"]?(\w+)[`"]?', 0.9),
            
            # Entity mentions
            (r'\b(\w+)\s+entity\b', 0.8),
            (r'\bentity\s+(\w+)\b', 0.8),
            (r'\b(\w+)\s+record[s]?\b', 0.7),
            (r'\b(\w+)\s+object[s]?\b', 0.7),
            
            # Business objects
            (r'\b(driver|vehicle|quote|policy|payment|claim)\b', 0.95),
            (r'\b(customer|producer|agent|insured)\b', 0.9),
            (r'\b(address|phone|email)\b', 0.85),
            
            # Data references
            (r'\b(\w+)\.id\b', 0.6),
            (r'\b(\w+)_id\b', 0.7),
            (r'\bget\s+(\w+)\b', 0.5),
            (r'\bcreate\s+(\w+)\b', 0.7),
            (r'\bupdate\s+(\w+)\b', 0.7),
        ]
        
        # Attribute patterns
        self.attribute_patterns = [
            (r'\b(\w+)\s+field[s]?\b', 0.8),
            (r'\b(\w+)\s+attribute[s]?\b', 0.8),
            (r'\b(\w+)\s+propert(?:y|ies)\b', 0.8),
            (r'\b(\w+):\s*\w+', 0.6),  # attribute: type
            (r'\.(\w+)\b', 0.5),  # entity.attribute
        ]
        
        # Relationship patterns
        self.relationship_patterns_regex = [
            (r'\b(\w+)\s+has\s+(?:many\s+)?(\w+)\b', 'has_many'),
            (r'\b(\w+)\s+belongs\s+to\s+(\w+)\b', 'belongs_to'),
            (r'\b(\w+)\s+(?:is\s+)?associated\s+with\s+(\w+)\b', 'associated_with'),
            (r'\bmap_(\w+)_(\w+)\b', 'many_to_many'),
            (r'\b(\w+)_(\w+)_map\b', 'many_to_many'),
            (r'\b(\w+)\s+references\s+(\w+)\b', 'references'),
            (r'\bforeign\s+key\s+to\s+(\w+)\b', 'foreign_key'),
        ]
        
        # Domain indicators
        self.domain_indicators = {
            'producer-portal': ['quote', 'producer', 'portal', 'submission'],
            'accounting': ['billing', 'payment', 'commission', 'invoice', 'ACH'],
            'program-manager': ['rate', 'factor', 'underwriting', 'rule'],
            'program-traits': ['program', 'trait', 'aguila', 'dorada'],
            'entity-integration': ['DCS', 'external', 'API', 'integration'],
            'reinstatement': ['reinstate', 'lapse', 'policy', 'lifecycle'],
            'sr22': ['SR22', 'SR26', 'financial', 'responsibility', 'filing']
        }
    
    def extract_entities(self, requirement_text: str, 
                        context: Optional[Dict] = None) -> List[ExtractedEntity]:
        """
        Extract entities from requirement text
        
        Args:
            requirement_text: Text to extract entities from
            context: Additional context (domain, type, etc.)
            
        Returns:
            List of extracted entities
        """
        extracted_entities = []
        seen_entities = set()
        
        # Normalize text
        normalized_text = requirement_text.lower()
        
        # Extract using patterns
        for pattern, confidence in self.entity_name_patterns:
            matches = re.finditer(pattern, normalized_text, re.IGNORECASE)
            for match in matches:
                entity_name = match.group(1).lower()
                
                # Skip if already extracted with higher confidence
                if entity_name in seen_entities:
                    continue
                
                # Classify entity
                entity_type = self._classify_entity(entity_name, normalized_text, context)
                
                # Extract attributes
                attributes = self._extract_attributes(entity_name, requirement_text)
                
                # Detect relationships
                relationships = self._detect_relationships(entity_name, normalized_text)
                
                # Check domain specificity
                domain_specific = self._is_domain_specific(entity_name, context)
                
                # Map to global requirement
                global_req = self._map_to_global_requirement(entity_name, entity_type)
                
                entity = ExtractedEntity(
                    name=entity_name,
                    type=entity_type,
                    confidence=confidence * self._calculate_context_boost(entity_name, context),
                    context=match.group(0),
                    attributes=attributes,
                    relationships=relationships,
                    domain_specific=domain_specific,
                    global_requirement=global_req,
                    source_text=requirement_text[max(0, match.start()-50):min(len(requirement_text), match.end()+50)],
                    metadata={'match_pattern': pattern}
                )
                
                extracted_entities.append(entity)
                seen_entities.add(entity_name)
        
        # Post-process and validate
        extracted_entities = self._validate_entities(extracted_entities)
        
        # Sort by confidence
        extracted_entities.sort(key=lambda e: e.confidence, reverse=True)
        
        return extracted_entities
    
    def _classify_entity(self, entity_name: str, text: str, context: Optional[Dict]) -> EntityType:
        """Classify entity into appropriate type"""
        
        # Check against known catalog
        if entity_name in self.entity_catalog:
            catalog_type = self.entity_catalog[entity_name].get('type', '')
            return self._map_catalog_type_to_enum(catalog_type)
        
        # Check patterns
        if entity_name in self.entity_patterns:
            pattern_type = self.entity_patterns[entity_name].get('entity_type', '')
            return self._map_catalog_type_to_enum(pattern_type)
        
        # Pattern-based classification
        if re.match(r'^map_\w+_\w+$', entity_name) or entity_name.endswith('_map'):
            return EntityType.RELATIONSHIP
        
        if entity_name in ['driver', 'vehicle', 'quote', 'policy', 'customer', 'producer']:
            return EntityType.CORE_BUSINESS
        
        if entity_name.endswith('_type') or entity_name.endswith('_status'):
            return EntityType.REFERENCE
        
        if entity_name in ['payment', 'commission', 'transaction', 'refund']:
            return EntityType.TRANSACTIONAL
        
        if entity_name in ['address', 'phone', 'email', 'name']:
            return EntityType.SUPPORTING
        
        if 'external' in text.lower() or 'api' in text.lower():
            return EntityType.EXTERNAL
        
        if entity_name in ['sr22', 'sr26', 'reinstatement']:
            return EntityType.COMPLIANCE
        
        if entity_name.endswith('_config') or 'configuration' in text.lower():
            return EntityType.CONFIGURATION
        
        # Default to core business
        return EntityType.CORE_BUSINESS
    
    def _map_catalog_type_to_enum(self, catalog_type: str) -> EntityType:
        """Map catalog type string to EntityType enum"""
        type_mapping = {
            'core': EntityType.CORE_BUSINESS,
            'reference': EntityType.REFERENCE,
            'relationship': EntityType.RELATIONSHIP,
            'external': EntityType.EXTERNAL,
            'supporting': EntityType.SUPPORTING,
            'transactional': EntityType.TRANSACTIONAL,
            'compliance': EntityType.COMPLIANCE,
            'configuration': EntityType.CONFIGURATION
        }
        
        return type_mapping.get(catalog_type.lower(), EntityType.CORE_BUSINESS)
    
    def _extract_attributes(self, entity_name: str, text: str) -> List[str]:
        """Extract attributes for an entity"""
        attributes = []
        
        # Check entity patterns
        if entity_name in self.entity_patterns:
            pattern_attrs = self.entity_patterns[entity_name].get('attributes', [])
            attributes.extend(pattern_attrs)
        
        # Look for attribute patterns near entity mentions
        entity_positions = [m.start() for m in re.finditer(rf'\b{entity_name}\b', text.lower())]
        
        for pos in entity_positions:
            # Check surrounding text
            context_start = max(0, pos - 100)
            context_end = min(len(text), pos + 100)
            context = text[context_start:context_end]
            
            # Look for attributes
            for pattern, _ in self.attribute_patterns:
                matches = re.finditer(pattern, context, re.IGNORECASE)
                for match in matches:
                    attr = match.group(1).lower()
                    if attr not in attributes and attr != entity_name:
                        attributes.append(attr)
        
        # Add common attributes based on entity type
        if entity_name == 'driver':
            common_attrs = ['name_id', 'date_of_birth', 'license_number']
            attributes.extend([attr for attr in common_attrs if attr not in attributes])
        elif entity_name == 'vehicle':
            common_attrs = ['vin', 'make', 'model', 'year']
            attributes.extend([attr for attr in common_attrs if attr not in attributes])
        
        return attributes[:10]  # Limit to top 10 attributes
    
    def _detect_relationships(self, entity_name: str, text: str) -> List[Dict[str, str]]:
        """Detect relationships for an entity"""
        relationships = []
        
        # Check known relationships
        for rel in self.relationship_patterns:
            if rel.get('source_entity') == entity_name:
                relationships.append({
                    'target': rel.get('target_entity'),
                    'type': rel.get('relationship_type'),
                    'cardinality': rel.get('cardinality', 'unknown')
                })
        
        # Pattern-based detection
        for pattern, rel_type in self.relationship_patterns_regex:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) >= 2:
                    entity1 = match.group(1).lower()
                    entity2 = match.group(2).lower() if len(match.groups()) >= 2 else None
                    
                    if entity1 == entity_name and entity2:
                        relationships.append({
                            'target': entity2,
                            'type': rel_type,
                            'cardinality': self._infer_cardinality(rel_type)
                        })
                    elif entity2 == entity_name:
                        relationships.append({
                            'target': entity1,
                            'type': self._reverse_relationship(rel_type),
                            'cardinality': self._infer_cardinality(rel_type, reverse=True)
                        })
        
        return relationships
    
    def _infer_cardinality(self, relationship_type: str, reverse: bool = False) -> str:
        """Infer cardinality from relationship type"""
        cardinality_map = {
            'has_many': 'one-to-many',
            'belongs_to': 'many-to-one',
            'has_one': 'one-to-one',
            'many_to_many': 'many-to-many',
            'references': 'many-to-one',
            'foreign_key': 'many-to-one'
        }
        
        cardinality = cardinality_map.get(relationship_type, 'unknown')
        
        if reverse and cardinality != 'unknown':
            # Reverse the cardinality
            if cardinality == 'one-to-many':
                return 'many-to-one'
            elif cardinality == 'many-to-one':
                return 'one-to-many'
        
        return cardinality
    
    def _reverse_relationship(self, relationship_type: str) -> str:
        """Get reverse of a relationship type"""
        reverse_map = {
            'has_many': 'belongs_to',
            'belongs_to': 'has_many',
            'has_one': 'belongs_to',
            'references': 'referenced_by',
            'foreign_key': 'primary_key_for'
        }
        
        return reverse_map.get(relationship_type, relationship_type)
    
    def _is_domain_specific(self, entity_name: str, context: Optional[Dict]) -> bool:
        """Check if entity is domain-specific"""
        if not context or 'domain' not in context:
            return False
        
        domain = context['domain']
        
        # Check domain indicators
        for dom, indicators in self.domain_indicators.items():
            if dom == domain:
                for indicator in indicators:
                    if indicator.lower() in entity_name:
                        return True
        
        # Check catalog
        if entity_name in self.entity_catalog:
            domains = self.entity_catalog[entity_name].get('domains', [])
            return len(domains) == 1 and domain in domains
        
        return False
    
    def _map_to_global_requirement(self, entity_name: str, entity_type: EntityType) -> Optional[str]:
        """Map entity to relevant Global Requirement"""
        
        # Direct mappings
        gr_mappings = {
            EntityType.EXTERNAL: 'GR-52',  # Universal Entity Management
            EntityType.COMPLIANCE: 'GR-10' if 'sr22' in entity_name else 'GR-64',
            EntityType.TRANSACTIONAL: 'GR-44',  # Communication Architecture
            EntityType.CONFIGURATION: 'GR-38'  # Microservice Architecture
        }
        
        if entity_type in gr_mappings:
            return gr_mappings[entity_type]
        
        # Check catalog
        if entity_name in self.entity_catalog:
            return self.entity_catalog[entity_name].get('global_requirement')
        
        # Default core entities to GR-52
        if entity_type == EntityType.CORE_BUSINESS:
            return 'GR-52'
        
        return None
    
    def _calculate_context_boost(self, entity_name: str, context: Optional[Dict]) -> float:
        """Calculate confidence boost based on context"""
        boost = 1.0
        
        if not context:
            return boost
        
        # Boost if in expected domain
        if 'domain' in context:
            domain = context['domain']
            for dom, indicators in self.domain_indicators.items():
                if dom == domain:
                    for indicator in indicators:
                        if indicator.lower() in entity_name:
                            boost *= 1.2
                            break
        
        # Boost if matches expected type
        if 'expected_entities' in context:
            if entity_name in context['expected_entities']:
                boost *= 1.5
        
        # Boost if in catalog
        if entity_name in self.entity_catalog:
            boost *= 1.3
        
        return min(boost, 2.0)  # Cap at 2x boost
    
    def _validate_entities(self, entities: List[ExtractedEntity]) -> List[ExtractedEntity]:
        """Validate and clean extracted entities"""
        validated = []
        
        for entity in entities:
            # Skip common false positives
            if entity.name in ['the', 'a', 'an', 'and', 'or', 'for', 'from', 'with']:
                continue
            
            # Skip if too short
            if len(entity.name) < 3:
                continue
            
            # Skip if all numbers
            if entity.name.isdigit():
                continue
            
            # Boost confidence if in catalog
            if entity.name in self.entity_catalog:
                entity.confidence = min(entity.confidence * 1.2, 1.0)
            
            validated.append(entity)
        
        return validated
    
    def extract_entity_relationships(self, entities: List[ExtractedEntity], 
                                   requirement_text: str) -> List[EntityRelationship]:
        """
        Extract relationships between identified entities
        
        Args:
            entities: List of extracted entities
            requirement_text: Original requirement text
            
        Returns:
            List of entity relationships
        """
        relationships = []
        entity_names = {e.name for e in entities}
        
        # Check each entity's detected relationships
        for entity in entities:
            for rel in entity.relationships:
                target = rel.get('target')
                if target in entity_names:
                    relationship = EntityRelationship(
                        source_entity=entity.name,
                        target_entity=target,
                        relationship_type=rel.get('type', 'unknown'),
                        cardinality=rel.get('cardinality', 'unknown'),
                        confidence=entity.confidence * 0.8,  # Slightly lower than entity confidence
                        context=f"{entity.name} {rel.get('type', 'relates to')} {target}"
                    )
                    relationships.append(relationship)
        
        # Look for additional relationship patterns
        for pattern, rel_type in self.relationship_patterns_regex:
            matches = re.finditer(pattern, requirement_text, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) >= 2:
                    entity1 = match.group(1).lower()
                    entity2 = match.group(2).lower()
                    
                    if entity1 in entity_names and entity2 in entity_names:
                        # Check if already found
                        exists = any(
                            r.source_entity == entity1 and r.target_entity == entity2
                            for r in relationships
                        )
                        
                        if not exists:
                            relationship = EntityRelationship(
                                source_entity=entity1,
                                target_entity=entity2,
                                relationship_type=rel_type,
                                cardinality=self._infer_cardinality(rel_type),
                                confidence=0.7,
                                context=match.group(0)
                            )
                            relationships.append(relationship)
        
        # Remove duplicates
        unique_relationships = []
        seen = set()
        
        for rel in relationships:
            key = (rel.source_entity, rel.target_entity, rel.relationship_type)
            if key not in seen:
                seen.add(key)
                unique_relationships.append(rel)
        
        return unique_relationships
    
    def discover_new_entities(self, entities: List[ExtractedEntity]) -> List[Dict]:
        """
        Identify potentially new entities not in the catalog
        
        Args:
            entities: List of extracted entities
            
        Returns:
            List of new entity candidates
        """
        new_entities = []
        
        for entity in entities:
            if entity.name not in self.entity_catalog and entity.confidence > 0.7:
                new_entity = {
                    'name': entity.name,
                    'type': entity.type.value,
                    'confidence': entity.confidence,
                    'attributes': entity.attributes,
                    'relationships': entity.relationships,
                    'domain_specific': entity.domain_specific,
                    'global_requirement': entity.global_requirement,
                    'discovery_context': entity.source_text,
                    'recommendation': self._generate_entity_recommendation(entity)
                }
                new_entities.append(new_entity)
        
        return new_entities
    
    def _generate_entity_recommendation(self, entity: ExtractedEntity) -> str:
        """Generate recommendation for new entity"""
        if entity.confidence > 0.9:
            return f"High confidence new entity '{entity.name}' - recommend adding to catalog"
        elif entity.confidence > 0.7:
            return f"Potential new entity '{entity.name}' - review for catalog inclusion"
        else:
            return f"Low confidence entity '{entity.name}' - further validation needed"
    
    def export_extraction_report(self, requirement_text: str, 
                               context: Optional[Dict] = None) -> Dict:
        """Generate comprehensive entity extraction report"""
        
        # Extract entities
        entities = self.extract_entities(requirement_text, context)
        
        # Extract relationships
        relationships = self.extract_entity_relationships(entities, requirement_text)
        
        # Discover new entities
        new_entities = self.discover_new_entities(entities)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'requirement_length': len(requirement_text),
            'context': context or {},
            'extracted_entities': [
                {
                    'name': e.name,
                    'type': e.type.value,
                    'confidence': e.confidence,
                    'attributes': e.attributes,
                    'relationships': e.relationships,
                    'domain_specific': e.domain_specific,
                    'global_requirement': e.global_requirement,
                    'context': e.context
                }
                for e in entities
            ],
            'entity_relationships': [
                {
                    'source': r.source_entity,
                    'target': r.target_entity,
                    'type': r.relationship_type,
                    'cardinality': r.cardinality,
                    'confidence': r.confidence
                }
                for r in relationships
            ],
            'new_entity_candidates': new_entities,
            'statistics': {
                'total_entities': len(entities),
                'unique_entities': len(set(e.name for e in entities)),
                'total_relationships': len(relationships),
                'entity_types': {
                    entity_type.value: sum(1 for e in entities if e.type == entity_type)
                    for entity_type in EntityType
                },
                'average_confidence': sum(e.confidence for e in entities) / len(entities) if entities else 0,
                'new_entities_discovered': len(new_entities)
            }
        }
        
        return report


# Example usage and testing
if __name__ == "__main__":
    # Initialize engine
    engine = EntityExtractionEngine("/app/workspace/requirements/shared-infrastructure/knowledge-base")
    
    # Example requirement text
    requirement_text = """
    Create a new requirement for updating driver information in the quote process.
    
    The system needs to get driver.* from driver table
    -> join name on driver.name_id = name.id
    -> join driver_type on driver.driver_type_id = driver_type.id
    -> get vehicle records associated with the driver through map_driver_vehicle
    
    The driver entity has many vehicles and belongs to a quote. Each driver must have
    a valid license and pass age verification. The driver's address and phone information
    should be stored in separate tables with proper foreign key relationships.
    
    This integrates with the DCS API for driver verification and updates the quote
    calculation based on driver risk factors. Payment information is processed through
    the accounting system.
    
    Global Requirements: GR-52 (Universal Entity Management), GR-44 (Communication)
    """
    
    context = {
        'domain': 'producer-portal',
        'requirement_type': 'entity_update',
        'expected_entities': ['driver', 'vehicle', 'quote']
    }
    
    # Extract entities
    print("Extracting entities...")
    entities = engine.extract_entities(requirement_text, context)
    
    print(f"\nFound {len(entities)} entities:")
    for entity in entities[:10]:  # Show top 10
        print(f"\n- {entity.name} ({entity.type.value})")
        print(f"  Confidence: {entity.confidence:.2f}")
        print(f"  Attributes: {', '.join(entity.attributes[:5])}")
        if entity.relationships:
            print(f"  Relationships: {entity.relationships[0]}")
        if entity.global_requirement:
            print(f"  Global Requirement: {entity.global_requirement}")
    
    # Extract relationships
    print("\n\nExtracting relationships...")
    relationships = engine.extract_entity_relationships(entities, requirement_text)
    
    print(f"\nFound {len(relationships)} relationships:")
    for rel in relationships[:5]:  # Show top 5
        print(f"- {rel.source_entity} {rel.relationship_type} {rel.target_entity} ({rel.cardinality})")
    
    # Discover new entities
    print("\n\nChecking for new entities...")
    new_entities = engine.discover_new_entities(entities)
    
    if new_entities:
        print(f"\nDiscovered {len(new_entities)} potential new entities:")
        for new_entity in new_entities:
            print(f"- {new_entity['name']}: {new_entity['recommendation']}")
    
    # Generate report
    print("\n\nGenerating extraction report...")
    report = engine.export_extraction_report(requirement_text, context)
    print(f"\nReport Statistics:")
    print(f"- Total entities: {report['statistics']['total_entities']}")
    print(f"- Unique entities: {report['statistics']['unique_entities']}")
    print(f"- Total relationships: {report['statistics']['total_relationships']}")
    print(f"- Average confidence: {report['statistics']['average_confidence']:.2f}")