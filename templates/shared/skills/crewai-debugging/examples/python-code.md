# CrewAI Debugging - Python Code Examples

Python examples and implementation snippets for `crewai-debugging`.

## Extracted Python Snippets

### Python Example 1

```python
agent = Agent(role="...", verbose=True)
crew = Crew(agents=[...], verbose=True)
```

### Python Example 2

```python
crew = Crew(
    agents=[...],
    output_log_file="debug_logs.json"
)
```

### Python Example 3

```python
result = crew.kickoff()
print(crew.usage_metrics)
```

### Python Example 4

```python
agent = Agent(
    role="...",
    max_rpm=30  # Limit requests per minute
)

# Or at crew level
crew = Crew(
    agents=[...],
    max_rpm=60
)
```

### Python Example 5

```python
agent = Agent(
    role="...",
    respect_context_window=True  # Auto-summarize
)

# Or use RAG for large documents
from crewai_tools import RagTool
agent = Agent(tools=[RagTool()])
```

### Python Example 6

```python
# Ensure tool is instantiated and assigned
agent = Agent(
    role="...",
    tools=[MyTool()]  # Not MyTool (class)
)

# Improve tool description
class MyTool(BaseTool):
    description = """
    Use this tool when you need to [specific use case].
    Input: [describe expected input]
    Output: [describe expected output]
    """
```

### Python Example 7

```python
# Reduce iterations
agent = Agent(
    role="...",
    max_iter=15,
    allow_delegation=False  # Prevent delegation loops
)

# Clarify task
task = Task(
    description="[Specific, actionable description]",
    expected_output="[Clear, measurable output]"
)
```

### Python Example 8

```python
# Make model more flexible
from typing import Optional

class OutputModel(BaseModel):
    required_field: str
    optional_field: Optional[str] = None

# Improve expected_output
task = Task(
    expected_output="""
    Return a JSON object with:
    - required_field: string (required)
    - optional_field: string (optional)
    """,
    output_pydantic=OutputModel
)
```

### Python Example 9

```python
import asyncio

async def main():
    result = await crew.akickoff(inputs={...})
    return result

asyncio.run(main())
```

### Python Example 10

```python
# Agent-level
agent = Agent(role="...", verbose=True)

# Crew-level
crew = Crew(agents=[...], verbose=True)

# File logging
crew = Crew(
    agents=[...],
    output_log_file="debug_logs.json"
)
```

### Python Example 11

```python
result = crew.kickoff()
print(crew.usage_metrics)

# Per-task analysis
for task_output in result.tasks_output:
    print(f"Task: {task_output.description[:50]}")
    print(f"Tokens: {task_output.token_usage}")
```
