---
description: Canonical command for migration and structural evolution
agent: crewai-orchestrator
canonical: true
command_id: crew.evolve.v1
---

# /crew evolve

Canonical command for migration, refactoring, and flow-oriented evolution.

## Syntax

```
/crew evolve {source_path} [--to="{flow|yaml|modular}"]
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| source_path | Yes | Path to the project or component to evolve |
| --to | No | Target structure (default: `flow`) |

## What It Does

1. Assesses current project structure and migration risk
2. Produces a staged refactor or migration plan
3. Applies structural changes with rollback guidance
4. Validates updated paths and runtime integrity

## Output

- Current vs target structure summary
- Planned or executed file operations
- Rollback instructions
- Validation checklist

## Response Contract (Required)

Every command response must include these sections in order:

1. `findings` - observations grounded in repository evidence
2. `plan` - ordered execution steps
3. `proposed changes` - concrete file/config changes (or `none`)
4. `validation steps` - checks to confirm correctness

## Related Commands

- `/crew inspect` - Evaluate architecture before migration
- `/crew fix` - Stabilize runtime before and after migration
- `/crew docs` - Regenerate documentation for the evolved structure
