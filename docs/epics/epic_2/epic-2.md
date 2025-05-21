# Epic 2: File-Based Blueprint Implementation

**Goal:** To enable Architectum to generate File-Based Blueprints from an explicit list of user-specified files, allowing AI agents and visualization tools to analyze a curated collection of code files at varying levels of detail with relationship mapping across file boundaries.

## Story List

### Story 2.1: Implement YAML-Based Blueprint Definition

- **User Story / Goal:** As an AI agent or developer, I want to define a File-Based Blueprint using a YAML configuration file, so that I can declaratively specify which files to include and how they should be processed.
- **Dependencies:**
  - Epic 1 must be completed, particularly Story 1.6 (Expose Blueprint Generation via Initial API/CLI)
- **Detailed Requirements:**
  - Design and implement a YAML schema for blueprint definition:
    ```yaml
    type: file  # or component, feature, temporary
    name: auth-system-blueprint
    description: "Core authentication system files"
    persistence: temporary  # or persistent
    
    # Files to include
    components:
      - file: src/auth/login.js
        # Empty elements means include entire file
        elements: []
      
      - file: src/auth/register.js
        elements: []
    ```
  - Implement a YAML parser that validates blueprint definitions
  - Create a repository for storing and retrieving blueprint definitions
  - Integrate with the blueprint generation system from Epic 1
  - Support both file paths and glob patterns for flexible file selection
- **Acceptance Criteria (ACs):**
  - AC1: YAML blueprint definitions can be parsed and validated.
  - AC2: Blueprint definitions correctly specify files to include.
  - AC3: Invalid YAML definitions are rejected with clear error messages.
  - AC4: Blueprint generation can be triggered from YAML definitions.
  - AC5: Both explicit file paths and glob patterns are supported for file selection.
  - **AC6: Testing Requirements:**
    - **Coverage:** At least 80% code coverage for the YAML parsing and validation functionality
    - **Framework:** Implementation using pytest with YAML fixtures
    - **Schema Testing:** Test validation of various valid and invalid YAML structures
    - **Property Testing:** Use hypothesis to generate and test random YAML structures
    - **Integration Testing:** Verify blueprint generation from YAML definitions
    - **Error Handling:** Test validation error messages for various invalid inputs

### Story 2.2: Enhance File-Based Blueprint with Cross-File Relationships

- **User Story / Goal:** As an AI agent, I want File-Based Blueprints to include comprehensive cross-file relationships, so that I can understand how the selected files interact with each other.
- **Dependencies:**
  - Story 2.1 (YAML-Based Blueprint Definition) must be completed
  - Story 1.5 (Basic File-Based Blueprint Generation) must be completed
- **Detailed Requirements:**
  - Enhance the File-Based Blueprint generation to focus on relationships between files:
    - Imports/exports between files
    - Function calls across file boundaries
    - Type references and inheritance relationships
    - Other dependencies between files
  - Extract these relationships from the Relationship Map
  - Ensure the relationships are included in the blueprint regardless of detail level
  - Add metadata to relationships to indicate their nature and origin
  - Handle circular relationships appropriately
- **Acceptance Criteria (ACs):**
  - AC1: File-Based Blueprints include cross-file relationships between the specified files.
  - AC2: Different types of relationships (imports, calls, type references) are clearly distinguished.
  - AC3: Relationship metadata provides context about the nature of each relationship.
  - AC4: Circular relationships are handled without causing infinite loops or errors.
  - AC5: Relationships from both the Relationship Map and JSON Mirrors are integrated cohesively.
  - **AC6: Testing Requirements:**
    - **Coverage:** At least 80% code coverage for the relationship extraction and integration functionality
    - **Framework:** Implementation using pytest with multi-file test fixtures
    - **Snapshot Testing:** Create snapshots showing cross-file relationships in blueprints
    - **Integration Testing:** Test relationship extraction across both representations
    - **Related File Testing:** Test files with known relationships to verify detection
    - **Language Testing:** Ensure cross-file relationship detection works for all supported languages

### Story 2.3: Implement Detail Level Support for File-Based Blueprints

- **User Story / Goal:** As an AI agent, I want to request File-Based Blueprints at different detail levels, so that I can balance comprehensiveness against token efficiency for different use cases.
- **Dependencies:**
  - Story 2.1 (YAML-Based Blueprint Definition) must be completed
  - Story 1.4 (Detail Level Configuration) must be completed
- **Detailed Requirements:**
  - Implement detail level configuration specifically for File-Based Blueprints:
    - **Minimal**: Basic file structure and primary relationships, optimized for navigation
    - **Standard**: Type information, signatures, and expanded relationships
    - **Detailed**: Documentation, implementation insights, and comprehensive relationships
  - Ensure the detail level can be specified in YAML definitions:
    ```yaml
    type: file
    name: auth-system-blueprint
    detail_level: standard  # or minimal, detailed
    components:
      # ...
    ```
  - Apply detail level settings consistently across both representation sources
  - Implement size estimation to warn about token count for large blueprints
- **Acceptance Criteria (ACs):**
  - AC1: File-Based Blueprints can be generated at different detail levels.
  - AC2: Detail level can be specified in YAML definitions.
  - AC3: Minimal detail level produces streamlined blueprints for efficiency.
  - AC4: Standard detail level includes type information and signatures.
  - AC5: Detailed detail level includes comprehensive information including documentation.
  - AC6: Large blueprints include size warnings to prevent token limit issues.
  - **AC7: Testing Requirements:**
    - **Coverage:** At least 80% code coverage for the detail level configuration and application
    - **Framework:** Implementation using pytest with parameterized tests for detail levels
    - **Snapshot Testing:** Create snapshots comparing blueprints at different detail levels
    - **Contract Testing:** Verify blueprint formats at different detail levels meet schema requirements
    - **Size Testing:** Verify size warnings for large blueprints
    - **YAML Integration:** Test detail level specification in YAML definitions

### Story 2.4: Implement Blueprint Persistence for File-Based Blueprints

- **User Story / Goal:** As a developer, I want to save File-Based Blueprints for future use, so that I can reference them without regenerating them each time.
- **Dependencies:**
  - Story 2.1 (YAML-Based Blueprint Definition) must be completed
  - Story 2.3 (Detail Level Support) must be completed
- **Detailed Requirements:**
  - Implement a persistence mechanism for blueprints:
    - Persistent storage location for blueprints
    - Naming and versioning system
    - Metadata about creation time, source files, and configuration
  - Support persistence configuration in YAML:
    ```yaml
    type: file
    name: auth-system-blueprint
    persistence: persistent  # or temporary
    # ...
    ```
  - Implement blueprint retrieval by name
  - Add commands for listing and managing saved blueprints
  - Handle blueprint updates when source files change
- **Acceptance Criteria (ACs):**
  - AC1: File-Based Blueprints can be saved as persistent resources.
  - AC2: Persistence can be configured through YAML definitions.
  - AC3: Persistent blueprints can be retrieved by name.
  - AC4: Commands exist for listing and managing saved blueprints.
  - AC5: Blueprint updates maintain persistence while reflecting changed source files.
  - **AC6: Testing Requirements:**
    - **Coverage:** At least 80% code coverage for the persistence functionality
    - **Framework:** Implementation using pytest with mocked storage
    - **Integration Testing:** End-to-end tests for saving and retrieving blueprints
    - **Metadata Testing:** Verify metadata is correctly maintained for persistent blueprints
    - **Update Testing:** Verify blueprint updates maintain persistence
    - **Command Testing:** Test commands for blueprint management

### Story 2.5: Expose File-Based Blueprints via Enhanced API/CLI

- **User Story / Goal:** As a developer or another service, I want comprehensive CLI and API access to File-Based Blueprint functionality, so that I can easily create, retrieve, and utilize blueprints in my workflows.
- **Dependencies:**
  - Story 2.4 (Blueprint Persistence) must be completed
  - Story 1.6 (Expose Blueprint Generation via Initial API/CLI) must be completed
- **Detailed Requirements:**
  - Enhance the CLI for File-Based Blueprints:
    - `architectum blueprint create -f blueprint.yaml` for creating from YAML
    - `architectum blueprint list` for listing available blueprints
    - `architectum blueprint get -n blueprint-name` for retrieving by name
    - Support for different output formats and destinations
  - If API-based: Implement comprehensive endpoints for blueprint management
  - Add support for blueprint combination (merging multiple blueprints)
  - Integrate with IDE extensions (foundation only)
  - Include comprehensive help and examples
- **Acceptance Criteria (ACs):**
  - AC1: Enhanced CLI commands successfully manage File-Based Blueprints.
  - AC2: All commands include appropriate options and parameters.
  - AC3: Blueprint combination produces valid merged blueprints.
  - AC4: Foundation for IDE integration is established.
  - AC5: Help documentation includes clear examples and usage guidance.
  - **AC6: Testing Requirements:**
    - **Coverage:** At least 80% code coverage for the enhanced CLI/API functionality
    - **Framework:** Implementation using pytest with CLI invocation testing
    - **Integration Testing:** End-to-end tests for all commands and options
    - **Combination Testing:** Test blueprint merging with various inputs
    - **API Testing:** Test API endpoints for blueprint management if implemented
    - **Documentation Testing:** Verify help output and examples

## Implementation Sequence

The implementation of this epic should follow this sequence:

1. YAML-Based Blueprint Definition (Story 2.1)
2. Enhance File-Based Blueprint with Cross-File Relationships (Story 2.2) and Detail Level Support (Story 2.3) can be implemented in parallel
3. Blueprint Persistence for File-Based Blueprints (Story 2.4)
4. Expose File-Based Blueprints via Enhanced API/CLI (Story 2.5)

## Change Log

| Change        | Date       | Version | Description                    | Author         |
| ------------- | ---------- | ------- | ------------------------------ | -------------- |
| Initial draft | 05-16-2025 | 0.1     | Initial draft of Epic 2        | Product Manager |
| Updated with graph approach | 05-17-2025 | 0.2 | Enhanced Epic 2 with graph-based model | Technical Scrum Master |
| Added testing requirements | 05-17-2025 | 0.3 | Added comprehensive testing strategy | Technical Scrum Master |
| Refined architecture | 05-18-2025 | 0.4 | Updated to reflect YAML-based blueprint definition and File-Based Blueprint approach | System Architect |
| Added dependencies | 05-18-2025 | 0.5 | Added explicit dependencies to stories | POSM |
