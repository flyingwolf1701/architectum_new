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
    )
) -> None:
    """
    Generate a blueprint from specified files.
    """
    typer.echo(f"{Fore.YELLOW}Blueprint generation not yet implemented{Style.RESET_ALL}")
    typer.echo(f"Would generate blueprint for files: {files}")
    typer.echo(f"Output: {output}, Format: {format}, Detail Level: {detail_level}")


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
    )
) -> None:
    """
    Scan a directory path and generate both representations.
    """
    try:
        # Create and run the path scanner
        scanner = PathScanner(path, exclude_patterns=exclude)
        relationship_map, json_mirrors = scanner.scan(max_depth=depth)
        
        node_count = relationship_map.node_count()
        relationship_count = relationship_map.relationship_count()
        
        typer.echo(f"{Fore.GREEN}Scan completed successfully:{Style.RESET_ALL}")
        typer.echo(f"Path: {os.path.abspath(path)}")
        typer.echo(f"Depth: {depth if depth > 0 else 'unlimited'}")
        typer.echo(f"Nodes: {node_count}")
        typer.echo(f"Relationships: {relationship_count}")
        
        # If output directory specified, save representations
        if output:
            output_dir = os.path.abspath(output)
            os.makedirs(output_dir, exist_ok=True)
            
            # Save relationship map to JSON
            map_output = os.path.join(output_dir, "relationship_map.json")
            with open(map_output, 'w', encoding='utf-8') as f:
                json.dump(relationship_map.to_json(), f, indent=2)
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
    )
) -> None:
    """
    Synchronize code files with Architectum.
    """
    typer.echo(f"{Fore.YELLOW}Synchronization not yet implemented{Style.RESET_ALL}")
    typer.echo(f"Would synchronize path: {path}")
    typer.echo(f"Recursive: {recursive}, Force: {force}")


if __name__ == "__main__":
    app()
