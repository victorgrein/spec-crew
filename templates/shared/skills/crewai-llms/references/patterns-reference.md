# CrewAI Llms - Patterns and Archetypes

This document captures reusable patterns, archetypes, and workflow guidance for `crewai-llms`.

## Common Archetypes and Patterns

### Model Selection by Use Case

| Use Case | Recommended Model | Reason |
|----------|-------------------|--------|
| Complex reasoning | `gpt-4o`, `claude-3-5-sonnet` | Best quality |
| Code generation | `claude-3-5-sonnet`, `gpt-4o` | Strong coding |
| Simple tasks | `gpt-4o-mini`, `claude-3-haiku` | Fast, cheap |
| Function calling | `gpt-4o-mini`, `gpt-3.5-turbo` | Cost-effective |
| Long documents | `claude-3-5-sonnet` (200K) | Largest context |
| Multimodal | `gpt-4o` | Vision support |

### Best Practices

1. **Start with cheaper models** and upgrade only if needed
2. **Use function_calling_llm** for cost savings on tool calls
3. **Enable caching** to reduce redundant API calls
4. **Set max_rpm** to avoid rate limit errors
5. **Monitor usage_metrics** to track token consumption
6. **Use respect_context_window=True** for long conversations
7. **Match model to task complexity** - don't use GPT-4 for simple tasks

## Integration Patterns

- Pair with `crewai-agents` for role/goal/backstory contracts.
- Pair with `crewai-tasks` for deterministic output and dependencies.
- Pair with `crewai-debugging` and `crewai-optimization` for reliability/performance loops.

## Workflow Notes

- Define constraints first, then implementation details.
- Use measurable checkpoints at each major step.
- Preserve progressive disclosure: keep SKILL.md concise and place depth here.
