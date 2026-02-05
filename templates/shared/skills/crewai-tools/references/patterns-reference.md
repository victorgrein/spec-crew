# CrewAI Tools - Patterns and Archetypes

This document captures reusable patterns, archetypes, and workflow guidance for `crewai-tools`.

## Common Archetypes and Patterns

### Tool Description Guidelines

**Good description:**
```python
description = """
Use this tool to search the web for current information.
Best for: Finding recent news, articles, and data.
Input: A search query string.
Output: List of relevant search results with titles and snippets.
"""
```

**Bad description:**
```python
description = "Searches the web"  # Too vague
```

### Best Practices

1. **Clear Descriptions**: Agents use descriptions to decide which tool to use
2. **Error Handling**: Always wrap operations in try/except, return error strings
3. **Input Validation**: Use Pydantic models with Field descriptions
4. **Caching**: Enable for expensive operations
5. **Async**: Use for I/O-bound operations
6. **Rate Limiting**: Consider API limits in tool implementation

## Integration Patterns

- Pair with `crewai-agents` for role/goal/backstory contracts.
- Pair with `crewai-tasks` for deterministic output and dependencies.
- Pair with `crewai-debugging` and `crewai-optimization` for reliability/performance loops.

## Workflow Notes

- Define constraints first, then implementation details.
- Use measurable checkpoints at each major step.
- Preserve progressive disclosure: keep SKILL.md concise and place depth here.
