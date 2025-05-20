"""
Detail level configuration for representations.

This module defines the detail level options and configuration for controlling
the granularity of information in both the Relationship Map and JSON Mirrors
representations.
"""

from enum import Enum
from typing import Dict, Optional, Any
from dataclasses import dataclass


class DetailLevel(Enum):
    """Detail level options for controlling information granularity."""
    MINIMAL = "minimal"
    STANDARD = "standard"
    DETAILED = "detailed"
    
    @classmethod
    def from_string(cls, value: str) -> "DetailLevel":
        """
        Convert string to DetailLevel enum.
        
        Args:
            value: String representation of detail level
            
        Returns:
            DetailLevel enum value
            
        Raises:
            ValueError: If the string is not a valid detail level
        """
        normalized = value.lower().strip()
        for level in cls:
            if level.value == normalized:
                return level
        raise ValueError(f"Invalid detail level: {value}. Valid options are: {[l.value for l in cls]}")


@dataclass
class DetailLevelConfig:
    """Configuration for detail levels across different representations."""
    relationship_map: DetailLevel = DetailLevel.STANDARD
    json_mirrors: DetailLevel = DetailLevel.STANDARD
    
    def to_dict(self) -> Dict[str, str]:
        """
        Convert config to dictionary for serialization.
        
        Returns:
            Dictionary representation of the configuration
        """
        return {
            "relationship_map": self.relationship_map.value,
            "json_mirrors": self.json_mirrors.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "DetailLevelConfig":
        """
        Create config from dictionary.
        
        Args:
            data: Dictionary representation of the configuration
            
        Returns:
            DetailLevelConfig instance
        """
        return cls(
            relationship_map=DetailLevel.from_string(data.get("relationship_map", "standard")),
            json_mirrors=DetailLevel.from_string(data.get("json_mirrors", "standard"))
        )
    
    @classmethod
    def uniform(cls, detail_level: DetailLevel) -> "DetailLevelConfig":
        """
        Create a config with the same detail level for all representations.
        
        Args:
            detail_level: Detail level to use for all representations
            
        Returns:
            DetailLevelConfig instance with uniform detail level
        """
        return cls(
            relationship_map=detail_level,
            json_mirrors=detail_level
        )
