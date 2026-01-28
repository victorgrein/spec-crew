---
description: Analyze CrewAI crew performance and identify bottlenecks
agent: crewai-orchestrator
---

# /crew analyze

Analyze a CrewAI crew's performance, token usage, and identify optimization opportunities.

## Syntax

```
/crew analyze {crew_path}
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| crew_path | Yes | Path to the crew directory or file |

## Examples

```
/crew analyze ./my_crew

/crew analyze src/my_project/crews/research_crew

/crew analyze ./crew.py
```

## What It Does

1. **Reads** crew configuration and code
2. **Analyzes** agent LLM settings and configurations
3. **Estimates** token usage and costs
4. **Identifies** potential bottlenecks
5. **Checks** caching and rate limiting settings
6. **Provides** optimization recommendations

## Output

- Current configuration summary
- Token usage estimates
- Cost projections
- Bottleneck identification
- Optimization recommendations

## Analysis Areas

- **LLM Configuration**: Model choices, function calling LLM
- **Performance Settings**: max_iter, max_rpm, caching
- **Task Design**: Complexity, dependencies, context passing
- **Agent Design**: Tool assignments, delegation settings
- **Memory/Context**: Memory usage, context window management

## Related Commands

- `/crew optimize` - Apply optimizations
- `/crew review` - Review architecture
- `/crew debug` - Debug issues
