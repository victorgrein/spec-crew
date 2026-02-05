# CrewAI Processes - Patterns and Archetypes

This document captures reusable patterns, archetypes, and workflow guidance for `crewai-processes`.

## Common Archetypes and Patterns

### Process Comparison

| Aspect | Sequential | Hierarchical |
|--------|------------|--------------|
| **Complexity** | Simple | Complex |
| **Control** | Predictable | Dynamic |
| **Coordination** | Implicit (order) | Explicit (manager) |
| **Validation** | None built-in | Manager validates |
| **Best For** | Linear workflows | Complex projects |
| **Requirements** | None | manager_llm or manager_agent |
| **Token Usage** | Lower | Higher (manager overhead) |

### Sequential Process (Default)

Tasks execute one after another in the order they are defined.

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, write_task, edit_task],
    process=Process.sequential  # Default
)
```

### Hierarchical Process

A manager agent coordinates and delegates tasks to worker agents.

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer, analyst],
    tasks=[research_task, write_task, analysis_task],
    process=Process.hierarchical,
    manager_llm="gpt-4o"  # Required for hierarchical
)
```

### Process Selection Guide

- Refer to SKILL.md for details.

## Integration Patterns

- Pair with `crewai-agents` for role/goal/backstory contracts.
- Pair with `crewai-tasks` for deterministic output and dependencies.
- Pair with `crewai-debugging` and `crewai-optimization` for reliability/performance loops.

## Workflow Notes

- Define constraints first, then implementation details.
- Use measurable checkpoints at each major step.
- Preserve progressive disclosure: keep SKILL.md concise and place depth here.
