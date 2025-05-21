# Story 2.1: Implement Base Blueprint and File-Based Blueprint Models

## Status: Draft

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

- [ ] Implement base Blueprint class (AC1, AC2)
  - [ ] Create blueprint module structure with `__init__.py` and `base.py`
  - [ ] Define base `Blueprint` class with integration points for both core representations
  - [ ] Implement serialization methods (`to_json()` and `to_xml()`)
  - [ ] Add validation and error handling for common blueprint operations

- [ ] Implement FileBasedBlueprint class (AC3, AC4)
  - [ ] Create `file_based.py` module for file-based blueprint implementation
  - [ ] Define `FileBasedBlueprint` class extending the base class
  - [ ] Implement file path validation and handling
  - [ ] Implement `generate()` method to create a blueprint from file paths
  - [ ] Handle file-specific detail level controls

- [ ] Implement serialization functionality (AC5)
  - [ ] Create serialization module for format-specific conversions
  - [ ] Implement JSON serialization with appropriate structure
  - [ ] Implement XML serialization with appropriate tags and attributes
  - [ ] Ensure both formats include necessary context for AI consumption

- [ ] Implement blueprint caching (AC6)
  - [ ] Create cache module for blueprint storage
  - [ ] Implement LRU (Least Recently Used) caching strategy
  - [ ] Add cache invalidation based on file changes
  - [ ] Include configuration options for cache size and policy

- [ ] Create unit tests (AC7)
  - [ ] Write tests for base Blueprint class
  - [ ] Write tests for FileBasedBlueprint class
  - [ ] Test serialization for both JSON and XML formats
  - [ ] Verify cache operations and policies
  - [ ] Ensure coverage meets the 80% threshold

- [ ] Update documentation (AC8)
  - [ ] Add docstrings to all new classes and methods
  - [ ] Update README with blueprint model information
  - [ ] Create usage examples for file-based blueprints
  - [ ] Update architecture document to reflect implementation details

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

### Agent Model Used: `None yet`

### Completion Notes List
- Not started

### QA Testing Guide
- Not applicable yet