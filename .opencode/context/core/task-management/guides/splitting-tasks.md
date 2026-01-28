# Splitting Tasks

This guide explains how to break down features into atomic subtasks.

## Principles

### Atomicity
Each subtask should:
- Be completable in 1-2 hours
- Have a single, clear objective
- Be independently verifiable
- Not depend on multiple other tasks

### Dependency Management
- **Sequential**: Task B depends on Task A completing
- **Parallel**: Tasks can run simultaneously with no dependencies
- **Independent**: Task doesn't affect or depend on others

## Breaking Down Features

### Step 1: Identify Core Components
Break the feature into logical components:
- Data structures
- API endpoints
- UI components
- Business logic

### Step 2: Define Natural Boundaries
Group related work into tasks:
- One file/module per task when possible
- Related tests together
- Configuration separate from code

### Step 3: Establish Dependencies
Map what must come first:
- Data structures before APIs
- APIs before UI
- Core logic before edge cases

### Step 4: Mark Parallel Tasks
Identify independent work:
- Different modules can be built in parallel
- Tests can be written alongside code
- Documentation can be created independently

## Example

Bad breakdown:
1. Build entire feature (too large)

Good breakdown:
1. Create data models (independent)
2. Implement API endpoints [parallel]
3. Build UI components [parallel]
4. Integrate API with UI (depends on 2,3)
5. Write tests (depends on 1-4)
