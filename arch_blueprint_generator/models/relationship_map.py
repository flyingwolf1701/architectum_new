"""
Relationship Map model for code representation.
"""

import json
import os
import networkx as nx
from typing import Dict, List, Set, Optional, Any, Union, Tuple, Iterator, TypeVar
import pickle
import copy

from arch_blueprint_generator.models.nodes import (
    Node, Relationship, NodeType, RelationshipType,
    FileNode, DirectoryNode, FunctionNode, ClassNode, MethodNode, FeatureNode,
    ContainsRelationship, CallsRelationship, ImportsRelationship, 
    InheritsRelationship, ImplementsRelationship
)
from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.errors.exceptions import ModelError
from arch_blueprint_generator.utils.logging import get_logger

logger = get_logger(__name__)

T = TypeVar('T', bound=Node)


class RelationshipMap:
    """
    Represents code as a network of nodes and relationships.
    
    The RelationshipMap is the central component for navigation, 
    representing code as a directed graph of nodes and relationships.
    """
    
    def __init__(self):
        """Initialize an empty relationship map."""
        self.graph = nx.DiGraph()
        self.nodes_by_type: Dict[NodeType, Dict[str, Node]] = {
            node_type: {} for node_type in NodeType
        }
        self.detail_level = DetailLevel.STANDARD
        logger.info("Initialized empty RelationshipMap")
    
    def add_node(self, node: Node) -> None:
        """
        Add a node to the relationship map.
        
        Args:
            node: The node to add
            
        Raises:
            ModelError: If a node with the same ID already exists
        """
        if node.id in self.graph:
            raise ModelError(f"Node with ID '{node.id}' already exists")
        
        self.graph.add_node(node.id, node=node)
        self.nodes_by_type[node.type][node.id] = node
        logger.debug(f"Added node: {node.id} ({node.type.value})")
    
    def add_relationship(self, relationship: Relationship) -> None:
        """
        Add a relationship to the relationship map.
        
        Args:
            relationship: The relationship to add
            
        Raises:
            ModelError: If the source or target node does not exist
        """
        if relationship.source_id not in self.graph:
            raise ModelError(f"Source node '{relationship.source_id}' does not exist")
        
        if relationship.target_id not in self.graph:
            raise ModelError(f"Target node '{relationship.target_id}' does not exist")
        
        self.graph.add_edge(
            relationship.source_id, 
            relationship.target_id, 
            relationship=relationship
        )
        logger.debug(
            f"Added relationship: {relationship.source_id} -> "
            f"{relationship.target_id} ({relationship.type.value})"
        )
    
    def get_node(self, node_id: str, detail_level: DetailLevel = DetailLevel.STANDARD) -> Optional[Node]:
        """
        Get a node by ID with the specified detail level.
        
        Args:
            node_id: The ID of the node to get
            detail_level: The level of detail to include
            
        Returns:
            The node, or None if not found
        """
        if node_id not in self.graph:
            return None
        
        node = self.graph.nodes[node_id]["node"]
        return self._apply_detail_level_to_node(node, detail_level)
    
    def get_nodes_by_type(self, node_type: NodeType, detail_level: DetailLevel = DetailLevel.STANDARD) -> List[Node]:
        """
        Get all nodes of a specific type with the specified detail level.
        
        Args:
            node_type: The type of nodes to get
            detail_level: The level of detail to include
            
        Returns:
            List of nodes of the specified type
        """
        nodes = list(self.nodes_by_type[node_type].values())
        return [self._apply_detail_level_to_node(node, detail_level) for node in nodes]
    
    def get_relationship(self, source_id: str, target_id: str, detail_level: DetailLevel = DetailLevel.STANDARD) -> Optional[Relationship]:
        """
        Get a relationship by source and target node IDs with the specified detail level.
        
        Args:
            source_id: The ID of the source node
            target_id: The ID of the target node
            detail_level: The level of detail to include
            
        Returns:
            The relationship, or None if not found
        """
        if not self.graph.has_edge(source_id, target_id):
            return None
        
        relationship = self.graph.edges[source_id, target_id]["relationship"]
        return self._apply_detail_level_to_relationship(relationship, detail_level)
    
    def get_outgoing_relationships(self, node_id: str, detail_level: DetailLevel = DetailLevel.STANDARD) -> List[Relationship]:
        """
        Get all outgoing relationships from a node with the specified detail level.
        
        Args:
            node_id: The ID of the node
            detail_level: The level of detail to include
            
        Returns:
            List of outgoing relationships
            
        Raises:
            ModelError: If the node does not exist
        """
        if node_id not in self.graph:
            raise ModelError(f"Node '{node_id}' does not exist")
        
        relationships = []
        for _, target_id in self.graph.out_edges(node_id):
            relationship = self.graph.edges[node_id, target_id]["relationship"]
            relationships.append(self._apply_detail_level_to_relationship(relationship, detail_level))
        
        return relationships
    
    def get_incoming_relationships(self, node_id: str, detail_level: DetailLevel = DetailLevel.STANDARD) -> List[Relationship]:
        """
        Get all incoming relationships to a node with the specified detail level.
        
        Args:
            node_id: The ID of the node
            detail_level: The level of detail to include
            
        Returns:
            List of incoming relationships
            
        Raises:
            ModelError: If the node does not exist
        """
        if node_id not in self.graph:
            raise ModelError(f"Node '{node_id}' does not exist")
        
        relationships = []
        for source_id, _ in self.graph.in_edges(node_id):
            relationship = self.graph.edges[source_id, node_id]["relationship"]
            relationships.append(self._apply_detail_level_to_relationship(relationship, detail_level))
        
        return relationships
    
    def get_relationships_by_type(self, relationship_type: RelationshipType, detail_level: DetailLevel = DetailLevel.STANDARD) -> List[Relationship]:
        """
        Get all relationships of a specific type with the specified detail level.
        
        Args:
            relationship_type: The type of relationships to get
            detail_level: The level of detail to include
            
        Returns:
            List of relationships of the specified type
        """
        relationships = []
        for source_id, target_id, data in self.graph.edges(data=True):
            relationship = data["relationship"]
            if relationship.type == relationship_type:
                relationships.append(self._apply_detail_level_to_relationship(relationship, detail_level))
        
        return relationships
    
    def remove_node(self, node_id: str) -> None:
        """
        Remove a node from the relationship map.
        
        Args:
            node_id: The ID of the node to remove
            
        Raises:
            ModelError: If the node does not exist
        """
        if node_id not in self.graph:
            raise ModelError(f"Node '{node_id}' does not exist")
        
        node = self.graph.nodes[node_id]["node"]
        self.graph.remove_node(node_id)
        del self.nodes_by_type[node.type][node_id]
        logger.debug(f"Removed node: {node_id}")
    
    def remove_relationship(self, source_id: str, target_id: str) -> None:
        """
        Remove a relationship from the relationship map.
        
        Args:
            source_id: The ID of the source node
            target_id: The ID of the target node
            
        Raises:
            ModelError: If the relationship does not exist
        """
        if not self.graph.has_edge(source_id, target_id):
            raise ModelError(f"Relationship from '{source_id}' to '{target_id}' does not exist")
        
        self.graph.remove_edge(source_id, target_id)
        logger.debug(f"Removed relationship: {source_id} -> {target_id}")
    
    def clear(self) -> None:
        """Clear the relationship map."""
        self.graph.clear()
        self.nodes_by_type = {node_type: {} for node_type in NodeType}
        logger.info("Cleared RelationshipMap")
    
    def node_count(self) -> int:
        """
        Get the number of nodes in the relationship map.
        
        Returns:
            Number of nodes
        """
        return self.graph.number_of_nodes()
    
    def relationship_count(self) -> int:
        """
        Get the number of relationships in the relationship map.
        
        Returns:
            Number of relationships
        """
        return self.graph.number_of_edges()
    
    def get_node_type_counts(self) -> Dict[NodeType, int]:
        """
        Get counts of nodes by type.
        
        Returns:
            Dictionary mapping node types to counts
        """
        return {node_type: len(nodes) for node_type, nodes in self.nodes_by_type.items()}
    
    def get_relationship_type_counts(self) -> Dict[RelationshipType, int]:
        """
        Get counts of relationships by type.
        
        Returns:
            Dictionary mapping relationship types to counts
        """
        counts: Dict[RelationshipType, int] = {relationship_type: 0 for relationship_type in RelationshipType}
        
        for _, _, data in self.graph.edges(data=True):
            relationship = data["relationship"]
            counts[relationship.type] += 1
        
        return counts
    
    def get_subgraph(self, node_ids: List[str], detail_level: DetailLevel = DetailLevel.STANDARD) -> 'RelationshipMap':
        """
        Create a subgraph containing specified nodes and their relationships with the specified detail level.
        
        Args:
            node_ids: IDs of nodes to include in the subgraph
            detail_level: The level of detail to include
            
        Returns:
            New RelationshipMap containing the subgraph
            
        Raises:
            ModelError: If any node does not exist
        """
        for node_id in node_ids:
            if node_id not in self.graph:
                raise ModelError(f"Node '{node_id}' does not exist")
        
        subgraph = RelationshipMap()
        
        # Add nodes with appropriate detail level
        for node_id in node_ids:
            node = self.graph.nodes[node_id]["node"]
            filtered_node = self._apply_detail_level_to_node(node, detail_level)
            subgraph.add_node(filtered_node)
        
        # Add relationships between nodes in the subgraph with appropriate detail level
        for source_id in node_ids:
            for target_id in node_ids:
                if self.graph.has_edge(source_id, target_id):
                    relationship = self.graph.edges[source_id, target_id]["relationship"]
                    filtered_relationship = self._apply_detail_level_to_relationship(relationship, detail_level)
                    subgraph.add_relationship(filtered_relationship)
        
        return subgraph
    
    def find_nodes(self, detail_level: DetailLevel = DetailLevel.STANDARD, **filters) -> List[Node]:
        """
        Find nodes matching specified filters with the specified detail level.
        
        Args:
            detail_level: The level of detail to include
            **filters: Attributes to filter by
            
        Returns:
            List of matching nodes
        """
        result = []
        
        node_type = filters.pop('type', None)
        nodes_to_check = []
        
        if node_type:
            if isinstance(node_type, str):
                node_type = NodeType(node_type)
            nodes_to_check = list(self.nodes_by_type[node_type].values())
        else:
            for node_dict in self.nodes_by_type.values():
                nodes_to_check.extend(node_dict.values())
        
        for node in nodes_to_check:
            match = True
            for attr, value in filters.items():
                if not hasattr(node, attr) or getattr(node, attr) != value:
                    match = False
                    break
            
            if match:
                result.append(self._apply_detail_level_to_node(node, detail_level))
        
        return result
    
    def find_relationships(self, detail_level: DetailLevel = DetailLevel.STANDARD, **filters) -> List[Relationship]:
        """
        Find relationships matching specified filters with the specified detail level.
        
        Args:
            detail_level: The level of detail to include
            **filters: Attributes to filter by
            
        Returns:
            List of matching relationships
        """
        result = []
        
        relationship_type = filters.pop('type', None)
        source_id = filters.pop('source_id', None)
        target_id = filters.pop('target_id', None)
        
        edges_to_check = []
        
        if source_id and target_id:
            if self.graph.has_edge(source_id, target_id):
                edges_to_check = [(source_id, target_id)]
            else:
                return []
        elif source_id:
            edges_to_check = [(source_id, t) for _, t in self.graph.out_edges(source_id)]
        elif target_id:
            edges_to_check = [(s, target_id) for s, _ in self.graph.in_edges(target_id)]
        else:
            edges_to_check = list(self.graph.edges())
        
        for source, target in edges_to_check:
            relationship = self.graph.edges[source, target]["relationship"]
            
            if relationship_type and relationship.type != relationship_type:
                continue
            
            match = True
            for attr, value in filters.items():
                if not hasattr(relationship, attr) or getattr(relationship, attr) != value:
                    match = False
                    break
            
            if match:
                result.append(self._apply_detail_level_to_relationship(relationship, detail_level))
        
        return result
    
    def shortest_path(self, source_id: str, target_id: str, detail_level: DetailLevel = DetailLevel.STANDARD) -> List[Node]:
        """
        Find the shortest path between two nodes with the specified detail level.
        
        Args:
            source_id: ID of the source node
            target_id: ID of the target node
            detail_level: The level of detail to include
            
        Returns:
            List of nodes representing the shortest path
            
        Raises:
            ModelError: If the source or target node does not exist,
                        or if no path exists
        """
        if source_id not in self.graph:
            raise ModelError(f"Source node '{source_id}' does not exist")
        
        if target_id not in self.graph:
            raise ModelError(f"Target node '{target_id}' does not exist")
        
        try:
            path = nx.shortest_path(self.graph, source_id, target_id)
            return [self._apply_detail_level_to_node(self.graph.nodes[node_id]["node"], detail_level) 
                    for node_id in path]
        except nx.NetworkXNoPath:
            raise ModelError(f"No path exists from '{source_id}' to '{target_id}'")
    
    def get_connected_components(self) -> List[Set[str]]:
        """
        Get the connected components of the graph.
        
        Returns:
            List of sets of node IDs, each set representing a connected component
        """
        return [set(component) for component in nx.weakly_connected_components(self.graph)]
    
    def to_json(self, detail_level: DetailLevel = DetailLevel.STANDARD) -> Dict[str, Any]:
        """
        Convert the relationship map to a JSON representation with the specified detail level.
        
        Args:
            detail_level: The level of detail to include
            
        Returns:
            JSON representation of the relationship map
        """
        nodes = []
        for node_id in self.graph.nodes:
            node = self.graph.nodes[node_id]["node"]
            filtered_node = self._apply_detail_level_to_node(node, detail_level)
            nodes.append(filtered_node.to_json())
        
        relationships = []
        for source_id, target_id, data in self.graph.edges(data=True):
            relationship = data["relationship"]
            filtered_relationship = self._apply_detail_level_to_relationship(relationship, detail_level)
            relationships.append(filtered_relationship.to_json())
        
        return {
            "nodes": nodes,
            "relationships": relationships,
            "detail_level": detail_level.value
        }
    
    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'RelationshipMap':
        """
        Create a relationship map from a JSON representation.
        
        Args:
            data: JSON representation of the relationship map
            
        Returns:
            RelationshipMap instance
        """
        relationship_map = cls()
        
        for node_data in data["nodes"]:
            node = Node.from_json(node_data)
            relationship_map.add_node(node)
        
        for relationship_data in data["relationships"]:
            relationship = Relationship.from_json(relationship_data)
            relationship_map.add_relationship(relationship)
        
        return relationship_map
    
    def save(self, path: str) -> None:
        """
        Save the relationship map to a file.
        
        Args:
            path: Path to the output file
        """
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        
        with open(path, 'wb') as f:
            pickle.dump(self, f)
        
        logger.info(f"Saved RelationshipMap to {path}")

    
    @classmethod
    def load(cls, path: str) -> 'RelationshipMap':
        """
        Load a relationship map from a file.
        
        Args:
            path: Path to the input file
            
        Returns:
            RelationshipMap instance
            
        Raises:
            FileNotFoundError: If the file does not exist
        """
        with open(path, 'rb') as f:
            relationship_map = pickle.load(f)
        
        logger.info(f"Loaded RelationshipMap from {path}")
        return relationship_map
    
    def _apply_detail_level_to_node(self, node: Node, detail_level: DetailLevel) -> Node:
        """
        Apply detail level filtering to a node.
        
        Args:
            node: The node to filter
            detail_level: The level of detail to include
            
        Returns:
            Filtered node
        """
        # Create a copy of the node to avoid modifying the original
        filtered_node = copy.deepcopy(node)
        
        if detail_level == DetailLevel.MINIMAL:
            # Minimal detail level: keep only essential fields, strip metadata
            filtered_node.metadata = {}
            
            # For FunctionNode, keep only name and type, remove details
            if isinstance(filtered_node, FunctionNode):
                filtered_node.parameters = []
                filtered_node.return_type = None
                
            # For ClassNode, keep only name and type, remove details
            elif isinstance(filtered_node, ClassNode):
                filtered_node.properties = []
                
            # For MethodNode, keep only name and parent class, remove details
            elif isinstance(filtered_node, MethodNode):
                filtered_node.parameters = []
                filtered_node.return_type = None
                
        elif detail_level == DetailLevel.STANDARD:
            # Standard detail level: keep essential fields and basic metadata
            
            # Remove non-essential metadata
            metadata_to_keep = ["visibility", "deprecation", "access_level", "source_file"]
            filtered_metadata = {}
            for key in metadata_to_keep:
                if key in filtered_node.metadata:
                    filtered_metadata[key] = filtered_node.metadata[key]
            filtered_node.metadata = filtered_metadata
            
            # For FunctionNode, keep parameters but remove detailed type info
            if isinstance(filtered_node, FunctionNode) and filtered_node.parameters:
                for param in filtered_node.parameters:
                    if "type" in param and param["type"] is not None:
                        # Keep only name and is_optional from type info
                        minimal_type = {"name": param["type"].get("name", "any")}
                        if "is_optional" in param["type"]:
                            minimal_type["is_optional"] = param["type"]["is_optional"]
                        param["type"] = minimal_type
                        
            # Similar simplifications for ClassNode and MethodNode
            # ...
        
        # For DetailLevel.DETAILED, return the full node as is
        
        return filtered_node
    
    def _apply_detail_level_to_relationship(self, relationship: Relationship, detail_level: DetailLevel) -> Relationship:
        """
        Apply detail level filtering to a relationship.
        
        Args:
            relationship: The relationship to filter
            detail_level: The level of detail to include
            
        Returns:
            Filtered relationship
        """
        # Create a copy of the relationship to avoid modifying the original
        filtered_relationship = copy.deepcopy(relationship)
        
        if detail_level == DetailLevel.MINIMAL:
            # Minimal detail level: strip all metadata
            filtered_relationship.metadata = {}
            
            # For CallsRelationship, remove line number
            if isinstance(filtered_relationship, CallsRelationship):
                filtered_relationship.line_number = None
                
        elif detail_level == DetailLevel.STANDARD:
            # Standard detail level: keep essential metadata
            metadata_to_keep = ["visibility", "call_type", "importance"]
            filtered_metadata = {}
            for key in metadata_to_keep:
                if key in filtered_relationship.metadata:
                    filtered_metadata[key] = filtered_relationship.metadata[key]
            filtered_relationship.metadata = filtered_metadata
        
        # For DetailLevel.DETAILED, return the full relationship as is
        
        return filtered_relationship
