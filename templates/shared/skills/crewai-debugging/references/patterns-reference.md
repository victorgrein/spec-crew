# CrewAI Debugging - Patterns and Archetypes

This document captures reusable patterns, archetypes, and workflow guidance for `crewai-debugging`.

## Common Archetypes and Patterns

### Common Issues

| Category | Symptoms | Check |
|----------|----------|-------|
| Rate Limits | 429 errors, intermittent failures | max_rpm settings |
| Context Window | Truncated output, lost context | respect_context_window |
| Tool Errors | Tool not found, wrong arguments | Tool assignment, descriptions |
| Agent Loops | max_iter reached, repeated actions | Task clarity, delegation |
| Output Parsing | Pydantic errors, JSON failures | Output format, model |

### Debugging Workflow

- Refer to SKILL.md for details.

### Common Issues and Solutions

- Refer to SKILL.md for details.

### Debugging Checklist

- [ ] Verbose mode enabled
- [ ] Logs being captured
- [ ] Issue reproducible
- [ ] Root cause identified
- [ ] Fix tested
- [ ] Preventive measures added

## Integration Patterns

- Pair with `crewai-agents` for role/goal/backstory contracts.
- Pair with `crewai-tasks` for deterministic output and dependencies.
- Pair with `crewai-debugging` and `crewai-optimization` for reliability/performance loops.

## Workflow Notes

- Define constraints first, then implementation details.
- Use measurable checkpoints at each major step.
- Preserve progressive disclosure: keep SKILL.md concise and place depth here.
