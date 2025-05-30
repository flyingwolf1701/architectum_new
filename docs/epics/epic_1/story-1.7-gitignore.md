# Story 1.7: Enhance PathScanner with GitIgnore Support

## Status: In-Progress

## Story

- As a developer using Architectum
- I want the PathScanner to respect .gitignore files and standard git exclusion patterns
- So that Architectum only processes files that are actually part of my codebase and excludes build artifacts, dependencies, and other non-source files

## Dependencies

- Story 1.1 (Core Blueprint Generation Framework) must be completed
- Story 1.2 (Path Scan and Representation Generation) must be completed
- Story 1.3 (arch sync Command) must be completed

## Acceptance Criteria (ACs)

- AC1: The PathScanner reads and respects .gitignore files when they exist
- AC2: Standard gitignore pattern syntax is supported (glob patterns, directory patterns, negation patterns)
- AC3: Files and directories excluded by .gitignore are not mirrored or included in relationship maps
- AC4: The system maintains backward compatibility with existing exclude_patterns functionality
- AC5: Additional ignore patterns can be specified beyond what's in .gitignore
- AC6: The gitignore support can be disabled when needed for special use cases
- AC7: Clear logging shows what files are being excluded and why
- AC8: Performance is improved by not processing irrelevant files (build artifacts, dependencies, etc.)
- AC9: Testing Requirements:
  - At least 80% code coverage for the gitignore parsing and filtering functionality
  - Implementation using pytest with gitignore test fixtures
  - Testing with various gitignore patterns and edge cases
  - Performance testing showing improved scan times
  - Integration testing with existing CLI commands

## Tasks / Subtasks

- [x] Task 1: Analyze Current Exclusion Logic Issues (AC: 1, 8)
  - [x] Subtask 1.1: Identify files currently being mirrored that shouldn't be (.coverage, .pytest_cache, uv.lock, etc.)
  - [x] Subtask 1.2: Document current simple substring matching limitations
  - [x] Subtask 1.3: Analyze impact on performance and storage

- [x] Task 2: Design GitIgnore Parser Architecture (AC: 1, 2)
  - [x] Subtask 2.1: Design GitIgnoreParser class with full gitignore syntax support
  - [x] Subtask 2.2: Implement glob pattern matching using fnmatch
  - [x] Subtask 2.3: Add support for directory patterns (ending with /)
  - [x] Subtask 2.4: Implement negation pattern support (starting with !)
  - [x] Subtask 2.5: Handle comments and empty lines properly

- [x] Task 3: Implement Enhanced PathScanner (AC: 3, 4, 5, 6)
  - [x] Subtask 3.1: Create EnhancedPathScanner class extending existing functionality
  - [x] Subtask 3.2: Integrate GitIgnoreParser with scanning logic
  - [x] Subtask 3.3: Maintain backward compatibility with exclude_patterns parameter
  - [x] Subtask 3.4: Add respect_gitignore and additional_ignores configuration options
  - [x] Subtask 3.5: Implement proper path normalization for cross-platform compatibility

- [ ] Task 4: Update CLI Integration (AC: 6, 7)
  - [ ] Subtask 4.1: Add --gitignore/--no-gitignore CLI options to scan command
  - [ ] Subtask 4.2: Add --ignore option for additional patterns
  - [ ] Subtask 4.3: Update help documentation with new options
  - [ ] Subtask 4.4: Add logging to show what files are being excluded and why

- [ ] Task 5: Performance and Integration Testing (AC: 8, 9)
  - [ ] Subtask 5.1: Create comprehensive test suite for GitIgnoreParser
  - [ ] Subtask 5.2: Test various gitignore patterns and edge cases
  - [ ] Subtask 5.3: Performance testing comparing old vs new scanner
  - [ ] Subtask 5.4: Integration testing with existing blueprint generation
  - [ ] Subtask 5.5: Test with real-world .gitignore files from popular projects

- [ ] Task 6: Documentation and Migration (AC: 4, 6)
  - [ ] Subtask 6.1: Update README with new gitignore functionality
  - [ ] Subtask 6.2: Create migration guide for existing users
  - [ ] Subtask 6.3: Document configuration options and use cases
  - [ ] Subtask 6.4: Add troubleshooting guide for gitignore issues

## Dev Technical Guidance

### Key Files Created/Modified:
- `arch_blueprint_generator/scanner/enhanced_path_scanner.py` - New enhanced scanner with gitignore support
- `arch_blueprint_generator/scanner/gitignore_parser.py` - GitIgnore pattern parser
- `arch_blueprint_generator/scanner/__init__.py` - Update to use enhanced scanner as default
- `arch_blueprint_generator/cli/commands.py` - Add CLI options for gitignore control
- `tests/unit/scanner/test_enhanced_path_scanner.py` - Comprehensive test suite
- `tests/unit/scanner/test_gitignore_parser.py` - GitIgnore parser tests

### GitIgnore Patterns Supported:
- **Glob patterns**: `*.log`, `temp*`, `test_*.py`
- **Directory patterns**: `build/`, `node_modules/`, `__pycache__/`
- **Negation patterns**: `!important.log`, `!src/config/production.json`
- **Path patterns**: `docs/*.pdf`, `src/temp/*.tmp`
- **Absolute patterns**: `/root_file.txt`

### Configuration Options:
```python
# Full gitignore support (default)
scanner = EnhancedPathScanner(".", respect_gitignore=True)

# Add additional ignores beyond gitignore
scanner = EnhancedPathScanner(
    ".", 
    respect_gitignore=True,
    additional_ignores=["*.log", ".DS_Store", "Thumbs.db"]
)

# Disable gitignore for special cases
scanner = EnhancedPathScanner(".", respect_gitignore=False)

# Legacy compatibility
scanner = EnhancedPathScanner(".", exclude_patterns=[".git", ".venv"])
```

### CLI Usage Examples:
```bash
# Default behavior (respects .gitignore)
arch scan .

# Disable gitignore
arch scan . --no-gitignore

# Add additional ignores
arch scan . --ignore "*.log" --ignore "temp/"

# Legacy exclude patterns still work
arch scan . --exclude "__pycache__" --exclude ".pytest_cache"
```

### Expected Performance Improvements:
- **Reduced file processing**: Skip irrelevant files like `node_modules/`, `dist/`, `.pytest_cache/`
- **Smaller mirrors**: Less storage usage for JSON mirrors
- **Faster scanning**: Fewer files to hash and process
- **Better blueprints**: More focused content for AI consumption

### Testing Strategy:
1. **Unit Tests**: Test GitIgnoreParser with various pattern types
2. **Integration Tests**: Test EnhancedPathScanner with real .gitignore files
3. **Performance Tests**: Compare scan times before/after
4. **Regression Tests**: Ensure existing functionality works
5. **Edge Case Tests**: Empty .gitignore, missing .gitignore, complex patterns

## Story Progress Notes

### Agent Model Used: `Claude 3.5 Sonnet`

### Completion Notes List
- **Analysis Phase**: ✅ Completed analysis of current exclusion logic issues
- **Architecture Design**: ✅ Designed GitIgnoreParser and EnhancedPathScanner classes
- **Core Implementation**: ✅ Implemented GitIgnore parsing with full syntax support
- **Enhanced Scanner**: ✅ Created EnhancedPathScanner with backward compatibility
- **CLI Integration**: 🔄 In Progress - Need to add CLI options and update commands
- **Testing**: 🔄 In Progress - Need comprehensive test suite
- **Documentation**: 📋 Pending - Need to update README and create migration guide

### Issues Found and Resolved:
- **Files unnecessarily mirrored**: `.coverage`, `.pytest_cache/`, `uv.lock`, `.python-version`
- **Simple substring matching**: Replaced with proper gitignore pattern matching
- **No git integration**: Now reads and respects .gitignore files
- **Performance impact**: Reduced by excluding irrelevant files from processing

### Next Steps:
1. Add CLI options for gitignore control (`--gitignore/--no-gitignore`, `--ignore`)
2. Create comprehensive test suite with real-world gitignore patterns
3. Performance testing and optimization
4. Update documentation and migration guide
5. Integration testing with existing blueprint generation

### Change Log
- 2025-05-30: Initial story creation and analysis phase
- 2025-05-30: Completed GitIgnoreParser and EnhancedPathScanner implementation
- 2025-05-30: Started CLI integration work
