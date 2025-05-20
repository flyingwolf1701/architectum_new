"""
File-based blueprint implementation.
"""

import os
from typing import Dict, Any, List, Optional, Set, Union

from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors, FileContent
from arch_blueprint_generator.models.nodes import (
    NodeType, FileNode, ContainsRelationship
)
from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.blueprints.base import Blueprint
from arch_blueprint_generator.errors.exceptions import BlueprintError
from arch_blueprint_generator.utils.logging import get_logger

logger = get_logger(__name__)


class FileBasedBlueprint(Blueprint):
    """
    Blueprint focusing on entire files.
    
    File-based blueprints combine information from both representations
    to provide a comprehensive view of specific files. They include
    both structural information (from the relationship map) and content
    details (from JSON mirrors).
    """
    
    def __init__(
        self,
        relationship_map: RelationshipMap,
        json_mirrors: JSONMirrors,
        file_paths: List[str],
        name: Optional[str] = None,
        detail_level: DetailLevel = DetailLevel.STANDARD
    ):
        """
        Initialize a file-based blueprint.
        
        Args:
            relationship_map: Relationship map containing code structure and relationships
            json_mirrors: JSON mirrors containing detailed file content
            file_paths: List of file paths to include in the blueprint
            name: Optional name for the blueprint
            detail_level: Level of detail to include in the blueprint
            
        Raises:
            BlueprintError: If any file path is invalid
        """
        super().__init__(relationship_map, json_mirrors, name, detail_level)
        
        if not file_paths:
            raise BlueprintError("At least one file path must be specified")
        
        self.file_paths = [os.path.abspath(path) for path in file_paths]

        # Validate file paths and remove or raise errors for invalid ones
        self._validate_file_paths()
        
    def generate(self) -> None:
        """
        Generate a file-based blueprint.
        
        Combines information from both representations to create a comprehensive
        view of the specified files.
        
        Raises:
            BlueprintError: If blueprint generation fails
        """
        try:
            self.content = {
                "files": [],
                "relationships": []
            }
            
            # Process each file
            for file_path in self.file_paths:
                file_info = self._process_file(file_path)
                if file_info:
                    self.content["files"].append(file_info)
            
            # Add relationships between files
            self._add_relationships()
            
            logger.info(f"Generated file-based blueprint for {len(self.file_paths)} files")
        except Exception as e:
            logger.error(f"Error generating file-based blueprint: {str(e)}")
            raise BlueprintError(f"Failed to generate file-based blueprint: {str(e)}")

    def to_json(self) -> Dict[str, Any]:
        """Return JSON representation including file paths."""
        data = super().to_json()
        data["file_paths"] = self.file_paths
        return data
    
    def _process_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Process a file to extract its information.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary of file information, or None if the file is not found
        """
        file_info: Dict[str, Any] = {
            "path": file_path,
            "elements": []
        }
        
        # Get file node from relationship map
        file_node_id = f"file:{file_path}"
        file_node = self.relationship_map.get_node(file_node_id, self.detail_level)
        
        if file_node and isinstance(file_node, FileNode):
            file_info["extension"] = file_node.extension
            
            # Add node metadata based on detail level
            if self.detail_level != DetailLevel.MINIMAL and file_node.metadata:
                file_info["metadata"] = file_node.metadata
            
            # Get file elements (functions, classes, etc.)
            self._add_file_elements(file_node_id, file_info)
        
        # Get file content from JSON mirrors
        file_content = self.json_mirrors.get_mirrored_content(file_path, self.detail_level)
        
        if file_content and isinstance(file_content, FileContent):
            # Add extension if not already added
            if "extension" not in file_info:
                file_info["extension"] = file_content.extension
            
            # Add imports if available
            if file_content.imports and (self.detail_level != DetailLevel.MINIMAL):
                file_info["imports"] = file_content.imports
            
            # Add code elements from JSON mirrors if available
            if file_content.elements and (self.detail_level != DetailLevel.MINIMAL):
                json_elements = []
                for name, element in file_content.elements.items():
                    element_info = {
                        "name": name,
                        "type": element.type,
                        "line_start": element.line_start,
                        "line_end": element.line_end
                    }
                    
                    # Add metadata for detailed level
                    if self.detail_level == DetailLevel.DETAILED and element.metadata:
                        element_info["metadata"] = element.metadata
                    
                    json_elements.append(element_info)
                
                # Only add JSON elements if not already added from relationship map
                if not file_info["elements"]:
                    file_info["elements"] = json_elements
                
                # Combine with existing elements if both sources have elements
                # This is a simple approach - in a real system, we might want to
                # merge elements from both sources more intelligently
                element_names = {e["name"] for e in file_info["elements"]}
                for element in json_elements:
                    if element["name"] not in element_names:
                        file_info["elements"].append(element)
                        element_names.add(element["name"])
        
        # Return file info if we have any information from either representation
        if file_node or file_content:
            return file_info
        
        return None
    
    def _add_file_elements(self, file_node_id: str, file_info: Dict[str, Any]) -> None:
        """
        Add file elements from the relationship map.
        
        Args:
            file_node_id: ID of the file node
            file_info: Dictionary to add elements to
        """
        # Get outgoing "contains" relationships to find elements
        outgoing_rels = self.relationship_map.get_outgoing_relationships(file_node_id, self.detail_level)
        contains_rels = [rel for rel in outgoing_rels if rel.type.value == "contains"]
        
        elements = []
        for rel in contains_rels:
            target_id = rel.target_id
            element_node = self.relationship_map.get_node(target_id, self.detail_level)
            
            if element_node:
                element_info = {
                    "id": element_node.id,
                    "type": element_node.type.value
                }
                
                # Add specific fields based on node type
                if hasattr(element_node, "name"):
                    element_info["name"] = element_node.name
                
                if hasattr(element_node, "line_start") and element_node.line_start is not None:
                    element_info["line_start"] = element_node.line_start
                
                if hasattr(element_node, "line_end") and element_node.line_end is not None:
                    element_info["line_end"] = element_node.line_end
                
                # Add metadata for detailed level
                if self.detail_level == DetailLevel.DETAILED and element_node.metadata:
                    element_info["metadata"] = element_node.metadata
                
                elements.append(element_info)
        
        if elements:
            file_info["elements"] = elements
    
    def _add_relationships(self) -> None:
        """
        Add relationships between files in the blueprint.
        
        This includes file imports, function calls between files, etc.
        """
        # Create a set of node IDs for the files in this blueprint
        file_node_ids = {f"file:{path}" for path in self.file_paths}
        
        # Get all relationships where both source and target are in this blueprint
        relationships = []
        for source_id in file_node_ids:
            # Check outgoing relationships
            outgoing_rels = self.relationship_map.get_outgoing_relationships(source_id, self.detail_level)
            for rel in outgoing_rels:
                # Skip "contains" relationships as they're already handled in file elements
                if rel.type.value == "contains":
                    continue
                
                # Only include relationships to other files in this blueprint
                if rel.target_id in file_node_ids:
                    relationships.append({
                        "type": rel.type.value,
                        "source_id": rel.source_id,
                        "target_id": rel.target_id
                    })
                    
                    # Add metadata for detailed level
                    if self.detail_level == DetailLevel.DETAILED and rel.metadata:
                        relationships[-1]["metadata"] = rel.metadata
        
        self.content["relationships"] = relationships

    def _validate_file_paths(self) -> None:
        """Validate provided file paths and handle invalid ones."""
        invalid_paths = []
        for path in self.file_paths:
            if not self._is_valid_file_path(path):
                invalid_paths.append(path)

        if invalid_paths:
            if len(invalid_paths) == len(self.file_paths):
                raise BlueprintError(
                    f"All specified file paths are invalid: {invalid_paths}"
                )
            logger.warning(
                f"Some file paths are invalid and will be skipped: {invalid_paths}"
            )
            self.file_paths = [p for p in self.file_paths if p not in invalid_paths]

    def _is_valid_file_path(self, path: str) -> bool:
        """Return True if the file path is valid in any representation."""
        if os.path.isfile(path) and os.access(path, os.R_OK):
            return True

        file_node_id = f"file:{path}"
        if self.relationship_map.get_node(file_node_id):
            return True

        if self.json_mirrors.exists(path):
            return True

        return False
