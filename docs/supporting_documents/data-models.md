# Data Models

This document details the core data models used in the Architectum system. These models form the foundation of the three-component approach (System Map, JSON Mirrors, and Blueprints) used to provide efficient code comprehension.

## System Map Models

The System Map represents code as a directed graph of nodes and relationships, optimized for navigation and relationship analysis.

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
    
    system_map: SystemMap
    json_mirrors: JSONMirrors
    
    def to_json(self) -> Dict[str, Any]:
        """Convert blueprint to JSON representation."""
        
    def to_xml(self) -> str:
        """Convert blueprint to XML representation."""

class PathBasedBlueprint(Blueprint):
    """Blueprint focusing on directory structures."""
    
    path: str
    depth: int  # 0 for all levels
    
    def generate(self) -> None:
        """Generate blueprint for the specified path with given depth."""

class MethodBasedBlueprint(Blueprint):
    """Blueprint focusing on specific methods within files."""
    
    components: Dict[str, List[str]]  # Maps file paths to method names (empty list means entire file)
    
    def generate(self) -> None:
        """Generate blueprint for the specified methods."""
```

## Catalog Models

Architectum uses two YAML catalog files to track the codebase.

### Project Catalog (Raw Inventory)

The `project_catalog.yaml` file serves as a canonical inventory of everything in the codebase.

```python
class ProjectCatalog:
    """Manages the project catalog."""
    
    catalog_path: str
    
    def load(self) -> List[Dict[str, Any]]:
        """Load the project catalog from the YAML file."""
        
    def save(self, catalog: List[Dict[str, Any]]) -> None:
        """Save the project catalog to the YAML file."""
        
    def update_file(self, file_path: str, functions: List[str], classes: List[Dict[str, Any]], tracking: Dict[str, bool]) -> None:
        """Update a file entry in the project catalog."""
        
    def get_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get a file entry from the project catalog."""
        
    def remove_file(self, file_path: str) -> None:
        """Remove a file entry from the project catalog."""
```

Example Project Catalog entry:

```yaml
- path: "src/utils/time.js"
  functions:
    - "formatDate"
    - "parseTimestamp"
  tracking:
    json_representation: false
    system_map_updated: false
```

### Feature Catalog (Task Context Mapping)

The `feature_catalog.yaml` file organizes code by feature across multiple files.

```python
class FeatureCatalog:
    """Manages the feature catalog."""
    
    catalog_path: str
    
    def load(self) -> List[Dict[str, Any]]:
        """Load the feature catalog from the YAML file."""
        
    def save(self, catalog: List[Dict[str, Any]]) -> None:
        """Save the feature catalog to the YAML file."""
        
    def add_feature(self, feature_name: str, files: List[Dict[str, Any]]) -> None:
        """Add a new feature to the catalog."""
        
    def update_feature(self, feature_name: str, files: List[Dict[str, Any]]) -> None:
        """Update a feature in the catalog."""
        
    def get_feature(self, feature_name: str) -> Optional[Dict[str, Any]]:
        """Get a feature from the catalog."""
        
    def remove_feature(self, feature_name: str) -> None:
        """Remove a feature from the catalog."""
```

Example Feature Catalog entry:

```yaml
- feature: "User Authentication"
  files:
    - path: "src/auth/login.js"
      functions:
        - "validateCredentials"
        - "createSession"
    - path: "src/models/user.js"
      classes:
        - "User"
        - "AuthenticationService"
          methods:
            - "verify"
            - "generateToken"
```

## Data Persistence Models

### SQLite Schema

The SQLite database is used for local storage of blueprint metadata and cache references:

#### Blueprints Table
- `id`: UUID primary key
- `name`: String, blueprint name
- `type`: String, blueprint type (path, method)
- `creation_date`: Timestamp
- `last_updated`: Timestamp

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
