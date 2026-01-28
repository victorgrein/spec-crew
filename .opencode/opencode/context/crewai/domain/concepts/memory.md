# CrewAI Memory

> Source: Official CrewAI Documentation

## Overview

CrewAI provides a sophisticated memory system that enables agents to store, recall, and leverage information across interactions. This system enhances decision-making and task execution.

## Memory Types

### Short-Term Memory

Stores information from the current session/execution:
- Recent conversation context
- Current task outputs
- Temporary working data

### Long-Term Memory

Persists information across sessions:
- Historical interactions
- Learned patterns
- Accumulated knowledge

### Entity Memory

Tracks information about specific entities:
- People, organizations, concepts
- Relationships between entities
- Entity-specific context

## Enabling Memory

### Agent-Level

```python
from crewai import Agent

agent = Agent(
    role="Research Analyst",
    goal="Research and remember findings",
    backstory="Expert analyst with excellent memory",
    memory=True  # Enable memory
)
```

### Crew-Level

```python
from crewai import Crew

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    memory=True  # Enable for all agents
)
```

## Embedder Configuration

Memory uses embeddings for semantic search:

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

### Supported Providers

| Provider | Configuration |
|----------|---------------|
| OpenAI | `{"provider": "openai"}` |
| Cohere | `{"provider": "cohere"}` |
| HuggingFace | `{"provider": "huggingface"}` |
| Custom | `{"provider": "custom", "config": {...}}` |

## Use Cases

### Research Tasks

Memory helps agents build on previous research:

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

### Customer Support

Remember customer history and preferences:

```python
support_agent = Agent(
    role="Customer Support",
    goal="Provide personalized support",
    backstory="Support agent who remembers customer interactions",
    memory=True
)
```

### Complex Analysis

Maintain context across multi-step analysis:

```python
analyst = Agent(
    role="Data Analyst",
    goal="Perform deep analysis with context",
    backstory="Analyst who tracks patterns over time",
    memory=True,
    respect_context_window=True  # Auto-summarize if needed
)
```

## Memory with Knowledge Sources

Combine memory with external knowledge:

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

## Best Practices

1. **Enable for Complex Tasks**: Use memory for multi-step or iterative tasks
2. **Combine with Context Window Management**: Use `respect_context_window=True`
3. **Configure Embedder**: Choose appropriate embedding model for your use case
4. **Monitor Memory Usage**: Memory increases token usage
5. **Clear When Needed**: Start fresh sessions when context should be reset

## Limitations

- Memory increases token consumption
- Long-term memory requires persistent storage
- Entity extraction may not be perfect
- Memory retrieval adds latency

## Example: Memory-Enabled Crew

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
