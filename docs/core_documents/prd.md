# Architectum Product Requirements Document (PRD)

## Intro

Architectum aims to revolutionize how both AI assistants and humans understand and interact with complex codebases through a dual representation approach. Rather than treating code as a hierarchy of files and directories, Architectum reveals the true network of relationships between code elements through its Relationship Map, while providing detailed content through JSON Mirrors. From these core representations, specialized Blueprints are assembled to enable analysis across architectural boundaries regardless of physical code organization. This initial version (MVP) focuses on establishing these core capabilities and the blueprint generation system that can be consumed by AI agents and visualized by human developers.

## Goals and Context

- **Project Objectives:**
    - To create a dual representation system with Relationship Maps (for efficient navigation) and JSON Mirrors (for detailed content)
    - To enable blueprint generation for different use cases (Path-Based, File-Based, Method-Based) with persistence options (Feature and Temporary)
    - To enable AI agents to understand code structure and relationships across architectural boundaries
    - To provide developers with visualization tools for navigating complex code relationships
    - To establish a foundation for intelligent, incremental updating of blueprints when code changes

- **Measurable Outcomes:**
    - Reduction in tokens required for AI to understand code structure (target: 70% reduction compared to raw code)
    - Improvement in AI task completion accuracy when using blueprints (target: 30% improvement)
    - Reduction in time required for developers to understand unfamiliar code (target: 40% reduction)
    - Relationship extraction accuracy (target: >90% of function calls correctly identified)
    - Blueprint update performance (target: <5 seconds for incremental updates on 100-file projects)

- **Success Criteria:**
    - The system successfully generates all blueprint types from YAML definitions
    - Incremental updates correctly maintain blueprint accuracy after code changes via `arch sync`
    - Generated blueprints can be consumed by AI agents to answer structure-related questions
    - Proof-of-concept visualization demonstrates the relationship-based representation
    - Feature (persistent) Blueprints serve as effective documentation for codebase features

- **Key Performance Indicators (KPIs):**
    - Blueprint generation success rate
    - Relationship extraction accuracy percentage
    - Token efficiency ratio (tokens in blueprint vs. tokens in raw code)
    - Update performance metrics (time to regenerate after changes)
    - AI task performance improvement metrics
    - Blueprint usage metrics (for documentation)

## Scope and Requirements (MVP / Current Version)

### Functional Requirements (High-Level)

#### 1. Core Representations

- **1.1 Relationship Map**
  - The system must create and maintain a graph-based representation optimized for navigation
  - Each node must have a unique identifier and type designation (file, function, class, method, feature)
  - Relationships must be directional with clear source and target (calls, contains, imports, etc.)
  - The Relationship Map should typically use "Minimal" detail level for efficiency

- **1.2 JSON Mirrors**
  - The system must create and maintain JSON representations that mirror code files
  - Mirrors must include detailed structure of each file (functions, classes, methods, properties)
  - Mirrors must include type information, signatures, and file-level context
  - JSON Mirrors should typically use "Standard" detail level for comprehensiveness

- **1.3 Synchronization**
  - The system must provide an `arch sync` command to update both representations when code changes
  - Synchronization must be incremental, only updating affected parts
  - The system must track which files need synchronization
  - Synchronization must support individual files, directories, and interactive selection

#### 2. Blueprint Generation System

- **2.1 Path-Based Blueprint**
  - The system must generate a blueprint from a specified directory with configurable depth
  - Depth parameter must control how many levels of subdirectories to include (0 for all levels)
  - The blueprint must include the directory structure and contained files
  - Relationships between elements across the directory must be captured
  - The system must handle invalid or inaccessible directories gracefully

- **2.2 File-Based Blueprint**
  - The system must generate a blueprint from a specified list of files
  - The blueprint must include the specified files and their contained code elements
  - Relationships between elements across the specified files must be captured
  - The system must handle invalid or missing files gracefully

- **2.3 Method-Based Blueprint**
  - The system must generate a blueprint focused on specific methods, functions, or classes
  - The blueprint must include the specified elements and their immediate relationships
  - The system must provide file-level context necessary for the specified components
  - The system must handle elements that cannot be found gracefully

- **2.4 Blueprint Persistence Settings**
  - The system must support saving blueprints as persistent documentation (Feature Blueprints)
  - The system must support temporary blueprints for immediate use (Temporary Blueprints)
  - The system must store Feature Blueprints for reference and documentation
  - The system must clear Temporary Blueprints after use to minimize storage
  - Temporary Blueprints must be easily convertible to Feature Blueprints if desired

- **2.5 YAML Blueprint Definition**
  - The system must support blueprint definition through YAML files
  - YAML definitions must allow specification of files and components to include
  - YAML definitions must allow specification of blueprint type and persistence setting
  - The system must validate YAML definitions before processing

- **2.6 Detail Level Configuration**
  - All blueprint types must support three detail levels:
    - **Minimal**: Basic structure and relationship information
    - **Standard**: Additional type information and signatures
    - **Detailed**: Comprehensive information including documentation
  - Detail levels must be applied consistently across all blueprint types
  - The system must respect detail level settings when generating output

#### 3. LSP Integration & Code Analysis

- **3.1 Language Server Protocol (LSP) Integration**
  - The system must connect to language servers for accurate code analysis
  - The system must extract precise relationship data, including line numbers
  - The system must leverage LSP for call hierarchy information
  - Initial support must focus on TypeScript/JavaScript and Python

- **3.2 Smart Querying**
  - The system must use targeted LSP queries to minimize analysis overhead
  - The system must detect file types and use appropriate language servers
  - The system must handle unsupported languages gracefully
  - The system must optimize query patterns for performance

- **3.3 Parser Abstraction**
  - The system must provide a consistent interface across different language parsers
  - The system must be extensible to support additional languages in the future
  - The system must normalize language-specific constructs into the common representations
  - The system must handle language-specific features appropriately

#### 4. Caching & Incremental Updates

- **4.1 Blueprint Storage**
  - The system must store generated blueprints in a structured format
  - The system must include metadata about the generation process in stored blueprints
  - The storage format must efficiently represent the graph structure
  - The storage format must support incremental updates

- **4.2 Change Detection**
  - The system must track file hashes to detect changes
  - The system must identify which parts of the representations are affected by file changes
  - The system must support Git integration for change detection
  - The system must handle renamed or moved files appropriately

- **4.3 Incremental Updates**
  - The system must regenerate only affected portions of the representations when files change
  - The system must maintain relationship integrity during partial updates
  - The system must handle cascading effects of changes
  - The system must validate the consistency of the updated representations
  - The system must provide an `arch sync` command for managing updates

#### 5. Output & Format Optimization

- **5.1 Internal Representation**
  - The system must use JSON for internal processing
  - The internal representation must be optimized for processing efficiency
  - The representation must preserve all node and relationship metadata
  - The representation must support serialization and deserialization

- **5.2 AI Consumption Format**
  - The system must generate output optimized for AI token efficiency
  - The system must support transformation to XML if it proves more efficient for AI
  - The output must be structured for easy traversal by AI
  - The output must include sufficient metadata for AI comprehension

- **5.3 Visualization Format**
  - The system must generate output suitable for graph visualization tools
  - The visualization format must support rendering nodes, edges, and labels
  - The format must include visual metadata (e.g., node types, relationship types)
  - The format must support interactive navigation

#### 6. Command-Line Interface & API

- **6.1 CLI Implementation**
  - The system must provide a command-line interface for core operations
  - The CLI must support all blueprint types and detail levels
  - The CLI must include options for output format and destination
  - The CLI must provide clear error messages and help documentation

- **6.1.1 Blueprint Commands**
  - The CLI must support generating blueprints from YAML definitions
  - The CLI must support both persistent Feature Blueprints and Temporary Blueprints
  - The CLI must include commands for Path-Based, File-Based, and Method-Based blueprint creation
  - The CLI must provide options for blueprint detail level and output format

- **6.1.2 Synchronization Commands**
  - The system must provide an `arch sync` command for synchronizing code with Architectum
  - Synchronization must update both the Relationship Map and JSON Mirrors
  - The system must support synchronizing individual files, open files, and directories
  - The system must provide clear status information during synchronization

- **6.2 API Design**
  - The system must provide a programmatic API for integration
  - The API must support all blueprint generation capabilities
  - The API must follow consistent patterns and naming conventions
  - The API must include proper error handling and validation

#### 7. Proof-of-Concept Visualizer

- **7.1 Graph Rendering**
  - The system must include a basic web-based graph visualization component
  - The visualizer must render nodes and relationships from blueprint data
  - The visualizer must visually distinguish between node and relationship types
  - The visualizer must support zooming and panning operations

- **7.2 Interactive Features**
  - The visualizer must support clicking on nodes to view details
  - The visualizer must support following relationships between nodes
  - The visualizer must include basic filtering capabilities
  - The visualizer must support graph navigation operations

### Non-Functional Requirements (NFRs)

- **Performance:**
  - Blueprint generation must complete within reasonable time (target: <10s for 100-file projects)
  - Incremental updates must be significantly faster than full regeneration
  - The system must be memory-efficient when processing large codebases
  - The visualizer must handle rendering at least 200 nodes without performance degradation

- **Scalability:**
  - The architecture must support extension to additional programming languages
  - The graph model must scale to handle projects with thousands of files
  - The caching system must efficiently handle large blueprint storage
  - Processing overhead must grow sub-linearly with codebase size

- **Reliability/Availability:**
  - The system must handle malformed or unparseable code gracefully
  - Invalid inputs or parameters must result in clear error messages
  - The system must be resilient to LSP server failures
  - The caching system must maintain data integrity

- **Security:**
  - The system must handle code access according to repository permissions
  - The system must not compromise code privacy or intellectual property
  - The visualization must respect access controls on code elements
  - Blueprint storage must follow security best practices

- **Maintainability:**
  - The codebase must be modular and well-documented
  - The architecture must be extensible for future enhancements
  - The system must include comprehensive logging for troubleshooting
  - The architecture must allow for component upgrades or replacements

### User Experience (UX) Requirements

- **CLI Experience:**
  - Command structure must be intuitive and consistent
  - Parameters must follow standard CLI conventions
  - Help documentation must be comprehensive and accessible
  - Output formatting must be clear and readable

- **API Experience:**
  - API calls must be consistent and predictable
  - Method names must be descriptive and unambiguous
  - Documentation must include examples for common operations
  - Error messages must be actionable

- **Visualization Experience:**
  - The graph layout must present relationships clearly
  - Visual encoding must distinguish different node and relationship types
  - Navigation controls must be intuitive
  - Performance must remain smooth during interaction

### Integration Requirements

- **Version Control Integration:**
  - The system should support integration with Git for change detection
  - Blueprint updates can be triggered by Git hooks
  - Blueprints can be stored alongside code or in a separate repository

- **CI/CD Integration:**
  - The system should support integration with CI/CD pipelines
  - Blueprint generation can be triggered by continuous integration
  - Blueprint validation can be part of continuous delivery checks

- **IDE Integration (Future):**
  - The architecture should enable future IDE plugin development
  - The API should expose capabilities needed for IDE integration
  - The visualization format should be compatible with IDE rendering

## Epic Overview (MVP / Current Version)

### Epic 1: Core Blueprint Generation Framework and Dual Representation Implementation

**Goal:** To establish the foundational infrastructure for Architectum's codebase blueprint generation and deliver the core functionality for the dual representation approach (Relationship Map and JSON Mirrors), enabling AI agents and visualization tools to analyze code structures at varying levels of detail.

### Epic 2: File-Based Blueprint Implementation

**Goal:** To enable Architectum to generate blueprints based on an explicit list of user-specified files, allowing AI agents and visualization tools to analyze a curated collection of code files at varying levels of detail.

### Epic 3: Method-Based Blueprint Implementation

**Goal:** To empower Architectum with the ability to generate highly focused blueprints detailing specific code elements (like functions, classes, methods) within files, enabling AI agents to perform granular analysis.

### Epic 4: Path-Based Blueprint Implementation

**Goal:** To implement directory-level blueprint generation with configurable depth settings, allowing analysis of code structure from entire projects down to specific folders.

### Epic 5: Blueprint Persistence and YAML Definition

**Goal:** To implement a system for saving blueprints as documentation (Feature Blueprints) and defining blueprints through YAML configuration files.

### Epic 6: Caching and Incremental Updates

**Goal:** To implement an intelligent caching system that stores blueprints and supports efficient incremental updates when code changes, including the `arch sync` command.

### Epic 7: Proof-of-Concept Visualization

**Goal:** To develop a basic web-based visualization component that renders blueprint graphs for human navigation and comprehension.

## Key Reference Documents

- `docs/project-brief.md`
- `docs/architecture.md`
- `docs/epic1.md`, `docs/epic2.md`, ...
- `docs/tech-stack.md`
- `docs/api-reference.md`
- `docs/relationship-map.md`
- `docs/json-mirrors.md`
- `docs/yaml-specification.md`
- `docs/output-formats.md`

## Post-MVP / Future Enhancements

- **Enhanced Language Support:**
  - Expand to additional programming languages (Java, C#, Ruby, etc.)
  - Improve language-specific feature detection
  - Support multi-language projects

- **Advanced Graph Operations:**
  - Impact analysis (what would break if X changes)
  - Similarity detection between code elements
  - Pattern detection and architectural conformance checking

- **Advanced Feature Association:**
  - AI-assisted feature association
  - Feature boundary detection
  - Automatic tagging based on naming conventions or comments

- **Props Tracking:**
  - Track component property flow across React/Vue components
  - Identify prop origins and usage
  - Visualize prop flow in relationship maps

- **Enhanced Visualization:**
  - Interactive 3D graph visualization
  - Time-based animation of code evolution
  - Customizable visual encoding

- **Collaboration Features:**
  - Shared annotations on the graph
  - Team-based feature ownership
  - Code review integration

- **Deeper Integration:**
  - IDE plugins
  - Code generation support
  - Integration with code quality tools

## Change Log

| Change        | Date       | Version | Description                  | Author         |
| ------------- | ---------- | ------- | ---------------------------- | -------------- |
| Initial draft | 05-17-2025 | 0.1     | Initial PRD with graph focus | Product Manager |
| Update        | 05-17-2025 | 0.2     | Revised with dual representation and updated blueprint types | Product Manager |
| Update        | 05-18-2025 | 0.3     | Corrected terminology and blueprint types to align with implementation | POSM |

## Initial Architect Prompt

Based on our discussions and requirements analysis for the Architectum platform, I've compiled the following technical guidance to inform your architecture decisions:

### Technical Infrastructure

- **Module Integration:** The `arch_blueprint_generator` module should be integrated within the existing `Architectum` repository while maintaining clear separation of concerns.
- **Dual Representation:** The foundation of the system should be a robust dual representation with Relationship Maps for navigation efficiency and JSON Mirrors for detailed content.
- **LSP Integration:** The system should leverage Language Server Protocol for accurate code analysis, but with smart querying patterns to minimize overhead.
- **Caching Strategy:** Implement an efficient caching system that enables incremental updates rather than full regeneration.

### Key Architectural Decisions

1. **Blueprint Types:** Design a system that supports Path-Based Blueprints, File-Based Blueprints, and Method-Based Blueprints, with options for persistent (Feature) and temporary storage.
2. **YAML Definition:** Implement support for declarative blueprint definition through YAML files.
3. **Synchronization Workflow:** Create an `arch sync` command for keeping representations up to date with code changes.
4. **Parser Abstraction:** Create a clean abstraction layer over language-specific parsing to enable future language support.
5. **Format Transformation:** Separate internal processing format (JSON) from AI consumption format (potentially XML) and visualization format.

### Technical Constraints

- **LSP Efficiency:** The system must use LSP judiciously to avoid performance bottlenecks.
- **Language Support:** Initial focus should be on TypeScript/JavaScript and Python.
- **Visualization Performance:** Graph rendering must handle at least 200 nodes smoothly.
- **Token Efficiency:** Output format must prioritize AI token efficiency.

### Deployment Considerations

- **Integration:** The system should support integration with Git, CI/CD, and potentially IDE plugins.
- **Automation:** Blueprint generation should be automatable through hooks and pipelines.
- **Standalone Operations:** The system should be usable both within and independent of the main Architectum application.

Please design an architecture that emphasizes the dual representation approach, with YAML-based blueprint definition, efficient synchronization, and format optimization. The system should be modular, extensible, and performance-oriented, with clear boundaries between components. Consider both immediate implementation needs and future scalability as the system grows.