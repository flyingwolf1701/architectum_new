"""Tests for the MethodBasedBlueprint class."""

import os
import tempfile
from typing import Dict, List

import pytest

from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors, FileContent, CodeElement
from arch_blueprint_generator.models.nodes import (
    FileNode,
    FunctionNode,
    ContainsRelationship,
)
from arch_blueprint_generator.blueprints.method_based import MethodBasedBlueprint


class TestMethodBasedBlueprint:
    """Tests for method-focused blueprint generation."""

    @pytest.fixture
    def temp_file(self, tmp_path) -> str:
        path = tmp_path / "file.py"
        path.write_text("def foo():\n    return 1\n")
        return str(path)

    @pytest.fixture
    def relationship_map(self, temp_file) -> RelationshipMap:
        rm = RelationshipMap()
        file_node = FileNode(f"file:{temp_file}", temp_file, ".py")
        func_node = FunctionNode(
            f"func:{temp_file}:foo",
            "foo",
            parameters=[],
            return_type=None,
            line_start=1,
            line_end=2,
        )
        rm.add_node(file_node)
        rm.add_node(func_node)
        rm.add_relationship(ContainsRelationship(file_node.id, func_node.id))
        return rm

    @pytest.fixture
    def json_mirrors(self, temp_file) -> JSONMirrors:
        jm = JSONMirrors(os.path.dirname(temp_file))
        elements = {
            "foo": CodeElement("foo", "function", 1, 2, {})
        }
        jm.create_file_mirror(temp_file, elements, [])
        return jm

    def test_generate(self, relationship_map, json_mirrors, temp_file):
        bp = MethodBasedBlueprint(
            relationship_map,
            json_mirrors,
            {temp_file: ["foo"]},
        )

        bp.generate()

        assert "files" in bp.content
        assert len(bp.content["files"]) == 1
        file_info = bp.content["files"][0]
        assert file_info["path"] == temp_file
        assert any(e["name"] == "foo" for e in file_info["elements"])

    def test_missing_method(self, relationship_map, json_mirrors, temp_file):
        bp = MethodBasedBlueprint(
            relationship_map,
            json_mirrors,
            {temp_file: ["bar"]},
        )

        bp.generate()

        assert bp.content.get("missing_methods")
        assert f"{temp_file}:bar" in bp.content["missing_methods"]

