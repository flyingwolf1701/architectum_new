# Epic 3: Method-Based Blueprint Implementation

**Goal:** To empower Architectum with the ability to generate highly focused Method-Based Blueprints detailing specific code elements (like functions, classes, methods) within files, enabling AI agents to perform granular analysis of targeted code components and their immediate relationships.

## Story List

### Story 3.1: Implement Method-Based Blueprint Logic

- **User Story / Goal:** As an AI agent (via Architectum), I want to request a Method-Based Blueprint by providing a file path and a list of specific method names (e.g., function names, class names), so that I can receive a focused representation of only those components within that file.
- **Dependencies:**
  - Epic 2 must be completed, particularly Story 2.1 (YAML-Based Blueprint Definition)
  - Story 1.5 (Basic File-Based Blueprint Generation) must be completed
- **Detailed Requirements:**
  - Enhance the blueprint generation system to support method-level focus:
    - Accept a single file path and a list of method names
    - Extract relevant methods from both the Relationship Map and JSON Mirrors
    - Include necessary file-level context for the methods
    - Maintain relationships between the specified methods
  - Support method specification in YAML:
    ```yaml
    type: method
    name: auth-functions-blueprint
    components:
      - file: src/auth/service.js
        elements:
          - validateCredentials
          - hashPassword
          - comparePasswords
    ```
  - Ensure the blueprint includes both structural relationships and detailed content
  - Handle cases where methods cannot be found
- **Acceptance Criteria (ACs):**
  - AC1: Given a valid file path and method names, the system generates a Method-Based Blueprint.
  - AC2: The blueprint includes elements from both the Relationship Map and JSON Mirrors for the specified methods.
  - AC3: File-level context necessary for understanding the methods is included.
  - AC4: If some methods are not found, the system processes found methods and reports on missing ones.
  - AC5: YAML-based method specification works correctly.
  - **AC6: Testing Requirements:**
    - **Coverage:** At least 80% code coverage for the method selection and blueprint generation functionality
    - **Framework:** Implementation using pytest with file fixtures containing known methods
    - **Snapshot Testing:** Create snapshots for representative method selections
    - **YAML Testing:** Test method specification through YAML definitions
    - **Error Handling:** Test various error conditions (invalid file, missing methods)
    - **Context Testing:** Verify that necessary file-level context is included

### Story 3.2: Implement Local Relationship Mapping for Methods

- **User Story / Goal:** As an AI agent, I want Method-Based Blueprints to include comprehensive relationship mapping for the selected methods, so that I can understand how they interact with other code elements.
- **Dependencies:**
  - Story 3.1 (Method-Based Blueprint Logic) must be completed
  - Story 2.2 (Enhance File-Based Blueprint with Cross-File Relationships) should be completed
- **Detailed Requirements:**
  - Enhance relationship mapping for Method-Based Blueprints:
    - Identify methods that directly call the specified methods
    - Identify methods called by the specified methods
    - Include inheritance and implementation relationships
    - Include type reference relationships
  - Add configurable relationship depth:
    ```yaml
    type: method
    name: auth-functions-blueprint
    relationship_depth: 2  # How many levels of relationships to include
    components:
      # ...
    ```
  - Include metadata for each relationship to provide context
  - Support filtering of certain relationship types
- **Acceptance Criteria (ACs):**
  - AC1: Method-Based Blueprints include relationship mapping for the specified methods.
  - AC2: Both incoming and outgoing relationships are represented.
  - AC3: Relationship depth can be configured to control the scope of included relationships.
  - AC4: Relationship metadata provides context for understanding the connections.
  - AC5: Certain relationship types can be filtered if desired.
  - **AC6: Testing Requirements:**
    - **Coverage:** At least 80% code coverage for the relationship mapping functionality
    - **Framework:** Implementation using pytest with relationship test fixtures
    - **Snapshot Testing:** Create snapshots showing different relationship depths
    - **Configuration Testing:** Test different relationship depth settings
    - **Filter Testing:** Test relationship type filtering
    - **Metadata Testing:** Verify relationship metadata is correctly included

### Story 3.3: Implement Detail Level Support for Method-Based Blueprints

- **User Story / Goal:** As an AI agent, I want to request Method-Based Blueprints at different detail levels, so that I can balance comprehensiveness against token efficiency for different use cases.
- **Dependencies:**
  - Story 3.1 (Method-Based Blueprint Logic) must be completed
  - Story 2.3 (Detail Level Support for File-Based Blueprints) should be completed
- **Detailed Requirements:**
  - Implement detail level configuration specifically for Method-Based Blueprints:
    - **Minimal**: Basic method signatures and immediate relationships
    - **Standard**: Type information, parameters, and expanded relationships
    - **Detailed**: Documentation, implementation insights, and comprehensive relationships
  - Ensure the detail level can be specified in YAML definitions:
    ```yaml
    type: method
    name: auth-functions-blueprint
    detail_level: standard  # or minimal, detailed
    components:
      # ...
    ```
  - Apply detail level settings consistently across both representation sources
  - Implement smart context inclusion that adapts to detail level
- **Acceptance Criteria (ACs):**
  - AC1: Method-Based Blueprints can be generated at different detail levels.
  - AC2: Detail level can be specified in YAML definitions.
  - AC3: Minimal detail level focuses on signatures and immediate relationships.
  - AC4: Standard detail level includes type information and parameters.
  - AC5: Detailed detail level includes documentation and implementation insights.
  - AC6: Context inclusion intelligently adapts to the specified detail level.
  - **AC7: Testing Requirements:**
    - **Coverage:** At least 80% code coverage for the detail level configuration and application
    - **Framework:** Implementation using pytest with parameterized tests for detail levels
    - **Snapshot Testing:** Create snapshots comparing blueprints at different detail levels
    - **Contract Testing:** Verify blueprint formats at different detail levels meet schema requirements
    - **Context Testing:** Verify context inclusion adapts to detail level
    - **YAML Integration:** Test detail level specification in YAML definitions

### Story 3.4: Implement Cross-File Method Analysis

- **User Story / Goal:** As an AI agent, I want Method-Based Blueprints to include related methods from other files, so that I can understand cross-file dependencies and relationships.
- **Dependencies:**
  - Story 3.2 (Local Relationship Mapping for Methods) must be completed
  - Story 2.2 (Enhance File-Based Blueprint with Cross-File Relationships) must be completed
- **Detailed Requirements:**
  - Enhance Method-Based Blueprints to include cross-file analysis:
    - Identify methods in other files that call the specified methods
    - Identify methods in other files that are called by the specified methods
    - Include type dependencies from other files
    - Include inheritance relationships that span files
  - Add configuration for cross-file analysis depth:
    ```yaml
    type: method
    name: auth-functions-blueprint
    relationship_depth: 2
    cross_file: true  # Whether to include methods from other files
    cross_file_depth: 1  # How many files away to analyze
    components:
      # ...
    ```
  - Implement intelligent boundary detection to prevent excessive expansion
  - Include file context for cross-file methods
- **Acceptance Criteria (ACs):**
  - AC1: Method-Based Blueprints can include related methods from other files.
  - AC2: Cross-file analysis can be configured through YAML definitions.
  - AC3: File boundaries are clearly indicated in the blueprint.
  - AC4: Intelligent boundary detection prevents excessive expansion.
  - AC5: File context is included for cross-file methods.
  - **AC6: Testing Requirements:**
    - **Coverage:** At least 80% code coverage for the cross-file analysis functionality
    - **Framework:** Implementation using pytest with multi-file test fixtures
    - **Snapshot Testing:** Create snapshots showing cross-file method inclusion
    - **Configuration Testing:** Test different cross-file depth settings
    - **Boundary Testing:** Verify intelligent boundary detection
    - **Context Testing:** Verify file context is included for cross-file methods

### Story 3.5: Expose Method-Based Blueprints via Enhanced API/CLI

- **User Story / Goal:** As a developer or another service, I want comprehensive CLI and API access to Method-Based Blueprint functionality, so that I can easily create, retrieve, and utilize method-focused blueprints in my workflows.
- **Dependencies:**
  - Story 3.1-3.4 must be completed
  - Story 2.5 (Expose File-Based Blueprints via Enhanced API/CLI) should be completed
- **Detailed Requirements:**
  - Enhance the CLI for Method-Based Blueprints:
    - `architectum blueprint method -f file.js -c method1,method2` for direct creation
    - `architectum blueprint create -f method-blueprint.yaml` for YAML-based creation
    - Support for different output formats and destinations
  - If API-based: Implement comprehensive endpoints for method blueprint management
  - Add support for combining multiple method blueprints
  - Include filtering options for relationships and methods
  - Provide comprehensive help and examples
- **Acceptance Criteria (ACs):**
  - AC1: Enhanced CLI commands successfully manage Method-Based Blueprints.
  - AC2: All commands include appropriate options and parameters.
  - AC3: Blueprint combination produces valid merged blueprints.
  - AC4: Filtering options effectively control blueprint content.
  - AC5: Help documentation includes clear examples and usage guidance.
  - **AC6: Testing Requirements:**
    - **Coverage:** At least 80% code coverage for the enhanced CLI/API functionality
    - **Framework:** Implementation using pytest with CLI invocation testing
    - **Integration Testing:** End-to-end tests for all commands and options
    - **Combination Testing:** Test blueprint merging with various method selections
    - **Filter Testing:** Test relationship and method filtering options
    - **Documentation Testing:** Verify help output and examples

## Implementation Sequence

The implementation of this epic should follow this sequence:

1. Method-Based Blueprint Logic (Story 3.1)
2. Local Relationship Mapping for Methods (Story 3.2)
3. Detail Level Support (Story 3.3) and Cross-File Method Analysis (Story 3.4) can be implemented in parallel
4. Expose Method-Based Blueprints via Enhanced API/CLI (Story 3.5)

## Change Log

| Change        | Date       | Version | Description                    | Author         |
| ------------- | ---------- | ------- | ------------------------------ | -------------- |
| Initial draft | 05-16-2025 | 0.1     | Initial draft of Epic 3        | Product Manager |
| Updated with graph approach | 05-17-2025 | 0.2 | Enhanced Epic 3 with graph-based model | Technical Scrum Master |
| Added testing requirements | 05-17-2025 | 0.3 | Added comprehensive testing strategy | Technical Scrum Master |
| Refined architecture | 05-18-2025 | 0.4 | Updated to reflect Method-Based Blueprint approach and YAML definition | System Architect |
| Added dependencies | 05-18-2025 | 0.5 | Added explicit dependencies to stories | POSM |
| Updated terminology | 05-19-2025 | 0.6 | Changed "Component-Based Blueprint" to "Method-Based Blueprint" for consistency | POSM |