# Architectum Blueprint Generator

## Overview

The Architectum Blueprint Generator is a core module that transforms codebases into navigable networks serving both AI assistants and human developers. This module implements the dual representation approach: a Relationship Map and JSON Mirrors structure.

## Dual Representation Approach

Architectum employs a multi-layered architecture with two core representations:

1. **Relationship Map**: A graph model capturing relationships between code elements
   - Implements nodes representing code entities (files, functions, classes)
   - Defines relationships between nodes (contains, calls, imports)
   - Optimized for navigation and relationship analysis
   - Provides efficient traversal and querying operations

2. **JSON Mirrors**: A parallel file structure that mirrors the original codebase with JSON representations
   - Creates and maintains JSON representations of source files
   - Preserves detailed content and structure information
   - Provides quick access to specific file components
   - Enables detailed content analysis

These core representations are then used to generate various types of Blueprints - specialized views assembled for specific purposes.

## Core Components

### Node Types

The Relationship Map includes various node types:

- **FileNode**: Represents a file in the codebase
- **DirectoryNode**: Represents a directory in the codebase
- **FunctionNode**: Represents a function in the codebase
- **ClassNode**: Represents a class in the codebase
- **MethodNode**: Represents a method in a class
- **FeatureNode**: Represents a virtual feature grouping

### Relationship Types

The Relationship Map defines different relationship types:

- **ContainsRelationship**: Represents a containment relationship
- **CallsRelationship**: Represents a function call relationship
- **ImportsRelationship**: Represents a file import relationship
- **InheritsRelationship**: Represents a class inheritance relationship
- **ImplementsRelationship**: Represents a function implementing a feature

### JSON Mirror Components

The JSON Mirrors structure includes:

- **CodeElement**: Represents a code element within a file
- **FileContent**: Represents the content of a file
- **DirectoryContent**: Represents the content of a directory
- **JSONMirrors**: Container class managing the mirror representations

## Usage

Blueprint generation and file synchronization can be performed through the CLI:

```bash
# Generate a blueprint from specified files
architectum blueprint file1.py file2.py --output blueprint.json

# Synchronize code files with Architectum
architectum sync --recursive
```

## Development Workflow

Architectum follows this general workflow:

1. Analyze source code files to extract structural information
2. Build and maintain the dual representation (Relationship Map and JSON Mirrors)
3. Generate blueprints based on specific needs
4. Update representations when code changes

## Core Benefits

The dual representation approach provides several advantages:

- **Efficient Navigation**: The graph structure enables quick traversal and relationship analysis
- **Detailed Content Access**: JSON mirrors provide detailed information about specific code elements
- **Flexible Blueprint Generation**: Combine elements from both representations for specialized views
- **Incremental Updates**: Only changed files need to be reprocessed

## Getting Started

To use the Architectum Blueprint Generator:

```python
from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors
from arch_blueprint_generator.models.nodes import FileNode, FunctionNode

# Initialize the dual representation
relationship_map = RelationshipMap()
json_mirrors = JSONMirrors("path/to/source")

# Add nodes to the relationship map
file_node = FileNode("file1", "path/to/file1.py", ".py")
function_node = FunctionNode("func1", "my_function")
relationship_map.add_node(file_node)
relationship_map.add_node(function_node)

# Create JSON mirror for a file
json_mirrors.create_file_mirror(
    "path/to/file1.py",
    {"my_function": code_element},
    ["imported_module.py"]
)
```
