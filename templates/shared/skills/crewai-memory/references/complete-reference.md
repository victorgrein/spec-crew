# CrewAI Memory - Complete Reference

This document centralizes detailed reference material for `crewai-memory` and supports progressive disclosure during skill execution.

## Source Material

- Core skill file: `../SKILL.md`
- Legacy reference files:
  - `memory-reference.md`

## Section Index from SKILL.md

- What This Skill Does
- When to Use This Skill
- Quick Reference
-   Memory Types
-   Short-Term Memory
-   Long-Term Memory
-   Entity Memory
- Enabling Memory
-   Agent-Level
-   Crew-Level
- Embedder Configuration
-   Supported Providers
- Use Cases
-   Research Tasks
-   Customer Support
-   Complex Analysis
- Memory with Knowledge Sources
- Complete Example
- Best Practices
- Limitations
- Related Skills

## Essential Attributes

The following tables were extracted from `SKILL.md` and should be considered the canonical attribute and option index for this phase.

### Table 1

| Type | Description | Persistence |
|------|-------------|-------------|
| Short-Term | Current session context | Session only |
| Long-Term | Historical interactions | Across sessions |
| Entity | Information about specific entities | Across sessions |

### Table 2

| Provider | Configuration |
|----------|---------------|
| OpenAI | `{"provider": "openai"}` |
| Cohere | `{"provider": "cohere"}` |
| HuggingFace | `{"provider": "huggingface"}` |
| Custom | `{"provider": "custom", "config": {...}}` |

## Edge Cases and Limitations

- Review `Limitations` in `../SKILL.md` during troubleshooting.

## Common Pitfalls

| Problem | Cause | Solution |
|---|---|---|
| Ambiguous outcomes | Expected outputs are underspecified | Define concrete acceptance criteria and output format. |
| Execution drift | Role/task boundaries are unclear | Tighten role, goal, and task contracts. |
| Rework loops | Validation occurs too late | Add checkpoints and early review tasks. |
| Tool instability | Missing error handling and retries | Implement timeouts, retries, and fallback behavior. |

## Additional Notes

- This file is generated for Phase 4 standardization and can be expanded with skill-specific deep dives in later iterations.
