---
description: Canonical command for CrewAI documentation and diagram generation
agent: crewai-orchestrator
canonical: true
command_id: crew.docs.v1
---

# /crew docs

Generate comprehensive documentation for a CrewAI crew or flow.

## Syntax

```
/crew docs {crew_path} [--format="{md|html}"] [--include-diagram="{auto|architecture|flow|none}"]
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| crew_path | Yes | Path to the crew or flow |
| --format | No | Output format (default: `md`) |
| --include-diagram | No | Diagram mode (default: `auto`) |

## What It Does

1. Analyzes crew/flow structure and ownership
2. Extracts agent, task, and process metadata
3. Generates architecture or flow diagrams when requested
4. Produces README-focused technical documentation with usage guidance

## Output

- README-ready content
- Optional architecture or flow diagram (ASCII/Mermaid)
- Configuration and operational notes
- Validation checklist for docs accuracy

## Response Contract (Required)

Every command response must include these sections in order:

1. `findings` - observations grounded in repository evidence
2. `plan` - ordered execution steps
3. `proposed changes` - concrete file/config changes (or `none`)
4. `validation steps` - checks to confirm correctness

## Related Commands

- `/crew init` - Initialize standards and project context
- `/crew inspect` - Review architecture before documentation
- `/crew evolve` - Regenerate docs after migrations
