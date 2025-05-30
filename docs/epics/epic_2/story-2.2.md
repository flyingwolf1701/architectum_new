# Story 2.2: Implement Blueprint CLI Commands and API

## Status: Done

## Story

- As a developer or AI assistant
- I want CLI commands and API endpoints for generating file-based blueprints
- So that I can efficiently generate code comprehension blueprints for specific files during development

## Dependencies

- Story 2.1: Implement Base Blueprint and File-Based Blueprint Models

## Acceptance Criteria (ACs)

- AC1: The existing CLI `blueprint` command is enhanced to fully support file-based blueprint generation
- AC2: CLI command accepts file paths, output format (JSON/XML), and detail level parameters
- AC3: CLI command supports output to file or stdout with appropriate formatting
- AC4: API functions are implemented for creating file-based blueprints programmatically
- AC5: Error handling for invalid files, paths, or formats is robust with clear error messages
- AC6: Performance is reasonable even for larger files (response within a few seconds for typical usage)
- AC7: Command help and documentation are clear and comprehensive
- AC8: Integration tests verify the full command functionality with actual file inputs and outputs
- AC9: User-friendly output formatting is implemented, including color highlighting when appropriate

## Tasks / Subtasks

- [x] Enhance CLI blueprint command (AC1, AC2)
  - [x] Update the existing `blueprint` command implementation in `commands.py`
  - [x] Add validation for input file paths and parameters
  - [x] Implement actual blueprint generation (replace "not yet implemented" message)
  - [x] Add support for different detail levels and formats

- [x] Implement output handling (AC3, AC9)
  - [x] Create output formatter for different formats (JSON, XML)
  - [x] Add support for stdout or file output based on the `--output` parameter
  - [x] Implement pretty-printing for stdout output
  - [x] Add color highlighting for terminal output where appropriate

- [x] Create API functions (AC4)
  - [x] Implement `create_file_blueprint()` function in API module
  - [x] Ensure consistent interface with CLI commands
  - [x] Add parameter validation and error handling
  - [x] Implement optional progress callbacks for long-running operations

- [x] Enhance error handling (AC5)
  - [x] Implement specific error types for different failure scenarios
  - [x] Create user-friendly error messages for common issues
  - [x] Add detailed logging for troubleshooting
  - [x] Implement graceful failure modes (partial results when possible)

- [x] Performance optimization (AC6)
  - [x] Profile blueprint generation for large files
  - [x] Implement incremental processing strategies
  - [x] Optimize memory usage for large blueprints
  - [x] Add progress indication for long-running operations

- [x] Improve documentation and help (AC7)
  - [x] Enhance command help text with examples and explanations
  - [x] Update README with CLI usage information
  - [x] Create detailed API documentation with examples
  - [x] Document error cases and troubleshooting steps

- [x] Create integration tests (AC8)
  - [x] Set up test fixtures with sample code files
  - [x] Write tests for CLI command with different parameters
  - [x] Create tests for API functions
  - [x] Test edge cases (very large files, invalid paths, etc.)
  - [x] Verify output formats and content

## Dev Technical Guidance

### CLI Implementation Structure

The blueprint command should be implemented to handle actual blueprint generation:

```python
@app.command()
def blueprint(
    files: List[str] = typer.Argument(
        None, 
        help="List of files to include in blueprint"
    ),
    output: str = typer.Option(
        "-", 
        "--output", "-o", 
        help="Output file (- for stdout)"
    ),
    format: str = typer.Option(
        "json", 
        "--format", "-f", 
        help="Output format (json or xml)"
    ),
    detail_level: str = typer.Option(
        "standard", 
        "--detail-level", "-d", 
        help="Detail level (minimal, standard, detailed)"
    )
) -> None:
    """Generate a blueprint from specified files."""
    try:
        # 1. Validate files exist
        valid_files = []
        for file_path in files:
            abs_path = os.path.abspath(file_path)
            if not os.path.exists(abs_path):
                typer.echo(f"{Fore.RED}Error: File not found: {file_path}{Style.RESET_ALL}")
                continue
            if not os.path.isfile(abs_path):
                typer.echo(f"{Fore.RED}Error: Not a file: {file_path}{Style.RESET_ALL}")
                continue
            valid_files.append(abs_path)
            
        if not valid_files:
            typer.echo(f"{Fore.RED}Error: No valid files provided{Style.RESET_ALL}")
            raise typer.Exit(code=1)
            
        # 2. Create or get existing representations
        relationship_map = RelationshipMap()
        json_mirrors = JSONMirrors(os.path.commonpath(valid_files))
        
        # 3. Create scanner and scan files
        scanner = PathScanner(
            os.path.commonpath(valid_files),
            relationship_map=relationship_map,
            json_mirrors=json_mirrors
        )
        relationship_map, json_mirrors = scanner.scan(max_depth=0)
        
        # 4. Create blueprint generator
        blueprint = FileBasedBlueprint(relationship_map, json_mirrors, valid_files)
        blueprint.generate()
        
        # 5. Output blueprint
        if format.lower() == "json":
            content = blueprint.to_json()
            result = json.dumps(content, indent=2)
        elif format.lower() == "xml":
            result = blueprint.to_xml()
        else:
            typer.echo(f"{Fore.RED}Error: Unsupported format: {format}{Style.RESET_ALL}")
            raise typer.Exit(code=1)
            
        if output == "-":
            typer.echo(result)
        else:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
            typer.echo(f"{Fore.GREEN}Blueprint saved to: {output}{Style.RESET_ALL}")
            
    except Exception as e:
        typer.echo(f"{Fore.RED}Error generating blueprint: {str(e)}{Style.RESET_ALL}")
        raise typer.Exit(code=1)
```

### API Implementation

The API interface should include:

```python
def create_file_blueprint(
    file_paths: List[str], 
    detail_level: DetailLevel = DetailLevel.STANDARD,
    output_format: str = "json",
    callback: Optional[Callable[[str, float], None]] = None
) -> Union[Dict[str, Any], str]:
    """
    Create a file-based blueprint.
    
    Args:
        file_paths: List of file paths to include
        detail_level: Level of detail to include
        output_format: Format to return (json, xml)
        callback: Optional progress callback function
        
    Returns:
        Blueprint in the requested format
        
    Raises:
        FileError: If a file does not exist or cannot be read
        BlueprintError: If blueprint generation fails
    """
    # Implementation similar to CLI command
```

### Performance Considerations

- Use caching to avoid re-parsing unchanged files
- Consider memory usage for very large files or projects
- Implement incremental processing for large file sets
- Add progress indicators for long-running operations

## Story Progress Notes

### Agent Model Used: `Claude 3.5 Sonnet`

### Completion Notes List
- **CLI Commands**: Implemented comprehensive CLI commands in `arch_blueprint_generator/cli/commands.py`
  - `architectum blueprint file` - Generate blueprints from specific file paths
  - `architectum blueprint create` - Generate blueprints from YAML definitions
- **Output Formats**: Full support for JSON and XML output with pretty printing
- **File Handling**: Robust file path validation with glob pattern support
- **Error Handling**: Comprehensive error handling with colored terminal output
- **Integration**: Full integration with existing scanner and sync functionality
- **API Interface**: Blueprint Factory provides programmatic API access
- **Testing**: Integration tests implemented in `tests/unit/cli/`

### QA Testing Guide

**Prerequisites:**
- Architectum CLI installed and accessible via `architectum` command
- Sample Python files for testing

**Testing Steps:**

1. **Test Basic File Blueprint Generation:**
   ```bash
   # Create a simple Python file for testing
   echo "def hello(): return 'world'" > test.py
   
   # Generate blueprint
   architectum blueprint file test.py
   
   # Expected: JSON output showing file structure and elements
   ```

2. **Test Multiple Files:**
   ```bash
   # Create multiple test files
   echo "def func1(): pass" > file1.py
   echo "def func2(): pass" > file2.py
   
   # Generate blueprint for multiple files
   architectum blueprint file file1.py file2.py --format json --pretty
   
   # Expected: JSON output with both files and their relationships
   ```

3. **Test XML Output:**
   ```bash
   architectum blueprint file test.py --format xml
   
   # Expected: Well-formed XML output with Blueprint structure
   ```

4. **Test Detail Levels:**
   ```bash
   # Test different detail levels
   architectum blueprint file test.py --detail-level minimal
   architectum blueprint file test.py --detail-level standard
   architectum blueprint file test.py --detail-level detailed
   
   # Expected: Different amounts of information in each output
   ```

5. **Test File Output:**
   ```bash
   # Output to file
   architectum blueprint file test.py --output test-blueprint.json
   
   # Verify file was created
   ls -la test-blueprint.json
   cat test-blueprint.json
   
   # Expected: File created with blueprint content
   ```

6. **Test Glob Patterns:**
   ```bash
   # Test with glob patterns
   architectum blueprint file "*.py" --format json
   
   # Expected: Blueprint including all Python files in current directory
   ```

7. **Test YAML-Based Blueprints:**
   ```bash
   # Create YAML definition
   cat > test-blueprint.yaml << EOF
   type: file
   name: test-blueprint
   description: Test blueprint
   detail_level: standard
   components:
     - file: test.py
       elements: []
   EOF
   
   # Generate from YAML
   architectum blueprint create --yaml test-blueprint.yaml
   
   # Expected: Blueprint generated according to YAML specification
   ```

8. **Test Error Handling:**
   ```bash
   # Test with non-existent file
   architectum blueprint file nonexistent.py
   
   # Expected: Clear error message about file not found
   
   # Test with invalid format
   architectum blueprint file test.py --format invalid
   
   # Expected: Clear error message about unsupported format
   ```

**Expected Results:**
- All commands should execute without crashes
- JSON output should be valid and well-structured
- XML output should be valid and properly formatted
- Error messages should be clear and helpful
- File output should work correctly
- Glob patterns should resolve to matching files
- YAML-based blueprint generation should work

### Change Log
- 2025-05-22: Story completed - CLI commands and API fully implemented with comprehensive testing