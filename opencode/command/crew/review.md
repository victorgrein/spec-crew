---
description: Review CrewAI crew architecture and suggest improvements
agent: crewai-orchestrator
---

# /crew review

Review a CrewAI crew's architecture and provide improvement suggestions.

## Syntax

```
/crew review {crew_path}
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| crew_path | Yes | Path to the crew directory or file |

## Examples

```
/crew review ./my_crew

/crew review src/my_project/crews/research_crew

/crew review ./crew.py
```

## What It Does

1. **Reads** crew configuration and code
2. **Analyzes** architecture against best practices
3. **Checks** agent design (roles, goals, backstories)
4. **Validates** task design (descriptions, outputs, dependencies)
5. **Reviews** tool assignments
6. **Evaluates** process type choice
7. **Provides** improvement recommendations

## Review Checklist

### Architecture
- [ ] Clear separation of agent responsibilities
- [ ] Appropriate process type for workflow
- [ ] Proper task sequencing and dependencies
- [ ] Memory configuration if needed
- [ ] Cache settings optimized

### Agents
- [ ] Well-defined roles, goals, backstories
- [ ] Appropriate tools assigned
- [ ] LLM configuration suitable for tasks
- [ ] Delegation settings correct

### Tasks
- [ ] Clear descriptions and expected outputs
- [ ] Proper agent assignments
- [ ] Context passing configured
- [ ] Output files specified if needed

### Performance
- [ ] max_rpm set to avoid rate limits
- [ ] Appropriate max_iter values
- [ ] Caching enabled where beneficial

## Output

- Overall quality score (1-10)
- Strengths identified
- Issues found with severity
- Specific improvement recommendations
- Optimized architecture (if needed)

## Related Commands

- `/crew optimize` - Apply optimizations
- `/crew analyze` - Analyze performance
- `/crew docs` - Generate documentation
