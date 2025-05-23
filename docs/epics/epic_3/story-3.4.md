# Story 3.4: Implement Cross-File Method Analysis

## Status: Draft

## Story

As an AI agent, I want Method-Based Blueprints to include related methods from other files, so that I can understand cross-file dependencies and relationships.

## Acceptance Criteria (ACs)

1. **AC1: Cross-File Method Inclusion** - Method-Based Blueprints can include related methods from other files.

2. **AC2: YAML Cross-File Configuration** - Cross-file analysis can be configured through YAML definitions:
   ```yaml
   type: method
   name: auth-functions-blueprint
   relationship_depth: 2
   cross_file: true  # Whether to include methods from other files
   cross_file_depth: 1  # How many files away to analyze
   components:
     # ...
   ```

3. **AC3: Clear File Boundaries** - File boundaries are clearly indicated in the blueprint.

4. **AC4: Intelligent Boundary Detection** - Intelligent boundary detection prevents excessive expansion.

5. **AC5: Cross-File Context** - File context is included for cross-file methods.

6. **AC6: Testing Requirements** - Comprehensive testing implemented:
   - At least 80% code coverage for cross-file analysis functionality
   - Implementation using pytest with multi-file test fixtures
   - Snapshot testing showing cross-file method inclusion
   - Configuration testing for different cross-file depth settings
   - Boundary testing to verify intelligent boundary detection
   - Context testing to verify file context is included for cross-file methods

## Tasks / Subtasks

- [ ] Task 1: Design Cross-File Analysis Architecture (AC: 1, 3, 5)
  - [ ] Subtask 1.1: Define cross-file relationship discovery algorithms
  - [ ] Subtask 1.2: Design file boundary representation
  - [ ] Subtask 1.3: Create cross-file context inclusion framework
  - [ ] Subtask 1.4: Design multi-file blueprint structure

- [ ] Task 2: Implement Cross-File Relationship Discovery (AC: 1, 4)
  - [ ] Subtask 2.1: Implement cross-file method caller identification
  - [ ] Subtask 2.2: Implement cross-file method callee identification
  - [ ] Subtask 2.3: Add intelligent expansion boundary detection
  - [ ] Subtask 2.4: Create cross-file relationship traversal

- [ ] Task 3: Add YAML Configuration Support (AC: 2)
  - [ ] Subtask 3.1: Extend YAML parser for cross-file configuration
  - [ ] Subtask 3.2: Add cross-file depth validation
  - [ ] Subtask 3.3: Implement cross-file toggle support
  - [ ] Subtask 3.4: Create cross-file configuration documentation

- [ ] Task 4: Implement File Context and Boundaries (AC: 3, 5)
  - [ ] Subtask 4.1: Create file boundary markers in blueprints
  - [ ] Subtask 4.2: Implement cross-file context extraction
  - [ ] Subtask 4.3: Add file-specific metadata inclusion
  - [ ] Subtask 4.4: Create clear file organization in blueprint output

- [ ] Task 5: Comprehensive Testing Implementation (AC: 6)
  - [ ] Subtask 5.1: Create multi-file test fixtures
  - [ ] Subtask 5.2: Implement cross-file analysis unit tests
  - [ ] Subtask 5.3: Create snapshot tests for cross-file inclusion
  - [ ] Subtask 5.4: Test configuration options
  - [ ] Subtask 5.5: Test boundary detection algorithms
  - [ ] Subtask 5.6: Verify cross-file context inclusion

## Dev Technical Guidance

**Key Files to Create/Modify:**
- `arch_blueprint_generator/cross_file/` - New package for cross-file analysis
- `arch_blueprint_generator/cross_file/analyzer.py` - Cross-file relationship analysis
- `arch_blueprint_generator/cross_file/boundary_detector.py` - Intelligent boundary detection
- Update `arch_blueprint_generator/blueprints/method_based.py` - Integrate cross-file analysis

**Dependencies:**
- Story 3.2 (Local Relationship Mapping for Methods) must be completed
- Story 2.2 (Enhance File-Based Blueprint with Cross-File Relationships) must be completed
- Requires established cross-file relationship mapping capabilities

## Story Progress Notes

### Agent Model Used: `<To be filled by implementing agent>`

### Completion Notes List
{To be filled during implementation}

### Change Log
{To be updated during implementation}
