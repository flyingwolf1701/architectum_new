"""
Command-line interface for Architectum Blueprint Generator.
"""

import typer
from typing import List, Optional
from colorama import Fore, Style

from arch_blueprint_generator.utils.logging import configure_logging, get_logger

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
