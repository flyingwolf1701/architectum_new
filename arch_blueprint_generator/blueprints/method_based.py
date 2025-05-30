"""Method-based blueprint implementation."""

from __future__ import annotations

import os
from typing import Dict, List, Any, Optional

from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors, FileContent
from arch_blueprint_generator.models.nodes import FileNode
from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.blueprints.base import Blueprint
from arch_blueprint_generator.errors.exceptions import BlueprintError
from arch_blueprint_generator.utils.logging import get_logger
from arch_blueprint_generator.extractors import MethodExtractor


logger = get_logger(__name__)


class MethodBasedBlueprint(Blueprint):
    """Blueprint focusing on specific methods within files."""

    def __init__(
        self,
        relationship_map: RelationshipMap,
        json_mirrors: JSONMirrors,
        components: Dict[str, List[str]],
        name: Optional[str] = None,
        detail_level: DetailLevel = DetailLevel.STANDARD,
    ) -> None:
        super().__init__(relationship_map, json_mirrors, name, detail_level)

        if not components:
            raise BlueprintError("At least one file component must be specified")

        self.components: Dict[str, List[str]] = {
            os.path.abspath(path): elems for path, elems in components.items()
        }

        self.missing: List[str] = []
        self._element_to_file: Dict[str, str] = {}

        self._validate_file_paths()

    def generate(self) -> None:
        """Generate a method-based blueprint."""

        self.content = {"files": [], "relationships": [], "missing_methods": []}

        for file_path, methods in self.components.items():
            info = self._process_file(file_path, methods)
            if info:
                self.content["files"].append(info)

        self._add_relationships()
        if self.missing:
            self.content["missing_methods"] = self.missing

        logger.info(
            f"Generated method-based blueprint for {len(self.components)} files"
        )

    def _process_file(self, file_path: str, methods: List[str]) -> Optional[Dict[str, Any]]:
        file_info: Dict[str, Any] = {"path": file_path, "elements": []}

        file_node_id = f"file:{file_path}"
        file_node = self.relationship_map.get_node(file_node_id, self.detail_level)

        if file_node and isinstance(file_node, FileNode):
            file_info["extension"] = file_node.extension
            if self.detail_level != DetailLevel.MINIMAL and file_node.metadata:
                file_info["metadata"] = file_node.metadata

        file_content = self.json_mirrors.get_mirrored_content(file_path, self.detail_level)
        if file_content and isinstance(file_content, FileContent):
            if "extension" not in file_info:
                file_info["extension"] = file_content.extension
            if file_content.imports and self.detail_level != DetailLevel.MINIMAL:
                file_info["imports"] = file_content.imports

        extractor = MethodExtractor(self.relationship_map, self.json_mirrors)
        elements, missing = extractor.extract(file_path, methods, self.detail_level)

        for element in elements:
            file_info["elements"].append(element)
            if "id" in element:
                self._element_to_file[element["id"]] = file_node_id

        for m in missing:
            self.missing.append(f"{file_path}:{m}")

        if file_node or file_content:
            return file_info
        return None

    def _add_relationships(self) -> None:
        relationships: List[Dict[str, Any]] = []

        def serialize(rel) -> Dict[str, Any]:
            info = {
                "type": rel.type.value,
                "source_id": rel.source_id,
                "target_id": rel.target_id,
            }
            if hasattr(rel, "line_number") and getattr(rel, "line_number") is not None:
                info["line_number"] = rel.line_number
            if self.detail_level == DetailLevel.DETAILED and rel.metadata:
                info["metadata"] = rel.metadata
            return info

        element_ids = set(self._element_to_file.keys())
        for element_id in element_ids:
            for rel in self.relationship_map.get_outgoing_relationships(element_id, self.detail_level):
                if rel.target_id in element_ids:
                    relationships.append(serialize(rel))

        self.content["relationships"] = relationships

    def _validate_file_paths(self) -> None:
        invalid = [p for p in self.components if not self._is_valid_file_path(p)]
        if invalid:
            raise BlueprintError(f"Invalid file paths: {invalid}")

    def _is_valid_file_path(self, path: str) -> bool:
        if os.path.isfile(path) and os.access(path, os.R_OK):
            return True
        file_node_id = f"file:{path}"
        if self.relationship_map.get_node(file_node_id):
            return True
        if self.json_mirrors.exists(path):
            return True
        return False

