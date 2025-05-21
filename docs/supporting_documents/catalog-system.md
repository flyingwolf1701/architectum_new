# Architectum Catalog System

This document details the catalog system used in Architectum to track and organize code elements for efficient comprehension by both AI agents and human developers.

## Overview

Architectum uses two complementary YAML catalog files to maintain a complete picture of the codebase:

1. **`project_catalog.yaml`**: A raw inventory of all files and their elements
2. **`feature_catalog.yaml`**: A feature-oriented view that maps code elements to features

These catalogs serve different purposes and are used together to enable powerful code comprehension capabilities.

## Project Catalog (`project_catalog.yaml`)

### Purpose

The `project_catalog.yaml` file serves as a canonical inventory of everything that exists in the codebase. It tracks:

- Every file path in the project
- All functions and classes contained in each file
- Processing status through the tracking block

### Key Characteristics

- **File-Centric Organization**: Each entry represents a single file
- **Comprehensive Inventory**: Lists all files, functions, and classes
- **No Feature Context**: Doesn't include information about which features a file relates to
- **Mandatory Tracking Block**: Every file must include a tracking block
- **No Duplication**: Each file appears exactly once in this catalog

### Structure

```yaml
- path: "src/utils/time.js"
  functions:
    - "formatDate"
    - "parseTimestamp"
  tracking:
    json_representation: false
    system_map_updated: false

- path: "src/models/user.js"
  classes:
    - "User"
    - "UserSettings"
  tracking:
    json_representation: false
    system_map_updated: false
```

### Required Fields

- **`path`**: The relative path to the file from the project root
- **`functions`**: List of function names in the file (empty array if none)
- **`classes`**: List of class names in the file (empty array if none)
- **`tracking`**: Status block with processing flags
  - **`json_representation`**: Whether a JSON Mirror has been generated for this file
  - **`system_map_updated`**: Whether this file has been added to the System Map

### Implementation Details

The project catalog is managed by the `ProjectCatalog` class, which provides methods for:

- Loading and saving the catalog
- Adding, updating, and removing file entries
- Querying files and their elements
- Updating tracking status

## Feature Catalog (`feature_catalog.yaml`)

### Purpose

The `feature_catalog.yaml` file organizes code by feature rather than by file. It provides context for focused tasks like refactors or comprehensive understanding of specific features.

### Key Characteristics

- **Feature-Centric Organization**: Entries are grouped by feature
- **Cross-Cutting View**: A single file can appear in multiple features
- **No Tracking Block**: Feature entries don't require tracking metadata
- **Focused Content**: Contains only classes and methods, no extraneous metadata

### Structure

```yaml
- feature: "User Authentication"
  files:
    - path: "src/auth/login.js"
      functions:
        - "validateCredentials"
        - "createSession"
    - path: "src/models/user.js"
      classes:
        - "User"
        - "AuthenticationService"
          methods:
            - "verify"
            - "generateToken"

- feature: "Permissions System"
  files:
    - path: "src/auth/permissions.js"
      functions:
        - "canAccess"
        - "getUserPermissions"
    - path: "src/models/user.js"
      classes:
        - "User"
          methods:
            - "hasRole"
            - "getRoles"
```

### Required Fields

- **`feature`**: The name of the feature
- **`files`**: List of file entries related to this feature
  - **`path`**: The relative path to the file from the project root
  - **`functions`**: List of function names in this file that are part of this feature
  - **`classes`**: List of class entries in this file that are part of this feature
    - Class name
    - **`methods`**: List of methods in this class that are part of this feature

### Implementation Details

The feature catalog is managed by the `FeatureCatalog` class, which provides methods for:

- Loading and saving the catalog
- Adding, updating, and removing feature entries
- Querying features and their related code elements
- Generating feature-based views of the codebase

## Catalog Comparison

| Purpose | File Name | Structure By | Tracking Block | Can Duplicate File Entries? |
|---------|-----------|--------------|---------------|----------------------------|
| Raw inventory | `project_catalog.yaml` | File | ✅ Required | 🚫 No |
| Task context mapping | `feature_catalog.yaml` | Feature | 🚫 Not needed | ✅ Yes |

## Usage Workflows

### 1. Codebase Analysis

When analyzing a codebase, Architectum:

1. Scans all files to generate the initial `project_catalog.yaml`
2. Sets all tracking flags to `false`
3. Processes each file to generate JSON Mirrors and update the System Map
4. Updates tracking flags to `true` as files are processed

### 2. Feature Organization

Features can be organized in `feature_catalog.yaml`:

1. Manually by the user or AI assistant
2. By analyzing code patterns, naming conventions, and relationships
3. Through an interactive process of grouping related functionality

### 3. Blueprint Generation

When generating blueprints for AI consumption:

1. **Path-based blueprint**: Uses the directory structure and the `project_catalog.yaml` to identify all relevant files
2. **Method-based blueprint**: Uses the `feature_catalog.yaml` to find all methods related to a specific feature or task

## Integration with System Map and JSON Mirrors

The catalog system works in conjunction with the System Map and JSON Mirrors:

1. The `project_catalog.yaml` tracks which files have been processed into JSON Mirrors and added to the System Map
2. The `feature_catalog.yaml` helps create focused views of the System Map for specific features
3. Together, they enable efficient blueprint generation without scanning the entire codebase repeatedly
