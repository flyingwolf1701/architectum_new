"""
Unit tests for GitIgnoreParser functionality.
"""

import os
import tempfile
import shutil
import pytest

from arch_blueprint_generator.scanner.enhanced_path_scanner import GitIgnoreParser


class TestGitIgnoreParser:
    """Test cases for GitIgnoreParser functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.gitignore_path = os.path.join(self.temp_dir, '.gitignore')
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_parser_with_no_gitignore_file(self):
        """Test parser behavior when .gitignore file doesn't exist."""
        non_existent_path = os.path.join(self.temp_dir, 'nonexistent.gitignore')
        parser = GitIgnoreParser(non_existent_path)
        
        assert parser.patterns == []
        assert parser.directory_patterns == []
        assert parser.negation_patterns == []
        assert not parser.should_ignore('any_file.txt')
    
    def test_parser_with_empty_gitignore(self):
        """Test parser with empty .gitignore file."""
        with open(self.gitignore_path, 'w') as f:
            f.write('')
        
        parser = GitIgnoreParser(self.gitignore_path)
        assert parser.patterns == []
        assert not parser.should_ignore('any_file.txt')
    
    def test_parser_with_comments_and_empty_lines(self):
        """Test parser correctly handles comments and empty lines."""
        with open(self.gitignore_path, 'w') as f:
            f.write('# This is a comment\n')
            f.write('\n')
            f.write('*.log\n')
            f.write('# Another comment\n')
            f.write('\n')
            f.write('temp/\n')
        
        parser = GitIgnoreParser(self.gitignore_path)
        assert '*.log' in parser.patterns
        assert 'temp' in parser.directory_patterns
        assert len(parser.patterns) == 1
        assert len(parser.directory_patterns) == 1
    
    def test_glob_patterns(self):
        """Test various glob patterns."""
        with open(self.gitignore_path, 'w') as f:
            f.write('*.log\n')
            f.write('test_*.py\n')
            f.write('temp*\n')
        
        parser = GitIgnoreParser(self.gitignore_path)
        
        # Should ignore files matching patterns
        assert parser.should_ignore('debug.log')
        assert parser.should_ignore('error.log')
        assert parser.should_ignore('test_main.py')
        assert parser.should_ignore('test_utils.py')
        assert parser.should_ignore('temp123')
        assert parser.should_ignore('temporary')
        
        # Should not ignore files not matching patterns
        assert not parser.should_ignore('main.py')
        assert not parser.should_ignore('config.txt')
        assert not parser.should_ignore('src/test.py')
    
    def test_directory_patterns(self):
        """Test directory-specific patterns."""
        with open(self.gitignore_path, 'w') as f:
            f.write('build/\n')
            f.write('node_modules/\n')
            f.write('__pycache__/\n')
        
        parser = GitIgnoreParser(self.gitignore_path)
        
        # Should ignore directories
        assert parser.should_ignore('build', is_directory=True)
        assert parser.should_ignore('node_modules', is_directory=True)
        assert parser.should_ignore('__pycache__', is_directory=True)
        
        # Should not ignore files with same names
        assert not parser.should_ignore('build')
        assert not parser.should_ignore('node_modules')
        assert not parser.should_ignore('__pycache__')
    
    def test_negation_patterns(self):
        """Test negation patterns that un-ignore files."""
        with open(self.gitignore_path, 'w') as f:
            f.write('*.log\n')
            f.write('!important.log\n')
            f.write('temp/\n')
            f.write('!temp/keep.txt\n')
        
        parser = GitIgnoreParser(self.gitignore_path)
        
        # Should ignore all .log files except important.log
        assert parser.should_ignore('debug.log')
        assert parser.should_ignore('error.log')
        assert not parser.should_ignore('important.log')  # Negated
        
        # Should ignore temp directory but not keep.txt in it
        assert parser.should_ignore('temp', is_directory=True)
        assert not parser.should_ignore('temp/keep.txt')  # Negated
    
    def test_path_patterns(self):
        """Test patterns with path separators."""
        with open(self.gitignore_path, 'w') as f:
            f.write('docs/*.pdf\n')
            f.write('src/temp/*.tmp\n')
            f.write('/root_file.txt\n')
        
        parser = GitIgnoreParser(self.gitignore_path)
        
        # Should match path patterns
        assert parser.should_ignore('docs/manual.pdf')
        assert parser.should_ignore('src/temp/cache.tmp')
        assert parser.should_ignore('root_file.txt')
        
        # Should not match patterns in wrong locations
        assert not parser.should_ignore('src/manual.pdf')
        assert not parser.should_ignore('docs/temp/cache.tmp')
        assert not parser.should_ignore('subdir/root_file.txt')
    
    def test_normalize_pattern(self):
        """Test pattern normalization."""
        parser = GitIgnoreParser('nonexistent')
        
        # Test removal of leading slash
        assert parser._normalize_pattern('/absolute.txt') == 'absolute.txt'
        assert parser._normalize_pattern('relative.txt') == 'relative.txt'
        assert parser._normalize_pattern('path/to/file.txt') == 'path/to/file.txt'
    
    def test_matches_pattern(self):
        """Test pattern matching logic."""
        parser = GitIgnoreParser('nonexistent')
        
        # Test basename matching
        assert parser._matches_pattern('src/test.py', '*.py')
        assert parser._matches_pattern('deep/nested/test.py', '*.py')
        assert not parser._matches_pattern('src/test.js', '*.py')
        
        # Test path matching
        assert parser._matches_pattern('docs/readme.md', 'docs/*.md')
        assert not parser._matches_pattern('src/readme.md', 'docs/*.md')
        
        # Test exact matching
        assert parser._matches_pattern('config.ini', 'config.ini')
        assert not parser._matches_pattern('src/config.ini', 'config.ini')


class TestGitIgnoreEdgeCases:
    """Test edge cases for GitIgnore functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_gitignore_with_special_characters(self):
        """Test gitignore with special characters in filenames."""
        gitignore_path = os.path.join(self.temp_dir, '.gitignore')
        with open(gitignore_path, 'w') as f:
            f.write('*.log\n')
            f.write('test-[0-9]*.py\n')
            f.write('file with spaces.txt\n')
        
        parser = GitIgnoreParser(gitignore_path)
        
        # Test special characters
        assert parser.should_ignore('debug.log')
        assert parser.should_ignore('test-123.py')
        assert parser.should_ignore('test-9.py')
        assert parser.should_ignore('file with spaces.txt')
        
        assert not parser.should_ignore('test-abc.py')
        assert not parser.should_ignore('different file.txt')
    
    def test_gitignore_with_unicode_characters(self):
        """Test gitignore with unicode characters."""
        gitignore_path = os.path.join(self.temp_dir, '.gitignore')
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write('测试文件.txt\n')
            f.write('файл.log\n')
        
        parser = GitIgnoreParser(gitignore_path)
        
        # Test unicode patterns
        assert parser.should_ignore('测试文件.txt')
        assert parser.should_ignore('файл.log')
        
        assert not parser.should_ignore('test.txt')
        assert not parser.should_ignore('file.log')
    
    def test_gitignore_with_malformed_patterns(self):
        """Test gitignore with malformed patterns."""
        gitignore_path = os.path.join(self.temp_dir, '.gitignore')
        with open(gitignore_path, 'w') as f:
            f.write('   \n')  # Whitespace only
            f.write('*.log\n')
            f.write('!\n')    # Invalid negation
            f.write('/\n')    # Invalid absolute pattern
            f.write('normal.txt\n')
        
        # Should not raise exceptions
        parser = GitIgnoreParser(gitignore_path)
        
        # Should still work for valid patterns
        assert parser.should_ignore('debug.log')
        assert parser.should_ignore('normal.txt')
