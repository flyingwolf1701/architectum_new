# Project Structure

This document outlines the structure of the Architectum codebase, explaining the organization and purpose of each directory and key file.

## High-Level Directory Structure

```
architectum/
├── arch_blueprint_generator/  # Core package
├── docs/                      # Documentation
├── tests/                     # Test suite
├── vscode-extension/          # VS Code extension
├── README.md                  # Project overview
├── pyproject.toml             # Project configuration
└── main.py                    # Entry point
```

## Core Package Structure

The `arch_blueprint_generator` directory contains the core functionality of Architectum:

```
arch_blueprint_generator/
├── __init__.py
├── models/                   # Core data models
│   ├── __init__.py
│   ├── relationship_map.py   # Relationship map model
│   ├── json_mirrors.py       # JSON mirrors model
│   └── nodes.py              # Node and relationship types
├── parsers/                  # Code parsing
│   ├── __init__.py
│   ├── parser_base.py        # Base parser interface
│   ├── python_parser.py      # Python-specific parser
│   └── javascript_parser.py  # JavaScript/TypeScript parser
├── blueprints/               # Blueprint types
│   ├── __init__.py
│   ├── base.py               # Blueprint base class
│   ├── file_based.py         # File-based blueprint
│   ├── component_based.py    # Component-based blueprint
│   ├── feature.py            # Feature blueprint
│   └── temporary.py          # Temporary blueprint
├── navigation/               # Navigation components
│   ├── __init__.py
│   ├── file_navigator.py     # JSON mirror navigation
│   └── graph_navigator.py    # Relationship map navigation
├── yaml/                     # YAML processing
│   ├── __init__.py
│   └── blueprint_config.py   # YAML blueprint configuration
├── formatters/               # Output formatting
│   ├── __init__.py
│   ├── json_formatter.py     # JSON output
│   └── xml_formatter.py      # XML output
├── cache/                    # Caching system
│   ├── __init__.py
│   └── blueprint_cache.py    # Blueprint caching
├── sync/                     # Synchronization components
│   ├── __init__.py
│   ├── arch_sync.py          # arch sync implementation
│   └── change_tracker.py     # Change tracking
├── cli/                      # Command-line interface
│   ├── __init__.py
│   └── commands.py           # CLI commands
├── api/                      # API interface
│   ├── __init__.py
│   └── routes.py             # API endpoints
└── errors/                   # Error handling
    ├── __init__.py
    └── exceptions.py         # Custom exceptions
```

## Documentation Structure

The `docs` directory contains project documentation:

```
docs/
├── index.md                   # Documentation index
├── api-reference.md           # API documentation
├── coding-standards.md        # Code style and best practices
├── data-models.md             # Core data structures and relationships
├── environment-vars.md        # Configuration options
├── project-structure.md       # Codebase organization (this file)
├── tech-stack.md              # Technology choices and rationale
├── testing-decisions.md       # Testing approach
├── epic-1.md                  # Epic 1 documentation
├── epic-2.md                  # Epic 2 documentation
├── epic-3.md                  # Epic 3 documentation
├── epic-4.md                  # Epic 4 documentation
├── prd.md                     # Product Requirements Document
├── project-brief.md           # Project overview
├── architecture.md            # Architecture overview
├── dependencies.md            # Story dependencies and testing requirements
├── test-coverage.md           # Coverage thresholds and implementation
├── sphinx-setup.md            # Sphinx documentation framework setup
└── cli-guide.md               # Command-line interface usage
```

## Test Suite Structure

The `tests` directory mirrors the structure of the core package:

```
tests/
├── unit/                     # Unit tests
│   ├── models/               # Tests for models
│   ├── parsers/              # Tests for parsers
│   ├── blueprints/           # Tests for blueprints
│   ├── navigation/           # Tests for navigation
│   ├── yaml/                 # Tests for YAML processing
│   ├── formatters/           # Tests for formatters
│   ├── cache/                # Tests for caching
│   ├── sync/                 # Tests for synchronization
│   ├── cli/                  # Tests for CLI
│   └── api/                  # Tests for API
├── integration/              # Integration tests
│   ├── blueprints/           # Blueprint generation tests
│   ├── sync/                 # Synchronization tests
│   └── api/                  # API tests
├── contracts/                # Contract tests
│   └── schemas/              # Schema definitions
├── snapshots/                # Snapshot tests
│   └── fixtures/             # Reference outputs
└── fixtures/                 # Test fixtures
    ├── python/               # Python test files
    ├── javascript/           # JavaScript test files
    └── mixed/                # Multi-language fixtures
```

## VS Code Extension Structure

The `vscode-extension` directory contains the VS Code extension:

```
vscode-extension/
├── src/                      # Extension source code
│   ├── extension.ts          # Extension entry point
│   ├── synchronizer.ts       # File synchronization
│   └── commands.ts           # VS Code commands
├── package.json              # Extension manifest
└── tsconfig.json             # TypeScript configuration
```

## Key Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Project configuration, dependencies, and build settings |
| `main.py` | Entry point for the application |
| `arch_blueprint_generator/__init__.py` | Package initialization and version information |
| `arch_blueprint_generator/models/relationship_map.py` | Core relationship map implementation |
| `arch_blueprint_generator/models/json_mirrors.py` | JSON mirrors implementation |
| `arch_blueprint_generator/cli/commands.py` | CLI command definitions |
| `arch_blueprint_generator/api/routes.py` | API endpoint definitions |
| `arch_blueprint_generator/sync/arch_sync.py` | Synchronization implementation |
| `arch_blueprint_generator/errors/exceptions.py` | Custom exception definitions |

## Package Structure Design Decisions

### Separation of Concerns

The package is structured to maintain clear separation of concerns:

- **Models**: Core data structures and operations
- **Parsers**: Language-specific code parsing logic
- **Blueprints**: Blueprint type implementations
- **CLI/API**: Interface layers
- **Cache/Sync**: Persistence and synchronization logic

### Modular Design

The modular design enables:

- Easy extension with new language parsers
- Addition of new blueprint types
- Alternative output formats
- Customizable caching strategies

### Testing Alignment

The test directory structure mirrors the package structure to ensure:

- Clear mapping between code and tests
- Comprehensive coverage of all components
- Isolated testing of each component
- Easy navigation between code and corresponding tests

### Extensibility

The structure facilitates future extensions:

- New language support through additional parsers
- New blueprint types by extending the Blueprint base class
- Additional output formats via new formatters
- Enhanced visualization through the API interface
