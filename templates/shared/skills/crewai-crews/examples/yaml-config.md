# CrewAI Crews - YAML Configuration Examples

YAML configuration patterns for `crewai-crews`.

## Extracted YAML Snippets

### YAML Example 1

```yaml
# config/agents.yaml
researcher:
  role: >
    {topic} Senior Data Researcher
  goal: >
    Uncover cutting-edge developments in {topic}
  backstory: >
    You're a seasoned researcher with a knack for uncovering the latest
    developments in {topic}.
```

### YAML Example 2

```yaml
# config/tasks.yaml
research_task:
  description: >
    Research the latest developments in {topic}
  expected_output: >
    A comprehensive report on {topic}
  agent: researcher
```
