"""
Factory for creating blueprints.
"""

from typing import Dict, Any, List, Optional, Type, Union

from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors
from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.blueprints.base import Blueprint
from arch_blueprint_generator.errors.exceptions import BlueprintError
from arch_blueprint_generator.utils.logging import get_logger

# Import implementation classes
from arch_blueprint_generator.blueprints.file_based import FileBasedBlueprint
from arch_blueprint_generator.blueprints.method_based import MethodBasedBlueprint

logger = get_logger(__name__)


class BlueprintFactory:
    """
    Factory for creating various types of blueprints.
    
    This class provides methods for creating blueprints of different types
    based on string identifiers, allowing dynamic blueprint creation.
    """
    
    # Registry of blueprint types
    _blueprint_types: Dict[str, Type[Blueprint]] = {
        "FileBasedBlueprint": FileBasedBlueprint,
        "MethodBasedBlueprint": MethodBasedBlueprint,
        # More blueprint types will be added here as they are implemented
    }
    
    @classmethod
    def register_blueprint_type(cls, name: str, blueprint_class: Type[Blueprint]) -> None:
        """
        Register a new blueprint type.
        
        Args:
            name: Name to register the blueprint type under
            blueprint_class: Blueprint class to register
            
        Raises:
            BlueprintError: If the name is already registered
        """
        if name in cls._blueprint_types:
            raise BlueprintError(f"Blueprint type '{name}' is already registered")
        
        cls._blueprint_types[name] = blueprint_class
        logger.debug(f"Registered blueprint type: {name}")
    
    @classmethod
    def create_blueprint(
        cls,
        blueprint_type: str,
        relationship_map: RelationshipMap,
        json_mirrors: JSONMirrors,
        name: Optional[str] = None,
        detail_level: DetailLevel = DetailLevel.STANDARD,
        **kwargs
    ) -> Blueprint:
        """
        Create a blueprint of the specified type.
        
        Args:
            blueprint_type: Type of blueprint to create
            relationship_map: Relationship map to use
            json_mirrors: JSON mirrors to use
            name: Optional name for the blueprint
            detail_level: Detail level to use
            **kwargs: Additional arguments to pass to the blueprint constructor
            
        Returns:
            Created blueprint
            
        Raises:
            BlueprintError: If the blueprint type is not registered
        """
        # Handle various ways the type might be specified
        if blueprint_type in cls._blueprint_types:
            blueprint_class = cls._blueprint_types[blueprint_type]
        else:
            # Try to match with or without 'Blueprint' suffix
            normalized_type = blueprint_type
            if not normalized_type.endswith("Blueprint"):
                normalized_type += "Blueprint"
            
            if normalized_type in cls._blueprint_types:
                blueprint_class = cls._blueprint_types[normalized_type]
            else:
                raise BlueprintError(
                    f"Unknown blueprint type: '{blueprint_type}'. "
                    f"Available types: {', '.join(cls._blueprint_types.keys())}"
                )
        
        # Create blueprint instance
        try:
            blueprint = blueprint_class(
                relationship_map,
                json_mirrors,
                name=name,
                detail_level=detail_level,
                **kwargs
            )
            
            logger.info(f"Created blueprint of type: {blueprint_class.__name__}")
            return blueprint
        except Exception as e:
            raise BlueprintError(f"Failed to create blueprint: {str(e)}")
    
    @classmethod
    def create_file_blueprint(
        cls,
        relationship_map: RelationshipMap,
        json_mirrors: JSONMirrors,
        file_paths: List[str],
        name: Optional[str] = None,
        detail_level: DetailLevel = DetailLevel.STANDARD
    ) -> FileBasedBlueprint:
        """
        Create a file-based blueprint.
        
        Args:
            relationship_map: Relationship map to use
            json_mirrors: JSON mirrors to use
            file_paths: List of file paths to include
            name: Optional name for the blueprint
            detail_level: Detail level to use
            
        Returns:
            Created file-based blueprint
        """
        return cls.create_blueprint(
            "FileBasedBlueprint",
            relationship_map,
            json_mirrors,
            name=name,
            detail_level=detail_level,
            file_paths=file_paths
        )

    @classmethod
    def create_method_blueprint(
        cls,
        relationship_map: RelationshipMap,
        json_mirrors: JSONMirrors,
        components: Dict[str, List[str]],
        name: Optional[str] = None,
        detail_level: DetailLevel = DetailLevel.STANDARD,
    ) -> MethodBasedBlueprint:
        """Create a method-based blueprint."""

        return cls.create_blueprint(
            "MethodBasedBlueprint",
            relationship_map,
            json_mirrors,
            name=name,
            detail_level=detail_level,
            components=components,
        )
