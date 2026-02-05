# CrewAI Tasks - Patterns and Archetypes

This document captures reusable patterns, archetypes, and workflow guidance for `crewai-tasks`.

## Common Archetypes and Patterns

### YAML Configuration Pattern

```yaml
# config/tasks.yaml
research_task:
  description: >
    Research the latest developments in {topic} from the past month.
    Focus on peer-reviewed sources and industry reports.
  expected_output: >
    A comprehensive report of 500-800 words covering:
    1) Key findings
    2) Market implications
    3) Recommended actions
    Use markdown formatting.
  agent: researcher

analysis_task:
  description: >
    Analyze the research findings and identify key patterns.
  expected_output: >
    An analysis report with insights and recommendations.
  agent: analyst
  context:
    - research_task
```

```python
@task
def research_task(self) -> Task:
    return Task(config=self.tasks_config['research_task'])

@task
def analysis_task(self) -> Task:
    return Task(
        config=self.tasks_config['analysis_task'],
        context=[self.research_task()]
    )
```

### Task Patterns

- Refer to SKILL.md for details.

### Best Practices

1. **Clear Descriptions**: Be specific about what needs to be done
2. **Measurable Outputs**: Define concrete, verifiable expected outputs
3. **Proper Context**: List all tasks whose output is needed
4. **Avoid Circular Dependencies**: Tasks can't depend on each other
5. **Use Variables**: Use `{variable}` for dynamic content
6. **Output Files**: Specify for tasks generating artifacts
7. **Structured Output**: Use Pydantic models for data extraction

## Integration Patterns

- Pair with `crewai-agents` for role/goal/backstory contracts.
- Pair with `crewai-tasks` for deterministic output and dependencies.
- Pair with `crewai-debugging` and `crewai-optimization` for reliability/performance loops.

## Workflow Notes

- Define constraints first, then implementation details.
- Use measurable checkpoints at each major step.
- Preserve progressive disclosure: keep SKILL.md concise and place depth here.
