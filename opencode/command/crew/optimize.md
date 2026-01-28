---
description: Optimize CrewAI crew for cost, latency, or quality
agent: crewai-orchestrator
---

# /crew optimize

Optimize a CrewAI crew for a specific target: cost reduction, latency improvement, or quality enhancement.

## Syntax

```
/crew optimize {crew_path} --target="{cost|latency|quality}"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| crew_path | Yes | Path to the crew directory or file |
| --target | No | Optimization target (default: cost) |

## Examples

```
/crew optimize ./my_crew --target="cost"

/crew optimize ./research_crew --target="latency"

/crew optimize ./critical_crew --target="quality"
```

## Optimization Targets

### Cost
- Use cheaper models (gpt-4o-mini, claude-3-haiku)
- Separate function_calling_llm with cheaper model
- Enable caching
- Reduce max_iter

### Latency
- Use faster models
- Enable caching
- Use async execution
- Set execution timeouts

### Quality
- Use best models (gpt-4o, claude-3-5-sonnet)
- Enable reasoning
- Increase max_iter
- Enable memory

## What It Does

1. **Analyzes** current configuration
2. **Identifies** optimization opportunities
3. **Generates** optimized configuration
4. **Asks** for LLM preference
5. **Shows** before/after comparison
6. **Requests** permission to apply changes

## Output

- Current vs optimized configuration
- Expected improvement metrics
- Code changes to apply
- Verification steps

## Related Commands

- `/crew analyze` - Analyze without optimizing
- `/crew review` - Review architecture
