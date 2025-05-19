# Story E7.2: Create User Documentation and CLI Guide

## Status: Draft

## Story

- As an end user of Architectum
- I want clear, comprehensive user documentation and CLI guide
- So that I can effectively use Architectum to analyze and understand codebases

## Dependencies

- Story 1.6 (Expose Blueprint Generation via Initial API/CLI) must be completed
- Story 7.1 (Documentation Framework) must be completed
- CLI functionality must be implemented and stable

## Acceptance Criteria (ACs)

- AC1: User documentation includes a clear "Getting Started" guide
- AC2: Each CLI command has detailed documentation with examples
- AC3: Blueprint types and their purposes are clearly explained
- AC4: Common workflows are documented with step-by-step instructions
- AC5: Error messages and troubleshooting steps are documented
- AC6: Documentation is accessible in HTML format and via --help commands
- AC7: User feedback indicates the documentation is clear and helpful

## Tasks / Subtasks

- [ ] Create "Getting Started" guide (AC: 1)
  - [ ] Document installation process
  - [ ] Explain core concepts (Relationship Map, JSON Mirrors, Blueprints)
  - [ ] Provide basic usage examples
  - [ ] Explain project setup requirements
- [ ] Document CLI commands (AC: 2, 6)
  - [ ] Create comprehensive command reference
  - [ ] Document all options and flags
  - [ ] Provide example command invocations
  - [ ] Ensure --help output is informative and complete
- [ ] Create blueprint type explanations (AC: 3)
  - [ ] Document File-Based Blueprints with examples
  - [ ] Document Component-Based Blueprints with examples
  - [ ] Document Feature Blueprints with examples
  - [ ] Document Temporary Blueprints with examples
  - [ ] Explain when to use each blueprint type
- [ ] Document common workflows (AC: 4)
  - [ ] Create "Analyzing a New Codebase" walkthrough
  - [ ] Create "Tracking Code Changes" workflow
  - [ ] Create "Documenting Features" workflow
  - [ ] Create "Using Blueprints with AI Assistants" guide
- [ ] Create troubleshooting guide (AC: 5)
  - [ ] Document common error messages and their solutions
  - [ ] Create FAQ section for common issues
  - [ ] Provide diagnostic steps for unclear errors
  - [ ] Include performance optimization tips
- [ ] Conduct user testing (AC: 7)
  - [ ] Create documentation feedback survey
  - [ ] Recruit testers to use documentation
  - [ ] Collect and analyze feedback
  - [ ] Implement improvements based on feedback

## Dev Technical Guidance

- Use clear, concise language without unnecessary jargon
- Include screenshots or diagrams where helpful
- Structure documentation in a logical, task-oriented manner
- Follow technical writing best practices for clarity
- Test documentation with new users to identify unclear sections
- Ensure error messages in the application match those in documentation
- Use a consistent voice and terminology throughout

## Story Progress Notes

### Agent Model Used: `Claude 3.7 Sonnet`

### Completion Notes List
- None yet

### Change Log
- Initial draft created
