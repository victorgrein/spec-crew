# CrewAI Crews - Complete Reference

This document centralizes detailed reference material for `crewai-crews` and supports progressive disclosure during skill execution.

## Source Material

- Core skill file: `../SKILL.md`
- Legacy reference files:
  - `crews-reference.md`

## Section Index from SKILL.md

- What This Skill Does
- When to Use This Skill
- Quick Reference
-   Key Attributes
-   Crew Output
- Basic Crew Pattern
-   YAML Configuration
-   Crew Class
- Process Types
-   Sequential Process (Default)
-   Hierarchical Process
- Decorators
- Kickoff Methods
-   Synchronous
-   Asynchronous (Native)
-   Asynchronous (Thread-based)
- Streaming Execution
- Memory and Cache
- Usage Metrics
- Logging
- Replay from Task
- Best Practices
- Related Skills

## Essential Attributes

The following tables were extracted from `SKILL.md` and should be considered the canonical attribute and option index for this phase.

### Table 1

| Attribute | Description | Default |
|-----------|-------------|---------|
| `agents` | List of agents in the crew | Required |
| `tasks` | List of tasks to execute | Required |
| `process` | Execution flow (sequential/hierarchical) | `sequential` |
| `verbose` | Enable detailed logging | `False` |
| `memory` | Enable execution memories | `False` |
| `cache` | Cache tool results | `True` |
| `manager_llm` | LLM for hierarchical manager | Required for hierarchical |

### Table 2

| Attribute | Type | Description |
|-----------|------|-------------|
| `raw` | `str` | Raw output string |
| `pydantic` | `Optional[BaseModel]` | Structured Pydantic output |
| `json_dict` | `Optional[Dict]` | JSON dictionary output |
| `tasks_output` | `List[TaskOutput]` | Individual task outputs |
| `token_usage` | `Dict[str, Any]` | Token usage summary |

### Table 3

| Decorator | Purpose |
|-----------|---------|
| `@CrewBase` | Marks class as crew base |
| `@agent` | Denotes method returning Agent |
| `@task` | Denotes method returning Task |
| `@crew` | Denotes method returning Crew |
| `@before_kickoff` | Execute before crew starts |
| `@after_kickoff` | Execute after crew finishes |

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
