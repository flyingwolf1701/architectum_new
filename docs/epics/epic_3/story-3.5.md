# Story 3.5: Expose Method-Based Blueprints via Enhanced API/CLI

## Status: Draft

## Story

As a developer or another service, I want comprehensive CLI and API access to Method-Based Blueprint functionality, so that I can easily create, retrieve, and utilize method-focused blueprints in my workflows.

## Acceptance Criteria (ACs)

1. **AC1: Enhanced CLI Commands** - Enhanced CLI commands successfully manage Method-Based Blueprints:
   - `architectum blueprint method -f file.js -c method1,method2` for direct creation
   - `architectum blueprint create -f method-blueprint.yaml` for YAML-based creation

2. **AC2: Comprehensive Command Options** - All commands include appropriate options and parameters for:
   - Output format selection
   - Detail level specification
   - Relationship depth configuration
   - Cross-file analysis options

3. **AC3: Blueprint Combination** - Blueprint combination produces valid merged blueprints.

4. **AC4: Filtering Options** - Filtering options effectively control blueprint content.

5. **AC5: Documentation and Help** - Help documentation includes clear examples and usage guidance.

6. **AC6: Testing Requirements** - Comprehensive testing implemented:
   - At least 80% code coverage for enhanced CLI/API functionality
   - Implementation using pytest with CLI invocation testing
   - End-to-end integration tests for all commands and options
   - Combination testing for blueprint merging with various method selections
   - Filter testing for relationship and method filtering options
   - Documentation testing to verify help output and examples

## Tasks / Subtasks

- [ ] Task 1: Design Enhanced CLI Architecture (AC: 1, 2)
  - [ ] Subtask 1.1: Design method-specific CLI command structure
  - [ ] Subtask 1.2: Define comprehensive option and parameter sets
  - [ ] Subtask 1.3: Create CLI argument validation
  - [ ] Subtask 1.4: Design output format handling

- [ ] Task 2: Implement Method-Specific CLI Commands (AC: 1, 2)
  - [ ] Subtask 2.1: Implement direct method blueprint creation command
  - [ ] Subtask 2.2: Implement YAML-based method blueprint creation
  - [ ] Subtask 2.3: Add comprehensive option support
  - [ ] Subtask 2.4: Integrate with existing CLI framework

- [ ] Task 3: Implement Blueprint Combination (AC: 3)
  - [ ] Subtask 3.1: Design blueprint merging algorithms
  - [ ] Subtask 3.2: Implement method blueprint combination logic
  - [ ] Subtask 3.3: Add conflict resolution for overlapping methods
  - [ ] Subtask 3.4: Create combined blueprint validation

- [ ] Task 4: Add Filtering and Control Options (AC: 4)
  - [ ] Subtask 4.1: Implement relationship filtering options
  - [ ] Subtask 4.2: Add method selection filtering
  - [ ] Subtask 4.3: Create output content control options
  - [ ] Subtask 4.4: Add performance optimization filters

- [ ] Task 5: Create Documentation and Help (AC: 5)
  - [ ] Subtask 5.1: Create comprehensive help documentation
  - [ ] Subtask 5.2: Add practical usage examples
  - [ ] Subtask 5.3: Create command reference documentation
  - [ ] Subtask 5.4: Add troubleshooting guides

- [ ] Task 6: Comprehensive Testing Implementation (AC: 6)
  - [ ] Subtask 6.1: Create CLI invocation tests
  - [ ] Subtask 6.2: Implement end-to-end integration tests
  - [ ] Subtask 6.3: Test blueprint combination functionality
  - [ ] Subtask 6.4: Test filtering options
  - [ ] Subtask 6.5: Verify help and documentation output
  - [ ] Subtask 6.6: Test error handling and edge cases

## Dev Technical Guidance

**Key Files to Create/Modify:**
- `arch_blueprint_generator/cli/method_commands.py` - Method-specific CLI commands
- `arch_blueprint_generator/cli/blueprint_merger.py` - Blueprint combination logic
- `arch_blueprint_generator/cli/filters.py` - CLI filtering options
- Update `arch_blueprint_generator/cli/commands.py` - Integrate new commands

**Dependencies:**
- Stories 3.1-3.4 must be completed
- Story 2.5 (Expose File-Based Blueprints via Enhanced API/CLI) should be completed
- Requires established CLI framework from previous epics

## Story Progress Notes

### Agent Model Used: `<To be filled by implementing agent>`

### Completion Notes List
{To be filled during implementation}

### Change Log
{To be updated during implementation}
