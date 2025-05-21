# Project Catalog

This document provides a file-centric inventory of all code elements in the project, serving as a comprehensive registry of the codebase's structure.

## Purpose

The Project Catalog serves as the canonical inventory of all files, functions, and classes in the codebase. It tracks which elements have been processed into the System Map and JSON Mirrors, ensuring complete coverage of the codebase.

## File Entries

### File: `path/to/file1.js`

**Functions:**
- `functionName1`
- `functionName2`

**Classes:**
- `ClassName1`
  - Methods: `methodName1`, `methodName2`

**Tracking Status:**
- JSON Representation: ✅ Generated
- System Map Updated: ✅ Updated

### File: `path/to/file2.py`

**Functions:**
- `function_name_1`
- `function_name_2`

**Classes:**
- `ClassName2`
  - Methods: `method_name_1`, `method_name_2`

**Tracking Status:**
- JSON Representation: ✅ Generated
- System Map Updated: ❌ Pending

## Usage

This catalog is used by:

1. The System Map and JSON Mirrors to track processing status
2. The Blueprint Generator to identify all files in specific directories
3. The `arch sync` command to determine which files need updating
4. The YAML parser to maintain the authoritative YAML representation

## Maintenance

This catalog should be updated whenever:

1. New files are added to the codebase
2. Existing files are modified (functions/classes added or removed)
3. Files are renamed or moved
4. The `arch sync` command is run

## Related Documents

- [Feature Catalog](./feature_catalog.md) - Provides a feature-centric view of the codebase
- [Catalog System](../supporting_documents/catalog-system.md) - Explains the overall catalog system
