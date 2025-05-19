"""
JSON Mirrors structure for code representation.
"""

import json
import os
from typing import Dict, List, Optional, Any, Union, Tuple
import hashlib
from pathlib import Path

from arch_blueprint_generator.errors.exceptions import FileError, ModelError
from arch_blueprint_generator.utils.logging import get_logger

logger = get_logger(__name__)


class CodeElement:
    """Represents a code element (function, class, etc.)."""
    
    def __init__(
        self,
        name: str,
        element_type: str,
        line_start: int,
        line_end: int,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a code element.
        
        Args:
            name: Element name
            element_type: Type of the element
            line_start: Starting line number
            line_end: Ending line number
            metadata: Additional metadata for the element
        """
        self.name = name
        self.type = element_type
        self.line_start = line_start
        self.line_end = line_end
        self.metadata = metadata or {}
    
    def to_json(self) -> Dict[str, Any]:
        """
        Convert the code element to a JSON representation.
        
        Returns:
            JSON representation of the code element
        """
        return {
            "name": self.name,
            "type": self.type,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "metadata": self.metadata
        }

    
    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'CodeElement':
        """
        Create a code element from a JSON representation.
        
        Args:
            data: JSON representation of the code element
            
        Returns:
            CodeElement instance
        """
        return cls(
            data["name"],
            data["type"],
            data["line_start"],
            data["line_end"],
            data.get("metadata", {})
        )


class FileContent:
    """Represents the content of a file."""
    
    def __init__(
        self,
        path: str,
        extension: str,
        elements: Optional[Dict[str, CodeElement]] = None,
        imports: Optional[List[str]] = None,
        source_hash: Optional[str] = None
    ):
        """
        Initialize a file content object.
        
        Args:
            path: Path to the file
            extension: File extension
            elements: Dictionary mapping element names to CodeElement objects
            imports: List of imported file paths
            source_hash: Hash of the source file content
        """
        self.path = path
        self.extension = extension
        self.elements = elements or {}
        self.imports = imports or []
        self.source_hash = source_hash
    
    def add_element(self, element: CodeElement) -> None:
        """
        Add a code element to the file.
        
        Args:
            element: The element to add
            
        Raises:
            ModelError: If an element with the same name already exists
        """
        if element.name in self.elements:
            raise ModelError(f"Element '{element.name}' already exists in file '{self.path}'")
        
        self.elements[element.name] = element
    
    def remove_element(self, name: str) -> None:
        """
        Remove a code element from the file.
        
        Args:
            name: The name of the element to remove
            
        Raises:
            ModelError: If the element does not exist
        """
        if name not in self.elements:
            raise ModelError(f"Element '{name}' does not exist in file '{self.path}'")
        
        del self.elements[name]
    
    def add_import(self, import_path: str) -> None:
        """
        Add an import to the file.
        
        Args:
            import_path: The path of the imported file
        """
        if import_path not in self.imports:
            self.imports.append(import_path)
    
    def remove_import(self, import_path: str) -> None:
        """
        Remove an import from the file.
        
        Args:
            import_path: The path of the imported file
        """
        if import_path in self.imports:
            self.imports.remove(import_path)
    
    def to_json(self) -> Dict[str, Any]:
        """
        Convert the file content to a JSON representation.
        
        Returns:
            JSON representation of the file content
        """
        elements_json = {name: element.to_json() for name, element in self.elements.items()}
        
        result = {
            "path": self.path,
            "extension": self.extension,
            "elements": elements_json,
            "imports": self.imports
        }
        
        if self.source_hash:
            result["source_hash"] = self.source_hash
        
        return result
    
    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'FileContent':
        """
        Create a file content object from a JSON representation.
        
        Args:
            data: JSON representation of the file content
            
        Returns:
            FileContent instance
        """
        elements = {}
        for name, element_data in data["elements"].items():
            elements[name] = CodeElement.from_json(element_data)
        
        return cls(
            data["path"],
            data["extension"],
            elements,
            data.get("imports", []),
            data.get("source_hash")
        )


class DirectoryContent:
    """Represents the content of a directory."""
    
    def __init__(
        self,
        path: str,
        files: Optional[List[str]] = None,
        subdirectories: Optional[List[str]] = None
    ):
        """
        Initialize a directory content object.
        
        Args:
            path: Path to the directory
            files: List of file paths in the directory
            subdirectories: List of subdirectory paths in the directory
        """
        self.path = path
        self.files = files or []
        self.subdirectories = subdirectories or []
    
    def add_file(self, file_path: str) -> None:
        """
        Add a file to the directory.
        
        Args:
            file_path: The path of the file to add
        """
        if file_path not in self.files:
            self.files.append(file_path)
    
    def remove_file(self, file_path: str) -> None:
        """
        Remove a file from the directory.
        
        Args:
            file_path: The path of the file to remove
        """
        if file_path in self.files:
            self.files.remove(file_path)
    
    def add_subdirectory(self, directory_path: str) -> None:
        """
        Add a subdirectory to the directory.
        
        Args:
            directory_path: The path of the subdirectory to add
        """
        if directory_path not in self.subdirectories:
            self.subdirectories.append(directory_path)
    
    def remove_subdirectory(self, directory_path: str) -> None:
        """
        Remove a subdirectory from the directory.
        
        Args:
            directory_path: The path of the subdirectory to remove
        """
        if directory_path in self.subdirectories:
            self.subdirectories.remove(directory_path)
    
    def to_json(self) -> Dict[str, Any]:
        """
        Convert the directory content to a JSON representation.
        
        Returns:
            JSON representation of the directory content
        """
        return {
            "path": self.path,
            "files": self.files,
            "subdirectories": self.subdirectories
        }
    
    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'DirectoryContent':
        """
        Create a directory content object from a JSON representation.
        
        Args:
            data: JSON representation of the directory content
            
        Returns:
            DirectoryContent instance
        """
        return cls(
            data["path"],
            data.get("files", []),
            data.get("subdirectories", [])
        )


class JSONMirrors:
    """Manages the JSON mirror representation of code files."""
    
    def __init__(self, root_path: str, mirror_path: Optional[str] = None):
        """
        Initialize a JSON mirrors container.
        
        Args:
            root_path: Path to the root directory of the source code
            mirror_path: Path to the directory where mirrors are stored
        """
        self.root_path = os.path.abspath(root_path)
        
        if mirror_path:
            self.mirror_path = os.path.abspath(mirror_path)
        else:
            self.mirror_path = os.path.join(self.root_path, ".architectum", "mirrors")
        
        os.makedirs(self.mirror_path, exist_ok=True)
        logger.info(f"Initialized JSONMirrors: root={self.root_path}, mirrors={self.mirror_path}")
    
    def get_mirror_path(self, source_path: str) -> str:
        """
        Get the path of the mirrored JSON file for a source code file.
        
        Args:
            source_path: Path to the source code file
            
        Returns:
            Path to the mirrored JSON file
        """
        rel_path = os.path.relpath(os.path.abspath(source_path), self.root_path)
        mirror_dir = os.path.join(self.mirror_path, os.path.dirname(rel_path))
        os.makedirs(mirror_dir, exist_ok=True)
        
        base_name = os.path.basename(rel_path)
        mirror_name = f"{base_name}.json"
        
        return os.path.join(mirror_dir, mirror_name)
    
    def get_mirrored_content(self, source_path: str) -> Optional[Union[FileContent, DirectoryContent]]:
        """
        Get the JSON representation of a source code file or directory.
        
        Args:
            source_path: Path to the source code file or directory
            
        Returns:
            FileContent or DirectoryContent object, or None if not found
        """
        mirror_path = self.get_mirror_path(source_path)
        
        if not os.path.exists(mirror_path):
            return None
        
        try:
            with open(mirror_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Determine if this is a file or directory content
            if "elements" in data:
                return FileContent.from_json(data)
            else:
                return DirectoryContent.from_json(data)
        except Exception as e:
            logger.error(f"Error reading mirrored content for {source_path}: {str(e)}")
            return None
    
    def update_mirrored_content(
        self, 
        source_path: str, 
        content: Union[FileContent, DirectoryContent]
    ) -> None:
        """
        Update the JSON representation of a source code file or directory.
        
        Args:
            source_path: Path to the source code file or directory
            content: FileContent or DirectoryContent object
        """
        mirror_path = self.get_mirror_path(source_path)
        
        try:
            with open(mirror_path, 'w', encoding='utf-8') as f:
                json.dump(content.to_json(), f, indent=2)
            
            logger.debug(f"Updated mirrored content for {source_path}")
        except Exception as e:
            logger.error(f"Error updating mirrored content for {source_path}: {str(e)}")
            raise FileError(f"Failed to update mirrored content: {str(e)}")
    
    def exists(self, source_path: str) -> bool:
        """
        Check if a mirrored file exists for the given source path.
        
        Args:
            source_path: Path to the source code file or directory
            
        Returns:
            True if a mirror exists, False otherwise
        """
        mirror_path = self.get_mirror_path(source_path)
        return os.path.exists(mirror_path)
    
    def remove(self, source_path: str) -> None:
        """
        Remove a mirrored file.
        
        Args:
            source_path: Path to the source code file or directory
        """
        mirror_path = self.get_mirror_path(source_path)
        
        if os.path.exists(mirror_path):
            os.remove(mirror_path)
            logger.debug(f"Removed mirrored content for {source_path}")
    
    def compute_file_hash(self, file_path: str) -> str:
        """
        Compute a hash of a file's content.
        
        Args:
            file_path: Path to the file
            
        Returns:
            SHA-256 hash of the file content
            
        Raises:
            FileError: If the file cannot be read
        """
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            return file_hash
        except Exception as e:
            raise FileError(f"Failed to compute hash for {file_path}: {str(e)}")
    
    def is_mirror_up_to_date(self, source_path: str) -> bool:
        """
        Check if a mirrored file is up to date with its source.
        
        Args:
            source_path: Path to the source code file
            
        Returns:
            True if the mirror is up to date, False otherwise
        """
        if not self.exists(source_path) or not os.path.isfile(source_path):
            return False
        
        try:
            content = self.get_mirrored_content(source_path)
            if not isinstance(content, FileContent) or not content.source_hash:
                return False
            
            current_hash = self.compute_file_hash(source_path)
            return content.source_hash == current_hash
        except Exception:
            return False
    
    def create_file_mirror(
        self,
        source_path: str,
        elements: Dict[str, CodeElement],
        imports: List[str]
    ) -> None:
        """
        Create a mirror for a source code file.
        
        Args:
            source_path: Path to the source code file
            elements: Dictionary mapping element names to CodeElement objects
            imports: List of imported file paths
        """
        abs_path = os.path.abspath(source_path)
        extension = os.path.splitext(abs_path)[1]
        source_hash = self.compute_file_hash(abs_path)
        
        file_content = FileContent(abs_path, extension, elements, imports, source_hash)
        self.update_mirrored_content(abs_path, file_content)
    
    def create_directory_mirror(
        self,
        source_path: str,
        files: List[str],
        subdirectories: List[str]
    ) -> None:
        """
        Create a mirror for a directory.
        
        Args:
            source_path: Path to the directory
            files: List of file paths in the directory
            subdirectories: List of subdirectory paths in the directory
        """
        abs_path = os.path.abspath(source_path)
        directory_content = DirectoryContent(abs_path, files, subdirectories)
        self.update_mirrored_content(abs_path, directory_content)
    
    def list_all_mirrors(self) -> List[str]:
        """
        List all mirrored files.
        
        Returns:
            List of mirrored file paths
        """
        result = []
        
        for root, _, files in os.walk(self.mirror_path):
            for file in files:
                if file.endswith('.json'):
                    mirror_path = os.path.join(root, file)
                    rel_path = os.path.relpath(mirror_path, self.mirror_path)
                    
                    # Convert back to source path format (remove .json extension)
                    source_rel_path = os.path.splitext(rel_path)[0]
                    source_path = os.path.join(self.root_path, source_rel_path)
                    
                    result.append(source_path)
        
        return result
    
    def scan_directory(self, directory_path: str) -> Tuple[List[str], List[str]]:
        """
        Scan a directory for files and subdirectories.
        
        Args:
            directory_path: Path to the directory
            
        Returns:
            Tuple containing (list of file paths, list of subdirectory paths)
        """
        abs_path = os.path.abspath(directory_path)
        
        if not os.path.isdir(abs_path):
            raise FileError(f"Not a directory: {abs_path}")
        
        files = []
        subdirectories = []
        
        for item in os.listdir(abs_path):
            item_path = os.path.join(abs_path, item)
            
            # Skip hidden files and directories
            if item.startswith('.'):
                continue
            
            if os.path.isfile(item_path):
                files.append(item_path)
            elif os.path.isdir(item_path):
                subdirectories.append(item_path)
        
        return files, subdirectories
    
    def clear(self) -> None:
        """Clear all mirrored files."""
        for item in os.listdir(self.mirror_path):
            item_path = os.path.join(self.mirror_path, item)
            
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                import shutil
                shutil.rmtree(item_path)
        
        logger.info("Cleared all JSONMirrors")
