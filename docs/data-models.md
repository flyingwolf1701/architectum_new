# Data Models

This document details the core data models used in the Architectum system. These models form the foundation of the dual representation approach (Relationship Map and JSON Mirrors) used to provide efficient code comprehension.

## Relationship Map Models

The Relationship Map represents code as a directed graph of nodes and relationships, optimized for navigation and relationship analysis.

### Node Types

```python
class Node:
    """Base class for all nodes in the graph."""
    id: str
    type: NodeType
    metadata: Dict[str, Any]

class FileNode(Node):
    """Represents a file in the codebase."""
    path: str
    extension: str
    
class DirectoryNode(Node):
    """Represents a directory in the codebase."""
    path: str

class FunctionNode(Node):
    """Represents a function/method in the codebase."""
    name: str
    parameters: List[ParameterInfo]
    return_type: Optional[TypeInfo]
    line_start: int
    line_end: int

class ClassNode(Node):
    """Represents a class in the codebase."""
    name: str
    properties: List[PropertyInfo]
    line_start: int
    line_end: int

class FeatureNode(Node):
    """Represents a virtual feature grouping."""
    name: str
    description: str
```

### Relationship Types

```python
class Relationship:
    """Base class for all relationships in the graph."""
    source_id: str
    target_id: str
    type: RelationshipType
    metadata: Dict[str, Any]

class ContainsRelationship(Relationship):
    """Represents a containment relationship (directory contains file, file contains function)."""
    
class CallsRelationship(Relationship):
    """Represents a function call relationship."""
    line_number: Optional[int]
    
class ImportsRelationship(Relationship):
    """Represents a file import relationship."""
    
class InheritsRelationship(Relationship):
    """Represents a class inheritance relationship."""
    
class ImplementsRelationship(Relationship):
    """Represents a function implementing a feature."""
```

## JSON Mirrors Models

JSON Mirrors maintain a mirrored JSON representation of each file in the codebase, optimized for detailed content access.

### Mirror Structure Model

```python
class JSONMirrors:
    """Manages the JSON mirror representation of code files."""
    
    root_path: str
    mirror_path: str
    
    def get_mirror_path(self, source_path: str) -> str:
        """Get the path of the mirrored JSON file for a source code file."""
        
    def get_mirrored_content(self, source_path: str) -> Optional[Dict[str, Any]]:
        """Get the JSON representation of a source code file."""
        
    def update_mirrored_content(self, source_path: str, content: Dict[str, Any]) -> None:
        """Update the JSON representation of a source code file."""
        
    def exists(self, source_path: str) -> bool:
        """Check if a mirrored file exists for the given source path."""

class FileContent:
    """Represents the content of a file."""
    
    path: str
    extension: str
    elements: Dict[str, CodeElement]
    imports: List[str]
    
    def to_json(self) -> Dict[str, Any]:
        """Convert the file content to a JSON representation."""

class DirectoryContent:
    """Represents the content of a directory."""
    
    path: str
    files: List[str]
    subdirectories: List[str]
    
    def to_json(self) -> Dict[str, Any]:
        """Convert the directory content to a JSON representation."""

class CodeElement:
    """Represents a code element (function, class, etc.)."""
    
    name: str
    type: ElementType
    line_start: int
    line_end: int
    metadata: Dict[str, Any]
    
    def to_json(self) -> Dict[str, Any]:
        """Convert the code element to a JSON representation."""
```

## Blueprint Models

Blueprints combine elements from both core representations to create specialized views for different use cases.

```python
class Blueprint:
    """Base class for all blueprint types."""
    
    relationship_map: RelationshipMap
    json_mirrors: JSONMirrors
    
    def to_json(self) -> Dict[str, Any]:
        """Convert blueprint to JSON representation."""
        
    def to_xml(self) -> str:
        """Convert blueprint to XML representation."""

class FileBasedBlueprint(Blueprint):
    """Blueprint focusing on entire files."""
    
    file_paths: List[str]
    
    def generate(self) -> None:
        """Generate blueprint for the specified files."""

class ComponentBasedBlueprint(Blueprint):
    """Blueprint focusing on specific components within files."""
    
    components: Dict[str, List[str]]  # Maps file paths to component names
    
    def generate(self) -> None:
        """Generate blueprint for the specified components."""

class FeatureBlueprint(Blueprint):
    """Persistent blueprint documenting a complete feature."""
    
    name: str
    description: str
    components: Dict[str, List[str]]  # Maps file paths to component names
    yaml_path: str  # Path to the YAML definition
    
    def generate(self) -> None:
        """Generate blueprint for the feature."""
        
    def save(self) -> None:
        """Save the feature blueprint for future reference."""

class TemporaryBlueprint(Blueprint):
    """Ad-hoc blueprint for immediate development tasks."""
    
    components: Dict[str, List[str]]  # Maps file paths to component names
    
    def generate(self) -> None:
        """Generate blueprint for temporary use."""
        
    def clear(self) -> None:
        """Clear the temporary blueprint after use."""
```

## Data Persistence Models

### SQLite Schema

The SQLite database is used for local storage of blueprint metadata and cache references:

#### Blueprints Table
- `id`: UUID primary key
- `name`: String, blueprint name
- `type`: String, blueprint type (file, component, feature, temporary)
- `creation_date`: Timestamp
- `last_updated`: Timestamp
- `yaml_definition`: Text, YAML definition for the blueprint

#### Blueprint Files Table
- `blueprint_id`: UUID, foreign key to blueprints table
- `file_path`: String, path to source file
- `file_hash`: String, hash of file content

#### Relationship Cache Table
- `source_id`: String, source node ID
- `target_id`: String, target node ID
- `relationship_type`: String
- `metadata_json`: Text, JSON-serialized metadata

#### File Mirrors Table
- `file_path`: String, path to source file
- `mirror_path`: String, path to mirror file
- `last_updated`: Timestamp
- `file_hash`: String, hash of file content

### Caching Models

Cache storage uses Python's native serialization capabilities:

- Blueprint cache using Python's `pickle` module
- LRU (Least Recently Used) caching strategy for in-memory components
- Hash-based cache invalidation
- Configurable cache size and cleanup policies
