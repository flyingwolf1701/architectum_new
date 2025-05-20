import json
import os

from arch_blueprint_generator.models.nodes import FileNode, FunctionNode, ContainsRelationship
from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors, CodeElement
from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.blueprints.factory import BlueprintFactory


def _create_blueprint(tmp_path):
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


def test_file_based_blueprint_snapshot(tmp_path):
    blueprint = _create_blueprint(str(tmp_path))
    data = blueprint.to_json()
    snapshot = tmp_path / "file_blueprint_standard.json"
    snapshot.write_text(json.dumps(data, indent=2))
    loaded = json.loads(snapshot.read_text())
    assert loaded == data

