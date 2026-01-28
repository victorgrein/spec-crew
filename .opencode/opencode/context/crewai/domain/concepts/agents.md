# CrewAI Agents

> Source: Official CrewAI Documentation

## Overview

An Agent in CrewAI is an autonomous unit that can:
- Perform specific tasks
- Make decisions based on its role and goal
- Use tools to accomplish objectives
- Communicate and collaborate with other agents
- Maintain memory of interactions
- Delegate tasks when allowed

## Agent Attributes

### Essential Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `role` | `str` | Defines the agent's function and expertise |
| `goal` | `str` | Individual objective guiding decision-making |
| `backstory` | `str` | Provides context and personality |

### LLM Configuration

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `llm` | `Union[str, LLM, Any]` | `gpt-4` | Language model powering the agent |
| `function_calling_llm` | `Optional[Any]` | None | Separate LLM for tool calling |
| `step_callback` | `Optional[Any]` | None | Function called after each step |
| `knowledge_sources` | `Optional[List[Any]]` | None | Domain knowledge sources |
| `embedder` | `Optional[Dict]` | None | Embedder configuration |
| `use_system_prompt` | `Optional[bool]` | True | Use system prompt (for o1 models) |

### Behavior Settings

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `verbose` | `bool` | False | Enable detailed logging |
| `allow_delegation` | `bool` | False | Allow delegating to other agents |
| `max_iter` | `int` | 20 | Max iterations before best answer |
| `max_rpm` | `Optional[int]` | None | Rate limit for API calls |
| `max_execution_time` | `Optional[int]` | None | Timeout in seconds |
| `max_retry_limit` | `int` | 2 | Retries on error |

### Advanced Features

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `memory` | `bool` | False | Maintain conversation history |
| `cache` | `bool` | True | Cache tool results |
| `reasoning` | `bool` | False | Enable planning before execution |
| `max_reasoning_attempts` | `Optional[int]` | None | Limit planning iterations |
| `multimodal` | `bool` | False | Process text and images |
| `allow_code_execution` | `bool` | False | Enable code execution |
| `code_execution_mode` | `Literal["safe", "unsafe"]` | "safe" | Docker or direct execution |
| `respect_context_window` | `bool` | True | Auto-summarize if context exceeded |
| `inject_date` | `bool` | False | Inject current date into tasks |
| `date_format` | `str` | "%Y-%m-%d" | Date format string |

### Templates

| Attribute | Type | Description |
|-----------|------|-------------|
| `system_template` | `Optional[str]` | Custom system prompt |
| `prompt_template` | `Optional[str]` | Custom input format |
| `response_template` | `Optional[str]` | Custom output format |

## Creating Agents

### YAML Configuration (Recommended)

```yaml
# config/agents.yaml
researcher:
  role: >
    {topic} Senior Data Researcher
  goal: >
    Uncover cutting-edge developments in {topic}
  backstory: >
    You're a seasoned researcher with a knack for uncovering the latest
    developments in {topic}. Known for your ability to find the most relevant
    information and present it in a clear and concise manner.
```

```python
@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config['researcher'],
        tools=[SerperDevTool()],
        verbose=True
    )
```

### Direct Code Definition

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

## Agent Archetypes

### Research Agent

```python
researcher = Agent(
    role="Research Analyst",
    goal="Find and summarize information about specific topics",
    backstory="Experienced researcher with attention to detail",
    tools=[SerperDevTool()],
    verbose=True
)
```

### Code Development Agent

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

### Analysis Agent

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

### Reasoning Agent

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

## Direct Agent Interaction

Use `kickoff()` for direct agent interaction without crew:

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

## Context Window Management

### Auto-Summarization (Default)

```python
agent = Agent(
    role="...",
    respect_context_window=True  # Auto-summarize when exceeded
)
```

### Strict Mode

```python
agent = Agent(
    role="...",
    respect_context_window=False  # Error on context limit
)
```

## Best Practices

1. **Role Design**: Be specific about expertise area and seniority
2. **Goal Design**: Focus on outcomes, be measurable
3. **Backstory Design**: Provide relevant context, keep concise (2-4 sentences)
4. **Tool Assignment**: Match tools to agent's purpose
5. **Memory**: Enable for complex, multi-step tasks
6. **Rate Limiting**: Set `max_rpm` to avoid API limits
7. **Caching**: Keep enabled for repetitive operations
