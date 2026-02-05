# CrewAI Crew Creation - YAML Configuration Examples

YAML configuration patterns for `crewai-crew-creation`.

## Extracted YAML Snippets

### YAML Example 1

```yaml
# config/agents.yaml
researcher:
  role: >
    {topic} Research Specialist
  goal: >
    Find comprehensive, accurate information about {topic}
  backstory: >
    Expert researcher with years of experience finding
    and synthesizing information from diverse sources.

writer:
  role: >
    Content Writer
  goal: >
    Create engaging, well-structured content
  backstory: >
    Skilled writer who transforms complex information
    into clear, compelling narratives.
```

### YAML Example 2

```yaml
# config/tasks.yaml
research_task:
  description: >
    Research {topic} thoroughly. Find key facts, recent
    developments, and expert opinions.
  expected_output: >
    Comprehensive research report with:
    - Key findings (5+ points)
    - Sources cited
    - Recent developments
  agent: researcher

writing_task:
  description: >
    Write an engaging article about {topic} based on
    the research findings.
  expected_output: >
    Well-structured article (800-1200 words) in markdown
    format with introduction, body, and conclusion.
  agent: writer
  context:
    - research_task
  output_file: output/article.md
```
