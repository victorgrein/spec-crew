# CrewAI Migration - Patterns and Archetypes

This document captures reusable patterns, archetypes, and workflow guidance for `crewai-migration`.

## Common Archetypes and Patterns

### Migration Checklist

- [ ] Backup existing project
- [ ] Create target structure
- [ ] Move/update crew files
- [ ] Update imports
- [ ] Create flow (if migrating to flow)
- [ ] Update pyproject.toml
- [ ] Test all functionality
- [ ] Update documentation
- [ ] Clean up old files

## Integration Patterns

- Pair with `crewai-agents` for role/goal/backstory contracts.
- Pair with `crewai-tasks` for deterministic output and dependencies.
- Pair with `crewai-debugging` and `crewai-optimization` for reliability/performance loops.

## Workflow Notes

- Define constraints first, then implementation details.
- Use measurable checkpoints at each major step.
- Preserve progressive disclosure: keep SKILL.md concise and place depth here.
