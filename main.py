#!/usr/bin/env python3
"""
Main entry point for Architectum Blueprint Generator.
"""

from arch_blueprint_generator.cli.commands import app
from arch_blueprint_generator.utils.logging import configure_logging


def main():
    """Run the Architectum Blueprint Generator CLI."""
    configure_logging()
    app()


if __name__ == "__main__":
    main()
