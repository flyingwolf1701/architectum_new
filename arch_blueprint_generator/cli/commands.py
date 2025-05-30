"""
Command-line interface for Architectum Blueprint Generator.
"""

import json
import os
import glob
import sys
from enum import Enum
from typing import List, Optional

import typer
from colorama import Fore, Style

from arch_blueprint_generator.utils.logging import configure_logging, get_logger
from arch_blueprint_generator.scanner.enhanced_path_scanner import EnhancedPathScanner
from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.errors.exceptions import BlueprintError
from arch_blueprint_generator.yaml import load_blueprint_config, YAMLValidationError

app = typer.Typer(help="Architectum Blueprint Generator")
blueprint_app = typer.Typer(help="Generate blueprints from code.")
app.add_typer(blueprint_app, name="blueprint")
logger = get_logger(__name__)


class OutputFormat(str, Enum):
    """Supported output formats."""

    JSON = "json"
    XML = "xml"


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


def version_callback(value: bool):
    """
    Display version information.

    Args:
        value: Whether to display version information
    """
    if value:
        from arch_blueprint_generator import __version__

        typer.echo(f"Architectum Blueprint Generator v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version information and exit.",
    ),
    verbose: bool = typer.Option(False, "--verbose", help="Enable verbose output."),
):
    """
    Architectum Blueprint Generator - A tool for code comprehension.
    """
    import logging

    log_level = logging.DEBUG if verbose else logging.INFO
    configure_logging(log_level)


@blueprint_app.command("file")
def blueprint_file(
    files: List[str] = typer.Argument(
        ...,
        help="File paths to include in the blueprint",
    ),
    output: str = typer.Option(
        "-",
        "--output",
        "-o",
        help="Output file (- for stdout)",
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.JSON,
        "--format",
        "-f",
        help="Output format",
    ),
    detail_level: str = typer.Option(
        "standard",
        "--detail-level",
        "-d",
        help="Detail level (minimal, standard, detailed)",
    ),
    pretty: bool = typer.Option(
        True,
        "--pretty/--compact",
        help="Pretty print output",
    ),
    sync: bool = typer.Option(
        False,
        "--sync",
        help="Synchronize files before generating blueprint",
    ),
) -> None:
    """Generate a File-Based Blueprint for specified files."""
    try:
        resolved_files: List[str] = []
        for pattern in files:
            matches = glob.glob(pattern, recursive=True)
            if not matches:
                warning(f"No files match pattern '{pattern}'")
            resolved_files.extend(matches)

        if not resolved_files:
            error("No valid files specified", exit_code=1)

        try:
            dl = DetailLevel.from_string(detail_level)
        except ValueError as e:
            error(str(e), exit_code=1)

        if sync:
            from arch_blueprint_generator.sync.arch_sync import ArchSync

            debug("Synchronizing files before blueprint generation")
            sync_instance = ArchSync()
            try:
                sync_instance.sync(resolved_files, recursive=False, force=False)
            except Exception as e:
                warning(f"Synchronization failed: {str(e)}")

        root_dir = os.path.commonpath(resolved_files)
        scanner = EnhancedPathScanner(root_dir)
        relationship_map, json_mirrors = scanner.scan()

        from arch_blueprint_generator.blueprints.factory import BlueprintFactory

        blueprint = BlueprintFactory.create_file_blueprint(
            relationship_map,
            json_mirrors,
            resolved_files,
            detail_level=dl,
        )

        blueprint.generate()

        if format == OutputFormat.JSON:
            output_content = json.dumps(
                blueprint.to_json(), indent=2 if pretty else None
            )
        else:
            output_content = blueprint.to_xml()

        if output == "-":
            typer.echo(output_content)
        else:
            with open(output, "w", encoding="utf-8") as f:
                f.write(output_content)
            success(f"Blueprint written to {output}")

    except Exception as e:
        error(f"Error generating blueprint: {str(e)}", exit_code=1)


@blueprint_app.command("create")
def blueprint_create(
    yaml: str = typer.Option(
        ..., "--yaml", "-f", help="YAML blueprint definition file"
    ),
    output: str = typer.Option(
        "-", "--output", "-o", help="Output file (- for stdout)"
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.JSON, "--format", "-m", help="Output format"
    ),
    pretty: bool = typer.Option(True, "--pretty/--compact", help="Pretty print output"),
) -> None:
    """Create a blueprint from a YAML definition."""
    try:
        try:
            config = load_blueprint_config(yaml)
        except (FileNotFoundError, YAMLValidationError) as e:
            error(str(e), exit_code=1)

        files = []
        yaml_dir = os.path.dirname(os.path.abspath(yaml))
        for comp in config.components:
            file_path = comp.file
            if not os.path.isabs(file_path):
                file_path = os.path.join(yaml_dir, file_path)
            files.append(os.path.abspath(file_path))
        if not files:
            error("No files specified in YAML", exit_code=1)

        root_dir = os.path.commonpath(files)
        scanner = EnhancedPathScanner(root_dir)
        relationship_map, json_mirrors = scanner.scan()

        from arch_blueprint_generator.blueprints.factory import BlueprintFactory

        dl = DetailLevel.from_string(config.detail_level)
        blueprint = BlueprintFactory.create_file_blueprint(
            relationship_map,
            json_mirrors,
            files,
            name=config.name,
            detail_level=dl,
        )
        blueprint.generate()

        if format == OutputFormat.JSON:
            content = json.dumps(blueprint.to_json(), indent=2 if pretty else None)
        else:
            content = blueprint.to_xml()

        if output == "-":
            typer.echo(content)
        else:
            with open(output, "w", encoding="utf-8") as f:
                f.write(content)
            success(f"Blueprint written to {output}")

    except Exception as e:
        error(f"Error creating blueprint: {str(e)}", exit_code=1)


@app.command()
def scan(
    path: str = typer.Argument(".", help="Path to scan"),
    depth: int = typer.Option(
        0, "--depth", "-d", help="Maximum depth to scan (0 for no limit)"
    ),
    output: str = typer.Option(
        None, "--output", "-o", help="Output directory for saving representations"
    ),
    exclude: List[str] = typer.Option(
        [],
        "--exclude",
        "-e",
        help="Patterns to exclude from scanning (legacy compatibility)",
    ),
    detail_level: str = typer.Option(
        "standard",
        "--detail-level",
        "-l",
        help="Detail level (minimal, standard, detailed)",
    ),
    gitignore: bool = typer.Option(
        True,
        "--gitignore/--no-gitignore",
        help="Respect .gitignore files when scanning (default: True)",
    ),
    ignore: List[str] = typer.Option(
        [],
        "--ignore",
        "-i",
        help="Additional patterns to ignore beyond .gitignore",
    ),
) -> None:
    """
    Scan a directory path and generate both representations.

    Creates both Relationship Map and JSON Mirrors representations
    for the specified path. The detail level controls how much
    information is included:

    - minimal: Basic structure information only
    - standard: Essential information including types and basic attributes
    - detailed: Comprehensive information including documentation

    GitIgnore Support:
    - Automatically respects .gitignore files when found
    - Use --no-gitignore to disable git ignore patterns
    - Use --ignore to add additional patterns beyond .gitignore
    - Legacy --exclude patterns are also supported

    Examples:
    
        # Basic scan with gitignore support
        arch scan .
        
        # Scan without respecting gitignore
        arch scan . --no-gitignore
        
        # Add additional ignore patterns
        arch scan . --ignore "*.log" --ignore "temp/"
        
        # Use legacy exclude patterns
        arch scan . --exclude "__pycache__" --exclude ".pytest_cache"
    """
    try:
        # Convert string detail level to enum
        try:
            detail = DetailLevel.from_string(detail_level)
        except ValueError as e:
            typer.echo(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
            raise typer.Exit(code=1)

        # Handle default exclude patterns
        if not exclude:
            exclude = [".git", ".venv", "__pycache__"]
        
        # Create and run the enhanced path scanner
        scanner = EnhancedPathScanner(
            path, 
            exclude_patterns=exclude,
            respect_gitignore=gitignore,
            additional_ignores=ignore
        )
        relationship_map, json_mirrors = scanner.scan(
            max_depth=depth, detail_level=detail
        )

        node_count = relationship_map.node_count()
        relationship_count = relationship_map.relationship_count()

        typer.echo(f"{Fore.GREEN}Scan completed successfully:{Style.RESET_ALL}")
        typer.echo(f"Path: {os.path.abspath(path)}")
        typer.echo(f"Depth: {depth if depth > 0 else 'unlimited'}")
        typer.echo(f"Detail Level: {detail.value}")
        typer.echo(f"GitIgnore: {'enabled' if gitignore else 'disabled'}")
        typer.echo(f"Nodes: {node_count}")
        typer.echo(f"Relationships: {relationship_count}")
        
        # Show exclusion information
        if gitignore and scanner.gitignore_parser:
            gitignore_count = len(scanner.gitignore_parser.patterns)
            typer.echo(f"GitIgnore patterns: {gitignore_count} loaded from .gitignore")
        
        if ignore:
            typer.echo(f"Additional ignore patterns: {len(ignore)}")
        
        if exclude and exclude != [".git", ".venv", "__pycache__"]:
            typer.echo(f"Legacy exclude patterns: {len(exclude)}")

        # If output directory specified, save representations
        if output:
            output_dir = os.path.abspath(output)
            os.makedirs(output_dir, exist_ok=True)

            # Save relationship map to JSON
            map_output = os.path.join(output_dir, "relationship_map.json")
            with open(map_output, "w", encoding="utf-8") as f:
                json.dump(relationship_map.to_json(detail), f, indent=2)
            typer.echo(f"Relationship map saved to: {map_output}")

            # Save example of JSON mirrors structure
            mirrors_output = os.path.join(output_dir, "json_mirrors_paths.json")
            with open(mirrors_output, "w", encoding="utf-8") as f:
                mirror_paths = json_mirrors.list_all_mirrors()
                json.dump({"mirrored_files": mirror_paths}, f, indent=2)
            typer.echo(f"JSON mirrors paths saved to: {mirrors_output}")

            typer.echo(f"JSON mirror files stored in: {json_mirrors.mirror_path}")

    except Exception as e:
        typer.echo(f"{Fore.RED}Error scanning path: {str(e)}{Style.RESET_ALL}")
        raise typer.Exit(code=1)


@app.command()
def sync(
    path: str = typer.Argument(".", help="Path to synchronize"),
    recursive: bool = typer.Option(
        False, "--recursive", "-r", help="Recursively synchronize subdirectories"
    ),
    force: bool = typer.Option(
        False, "--force", help="Force synchronization even if files are up to date"
    ),
    detail_level: str = typer.Option(
        "standard",
        "--detail-level",
        "-l",
        help="Detail level (minimal, standard, detailed)",
    ),
) -> None:
    """
    Synchronize code files with Architectum.

    Updates both the Relationship Map and JSON Mirrors representations
    for the specified files or directories. Only changed files are
    processed by default, unless --force is specified.

    The detail level controls how much information is included:

    - minimal: Basic structure information only
    - standard: Essential information including types and basic attributes
    - detailed: Comprehensive information including documentation
    """
    try:
        # Convert string detail level to enum
        try:
            detail = DetailLevel.from_string(detail_level)
        except ValueError as e:
            typer.echo(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
            raise typer.Exit(code=1)

        # Create ArchSync instance
        from arch_blueprint_generator.sync.arch_sync import ArchSync

        sync_instance = ArchSync()

        # Perform synchronization
        try:
            updated, added, removed = sync_instance.sync([path], recursive, force)

            typer.echo(
                f"{Fore.GREEN}Synchronization completed successfully:{Style.RESET_ALL}"
            )
            typer.echo(f"Paths: {path}")
            typer.echo(f"Updated: {updated}, Added: {added}, Removed: {removed}")
            typer.echo(f"Detail level: {detail.value}")
        except Exception as e:
            typer.echo(f"{Fore.RED}Error synchronizing: {str(e)}{Style.RESET_ALL}")
            raise typer.Exit(code=1)

    except Exception as e:
        typer.echo(f"{Fore.RED}Error synchronizing: {str(e)}{Style.RESET_ALL}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
