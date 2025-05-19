# Story 1.6: Expose Blueprint Generation via Initial API/CLI

## Status: Draft

## Story

- As a developer or another service
- I want to trigger blueprint generation via a defined API endpoint or CLI command within Architectum
- So that I can integrate this capability into other tools or workflows

## Acceptance Criteria (ACs)

- AC1: The CLI command successfully triggers blueprint generation.
- AC2: All required parameters can be passed and are correctly used.
- AC3: Generated blueprints are correctly output in the specified format.
- AC4: Output format and destination options are functional.
- AC5: Proper error handling is implemented for invalid inputs or generation failures.
- AC6: Help documentation is clear and comprehensive.
- AC7: Testing Requirements:
  - Coverage: At least 80% code coverage for the CLI implementation and output handling
  - Framework: Implementation using pytest with CLI invocation testing
  - Integration Testing: End-to-end tests calling the CLI with various parameters
  - Contract Testing: Verify the output format options produce valid outputs
  - Parameter Testing: Test all parameter combinations and error handling
  - Output Format Testing: Test different output formats if implemented
## Tasks / Subtasks

- [ ] Define and implement CLI structure using Typer (AC: 1, 2, 6)
  - [ ] Create main CLI structure with command groups
  - [ ] Implement `blueprint` command group
  - [ ] Implement `blueprint file` subcommand for File-Based Blueprints
  - [ ] Add parameters for file paths, output destination, and format options
  - [ ] Create comprehensive help documentation
  - [ ] Implement command discovery and plugin architecture for future extensions

- [ ] Implement blueprint command execution logic (AC: 1, 3)
  - [ ] Create command handler for File-Based Blueprint generation
  - [ ] Implement parameter validation and preprocessing
  - [ ] Add integration with the Blueprint Factory
  - [ ] Create wrapper for connecting CLI commands to blueprint generation logic
  - [ ] Add support for glob patterns in file paths

- [ ] Implement output formatting and handling (AC: 3, 4)
  - [ ] Implement JSON output formatting
  - [ ] Add optional support for other output formats
  - [ ] Create output destination handling (stdout, file)
  - [ ] Implement pretty-printing options for human readability
  - [ ] Add colorized output for terminal display

- [ ] Implement error handling and reporting (AC: 5)
  - [ ] Create robust error handling for CLI commands
  - [ ] Implement user-friendly error messages
  - [ ] Add debug output options for troubleshooting
  - [ ] Create graceful failure modes for common error scenarios
  - [ ] Implement exception handling with appropriate exit codes

- [ ] Integrate with existing synchronization command (AC: 1)
  - [ ] Add option to synchronize before blueprint generation
  - [ ] Ensure blueprint generation uses up-to-date representations
  - [ ] Handle cases where synchronization fails but blueprint generation can proceed

- [ ] Create comprehensive testing suite (AC: 7)
  - [ ] Implement unit tests for CLI command structure and parameters
  - [ ] Create integration tests for end-to-end functionality
  - [ ] Add contract tests for output format validation
  - [ ] Implement tests for all parameter combinations
  - [ ] Create tests for error handling and reporting
  - [ ] Test output formatting options
  - [ ] Generate test coverage report to ensure 80% minimum coverage
## Dev Technical Guidance

### CLI Structure with Typer

Implement the CLI structure using Typer, which provides a clean interface with type hints:

```python
import typer
from typing import List, Optional
from pathlib import Path
from enum import Enum
import sys

# Import core components
from arch_blueprint_generator.models import DetailLevel, DetailLevelConfig
from arch_blueprint_generator.blueprints import BlueprintFactory

# Create app instance
app = typer.Typer(help="Architectum CLI for code comprehension and AI assistance.")

# Create blueprint subcommand group
blueprint_app = typer.Typer(help="Generate blueprints from code.")
app.add_typer(blueprint_app, name="blueprint")

# Output format enum
class OutputFormat(str, Enum):
    JSON = "json"
    XML = "xml"

@blueprint_app.command("file")
def file_blueprint(
    files: List[str] = typer.Argument(
        ..., 
        help="File paths to include in the blueprint"
    ),
    output: str = typer.Option(
        "-", 
        "--output", 
        "-o", 
        help="Output file (- for stdout)"
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.JSON, 
        "--format", 
        "-f", 
        help="Output format"
    ),
    detail_level: str = typer.Option(
        "standard", 
        "--detail-level", 
        "-d", 
        help="Detail level (minimal, standard, detailed)"
    ),
    pretty: bool = typer.Option(
        True, 
        "--pretty/--compact", 
        help="Pretty print output"
    ),
    sync: bool = typer.Option(
        False, 
        "--sync", 
        help="Synchronize files before generating blueprint"
    )
) -> None:
```    """
    Generate a File-Based Blueprint for specified files.
    
    This command creates a blueprint that combines data from both the Relationship Map
    and JSON Mirrors for the specified files, providing a comprehensive view for
    AI assistants or visualization tools.
    
    Examples:
    
        arch blueprint file src/main.py src/utils.py
        
        arch blueprint file src/auth/*.js --output auth-blueprint.json --detail-level detailed
    """
    try:
        # Validate and expand file paths
        resolved_files = []
        for file_pattern in files:
            # Handle glob patterns
            import glob
            matches = glob.glob(file_pattern, recursive=True)
            if not matches:
                typer.echo(f"Warning: No files match pattern '{file_pattern}'", err=True)
            resolved_files.extend(matches)
        
        if not resolved_files:
            typer.echo("Error: No valid files specified", err=True)
            raise typer.Exit(code=1)
        
        # Parse detail level
        try:
            dl = DetailLevel.from_string(detail_level)
            detail_config = DetailLevelConfig(
                relationship_map=dl,
                json_mirrors=dl
            )
        except ValueError as e:
            typer.echo(f"Error: {str(e)}", err=True)
            raise typer.Exit(code=1)
        
        # Synchronize if requested
        if sync:
            from arch_blueprint_generator.sync import synchronize_files
            typer.echo("Synchronizing files...")
            synchronize_files(resolved_files)
        
        # Initialize components
        from arch_blueprint_generator.models import RelationshipMap, JSONMirrors
        relationship_map = RelationshipMap()
        json_mirrors = JSONMirrors()
        
        # Generate blueprint
        factory = BlueprintFactory(relationship_map, json_mirrors)
        blueprint = factory.create_file_blueprint(
            file_paths=resolved_files,
            detail_level_config=detail_config
        )
```        
        # Format output
        if format == OutputFormat.JSON:
            output_content = blueprint.to_string(indent=2 if pretty else None)
        elif format == OutputFormat.XML:
            # XML format implementation to be added in the future
            typer.echo("XML format not yet implemented, falling back to JSON", err=True)
            output_content = blueprint.to_string(indent=2 if pretty else None)
        
        # Write output
        if output == "-":
            typer.echo(output_content)
        else:
            with open(output, "w") as f:
                f.write(output_content)
            typer.echo(f"Blueprint written to {output}")
            
    except Exception as e:
        typer.echo(f"Error generating blueprint: {str(e)}", err=True)
        if "--debug" in sys.argv:
            import traceback
            typer.echo(traceback.format_exc(), err=True)
        raise typer.Exit(code=1)
```

### Entry Point Setup

Create a clear entry point for the CLI application:

```python
# In main.py or __main__.py

def main():
    """Entry point for the Architectum CLI."""
    from arch_blueprint_generator.cli.commands import app
    app()

if __name__ == "__main__":
    main()
```

### Package Configuration

Configure the package to expose the CLI command:

```
# In pyproject.toml
[project.scripts]
arch = "arch_blueprint_generator.cli.commands:app"
```
### Error Handling Strategy

Implement robust error handling in the CLI:

1. Use specific error messages for different failure scenarios
2. Add color coding for errors and warnings using colorama
3. Implement a debug mode for detailed error information
4. Use appropriate exit codes for different error types
5. Add logging for diagnostic information

Example error handling improvements:

```python
import typer
from typing import Optional
import sys
from colorama import Fore, Style, init

# Initialize colorama
init()

def error(message: str, exit_code: Optional[int] = None) -> None:
    """Display an error message and optionally exit."""
    typer.echo(f"{Fore.RED}Error: {message}{Style.RESET_ALL}", err=True)
    if exit_code is not None:
        raise typer.Exit(code=exit_code)

def warning(message: str) -> None:
    """Display a warning message."""
    typer.echo(f"{Fore.YELLOW}Warning: {message}{Style.RESET_ALL}", err=True)

def success(message: str) -> None:
    """Display a success message."""
    typer.echo(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

def debug(message: str) -> None:
    """Display a debug message if debug mode is enabled."""
    if "--debug" in sys.argv:
        typer.echo(f"{Fore.BLUE}Debug: {message}{Style.RESET_ALL}", err=True)
```

### Testing Strategy

Focus on comprehensive testing of the CLI:

1. Test CLI command structure and parameter parsing
2. Create integration tests that invoke CLI commands and verify outputs
3. Test error handling with invalid inputs
4. Verify output formats and destinations work correctly
5. Test with various parameter combinations
6. Use mock components to isolate CLI testing from other components

Example CLI test:

```python
from typer.testing import CliRunner
from arch_blueprint_generator.cli.commands import app
import os
import json
import pytest

@pytest.fixture
def runner():
    return CliRunner()

def test_file_blueprint_command(runner, tmp_path):
    # Create test files
    test_file1 = tmp_path / "test1.py"
    test_file2 = tmp_path / "test2.py"
    
    test_file1.write_text("def test_function():\n    return 'test'")
    test_file2.write_text("def another_function():\n    return 'another'")
    
    # Run command
    output_file = tmp_path / "blueprint.json"
    result = runner.invoke(app, [
        "blueprint", 
        "file", 
        str(test_file1), 
        str(test_file2), 
        "--output", 
        str(output_file)
    ])
    
    # Check command succeeded
    assert result.exit_code == 0
    
    # Check output file exists and contains valid JSON
    assert output_file.exists()
    with open(output_file) as f:
        blueprint = json.load(f)
    
    # Check blueprint structure
    assert "name" in blueprint
    assert "content" in blueprint
    assert "files" in blueprint["content"]
    
    # Check files are included
    file_paths = list(blueprint["content"]["files"].keys())
    assert str(test_file1) in file_paths
    assert str(test_file2) in file_paths
```

## Story Progress Notes

### Agent Model Used: `<Agent Model Name/Version>`

### Completion Notes List
{Not started yet}

### Change Log
- Initial story draft created by POSM

## QA Testing Guide

{This section should be completed when the story implementation is done and tests are passing. Include step-by-step instructions for how a human tester can verify the functionality works as expected. Include example inputs, expected outputs, and any edge cases that should be tested.}