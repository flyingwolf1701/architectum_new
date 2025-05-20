"""
Tests for the path scanner module.
"""

import os
import tempfile
import shutil
import pytest
from pathlib import Path

from arch_blueprint_generator.scanner.path_scanner import PathScanner
from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors
from arch_blueprint_generator.models.nodes import NodeType, RelationshipType
from arch_blueprint_generator.errors.exceptions import FileError


class TestPathScanner:
    """Tests for the PathScanner class."""
    
    @pytest.fixture
    def test_directory(self):
        """Create a temporary directory with files and subdirectories for testing."""
        temp_dir = tempfile.mkdtemp()
        
        # Create structure:
        # temp_dir/
        #   ├── file1.txt
        #   ├── file2.py
        #   ├── subdir1/
        #   │   ├── subfile1.txt
        #   │   └── subfile2.py
        #   └── subdir2/
        #       └── subsubdir/
        #           └── deep_file.txt
        
        # Create files in root
        with open(os.path.join(temp_dir, "file1.txt"), "w") as f:
            f.write("Test file 1")
        with open(os.path.join(temp_dir, "file2.py"), "w") as f:
            f.write("print('Test file 2')")
        
        # Create subdir1 and its files
        subdir1 = os.path.join(temp_dir, "subdir1")
        os.makedirs(subdir1)
        with open(os.path.join(subdir1, "subfile1.txt"), "w") as f:
            f.write("Test subfile 1")
        with open(os.path.join(subdir1, "subfile2.py"), "w") as f:
            f.write("print('Test subfile 2')")
        
        # Create subdir2 and its nested directory
        subdir2 = os.path.join(temp_dir, "subdir2")
        subsubdir = os.path.join(subdir2, "subsubdir")
        os.makedirs(subsubdir)
        with open(os.path.join(subsubdir, "deep_file.txt"), "w") as f:
            f.write("Test deep file")
        
        # Create excluded directory
        excluded_dir = os.path.join(temp_dir, "__pycache__")
        os.makedirs(excluded_dir)
        with open(os.path.join(excluded_dir, "excluded_file.py"), "w") as f:
            f.write("print('This should be excluded')")
        
        yield temp_dir
        
        # Cleanup after test
        shutil.rmtree(temp_dir)
    
    def test_init(self, test_directory):
        """Test initialization of PathScanner."""
        scanner = PathScanner(test_directory)
        
        assert scanner.root_path == os.path.abspath(test_directory)
        assert isinstance(scanner.relationship_map, RelationshipMap)
        assert isinstance(scanner.json_mirrors, JSONMirrors)
        assert "__pycache__" in scanner.exclude_patterns
    
    def test_init_invalid_path(self):
        """Test initialization with invalid path."""
        with pytest.raises(FileError):
            PathScanner("non_existent_path")
    
    def test_init_not_directory(self, test_directory):
        """Test initialization with a path that is not a directory."""
        file_path = os.path.join(test_directory, "file1.txt")
        with pytest.raises(FileError):
            PathScanner(file_path)
    
    def test_scan_unlimited_depth(self, test_directory):
        """Test scanning with unlimited depth."""
        scanner = PathScanner(test_directory)
        relationship_map, json_mirrors = scanner.scan()
        
        # Verify root node was created
        root_node_id = f"dir:{os.path.abspath(test_directory)}"
        root_node = relationship_map.get_node(root_node_id)
        assert root_node is not None
        
        # Verify all files and directories were found
        # Should be: 1 root dir + 2 subdirs + 1 subsubdir + 2 root files + 2 subfiles + a deep file
        # Total: 4 directories + 5 files = 9 nodes (excluding excluded directories/files)
        
        # Count nodes
        dir_nodes = relationship_map.get_nodes_by_type(NodeType.DIRECTORY)
        file_nodes = relationship_map.get_nodes_by_type(NodeType.FILE)
        
        assert len(dir_nodes) == 4  # root, subdir1, subdir2, subsubdir
        assert len(file_nodes) == 5  # file1.txt, file2.py, subfile1.txt, subfile2.py, deep_file.txt
        
        # Verify contains relationships (including transitivity)
        contains_rels = relationship_map.get_relationships_by_type(RelationshipType.CONTAINS)
        assert len(contains_rels) == 9  # Each node except the root has a container
        
        # Verify excluded files/dirs were not included
        excluded_path = os.path.join(test_directory, "__pycache__")
        excluded_node_id = f"dir:{excluded_path}"
        assert relationship_map.get_node(excluded_node_id) is None
        
        # Verify JSON mirrors for all items
        mirror_paths = json_mirrors.list_all_mirrors()
        assert len(mirror_paths) == 9  # All nodes should have mirrors
    
    def test_scan_depth_1(self, test_directory):
        """Test scanning with depth 1 (immediate files and directories only)."""
        scanner = PathScanner(test_directory)
        relationship_map, json_mirrors = scanner.scan(max_depth=1)
        
        # Verify nodes
        dir_nodes = relationship_map.get_nodes_by_type(NodeType.DIRECTORY)
        file_nodes = relationship_map.get_nodes_by_type(NodeType.FILE)
        
        # At depth 1, should find root + subdir1 + subdir2 + file1.txt + file2.py = 5 nodes
        assert len(dir_nodes) == 3  # root, subdir1, subdir2
        assert len(file_nodes) == 2  # file1.txt, file2.py
        
        # Verify subsubdir was not included
        subsubdir_path = os.path.join(test_directory, "subdir2", "subsubdir")
        subsubdir_node_id = f"dir:{subsubdir_path}"
        assert relationship_map.get_node(subsubdir_node_id) is None
        
        # Verify deep file was not included
        deep_file_path = os.path.join(subsubdir_path, "deep_file.txt")
        deep_file_node_id = f"file:{deep_file_path}"
        assert relationship_map.get_node(deep_file_node_id) is None
    
    def test_scan_is_binary_file(self, test_directory):
        """Test binary file detection."""
        # Create a binary file
        binary_path = os.path.join(test_directory, "binary_file.bin")
        with open(binary_path, "wb") as f:
            f.write(bytes([0x00, 0x01, 0x02, 0x03, 0xFF, 0xFE, 0xFD, 0xFC]))
        
        # Test the method
        assert PathScanner.is_binary_file(binary_path) is True
        
        # Test with a text file
        text_path = os.path.join(test_directory, "file1.txt")
        assert PathScanner.is_binary_file(text_path) is False
    
    def test_scan_with_custom_exclude(self, test_directory):
        """Test scanning with custom exclude patterns."""
        # Create a custom directory that would normally be included
        custom_dir = os.path.join(test_directory, "custom_dir")
        os.makedirs(custom_dir)
        with open(os.path.join(custom_dir, "custom_file.txt"), "w") as f:
            f.write("Custom file")
        
        # Scan with custom exclusion pattern
        scanner = PathScanner(test_directory, exclude_patterns=["custom_dir", "__pycache__"])
        relationship_map, _ = scanner.scan()
        
        # Verify custom directory was excluded
        custom_node_id = f"dir:{custom_dir}"
        assert relationship_map.get_node(custom_node_id) is None
        
        # But subdir1 should still be included
        subdir1_path = os.path.join(test_directory, "subdir1")
        subdir1_node_id = f"dir:{subdir1_path}"
        assert relationship_map.get_node(subdir1_node_id) is not None
