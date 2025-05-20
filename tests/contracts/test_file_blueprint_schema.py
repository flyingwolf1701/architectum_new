import os
from pydantic import BaseModel, ValidationError
from typing import List, Dict, Any

from arch_blueprint_generator.models.nodes import FileNode, FunctionNode, ContainsRelationship
from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors, CodeElement
from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.blueprints.factory import BlueprintFactory


class FileEntry(BaseModel):
    path: str
    extension: str | None = None
    elements: List[Dict[str, Any]] = []


class FileBlueprintSchema(BaseModel):
    name: str
    type: str
    detail_level: str
    file_paths: List[str]
    content: Dict[str, Any]


def _create_blueprint(tmp_path: str):
    file_path = os.path.join(tmp_path, "file.py")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("def func():\n    pass\n")

    relationship_map = RelationshipMap()
    json_mirrors = JSONMirrors(tmp_path)

    file_node = FileNode(f"file:{file_path}", file_path, ".py")
    func_node = FunctionNode(f"func:{file_path}:func", "func")
    relationship_map.add_node(file_node)
    relationship_map.add_node(func_node)
    relationship_map.add_relationship(ContainsRelationship(file_node.id, func_node.id))

    elements = {"func": CodeElement("func", "function", 1, 2, {})}
    json_mirrors.create_file_mirror(file_path, elements, [])

    blueprint = BlueprintFactory.create_file_blueprint(
        relationship_map,
        json_mirrors,
        [file_path],
        detail_level=DetailLevel.STANDARD,
    )
    blueprint.generate()
    return blueprint


def test_file_blueprint_contract(tmp_path):
    blueprint = _create_blueprint(str(tmp_path))
    data = blueprint.to_json()

    # Validate top-level schema
    schema = FileBlueprintSchema.model_validate(data)

    # Validate each file entry
    files = schema.content.get("files", [])
    for entry in files:
        FileEntry.model_validate(entry)

