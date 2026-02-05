# CrewAI Agents - Python Code Examples

Python examples and implementation snippets for `crewai-agents`.

## Extracted Python Snippets

### Python Example 1

```python
@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config['researcher'],
        tools=[SerperDevTool()],
        verbose=True
    )
```

### Python Example 2

```python
researcher = Agent(
    role="Research Analyst",
    goal="Find and summarize information about specific topics",
    backstory="Experienced researcher with attention to detail",
    tools=[SerperDevTool()],
    verbose=True
)
```

### Python Example 3

```python
developer = Agent(
    role="Senior Python Developer",
    goal="Write and debug Python code",
    backstory="Expert Python developer with 10 years of experience",
    allow_code_execution=True,
    code_execution_mode="safe",
    max_execution_time=300,
    max_retry_limit=3
)
```

### Python Example 4

```python
analyst = Agent(
    role="Data Analyst",
    goal="Perform deep analysis of large datasets",
    backstory="Specialized in big data analysis",
    memory=True,
    respect_context_window=True,
    max_rpm=10,
    function_calling_llm="gpt-4o-mini"
)
```

### Python Example 5

```python
strategic_agent = Agent(
    role="Strategic Planner",
    goal="Analyze complex problems and create execution plans",
    backstory="Expert strategic planner",
    reasoning=True,
    max_reasoning_attempts=3,
    max_iter=30,
    verbose=True
)
```

### Python Example 6

```python
result = agent.kickoff("What are the latest developments in AI?")
print(result.raw)

# With structured output
class ResearchFindings(BaseModel):
    main_points: List[str]
    key_technologies: List[str]

result = agent.kickoff(
    "Summarize AI developments",
    response_format=ResearchFindings
)
print(result.pydantic.main_points)

# Async
result = await agent.kickoff_async("Query here")
```

### Python Example 7

```python
agent = Agent(
    role="...",
    respect_context_window=True  # Auto-summarize when exceeded
)
```

### Python Example 8

```python
agent = Agent(
    role="...",
    respect_context_window=False  # Error on context limit
)
```

### Python Example 9

```python
from crewai import Agent
from crewai_tools import SerperDevTool

agent = Agent(
    role="Senior Data Scientist",
    goal="Analyze and interpret complex datasets",
    backstory="With over 10 years of experience in data science...",
    llm="gpt-4o",
    tools=[SerperDevTool()],
    verbose=True,
    memory=True
)
```

### Python Example 10

```python
# Pass variables when running
crew.kickoff(inputs={"topic": "AI trends"})
```
