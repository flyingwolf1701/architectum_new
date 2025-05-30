# Story 3.2: Implement Local Relationship Mapping for Methods

## Status: Approved

## Story

As an AI agent, I want Method-Based Blueprints to include comprehensive relationship mapping for the selected methods, so that I can understand how they interact with other code elements.

## Acceptance Criteria (ACs)

1. **AC1: Relationship Mapping Integration** - Method-Based Blueprints include relationship mapping for the specified methods.

2. **AC2: Bidirectional Relationships** - Both incoming and outgoing relationships are represented.

3. **AC3: Configurable Relationship Depth** - Relationship depth can be configured to control the scope of included relationships:
   ```yaml
   type: method
   name: auth-functions-blueprint
   relationship_depth: 2  # How many levels of relationships to include
   components:
     # ...
   ```

4. **AC4: Relationship Metadata** - Relationship metadata provides context for understanding the connections.

5. **AC5: Relationship Type Filtering** - Certain relationship types can be filtered if desired.

6. **AC6: Testing Requirements** - Comprehensive testing implemented:
   - At least 80% code coverage for the relationship mapping functionality
   - Implementation using pytest with relationship test fixtures
   - Snapshot testing showing different relationship depths
   - Configuration testing for different relationship depth settings
   - Filter testing for relationship type filtering
   - Metadata testing to verify relationship metadata is correctly included

## Tasks / Subtasks

- [ ] Task 1: Design Relationship Mapping Architecture (AC: 1, 2)
  - [ ] Subtask 1.1: Define relationship extraction interfaces for methods
  - [ ] Subtask 1.2: Design bidirectional relationship representation
  - [ ] Subtask 1.3: Create relationship metadata structure
  - [ ] Subtask 1.4: Design relationship traversal algorithms

- [ ] Task 2: Implement Relationship Discovery Logic (AC: 1, 2, 4)
  - [ ] Subtask 2.1: Implement incoming relationship detection
  - [ ] Subtask 2.2: Implement outgoing relationship detection
  - [ ] Subtask 2.3: Add relationship metadata extraction
  - [ ] Subtask 2.4: Integrate with existing relationship mapping system

- [ ] Task 3: Add Configurable Relationship Depth (AC: 3)
  - [ ] Subtask 3.1: Implement depth-limited relationship traversal
  - [ ] Subtask 3.2: Add YAML configuration for relationship depth
  - [ ] Subtask 3.3: Create depth validation and bounds checking
  - [ ] Subtask 3.4: Optimize performance for deep relationship queries

- [ ] Task 4: Implement Relationship Type Filtering (AC: 5)
  - [ ] Subtask 4.1: Define filterable relationship types
  - [ ] Subtask 4.2: Implement filtering logic
  - [ ] Subtask 4.3: Add YAML configuration for filtering
  - [ ] Subtask 4.4: Create filter validation system

- [ ] Task 5: Comprehensive Testing Implementation (AC: 6)
  - [ ] Subtask 5.1: Create relationship test fixtures
  - [ ] Subtask 5.2: Implement relationship mapping unit tests
  - [ ] Subtask 5.3: Create snapshot tests for different depths
  - [ ] Subtask 5.4: Test configuration options
  - [ ] Subtask 5.5: Test filtering functionality
  - [ ] Subtask 5.6: Verify metadata correctness

## Dev Technical Guidance

**Key Files to Create/Modify:**
- `arch_blueprint_generator/relationships/method_mapper.py` - Method relationship mapping
- `arch_blueprint_generator/relationships/depth_traversal.py` - Depth-limited traversal
- `arch_blueprint_generator/relationships/filters.py` - Relationship filtering
- Update `arch_blueprint_generator/blueprints/method_based.py` - Integrate relationship mapping

**Dependencies:**
- Story 3.1 (Method-Based Blueprint Logic) must be completed
- Story 2.2 (Enhance File-Based Blueprint with Cross-File Relationships) should be completed
- Requires established relationship mapping from Epic 1

**Technical Integration Points:**
- Leverage existing RelationshipMap from core framework
- Extend method-based blueprints with relationship data
- Integrate with YAML configuration system
- Maintain performance for large codebases

## Story Progress Notes

### Agent Model Used: `<To be filled by implementing agent>`

### Completion Notes List
{To be filled during implementation}

### Change Log
{To be updated during implementation}
