"""
Tests for the blueprint factory.
"""

import pytest
from unittest.mock import MagicMock

from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors
from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.blueprints.base import Blueprint
from arch_blueprint_generator.blueprints.file_based import FileBasedBlueprint
from arch_blueprint_generator.blueprints.factory import BlueprintFactory
from arch_blueprint_generator.errors.exceptions import BlueprintError


class TestBlueprintFactory:
    """Tests for the BlueprintFactory class."""
    
    @pytest.fixture
    def relationship_map(self):
        """Create a mock relationship map."""
        return MagicMock(spec=RelationshipMap)
    
    @pytest.fixture
    def json_mirrors(self):
        """Create a mock JSON mirrors."""
        return MagicMock(spec=JSONMirrors)
    
    def test_register_blueprint_type(self):
        """Test registering a new blueprint type."""
        # Create a test blueprint class
        class TestBlueprint(Blueprint):
            def generate(self):
                pass
        
        # Register the test blueprint type
        BlueprintFactory.register_blueprint_type("TestBlueprint", TestBlueprint)
        
        # Check that it was registered
        assert "TestBlueprint" in BlueprintFactory._blueprint_types
        assert BlueprintFactory._blueprint_types["TestBlueprint"] is TestBlueprint
    
    def test_register_blueprint_type_already_registered(self):
        """Test registering a blueprint type that is already registered."""
        with pytest.raises(BlueprintError):
            BlueprintFactory.register_blueprint_type("FileBasedBlueprint", FileBasedBlueprint)
    
    def test_create_blueprint(self, relationship_map, json_mirrors):
        """Test creating a blueprint of a specific type."""
        blueprint = BlueprintFactory.create_blueprint(
            "FileBasedBlueprint",
            relationship_map,
            json_mirrors,
            file_paths=["test.py"]
        )
        
        assert isinstance(blueprint, FileBasedBlueprint)
        assert blueprint.relationship_map is relationship_map
        assert blueprint.json_mirrors is json_mirrors
        assert len(blueprint.file_paths) == 1
        assert blueprint.file_paths[0].endswith("test.py")
    
    def test_create_blueprint_without_blueprint_suffix(self, relationship_map, json_mirrors):
        """Test creating a blueprint without 'Blueprint' suffix."""
        blueprint = BlueprintFactory.create_blueprint(
            "FileBased",
            relationship_map,
            json_mirrors,
            file_paths=["test.py"]
        )
        
        assert isinstance(blueprint, FileBasedBlueprint)
    
    def test_create_blueprint_unknown_type(self, relationship_map, json_mirrors):
        """Test creating a blueprint with an unknown type."""
        with pytest.raises(BlueprintError):
            BlueprintFactory.create_blueprint(
                "UnknownBlueprint",
                relationship_map,
                json_mirrors
            )
    
    def test_create_blueprint_missing_argument(self, relationship_map, json_mirrors):
        """Test creating a blueprint with a missing required argument."""
        with pytest.raises(BlueprintError):
            # FileBasedBlueprint requires file_paths
            BlueprintFactory.create_blueprint(
                "FileBasedBlueprint",
                relationship_map,
                json_mirrors
            )
    
    def test_create_file_blueprint(self, relationship_map, json_mirrors):
        """Test creating a file-based blueprint."""
        blueprint = BlueprintFactory.create_file_blueprint(
            relationship_map,
            json_mirrors,
            ["test.py"],
            "Test Blueprint",
            DetailLevel.DETAILED
        )
        
        assert isinstance(blueprint, FileBasedBlueprint)
        assert blueprint.relationship_map is relationship_map
        assert blueprint.json_mirrors is json_mirrors
        assert len(blueprint.file_paths) == 1
        assert blueprint.file_paths[0].endswith("test.py")
        assert blueprint.name == "Test Blueprint"
        assert blueprint.detail_level == DetailLevel.DETAILED
