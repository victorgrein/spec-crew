# Create Crew Workflow

## Overview

Workflow for creating a complete CrewAI crew from natural language specification.

## Trigger

- `/crew create "{specification}"`
- "create a crew for...", "build a crew that..."

## Context Dependencies

- `context/crewai/domain/concepts/crews.md`
- `context/crewai/domain/concepts/agents.md`
- `context/crewai/domain/concepts/tasks.md`
- `context/crewai/templates/agent-yaml.md`
- `context/crewai/templates/task-yaml.md`
- `context/crewai/standards/project-structure.md`

## Workflow Stages

### Stage 1: Analyze Specification

**Action:** Parse user specification to extract requirements

**Process:**
1. Identify the crew's primary objective
2. Determine required agents and their roles
3. Identify tasks and their dependencies
4. Determine process type (sequential/hierarchical)
5. Identify required tools

**Output:** Structured requirements document

### Stage 2: Design Architecture

**Action:** Design crew architecture based on requirements

**Subagent:** @crew-architect

**Process:**
1. Define agent roles, goals, backstories
2. Design task flow and dependencies
3. Select appropriate process type
4. Assign tools to agents
5. Configure LLM settings (ask user for preference)

**Output:** Architecture design document

### Stage 3: Generate Configuration

**Action:** Generate YAML configuration files

**Subagent:** @agent-designer, @task-designer

**Process:**
1. Generate agents.yaml from architecture
2. Generate tasks.yaml from architecture
3. Validate configuration syntax
4. Check for consistency

**Output:** YAML configuration files

### Stage 4: Generate Code

**Action:** Generate crew class implementation

**Subagent:** @coder-agent (existing)

**Process:**
1. Generate crew.py with @CrewBase decorator
2. Generate main.py entry point
3. Generate custom tools if needed
4. Generate pyproject.toml

**Output:** Python code files

### Stage 5: Validate and Present

**Action:** Validate generated crew and present to user

**Process:**
1. Validate all files are consistent
2. Check for common issues
3. Present complete crew to user
4. Ask for confirmation before writing files

**Output:** Complete crew ready for deployment

## Success Criteria

- [ ] All agents have clear roles, goals, backstories
- [ ] All tasks have clear descriptions and expected outputs
- [ ] Task dependencies are correctly defined
- [ ] Process type matches workflow complexity
- [ ] LLM configuration is appropriate
- [ ] Code follows CrewAI best practices
- [ ] User has confirmed file creation

## Output Format

```
## Crew Created: {crew_name}

### Architecture
{architecture_diagram}

### Agents
| Agent | Role | Tools |
|-------|------|-------|
| ... | ... | ... |

### Tasks
| Task | Agent | Dependencies |
|------|-------|--------------|
| ... | ... | ... |

### Files to Create
- src/{crew_name}/crew.py
- src/{crew_name}/config/agents.yaml
- src/{crew_name}/config/tasks.yaml
- src/{crew_name}/main.py

### Configuration
```yaml
# agents.yaml
{agents_yaml}
```

```yaml
# tasks.yaml
{tasks_yaml}
```

### Code
```python
# crew.py
{crew_code}
```

**Create these files? [y/n]**
```

## Error Handling

- If specification is unclear, ask clarifying questions
- If tools are unavailable, suggest alternatives
- If LLM preference not specified, ask user
