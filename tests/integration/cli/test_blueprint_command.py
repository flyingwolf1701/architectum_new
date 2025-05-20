"""Integration tests for blueprint CLI."""

import json
from typer.testing import CliRunner
from arch_blueprint_generator.cli.commands import app


def test_cli_file_blueprint(tmp_path):
    runner = CliRunner()
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
