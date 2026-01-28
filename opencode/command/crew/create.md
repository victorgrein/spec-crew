---
description: Create a new CrewAI crew from natural language specification
agent: crewai-orchestrator
---

# /crew create

Create a complete CrewAI crew from a natural language specification.

## Syntax

```
/crew create "{specification}"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| specification | Yes | Natural language description of the crew |

## Examples

```
/crew create "A research crew that analyzes AI trends and writes reports"

/crew create "A customer support crew with agents for triage, response, and escalation"

/crew create "A content creation crew with researcher, writer, and editor agents"
```

## What It Does

1. **Analyzes** your specification to identify required agents and tasks
2. **Designs** the crew architecture (agents, tasks, process type)
3. **Generates** YAML configuration files (agents.yaml, tasks.yaml)
4. **Creates** Python code (crew.py, main.py)
5. **Asks** for your LLM preference (OpenAI/Anthropic model)
6. **Requests** permission before creating files

## Output

- Complete crew architecture diagram
- agents.yaml configuration
- tasks.yaml configuration
- crew.py implementation
- main.py entry point
- Ready-to-run project structure

## Related Commands

- `/crew add-agent` - Add agent to existing crew
- `/crew generate-flow` - Create flow structure
- `/crew review` - Review existing crew architecture
