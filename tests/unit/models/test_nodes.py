"""
Tests for the nodes module.
"""

import pytest

from arch_blueprint_generator.models.nodes import (
    NodeType, RelationshipType, TypeInfo, ParameterInfo, PropertyInfo,
    Node, FileNode, DirectoryNode, FunctionNode, ClassNode, MethodNode, FeatureNode,
    Relationship, ContainsRelationship, CallsRelationship, ImportsRelationship,
    InheritsRelationship, ImplementsRelationship
)


class TestNodeTypes:
    """Tests for node type definitions."""
    
    def test_node_type_enum(self):
        """Test NodeType enum values."""
        assert NodeType.FILE.value == "file"
        assert NodeType.DIRECTORY.value == "directory"
        assert NodeType.FUNCTION.value == "function"
        assert NodeType.CLASS.value == "class"
        assert NodeType.METHOD.value == "method"
        assert NodeType.FEATURE.value == "feature"


class TestRelationshipTypes:
    """Tests for relationship type definitions."""
    
    def test_relationship_type_enum(self):
        """Test RelationshipType enum values."""
        assert RelationshipType.CONTAINS.value == "contains"
        assert RelationshipType.CALLS.value == "calls"
        assert RelationshipType.IMPORTS.value == "imports"
        assert RelationshipType.INHERITS.value == "inherits"
        assert RelationshipType.IMPLEMENTS.value == "implements"


class TestNode:
    """Tests for the Node class."""
    
    def test_init(self):
        """Test initialization of a node."""
        node = Node("test_id", NodeType.FILE, {"key": "value"})
        
        assert node.id == "test_id"
        assert node.type == NodeType.FILE
        assert node.metadata == {"key": "value"}
        
        # Test default metadata
        node = Node("test_id", NodeType.FILE)
        assert node.metadata == {}
    
    def test_to_json(self):
        """Test converting a node to JSON."""
        node = Node("test_id", NodeType.FILE, {"key": "value"})
        
        json_data = node.to_json()
        
        assert json_data["id"] == "test_id"
        assert json_data["type"] == "file"
        assert json_data["metadata"] == {"key": "value"}
    
    def test_from_json(self):
        """Test creating a node from JSON."""
        # Test FileNode
        file_data = {
            "id": "file1",
            "type": "file",
            "path": "path/to/file1.py",
            "extension": ".py",
            "metadata": {"key": "value"}
        }
        
        file_node = Node.from_json(file_data)
        
        assert isinstance(file_node, FileNode)
        assert file_node.id == "file1"
        assert file_node.type == NodeType.FILE
        assert file_node.path == "path/to/file1.py"
        assert file_node.extension == ".py"
        assert file_node.metadata == {"key": "value"}
        
        # Test DirectoryNode
        dir_data = {
            "id": "dir1",
            "type": "directory",
            "path": "path/to/dir1",
            "metadata": {"key": "value"}
        }
        
        dir_node = Node.from_json(dir_data)
        
        assert isinstance(dir_node, DirectoryNode)
        assert dir_node.id == "dir1"
        assert dir_node.type == NodeType.DIRECTORY
        assert dir_node.path == "path/to/dir1"
        assert dir_node.metadata == {"key": "value"}
        
        # Test FunctionNode
        func_data = {
            "id": "func1",
            "type": "function",
            "name": "my_function",
            "parameters": [],
            "return_type": None,
            "line_start": 10,
            "line_end": 20,
            "metadata": {"key": "value"}
        }
        
        func_node = Node.from_json(func_data)
        
        assert isinstance(func_node, FunctionNode)
        assert func_node.id == "func1"
        assert func_node.type == NodeType.FUNCTION
        assert func_node.name == "my_function"
        assert func_node.parameters == []
        assert func_node.return_type is None
        assert func_node.line_start == 10
        assert func_node.line_end == 20
        assert func_node.metadata == {"key": "value"}


class TestFileNode:
    """Tests for the FileNode class."""
    
    def test_init(self):
        """Test initialization of a file node."""
        file_node = FileNode("file1", "path/to/file1.py", ".py", {"key": "value"})
        
        assert file_node.id == "file1"
        assert file_node.type == NodeType.FILE
        assert file_node.path == "path/to/file1.py"
        assert file_node.extension == ".py"
        assert file_node.metadata == {"key": "value"}
    
    def test_to_json(self):
        """Test converting a file node to JSON."""
        file_node = FileNode("file1", "path/to/file1.py", ".py", {"key": "value"})
        
        json_data = file_node.to_json()
        
        assert json_data["id"] == "file1"
        assert json_data["type"] == "file"
        assert json_data["path"] == "path/to/file1.py"
        assert json_data["extension"] == ".py"
        assert json_data["metadata"] == {"key": "value"}


class TestDirectoryNode:
    """Tests for the DirectoryNode class."""
    
    def test_init(self):
        """Test initialization of a directory node."""
        dir_node = DirectoryNode("dir1", "path/to/dir1", {"key": "value"})
        
        assert dir_node.id == "dir1"
        assert dir_node.type == NodeType.DIRECTORY
        assert dir_node.path == "path/to/dir1"
        assert dir_node.metadata == {"key": "value"}
    
    def test_to_json(self):
        """Test converting a directory node to JSON."""
        dir_node = DirectoryNode("dir1", "path/to/dir1", {"key": "value"})
        
        json_data = dir_node.to_json()
        
        assert json_data["id"] == "dir1"
        assert json_data["type"] == "directory"
        assert json_data["path"] == "path/to/dir1"
        assert json_data["metadata"] == {"key": "value"}


class TestFunctionNode:
    """Tests for the FunctionNode class."""
    
    def test_init(self):
        """Test initialization of a function node."""
        func_node = FunctionNode(
            "func1", 
            "my_function", 
            [{"name": "param1", "type": {"name": "str"}}],
            {"name": "int"},
            10, 
            20, 
            {"key": "value"}
        )
        
        assert func_node.id == "func1"
        assert func_node.type == NodeType.FUNCTION
        assert func_node.name == "my_function"
        assert func_node.parameters == [{"name": "param1", "type": {"name": "str"}}]
        assert func_node.return_type == {"name": "int"}
        assert func_node.line_start == 10
        assert func_node.line_end == 20
        assert func_node.metadata == {"key": "value"}
        
        # Test with defaults
        func_node = FunctionNode("func1", "my_function")
        
        assert func_node.parameters == []
        assert func_node.return_type is None
        assert func_node.line_start is None
        assert func_node.line_end is None
        assert func_node.metadata == {}
    
    def test_to_json(self):
        """Test converting a function node to JSON."""
        func_node = FunctionNode(
            "func1", 
            "my_function", 
            [{"name": "param1", "type": {"name": "str"}}],
            {"name": "int"},
            10, 
            20, 
            {"key": "value"}
        )
        
        json_data = func_node.to_json()
        
        assert json_data["id"] == "func1"
        assert json_data["type"] == "function"
        assert json_data["name"] == "my_function"
        assert json_data["parameters"] == [{"name": "param1", "type": {"name": "str"}}]
        assert json_data["return_type"] == {"name": "int"}
        assert json_data["line_start"] == 10
        assert json_data["line_end"] == 20
        assert json_data["metadata"] == {"key": "value"}


class TestRelationship:
    """Tests for the Relationship class."""
    
    def test_init(self):
        """Test initialization of a relationship."""
        relationship = Relationship(
            "source_id", 
            "target_id", 
            RelationshipType.CONTAINS,
            {"key": "value"}
        )
        
        assert relationship.source_id == "source_id"
        assert relationship.target_id == "target_id"
        assert relationship.type == RelationshipType.CONTAINS
        assert relationship.metadata == {"key": "value"}
        
        # Test with default metadata
        relationship = Relationship("source_id", "target_id", RelationshipType.CONTAINS)
        assert relationship.metadata == {}
    
    def test_to_json(self):
        """Test converting a relationship to JSON."""
        relationship = Relationship(
            "source_id", 
            "target_id", 
            RelationshipType.CONTAINS,
            {"key": "value"}
        )
        
        json_data = relationship.to_json()
        
        assert json_data["source_id"] == "source_id"
        assert json_data["target_id"] == "target_id"
        assert json_data["type"] == "contains"
        assert json_data["metadata"] == {"key": "value"}
    
    def test_from_json(self):
        """Test creating a relationship from JSON."""
        # Test ContainsRelationship
        contains_data = {
            "source_id": "source_id",
            "target_id": "target_id",
            "type": "contains",
            "metadata": {"key": "value"}
        }
        
        contains = Relationship.from_json(contains_data)
        
        assert isinstance(contains, ContainsRelationship)
        assert contains.source_id == "source_id"
        assert contains.target_id == "target_id"
        assert contains.type == RelationshipType.CONTAINS
        assert contains.metadata == {"key": "value"}
        
        # Test CallsRelationship
        calls_data = {
            "source_id": "source_id",
            "target_id": "target_id",
            "type": "calls",
            "line_number": 10,
            "metadata": {"key": "value"}
        }
        
        calls = Relationship.from_json(calls_data)
        
        assert isinstance(calls, CallsRelationship)
        assert calls.source_id == "source_id"
        assert calls.target_id == "target_id"
        assert calls.type == RelationshipType.CALLS
        assert calls.line_number == 10
        assert calls.metadata == {"key": "value"}
        
        # Test ImportsRelationship
        imports_data = {
            "source_id": "source_id",
            "target_id": "target_id",
            "type": "imports",
            "metadata": {"key": "value"}
        }
        
        imports = Relationship.from_json(imports_data)
        
        assert isinstance(imports, ImportsRelationship)
        assert imports.source_id == "source_id"
        assert imports.target_id == "target_id"
        assert imports.type == RelationshipType.IMPORTS
        assert imports.metadata == {"key": "value"}


class TestCallsRelationship:
    """Tests for the CallsRelationship class."""
    
    def test_init(self):
        """Test initialization of a calls relationship."""
        relationship = CallsRelationship(
            "source_id", 
            "target_id", 
            10,
            {"key": "value"}
        )
        
        assert relationship.source_id == "source_id"
        assert relationship.target_id == "target_id"
        assert relationship.type == RelationshipType.CALLS
        assert relationship.line_number == 10
        assert relationship.metadata == {"key": "value"}
        
        # Test with defaults
        relationship = CallsRelationship("source_id", "target_id")
        assert relationship.line_number is None
        assert relationship.metadata == {}
    
    def test_to_json(self):
        """Test converting a calls relationship to JSON."""
        relationship = CallsRelationship(
            "source_id", 
            "target_id", 
            10,
            {"key": "value"}
        )
        
        json_data = relationship.to_json()
        
        assert json_data["source_id"] == "source_id"
        assert json_data["target_id"] == "target_id"
        assert json_data["type"] == "calls"
        assert json_data["line_number"] == 10
        assert json_data["metadata"] == {"key": "value"}
