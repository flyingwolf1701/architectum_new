# Story 2.3: Implement Blueprint Serialization and Output Formats

## Status: Done

## Story

- As a developer or AI assistant
- I want blueprint serialization with multiple output formats (JSON, XML) with consistent structure
- So that generated blueprints can be consumed by various tools and systems for code comprehension

## Dependencies

- Story 2.1: Implement Base Blueprint and File-Based Blueprint Models
- Story 2.2: Implement Blueprint CLI Commands and API

## Acceptance Criteria (ACs)

- AC1: A dedicated serialization layer is implemented for converting blueprints to different formats
- AC2: JSON serialization supports comprehensive representation of all blueprint data
- AC3: XML serialization provides a rich, hierarchical representation suitable for AI consumption
- AC4: HTML visualization output is supported for human-friendly blueprint viewing (optional, if time permits)
- AC5: Serialized outputs maintain consistent structure and naming across formats
- AC6: Large blueprints are handled efficiently without excessive memory usage
- AC7: Special characters and encoding issues are properly handled in all formats
- AC8: Unit tests verify serialization functionality and output structure
- AC9: Documentation includes format specifications and schema information

## Tasks / Subtasks

- [x] Create serialization framework (AC1)
  - [x] Implement formatter base class with common functionality
  - [x] Design consistent output structure for all formats
  - [x] Create format registry for extensibility
  - [x] Add configuration options for controlling output details

- [x] Implement JSON formatter (AC2, AC5)
  - [x] Create JSON-specific formatter class
  - [x] Define blueprint JSON schema structure
  - [x] Implement transformation logic from internal model to JSON
  - [x] Add indentation and pretty-printing options
  - [x] Handle special cases (circular references, etc.)

- [x] Implement XML formatter (AC3, AC5)
  - [x] Create XML-specific formatter class
  - [x] Define XML schema for blueprints
  - [x] Implement transformation logic from internal model to XML
  - [x] Add namespace and validation options
  - [x] Ensure proper escaping of special characters

- [x] Implement HTML visualization (AC4, optional)
  - [x] Create HTML formatter for visual blueprint representation
  - [x] Implement basic CSS styling for readability
  - [x] Add interactive navigation elements (optional)
  - [x] Support syntax highlighting for code snippets

- [x] Optimize for large blueprints (AC6)
  - [x] Implement streaming output for large blueprints
  - [x] Add memory-efficient transformation algorithms
  - [x] Optimize serialization performance for large datasets
  - [x] Add progress reporting for long-running serializations

- [x] Handle encoding and special characters (AC7)
  - [x] Implement proper character escaping for all formats
  - [x] Add UTF-8 encoding support
  - [x] Test with special characters in code and comments
  - [x] Handle multi-line strings and comments correctly

- [x] Create tests for serialization (AC8)
  - [x] Write unit tests for all formatters
  - [x] Test with various blueprint sizes and structures
  - [x] Verify output against schema definitions
  - [x] Test edge cases like empty blueprints, special characters

- [x] Create documentation (AC9)
  - [x] Document JSON schema structure
  - [x] Document XML schema structure
  - [x] Create format examples and usage guide
  - [x] Add schema files for validation (optional)

## Dev Technical Guidance

### Serialization Framework

Implement a flexible serialization framework that can be extended with new formats:

```python
class OutputFormatter:
    """Base class for blueprint output formatters."""
    
    def format(self, blueprint: Blueprint) -> str:
        """
        Format a blueprint into a specific output format.
        
        Args:
            blueprint: The blueprint to format
            
        Returns:
            Formatted output as a string
        """
        raise NotImplementedError
        
class JSONFormatter(OutputFormatter):
    """Format blueprints as JSON."""
    
    def format(self, blueprint: Blueprint) -> str:
        """Format blueprint as JSON string."""
        data = self._convert_blueprint(blueprint)
        return json.dumps(data, indent=2)
        
    def _convert_blueprint(self, blueprint: Blueprint) -> Dict[str, Any]:
        """Convert blueprint to dictionary structure for JSON."""
        # Implementation...
        
class XMLFormatter(OutputFormatter):
    """Format blueprints as XML."""
    
    def format(self, blueprint: Blueprint) -> str:
        """Format blueprint as XML string."""
        root = self._create_xml_root(blueprint)
        # Build XML structure
        return self._serialize_xml(root)
        
    def _create_xml_root(self, blueprint: Blueprint) -> Element:
        """Create XML root element for blueprint."""
        # Implementation using xml.etree.ElementTree or similar
```

### JSON Schema Structure

The JSON output should follow a consistent structure:

```json
{
  "blueprint_type": "file",
  "generation_time": "2023-05-20T15:30:00Z",
  "files": [
    {
      "path": "src/main.py",
      "content_hash": "abc123...",
      "elements": [
        {
          "name": "main_function",
          "type": "function",
          "line_start": 10,
          "line_end": 20,
          "source": "def main_function():\n    ..."
        }
      ]
    }
  ],
  "relationships": [
    {
      "source": "file:src/main.py",
      "target": "function:main_function",
      "type": "contains"
    }
  ]
}
```

### XML Schema Structure

The XML output should use a hierarchical structure:

```xml
<blueprint type="file" timestamp="2023-05-20T15:30:00Z">
  <files>
    <file path="src/main.py" hash="abc123...">
      <element name="main_function" type="function" line-start="10" line-end="20">
        <source><![CDATA[def main_function():
    ...]]></source>
      </element>
    </file>
  </files>
  <relationships>
    <relationship type="contains">
      <source>file:src/main.py</source>
      <target>function:main_function</target>
    </relationship>
  </relationships>
</blueprint>
```

### Memory Efficiency

For large blueprints, implement streaming approaches:

- Use iterative processing instead of building the entire structure in memory
- Consider generator functions for large collections
- Use chunked output writing for very large blueprints
- Implement lazy loading of file content when possible

## Story Progress Notes

### Agent Model Used: `Claude 3.5 Sonnet`

### Completion Notes List
- **Serialization Framework**: Implemented in `blueprints/base.py` with consistent structure across formats
- **JSON Serialization**: Complete implementation with pretty printing and compact options
- **XML Serialization**: Full hierarchical XML output with proper escaping and formatting
- **Character Handling**: UTF-8 encoding and special character escaping implemented
- **Performance**: Memory-efficient serialization for large blueprints
- **Testing**: Comprehensive test coverage in `tests/unit/blueprints/`
- **Integration**: Seamless integration with CLI and API interfaces

### QA Testing Guide

**Testing Steps:**

1. **Test JSON Serialization:**
   ```python
   # Generate a blueprint and test JSON output
   blueprint.generate()
   json_output = blueprint.to_json()
   
   # Verify structure
   assert "name" in json_output
   assert "type" in json_output
   assert "content" in json_output
   assert "files" in json_output["content"]
   assert "relationships" in json_output["content"]
   ```

2. **Test XML Serialization:**
   ```python
   # Test XML output
   xml_output = blueprint.to_xml()
   
   # Verify XML structure
   assert xml_output.startswith('<?xml')
   assert '<Blueprint' in xml_output
   assert '</Blueprint>' in xml_output
   ```

3. **Test Pretty vs Compact JSON:**
   ```bash
   # Pretty format (default)
   architectum blueprint file test.py --pretty
   
   # Compact format
   architectum blueprint file test.py --compact
   ```

**Expected Results:**
- JSON output should be valid and well-structured
- XML output should be valid XML with proper hierarchy
- Pretty printing should include proper indentation
- Special characters should be properly escaped

### Change Log
- 2025-05-22: Story completed - Serialization and output formats fully implemented