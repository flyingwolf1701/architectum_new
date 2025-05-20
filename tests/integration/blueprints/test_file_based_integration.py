"""
Integration tests for file-based blueprint generation.
"""

import pytest
import os
import tempfile
import json

from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors
from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.scanner.path_scanner import PathScanner
from arch_blueprint_generator.blueprints.factory import BlueprintFactory


class TestFileBasedBlueprintIntegration:
    """Integration tests for file-based blueprint generation."""
    
    @pytest.fixture
    def test_directory(self):
        """Create a temporary test directory with files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            file1_path = os.path.join(temp_dir, "file1.py")
            file2_path = os.path.join(temp_dir, "file2.py")
            
            with open(file1_path, 'w', encoding='utf-8') as f:
                f.write("""
def test_function(value: str) -> bool:
    \"\"\"
    Test function that returns a boolean.
    
    Args:
        value: Value to test
        
    Returns:
        True if value is 'test', False otherwise
    \"\"\"
    return value == 'test'
""")
            
            with open(file2_path, 'w', encoding='utf-8') as f:
                f.write("""
class TestClass:
    \"\"\"
    Test class with a method.
    \"\"\"
    
    def __init__(self, value: str):
        \"\"\"
        Initialize with a value.
        
        Args:
            value: Value to store
        \"\"\"
        self.value = value
    
    def test_method(self) -> bool:
        \"\"\"
        Test method that returns a boolean.
        
        Returns:
            True if stored value is 'test', False otherwise
        \"\"\"
        return self.value == 'test'
""")
            
            yield temp_dir
    
    def test_file_based_blueprint_generation(self, test_directory):
        """Test generating a file-based blueprint from real files."""
        # Create a Python parser to extract functions and classes
        from arch_blueprint_generator.models.nodes import FunctionNode, ClassNode, ContainsRelationship
        
        # Scan directory to create representations
        scanner = PathScanner(test_directory)
        relationship_map, json_mirrors = scanner.scan()
        
        # Get the file paths
        file_paths = [
            os.path.join(test_directory, "file1.py"),
            os.path.join(test_directory, "file2.py")
        ]
        
        # Manually add function and class nodes to the relationship map
        # since the basic scanner doesn't parse Python files
        file1_node_id = f"file:{file_paths[0]}"
        func_node_id = f"func:{file_paths[0]}:test_function"
        func_node = FunctionNode(
            func_node_id,
            "test_function",
            parameters=[{"name": "value", "type": {"name": "str"}}],
            return_type={"name": "bool"},
            line_start=2,
            line_end=11
        )
        relationship_map.add_node(func_node)
        relationship_map.add_relationship(ContainsRelationship(file1_node_id, func_node_id))
        
        file2_node_id = f"file:{file_paths[1]}"
        class_node_id = f"class:{file_paths[1]}:TestClass"
        class_node = ClassNode(
            class_node_id,
            "TestClass",
            properties=[{"name": "value", "type": {"name": "str"}}],
            line_start=2,
            line_end=21
        )
        relationship_map.add_node(class_node)
        relationship_map.add_relationship(ContainsRelationship(file2_node_id, class_node_id))
        
        # Create a file-based blueprint
        blueprint = BlueprintFactory.create_file_blueprint(
            relationship_map,
            json_mirrors,
            file_paths,
            "Test Blueprint"
        )
        
        # Generate the blueprint
        blueprint.generate()
        
        # Verify the blueprint content
        assert "files" in blueprint.content
        assert len(blueprint.content["files"]) == 2
        
        # Check file entries
        for file_entry in blueprint.content["files"]:
            assert file_entry["path"] in file_paths
            assert file_entry["extension"] == ".py"
            assert "elements" in file_entry
        
        # Check first file elements
        file1_entry = next(f for f in blueprint.content["files"] if f["path"] == file_paths[0])
        assert any(e["name"] == "test_function" for e in file1_entry["elements"])
        
        # Check second file elements
        file2_entry = next(f for f in blueprint.content["files"] if f["path"] == file_paths[1])
        assert any(e["name"] == "TestClass" for e in file2_entry["elements"])
        
        # Check that relationships are included
        assert "relationships" in blueprint.content
    
    def test_file_based_blueprint_detail_levels(self, test_directory):
        """Test that detail level properly controls blueprint content."""
        # Create nodes with different levels of metadata
        from arch_blueprint_generator.models.nodes import FunctionNode, ContainsRelationship
        
        # Scan directory to create representations
        scanner = PathScanner(test_directory)
        relationship_map, json_mirrors = scanner.scan()
        
        # Get file path
        file_path = os.path.join(test_directory, "file1.py")
        
        # Add function node with detailed metadata
        file_node_id = f"file:{file_path}"
        func_node_id = f"func:{file_path}:test_function"
        func_node = FunctionNode(
            func_node_id,
            "test_function",
            parameters=[{"name": "value", "type": {"name": "str"}}],
            return_type={"name": "bool"},
            line_start=2,
            line_end=11,
            metadata={
                "doc": "Test function that returns a boolean.",
                "complexity": "O(1)",
                "author": "Test Author",
                "created_date": "2025-05-20",
                "some_extra_data": "This will only appear in detailed level"
            }
        )
        relationship_map.add_node(func_node)
        relationship_map.add_relationship(ContainsRelationship(file_node_id, func_node_id))
        
        # Also update the JSON mirror with detailed information
        from arch_blueprint_generator.models.json_mirrors import CodeElement
        elements = {
            "test_function": CodeElement(
                "test_function",
                "function",
                2, 11,
                {
                    "doc": "Test function that returns a boolean.",
                    "parameters": [{"name": "value", "type": "str"}],
                    "return_type": "bool",
                    "complexity": "O(1)",
                    "author": "Test Author",
                    "created_date": "2025-05-20"
                }
            )
        }
        json_mirrors.create_file_mirror(file_path, elements, [])
        
        # Create and generate blueprints with different detail levels
        minimal_blueprint = BlueprintFactory.create_file_blueprint(
            relationship_map,
            json_mirrors,
            [file_path],
            detail_level=DetailLevel.MINIMAL
        )
        minimal_blueprint.generate()
        
        standard_blueprint = BlueprintFactory.create_file_blueprint(
            relationship_map,
            json_mirrors,
            [file_path],
            detail_level=DetailLevel.STANDARD
        )
        standard_blueprint.generate()
        
        detailed_blueprint = BlueprintFactory.create_file_blueprint(
            relationship_map,
            json_mirrors,
            [file_path],
            detail_level=DetailLevel.DETAILED
        )
        detailed_blueprint.generate()
        
        # Convert to JSON for easy comparison
        minimal_json = json.dumps(minimal_blueprint.to_json())
        standard_json = json.dumps(standard_blueprint.to_json())
        detailed_json = json.dumps(detailed_blueprint.to_json())
        
        # Verify that minimal has fewer details than standard, which has fewer than detailed
        assert len(minimal_json) <= len(standard_json) <= len(detailed_json)
        
        # Check specific elements in minimal blueprint
        minimal_file = minimal_blueprint.content["files"][0]
        if "elements" in minimal_file and minimal_file["elements"]:
            for element in minimal_file["elements"]:
                assert "metadata" not in element
        
        # Check specific elements in detailed blueprint
        detailed_file = detailed_blueprint.content["files"][0]
        if "elements" in detailed_file and detailed_file["elements"]:
            has_metadata = False
            for element in detailed_file["elements"]:
                if "metadata" in element:
                    has_metadata = True
                    break
            assert has_metadata
    
    def test_file_based_blueprint_output_formats(self, test_directory, tmp_path):
        """Test generating blueprints in different output formats."""
        # Scan directory to create representations
        scanner = PathScanner(test_directory)
        relationship_map, json_mirrors = scanner.scan()
        
        # Get file path
        file_path = os.path.join(test_directory, "file1.py")
        
        # Create a file-based blueprint
        blueprint = BlueprintFactory.create_file_blueprint(
            relationship_map,
            json_mirrors,
            [file_path]
        )
        blueprint.generate()
        
        # Save in JSON format
        json_path = os.path.join(tmp_path, "blueprint.json")
        blueprint.save(json_path, "json")
        
        # Save in XML format
        xml_path = os.path.join(tmp_path, "blueprint.xml")
        blueprint.save(xml_path, "xml")
        
        # Verify files exist and have appropriate formats
        assert os.path.exists(json_path)
        with open(json_path, 'r', encoding='utf-8') as f:
            json_content = f.read()
            assert json_content.startswith("{")
            assert '"name":' in json_content
            assert '"type":' in json_content
            assert '"content":' in json_content
        
        assert os.path.exists(xml_path)
        with open(xml_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
            assert xml_content.startswith('<?xml')
            assert '<Blueprint' in xml_content
            assert '<Content>' in xml_content
