# CrewAI Debugging - Complete Reference

This document centralizes detailed reference material for `crewai-debugging` and supports progressive disclosure during skill execution.

## Source Material

- Core skill file: `../SKILL.md`
- Legacy reference files:
  - `debugging-reference.md`

## Section Index from SKILL.md

- What This Skill Does
- When to Use This Skill
- Quick Reference
-   Common Issues
- Debugging Workflow
-   Step 1: Gather Information
-   Step 2: Reproduce the Issue
-   Step 3: Analyze Traces
-   Step 4: Identify Root Cause
-   Step 5: Apply Fix
- Common Issues and Solutions
-   Rate Limit Errors
-   Context Window Exceeded
-   Tool Not Working
-   Agent Stuck in Loop
-   Output Parsing Errors
-   Async Errors
- Debugging Commands
- Debugging Checklist
- Related Skills

## Essential Attributes

The following tables were extracted from `SKILL.md` and should be considered the canonical attribute and option index for this phase.

### Table 1

| Category | Symptoms | Check |
|----------|----------|-------|
| Rate Limits | 429 errors, intermittent failures | max_rpm settings |
| Context Window | Truncated output, lost context | respect_context_window |
| Tool Errors | Tool not found, wrong arguments | Tool assignment, descriptions |
| Agent Loops | max_iter reached, repeated actions | Task clarity, delegation |
| Output Parsing | Pydantic errors, JSON failures | Output format, model |

## Edge Cases and Limitations

- Review `Common Issues` in `../SKILL.md` during troubleshooting.
- Review `Debugging Workflow` in `../SKILL.md` during troubleshooting.
- Review `Step 2: Reproduce the Issue` in `../SKILL.md` during troubleshooting.
- Review `Common Issues and Solutions` in `../SKILL.md` during troubleshooting.
- Review `Rate Limit Errors` in `../SKILL.md` during troubleshooting.
- Review `Context Window Exceeded` in `../SKILL.md` during troubleshooting.
- Review `Output Parsing Errors` in `../SKILL.md` during troubleshooting.
- Review `Async Errors` in `../SKILL.md` during troubleshooting.
- Review `Debugging Commands` in `../SKILL.md` during troubleshooting.
- Review `Debugging Checklist` in `../SKILL.md` during troubleshooting.

## Common Pitfalls

| Problem | Cause | Solution |
|---|---|---|
| Ambiguous outcomes | Expected outputs are underspecified | Define concrete acceptance criteria and output format. |
| Execution drift | Role/task boundaries are unclear | Tighten role, goal, and task contracts. |
| Rework loops | Validation occurs too late | Add checkpoints and early review tasks. |
| Tool instability | Missing error handling and retries | Implement timeouts, retries, and fallback behavior. |

## Additional Notes

- This file is generated for Phase 4 standardization and can be expanded with skill-specific deep dives in later iterations.
