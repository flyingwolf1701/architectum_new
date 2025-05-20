# Story 1.3: Implement 'arch sync' Command for Representation Updates

## Status: Completed

## Story

- As a developer using Architectum
- I want an efficient 'arch sync' command that updates representations only for changed files
- So that I can keep the blueprint representations in sync with my code without unnecessary processing

## Dependencies

- Story 1.1: Setup Blueprint Generation Core Module with Dual Representation Model
- Story 1.2: Implement Path Scanner for Initial Representation Generation

## Acceptance Criteria (ACs)

- AC1: ✅ The 'arch sync' command updates both the Relationship Map and JSON Mirrors representations for specified files or directories.
- AC2: ✅ The command detects file changes using hash comparisons stored in the JSON Mirrors.
- AC3: ✅ Incremental updates process only modified files, newly added files, and deleted files.
- AC4: ✅ The command supports synchronizing individual files, directories, or multiple paths specified as command arguments.
- AC5: ✅ The command has a '--recursive' flag to process subdirectories and a '--force' flag to override incrementality.
- AC6: ✅ Tests demonstrate that incremental updates are faster than full rescans when only a few files have changed.

## Tasks / Subtasks

- [x] Design and implement ChangeTracker class for detecting file changes (AC2)
  - [x] Create method to detect modified files using hash comparison
  - [x] Create method to detect new files
  - [x] Create method to detect deleted files
  - [x] Implement path filtering to focus change detection on specified paths

- [x] Implement ArchSync class for synchronization logic (AC1, AC3)
  - [x] Create incremental update path for processing only changed files
  - [x] Create force rescan path for processing all files
  - [x] Implement file add/update/remove operations
  - [x] Handle file-specific and directory synchronization

- [x] Update CLI interface with sync command (AC4, AC5)
  - [x] Implement multiple path arguments support
  - [x] Add recursive and force flag options
  - [x] Create detailed help text and usage examples
  - [x] Implement error handling for synchronization failures

- [x] Create comprehensive test suite (AC6)
  - [x] Implement unit tests for the ChangeTracker class
  - [x] Implement unit tests for the ArchSync class
  - [x] Implement unit tests for the CLI sync command
  - [x] Create performance tests comparing incremental vs. full updates
  - [x] Ensure at least 80% code coverage

## Dev Technical Guidance

The 'arch sync' command is a critical component for the developer experience with Architectum. It should be optimized for performance, particularly when dealing with large codebases where only a few files have changed.

### File Change Detection

Use the file hash tracking that is already implemented in the JSONMirrors class. When a file changes, its hash will be different from the stored hash in the JSON mirror.

### Implementation Approach

1. Create a ChangeTracker class to detect which files have changed
2. Create an ArchSync class to implement the synchronization logic
3. Update the CLI interface to use these components

### Performance Considerations

- Only process files that have actually changed
- Avoid re-parsing files that haven't changed
- Implement targeted updates to the relationship map rather than rebuilding it

## Story Progress Notes

### Agent Model Used: `Claude 3.7 Sonnet`

### Completion Notes List
- Implemented ChangeTracker class for detecting modified, new, and deleted files
- Created ArchSync class with both incremental and force synchronization options
- Updated CLI interface with improved path handling and recursive/force flags
- Added comprehensive test suite with performance comparison
- Implemented path expansion and filtering for directory synchronization
- Added efficient representation cleanup for removed files

### QA Testing Guide
To verify this implementation:

1. **Setup**:
   - Create a test directory with multiple files and subdirectories
   - Run the initial scan: `python -m arch_blueprint_generator scan test_directory`

2. **Basic Synchronization**:
   - Modify a file in the test directory
   - Run: `python -m arch_blueprint_generator sync test_directory`
   - Verify the command reports the file as updated

3. **Force Rescan**:
   - Run: `python -m arch_blueprint_generator sync test_directory --force`
   - Verify all files are processed

4. **Recursive Synchronization**:
   - Create a new file in a subdirectory
   - Run: `python -m arch_blueprint_generator sync test_directory --recursive`
   - Verify the new file is detected and processed

5. **Performance Testing**:
   - Create a large directory with many files
   - Run an initial sync with force: `python -m arch_blueprint_generator sync large_directory --force`
   - Modify a single file
   - Run incremental sync and compare execution time: `python -m arch_blueprint_generator sync large_directory`

6. **Multiple Paths**:
   - Run: `python -m arch_blueprint_generator sync file1.txt file2.py directory/`
   - Verify all specified paths are processed correctly

### Change Log
- Initial implementation of ChangeTracker class
- Initial implementation of ArchSync class
- Updated CLI interface for sync command
- Added unit tests for ChangeTracker
- Added unit tests for ArchSync
- Added unit tests for sync command
- Added integration tests
- Updated documentation