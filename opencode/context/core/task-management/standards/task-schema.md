# Task Schema Standards

JSON schema definitions for task and subtask files.

## task.json Schema

```json
{
  "id": "string",           // kebab-case feature identifier
  "name": "string",         // Human-readable feature name
  "status": "string",       // active | completed
  "objective": "string",    // Max 200 chars
  "context_files": ["string"], // Array of file paths
  "exit_criteria": ["string"], // Completion criteria
  "subtask_count": "number",   // Total subtasks
  "completed_count": "number",  // Completed subtasks
  "created_at": "ISO8601",   // Creation timestamp
  "completed_at": "ISO8601 | null" // Completion timestamp
}
```

## subtask_##.json Schema

```json
{
  "id": "string",           // {feature}-{seq}
  "seq": "string",         // 2-digit zero-padded (01, 02...)
  "title": "string",       // Human-readable task title
  "status": "string",     // pending | in_progress | completed | blocked
  "depends_on": ["string"], // Array of dependency seqs
  "parallel": "boolean",   // Can run in parallel
  "context_files": ["string"], // Context for this task
  "acceptance_criteria": ["string"], // Pass/fail criteria
  "deliverables": ["string"], // Files/endpoints to create
  "agent_id": "string",   // Agent working on task
  "started_at": "ISO8601 | null",
  "completed_at": "ISO8601 | null",
  "completion_summary": "string | null" // Max 200 chars
}
```

## Directory Structure

```
.tmp/tasks/
├── {feature-slug}/
│   ├── task.json
│   ├── subtask_01.json
│   ├── subtask_02.json
│   └── ...
└── completed/
    └── {feature-slug}/
```

## Naming Conventions

- **Features**: kebab-case (e.g., `user-authentication`)
- **Sequence numbers**: 2-digit zero-padded (01, 02, 03...)
- **File names**: `subtask_{seq}.json`
- **Agent IDs**: dash-case (e.g., `coder-agent`)

## Status Flow

```
pending → in_progress → completed
         ↓
      blocked
```

## Validation Rules

1. All subtask IDs must follow pattern `{feature}-{seq}`
2. Dependencies must reference valid sequence numbers
3. Parallel tasks cannot depend on each other
4. Completion summary max 200 characters
5. Exit criteria must be defined for each feature
