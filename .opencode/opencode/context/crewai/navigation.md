# CrewAI Context Navigation

## Overview

Comprehensive CrewAI knowledge base organized for efficient context loading.

## Directory Structure

```
crewai/
├── domain/
│   ├── concepts/           # Core CrewAI concepts
│   │   ├── flows.md        # Flow architecture
│   │   ├── crews.md        # Crew configuration
│   │   ├── agents.md       # Agent design
│   │   ├── tasks.md        # Task configuration
│   │   ├── tools.md        # Tool creation
│   │   ├── llms.md         # LLM configuration
│   │   ├── memory.md       # Memory system
│   │   ├── processes.md    # Process types
│   │   └── cli.md          # CLI commands
│   └── navigation.md
├── processes/              # Step-by-step workflows
│   ├── crew-creation.md    # Create new crews
│   ├── debugging.md        # Debug issues
│   ├── optimization.md     # Optimize performance
│   ├── migration.md        # Migrate projects
│   └── navigation.md
├── standards/              # Quality standards
│   ├── code-quality.md     # Code standards
│   ├── project-structure.md # Project structure
│   └── navigation.md
├── templates/              # Reusable templates
│   ├── agent-yaml.md       # Agent templates
│   ├── task-yaml.md        # Task templates
│   ├── flow-class.md       # Flow templates
│   └── navigation.md
└── navigation.md           # This file
```

## Context Loading Strategy

### Level 1: Minimal (Single Task)

Load only the specific file needed:

| Task | Load |
|------|------|
| Create agent | `domain/concepts/agents.md` |
| Create task | `domain/concepts/tasks.md` |
| Create tool | `domain/concepts/tools.md` |
| Configure LLM | `domain/concepts/llms.md` |

### Level 2: Standard (Related Files)

Load related concept files:

| Task | Load |
|------|------|
| Create crew | `crews.md`, `agents.md`, `tasks.md` |
| Create flow | `flows.md`, `crews.md` |
| Debug issue | `processes/debugging.md`, relevant concept |
| Optimize | `processes/optimization.md`, `llms.md` |

### Level 3: Comprehensive (Full Context)

Load all relevant files:

| Task | Load |
|------|------|
| Migrate project | All concepts, `processes/migration.md`, standards |
| Full system design | All concepts, all templates, standards |
| Complex debugging | All concepts, `processes/debugging.md` |

## Quick Reference

### Creating Components

| Component | Primary File | Templates |
|-----------|--------------|-----------|
| Crew | `domain/concepts/crews.md` | - |
| Flow | `domain/concepts/flows.md` | `templates/flow-class.md` |
| Agent | `domain/concepts/agents.md` | `templates/agent-yaml.md` |
| Task | `domain/concepts/tasks.md` | `templates/task-yaml.md` |
| Tool | `domain/concepts/tools.md` | - |

### Common Operations

| Operation | Process File | Concepts Needed |
|-----------|--------------|-----------------|
| Create crew | `processes/crew-creation.md` | crews, agents, tasks |
| Debug | `processes/debugging.md` | All relevant |
| Optimize | `processes/optimization.md` | llms |
| Migrate | `processes/migration.md` | All |

### Standards

| Standard | File |
|----------|------|
| Code quality | `standards/code-quality.md` |
| Project structure | `standards/project-structure.md` |

## File Sizes

All files optimized for context efficiency:
- Concept files: 100-200 lines each
- Process files: 100-150 lines each
- Template files: 100-200 lines each
- Total: ~2500 lines

## Usage Tips

1. **Start minimal**: Load only what's needed
2. **Add as needed**: Load more context if task requires
3. **Use templates**: Copy and customize templates
4. **Follow standards**: Check standards for quality
5. **Use processes**: Follow step-by-step workflows
