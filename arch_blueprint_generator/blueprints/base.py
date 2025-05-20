"""
Base class for blueprints.
"""

import json
import os
from abc import ABC, abstractmethod
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Optional, Set, Union, TypeVar, Generic

from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors
from arch_blueprint_generator.errors.exceptions import BlueprintError
from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.utils.logging import get_logger

logger = get_logger(__name__)


class Blueprint(ABC):
    """
    Abstract base class for all blueprint types.
    
    Blueprints combine elements from both core representations 
    (Relationship Map and JSON Mirrors) to create specialized views
    for different use cases.
    """
    
    def __init__(
        self, 
        relationship_map: RelationshipMap,
        json_mirrors: JSONMirrors,
        name: Optional[str] = None,
        detail_level: DetailLevel = DetailLevel.STANDARD
    ):
        """
        Initialize a blueprint.
        
        Args:
            relationship_map: Relationship map containing code structure and relationships
            json_mirrors: JSON mirrors containing detailed file content
            name: Optional name for the blueprint
            detail_level: Level of detail to include in the blueprint
            
        Raises:
            BlueprintError: If the relationship map or JSON mirrors are invalid
        """
        if not isinstance(relationship_map, RelationshipMap):
            raise BlueprintError("relationship_map must be a RelationshipMap instance")
        
        if not isinstance(json_mirrors, JSONMirrors):
            raise BlueprintError("json_mirrors must be a JSONMirrors instance")
        
        self.relationship_map = relationship_map
        self.json_mirrors = json_mirrors
        self.name = name or self.__class__.__name__
        self.detail_level = detail_level
        self.content: Dict[str, Any] = {}
        
        logger.info(f"Initialized {self.__class__.__name__} blueprint with {detail_level.value} detail level")
    
    @abstractmethod
    def generate(self) -> None:
        """
        Generate the blueprint content.
        
        This method must be implemented by subclasses to populate
        the blueprint's content dictionary.
        
        Raises:
            BlueprintError: If blueprint generation fails
        """
        pass
    
    def to_json(self) -> Dict[str, Any]:
        """
        Convert the blueprint to a JSON representation.
        
        Returns:
            JSON representation of the blueprint
            
        Raises:
            BlueprintError: If blueprint content has not been generated
        """
        if not self.content:
            raise BlueprintError("Blueprint content has not been generated. Call generate() first.")
        
        result = {
            "name": self.name,
            "type": self.__class__.__name__,
            "detail_level": self.detail_level.value,
            "content": self.content
        }
        
        return result
    
    def to_xml(self) -> str:
        """
        Convert the blueprint to an XML representation.
        
        Returns:
            XML representation of the blueprint
            
        Raises:
            BlueprintError: If blueprint content has not been generated
        """
        if not self.content:
            raise BlueprintError("Blueprint content has not been generated. Call generate() first.")
        
        def dict_to_xml(parent_elem, data):
            """Convert a dictionary to XML elements."""
            if isinstance(data, dict):
                for key, value in data.items():
                    if key.startswith('@'):
                        # Handle attributes
                        parent_elem.set(key[1:], str(value))
                    elif key == '#text':
                        # Handle text content
                        parent_elem.text = str(value)
                    else:
                        # Create new element
                        child = ET.SubElement(parent_elem, key)
                        dict_to_xml(child, value)
            elif isinstance(data, list):
                for item in data:
                    # For lists, create items with the parent's tag + "Item"
                    item_tag = parent_elem.tag + "Item"
                    child = ET.SubElement(parent_elem, item_tag)
                    dict_to_xml(child, item)
            else:
                # For primitives, just set the text
                parent_elem.text = str(data)
        
        # Create root element
        root = ET.Element("Blueprint")
        root.set("name", self.name)
        root.set("type", self.__class__.__name__)
        root.set("detailLevel", self.detail_level.value)
        
        # Add content
        content_elem = ET.SubElement(root, "Content")
        dict_to_xml(content_elem, self.content)
        
        # Convert to string with pretty formatting
        rough_string = ET.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def save(self, path: str, format: str = "json") -> None:
        """
        Save the blueprint to a file.
        
        Args:
            path: Path to save the blueprint to
            format: Format to save in ("json" or "xml")
            
        Raises:
            BlueprintError: If an invalid format is specified or if saving fails
        """
        if not self.content:
            raise BlueprintError("Blueprint content has not been generated. Call generate() first.")
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
            
            if format.lower() == "json":
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(self.to_json(), f, indent=2)
            elif format.lower() == "xml":
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(self.to_xml())
            else:
                raise BlueprintError(f"Invalid format: {format}. Supported formats are 'json' and 'xml'.")
            
            logger.info(f"Saved blueprint to {path} in {format} format")
        except Exception as e:
            raise BlueprintError(f"Failed to save blueprint: {str(e)}")
    
    @classmethod
    def load(cls, path: str, relationship_map: RelationshipMap, json_mirrors: JSONMirrors) -> 'Blueprint':
        """
        Load a blueprint from a file.
        
        Args:
            path: Path to load the blueprint from
            relationship_map: Relationship map to use for the blueprint
            json_mirrors: JSON mirrors to use for the blueprint
            
        Returns:
            Loaded blueprint
            
        Raises:
            BlueprintError: If loading fails
        """
        try:
            # Determine format based on file extension
            ext = os.path.splitext(path)[1].lower()
            
            if ext == '.json':
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Import here to avoid circular imports
                from arch_blueprint_generator.blueprints.factory import BlueprintFactory
                
                # Create blueprint of the right type
                blueprint_type = data.get("type", cls.__name__)
                extra_args = {}
                if "file_paths" in data:
                    extra_args["file_paths"] = data["file_paths"]

                blueprint = BlueprintFactory.create_blueprint(
                    blueprint_type,
                    relationship_map,
                    json_mirrors,
                    data.get("name"),
                    DetailLevel.from_string(data.get("detail_level", "standard")),
                    **extra_args,
                )
                
                # Set content
                blueprint.content = data.get("content", {})
                
                return blueprint
            else:
                raise BlueprintError(f"Unsupported file format: {ext}")
        except Exception as e:
            raise BlueprintError(f"Failed to load blueprint: {str(e)}")
