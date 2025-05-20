"""
Tests for the detail level module.
"""

import pytest
from arch_blueprint_generator.models.detail_level import DetailLevel, DetailLevelConfig


class TestDetailLevel:
    """Tests for the DetailLevel enum."""
    
    def test_values(self):
        """Test that the enum has the expected values."""
        assert DetailLevel.MINIMAL.value == "minimal"
        assert DetailLevel.STANDARD.value == "standard"
        assert DetailLevel.DETAILED.value == "detailed"
    
    def test_from_string_valid(self):
        """Test converting valid strings to DetailLevel enum values."""
        assert DetailLevel.from_string("minimal") == DetailLevel.MINIMAL
        assert DetailLevel.from_string("standard") == DetailLevel.STANDARD
        assert DetailLevel.from_string("detailed") == DetailLevel.DETAILED
        
        # Test case insensitivity and whitespace handling
        assert DetailLevel.from_string("MINIMAL") == DetailLevel.MINIMAL
        assert DetailLevel.from_string(" standard ") == DetailLevel.STANDARD
        assert DetailLevel.from_string("DETAILED") == DetailLevel.DETAILED
    
    def test_from_string_invalid(self):
        """Test that invalid strings raise ValueError."""
        with pytest.raises(ValueError):
            DetailLevel.from_string("invalid")
        
        with pytest.raises(ValueError):
            DetailLevel.from_string("")


class TestDetailLevelConfig:
    """Tests for the DetailLevelConfig class."""
    
    def test_init_defaults(self):
        """Test initialization with default values."""
        config = DetailLevelConfig()
        assert config.relationship_map == DetailLevel.STANDARD
        assert config.json_mirrors == DetailLevel.STANDARD
    
    def test_init_custom(self):
        """Test initialization with custom values."""
        config = DetailLevelConfig(
            relationship_map=DetailLevel.MINIMAL,
            json_mirrors=DetailLevel.DETAILED
        )
        assert config.relationship_map == DetailLevel.MINIMAL
        assert config.json_mirrors == DetailLevel.DETAILED
    
    def test_to_dict(self):
        """Test converting config to dictionary."""
        config = DetailLevelConfig(
            relationship_map=DetailLevel.MINIMAL,
            json_mirrors=DetailLevel.DETAILED
        )
        data = config.to_dict()
        assert data["relationship_map"] == "minimal"
        assert data["json_mirrors"] == "detailed"
    
    def test_from_dict(self):
        """Test creating config from dictionary."""
        data = {"relationship_map": "minimal", "json_mirrors": "detailed"}
        config = DetailLevelConfig.from_dict(data)
        assert config.relationship_map == DetailLevel.MINIMAL
        assert config.json_mirrors == DetailLevel.DETAILED
    
    def test_from_dict_defaults(self):
        """Test creating config from dictionary with missing values."""
        data = {}
        config = DetailLevelConfig.from_dict(data)
        assert config.relationship_map == DetailLevel.STANDARD
        assert config.json_mirrors == DetailLevel.STANDARD
        
        data = {"relationship_map": "minimal"}
        config = DetailLevelConfig.from_dict(data)
        assert config.relationship_map == DetailLevel.MINIMAL
        assert config.json_mirrors == DetailLevel.STANDARD
    
    def test_uniform(self):
        """Test creating config with uniform detail level."""
        config = DetailLevelConfig.uniform(DetailLevel.MINIMAL)
        assert config.relationship_map == DetailLevel.MINIMAL
        assert config.json_mirrors == DetailLevel.MINIMAL
        
        config = DetailLevelConfig.uniform(DetailLevel.DETAILED)
        assert config.relationship_map == DetailLevel.DETAILED
        assert config.json_mirrors == DetailLevel.DETAILED
