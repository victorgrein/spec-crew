# CrewAI Memory - Patterns and Archetypes

This document captures reusable patterns, archetypes, and workflow guidance for `crewai-memory`.

## Common Archetypes and Patterns

### Use Cases

- Refer to SKILL.md for details.

### Best Practices

1. **Enable for Complex Tasks**: Use memory for multi-step or iterative tasks
2. **Combine with Context Window Management**: Use `respect_context_window=True`
3. **Configure Embedder**: Choose appropriate embedding model for your use case
4. **Monitor Memory Usage**: Memory increases token usage
5. **Clear When Needed**: Start fresh sessions when context should be reset

## Integration Patterns

- Pair with `crewai-agents` for role/goal/backstory contracts.
- Pair with `crewai-tasks` for deterministic output and dependencies.
- Pair with `crewai-debugging` and `crewai-optimization` for reliability/performance loops.

## Workflow Notes

- Define constraints first, then implementation details.
- Use measurable checkpoints at each major step.
- Preserve progressive disclosure: keep SKILL.md concise and place depth here.
