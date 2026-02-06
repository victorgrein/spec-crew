---
name: create-crew
description: Create a complete CrewAI crew from natural language specification. Use when asked to build, create, or generate a new crew.
context: fork
agent: general-purpose
skills:
  - core-build
  - tools
  - governance
---

# Create Crew Workflow

Create a CrewAI crew based on the specification: $ARGUMENTS

## Your Process

### Stage 1: Analyze Specification
1. Parse the user specification to extract requirements
2. Identify the crew's primary objective
3. Determine required agents and their roles
4. Identify tasks and their dependencies
5. Determine process type (sequential/hierarchical)
6. Identify required tools

### Stage 2: Design Architecture
1. Define agent roles, goals, backstories
2. Design task flow and dependencies
3. Select appropriate process type
4. Assign tools to agents
5. Ask user for LLM preference (OpenAI/Anthropic model)

### Stage 3: Generate Configuration
1. Generate agents.yaml from architecture
2. Generate tasks.yaml from architecture
3. Validate configuration syntax
4. Check for consistency

### Stage 4: Generate Code
1. Generate crew.py with @CrewBase decorator
2. Generate main.py entry point
3. Generate custom tools if needed
4. Generate pyproject.toml

### Stage 5: Validate and Present
1. Validate all files are consistent
2. Check for common issues
3. Present complete crew to user
4. Ask for confirmation before writing files

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

## Success Criteria
- [ ] All agents have clear roles, goals, backstories
- [ ] All tasks have clear descriptions and expected outputs
- [ ] Task dependencies are correctly defined
- [ ] Process type matches workflow complexity
- [ ] LLM configuration is appropriate
- [ ] Code follows CrewAI best practices
- [ ] User has confirmed file creation
