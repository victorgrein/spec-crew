# CrewAI Project Structure - YAML Configuration Examples

YAML configuration patterns for `crewai-project-structure`.

## Extracted YAML Snippets

### YAML Example 1

```yaml
researcher:
  role: >
    {topic} Research Analyst
  goal: >
    Find comprehensive, accurate information about {topic}
  backstory: >
    Expert researcher with years of experience finding
    and synthesizing information from diverse sources.
```

### YAML Example 2

```yaml
research_task:
  description: >
    Research {topic} thoroughly. Find key facts, recent
    developments, and expert opinions.
  expected_output: >
    Comprehensive research report with key findings,
    sources cited, and relevant data points.
  agent: researcher
```
