"""
Tests for the blueprint base class.
"""

import pytest
import os
from unittest.mock import MagicMock

from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors
from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.blueprints.base import Blueprint
from arch_blueprint_generator.errors.exceptions import BlueprintError


# Create a concrete subclass for testing
class TestBlueprint(Blueprint):
    """Concrete Blueprint subclass for testing."""
    __test__ = False  # Prevent pytest from collecting this class as tests
    
    def __init__(
        self,
        relationship_map: RelationshipMap,
        json_mirrors: JSONMirrors,
        name: str = None,
        detail_level: DetailLevel = DetailLevel.STANDARD
    ):
        super().__init__(relationship_map, json_mirrors, name, detail_level)
    
    def generate(self) -> None:
        """Test implementation of generate method."""
        self.content = {
            "test": "content",
            "number": 42,
            "nested": {
                "key": "value"
            }
        }


class TestBlueprintBase:
    """Tests for the Blueprint base class."""
    
    @pytest.fixture
    def relationship_map(self):
        """Create a mock relationship map."""
        return MagicMock(spec=RelationshipMap)
    
    @pytest.fixture
    def json_mirrors(self):
        """Create a mock JSON mirrors."""
        return MagicMock(spec=JSONMirrors)
    
    @pytest.fixture
    def blueprint(self, relationship_map, json_mirrors):
        """Create a test blueprint."""
        return TestBlueprint(relationship_map, json_mirrors, "Test Blueprint")
    
    def test_init(self, relationship_map, json_mirrors):
        """Test initialization of a blueprint."""
        # Test with all parameters
        blueprint = TestBlueprint(
            relationship_map,
            json_mirrors,
            "Test Blueprint",
            DetailLevel.DETAILED
        )
        
        assert blueprint.relationship_map is relationship_map
        assert blueprint.json_mirrors is json_mirrors
        assert blueprint.name == "Test Blueprint"
        assert blueprint.detail_level == DetailLevel.DETAILED
        assert blueprint.content == {}
        
        # Test with default parameters
        blueprint = TestBlueprint(relationship_map, json_mirrors)
        
        assert blueprint.name == "TestBlueprint"
        assert blueprint.detail_level == DetailLevel.STANDARD
    
    def test_init_invalid_relationship_map(self, json_mirrors):
        """Test initialization with invalid relationship map."""
        with pytest.raises(BlueprintError):
            TestBlueprint("not a relationship map", json_mirrors)
    
    def test_init_invalid_json_mirrors(self, relationship_map):
        """Test initialization with invalid JSON mirrors."""
        with pytest.raises(BlueprintError):
            TestBlueprint(relationship_map, "not json mirrors")
    
    def test_generate(self, blueprint):
        """Test generating a blueprint."""
        assert blueprint.content == {}
        
        blueprint.generate()
        
        assert blueprint.content == {
            "test": "content",
            "number": 42,
            "nested": {
                "key": "value"
            }
        }
    
    def test_to_json_without_generate(self, blueprint):
        """Test to_json without generating first."""
        with pytest.raises(BlueprintError):
            blueprint.to_json()
    
    def test_to_json(self, blueprint):
        """Test converting a blueprint to JSON."""
        blueprint.generate()
        json_data = blueprint.to_json()
        
        assert json_data["name"] == "Test Blueprint"
        assert json_data["type"] == "TestBlueprint"
        assert json_data["detail_level"] == "standard"
        assert json_data["content"] == {
            "test": "content",
            "number": 42,
            "nested": {
                "key": "value"
            }
        }
    
    def test_to_xml_without_generate(self, blueprint):
        """Test to_xml without generating first."""
        with pytest.raises(BlueprintError):
            blueprint.to_xml()
    
    def test_to_xml(self, blueprint):
        """Test converting a blueprint to XML."""
        blueprint.generate()
        xml_data = blueprint.to_xml()
        
        assert '<?xml version="1.0" ?>' in xml_data
        assert 'Blueprint name="Test Blueprint"' in xml_data
        assert 'type="TestBlueprint"' in xml_data
        assert 'detailLevel="standard"' in xml_data
        assert '<Content>' in xml_data
        assert '<test>content</test>' in xml_data
        assert '<number>42</number>' in xml_data
        assert '<nested>' in xml_data
        assert '<key>value</key>' in xml_data
    
    def test_save_without_generate(self, blueprint, tmp_path):
        """Test saving a blueprint without generating first."""
        output_path = os.path.join(tmp_path, "blueprint.json")
        
        with pytest.raises(BlueprintError):
            blueprint.save(output_path)
    
    def test_save_json(self, blueprint, tmp_path):
        """Test saving a blueprint as JSON."""
        output_path = os.path.join(tmp_path, "blueprint.json")
        
        blueprint.generate()
        blueprint.save(output_path, "json")
        
        assert os.path.exists(output_path)
        
        # Verify file content
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Test Blueprint" in content
            assert "TestBlueprint" in content
            assert "standard" in content
            assert "content" in content
    
    def test_save_xml(self, blueprint, tmp_path):
        """Test saving a blueprint as XML."""
        output_path = os.path.join(tmp_path, "blueprint.xml")
        
        blueprint.generate()
        blueprint.save(output_path, "xml")
        
        assert os.path.exists(output_path)
        
        # Verify file content
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert '<?xml version="1.0" ?>' in content
            assert 'Blueprint name="Test Blueprint"' in content
            assert 'type="TestBlueprint"' in content
            assert '<test>content</test>' in content
    
    def test_load(self, relationship_map, json_mirrors, tmp_path):
        """Test loading a blueprint from a file."""
        # Create a FileBasedBlueprint instead of TestBlueprint
        from arch_blueprint_generator.blueprints.file_based import FileBasedBlueprint
        
        # Create a blueprint with a simple file path
        test_blueprint = FileBasedBlueprint(
            relationship_map,
            json_mirrors,
            ["test.py"],
            "Test Blueprint"
        )
        test_blueprint.content = {"test": "content"}
        
        # Save the blueprint to a file
        output_path = os.path.join(tmp_path, "blueprint.json")
        test_blueprint.save(output_path, "json")
        
        # Load the blueprint
        loaded_blueprint = Blueprint.load(output_path, relationship_map, json_mirrors)
        
        # Verify the loaded blueprint
        assert loaded_blueprint.name == test_blueprint.name
        assert loaded_blueprint.detail_level == test_blueprint.detail_level
        assert loaded_blueprint.content == test_blueprint.content
