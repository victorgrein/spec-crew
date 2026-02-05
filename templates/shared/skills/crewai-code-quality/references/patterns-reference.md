# CrewAI Code Quality - Patterns and Archetypes

This document captures reusable patterns, archetypes, and workflow guidance for `crewai-code-quality`.

## Common Archetypes and Patterns

### Quality Checklist

- [ ] Project follows standard structure
- [ ] Naming conventions followed
- [ ] Agents have detailed roles, goals, backstories
- [ ] Tasks have clear descriptions and expected outputs
- [ ] Tools have proper error handling
- [ ] Environment variables documented
- [ ] README.md complete
- [ ] Tests included

## Integration Patterns

- Pair with `crewai-agents` for role/goal/backstory contracts.
- Pair with `crewai-tasks` for deterministic output and dependencies.
- Pair with `crewai-debugging` and `crewai-optimization` for reliability/performance loops.

## Workflow Notes

- Define constraints first, then implementation details.
- Use measurable checkpoints at each major step.
- Preserve progressive disclosure: keep SKILL.md concise and place depth here.
