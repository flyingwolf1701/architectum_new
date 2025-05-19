# Story 1.1: Setup Blueprint Generation Core Module with Dual Representation Model

## Status: Draft

## Story

- As a system architect
- I want a core module for blueprint generation established with both a Relationship Map model and JSON Mirrors structure
- So that different blueprint types can be developed and integrated in a consistent and maintainable manner within the existing Architectum repository

## Dependencies

- None (this is the first story of the project)

## Acceptance Criteria (ACs)

- AC1: The new module/package `arch_blueprint_generator` is created within the `Architectum` repository and is buildable/integrable with the main project.
- AC2: The Relationship Map model is implemented with support for nodes, relationships, and efficient navigation.
- AC3: The JSON Mirrors structure is implemented with the ability to create and access JSON representations of source files.
- AC4: Basic operations for both representations are functional and can be used independently.
- AC5: A placeholder CLI command or API endpoint exists and returns a "not yet implemented" message or basic help.
- AC6: Basic logging for module initialization and errors is functional with color-coded output.
- AC7: The module includes a README with an overview of the dual representation approach.
- AC8: Test coverage reaches at least 80% for both representation models and core operations.

## Tasks / Subtasks

- [ ] Setup project structure (AC1)
  - [ ] Create `arch_blueprint_generator` module within the repository
  - [ ] Configure project dependencies in pyproject.toml (NetworkX, Typer, etc.)
  - [ ] Create initial package structure with proper imports
  - [ ] Setup basic logging configuration with colorama

- [ ] Implement Relationship Map model (AC2)
  - [ ] Create base Node and Relationship classes with proper type hints
  - [ ] Implement node types (FileNode, DirectoryNode, FunctionNode, ClassNode, etc.)
  - [ ] Implement relationship types (ContainsRelationship, CallsRelationship, ImportsRelationship, etc.) with name and path fields
  - [ ] Implement graph operations (create, read, update, delete nodes/relationships)
  - [ ] Implement traversal methods for efficient navigation

- [ ] Implement JSON Mirrors structure (AC3)
  - [ ] Create JSONMirrors container class with appropriate type hints
  - [ ] Implement file content representation model
  - [ ] Implement directory content representation model
  - [ ] Create methods to get/update mirrored content

- [ ] Implement serialization/deserialization for both models (AC4)
  - [ ] Create JSON serialization for Relationship Map
  - [ ] Create JSON serialization for Mirrors
  - [ ] Implement file-based persistence for both models
  - [ ] Ensure models can be reconstructed from serialized forms

- [ ] Create placeholder CLI/API interface (AC5)
  - [ ] Setup Typer command structure with type hints
  - [ ] Create placeholder commands with "not yet implemented" responses
  - [ ] Implement help text and basic parameter parsing
  - [ ] Setup command discovery mechanism

- [ ] Implement test suite (AC8)
  - [ ] Create unit tests for Relationship Map model
  - [ ] Create unit tests for JSON Mirrors structure
  - [ ] Implement property-based tests using hypothesis
  - [ ] Generate test coverage reports
  - [ ] Ensure 80% code coverage minimum

- [ ] Create documentation (AC7)
  - [ ] Write comprehensive README for the module
  - [ ] Document core concepts (Relationship Map, JSON Mirrors)
  - [ ] Document public API interfaces
  - [ ] Add inline documentation for classes and methods

## Dev Technical Guidance

### Installation & Dependencies

Use uv to install the required dependencies:

```bash
# Core dependencies
uv add networkx        # Graph operations
uv add typer           # CLI framework with type hints
uv add pydantic        # Data validation
uv add colorama        # Terminal colors for logging
uv add structlog       # Structured logging

# API-related dependencies (if implementing API endpoints)
uv add fastapi
uv add uvicorn

# Testing dependencies
uv add pytest pytest-cov hypothesis --dev
```

### Tech Stack Information
- Use Python 3.13 as specified in project requirements
- Use NetworkX for the graph model implementation
- Use Typer (instead of Click) for CLI framework to leverage type hints
- Use FastAPI for API endpoints if implementing them
- Use colorama for colored terminal output in logs and CLI
- Use pytest, hypothesis, and pytest-cov for testing
- Use comprehensive type hints throughout the codebase
- Follow the module organization as described in the architecture document:
  ```
  architectum/
  ├── arch_blueprint_generator/
  │   ├── __init__.py
  │   ├── models/                   # Core data models
  │   │   ├── __init__.py
  │   │   ├── relationship_map.py   # Relationship map model
  │   │   ├── json_mirrors.py       # JSON mirrors model
  │   │   └── nodes.py              # Node and relationship types
  ```

### Type Hints and Relationship Model Implementation
Use comprehensive type hints throughout the code. For example:

```python
from typing import Optional, Dict, Any, List, Tuple
from enum import Enum

class RelationshipType(Enum):
    CONTAINS = "contains"
    CALLS = "calls"
    IMPORTS = "imports"
    INHERITS = "inherits"
    IMPLEMENTS = "implements"

class Relationship:
    """Base class for all relationships in the graph."""
    source_id: str
    target_id: str
    type: RelationshipType
    metadata: Dict[str, Any]

class CallsRelationship(Relationship):
    """Represents a function call relationship."""
    name: str  # Name of the called method/function
    path: str  # Path to the file containing the called method/function
    line_number: Optional[int]
```

### Colorized Logging Example

```python
import logging
import colorama
import structlog
from colorama import Fore, Style

# Initialize colorama
colorama.init()

# Configure structlog with colorama
def add_colors(_, __, event_dict):
    level = event_dict.get("level", "info").upper()
    if level == "DEBUG":
        event_dict["colored_level"] = f"{Fore.BLUE}{level}{Style.RESET_ALL}"
    elif level == "INFO":
        event_dict["colored_level"] = f"{Fore.GREEN}{level}{Style.RESET_ALL}"
    elif level == "WARNING":
        event_dict["colored_level"] = f"{Fore.YELLOW}{level}{Style.RESET_ALL}"
    elif level == "ERROR":
        event_dict["colored_level"] = f"{Fore.RED}{level}{Style.RESET_ALL}"
    elif level == "CRITICAL":
        event_dict["colored_level"] = f"{Fore.MAGENTA}{level}{Style.RESET_ALL}"
    else:
        event_dict["colored_level"] = level
    return event_dict

# Configure structured logging
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        add_colors,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()
```

### Typer CLI Example
Typer simplifies CLI creation with type hints:

```python
import typer
from typing import List, Optional
from colorama import Fore, Style

app = typer.Typer()

@app.command()
def blueprint(
    files: List[str] = typer.Argument(None, help="List of files to include in blueprint"),
    output: str = typer.Option("-", help="Output file (- for stdout)"),
    format: str = typer.Option("json", help="Output format (json or xml)"),
    detail_level: str = typer.Option("standard", help="Detail level (minimal, standard, detailed)")
) -> None:
    """Generate a blueprint from specified files."""
    typer.echo(f"{Fore.YELLOW}Blueprint generation not yet implemented{Style.RESET_ALL}")
```

## Story Progress Notes

### Agent Model Used: `<Agent Model Name/Version>`

### Completion Notes List
{Not started yet}

### Change Log
- Initial story draft created by POSM from Epic 1 documentation
- Updated to use Typer instead of Click for better type hint support
- Added colorama for terminal colors and structured logging
- Added uv installation commands for dependencies