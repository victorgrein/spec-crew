# CrewAI Workflows Navigation

## Overview

Automated workflows for common CrewAI operations.

## Available Workflows

| Workflow | Trigger | Description |
|----------|---------|-------------|
| [create-crew.md](create-crew.md) | `/crew create` | Create new crew from specification |
| [create-flow.md](create-flow.md) | `/crew generate-flow` | Create flow with crew integration |
| [debug-crew.md](debug-crew.md) | `/crew debug`, `/crew fix` | Debug execution issues |
| [optimize-crew.md](optimize-crew.md) | `/crew optimize` | Optimize for cost/latency/quality |
| [migrate-project.md](migrate-project.md) | `/crew migrate` | Migrate to standard structure |

## Workflow Selection

| Situation | Workflow |
|-----------|----------|
| New crew needed | create-crew |
| Multi-crew orchestration | create-flow |
| Errors occurring | debug-crew |
| Too slow/expensive | optimize-crew |
| Restructuring needed | migrate-project |

## Quick Reference

### Create Crew
```
/crew create "A research crew that analyzes market trends"
```

### Create Flow
```
/crew generate-flow "content_pipeline"
```

### Debug
```
/crew debug ./my_crew --trace="abc123"
/crew fix ./my_crew --issue="rate limit errors"
```

### Optimize
```
/crew optimize ./my_crew --target="cost"
/crew analyze ./my_crew
```

### Migrate
```
/crew migrate ./old_crew --to="flow"
/crew standardize ./my_project
```

## Workflow Stages

All workflows follow similar stages:

1. **Analyze** - Understand requirements/current state
2. **Design** - Plan the solution
3. **Generate** - Create code/configuration
4. **Validate** - Check for issues
5. **Present** - Show results and ask permission

## Context Loading

Each workflow specifies required context files:
- Domain concepts for understanding
- Templates for generation
- Standards for validation
- Processes for step-by-step guidance
