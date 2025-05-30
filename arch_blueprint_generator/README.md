# Architectum Blueprint Generator

## Overview

The Architectum Blueprint Generator is a core module that transforms codebases into navigable networks serving both AI assistants and human developers. This module implements a dual representation approach: a **Relationship Map** for efficient navigation and **JSON Mirrors** for detailed content access, which are then used to generate specialized **Blueprints** for different use cases.

## Architecture

Architectum employs a three-component architecture:

### 1. Relationship Map
A graph-based representation optimized for navigation and relationship discovery:
- Implements nodes representing code entities (files, functions, classes, methods)
- Defines relationships between nodes (contains, calls, imports, inherits)
- Optimized for traversal and querying operations
- Enables efficient cross-architectural navigation

### 2. JSON Mirrors
A parallel file structure that mirrors the original codebase with JSON representations:
- Creates and maintains JSON representations of source files
- Preserves detailed content and structure information
- Provides quick access to specific file components
- Enables detailed content analysis without parsing original files

### 3. Blueprints
Specialized views assembled from the core representations for specific purposes:
- **Path-Based Blueprints**: Analyze directory structures with configurable depth
- **File-Based Blueprints**: Focus on specific collections of files
- **Method-Based Blueprints**: Examine specific methods, functions, or classes

## Blueprint Types

### Path-Based Blueprint
Analyzes directory structures with configurable depth settings:
```bash
# Analyze entire directory tree
arch blueprint path /src/components --depth 0

# Analyze only immediate subdirectories
arch blueprint path /src/components --depth 1
```

### File-Based Blueprint
Focuses on explicitly specified files:
```bash
# Generate blueprint for specific files
arch blueprint file src/auth.py src/models/user.py --output auth_blueprint.json
```

### Method-Based Blueprint
Examines specific methods, functions, or classes within files:
```bash
# Focus on specific methods (requires YAML definition)
arch blueprint create --yaml auth_methods.yaml
```

## Detail Levels

All blueprints support three configurable detail levels:

- **Minimal**: Basic structure and relationship information only
- **Standard**: Essential information including types and basic metadata (default)
- **Detailed**: Comprehensive information including documentation and full metadata

```bash
# Generate with minimal detail for AI token efficiency
arch blueprint file auth.py --detail-level minimal

# Generate with detailed information for comprehensive analysis
arch blueprint file auth.py --detail-level detailed
```

## YAML Configuration

Blueprints can be defined declaratively using YAML files:

```yaml
# auth_blueprint.yaml
type: method
name: "Authentication System"
description: "Core authentication methods and classes"
persistence: feature
detail_level: standard
components:
  - file: "src/auth/login.py"
    elements: ["validate_credentials", "create_session"]
  - file: "src/models/user.py"
    elements: ["User", "authenticate"]
```

Generate from YAML:
```bash
arch blueprint create --yaml auth_blueprint.yaml --output auth_system.json
```

## Synchronization Workflow

Architectum uses explicit synchronization to keep representations up to date with code changes:

```bash
# Sync current directory
arch sync .

# Sync with recursive subdirectories
arch sync . --recursive

# Force full resynchronization
arch sync . --force

# Sync specific files
arch sync src/auth.py src/models/user.py
```

The sync process:
1. Detects file changes using hash comparison
2. Performs incremental updates to both representations
3. Maintains relationship integrity during updates
4. Provides status feedback on changes processed

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

## Usage Examples

### Basic Scanning
```bash
# Scan current directory with standard detail
arch scan .

# Scan with unlimited depth and detailed information
arch scan /src --depth 0 --detail-level detailed

# Save representations to output directory
arch scan /src --output ./architectum_output
```

### Blueprint Generation
```bash
# File-based blueprint
arch blueprint file src/auth.py src/models/user.py \
  --detail-level standard \
  --format json \
  --output auth_blueprint.json

# Create from YAML definition
arch blueprint create --yaml feature_definitions/auth.yaml \
  --format xml \
  --output auth_system.xml
```

### Programmatic Usage
```python
from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors
from arch_blueprint_generator.models.nodes import FileNode, FunctionNode
from arch_blueprint_generator.blueprints.factory import BlueprintFactory
from arch_blueprint_generator.models.detail_level import DetailLevel

# Initialize the dual representation
relationship_map = RelationshipMap()
json_mirrors = JSONMirrors("path/to/source")

# Add nodes to the relationship map
file_node = FileNode("file1", "path/to/file1.py", ".py")
function_node = FunctionNode("func1", "my_function")
relationship_map.add_node(file_node)
relationship_map.add_node(function_node)

# Create JSON mirror for a file
from arch_blueprint_generator.models.json_mirrors import CodeElement
code_element = CodeElement("my_function", "function", 10, 25)
json_mirrors.create_file_mirror(
    "path/to/file1.py",
    {"my_function": code_element},
    ["imported_module.py"]
)

# Generate a file-based blueprint
blueprint = BlueprintFactory.create_file_blueprint(
    relationship_map,
    json_mirrors,
    ["path/to/file1.py"],
    detail_level=DetailLevel.STANDARD
)
blueprint.generate()

# Export blueprint
blueprint_json = blueprint.to_json()
blueprint.save("output.json", format="json")
```

## Blueprint Persistence

Blueprints can be saved as persistent documentation or used temporarily:

- **Feature Blueprints**: Saved permanently as documentation of codebase features
- **Temporary Blueprints**: Generated for immediate analysis and automatically cleaned up

Specify persistence in YAML:
```yaml
persistence: feature  # or "temporary"
```

## Output Formats

Blueprints can be generated in multiple formats:

- **JSON**: Default format, optimized for programmatic processing and AI consumption
- **XML**: Alternative format for systems that require XML structure

```bash
# JSON output (default)
arch blueprint file auth.py --format json

# XML output  
arch blueprint file auth.py --format xml
```

## Core Benefits

The dual representation approach provides several advantages:

- **Efficient Navigation**: The graph structure enables quick traversal and relationship analysis
- **Detailed Content Access**: JSON mirrors provide detailed information about specific code elements
- **Flexible Blueprint Generation**: Combine elements from both representations for specialized views
- **Incremental Updates**: Only changed files need to be reprocessed during synchronization
- **Token-Efficient Representations**: JSON format optimized for AI assistant consumption
- **Human Visualization**: Graph-compatible outputs for human navigation tools

## Installation & Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize Architectum in a project
cd /path/to/your/project
arch scan . --output .architectum

# Generate your first blueprint
arch blueprint file main.py --detail-level standard
```

## Integration with Development Workflow

Architectum can be integrated into development workflows:

```bash
# Git hook example - sync on commit
git add .git/hooks/post-commit
echo "arch sync . --recursive" > .git/hooks/post-commit
chmod +x .git/hooks/post-commit

# CI/CD integration - validate blueprint accuracy
arch sync . --recursive
arch blueprint create --yaml ci/validation.yaml --output validation_blueprint.json
```

## Getting Started

1. **Scan your codebase**: Start with `arch scan .` to create initial representations
2. **Experiment with blueprints**: Try different blueprint types with `arch blueprint file`
3. **Create YAML definitions**: Define reusable blueprints for important features
4. **Integrate sync workflow**: Use `arch sync` to keep representations current
5. **Explore detail levels**: Adjust detail levels based on your use case (AI vs human consumption)

For more detailed information, see the [Architecture Documentation](../docs/core_documents/architecture.md) and [Product Requirements Document](../docs/core_documents/prd.md).

---

*"Structure first, implementation second. Architectum reveals the invisible relationships that define how software really works."*