"""
Simple test to verify detail level imports and basic functionality.
"""

from arch_blueprint_generator.models.detail_level import DetailLevel, DetailLevelConfig
from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors


def test_detail_level_imports():
    """Test that detail level imports work correctly."""
    # Create a detail level config
    config = DetailLevelConfig(
        relationship_map=DetailLevel.MINIMAL,
        json_mirrors=DetailLevel.DETAILED
    )
    
    # Verify config values
    assert config.relationship_map == DetailLevel.MINIMAL
    assert config.json_mirrors == DetailLevel.DETAILED
    
    # Test uniform config creation
    uniform_config = DetailLevelConfig.uniform(DetailLevel.STANDARD)
    assert uniform_config.relationship_map == DetailLevel.STANDARD
    assert uniform_config.json_mirrors == DetailLevel.STANDARD
    
    # Test to_dict and from_dict
    config_dict = config.to_dict()
    assert config_dict["relationship_map"] == "minimal"
    assert config_dict["json_mirrors"] == "detailed"
    
    # Test string conversion
    assert DetailLevel.from_string("minimal") == DetailLevel.MINIMAL
    assert DetailLevel.from_string("STANDARD") == DetailLevel.STANDARD
    assert DetailLevel.from_string(" detailed ") == DetailLevel.DETAILED
