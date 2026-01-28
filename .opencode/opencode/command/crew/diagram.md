---
description: Create visual architecture diagram for CrewAI crews and flows
agent: crewai-orchestrator
---

# /crew diagram

Generate visual architecture diagrams for CrewAI crews and flows.

## Syntax

```
/crew diagram {crew_path} [--type="{architecture|flow}"]
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| crew_path | Yes | Path to the crew or flow |
| --type | No | Diagram type (default: architecture) |

## Examples

```
/crew diagram ./my_crew

/crew diagram ./my_flow --type="flow"

/crew diagram ./research_crew --type="architecture"
```

## Diagram Types

### Architecture (`--type="architecture"`)
Shows agents, tasks, and their relationships:
```
┌─────────────┐    ┌─────────────┐
│  Agent 1    │───▶│  Agent 2    │
│ (Research)  │    │ (Writing)   │
└─────────────┘    └─────────────┘
      │                  │
      ▼                  ▼
┌─────────────┐    ┌─────────────┐
│   Task 1    │───▶│   Task 2    │
└─────────────┘    └─────────────┘
```

### Flow (`--type="flow"`)
Shows flow stages and routing:
```mermaid
graph TD
    Start --> A[@start: begin]
    A --> B[@listen: process]
    B --> C{@router: decide}
    C -->|success| D[success_path]
    C -->|failure| E[failure_path]
```

## What It Does

1. **Analyzes** crew/flow structure
2. **Identifies** components and relationships
3. **Generates** ASCII or Mermaid diagram
4. **Shows** task dependencies
5. **Highlights** tool assignments

## Output Formats

- ASCII art (terminal-friendly)
- Mermaid (for markdown/HTML)

## Related Commands

- `/crew docs` - Generate full documentation
- `/crew review` - Review architecture
