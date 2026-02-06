---
name: optimize-crew
description: Optimize CrewAI crews for cost, latency, or quality. Use when asked to reduce costs, make faster, or improve quality.
context: fork
agent: general-purpose
skills:
  - runtime
  - tools
---

# Optimize Crew Workflow

Optimize the CrewAI crew for: $ARGUMENTS

## Your Process

### Stage 1: Analyze Current State
1. Read crew configuration
2. Analyze agent LLM settings
3. Check caching configuration
4. Review task complexity
5. Estimate current costs

### Stage 2: Identify Bottlenecks
1. Identify high token usage components
2. Find slow execution paths
3. Check cache hit rates
4. Analyze API call patterns
5. Review agent iteration counts

### Stage 3: Generate Recommendations
Based on target (cost/latency/quality):

**Cost Optimization:**
- Use cheaper models (gpt-4o-mini, claude-3-haiku)
- Enable caching
- Reduce iterations
- Use function_calling_llm with cheaper model

**Latency Optimization:**
- Use faster models
- Enable caching
- Use async execution
- Set timeouts

**Quality Optimization:**
- Use better models (gpt-4o, claude-3-5-sonnet)
- Enable reasoning
- Increase iterations
- Enable memory

### Stage 4: Generate Optimized Configuration
1. Generate optimized agent configurations
2. Update LLM settings
3. Configure caching
4. Adjust iteration limits
5. Add rate limiting

### Stage 5: Present and Apply
1. Show before/after comparison
2. Estimate impact
3. Ask user for LLM preferences
4. Ask permission to apply changes

## Output Format

```
## Optimization Report

### Current State
| Metric | Value |
|--------|-------|
| Estimated Cost/Run | ${cost} |
| Estimated Time | {time} |
| Token Usage | {tokens} |

### Bottlenecks Identified
1. **{bottleneck_1}**: {description}
2. **{bottleneck_2}**: {description}

### Optimization Target: {cost|latency|quality}

### Recommendations

#### Priority 1 (High Impact)
{recommendation}
```python
{code_change}
```
**Expected Improvement**: {improvement}

#### Priority 2 (Medium Impact)
{recommendation}

### LLM Configuration
**Which model would you like to use?**
- OpenAI: gpt-4o, gpt-4o-mini, gpt-3.5-turbo
- Anthropic: claude-3-5-sonnet, claude-3-haiku

### Expected Results
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Cost | ${before} | ${after} | -{percent}% |
| Time | {before} | {after} | -{percent}% |

**Apply these optimizations? [y/n]**
```

## Optimization Code Examples

### Cost Optimization
```python
agent = Agent(
    llm="gpt-4o-mini",
    function_calling_llm="gpt-3.5-turbo",
    cache=True,
    max_iter=15
)
```

### Latency Optimization
```python
agent = Agent(
    llm="gpt-4o-mini",
    cache=True,
    max_iter=10,
    max_execution_time=60
)
# Use async
result = await crew.akickoff()
```

### Quality Optimization
```python
agent = Agent(
    llm="gpt-4o",
    reasoning=True,
    max_iter=25,
    memory=True
)
```

## Success Criteria
- [ ] Baseline metrics collected
- [ ] Bottlenecks identified
- [ ] Recommendations prioritized
- [ ] Expected improvement estimated
- [ ] User confirmed LLM choices
- [ ] Changes applied successfully
