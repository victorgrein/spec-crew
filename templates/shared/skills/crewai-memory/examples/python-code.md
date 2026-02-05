# CrewAI Memory - Python Code Examples

Python examples and implementation snippets for `crewai-memory`.

## Extracted Python Snippets

### Python Example 1

```python
from crewai import Agent

agent = Agent(
    role="Research Analyst",
    goal="Research and remember findings",
    backstory="Expert analyst with excellent memory",
    memory=True  # Enable memory
)
```

### Python Example 2

```python
from crewai import Crew

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    memory=True  # Enable for all agents
)
```

### Python Example 3

```python
crew = Crew(
    agents=[...],
    tasks=[...],
    memory=True,
    embedder={
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small"
        }
    }
)
```

### Python Example 4

```python
researcher = Agent(
    role="Research Analyst",
    goal="Build comprehensive knowledge over time",
    backstory="Researcher who remembers all findings",
    memory=True,
    verbose=True
)

# First execution - learns about topic
crew.kickoff(inputs={"topic": "AI trends"})

# Second execution - builds on previous knowledge
crew.kickoff(inputs={"topic": "AI applications"})
```

### Python Example 5

```python
support_agent = Agent(
    role="Customer Support",
    goal="Provide personalized support",
    backstory="Support agent who remembers customer interactions",
    memory=True
)
```

### Python Example 6

```python
analyst = Agent(
    role="Data Analyst",
    goal="Perform deep analysis with context",
    backstory="Analyst who tracks patterns over time",
    memory=True,
    respect_context_window=True  # Auto-summarize if needed
)
```

### Python Example 7

```python
from crewai import Agent
from crewai.knowledge.source import TextKnowledgeSource

knowledge = TextKnowledgeSource(
    content="Domain-specific knowledge...",
    metadata={"topic": "AI"}
)

agent = Agent(
    role="Expert",
    goal="Apply knowledge and remember interactions",
    backstory="Expert with deep knowledge",
    memory=True,
    knowledge_sources=[knowledge]
)
```

### Python Example 8

```python
from crewai import Agent, Crew, Task

# Memory-enabled agents
researcher = Agent(
    role="Researcher",
    goal="Research and remember findings",
    backstory="Expert researcher",
    memory=True,
    verbose=True
)

analyst = Agent(
    role="Analyst",
    goal="Analyze with historical context",
    backstory="Analyst who tracks patterns",
    memory=True
)

# Tasks
research_task = Task(
    description="Research {topic}",
    expected_output="Research findings",
    agent=researcher
)

analysis_task = Task(
    description="Analyze findings with historical context",
    expected_output="Analysis with trends",
    agent=analyst,
    context=[research_task]
)

# Memory-enabled crew
crew = Crew(
    agents=[researcher, analyst],
    tasks=[research_task, analysis_task],
    memory=True,
    embedder={"provider": "openai"}
)

# Execute - agents will remember across calls
result = crew.kickoff(inputs={"topic": "AI trends 2024"})
```
