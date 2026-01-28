# CrewAI Optimization Process

## Overview

Systematic approach to optimizing CrewAI crews for cost, latency, or quality.

## Optimization Targets

### Cost Optimization

**Goal:** Reduce API costs while maintaining acceptable quality

**Strategies:**
1. Use cheaper models for simple tasks
2. Separate function_calling_llm (cheaper model for tools)
3. Enable caching
4. Reduce max_iter
5. Optimize prompts for fewer tokens

**Implementation:**
```python
agent = Agent(
    role="...",
    llm="gpt-4o-mini",  # Cheaper main model
    function_calling_llm="gpt-3.5-turbo",  # Even cheaper for tools
    cache=True,
    max_iter=15,
    respect_context_window=True
)
```

### Latency Optimization

**Goal:** Reduce execution time

**Strategies:**
1. Use faster models
2. Enable caching
3. Use async execution
4. Reduce max_iter
5. Set execution timeouts

**Implementation:**
```python
agent = Agent(
    role="...",
    llm="gpt-4o-mini",  # Fast model
    cache=True,
    max_iter=10,
    max_execution_time=60
)

# Use async kickoff
result = await crew.akickoff(inputs={...})
```

### Quality Optimization

**Goal:** Maximize output quality

**Strategies:**
1. Use best models
2. Enable reasoning
3. Increase max_iter
4. Enable memory
5. Add validation tasks

**Implementation:**
```python
agent = Agent(
    role="...",
    llm="gpt-4o",  # Best quality
    reasoning=True,
    max_iter=25,
    memory=True,
    verbose=True
)
```

## Optimization Process

### Step 1: Baseline Measurement

**Collect metrics:**
```python
result = crew.kickoff(inputs={...})
print(f"Token Usage: {crew.usage_metrics}")
print(f"Execution Time: {execution_time}")
```

**Document baseline:**
- Total tokens
- Execution time
- Output quality (manual assessment)
- Cost estimate

### Step 2: Identify Bottlenecks

**Analyze token usage by component:**
```python
for task_output in result.tasks_output:
    print(f"Task: {task_output.description[:50]}")
    print(f"Tokens: {task_output.token_usage}")
```

**Common bottlenecks:**
- High token usage in specific agents
- Long execution time in specific tasks
- Excessive API calls (low cache hit rate)
- Agent loops (max_iter reached)

### Step 3: Apply Optimizations

**For cost:**
```python
# Tiered model strategy
manager = Agent(llm="gpt-4o")  # Best for coordination
worker = Agent(
    llm="gpt-4o-mini",
    function_calling_llm="gpt-3.5-turbo"
)
```

**For latency:**
```python
# Parallel execution
task1 = Task(..., async_execution=True)
task2 = Task(..., async_execution=True)
task3 = Task(..., context=[task1, task2])  # Waits for both
```

**For quality:**
```python
# Add review task
review_task = Task(
    description="Review and improve the output",
    expected_output="Refined, high-quality output",
    agent=reviewer,
    context=[main_task]
)
```

### Step 4: Measure Improvement

**Compare to baseline:**
- Token reduction %
- Time reduction %
- Quality change (better/same/worse)
- Cost savings

### Step 5: Iterate

**Fine-tune based on results:**
- Adjust model choices
- Tune max_iter values
- Optimize prompts
- Add/remove caching

## Model Selection Guide

| Optimization | Main LLM | Function Calling LLM |
|--------------|----------|---------------------|
| Cost | gpt-4o-mini | gpt-3.5-turbo |
| Latency | gpt-4o-mini | gpt-4o-mini |
| Quality | gpt-4o | gpt-4o-mini |
| Balanced | gpt-4o-mini | gpt-3.5-turbo |

## Cost Estimation

```python
def estimate_cost(metrics, model="gpt-4o"):
    prices = {
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    }
    price = prices.get(model, prices["gpt-4o"])
    input_cost = (metrics["prompt_tokens"] / 1000) * price["input"]
    output_cost = (metrics["completion_tokens"] / 1000) * price["output"]
    return input_cost + output_cost
```

## Optimization Checklist

- [ ] Baseline metrics collected
- [ ] Bottlenecks identified
- [ ] Optimization target chosen (cost/latency/quality)
- [ ] Appropriate models selected
- [ ] Caching enabled
- [ ] max_iter tuned
- [ ] Async execution where applicable
- [ ] Improvement measured
- [ ] Quality verified
