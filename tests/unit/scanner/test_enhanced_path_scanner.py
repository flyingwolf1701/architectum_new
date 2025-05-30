"""
Unit tests for EnhancedPathScanner.
"""

import os
import tempfile
import shutil
import pytest
from unittest.mock import patch

from arch_blueprint_generator.scanner.enhanced_path_scanner import EnhancedPathScanner
from arch_blueprint_generator.models.detail_level import DetailLevel
from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors
from arch_blueprint_generator.models.nodes import NodeType
from arch_blueprint_generator.errors.exceptions import FileError


class TestEnhancedPathScanner:
    """Test cases for EnhancedPathScanner functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.setup_test_directory()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def setup_test_directory(self):
        """Create a test directory structure."""
        # Create directories
        os.makedirs(os.path.join(self.temp_dir, 'src'))
        os.makedirs(os.path.join(self.temp_dir, 'build'))
        os.makedirs(os.path.join(self.temp_dir, '__pycache__'))
        os.makedirs(os.path.join(self.temp_dir, 'tests'))
        
        # Create files
        test_files = ['src/main.py', 'src/utils.py', 'build/output.exe',
                     '__pycache__/main.cpython-39.pyc', 'tests/test_main.py',
                     'README.md', 'config.log', 'important.log']
        
        for file_path in test_files:
            full_path = os.path.join(self.temp_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(f'# Content of {file_path}\n')
    
    def test_scanner_initialization(self):
        """Test EnhancedPathScanner initialization."""
        scanner = EnhancedPathScanner(self.temp_dir)
        
        assert scanner.root_path == os.path.abspath(self.temp_dir)
        assert scanner.respect_gitignore is True
        assert scanner.exclude_patterns == [".git", ".venv", "__pycache__", ".architectum"]
        assert isinstance(scanner.relationship_map, RelationshipMap)
        assert isinstance(scanner.json_mirrors, JSONMirrors)
    
    def test_scanner_with_invalid_path(self):
        """Test scanner with invalid path."""
        with pytest.raises(FileError):
            EnhancedPathScanner('/nonexistent/path')
    
    def test_scanner_with_file_path(self):
        """Test scanner with file path instead of directory."""
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test content')
        
        with pytest.raises(FileError):
            EnhancedPathScanner(test_file)
    
    def test_scanner_with_gitignore_disabled(self):
        """Test scanner with gitignore disabled."""
        gitignore_path = os.path.join(self.temp_dir, '.gitignore')
        with open(gitignore_path, 'w') as f:
            f.write('*.log\n')
        
        scanner = EnhancedPathScanner(self.temp_dir, respect_gitignore=False)
        assert scanner.gitignore_parser is None
        assert not scanner.respect_gitignore
    
    def test_scanner_with_gitignore_enabled(self):
        """Test scanner with gitignore enabled."""
        gitignore_path = os.path.join(self.temp_dir, '.gitignore')
        with open(gitignore_path, 'w') as f:
            f.write('*.log\n')
            f.write('build/\n')
        
        scanner = EnhancedPathScanner(self.temp_dir, respect_gitignore=True)
        assert scanner.gitignore_parser is not None
        assert scanner.respect_gitignore
    
    def test_scanner_with_additional_ignores(self):
        """Test scanner with additional ignore patterns."""
        additional_ignores = ['*.tmp', '.DS_Store']
        scanner = EnhancedPathScanner(
            self.temp_dir, 
            additional_ignores=additional_ignores
        )
        
        # Should include both default and additional patterns
        assert '*.tmp' in scanner.exclude_patterns
        assert '.DS_Store' in scanner.exclude_patterns
        assert '.git' in scanner.exclude_patterns  # Default pattern
    
    def test_should_exclude_with_legacy_patterns(self):
        """Test exclusion with legacy exclude patterns."""
        scanner = EnhancedPathScanner(
            self.temp_dir,
            exclude_patterns=['test_', 'cache'],
            respect_gitignore=False
        )
        
        assert scanner._should_exclude('test_file.py')
        assert scanner._should_exclude('cache_dir')
        assert scanner._should_exclude('some_cache_file.txt')
        assert not scanner._should_exclude('main.py')
    
    def test_should_exclude_with_gitignore(self):
        """Test exclusion with gitignore patterns."""
        gitignore_path = os.path.join(self.temp_dir, '.gitignore')
        with open(gitignore_path, 'w') as f:
            f.write('*.log\n')
            f.write('build/\n')
            f.write('!important.log\n')
        
        scanner = EnhancedPathScanner(self.temp_dir, respect_gitignore=True)
        
        # Should exclude files matching gitignore patterns
        assert scanner._should_exclude('config.log')
        assert scanner._should_exclude('build', is_directory=True)
        
        # Should not exclude negated files
        assert not scanner._should_exclude('important.log')
        
        # Should not exclude unmatched files
        assert not scanner._should_exclude('main.py')
    
    def test_scan_basic_functionality(self):
        """Test basic scanning functionality."""
        scanner = EnhancedPathScanner(self.temp_dir, respect_gitignore=False)
        relationship_map, json_mirrors = scanner.scan()
        
        # Check that scanning produces results
        assert relationship_map.node_count() > 0
        assert relationship_map.relationship_count() > 0
        
        # Check that some files are included
        file_nodes = relationship_map.get_nodes_by_type(NodeType.FILE)
        file_paths = [node.path for node in file_nodes if hasattr(node, 'path')]
        
        # Should include source files
        assert any('main.py' in path for path in file_paths)
        assert any('README.md' in path for path in file_paths)
    
    def test_scan_with_gitignore_filtering(self):
        """Test scanning with gitignore filtering."""
        gitignore_path = os.path.join(self.temp_dir, '.gitignore')
        with open(gitignore_path, 'w') as f:
            f.write('*.log\n')
            f.write('build/\n')
            f.write('__pycache__/\n')
        
        scanner = EnhancedPathScanner(self.temp_dir, respect_gitignore=True)
        relationship_map, json_mirrors = scanner.scan()
        
        # Get all file paths in the relationship map
        file_nodes = relationship_map.get_nodes_by_type(NodeType.FILE)
        file_paths = [node.path for node in file_nodes if hasattr(node, 'path')]
        
        # Should not include gitignored files
        assert not any('config.log' in path for path in file_paths)
        assert not any('build/' in path for path in file_paths)
        assert not any('__pycache__/' in path for path in file_paths)
        
        # Should include non-ignored files
        assert any('main.py' in path for path in file_paths)
        assert any('README.md' in path for path in file_paths)
    
    def test_scan_with_max_depth(self):
        """Test scanning with depth limitation."""
        scanner = EnhancedPathScanner(self.temp_dir, respect_gitignore=False)
        relationship_map, json_mirrors = scanner.scan(max_depth=1)
        
        # Should include files at root and first level
        file_nodes = relationship_map.get_nodes_by_type(NodeType.FILE)
        file_paths = [node.path for node in file_nodes if hasattr(node, 'path')]
        
        # Should include top-level files
        assert any('README.md' in path for path in file_paths)
        
        # Should include first-level subdirectory files
        assert any('src/main.py' in path for path in file_paths)
    
    def test_scan_with_different_detail_levels(self):
        """Test scanning with different detail levels."""
        scanner = EnhancedPathScanner(self.temp_dir, respect_gitignore=False)
        
        # Test minimal detail level
        rm_minimal, jm_minimal = scanner.scan(detail_level=DetailLevel.MINIMAL)
        
        # Test standard detail level
        rm_standard, jm_standard = scanner.scan(detail_level=DetailLevel.STANDARD)
        
        # Test detailed detail level
        rm_detailed, jm_detailed = scanner.scan(detail_level=DetailLevel.DETAILED)
        
        # All should produce results
        assert rm_minimal.node_count() > 0
        assert rm_standard.node_count() > 0
        assert rm_detailed.node_count() > 0
