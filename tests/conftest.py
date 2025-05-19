"""
Pytest configuration for Architectum Blueprint Generator tests.
"""

import pytest
import os
import tempfile
import shutil

from arch_blueprint_generator.models.relationship_map import RelationshipMap
from arch_blueprint_generator.models.json_mirrors import JSONMirrors, CodeElement, FileContent


@pytest.fixture
def relationship_map():
    """Fixture for creating a relationship map."""
    return RelationshipMap()


@pytest.fixture
def temp_dir():
    """Fixture for creating a temporary directory."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def json_mirrors(temp_dir):
    """Fixture for creating a JSON mirrors container."""
    root_path = os.path.join(temp_dir, "root")
    mirror_path = os.path.join(temp_dir, "mirrors")
    
    os.makedirs(root_path, exist_ok=True)
    
    return JSONMirrors(root_path, mirror_path)


@pytest.fixture
def test_file(temp_dir):
    """Fixture for creating a test file."""
    root_path = os.path.join(temp_dir, "root")
    file_path = os.path.join(root_path, "test_file.py")
    
    os.makedirs(root_path, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("def test_function():\n    return 'test'")
    
    return file_path
