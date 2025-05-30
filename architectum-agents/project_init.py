#!/usr/bin/env python3
"""
Architectum Project Initialization Script
Creates the complete product-docs structure for new projects.
"""

import os
import sys
from pathlib import Path
import yaml

def create_directory_structure():
    """Create the product-docs directory structure."""
    base_path = Path("product-docs")
    
    directories = [
        "catalogs",
        "core_documents", 
        "epics",
        "supporting_documents"
    ]
    
    for directory in directories:
        (base_path / directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {base_path / directory}")

def create_project_checklist():
    """Create the master project checklist YAML file."""
    checklist_data = {
        "project_status": {
            "current_phase": "initialization",
            "last_updated": "auto-generated",
            "agent_context": "project_planner"
        },
        "phases": {
            "1_ideation": {
                "status": "pending",
                "artifacts": ["project-brief.md"],
                "completed": False
            },
            "2_requirements": {
                "status": "pending", 
                "artifacts": ["prd.md"],
                "completed": False
            },
            "3_architecture": {
                "status": "pending",
                "artifacts": ["architecture.md"],
                "completed": False
            },
            "4_epic_breakdown": {
                "status": "pending",
                "artifacts": ["epic-*.md files"],
                "completed": False
            },
            "5_story_preparation": {
                "status": "pending",
                "artifacts": ["story-*.md files"],
                "completed": False
            },
            "6_doc_sharding": {
                "status": "pending",
                "artifacts": ["supporting_documents/*"],
                "completed": False
            },
            "7_ready_for_dev": {
                "status": "pending",
                "artifacts": ["all artifacts complete"],
                "completed": False
            }
        },
        "current_epic": None,
        "current_story": None,
        "notes": []
    }
    
    checklist_path = Path("product-docs/project-checklist.yaml")
    with open(checklist_path, 'w') as f:
        yaml.dump(checklist_data, f, default_flow_style=False, sort_keys=False)
    print(f"✓ Created {checklist_path}")

def create_catalog_files():
    """Create initial catalog YAML files."""
    
    # Project catalog structure
    project_catalog = {
        "files": []
    }
    
    # Feature catalog structure  
    feature_catalog = {
        "features": []
    }
    
    # Write catalog files
    catalogs_path = Path("product-docs/catalogs")
    
    with open(catalogs_path / "project_catalog.yaml", 'w') as f:
        yaml.dump(project_catalog, f, default_flow_style=False)
    print(f"✓ Created {catalogs_path / 'project_catalog.yaml'}")
    
    with open(catalogs_path / "feature_catalog.yaml", 'w') as f:
        yaml.dump(feature_catalog, f, default_flow_style=False)
    print(f"✓ Created {catalogs_path / 'feature_catalog.yaml'}")

def create_template_files():
    """Create template files for core documents."""
    core_docs_path = Path("product-docs/core_documents")
    
    # Project brief template
    project_brief_template = """# Project Brief: {Project Name}

## Problem Statement
{Describe the core problem being solved}

## Vision & Goals
- **Vision:** {High-level desired future state}
- **Primary Goals:**
  - Goal 1: {Specific, measurable goal}
  - Goal 2: {Another specific goal}

## Target Users
{Describe primary users and their characteristics}

## Key Features (MVP Scope)
- Feature 1: {Core functionality}
- Feature 2: {Essential capability}

## Known Constraints
- Technical: {Any known limitations}
- Timeline: {Time constraints}
- Budget: {Resource constraints}

## Success Metrics
{How will success be measured}
"""
    
    # PRD template
    prd_template = """# {Project Name} Product Requirements Document

## Status: Draft

## Goals & Context
{Copy from project brief and expand}

## Functional Requirements (MVP)
{Core functionality requirements}

## Non-Functional Requirements
{Performance, security, scalability requirements}

## Technical Assumptions
{Technology choices and constraints}

## Epic Overview
{High-level epic breakdown}

## Out of Scope (Post-MVP)
{Features deliberately excluded from MVP}
"""
    
    # Architecture template
    architecture_template = """# {Project Name} Architecture Document

## Status: Draft

## Technical Summary
{Brief overview of architecture approach}

## High-Level Overview
{System architecture and key components}

## Technology Stack
{Definitive technology selections}

## Component Architecture
{Detailed component breakdown}

## Data Models
{Core data structures and relationships}

## API Design
{API contracts and interfaces}

## Security & Compliance
{Security approach and requirements}

## Testing Strategy
{Testing approach and coverage}

## Deployment & Operations
{Deployment and operational considerations}
"""
    
    # Write template files
    templates = [
        ("project-brief.md", project_brief_template),
        ("prd.md", prd_template), 
        ("architecture.md", architecture_template)
    ]
    
    for filename, content in templates:
        with open(core_docs_path / filename, 'w') as f:
            f.write(content)
        print(f"✓ Created {core_docs_path / filename}")

def create_index_file():
    """Create the master index.md file."""
    index_content = """# {Project Name} Documentation Index

## Project Status
See `project-checklist.yaml` for current phase and progress.

## Core Documents
- [Project Brief](core_documents/project-brief.md) - Initial project definition
- [Product Requirements](core_documents/prd.md) - Detailed requirements and epics  
- [Architecture](core_documents/architecture.md) - Technical architecture and design

## Epics & Stories
{Epic directories will be created during planning phase}

## Supporting Documents
{Detailed documentation will be generated during sharding phase}

## Catalogs
- [Project Catalog](catalogs/project_catalog.yaml) - File and component inventory
- [Feature Catalog](catalogs/feature_catalog.yaml) - Feature-to-code mapping

---
*This index is automatically maintained by Architectum agents*
"""
    
    index_path = Path("product-docs/index.md")
    with open(index_path, 'w') as f:
        f.write(index_content)
    print(f"✓ Created {index_path}")

def main():
    """Main initialization function."""
    print("🚀 Initializing Architectum project structure...")
    
    # Check if product-docs already exists
    if Path("product-docs").exists():
        response = input("product-docs/ directory already exists. Continue? (y/N): ")
        if response.lower() != 'y':
            print("❌ Initialization cancelled.")
            sys.exit(1)
    
    # Create structure
    create_directory_structure()
    create_project_checklist()
    create_catalog_files()
    create_template_files()
    create_index_file()
    
    print("\n✅ Architectum project structure initialized successfully!")
    print("\nNext steps:")
    print("1. Run the project_planner agent")
    print("2. Start with ideation and project brief creation")
    print("3. Follow the project-checklist.yaml for progress tracking")
    print("\nProject structure created in: product-docs/")

if __name__ == "__main__":
    main()