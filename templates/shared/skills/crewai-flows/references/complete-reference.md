# CrewAI Flows - Complete Reference

This document centralizes detailed reference material for `crewai-flows` and supports progressive disclosure during skill execution.

## Source Material

- Core skill file: `../SKILL.md`
- Legacy reference files:
  - `flows-reference.md`

## Section Index from SKILL.md

- What This Skill Does
- When to Use This Skill
- Quick Reference
-   Key Benefits
-   Core Decorators
-   Conditional Logic
- Basic Flow Pattern
- Flow with Crew Integration
- Flow with Router (Conditional Logic)
- Flow with Parallel Execution
- State Management
-   Structured State (Recommended)
-   Unstructured State
- Flow Persistence
- Human-in-the-Loop
- Running Flows
- Visualization
- Flow Project Structure
- Best Practices
- Related Skills

## Essential Attributes

The following tables were extracted from `SKILL.md` and should be considered the canonical attribute and option index for this phase.

### Table 1

| Decorator | Purpose |
|-----------|---------|
| `@start()` | Marks entry points for a Flow |
| `@listen()` | Listens for output of another task |
| `@router()` | Defines conditional routing logic |

### Table 2

| Function | Purpose |
|----------|---------|
| `or_()` | Trigger when ANY specified methods emit |
| `and_()` | Trigger when ALL specified methods emit |

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
