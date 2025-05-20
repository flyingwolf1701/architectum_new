"""
Integration tests for PathScanner with detail level support.
"""

import pytest
import os
import tempfile
import shutil
import json

from arch_blueprint_generator.scanner.path_scanner import PathScanner
from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.models.nodes import NodeType, FileNode
from arch_blueprint_generator.models.json_mirrors import FileContent


class TestPathScannerDetailLevel:
    """Integration tests for PathScanner with detail level support."""
    
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
            f.write("def test_function():\n    return 'test'")
        
        # Create subdir1 and its files
        subdir1 = os.path.join(temp_dir, "subdir1")
        os.makedirs(subdir1)
        with open(os.path.join(subdir1, "subfile1.txt"), "w") as f:
            f.write("Test subfile 1")
        with open(os.path.join(subdir1, "subfile2.py"), "w") as f:
            f.write("class TestClass:\n    def test_method(self):\n        return 'test'")
        
        # Create subdir2 and its nested directory
        subdir2 = os.path.join(temp_dir, "subdir2")
        subsubdir = os.path.join(subdir2, "subsubdir")
        os.makedirs(subsubdir)
        with open(os.path.join(subsubdir, "deep_file.txt"), "w") as f:
            f.write("Test deep file")
        
        yield temp_dir
        
        # Cleanup after test
        shutil.rmtree(temp_dir)
    
    def test_scan_with_minimal_detail_level(self, test_directory):
        """Test scanning with minimal detail level."""
        # Create and run scanner with minimal detail level
        scanner = PathScanner(test_directory)
        relationship_map, json_mirrors = scanner.scan(detail_level=DetailLevel.MINIMAL)
        
        # Check that nodes were created
        assert relationship_map.node_count() > 0
        assert relationship_map.relationship_count() > 0
        
        # Check that file nodes were created with minimal detail
        file_node_ids = [node.id for node in relationship_map.get_nodes_by_type(NodeType.FILE)]
        assert len(file_node_ids) > 0
        
        # Select a file node and check its detail level
        file_node = relationship_map.get_node(file_node_ids[0])
        assert file_node.metadata == {}  # Minimal detail should have empty metadata
        
        # Check that mirrors were created
        mirror_paths = json_mirrors.list_all_mirrors()
        assert len(mirror_paths) > 0
        
        # Get a mirrored file content and check its detail level
        for path in mirror_paths:
            content = json_mirrors.get_mirrored_content(path)
            if isinstance(content, FileContent):
                # In minimal detail, elements and imports should be empty
                assert len(content.elements) == 0
                assert len(content.imports) == 0
                break
    
    def test_scan_with_detailed_detail_level(self, test_directory):
        """Test scanning with detailed detail level."""
        # Create and run scanner with detailed detail level
        scanner = PathScanner(test_directory)
        relationship_map, json_mirrors = scanner.scan(detail_level=DetailLevel.DETAILED)
        
        # Check that nodes were created
        assert relationship_map.node_count() > 0
        assert relationship_map.relationship_count() > 0
        
        # Get a JSON representation of the relationship map
        json_data = relationship_map.to_json()
        
        # Check that detail level is included
        assert "detail_level" in json_data
        assert json_data["detail_level"] == "detailed"
        
        # For now, we're just testing that the scan completes successfully
        # In a real test, we would check specific details of the generated representations
    
    def test_scan_serialization_with_different_detail_levels(self, test_directory, tmp_path):
        """Test serializing scanned data with different detail levels."""
        # Create scanner
        scanner = PathScanner(test_directory)
        
        # Scan with minimal detail level
        relationship_map_minimal, _ = scanner.scan(detail_level=DetailLevel.MINIMAL)
        
        # Scan with detailed detail level
        relationship_map_detailed, _ = scanner.scan(detail_level=DetailLevel.DETAILED)
        
        # Serialize both maps to JSON
        json_minimal = relationship_map_minimal.to_json()
        json_detailed = relationship_map_detailed.to_json()
        
        # Check that both have the correct detail level
        assert json_minimal["detail_level"] == "minimal"
        assert json_detailed["detail_level"] == "detailed"
        
        # Check that minimal JSON is smaller than detailed JSON
        minimal_size = len(json.dumps(json_minimal))
        detailed_size = len(json.dumps(json_detailed))
        assert minimal_size < detailed_size, "Minimal detail level should result in smaller JSON"