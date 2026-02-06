---
name: flows
description: Consolidated skill pack for CrewAI flow orchestration, including state design, routing, listeners, and parallel branch coordination.
version: 1.0.0
---

# Flows

## What This Pack Covers

Flow-specific architecture and execution guidance for event-driven CrewAI systems.

- Flow class and state modeling
- `@start`, `@listen`, and router usage
- Branching, joins, and resumability patterns
- Flow reliability and observability checkpoints

## Use This Pack When

- The request involves flow authoring, refactoring, or orchestration.
- The user asks for routing logic, listeners, or state transitions.
- A migration targets flow-first architecture.

## Normalized Trigger Phrases

- create flow
- flow routing
- flow state
- listen router decorators
- event driven orchestration

## Operating Rules

- Keep state transitions explicit and typed where possible.
- Keep route selection deterministic and testable.
- Keep branch merge logic simple and observable.

## Additional Resources

- `references/index.md`
- `examples/index.md`
