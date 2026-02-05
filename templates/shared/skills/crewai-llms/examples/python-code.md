# CrewAI Llms - Python Code Examples

Python examples and implementation snippets for `crewai-llms`.

## Extracted Python Snippets

### Python Example 1

```python
agent = Agent(
    role="...",
    llm="gpt-4o",  # Main LLM for reasoning
    function_calling_llm="gpt-4o-mini"  # Cheaper LLM for tool calls
)
```

### Python Example 2

```python
crew = Crew(
    agents=[...],
    tasks=[...],
    function_calling_llm="gpt-4o-mini"  # Applies to all agents
)
```

### Python Example 3

```python
# Manager with best model
manager = Agent(
    role="Project Manager",
    llm="gpt-4o",
    allow_delegation=True
)

# Workers with cheaper models
researcher = Agent(
    role="Researcher",
    llm="gpt-4o-mini",
    function_calling_llm="gpt-3.5-turbo"
)
```

### Python Example 4

```python
agent = Agent(
    role="...",
    llm="gpt-4o",  # For reasoning
    function_calling_llm="gpt-4o-mini"  # For tool calls (cheaper)
)
```

### Python Example 5

```python
agent = Agent(
    role="...",
    cache=True  # Default: True
)
```

### Python Example 6

```python
agent = Agent(
    role="...",
    max_rpm=30  # Max 30 requests per minute
)
```

### Python Example 7

```python
crew = Crew(
    agents=[...],
    max_rpm=60  # Shared limit for all agents
)
```

### Python Example 8

```python
agent = Agent(
    role="...",
    respect_context_window=True  # Auto-summarize when exceeded
)
```

### Python Example 9

```python
agent = Agent(
    role="...",
    respect_context_window=False  # Error on context limit
)
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

### Python Example 13

```python
from crewai import Agent

# Using model name string
agent = Agent(
    role="Researcher",
    goal="Research topics",
    backstory="Expert researcher",
    llm="gpt-4o"  # or "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"
)
```

### Python Example 14

```python
agent = Agent(
    role="Analyst",
    goal="Analyze data",
    backstory="Expert analyst",
    llm="claude-3-5-sonnet"  # or "claude-3-opus", "claude-3-sonnet", "claude-3-haiku"
)
```
