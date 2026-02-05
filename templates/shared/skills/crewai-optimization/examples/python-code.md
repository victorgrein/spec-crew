# CrewAI Optimization - Python Code Examples

Python examples and implementation snippets for `crewai-optimization`.

## Extracted Python Snippets

### Python Example 1

```python
result = crew.kickoff(inputs={...})
print(f"Token Usage: {crew.usage_metrics}")
print(f"Execution Time: {execution_time}")
```

### Python Example 2

```python
for task_output in result.tasks_output:
    print(f"Task: {task_output.description[:50]}")
    print(f"Tokens: {task_output.token_usage}")
```

### Python Example 3

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

### Python Example 4

```python
# Manager with best model
manager = Agent(llm="gpt-4o")  # Best for coordination

# Workers with cheaper models
worker = Agent(
    llm="gpt-4o-mini",
    function_calling_llm="gpt-3.5-turbo"
)
```

### Python Example 5

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

### Python Example 6

```python
# Parallel execution
task1 = Task(..., async_execution=True)
task2 = Task(..., async_execution=True)
task3 = Task(..., context=[task1, task2])  # Waits for both
```

### Python Example 7

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

### Python Example 8

```python
review_task = Task(
    description="Review and improve the output",
    expected_output="Refined, high-quality output",
    agent=reviewer,
    context=[main_task]
)
```

### Python Example 9

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

### Python Example 10

```python
agent = Agent(
    llm="gpt-4o-mini",
    function_calling_llm="gpt-3.5-turbo",
    cache=True,
    max_iter=15
)
```

### Python Example 11

```python
agent = Agent(
    llm="gpt-4o",
    reasoning=True,
    max_iter=25,
    memory=True
)
```

### Python Example 12

```python
agent = Agent(
    llm="gpt-4o-mini",
    cache=True,
    max_iter=10,
    max_execution_time=60
)
```
