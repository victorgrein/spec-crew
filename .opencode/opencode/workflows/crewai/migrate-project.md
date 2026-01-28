# Migrate Project Workflow

## Overview

Workflow for migrating CrewAI projects to standard flow structure.

## Trigger

- `/crew migrate {source_path} --to="{flow_structure}"`
- `/crew refactor {crew_path} --pattern="modular|component"`
- `/crew standardize {project_path}`
- "migrate to flow", "refactor this project", "standardize structure"

## Context Dependencies

- `context/crewai/processes/migration.md`
- `context/crewai/domain/concepts/flows.md`
- `context/crewai/domain/concepts/crews.md`
- `context/crewai/standards/project-structure.md`

## Workflow Stages

### Stage 1: Analyze Current Project

**Action:** Understand current project structure

**Subagent:** @migration-specialist

**Process:**
1. Scan project directory structure
2. Identify existing crews and agents
3. Analyze task dependencies
4. Check for custom tools
5. Review configuration files

**Output:** Current state analysis

### Stage 2: Plan Migration

**Action:** Create migration plan

**Subagent:** @migration-specialist

**Process:**
1. Determine target structure
2. Map current components to new structure
3. Identify files to create/move/modify
4. Plan import updates
5. Create rollback strategy

**Output:** Migration plan

### Stage 3: Generate New Structure

**Action:** Create new project structure

**Subagent:** @migration-specialist, @coder-agent

**Process:**
1. Generate new directory structure
2. Create flow class if migrating to flow
3. Move/update crew files
4. Update imports
5. Generate new configuration files

**Output:** New project files

### Stage 4: Validate Migration

**Action:** Validate migrated project

**Process:**
1. Check all files are in place
2. Validate imports
3. Check configuration consistency
4. Verify no functionality lost
5. Generate test commands

**Output:** Validation report

### Stage 5: Present and Execute

**Action:** Present migration plan and execute

**Process:**
1. Show before/after structure
2. List all file operations
3. Ask user permission
4. Execute migration
5. Provide verification steps

**Output:** Migrated project

## Success Criteria

- [ ] Current structure fully analyzed
- [ ] Migration plan is complete
- [ ] All files mapped to new locations
- [ ] Imports updated correctly
- [ ] No functionality lost
- [ ] User confirmed migration
- [ ] Verification steps provided

## Output Format

```
## Migration Plan

### Current Structure
```
{current_structure}
```

### Target Structure
```
{target_structure}
```

### Migration Type
{crew_to_flow|code_to_yaml|monolithic_to_modular}

### File Operations

#### Files to Create
| File | Purpose |
|------|---------|
| {path} | {purpose} |

#### Files to Move
| From | To |
|------|-----|
| {old_path} | {new_path} |

#### Files to Modify
| File | Changes |
|------|---------|
| {path} | {changes} |

#### Files to Delete (after backup)
| File | Reason |
|------|--------|
| {path} | {reason} |

### New Flow Structure
```python
{flow_code}
```

### Backup Location
`.backup/{timestamp}/`

### Verification Steps
1. Run `crewai install`
2. Run `crewai run`
3. Verify output matches original

### Rollback Command
```bash
cp -r .backup/{timestamp}/* .
```

**Execute this migration? [y/n]**
```

## Migration Patterns

### Crew to Flow
1. Create flow project structure
2. Move crew to crews/ directory
3. Create Flow class
4. Update entry points

### Code to YAML
1. Extract agent definitions to agents.yaml
2. Extract task definitions to tasks.yaml
3. Update crew class to use @CrewBase
4. Add decorators

### Monolithic to Modular
1. Identify logical groupings
2. Create separate crews
3. Extract shared tools
4. Create orchestrating flow
