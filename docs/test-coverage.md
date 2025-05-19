# Test Coverage Requirements

## Overview

This document outlines the test coverage requirements for the Architectum project. All stories and components must adhere to these standards before being considered complete.

## Coverage Requirements

### Minimum Coverage Thresholds

- **Overall Code Coverage**: Minimum 80% line coverage across the codebase
- **Critical Component Coverage**: 90% coverage for core graph model and blueprint generators
- **Edge Case Coverage**: Explicit tests for error conditions and boundary cases

### Component-Specific Coverage

| Component | Minimum Coverage | Key Testing Focus |
|-----------|-----------------|-------------------|
| Graph Model | 90% | Node/relationship integrity, traversal operations |
| Blueprint Generators | 85% | Correct graph construction, detail level implementation |
| Parsers | 85% | Accurate extraction of code elements and relationships |
| CLI/API | 80% | Parameter validation, output formatting |
| Caching/Incremental Update | 85% | Change detection, partial regeneration |

## Implementation Guide

### Tracking Coverage

1. **Command**: Use `pytest --cov=arch_blueprint_generator tests/` to generate coverage reports
2. **HTML Reports**: Generate detailed HTML reports with `pytest --cov=arch_blueprint_generator --cov-report=html tests/`
3. **CI Integration**: Coverage reports must be generated as part of the CI process

### Story Completion Gate

1. Each story must achieve its component-specific coverage requirement before being considered complete
2. Coverage reports must be reviewed and attached to the story completion documentation
3. Exceptions to coverage requirements must be explicitly documented and approved

### Addressing Coverage Gaps

When coverage falls below requirements:

1. Identify uncovered code paths
2. Prioritize critical function coverage
3. Add tests for edge cases and error conditions
4. Document any code that is intentionally excluded from coverage with justification

## Exemptions

Exemptions from coverage requirements may be granted for:

1. Auto-generated code
2. Third-party integration points with limited testability
3. UI-specific code that requires specialized testing approaches

All exemptions must be documented and approved before the story can be considered complete.
