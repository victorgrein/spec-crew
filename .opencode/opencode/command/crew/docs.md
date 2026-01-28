---
description: Generate documentation for CrewAI crews and flows
agent: crewai-orchestrator
---

# /crew docs

Generate comprehensive documentation for a CrewAI crew or flow.

## Syntax

```
/crew docs {crew_path} [--format="{md|html}"]
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| crew_path | Yes | Path to the crew or flow |
| --format | No | Output format (default: md) |

## Examples

```
/crew docs ./my_crew

/crew docs ./my_flow --format="html"

/crew docs src/my_project/crews/research_crew
```

## What It Does

1. **Analyzes** crew/flow structure
2. **Extracts** agent and task information
3. **Generates** architecture diagram
4. **Creates** comprehensive README
5. **Documents** configuration options
6. **Includes** usage examples

## Generated Documentation

### README.md Contents
- Project description
- Architecture diagram
- Agent table (role, tools)
- Task table (description, dependencies)
- Installation instructions
- Configuration guide
- Usage examples
- Troubleshooting

### Additional Files (optional)
- ARCHITECTURE.md - Detailed architecture
- API.md - Tool documentation
- CHANGELOG.md - Version history

## Output

- README.md content
- Architecture diagram (ASCII/Mermaid)
- Configuration documentation
- Usage examples

## Related Commands

- `/crew diagram` - Generate architecture diagram
- `/crew review` - Review architecture
