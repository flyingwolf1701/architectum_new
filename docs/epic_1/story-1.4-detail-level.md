# Story 1.4: Implement Detail Level Configuration for Representations

## Status: Draft

## Story

- As an AI agent or developer
- I want to configure the detail level of the representations
- So that I can control the balance between comprehensiveness and efficiency for different use cases

## Acceptance Criteria (ACs)

- AC1: Detail level configuration can be specified for both representations independently.
- AC2: The Minimal detail level produces streamlined representations for efficiency.
- AC3: The Standard detail level includes type information and signatures.
- AC4: The Detailed detail level includes comprehensive information including documentation.
- AC5: Detail level settings are correctly applied during representation generation.
- AC6: Testing Requirements:
  - Coverage: At least 80% code coverage for the detail level configuration functionality
  - Framework: Implementation using pytest with parameterized tests for detail levels
  - Snapshot Testing: Create snapshots comparing representations at different detail levels
  - Contract Testing: Verify outputs at different detail levels meet schema requirements
  - Performance Testing: Measure representation size and generation time at different detail levels
  - Configuration Testing: Test application of different detail level combinations

## Tasks / Subtasks

- [ ] Define detail level models and configuration system (AC: 1)
  - [ ] Create a DetailLevel enum with Minimal, Standard, and Detailed options
  - [ ] Implement a configuration class to store detail level settings
  - [ ] Create methods to set detail levels for each representation independently
  - [ ] Implement configuration validation to ensure valid detail level settings

- [ ] Implement detail level for Relationship Map (AC: 1, 2, 3, 4, 5)
  - [ ] Implement Minimal detail level (basic structure and primary relationships)
  - [ ] Implement Standard detail level (enhanced metadata and secondary relationships)
  - [ ] Implement Detailed detail level (comprehensive metadata and full relationship network)
  - [ ] Create a strategy for applying detail level during graph traversal and access
  - [ ] Implement filtering mechanism to limit information based on detail level

- [ ] Implement detail level for JSON Mirrors (AC: 1, 2, 3, 4, 5)
  - [ ] Implement Minimal detail level (basic file structure and element signatures)
  - [ ] Implement Standard detail level (type information and interface details)
  - [ ] Implement Detailed detail level (documentation and implementation insights)
  - [ ] Create methods to retrieve JSON content at specified detail level
  - [ ] Ensure consistency between JSON mirror detail levels

- [ ] Create integration points for detail level configuration (AC: 1, 5)
  - [ ] Update path scan functionality to accept detail level configuration
  - [ ] Modify parsing logic to extract information based on detail level
  - [ ] Ensure synchronization respects detail level settings
  - [ ] Implement detail level propagation through the system

- [ ] Develop comprehensive testing suite (AC: 6)
  - [ ] Create unit tests for configuration system with parametrized test cases
  - [ ] Implement snapshot tests to compare outputs at different detail levels
  - [ ] Create contract tests to verify schema compliance at each detail level
  - [ ] Implement performance benchmarks for different detail levels
  - [ ] Test handling of mixed detail level configurations
  - [ ] Generate test coverage report to ensure 80% minimum coverage

## Dev Technical Guidance

### Detail Level Model Implementation

Implement the detail level as an enum to ensure consistency throughout the codebase:

```python
from enum import Enum
from typing import Dict, Optional, Any
from dataclasses import dataclass

class DetailLevel(Enum):
    MINIMAL = "minimal"
    STANDARD = "standard"
    DETAILED = "detailed"
    
    @classmethod
    def from_string(cls, value: str) -> "DetailLevel":
        """Convert string to DetailLevel enum."""
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
        """Convert config to dictionary for serialization."""
        return {
            "relationship_map": self.relationship_map.value,
            "json_mirrors": self.json_mirrors.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "DetailLevelConfig":
        """Create config from dictionary."""
        return cls(
            relationship_map=DetailLevel.from_string(data.get("relationship_map", "standard")),
            json_mirrors=DetailLevel.from_string(data.get("json_mirrors", "standard"))
        )
```

### Relationship Map Detail Level Implementation

For the Relationship Map, implement detail level filtering at both node and relationship levels:

```python
class RelationshipMap:
    # ... existing methods ...
    
    def get_node(self, node_id: str, detail_level: DetailLevel = DetailLevel.STANDARD) -> Optional[Node]:
        """
        Get a node by ID with the specified detail level.
        
        Args:
            node_id: The ID of the node to retrieve
            detail_level: The level of detail to include
            
        Returns:
            The node if found, None otherwise
        """
        node = self._get_raw_node(node_id)
        if node is None:
            return None
        
        return self._apply_detail_level_to_node(node, detail_level)
    
    def _apply_detail_level_to_node(self, node: Node, detail_level: DetailLevel) -> Node:
        """Apply detail level filtering to a node."""
        if detail_level == DetailLevel.MINIMAL:
            # Return minimal information (only essential fields)
            return self._create_minimal_node(node)
        elif detail_level == DetailLevel.STANDARD:
            # Return standard information (essential fields + type info)
            return self._create_standard_node(node)
        else:  # DetailLevel.DETAILED
            # Return all information
            return node.copy()
    
    # Similar methods for relationships and traversal...
```

### JSON Mirrors Detail Level Implementation

For JSON Mirrors, implement detail level filtering during content retrieval:

```python
class JSONMirrors:
    # ... existing methods ...
    
    def get_mirrored_content(
        self, 
        source_path: str, 
        detail_level: DetailLevel = DetailLevel.STANDARD
    ) -> Optional[Dict[str, Any]]:
        """
        Get the JSON representation of a source code file with the specified detail level.
        
        Args:
            source_path: Path to the source file
            detail_level: Level of detail to include
            
        Returns:
            JSON content if found, None otherwise
        """
        content = self._get_raw_content(source_path)
        if content is None:
            return None
        
        return self._apply_detail_level_to_content(content, detail_level)
    
    def _apply_detail_level_to_content(
        self, 
        content: Dict[str, Any], 
        detail_level: DetailLevel
    ) -> Dict[str, Any]:
        """Apply detail level filtering to JSON content."""
        if detail_level == DetailLevel.MINIMAL:
            # Return minimal information (file structure and signatures)
            return self._create_minimal_content(content)
        elif detail_level == DetailLevel.STANDARD:
            # Return standard information (structure, signatures, types)
            return self._create_standard_content(content)
        else:  # DetailLevel.DETAILED
            # Return all information including documentation
            return content.copy()
```

### Configuration Integration

Ensure the detail level configuration is integrated with the CLI and API:

```python
def parse_file(
    file_path: str, 
    detail_level_config: Optional[DetailLevelConfig] = None
) -> Tuple[List[Node], FileContent]:
    """
    Parse a file with the specified detail level configuration.
    
    Args:
        file_path: Path to the file to parse
        detail_level_config: Detail level configuration (default: all Standard)
        
    Returns:
        Tuple of (nodes, file_content)
    """
    if detail_level_config is None:
        detail_level_config = DetailLevelConfig()
    
    # Use the appropriate detail level for each representation
    relationship_detail = detail_level_config.relationship_map
    json_detail = detail_level_config.json_mirrors
    
    # Implementation details...
```

### Testing Strategy

Focus on comprehensive testing of detail level behaviors:

1. Create test fixtures with known content at different detail levels
2. Use parametrized tests to verify behavior across all detail levels
3. Implement snapshot tests to capture and verify expected outputs
4. Measure and benchmark performance characteristics
5. Verify schema compliance at each detail level

## Story Progress Notes

### Agent Model Used: `<Agent Model Name/Version>`

### Completion Notes List
{Not started yet}

### Change Log
- Initial story draft created by POSM

## QA Testing Guide

{This section should be completed when the story implementation is done and tests are passing. Include step-by-step instructions for how a human tester can verify the functionality works as expected. Include example inputs, expected outputs, and any edge cases that should be tested.}