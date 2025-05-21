# Tech Stack

This document outlines the technology stack used in the Architectum project, providing details and rationale for the selected technologies.

## Core Technologies

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Programming Language | Python | 3.13 | Main application language |
| Graph Library | NetworkX | 3.2 | Graph data structure for relationships |
| CLI Framework | Click | 8.1 | Command-line interface implementation |
| API Framework | FastAPI | 0.105.0 | API interface implementation |
| Serialization | JSON | - | Data serialization and deserialization |
| Database | SQLite | 3.40.0 | Local storage for blueprint metadata |
| Caching | Python pickle | - | Efficient blueprint caching |
| Package Manager | UV | 0.1.5 | Modern, faster Python package manager |

## Testing Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Test Framework | pytest | 7.4.0 | Unit and integration testing |
| Property Testing | hypothesis | 6.82.0 | Property-based testing for robustness |
| Contract Testing | pact-python | 1.7.0 | API contract verification |
| Snapshot Testing | pytest-snapshot | 0.9.0 | Output verification against references |
| Coverage | pytest-cov | 4.1.0 | Code coverage measurement |
| Performance Testing | pytest-benchmark | 4.0.0 | Performance testing for critical operations |
| Mocking | unittest.mock | - | Test isolation and dependency mocking |

## Documentation Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Documentation Generator | Sphinx | 7.2.0 | API documentation generation |
| Theme | sphinx-rtd-theme | 1.3.0 | Documentation theme |
| Type Hints | sphinx-autodoc-typehints | 1.25.0 | Type hint integration |
| CLI Documentation | sphinx-click | 5.0.0 | CLI command documentation |

## VSCode Extension Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Language | TypeScript | 5.2 | Extension implementation |
| VS Code API | vscode | 1.85.0 | VS Code integration |

## Additional Libraries

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Logging | structlog | 23.1.0 | Structured logging |
| YAML Processing | PyYAML | 6.0.1 | YAML parsing and generation |
| Environment Management | python-dotenv | 1.0.0 | Environment variable management |
| Error Retry | tenacity | 8.2.3 | Automatic retries with backoff |
| CLI Progress | click-spinner | 0.1.10 | Command-line progress indication |
| Language Parsing | tree-sitter | 0.20.1 | Efficient code parsing |

## Technology Selection Rationale

### Python 3.13

Python 3.13 was selected as the primary language for Architectum for several reasons:

1. **Advanced Type Annotations**: Python 3.13 includes significant improvements to type annotations, which is critical for maintaining a complex codebase.
2. **Performance Improvements**: Python 3.13 offers better performance compared to previous versions, particularly for I/O operations.
3. **Rich Ecosystem**: Python has a vast ecosystem of libraries for parsing, graph manipulation, and code analysis.
4. **Accessibility**: Python's readability and ease of use make it accessible for contributors.

### NetworkX

NetworkX was chosen for the graph data structure implementation:

1. **Mature Library**: NetworkX is a well-established library with comprehensive documentation.
2. **Flexible Data Model**: It allows attaching arbitrary data to nodes and edges, which is crucial for the relationship metadata.
3. **Algorithmic Support**: It provides built-in graph algorithms that can be used for relationship analysis.
4. **Serialization Support**: NetworkX graphs can be easily serialized to and from various formats.

### Click

Click was selected for the CLI framework:

1. **Composable Commands**: Click makes it easy to compose complex command hierarchies.
2. **Automatic Help Generation**: Click generates comprehensive help documentation.
3. **Type Conversion**: Click handles parameter type conversion automatically.
4. **Testing Support**: Click's design makes it easy to test CLI applications.

### FastAPI

FastAPI was chosen for the API framework:

1. **Performance**: FastAPI is one of the fastest Python frameworks available.
2. **Automatic Documentation**: FastAPI generates OpenAPI documentation automatically.
3. **Type Validation**: FastAPI leverages Python type hints for request validation.
4. **Async Support**: FastAPI's async capabilities enable efficient handling of concurrent requests.

### SQLite

SQLite was selected for local storage:

1. **Serverless**: SQLite doesn't require a separate server process.
2. **Self-Contained**: The entire database is stored in a single file, making it easy to distribute.
3. **Reliable**: SQLite is known for its reliability and durability.
4. **Efficient**: SQLite is efficient for the scale of data Architectum needs to store.
