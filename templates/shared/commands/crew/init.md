---
description: Canonical command for CrewAI project setup and new crew initialization
agent: crewai-orchestrator
canonical: true
command_id: crew.init.v1
---

# /crew init

Canonical entry point for project setup and natural-language crew creation.

## Syntax

```
/crew init [target_path] [--spec="{specification}"] [--mode="{create|merge|refresh}"] [--project="{auto|new|existing}"]
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| target_path | No | Path to scan or create into (default: current directory) |
| --spec | No | Natural language crew specification |
| --mode | No | AGENTS.md handling mode: `create`, `merge`, or `refresh` |
| --project | No | Project mode: `auto`, `new`, or `existing` |

## What It Does

1. Detects repository signals and project constraints
2. Builds or updates `AGENTS.md` with CrewAI operating rules
3. Designs agents, tasks, and crew structure when `--spec` is provided
4. Generates implementation scaffolding when required
5. Returns a contract-compliant plan before write operations

## Output

- Repository findings and confidence notes
- Initialization plan and task breakdown
- Proposed file changes for setup or creation
- Validation and follow-up checks

## Response Contract (Required)

Every command response must include these sections in order:

1. `findings` - observations grounded in repository evidence
2. `plan` - ordered execution steps
3. `proposed changes` - concrete file/config changes (or `none`)
4. `validation steps` - checks to confirm correctness

## Related Commands

- `/crew inspect` - Analyze existing architecture and performance
- `/crew fix` - Debug and optimize runtime behavior
- `/crew evolve` - Refactor and migrate project structure
- `/crew docs` - Generate implementation documentation
