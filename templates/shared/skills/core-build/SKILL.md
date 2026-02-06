---
name: core-build
description: Consolidated skill pack for CrewAI build workflows, including crew design, agent/task configuration, process selection, and initialization patterns.
version: 1.0.0
---

# Core Build

## What This Pack Covers

Build-time design and implementation guidance for creating and updating CrewAI projects.

- Crew composition and process strategy
- Agent contracts (role, goal, backstory, boundaries)
- Task contracts, dependencies, and expected outputs
- Bootstrap and initialization workflows

## Use This Pack When

- The request is about creating or restructuring crews, agents, or tasks.
- A command path is anchored on `/crew init`.
- The user needs process choice guidance (`sequential` vs `hierarchical`).

## Normalized Trigger Phrases

- create crew
- create agent
- define task
- configure process
- bootstrap project

## Operating Rules

- Keep one primary owner per command outcome.
- Keep outputs contract-first and validation-ready.
- Keep deep implementation details in references and examples.

## Additional Resources

- `references/index.md`
- `examples/index.md`
