"""
Change tracking for file synchronization.
"""

import os
import time
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple, Any

from arch_blueprint_generator.errors.exceptions import FileError
from arch_blueprint_generator.models.json_mirrors import JSONMirrors
from arch_blueprint_generator.utils.logging import get_logger

logger = get_logger(__name__)


class ChangeTracker:
    """
    Tracks file changes to determine which files need to be synchronized.
    
    The ChangeTracker uses file hashes stored in JSONMirrors to detect
    when files have been modified, created, or deleted.
    """
    
    def __init__(self, json_mirrors: JSONMirrors):
        """
        Initialize a change tracker.
        
        Args:
            json_mirrors: JSON mirrors container for hash comparison
        """
        self.json_mirrors = json_mirrors
        logger.info("Initialized ChangeTracker")
    
    def detect_changes(self, paths: List[str]) -> Tuple[List[str], List[str], List[str]]:
        """
        Detect changes in the specified paths.
        
        Args:
            paths: List of file or directory paths to check
            
        Returns:
            Tuple of (modified_files, new_files, deleted_files)
        """
        logger.info(f"Detecting changes in {len(paths)} paths")
        
        # Expand paths to include all files if directories are provided
        all_files = self._expand_paths(paths)
        
        # Check for modified and new files
        modified_files = []
        new_files = []
        
        for file_path in all_files:
            try:
                if os.path.isfile(file_path):
                    if not self.json_mirrors.exists(file_path):
                        new_files.append(file_path)
                        logger.debug(f"New file detected: {file_path}")
                    elif not self.json_mirrors.is_mirror_up_to_date(file_path):
                        modified_files.append(file_path)
                        logger.debug(f"Modified file detected: {file_path}")
            except Exception as e:
                logger.warning(f"Error checking file {file_path}: {str(e)}")
        
        # Check for deleted files
        deleted_files = self._detect_deleted_files(paths)
        
        logger.info(f"Detected {len(modified_files)} modified files, "
                    f"{len(new_files)} new files, "
                    f"{len(deleted_files)} deleted files")
        
        return modified_files, new_files, deleted_files
    
    def _expand_paths(self, paths: List[str]) -> List[str]:
        """
        Expand paths to include all files if directories are provided.
        
        Args:
            paths: List of file or directory paths
            
        Returns:
            List of file paths
        """
        expanded_paths = []
        
        for path in paths:
            abs_path = os.path.abspath(path)
            
            if os.path.isfile(abs_path):
                expanded_paths.append(abs_path)
            elif os.path.isdir(abs_path):
                # Walk the directory and add all files
                for root, _, files in os.walk(abs_path):
                    for file in files:
                        expanded_paths.append(os.path.join(root, file))
            else:
                logger.warning(f"Path does not exist: {abs_path}")
        
        return expanded_paths
    
    def _detect_deleted_files(self, paths: List[str]) -> List[str]:
        """
        Detect files that have been deleted.
        
        Args:
            paths: List of paths to check for deletions
            
        Returns:
            List of deleted file paths
        """
        deleted_files = []
        
        # Get all mirrored files
        mirrored_files = self.json_mirrors.list_all_mirrors()
        
        # Check if each mirrored file exists in the file system
        for mirror_path in mirrored_files:
            # Only check for deletions within the specified paths
            if not self._is_within_paths(mirror_path, paths):
                continue
                
            if not os.path.exists(mirror_path):
                deleted_files.append(mirror_path)
                logger.debug(f"Deleted file detected: {mirror_path}")
        
        return deleted_files
    
    def _is_within_paths(self, file_path: str, paths: List[str]) -> bool:
        """
        Check if a file is within one of the specified paths.
        
        Args:
            file_path: File path to check
            paths: List of paths to check against
            
        Returns:
            True if the file is within one of the paths, False otherwise
        """
        abs_file_path = os.path.abspath(file_path)
        
        for path in paths:
            abs_path = os.path.abspath(path)
            
            if os.path.isfile(abs_path):
                if abs_file_path == abs_path:
                    return True
            elif os.path.isdir(abs_path):
                if abs_file_path.startswith(abs_path + os.sep):
                    return True
        
        return False
