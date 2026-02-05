# CrewAI Project Structure - Patterns and Archetypes

This document captures reusable patterns, archetypes, and workflow guidance for `crewai-project-structure`.

## Common Archetypes and Patterns

### Best Practices

1. **Keep configs in YAML**: Easier to maintain and modify
2. **Separate tools**: Custom tools in dedicated directory
3. **Use __init__.py**: Proper Python package structure
4. **Output directory**: Keep generated files organized
5. **Environment variables**: Never commit .env files
6. **Tests**: Include basic tests for crews

## Integration Patterns

- Pair with `crewai-agents` for role/goal/backstory contracts.
- Pair with `crewai-tasks` for deterministic output and dependencies.
- Pair with `crewai-debugging` and `crewai-optimization` for reliability/performance loops.

## Workflow Notes

- Define constraints first, then implementation details.
- Use measurable checkpoints at each major step.
- Preserve progressive disclosure: keep SKILL.md concise and place depth here.
