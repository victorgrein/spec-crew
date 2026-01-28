# Managing Tasks

This guide explains how to manage task breakdowns and track progress.

## Task States

- **pending** - Not started, waiting for dependencies
- **in_progress** - Currently being worked on
- **completed** - Finished and verified
- **blocked** - Cannot proceed due to issues

## Progress Tracking

Use the task management CLI to:
- Check status of all tasks
- Find next eligible tasks
- Identify blocked tasks
- Mark tasks as complete

## Best Practices

1. **Atomic Tasks** - Each task should be completable in 1-2 hours
2. **Clear Objectives** - Single, measurable outcome per task
3. **Dependencies** - Map dependencies accurately to prevent blocking
4. **Parallel Execution** - Mark independent tasks as parallel for efficiency

## CLI Commands

```bash
# Check status
npx ts-node .opencode/skill/task-management/scripts/task-cli.ts status

# Find next tasks
npx ts-node .opencode/skill/task-management/scripts/task-cli.ts next

# Mark complete
npx ts-node .opencode/skill/task-management/scripts/task-cli.ts complete <feature> <seq> "summary"
```
