# CrewAI Processes - Complete Reference

This document centralizes detailed reference material for `crewai-processes` and supports progressive disclosure during skill execution.

## Source Material

- Core skill file: `../SKILL.md`
- Legacy reference files:
  - `processes-reference.md`

## Section Index from SKILL.md

- What This Skill Does
- When to Use This Skill
- Quick Reference
-   Process Comparison
- Sequential Process (Default)
-   Characteristics
-   Flow Diagram
-   Task Order and Context
-   When to Use Sequential
- Hierarchical Process
-   Characteristics
-   Requirements
-   Flow Diagram
-   Manager Configuration
-   Manager Responsibilities
-   When to Use Hierarchical
- Process Selection Guide
-   Use Sequential When:
-   Use Hierarchical When:
- Examples
-   Sequential Crew
-   Hierarchical Crew
- Related Skills

## Essential Attributes

The following tables were extracted from `SKILL.md` and should be considered the canonical attribute and option index for this phase.

### Table 1

| Aspect | Sequential | Hierarchical |
|--------|------------|--------------|
| **Complexity** | Simple | Complex |
| **Control** | Predictable | Dynamic |
| **Coordination** | Implicit (order) | Explicit (manager) |
| **Validation** | None built-in | Manager validates |
| **Best For** | Linear workflows | Complex projects |
| **Requirements** | None | manager_llm or manager_agent |
| **Token Usage** | Lower | Higher (manager overhead) |

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
