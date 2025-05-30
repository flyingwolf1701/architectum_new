"""Utilities for extracting method information from representations."""

from typing import List, Tuple, Dict, Any

from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors, FileContent
from arch_blueprint_generator.models.nodes import NodeType
from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.utils.logging import get_logger


logger = get_logger(__name__)


class MethodExtractor:
    """Extract method details from both representations."""

    def __init__(self, relationship_map: RelationshipMap, json_mirrors: JSONMirrors) -> None:
        self.relationship_map = relationship_map
        self.json_mirrors = json_mirrors

    def extract(
        self,
        file_path: str,
        method_names: List[str],
        detail_level: DetailLevel = DetailLevel.STANDARD,
    ) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Return information for requested methods and list missing ones."""

        found: List[Dict[str, Any]] = []
        missing: List[str] = []

        file_content = self.json_mirrors.get_mirrored_content(file_path, detail_level)

        for name in method_names:
            element_info: Dict[str, Any] | None = None

            # Search relationship map
            for node_type in [NodeType.FUNCTION, NodeType.CLASS, NodeType.METHOD]:
                nodes = self.relationship_map.nodes_by_type.get(node_type, {})
                for node_id, node in nodes.items():
                    if file_path in node_id and getattr(node, "name", None) == name:
                        element_info = {
                            "id": node.id,
                            "type": node.type.value,
                            "name": node.name,
                        }
                        if hasattr(node, "line_start") and node.line_start is not None:
                            element_info["line_start"] = node.line_start
                        if hasattr(node, "line_end") and node.line_end is not None:
                            element_info["line_end"] = node.line_end
                        if detail_level == DetailLevel.DETAILED and node.metadata:
                            element_info["metadata"] = node.metadata
                        break
                if element_info:
                    break

            # Add data from JSON mirrors
            if file_content and isinstance(file_content, FileContent):
                elem = file_content.elements.get(name)
                if elem:
                    if element_info is None:
                        element_info = {
                            "name": elem.name,
                            "type": elem.type,
                        }
                    element_info.setdefault("line_start", elem.line_start)
                    element_info.setdefault("line_end", elem.line_end)
                    if detail_level != DetailLevel.MINIMAL and elem.metadata:
                        if detail_level == DetailLevel.DETAILED:
                            element_info.setdefault("metadata", elem.metadata)
                        else:
                            essential = {
                                k: v
                                for k, v in elem.metadata.items()
                                if k
                                in {"visibility", "return_type", "parameters", "doc_summary"}
                            }
                            if essential:
                                element_info.setdefault("metadata", essential)

            if element_info:
                found.append(element_info)
            else:
                missing.append(name)

        return found, missing

