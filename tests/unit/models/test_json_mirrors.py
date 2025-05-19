"""
Tests for the JSON mirrors model.
"""

import os
import pytest
import tempfile
import json
import shutil
from pathlib import Path

from arch_blueprint_generator.models.json_mirrors import (
    JSONMirrors, FileContent, DirectoryContent, CodeElement
)
from arch_blueprint_generator.errors.exceptions import FileError, ModelError


class TestCodeElement:
    """Tests for the CodeElement class."""
    
    def test_init(self):
        """Test initialization of a code element."""
        element = CodeElement("my_function", "function", 10, 20, {"key": "value"})
        
        assert element.name == "my_function"
        assert element.type == "function"
        assert element.line_start == 10
        assert element.line_end == 20
        assert element.metadata == {"key": "value"}
    
    def test_to_json(self):
        """Test converting a code element to JSON."""
        element = CodeElement("my_function", "function", 10, 20, {"key": "value"})
        
        json_data = element.to_json()
        
        assert json_data["name"] == "my_function"
        assert json_data["type"] == "function"
        assert json_data["line_start"] == 10
        assert json_data["line_end"] == 20
        assert json_data["metadata"] == {"key": "value"}
    
    def test_from_json(self):
        """Test creating a code element from JSON."""
        json_data = {
            "name": "my_function",
            "type": "function",
            "line_start": 10,
            "line_end": 20,
            "metadata": {"key": "value"}
        }
        
        element = CodeElement.from_json(json_data)
        
        assert element.name == "my_function"
        assert element.type == "function"
        assert element.line_start == 10
        assert element.line_end == 20
        assert element.metadata == {"key": "value"}


class TestFileContent:
    """Tests for the FileContent class."""
    
    def test_init(self):
        """Test initialization of a file content object."""
        element = CodeElement("my_function", "function", 10, 20)
        elements = {"my_function": element}
        imports = ["path/to/imported.py"]
        
        file_content = FileContent(
            "path/to/file.py", 
            ".py", 
            elements, 
            imports, 
            "hash123"
        )
        
        assert file_content.path == "path/to/file.py"
        assert file_content.extension == ".py"
        assert file_content.elements == elements
        assert file_content.imports == imports
        assert file_content.source_hash == "hash123"
    
    def test_add_element(self):
        """Test adding an element to a file content object."""
        file_content = FileContent("path/to/file.py", ".py")
        element = CodeElement("my_function", "function", 10, 20)
        
        file_content.add_element(element)
        
        assert "my_function" in file_content.elements
        assert file_content.elements["my_function"] == element
        
        # Test adding an element with the same name raises an error
        with pytest.raises(ModelError):
            file_content.add_element(element)
    
    def test_to_json(self):
        """Test converting a file content object to JSON."""
        element = CodeElement("my_function", "function", 10, 20)
        elements = {"my_function": element}
        imports = ["path/to/imported.py"]
        
        file_content = FileContent(
            "path/to/file.py", 
            ".py", 
            elements, 
            imports, 
            "hash123"
        )
        
        json_data = file_content.to_json()
        
        assert json_data["path"] == "path/to/file.py"
        assert json_data["extension"] == ".py"
        assert "my_function" in json_data["elements"]
        assert json_data["imports"] == imports
        assert json_data["source_hash"] == "hash123"
