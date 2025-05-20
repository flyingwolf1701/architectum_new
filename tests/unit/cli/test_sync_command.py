"""
Tests for the sync command in the CLI module.
"""

import os
import pytest
from typer.testing import CliRunner

from arch_blueprint_generator.cli.commands import app
from arch_blueprint_generator.sync.arch_sync import ArchSync


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


def test_sync_help(runner):
    """Test the sync command help text."""
    result = runner.invoke(app, ["sync", "--help"])
    
    # Check that the command executes successfully
    assert result.exit_code == 0
    
    # Check that help text includes key options
    assert "Synchronize code files with Architectum" in result.output
    assert "--recursive" in result.output
    assert "--force" in result.output


def test_sync_version(runner):
    """Test the global version option with the sync command."""
    result = runner.invoke(app, ["--version", "sync"])
    
    # Check that the command executes successfully
    assert result.exit_code == 0
    
    # Check that version information is displayed
    assert "Architectum Blueprint Generator v" in result.output


# Mock the ArchSync.sync method to avoid file system access
def test_sync_command_execution(runner, monkeypatch):
    """Test that the sync command executes correctly."""
    # Mock the ArchSync.sync method
    def mock_sync(self, paths, recursive, force):
        return 1, 2, 3  # updated, added, removed
    
    monkeypatch.setattr(ArchSync, "sync", mock_sync)
    
    # Run the command
    result = runner.invoke(app, ["sync", "test_path", "--recursive", "--force"])
    
    # Check that the command executes successfully
    assert result.exit_code == 0
    
    # Check that the output contains the expected information
    assert "Synchronization completed successfully" in result.output
    assert "Paths: test_path" in result.output
    assert "Updated: 1, Added: 2, Removed: 3" in result.output


# Mock the ArchSync.sync method to raise an exception
def test_sync_command_error(runner, monkeypatch):
    """Test that the sync command handles errors correctly."""
    # Mock the ArchSync.sync method to raise an exception
    def mock_sync_error(self, paths, recursive, force):
        raise Exception("Test error")
    
    monkeypatch.setattr(ArchSync, "sync", mock_sync_error)
    
    # Run the command
    result = runner.invoke(app, ["sync", "test_path"])
    
    # Check that the command fails with the expected error
    assert result.exit_code == 1
    assert "Error synchronizing: Test error" in result.output
