# Task Management - Patterns and Archetypes

This document captures reusable patterns, archetypes, and workflow guidance for `task-management`.

## Common Archetypes and Patterns

### Integration with TaskManager

The TaskManager subagent creates task files using this format. When you delegate to TaskManager:

```
task(subagent_type="TaskManager", description="Implement feature X")
```

TaskManager creates:
1. `.tmp/tasks/{feature}/task.json` - Feature metadata
2. `.tmp/tasks/{feature}/subtask_XX.json` - Individual subtasks

You can then use this skill to track and manage progress.

## Integration Patterns

- Pair with `crewai-agents` for role/goal/backstory contracts.
- Pair with `crewai-tasks` for deterministic output and dependencies.
- Pair with `crewai-debugging` and `crewai-optimization` for reliability/performance loops.

## Workflow Notes

- Define constraints first, then implementation details.
- Use measurable checkpoints at each major step.
- Preserve progressive disclosure: keep SKILL.md concise and place depth here.
