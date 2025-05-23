# Story 3.1: Implement Method-Based Blueprint Logic

## Status: Approved

## Story

As an AI agent (via Architectum), I want to request a Method-Based Blueprint by providing a file path and a list of specific method names (e.g., function names, class names), so that I can receive a focused representation of only those components within that file.

## Acceptance Criteria (ACs)

1. **AC1: Basic Method-Based Blueprint Generation** - Given a valid file path and method names, the system generates a Method-Based Blueprint.

2. **AC2: Dual Representation Integration** - The blueprint includes elements from both the Relationship Map and JSON Mirrors for the specified methods.

3. **AC3: File-Level Context Inclusion** - File-level context necessary for understanding the methods is included.

4. **AC4: Graceful Handling of Missing Methods** - If some methods are not found, the system processes found methods and reports on missing ones.

5. **AC5: YAML-Based Method Specification** - YAML-based method specification works correctly with the following format:
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

6. **AC6: Testing Requirements** - Comprehensive testing implemented:
   - At least 80% code coverage for the method selection and blueprint generation functionality
   - Implementation using pytest with file fixtures containing known methods
   - Snapshot testing for representative method selections
   - YAML testing for method specification through YAML definitions
   - Error handling tests for various error conditions (invalid file, missing methods)
   - Context testing to verify that necessary file-level context is included

## Tasks / Subtasks

- [ ] Task 1: Design Method-Based Blueprint Architecture (AC: 1, 2)
  - [ ] Subtask 1.1: Define method selection interface in blueprint generator
  - [ ] Subtask 1.2: Create method extraction logic for Relationship Map
  - [ ] Subtask 1.3: Create method extraction logic for JSON Mirrors
  - [ ] Subtask 1.4: Design method-focused blueprint data structure

- [ ] Task 2: Implement Core Method Selection Logic (AC: 1, 2, 3)
  - [ ] Subtask 2.1: Create method identification system
  - [ ] Subtask 2.2: Implement file-level context extraction
  - [ ] Subtask 2.3: Integrate method extraction with existing blueprint framework
  - [ ] Subtask 2.4: Implement blueprint assembly for method-focused content

- [ ] Task 3: Add YAML Support for Method Specification (AC: 5)
  - [ ] Subtask 3.1: Extend YAML parser to handle method type blueprints
  - [ ] Subtask 3.2: Implement method component specification validation
  - [ ] Subtask 3.3: Create method-specific YAML blueprint processing

- [ ] Task 4: Implement Error Handling and Graceful Degradation (AC: 4)
  - [ ] Subtask 4.1: Create missing method detection and reporting
  - [ ] Subtask 4.2: Implement partial blueprint generation for found methods
  - [ ] Subtask 4.3: Add user-friendly error messages and warnings

- [ ] Task 5: Comprehensive Testing Implementation (AC: 6)
  - [ ] Subtask 5.1: Create test fixtures with known methods for various languages
  - [ ] Subtask 5.2: Implement unit tests for method selection logic
  - [ ] Subtask 5.3: Create snapshot tests for method blueprint generation
  - [ ] Subtask 5.4: Implement YAML method specification tests
  - [ ] Subtask 5.5: Create error handling and edge case tests
  - [ ] Subtask 5.6: Implement context inclusion verification tests

## Dev Technical Guidance

**Key Files to Create/Modify:**
- `arch_blueprint_generator/blueprints/method_based.py` - Main method-based blueprint implementation
- `arch_blueprint_generator/yaml/method_definition.py` - YAML method specification handling
- `arch_blueprint_generator/extractors/method_extractor.py` - Method extraction logic
- `tests/blueprints/test_method_based.py` - Comprehensive test suite

**Dependencies:**
- Epic 2 must be completed, particularly Story 2.1 (YAML-Based Blueprint Definition)
- Story 1.5 (Basic File-Based Blueprint Generation) must be completed
- Requires `RelationshipMap` and `JSONMirrors` from Epic 1

**Technical Integration Points:**
- Extend the existing blueprint generation framework from Epic 1
- Leverage YAML definition system from Epic 2, Story 2.1
- Integrate with the dual representation system (Relationship Map + JSON Mirrors)
- Follow the established blueprint patterns from File-Based blueprints

**Error Handling Considerations:**
- Invalid file paths should return descriptive error messages
- Missing methods should be reported without failing the entire operation
- YAML validation should provide clear feedback on specification errors
- File parsing errors should be handled gracefully

**Testing Strategy:**
- Use pytest framework established in previous stories
- Create diverse test fixtures covering multiple programming languages
- Implement snapshot testing to catch regressions in blueprint format
- Test both success paths and error conditions comprehensively

## Story Progress Notes

### Agent Model Used: `<To be filled by implementing agent>`

### Completion Notes List
{To be filled during implementation}

### Change Log
{To be updated during implementation}
