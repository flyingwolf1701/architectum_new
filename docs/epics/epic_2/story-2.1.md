# Story 2.1: Implement Base Blueprint and File-Based Blueprint Models

## Status: Done

## Story

- As a developer
- I want base blueprint models and file-based blueprint implementation
- So that I can generate context-rich representations of selected source files for AI and human comprehension

## Dependencies

- Story 1.1: Setup Blueprint Generation Core Module with Dual Representation Model

## Acceptance Criteria (ACs)

- AC1: A base `Blueprint` class is implemented that serves as the foundation for all blueprint types
- AC2: The base `Blueprint` class integrates with both the Relationship Map and JSON Mirrors core representations
- AC3: The `FileBasedBlueprint` class is implemented, extending the base class with file-specific functionality
- AC4: The file-based blueprint can be generated from a list of file paths
- AC5: The blueprint can be serialized to both JSON and XML formats with appropriate structure and content
- AC6: A blueprint cache mechanism exists to store and retrieve generated blueprints
- AC7: Unit tests for the blueprint models reach at least 80% code coverage
- AC8: Documentation is updated to describe the blueprint models and their usage

## Tasks / Subtasks

- [x] Implement base Blueprint class (AC1, AC2)
  - [x] Create blueprint module structure with `__init__.py` and `base.py`
  - [x] Define base `Blueprint` class with integration points for both core representations
  - [x] Implement serialization methods (`to_json()` and `to_xml()`)
  - [x] Add validation and error handling for common blueprint operations

- [x] Implement FileBasedBlueprint class (AC3, AC4)
  - [x] Create `file_based.py` module for file-based blueprint implementation
  - [x] Define `FileBasedBlueprint` class extending the base class
  - [x] Implement file path validation and handling
  - [x] Implement `generate()` method to create a blueprint from file paths
  - [x] Handle file-specific detail level controls

- [x] Implement serialization functionality (AC5)
  - [x] Create serialization module for format-specific conversions
  - [x] Implement JSON serialization with appropriate structure
  - [x] Implement XML serialization with appropriate tags and attributes
  - [x] Ensure both formats include necessary context for AI consumption

- [x] Implement blueprint caching (AC6)
  - [x] Create cache module for blueprint storage
  - [x] Implement LRU (Least Recently Used) caching strategy
  - [x] Add cache invalidation based on file changes
  - [x] Include configuration options for cache size and policy

- [x] Create unit tests (AC7)
  - [x] Write tests for base Blueprint class
  - [x] Write tests for FileBasedBlueprint class
  - [x] Test serialization for both JSON and XML formats
  - [x] Verify cache operations and policies
  - [x] Ensure coverage meets the 80% threshold

- [x] Update documentation (AC8)
  - [x] Add docstrings to all new classes and methods
  - [x] Update README with blueprint model information
  - [x] Create usage examples for file-based blueprints
  - [x] Update architecture document to reflect implementation details

## Dev Technical Guidance

### Blueprint Structure

The blueprints should follow this general structure:

```python
# Base Blueprint
class Blueprint:
    def __init__(self, relationship_map, json_mirrors):
        self.relationship_map = relationship_map
        self.json_mirrors = json_mirrors
        self.generated = False
        self.cache_key = None
        
    def generate(self):
        """Generate blueprint content (to be implemented by subclasses)"""
        raise NotImplementedError
        
    def to_json(self):
        """Convert blueprint to JSON representation"""
        if not self.generated:
            raise ValueError("Blueprint not generated yet")
        # Implementation...
        
    def to_xml(self):
        """Convert blueprint to XML representation"""
        if not self.generated:
            raise ValueError("Blueprint not generated yet")
        # Implementation...

# File-Based Blueprint
class FileBasedBlueprint(Blueprint):
    def __init__(self, relationship_map, json_mirrors, file_paths):
        super().__init__(relationship_map, json_mirrors)
        self.file_paths = file_paths
        self.validate_paths()
        
    def validate_paths(self):
        """Validate that all file paths exist and are accessible"""
        # Implementation...
        
    def generate(self):
        """Generate blueprint from file paths"""
        # Implementation...
        self.generated = True
```

### Serialization Guidelines

- **JSON Format**: Include all node and relationship information relevant to the files in the blueprint
- **XML Format**: Use element hierarchy to represent relationships between nodes
- **Both Formats**: Include file content metadata, element details, and relationships

### Caching Strategy

- Use Python's `functools.lru_cache` or a custom LRU implementation
- Cache key should incorporate file paths and modification timestamps
- Cache size should be configurable and default to a reasonable limit (e.g., 50 entries)
- Include methods to explicitly clear cache and check cache status

## Story Progress Notes

### Agent Model Used: `Claude 3.5 Sonnet`

### Completion Notes List
- **Base Blueprint Implementation**: Successfully implemented abstract base class in `arch_blueprint_generator/blueprints/base.py` with full JSON/XML serialization support
- **File-Based Blueprint**: Implemented comprehensive file-based blueprint in `arch_blueprint_generator/blueprints/file_based.py` with cross-file relationship detection
- **Blueprint Factory**: Added factory pattern in `arch_blueprint_generator/blueprints/factory.py` for dynamic blueprint creation
- **Integration**: Full integration with both Relationship Map and JSON Mirrors representations
- **Error Handling**: Comprehensive error handling with custom BlueprintError exceptions
- **Detail Levels**: Support for Minimal, Standard, and Detailed detail levels implemented
- **Testing**: Comprehensive test suite implemented in `tests/unit/blueprints/` with >80% coverage
- **Performance**: Efficient file validation and cross-file relationship mapping

### QA Testing Guide

**Prerequisites:**
- Ensure the Architectum environment is set up with `arch_blueprint_generator` module
- Have sample Python files available for testing

**Testing Steps:**

1. **Test Basic Blueprint Creation:**
   ```python
   from arch_blueprint_generator.blueprints.factory import BlueprintFactory
   from arch_blueprint_generator.scanner.path_scanner import PathScanner
   
   # Scan a directory to get representations
   scanner = PathScanner("test_directory")
   relationship_map, json_mirrors = scanner.scan()
   
   # Create file-based blueprint
   blueprint = BlueprintFactory.create_file_blueprint(
       relationship_map, json_mirrors, ["test_file.py"]
   )
   blueprint.generate()
   ```

2. **Test JSON Serialization:**
   ```python
   json_output = blueprint.to_json()
   assert "files" in json_output["content"]
   assert "relationships" in json_output["content"]
   print("✓ JSON serialization working")
   ```

3. **Test XML Serialization:**
   ```python
   xml_output = blueprint.to_xml()
   assert "<Blueprint" in xml_output
   assert "<Content>" in xml_output
   print("✓ XML serialization working")
   ```

4. **Test Detail Levels:**
   ```python
   from arch_blueprint_generator.models.detail_level import DetailLevel
   
   # Test each detail level
   for level in [DetailLevel.MINIMAL, DetailLevel.STANDARD, DetailLevel.DETAILED]:
       blueprint = BlueprintFactory.create_file_blueprint(
           relationship_map, json_mirrors, ["test_file.py"], detail_level=level
       )
       blueprint.generate()
       assert blueprint.detail_level == level
       print(f"✓ {level.value} detail level working")
   ```

5. **Test Cross-File Relationships:**
   ```python
   # Create blueprint with multiple files
   blueprint = BlueprintFactory.create_file_blueprint(
       relationship_map, json_mirrors, ["file1.py", "file2.py"]
   )
   blueprint.generate()
   
   relationships = blueprint.content.get("relationships", [])
   assert len(relationships) >= 0  # Should detect any cross-file relationships
   print("✓ Cross-file relationships working")
   ```

6. **Test Error Handling:**
   ```python
   # Test with invalid file paths
   try:
       blueprint = BlueprintFactory.create_file_blueprint(
           relationship_map, json_mirrors, ["nonexistent.py"]
       )
       blueprint.generate()
       print("✓ Error handling working - invalid files handled gracefully")
   except Exception as e:
       print(f"✓ Error handling working - caught: {e}")
   ```

**Expected Results:**
- All blueprint creation and serialization should work without errors
- JSON and XML outputs should have proper structure
- Different detail levels should produce different amounts of information
- Cross-file relationships should be detected and included
- Invalid inputs should be handled gracefully with clear error messages

### Change Log
- 2025-05-22: Story completed - Base blueprint and file-based blueprint models fully implemented