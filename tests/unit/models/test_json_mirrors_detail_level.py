"""
Tests for JSON mirrors detail level filtering.
"""

import pytest
import os
import tempfile
import shutil
import json

from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.models.json_mirrors import (
    JSONMirrors, CodeElement, FileContent, DirectoryContent
)


class TestJSONMirrorsDetailLevel:
    """Tests for JSONMirrors detail level filtering."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def json_mirrors(self, temp_dir):
        """Create a JSON mirrors container for testing."""
        root_path = os.path.join(temp_dir, "root")
        mirror_path = os.path.join(temp_dir, "mirrors")
        
        os.makedirs(root_path, exist_ok=True)
        
        return JSONMirrors(root_path, mirror_path)
    
    def setup_test_elements(self):
        """Create test code elements with various detail levels."""
        # Create a function element with detailed metadata
        function_element = CodeElement(
            "test_function",
            "function",
            10, 20,
            {
                "visibility": "public",
                "return_type": "bool",
                "parameters": [
                    {"name": "param1", "type": "int", "default_value": "0"},
                    {"name": "param2", "type": "str", "default_value": None}
                ],
                "doc_summary": "This is a test function",
                "doc_details": "More detailed documentation here...",
                "complexity": "O(n)",
                "author": "Test User",
                "created_date": "2023-01-01"
            }
        )
        
        # Create a class element with detailed metadata
        class_element = CodeElement(
            "TestClass",
            "class",
            30, 50,
            {
                "visibility": "public",
                "properties": [
                    {"name": "prop1", "type": "int", "visibility": "public"},
                    {"name": "prop2", "type": "str", "visibility": "private"}
                ],
                "methods": ["method1", "method2"],
                "doc_summary": "This is a test class",
                "doc_details": "More detailed documentation here...",
                "author": "Test User",
                "created_date": "2023-01-01"
            }
        )
        
        return {
            "test_function": function_element,
            "TestClass": class_element
        }
    
    def test_code_element_to_json_minimal(self):
        """Test serializing a code element with minimal detail level."""
        elements = self.setup_test_elements()
        function_element = elements["test_function"]
        
        # Get JSON with minimal detail
        json_data = function_element.to_json(DetailLevel.MINIMAL)
        
        # Check that only essential fields are included
        assert json_data["name"] == "test_function"
        assert json_data["type"] == "function"
        assert json_data["line_start"] == 10
        assert json_data["line_end"] == 20
        assert "metadata" not in json_data
    
    def test_code_element_to_json_standard(self):
        """Test serializing a code element with standard detail level."""
        elements = self.setup_test_elements()
        function_element = elements["test_function"]
        
        # Get JSON with standard detail
        json_data = function_element.to_json(DetailLevel.STANDARD)
        
        # Check that essential fields and basic metadata are included
        assert json_data["name"] == "test_function"
        assert json_data["type"] == "function"
        assert json_data["line_start"] == 10
        assert json_data["line_end"] == 20
        assert "metadata" in json_data
        
        # Check that specific metadata fields are included
        metadata = json_data["metadata"]
        assert "visibility" in metadata
        assert "return_type" in metadata
        assert "parameters" in metadata
        assert "doc_summary" in metadata
        
        # Check that detailed metadata is not included
        assert "doc_details" not in metadata
        assert "complexity" not in metadata
        assert "author" not in metadata
        assert "created_date" not in metadata
    
    def test_code_element_to_json_detailed(self):
        """Test serializing a code element with detailed detail level."""
        elements = self.setup_test_elements()
        function_element = elements["test_function"]
        
        # Get JSON with detailed detail
        json_data = function_element.to_json(DetailLevel.DETAILED)
        
        # Check that all fields are included
        assert json_data["name"] == "test_function"
        assert json_data["type"] == "function"
        assert json_data["line_start"] == 10
        assert json_data["line_end"] == 20
        assert "metadata" in json_data
        
        # Check that all metadata fields are included
        metadata = json_data["metadata"]
        assert "visibility" in metadata
        assert "return_type" in metadata
        assert "parameters" in metadata
        assert "doc_summary" in metadata
        assert "doc_details" in metadata
        assert "complexity" in metadata
        assert "author" in metadata
        assert "created_date" in metadata
    
    def test_file_content_to_json_minimal(self, temp_dir):
        """Test serializing file content with minimal detail level."""
        elements = self.setup_test_elements()
        
        # Create a file content object
        file_path = os.path.join(temp_dir, "test_file.py")
        file_content = FileContent(
            file_path,
            ".py",
            elements,
            ["import1.py", "import2.py"],
            "hash123"
        )
        
        # Get JSON with minimal detail
        json_data = file_content.to_json(DetailLevel.MINIMAL)
        
        # Check that only essential fields are included
        assert json_data["path"] == file_path
        assert json_data["extension"] == ".py"
        assert "element_count" in json_data
        assert json_data["element_count"] == 2
        assert "import_count" in json_data
        assert json_data["import_count"] == 2
        
        # Check that elements and imports are not included
        assert "elements" not in json_data
        assert "imports" not in json_data
        assert "source_hash" not in json_data
    
    def test_file_content_to_json_standard(self, temp_dir):
        """Test serializing file content with standard detail level."""
        elements = self.setup_test_elements()
        
        # Create a file content object
        file_path = os.path.join(temp_dir, "test_file.py")
        file_content = FileContent(
            file_path,
            ".py",
            elements,
            ["import1.py", "import2.py"],
            "hash123"
        )
        
        # Get JSON with standard detail
        json_data = file_content.to_json(DetailLevel.STANDARD)
        
        # Check that essential fields and imports are included
        assert json_data["path"] == file_path
        assert json_data["extension"] == ".py"
        assert "elements" in json_data
        assert "imports" in json_data
        assert json_data["imports"] == ["import1.py", "import2.py"]
        assert "source_hash" in json_data
        assert json_data["source_hash"] == "hash123"
        
        # Check that elements are serialized with standard detail
        for name, element_data in json_data["elements"].items():
            assert "metadata" in element_data
            metadata = element_data["metadata"]
            
            # Standard fields should be included
            if name == "test_function":
                assert "visibility" in metadata
                assert "return_type" in metadata
                assert "parameters" in metadata
                assert "doc_summary" in metadata
                
                # Detailed fields should not be included
                assert "doc_details" not in metadata
                assert "complexity" not in metadata
    
    def test_file_content_to_json_detailed(self, temp_dir):
        """Test serializing file content with detailed detail level."""
        elements = self.setup_test_elements()
        
        # Create a file content object
        file_path = os.path.join(temp_dir, "test_file.py")
        file_content = FileContent(
            file_path,
            ".py",
            elements,
            ["import1.py", "import2.py"],
            "hash123"
        )
        
        # Get JSON with detailed detail
        json_data = file_content.to_json(DetailLevel.DETAILED)
        
        # Check that all fields are included
        assert json_data["path"] == file_path
        assert json_data["extension"] == ".py"
        assert "elements" in json_data
        assert "imports" in json_data
        assert json_data["imports"] == ["import1.py", "import2.py"]
        assert "source_hash" in json_data
        assert json_data["source_hash"] == "hash123"
        assert "detail_level" in json_data
        assert json_data["detail_level"] == "detailed"
        
        # Check that elements are serialized with detailed detail
        for name, element_data in json_data["elements"].items():
            assert "metadata" in element_data
            metadata = element_data["metadata"]
            
            # All metadata fields should be included
            if name == "test_function":
                assert "visibility" in metadata
                assert "return_type" in metadata
                assert "parameters" in metadata
                assert "doc_summary" in metadata
                assert "doc_details" in metadata
                assert "complexity" in metadata
                assert "author" in metadata
                assert "created_date" in metadata
    
    def test_directory_content_to_json_minimal(self, temp_dir):
        """Test serializing directory content with minimal detail level."""
        # Create a directory content object
        dir_path = os.path.join(temp_dir, "test_dir")
        dir_content = DirectoryContent(
            dir_path,
            ["file1.py", "file2.py"],
            ["subdir1", "subdir2"]
        )
        
        # Get JSON with minimal detail
        json_data = dir_content.to_json(DetailLevel.MINIMAL)
        
        # Check that only essential fields are included
        assert json_data["path"] == dir_path
        assert "file_count" in json_data
        assert json_data["file_count"] == 2
        assert "subdirectory_count" in json_data
        assert json_data["subdirectory_count"] == 2
        
        # Check that files and subdirectories are not included
        assert "files" not in json_data
        assert "subdirectories" not in json_data
    
    def test_directory_content_to_json_standard(self, temp_dir):
        """Test serializing directory content with standard detail level."""
        # Create a directory content object
        dir_path = os.path.join(temp_dir, "test_dir")
        dir_content = DirectoryContent(
            dir_path,
            ["file1.py", "file2.py"],
            ["subdir1", "subdir2"]
        )
        
        # Get JSON with standard detail
        json_data = dir_content.to_json(DetailLevel.STANDARD)
        
        # Check that all fields are included
        assert json_data["path"] == dir_path
        assert "files" in json_data
        assert json_data["files"] == ["file1.py", "file2.py"]
        assert "subdirectories" in json_data
        assert json_data["subdirectories"] == ["subdir1", "subdir2"]
    
    def test_directory_content_to_json_detailed(self, temp_dir):
        """Test serializing directory content with detailed detail level."""
        # Create a directory content object
        dir_path = os.path.join(temp_dir, "test_dir")
        dir_content = DirectoryContent(
            dir_path,
            ["file1.py", "file2.py"],
            ["subdir1", "subdir2"]
        )
        
        # Get JSON with detailed detail (should be same as standard)
        json_data = dir_content.to_json(DetailLevel.DETAILED)
        
        # Check that all fields are included
        assert json_data["path"] == dir_path
        assert "files" in json_data
        assert json_data["files"] == ["file1.py", "file2.py"]
        assert "subdirectories" in json_data
        assert json_data["subdirectories"] == ["subdir1", "subdir2"]
    
    def test_get_mirrored_content_with_detail_levels(self, json_mirrors, temp_dir):
        """Test getting mirrored content with different detail levels."""
        # Setup a test file and content in the mirrors
        elements = self.setup_test_elements()
        source_path = os.path.join(temp_dir, "root", "test_file.py")
        
        # Create the file
        os.makedirs(os.path.dirname(source_path), exist_ok=True)
        with open(source_path, 'w', encoding='utf-8') as f:
            f.write("def test_function():\n    return True")
        
        # Create mirror with detailed detail level
        json_mirrors.create_file_mirror(
            source_path,
            elements,
            ["import1.py", "import2.py"],
            DetailLevel.DETAILED
        )
        
        # Get content with minimal detail level
        content = json_mirrors.get_mirrored_content(source_path, DetailLevel.MINIMAL)
        
        # Check that it's a FileContent object
        assert isinstance(content, FileContent)
        
        # Check that it has expected characteristics of minimal detail level
        assert content.path == source_path
        assert content.extension == ".py"
        assert len(content.elements) == 0  # Should be empty in minimal detail
        assert len(content.imports) == 0  # Should be empty in minimal detail
        
        # Check that source_hash is preserved for up-to-date checks
        assert content.source_hash is not None
        
        # Get content with detailed detail level
        content = json_mirrors.get_mirrored_content(source_path, DetailLevel.DETAILED)
        
        # Check that it's a FileContent object with full detail
        assert isinstance(content, FileContent)
        assert content.path == source_path
        assert content.extension == ".py"
        assert len(content.elements) == 2  # Should have all elements
        assert len(content.imports) == 2  # Should have all imports
        assert "test_function" in content.elements
        assert "TestClass" in content.elements
    
    def test_update_mirrored_content_with_detail_levels(self, json_mirrors, temp_dir):
        """Test updating mirrored content with different detail levels."""
        # Setup a test file and content
        elements = self.setup_test_elements()
        source_path = os.path.join(temp_dir, "root", "test_file.py")
        
        # Create the file
        os.makedirs(os.path.dirname(source_path), exist_ok=True)
        with open(source_path, 'w', encoding='utf-8') as f:
            f.write("def test_function():\n    return True")
        
        # Create a file content object
        file_content = FileContent(
            source_path,
            ".py",
            elements,
            ["import1.py", "import2.py"],
            "hash123"
        )
        
        # Update with minimal detail level
        json_mirrors.update_mirrored_content(source_path, file_content, DetailLevel.MINIMAL)
        
        # Get the content and verify it's minimal
        mirror_path = json_mirrors.get_mirror_path(source_path)
        with open(mirror_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check that it follows minimal format
        assert "element_count" in data
        assert data["element_count"] == 2
        assert "elements" not in data
