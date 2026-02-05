# CrewAI Migration - YAML Configuration Examples

YAML configuration patterns for `crewai-migration`.

## Extracted YAML Snippets

### YAML Example 1

```yaml
# config/agents.yaml
researcher:
  role: >
    Research Analyst
  goal: >
    Find accurate information
  backstory: >
    Expert researcher with attention to detail
```

### YAML Example 2

```yaml
# config/tasks.yaml
research_task:
  description: >
    Research the topic thoroughly
  expected_output: >
    Comprehensive research report
  agent: researcher
```
