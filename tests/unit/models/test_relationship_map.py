"""
Tests for the relationship map model.
"""

import os
import pytest
import tempfile

from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.nodes import (
    NodeType, RelationshipType, Node, FileNode, FunctionNode,
    Relationship, ContainsRelationship
)
from arch_blueprint_generator.errors.exceptions import ModelError


class TestRelationshipMap:
    """Tests for the RelationshipMap class."""
    
    def test_init(self):
        """Test initialization of a relationship map."""
        relationship_map = RelationshipMap()
        assert relationship_map.node_count() == 0
        assert relationship_map.relationship_count() == 0
    
    def test_add_node(self):
        """Test adding a node to a relationship map."""
        relationship_map = RelationshipMap()
        
        file_node = FileNode("file1", "path/to/file1.py", ".py")
        relationship_map.add_node(file_node)
        
        assert relationship_map.node_count() == 1
        assert relationship_map.get_node("file1") == file_node
        
        # Test adding a node with the same ID raises an error
        with pytest.raises(ModelError):
            relationship_map.add_node(file_node)
    
    def test_add_relationship(self):
        """Test adding a relationship to a relationship map."""
        relationship_map = RelationshipMap()
        
        file_node = FileNode("file1", "path/to/file1.py", ".py")
        function_node = FunctionNode("func1", "my_function")
        
        relationship_map.add_node(file_node)
        relationship_map.add_node(function_node)
        
        relationship = ContainsRelationship("file1", "func1")
        relationship_map.add_relationship(relationship)
        
        assert relationship_map.relationship_count() == 1
        assert relationship_map.get_relationship("file1", "func1") == relationship
        
        # Test adding a relationship with a non-existent source node raises an error
        with pytest.raises(ModelError):
            relationship_map.add_relationship(ContainsRelationship("non_existent", "func1"))
        
        # Test adding a relationship with a non-existent target node raises an error
        with pytest.raises(ModelError):
            relationship_map.add_relationship(ContainsRelationship("file1", "non_existent"))
