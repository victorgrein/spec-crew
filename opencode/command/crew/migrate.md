---
description: Migrate CrewAI project to standard flow structure
agent: crewai-orchestrator
---

# /crew migrate

Migrate a CrewAI project to standard flow structure or refactor existing structure.

## Syntax

```
/crew migrate {source_path} --to="{target_structure}"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| source_path | Yes | Path to the project to migrate |
| --to | No | Target structure (flow, yaml, modular) |

## Examples

```
/crew migrate ./my_crew --to="flow"

/crew migrate ./old_project --to="yaml"

/crew migrate ./monolithic_crew --to="modular"
```

## Migration Types

### Crew to Flow (`--to="flow"`)
- Convert standalone crew to flow-based architecture
- Create Flow class that orchestrates crew
- Update project structure

### Code to YAML (`--to="yaml"`)
- Move inline agent/task definitions to YAML
- Update crew class to use @CrewBase
- Add decorators

### Monolithic to Modular (`--to="modular"`)
- Break large crew into smaller crews
- Extract shared tools
- Create orchestrating flow

## What It Does

1. **Analyzes** current project structure
2. **Creates** migration plan
3. **Generates** new structure
4. **Creates** backup of original
5. **Shows** before/after comparison
6. **Requests** permission to execute
7. **Provides** verification steps

## Output

- Current vs target structure
- File operations (create, move, modify, delete)
- New code/configuration
- Backup location
- Rollback instructions
- Verification steps

## Related Commands

- `/crew standardize` - Apply standard structure
- `/crew refactor` - Refactor specific patterns
