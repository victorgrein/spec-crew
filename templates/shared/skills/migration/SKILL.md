---
name: migration
description: Consolidated skill pack for CrewAI migration and refactor workflows, including staged rollouts, integration checks, and rollback planning.
version: 1.0.0
---

# Migration

## What This Pack Covers

Migration and structural evolution guidance for safe project changes.

- Crew-to-flow migration planning
- Module and directory refactoring
- Compatibility checkpoints
- Rollback strategy and release safety

## Use This Pack When

- The request targets `/crew evolve` outcomes.
- The user asks to migrate architecture or modernize structure.
- Structural changes carry rollback risk.

## Normalized Trigger Phrases

- migrate crew
- crew to flow migration
- refactor project structure
- modularize package layout
- rollback plan

## Operating Rules

- Sequence migrations into reversible phases.
- Preserve behavior unless change is explicitly requested.
- Validate integration integrity before each phase gate.

## Additional Resources

- `references/index.md`
- `examples/index.md`
