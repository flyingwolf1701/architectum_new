# Coding Standards

This document outlines the coding standards and best practices for the Architectum project. All contributors should adhere to these guidelines to maintain code quality and consistency.

## Python Coding Style

### General Guidelines

- Follow [PEP 8](https://pep8.org/) style guide for Python code
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (compatible with Black)
- Use meaningful variable and function names
- Write docstrings for all public functions, classes, and methods

### Formatting
We use [Ruff](https://github.com/astral-sh/ruff) as the code formatter with a line length of 88 characters:

```bash
# Format a single file
ruff format arch_blueprint_generator/module.py

# Format the entire project
ruff format arch_blueprint_generator/
```

### Import Order

We use [isort](https://github.com/pycqa/isort) for organizing imports:

```python
# Standard library imports
import os
import sys
from typing import Dict, List, Optional

# Third-party imports
import click
import networkx as nx
from fastapi import FastAPI

# Local application imports
from arch_blueprint_generator.models import Node, Relationship
from arch_blueprint_generator.parsers import PythonParser
```

Configure isort to be compatible with Black:

```ini
# .isort.cfg
[settings]
profile = black
line_length = 88
```

### Type Annotations

- Use type hints for all function parameters and return values
- Use the built-in `typing` module
- Follow [PEP 484](https://www.python.org/dev/peps/pep-0484/) and [PEP 585](https://www.python.org/dev/peps/pep-0585/) guidelines

```python
def get_nodes(file_path: str, detail_level: str = "standard") -> List[Node]:
    """
    Extract nodes from a file.
    
    Args:
        file_path: Path to the file
        detail_level: Level of detail to extract
        
    Returns:
        List of Node objects
    """
    # Implementation...
```

### Testing

- Write unit tests for all public functions and methods
- Maintain at least 80% code coverage
- Use descriptive test names (test_<function>_<scenario>)
- One assertion per test when possible

```python
def test_parse_file_valid_python():
    """Test that a valid Python file is parsed correctly."""
    # Setup
    parser = PythonParser()
    file_path = "tests/fixtures/python/valid.py"
    
    # Execute
    nodes, content = parser.parse_file(file_path)
    
    # Assert
    assert len(nodes) > 0
    assert content.path == file_path
```

### Documentation

- Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Short description of function.
    
    More detailed description of the function,
    explaining its purpose and behavior.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is not an integer
        
    Examples:
        >>> function_name("test", 42)
        True
    """
```

## Error Handling

### Exception Hierarchy

- Use a custom exception hierarchy based on `ArchitectumError`:

```python
class ArchitectumError(Exception):
    """Base class for all Architectum exceptions."""
    pass

class ParseError(ArchitectumError):
    """Error while parsing code files."""
    pass

class BlueprintError(ArchitectumError):
    """Error while generating blueprints."""
    pass
```

### Business Exceptions

- Business exceptions should include `code`, `message`, and `details`:

```python
class BusinessError(ArchitectumError):
    """Base class for business logic errors."""
    
    def __init__(self, code: str, message: str, details: Optional[Dict] = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(message)
```

### Exception Handling

- Use context managers for resource management:

```python
def read_file(file_path: str) -> str:
    """Read file content, handling common errors."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileError(f"File not found: {file_path}")
    except PermissionError:
        raise FileError(f"Permission denied: {file_path}")
    except UnicodeDecodeError:
        raise FileError(f"Unable to decode file: {file_path}")
```

- Use explicit exception types rather than catching all exceptions:

```python
# Good
try:
    data = json.loads(content)
except json.JSONDecodeError:
    raise ParseError("Invalid JSON content")

# Bad
try:
    data = json.loads(content)
except Exception:  # Too broad!
    raise ParseError("Error parsing content")
```

## Code Organization

### Module Structure

- Each module should have a clear, single responsibility
- Keep modules small and focused
- Use meaningful and consistent naming

### Class Design

- Follow the single responsibility principle
- Use composition over inheritance
- Keep classes small and focused

```python
# Good
class Parser:
    """Base parser interface."""
    
    def parse_file(self, file_path: str) -> Tuple[List[Node], FileContent]:
        """Parse a file and return extracted nodes and file content."""
        raise NotImplementedError
    
    def detect_relationships(self, nodes: List[Node]) -> List[Relationship]:
        """Detect relationships between nodes."""
        raise NotImplementedError

class PythonParser(Parser):
    """Parser implementation for Python files."""
    
    def parse_file(self, file_path: str) -> Tuple[List[Node], FileContent]:
        """Parse a Python file."""
        # Implementation...
    
    def detect_relationships(self, nodes: List[Node]) -> List[Relationship]:
        """Detect relationships between Python nodes."""
        # Implementation...
```

### Function Design

- Functions should do one thing and do it well
- Keep functions small and focused
- Avoid side effects where possible
- Use pure functions where appropriate

```python
# Good
def extract_nodes(content: str) -> List[Node]:
    """Extract nodes from content."""
    # Implementation...

def extract_relationships(nodes: List[Node]) -> List[Relationship]:
    """Extract relationships between nodes."""
    # Implementation...

# Bad
def process_file(file_path: str) -> Tuple[List[Node], List[Relationship]]:
    """Process a file to extract nodes and relationships."""
    # This function does too many things:
    # - Read the file
    # - Parse the content
    # - Extract nodes
    # - Extract relationships
    # - Could have side effects
    # Implementation...
```

## API Design

### CLI Interface

- Use consistent command structure
- Provide meaningful help text
- Implement appropriate input validation
- Include examples in help text

```python
@click.command()
@click.argument('file_paths', nargs=-1, required=True)
@click.option('--output', default='-', help='Output file (- for stdout)')
@click.option('--format', default='json', help='Output format (json, xml)')
@click.option('--detail-level', default='standard', help='Detail level (minimal, standard, detailed)')
def file_blueprint(file_paths, output, format, detail_level):
    """Generate blueprint for specified files.
    
    Examples:
        architectum blueprint file src/main.py src/utils.py
        architectum blueprint file src/auth/*.js --output auth-blueprint.json --detail-level detailed
    """
    # Implementation...
```

### REST API

- Use RESTful design principles
- Implement consistent error handling
- Use appropriate HTTP status codes
- Include comprehensive OpenAPI documentation

```python
@router.post("/blueprints/file", response_model=Blueprint)
async def create_file_blueprint(request: FileBlueprintRequest):
    """
    Create a file-based blueprint.
    
    Args:
        request: Blueprint request parameters
        
    Returns:
        Generated blueprint
        
    Raises:
        404: If file not found
        400: If invalid parameters
    """
    # Implementation...
```

## Logging

- Use structured logging with `structlog`
- Include context information in logs
- Use appropriate log levels
- Sanitize sensitive data

```python
import structlog

logger = structlog.get_logger()

def process_blueprint(blueprint_id: str, user_id: str):
    """Process a blueprint."""
    logger.info("Processing blueprint", blueprint_id=blueprint_id, user_id=user_id)
    
    try:
        # Implementation...
        logger.info("Blueprint processed successfully", blueprint_id=blueprint_id)
    except Exception as e:
        logger.exception("Error processing blueprint", blueprint_id=blueprint_id, error=str(e))
        raise
```

## Version Control

### Commit Messages

- Use clear, descriptive commit messages
- Follow the conventional commits format:
  - `feat`: New feature
  - `fix`: Bug fix
  - `docs`: Documentation changes
  - `style`: Code style changes (formatting, etc.)
  - `refactor`: Code changes that neither fix bugs nor add features
  - `test`: Adding or fixing tests
  - `chore`: Changes to the build process, tools, etc.

```
feat(blueprints): Add support for feature blueprints

Implement core structure for feature blueprints with
persistent storage and metadata support.

Resolves: #123
```

### Pull Requests

- Keep pull requests focused on a single responsibility
- Provide clear descriptions
- Reference issues being fixed
- Ensure all tests pass
- Maintain code coverage requirements

## Additional Guidelines

### Security

- Do not hardcode credentials or sensitive information
- Validate all user input
- Handle errors securely without revealing sensitive information
- Use secure defaults

### Performance

- Be mindful of performance implications, especially for large codebases
- Use profiling to identify bottlenecks
- Implement lazy loading where appropriate
- Consider concurrency for long-running operations

### Accessibility

- Write clear error messages
- Provide meaningful feedback for CLI and API operations
- Consider colorblind users when using colors in output