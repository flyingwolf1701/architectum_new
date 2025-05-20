"""
Tests for the change tracker module.
"""

import os
import pytest
import tempfile
import shutil
import time
from pathlib import Path

from arch_blueprint_generator.sync.change_tracker import ChangeTracker
from arch_blueprint_generator.models.json_mirrors import JSONMirrors


class TestChangeTracker:
    """Tests for the ChangeTracker class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def json_mirrors(self, temp_dir):
        """Create a JSONMirrors instance for testing."""
        root_path = os.path.join(temp_dir, "root")
        mirror_path = os.path.join(temp_dir, "mirrors")
        
        os.makedirs(root_path, exist_ok=True)
        
        return JSONMirrors(root_path, mirror_path)
    
    @pytest.fixture
    def change_tracker(self, json_mirrors):
        """Create a ChangeTracker instance for testing."""
        return ChangeTracker(json_mirrors)
    
    @pytest.fixture
    def test_files(self, temp_dir, json_mirrors):
        """Create test files for testing."""
        root_path = os.path.join(temp_dir, "root")
        os.makedirs(root_path, exist_ok=True)
        
        # Create a file structure for testing
        file1_path = os.path.join(root_path, "file1.txt")
        file2_path = os.path.join(root_path, "file2.py")
        
        subdir_path = os.path.join(root_path, "subdir")
        os.makedirs(subdir_path, exist_ok=True)
        
        subfile_path = os.path.join(subdir_path, "subfile.txt")
        
        # Write content to files
        with open(file1_path, 'w', encoding='utf-8') as f:
            f.write("File 1 content")
        
        with open(file2_path, 'w', encoding='utf-8') as f:
            f.write("File 2 content")
        
        with open(subfile_path, 'w', encoding='utf-8') as f:
            f.write("Subfile content")
        
        # Create mirrors for the files
        json_mirrors.create_file_mirror(file1_path, {}, [])
        json_mirrors.create_file_mirror(file2_path, {}, [])
        json_mirrors.create_file_mirror(subfile_path, {}, [])
        
        # Create mirror for the directory
        json_mirrors.create_directory_mirror(
            subdir_path,
            [subfile_path],
            []
        )
        
        return {
            "root": root_path,
            "file1": file1_path,
            "file2": file2_path,
            "subdir": subdir_path,
            "subfile": subfile_path
        }
    
    def test_detect_changes_no_changes(self, change_tracker, test_files):
        """Test detecting changes when no files have changed."""
        modified, new, deleted = change_tracker.detect_changes([test_files["root"]])
        
        assert len(modified) == 0
        assert len(new) == 0
        assert len(deleted) == 0
    
    def test_detect_changes_modified_file(self, change_tracker, test_files):
        """Test detecting a modified file."""
        # Modify file1
        with open(test_files["file1"], 'w', encoding='utf-8') as f:
            f.write("Modified file 1 content")
        
        # Wait a moment to ensure file system timestamp changes
        time.sleep(0.1)
        
        modified, new, deleted = change_tracker.detect_changes([test_files["file1"]])
        
        assert len(modified) == 1
        assert test_files["file1"] in modified
        assert len(new) == 0
        assert len(deleted) == 0
    
    def test_detect_changes_new_file(self, change_tracker, test_files):
        """Test detecting a new file."""
        # Create a new file
        new_file_path = os.path.join(test_files["root"], "new_file.txt")
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write("New file content")
        
        modified, new, deleted = change_tracker.detect_changes([test_files["root"]])
        
        assert len(modified) == 0
        assert len(new) == 1
        assert new_file_path in new
        assert len(deleted) == 0
    
    def test_detect_changes_deleted_file(self, change_tracker, test_files):
        """Test detecting a deleted file."""
        # Delete file2
        os.remove(test_files["file2"])
        
        modified, new, deleted = change_tracker.detect_changes([test_files["root"]])
        
        assert len(modified) == 0
        assert len(new) == 0
        assert len(deleted) == 1
        assert test_files["file2"] in deleted
    
    def test_detect_changes_multiple(self, change_tracker, test_files):
        """Test detecting multiple types of changes."""
        # Modify file1
        with open(test_files["file1"], 'w', encoding='utf-8') as f:
            f.write("Modified file 1 content")
        
        # Create a new file
        new_file_path = os.path.join(test_files["root"], "new_file.txt")
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write("New file content")
        
        # Delete file2
        os.remove(test_files["file2"])
        
        # Wait a moment to ensure file system timestamp changes
        time.sleep(0.1)
        
        modified, new, deleted = change_tracker.detect_changes([test_files["root"]])
        
        assert len(modified) == 1
        assert test_files["file1"] in modified
        assert len(new) == 1
        assert new_file_path in new
        assert len(deleted) == 1
        assert test_files["file2"] in deleted
    
    def test_is_within_paths(self, change_tracker, test_files):
        """Test checking if a file is within specified paths."""
        # File is within its own path
        assert change_tracker._is_within_paths(
            test_files["file1"],
            [test_files["file1"]]
        ) is True
        
        # File is within parent directory path
        assert change_tracker._is_within_paths(
            test_files["file1"],
            [test_files["root"]]
        ) is True
        
        # File is not within unrelated path
        assert change_tracker._is_within_paths(
            test_files["file1"],
            [test_files["subdir"]]
        ) is False
        
        # File is within one of multiple paths
        assert change_tracker._is_within_paths(
            test_files["file1"],
            [test_files["subdir"], test_files["root"]]
        ) is True
