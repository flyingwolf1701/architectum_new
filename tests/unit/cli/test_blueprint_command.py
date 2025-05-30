"""Tests for the blueprint CLI command group."""

import json
import os
import pytest
from typer.testing import CliRunner
import textwrap

from arch_blueprint_generator.cli.commands import app


@pytest.fixture
def runner():
    """CLI runner fixture."""
    return CliRunner()


def test_blueprint_file_help(runner):
    """Verify help text for blueprint file command."""
    result = runner.invoke(app, ["blueprint", "file", "--help"])
    assert result.exit_code == 0
    assert "Generate a File-Based Blueprint" in result.output
    assert "--output" in result.output
    assert "--detail-level" in result.output


def test_blueprint_file_generation(runner, tmp_path):
    """Generate a blueprint from test files."""
    file1 = tmp_path / "a.py"
    file2 = tmp_path / "b.py"
    file1.write_text("def a():\n    return 1")
    file2.write_text("class B:\n    pass")

    output_file = tmp_path / "bp.json"
    result = runner.invoke(
        app,
        [
            "blueprint",
            "file",
            str(file1),
            str(file2),
            "--output",
            str(output_file),
        ],
    )
    assert result.exit_code == 0
    assert output_file.exists()
    data = json.loads(output_file.read_text())
    assert "files" in data["content"]
    assert len(data["content"]["files"]) == 2


def test_blueprint_file_invalid_detail_level(runner, tmp_path):
    """Invalid detail level should return error."""
    file1 = tmp_path / "a.py"
    file1.write_text("print('hi')")

    result = runner.invoke(
        app,
        ["blueprint", "file", str(file1), "--detail-level", "invalid"],
    )
    assert result.exit_code == 1
    assert "Invalid detail level" in result.output


def test_blueprint_file_with_detailed_level(runner, tmp_path):
    """Generate blueprint with detailed detail level."""
    file1 = tmp_path / "one.py"
    file2 = tmp_path / "two.py"
    file1.write_text("def x():\n    pass")
    file2.write_text("def y():\n    pass")
    output_file = tmp_path / "out.json"

    result = runner.invoke(
        app,
        [
            "blueprint",
            "file",
            str(file1),
            str(file2),
            "--output",
            str(output_file),
            "--detail-level",
            "detailed",
        ],
    )
    assert result.exit_code == 0
    assert output_file.exists()
    data = json.loads(output_file.read_text())
    assert len(data["content"]["files"]) == 2


def test_blueprint_create_from_yaml(runner, tmp_path):
    """Generate a blueprint using the create command with YAML."""
    yaml_content = textwrap.dedent(
        """
        type: file
        name: sample
        detail_level: minimal
        components:
          - file: a.py
            elements: []
          - file: b.py
            elements: []
        """
    )
    bp_yaml = tmp_path / "bp.yaml"
    bp_yaml.write_text(yaml_content)

    (tmp_path / "a.py").write_text("def a():\n    pass")
    (tmp_path / "b.py").write_text("def b():\n    pass")
    output_file = tmp_path / "out.json"

    result = runner.invoke(
        app,
        [
            "blueprint",
            "create",
            "-f",
            str(bp_yaml),
            "--output",
            str(output_file),
        ],
    )
    assert result.exit_code == 0
    assert output_file.exists()

