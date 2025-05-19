# Epic 1: Core Blueprint Generation Framework and Dual Representation Implementation

**Goal:** To establish the foundational infrastructure for Architectum's blueprint generation system with its dual representation approach (Relationship Map and JSON Mirrors), and to deliver basic blueprint capabilities that enable AI agents and visualization tools to analyze code structures at varying levels of detail.

## Story List

### Story 1.1: Setup Blueprint Generation Core Module with Dual Representation Model

- **User Story / Goal:** As a system architect, I want a core module for blueprint generation established with both a Relationship Map model and JSON Mirrors structure, so that different blueprint types can be developed and integrated in a consistent and maintainable manner within the existing Architectum repository.
- **Detailed Requirements:**
  - **Establish a new module or package named `arch_blueprint_generator` within the existing `Architectum` repository to house the blueprint generation capabilities.**
  - Design and implement the core dual representation model:
    - **Relationship Map**: Define a node-relationship structure for navigation efficiency
      - Define node types (files, functions, classes, methods, features)
      - Define relationship types (contains, calls, implements, imports, inherits)
      - Create base classes/interfaces for nodes and relationships
    - **JSON Mirrors**: Define a structure for detailed content representation
      - Create parallel file structure that mirrors the codebase
      - Define JSON schema for file content representation
  - Implement basic operations for both representations (creation, navigation, update)
  - Create serialization/deserialization support for both models
  - Implement a basic command-line interface (CLI) or an API endpoint structure
  - Set up initial logging and error handling mechanisms for the module
  - Include a basic README for this new module, outlining its purpose and how to use it
- **Acceptance Criteria (ACs):**
  - AC1: The new module/package `arch_blueprint_generator` is created within the `Architectum` repository and is buildable/integrable with the main project.
  - AC2: The Relationship Map model is implemented with support for nodes, relationships, and efficient navigation.
  - AC3: The JSON Mirrors structure is implemented with the ability to create and access JSON representations of source files.
  - AC4: Basic operations for both representations are functional and can be used independently.
  - AC5: A placeholder CLI command or API endpoint exists and returns a "not yet implemented" message or basic help.
  - AC6: Basic logging for module initialization and errors is functional.
  - AC7: The module includes a README with an overview of the dual representation approach.
  - **AC8: Testing Requirements:**
    - **Coverage:** At least 80% code coverage for both representation models and core operations
    - **Framework:** Implementation using pytest for unit testing
    - **Property Testing:** Use hypothesis to test operations with property-based tests for robustness across random inputs
    - **Test Cases:** Must include tests for node creation, relationship establishment, and JSON mirror operations
    - **Documentation:** Test cases must document expected behavior through descriptive test names and docstrings

### Story 1.2: Implement Basic Path Scan and Representation Generation

- **User Story / Goal:** As an AI agent (via Architectum), I want to request a Path Scan and have both representations generated, so that I can access both navigation-focused and content-focused views of a specified directory.
- **Dependencies:**
  - Story 1.1 (Core Blueprint Generation Framework) must be completed
  - Relationship Map and JSON Mirrors models must be implemented and tested
  - Basic CLI structure must be in place
  - Parser interfaces must be defined
- **Detailed Requirements:**
  - Implement the logic to traverse a path structure based on a given path and depth parameter.
  - For each directory and file encountered:
    - Create appropriate nodes in the Relationship Map
    - Create JSON mirror representations for each source file
  - Establish "contains" relationships between directories and their contents in the Relationship Map.
  - For each file, extract basic information (e.g., filename, path, extension) for both representations.
  - Handle cases where the provided path is invalid or inaccessible.
  - Implement a unified interface for requesting Path Scans that updates both representations.
- **Acceptance Criteria (ACs):**
  - AC1: Given a valid directory path and depth, the system generates both a Relationship Map and JSON Mirrors for the path structure.
  - AC2: Given an invalid directory path, the system returns an appropriate error.
  - AC3: The Relationship Map correctly represents nested structures of directories and files with "contains" relationships.
  - AC4: The JSON Mirrors structure correctly contains JSON representations for each source file.
  - AC5: Scan depth 0 correctly scans all subdirectories and files.
  - AC6: Scan depth 1 correctly scans only the immediate files and folders in the specified directory.
  - **AC7: Testing Requirements:**
    - **Coverage:** At least 80% code coverage for the path traversal and representation generation functionality
    - **Framework:** Implementation using pytest with appropriate fixtures for file system operations
    - **Mocking:** Tests should use mock file systems to avoid external dependencies
    - **Contract Testing:** Use pact to verify the JSON outputs match the expected schemas
    - **Snapshot Testing:** Create snapshot tests for representative path structures
    - **Edge Cases:** Tests must cover error conditions, empty directories, and unusual file names

### Story 1.3: Implement 'arch sync' Command for Representation Updates

- **User Story / Goal:** As a developer, I want to use the `arch sync` command to synchronize code changes with Architectum's representations, so that both the Relationship Map and JSON Mirrors remain up to date.
- **Dependencies:**
  - Story 1.1 (Core Blueprint Generation Framework) must be completed
  - Story 1.2 (Path Scan) must be completed
- **Detailed Requirements:**
  - Implement a command-line interface for the `arch sync` command with the following options:
    - Sync a specific file
    - Sync a directory
    - Sync open/modified files (foundation for IDE integration)
  - Create a change detection mechanism to identify which files have changed since last sync
  - Implement incremental updates for both representations:
    - Update only affected nodes and relationships in the Relationship Map
    - Update only changed files in the JSON Mirrors
  - Add status reporting to show which files were synchronized
  - Implement error handling for synchronization failures
- **Acceptance Criteria (ACs):**
  - AC1: The `arch sync` command successfully updates both representations when files change.
  - AC2: Only changed files are processed, improving performance for incremental updates.
  - AC3: The command supports synchronizing individual files, directories, and multiple files.
  - AC4: Status information is displayed showing which files were synchronized.
  - AC5: Proper error handling is implemented for synchronization failures.
  - **AC6: Testing Requirements:**
    - **Coverage:** At least 80% code coverage for the synchronization functionality
    - **Framework:** Implementation using pytest with file modification simulation
    - **Mocking:** Mock file changes to test change detection
    - **Integration Testing:** End-to-end tests for the sync command with various parameters
    - **Performance Testing:** Verify incremental updates are significantly faster than full scans
    - **Error Handling:** Test recovery from various error conditions during synchronization

### Story 1.4: Implement Detail Level Configuration for Representations

- **User Story / Goal:** As an AI agent or developer, I want to configure the detail level of the representations, so that I can control the balance between comprehensiveness and efficiency for different use cases.
- **Dependencies:**
  - Story 1.1 (Core Blueprint Generation Framework) must be completed
  - Story 1.2 (Path Scan) must be completed
- **Detailed Requirements:**
  - Implement detail level configuration for both representations:
    - **Minimal**: Basic structure and relationship information, optimized for navigation efficiency
    - **Standard**: Additional type information and signatures, balancing detail and efficiency
    - **Detailed**: Comprehensive information including documentation, maximizing completeness
  - For the Relationship Map:
    - Minimal: Basic node types and primary relationships
    - Standard: Enhanced metadata and secondary relationships
    - Detailed: Comprehensive metadata and full relationship network
  - For JSON Mirrors:
    - Minimal: Basic file structure and element signatures
    - Standard: Type information and interface details
    - Detailed: Documentation and implementation insights
  - Allow per-representation detail level configuration
  - Implement mechanisms to apply detail level settings during generation
- **Acceptance Criteria (ACs):**
  - AC1: Detail level configuration can be specified for both representations independently.
  - AC2: The Minimal detail level produces streamlined representations for efficiency.
  - AC3: The Standard detail level includes type information and signatures.
  - AC4: The Detailed detail level includes comprehensive information including documentation.
  - AC5: Detail level settings are correctly applied during representation generation.
  - **AC6: Testing Requirements:**
    - **Coverage:** At least 80% code coverage for the detail level configuration functionality
    - **Framework:** Implementation using pytest with parameterized tests for detail levels
    - **Snapshot Testing:** Create snapshots comparing representations at different detail levels
    - **Contract Testing:** Verify outputs at different detail levels meet schema requirements
    - **Performance Testing:** Measure representation size and generation time at different detail levels
    - **Configuration Testing:** Test application of different detail level combinations

### Story 1.5: Implement Basic File-Based Blueprint Generation

- **User Story / Goal:** As an AI agent, I want to request a basic File-Based Blueprint, so that I can receive a focused view of specific files regardless of their location in the path structure.
- **Dependencies:**
  - Story 1.1 (Core Blueprint Generation Framework) must be completed
  - Story 1.2 (Path Scan) must be completed
  - Story 1.4 (Detail Level Configuration) must be completed
- **Detailed Requirements:**
  - Implement the infrastructure for blueprint generation based on the dual representations
  - Create a File-Based Blueprint generator that:
    - Accepts a list of file paths
    - Extracts relevant sections from both the Relationship Map and JSON Mirrors
    - Combines them into a unified blueprint structure
    - Preserves relationships between the specified files
  - Create serialization support for the blueprint (initially JSON)
  - Handle cases where specified files don't exist or aren't accessible
  - Support different detail level configurations
- **Acceptance Criteria (ACs):**
  - AC1: Given a list of valid file paths, the system generates a File-Based Blueprint.
  - AC2: The blueprint includes elements from both the Relationship Map and JSON Mirrors.
  - AC3: Relationships between files are preserved in the blueprint.
  - AC4: Different detail levels produce appropriately varied blueprint contents.
  - AC5: Invalid file paths are handled gracefully with appropriate error messages.
  - **AC6: Testing Requirements:**
    - **Coverage:** At least 80% code coverage for the File-Based Blueprint generation functionality
    - **Framework:** Implementation using pytest with file fixture sets
    - **Snapshot Testing:** Create snapshots for various file combinations and detail levels
    - **Contract Testing:** Verify blueprint outputs meet schema requirements
    - **Error Handling:** Test responses to invalid paths and other error conditions
    - **Detail Level Testing:** Verify blueprint content varies appropriately with detail level settings

### Story 1.6: Expose Blueprint Generation via Initial API/CLI

- **User Story / Goal:** As a developer or another service, I want to trigger blueprint generation via a defined API endpoint or CLI command within Architectum, so that I can integrate this capability into other tools or workflows.
- **Dependencies:**
  - Story 1.1 (Core Blueprint Generation Framework) must be completed
  - Story 1.5 (Basic File-Based Blueprint Generation) must be completed
- **Detailed Requirements:**
  - Implement a CLI interface for blueprint generation:
    - `architectum blueprint file --files <file1,file2> --level <level>` for File-Based Blueprints
    - Support for different output formats (JSON, potentially XML)
    - Options for output destination (stdout, file)
  - If API-based: Define and implement an endpoint (e.g., `POST /blueprints/file`) that accepts file paths and detail level parameters.
  - Integrate the blueprint generation with the existing `arch sync` command to ensure representations are up to date.
  - Add appropriate error handling and validation.
  - Include comprehensive help documentation.
- **Acceptance Criteria (ACs):**
  - AC1: The CLI command successfully triggers blueprint generation.
  - AC2: All required parameters can be passed and are correctly used.
  - AC3: Generated blueprints are correctly output in the specified format.
  - AC4: Output format and destination options are functional.
  - AC5: Proper error handling is implemented for invalid inputs or generation failures.
  - AC6: Help documentation is clear and comprehensive.
  - **AC7: Testing Requirements:**
    - **Coverage:** At least 80% code coverage for the CLI implementation and output handling
    - **Framework:** Implementation using pytest with CLI invocation testing
    - **Integration Testing:** End-to-end tests calling the CLI with various parameters
    - **Contract Testing:** Verify the output format options produce valid outputs
    - **Parameter Testing:** Test all parameter combinations and error handling
    - **Output Format Testing:** Test different output formats if implemented

## Implementation Sequence

The implementation of this epic should follow this sequence:

1. Core Blueprint Generation Framework (Story 1.1)
2. Basic Path Scan (Story 1.2)
3. Detail Level Configuration (Story 1.4) and arch sync Command (Story 1.3) can be implemented in parallel
4. Basic File-Based Blueprint Generation (Story 1.5)
5. Expose Blueprint Generation via Initial API/CLI (Story 1.6)

## Change Log

| Change        | Date       | Version | Description                    | Author         |
| ------------- | ---------- | ------- | ------------------------------ | -------------- |
| Initial draft | 05-16-2025 | 0.1     | Initial draft of Epic 1        | Product Manager |
| Updated with graph approach | 05-17-2025 | 0.2 | Enhanced Epic 1 with graph-based model | Technical Scrum Master |
| Added testing requirements | 05-17-2025 | 0.3 | Added comprehensive testing strategy | Technical Scrum Master |
| Refined architecture | 05-18-2025 | 0.4 | Updated to reflect dual representation and revised blueprint approach | System Architect |
| Added dependencies | 05-18-2025 | 0.5 | Added explicit dependencies to stories | POSM |
| Updated terminology | 05-19-2025 | 0.6 | Changed "Directory Scan" to "Path Scan" for consistency | POSM |