# Task Commands Reference

Quick reference for task management CLI commands.

## Command Index

| Command | Purpose | Example |
|---------|---------|---------|
| `status [feature]` | Show task status | `status my-feature` |
| `next [feature]` | Show eligible tasks | `next my-feature` |
| `parallel [feature]` | Show parallelizable tasks | `parallel my-feature` |
| `deps <feature> <seq>` | Show dependency tree | `deps my-feature 05` |
| `blocked [feature]` | Show blocked tasks | `blocked my-feature` |
| `complete <feature> <seq> "summary"` | Mark task complete | `complete my-feature 05 "Done"` |
| `validate [feature]` | Validate JSON files | `validate my-feature` |

## Command Details

### status
Display summary of task status for a feature or all features.

### next
Show tasks that are ready to start (dependencies satisfied).

### parallel
Show tasks that can run in parallel (all have satisfied dependencies).

### deps
Display dependency tree for a specific subtask.

### blocked
Show tasks that are blocked and why.

### complete
Mark a subtask as complete. Requires a summary (max 200 chars).

### validate
Check JSON files for validity and verify dependency tree.

## Script Location

`.opencode/skill/task-management/scripts/task-cli.ts`

## Note

The task-cli.ts script was removed during cleanup. These commands are for reference only and would need to be reimplemented if needed.
