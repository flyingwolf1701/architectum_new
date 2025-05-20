"""
Synchronization implementation for Architectum representations.
"""

import os
import time
from typing import List, Dict, Optional, Tuple, Any

from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors
from arch_blueprint_generator.models.nodes import (
    NodeType, FileNode, DirectoryNode, ContainsRelationship
)
from arch_blueprint_generator.scanner.path_scanner import PathScanner
from arch_blueprint_generator.sync.change_tracker import ChangeTracker
from arch_blueprint_generator.errors.exceptions import FileError
from arch_blueprint_generator.utils.logging import get_logger

logger = get_logger(__name__)


class ArchSync:
    """
    Implements the 'arch sync' functionality for synchronizing code with Architectum.
    
    ArchSync provides efficient synchronization of code files with both the
    Relationship Map and JSON Mirrors representations, performing incremental
    updates when possible.
    """
    
    def __init__(
        self,
        relationship_map: Optional[RelationshipMap] = None,
        json_mirrors: Optional[JSONMirrors] = None
    ):
        """
        Initialize an ArchSync instance.
        
        Args:
            relationship_map: Existing relationship map to update, or None to create a new one
            json_mirrors: Existing JSON mirrors to update, or None to create a new one
        """
        # Initialize with empty representations if none provided
        self.relationship_map = relationship_map or RelationshipMap()
        
        # For JSONMirrors, we need a root path. Use current directory as fallback.
        if json_mirrors:
            self.json_mirrors = json_mirrors
        else:
            root_path = os.getcwd()
            self.json_mirrors = JSONMirrors(root_path)
        
        self.change_tracker = ChangeTracker(self.json_mirrors)
        logger.info("Initialized ArchSync")
    
    def sync(
        self,
        paths: List[str],
        recursive: bool = False,
        force: bool = False
    ) -> Tuple[int, int, int]:
        """
        Synchronize code files with Architectum representations.
        
        Args:
            paths: List of paths to synchronize
            recursive: Whether to recursively synchronize subdirectories
            force: Whether to force synchronization even if files are up to date
            
        Returns:
            Tuple of (files_updated, files_added, files_removed)
        """
        start_time = time.time()
        logger.info(f"Starting synchronization of {len(paths)} paths")
        
        # Prepare paths for processing
        processed_paths = self._prepare_paths(paths, recursive)
        
        if force:
            # Force full rescan of all paths
            logger.info("Forcing full rescan of all paths")
            updated, added, removed = self._force_rescan(processed_paths)
        else:
            # Perform incremental update
            updated, added, removed = self._incremental_update(processed_paths)
        
        duration = time.time() - start_time
        logger.info(f"Synchronization completed in {duration:.2f}s: "
                    f"{updated} updated, {added} added, {removed} removed")
        
        return updated, added, removed
    
    def _prepare_paths(self, paths: List[str], recursive: bool) -> List[str]:
        """
        Prepare paths for processing, resolving to absolute paths and
        expanding directories if recursive is True.
        
        Args:
            paths: List of paths to prepare
            recursive: Whether to recursively include subdirectories
            
        Returns:
            List of prepared paths
        """
        prepared_paths = []
        
        for path in paths:
            abs_path = os.path.abspath(path)
            
            if not os.path.exists(abs_path):
                logger.warning(f"Path does not exist: {abs_path}")
                continue
            
            if os.path.isfile(abs_path):
                prepared_paths.append(abs_path)
            elif os.path.isdir(abs_path):
                if recursive:
                    # Include the directory and all its content
                    prepared_paths.append(abs_path)
                else:
                    # Include only the immediate files in the directory
                    try:
                        for item in os.listdir(abs_path):
                            item_path = os.path.join(abs_path, item)
                            if os.path.isfile(item_path):
                                prepared_paths.append(item_path)
                    except Exception as e:
                        logger.error(f"Error listing directory {abs_path}: {str(e)}")
        
        return prepared_paths
    
    def _force_rescan(self, paths: List[str]) -> Tuple[int, int, int]:
        """
        Force a complete rescan of all paths.
        
        Args:
            paths: List of paths to rescan
            
        Returns:
            Tuple of (files_updated, files_added, files_removed)
        """
        if not paths:
            return 0, 0, 0
        
        # Count number of files processed
        file_count = 0
        
        # Use PathScanner to perform a full scan
        for path in paths:
            if os.path.isdir(path):
                logger.info(f"Performing full rescan of directory: {path}")
                scanner = PathScanner(
                    path,
                    relationship_map=self.relationship_map,
                    json_mirrors=self.json_mirrors
                )
                rel_map, _ = scanner.scan()
                
                # Count the number of file nodes added
                file_count += len(rel_map.get_nodes_by_type(NodeType.FILE))
            elif os.path.isfile(path):
                logger.info(f"Rescanning file: {path}")
                # Remove any existing nodes for the file then add it back
                self._clean_existing_file_nodes(path)
                self._add_file(path)
                file_count += 1
        
        # Since we're doing a force rescan, count all files as updates
        return file_count, 0, 0
    
    def _incremental_update(self, paths: List[str]) -> Tuple[int, int, int]:
        """
        Perform an incremental update of the specified paths.
        
        Args:
            paths: List of paths to update
            
        Returns:
            Tuple of (files_updated, files_added, files_removed)
        """
        if not paths:
            return 0, 0, 0
        
        # Detect changes using the change tracker
        modified_files, new_files, deleted_files = self.change_tracker.detect_changes(paths)
        
        # Process modified files
        for file_path in modified_files:
            self._update_file(file_path)
        
        # Process new files
        for file_path in new_files:
            self._add_file(file_path)
        
        # Process deleted files
        for file_path in deleted_files:
            self._remove_file(file_path)
        
        return len(modified_files), len(new_files), len(deleted_files)
    
    def _update_file(self, file_path: str) -> None:
        """
        Update representations for a modified file.
        
        Args:
            file_path: Path to the modified file
        """
        logger.debug(f"Updating file: {file_path}")
        
        try:
            # Remove existing nodes for the file
            self._clean_existing_file_nodes(file_path)
            
            # Add the file back with updated content
            self._add_file(file_path)
        except Exception as e:
            logger.error(f"Error updating file {file_path}: {str(e)}")
    
    def _add_file(self, file_path: str) -> None:
        """
        Add representations for a new file.
        
        Args:
            file_path: Path to the new file
        """
        logger.debug(f"Adding file: {file_path}")
        
        try:
            # Get the parent directory
            parent_dir = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            
            # Check if parent directory exists in relationship map
            parent_dir_id = f"dir:{parent_dir}"
            parent_node = self.relationship_map.get_node(parent_dir_id)
            
            # If parent not in relationship map, we need to add it
            if not parent_node:
                parent_node = DirectoryNode(parent_dir_id, parent_dir)
                self.relationship_map.add_node(parent_node)
                # Create directory mirror if needed
                if not self.json_mirrors.exists(parent_dir):
                    files, subdirs = self.json_mirrors.scan_directory(parent_dir)
                    self.json_mirrors.create_directory_mirror(parent_dir, files, subdirs)
            
            # Create file node
            file_ext = os.path.splitext(file_path)[1]
            file_node_id = f"file:{file_path}"
            file_node = FileNode(file_node_id, file_path, file_ext)
            self.relationship_map.add_node(file_node)
            
            # Create relationship from parent to file
            rel = ContainsRelationship(parent_dir_id, file_node_id)
            self.relationship_map.add_relationship(rel)
            
            # Create file mirror
            self.json_mirrors.create_file_mirror(file_path, {}, [])
            
        except Exception as e:
            logger.error(f"Error adding file {file_path}: {str(e)}")
    
    def _remove_file(self, file_path: str) -> None:
        """
        Remove representations for a deleted file.
        
        Args:
            file_path: Path to the deleted file
        """
        logger.debug(f"Removing file: {file_path}")
        
        try:
            # Remove nodes from the relationship map
            self._clean_existing_file_nodes(file_path)
            
            # Remove from JSON mirrors
            self.json_mirrors.remove(file_path)
        except Exception as e:
            logger.error(f"Error removing file {file_path}: {str(e)}")
    
    def _clean_existing_file_nodes(self, file_path: str) -> None:
        """
        Remove existing nodes for a file from the relationship map.
        
        Args:
            file_path: Path to the file
        """
        # Find the file node
        file_node_id = f"file:{file_path}"
        file_node = self.relationship_map.get_node(file_node_id)
        
        if file_node:
            # Get all relationships involving this node
            incoming = self.relationship_map.get_incoming_relationships(file_node_id)
            outgoing = self.relationship_map.get_outgoing_relationships(file_node_id)
            
            # Remove all relationships
            for rel in incoming:
                self.relationship_map.remove_relationship(rel.source_id, rel.target_id)
            
            for rel in outgoing:
                self.relationship_map.remove_relationship(rel.source_id, rel.target_id)
            
            # Remove the node itself
            self.relationship_map.remove_node(file_node_id)
