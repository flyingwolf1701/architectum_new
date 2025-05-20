"""
Node and relationship type definitions for the Relationship Map.
"""

from enum import Enum
from typing import Dict, Any, List, Optional, TypedDict, Union


class NodeType(Enum):
    """Types of nodes in the relationship map."""
    FILE = "file"
    DIRECTORY = "directory"
    FUNCTION = "function"
    CLASS = "class"
    METHOD = "method"
    FEATURE = "feature"


class RelationshipType(Enum):
    """Types of relationships in the relationship map."""
    CONTAINS = "contains"
    CALLS = "calls"
    IMPORTS = "imports"
    INHERITS = "inherits"
    IMPLEMENTS = "implements"


class TypeInfo(TypedDict, total=False):
    """Type information for a parameter or return value."""
    name: str
    is_optional: bool
    is_list: bool
    subtypes: List['TypeInfo']


class ParameterInfo(TypedDict, total=False):
    """Information about a function/method parameter."""
    name: str
    type: Optional[TypeInfo]
    default_value: Optional[str]
    is_optional: bool
    is_variadic: bool


class PropertyInfo(TypedDict, total=False):
    """Information about a class property."""
    name: str
    type: Optional[TypeInfo]
    visibility: str  # public, private, protected
    is_static: bool
    default_value: Optional[str]


class Node:
    """Base class for all nodes in the graph."""
    
    def __init__(self, node_id: str, node_type: NodeType, metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a node.
        
        Args:
            node_id: Unique identifier for the node
            node_type: Type of the node
            metadata: Additional metadata for the node
        """
        self.id = node_id
        self.type = node_type
        self.metadata = metadata or {}
    
    def to_json(self) -> Dict[str, Any]:
        """
        Convert the node to a JSON representation.
        
        Returns:
            JSON representation of the node
        """
        return {
            "id": self.id,
            "type": self.type.value,
            "metadata": self.metadata
        }
    
    def __eq__(self, other):
        """
        Check if two nodes are equal.
        
        Args:
            other: Node to compare with
            
        Returns:
            True if nodes are equal, False otherwise
        """
        if not isinstance(other, Node):
            return False
            
        return (
            self.id == other.id and
            self.type == other.type
        )
    
    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Node':
        """
        Create a node from a JSON representation.
        
        Args:
            data: JSON representation of the node
            
        Returns:
            Node instance
        """
        node_type = NodeType(data["type"])
        node_id = data["id"]
        metadata = data.get("metadata", {})
        
        if node_type == NodeType.FILE:
            return FileNode(node_id, data["path"], data["extension"], metadata)
        elif node_type == NodeType.DIRECTORY:
            return DirectoryNode(node_id, data["path"], metadata)
        elif node_type == NodeType.FUNCTION:
            return FunctionNode(
                node_id,
                data["name"],
                data.get("parameters", []),
                data.get("return_type"),
                data.get("line_start"),
                data.get("line_end"),
                metadata
            )
        elif node_type == NodeType.CLASS:
            return ClassNode(
                node_id,
                data["name"],
                data.get("properties", []),
                data.get("line_start"),
                data.get("line_end"),
                metadata
            )
        elif node_type == NodeType.METHOD:
            return MethodNode(
                node_id,
                data["name"],
                data.get("parameters", []),
                data.get("return_type"),
                data.get("parent_class"),
                data.get("line_start"),
                data.get("line_end"),
                metadata
            )
        elif node_type == NodeType.FEATURE:
            return FeatureNode(node_id, data["name"], data.get("description", ""), metadata)
        else:
            return cls(node_id, node_type, metadata)


class FileNode(Node):
    """Represents a file in the codebase."""
    
    def __init__(
        self, 
        node_id: str, 
        path: str, 
        extension: str, 
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a file node.
        
        Args:
            node_id: Unique identifier for the node
            path: Path to the file
            extension: File extension
            metadata: Additional metadata for the node
        """
        super().__init__(node_id, NodeType.FILE, metadata)
        self.path = path
        self.extension = extension
    
    def to_json(self) -> Dict[str, Any]:
        """
        Convert the file node to a JSON representation.
        
        Returns:
            JSON representation of the file node
        """
        result = super().to_json()
        result.update({
            "path": self.path,
            "extension": self.extension
        })
        return result


class DirectoryNode(Node):
    """Represents a directory in the codebase."""
    
    def __init__(
        self, 
        node_id: str, 
        path: str, 
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a directory node.
        
        Args:
            node_id: Unique identifier for the node
            path: Path to the directory
            metadata: Additional metadata for the node
        """
        super().__init__(node_id, NodeType.DIRECTORY, metadata)
        self.path = path
    
    def to_json(self) -> Dict[str, Any]:
        """
        Convert the directory node to a JSON representation.
        
        Returns:
            JSON representation of the directory node
        """
        result = super().to_json()
        result.update({
            "path": self.path
        })
        return result


class FunctionNode(Node):
    """Represents a function in the codebase."""
    
    def __init__(
        self, 
        node_id: str, 
        name: str, 
        parameters: Optional[List[ParameterInfo]] = None,
        return_type: Optional[TypeInfo] = None,
        line_start: Optional[int] = None,
        line_end: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a function node.
        
        Args:
            node_id: Unique identifier for the node
            name: Function name
            parameters: List of parameter information
            return_type: Return type information
            line_start: Starting line number
            line_end: Ending line number
            metadata: Additional metadata for the node
        """
        super().__init__(node_id, NodeType.FUNCTION, metadata)
        self.name = name
        self.parameters = parameters or []
        self.return_type = return_type
        self.line_start = line_start
        self.line_end = line_end
    
    def to_json(self) -> Dict[str, Any]:
        """
        Convert the function node to a JSON representation.
        
        Returns:
            JSON representation of the function node
        """
        result = super().to_json()
        result.update({
            "name": self.name,
            "parameters": self.parameters,
            "return_type": self.return_type,
            "line_start": self.line_start,
            "line_end": self.line_end
        })
        return result


class ClassNode(Node):
    """Represents a class in the codebase."""
    
    def __init__(
        self, 
        node_id: str, 
        name: str, 
        properties: Optional[List[PropertyInfo]] = None,
        line_start: Optional[int] = None,
        line_end: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a class node.
        
        Args:
            node_id: Unique identifier for the node
            name: Class name
            properties: List of property information
            line_start: Starting line number
            line_end: Ending line number
            metadata: Additional metadata for the node
        """
        super().__init__(node_id, NodeType.CLASS, metadata)
        self.name = name
        self.properties = properties or []
        self.line_start = line_start
        self.line_end = line_end
    
    def to_json(self) -> Dict[str, Any]:
        """
        Convert the class node to a JSON representation.
        
        Returns:
            JSON representation of the class node
        """
        result = super().to_json()
        result.update({
            "name": self.name,
            "properties": self.properties,
            "line_start": self.line_start,
            "line_end": self.line_end
        })
        return result


class MethodNode(Node):
    """Represents a method in a class."""
    
    def __init__(
        self, 
        node_id: str, 
        name: str, 
        parameters: Optional[List[ParameterInfo]] = None,
        return_type: Optional[TypeInfo] = None,
        parent_class: Optional[str] = None,
        line_start: Optional[int] = None,
        line_end: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a method node.
        
        Args:
            node_id: Unique identifier for the node
            name: Method name
            parameters: List of parameter information
            return_type: Return type information
            parent_class: ID of the parent class node
            line_start: Starting line number
            line_end: Ending line number
            metadata: Additional metadata for the node
        """
        super().__init__(node_id, NodeType.METHOD, metadata)
        self.name = name
        self.parameters = parameters or []
        self.return_type = return_type
        self.parent_class = parent_class
        self.line_start = line_start
        self.line_end = line_end
    
    def to_json(self) -> Dict[str, Any]:
        """
        Convert the method node to a JSON representation.
        
        Returns:
            JSON representation of the method node
        """
        result = super().to_json()
        result.update({
            "name": self.name,
            "parameters": self.parameters,
            "return_type": self.return_type,
            "parent_class": self.parent_class,
            "line_start": self.line_start,
            "line_end": self.line_end
        })
        return result


class FeatureNode(Node):
    """Represents a virtual feature grouping."""
    
    def __init__(
        self, 
        node_id: str, 
        name: str, 
        description: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a feature node.
        
        Args:
            node_id: Unique identifier for the node
            name: Feature name
            description: Feature description
            metadata: Additional metadata for the node
        """
        super().__init__(node_id, NodeType.FEATURE, metadata)
        self.name = name
        self.description = description
    
    def to_json(self) -> Dict[str, Any]:
        """
        Convert the feature node to a JSON representation.
        
        Returns:
            JSON representation of the feature node
        """
        result = super().to_json()
        result.update({
            "name": self.name,
            "description": self.description
        })
        return result


class Relationship:
    """Base class for all relationships in the graph."""
    
    def __init__(
        self, 
        source_id: str, 
        target_id: str, 
        relationship_type: RelationshipType,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a relationship.
        
        Args:
            source_id: ID of the source node
            target_id: ID of the target node
            relationship_type: Type of the relationship
            metadata: Additional metadata for the relationship
        """
        self.source_id = source_id
        self.target_id = target_id
        self.type = relationship_type
        self.metadata = metadata or {}
    
    def to_json(self) -> Dict[str, Any]:
        """
        Convert the relationship to a JSON representation.
        
        Returns:
            JSON representation of the relationship
        """
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "type": self.type.value,
            "metadata": self.metadata
        }
    
    def __eq__(self, other):
        """
        Check if two relationships are equal.
        
        Args:
            other: Relationship to compare with
            
        Returns:
            True if relationships are equal, False otherwise
        """
        if not isinstance(other, Relationship):
            return False
            
        return (
            self.source_id == other.source_id and
            self.target_id == other.target_id and
            self.type == other.type
        )
    
    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Relationship':
        """
        Create a relationship from a JSON representation.
        
        Args:
            data: JSON representation of the relationship
            
        Returns:
            Relationship instance
        """
        relationship_type = RelationshipType(data["type"])
        source_id = data["source_id"]
        target_id = data["target_id"]
        metadata = data.get("metadata", {})
        
        if relationship_type == RelationshipType.CONTAINS:
            return ContainsRelationship(source_id, target_id, metadata)
        elif relationship_type == RelationshipType.CALLS:
            return CallsRelationship(
                source_id, 
                target_id, 
                data.get("line_number"),
                metadata
            )
        elif relationship_type == RelationshipType.IMPORTS:
            return ImportsRelationship(source_id, target_id, metadata)
        elif relationship_type == RelationshipType.INHERITS:
            return InheritsRelationship(source_id, target_id, metadata)
        elif relationship_type == RelationshipType.IMPLEMENTS:
            return ImplementsRelationship(source_id, target_id, metadata)
        else:
            return cls(source_id, target_id, relationship_type, metadata)


class ContainsRelationship(Relationship):
    """Represents a containment relationship (directory contains file, file contains function)."""
    
    def __init__(
        self, 
        source_id: str, 
        target_id: str, 
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a contains relationship.
        
        Args:
            source_id: ID of the container node
            target_id: ID of the contained node
            metadata: Additional metadata for the relationship
        """
        super().__init__(source_id, target_id, RelationshipType.CONTAINS, metadata)


class CallsRelationship(Relationship):
    """Represents a function call relationship."""
    
    def __init__(
        self, 
        source_id: str, 
        target_id: str, 
        line_number: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a calls relationship.
        
        Args:
            source_id: ID of the calling function/method node
            target_id: ID of the called function/method node
            line_number: Line number of the call
            metadata: Additional metadata for the relationship
        """
        super().__init__(source_id, target_id, RelationshipType.CALLS, metadata)
        self.line_number = line_number
    
    def to_json(self) -> Dict[str, Any]:
        """
        Convert the calls relationship to a JSON representation.
        
        Returns:
            JSON representation of the calls relationship
        """
        result = super().to_json()
        result.update({
            "line_number": self.line_number
        })
        return result


class ImportsRelationship(Relationship):
    """Represents a file import relationship."""
    
    def __init__(
        self, 
        source_id: str, 
        target_id: str, 
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize an imports relationship.
        
        Args:
            source_id: ID of the importing file node
            target_id: ID of the imported file node
            metadata: Additional metadata for the relationship
        """
        super().__init__(source_id, target_id, RelationshipType.IMPORTS, metadata)


class InheritsRelationship(Relationship):
    """Represents a class inheritance relationship."""
    
    def __init__(
        self, 
        source_id: str, 
        target_id: str, 
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize an inherits relationship.
        
        Args:
            source_id: ID of the child class node
            target_id: ID of the parent class node
            metadata: Additional metadata for the relationship
        """
        super().__init__(source_id, target_id, RelationshipType.INHERITS, metadata)


class ImplementsRelationship(Relationship):
    """Represents a function implementing a feature."""
    
    def __init__(
        self, 
        source_id: str, 
        target_id: str, 
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize an implements relationship.
        
        Args:
            source_id: ID of the function/method node
            target_id: ID of the feature node
            metadata: Additional metadata for the relationship
        """
        super().__init__(source_id, target_id, RelationshipType.IMPLEMENTS, metadata)