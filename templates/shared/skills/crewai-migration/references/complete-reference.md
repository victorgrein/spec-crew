# CrewAI Migration - Complete Reference

This document centralizes detailed reference material for `crewai-migration` and supports progressive disclosure during skill execution.

## Source Material

- Core skill file: `../SKILL.md`
- Legacy reference files:
  - `migration-reference.md`

## Section Index from SKILL.md

- What This Skill Does
- When to Use This Skill
- Quick Reference
-   Migration Types
-   Target Project Structure
- Crew to Flow Migration
-   Step 1: Create Flow Project Structure
-   Step 2: Move Existing Crew
-   Step 3: Update Crew Imports
-   Step 4: Create Flow
-   Step 5: Update pyproject.toml
- Code to YAML Migration
-   Before (Inline Code)
-   After (YAML + Decorators)
- Monolithic to Modular Migration
-   Step 1: Identify Logical Groups
-   Step 2: Extract Crews
-   Step 3: Extract Shared Tools
-   Step 4: Create Orchestrating Flow
- Version Upgrade
-   Step 1: Backup
-   Step 2: Update Dependencies
-   Step 3: Check Breaking Changes
-   Step 4: Update Code
-   Step 5: Test
- Migration Checklist
- Related Skills

## Essential Attributes

The following tables were extracted from `SKILL.md` and should be considered the canonical attribute and option index for this phase.

### Table 1

| Type | Description |
|------|-------------|
| Crew to Flow | Convert standalone crew to flow-based architecture |
| Code to YAML | Move inline definitions to YAML configuration |
| Monolithic to Modular | Break large crew into smaller components |
| Version Upgrade | Update to latest CrewAI version |

## Edge Cases and Limitations

- Validate configuration compatibility before execution.
- Keep prompts concise to avoid context-window pressure.
- Add retries and guardrails for external tool/API calls.

## Common Pitfalls

| Problem | Cause | Solution |
|---|---|---|
| Ambiguous outcomes | Expected outputs are underspecified | Define concrete acceptance criteria and output format. |
| Execution drift | Role/task boundaries are unclear | Tighten role, goal, and task contracts. |
| Rework loops | Validation occurs too late | Add checkpoints and early review tasks. |
| Tool instability | Missing error handling and retries | Implement timeouts, retries, and fallback behavior. |

## Additional Notes

- This file is generated for Phase 4 standardization and can be expanded with skill-specific deep dives in later iterations.
