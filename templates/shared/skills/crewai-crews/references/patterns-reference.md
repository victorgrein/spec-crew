# CrewAI Crews - Patterns and Archetypes

This document captures reusable patterns, archetypes, and workflow guidance for `crewai-crews`.

## Common Archetypes and Patterns

### Basic Crew Pattern

- Refer to SKILL.md for details.

### Process Types

- Refer to SKILL.md for details.

### Sequential Process (Default)

Tasks execute one after another in order:

```python
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential
)
```

**Flow:** `Task 1 → Task 2 → Task 3 → Output`

### Hierarchical Process

Manager agent coordinates and delegates:

```python
crew = Crew(
    agents=[researcher, writer, analyst],
    tasks=[research_task, write_task, analysis_task],
    process=Process.hierarchical,
    manager_llm="gpt-4o"  # Required for hierarchical
)
```

### Best Practices

1. **Choose Process Wisely**: Sequential for linear, hierarchical for complex
2. **Enable Memory**: For multi-step or iterative tasks
3. **Use Caching**: Reduces redundant API calls
4. **Set Rate Limits**: Avoid API limit errors
5. **Log Outputs**: For debugging and monitoring
6. **Use Verbose Mode**: During development

## Integration Patterns

- Pair with `crewai-agents` for role/goal/backstory contracts.
- Pair with `crewai-tasks` for deterministic output and dependencies.
- Pair with `crewai-debugging` and `crewai-optimization` for reliability/performance loops.

## Workflow Notes

- Define constraints first, then implementation details.
- Use measurable checkpoints at each major step.
- Preserve progressive disclosure: keep SKILL.md concise and place depth here.
