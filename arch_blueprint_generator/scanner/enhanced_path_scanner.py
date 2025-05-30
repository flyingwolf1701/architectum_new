"""
Enhanced PathScanner with GitIgnore support for Architectum.

This implementation adds proper .gitignore pattern matching to the existing
PathScanner, ensuring that files ignored by git are also excluded from
Architectum's mirrors and relationship maps.
"""

import os
import pathlib
import fnmatch
from typing import Optional, List, Dict, Any, Tuple, Iterator, Set

from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors
from arch_blueprint_generator.models.detail_level import DetailLevel, DetailLevelConfig
from arch_blueprint_generator.models.nodes import (
    FileNode, DirectoryNode, ContainsRelationship, NodeType
)
from arch_blueprint_generator.errors.exceptions import FileError
from arch_blueprint_generator.utils.logging import get_logger

logger = get_logger(__name__)


class GitIgnoreParser:
    """
    Parser for .gitignore files that handles gitignore pattern matching.
    
    Supports:
    - Glob patterns (*, ?, [abc])
    - Directory patterns (ending with /)
    - Negation patterns (starting with !)
    - Comments (starting with #)
    - Absolute vs relative patterns
    """
    
    def __init__(self, gitignore_path: str):
        """
        Initialize parser with path to .gitignore file.
        
        Args:
            gitignore_path: Path to the .gitignore file
        """
        self.gitignore_path = gitignore_path
        self.patterns = []
        self.directory_patterns = []
        self.negation_patterns = []
        
        if os.path.exists(gitignore_path):
            self._parse_gitignore()
    
    def _parse_gitignore(self) -> None:
        """Parse the .gitignore file and extract patterns."""
        try:
            with open(self.gitignore_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Handle negation patterns
                    if line.startswith('!'):
                        pattern = line[1:].strip()
                        if pattern:
                            self.negation_patterns.append(self._normalize_pattern(pattern))
                        continue
                    
                    # Handle directory patterns
                    if line.endswith('/'):
                        self.directory_patterns.append(self._normalize_pattern(line[:-1]))
                        continue
                    
                    # Regular patterns
                    self.patterns.append(self._normalize_pattern(line))
                    
        except Exception as e:
            logger.warning(f"Error parsing .gitignore at {self.gitignore_path}: {str(e)}")
    
    def _normalize_pattern(self, pattern: str) -> str:
        """
        Normalize a gitignore pattern for consistent matching.
        
        Args:
            pattern: Raw pattern from .gitignore
            
        Returns:
            Normalized pattern
        """
        # Remove leading slash for absolute patterns
        if pattern.startswith('/'):
            pattern = pattern[1:]
        
        # Convert gitignore patterns to fnmatch patterns
        # GitIgnore uses different semantics than fnmatch in some cases
        return pattern
    
    def should_ignore(self, file_path: str, is_directory: bool = False) -> bool:
        """
        Check if a file/directory should be ignored based on gitignore patterns.
        
        Args:
            file_path: Path to check (relative to git root)
            is_directory: Whether the path is a directory
            
        Returns:
            True if the file should be ignored, False otherwise
        """
        # Convert absolute path to relative path for matching
        if os.path.isabs(file_path):
            try:
                git_root = self._find_git_root(file_path)
                if git_root:
                    file_path = os.path.relpath(file_path, git_root)
                else:
                    # If no git root found, use basename
                    file_path = os.path.basename(file_path)
            except ValueError:
                file_path = os.path.basename(file_path)
        
        # Normalize path separators
        file_path = file_path.replace('\\', '/')
        
        # Check directory patterns first if this is a directory
        if is_directory:
            for pattern in self.directory_patterns:
                if self._matches_pattern(file_path, pattern):
                    # Check for negation
                    if not self._is_negated(file_path):
                        return True
        
        # Check regular patterns
        for pattern in self.patterns:
            if self._matches_pattern(file_path, pattern):
                # Check for negation
                if not self._is_negated(file_path):
                    return True
        
        return False
    
    def _matches_pattern(self, file_path: str, pattern: str) -> bool:
        """
        Check if a file path matches a gitignore pattern.
        
        Args:
            file_path: File path to check
            pattern: GitIgnore pattern
            
        Returns:
            True if the pattern matches
        """
        # Handle different pattern types
        
        # If pattern contains '/', it's a path pattern
        if '/' in pattern:
            return fnmatch.fnmatch(file_path, pattern)
        
        # Otherwise, match against basename or any part of the path
        basename = os.path.basename(file_path)
        if fnmatch.fnmatch(basename, pattern):
            return True
        
        # Also check if any part of the path matches
        path_parts = file_path.split('/')
        for part in path_parts:
            if fnmatch.fnmatch(part, pattern):
                return True
        
        return False
    
    def _is_negated(self, file_path: str) -> bool:
        """
        Check if a file path is negated (un-ignored) by a negation pattern.
        
        Args:
            file_path: File path to check
            
        Returns:
            True if the file is negated (should not be ignored)
        """
        for pattern in self.negation_patterns:
            if self._matches_pattern(file_path, pattern):
                return True
        return False
    
    def _find_git_root(self, path: str) -> Optional[str]:
        """
        Find the git root directory for a given path.
        
        Args:
            path: Path to start searching from
            
        Returns:
            Path to git root directory, or None if not found
        """
        current_path = os.path.abspath(path)
        
        while current_path != os.path.dirname(current_path):  # Not at filesystem root
            if os.path.exists(os.path.join(current_path, '.git')):
                return current_path
            current_path = os.path.dirname(current_path)
        
        return None


class EnhancedPathScanner:
    """
    Enhanced PathScanner with GitIgnore support.
    
    This scanner respects .gitignore files and provides better filtering
    while maintaining compatibility with the existing PathScanner interface.
    """
    
    def __init__(
        self, 
        root_path: str, 
        relationship_map: Optional[RelationshipMap] = None,
        json_mirrors: Optional[JSONMirrors] = None,
        exclude_patterns: Optional[List[str]] = None,
        respect_gitignore: bool = True,
        additional_ignores: Optional[List[str]] = None
    ):
        """
        Initialize an enhanced path scanner.
        
        Args:
            root_path: Root path to scan
            relationship_map: Existing relationship map to update
            json_mirrors: Existing JSON mirrors to update
            exclude_patterns: List of patterns to exclude (legacy compatibility)
            respect_gitignore: Whether to respect .gitignore files
            additional_ignores: Additional patterns to ignore beyond .gitignore
        """
        self.root_path = os.path.abspath(root_path)
        if not os.path.exists(self.root_path):
            raise FileError(f"Path does not exist: {self.root_path}")
        if not os.path.isdir(self.root_path):
            raise FileError(f"Path is not a directory: {self.root_path}")
        
        self.relationship_map = relationship_map or RelationshipMap()
        self.json_mirrors = json_mirrors or JSONMirrors(self.root_path)
        self.respect_gitignore = respect_gitignore
        
        # Set up exclusion patterns
        self.exclude_patterns = exclude_patterns or [".git", ".venv", "__pycache__", ".architectum"]
        if additional_ignores:
            self.exclude_patterns.extend(additional_ignores)
        
        # Initialize gitignore parser if enabled
        self.gitignore_parser = None
        if respect_gitignore:
            gitignore_path = os.path.join(self.root_path, '.gitignore')
            if os.path.exists(gitignore_path):
                self.gitignore_parser = GitIgnoreParser(gitignore_path)
                logger.info(f"Loaded .gitignore patterns from {gitignore_path}")
            else:
                logger.debug(f"No .gitignore file found at {gitignore_path}")
        
        logger.info(f"Initialized EnhancedPathScanner for {self.root_path}")
    
    def scan(
        self, 
        max_depth: int = 0, 
        detail_level: DetailLevel = DetailLevel.STANDARD
    ) -> Tuple[RelationshipMap, JSONMirrors]:
        """
        Scan the directory structure and generate both representations.
        
        Args:
            max_depth: Maximum depth to scan (0 for no limit)
            detail_level: The level of detail to include
            
        Returns:
            Tuple of (RelationshipMap, JSONMirrors)
        """
        logger.info(f"Starting enhanced scan of {self.root_path} with max_depth={max_depth}, detail_level={detail_level.value}")
        
        # Create detail level configuration
        detail_config = DetailLevelConfig.uniform(detail_level)
        
        # Clear existing data that might overlap with this scan
        self._clean_existing_nodes(self.root_path)
        
        # Create root directory node
        root_node_id = f"dir:{self.root_path}"
        root_dir_node = DirectoryNode(root_node_id, self.root_path)
        self.relationship_map.add_node(root_dir_node)
        
        # Start recursive scanning
        self._scan_directory(self.root_path, root_node_id, 0, max_depth, detail_config)
        
        total_nodes = self.relationship_map.node_count()
        total_relationships = self.relationship_map.relationship_count()
        
        logger.info(f"Enhanced scan completed: {total_nodes} nodes, {total_relationships} relationships")
        
        # Store the detail level in the relationship map
        self.relationship_map.detail_level = detail_level
        
        return self.relationship_map, self.json_mirrors
    
    def _should_exclude(self, item_path: str, is_directory: bool = False) -> bool:
        """
        Determine if an item should be excluded based on all filtering rules.
        
        Args:
            item_path: Path to the item
            is_directory: Whether the item is a directory
            
        Returns:
            True if the item should be excluded
        """
        item_name = os.path.basename(item_path)
        
        # Check legacy exclude patterns first (for backward compatibility)
        for pattern in self.exclude_patterns:
            if pattern in item_name:
                logger.debug(f"Excluding {item_path} due to exclude pattern: {pattern}")
                return True
        
        # Check gitignore patterns if enabled
        if self.gitignore_parser:
            if self.gitignore_parser.should_ignore(item_path, is_directory):
                logger.debug(f"Excluding {item_path} due to .gitignore patterns")
                return True
        
        return False
    
    def _scan_directory(
        self, 
        directory: str, 
        parent_node_id: str, 
        current_depth: int, 
        max_depth: int,
        detail_config: DetailLevelConfig
    ) -> None:
        """
        Recursively scan a directory and its contents with enhanced filtering.
        
        Args:
            directory: Directory path to scan
            parent_node_id: ID of the parent node in the relationship map
            current_depth: Current scan depth
            max_depth: Maximum depth to scan (0 for no limit)
            detail_config: Detail level configuration
        """
        if max_depth > 0 and current_depth >= max_depth:
            logger.debug(f"Reached max depth at {directory}")
            return
        
        # List all items in the directory with enhanced filtering
        try:
            items = self._list_directory_content(directory)
        except Exception as e:
            logger.error(f"Error scanning directory {directory}: {str(e)}")
            return
        
        # Create JSON mirror for the directory
        try:
            valid_files = []
            valid_subdirs = []
            
            for item in items:
                item_path = os.path.join(directory, item)
                if os.path.isfile(item_path):
                    valid_files.append(item_path)
                elif os.path.isdir(item_path):
                    valid_subdirs.append(item_path)
            
            self.json_mirrors.create_directory_mirror(
                directory, 
                valid_files,
                valid_subdirs,
                detail_config.json_mirrors
            )
        except Exception as e:
            logger.error(f"Error creating directory mirror for {directory}: {str(e)}")
        
        # Process each item in the directory
        for item in items:
            item_path = os.path.join(directory, item)
            
            if os.path.isdir(item_path):
                # Create node for subdirectory
                subdir_node_id = f"dir:{item_path}"
                subdir_node = DirectoryNode(subdir_node_id, item_path)
                self.relationship_map.add_node(subdir_node)
                
                # Create "contains" relationship
                contains_rel = ContainsRelationship(parent_node_id, subdir_node_id)
                self.relationship_map.add_relationship(contains_rel)
                
                # Recursively scan subdirectory
                self._scan_directory(item_path, subdir_node_id, current_depth + 1, max_depth, detail_config)
            
            elif os.path.isfile(item_path):
                # Create node for file
                file_ext = os.path.splitext(item_path)[1]
                file_node_id = f"file:{item_path}"
                file_node = FileNode(file_node_id, item_path, file_ext)
                self.relationship_map.add_node(file_node)
                
                # Create "contains" relationship
                contains_rel = ContainsRelationship(parent_node_id, file_node_id)
                self.relationship_map.add_relationship(contains_rel)
                
                # Create JSON mirror for the file
                try:
                    self.json_mirrors.create_file_mirror(
                        item_path,
                        {},  # Empty elements dict for now
                        [],  # Empty imports list for now
                        detail_config.json_mirrors
                    )
                except Exception as e:
                    logger.error(f"Error creating file mirror for {item_path}: {str(e)}")
    
    def _list_directory_content(self, directory: str) -> List[str]:
        """
        List items in a directory with enhanced filtering.
        
        Args:
            directory: Directory path to list
            
        Returns:
            List of filenames in the directory (not full paths)
        """
        try:
            all_items = os.listdir(directory)
        except Exception as e:
            raise FileError(f"Cannot list directory {directory}: {str(e)}")
        
        # Filter out excluded items
        filtered_items = []
        for item in all_items:
            item_path = os.path.join(directory, item)
            is_directory = os.path.isdir(item_path)
            
            if not self._should_exclude(item_path, is_directory):
                filtered_items.append(item)
            else:
                logger.debug(f"Filtered out: {item}")
        
        return filtered_items
    
    def _clean_existing_nodes(self, path: str) -> None:
        """
        Remove existing nodes that correspond to the scan path.
        
        Args:
            path: Path to clean nodes for
        """
        nodes_to_remove = []
        
        # Find directory and file nodes that start with the path
        for node_type_enum in [NodeType.DIRECTORY, NodeType.FILE]:
            for node in self.relationship_map.get_nodes_by_type(node_type_enum):
                if hasattr(node, 'path') and node.path.startswith(path):
                    nodes_to_remove.append(node.id)
        
        # Remove the nodes
        for node_id in nodes_to_remove:
            try:
                self.relationship_map.remove_node(node_id)
            except Exception as e:
                logger.warning(f"Failed to remove node {node_id}: {str(e)}")


# Usage example and testing
if __name__ == "__main__":
    # Example usage
    scanner = EnhancedPathScanner(
        ".", 
        respect_gitignore=True,
        additional_ignores=["*.log", "*.tmp", ".DS_Store"]
    )
    
    relationship_map, json_mirrors = scanner.scan(max_depth=2, detail_level=DetailLevel.STANDARD)
    
    print(f"Scanned with gitignore support: {relationship_map.node_count()} nodes")
