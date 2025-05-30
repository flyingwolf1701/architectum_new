"""Tests for the scan CLI command with gitignore support."""

import json
import os
import pytest
from typer.testing import CliRunner
import tempfile
import textwrap

from arch_blueprint_generator.cli.commands import app


@pytest.fixture
def runner():
    """CLI runner fixture."""
    return CliRunner()


@pytest.fixture
def test_project(tmp_path):
    """Create a test project structure with .gitignore."""
    # Create main source files
    (tmp_path / "main.py").write_text("def main(): pass")
    (tmp_path / "utils.py").write_text("def helper(): pass")
    
    # Create a subdirectory with files
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "module.py").write_text("class Module: pass")
    
    # Create files that should be ignored
    (tmp_path / "build.log").write_text("build output")
    (tmp_path / ".coverage").write_text("coverage data")
    
    build_dir = tmp_path / "build"
    build_dir.mkdir()
    (build_dir / "output.exe").write_text("binary")
    
    # Create .gitignore file
    gitignore_content = textwrap.dedent("""
        # Build artifacts
        build/
        *.log
        .coverage
        
        # Dependencies
        node_modules/
        __pycache__/
        
        # IDE files
        .vscode/
        *.pyc
    """).strip()
    (tmp_path / ".gitignore").write_text(gitignore_content)
    
    return tmp_path


def test_scan_help(runner):
    """Verify help text for scan command includes gitignore options."""
    result = runner.invoke(app, ["scan", "--help"])
    assert result.exit_code == 0
    assert "gitignore" in result.output.lower()
    assert "--ignore" in result.output
    assert "--no-gitignore" in result.output
    assert "GitIgnore Support" in result.output


def test_scan_basic_functionality(runner, test_project):
    """Test basic scan functionality with default gitignore support."""
    result = runner.invoke(app, ["scan", str(test_project)])
    assert result.exit_code == 0
    assert "Scan completed successfully" in result.output
    assert "GitIgnore: enabled" in result.output
    assert "GitIgnore patterns:" in result.output


def test_scan_with_gitignore_disabled(runner, test_project):
    """Test scan with gitignore disabled."""
    result = runner.invoke(app, ["scan", str(test_project), "--no-gitignore"])
    assert result.exit_code == 0
    assert "Scan completed successfully" in result.output
    assert "GitIgnore: disabled" in result.output


def test_scan_with_additional_ignores(runner, test_project):
    """Test scan with additional ignore patterns."""
    result = runner.invoke(app, [
        "scan", str(test_project),
        "--ignore", "*.tmp",
        "--ignore", "temp/"
    ])
    assert result.exit_code == 0
    assert "Scan completed successfully" in result.output
    assert "Additional ignore patterns: 2" in result.output


def test_scan_with_legacy_exclude_patterns(runner, test_project):
    """Test scan with legacy exclude patterns."""
    result = runner.invoke(app, [
        "scan", str(test_project),
        "--exclude", "custom_pattern",
        "--exclude", "another_pattern"
    ])
    assert result.exit_code == 0
    assert "Scan completed successfully" in result.output
    assert "Legacy exclude patterns: 2" in result.output


def test_scan_with_output_directory(runner, test_project, tmp_path):
    """Test scan with output directory specified."""
    output_dir = tmp_path / "output"
    result = runner.invoke(app, [
        "scan", str(test_project),
        "--output", str(output_dir)
    ])
    assert result.exit_code == 0
    assert "Scan completed successfully" in result.output
    
    # Check that output files are created
    assert (output_dir / "relationship_map.json").exists()
    assert (output_dir / "json_mirrors_paths.json").exists()


def test_scan_shows_pattern_counts(runner, test_project):
    """Test that scan shows gitignore pattern counts when patterns are loaded."""
    result = runner.invoke(app, ["scan", str(test_project)])
    assert result.exit_code == 0
    
    # Should show that gitignore patterns were loaded
    assert "GitIgnore patterns:" in result.output
    
    # Check for pattern count (should be > 0 due to our test .gitignore)
    lines = result.output.split('\n')
    gitignore_line = [line for line in lines if "GitIgnore patterns:" in line]
    assert len(gitignore_line) == 1
    
    # Extract the number and verify it's greater than 0
    import re
    match = re.search(r'GitIgnore patterns: (\d+)', gitignore_line[0])
    assert match
    pattern_count = int(match.group(1))
    assert pattern_count > 0


def test_scan_without_gitignore_file(runner, tmp_path):
    """Test scan in directory without .gitignore file."""
    # Create a simple directory without .gitignore
    (tmp_path / "main.py").write_text("def main(): pass")
    
    result = runner.invoke(app, ["scan", str(tmp_path)])
    assert result.exit_code == 0
    assert "Scan completed successfully" in result.output
    assert "GitIgnore: enabled" in result.output
    # Should not show gitignore patterns line since no .gitignore exists
    assert "GitIgnore patterns:" not in result.output


def test_scan_combined_options(runner, test_project):
    """Test scan with multiple options combined."""
    result = runner.invoke(app, [
        "scan", str(test_project),
        "--detail-level", "detailed",
        "--depth", "2",
        "--ignore", "*.bak",
        "--exclude", "custom",
        "--no-gitignore"
    ])
    assert result.exit_code == 0
    assert "Scan completed successfully" in result.output
    assert "Detail Level: detailed" in result.output
    assert "Depth: 2" in result.output
    assert "GitIgnore: disabled" in result.output
    assert "Additional ignore patterns: 1" in result.output
    assert "Legacy exclude patterns: 2" in result.output
