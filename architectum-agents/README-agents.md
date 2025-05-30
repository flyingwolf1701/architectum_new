# Architectum Agents

**Token-efficient AI-driven development methodology**  
*Get excellent output with fewer tokens through streamlined agents and smart automation.*

## Quick Start

### 1. Initialize New Project
```bash
python init_project.py
```
Creates `product-docs/` structure with templates and tracking files.

### 2. Run Project Planner
Use `project_planner.md` agent to guide from idea → development-ready stories.

### 3. Develop Stories  
Use `AGENT.md` for focused story implementation.

### 4. Validate Completion
Use `code_reviewer.md` for story validation and quality assurance.

## Core Philosophy

**Simplicity Over Complexity**
- 3 focused agents instead of 8+ specialized personas
- Scripts for automation instead of agent tokens
- Single source of truth for progress tracking
- Token-efficient documentation that serves dev agents

**Quality Without Bloat**
- Maintain excellent output quality
- Reduce token usage by 60-80%
- Clear handoff points between agents
- Automated progress tracking

## Agent Architecture

### 🎯 Project Planner (`project_planner.md`)
**Scope:** Idea → Development-Ready Stories  
**Phases:** Ideation, Requirements, Architecture, Epic Breakdown, Story Prep, Doc Sharding

- Handles complete planning workflow
- Manages `project-checklist.yaml` progress tracking
- Creates all core documents and supporting materials
- Prepares token-efficient context for dev agents

### ⚡ Dev Agent (`AGENT.md`) 
**Scope:** Individual Story Implementation  
**Focus:** Efficient, focused development with catalog-driven navigation

- Implements one story at a time
- Maintains catalog system accuracy
- Generates comprehensive tests (≥80% coverage)
- Creates QA testing guides
- Updates progress tracking

### 🔍 Code Reviewer (`code_reviewer.md`)
**Scope:** Story Validation & Quality Assurance  
**Focus:** Automated testing, catalog verification, quality validation

- Runs automated test suites
- Validates catalog accuracy
- Checks compliance with standards
- Generates validation reports
- Manages story approval workflow

## Project Structure

```
product-docs/
├── catalogs/
│   ├── project_catalog.yaml      # File/component inventory
│   └── feature_catalog.yaml      # Feature-to-code mapping
├── core_documents/
│   ├── project-brief.md          # Initial project definition
│   ├── prd.md                    # Product requirements & epics
│   └── architecture.md           # Technical architecture
├── epics/
│   ├── epic_1/
│   │   ├── epic-1.md            # Epic definition
│   │   ├── story-1.1.md         # Individual stories
│   │   └── story-1.2.md
│   └── epic_2/
├── supporting_documents/         # Token-efficient dev context
│   ├── api-reference.md
│   ├── data-models.md
│   ├── operational-guidelines.md
│   └── tech-stack.md
├── index.md                      # Navigation hub
└── project-checklist.yaml       # Single source of truth
```

## Progress Tracking

### Master Checklist (`project-checklist.yaml`)
**Single source of truth** for:
- Current phase and active agent
- Completion status of all phases
- Story-level progress tracking
- Session continuity across agents
- Agent handoff logging

### Benefits:
- **Session Continuity:** Resume work across multiple sessions
- **Clear Handoffs:** Know exactly where you are in the process
- **Progress Visibility:** Track completion at all levels
- **Agent Context:** Each agent knows what's been done

## Key Improvements Over BMAD

### Token Efficiency
- **3 agents** instead of 8+ personas
- **No personality traits** - focus on functionality
- **Automated scripts** replace repetitive agent tasks
- **Concise documentation** optimized for AI consumption

### Simplified Workflow
```
Init Script → Project Planner → Dev Agent → Code Reviewer
     ↓              ↓              ↓           ↓
Structure    All Planning    Implementation  Validation
Created      Complete        Story-by-Story  & Approval
```

### Quality Maintenance
- **Same excellent output** with fewer tokens
- **Comprehensive testing** (≥80% coverage requirement)
- **Catalog system** for efficient code navigation
- **Automated validation** with clear quality gates

## Catalog System

### Purpose
Enable efficient AI agent navigation without extensive code scanning.

### Project Catalog (`project_catalog.yaml`)
```yaml
files:
  - path: "src/auth/login.js"
    functions: ["validateCredentials", "createSession"] 
    classes: ["AuthService"]
    tracking:
      json_representation: false
      system_map_updated: false
```

### Feature Catalog (`feature_catalog.yaml`) 
```yaml
features:
  - name: "User Authentication"
    files:
      - path: "src/auth/login.js"
        functions: ["validateCredentials"]
        classes:
          - name: "AuthService"
            methods: ["login", "logout"]
```

### Benefits
- **Fast Navigation:** Agents find relevant code instantly
- **Dependency Tracking:** Understand code relationships
- **Change Impact:** Know what's affected by modifications
- **Quality Assurance:** Verify all changes are cataloged

## Usage Patterns

### Starting New Project
1. Run `python init_project.py`
2. Activate `project_planner.md` agent
3. Follow guided workflow through all planning phases
4. Handoff to development when stories are ready

### Resuming Work
1. Check `product-docs/project-checklist.yaml` for current status
2. Activate appropriate agent based on current phase
3. Agent automatically resumes from checklist state

### Development Phase
1. Use `AGENT.md` to implement stories one at a time
2. Dev agent maintains catalogs and runs tests
3. Use `code_reviewer.md` to validate completion
4. Repeat until all stories complete

## Migration from BMAD

### What's Kept
- Epic/story structure and quality
- Comprehensive documentation approach
- Testing requirements and standards
- Checklist-driven validation

### What's Simplified
- Single project planner instead of multiple planning agents
- YAML-based progress tracking instead of complex orchestration
- Scripts for automation instead of token-heavy agents
- Focused agent roles instead of personality-driven personas

### What's Improved
- 60-80% reduction in token usage
- Clearer handoff points and progress visibility
- Better session continuity
- Faster project initialization

## Success Metrics

- **Token Efficiency:** 60-80% reduction while maintaining quality
- **Setup Speed:** Project ready in minutes, not hours
- **Quality Maintenance:** Same comprehensive outputs
- **Developer Experience:** Clear, actionable development context
- **Progress Visibility:** Always know current status and next steps

---

*Architectum Agents: Maximum output, minimum tokens.*