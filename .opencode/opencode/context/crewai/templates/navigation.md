# CrewAI Templates Navigation

## Overview

Reusable templates for common CrewAI components.

## Available Templates

| File | Description | When to Use |
|------|-------------|-------------|
| [agent-yaml.md](agent-yaml.md) | Agent YAML configurations | Creating agents |
| [task-yaml.md](task-yaml.md) | Task YAML configurations | Creating tasks |
| [flow-class.md](flow-class.md) | Flow class implementations | Creating flows |

## Quick Reference

### Agent Template

```yaml
agent_name:
  role: >
    {Role with expertise}
  goal: >
    {Specific objective}
  backstory: >
    {Context in 2-4 sentences}
```

### Task Template

```yaml
task_name:
  description: >
    {Clear instructions}
  expected_output: >
    {Specific deliverable}
  agent: {agent_name}
```

### Flow Template

```python
class MyFlow(Flow[MyState]):
    @start()
    def begin(self):
        return data
    
    @listen(begin)
    def process(self, data):
        return result
```

## Template Categories

### By Component

- **Agents**: Researcher, Writer, Analyst, Developer, Reviewer, Manager
- **Tasks**: Research, Analysis, Writing, Review, Extraction, Summary
- **Flows**: Basic, Crew Integration, Router, Parallel, Persistent

### By Use Case

| Use Case | Templates Needed |
|----------|------------------|
| Research project | Researcher agent, Research task |
| Content creation | Writer agent, Writing task |
| Data analysis | Analyst agent, Analysis task |
| Multi-crew workflow | Flow with crew integration |
| Quality review | Reviewer agent, Review task, Router flow |
