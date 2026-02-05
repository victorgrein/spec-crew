# CrewAI Llms - Complete Reference

This document centralizes detailed reference material for `crewai-llms` and supports progressive disclosure during skill execution.

## Source Material

- Core skill file: `../SKILL.md`
- Legacy reference files:
  - `llms-reference.md`

## Section Index from SKILL.md

- What This Skill Does
- When to Use This Skill
- Quick Reference
-   Supported Providers
-   Model Selection by Use Case
- Configuration
-   Environment Variables
-   Agent-Level Configuration
-   Crew-Level Configuration
- Cost Optimization Strategies
-   1. Tiered Model Strategy
-   2. Function Calling LLM
-   3. Caching
- Rate Limiting
-   Agent-Level
-   Crew-Level (Overrides Agent Settings)
- Context Window Management
-   Auto-Summarization (Default)
-   Strict Mode
- Optimization Configurations
-   Cost Optimization
-   Quality Optimization
-   Latency Optimization
- Approximate Costs (per 1K tokens)
- Best Practices
- Related Skills

## Essential Attributes

The following tables were extracted from `SKILL.md` and should be considered the canonical attribute and option index for this phase.

### Table 1

| Provider | Models | Context |
|----------|--------|---------|
| OpenAI | gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo | 16K-128K |
| Anthropic | claude-3-5-sonnet, claude-3-opus, claude-3-haiku | 200K |

### Table 2

| Use Case | Recommended Model | Reason |
|----------|-------------------|--------|
| Complex reasoning | `gpt-4o`, `claude-3-5-sonnet` | Best quality |
| Code generation | `claude-3-5-sonnet`, `gpt-4o` | Strong coding |
| Simple tasks | `gpt-4o-mini`, `claude-3-haiku` | Fast, cheap |
| Function calling | `gpt-4o-mini`, `gpt-3.5-turbo` | Cost-effective |
| Long documents | `claude-3-5-sonnet` (200K) | Largest context |
| Multimodal | `gpt-4o` | Vision support |

### Table 3

| Model | Input | Output |
|-------|-------|--------|
| gpt-4o | $0.005 | $0.015 |
| gpt-4o-mini | $0.00015 | $0.0006 |
| gpt-3.5-turbo | $0.0005 | $0.0015 |
| claude-3-5-sonnet | $0.003 | $0.015 |
| claude-3-opus | $0.015 | $0.075 |
| claude-3-haiku | $0.00025 | $0.00125 |

## Edge Cases and Limitations

- Review `Rate Limiting` in `../SKILL.md` during troubleshooting.
- Review `Context Window Management` in `../SKILL.md` during troubleshooting.

## Common Pitfalls

| Problem | Cause | Solution |
|---|---|---|
| Ambiguous outcomes | Expected outputs are underspecified | Define concrete acceptance criteria and output format. |
| Execution drift | Role/task boundaries are unclear | Tighten role, goal, and task contracts. |
| Rework loops | Validation occurs too late | Add checkpoints and early review tasks. |
| Tool instability | Missing error handling and retries | Implement timeouts, retries, and fallback behavior. |

## Additional Notes

- This file is generated for Phase 4 standardization and can be expanded with skill-specific deep dives in later iterations.
