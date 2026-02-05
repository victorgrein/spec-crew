# CrewAI Tasks - Complete Reference

This document centralizes detailed reference material for `crewai-tasks` and supports progressive disclosure during skill execution.

## Source Material

- Core skill file: `../SKILL.md`
- Legacy reference files:
  - `tasks-reference.md`

## Section Index from SKILL.md

- What This Skill Does
- When to Use This Skill
- Quick Reference
-   Essential Attributes
-   Context and Dependencies
-   Output Handling
-   Execution Settings
-   YAML Configuration Pattern
- Task Patterns
-   Research Task
-   Writing Task with Output File
-   Structured Output Task
- Context Passing
- Async Execution
- Human Input
- Task Callbacks
- Best Practices
- Templates
- Related Skills

## Essential Attributes

The following tables were extracted from `SKILL.md` and should be considered the canonical attribute and option index for this phase.

### Table 1

| Attribute | Type | Description |
|-----------|------|-------------|
| `description` | `str` | Clear, detailed description of what needs to be done |
| `expected_output` | `str` | Specific description of expected deliverable |
| `agent` | `Agent` | Agent responsible for the task |
| `name` | `str` | Identifier for the task |

### Table 2

| Attribute | Type | Description |
|-----------|------|-------------|
| `context` | `List[Task]` | Tasks whose output provides context |
| `tools` | `List[BaseTool]` | Task-specific tools (override agent tools) |

### Table 3

| Attribute | Type | Description |
|-----------|------|-------------|
| `output_file` | `str` | Save output to file |
| `output_json` | `Type[BaseModel]` | Parse output as JSON |
| `output_pydantic` | `Type[BaseModel]` | Parse output as Pydantic model |

### Table 4

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `async_execution` | `bool` | False | Run asynchronously |
| `human_input` | `bool` | False | Require human approval |
| `callback` | `Callable` | None | Function called after completion |

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
