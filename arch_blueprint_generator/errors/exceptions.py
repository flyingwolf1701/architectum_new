"""
Custom exception classes for the arch_blueprint_generator module.
"""

from typing import Dict, Any, Optional


class ArchitectumError(Exception):
    """Base class for all Architectum exceptions."""
    pass


class ParseError(ArchitectumError):
    """Error while parsing code files."""
    pass


class BlueprintError(ArchitectumError):
    """Error while generating blueprints."""
    pass


class FileError(ArchitectumError):
    """Error related to file operations."""
    pass


class ModelError(ArchitectumError):
    """Error related to data models."""
    pass


class BusinessError(ArchitectumError):
    """Base class for business logic errors."""
    
    def __init__(self, code: str, message: str, details: Optional[Dict[str, Any]] = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(message)
