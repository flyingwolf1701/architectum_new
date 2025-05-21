# Feature Catalog

This document provides a feature-oriented view of the codebase, organizing code elements by logical features rather than by their physical file locations.

## Purpose

The Feature Catalog serves as a map that associates code elements (files, functions, classes, methods) with the logical features they implement. This allows both AI agents and human developers to understand how functionality is distributed across the codebase's architecture.

## Feature Entries

### Feature: [Feature Name 1]

**Description:** Brief description of what this feature does and its purpose in the system.

**Files and Components:**
- `path/to/file1.js`
  - Functions: `functionName1`, `functionName2`
  - Classes: 
    - `ClassName1`
      - Methods: `methodName1`, `methodName2`
- `path/to/file2.py`
  - Functions: `function_name_3`, `function_name_4`
  - Classes:
    - `ClassName2`
      - Methods: `method_name_3`, `method_name_4`

### Feature: [Feature Name 2]

**Description:** Brief description of what this feature does and its purpose in the system.

**Files and Components:**
- `path/to/file3.ts`
  - Functions: `functionName5`, `functionName6`
  - Classes: 
    - `ClassName3`
      - Methods: `methodName5`, `methodName6`
- `path/to/file1.js` (Note: Same file can appear in multiple features)
  - Functions: `functionName7`
  - Classes:
    - `ClassName1`
      - Methods: `methodName7`

## Usage

This catalog is used by:

1. The Blueprint Generator to create feature-focused blueprints
2. AI agents to understand all code elements related to a specific feature
3. Developers to trace functionality across architectural boundaries

## Maintenance

This catalog should be updated whenever:

1. New features are added to the system
2. Existing features are modified or their implementation changes
3. Code is refactored in a way that changes feature associations

## Related Documents

- [Project Catalog](./project_catalog.md) - Provides a file-centric view of the codebase
- [Catalog System](../supporting_documents/catalog-system.md) - Explains the overall catalog system
