# CrewAI Debugging Process

## Overview

Systematic approach to debugging CrewAI crews and flows.

## Debugging Workflow

### Step 1: Gather Information

**Collect:**
- Error message or unexpected behavior description
- Trace ID (if available)
- Recent code changes
- Input data used

**Enable verbose logging:**
```python
agent = Agent(role="...", verbose=True)
crew = Crew(agents=[...], verbose=True)
```

**Enable file logging:**
```python
crew = Crew(
    agents=[...],
    output_log_file="debug_logs.json"
)
```

### Step 2: Reproduce the Issue

**Isolate the problem:**
- Use minimal inputs
- Test individual agents with `agent.kickoff()`
- Run single tasks if possible

**Check consistency:**
- Is the issue reproducible?
- Does it happen with different inputs?
- Is it intermittent or consistent?

### Step 3: Analyze Traces

**View task outputs:**
```bash
crewai log-tasks-outputs
```

**Check token usage:**
```python
result = crew.kickoff()
print(crew.usage_metrics)
```

**Examine execution flow:**
- Which agent/task failed?
- What was the last successful output?
- Where did execution diverge from expected?

### Step 4: Identify Root Cause

**Common categories:**

| Category | Symptoms | Check |
|----------|----------|-------|
| Rate Limits | 429 errors, intermittent failures | max_rpm settings |
| Context Window | Truncated output, lost context | respect_context_window |
| Tool Errors | Tool not found, wrong arguments | Tool assignment, descriptions |
| Agent Loops | max_iter reached, repeated actions | Task clarity, delegation |
| Output Parsing | Pydantic errors, JSON failures | Output format, model |

### Step 5: Apply Fix

**Test the fix:**
- Use same inputs that caused the issue
- Verify expected behavior
- Check for side effects

**Document the fix:**
- What was the root cause?
- What change resolved it?
- How to prevent in future?

## Common Issues and Solutions

### Rate Limit Errors

**Symptoms:**
- "Rate limit exceeded" errors
- 429 HTTP status codes

**Solution:**
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

### Context Window Exceeded

**Symptoms:**
- "Context length exceeded" errors
- Agent losing context

**Solution:**
```python
agent = Agent(
    role="...",
    respect_context_window=True  # Auto-summarize
)

# Or use RAG for large documents
from crewai_tools import RagTool
agent = Agent(tools=[RagTool()])
```

### Tool Not Working

**Symptoms:**
- Tool not being used
- Wrong tool selected
- Tool errors

**Solution:**
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

### Agent Stuck in Loop

**Symptoms:**
- max_iter reached
- Repeated similar outputs

**Solution:**
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

### Output Parsing Errors

**Symptoms:**
- Pydantic validation errors
- JSON parsing failures

**Solution:**
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

### Async Errors

**Symptoms:**
- "Event loop already running"
- Deadlocks

**Solution:**
```python
import asyncio

async def main():
    result = await crew.akickoff(inputs={...})
    return result

asyncio.run(main())
```

## Debugging Commands

```bash
# View task outputs
crewai log-tasks-outputs

# Replay from specific task
crewai replay -t <task_id>
```

## Debugging Checklist

- [ ] Verbose mode enabled
- [ ] Logs being captured
- [ ] Issue reproducible
- [ ] Root cause identified
- [ ] Fix tested
- [ ] Preventive measures added
