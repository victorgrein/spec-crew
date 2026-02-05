# CrewAI Agents - Patterns and Archetypes

This document captures reusable patterns, archetypes, and workflow guidance for `crewai-agents`.

## Common Archetypes and Patterns

### YAML Configuration Pattern

```yaml
# config/agents.yaml
researcher:
  role: >
    {topic} Senior Data Researcher
  goal: >
    Uncover cutting-edge developments in {topic}
  backstory: >
    You're a seasoned researcher with a knack for uncovering the latest
    developments in {topic}. Known for your ability to find the most relevant
    information and present it in a clear and concise manner.
```

```python
@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config['researcher'],
        tools=[SerperDevTool()],
        verbose=True
    )
```

### Agent Archetypes

- Refer to SKILL.md for details.

### Best Practices

1. **Role Design**: Be specific about expertise area and seniority
2. **Goal Design**: Focus on outcomes, be measurable
3. **Backstory Design**: Provide relevant context, keep concise (2-4 sentences)
4. **Tool Assignment**: Match tools to agent's purpose
5. **Memory**: Enable for complex, multi-step tasks
6. **Rate Limiting**: Set `max_rpm` to avoid API limits
7. **Caching**: Keep enabled for repetitive operations

## Integration Patterns

- Pair with `crewai-agents` for role/goal/backstory contracts.
- Pair with `crewai-tasks` for deterministic output and dependencies.
- Pair with `crewai-debugging` and `crewai-optimization` for reliability/performance loops.

## Workflow Notes

- Define constraints first, then implementation details.
- Use measurable checkpoints at each major step.
- Preserve progressive disclosure: keep SKILL.md concise and place depth here.
