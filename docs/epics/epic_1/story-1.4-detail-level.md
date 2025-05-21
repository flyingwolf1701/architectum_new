# Story 1.4: Implement Detail Level Configuration for Representations

## Status: Completed

## Story

- As an AI agent or developer
- I want to configure the detail level of the representations
- So that I can control the balance between comprehensiveness and efficiency for different use cases

## Acceptance Criteria (ACs)

- AC1: ✅ Detail level configuration can be specified for both representations independently.
- AC2: ✅ The Minimal detail level produces streamlined representations for efficiency.
- AC3: ✅ The Standard detail level includes type information and signatures.
- AC4: ✅ The Detailed detail level includes comprehensive information including documentation.
- AC5: ✅ Detail level settings are correctly applied during representation generation.
- AC6: ✅ Testing Requirements:
  - Coverage: At least 80% code coverage for the detail level configuration functionality
  - Framework: Implementation using pytest with parameterized tests for detail levels
  - Snapshot Testing: Create snapshots comparing representations at different detail levels
  - Contract Testing: Verify outputs at different detail levels meet schema requirements
  - Performance Testing: Measure representation size and generation time at different detail levels
  - Configuration Testing: Test application of different detail level combinations

## Tasks / Subtasks

- [x] Define detail level models and configuration system (AC: 1)
  - [x] Create a DetailLevel enum with Minimal, Standard, and Detailed options
  - [x] Implement a configuration class to store detail level settings
  - [x] Create methods to set detail levels for each representation independently
  - [x] Implement configuration validation to ensure valid detail level settings

- [x] Implement detail level for Relationship Map (AC: 1, 2, 3, 4, 5)
  - [x] Implement Minimal detail level (basic structure and primary relationships)
  - [x] Implement Standard detail level (enhanced metadata and secondary relationships)
  - [x] Implement Detailed detail level (comprehensive metadata and full relationship network)
  - [x] Create a strategy for applying detail level during graph traversal and access
  - [x] Implement filtering mechanism to limit information based on detail level

- [x] Implement detail level for JSON Mirrors (AC: 1, 2, 3, 4, 5)
  - [x] Implement Minimal detail level (basic file structure and element signatures)
  - [x] Implement Standard detail level (type information and interface details)
  - [x] Implement Detailed detail level (documentation and implementation insights)
  - [x] Create methods to retrieve JSON content at specified detail level
  - [x] Ensure consistency between JSON mirror detail levels

- [x] Create integration points for detail level configuration (AC: 1, 5)
  - [x] Update path scan functionality to accept detail level configuration
  - [x] Modify parsing logic to extract information based on detail level
  - [x] Ensure synchronization respects detail level settings
  - [x] Implement detail level propagation through the system

- [x] Develop comprehensive testing suite (AC: 6)
  - [x] Create unit tests for configuration system with parametrized test cases
  - [x] Implement snapshot tests to compare outputs at different detail levels
  - [x] Create contract tests to verify schema compliance at each detail level
  - [x] Implement performance benchmarks for different detail levels
  - [x] Test handling of mixed detail level configurations
  - [x] Generate test coverage report to ensure 80% minimum coverage

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

## Story Progress Notes

### Agent Model Used: `Claude 3.7 Sonnet`

### Completion Notes List
- Implemented the DetailLevel enum with MINIMAL, STANDARD, and DETAILED options
- Created a DetailLevelConfig class to manage settings for both representations
- Enhanced RelationshipMap with detail level filtering for nodes and relationships
- Extended JSONMirrors to support different detail levels for content retrieval
- Updated PathScanner to apply detail level settings during scanning
- Modified CLI commands to support detail level parameters
- Created comprehensive unit tests for detail level functionality
- Implemented integration tests for detail level across the system
- Added performance comparison tests for different detail levels
- Updated epic1_features.yaml with new components and functionality

### QA Testing Guide

To verify the Detail Level Configuration functionality:

1. **Unit Testing**:
   - Run unit tests for detail level models: 
     ```
     cd /d D:\Coding\2025\architectum_new && .venv\Scripts\python.exe -m pytest tests/unit/models/test_detail_level.py -v
     ```
   - Run tests for relationship map with detail level:
     ```
     cd /d D:\Coding\2025\architectum_new && .venv\Scripts\python.exe -m pytest tests/unit/models/test_relationship_map_detail_level.py -v
     ```
   - Run tests for JSON mirrors with detail level:
     ```
     cd /d D:\Coding\2025\architectum_new && .venv\Scripts\python.exe -m pytest tests/unit/models/test_json_mirrors_detail_level.py -v
     ```

2. **Integration Testing**:
   - Run integration tests for path scanner with detail level:
     ```
     cd /d D:\Coding\2025\architectum_new && .venv\Scripts\python.exe -m pytest tests/integration/scanner/test_path_scanner_detail_level.py -v
     ```

3. **CLI Testing**:
   - Test the scan command with different detail levels:
     ```
     cd /d D:\Coding\2025\architectum_new && .venv\Scripts\python.exe -m arch_blueprint_generator.cli.commands scan . --detail-level minimal
     ```
     Compare with:
     ```
     cd /d D:\Coding\2025\architectum_new && .venv\Scripts\python.exe -m arch_blueprint_generator.cli.commands scan . --detail-level detailed
     ```

4. **Check Test Coverage**:
   - Ensure code coverage meets requirements:
     ```
     cd /d D:\Coding\2025\architectum_new && .venv\Scripts\python.exe -m pytest --cov=arch_blueprint_generator.models.detail_level --cov-report=term
     ```
   - Coverage should be at least 80%

5. **Verify Manual Behavior**:
   - Check that the minimal detail level significantly reduces the amount of data included
   - Verify that standard includes essential information for common tasks
   - Confirm that detailed includes all information available

## Change Log
- 2025-05-20: Initial implementation of DetailLevel and DetailLevelConfig classes
- 2025-05-20: Added detail level support to RelationshipMap
- 2025-05-20: Added detail level support to JSONMirrors
- 2025-05-20: Updated PathScanner to support detail level configuration
- 2025-05-20: Updated CLI commands to accept detail level parameters
- 2025-05-20: Created comprehensive test suite for detail level functionality
- 2025-05-20: Updated epic1_features.yaml with detail level components
- 2025-05-20: Marked story as completed with all acceptance criteria met