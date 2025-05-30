# Story Update Procedures for Agents

This document provides step-by-step procedures for properly updating story files during implementation and completion.

## Story Lifecycle States

Stories progress through these states:
- `Draft` → `Approved` → `In-Progress` → `Review` → `Completed`

## Required Story Updates During Implementation

### 1. Starting a Story (Initialization)

When picking up a story:
1. **Verify Status**: Ensure story status is `Approved` 
2. **Update Status**: Change to `Status: In-Progress`
3. **Add Start Notes**: Add entry to Change Log with start date

```markdown
## Status: In-Progress

### Change Log
- 2025-01-XX: Started implementation (Agent: Claude 3.7 Sonnet)
```

### 2. During Implementation (Progress Updates)

As you complete tasks:
1. **Mark Tasks Complete**: Change `[ ]` to `[x]` for completed tasks
2. **Update Acceptance Criteria**: Mark ACs as complete with ✅
3. **Document Decisions**: Add important implementation decisions to notes

```markdown
## Acceptance Criteria (ACs)
- AC1: ✅ The new module/package is created and buildable
- AC2: ✅ The Relationship Map model is implemented
- AC3: [ ] JSON Mirrors structure is implemented (IN PROGRESS)
```

### 3. Catalog System Updates (CRITICAL)

**EVERY file change must update catalogs:**

#### For New Files:
Add to `docs/catalogs/project_catalog.yaml`:
```yaml
- path: "path/to/new/file.py"
  classes:
    - "NewClass"
  functions:
    - "new_function"
  tracking:
    json_representation: false
    system_map_updated: false
```

#### For New Features:
Add to `docs/catalogs/feature_catalog.yaml`:
```yaml
- feature: "Feature Name"
  files:
    - path: "path/to/file.py"
      classes:
        - name: "ClassName"
          methods:
            - "method1"
            - "method2"
      functions:
        - "function_name"
```

### 4. Pre-Completion Requirements (CRITICAL)

Before marking a story complete, you MUST:

#### A. Create QA Testing Guide
Add comprehensive testing instructions:

```markdown
### QA Testing Guide
To verify this implementation:

1. **Project Structure**:
   - Verify the module is properly structured
   - Check that required files are present

2. **Core Functionality**:
   - Test key operations work as expected
   - Verify error handling

3. **Run Tests**:
   ```bash
   # Specific commands to test the implementation
   python -m pytest tests/
   ```

4. **Verify Acceptance Criteria**:
   - AC1: Check that [specific verification steps]
   - AC2: Verify that [specific verification steps]
```

#### B. Add Completion Notes
Document what was implemented:

```markdown
### Completion Notes List
- Successfully implemented [key features]
- Made design decisions about [important choices]
- Added [testing/documentation elements]
- Challenges encountered: [any issues resolved]
```

#### C. Update Change Log
Add completion entry:

```markdown
### Change Log
- 2025-01-XX: Started implementation (Agent: Claude 3.7 Sonnet)
- 2025-01-XX: Completed implementation with all ACs met
- 2025-01-XX: Added QA testing guide and completion notes
```

### 5. Final Story Completion

When all work is done:
1. **Update Status**: Change to `Status: Review`
2. **Verify All Tasks**: Ensure all `[x]` are marked complete
3. **Verify All ACs**: Ensure all have ✅
4. **Verify Catalogs**: Ensure all code changes are reflected in catalogs
5. **Present DoD Report**: Show completed Definition of Done checklist

```markdown
## Status: Review

## Tasks / Subtasks
- [x] All tasks completed

## Acceptance Criteria (ACs)
- AC1: ✅ All criteria met
- AC2: ✅ All criteria met
```

## Critical Rules for Agents

### ❌ Never Skip These Steps:
1. **Catalog Updates**: Every file change MUST update both catalogs
2. **QA Testing Guide**: Every story MUST have verification steps
3. **Status Updates**: Keep status current throughout implementation
4. **Task Tracking**: Mark tasks complete as you finish them

### ✅ Always Include:
1. **Agent Model Used**: Document which AI model completed the work
2. **Specific Test Commands**: Exact commands to verify the implementation
3. **Implementation Details**: Key decisions and approaches used
4. **Catalog Entries**: All new/modified files properly cataloged

## Example Complete Story Structure

```markdown
# Story X.Y: Title

## Status: Completed

## Story
- As a [role]
- I want [goal]  
- So that [benefit]

## Acceptance Criteria (ACs)
- AC1: ✅ Criteria met
- AC2: ✅ Criteria met

## Tasks / Subtasks
- [x] Task 1 completed
- [x] Task 2 completed

## Story Progress Notes

### Agent Model Used: `Claude 3.7 Sonnet`

### Completion Notes List
- Successfully implemented [features]
- Made design decisions about [choices]

### QA Testing Guide
To verify this implementation:
1. [Specific verification steps]
2. [Test commands to run]

### Change Log
- Start/completion dates and key milestones
```

This structure ensures stories are properly tracked and can be verified by users or other agents.
