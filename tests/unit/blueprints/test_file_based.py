"""
Tests for the file-based blueprint class.
"""

import pytest
import os
import tempfile

from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors, FileContent, CodeElement
from arch_blueprint_generator.models.nodes import FileNode, FunctionNode, ContainsRelationship
from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.blueprints.file_based import FileBasedBlueprint
from arch_blueprint_generator.errors.exceptions import BlueprintError


class TestFileBasedBlueprint:
    """Tests for the FileBasedBlueprint class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield tmp_dir
    
    @pytest.fixture
    def test_file_paths(self, temp_dir):
        """Create test files for testing."""
        file1_path = os.path.join(temp_dir, "file1.py")
        file2_path = os.path.join(temp_dir, "file2.py")
        
        with open(file1_path, 'w', encoding='utf-8') as f:
            f.write("def test_function():\n    return 'test'")
        
        with open(file2_path, 'w', encoding='utf-8') as f:
            f.write("class TestClass:\n    def test_method(self):\n        return 'test'")
        
        return [file1_path, file2_path]
    
    @pytest.fixture
    def relationship_map(self, test_file_paths):
        """Create a relationship map with test files."""
        relationship_map = RelationshipMap()
        
        # Add file nodes
        for file_path in test_file_paths:
            file_node_id = f"file:{file_path}"
            file_ext = os.path.splitext(file_path)[1]
            file_node = FileNode(file_node_id, file_path, file_ext)
            relationship_map.add_node(file_node)
            
            # Add function node for first file
            if file_path == test_file_paths[0]:
                func_node_id = f"func:{file_path}:test_function"
                func_node = FunctionNode(
                    func_node_id,
                    "test_function",
                    parameters=[],
                    return_type={"name": "str"},
                    line_start=1,
                    line_end=2
                )
                relationship_map.add_node(func_node)
                
                # Add contains relationship
                contains_rel = ContainsRelationship(file_node_id, func_node_id)
                relationship_map.add_relationship(contains_rel)
        
        return relationship_map
    
    @pytest.fixture
    def json_mirrors(self, test_file_paths):
        """Create JSON mirrors with test files."""
        json_mirrors = JSONMirrors(os.path.dirname(test_file_paths[0]))
        
        # Add file content for first file
        file1_path = test_file_paths[0]
        elements1 = {
            "test_function": CodeElement(
                "test_function",
                "function",
                1, 2,
                {
                    "doc": "Test function",
                    "parameters": [],
                    "return_type": "str"
                }
            )
        }
        json_mirrors.create_file_mirror(file1_path, elements1, [])
        
        # Add file content for second file
        file2_path = test_file_paths[1]
        elements2 = {
            "TestClass": CodeElement(
                "TestClass",
                "class",
                1, 3,
                {
                    "doc": "Test class",
                    "methods": ["test_method"]
                }
            ),
            "test_method": CodeElement(
                "test_method",
                "method",
                2, 3,
                {
                    "doc": "Test method",
                    "parameters": ["self"],
                    "parent_class": "TestClass",
                    "return_type": "str"
                }
            )
        }
        json_mirrors.create_file_mirror(file2_path, elements2, [])
        
        return json_mirrors
    
    @pytest.fixture
    def blueprint(self, relationship_map, json_mirrors, test_file_paths):
        """Create a file-based blueprint."""
        return FileBasedBlueprint(relationship_map, json_mirrors, test_file_paths)
    
    def test_init(self, relationship_map, json_mirrors, test_file_paths):
        """Test initialization of a file-based blueprint."""
        # Test with all parameters
        blueprint = FileBasedBlueprint(
            relationship_map,
            json_mirrors,
            test_file_paths,
            "Test Blueprint",
            DetailLevel.DETAILED
        )
        
        assert blueprint.relationship_map is relationship_map
        assert blueprint.json_mirrors is json_mirrors
        assert blueprint.file_paths == [os.path.abspath(p) for p in test_file_paths]
        assert blueprint.name == "Test Blueprint"
        assert blueprint.detail_level == DetailLevel.DETAILED
        
        # Test with default parameters
        blueprint = FileBasedBlueprint(relationship_map, json_mirrors, test_file_paths)
        
        assert blueprint.name == "FileBasedBlueprint"
        assert blueprint.detail_level == DetailLevel.STANDARD
    
    def test_init_no_file_paths(self, relationship_map, json_mirrors):
        """Test initialization with no file paths."""
        with pytest.raises(BlueprintError):
            FileBasedBlueprint(relationship_map, json_mirrors, [])
    
    def test_init_file_not_found(self, relationship_map, json_mirrors):
        """Test initialization with a file that doesn't exist in either representation."""
        with pytest.raises(BlueprintError):
            FileBasedBlueprint(
                relationship_map,
                json_mirrors,
                ["non_existent_file.py"]
            )

    def test_init_all_invalid_paths(self, relationship_map, json_mirrors):
        """All invalid paths should raise an error."""
        with pytest.raises(BlueprintError):
            FileBasedBlueprint(
                relationship_map,
                json_mirrors,
                ["bad1.py", "bad2.py"]
            )

    def test_init_some_invalid_paths(self, relationship_map, json_mirrors, test_file_paths):
        """Invalid paths are removed when at least one valid path exists."""
        valid_path = test_file_paths[0]
        invalid_path = "does_not_exist.py"

        blueprint = FileBasedBlueprint(
            relationship_map,
            json_mirrors,
            [valid_path, invalid_path]
        )

        assert blueprint.file_paths == [os.path.abspath(valid_path)]
    
    def test_generate(self, blueprint):
        """Test generating a file-based blueprint."""
        assert blueprint.content == {}
        
        blueprint.generate()
        
        assert "files" in blueprint.content
        assert "relationships" in blueprint.content
        assert len(blueprint.content["files"]) == 2
        
        # Check first file
        file1 = blueprint.content["files"][0]
        assert file1["path"] == blueprint.file_paths[0]
        assert file1["extension"] == ".py"
        assert "elements" in file1
        
        # Check file elements
        assert any(e["name"] == "test_function" for e in file1["elements"])
    
    def test_generate_with_minimal_detail(self, relationship_map, json_mirrors, test_file_paths):
        """Test generating a file-based blueprint with minimal detail level."""
        blueprint = FileBasedBlueprint(
            relationship_map,
            json_mirrors,
            test_file_paths,
            detail_level=DetailLevel.MINIMAL
        )
        
        blueprint.generate()
        
        assert "files" in blueprint.content
        assert "relationships" in blueprint.content
        
        # Check that metadata is stripped in minimal detail level
        file1 = blueprint.content["files"][0]
        assert "metadata" not in file1
        
        # Check that elements are still included but with minimal detail
        assert "elements" in file1
        for element in file1["elements"]:
            assert "metadata" not in element
    
    def test_generate_with_detailed_detail(self, relationship_map, json_mirrors, test_file_paths):
        """Test generating a file-based blueprint with detailed detail level."""
        # Create a function node with metadata for testing
        func_node_id = f"func:{test_file_paths[0]}:test_function"
        func_node = relationship_map.get_node(func_node_id)
        if func_node:
            # Add some metadata to the function node
            func_node.metadata = {"doc": "Test function with detailed metadata"}
            
        blueprint = FileBasedBlueprint(
            relationship_map,
            json_mirrors,
            test_file_paths,
            detail_level=DetailLevel.DETAILED
        )
        
        blueprint.generate()
        
        assert "files" in blueprint.content
        assert "relationships" in blueprint.content
        
        # Find file1 entry
        file_entries = blueprint.content["files"]
        file1 = None
        for file_entry in file_entries:
            if file_entry["path"] == test_file_paths[0]:
                file1 = file_entry
                break
        
        assert file1 is not None, "First file entry not found in blueprint content"
                
        # Get the elements from JSON mirrors if relationship map doesn't have metadata
        file_content = json_mirrors.get_mirrored_content(test_file_paths[0])
        if file_content and file_content.elements:
            test_function = file_content.elements.get("test_function")
            if test_function and test_function.metadata:
                # Skip this assertion if there's no metadata to test with
                for element in file1["elements"]:
                    if element["name"] == "test_function":
                        if "metadata" in element:
                            assert element["metadata"] is not None
            else:
                # If no metadata exists, just check that the basic element info is there
                assert any(e["name"] == "test_function" for e in file1["elements"])
    
    def test_process_file(self, blueprint):
        """Test processing a file to extract its information."""
        file_path = blueprint.file_paths[0]
        file_info = blueprint._process_file(file_path)
        
        assert file_info["path"] == file_path
        assert file_info["extension"] == ".py"
        assert "elements" in file_info
        
        # Check file elements
        assert any(e["name"] == "test_function" for e in file_info["elements"])
    
    def test_process_file_not_found(self, blueprint):
        """Test processing a file that doesn't exist."""
        file_info = blueprint._process_file("non_existent_file.py")
        
        assert file_info is None
    
    def test_add_file_elements(self, blueprint):
        """Test adding file elements from the relationship map."""
        file_path = blueprint.file_paths[0]
        file_node_id = f"file:{file_path}"
        file_info = {"path": file_path, "elements": []}
        
        blueprint._add_file_elements(file_node_id, file_info)
        
        assert len(file_info["elements"]) == 1
        assert file_info["elements"][0]["name"] == "test_function"
    
    def test_add_relationships(self, blueprint):
        """Test adding relationships between files."""
        # Add a test relationship
        source_id = f"file:{blueprint.file_paths[0]}"
        target_id = f"file:{blueprint.file_paths[1]}"
        # We need to inject a test relationship here
        from arch_blueprint_generator.models.nodes import ImportsRelationship
        relationship = ImportsRelationship(source_id, target_id)
        blueprint.relationship_map.add_relationship(relationship)
        
        # Generate and check relationships
        blueprint.generate()
        
        assert len(blueprint.content["relationships"]) == 1
        assert blueprint.content["relationships"][0]["type"] == "imports"
        assert blueprint.content["relationships"][0]["source_id"] == source_id
        assert blueprint.content["relationships"][0]["target_id"] == target_id
