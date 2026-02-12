# Crew Attributes Reference

Complete reference of all Crew configuration attributes in CrewAI.

## Required Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `agents` | List[Agent] | - | List of agents in the crew |
| `tasks` | List[Task] | - | List of tasks to execute |

## Optional Attributes

### Process Configuration

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `process` | Process | sequential | Execution flow: `sequential` or `hierarchical` |
| `manager_llm` | str/LLM | None | LLM for manager in hierarchical process |
| `manager_agent` | Agent | None | Custom manager agent for hierarchical process |

### Execution Control

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `verbose` | bool/int | False | Logging level: False, True, or 0-2 for verbosity levels |
| `memory` | bool | False | Enable long-term memory across executions |
| `max_iterations` | int | None | Maximum iterations for crew execution |
| `max_rpm` | int | None | Rate limit in requests per minute |
| `timeout` | int | None | Maximum execution time in seconds |

### Output Configuration

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `output_log_file` | str | None | Path to save execution logs |
| `output_callback` | Callable | None | Callback function for outputs |
| `step_callback` | Callable | None | Callback after each step |
| `task_callback` | Callable | None | Callback after each task |

### Caching and Performance

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `cache` | bool | True | Enable response caching |
| `embedder` | dict | None | Custom embedding configuration for memory |

### Planning and Callbacks

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `planning` | bool | False | Enable planning phase before execution |
| `planning_llm` | str/LLM | None | LLM for planning phase |
| `function_calling_llm` | str/LLM | None | LLM for function/tool calling |

## Process Types

### Sequential Process

Tasks execute in order, one after another. Each task can access outputs from previous tasks via context.

```python
from crewai import Crew, Process

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2, task3],
    process=Process.sequential,
    verbose=True
)
```

**Best for:**
- Linear workflows
- Tasks with clear dependencies
- Simple pipelines

### Hierarchical Process

Manager agent coordinates task execution, delegates to workers, and reviews results.

```python
from crewai import Crew, Process

crew = Crew(
    agents=[agent1, agent2, manager_agent],
    tasks=[task1, task2],
    process=Process.hierarchical,
    manager_llm="gpt-4",
    verbose=True
)
```

**Best for:**
- Complex projects requiring oversight
- Multi-step workflows with decision points
- Quality assurance needs

## Attribute Details

### Verbose Levels

- `False` or `0`: No logging
- `True` or `1`: Basic logging
- `2`: Detailed logging with intermediate outputs

### Memory Configuration

When enabled, crew maintains context across executions:

```python
crew = Crew(
    agents=agents,
    tasks=tasks,
    memory=True,
    embedder={
        "provider": "openai",
        "config": {"model": "text-embedding-3-small"}
    }
)
```

### Rate Limiting

Control API usage with max_rpm:

```python
crew = Crew(
    agents=agents,
    tasks=tasks,
    max_rpm=10,  # Maximum 10 requests per minute
    max_iterations=50
)
```

### Planning Mode

Enable planning phase for complex workflows:

```python
crew = Crew(
    agents=agents,
    tasks=tasks,
    planning=True,
    planning_llm="gpt-4"
)
```

## Usage Examples

### Basic Crew
```python
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    verbose=True
)
```

### Advanced Crew with All Features
```python
crew = Crew(
    agents=[agent1, agent2, agent3, manager],
    tasks=[task1, task2, task3, task4],
    process=Process.hierarchical,
    manager_agent=manager,
    memory=True,
    cache=True,
    verbose=2,
    max_rpm=20,
    planning=True,
    output_log_file="logs/execution.log"
)
```

### Async Execution Crew
```python
crew = Crew(
    agents=[processor1, processor2],
    tasks=async_task1, async_task2,
    process=Process.sequential,
    verbose=True
)
result = crew.kickoff_async()
```

## Execution Methods

### kickoff()
Standard synchronous execution:
```python
result = crew.kickoff(inputs={"topic": "AI"})
```

### kickoff_async()
Asynchronous execution:
```python
result = await crew.kickoff_async(inputs={"topic": "AI"})
```

### kickoff_for_each()
Execute for multiple inputs:
```python
inputs_list = [
    {"topic": "AI"},
    {"topic": "ML"},
    {"topic": "Data Science"}
]
results = crew.kickoff_for_each(inputs=inputs_list)
```

## Output Format

### Raw Output
```python
result = crew.kickoff()
print(result.raw)  # Raw text output
```

### JSON Output
```python
result = crew.kickoff()
print(result.json_dict)  # Dictionary if output_pydantic used
```

### Token Usage
```python
result = crew.kickoff()
print(result.token_usage)  # Total token usage
```
