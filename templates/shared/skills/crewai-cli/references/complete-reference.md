# CrewAI Cli - Complete Reference

This document centralizes detailed reference material for `crewai-cli` and supports progressive disclosure during skill execution.

## Source Material

- Core skill file: `../SKILL.md`
- Legacy reference files:
  - `cli-reference.md`

## Section Index from SKILL.md

- What This Skill Does
- When to Use This Skill
- Quick Reference
-   Essential Commands
- Project Commands
-   Create New Project
-   Generated Structure (Crew)
-   Generated Structure (Flow)
-   Install Dependencies
-   Run Project
-   Activate Virtual Environment
- Dependency Management
-   Add Dependencies
-   Sync Dependencies
-   Update Dependencies
- Debugging Commands
-   View Task Outputs
-   Replay from Task
- Flow Commands
-   Kickoff Flow
-   Plot Flow
- Running with uv
- Project Configuration
-   pyproject.toml (Crew)
-   pyproject.toml (Flow)
-   Environment Variables
- Common Workflows
-   Starting a New Crew Project
-   Starting a New Flow Project
-   Debugging a Crew
- Tips
- Related Skills

## Essential Attributes

The following tables were extracted from `SKILL.md` and should be considered the canonical attribute and option index for this phase.

### Table 1

| Command | Purpose |
|---------|---------|
| `crewai create crew <name>` | Create new crew project |
| `crewai create flow <name>` | Create new flow project |
| `crewai install` | Install dependencies |
| `crewai run` | Run crew or flow |
| `crewai log-tasks-outputs` | View task outputs |
| `crewai replay -t <id>` | Replay from task |

## Edge Cases and Limitations

- Review `Debugging Commands` in `../SKILL.md` during troubleshooting.
- Review `Debugging a Crew` in `../SKILL.md` during troubleshooting.

## Common Pitfalls

| Problem | Cause | Solution |
|---|---|---|
| Ambiguous outcomes | Expected outputs are underspecified | Define concrete acceptance criteria and output format. |
| Execution drift | Role/task boundaries are unclear | Tighten role, goal, and task contracts. |
| Rework loops | Validation occurs too late | Add checkpoints and early review tasks. |
| Tool instability | Missing error handling and retries | Implement timeouts, retries, and fallback behavior. |

## Additional Notes

- This file is generated for Phase 4 standardization and can be expanded with skill-specific deep dives in later iterations.
