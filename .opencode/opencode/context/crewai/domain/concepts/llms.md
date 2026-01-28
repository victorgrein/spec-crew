# CrewAI LLMs

> Source: Official CrewAI Documentation

## Overview

Large Language Models (LLMs) are the core intelligence behind CrewAI agents. They enable agents to understand context, make decisions, and generate human-like responses.

## Supported Providers

### OpenAI

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

**Available Models:**
| Model | Context Window | Best For |
|-------|---------------|----------|
| `gpt-4o` | 128K | Complex reasoning, multimodal |
| `gpt-4o-mini` | 128K | Fast, cost-effective, function calling |
| `gpt-4-turbo` | 128K | Strong reasoning, long documents |
| `gpt-3.5-turbo` | 16K | Simple tasks, prototyping |

### Anthropic

```python
agent = Agent(
    role="Analyst",
    goal="Analyze data",
    backstory="Expert analyst",
    llm="claude-3-5-sonnet"  # or "claude-3-opus", "claude-3-sonnet", "claude-3-haiku"
)
```

**Available Models:**
| Model | Context Window | Best For |
|-------|---------------|----------|
| `claude-3-5-sonnet` | 200K | Excellent reasoning, coding |
| `claude-3-opus` | 200K | Highest quality, best reasoning |
| `claude-3-sonnet` | 200K | Good balance of quality/speed |
| `claude-3-haiku` | 200K | Fast, cost-effective |

## Configuration

### Environment Variables

```bash
# OpenAI
export OPENAI_API_KEY="your-api-key"
export OPENAI_MODEL_NAME="gpt-4o"  # Default model

# Anthropic
export ANTHROPIC_API_KEY="your-api-key"
```

### Agent-Level Configuration

```python
agent = Agent(
    role="...",
    llm="gpt-4o",  # Main LLM for reasoning
    function_calling_llm="gpt-4o-mini"  # Cheaper LLM for tool calls
)
```

### Crew-Level Configuration

```python
crew = Crew(
    agents=[...],
    tasks=[...],
    function_calling_llm="gpt-4o-mini"  # Applies to all agents
)
```

## Cost Optimization Strategies

### 1. Tiered Model Strategy

Use expensive models for reasoning, cheap models for tools:

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

### 2. Function Calling LLM

Separate LLM for tool calls reduces costs:

```python
agent = Agent(
    role="...",
    llm="gpt-4o",  # For reasoning
    function_calling_llm="gpt-4o-mini"  # For tool calls (cheaper)
)
```

### 3. Caching

Enable caching to avoid redundant API calls:

```python
agent = Agent(
    role="...",
    cache=True  # Default: True
)
```

## Rate Limiting

### Agent-Level

```python
agent = Agent(
    role="...",
    max_rpm=30  # Max 30 requests per minute
)
```

### Crew-Level (Overrides Agent Settings)

```python
crew = Crew(
    agents=[...],
    max_rpm=60  # Shared limit for all agents
)
```

## Context Window Management

### Auto-Summarization (Default)

```python
agent = Agent(
    role="...",
    respect_context_window=True  # Auto-summarize when exceeded
)
```

When context exceeds limit:
- Warning: "Context length exceeded. Summarizing content..."
- Automatic summarization of conversation history
- Execution continues with summarized context

### Strict Mode

```python
agent = Agent(
    role="...",
    respect_context_window=False  # Error on context limit
)
```

When context exceeds limit:
- Error: "Context length exceeded. Consider using smaller text or RAG tools."
- Execution stops

## Model Selection Guide

### By Use Case

| Use Case | Recommended Model | Reason |
|----------|-------------------|--------|
| Complex reasoning | `gpt-4o`, `claude-3-5-sonnet` | Best quality |
| Code generation | `claude-3-5-sonnet`, `gpt-4o` | Strong coding |
| Simple tasks | `gpt-4o-mini`, `claude-3-haiku` | Fast, cheap |
| Function calling | `gpt-4o-mini`, `gpt-3.5-turbo` | Cost-effective |
| Long documents | `claude-3-5-sonnet` (200K) | Largest context |
| Multimodal | `gpt-4o` | Vision support |

### By Optimization Target

**Cost Optimization:**
```python
agent = Agent(
    llm="gpt-4o-mini",
    function_calling_llm="gpt-3.5-turbo",
    cache=True,
    max_iter=15
)
```

**Quality Optimization:**
```python
agent = Agent(
    llm="gpt-4o",
    reasoning=True,
    max_iter=25,
    memory=True
)
```

**Latency Optimization:**
```python
agent = Agent(
    llm="gpt-4o-mini",
    cache=True,
    max_iter=10,
    max_execution_time=60
)
```

## Approximate Costs (per 1K tokens)

| Model | Input | Output |
|-------|-------|--------|
| gpt-4o | $0.005 | $0.015 |
| gpt-4o-mini | $0.00015 | $0.0006 |
| gpt-3.5-turbo | $0.0005 | $0.0015 |
| claude-3-5-sonnet | $0.003 | $0.015 |
| claude-3-opus | $0.015 | $0.075 |
| claude-3-haiku | $0.00025 | $0.00125 |

*Prices subject to change. Check provider documentation for current pricing.*

## Best Practices

1. **Start with cheaper models** and upgrade only if needed
2. **Use function_calling_llm** for cost savings on tool calls
3. **Enable caching** to reduce redundant API calls
4. **Set max_rpm** to avoid rate limit errors
5. **Monitor usage_metrics** to track token consumption
6. **Use respect_context_window=True** for long conversations
7. **Match model to task complexity** - don't use GPT-4 for simple tasks
