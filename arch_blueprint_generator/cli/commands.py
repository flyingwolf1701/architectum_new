"""
Command-line interface for Architectum Blueprint Generator.
"""

import json
import os
import typer
from typing import List, Optional
from colorama import Fore, Style

from arch_blueprint_generator.utils.logging import configure_logging, get_logger
from arch_blueprint_generator.scanner.path_scanner import PathScanner
from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.errors.exceptions import BlueprintError

app = typer.Typer(help="Architectum Blueprint Generator")
logger = get_logger(__name__)


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
        False, "--version", "-v", callback=version_callback, is_eager=True,
        help="Show version information and exit."
    ),
    verbose: bool = typer.Option(
        False, "--verbose", help="Enable verbose output."
    )
):
    """
    Architectum Blueprint Generator - A tool for code comprehension.
    """
    import logging
    log_level = logging.DEBUG if verbose else logging.INFO
    configure_logging(log_level)


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
    ),
    name: Optional[str] = typer.Option(
        None,
        "--name", "-n",
        help="Name for the blueprint"
    ),
    type: str = typer.Option(
        "file",
        "--type", "-t",
        help="Blueprint type (file, component, feature, temporary)"
    )
) -> None:
    """
    Generate a blueprint from specified files.
    
    Creates a blueprint representation of the specified files with the chosen
    detail level. The detail level controls how much information is included:
    
    - minimal: Basic structure information only
    - standard: Essential information including types and basic attributes
    - detailed: Comprehensive information including documentation
    """
    try:
        # Check if files are provided
        if not files:
            typer.echo(f"{Fore.RED}Error: No files specified{Style.RESET_ALL}")
            raise typer.Exit(code=1)
        
        # Convert string detail level to enum
        try:
            detail = DetailLevel.from_string(detail_level)
        except ValueError as e:
            typer.echo(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
            raise typer.Exit(code=1)
        
        # Normalize blueprint type
        blueprint_type = type.lower()
        if blueprint_type == "file":
            blueprint_type = "FileBasedBlueprint"
        else:
            typer.echo(f"{Fore.RED}Error: Unsupported blueprint type: {type}{Style.RESET_ALL}")
            typer.echo(f"Supported types: file")
            raise typer.Exit(code=1)
        
        # Create scanner for the first file to ensure we have representations
        first_file_dir = os.path.dirname(os.path.abspath(files[0]))
        scanner = PathScanner(first_file_dir)
        relationship_map, json_mirrors = scanner.scan()
        
        # Create blueprint factory
        from arch_blueprint_generator.blueprints.factory import BlueprintFactory
        
        # Create blueprint based on type
        if blueprint_type == "FileBasedBlueprint":
            blueprint = BlueprintFactory.create_file_blueprint(
                relationship_map,
                json_mirrors,
                files,
                name=name,
                detail_level=detail
            )
        
        # Generate blueprint content
        blueprint.generate()
        
        # Output the blueprint
        if output == "-":
            # Print to stdout
            if format.lower() == "json":
                result = json.dumps(blueprint.to_json(), indent=2)
                typer.echo(result)
            elif format.lower() == "xml":
                typer.echo(blueprint.to_xml())
            else:
                typer.echo(f"{Fore.RED}Error: Unsupported format: {format}{Style.RESET_ALL}")
                typer.echo(f"Supported formats: json, xml")
                raise typer.Exit(code=1)
        else:
            # Save to file
            blueprint.save(output, format)
            typer.echo(f"{Fore.GREEN}Blueprint saved to: {output}{Style.RESET_ALL}")
        
    except Exception as e:
        typer.echo(f"{Fore.RED}Error generating blueprint: {str(e)}{Style.RESET_ALL}")
        raise typer.Exit(code=1)


@app.command()
def scan(
    path: str = typer.Argument(
        ".", 
        help="Path to scan"
    ),
    depth: int = typer.Option(
        0, 
        "--depth", "-d", 
        help="Maximum depth to scan (0 for no limit)"
    ),
    output: str = typer.Option(
        None, 
        "--output", "-o", 
        help="Output directory for saving representations"
    ),
    exclude: List[str] = typer.Option(
        [".git", ".venv", "__pycache__"], 
        "--exclude", "-e", 
        help="Patterns to exclude from scanning"
    ),
    detail_level: str = typer.Option(
        "standard", 
        "--detail-level", "-l", 
        help="Detail level (minimal, standard, detailed)"
    )
) -> None:
    """
    Scan a directory path and generate both representations.
    
    Creates both Relationship Map and JSON Mirrors representations
    for the specified path. The detail level controls how much
    information is included:
    
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
            
        # Create and run the path scanner
        scanner = PathScanner(path, exclude_patterns=exclude)
        relationship_map, json_mirrors = scanner.scan(max_depth=depth, detail_level=detail)
        
        node_count = relationship_map.node_count()
        relationship_count = relationship_map.relationship_count()
        
        typer.echo(f"{Fore.GREEN}Scan completed successfully:{Style.RESET_ALL}")
        typer.echo(f"Path: {os.path.abspath(path)}")
        typer.echo(f"Depth: {depth if depth > 0 else 'unlimited'}")
        typer.echo(f"Detail Level: {detail.value}")
        typer.echo(f"Nodes: {node_count}")
        typer.echo(f"Relationships: {relationship_count}")
        
        # If output directory specified, save representations
        if output:
            output_dir = os.path.abspath(output)
            os.makedirs(output_dir, exist_ok=True)
            
            # Save relationship map to JSON
            map_output = os.path.join(output_dir, "relationship_map.json")
            with open(map_output, 'w', encoding='utf-8') as f:
                json.dump(relationship_map.to_json(detail), f, indent=2)
            typer.echo(f"Relationship map saved to: {map_output}")
            
            # Save example of JSON mirrors structure
            mirrors_output = os.path.join(output_dir, "json_mirrors_paths.json")
            with open(mirrors_output, 'w', encoding='utf-8') as f:
                mirror_paths = json_mirrors.list_all_mirrors()
                json.dump({"mirrored_files": mirror_paths}, f, indent=2)
            typer.echo(f"JSON mirrors paths saved to: {mirrors_output}")
            
            typer.echo(f"JSON mirror files stored in: {json_mirrors.mirror_path}")
            
    except Exception as e:
        typer.echo(f"{Fore.RED}Error scanning path: {str(e)}{Style.RESET_ALL}")
        raise typer.Exit(code=1)


@app.command()
def sync(
    path: str = typer.Argument(
        ".", 
        help="Path to synchronize"
    ),
    recursive: bool = typer.Option(
        False, 
        "--recursive", "-r", 
        help="Recursively synchronize subdirectories"
    ),
    force: bool = typer.Option(
        False, 
        "--force", 
        help="Force synchronization even if files are up to date"
    ),
    detail_level: str = typer.Option(
        "standard", 
        "--detail-level", "-l", 
        help="Detail level (minimal, standard, detailed)"
    )
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
            
            typer.echo(f"{Fore.GREEN}Synchronization completed successfully:{Style.RESET_ALL}")
            typer.echo(f"Paths: {path}")
            typer.echo(f"Updated: {updated}, Added: {added}, Removed: {removed}")
            typer.echo(f"Detail level: {detail.value}")
        except Exception as e:
            typer.echo(f"{Fore.RED}Error synchronizing: {str(e)}{Style.RESET_ALL}")
            raise typer.Exit(code=1)
            
    except Exception as e:
        typer.echo(f"{Fore.RED}Error synchronizing: {str(e)}{Style.RESET_ALL}")
        raise typer.Exit(code=1)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
