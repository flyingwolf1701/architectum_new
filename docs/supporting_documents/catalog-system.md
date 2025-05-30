# Architectum Catalog System

This document details the catalog system used in Architectum to track and organize code elements for efficient comprehension by both AI agents and human developers.

## Overview

Architectum uses three complementary YAML catalog files to maintain a complete picture of the codebase:

1. **`project_catalog.yaml`**: A raw inventory of all files and their elements
2. **`feature_catalog.yaml`**: A feature-oriented view that maps code elements to features
3. **`tests_catalog.yaml`**: A comprehensive test inventory and coverage mapping

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
files:
  - path: "src/utils/time.js"
    functions:
      - "formatDate"
      - "parseTimestamp"
    classes: []
    tracking:
      json_representation: false
      system_map_updated: false

  - path: "src/models/user.js"
    functions: []
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
features:
  - feature: "User Authentication"
    files:
      - path: "src/auth/login.js"
        functions:
          - "validateCredentials"
          - "createSession"
      - path: "src/models/user.js"
        classes:
          - name: "User"
            methods:
              - "authenticate"
              - "updatePassword"
          - name: "AuthenticationService"
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
          - name: "User"
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
    - **`name`**: Class name
    - **`methods`**: List of methods in this class that are part of this feature

## Tests Catalog (`tests_catalog.yaml`)

### Purpose

The `tests_catalog.yaml` file provides comprehensive test inventory and coverage mapping. It tracks:

- All test files and their test functions
- Clear descriptions of what each test validates
- Mapping between tests and the stories that created them
- Coverage targets showing what code each test exercises

### Key Characteristics

- **Test-Centric Organization**: Entries grouped by test file
- **Story Traceability**: Links tests back to the stories that created them
- **Coverage Mapping**: Shows what production code each test covers
- **Documentation**: Clear descriptions of test purpose and scope

### Structure

```yaml
tests:
  - test_file: "tests/auth/test_login.py"
    test_functions:
      - name: "test_valid_login_success"
        description: "Verifies successful login with valid email and password"
        story: "story-2.1"
        coverage_targets:
          - "src/auth/login.py::validateCredentials"
          - "src/auth/session.py::createSession"
      - name: "test_invalid_password_fails"
        description: "Ensures login fails gracefully with incorrect password"
        story: "story-2.1"
        coverage_targets:
          - "src/auth/login.py::validateCredentials"
      - name: "test_account_lockout_after_attempts"
        description: "Verifies account locks after 5 failed login attempts"
        story: "story-2.3"
        coverage_targets:
          - "src/auth/login.py::validateCredentials"
          - "src/auth/security.py::trackFailedAttempts"

  - test_file: "tests/api/test_user_endpoints.py"
    test_functions:
      - name: "test_create_user_success"
        description: "Tests successful user creation via POST /api/users"
        story: "story-1.3"
        coverage_targets:
          - "src/api/users.py::create_user"
          - "src/models/user.py::User.__init__"
      - name: "test_create_user_duplicate_email"
        description: "Ensures 409 error when creating user with existing email"
        story: "story-1.3"
        coverage_targets:
          - "src/api/users.py::create_user"
          - "src/models/user.py::User.validate_unique_email"
```

### Required Fields

- **`test_file`**: The relative path to the test file from the project root
- **`test_functions`**: List of test function entries in this file
  - **`name`**: The exact test function name
  - **`description`**: Clear description of what this test validates
  - **`story`**: The story identifier that created this test (format: "story-X.Y")
  - **`coverage_targets`**: List of production code elements this test exercises
    - Format: "file_path::function_name" or "file_path::ClassName.method_name"

### Benefits of Tests Catalog

- **Test Visibility**: See all tests and their purpose at a glance
- **Story Traceability**: Track which story created each test
- **Coverage Mapping**: Understand what production code is tested
- **Test Documentation**: Clear descriptions prevent confusion
- **Maintenance**: Identify orphaned tests or coverage gaps
- **Quality Assurance**: Verify comprehensive test coverage

## Catalog Comparison

| Purpose | File Name | Structure By | Tracking Block | Can Duplicate Entries? | Story Link |
|---------|-----------|--------------|---------------|------------------------|------------|
| Raw inventory | `project_catalog.yaml` | File | ✅ Required | 🚫 No | 🚫 No |
| Feature mapping | `feature_catalog.yaml` | Feature | 🚫 Not needed | ✅ Yes | 🚫 No |
| Test coverage | `tests_catalog.yaml` | Test file | 🚫 Not needed | 🚫 No | ✅ Yes |

## Agent Usage Workflows

### 1. During Story Implementation

When implementing a story, agents must:

1. **Check project catalog** to understand existing code structure
2. **Check feature catalog** to see related functionality
3. **Update project catalog** with any new files/functions/classes created
4. **Update feature catalog** with new elements that belong to features
5. **Update tests catalog** with all tests written for the story

### 2. Finding Relevant Code

To find code related to a task:

1. **Use feature catalog** to identify all files in a feature
2. **Use project catalog** to get complete file inventories
3. **Use tests catalog** to understand test coverage and validation

### 3. Test Coverage Analysis

To understand test coverage:

1. **Review tests catalog** for coverage targets
2. **Cross-reference with project catalog** to identify untested code
3. **Use story links** to understand test creation context

## Catalog Maintenance Rules

### For All Agents

1. **Immediate Updates**: Update all relevant catalogs when making code changes
2. **Accurate Entries**: Ensure catalog entries match actual code structure
3. **Complete Coverage**: Every file must be in project catalog, every test in tests catalog
4. **Story Linking**: All tests must reference the story that created them

### Validation Checks

Before story completion, verify:

- [ ] All new files added to `project_catalog.yaml`
- [ ] All modified files updated in `project_catalog.yaml`
- [ ] Feature relationships updated in `feature_catalog.yaml`
- [ ] All tests documented in `tests_catalog.yaml` with proper descriptions
- [ ] Test coverage targets accurately reflect what code is tested
- [ ] Story references are correct in tests catalog

## Integration with Development Workflow

The three-catalog system enables:

1. **Efficient Code Discovery**: Find relevant code without scanning entire codebase
2. **Impact Analysis**: Understand what's affected by changes
3. **Test Coverage Verification**: Ensure comprehensive testing
4. **Story Traceability**: Link code and tests back to requirements
5. **Quality Assurance**: Systematic validation of catalog accuracy