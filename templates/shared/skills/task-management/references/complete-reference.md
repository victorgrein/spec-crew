# Task Management - Complete Reference

This document centralizes detailed reference material for `task-management` and supports progressive disclosure during skill execution.

## Source Material

- Core skill file: `../SKILL.md`
- Legacy reference files: none

## Section Index from SKILL.md

- What I do
- How to use me
-   Basic Commands
-   Command Reference
- Examples
-   Check Overall Progress
-   Find What's Next
-   Mark Complete
-   Check Dependencies
-   Validate Everything
- Architecture
- Task File Structure
-   task.json Schema
-   subtask_##.json Schema
- Integration with TaskManager
- Key Concepts
-   1. Dependency Resolution
-   2. Parallel Execution
-   3. Status Tracking
-   4. Exit Criteria

## Essential Attributes

The following tables were extracted from `SKILL.md` and should be considered the canonical attribute and option index for this phase.

### Table 1

| Command | Description |
|---------|-------------|
| `status [feature]` | Show task status summary for all features or specific one |
| `next [feature]` | Show next eligible tasks (dependencies satisfied) |
| `parallel [feature]` | Show parallelizable tasks ready to run |
| `deps <feature> <seq>` | Show dependency tree for a specific subtask |
| `blocked [feature]` | Show blocked tasks and why |
| `complete <feature> <seq> "summary"` | Mark subtask complete with summary |
| `validate [feature]` | Validate JSON files and dependencies |

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
