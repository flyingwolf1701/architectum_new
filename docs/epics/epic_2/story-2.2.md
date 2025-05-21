# Story 2.2: Implement Blueprint CLI Commands and API

## Status: Draft

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

- [ ] Enhance CLI blueprint command (AC1, AC2)
  - [ ] Update the existing `blueprint` command implementation in `commands.py`
  - [ ] Add validation for input file paths and parameters
  - [ ] Implement actual blueprint generation (replace "not yet implemented" message)
  - [ ] Add support for different detail levels and formats

- [ ] Implement output handling (AC3, AC9)
  - [ ] Create output formatter for different formats (JSON, XML)
  - [ ] Add support for stdout or file output based on the `--output` parameter
  - [ ] Implement pretty-printing for stdout output
  - [ ] Add color highlighting for terminal output where appropriate

- [ ] Create API functions (AC4)
  - [ ] Implement `create_file_blueprint()` function in API module
  - [ ] Ensure consistent interface with CLI commands
  - [ ] Add parameter validation and error handling
  - [ ] Implement optional progress callbacks for long-running operations

- [ ] Enhance error handling (AC5)
  - [ ] Implement specific error types for different failure scenarios
  - [ ] Create user-friendly error messages for common issues
  - [ ] Add detailed logging for troubleshooting
  - [ ] Implement graceful failure modes (partial results when possible)

- [ ] Performance optimization (AC6)
  - [ ] Profile blueprint generation for large files
  - [ ] Implement incremental processing strategies
  - [ ] Optimize memory usage for large blueprints
  - [ ] Add progress indication for long-running operations

- [ ] Improve documentation and help (AC7)
  - [ ] Enhance command help text with examples and explanations
  - [ ] Update README with CLI usage information
  - [ ] Create detailed API documentation with examples
  - [ ] Document error cases and troubleshooting steps

- [ ] Create integration tests (AC8)
  - [ ] Set up test fixtures with sample code files
  - [ ] Write tests for CLI command with different parameters
  - [ ] Create tests for API functions
  - [ ] Test edge cases (very large files, invalid paths, etc.)
  - [ ] Verify output formats and content

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

### Agent Model Used: `None yet`

### Completion Notes List
- Not started

### QA Testing Guide
- Not applicable yet