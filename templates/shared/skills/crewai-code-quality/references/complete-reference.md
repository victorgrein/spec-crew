# CrewAI Code Quality - Complete Reference

This document centralizes detailed reference material for `crewai-code-quality` and supports progressive disclosure during skill execution.

## Source Material

- Core skill file: `../SKILL.md`
- Legacy reference files:
  - `code-quality-reference.md`

## Section Index from SKILL.md

- What This Skill Does
- When to Use This Skill
- Quick Reference
-   Naming Conventions
- Agent Design Standards
-   Role Definition
-   Goal Definition
-   Backstory Definition
- Task Design Standards
-   Description
-   Expected Output
- Crew Class Standards
- Custom Tool Standards
- Error Handling Standards
-   In Tools
-   In Crews
- Configuration Standards
-   Environment Variables
-   pyproject.toml
- Documentation Standards
-   README.md
-   Code Comments
- Testing Standards
-   Basic Test
- Quality Checklist
- Related Skills

## Essential Attributes

The following tables were extracted from `SKILL.md` and should be considered the canonical attribute and option index for this phase.

### Table 1

| Component | Convention | Example |
|-----------|------------|---------|
| Project | snake_case | `my_crew_project` |
| Crew class | PascalCase | `ResearchCrew` |
| Agent methods | snake_case | `research_analyst` |
| Task methods | snake_case | `research_task` |
| YAML keys | snake_case | `research_analyst` |
| Tool classes | PascalCase | `CustomSearchTool` |

## Edge Cases and Limitations

- Review `Error Handling Standards` in `../SKILL.md` during troubleshooting.

## Common Pitfalls

| Problem | Cause | Solution |
|---|---|---|
| Ambiguous outcomes | Expected outputs are underspecified | Define concrete acceptance criteria and output format. |
| Execution drift | Role/task boundaries are unclear | Tighten role, goal, and task contracts. |
| Rework loops | Validation occurs too late | Add checkpoints and early review tasks. |
| Tool instability | Missing error handling and retries | Implement timeouts, retries, and fallback behavior. |

## Additional Notes

- This file is generated for Phase 4 standardization and can be expanded with skill-specific deep dives in later iterations.
