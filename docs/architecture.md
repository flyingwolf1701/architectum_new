# Architectum Architecture Document

## 1. Architecture Overview

Architectum is a code comprehension system designed to transform codebases into navigable networks that serve both AI assistants and human developers. This document outlines the technical architecture of Architectum, focusing on its core components, data models, and interactions.

### 1.1 High-Level Architecture

Architectum employs a multi-layered architecture with two core representations:
1. A **Relationship Map** - A graph model capturing relationships between code elements
2. **JSON Mirrors** - A parallel file structure that mirrors the original codebase with JSON representations of each file

These core representations are then used to generate various types of **Blueprints** - specialized views assembled for specific purposes.

```mermaid
graph TD
    classDef coreComponents fill:#f3bf,stroke:#333,stroke-width:2px
    classDef interfaces fill:#b1bf,stroke:#333,stroke-width:1px
    classDef dataStores fill:#b1fb,stroke:#333,stroke-width:1px
    classDef blueprints fill:#b1ff,stroke:#333,stroke-width:1px

    A[Code Files] --> B[Parser Layer]
    B --> C[Relationship Map]:::coreComponents
    B --> M[JSON Mirrors]:::coreComponents
    C <--> M
    
    C --> BP[Blueprint Generator]:::coreComponents
    M --> BP
    
    BP --> FB[File-Based Blueprint]:::blueprints
    BP --> CB[Component-Based Blueprint]:::blueprints
    BP --> FEB[Feature Blueprint]:::blueprints
    BP --> TB[Temporary Blueprint]:::blueprints
    
    FB --> E[Serialization Layer]
    CB --> E
    FEB --> E
    TB --> E
    E --> F[Output Formats]
    
    G[API/CLI Interface]:::interfaces --> B
    G --> BP
    
    C <--> H[Blueprint Cache]:::dataStores
    
    I[LSP Integration]:::interfaces --> B
    
    J[Visualization Engine]:::interfaces --> F
    
    K[Arch Sync Command]:::interfaces --> B
    K --> C
    K --> M
    
    Y[YAML Blueprint Definitions]:::dataStores --> BP
    
    L[VSCode Extension]:::interfaces --> K
    
    N[Change Tracker]:::dataStores <--> K
```

The architecture consists of:

1. **Parser Layer**: Extracts code structure and relationships from source files, optionally leveraging LSP
2. **Relationship Map**: Represents code as a network of nodes and relationships
3. **JSON Mirrors**: Maintains a mirrored JSON representation of each file in the codebase
4. **Blueprint Generator**: Creates different types of blueprints based on the core representations
5. **Blueprint Types**:
   - **File-Based Blueprint**: Combines selected files for comprehensive context
   - **Component-Based Blueprint**: Focuses on specific functions/classes within files
   - **Feature Blueprint**: Persistent documentation of a complete feature
   - **Temporary Blueprint**: Ad-hoc creation for immediate development tasks
6. **Serialization Layer**: Converts blueprints to various output formats
7. **API/CLI Interface**: Provides interaction points for users and other systems
8. **Blueprint Cache**: Stores generated blueprints for incremental updates
9. **LSP Integration**: Optional enhancement for more accurate relationship extraction
10. **Visualization Engine**: Renders graph-based blueprints for human consumption
11. **Arch Sync Command**: CLI tool and API for synchronizing code with its Architectum representation
12. **VSCode Extension**: IDE integration for synchronizing files with Architectum
13. **Change Tracker**: Tracks which files need synchronization
14. **YAML Blueprint Definitions**: Configuration files defining blueprint contents

### 1.2 Core Design Principles

Architectum's architecture is guided by the following principles:

- **Dual Core Representation**: Code is represented both as a relationship map (for navigation efficiency) and as JSON mirrors (for detailed content)
- **Blueprint Assembly**: Blueprints are specialized views that combine elements from the core representations based on use cases
- **Declarative Blueprint Definition**: YAML files provide a clear way to define what belongs in a blueprint
- **Developer-Controlled Synchronization**: Developers explicitly control when to synchronize code with Architectum using the `arch sync` command
- **Incremental Processing**: Changes should only regenerate affected portions of representations
- **Format Flexibility**: Internal processing uses JSON but supports transformation to other formats
- **Extension Points**: Clear interfaces for adding new languages, blueprint types, and features

## 2. Core Components

### 2.1 JSON Mirrors

Architectum maintains JSON mirrors that represent each file in the codebase.

#### 2.1.1 Mirror Structure Model

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

#### 2.1.2 JSON Mirror Example

```json
{
  "path": "src/services/user_service.py",
  "extension": ".py",
  "elements": {
    "UserService": {
      "name": "UserService",
      "type": "class",
      "line_start": 10,
      "line_end": 50,
      "methods": ["get_user", "update_user"],
      "properties": ["db_client"]
    },
    "get_user": {
      "name": "get_user",
      "type": "method",
      "line_start": 15,
      "line_end": 25,
      "parent": "UserService",
      "parameters": [{"name": "user_id", "type": "str"}],
      "return_type": "User"
    }
  },
  "imports": ["src/models/user.py", "src/database/client.py"]
}
```

#### 2.1.3 Directory Information Example

```json
{
  "path": "src/services",
  "files": ["user_service.py", "auth_service.py"],
  "subdirectories": ["utils"]
}
```

### 2.2 Relationship Map

The Relationship Map is the central component for navigation, representing code as a directed graph of nodes and relationships.

#### 2.2.1 Node Types

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

#### 2.2.2 Relationship Types

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

#### 2.2.3 Graph Operations

The Graph Model provides operations for:

- **Node and Relationship CRUD**: Create, read, update, and delete nodes and relationships
- **Traversal**: Navigate the graph structure in any direction
- **Filtering**: Select nodes and relationships based on criteria
- **Subgraph Extraction**: Create focused views for specific blueprint types
- **Serialization**: Convert to/from JSON representation
- **Caching**: Store and retrieve graph state

### 2.3 Parser Layer

The Parser Layer analyzes source code files to extract structural information and relationship data.

#### 2.3.1 Language-Specific Parsers

```python
class Parser:
    """Base interface for language-specific parsers."""
    
    def parse_file(self, file_path: str, detail_level: DetailLevel) -> Tuple[List[Node], FileContent]:
        """Parse a file and return extracted nodes and file content."""
        
    def detect_relationships(self, nodes: List[Node], detail_level: DetailLevel) -> List[Relationship]:
        """Detect relationships between nodes."""

class PythonParser(Parser):
    """Parser implementation for Python files."""
    
class JavaScriptParser(Parser):
    """Parser implementation for JavaScript/TypeScript files."""
```

#### 2.3.2 LSP Integration (Optional Enhancement)

```python
class LSPClient:
    """Client for communicating with language servers."""
    
    def connect_to_server(self, language: str) -> bool:
        """Connect to appropriate language server."""
        
    def get_document_symbols(self, file_path: str) -> Dict[str, Any]:
        """Get symbols from a document via LSP."""
        
    def get_call_hierarchy(self, position: Position) -> Dict[str, Any]:
        """Get call hierarchy for a position via LSP."""
```

### 2.4 Blueprint Types

Architectum generates specialized blueprint types based on the core representations.

#### 2.4.1 Blueprint Base Class

```python
class Blueprint:
    """Base class for all blueprint types."""
    
    relationship_map: RelationshipMap
    json_mirrors: JSONMirrors
    
    def to_json(self) -> Dict[str, Any]:
        """Convert blueprint to JSON representation."""
        
    def to_xml(self) -> str:
        """Convert blueprint to XML representation."""
```

#### 2.4.2 File-Based Blueprint

```python
class FileBasedBlueprint(Blueprint):
    """Blueprint focusing on entire files."""
    
    file_paths: List[str]
    
    def generate(self) -> None:
        """Generate blueprint for the specified files."""
```

#### 2.4.3 Component-Based Blueprint

```python
class ComponentBasedBlueprint(Blueprint):
    """Blueprint focusing on specific components within files."""
    
    components: Dict[str, List[str]]  # Maps file paths to component names
    
    def generate(self) -> None:
        """Generate blueprint for the specified components."""
```

#### 2.4.4 Feature Blueprint

```python
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
```

#### 2.4.5 Temporary Blueprint

```python
class TemporaryBlueprint(Blueprint):
    """Ad-hoc blueprint for immediate development tasks."""
    
    components: Dict[str, List[str]]  # Maps file paths to component names
    
    def generate(self) -> None:
        """Generate blueprint for temporary use."""
        
    def clear(self) -> None:
        """Clear the temporary blueprint after use."""
```

#### 2.4.6 YAML Blueprint Definition

Architectum uses YAML files to define blueprints:

```yaml
# Feature Blueprint: User Authentication
type: feature  # or file, component, temporary
name: user-authentication
description: "All components related to user authentication flow"
persistence: persistent  # or "temporary"

# Components to include
components:
  - file: src/auth/login.js
    # Empty elements means include entire file
    elements: []
  
  - file: src/auth/register.js
    elements: []
  
  - file: src/models/user.js
    elements:
      - validateCredentials
      - hashPassword
      - comparePasswords
  
  - file: src/utils/security.js
    elements:
      - generateToken
      - verifyToken
```

### 3.1 Blueprint CLI Commands

```python
@click.group()
def cli():
    """Architectum CLI for code comprehension and AI assistance."""

@cli.group()
def blueprint():
    """Generate blueprints from code."""

@blueprint.command('file')
@click.argument('files', nargs=-1, required=True)
@click.option('--output', default='-', help='Output file (- for stdout)')
@click.option('--format', default='json', help='Output format')
def file_blueprint(files, output, format):
    """Generate blueprint for specified files."""
    
@blueprint.command('component')
@click.option('--file', '-f', multiple=True, required=True, help='Source file path')
@click.option('--component', '-c', multiple=True, required=True, help='Component name within file')
@click.option('--output', default='-', help='Output file (- for stdout)')
@click.option('--format', default='json', help='Output format')
def component_blueprint(file, component, output, format):
    """Generate blueprint for specific components."""
    
@blueprint.command('feature')
@click.option('--yaml', required=True, help='YAML blueprint definition file')
@click.option('--output', default='-', help='Output file (- for stdout)')
@click.option('--format', default='json', help='Output format')
def feature_blueprint(yaml, output, format):
    """Generate blueprint from YAML definition."""
    
@blueprint.command('temporary')
@click.option('--yaml', required=True, help='YAML blueprint definition file')
@click.option('--output', default='-', help='Output file (- for stdout)')
@click.option('--format', default='json', help='Output format')
def temporary_blueprint(yaml, output, format):
    """Generate temporary blueprint from YAML definition."""
```

### 3.2 Blueprint API Interface

```python
def create_file_blueprint(file_paths: List[str], output_format: str = 'json') -> Union[Dict[str, Any], str]:
    """
    Create a file-based blueprint.
    
    Args:
        file_paths: List of file paths to include
        output_format: Format to return (json, xml)
        
    Returns:
        Blueprint in the requested format
    """

def create_component_blueprint(components: Dict[str, List[str]], output_format: str = 'json') -> Union[Dict[str, Any], str]:
    """
    Create a component-based blueprint.
    
    Args:
        components: Dictionary mapping file paths to component names
        output_format: Format to return (json, xml)
        
    Returns:
        Blueprint in the requested format
    """
    
def create_blueprint_from_yaml(yaml_path: str, output_format: str = 'json') -> Union[Dict[str, Any], str]:
    """
    Create a blueprint from a YAML definition.
    
    Args:
        yaml_path: Path to YAML definition file
        output_format: Format to return (json, xml)
        
    Returns:
        Blueprint in the requested format
    """
```

## 4. Human and AI Workflows

### 4.1 Human Developer Workflow

```mermaid
graph TD
    A[Edit Code in IDE] --> B{Save Changes}
    B --> C[Continue Development]
    B --> D[Sync with Architectum]
    D --> E[IDE Extension: Sync Current File]
    D --> F[CLI: arch sync]
    E --> H[Architectum Updates Representations]
    F --> H
    H --> I[Updated Relationship Map & JSON Mirrors]
    
    J[Need Code Understanding] --> K[Create Blueprint]
    K --> L[CLI: arch blueprint]
    K --> M[YAML Definition]
    L --> N[Blueprint Generated]
    M --> N
    N --> O[AI Analysis with Blueprint Context]
    O --> P[Continue Development with Insights]
    P --> A
```

### 4.2 AI Agent Workflow

```mermaid
graph TD
    A[Receive Task to Modify Code] --> B[Access Core Representations]
    B --> C[Create Blueprint for Context]
    C --> D[YAML Definition or API Call]
    D --> E[Blueprint Generated]
    E --> F[Analyze Code with Blueprint Context]
    F --> G[Write/Modify Code]
    G --> H[Save File]
    H --> I[Call architectum_sync_file API]
    I --> J[Architectum Updates Representations]
    J --> K[Continue Development with Updated Context]
    K --> C
```

### 4.3 Feature Documentation Workflow

```mermaid
graph TD
    A[Complete Feature Development] --> B[Define Feature Blueprint]
    B --> C[Create YAML Definition]
    C --> D[Generate Feature Blueprint]
    D --> E[Save as Persistent Documentation]
    E --> F[Add to Project Documentation]
    
    G[New Developer Joins Team] --> H[Reviews Feature Blueprints]
    H --> I[Selects Feature to Understand]
    I --> J[Views Feature Blueprint]
    J --> K[Faster Understanding of Codebase]
    K --> L[Begin Development with Context]
```

## 5. Technical Implementation

### 5.1 Technology Stack

- **Primary Language**: Python 3.9+
- **Graph Library**: NetworkX or custom implementation
- **CLI Framework**: Click
- **API Framework** (optional): Flask/FastAPI
- **Serialization**: JSON (primary), XML (for AI consumption)
- **VSCode Extension**: TypeScript
- **Testing**: pytest, hypothesis, pact
- **Documentation**: Sphinx

### 5.2 Module Organization

```
architectum/
├── arch_blueprint_generator/
│   ├── __init__.py
│   ├── models/                   # Core data models
│   │   ├── __init__.py
│   │   ├── relationship_map.py   # Relationship map model
│   │   ├── json_mirrors.py       # JSON mirrors model
│   │   └── nodes.py              # Node and relationship types
│   ├── parsers/                  # Code parsing
│   │   ├── __init__.py
│   │   ├── python_parser.py     # Python-specific parser
│   │   └── javascript_parser.py # JavaScript/TypeScript parser
│   ├── blueprints/               # Blueprint types
│   │   ├── __init__.py
│   │   ├── base.py              # Blueprint base class
│   │   ├── file_based.py        # File-based blueprint
│   │   ├── component_based.py   # Component-based blueprint
│   │   ├── feature.py           # Feature blueprint
│   │   └── temporary.py         # Temporary blueprint
│   ├── navigation/               # Navigation components
│   │   ├── __init__.py
│   │   ├── file_navigator.py    # JSON mirror navigation
│   │   └── graph_navigator.py   # Relationship map navigation
│   ├── yaml/                     # YAML processing
│   │   ├── __init__.py
│   │   └── blueprint_config.py  # YAML blueprint configuration
│   ├── formatters/               # Output formatting
│   │   ├── __init__.py
│   │   ├── json_formatter.py    # JSON output
│   │   └── xml_formatter.py     # XML output
│   ├── cache/                    # Caching system
│   │   ├── __init__.py
│   │   └── blueprint_cache.py   # Blueprint caching
│   ├── sync/                     # Synchronization components
│   │   ├── __init__.py
│   │   ├── arch_sync.py         # arch sync implementation
│   │   └── change_tracker.py    # Change tracking
│   ├── cli/                      # Command-line interface
│   │   ├── __init__.py
│   │   └── commands.py          # CLI commands
│   └── api/                      # API interface (optional)
│       ├── __init__.py
│       └── routes.py            # API endpoints
├── vscode-extension/            # VSCode extension
│   ├── src/                     # Extension source code
│   └── package.json             # Extension manifest
├── tests/                        # Testing
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   ├── contracts/                # Contract tests
│   └── snapshots/                # Snapshot tests
└── docs/                         # Documentation
```

## 6. Extension Points

Architectum is designed for extensibility in key areas:

### 6.1 New Languages

New language support can be added by implementing the Parser interface:

```python
class SwiftParser(Parser):
    """Parser implementation for Swift files."""
    
    def parse_file(self, file_path: str) -> Tuple[List[Node], FileContent]:
        """Parse a Swift file and return extracted nodes and file content."""
        
    def detect_relationships(self, nodes: List[Node]) -> List[Relationship]:
        """Detect relationships between Swift nodes."""
```

### 6.2 New Blueprint Types

Additional blueprint types can be created by extending the Blueprint base class:

```python
class CustomBlueprint(Blueprint):
    """Custom blueprint for specific needs."""
    
    def generate(self) -> None:
        """Generate the custom blueprint."""
```

### 6.3 New Output Formats

Support for new output formats can be added by implementing the OutputFormatter interface:

```python
class GraphMLFormatter(OutputFormatter):
    """Format blueprint as GraphML for visualization tools."""
    
    def format(self, blueprint: Blueprint) -> str:
        """Format blueprint as GraphML."""
```

## 7. Future Enhancements

### 7.1 Enhanced LSP Integration

- Deeper integration with Language Server Protocol
- Real-time updates as code is edited
- More accurate relationship detection

### 7.2 Git Integration

- Post-commit hooks for automatic synchronization
- Branch-aware blueprint generation
- Diff-based incremental updates

### 7.3 Props Tracking

- Track component property flow across React/Vue components
- Identify prop origins and prop usage
- Visualize prop flow in the relationship map

### 7.4 Advanced Feature Tagging

- AI-assisted feature boundary detection
- Automatic tagging based on naming conventions
- Feature tag propagation through relationships

### 7.5 Interactive Visualization

- Web-based graph visualization
- Interactive navigation through the codebase
- Custom views and filtering

## Change Log

| Change        | Date       | Version | Description                    | Author         |
| ------------- | ---------- | ------- | ------------------------------ | -------------- |
| Initial draft | 05-17-2025 | 0.1     | Initial architecture document  | System Architect |
| Update        | 05-17-2025 | 0.2     | Added arch sync workflow       | System Architect |
| Revision      | 05-17-2025 | 0.3     | Refined blueprint types and core representations | System Architect |