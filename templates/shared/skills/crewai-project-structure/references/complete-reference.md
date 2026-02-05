# CrewAI Project Structure - Complete Reference

This document centralizes detailed reference material for `crewai-project-structure` and supports progressive disclosure during skill execution.

## Source Material

- Core skill file: `../SKILL.md`
- Legacy reference files:
  - `project-structure-reference.md`

## Section Index from SKILL.md

- What This Skill Does
- When to Use This Skill
- Quick Reference
-   Directory Purposes
- Crew Project Structure
- Flow Project Structure
- File Contents
-   main.py (Crew)
-   main.py (Flow)
-   crew.py
-   config/agents.yaml
-   config/tasks.yaml
-   pyproject.toml (Crew)
-   pyproject.toml (Flow)
-   .env
-   .gitignore
- Best Practices
- Related Skills

## Essential Attributes

The following tables were extracted from `SKILL.md` and should be considered the canonical attribute and option index for this phase.

### Table 1

| Directory | Purpose |
|-----------|---------|
| `src/` | Source code |
| `config/` | YAML configurations |
| `tools/` | Custom tools |
| `tests/` | Test files |
| `output/` | Generated outputs |

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
