# Architectum Project Brief

## Introduction

Architectum addresses two parallel challenges in modern software development: AI comprehension limitations and human navigation difficulties in complex codebases. While these challenges manifest differently, they share a common solution in a relationship-based representation of code.

## Problem #1: AI Comprehension Barriers

AI assistants face significant challenges when working with modern codebases:

- **Context Window Limitations**: AI models have fixed token limits, making it impossible to load entire codebases into context.
- **Architectural Mismatch**: Production code typically uses layered or modular architectures that distribute feature code across multiple files and directories.
- **Feature Fragmentation**: Understanding a complete feature often requires seeing dozens of scattered files simultaneously.
- **Implementation Noise**: Raw code contains too much implementation detail, diluting the architectural signal AI needs.

This creates an inherent tension: the architectures best for human development teams are often worst for AI comprehension.

## Problem #2: Human Navigation Challenges

Developers struggle with their own navigation and comprehension difficulties:

- **Mental Model Limitations**: Humans cannot hold complex multi-dimensional relationships in memory.
- **Call Flow Tracing**: Following execution paths across architectural boundaries is mentally taxing.
- **Feature Discovery**: Identifying all code elements related to a specific feature is time-consuming.
- **Relationship Visualization**: Standard file trees fail to represent the network nature of code relationships.
- **Onboarding Friction**: New team members face steep learning curves understanding how code connects.

Current tools primarily offer hierarchical views (file trees) that fail to capture the network of relationships that define how code actually functions.

## A Unified Solution

Architectum addresses both AI and human challenges through a dual representation approach:

1. **Relationship Map**: Models code as a network of nodes and relationships for efficient navigation
2. **JSON Mirrors**: Maintains detailed JSON representations of code files in a parallel structure
3. **Blueprints**: Creates specialized views by assembling elements from both core representations, enabling cross-architectural views regardless of physical code organization

This approach bridges the gap between human-optimized code organization and comprehension patterns for both AI and humans.

## Vision & Goals

### Vision

To transform how both AI assistants and humans understand and interact with software systems by revealing the invisible network of relationships that define a codebase's true structure. Architectum aims to make any codebase comprehensible, navigable, and adaptable regardless of its underlying architectural pattern, enabling more efficient collaboration between humans and AI.

### Primary Goals (MVP)

1. **Dual Representation System**: Implement both a Relationship Map (for navigation efficiency) and JSON Mirrors (for content detail) to provide complementary views of the codebase.

2. **Blueprint Generation**: Create a system that assembles specialized views from the core representations, including:
   - Path-Based Blueprints: Analyzing directory structures with configurable depth settings
   - File-Based Blueprints: Grouping specifically chosen files for comprehensive context
   - Method-Based Blueprints: Focusing on specific methods, functions, or classes for detailed analysis
   - Support for both persistent (saved as "Feature Blueprints") and temporary blueprint instances
   - Output formats optimized for both AI consumption and human visualization

3. **LSP-Powered Relationship Extraction**: Leverage Language Server Protocol to extract precise relationship data, including line numbers, call hierarchies, and type information, while minimizing processing overhead.

4. **Intelligent Caching & Incremental Updates**: Implement a blueprint caching strategy that only regenerates affected portions when code changes, maintaining blueprint accuracy without constant full reprocessing.

5. **YAML-Based Blueprint Definition**: Enable declarative specification of blueprint contents through YAML files, supporting both persistent documentation and ad-hoc exploration.

6. **Format Optimization**: Generate blueprints in formats optimized for both AI consumption and human visualization.

7. **Proof-of-Concept Visualizer**: Develop a rudimentary web-based graph visualization that demonstrates the power of the relationship-centric approach.

### Success Metrics

- **AI Context Efficiency**: Reduction in token count required to provide equivalent architectural context to an AI model compared to raw source code.

- **AI Task Performance**: Measurable improvement in an AI's ability to perform code-related tasks when using Architectum blueprints versus traditional context.

- **Developer Comprehension Speed**: Reduction in time required for developers to understand unfamiliar code structures when using Architectum visualizations.

- **Relationship Accuracy**: Percentage of function calls and relationships correctly identified across architectural boundaries.

- **Update Performance**: Time taken to update blueprints after code changes, with particular focus on incremental update efficiency.

- **Blueprint Completeness**: Accuracy and comprehensiveness of generated blueprints as measured by the inclusion of all relevant code elements and their relationships.

## Target Audience & Use Cases

### For AI Assistants

- **Profile**: LLM-based coding assistants operating with limited context windows
- **Needs**:
  - Precise structural context without implementation noise
  - Ability to follow relationships across architectural boundaries
  - Feature-oriented views regardless of physical code organization
  - Token-efficient representation of code structure
- **Use Cases**:
  - **Feature Analysis**: "Explain how the authentication feature works across the codebase"
  - **Impact Assessment**: "What would be affected if I change this function?"
  - **Code Generation**: "Add error handling to this function considering all its callers"
  - **Refactoring Guidance**: "How should I extract this functionality into a separate module?"

### For Developers

- **Profile**: Software engineers working on complex, unfamiliar, or large-scale codebases
- **Needs**:
  - Visual representation of code relationships
  - Easy navigation of call flows and dependencies
  - Feature-centric views across architectural boundaries
  - Quick onboarding to unfamiliar code
- **Use Cases**:
  - **Codebase Exploration**: Visually navigate complex relationships to understand structure
  - **Feature Mapping**: Identify all components related to a specific feature
  - **Impact Analysis**: Visualize what would be affected by changes to a component
  - **Architecture Communication**: Share and discuss system architecture through relationship graphs
  - **Onboarding**: Help new team members understand system organization quickly

### For Technical Leads & Architects

- **Profile**: Engineers responsible for system design and architectural decisions
- **Needs**:
  - High-level system visualization
  - Architectural pattern validation
  - Communication tools for team alignment
  - Impact assessment for design changes
  - **Code ownership tagging and mapping**
- **Use Cases**:
  - **Architectural Validation**: Verify implementations match intended design patterns
  - **Dependency Analysis**: Identify problematic dependencies or cycles
  - **Design Communication**: Share and explain architectural decisions visually
  - **Technical Debt Assessment**: Identify areas where implementation diverges from design
  - **Ownership Tagging**: Associate components with specific teams, individuals, or domains
  - **Responsibility Mapping**: Quickly identify who to consult when making changes to specific areas
  - **Contribution Visualization**: See ownership distribution across the system's architecture

## Key Features / Technical Scope (MVP)

### 1. Dual Representation Core

- **Relationship Map**: Efficient graph-based representation for navigation
  - **Node Types**: Files, Functions, Classes, Methods, Features (virtual)
  - **Relationship Types**: Contains, Calls, Implements, Imports, Inherits, Depends-On
  - **Metadata**: Line numbers, signatures, basic type information
  - **Navigation Support**: Methods to traverse relationships in any direction

- **JSON Mirrors**: Detailed content representation mirroring code files
  - **Mirror Structure**: JSON representation for each code file
  - **Content Detail**: Functions, classes, methods, properties with full signatures
  - **Type Information**: Parameter types, return types, property types
  - **Context Preservation**: Import/export information, file-level declarations

### 2. Blueprint Types

- **Path-Based Blueprint**: Analyzes directory structures with configurable depth (0=all depth, 1=current folder, etc.)
- **File-Based Blueprint**: Groups specifically chosen files for comprehensive context
- **Method-Based Blueprint**: Focuses on specific methods, functions, or classes for detailed analysis
- **Persistence Settings**:
  - **Feature Blueprint**: Saved permanently as documentation of a feature
  - **Temporary Blueprint**: Non-persistent, created for immediate use cases
- **Detail Levels**: Configurable detail inclusion for different use cases

### 3. YAML-Based Blueprint Definition

- **Declarative Specification**: Define blueprint contents through YAML files
- **Component Selection**: Specify files and elements to include
- **Feature Tagging**: Associate elements with logical features
- **Persistence Control**: Define whether blueprints should be saved as documentation

### 4. LSP Integration

- **Smart Querying**: Targeted LSP queries for relationship extraction
- **Parser Bridge**: Abstraction over different language servers
- **Line Information**: Precise location tracking for all elements
- **Call Hierarchy Extraction**: Function-to-function call relationships
- **Initial Language Support**: TypeScript/JavaScript and Python

### 5. Caching & Update System

- **Blueprint Storage**: Efficient storage format for blueprint representation
- **Change Detection**: File hash-based change tracking
- **Incremental Updates**: Partial regeneration for changed components
- **Synchronization Command**: `arch sync` for keeping representations up to date

### 6. Output Formats

- **Internal Representation**: JSON-based structure for processing
- **AI Consumption Format**: Semantic, structured format (potentially XML)
- **Visualization Format**: Graph-compatible output for rendering tools
- **Format Conversion**: On-demand transformation between formats

### 7. Command-Line Interface

- **Blueprint Generation**: Commands for generating different blueprint types
- **YAML Support**: Blueprint creation from YAML definitions
- **Synchronization**: Commands for updating code representations
- **Output Control**: Format and destination options

### 8. Proof-of-Concept Visualizer

- **Graph Rendering**: Basic visualization of relationship structure 
- **Relationship Navigation**: Ability to follow connections between nodes
- **Filter Controls**: Options to focus the view on specific aspects
- **Export Capability**: Save or share visualizations

## Technical Approach & Constraints

### Implementation Strategy

- **Progressive Enhancement**:
  1. Start with file-level analysis and basic relationship structure
  2. Add function relationship mapping
  3. Implement feature tagging
  4. Build visualization capabilities

- **Hybrid Processing Model**:
  - Use LSP for accurate relationship extraction
  - Leverage scripts and automation for efficiency
  - Implement caching to minimize redundant processing
  - Integrate with development workflows for automatic updates

- **YAML-Based Blueprint Definition**:
  - Use YAML files to declaratively define blueprint contents
  - Support for file and component specifications
  - Enable feature tagging and documentation
  - Standardize blueprint configuration format

- **Format Flexibility**:
  - JSON for internal processing
  - Potentially XML for AI consumption (evaluating token efficiency vs. semantic clarity)
  - Visualization-optimized formats for human consumption

### Technical Constraints

- **Initial Language Focus**: TypeScript/JavaScript and Python for MVP
- **LSP Dependency**: Reliance on language server quality and capabilities
- **Performance Considerations**: Balanced approach for large codebases
- **Token Efficiency**: Optimizing for AI context window limitations
- **Visualization Limits**: Managing complexity in graph visualization

### Potential Risks

- **Graph Complexity Management**: Ensuring the representation remains manageable
- **Update Efficiency**: Maintaining accuracy with incremental updates
- **Language Support Variability**: Differences in LSP implementation quality
- **Feature Association Maintenance**: Keeping feature tags current
- **Visualization Scalability**: Rendering large graphs effectively

## Roadmap Overview

### Phase 1: Core Representation System

- Establish Relationship Map data model
- Implement JSON Mirrors structure
- Implement basic LSP integration
- Create synchronization workflow
- Set up caching framework
- Implement CLI interface

### Phase 2: Blueprint Types and YAML Definition

- Implement Path-Based Blueprint generation
- Implement File-Based Blueprint generation
- Implement Method-Based Blueprint generation
- Create YAML specification format
- Implement blueprint generation from YAML
- Add detail level configuration

### Phase 3: Feature Blueprints and Persistence

- Implement feature tagging system
- Create persistence mechanisms
- Implement Temporary Blueprint generation
- Optimize for AI consumption

### Phase 4: Visualization & Enhancement

- Create proof-of-concept visualizer
- Implement format transformations
- Add CI/CD integration
- Expand language support

## Conclusion

Architectum represents a fundamental shift in how we think about code representation for both AI and human consumption. By providing a dual representation through both Relationship Maps and JSON Mirrors, along with specialized Blueprint views, it enables AI assistants and human developers to understand and navigate complex codebases with greater efficiency and clarity. The system bridges the gap between human-optimized architectures and AI-optimized comprehension patterns, creating a unified view that serves both audiences without compromising the underlying code organization.

---

_"Structure first, implementation second. Architectum reveals the invisible relationships that define how software really works."_