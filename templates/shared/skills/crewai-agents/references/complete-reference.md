# CrewAI Agents - Complete Reference

This document centralizes detailed reference material for `crewai-agents` and supports progressive disclosure during skill execution.

## Source Material

- Core skill file: `../SKILL.md`
- Legacy reference files:
  - `agents-reference.md`

## Section Index from SKILL.md

- What This Skill Does
- When to Use This Skill
- Quick Reference
-   Essential Attributes
-   LLM Configuration
-   Behavior Settings
-   YAML Configuration Pattern
- Agent Archetypes
-   Research Agent
-   Code Development Agent
-   Analysis Agent
-   Reasoning Agent
- Direct Agent Interaction
- Best Practices
- Templates
-   Basic Agent YAML Template
-   Domain-Specific Templates
-     AI/ML Researcher
-     Code Reviewer
- Related Skills

## Essential Attributes

The following tables were extracted from `SKILL.md` and should be considered the canonical attribute and option index for this phase.

### Table 1

| Attribute | Type | Description |
|-----------|------|-------------|
| `role` | `str` | Defines the agent's function and expertise |
| `goal` | `str` | Individual objective guiding decision-making |
| `backstory` | `str` | Provides context and personality |

### Table 2

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `llm` | `Union[str, LLM, Any]` | `gpt-4` | Language model powering the agent |
| `function_calling_llm` | `Optional[Any]` | None | Separate LLM for tool calling |

### Table 3

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `verbose` | `bool` | False | Enable detailed logging |
| `allow_delegation` | `bool` | False | Allow delegating to other agents |
| `max_iter` | `int` | 20 | Max iterations before best answer |
| `max_rpm` | `Optional[int]` | None | Rate limit for API calls |
| `memory` | `bool` | False | Maintain conversation history |
| `cache` | `bool` | True | Cache tool results |
| `reasoning` | `bool` | False | Enable planning before execution |

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
