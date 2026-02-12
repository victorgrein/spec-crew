# Delegation Patterns

## Pattern 1: Single Owner
Use for one clear task.

`Ask the [specialist] to [action] with [paths/constraints/deliverables].`

## Pattern 2: Parallel Owners
Use for independent tasks.

`Ask the following specialists to work in parallel: [A task], [B task].`

## Pattern 3: Sequential Owners
Use when one output feeds the next.

`First ask [specialist A] to [task A]. Then ask [specialist B] to [task B using A output].`

## Pattern 4: Auditor Review then Implementation
Use for `/crew fix` or similar requests.

1. Ask `auditor` to perform read-only root-cause analysis.
2. Ask `builder` or `flow` to implement approved changes from auditor recommendations.

## Minimum Delegation Payload

- Goal
- Scope and file paths
- Allowed skills for selected specialist
- Deliverables
- Validation criteria
