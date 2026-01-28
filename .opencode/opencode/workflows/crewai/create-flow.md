# Create Flow Workflow

## Overview

Workflow for creating a CrewAI Flow with crew integration.

## Trigger

- `/crew generate-flow "{flow_type}"`
- "create a flow for...", "build a flow that..."

## Context Dependencies

- `context/crewai/domain/concepts/flows.md`
- `context/crewai/domain/concepts/crews.md`
- `context/crewai/templates/flow-class.md`
- `context/crewai/standards/project-structure.md`

## Workflow Stages

### Stage 1: Analyze Requirements

**Action:** Parse flow requirements

**Process:**
1. Identify flow objective
2. Determine number of stages
3. Identify crews to integrate
4. Determine state requirements
5. Identify routing/conditional logic needed

**Output:** Flow requirements document

### Stage 2: Design Flow Architecture

**Action:** Design flow structure

**Subagent:** @flow-engineer

**Process:**
1. Define flow state model (Pydantic)
2. Design stage sequence
3. Plan crew integration points
4. Design routing logic if needed
5. Plan error handling

**Output:** Flow architecture design

### Stage 3: Generate Flow Code

**Action:** Generate flow implementation

**Subagent:** @flow-engineer, @coder-agent

**Process:**
1. Generate state model class
2. Generate flow class with decorators
3. Generate crew integration code
4. Generate main.py entry point
5. Generate visualization code

**Output:** Flow Python code

### Stage 4: Generate Supporting Files

**Action:** Generate project files

**Process:**
1. Generate pyproject.toml
2. Generate README.md
3. Create directory structure
4. Generate .env template

**Output:** Complete project structure

### Stage 5: Validate and Present

**Action:** Validate and present to user

**Process:**
1. Validate flow structure
2. Generate flow diagram
3. Present complete flow
4. Ask for confirmation

**Output:** Complete flow ready for deployment

## Success Criteria

- [ ] Flow state model is well-defined
- [ ] All stages have clear purposes
- [ ] Crew integrations are correct
- [ ] Routing logic is sound
- [ ] Error handling is included
- [ ] Visualization works
- [ ] User has confirmed file creation

## Output Format

```
## Flow Created: {flow_name}

### Flow Diagram
```
{ascii_or_mermaid_diagram}
```

### State Model
```python
{state_model}
```

### Flow Implementation
```python
{flow_code}
```

### Crews Integrated
- {crew_1}: {purpose}
- {crew_2}: {purpose}

### Files to Create
- src/{flow_name}/main.py
- src/{flow_name}/crews/{crew}/...

**Create these files? [y/n]**
```

## Flow Patterns

### Linear Flow
```
@start → @listen → @listen → End
```

### Router Flow
```
@start → @router → "path_a" → End
                 → "path_b" → End
```

### Parallel Flow
```
@start → @listen (parallel) → @listen(and_) → End
       → @listen (parallel) ↗
```

### Crew Integration Flow
```
@start → prepare → run_crew_1 → run_crew_2 → finalize
```
