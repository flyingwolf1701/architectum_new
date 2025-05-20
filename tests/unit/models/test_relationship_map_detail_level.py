"""
Tests for relationship map detail level filtering.
"""

import pytest
import copy

from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.nodes import (
    NodeType, RelationshipType, FileNode, FunctionNode, ClassNode,
    ContainsRelationship, CallsRelationship
)


class TestRelationshipMapDetailLevel:
    """Tests for RelationshipMap detail level filtering."""
    
    def setup_test_graph(self):
        """Set up a test graph with various node and relationship types."""
        relationship_map = RelationshipMap()
        
        # Add file node
        file_node = FileNode(
            "file1",
            "path/to/file.py",
            ".py",
            {"author": "Test User", "created_date": "2023-01-01"}
        )
        relationship_map.add_node(file_node)
        
        # Add function node with detailed info
        func_node = FunctionNode(
            "func1",
            "test_function",
            [
                {"name": "param1", "type": {"name": "int"}, "default_value": "0"},
                {"name": "param2", "type": {"name": "str"}, "default_value": None}
            ],
            {"name": "bool"},
            10, 20,
            {"doc": "This is a test function", "complexity": "O(n)"}
        )
        relationship_map.add_node(func_node)
        
        # Add class node with detailed info
        class_node = ClassNode(
            "class1",
            "TestClass",
            [
                {"name": "prop1", "type": {"name": "int"}, "visibility": "public"},
                {"name": "prop2", "type": {"name": "str"}, "visibility": "private"}
            ],
            30, 50,
            {"doc": "This is a test class", "methods": ["method1", "method2"]}
        )
        relationship_map.add_node(class_node)
        
        # Add relationships
        contains_rel = ContainsRelationship(
            "file1", "func1", 
            {"location": "top-level"}
        )
        relationship_map.add_relationship(contains_rel)
        
        contains_rel2 = ContainsRelationship(
            "file1", "class1", 
            {"location": "top-level"}
        )
        relationship_map.add_relationship(contains_rel2)
        
        calls_rel = CallsRelationship(
            "func1", "class1", 
            15,  # line number
            {"call_type": "constructor", "arguments": ["arg1", "arg2"]}
        )
        relationship_map.add_relationship(calls_rel)
        
        return relationship_map
    
    def test_get_node_minimal_detail(self):
        """Test getting a node with minimal detail level."""
        relationship_map = self.setup_test_graph()
        
        # Get function node with minimal detail
        func_node = relationship_map.get_node("func1", DetailLevel.MINIMAL)
        
        # Check that essential fields are present
        assert func_node.id == "func1"
        assert func_node.type == NodeType.FUNCTION
        assert func_node.name == "test_function"
        
        # Check that non-essential fields are stripped
        assert func_node.metadata == {}
        assert func_node.parameters == []
        assert func_node.return_type is None
        
        # Get class node with minimal detail
        class_node = relationship_map.get_node("class1", DetailLevel.MINIMAL)
        
        # Check that essential fields are present
        assert class_node.id == "class1"
        assert class_node.type == NodeType.CLASS
        assert class_node.name == "TestClass"
        
        # Check that non-essential fields are stripped
        assert class_node.metadata == {}
        assert class_node.properties == []
    
    def test_get_node_standard_detail(self):
        """Test getting a node with standard detail level."""
        relationship_map = self.setup_test_graph()
        
        # Get function node with standard detail
        func_node = relationship_map.get_node("func1", DetailLevel.STANDARD)
        
        # Check that essential fields and basic metadata are present
        assert func_node.id == "func1"
        assert func_node.type == NodeType.FUNCTION
        assert func_node.name == "test_function"
        assert len(func_node.parameters) > 0
        assert func_node.return_type is not None
        
        # Check that detailed metadata is stripped
        assert len(func_node.metadata) < 2  # Less metadata than in the original
        
        # Get class node with standard detail
        class_node = relationship_map.get_node("class1", DetailLevel.STANDARD)
        
        # Similar checks for class node
        assert class_node.id == "class1"
        assert class_node.type == NodeType.CLASS
        assert class_node.name == "TestClass"
        assert len(class_node.properties) > 0
        assert len(class_node.metadata) < 2  # Less metadata than in the original
    
    def test_get_node_detailed_detail(self):
        """Test getting a node with detailed detail level."""
        relationship_map = self.setup_test_graph()
        
        # Get function node with detailed detail
        func_node = relationship_map.get_node("func1", DetailLevel.DETAILED)
        
        # Check that all fields are present
        assert func_node.id == "func1"
        assert func_node.type == NodeType.FUNCTION
        assert func_node.name == "test_function"
        assert len(func_node.parameters) == 2
        assert func_node.return_type == {"name": "bool"}
        assert func_node.line_start == 10
        assert func_node.line_end == 20
        assert "doc" in func_node.metadata
        assert "complexity" in func_node.metadata
        
        # Get class node with detailed detail
        class_node = relationship_map.get_node("class1", DetailLevel.DETAILED)
        
        # Check that all fields are present
        assert class_node.id == "class1"
        assert class_node.type == NodeType.CLASS
        assert class_node.name == "TestClass"
        assert len(class_node.properties) == 2
        assert class_node.line_start == 30
        assert class_node.line_end == 50
        assert "doc" in class_node.metadata
        assert "methods" in class_node.metadata
    
    def test_get_relationship_with_detail_levels(self):
        """Test getting relationships with different detail levels."""
        relationship_map = self.setup_test_graph()
        
        # Test minimal detail level
        rel = relationship_map.get_relationship("func1", "class1", DetailLevel.MINIMAL)
        assert rel.source_id == "func1"
        assert rel.target_id == "class1"
        assert rel.type == RelationshipType.CALLS
        assert rel.metadata == {}
        assert rel.line_number is None  # Line number should be stripped in minimal detail
        
        # Test standard detail level
        rel = relationship_map.get_relationship("func1", "class1", DetailLevel.STANDARD)
        assert rel.source_id == "func1"
        assert rel.target_id == "class1"
        assert rel.type == RelationshipType.CALLS
        assert "call_type" in rel.metadata  # Essential metadata should be present
        assert "arguments" not in rel.metadata  # Non-essential metadata should be stripped
        
        # Test detailed detail level
        rel = relationship_map.get_relationship("func1", "class1", DetailLevel.DETAILED)
        assert rel.source_id == "func1"
        assert rel.target_id == "class1"
        assert rel.type == RelationshipType.CALLS
        assert rel.line_number == 15
        assert "call_type" in rel.metadata
        assert "arguments" in rel.metadata  # All metadata should be present
    
    def test_to_json_with_detail_levels(self):
        """Test serializing the relationship map with different detail levels."""
        relationship_map = self.setup_test_graph()
        
        # Test minimal detail level
        json_data = relationship_map.to_json(DetailLevel.MINIMAL)
        
        # Check that nodes are included
        assert "nodes" in json_data
        assert len(json_data["nodes"]) == 3
        
        # Check that relationships are included
        assert "relationships" in json_data
        assert len(json_data["relationships"]) == 3
        
        # Check that detail level is included
        assert "detail_level" in json_data
        assert json_data["detail_level"] == "minimal"
        
        # Check that node metadata is stripped
        for node in json_data["nodes"]:
            if "metadata" in node:
                assert node["metadata"] == {}
        
        # Check that relationship metadata is stripped
        for rel in json_data["relationships"]:
            if "metadata" in rel:
                assert rel["metadata"] == {}
        
        # Test detailed detail level
        json_data = relationship_map.to_json(DetailLevel.DETAILED)
        
        # Check that detail level is included
        assert json_data["detail_level"] == "detailed"
        
        # Check that node metadata is preserved
        for node in json_data["nodes"]:
            if node["id"] == "func1":
                assert "doc" in node["metadata"]
                assert "complexity" in node["metadata"]
        
        # Check that relationship metadata is preserved
        for rel in json_data["relationships"]:
            if rel["source_id"] == "func1" and rel["target_id"] == "class1":
                assert "call_type" in rel["metadata"]
                assert "arguments" in rel["metadata"]
    
    def test_get_nodes_by_type_with_detail_levels(self):
        """Test getting all nodes of a specific type with different detail levels."""
        relationship_map = self.setup_test_graph()
        
        # Test minimal detail level
        nodes = relationship_map.get_nodes_by_type(NodeType.FUNCTION, DetailLevel.MINIMAL)
        assert len(nodes) == 1
        assert nodes[0].id == "func1"
        assert nodes[0].metadata == {}
        assert nodes[0].parameters == []
        
        # Test detailed detail level
        nodes = relationship_map.get_nodes_by_type(NodeType.FUNCTION, DetailLevel.DETAILED)
        assert len(nodes) == 1
        assert nodes[0].id == "func1"
        assert "doc" in nodes[0].metadata
        assert len(nodes[0].parameters) == 2
