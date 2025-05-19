# Sphinx Documentation Setup

## Overview

Architectum uses Sphinx for comprehensive API documentation generation. This setup creates auto-generated API documentation from docstrings while also supporting manual documentation pages.

## Setup Instructions

1. Install Sphinx and extensions:
```bash
uv add sphinx sphinx-rtd-theme sphinx-autodoc-typehints sphinx-click
```

2. Initialize Sphinx documentation:
```bash
mkdir -p docs/sphinx
cd docs/sphinx
sphinx-quickstart
```

3. Configure `conf.py`:
```python
# Add to extensions list
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
    'sphinx_autodoc_typehints',
    'sphinx_click',
]

# Set theme
html_theme = 'sphinx_rtd_theme'

# Add paths
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# Configure autodoc
autodoc_member_order = 'bysource'
autoclass_content = 'both'
autodoc_typehints = 'description'
```

## Documentation Structure

```
docs/
├── sphinx/
│   ├── _build/            # Generated documentation
│   ├── api/               # API documentation
│   │   ├── models.rst     # Data models documentation
│   │   ├── parsers.rst    # Parsers documentation
│   │   ├── blueprints.rst # Blueprint types documentation
│   │   └── cli.rst        # CLI documentation
│   ├── user/              # User documentation
│   │   ├── getting-started.rst
│   │   ├── cli-usage.rst
│   │   └── blueprint-types.rst
│   ├── dev/               # Developer documentation
│   │   ├── contributing.rst
│   │   ├── architecture.rst
│   │   └── testing.rst
│   ├── conf.py            # Sphinx configuration
│   ├── index.rst          # Main index
│   └── Makefile           # Build commands
```

## Documentation Generation

1. Generate API documentation:
```bash
cd docs/sphinx
sphinx-apidoc -o api/ ../../arch_blueprint_generator
```

2. Build HTML documentation:
```bash
cd docs/sphinx
make html
```

3. Build PDF documentation (optional):
```bash
cd docs/sphinx
make latexpdf
```

## Docstring Format

Use Google-style docstrings for all code:

```python
def example_function(param1: str, param2: int) -> bool:
    """Short description of the function.
    
    More detailed description of what this function does, how to use it,
    and any important notes.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is not an integer
        
    Examples:
        >>> example_function("test", 42)
        True
    """
```

## Automating Documentation

Add a CI job to build documentation on each commit:
```yaml
docs-build:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.13'
    - name: Install dependencies
      run: |
        python -m pip install uv
        uv install sphinx sphinx-rtd-theme sphinx-autodoc-typehints sphinx-click
        uv install -e .
    - name: Build documentation
      run: |
        cd docs/sphinx
        sphinx-apidoc -o api/ ../../arch_blueprint_generator
        make html
    - name: Upload documentation
      uses: actions/upload-artifact@v3
      with:
        name: documentation
        path: docs/sphinx/_build/html/
```
