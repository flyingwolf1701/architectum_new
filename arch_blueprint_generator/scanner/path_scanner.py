"""
Path scanning and representation generation.
"""

import os
import pathlib
from typing import Optional, List, Dict, Any, Tuple, Iterator, Set

from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors
from arch_blueprint_generator.models.detail_level import DetailLevel, DetailLevelConfig
from arch_blueprint_generator.models.nodes import (
    FileNode, DirectoryNode, ContainsRelationship
)
from arch_blueprint_generator.errors.exceptions import FileError
from arch_blueprint_generator.utils.logging import get_logger

logger = get_logger(__name__)


class PathScanner:
    """Scanner for directory paths to generate both representations."""
    
    def __init__(
        self, 
        root_path: str, 
        relationship_map: Optional[RelationshipMap] = None,
        json_mirrors: Optional[JSONMirrors] = None,
        exclude_patterns: Optional[List[str]] = None
    ):
        """
        Initialize a path scanner.
        
        Args:
            root_path: Root path to scan
            relationship_map: Existing relationship map to update, or None to create a new one
            json_mirrors: Existing JSON mirrors to update, or None to create a new one
            exclude_patterns: List of glob patterns to exclude from scanning
        """
        self.root_path = os.path.abspath(root_path)
        if not os.path.exists(self.root_path):
            raise FileError(f"Path does not exist: {self.root_path}")
        if not os.path.isdir(self.root_path):
            raise FileError(f"Path is not a directory: {self.root_path}")
        
        self.relationship_map = relationship_map or RelationshipMap()
        self.json_mirrors = json_mirrors or JSONMirrors(self.root_path)
        self.exclude_patterns = exclude_patterns or [".git", ".venv", "__pycache__"]
        
        logger.info(f"Initialized PathScanner for {self.root_path}")
    
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
        logger.info(f"Starting scan of {self.root_path} with max_depth={max_depth}, detail_level={detail_level.value}")
        
        # Create detail level configuration
        detail_config = DetailLevelConfig.uniform(detail_level)
        
        # Clear existing data that might overlap with this scan
        # (only for nodes within the scanned path)
        self._clean_existing_nodes(self.root_path)
        
        # Create root directory node
        root_node_id = f"dir:{self.root_path}"
        root_dir_node = DirectoryNode(root_node_id, self.root_path)
        self.relationship_map.add_node(root_dir_node)
        
        # Start recursive scanning
        self._scan_directory(self.root_path, root_node_id, 0, max_depth, detail_config)
        
        logger.info(f"Scan completed: {self.relationship_map.node_count()} nodes, "
                    f"{self.relationship_map.relationship_count()} relationships")
        
        return self.relationship_map, self.json_mirrors
    
    def _clean_existing_nodes(self, path: str) -> None:
        """
        Remove existing nodes that correspond to the scan path.
        
        Args:
            path: Path to clean nodes for
        """
        nodes_to_remove = []
        
        # Find directory and file nodes that start with the path
        for node_type in [DirectoryNode, FileNode]:
            for node in self.relationship_map.get_nodes_by_type(node_type):
                if hasattr(node, 'path') and node.path.startswith(path):
                    nodes_to_remove.append(node.id)
        
        # Remove the nodes
        for node_id in nodes_to_remove:
            try:
                self.relationship_map.remove_node(node_id)
            except Exception as e:
                logger.warning(f"Failed to remove node {node_id}: {str(e)}")
    
    def _scan_directory(
        self, 
        directory: str, 
        parent_node_id: str, 
        current_depth: int, 
        max_depth: int,
        detail_config: DetailLevelConfig
    ) -> None:
        """
        Recursively scan a directory and its contents.
        
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
        
        # List all items in the directory, filtering out excluded patterns
        try:
            items = self._list_directory_content(directory)
        except Exception as e:
            logger.error(f"Error scanning directory {directory}: {str(e)}")
            return
        
        # Create JSON mirror for the directory
        try:
            files = [item for item in items if os.path.isfile(os.path.join(directory, item))]
            subdirs = [item for item in items if os.path.isdir(os.path.join(directory, item))]
            self.json_mirrors.create_directory_mirror(
                directory, 
                [os.path.join(directory, f) for f in files],
                [os.path.join(directory, d) for d in subdirs],
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
                
                # Create JSON mirror for the file (basic version without detailed parsing)
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
        List items in a directory, filtering out excluded patterns.
        
        Args:
            directory: Directory path to list
            
        Returns:
            List of filenames in the directory (not full paths)
        """
        try:
            all_items = os.listdir(directory)
        except Exception as e:
            raise FileError(f"Cannot list directory {directory}: {str(e)}")
        
        # Filter out excluded patterns
        filtered_items = []
        for item in all_items:
            skip = False
            for pattern in self.exclude_patterns:
                if pattern in item:  # Simple string matching for now
                    skip = True
                    break
            
            if not skip:
                filtered_items.append(item)
        
        return filtered_items
    
    @staticmethod
    def is_binary_file(file_path: str) -> bool:
        """
        Check if a file is binary.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if the file is binary, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Try to read some content
                f.read(1024)
                return False
        except UnicodeDecodeError:
            return True
        except Exception:
            # For any other error, assume it's not binary
            return False
