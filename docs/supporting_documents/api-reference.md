# API Reference

This document provides a comprehensive reference for Architectum's API, including both CLI commands and programmatic interfaces. Use this guide to interact with Architectum's blueprint generation and management capabilities.

## CLI Commands

Architectum provides a command-line interface for generating and managing blueprints:

### Main Command Groups

```
arch
├── blueprint
│   ├── file - Generate File-Based Blueprints
│   ├── component - Generate Component-Based Blueprints
│   ├── feature - Generate Feature Blueprints
│   ├── temporary - Generate Temporary Blueprints
│   ├── create - Create blueprint from YAML definition
│   ├── list - List available blueprints
│   ├── get - Retrieve a blueprint by name
│   └── diff - Compare blueprint versions
└── sync - Synchronize code changes with Architectum representations
```

### Blueprint Commands

#### File-Based Blueprints

```bash
# Generate blueprint for specified files
arch blueprint file [OPTIONS] FILES...

Options:
  --output TEXT       Output file (- for stdout)
  --format TEXT       Output format (json, xml)
  --detail-level TEXT Detail level (minimal, standard, detailed)
  --help              Show help message

Examples:
  arch blueprint file src/main.py src/utils.py
  arch blueprint file src/auth/*.js --output auth-blueprint.json --detail-level detailed
```

#### Component-Based Blueprints

```bash
# Generate blueprint for specific components
arch blueprint component [OPTIONS]

Options:
  --file, -f TEXT      Source file path (can be specified multiple times)
  --component, -c TEXT Component name within file (can be specified multiple times)
  --output TEXT        Output file (- for stdout)
  --format TEXT        Output format (json, xml)
  --detail-level TEXT  Detail level (minimal, standard, detailed)
  --relationship-depth INTEGER  How many levels of relationships to include
  --cross-file BOOLEAN Whether to include components from other files
  --cross-file-depth INTEGER How many files away to analyze
  --help               Show help message

Examples:
  arch blueprint component -f src/auth.py -c authenticate -c validate
  arch blueprint component -f src/auth.py -c authenticate --relationship-depth 2 --cross-file true
```

#### Feature Blueprints

```bash
# Generate persistent blueprint from YAML definition
arch blueprint feature [OPTIONS]

Options:
  --yaml TEXT         YAML blueprint definition file
  --output TEXT       Output file (- for stdout)
  --format TEXT       Output format (json, xml)
  --help              Show help message

Examples:
  arch blueprint feature --yaml auth-feature.yaml
  arch blueprint feature --yaml auth-feature.yaml --output auth-feature.json
```

#### Create Blueprint from YAML

```bash
# Create blueprint from YAML definition
arch blueprint create [OPTIONS]

Options:
  --yaml, -f TEXT     YAML blueprint definition file
  --output TEXT       Output file (- for stdout)
  --format TEXT       Output format (json, xml)
  --help              Show help message

Examples:
  arch blueprint create -f blueprint.yaml
  arch blueprint create -f blueprint.yaml --output blueprint.json
```

#### List Blueprints

```bash
# List available blueprints
arch blueprint list [OPTIONS]

Options:
  --type TEXT         Filter by blueprint type
  --help              Show help message

Examples:
  arch blueprint list
  arch blueprint list --type feature
```

#### Get Blueprint

```bash
# Retrieve a blueprint by name
arch blueprint get [OPTIONS]

Options:
  --name, -n TEXT     Blueprint name
  --version, -v TEXT  Blueprint version (latest if not specified)
  --output TEXT       Output file (- for stdout)
  --format TEXT       Output format (json, xml)
  --help              Show help message

Examples:
  arch blueprint get -n auth-feature
  arch blueprint get -n auth-feature -v 1.2 --output auth-v1.2.json
```

#### Compare Blueprint Versions

```bash
# Compare blueprint versions
arch blueprint diff [OPTIONS]

Options:
  --name, -n TEXT      Blueprint name
  --version1, -v1 TEXT First version
  --version2, -v2 TEXT Second version
  --output TEXT        Output file (- for stdout)
  --help               Show help message

Examples:
  arch blueprint diff -n auth-feature -v1 1.0 -v2 2.0
  arch blueprint diff -n auth-feature -v1 1.0 -v2 2.0 --output auth-diff.json
```

### Synchronization Commands

```bash
# Synchronize code changes with Architectum
arch sync [OPTIONS]

Options:
  --file, -f TEXT     File to synchronize (can be specified multiple times)
  --directory, -d TEXT Directory to synchronize
  --status            Show sync status
  --help              Show help message

Examples:
  arch sync --file src/auth.py
  arch sync --directory src/
  arch sync --status
```

## Programmatic API

Architectum can also be used programmatically in Python applications:

### Blueprint Generation

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

### Blueprint Management

```python
def get_blueprint(name: str, version: Optional[str] = None) -> Union[Dict[str, Any], None]:
    """
    Retrieve a blueprint by name and optional version.
    
    Args:
        name: Blueprint name
        version: Optional version (latest if not specified)
        
    Returns:
        Blueprint if found, None otherwise
    """
    
def list_blueprints(blueprint_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List available blueprints with optional type filter.
    
    Args:
        blueprint_type: Optional blueprint type to filter (file, component, feature, temporary)
        
    Returns:
        List of blueprint metadata
    """
    
def diff_blueprints(name: str, version1: str, version2: str) -> Dict[str, Any]:
    """
    Compare two versions of a blueprint.
    
    Args:
        name: Blueprint name
        version1: First version
        version2: Second version
        
    Returns:
        Differences between the two versions
    """
```

### Synchronization

```python
def sync_file(file_path: str) -> bool:
    """
    Synchronize a file with Architectum representations.
    
    Args:
        file_path: Path to file
        
    Returns:
        True if successful, False otherwise
    """
    
def sync_directory(directory_path: str) -> Dict[str, bool]:
    """
    Synchronize a directory with Architectum representations.
    
    Args:
        directory_path: Path to directory
        
    Returns:
        Dictionary mapping file paths to sync status
    """
    
def get_sync_status() -> Dict[str, Any]:
    """
    Get synchronization status for tracked files.
    
    Returns:
        Dictionary with sync status information
    """
```

## YAML Blueprint Definition Format

Architectum uses YAML files to define blueprints. The format is as follows:

```yaml
# Common fields for all blueprint types
type: file  # or component, feature, temporary
name: auth-system-blueprint
description: "Core authentication system files"
persistence: temporary  # or persistent
detail_level: standard  # or minimal, detailed

# For File-Based Blueprints
components:
  - file: src/auth/login.js
    # Empty elements means include entire file
    elements: []
  
  - file: src/auth/register.js
    elements: []

# For Component-Based Blueprints (additional fields)
relationship_depth: 2
cross_file: true
cross_file_depth: 1

# For Feature Blueprints (additional fields)
owner: "Auth Team"
tags: ["security", "user-management"]
documentation:
  overview: |
    The authentication system provides secure user login, registration,
    and credential management.
  usage: |
    Authentication can be triggered from the login page or any
    secured route.
  sections:
    - title: "Security Considerations"
      content: |
        Passwords are hashed using bcrypt with work factor 12.
        Rate limiting is implemented to prevent brute force attacks.
```

## Error Handling

All API methods and CLI commands follow a consistent error handling approach:

- **Business Errors**: Inherit from `BusinessError` with `code`, `message`, and `details` fields
- **HTTP Errors**: Translated to specific exception types (e.g., `ApiNotFoundError`, `ApiServerError`)
- **Validation Errors**: Detailed messages about what failed validation
