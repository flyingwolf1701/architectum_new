import json
from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.models.nodes import FileNode, FunctionNode
from arch_blueprint_generator.models.relationship_map import (
    RelationshipMap,
    ContainsRelationship,
)


def _create_simple_map() -> RelationshipMap:
    relationship_map = RelationshipMap()
    file_node = FileNode("file1", "path/to/file.py", ".py")
    function_node = FunctionNode("func1", "test_function")
    relationship_map.add_node(file_node)
    relationship_map.add_node(function_node)
    relationship_map.add_relationship(ContainsRelationship("file1", "func1"))
    return relationship_map


def test_relationship_map_snapshot_minimal(tmp_path):
    relationship_map = _create_simple_map()
    data = relationship_map.to_json(detail_level=DetailLevel.MINIMAL)
    snapshot = tmp_path / "relationship_map_minimal.json"
    snapshot.write_text(json.dumps(data, indent=2))
    loaded = json.loads(snapshot.read_text())
    assert loaded == data


def test_relationship_map_snapshot_detailed(tmp_path):
    relationship_map = _create_simple_map()
    data = relationship_map.to_json(detail_level=DetailLevel.DETAILED)
    snapshot = tmp_path / "relationship_map_detailed.json"
    snapshot.write_text(json.dumps(data, indent=2))
    loaded = json.loads(snapshot.read_text())
    assert loaded == data
    minimal_size = len(
        json.dumps(relationship_map.to_json(detail_level=DetailLevel.MINIMAL))
    )
    detailed_size = len(json.dumps(loaded))
    assert detailed_size > minimal_size
