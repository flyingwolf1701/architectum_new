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
